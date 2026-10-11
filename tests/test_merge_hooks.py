"""Retain native hook selection across two-step merge finalization."""

import json
import shlex
from pathlib import Path

import pytest

from codexspec.automation import (
    AutomationError,
    ensure_dedicated_workspace,
    finish_initial_workspace,
    locate_repository,
)
from codexspec.commit_runtime import snapshot
from codexspec.worktrees import WorkspaceManager
from tests.automation_test_support import git, make_bare_remote
from tests.test_auto_dev_git import services
from tests.test_merge_commit_analysis import diverge
from tests.test_worktrees import FEATURE, configured, diverged, evidence


@pytest.mark.parametrize("flow", ["sync", "ordinary", "fixed"])
@pytest.mark.parametrize("behavior", ["deny", "mutate", "delegate"])
def test_automatic_merge_preserves_pre_merge_hook(tmp_path, flow, behavior):
    if flow == "sync":
        repo, _, service, token = services(tmp_path)
        work = service.workspace.path
        before = diverge(repo, work)
    else:
        repo, before, _ = diverged(tmp_path)
    hooks = repo / ".git/hooks"
    pre_commit = hooks / "pre-commit"
    pre_commit.write_text("#!/bin/sh\necho invoked >> hook-count\n")
    pre_commit.chmod(0o755)
    merge_hook = hooks / "pre-merge-commit"
    action = {
        "deny": "echo merge-policy-refused >&2\nexit 1\n",
        "mutate": "echo changed-by-hook > README.md\ngit add README.md\n",
        "delegate": 'exec "$(git rev-parse --git-path hooks)/pre-commit"\n',
    }[behavior]
    merge_hook.write_text("#!/bin/sh\necho invoked >> merge-hook-count\n" + action)
    merge_hook.chmod(0o755)
    if flow == "sync":
        assert service.sync_default(token)["state"] == "needs_verification"
        analysis = snapshot(work)

        def finish():
            return service.continue_sync(token, checks_passed=True, analysis=analysis, message="chore: integrate main")
    elif flow == "ordinary":
        manager = WorkspaceManager(repo)
        pending = manager.create(FEATURE)
        work = Path(pending["workspace"])
        proof = evidence(work)

        def finish():
            return manager.finish(FEATURE, proof)
    else:
        context = locate_repository(repo)
        with pytest.raises(AutomationError, match="initial_merge_requires"):
            ensure_dedicated_workspace(context)
        work = context.worktree_path
        proof = evidence(work)

        def finish():
            return finish_initial_workspace(context, proof)

    if behavior == "delegate":
        finish()
        assert (work / "hook-count").read_text() == "invoked\n"
        assert (work / "merge-hook-count").read_text() == "invoked\n"
        assert len(git(work, "show", "-s", "--format=%P", "HEAD").stdout.split()) == 2
    else:
        with pytest.raises(AutomationError, match="merge-policy-refused" if behavior == "deny" else "stale_analysis"):
            finish()
        assert git(work, "rev-parse", "HEAD").stdout.strip() == before
        assert git(work, "rev-parse", "--verify", "MERGE_HEAD").returncode == 0


def test_conflict_resolution_keeps_native_pre_commit_hook(tmp_path):
    repo, _, service, token = services(tmp_path)
    work = service.workspace.path
    diverge(repo, work, conflict=True)
    hooks = repo / ".git/hooks"
    (hooks / "pre-merge-commit").write_text("#!/bin/sh\nexit 93\n")
    (hooks / "pre-merge-commit").chmod(0o755)
    (hooks / "pre-commit").write_text("#!/bin/sh\necho invoked >> hook-count\n")
    (hooks / "pre-commit").chmod(0o755)
    for name, body in {
        "prepare-commit-msg": 'echo "$2 $(basename "$1")" >> hook-events\n',
        "post-commit": "echo post-commit >> hook-events\n",
        "post-merge": "echo post-merge >> hook-events\n",
    }.items():
        hook = hooks / name
        hook.write_text("#!/bin/sh\n" + body)
        hook.chmod(0o755)
    assert service.sync_default(token)["state"] == "needs_resolution"
    (work / "README.md").write_text("both\n")
    service.prepare_sync_verification(token, ["README.md"])
    service.continue_sync(token, checks_passed=True, analysis=snapshot(work), message="fix: reconcile README")
    assert (work / "hook-count").read_text() == "invoked\n"
    assert (work / "hook-events").read_text().splitlines() == ["message COMMIT_EDITMSG", "post-commit"]


