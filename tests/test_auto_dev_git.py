"""Tests for auto-dev synchronization and feature commits."""

import json
from pathlib import Path

import pytest

from codexspec.automation import (
    AutoDevGit,
    AutoDevOwnership,
    AutomationError,
    ensure_dedicated_workspace,
    locate_repository,
)
from tests.automation_test_support import git, make_bare_remote, make_repo
from tests.test_blueprint import FEATURE_ID


def services(tmp_path: Path) -> tuple[Path, AutoDevOwnership, AutoDevGit, str]:
    repo = make_repo(tmp_path / "project")
    context = locate_repository(repo)
    workspace = ensure_dedicated_workspace(context)
    owner = AutoDevOwnership(context)
    token = owner.acquire()
    return repo, owner, AutoDevGit(workspace, owner), token


def finish_sync(service: AutoDevGit, token: str) -> dict[str, object]:
    result = service.sync_default(token)
    while result["state"] == "needs_verification":
        assert service.continue_sync(token, checks_passed=True)["state"] == "clean"
        result = service.sync_default(token)
    return result


def test_sync_local_default_and_commit_exact_feature_scope(tmp_path: Path) -> None:
    repo, owner, service, token = services(tmp_path)
    (repo / "default.txt").write_text("from default\n")
    git(repo, "add", "default.txt")
    git(repo, "commit", "-m", "feat: default change")
    result = service.sync_default(token)
    assert result["state"] == "needs_verification"
    assert service.continue_sync(token, checks_passed=True)["state"] == "clean"
    result = service.sync_default(token)
    assert result["state"] == "clean"
    assert (service.workspace.path / "default.txt").exists()

    feature_path = service.workspace.path / "feature.txt"
    feature_path.write_text("feature\n")
    unrelated = service.workspace.path / "unrelated.txt"
    unrelated.write_text("staged separately\n")
    git(service.workspace.path, "add", "unrelated.txt")
    commit = service.commit_feature(token, FEATURE_ID, "feat", "implement login", ["feature.txt"])
    assert commit["state"] == "committed"
    assert git(service.workspace.path, "log", "-1", "--format=%s").stdout.strip() == (
        f"feat({FEATURE_ID}): implement login"
    )
    assert git(service.workspace.path, "diff", "--cached", "--name-only").stdout.strip() == "unrelated.txt"
    owner.release(token)


def test_commit_feature_rejects_blueprint_and_wrong_owner(tmp_path: Path) -> None:
    _, _, service, token = services(tmp_path)
    with pytest.raises(AutomationError, match="blueprint_path_forbidden"):
        service.commit_feature(token, FEATURE_ID, "feat", "bad", [".codexspec/blueprint.md"])
    for path in (".", ".codexspec", ":(glob)**"):
        with pytest.raises(AutomationError, match="blueprint_path_forbidden|invalid_commit_path"):
            service.commit_feature(token, FEATURE_ID, "feat", "bad", [path])
    with pytest.raises(Exception, match="lost_ownership"):
        service.sync_default("wrong-token")


def test_sync_requires_interrupted_blueprint_transaction_recovery(tmp_path: Path) -> None:
    _, _, service, token = services(tmp_path)
    recovery = service.workspace.repository.coordination_dir / "blueprint-transaction.json"
    recovery.parent.mkdir(parents=True, exist_ok=True)
    recovery.write_text("{}\n")

    with pytest.raises(AutomationError, match="blueprint_recovery_required"):
        service.sync_default(token)


