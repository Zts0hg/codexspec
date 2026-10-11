"""Real Git coverage for analysis before merge commits."""

from pathlib import Path

import pytest

from codexspec.automation import AutomationError
from codexspec.commit_runtime import commit_snapshot, snapshot
from tests.automation_test_support import git, make_repo
from tests.test_auto_dev_git import services


def diverge(repo, work, *, empty=False, conflict=False):
    for path, name in ((repo, "main"), (work, "feature")):
        if not empty:
            target = "README.md" if conflict else name + ".txt"
            (path / target).write_text(name + "\n")
            git(path, "add", target)
        git(path, "commit", "--allow-empty", "-m", "feat: " + name)
    return git(work, "rev-parse", "HEAD").stdout.strip()


@pytest.mark.parametrize("empty", [False, True])
def test_sync_waits_for_analysis_before_creating_merge(tmp_path, empty):
    repo, owner, service, token = services(tmp_path)
    work = service.workspace.path
    before = diverge(repo, work, empty=empty)
    state = service.sync_default(token)
    assert state["state"] == "needs_verification"
    assert git(work, "rev-parse", "HEAD").stdout.strip() == before
    analysis = snapshot(work)
    message = None if empty else "chore: integrate main changes\n\nInclude main.txt.\n"
    default = Path(git(work, "rev-parse", "--git-path", "MERGE_MSG").stdout.strip())
    if not default.is_absolute():
        default = work / default
    expected = default.read_text(encoding="utf-8") if empty else message
    with pytest.raises(AutomationError, match="analysis_required"):
        service.continue_sync(token, checks_passed=True)
    service.continue_sync(token, checks_passed=True, analysis=analysis, message=message)
    assert git(work, "show", "-s", "--format=%B", "HEAD").stdout.rstrip() == expected.rstrip()
    assert len(git(work, "rev-list", "--parents", "-n", "1", "HEAD").stdout.split()) == 3
    owner.release(token)


def test_resolved_merge_hook_cannot_change_analyzed_content(tmp_path):
    repo, _, service, token = services(tmp_path)
    work = service.workspace.path
    before = diverge(repo, work, conflict=True)
    assert service.sync_default(token)["state"] == "needs_resolution"
    (work / "README.md").write_text("resolved\n")
    service.prepare_sync_verification(token, ["README.md"])
    analysis = snapshot(work)
    hooks = Path(git(work, "rev-parse", "--path-format=absolute", "--git-path", "hooks").stdout.strip())
    hook = hooks / "pre-commit"
    hook.write_text("#!/bin/sh\nprintf 'other\\n' > README.md\ngit add README.md\n")
    hook.chmod(0o755)
    with pytest.raises(AutomationError, match="stale_analysis"):
        service.continue_sync(token, checks_passed=True, analysis=analysis, message="fix: reconcile README")
    assert git(work, "rev-parse", "HEAD").stdout.strip() == before
    assert service.merge_record.exists()


def test_empty_merge_snapshot_binds_parents_and_uses_default_message(tmp_path):
    repo = make_repo(tmp_path / "repo")
    git(repo, "branch", "other")
    git(repo, "commit", "--allow-empty", "-m", "main history")
    git(repo, "checkout", "other")
    git(repo, "commit", "--allow-empty", "-m", "other history")
    git(repo, "checkout", "main")
    git(repo, "merge", "--no-commit", "other")
    analysis = snapshot(repo)
    before = git(repo, "rev-parse", "HEAD").stdout.strip()
    merge_head = repo / ".git/MERGE_HEAD"
    original = merge_head.read_bytes()
    merge_head.write_bytes((before + "\n").encode("ascii"))
    with pytest.raises(AutomationError, match="stale_analysis"):
        commit_snapshot(repo, analysis, None)
    merge_head.write_bytes(original)
    commit_snapshot(repo, analysis, None)
    assert len(git(repo, "rev-list", "--parents", "-n", "1", "HEAD").stdout.split()) == 3
    with pytest.raises(AutomationError, match="empty_staged_changes"):
        snapshot(repo)


@pytest.mark.parametrize("fixed", [False, True])
@pytest.mark.parametrize("conflict", [False, True])
def test_initial_workspace_merge_waits_for_staged_analysis(tmp_path, fixed, conflict):
    from codexspec.automation import ensure_dedicated_workspace, locate_repository
    from codexspec.worktrees import WorkspaceManager
    from tests.test_worktrees import FEATURE, diverged

    repo, local, remote = diverged(tmp_path, conflict)
    context = locate_repository(repo)
    if fixed:
        with pytest.raises(AutomationError, match="initial_merge_requires"):
            ensure_dedicated_workspace(context)
        work = context.worktree_path
    else:
        manager = WorkspaceManager(repo)
        result = manager.create(FEATURE)
        work = Path(result["workspace"])
        assert not Path(result["requirements_file"]).exists()
    assert git(work, "rev-parse", "HEAD").stdout.strip() == local
    if conflict:
        (work / "README.md").write_text("both\n")
        git(work, "add", "README.md")
    analysis = snapshot(work)
    verification = {
        "head": analysis["head"],
        "tree": analysis["tree"],
        "checks": [{"command": "fixture check", "exit_code": 0}],
        "analysis": analysis,
        "message": "chore: integrate baseline changes",
    }
    if fixed:
        from codexspec.automation import finish_initial_workspace

        finish_initial_workspace(context, verification)
        assert ensure_dedicated_workspace(context).path == work
    else:
        assert manager.finish(FEATURE, verification)["status"] == "ready"
    assert git(work, "show", "-s", "--format=%P", "HEAD").stdout.split() == [local, remote]
    assert git(repo, "rev-parse", "HEAD").stdout.strip() == local


def test_sync_rejects_analyzed_merge_with_replaced_target(tmp_path):
    repo, _, service, token = services(tmp_path)
    work = service.workspace.path
    before = diverge(repo, work)
    assert service.sync_default(token)["state"] == "needs_verification"
    other = git(repo, "rev-parse", "main^").stdout.strip()
    path = Path(git(work, "rev-parse", "--path-format=absolute", "--git-path", "MERGE_HEAD").stdout.strip())
    path.write_bytes((other + "\n").encode("ascii"))
    analyzed = snapshot(work)
    with pytest.raises(AutomationError, match="stale_analysis"):
        service.continue_sync(token, checks_passed=True, analysis=analyzed, message="chore: integrate main")
    assert git(work, "rev-parse", "HEAD").stdout.strip() == before
