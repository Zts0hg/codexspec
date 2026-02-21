"""Pytest configuration and fixtures for CodexSpec tests."""

import os
from pathlib import Path
from typing import Generator

import pytest


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
