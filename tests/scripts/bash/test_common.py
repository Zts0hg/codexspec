"""Tests for scripts/bash/common.sh."""

import subprocess
import sys
from pathlib import Path

import pytest


@pytest.mark.skipif(
    sys.platform == "win32",
    reason="Bash tests only run on Unix-like systems (macOS/Linux)",
)
class TestLoggingFunctions:
    """Tests for logging functions."""

    def test_log_info_output(self, bash_scripts_dir: Path, tmp_path: Path):
        """log_info output contains [INFO]."""
        test_script = tmp_path / "test_log.sh"
        test_script.write_text(f'''
source "{bash_scripts_dir}/common.sh"
log_info "test message"
''')
        result = subprocess.run(["bash", str(test_script)], capture_output=True, text=True)
        assert "[INFO]" in result.stdout
        assert "test message" in result.stdout

    def test_log_success_output(self, bash_scripts_dir: Path, tmp_path: Path):
        """log_success output contains [SUCCESS]."""
        test_script = tmp_path / "test_log.sh"
        test_script.write_text(f'''
source "{bash_scripts_dir}/common.sh"
log_success "operation completed"
''')
        result = subprocess.run(["bash", str(test_script)], capture_output=True, text=True)
        assert "[SUCCESS]" in result.stdout
        assert "operation completed" in result.stdout

    def test_log_warning_output(self, bash_scripts_dir: Path, tmp_path: Path):
        """log_warning output contains [WARNING]."""
        test_script = tmp_path / "test_log.sh"
        test_script.write_text(f'''
source "{bash_scripts_dir}/common.sh"
log_warning "be careful"
''')
        result = subprocess.run(["bash", str(test_script)], capture_output=True, text=True)
        assert "[WARNING]" in result.stdout
        assert "be careful" in result.stdout

    def test_log_error_output(self, bash_scripts_dir: Path, tmp_path: Path):
        """log_error output contains [ERROR]."""
        test_script = tmp_path / "test_log.sh"
        test_script.write_text(f'''
source "{bash_scripts_dir}/common.sh"
log_error "something went wrong"
''')
        result = subprocess.run(["bash", str(test_script)], capture_output=True, text=True)
        assert "[ERROR]" in result.stdout
        assert "something went wrong" in result.stdout


@pytest.mark.skipif(
    sys.platform == "win32",
    reason="Bash tests only run on Unix-like systems (macOS/Linux)",
)
class TestCommandExists:
    """Tests for command_exists function."""

    def test_command_exists_true(self, bash_scripts_dir: Path, tmp_path: Path):
        """Existing command returns true."""
        test_script = tmp_path / "test_cmd.sh"
        test_script.write_text(f'''
source "{bash_scripts_dir}/common.sh"
if command_exists bash; then
    echo "FOUND"
fi
''')
        result = subprocess.run(["bash", str(test_script)], capture_output=True, text=True)
        assert "FOUND" in result.stdout

    def test_command_exists_false(self, bash_scripts_dir: Path, tmp_path: Path):
        """Non-existing command returns false."""
        test_script = tmp_path / "test_cmd.sh"
        test_script.write_text(f'''
source "{bash_scripts_dir}/common.sh"
if ! command_exists nonexistent_command_12345; then
    echo "NOT_FOUND"
fi
''')
        result = subprocess.run(["bash", str(test_script)], capture_output=True, text=True)
        assert "NOT_FOUND" in result.stdout


@pytest.mark.skipif(
    sys.platform == "win32",
    reason="Bash tests only run on Unix-like systems (macOS/Linux)",
)
class TestGetFeatureId:
    """Tests for get_feature_id function."""

    def test_get_feature_id_from_env(self, bash_scripts_dir: Path, tmp_path: Path):
        """Get feature ID from environment variable."""
        test_script = tmp_path / "test_feature.sh"
        test_script.write_text(f'''
source "{bash_scripts_dir}/common.sh"
echo "$(get_feature_id)"
''')
        result = subprocess.run(
            ["bash", str(test_script)],
            capture_output=True,
            text=True,
            env={"SPECIFY_FEATURE": "001-test-feature"},
        )
        assert "001-test-feature" in result.stdout

    def test_get_feature_id_from_branch(self, bash_scripts_dir: Path, temp_git_repo: Path):
        """Get feature ID from git branch."""
        # Create initial commit on master/main first (required for git to track branches)
        subprocess.run(
            ["git", "commit", "--allow-empty", "-m", "Initial commit"],
            cwd=temp_git_repo,
            check=True,
            capture_output=True,
        )
        # Create and checkout a feature branch
        subprocess.run(
            ["git", "checkout", "-b", "005-my-feature"],
            cwd=temp_git_repo,
            check=True,
            capture_output=True,
        )

        test_script = temp_git_repo / "test_feature.sh"
        # Script needs to change to the git repo directory first
        test_script.write_text(f'''#!/bin/bash
cd "{temp_git_repo}"
source "{bash_scripts_dir}/common.sh"
echo "$(get_feature_id)"
''')
        result = subprocess.run(
            ["bash", str(test_script)],
            capture_output=True,
            text=True,
        )
        assert "005-my-feature" in result.stdout

    def test_get_feature_id_empty(self, bash_scripts_dir: Path, tmp_path: Path):
        """Return empty when no feature is available."""
        test_script = tmp_path / "test_feature.sh"
        test_script.write_text(f'''
source "{bash_scripts_dir}/common.sh"
result="$(get_feature_id)"
if [ -z "$result" ]; then
    echo "EMPTY"
fi
''')
        result = subprocess.run(["bash", str(test_script)], capture_output=True, text=True)
        assert "EMPTY" in result.stdout


