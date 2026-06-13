"""Tests for scripts/powershell/create-new-feature.ps1."""

import json
import re
import subprocess
import sys
from pathlib import Path

import pytest


@pytest.mark.skipif(
    sys.platform != "win32",
    reason="PowerShell tests only run on Windows",
)
class TestCreateNewFeature:
    """Tests for create-new-feature.ps1 script."""

    def test_help_flag(self, powershell_scripts_dir: Path, tmp_path: Path):
        """-Help displays the current command interface."""
        script_path = powershell_scripts_dir / "create-new-feature.ps1"
        result = subprocess.run(
            ["pwsh", "-File", str(script_path), "-Help"],
            capture_output=True,
            text=True,
            cwd=tmp_path,
        )
        assert result.returncode == 0
        assert "Usage:" in result.stdout
        assert "-Json" in result.stdout
        assert "-ShortName" in result.stdout

    def test_requires_description(self, powershell_scripts_dir: Path, tmp_path: Path):
        """Reports error when description is missing."""
        script_path = powershell_scripts_dir / "create-new-feature.ps1"
        result = subprocess.run(
            ["pwsh", "-File", str(script_path)],
            capture_output=True,
            text=True,
            cwd=tmp_path,
        )
        assert result.returncode != 0

    def test_creates_timestamp_feature_dir(
        self,
        powershell_scripts_dir: Path,
        temp_codexspec_project: Path,
    ):
        """Creates a feature directory using the timestamp contract."""
        script_path = powershell_scripts_dir / "create-new-feature.ps1"
        result = subprocess.run(
            ["pwsh", "-File", str(script_path), "user authentication"],
            capture_output=True,
            text=True,
            cwd=temp_codexspec_project,
        )
        assert result.returncode == 0

        specs_dir = temp_codexspec_project / ".codexspec" / "specs"
        feature_dirs = list(specs_dir.glob("20??-????-??????-user-authentication"))
        assert len(feature_dirs) == 1
        assert (feature_dirs[0] / "requirements.md").exists()

    def test_json_output(self, powershell_scripts_dir: Path, temp_codexspec_project: Path):
        """-Json outputs the generated feature ID and paths."""
        script_path = powershell_scripts_dir / "create-new-feature.ps1"
        result = subprocess.run(
            ["pwsh", "-File", str(script_path), "-Json", "json test feature"],
            capture_output=True,
            text=True,
            cwd=temp_codexspec_project,
        )
        assert result.returncode == 0

        output = json.loads(result.stdout)
        assert re.fullmatch(r"\d{4}-\d{4}-\d{4}[a-z0-9]{2}", output["FEATURE_ID"])
        assert output["BRANCH_NAME"].startswith(f"{output['FEATURE_ID']}-")
        assert "REQUIREMENTS_FILE" in output
        assert "SPEC_FILE" in output

    def test_short_name(self, powershell_scripts_dir: Path, temp_codexspec_project: Path):
        """-ShortName provides the branch suffix."""
        script_path = powershell_scripts_dir / "create-new-feature.ps1"
        result = subprocess.run(
            [
                "pwsh",
                "-File",
                str(script_path),
                "-ShortName",
                "custom-auth",
                "user authentication system",
            ],
            capture_output=True,
            text=True,
            cwd=temp_codexspec_project,
        )
        assert result.returncode == 0
        branch_line = next(line for line in result.stdout.splitlines() if line.startswith("BRANCH_NAME:"))
        assert re.search(
            r"\d{4}-\d{4}-\d{4}[a-z0-9]{2}-custom-auth$",
            branch_line,
        )

    def test_creates_git_branch(
        self,
        powershell_scripts_dir: Path,
        temp_codexspec_git_project: Path,
    ):
        """Creates and checks out the generated feature branch."""
        script_path = powershell_scripts_dir / "create-new-feature.ps1"
        result = subprocess.run(
            ["pwsh", "-File", str(script_path), "git test feature"],
            capture_output=True,
            text=True,
            cwd=temp_codexspec_git_project,
        )
        assert result.returncode == 0

        branch_result = subprocess.run(
            ["git", "branch", "--show-current"],
            capture_output=True,
            text=True,
            cwd=temp_codexspec_git_project,
        )
        assert re.fullmatch(
            r"\d{4}-\d{4}-\d{4}[a-z0-9]{2}-git-test-feature\n?",
            branch_result.stdout,
        )

    def test_output_contains_feature_id(
        self,
        powershell_scripts_dir: Path,
        temp_codexspec_project: Path,
    ):
        """Text output includes the generated feature ID."""
        script_path = powershell_scripts_dir / "create-new-feature.ps1"
        result = subprocess.run(
            ["pwsh", "-File", str(script_path), "output test"],
            capture_output=True,
            text=True,
            cwd=temp_codexspec_project,
        )
        assert result.returncode == 0
        assert "BRANCH_NAME:" in result.stdout
        assert "REQUIREMENTS_FILE:" in result.stdout
        assert "SPEC_FILE:" in result.stdout
        assert re.search(
            r"FEATURE_ID: \d{4}-\d{4}-\d{4}[a-z0-9]{2}",
            result.stdout,
        )

    def test_truncates_long_branch_name(
        self,
        powershell_scripts_dir: Path,
        temp_codexspec_project: Path,
    ):
        """Truncation reserves space for the complete timestamp ID."""
        script_path = powershell_scripts_dir / "create-new-feature.ps1"
        long_short_name = "a" * 300
        result = subprocess.run(
            [
                "pwsh",
                "-File",
                str(script_path),
                "-ShortName",
                long_short_name,
                "long feature",
            ],
            capture_output=True,
            text=True,
            cwd=temp_codexspec_project,
        )
        assert result.returncode == 0
        branch_line = next(line for line in result.stdout.splitlines() if line.startswith("BRANCH_NAME:"))
        branch_name = branch_line.split(": ", 1)[1]
        assert len(branch_name) <= 244
