"""Tests for scripts/bash/create-new-feature.sh."""

import re
import subprocess
import sys
from pathlib import Path

import pytest


@pytest.mark.skipif(
    sys.platform == "win32",
    reason="Bash tests only run on Unix-like systems (macOS/Linux)",
)
class TestCreateNewFeature:
    """Tests for create-new-feature.sh script."""

    @pytest.fixture(autouse=True)
    def explicit_legacy_optout(self, request):
        """Existing cases exercise the intentionally preserved in-place mode."""
        for name in ("temp_codexspec_project", "temp_codexspec_git_project"):
            if name in request.fixturenames:
                project = request.getfixturevalue(name)
                config = project / ".codexspec/config.yml"
                config.write_text(config.read_text() + "workflow:\n  worktrees: false\n")

    def test_help_flag(self, bash_scripts_dir: Path, tmp_path: Path):
        """-h flag displays help message."""
        script_path = bash_scripts_dir / "create-new-feature.sh"
        result = subprocess.run(
            ["bash", str(script_path), "-h"],
            capture_output=True,
            text=True,
            cwd=tmp_path,
        )
        assert result.returncode == 0
        assert "Usage:" in result.stdout
        assert "-n, --name" in result.stdout

    def test_requires_feature_name(self, bash_scripts_dir: Path, tmp_path: Path):
        """Reports error when feature name is missing."""
        script_path = bash_scripts_dir / "create-new-feature.sh"
        result = subprocess.run(
            ["bash", str(script_path)],
            capture_output=True,
            text=True,
            cwd=tmp_path,
        )
        assert result.returncode != 0
        assert "Feature name is required" in result.stdout

    def test_requires_codexspec_project(self, bash_scripts_dir: Path, tmp_path: Path):
        """Reports error when not in a CodexSpec project."""
        non_project = tmp_path / "non-project"
        non_project.mkdir()

        script_path = bash_scripts_dir / "create-new-feature.sh"
        result = subprocess.run(
            ["bash", str(script_path), "-n", "test feature"],
            capture_output=True,
            text=True,
            cwd=non_project,
        )
        assert result.returncode != 0
        assert "Not a CodexSpec project" in result.stdout

    def test_rejects_name_without_ascii_alphanumerics(
        self,
        bash_scripts_dir: Path,
        temp_codexspec_project: Path,
    ):
        """A short name must retain at least one ASCII letter or digit."""
        script_path = bash_scripts_dir / "create-new-feature.sh"
        result = subprocess.run(
            ["bash", str(script_path), "-n", "纯中文功能"],
            capture_output=True,
            text=True,
            cwd=temp_codexspec_project,
        )

        assert result.returncode != 0
        assert "ASCII letters or numbers" in result.stdout
        specs_dir = temp_codexspec_project / ".codexspec" / "specs"
        assert not specs_dir.exists() or not any(specs_dir.iterdir())

    def test_creates_feature_dir(self, bash_scripts_dir: Path, temp_codexspec_project: Path):
        """Creates feature directory with correct name."""
        script_path = bash_scripts_dir / "create-new-feature.sh"
        result = subprocess.run(
            ["bash", str(script_path), "-n", "user authentication"],
            capture_output=True,
            text=True,
            cwd=temp_codexspec_project,
        )
        assert result.returncode == 0

        # Check feature directory was created
        specs_dir = temp_codexspec_project / ".codexspec" / "specs"
        feature_dirs = list(specs_dir.glob("20??-????-??????-*"))
        assert len(feature_dirs) == 1
        assert "user-authentication" in feature_dirs[0].name

    def test_creates_requirements_file(self, bash_scripts_dir: Path, temp_codexspec_project: Path):
        """Creates requirements.md as the first feature artifact."""
        script_path = bash_scripts_dir / "create-new-feature.sh"
        result = subprocess.run(
            ["bash", str(script_path), "-n", "test feature"],
            capture_output=True,
            text=True,
            cwd=temp_codexspec_project,
        )
        assert result.returncode == 0

        specs_dir = temp_codexspec_project / ".codexspec" / "specs"
        requirements_file = next(specs_dir.glob("20??-????-??????-test-feature/requirements.md"))
        assert requirements_file.exists()
        content = requirements_file.read_text(encoding="utf-8")
        for section in ["NEED-001", "CON-001", "DEC-001", "OUT-001"]:
            entry = content.split(section, 1)[1].split("\n## ", 1)[0]
            assert "**Status**: open" in entry

    def test_initializes_requirements_template_metadata(
        self,
        bash_scripts_dir: Path,
        temp_codexspec_project: Path,
    ):
        """Copied requirements templates contain the generated feature metadata."""
        template_source = Path(__file__).parents[3] / "templates" / "docs" / "requirements-template.md"
        template_dir = temp_codexspec_project / ".codexspec" / "templates" / "docs"
        template_dir.mkdir(parents=True)
        (template_dir / "requirements-template.md").write_text(
            template_source.read_text(encoding="utf-8"),
            encoding="utf-8",
        )

        script_path = bash_scripts_dir / "create-new-feature.sh"
        result = subprocess.run(
            ["bash", str(script_path), "-n", "Test Feature"],
            capture_output=True,
            text=True,
            cwd=temp_codexspec_project,
        )

        assert result.returncode == 0
        requirements_file = next(
            (temp_codexspec_project / ".codexspec" / "specs").glob("20??-????-??????-test-feature/requirements.md")
        )
        content = requirements_file.read_text(encoding="utf-8")
        feature_id = re.search(r"Feature ID: (\d{4}-\d{4}-\d{4}[a-z0-9]{2})", result.stdout)
        assert feature_id
        assert "# Confirmed Requirements: test-feature" in content
        assert f"**Feature ID**: `{feature_id.group(1)}`" in content
        assert "[FEATURE NAME]" not in content
        assert "[feature-id]" not in content
        assert "[DATE]" in content

    def test_default_id_is_timestamp(self, bash_scripts_dir: Path, temp_codexspec_project: Path):
        """Feature creation always uses the timestamp identifier format."""
        script_path = bash_scripts_dir / "create-new-feature.sh"
        result = subprocess.run(
            ["bash", str(script_path), "-n", "test feature"],
            capture_output=True,
            text=True,
            cwd=temp_codexspec_project,
        )
        assert result.returncode == 0

        specs_dir = temp_codexspec_project / ".codexspec" / "specs"
        feature_dirs = list(specs_dir.glob("20??-????-??????-test-feature"))
        assert len(feature_dirs) == 1
        assert (feature_dirs[0] / "requirements.md").exists()
        assert re.search(r"Feature ID: \d{4}-\d{4}-\d{4}[a-z0-9]{2}", result.stdout)

    def test_branch_name_generation(self, bash_scripts_dir: Path, temp_codexspec_project: Path):
        """Branch name is generated correctly from feature name."""
        script_path = bash_scripts_dir / "create-new-feature.sh"
        result = subprocess.run(
            ["bash", str(script_path), "-n", "User Authentication System"],
            capture_output=True,
            text=True,
            cwd=temp_codexspec_project,
        )
        assert result.returncode == 0
        assert re.search(
            r"\d{4}-\d{4}-\d{4}[a-z0-9]{2}-user-authentication-system",
            result.stdout,
        )

    def test_creates_git_branch(self, bash_scripts_dir: Path, temp_codexspec_git_project: Path):
        """Creates git branch when in a git repository."""
        script_path = bash_scripts_dir / "create-new-feature.sh"
        result = subprocess.run(
            ["bash", str(script_path), "-n", "git feature"],
            capture_output=True,
            text=True,
            cwd=temp_codexspec_git_project,
        )
        assert result.returncode == 0

        # Check git branch was created (branch name may have been transformed)
        branch_result = subprocess.run(
            ["git", "branch", "--show-current"],
            capture_output=True,
            text=True,
            cwd=temp_codexspec_git_project,
        )
        assert re.fullmatch(
            r"\d{4}-\d{4}-\d{4}[a-z0-9]{2}-git-feature\n?",
            branch_result.stdout,
        )

    def test_output_messages(self, bash_scripts_dir: Path, temp_codexspec_project: Path):
        """Outputs appropriate success messages."""
        script_path = bash_scripts_dir / "create-new-feature.sh"
        result = subprocess.run(
            ["bash", str(script_path), "-n", "output test"],
            capture_output=True,
            text=True,
            cwd=temp_codexspec_project,
        )
        assert result.returncode == 0
        assert "[INFO]" in result.stdout
        assert "[SUCCESS]" in result.stdout
        assert "Created feature directory" in result.stdout
        assert "Created requirements record" in result.stdout

    def test_next_steps_guidance(self, bash_scripts_dir: Path, temp_codexspec_project: Path):
        """Provides next steps guidance after creation."""
        script_path = bash_scripts_dir / "create-new-feature.sh"
        result = subprocess.run(
            ["bash", str(script_path), "-n", "guidance test"],
            capture_output=True,
            text=True,
            cwd=temp_codexspec_project,
        )
        assert result.returncode == 0
        assert "Next steps:" in result.stdout
        assert "Confirm the requirements record" in result.stdout


