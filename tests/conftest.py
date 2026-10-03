"""Pytest configuration and fixtures for CodexSpec tests."""

import os
from pathlib import Path
from typing import Generator

import pytest


@pytest.fixture(scope="session")
def isolated_git_config(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """Require fixtures to supply identity instead of borrowing it from the host."""
    config = tmp_path_factory.mktemp("git-config") / "config"
    config.write_text("[user]\n\tuseConfigOnly = true\n", encoding="utf-8")
    return config


@pytest.fixture(autouse=True)
def isolate_git_identity(isolated_git_config: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Apply the same Git identity boundary to direct pytest, hooks and CI."""
    monkeypatch.setenv("GIT_CONFIG_GLOBAL", str(isolated_git_config))
    monkeypatch.setenv("GIT_CONFIG_NOSYSTEM", "1")
    for name in ("GIT_AUTHOR_NAME", "GIT_AUTHOR_EMAIL", "GIT_COMMITTER_NAME", "GIT_COMMITTER_EMAIL", "EMAIL"):
        monkeypatch.delenv(name, raising=False)


@pytest.fixture
def temp_project_dir(tmp_path: Path) -> Generator[Path, None, None]:
    """Create a temporary directory for testing project initialization."""
    project_dir = tmp_path / "test_project"
    project_dir.mkdir()
    yield project_dir


@pytest.fixture
def clean_env() -> Generator[None, None, None]:
    """Clean environment variables that might affect tests."""
    env_vars_to_clean = [
        "CODEXSPEC_LANG",
        "LANG",
    ]
    original_values = {}

    for var in env_vars_to_clean:
        if var in os.environ:
            original_values[var] = os.environ[var]
            del os.environ[var]

    yield

    # Restore original values
    for var in env_vars_to_clean:
        if var in original_values:
            os.environ[var] = original_values[var]
        elif var in os.environ:
            del os.environ[var]