@pytest.mark.parametrize("empty", [False, True])
@pytest.mark.parametrize("recover", [False, True])
def test_automatic_merge_hook_refusal_remains_resumable(tmp_path, empty, recover):
    repo, owner, service, token = services(tmp_path)
    work = service.workspace.path
    before = diverge(repo, work, empty=empty)
    hook = repo / ".git/hooks/pre-merge-commit"
    hook.write_text("#!/bin/sh\nexit 93\n")
    hook.chmod(0o755)
    assert service.sync_default(token)["state"] == "needs_verification"
    if recover:
        record = json.loads(service.merge_record.read_text())
        record["phase"] = "merging"
        service.merge_record.write_text(json.dumps(record))
        owner.release(token)
        token = owner.acquire()
        assert service.recover_merge_ownership(token)["state"] == "needs_verification"
    analyzed = snapshot(work)
    message = None if empty else "chore: integrate main"
    with pytest.raises(AutomationError, match="git_command_failed"):
        service.continue_sync(token, checks_passed=True, analysis=analyzed, message=message)
    assert git(work, "rev-parse", "HEAD").stdout.strip() == before
    assert git(work, "rev-parse", "--verify", "MERGE_HEAD").returncode == 0
    assert service.merge_record.exists()
    hook.write_text("#!/bin/sh\nexit 0\n")
    assert service.continue_sync(token, checks_passed=True, analysis=analyzed, message=message)["state"] == "clean"
    assert git(work, "rev-parse", "HEAD^{tree}").stdout.strip() == analyzed["tree"]
    assert git(work, "show", "-s", "--format=%P", "HEAD").stdout.split() == [before, *analyzed["merge_heads"]]
    if empty:
        assert git(work, "show", "-s", "--format=%B", "HEAD").stdout.rstrip() == analyzed["default_message"].rstrip()
    assert not service.merge_record.exists()
    owner.release(token)


@pytest.mark.parametrize("flow", ["sync", "ordinary", "fixed"])
@pytest.mark.parametrize("empty", [False, True])
@pytest.mark.parametrize("reject", [None, "source", "prepare-path", "commit-path"])
def test_automatic_merge_preserves_full_hook_lifecycle(tmp_path, flow, empty, reject):
    if flow == "sync":
        repo, _, service, token = services(tmp_path)
        work = service.workspace.path
        before = diverge(repo, work, empty=empty)
    elif empty:
        repo = configured(tmp_path / "repo")
        remote = make_bare_remote(tmp_path / "remote.git", repo)
        peer = tmp_path / "peer"
        git(remote, "worktree", "add", str(peer), "main")
        git(repo, "commit", "--allow-empty", "-m", "local history")
        git(peer, "commit", "--allow-empty", "-m", "remote history")
        before = git(repo, "rev-parse", "HEAD").stdout.strip()
    else:
        repo, before, _ = diverged(tmp_path)
    hooks = repo / ".git/hooks"
    scripts = {
        "pre-merge-commit": "echo pre-merge >> hook-events\n",
        "pre-commit": "echo pre-commit >> hook-events\n",
        "prepare-commit-msg": 'echo "prepare $2" >> hook-events\n',
        "commit-msg": "echo commit-msg >> hook-events\n",
        "post-commit": "echo post-commit >> hook-events\n",
        "post-merge": 'echo "post-merge $1" >> hook-events\nexit 93\n',
    }
    if reject == "source":
        scripts["prepare-commit-msg"] += '[ "$2" != merge ] || { echo merge-policy-denied >&2; exit 1; }\n'
    elif reject:
        name = "prepare-commit-msg" if reject == "prepare-path" else "commit-msg"
        scripts[name] += 'case "$1" in *MERGE_MSG) echo merge-policy-denied >&2; exit 1;; esac\n'
    else:
        scripts["prepare-commit-msg"] += 'printf "\\nPrepared by hook\\n" >> "$1"\n'
        scripts["commit-msg"] += 'printf "\\nValidated by hook\\n" >> "$1"\n'
    for name, body in scripts.items():
        hook = hooks / name
        hook.write_text("#!/bin/sh\n" + body)
        hook.chmod(0o755)
    if flow == "sync":
        assert service.sync_default(token)["state"] == "needs_verification"
        analysis = snapshot(work)

        def finish():
            return service.continue_sync(
                token, checks_passed=True, analysis=analysis, message=None if empty else "chore: integrate main"
            )
    elif flow == "ordinary":
        manager = WorkspaceManager(repo)
        pending = manager.create(FEATURE)
        work = Path(pending["workspace"])
        proof = evidence(work)

        def finish():
            return manager.finish(FEATURE, proof)
    else:
        context = locate_repository(repo)
        with pytest.raises(AutomationError, match="initial_merge_requires"):
            ensure_dedicated_workspace(context)
        work = context.worktree_path
        proof = evidence(work)

        def finish():
            return finish_initial_workspace(context, proof)

    if reject:
        with pytest.raises(AutomationError, match="merge-policy-denied"):
            finish()
        assert git(work, "rev-parse", "HEAD").stdout.strip() == before
        assert git(work, "rev-parse", "--verify", "MERGE_HEAD").returncode == 0
        expected = ["pre-merge", "prepare merge"]
        if reject == "commit-path":
            expected.append("commit-msg")
        assert (work / "hook-events").read_text().splitlines() == expected
    else:
        finish()
        assert (work / "hook-events").read_text().splitlines() == [
            "pre-merge",
            "prepare merge",
            "commit-msg",
            "post-merge 0",
        ]
        assert len(git(work, "show", "-s", "--format=%P", "HEAD").stdout.split()) == 2
        committed_message = git(work, "show", "-s", "--format=%B", "HEAD").stdout
        assert "Prepared by hook" in committed_message
        assert "Validated by hook" in committed_message


