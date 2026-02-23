"""Tests for scripts/powershell/common.ps1."""

import subprocess
from pathlib import Path

import pytest


@pytest.mark.skipif(
    not __import__("shutil", fromlist=["which"]).which("pwsh"),
    reason="PowerShell not available",
)
class TestGetRepoRoot:
    """Tests for Get-RepoRoot function."""

    def test_get_repo_root_git(self, powershell_scripts_dir: Path, temp_git_repo: Path):
        """Get repository root from git repository."""
        result = subprocess.run(
            [
                "pwsh",
                "-Command",
                f'''
. "{powershell_scripts_dir}/common.ps1"
Get-RepoRoot
''',
            ],
            capture_output=True,
            text=True,
            cwd=temp_git_repo,
        )
        assert str(temp_git_repo) in result.stdout

    def test_get_repo_root_fallback(self, powershell_scripts_dir: Path, tmp_path: Path):
        """Fallback for non-git repository."""
        non_git = tmp_path / "non-git"
        non_git.mkdir()

        result = subprocess.run(
            [
                "pwsh",
                "-Command",
                f'''
. "{powershell_scripts_dir}/common.ps1"
Get-RepoRoot
''',
            ],
            capture_output=True,
            text=True,
            cwd=non_git,
        )
        # Should return some path (fallback to script location)
        assert result.stdout.strip() != ""


@pytest.mark.skipif(
    not __import__("shutil", fromlist=["which"]).which("pwsh"),
    reason="PowerShell not available",
)
class TestGetCurrentBranch:
    """Tests for Get-CurrentBranch function."""

    def test_get_current_branch_env(self, powershell_scripts_dir: Path, tmp_path: Path):
        """Get branch from environment variable."""
        result = subprocess.run(
            [
                "pwsh",
                "-Command",
                f'''
$env:CODEXSPEC_FEATURE = "001-test-feature"
. "{powershell_scripts_dir}/common.ps1"
Get-CurrentBranch
''',
            ],
            capture_output=True,
            text=True,
            cwd=tmp_path,
        )
        assert "001-test-feature" in result.stdout

    def test_get_current_branch_git(self, powershell_scripts_dir: Path, temp_git_repo: Path):
        """Get branch from git."""
        # Create and checkout a branch
        subprocess.run(
            ["git", "checkout", "-b", "002-test-branch"],
            cwd=temp_git_repo,
            check=True,
            capture_output=True,
        )

        result = subprocess.run(
            [
                "pwsh",
                "-Command",
                f'''
. "{powershell_scripts_dir}/common.ps1"
Get-CurrentBranch
''',
            ],
            capture_output=True,
            text=True,
            cwd=temp_git_repo,
        )
        assert "002-test-branch" in result.stdout


@pytest.mark.skipif(
    not __import__("shutil", fromlist=["which"]).which("pwsh"),
    reason="PowerShell not available",
)
class TestHasGit:
    """Tests for Test-HasGit function."""

    def test_has_git_true(self, powershell_scripts_dir: Path, temp_git_repo: Path):
        """Returns true when in git repository."""
        result = subprocess.run(
            [
                "pwsh",
                "-Command",
                f'''
. "{powershell_scripts_dir}/common.ps1"
if (Test-HasGit) {{ Write-Output "HAS_GIT" }}
''',
            ],
            capture_output=True,
            text=True,
            cwd=temp_git_repo,
        )
        assert "HAS_GIT" in result.stdout

    def test_has_git_false(self, powershell_scripts_dir: Path, tmp_path: Path):
        """Returns false when not in git repository."""
        non_git = tmp_path / "non-git"
        non_git.mkdir()

        result = subprocess.run(
            [
                "pwsh",
                "-Command",
                f'''
. "{powershell_scripts_dir}/common.ps1"
if (-not (Test-HasGit)) {{ Write-Output "NO_GIT" }}
''',
            ],
            capture_output=True,
            text=True,
            cwd=non_git,
        )
        assert "NO_GIT" in result.stdout


