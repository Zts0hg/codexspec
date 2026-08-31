"""Shared deterministic Git fixtures for automation tests."""

from __future__ import annotations

import os
import subprocess
from pathlib import Path

_GIT_LOCAL_ENV_VARS = (
    "GIT_DIR",
    "GIT_WORK_TREE",
    "GIT_INDEX_FILE",
    "GIT_OBJECT_DIRECTORY",
    "GIT_ALTERNATE_OBJECT_DIRECTORIES",
    "GIT_COMMON_DIR",
)


def sanitized_git_env() -> dict[str, str]:
    """Caller-local Git variables break nested repositories (see P-2026-0829-0035hy-1)."""
    env = os.environ.copy()
    for name in _GIT_LOCAL_ENV_VARS:
        env.pop(name, None)
    return env


def git(repo: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        check=check,
        capture_output=True,
        text=True,
        env=sanitized_git_env(),
    )


def make_repo(path: Path) -> Path:
    path.mkdir()
    # Route setup through the sanitized env too: under `git commit` the hook
    # environment exports GIT_INDEX_FILE etc. that would poison nested repos.
    subprocess.run(
        ["git", "init", "-b", "main", str(path)],
        check=True,
        capture_output=True,
        env=sanitized_git_env(),
    )
    git(path, "config", "user.name", "CodexSpec Tests")
    git(path, "config", "user.email", "tests@codexspec.invalid")
    (path / "README.md").write_text("initial\n")
    git(path, "add", "README.md")
    git(path, "commit", "-m", "chore: initial")
    return path


def make_bare_remote(path: Path, source: Path) -> Path:
    subprocess.run(
        ["git", "clone", "--bare", str(source), str(path)],
        check=True,
        capture_output=True,
        env=sanitized_git_env(),
    )
    git(source, "remote", "add", "origin", str(path))
    git(source, "fetch", "origin")
    git(source, "remote", "set-head", "origin", "main")
    return path
