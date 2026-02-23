"""PowerShell-specific fixtures for script tests."""

import subprocess
from pathlib import Path
from typing import Generator

import pytest


@pytest.fixture
def powershell_scripts_dir(scripts_dir: Path) -> Path:
    """Get the PowerShell scripts directory."""
    return scripts_dir / "powershell"


@pytest.fixture
def run_powershell_script(pwsh_available: bool):
    """Execute a PowerShell script and return the result."""

    def _run(
        script_path: Path,
        args: list[str] = None,
        cwd: Path = None,
        env: dict = None,
    ) -> subprocess.CompletedProcess:
        if not pwsh_available:
            pytest.skip("PowerShell not available")
        cmd = ["pwsh", "-File", str(script_path)]
        if args:
            cmd.extend(args)
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=cwd)
        return result

    return _run


@pytest.fixture
def run_powershell_command(pwsh_available: bool):
    """Execute a PowerShell command string and return the result."""

    def _run(command: str, cwd: Path = None) -> subprocess.CompletedProcess:
        if not pwsh_available:
            pytest.skip("PowerShell not available")
        cmd = ["pwsh", "-Command", command]
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=cwd)
        return result

    return _run


@pytest.fixture
def temp_powershell_test_env(tmp_path: Path, powershell_scripts_dir: Path) -> Generator[Path, None, None]:
    """Create a temporary directory for testing PowerShell scripts."""
    test_env = tmp_path / "pwsh-test-env"
    test_env.mkdir()
    yield test_env