@pytest.mark.skipif(sys.platform == "win32", reason="Bash requires Unix")
def test_s026_default_isolated_script(tmp_path, bash_scripts_dir):
    import json

    from tests.automation_test_support import git
    from tests.test_worktrees import configured

    repo = configured(tmp_path / "repo")
    result = subprocess.run(
        ["bash", str(bash_scripts_dir / "create-new-feature.sh"), "--name", "sample"],
        cwd=repo,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    data = json.loads(result.stdout)
    assert Path(data["workspace"]).parent == Path(str(repo) + "-codexspec-worktrees")
    assert Path(data["requirements_file"]).is_file()
    assert git(repo, "branch", "--show-current").stdout.strip() == "main"
    assert not (repo / ".codexspec/specs").exists()


@pytest.mark.skipif(sys.platform == "win32", reason="Bash requires Unix")
def test_s028_missing_helper_never_falls_back_to_main(tmp_path):
    import os
    import shutil
    import subprocess

    from tests.test_worktrees import configured

    repo = configured(tmp_path / "repo")
    commands = tmp_path / "commands"
    commands.mkdir()
    # Supply script prerequisites, deliberately excluding the CodexSpec executable.
    for name in ("dirname", "tr", "sed", "git", "date", "head", "pwd"):
        executable = shutil.which(name)
        if executable:
            (commands / name).symlink_to(executable)
    env = os.environ.copy()
    env["PATH"] = str(commands)
    script = Path(__file__).resolve().parents[3] / "scripts/bash/create-new-feature.sh"
    result = subprocess.run(
        ["/bin/bash", str(script), "--name", "missing-helper"],
        cwd=repo,
        env=env,
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0 and "runtime is unavailable" in result.stderr + result.stdout
    assert not (repo / ".codexspec/specs").exists()
    assert not Path(str(repo) + "-codexspec-worktrees").exists()
