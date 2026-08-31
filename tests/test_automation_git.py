"""Tests for repository discovery and the dedicated worktree."""

from pathlib import Path

import pytest

from codexspec.automation import (
    FIXED_BRANCH,
    WORKTREE_BASENAME,
    AutomationError,
    GitRunner,
    ensure_dedicated_workspace,
    locate_dedicated_workspace,
    locate_repository,
)
from tests.automation_test_support import git, make_bare_remote, make_repo


def test_locate_repository_from_nested_directory(tmp_path: Path) -> None:
    repo = make_repo(tmp_path / "project")
    nested = repo / "nested"
    nested.mkdir()
    context = locate_repository(nested)
    assert context.repository_root == repo.resolve()
    assert context.default_branch == "main"
    assert context.worktree_path.name == WORKTREE_BASENAME
    assert context.worktree_path.parent == Path(f"{repo.resolve()}-worktrees")


def test_adjacent_repositories_have_distinct_dedicated_worktree_paths(tmp_path: Path) -> None:
    first = make_repo(tmp_path / "first")
    second = make_repo(tmp_path / "second")
    first_context = locate_repository(first)
    second_context = locate_repository(second)
    assert first_context.worktree_path != second_context.worktree_path
    assert ensure_dedicated_workspace(first_context).path.exists()
    assert ensure_dedicated_workspace(second_context).path.exists()


def test_locate_rejects_non_repository(tmp_path: Path) -> None:
    with pytest.raises(AutomationError, match="not_git_repository"):
        locate_repository(tmp_path)


def test_ensure_creates_and_locate_validates_fixed_workspace(tmp_path: Path) -> None:
    repo = make_repo(tmp_path / "project")
    context = locate_repository(repo)
    workspace = ensure_dedicated_workspace(context)
    assert workspace.path.name == WORKTREE_BASENAME
    assert workspace.branch == FIXED_BRANCH
    assert git(repo, "show-ref", "--verify", f"refs/heads/{FIXED_BRANCH}").returncode == 0
    assert locate_dedicated_workspace(context) == workspace


def test_read_only_locate_does_not_create_missing_workspace(tmp_path: Path) -> None:
    repo = make_repo(tmp_path / "project")
    context = locate_repository(repo)
    with pytest.raises(AutomationError, match="missing_fixed_branch"):
        locate_dedicated_workspace(context)
    assert not context.worktree_path.exists()


def test_ensure_rejects_unregistered_occupied_path(tmp_path: Path) -> None:
    repo = make_repo(tmp_path / "project")
    context = locate_repository(repo)
    context.worktree_path.mkdir(parents=True)
    with pytest.raises(AutomationError, match="worktree_path_occupied"):
        ensure_dedicated_workspace(context)


def test_locate_rejects_wrong_registered_branch(tmp_path: Path) -> None:
    repo = make_repo(tmp_path / "project")
    context = locate_repository(repo)
    git(repo, "branch", FIXED_BRANCH, "main")
    git(repo, "worktree", "add", "-b", "wrong", str(context.worktree_path), "main")
    with pytest.raises(AutomationError, match="worktree_branch_mismatch"):
        locate_dedicated_workspace(context)


def test_git_runner_clears_hostile_repository_environment(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    repo = make_repo(tmp_path / "project")
    foreign = make_repo(tmp_path / "foreign")
    foreign_index = foreign / ".git" / "index"
    monkeypatch.setenv("GIT_DIR", str(foreign / ".git"))
    monkeypatch.setenv("GIT_WORK_TREE", str(foreign))
    monkeypatch.setenv("GIT_INDEX_FILE", str(foreign_index))
    result = GitRunner().run(repo, "rev-parse", "--show-toplevel")
    assert Path(result.stdout.strip()).resolve() == repo.resolve()


def test_ensure_excludes_caller_staged_and_untracked_content(tmp_path: Path) -> None:
    repo = make_repo(tmp_path / "project")
    (repo / "staged.txt").write_text("staged only\n")
    (repo / "untracked.txt").write_text("untracked only\n")
    git(repo, "add", "staged.txt")
    workspace = ensure_dedicated_workspace(locate_repository(repo))
    assert not (workspace.path / "staged.txt").exists()
    assert not (workspace.path / "untracked.txt").exists()
    assert git(repo, "diff", "--cached", "--name-only").stdout.strip() == "staged.txt"


def test_ensure_starts_from_remote_descendant(tmp_path: Path) -> None:
    repo = make_repo(tmp_path / "project")
    remote = make_bare_remote(tmp_path / "remote.git", repo)
    clone = tmp_path / "remote-change"
    git(tmp_path, "clone", str(remote), str(clone))
    git(clone, "config", "user.name", "CodexSpec Tests")
    git(clone, "config", "user.email", "tests@codexspec.invalid")
    (clone / "remote.txt").write_text("remote\n")
    git(clone, "add", "remote.txt")
    git(clone, "commit", "-m", "feat: remote")
    git(clone, "push", "origin", "main")

    workspace = ensure_dedicated_workspace(locate_repository(repo))
    assert (workspace.path / "remote.txt").read_text() == "remote\n"


def test_ensure_merges_diverged_local_and_remote_histories(tmp_path: Path) -> None:
    repo = make_repo(tmp_path / "project")
    remote = make_bare_remote(tmp_path / "remote.git", repo)
    clone = tmp_path / "remote-change"
    git(tmp_path, "clone", str(remote), str(clone))
    git(clone, "config", "user.name", "CodexSpec Tests")
    git(clone, "config", "user.email", "tests@codexspec.invalid")
    (clone / "remote.txt").write_text("remote\n")
    git(clone, "add", "remote.txt")
    git(clone, "commit", "-m", "feat: remote")
    git(clone, "push", "origin", "main")
    (repo / "local.txt").write_text("local\n")
    git(repo, "add", "local.txt")
    git(repo, "commit", "-m", "feat: local")

    workspace = ensure_dedicated_workspace(locate_repository(repo))
    assert (workspace.path / "local.txt").exists()
    assert (workspace.path / "remote.txt").exists()
    parents = git(workspace.path, "rev-list", "--parents", "-n", "1", "HEAD").stdout.split()
    assert len(parents) == 3


def test_ensure_supports_remote_default_without_matching_local_branch(tmp_path: Path) -> None:
    repo = make_repo(tmp_path / "project")
    make_bare_remote(tmp_path / "remote.git", repo)
    git(repo, "branch", "-m", "topic")
    context = locate_repository(repo)
    assert context.default_branch == "main"
    workspace = ensure_dedicated_workspace(context)
    assert git(workspace.path, "rev-parse", "HEAD").stdout == git(repo, "rev-parse", "refs/remotes/origin/main").stdout


def test_git_runner_times_out_hung_subprocess(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    repo = make_repo(tmp_path / "project")

    def hang(*args: object, **kwargs: object) -> None:
        raise __import__("subprocess").TimeoutExpired(cmd=["git"], timeout=600)

    monkeypatch.setattr("codexspec.automation.subprocess.run", hang)
    with pytest.raises(AutomationError, match="git_command_timeout"):
        GitRunner().run(repo, "status")