@pytest.mark.skipif(
    sys.platform == "win32",
    reason="Bash tests only run on Unix-like systems (macOS/Linux)",
)
class TestGetSpecsDir:
    """Tests for get_specs_dir function."""

    def test_get_specs_dir_default(self, bash_scripts_dir: Path, tmp_path: Path):
        """Default specs directory path."""
        test_script = tmp_path / "test_specs.sh"
        test_script.write_text(f'''
source "{bash_scripts_dir}/common.sh"
echo "$(get_specs_dir)"
''')
        result = subprocess.run(["bash", str(test_script)], capture_output=True, text=True)
        assert "/.codexspec/specs" in result.stdout

    def test_get_specs_dir_custom(self, bash_scripts_dir: Path, tmp_path: Path):
        """Custom base directory for specs."""
        test_script = tmp_path / "test_specs.sh"
        test_script.write_text(f'''
source "{bash_scripts_dir}/common.sh"
echo "$(get_specs_dir "/custom/path")"
''')
        result = subprocess.run(["bash", str(test_script)], capture_output=True, text=True)
        assert "/custom/path/.codexspec/specs" in result.stdout


@pytest.mark.skipif(
    sys.platform == "win32",
    reason="Bash tests only run on Unix-like systems (macOS/Linux)",
)
class TestIsCodexspecProject:
    """Tests for is_codexspec_project function."""

    def test_is_codexspec_project_true(self, bash_scripts_dir: Path, temp_codexspec_project: Path):
        """Return true when in a CodexSpec project."""
        test_script = temp_codexspec_project / "test_project.sh"
        test_script.write_text(f'''
source "{bash_scripts_dir}/common.sh"
if is_codexspec_project; then
    echo "IS_PROJECT"
fi
''')
        result = subprocess.run(
            ["bash", str(test_script)],
            capture_output=True,
            text=True,
            cwd=temp_codexspec_project,
        )
        assert "IS_PROJECT" in result.stdout

    def test_is_codexspec_project_false(self, bash_scripts_dir: Path, tmp_path: Path):
        """Return false when not in a CodexSpec project."""
        non_project = tmp_path / "non-project"
        non_project.mkdir()

        test_script = non_project / "test_project.sh"
        test_script.write_text(f'''
source "{bash_scripts_dir}/common.sh"
if ! is_codexspec_project; then
    echo "NOT_PROJECT"
fi
''')
        result = subprocess.run(
            ["bash", str(test_script)],
            capture_output=True,
            text=True,
            cwd=non_project,
        )
        assert "NOT_PROJECT" in result.stdout


@pytest.mark.skipif(
    sys.platform == "win32",
    reason="Bash tests only run on Unix-like systems (macOS/Linux)",
)
class TestRequireCodexspecProject:
    """Tests for require_codexspec_project function."""

    def test_require_codexspec_project_success(self, bash_scripts_dir: Path, temp_codexspec_project: Path):
        """Success when in a CodexSpec project."""
        test_script = temp_codexspec_project / "test_require.sh"
        test_script.write_text(f'''
source "{bash_scripts_dir}/common.sh"
require_codexspec_project
echo "CONTINUED"
''')
        result = subprocess.run(
            ["bash", str(test_script)],
            capture_output=True,
            text=True,
            cwd=temp_codexspec_project,
        )
        assert "CONTINUED" in result.stdout
        assert result.returncode == 0

    def test_require_codexspec_project_exit(self, bash_scripts_dir: Path, tmp_path: Path):
        """Exit when not in a CodexSpec project."""
        non_project = tmp_path / "non-project"
        non_project.mkdir()

        test_script = non_project / "test_require.sh"
        test_script.write_text(f'''
source "{bash_scripts_dir}/common.sh"
require_codexspec_project
echo "SHOULD_NOT_APPEAR"
''')
        result = subprocess.run(
            ["bash", str(test_script)],
            capture_output=True,
            text=True,
            cwd=non_project,
        )
        assert "SHOULD_NOT_APPEAR" not in result.stdout
        assert result.returncode != 0
