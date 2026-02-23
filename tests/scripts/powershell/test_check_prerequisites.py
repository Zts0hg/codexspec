"""Tests for scripts/powershell/check-prerequisites.ps1."""

import json
import subprocess
from pathlib import Path

import pytest


@pytest.mark.skipif(
    not __import__("shutil", fromlist=["which"]).which("pwsh"),
    reason="PowerShell not available",
)
class TestCheckPrerequisites:
    """Tests for check-prerequisites.ps1 script."""

    def test_help_flag(self, powershell_scripts_dir: Path, tmp_path: Path):
        """-Help displays help message."""
        script_path = powershell_scripts_dir / "check-prerequisites.ps1"
        result = subprocess.run(
            ["pwsh", "-File", str(script_path), "-Help"],
            capture_output=True,
            text=True,
            cwd=tmp_path,
        )
        assert result.returncode == 0
        assert "Usage:" in result.stdout
        assert "-Json" in result.stdout
        assert "-RequireTasks" in result.stdout

    def test_fails_outside_feature_branch(
        self,
        powershell_scripts_dir: Path,
        temp_codexspec_git_project: Path,
    ):
        """Fails when not on a feature branch."""
        # Project is on 'main' branch by default (not a feature branch)
        script_path = powershell_scripts_dir / "check-prerequisites.ps1"
        result = subprocess.run(
            ["pwsh", "-File", str(script_path)],
            capture_output=True,
            text=True,
            cwd=temp_codexspec_git_project,
        )
        assert result.returncode != 0
        # Script should fail - either due to branch validation or missing feature dir
        assert "ERROR" in result.stdout or result.returncode != 0

    def test_fails_missing_feature_dir(
        self,
        powershell_scripts_dir: Path,
        temp_codexspec_git_project: Path,
    ):
        """Fails when feature directory is missing."""
        # Create and checkout a feature branch
        subprocess.run(
            ["git", "checkout", "-b", "001-test-feature"],
            cwd=temp_codexspec_git_project,
            check=True,
            capture_output=True,
        )

        script_path = powershell_scripts_dir / "check-prerequisites.ps1"
        result = subprocess.run(
            ["pwsh", "-File", str(script_path)],
            capture_output=True,
            text=True,
            cwd=temp_codexspec_git_project,
        )
        assert result.returncode != 0
        assert "Feature directory not found" in result.stdout

    def test_fails_missing_plan(
        self,
        powershell_scripts_dir: Path,
        temp_codexspec_git_project: Path,
    ):
        """Fails when plan.md is missing."""
        # Create feature branch and directory
        subprocess.run(
            ["git", "checkout", "-b", "002-test-feature"],
            cwd=temp_codexspec_git_project,
            check=True,
            capture_output=True,
        )
        feature_dir = temp_codexspec_git_project / ".codexspec" / "specs" / "002-test-feature"
        feature_dir.mkdir(parents=True)

        script_path = powershell_scripts_dir / "check-prerequisites.ps1"
        result = subprocess.run(
            ["pwsh", "-File", str(script_path)],
            capture_output=True,
            text=True,
            cwd=temp_codexspec_git_project,
        )
        assert result.returncode != 0
        assert "plan.md not found" in result.stdout

    def test_require_tasks_missing(
        self,
        powershell_scripts_dir: Path,
        temp_codexspec_git_project: Path,
    ):
        """Fails when -RequireTasks and tasks.md is missing."""
        # Create feature branch, directory, and plan.md
        subprocess.run(
            ["git", "checkout", "-b", "003-test-feature"],
            cwd=temp_codexspec_git_project,
            check=True,
            capture_output=True,
        )
        feature_dir = temp_codexspec_git_project / ".codexspec" / "specs" / "003-test-feature"
        feature_dir.mkdir(parents=True)
        (feature_dir / "plan.md").write_text("# Plan")

        script_path = powershell_scripts_dir / "check-prerequisites.ps1"
        result = subprocess.run(
            ["pwsh", "-File", str(script_path), "-RequireTasks"],
            capture_output=True,
            text=True,
            cwd=temp_codexspec_git_project,
        )
        assert result.returncode != 0
        assert "tasks.md not found" in result.stdout

    def test_paths_only_mode(
        self,
        powershell_scripts_dir: Path,
        temp_codexspec_git_project: Path,
    ):
        """-PathsOnly outputs paths without validation."""
        # Create and checkout a feature branch
        subprocess.run(
            ["git", "checkout", "-b", "004-test-feature"],
            cwd=temp_codexspec_git_project,
            check=True,
            capture_output=True,
        )

        script_path = powershell_scripts_dir / "check-prerequisites.ps1"
        result = subprocess.run(
            ["pwsh", "-File", str(script_path), "-PathsOnly"],
            capture_output=True,
            text=True,
            cwd=temp_codexspec_git_project,
        )
        assert result.returncode == 0
        assert "REPO_ROOT:" in result.stdout
        assert "BRANCH:" in result.stdout
        assert "FEATURE_DIR:" in result.stdout
        # Check that branch reflects our feature branch (004-test-feature)
        assert "004-test-feature" in result.stdout

    def test_paths_only_json_mode(
        self,
        powershell_scripts_dir: Path,
        temp_codexspec_git_project: Path,
    ):
        """-PathsOnly -Json outputs JSON format."""
        # Create and checkout a feature branch
        subprocess.run(
            ["git", "checkout", "-b", "005-test-feature"],
            cwd=temp_codexspec_git_project,
            check=True,
            capture_output=True,
        )

        script_path = powershell_scripts_dir / "check-prerequisites.ps1"
        result = subprocess.run(
            ["pwsh", "-File", str(script_path), "-PathsOnly", "-Json"],
            capture_output=True,
            text=True,
            cwd=temp_codexspec_git_project,
        )
        assert result.returncode == 0

        # Parse JSON output
        output = json.loads(result.stdout)
        assert "REPO_ROOT" in output
        assert "BRANCH" in output
        assert "FEATURE_DIR" in output
        # Check that branch reflects our feature branch
        assert output["BRANCH"] == "005-test-feature"

    def test_success_with_plan(
        self,
        powershell_scripts_dir: Path,
        temp_codexspec_git_project: Path,
    ):
        """Succeeds when feature dir and plan.md exist."""
        # Create feature branch, directory, and plan.md
        subprocess.run(
            ["git", "checkout", "-b", "006-test-feature"],
            cwd=temp_codexspec_git_project,
            check=True,
            capture_output=True,
        )
        feature_dir = temp_codexspec_git_project / ".codexspec" / "specs" / "006-test-feature"
        feature_dir.mkdir(parents=True)
        (feature_dir / "plan.md").write_text("# Plan")

        script_path = powershell_scripts_dir / "check-prerequisites.ps1"
        result = subprocess.run(
            ["pwsh", "-File", str(script_path)],
            capture_output=True,
            text=True,
            cwd=temp_codexspec_git_project,
        )
        assert result.returncode == 0
        assert "FEATURE_DIR:" in result.stdout
        assert "AVAILABLE_DOCS:" in result.stdout

    def test_json_output(
        self,
        powershell_scripts_dir: Path,
        temp_codexspec_git_project: Path,
    ):
        """-Json outputs valid JSON with feature info."""
        # Create feature branch, directory, and plan.md
        subprocess.run(
            ["git", "checkout", "-b", "007-test-feature"],
            cwd=temp_codexspec_git_project,
            check=True,
            capture_output=True,
        )
        feature_dir = temp_codexspec_git_project / ".codexspec" / "specs" / "007-test-feature"
        feature_dir.mkdir(parents=True)
        (feature_dir / "plan.md").write_text("# Plan")

        script_path = powershell_scripts_dir / "check-prerequisites.ps1"
        result = subprocess.run(
            ["pwsh", "-File", str(script_path), "-Json"],
            capture_output=True,
            text=True,
            cwd=temp_codexspec_git_project,
        )
        assert result.returncode == 0

        output = json.loads(result.stdout)
        assert "FEATURE_DIR" in output
        assert "AVAILABLE_DOCS" in output
        assert isinstance(output["AVAILABLE_DOCS"], list)

    def test_available_docs_list(
        self,
        powershell_scripts_dir: Path,
        temp_codexspec_git_project: Path,
    ):
        """Lists available optional documents."""
        # Create feature branch with all optional docs
        subprocess.run(
            ["git", "checkout", "-b", "008-test-feature"],
            cwd=temp_codexspec_git_project,
            check=True,
            capture_output=True,
        )
        feature_dir = temp_codexspec_git_project / ".codexspec" / "specs" / "008-test-feature"
        feature_dir.mkdir(parents=True)
        (feature_dir / "plan.md").write_text("# Plan")
        (feature_dir / "research.md").write_text("# Research")
        (feature_dir / "data-model.md").write_text("# Data Model")
        (feature_dir / "tasks.md").write_text("# Tasks")

        script_path = powershell_scripts_dir / "check-prerequisites.ps1"
        result = subprocess.run(
            ["pwsh", "-File", str(script_path), "-Json", "-IncludeTasks"],
            capture_output=True,
            text=True,
            cwd=temp_codexspec_git_project,
        )
        assert result.returncode == 0

        output = json.loads(result.stdout)
        assert "research.md" in output["AVAILABLE_DOCS"]
        assert "data-model.md" in output["AVAILABLE_DOCS"]
        assert "tasks.md" in output["AVAILABLE_DOCS"]
