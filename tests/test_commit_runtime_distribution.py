"""Installed commit guards run without the CodexSpec package or CLI."""

import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
from typer.testing import CliRunner

from codexspec import app
from codexspec.automation import GitRunner
from tests.automation_test_support import git, make_repo

ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize("installation", ["claude", "codex", "plugin"])
def test_cli_free_snapshot_commit_and_hooks(tmp_path, installation):
    repo = make_repo(tmp_path / "project")
    if installation == "plugin":
        # Exercise the next release's repository-root bundle. Marketplace metadata
        # retains the preceding release's layout until the new tag is published.
        source = ROOT
        commands = Path(".claude/commands/codexspec")
        plugin = tmp_path / "plugin cache with spaces"
        shutil.copytree(source / commands, plugin / commands)
        command = (plugin / commands / "commit-staged.md").read_text(encoding="utf-8")
        (runtime_path,) = re.findall(r"\$\{CLAUDE_PLUGIN_ROOT\}/([^`]*commit-staged-helper\.py)", command)
        helper = plugin / runtime_path
    else:
        result = CliRunner().invoke(app, ["init", str(repo), "--force", "--ai", installation, "--lang", "en"])
        assert result.exit_code == 0, result.output
        helper = repo / ".codexspec/scripts/commit-staged-helper.py"
    assert helper.is_file(), "installation must retain the standalone commit runtime"
    assert helper.read_bytes() == (ROOT / "src/codexspec/commit_runtime.py").read_bytes()
    environment = GitRunner().environment()
    environment["PATH"] = os.pathsep.join([str(Path(shutil.which("git")).parent), os.defpath])
    assert shutil.which("codexspec", path=environment["PATH"]) is None

    def run(action, body=None):
        return subprocess.run(
            [sys.executable, "-I", "-S", str(helper), action],
            cwd=repo,
            env=environment,
            input=json.dumps(body) if body is not None else None,
            capture_output=True,
            text=True,
            check=False,
        )

    (repo / "README.md").write_text("staged\n")
    git(repo, "add", "README.md")
    (repo / "README.md").write_text("unstaged\n")
    before = git(repo, "rev-parse", "HEAD").stdout
    result = run("snapshot")
    assert result.returncode == 0, result.stderr
    analysis = json.loads(result.stdout)
    assert git(repo, "rev-parse", "HEAD").stdout == before
    hooks = repo / "hooks with spaces"
    hooks.mkdir()
    git(repo, "config", "core.hooksPath", str(hooks))
    hook = hooks / "pre-commit"
    hook.write_text("#!/bin/sh\necho original-hook >&2\nexit 1\n")
    hook.chmod(0o755)
    request = {"analysis": analysis, "message": "fix: retain staged content\n\nDetailed explanation.\n"}
    rejected = run("commit", request)
    assert rejected.returncode != 0
    assert "original-hook" in rejected.stderr
    assert git(repo, "rev-parse", "HEAD").stdout == before
    hook.write_text("#!/bin/sh\necho invoked > hook-ran\n")
    accepted = run("commit", request)
    assert accepted.returncode == 0, accepted.stderr
    assert json.loads(accepted.stdout)["state"] == "committed"
    assert git(repo, "show", "HEAD:README.md").stdout == "staged\n"
    assert git(repo, "log", "-1", "--format=%B").stdout.strip() == request["message"].strip()
    assert (repo / "README.md").read_text() == "unstaged\n"
    assert (repo / "hook-ran").is_file()


