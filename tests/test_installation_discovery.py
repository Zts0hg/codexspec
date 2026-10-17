import os
import subprocess

import pytest

from codexspec.installations.discovery import discover


def test_t03_s01_s04_s06_recursive_readonly(tmp_path, monkeypatch):
    import httpx

    monkeypatch.setattr(httpx, "get", lambda *a, **k: pytest.fail("scan used network"))
    names = [".codexspec", ".hidden/.codexspec", "nested/.codexspec", "nested/child/.codexspec"]
    for name in names:
        (tmp_path / name).mkdir(parents=True)
    (tmp_path / ".git/cache/.codexspec").mkdir(parents=True)
    (tmp_path / ".codexspec/specs/.codexspec").mkdir(parents=True)
    before = sorted(str(p.relative_to(tmp_path)) for p in tmp_path.rglob("*"))
    result = discover(tmp_path)
    assert len(result.installations) == 4
    assert all(
        item.inspection.version is None and item.inspection.state == "no_baseline" for item in result.installations
    )
    assert sorted(str(p.relative_to(tmp_path)) for p in tmp_path.rglob("*")) == before
    assert not result.issues


def test_t03_s02_links_not_followed(tmp_path):
    outside = tmp_path / "outside"
    (outside / ".codexspec").mkdir(parents=True)
    root = tmp_path / "root"
    root.mkdir()
    try:
        (root / "link").symlink_to(outside, target_is_directory=True)
        (root / ".codexspec").symlink_to(outside / ".codexspec", target_is_directory=True)
    except OSError:
        pytest.skip("symlinks unavailable")
    result = discover(root)
    assert result.installations == []
    assert result.issues


def test_t03_s03_worktrees_grouped_within_scope(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()

    def git(*args):
        return subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True)

    git("init")
    git("-c", "user.name=Test", "-c", "user.email=test@example.invalid", "commit", "--allow-empty", "-m", "initial")
    worktree = tmp_path / "worktree"
    git("worktree", "add", "-b", "feature", str(worktree))
    for path in [repo, worktree]:
        (path / ".codexspec").mkdir()
    result = discover(tmp_path)
    assert len(result.installations) == 2
    assert result.installations[0].repository == result.installations[1].repository
    assert len(discover(repo).installations) == 1


def test_t03_s05_invalid_root_and_unreadable_child(tmp_path, monkeypatch):
    with pytest.raises(ValueError):
        discover(tmp_path / "missing")
    bad = tmp_path / "bad"
    bad.mkdir()
    (tmp_path / "good/.codexspec").mkdir(parents=True)
    original = os.scandir

    def scan(path):
        if path == bad:
            raise PermissionError("denied")
        return original(path)

    monkeypatch.setattr(os, "scandir", scan)
    result = discover(tmp_path)
    assert len(result.installations) == 1
    assert len(result.issues) == 1
    assert "bad" in result.issues[0]


def test_t03_s05_unreadable_root_fails(tmp_path, monkeypatch):
    monkeypatch.setattr(os, "scandir", lambda *a: (_ for _ in ()).throw(PermissionError("denied")))
    with pytest.raises(ValueError, match="root"):
        discover(tmp_path)


def test_t03_s02_root_through_symlink_ancestor_rejected(tmp_path):
    (tmp_path / "real/child/.codexspec").mkdir(parents=True)
    link = tmp_path / "link"
    try:
        link.symlink_to(tmp_path / "real", target_is_directory=True)
    except OSError:
        pytest.skip("symlinks unavailable")
    with pytest.raises(ValueError):
        discover(link / "child")


def test_t03_s04_git_timeout_keeps_installations_visible(tmp_path, monkeypatch):
    from codexspec.commit_runtime import AutomationError
    from codexspec.installations import discovery

    (tmp_path / ".codexspec").mkdir()
    monkeypatch.setattr(discovery, "GitRunner", lambda: (_ for _ in ()).throw(AutomationError("git_command_timeout")))
    result = discover(tmp_path)
    assert len(result.installations) == 1
    assert result.installations[0].repository is None
