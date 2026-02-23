"""Common fixtures for script tests."""

import shutil
import subprocess
from pathlib import Path
from typing import Generator

import pytest


@pytest.fixture
def scripts_dir() -> Path:
    """Get the scripts source directory."""
    return Path(__file__).parent.parent.parent / "scripts"


@pytest.fixture
def temp_codexspec_project(tmp_path: Path) -> Generator[Path, None, None]:
    """Create a temporary CodexSpec project structure."""
    project = tmp_path / "test-project"
    project.mkdir()
    (project / ".codexspec").mkdir()
    (project / ".codexspec" / "specs").mkdir()
    (project / ".codexspec" / "config.yml").write_text("version: '1.0'\n")
    yield project


@pytest.fixture
def temp_git_repo(tmp_path: Path) -> Generator[Path, None, None]:
    """Create a temporary git repository with basic configuration and initial commit."""
    repo = tmp_path / "git-repo"
    repo.mkdir()
    subprocess.run(["git", "init"], cwd=repo, check=True, capture_output=True)
    subprocess.run(
        ["git", "config", "user.email", "test@example.com"],
        cwd=repo,
        check=True,
        capture_output=True,
    )
    subprocess.run(
        ["git", "config", "user.name", "Test User"],
        cwd=repo,
        check=True,
        capture_output=True,
    )
    # Set default branch name to main for consistency
    subprocess.run(
        ["git", "checkout", "-b", "main"],
        cwd=repo,
        check=True,
        capture_output=True,
    )
    # Create initial commit so git branch operations work properly
    subprocess.run(
        ["git", "commit", "--allow-empty", "-m", "Initial commit"],
        cwd=repo,
        check=True,
        capture_output=True,
    )
    yield repo


@pytest.fixture
def temp_codexspec_git_project(
    tmp_path: Path,
) -> Generator[Path, None, None]:
    """Create a temporary CodexSpec project with git initialized and initial commit."""
    project = tmp_path / "test-git-project"
    project.mkdir()
    (project / ".codexspec").mkdir()
    (project / ".codexspec" / "specs").mkdir()
    (project / ".codexspec" / "config.yml").write_text("version: '1.0'\n")
    subprocess.run(["git", "init"], cwd=project, check=True, capture_output=True)
    subprocess.run(
        ["git", "config", "user.email", "test@example.com"],
        cwd=project,
        check=True,
        capture_output=True,
    )
    subprocess.run(
        ["git", "config", "user.name", "Test User"],
        cwd=project,
        check=True,
        capture_output=True,
    )
    # Set default branch name to main for consistency
    subprocess.run(
        ["git", "checkout", "-b", "main"],
        cwd=project,
        check=True,
        capture_output=True,
    )
    # Create initial commit so git branch operations work properly
    subprocess.run(
        ["git", "commit", "--allow-empty", "-m", "Initial commit"],
        cwd=project,
        check=True,
        capture_output=True,
    )
    yield project


@pytest.fixture
def pwsh_available() -> bool:
    """Check if PowerShell is available."""
    return shutil.which("pwsh") is not None