def test_sync_reports_conflict_then_aborts_to_pre_merge_head(tmp_path: Path) -> None:
    repo = make_repo(tmp_path / "project")
    make_bare_remote(tmp_path / "remote.git", repo)
    context = locate_repository(repo)
    workspace = ensure_dedicated_workspace(context)
    owner = AutoDevOwnership(context)
    token = owner.acquire()
    service = AutoDevGit(workspace, owner)
    pre_head = git(workspace.path, "rev-parse", "HEAD").stdout.strip()

    (repo / "README.md").write_text("default conflict\n")
    git(repo, "add", "README.md")
    git(repo, "commit", "-m", "feat: default conflict")
    (workspace.path / "README.md").write_text("fixed conflict\n")
    git(workspace.path, "add", "README.md")
    git(workspace.path, "commit", "-m", f"feat({FEATURE_ID}): fixed conflict")
    fixed_pre_merge = git(workspace.path, "rev-parse", "HEAD").stdout.strip()

    result = service.sync_default(token)
    assert result["state"] == "needs_resolution"
    assert result["conflict_paths"] == ["README.md"]
    aborted = service.abort_sync(token)
    assert aborted["state"] == "aborted"
    assert git(workspace.path, "rev-parse", "HEAD").stdout.strip() == fixed_pre_merge
    assert pre_head != fixed_pre_merge


def test_resolved_conflict_is_prepared_before_verification_and_commit(tmp_path: Path) -> None:
    repo, _, service, token = services(tmp_path)
    (repo / "README.md").write_text("default conflict\n")
    git(repo, "add", "README.md")
    git(repo, "commit", "-m", "feat: default conflict")
    (service.workspace.path / "README.md").write_text("feature conflict\n")
    git(service.workspace.path, "add", "README.md")
    git(service.workspace.path, "commit", "-m", f"feat({FEATURE_ID}): feature conflict")

    assert service.sync_default(token)["state"] == "needs_resolution"
    with pytest.raises(AutomationError, match="merge_resolution_check_failed"):
        service.prepare_sync_verification(token, ["README.md"])
    (service.workspace.path / "README.md").write_text("resolved content\n")
    with pytest.raises(AutomationError, match="merge_conflicts_unresolved"):
        service.continue_sync(token, checks_passed=True)
    with pytest.raises(AutomationError, match="resolved_paths_mismatch"):
        service.prepare_sync_verification(token, ["not-conflicted.txt"])

    prepared = service.prepare_sync_verification(token, ["README.md"])
    assert prepared["state"] == "needs_verification"
    assert json.loads(service.merge_record.read_text())["phase"] == "resolved"
    interrupted_record = json.loads(service.merge_record.read_text())
    interrupted_record["phase"] = "merging"
    service.merge_record.write_text(json.dumps(interrupted_record))
    assert service.recover_merge_ownership(token)["state"] == "needs_verification"
    assert json.loads(service.merge_record.read_text())["phase"] == "resolved"
    assert service.continue_sync(token, checks_passed=True)["state"] == "clean"
    assert (service.workspace.path / "README.md").read_text() == "resolved content\n"
    assert not service.merge_record.exists()


def test_clean_merge_requires_verification_and_failed_checks_roll_back(tmp_path: Path) -> None:
    repo, _, service, token = services(tmp_path)
    pre_head = git(service.workspace.path, "rev-parse", "HEAD").stdout.strip()
    (repo / "default.txt").write_text("new default\n")
    git(repo, "add", "default.txt")
    git(repo, "commit", "-m", "feat: default")

    result = service.sync_default(token)
    assert result["state"] == "needs_verification"
    assert service.merge_record.exists()
    assert service.abort_sync(token)["state"] == "aborted"
    assert git(service.workspace.path, "rev-parse", "HEAD").stdout.strip() == pre_head
    assert not (service.workspace.path / "default.txt").exists()
    assert not service.merge_record.exists()


def test_fetch_failure_is_non_blocking_and_retried_each_sync(tmp_path: Path) -> None:
    repo = make_repo(tmp_path / "project")
    remote = make_bare_remote(tmp_path / "remote.git", repo)
    context = locate_repository(repo)
    workspace = ensure_dedicated_workspace(context)
    moved_remote = tmp_path / "unavailable.git"
    remote.rename(moved_remote)
    owner = AutoDevOwnership(context)
    token = owner.acquire()
    service = AutoDevGit(workspace, owner)

    first = service.sync_default(token)
    second = service.sync_default(token)
    assert first["state"] == second["state"] == "clean"
    assert first["fetch_warning"]
    assert second["fetch_warning"]