def test_standalone_helper_rejects_stale_analysis(tmp_path):
    repo = make_repo(tmp_path / "repo")
    helper = tmp_path / "guard.py"
    helper.write_bytes((ROOT / "src/codexspec/commit_runtime.py").read_bytes())
    (repo / "README.md").write_text("first\n")
    git(repo, "add", "README.md")
    command = [sys.executable, "-I", "-S", str(helper)]
    env = GitRunner().environment()
    result = subprocess.run([*command, "snapshot"], cwd=repo, env=env, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    analysis = json.loads(result.stdout)
    (repo / "README.md").write_text("second\n")
    git(repo, "add", "README.md")
    head = git(repo, "rev-parse", "HEAD").stdout
    result = subprocess.run(
        [*command, "commit"],
        cwd=repo,
        env=env,
        input=json.dumps({"analysis": analysis, "message": "fix: old analysis"}),
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0 and "stale_analysis" in result.stderr
    assert git(repo, "rev-parse", "HEAD").stdout == head


def test_tracked_runtime_copies_match():
    expected = (ROOT / "src/codexspec/commit_runtime.py").read_bytes()
    for directory in [".codexspec/scripts", ".claude/commands/codexspec"]:
        assert (ROOT / directory / "commit-staged-helper.py").read_bytes() == expected


def test_runtime_install_updates_and_rejects_shared_destination(tmp_path):
    from codexspec.commit_runtime import AutomationError, install_helper

    directory = tmp_path / "scripts"
    target = install_helper(directory)
    target.write_text("old runtime")
    install_helper(directory)
    assert target.read_bytes() == (ROOT / "src/codexspec/commit_runtime.py").read_bytes()
    outside = tmp_path / "caller-owned.py"
    outside.write_text("caller content")
    target.unlink()
    os.link(outside, target)
    with pytest.raises(AutomationError, match="shared_commit_helper"):
        install_helper(directory)
    assert outside.read_text() == "caller content"


@pytest.mark.parametrize(
    "body", [[], {"analysis": {}, "message": None}, {"analysis": {}}, {"analysis": [], "message": "fix: x"}]
)
def test_standalone_rejects_invalid_requests(tmp_path, body):
    result = subprocess.run(
        [sys.executable, "-I", "-S", str(ROOT / "src/codexspec/commit_runtime.py"), "commit"],
        cwd=tmp_path,
        input=json.dumps(body),
        capture_output=True,
        text=True,
    )
    assert result.returncode == 1
    assert "Traceback" not in result.stderr
    assert "analysis_required" in result.stderr or "invalid_commit_message" in result.stderr


def test_standalone_json_protocol_is_utf8_under_ascii_locale(tmp_path):
    repo = make_repo(tmp_path / "repo")
    (repo / "README.md").write_text("changed\n")
    git(repo, "add", "README.md")
    environment = GitRunner().environment()
    environment["LC_ALL"] = "C"
    command = [sys.executable, "-I", "-S", "-X", "utf8=0", str(ROOT / "src/codexspec/commit_runtime.py")]
    snap = subprocess.run([*command, "snapshot"], cwd=repo, env=environment, capture_output=True)
    assert snap.returncode == 0, snap.stderr
    message = "fix: 修正暂存内容\n\n保留完整说明。\n"
    result = subprocess.run(
        [*command, "commit"],
        cwd=repo,
        env=environment,
        capture_output=True,
        input=json.dumps({"analysis": json.loads(snap.stdout), "message": message}, ensure_ascii=False).encode("utf-8"),
    )
    assert result.returncode == 0, result.stderr
    assert git(repo, "log", "-1", "--format=%B").stdout.strip() == message.strip()


@pytest.mark.parametrize("phase", ["pre-commit", "prepare-commit-msg", "commit-msg"])
@pytest.mark.parametrize("entry", ["imported", "standalone"])
def test_hook_prefix_refusal_matches_git_from_subdirectory(tmp_path, phase, entry):
    from codexspec.commit_runtime import AutomationError, commit_snapshot, snapshot

    repo = make_repo(tmp_path / "repo")
    subdir = repo / "restricted"
    subdir.mkdir()
    (repo / "README.md").write_text("staged change\n")
    git(repo, "add", "README.md")
    hooks = repo / "hooks"
    hooks.mkdir()
    hook = hooks / phase
    hook.write_text('#!/bin/sh\nif [ "$GIT_PREFIX" = "restricted/" ]; then echo prefix-denied >&2; exit 1; fi\n')
    hook.chmod(0o755)
    git(repo, "config", "core.hooksPath", str(hooks))
    before = git(repo, "rev-parse", "HEAD").stdout
    native = git(subdir, "commit", "-m", "fix: native", check=False)
    assert native.returncode != 0 and "prefix-denied" in native.stderr
    analysis = snapshot(subdir)
    if entry == "imported":
        with pytest.raises(AutomationError, match="prefix-denied"):
            commit_snapshot(subdir, analysis, "fix: guarded")
    else:
        result = subprocess.run(
            [sys.executable, "-I", "-S", str(ROOT / "src/codexspec/commit_runtime.py"), "commit"],
            cwd=subdir,
            env=GitRunner().environment(),
            input=json.dumps({"analysis": analysis, "message": "fix: standalone"}),
            capture_output=True,
            text=True,
        )
        assert result.returncode != 0 and "prefix-denied" in result.stderr
    assert git(repo, "rev-parse", "HEAD").stdout == before
    # Root invocation has an empty prefix and remains accepted by this policy.
    commit_snapshot(repo, snapshot(repo), "fix: root invocation")
    assert git(repo, "show", "HEAD:README.md").stdout == "staged change\n"