@pytest.mark.skipif(
    not __import__("shutil", fromlist=["which"]).which("pwsh"),
    reason="PowerShell not available",
)
class TestFeatureBranch:
    """Tests for Test-FeatureBranch function."""

    def test_feature_branch_valid(self, powershell_scripts_dir: Path, tmp_path: Path):
        """Valid feature branch returns true."""
        result = subprocess.run(
            [
                "pwsh",
                "-Command",
                f'''
. "{powershell_scripts_dir}/common.ps1"
if (Test-FeatureBranch -Branch "001-valid-feature") {{ Write-Output "VALID" }}
''',
            ],
            capture_output=True,
            text=True,
            cwd=tmp_path,
        )
        assert "VALID" in result.stdout

    def test_feature_branch_invalid(self, powershell_scripts_dir: Path, tmp_path: Path):
        """Invalid feature branch returns false."""
        result = subprocess.run(
            [
                "pwsh",
                "-Command",
                f'''
. "{powershell_scripts_dir}/common.ps1"
if (-not (Test-FeatureBranch -Branch "main" -HasGit $true)) {{ Write-Output "INVALID" }}
''',
            ],
            capture_output=True,
            text=True,
            cwd=tmp_path,
        )
        assert "INVALID" in result.stdout

    def test_feature_branch_no_git(self, powershell_scripts_dir: Path, tmp_path: Path):
        """Returns true when no git available (warning issued)."""
        result = subprocess.run(
            [
                "pwsh",
                "-Command",
                f'''
. "{powershell_scripts_dir}/common.ps1"
if (Test-FeatureBranch -Branch "any-branch" -HasGit $false) {{ Write-Output "OK" }}
''',
            ],
            capture_output=True,
            text=True,
            cwd=tmp_path,
        )
        assert "OK" in result.stdout


@pytest.mark.skipif(
    not __import__("shutil", fromlist=["which"]).which("pwsh"),
    reason="PowerShell not available",
)
class TestGetFeatureDir:
    """Tests for Get-FeatureDir function."""

    def test_get_feature_dir(self, powershell_scripts_dir: Path, tmp_path: Path):
        """Returns correct feature directory path."""
        result = subprocess.run(
            [
                "pwsh",
                "-Command",
                f'''
. "{powershell_scripts_dir}/common.ps1"
Get-FeatureDir -RepoRoot "/test/repo" -Branch "001-my-feature"
''',
            ],
            capture_output=True,
            text=True,
            cwd=tmp_path,
        )
        assert "/test/repo/.codexspec/specs/001-my-feature" in result.stdout


@pytest.mark.skipif(
    not __import__("shutil", fromlist=["which"]).which("pwsh"),
    reason="PowerShell not available",
)
class TestGetFeaturePathsEnv:
    """Tests for Get-FeaturePathsEnv function."""

    def test_get_feature_paths_env(self, powershell_scripts_dir: Path, temp_codexspec_git_project: Path):
        """Returns all feature paths as object."""
        # Checkout a feature branch first
        subprocess.run(
            ["git", "checkout", "-b", "003-test-feature"],
            cwd=temp_codexspec_git_project,
            check=True,
            capture_output=True,
        )

        result = subprocess.run(
            [
                "pwsh",
                "-Command",
                f'''
. "{powershell_scripts_dir}/common.ps1"
$paths = Get-FeaturePathsEnv
Write-Output $paths.FEATURE_DIR
Write-Output $paths.FEATURE_SPEC
Write-Output $paths.IMPL_PLAN
Write-Output $paths.TASKS
''',
            ],
            capture_output=True,
            text=True,
            cwd=temp_codexspec_git_project,
        )
        assert ".codexspec/specs/003-test-feature" in result.stdout
        assert "spec.md" in result.stdout
        assert "plan.md" in result.stdout
        assert "tasks.md" in result.stdout


@pytest.mark.skipif(
    not __import__("shutil", fromlist=["which"]).which("pwsh"),
    reason="PowerShell not available",
)
class TestFileExists:
    """Tests for Test-FileExists function."""

    def test_file_exists_true(self, powershell_scripts_dir: Path, tmp_path: Path):
        """Returns true when file exists."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("test")

        result = subprocess.run(
            [
                "pwsh",
                "-Command",
                f'''
. "{powershell_scripts_dir}/common.ps1"
if (Test-FileExists -Path "{test_file}" -Description "test file") {{ Write-Output "EXISTS" }}
''',
            ],
            capture_output=True,
            text=True,
            cwd=tmp_path,
        )
        assert "EXISTS" in result.stdout
        assert "[OK]" in result.stdout

    def test_file_exists_false(self, powershell_scripts_dir: Path, tmp_path: Path):
        """Returns false when file missing."""
        result = subprocess.run(
            [
                "pwsh",
                "-Command",
                f'''
. "{powershell_scripts_dir}/common.ps1"
if (-not (Test-FileExists -Path "/nonexistent/file.txt" -Description "missing file")) {{ Write-Output "MISSING" }}
''',
            ],
            capture_output=True,
            text=True,
            cwd=tmp_path,
        )
        assert "MISSING" in result.stdout
        assert "[MISSING]" in result.stdout