def test_stale_run_takeover_recovers_merge_ownership(tmp_path: Path) -> None:
    repo = make_repo(tmp_path / "project")
    context = locate_repository(repo)
    workspace = ensure_dedicated_workspace(context)
    now = [100.0]
    ownership = AutoDevOwnership(context, clock=lambda: now[0], stale_after=10)
    old_token = ownership.acquire()
    service = AutoDevGit(workspace, ownership)
    service.merge_record.parent.mkdir(parents=True, exist_ok=True)
    pre_head = git(workspace.path, "rev-parse", "HEAD").stdout.strip()
    service.merge_record.write_text(
        json.dumps(
            {
                "token": old_token,
                "pre_head": pre_head,
                "target": "refs/heads/main",
                "phase": "merging",
            }
        )
    )

    now[0] = 111.0
    new_token = ownership.acquire()
    recovered = service.recover_merge_ownership(new_token)
    assert recovered["state"] == "none"
    assert not service.merge_record.exists()
    with pytest.raises(Exception, match="lost_ownership"):
        service.abort_sync(old_token)


def test_stale_takeover_recovers_merge_started_before_git_returns(tmp_path: Path) -> None:
    repo = make_repo(tmp_path / "project")
    context = locate_repository(repo)
    workspace = ensure_dedicated_workspace(context)
    now = [100.0]
    ownership = AutoDevOwnership(context, clock=lambda: now[0], stale_after=10)
    old_token = ownership.acquire()
    service = AutoDevGit(workspace, ownership)
    pre_head = git(workspace.path, "rev-parse", "HEAD").stdout.strip()
    service.merge_record.parent.mkdir(parents=True, exist_ok=True)
    service.merge_record.write_text(
        json.dumps(
            {
                "token": old_token,
                "pre_head": pre_head,
                "target": "refs/heads/main",
                "phase": "merging",
            }
        )
    )
    (workspace.path / "README.md").write_text("partial resolution\n")

    now[0] = 111.0
    new_token = ownership.acquire()
    recovered = service.recover_merge_ownership(new_token)
    assert recovered["state"] == "none"
    assert not service.merge_record.exists()
    assert git(workspace.path, "status", "--porcelain").stdout.strip() == ""
    assert git(workspace.path, "rev-parse", "HEAD").stdout.strip() == pre_head
    assert finish_sync(service, new_token)["state"] == "clean"


@pytest.mark.parametrize("strategy", ["merge", "squash", "rebase", "cherry-pick"])
def test_integrated_feature_is_absent_from_later_file_diff(tmp_path: Path, strategy: str) -> None:
    repo, owner, service, token = services(tmp_path)
    initial = git(repo, "rev-parse", "main").stdout.strip()
    first = service.workspace.path / "first.txt"
    first.write_text("first feature\n")
    git(service.workspace.path, "add", "first.txt")
    git(service.workspace.path, "commit", "-m", f"feat({FEATURE_ID}): first")
    first_commit = git(service.workspace.path, "rev-parse", "HEAD").stdout.strip()
    second = service.workspace.path / "second.txt"
    second.write_text("second feature\n")
    git(service.workspace.path, "add", "second.txt")
    git(service.workspace.path, "commit", "-m", "feat(2026-0830-1045cd): second")

    if strategy == "merge":
        git(repo, "merge", "--no-ff", "--no-edit", first_commit)
    elif strategy == "squash":
        git(repo, "merge", "--squash", first_commit)
        git(repo, "commit", "-m", "feat: integrate first")
    elif strategy == "cherry-pick":
        git(repo, "cherry-pick", first_commit)
    else:
        git(repo, "branch", "delivery", first_commit)
        git(repo, "checkout", "delivery")
        git(repo, "rebase", "--onto", "main", initial)
        git(repo, "checkout", "main")
        git(repo, "merge", "--ff-only", "delivery")

    assert finish_sync(service, token)["state"] == "clean"
    changed = git(service.workspace.path, "diff", "--name-only", "main...HEAD").stdout.splitlines()
    assert "first.txt" not in changed
    assert changed == ["second.txt"]
    owner.release(token)


