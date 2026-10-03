"""Shared deterministic Git fixtures for automation tests."""

from __future__ import annotations

import os
import subprocess
from pathlib import Path

_FALLBACK_GIT_LOCAL_ENV_VARS = {
    "GIT_CONFIG",
    "GIT_CONFIG_PARAMETERS",
    "GIT_CONFIG_COUNT",
    "GIT_DIR",
    "GIT_WORK_TREE",
    "GIT_IMPLICIT_WORK_TREE",
    "GIT_INDEX_FILE",
    "GIT_OBJECT_DIRECTORY",
    "GIT_ALTERNATE_OBJECT_DIRECTORIES",
    "GIT_COMMON_DIR",
    "GIT_GRAFT_FILE",
    "GIT_NO_REPLACE_OBJECTS",
    "GIT_REPLACE_REF_BASE",
    "GIT_PREFIX",
    "GIT_INTERNAL_SUPER_PREFIX",
    "GIT_SHALLOW_FILE",
}


def _git_local_environment_variables() -> frozenset[str]:
    discovery_environment = os.environ.copy()
    for name in _FALLBACK_GIT_LOCAL_ENV_VARS:
        discovery_environment.pop(name, None)
    result = subprocess.run(
        ["git", "rev-parse", "--local-env-vars"],
        check=False,
        capture_output=True,
        text=True,
        env=discovery_environment,
    )
    reported = set(result.stdout.split()) if result.returncode == 0 else set()
    return frozenset(_FALLBACK_GIT_LOCAL_ENV_VARS | reported)


def sanitized_git_env() -> dict[str, str]:
    """Caller-local Git variables break nested repositories (see P-2026-0829-0035hy-1)."""
    env = os.environ.copy()
    for name in _git_local_environment_variables():
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
