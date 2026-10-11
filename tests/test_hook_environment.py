"""Compare original-hook policy and environment with native Git."""

import json
import shlex
import subprocess
import sys
from pathlib import Path

import pytest

from codexspec.commit_runtime import AutomationError, commit_snapshot, snapshot
from tests.automation_test_support import git, make_repo, sanitized_git_env

ROOT = Path(__file__).resolve().parents[1]


def diverged_repo(tmp_path):
    repo = make_repo(tmp_path / "repo")
    git(repo, "switch", "-c", "topic")
    (repo / "sample.txt").write_text("FORBIDDEN text\n")
    git(repo, "add", "sample.txt")
    git(repo, "commit", "-m", "topic")
    target = git(repo, "rev-parse", "HEAD").stdout.strip()
    git(repo, "switch", "main")
    (repo / "main.md").write_text("main\n")
    git(repo, "add", "main.md")
    git(repo, "commit", "-m", "main")
    return repo, target


@pytest.mark.parametrize("mode", ["direct", "standalone", "merge"])
@pytest.mark.parametrize("phase", ["pre-commit", "prepare-commit-msg", "commit-msg"])
@pytest.mark.parametrize("deny", [False, True])
def test_hook_glob_policy_matches_native_git(tmp_path, monkeypatch, mode, phase, deny):
    for name in ["GIT_LITERAL_PATHSPECS", "GIT_GLOB_PATHSPECS", "GIT_NOGLOB_PATHSPECS", "GIT_ICASE_PATHSPECS"]:
        monkeypatch.delenv(name, raising=False)
    if mode == "merge":
        repo, target = diverged_repo(tmp_path)
    else:
        repo = make_repo(tmp_path / "repo")
        (repo / "sample.txt").write_text("FORBIDDEN text\n")
        git(repo, "add", "sample.txt")
    before = git(repo, "rev-parse", "HEAD").stdout.strip()
    hook_name = "pre-merge-commit" if mode == "merge" and phase == "pre-commit" else phase
    hook = repo / ".git/hooks" / hook_name
    policy = (
        'if git diff --cached -- "*.txt" | grep -q FORBIDDEN; then echo policy-denied >&2; exit 1; fi\n'
        if deny
        else 'git add -- "*.txt"\n'
    )
    hook.write_text("#!/bin/sh\n" + policy)
    hook.chmod(0o755)
    native = git(
        repo, *(["merge", "--no-edit", target] if mode == "merge" else ["commit", "-m", "feat: text"]), check=False
    )
    assert (native.returncode != 0) == deny, native.stderr
    if mode == "merge":
        if deny:
            git(repo, "merge", "--abort")
        else:
            git(repo, "reset", "--hard", before)
        git(repo, "merge", "--no-commit", target)
    elif not deny:
        git(repo, "reset", "--soft", before)
    analyzed = snapshot(repo)
    if mode == "standalone":
        result = subprocess.run(
            [sys.executable, "-I", "-S", str(ROOT / "src/codexspec/commit_runtime.py"), "commit"],
            cwd=repo,
            env=sanitized_git_env(),
            text=True,
            capture_output=True,
            check=False,
            input=json.dumps({"analysis": analyzed, "message": "feat: text"}),
        )
        assert (result.returncode != 0) == deny, result.stderr
        if deny:
            assert "policy-denied" in result.stderr
    elif deny:
        with pytest.raises(AutomationError, match="policy-denied"):
            commit_snapshot(repo, analyzed, "feat: text", merge_hook=mode == "merge")
    else:
        commit_snapshot(repo, analyzed, "feat: text", merge_hook=mode == "merge")
    if deny:
        assert git(repo, "rev-parse", "HEAD").stdout.strip() == before
        assert snapshot(repo) == analyzed
    else:
        assert git(repo, "rev-parse", "HEAD^{tree}").stdout.strip() == analyzed["tree"]