def test_non_ascii_conflict_paths_round_trip_unquoted(tmp_path: Path) -> None:
    repo, _, service, token = services(tmp_path)
    conflicted = "需求文档.md"
    (repo / conflicted).write_text("default side\n")
    git(repo, "add", conflicted)
    git(repo, "commit", "-m", "feat: default conflict")
    (service.workspace.path / conflicted).write_text("feature side\n")
    git(service.workspace.path, "add", conflicted)
    git(service.workspace.path, "commit", "-m", f"feat({FEATURE_ID}): feature conflict")

    result = service.sync_default(token)
    assert result["state"] == "needs_resolution"
    assert result["conflict_paths"] == [conflicted]
    (service.workspace.path / conflicted).write_text("resolved content\n")
    prepared = service.prepare_sync_verification(token, [conflicted])
    assert prepared["state"] == "needs_verification"


def test_resolution_with_trailing_whitespace_passes_marker_gate(tmp_path: Path) -> None:
    repo, _, service, token = services(tmp_path)
    (repo / "README.md").write_text("default conflict\n")
    git(repo, "add", "README.md")
    git(repo, "commit", "-m", "feat: default conflict")
    (service.workspace.path / "README.md").write_text("feature conflict\n")
    git(service.workspace.path, "add", "README.md")
    git(service.workspace.path, "commit", "-m", f"feat({FEATURE_ID}): feature conflict")

    assert service.sync_default(token)["state"] == "needs_resolution"
    (service.workspace.path / "README.md").write_text("resolved with break  \n")
    prepared = service.prepare_sync_verification(token, ["README.md"])
    assert prepared["state"] == "needs_verification"


def test_abort_sync_ignores_untracked_files_and_clears_merge_ownership(tmp_path: Path) -> None:
    repo, _, service, token = services(tmp_path)
    (repo / "README.md").write_text("default conflict\n")
    git(repo, "add", "README.md")
    git(repo, "commit", "-m", "feat: default conflict")
    (service.workspace.path / "README.md").write_text("feature conflict\n")
    git(service.workspace.path, "add", "README.md")
    git(service.workspace.path, "commit", "-m", f"feat({FEATURE_ID}): feature conflict")

    assert service.sync_default(token)["state"] == "needs_resolution"
    untracked = service.workspace.path / "check-output.txt"
    untracked.write_text("baseline check artifact\n")

    aborted = service.abort_sync(token)
    assert aborted["state"] == "aborted"
    assert untracked.read_text() == "baseline check artifact\n"
    assert not (service.workspace.repository.coordination_dir / "merge-owner.json").exists()
    untracked.unlink()

    restarted = service.sync_default(token)
    assert restarted["state"] == "needs_resolution"
    (service.workspace.path / "README.md").write_text("resolved after restart\n")
    assert service.prepare_sync_verification(token, ["README.md"])["state"] == "needs_verification"
    assert service.continue_sync(token, checks_passed=True)["state"] == "clean"
    assert service.sync_default(token)["state"] == "clean"


def test_orphan_blueprint_temporary_is_swept_before_sync(tmp_path: Path) -> None:
    _, _, service, token = services(tmp_path)
    orphan = service.workspace.blueprint_path.parent / ".blueprint.md.orphaned"
    orphan.parent.mkdir(parents=True, exist_ok=True)
    orphan.write_text("partial write\n")

    result = finish_sync(service, token)
    assert result["state"] == "clean"
    assert not orphan.exists()


def test_fetch_warning_redacts_remote_url_credentials(tmp_path: Path) -> None:
    repo = make_repo(tmp_path / "project")
    make_bare_remote(tmp_path / "remote.git", repo)
    context = locate_repository(repo)
    workspace = ensure_dedicated_workspace(context)
    owner = AutoDevOwnership(context)
    token = owner.acquire()
    service = AutoDevGit(workspace, owner)
    git(repo, "remote", "set-url", "origin", "https://user:secret-token@invalid.invalid/repo.git")

    result = service.sync_default(token)
    warning = result.get("fetch_warning") or ""
    assert warning
    assert "secret-token" not in warning
    owner.release(token)