@pytest.mark.parametrize("custom_action", [False, True])
def test_automatic_merge_preserves_reflog_action(tmp_path, monkeypatch, custom_action):
    repo, _, service, token = services(tmp_path)
    work = service.workspace.path
    before = diverge(repo, work)
    target = git(repo, "rev-parse", "HEAD").stdout.strip()
    if custom_action:
        monkeypatch.setenv("GIT_REFLOG_ACTION", "custom-action")
    else:
        monkeypatch.delenv("GIT_REFLOG_ACTION", raising=False)
    hook = repo / ".git/hooks/pre-merge-commit"
    hook.write_text('#!/bin/sh\nprintf "%s" "$GIT_REFLOG_ACTION" > hook-action\n')
    hook.chmod(0o755)
    git(work, "merge", "--no-edit", target)
    expected = (work / "hook-action").read_text()
    assert expected == ("custom-action" if custom_action else "merge " + target)
    git(work, "reset", "--hard", before)
    (work / "hook-action").unlink()
    assert service.sync_default(token)["state"] == "needs_verification"
    service.continue_sync(token, checks_passed=True, analysis=snapshot(work), message="chore: integrate main")
    assert (work / "hook-action").read_text() == expected


@pytest.mark.parametrize("flow", ["sync", "ordinary", "fixed"])
@pytest.mark.parametrize("empty", [False, True])
@pytest.mark.parametrize("explicit_editor", [False, True])
def test_automatic_merge_completion_keeps_native_environment(tmp_path, monkeypatch, flow, empty, explicit_editor):
    if flow == "sync":
        repo, _, service, token = services(tmp_path)
        work = service.workspace.path
        before = diverge(repo, work, empty=empty)
        target = git(repo, "rev-parse", "HEAD").stdout.strip()
    else:
        if empty:
            repo = configured(tmp_path / "repo")
            remote = make_bare_remote(tmp_path / "remote.git", repo)
            peer = tmp_path / "peer"
            git(remote, "worktree", "add", str(peer), "main")
            git(repo, "commit", "--allow-empty", "-m", "local history")
            git(peer, "commit", "--allow-empty", "-m", "remote history")
            before = git(repo, "rev-parse", "HEAD").stdout.strip()
            target = git(peer, "rev-parse", "HEAD").stdout.strip()
        else:
            repo, before, target = diverged(tmp_path)
        work = repo
        git(repo, "fetch", "origin")
    events = tmp_path / "hook-events"
    events.mkdir()
    editor = repo / ".git/merge-editor.sh"
    editor.write_text("#!/bin/sh\necho editor-invoked >> " + shlex.quote(str(events / "editor-events")) + "\n")
    command = "sh " + shlex.quote(str(editor))
    git(work, "config", "core.editor", command)
    if explicit_editor:
        monkeypatch.setenv("GIT_EDITOR", command)
    else:
        monkeypatch.delenv("GIT_EDITOR", raising=False)
    hooks = repo / ".git/hooks"
    post = hooks / "post-merge"
    post.write_text(
        '#!/bin/sh\nprintf "%s" "${GIT_INDEX_FILE-unset}" > '
        + shlex.quote(str(events / "post-index"))
        + '\neditor=$(git var GIT_EDITOR)\neval "$editor"\n'
    )
    post.chmod(0o755)
    reference = hooks / "reference-transaction"
    reference.write_text(
        '#!/bin/sh\nprintf "%s" "${GIT_INDEX_FILE-unset}" > ' + shlex.quote(str(events / "reference-index")) + "\n"
    )
    reference.chmod(0o755)
    git(work, "merge", "--no-edit", target)
    assert (events / "editor-events").read_text() == "editor-invoked\n"
    assert (events / "post-index").read_text() == "unset"
    assert (events / "reference-index").read_text() == "unset"
    git(work, "reset", "--hard", before)
    for name in ["editor-events", "post-index", "reference-index"]:
        (events / name).unlink()
    if flow == "sync":
        assert service.sync_default(token)["state"] == "needs_verification"
        service.continue_sync(
            token, checks_passed=True, analysis=snapshot(work), message=None if empty else "chore: integrate main"
        )
    elif flow == "ordinary":
        manager = WorkspaceManager(repo)
        work = Path(manager.create(FEATURE)["workspace"])
        manager.finish(FEATURE, evidence(work))
    else:
        context = locate_repository(repo)
        with pytest.raises(AutomationError, match="initial_merge_requires"):
            ensure_dedicated_workspace(context)
        work = context.worktree_path
        finish_initial_workspace(context, evidence(work))
    assert (events / "editor-events").is_file(), "post-merge must run the configured/caller editor"
    assert (events / "editor-events").read_text() == "editor-invoked\n"
    assert (events / "post-index").read_text() == "unset"
    assert (events / "reference-index").read_text() == "unset"