@pytest.mark.parametrize("explicit_author", [False, True])
def test_automatic_merge_hook_environment_matches_native_git(tmp_path, monkeypatch, explicit_author):
    repo, target = diverged_repo(tmp_path)
    foreign = make_repo(tmp_path / "foreign")
    git(foreign, "config", "user.name", "Foreign Author")
    for name, value in {
        "GIT_AUTHOR_NAME": "Caller Author",
        "GIT_AUTHOR_EMAIL": "caller@example.invalid",
        "GIT_AUTHOR_DATE": "2001-02-03T04:05:06+00:00",
    }.items():
        if explicit_author:
            monkeypatch.setenv(name, value)
        else:
            monkeypatch.delenv(name, raising=False)
    monkeypatch.delenv("GIT_LITERAL_PATHSPECS", raising=False)
    before = git(repo, "rev-parse", "HEAD").stdout.strip()
    events = tmp_path / "events.jsonl"
    dump = tmp_path / "dump.py"
    dump.write_text(
        "import json,os,subprocess,sys\nfrom pathlib import Path\n"
        'env={k:v for k,v in os.environ.items() if k.startswith("GIT_")}\n'
        'env.pop("GIT_CONFIG_PARAMETERS",None)\n'
        'if "GIT_INDEX_FILE" in env: env["GIT_INDEX_FILE"]=str(Path(env["GIT_INDEX_FILE"]).resolve())\n'
        "foreign_env=os.environ.copy()\n"
        'for name in subprocess.check_output(["git","rev-parse","--local-env-vars"],text=True).split():'
        " foreign_env.pop(name,None)\n"
        'author=subprocess.check_output(["git","-C",sys.argv[3],"var","GIT_AUTHOR_IDENT"],env=foreign_env,text=True).split(">",1)[0]+">"\n'
        'with open(sys.argv[2],"a",encoding="utf-8") as out: out.write(json.dumps([sys.argv[1],env,author])+"\\n")\n'
    )
    phases = ["pre-merge-commit", "prepare-commit-msg", "commit-msg", "reference-transaction", "post-merge"]
    for phase in phases:
        hook = repo / ".git/hooks" / phase
        hook.write_text(
            "#!/bin/sh\nexec "
            + shlex.join([sys.executable, "-I", "-S", str(dump), phase, str(events), str(foreign)])
            + "\n"
        )
        hook.chmod(0o755)
    git(repo, "merge", "--no-edit", target)
    native = {row[0]: row[1:] for row in map(json.loads, events.read_text().splitlines())}
    git(repo, "reset", "--hard", before)
    git(repo, "merge", "--no-commit", target)
    events.unlink()
    commit_snapshot(repo, snapshot(repo), "chore: integrate topic", merge_hook=True)
    guarded = {row[0]: row[1:] for row in map(json.loads, events.read_text().splitlines())}
    assert set(native) == set(guarded) == set(phases)
    for phase in phases:
        assert guarded[phase] == native[phase], phase
        assert guarded[phase][1].startswith("Caller Author <" if explicit_author else "Foreign Author <")


def configuration_environment(mechanism, values):
    env = sanitized_git_env()
    if mechanism == "count":
        env["GIT_CONFIG_COUNT"] = str(len(values))
        for i, (key, value) in enumerate(values.items()):
            env[f"GIT_CONFIG_KEY_{i}"] = key
            env[f"GIT_CONFIG_VALUE_{i}"] = value
    else:
        # Git's sq_dequote format requires every argument to be single-quoted.
        env["GIT_CONFIG_PARAMETERS"] = " ".join(
            "'" + f"{key}={value}".replace("'", "'\\''") + "'" for key, value in values.items()
        )
    return env


def invoke_configured_commit(repo, env, mode, monkeypatch):
    if mode == "standalone":
        helper = ROOT / ".codexspec/scripts/commit-staged-helper.py"
        command = [sys.executable, "-I", "-S", str(helper)]
        preview = subprocess.run(command + ["snapshot"], cwd=repo, env=env, text=True, capture_output=True, check=True)
        return subprocess.run(
            command + ["commit"],
            cwd=repo,
            env=env,
            text=True,
            capture_output=True,
            check=False,
            input=json.dumps({"analysis": json.loads(preview.stdout), "message": "feat: configured commit"}),
        )
    with monkeypatch.context() as patch:
        for name in ["GIT_CONFIG_COUNT", "GIT_CONFIG_PARAMETERS"]:
            patch.delenv(name, raising=False)
        for name, value in env.items():
            if name.startswith("GIT_CONFIG"):
                patch.setenv(name, value)
        try:
            commit_snapshot(repo, snapshot(repo), "feat: configured commit")
        except AutomationError as error:
            return subprocess.CompletedProcess([], 1, "", str(error))
        return subprocess.CompletedProcess([], 0, "", "")


