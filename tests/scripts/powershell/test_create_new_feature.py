"""Tests for scripts/powershell/create-new-feature.ps1."""

import json
import subprocess
from pathlib import Path

import pytest


@pytest.mark.skipif(
    not __import__("shutil", fromlist=["which"]).which("pwsh"),
    reason="PowerShell not available",
)
class TestCreateNewFeature:
    """Tests for create-new-feature.ps1 script."""

    def test_help_flag(self, powershell_scripts_dir: Path, tmp_path: Path):
        """-Help displays help message."""
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
        assert "-Number" in result.stdout

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

    def test_creates_feature_dir(self, powershell_scripts_dir: Path, temp_codexspec_project: Path):
        """Creates feature directory with correct name."""
        script_path = powershell_scripts_dir / "create-new-feature.ps1"
        # Use -Command to properly pass multi-word argument
        cmd = f"& '{script_path}' 'user authentication'"
        result = subprocess.run(
            ["pwsh", "-Command", cmd],
            capture_output=True,
            text=True,
            cwd=temp_codexspec_project,
        )
        assert result.returncode == 0

        # Check feature directory was created
        specs_dir = temp_codexspec_project / ".codexspec" / "specs"
        feature_dirs = list(specs_dir.glob("001-*"))
        assert len(feature_dirs) == 1

    def test_creates_spec_file(self, powershell_scripts_dir: Path, temp_codexspec_project: Path):
        """Creates spec.md file in feature directory."""
        script_path = powershell_scripts_dir / "create-new-feature.ps1"
        cmd = f"& '{script_path}' 'test feature'"
        result = subprocess.run(
            ["pwsh", "-Command", cmd],
            capture_output=True,
            text=True,
            cwd=temp_codexspec_project,
        )
        assert result.returncode == 0

        # Check spec.md was created
        specs_dir = temp_codexspec_project / ".codexspec" / "specs"
        spec_file = list(specs_dir.glob("001-*/spec.md"))
        assert len(spec_file) == 1
        assert spec_file[0].exists()

    def test_auto_number_first(self, powershell_scripts_dir: Path, temp_codexspec_project: Path):
        """First feature gets number 001."""
        script_path = powershell_scripts_dir / "create-new-feature.ps1"
        cmd = f"& '{script_path}' 'first feature'"
        result = subprocess.run(
            ["pwsh", "-Command", cmd],
            capture_output=True,
            text=True,
            cwd=temp_codexspec_project,
        )
        assert result.returncode == 0
        assert "FEATURE_NUM: 001" in result.stdout

    def test_auto_number_increment(self, powershell_scripts_dir: Path, temp_codexspec_project: Path):
        """Feature numbers increment automatically."""
        script_path = powershell_scripts_dir / "create-new-feature.ps1"

        # Create first feature
        cmd1 = f"& '{script_path}' 'first feature'"
        result1 = subprocess.run(
            ["pwsh", "-Command", cmd1],
            capture_output=True,
            text=True,
            cwd=temp_codexspec_project,
        )
        assert result1.returncode == 0
        assert "FEATURE_NUM: 001" in result1.stdout

        # Create second feature
        cmd2 = f"& '{script_path}' 'second feature'"
        result2 = subprocess.run(
            ["pwsh", "-Command", cmd2],
            capture_output=True,
            text=True,
            cwd=temp_codexspec_project,
        )
        assert result2.returncode == 0
        assert "FEATURE_NUM: 002" in result2.stdout

    def test_custom_number(self, powershell_scripts_dir: Path, temp_codexspec_project: Path):
        """Custom number can be specified with -Number parameter."""
        script_path = powershell_scripts_dir / "create-new-feature.ps1"
        cmd = f"& '{script_path}' -Number 42 'custom feature'"
        result = subprocess.run(
            ["pwsh", "-Command", cmd],
            capture_output=True,
            text=True,
            cwd=temp_codexspec_project,
        )
        assert result.returncode == 0
        assert "FEATURE_NUM: 042" in result.stdout

        # Check directory name
        specs_dir = temp_codexspec_project / ".codexspec" / "specs"
        assert any("042-" in d.name for d in specs_dir.iterdir())

    def test_json_output(self, powershell_scripts_dir: Path, temp_codexspec_project: Path):
        """-Json outputs valid JSON format."""
        script_path = powershell_scripts_dir / "create-new-feature.ps1"
        cmd = f"& '{script_path}' -Json 'json test feature'"
        result = subprocess.run(
            ["pwsh", "-Command", cmd],
            capture_output=True,
            text=True,
            cwd=temp_codexspec_project,
        )
        assert result.returncode == 0

        output = json.loads(result.stdout)
        assert "BRANCH_NAME" in output
        assert "SPEC_FILE" in output
        assert "FEATURE_NUM" in output
        assert output["FEATURE_NUM"] == "001"

    def test_short_name(self, powershell_scripts_dir: Path, temp_codexspec_project: Path):
        """-ShortName parameter provides custom branch suffix."""
        script_path = powershell_scripts_dir / "create-new-feature.ps1"
        cmd = f"& '{script_path}' -ShortName custom-auth 'user authentication system'"
        result = subprocess.run(
            ["pwsh", "-Command", cmd],
            capture_output=True,
            text=True,
            cwd=temp_codexspec_project,
        )
        assert result.returncode == 0
        assert "BRANCH_NAME:" in result.stdout
        assert "custom-auth" in result.stdout

    def test_branch_name_from_description(self, powershell_scripts_dir: Path, temp_codexspec_project: Path):
        """Branch name is generated from description."""
        script_path = powershell_scripts_dir / "create-new-feature.ps1"
        cmd = f"& '{script_path}' 'Add user authentication'"
        result = subprocess.run(
            ["pwsh", "-Command", cmd],
            capture_output=True,
            text=True,
            cwd=temp_codexspec_project,
        )
        assert result.returncode == 0
        assert "BRANCH_NAME:" in result.stdout
        # Branch name should contain meaningful words from description
        branch_line = [line for line in result.stdout.split("\n") if "BRANCH_NAME:" in line][0]
        # Check that the branch contains user or auth related words
        assert any(word in branch_line.lower() for word in ["user", "auth"])

    def test_creates_git_branch(self, powershell_scripts_dir: Path, temp_codexspec_git_project: Path):
        """Creates git branch when in a git repository."""
        script_path = powershell_scripts_dir / "create-new-feature.ps1"
        cmd = f"& '{script_path}' 'git test feature'"
        result = subprocess.run(
            ["pwsh", "-Command", cmd],
            capture_output=True,
            text=True,
            cwd=temp_codexspec_git_project,
        )
        assert result.returncode == 0

        # Check git branch was created
        branch_result = subprocess.run(
            ["git", "branch", "--list", "001-*"],
            capture_output=True,
            text=True,
            cwd=temp_codexspec_git_project,
        )
        # Branch name might differ due to word extraction
        assert branch_result.stdout.strip() != ""

    def test_no_git_warning(self, powershell_scripts_dir: Path, temp_codexspec_project: Path):
        """Warns when git is not available but still creates feature."""
        script_path = powershell_scripts_dir / "create-new-feature.ps1"
        cmd = f"& '{script_path}' 'no git feature'"
        result = subprocess.run(
            ["pwsh", "-Command", cmd],
            capture_output=True,
            text=True,
            cwd=temp_codexspec_project,
        )
        assert result.returncode == 0
        assert "HAS_GIT:" in result.stdout

    def test_output_contains_branch_name(self, powershell_scripts_dir: Path, temp_codexspec_project: Path):
        """Output contains BRANCH_NAME."""
        script_path = powershell_scripts_dir / "create-new-feature.ps1"
        cmd = f"& '{script_path}' 'output test'"
        result = subprocess.run(
            ["pwsh", "-Command", cmd],
            capture_output=True,
            text=True,
            cwd=temp_codexspec_project,
        )
        assert result.returncode == 0
        assert "BRANCH_NAME:" in result.stdout
        assert "SPEC_FILE:" in result.stdout
        assert "FEATURE_NUM:" in result.stdout

    def test_existing_spec_directories_increment(self, powershell_scripts_dir: Path, temp_codexspec_project: Path):
        """Number increments based on existing spec directories."""
        script_path = powershell_scripts_dir / "create-new-feature.ps1"

        # Create a feature with explicit number 010
        cmd1 = f"& '{script_path}' -Number 10 'tenth feature'"
        result1 = subprocess.run(
            ["pwsh", "-Command", cmd1],
            capture_output=True,
            text=True,
            cwd=temp_codexspec_project,
        )
        assert result1.returncode == 0

        # Next feature should be 011
        cmd2 = f"& '{script_path}' 'next feature'"
        result2 = subprocess.run(
            ["pwsh", "-Command", cmd2],
            capture_output=True,
            text=True,
            cwd=temp_codexspec_project,
        )
        assert result2.returncode == 0
        assert "FEATURE_NUM: 011" in result2.stdout

    def test_truncates_long_branch_name(self, powershell_scripts_dir: Path, temp_codexspec_project: Path):
        """Truncates branch names that exceed GitHub's limit."""
        script_path = powershell_scripts_dir / "create-new-feature.ps1"
        long_description = (
            "This is a very long feature description that should result in "
            "a branch name that needs to be truncated to fit within GitHub limits"
        )
        cmd = f"& '{script_path}' '{long_description}'"
        result = subprocess.run(
            ["pwsh", "-Command", cmd],
            capture_output=True,
            text=True,
            cwd=temp_codexspec_project,
        )
        assert result.returncode == 0
        # Branch name should be created (may be truncated)
        assert "BRANCH_NAME:" in result.stdout
