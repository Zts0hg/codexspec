"""Native merge signing and signoff policy survives deferred finalization."""

import shlex
from pathlib import Path

import pytest

from codexspec.automation import (
    AutomationError,
    ensure_dedicated_workspace,
    finish_initial_workspace,
    locate_repository,
)
from codexspec.commit_runtime import commit_snapshot, snapshot
from codexspec.worktrees import WorkspaceManager
from tests.automation_test_support import git, make_bare_remote
from tests.test_auto_dev_git import services
from tests.test_merge_commit_analysis import diverge
from tests.test_worktrees import FEATURE, configured, diverged, evidence


@pytest.mark.parametrize("flow", ["sync", "ordinary", "fixed"])
@pytest.mark.parametrize("empty", [False, True])
@pytest.mark.parametrize("option", ["--gpg-sign", "--gpg-sign=merge-key", "--no-gpg-sign", "--signoff"])
def test_merge_options_match_native_finalization(tmp_path, flow, empty, option):
    if flow == "sync":
        repo, owner, service, token = services(tmp_path)
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
    if flow == "sync":
        assert service.sync_default(token)["state"] == "needs_verification"
    elif flow == "ordinary":
        manager = WorkspaceManager(repo)
        pending = manager.create(FEATURE)
        work = Path(pending["workspace"])
    else:
        context = locate_repository(repo)
        with pytest.raises(AutomationError, match="initial_merge_requires"):
            ensure_dedicated_workspace(context)
        work = context.worktree_path
    target = git(work, "rev-parse", "MERGE_HEAD").stdout.strip()
    git(work, "merge", "--abort")
    branch = git(work, "symbolic-ref", "--short", "HEAD").stdout.strip()
    git(work, "config", f"branch.{branch}.mergeOptions", option)
    git(work, "config", "commit.gpgsign", "true" if option != "--gpg-sign" else "false")
    if option == "--signoff":
        git(work, "config", "commit.gpgsign", "false")
        hook = repo / ".git/hooks/commit-msg"
        hook.write_text('#!/bin/sh\ngrep -q "^Signed-off-by:" "$1"\n')
        hook.chmod(0o755)
    marker = tmp_path / "signer-args"
    signer = tmp_path / "signer"
    signer.write_text('#!/bin/sh\nprintf "%s\\n" "$@" > ' + shlex.quote(str(marker)) + "\nexit 1\n")
    signer.chmod(0o755)
    git(work, "config", "gpg.program", str(signer))
    git(work, "config", "user.signingkey", "default-key")
    native = git(work, "merge", "--no-edit", target, check=False)
    native_args = marker.read_text() if marker.exists() else None
    native_message = git(work, "show", "-s", "--format=%B", "HEAD").stdout
    if native.returncode:
        assert git(work, "rev-parse", "HEAD").stdout.strip() == before
        git(work, "merge", "--abort")
    else:
        git(work, "reset", "--hard", before)
    marker.unlink(missing_ok=True)
    assert git(work, "merge", "--no-edit", "--no-commit", target).returncode == 0
    analyzed = snapshot(work)
    proof = evidence(work)

    def finish():
        if flow == "sync":
            return service.continue_sync(
                token, checks_passed=True, analysis=analyzed, message=None if empty else "chore: integrate main"
            )
        if flow == "ordinary":
            return manager.finish(FEATURE, proof)
        return finish_initial_workspace(context, proof)

    if native.returncode:
        with pytest.raises(AutomationError, match="failed to sign"):
            finish()
        assert git(work, "rev-parse", "HEAD").stdout.strip() == before
        assert git(work, "rev-parse", "MERGE_HEAD").stdout.strip() == target
    else:
        finish()
        assert git(work, "rev-parse", "HEAD^{tree}").stdout.strip() == analyzed["tree"]
        assert git(work, "show", "-s", "--format=%P", "HEAD").stdout.split() == [before, target]
        if option == "--signoff":
            actual = git(work, "show", "-s", "--format=%B", "HEAD").stdout
            assert [x for x in actual.splitlines() if x.startswith("Signed-off-by:")] == [
                x for x in native_message.splitlines() if x.startswith("Signed-off-by:")
            ]
    assert (marker.read_text() if marker.exists() else None) == native_args
    if flow == "sync":
        owner.release(token)


@pytest.mark.parametrize(
    "options",
    [
        "-Smerge-key",
        "-qSmerge-key",
        "--gpg-s=merge-key",
        '--gpg-sign="key\\q"',
        "--gpg-sign --no-gpg-sign",
        "--no-gpg-sign --gpg-sign=last-key",
        "--signoff --no-signoff",
        '-m "--signoff"',
        '-m "--gpg-sign=wrong" --signoff',
        "--strategy-option --signoff",
    ],
)
def test_merge_option_parsing_matches_git(tmp_path, options):
    repo, _, service, _ = services(tmp_path)
    work = service.workspace.path
    before = diverge(repo, work)
    target = git(repo, "rev-parse", "HEAD").stdout.strip()
    branch = git(work, "symbolic-ref", "--short", "HEAD").stdout.strip()
    git(work, "config", f"branch.{branch}.mergeOptions", options)
    marker = tmp_path / "signer-args"
    signer = tmp_path / "signer"
    signer.write_text('#!/bin/sh\nprintf "%s\\n" "$@" > ' + shlex.quote(str(marker)) + "\nexit 1\n")
    signer.chmod(0o755)
    git(work, "config", "gpg.program", str(signer))
    native = git(work, "merge", "--no-edit", target, check=False)
    native_args = marker.read_text() if marker.exists() else None
    native_message = git(work, "show", "-s", "--format=%B", "HEAD").stdout
    if git(work, "rev-parse", "--verify", "MERGE_HEAD", check=False).returncode == 0:
        git(work, "merge", "--abort")
    else:
        git(work, "reset", "--hard", before)
    marker.unlink(missing_ok=True)
    prepared = git(work, "merge", "--no-edit", "--no-commit", target, check=False)
    if prepared.returncode:
        # Invalid native strategy arguments fail before finalization in both paths.
        assert native.returncode and native_args is None
        return
    analyzed = snapshot(work)
    if native.returncode:
        with pytest.raises(AutomationError, match="failed to sign"):
            commit_snapshot(work, analyzed, "chore: integrate", merge_hook=True)
    else:
        commit_snapshot(work, analyzed, "chore: integrate", merge_hook=True)
        actual = git(work, "show", "-s", "--format=%B", "HEAD").stdout
        assert ("Signed-off-by:" in actual) == ("Signed-off-by:" in native_message)
    assert (marker.read_text() if marker.exists() else None) == native_args


def test_manual_merge_commit_does_not_inherit_merge_options(tmp_path):
    repo, _, service, _ = services(tmp_path)
    work = service.workspace.path
    diverge(repo, work)
    branch = git(work, "symbolic-ref", "--short", "HEAD").stdout.strip()
    git(work, "config", f"branch.{branch}.mergeOptions", "--gpg-sign --signoff")
    assert git(work, "merge", "--no-edit", "--no-commit", "main").returncode == 0
    commit_snapshot(work, snapshot(work), "chore: manual merge", merge_hook=False)
    message = git(work, "show", "-s", "--format=%B", "HEAD").stdout
    assert "Signed-off-by:" not in message