@pytest.mark.parametrize("mechanism", ["count", "parameters"])
@pytest.mark.parametrize("mode", ["direct", "standalone"])
@pytest.mark.parametrize("phase", ["pre-commit", "prepare-commit-msg", "commit-msg"])
@pytest.mark.parametrize("deny", [False, True])
def test_current_repository_hook_configuration_is_preserved(tmp_path, monkeypatch, mechanism, mode, phase, deny):
    repo = make_repo(tmp_path / "repo")
    (repo / "README.md").write_text("changed\n")
    git(repo, "add", "README.md")
    before = git(repo, "rev-parse", "HEAD").stdout.strip()
    tree = git(repo, "write-tree").stdout.strip()
    hooks = tmp_path / "policy hooks 'quoted'"
    hooks.mkdir()
    marker = tmp_path / "hook-ran"
    hook = hooks / phase
    hook.write_text(
        "#!/bin/sh\nprintf ran >> " + shlex.quote(str(marker)) + "\n"
        "policy=$(git config codexspec.policy) || exit 2\n"
        'if [ "$policy" = deny ]; then echo configured-policy-denied >&2; exit 1; fi\n'
        '[ "$policy" = allow ]\n'
    )
    hook.chmod(0o755)
    env = configuration_environment(
        mechanism, {"core.hooksPath": str(hooks), "codexspec.policy": "deny" if deny else "allow"}
    )
    native = subprocess.run(
        ["git", "-C", str(repo), "commit", "-m", "feat: configured commit"],
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )
    assert (native.returncode != 0) == deny, native.stderr
    assert marker.read_text() == "ran"
    marker.unlink()
    if not deny:
        git(repo, "reset", "--soft", before)
    result = invoke_configured_commit(repo, env, mode, monkeypatch)
    assert (result.returncode != 0) == deny, result.stderr
    assert marker.read_text() == "ran"
    if deny:
        assert "configured-policy-denied" in result.stderr
        assert git(repo, "rev-parse", "HEAD").stdout.strip() == before
        assert git(repo, "write-tree").stdout.strip() == tree
    else:
        assert git(repo, "show", "HEAD:README.md").stdout == "changed\n"


@pytest.mark.parametrize("mechanism", ["count", "parameters"])
@pytest.mark.parametrize("mode", ["direct", "standalone"])
def test_current_repository_signing_configuration_is_preserved(tmp_path, monkeypatch, mechanism, mode):
    repo = make_repo(tmp_path / "repo")
    (repo / "README.md").write_text("changed\n")
    git(repo, "add", "README.md")
    before = git(repo, "rev-parse", "HEAD").stdout.strip()
    signer = tmp_path / "signer"
    marker = tmp_path / "signer-ran"
    signer.write_text("#!/bin/sh\nprintf ran > " + shlex.quote(str(marker)) + "\nexit 1\n")
    signer.chmod(0o755)
    env = configuration_environment(mechanism, {"commit.gpgsign": "true", "gpg.program": str(signer)})
    native = subprocess.run(
        ["git", "-C", str(repo), "commit", "-m", "feat: signed"], env=env, text=True, capture_output=True, check=False
    )
    assert native.returncode != 0 and "failed to sign" in native.stderr
    assert marker.read_text() == "ran"
    marker.unlink()
    result = invoke_configured_commit(repo, env, mode, monkeypatch)
    assert result.returncode != 0 and "failed to sign" in result.stderr
    assert marker.read_text() == "ran"
    assert git(repo, "rev-parse", "HEAD").stdout.strip() == before


@pytest.mark.parametrize("mechanism", ["count", "parameters"])
def test_foreign_repository_runner_still_clears_caller_configuration(tmp_path, monkeypatch, mechanism):
    from codexspec.commit_runtime import GitRunner

    repo = make_repo(tmp_path / "repo")
    env = configuration_environment(mechanism, {"core.bare": "true"})
    for name, value in env.items():
        if name.startswith("GIT_CONFIG"):
            monkeypatch.setenv(name, value)
    assert GitRunner().run(repo, "rev-parse", "--is-bare-repository").stdout.strip() == "false"
