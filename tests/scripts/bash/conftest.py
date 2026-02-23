"""Bash-specific fixtures for script tests."""

import os
import subprocess
from pathlib import Path
from typing import Generator

import pytest


@pytest.fixture
def bash_scripts_dir(scripts_dir: Path) -> Path:
    """Get the bash scripts directory."""
    return scripts_dir / "bash"


@pytest.fixture
def run_bash_script():
    """Execute a Bash script and return the result."""

    def _run(
        script_path: Path,
        args: list[str] = None,
        cwd: Path = None,
        env: dict = None,
    ) -> subprocess.CompletedProcess:
        cmd = ["bash", str(script_path)]
        if args:
            cmd.extend(args)
        run_env = os.environ.copy()
        if env:
            run_env.update(env)
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=cwd, env=run_env)
        return result

    return _run


@pytest.fixture
def temp_bash_test_env(tmp_path: Path, bash_scripts_dir: Path) -> Generator[Path, None, None]:
    """Create a temporary directory for testing bash scripts."""
    test_env = tmp_path / "bash-test-env"
    test_env.mkdir()
    yield test_env


@pytest.fixture
def create_test_script(tmp_path: Path, bash_scripts_dir: Path):
    """Create a test script that sources common.sh and runs commands."""

    def _create(content: str, cwd: Path = None) -> Path:
        script_dir = cwd if cwd else tmp_path
        test_script = script_dir / "test_runner.sh"
        test_script.write_text(f"""#!/bin/bash
source "{bash_scripts_dir}/common.sh"
{content}
""")
        return test_script

    return _create
