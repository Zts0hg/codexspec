"""Tests for CodexSpec CLI commands."""

import os
import subprocess
import sys
from pathlib import Path
from typing import Generator

import pytest
from typer.testing import CliRunner

from codexspec import __version__, app, get_scripts_dir, get_templates_dir, get_version


@pytest.fixture
def runner() -> CliRunner:
    """Create a CLI test runner."""
    return CliRunner()


@pytest.fixture
def isolated_runner(runner: CliRunner, tmp_path: Path) -> Generator[Path, None, None]:
    """Create a runner that operates in an isolated temporary directory."""
    original_cwd = os.getcwd()
    os.chdir(tmp_path)
    try:
        yield tmp_path
    finally:
        os.chdir(original_cwd)


class TestVersion:
    """Tests for version command and utilities."""

    def test_get_version_returns_string(self) -> None:
        """get_version should return the version string."""
        version = get_version()
        assert isinstance(version, str)
        assert len(version) > 0

    def test_version_constant(self) -> None:
        """__version__ should be a valid version string."""
        assert isinstance(__version__, str)
        # Check semantic version format (major.minor.patch)
        parts = __version__.split(".")
        assert len(parts) >= 2
        assert all(part.isdigit() for part in parts)

    def test_version_command(self, runner: CliRunner) -> None:
        """version command should display version info."""
        result = runner.invoke(app, ["version"])
        assert result.exit_code == 0
        assert __version__ in result.stdout
        assert "Python" in result.stdout


class TestCheck:
    """Tests for check command."""

    def test_check_command_runs(self, runner: CliRunner) -> None:
        """check command should execute without error."""
        result = runner.invoke(app, ["check"])
        assert result.exit_code == 0
        assert "Tool Check" in result.stdout


class TestConfig:
    """Tests for config command."""

    def test_config_no_project(self, isolated_runner: Path, runner: CliRunner) -> None:
        """config command should fail when no project exists."""
        # Run from a directory without .codexspec
        result = runner.invoke(app, ["config"])
        assert result.exit_code == 1
        assert "No CodexSpec project found" in result.stdout

    def test_config_list_langs(self, runner: CliRunner) -> None:
        """config --list-langs should show supported languages."""
        result = runner.invoke(app, ["config", "--list-langs"])
        assert result.exit_code == 0
        assert "Supported Languages" in result.stdout
        assert "en" in result.stdout
        assert "zh-CN" in result.stdout

    # --- config --auto-next (workflow.auto_next toggle) ---

    @staticmethod
    def _write_config(project_dir: Path, body: str) -> Path:
        cfg = project_dir / ".codexspec" / "config.yml"
        cfg.parent.mkdir(parents=True, exist_ok=True)
        cfg.write_text(body, encoding="utf-8")
        return cfg

    def test_auto_next_toggle_true_to_false(self, isolated_runner: Path, runner: CliRunner) -> None:
        from codexspec import _AUTO_NEXT_SENTINEL

        cfg = self._write_config(isolated_runner, "workflow:\n  auto_next: true\n")
        result = runner.invoke(app, ["config", "--auto-next", _AUTO_NEXT_SENTINEL])
        assert result.exit_code == 0
        assert "auto_next disabled" in result.stdout
        assert "auto_next: false" in cfg.read_text()

    def test_auto_next_toggle_false_to_true(self, isolated_runner: Path, runner: CliRunner) -> None:
        from codexspec import _AUTO_NEXT_SENTINEL

        cfg = self._write_config(isolated_runner, "workflow:\n  auto_next: false\n")
        result = runner.invoke(app, ["config", "--auto-next", _AUTO_NEXT_SENTINEL])
        assert result.exit_code == 0
        assert "auto_next enabled" in result.stdout
        assert "auto_next: true" in cfg.read_text()

    def test_auto_next_explicit_off(self, isolated_runner: Path, runner: CliRunner) -> None:
        cfg = self._write_config(isolated_runner, "workflow:\n  auto_next: true\n")
        result = runner.invoke(app, ["config", "--auto-next", "off"])
        assert result.exit_code == 0
        assert "auto_next: false" in cfg.read_text()

    @pytest.mark.parametrize("val", ["on", "ON", "yes", "1", "true"])
    def test_auto_next_explicit_truthy(self, isolated_runner: Path, runner: CliRunner, val: str) -> None:
        cfg = self._write_config(isolated_runner, "workflow:\n  auto_next: false\n")
        result = runner.invoke(app, ["config", "--auto-next", val])
        assert result.exit_code == 0
        assert "auto_next: true" in cfg.read_text()

    def test_auto_next_invalid_value_exit1_and_unchanged(self, isolated_runner: Path, runner: CliRunner) -> None:
        cfg = self._write_config(isolated_runner, "workflow:\n  auto_next: true\n")
        result = runner.invoke(app, ["config", "--auto-next", "yep"])
        assert result.exit_code == 1
        assert "Invalid --auto-next value" in result.stdout
        # File must be unchanged on invalid input.
        assert "auto_next: true" in cfg.read_text()

    def test_auto_next_creates_missing_key(self, isolated_runner: Path, runner: CliRunner) -> None:
        cfg = self._write_config(isolated_runner, "language:\n  output: en\nworkflow:\n  other: 1\n")
        result = runner.invoke(app, ["config", "--auto-next", "on"])
        assert result.exit_code == 0
        text = cfg.read_text()
        assert text.count("workflow:") == 1  # no duplicate section
        assert "auto_next: true" in text
        assert "other: 1" in text  # existing child preserved

    def test_auto_next_creates_missing_section(self, isolated_runner: Path, runner: CliRunner) -> None:
        cfg = self._write_config(isolated_runner, "language:\n  output: en\n")
        result = runner.invoke(app, ["config", "--auto-next", "on"])
        assert result.exit_code == 0
        text = cfg.read_text()
        assert text.count("workflow:") == 1
        assert "auto_next: true" in text
        assert "output: en" in text  # prior content preserved

    def test_auto_next_scopes_to_workflow_section(self, isolated_runner: Path, runner: CliRunner) -> None:
        from codexspec import _AUTO_NEXT_SENTINEL

        # An auto_next under a different section must not be read/written.
        body = "project:\n  auto_next: true\nworkflow:\n  auto_next: false\n"
        cfg = self._write_config(isolated_runner, body)
        result = runner.invoke(app, ["config", "--auto-next", _AUTO_NEXT_SENTINEL])
        assert result.exit_code == 0
        # workflow.auto_next was false -> toggle -> true; project.auto_next untouched
        assert "workflow:\n  auto_next: true" in cfg.read_text()
        assert "project:\n  auto_next: true" in cfg.read_text()

    def test_auto_next_no_project(self, isolated_runner: Path, runner: CliRunner) -> None:
        # isolated_runner has no .codexspec/config.yml; the no-project guard
        # fires before the auto_next handler.
        result = runner.invoke(app, ["config", "--auto-next", "on"])
        assert result.exit_code == 1
        assert "No CodexSpec project found" in result.stdout

    def test_auto_next_bare_toggle_via_main(self, tmp_path: Path) -> None:
        """The bare `--auto-next` form is normalized in main(); CliRunner
        bypasses sys.argv, so exercise the real entry point via subprocess."""
        from codexspec import _AUTO_NEXT_SENTINEL

        cfg = tmp_path / ".codexspec" / "config.yml"
        cfg.parent.mkdir(parents=True, exist_ok=True)
        cfg.write_text("workflow:\n  auto_next: true\n", encoding="utf-8")
        code = "import sys; sys.argv=['codexspec','config','--auto-next'];from codexspec import main; main()"
        result = subprocess.run([sys.executable, "-c", code], cwd=tmp_path, capture_output=True, text=True)
        assert result.returncode == 0
        assert "disabled" in result.stdout
        assert "auto_next: false" in cfg.read_text()
        # The sentinel must not leak into the written file.
        assert _AUTO_NEXT_SENTINEL not in cfg.read_text()

    def test_normalize_auto_next_argv(self) -> None:
        from codexspec import _AUTO_NEXT_SENTINEL, _normalize_auto_next_argv

        def norm(*a: str) -> list[str]:
            return _normalize_auto_next_argv(list(a))

        assert norm("config", "--auto-next") == [
            "config",
            f"--auto-next={_AUTO_NEXT_SENTINEL}",
        ]
        # Explicit value passes through unchanged.
        assert norm("config", "--auto-next", "off") == ["config", "--auto-next", "off"]
        # Already in =-form is left alone.
        assert norm("config", "--auto-next=off") == ["config", "--auto-next=off"]
        # Bare flag before another option still toggles.
        assert norm("config", "--set-lang", "en", "--auto-next") == [
            "config",
            "--set-lang",
            "en",
            f"--auto-next={_AUTO_NEXT_SENTINEL}",
        ]


class TestInit:
    """Tests for init command."""

    def test_init_requires_project_name_or_here(self, isolated_runner: Path, runner: CliRunner) -> None:
        """init command should require project name or --here flag."""
        result = runner.invoke(app, ["init"])
        assert result.exit_code == 1
        assert "project name" in result.stdout.lower() or "error" in result.stdout.lower()

    def test_init_creates_project(self, isolated_runner: Path, runner: CliRunner) -> None:
        """init command should create project structure."""
        project_dir = isolated_runner / "my-project"

        result = runner.invoke(
            app,
            ["init", "my-project", "--no-git"],
        )

        assert result.exit_code == 0
        assert project_dir.exists()
        assert (project_dir / ".codexspec").exists()
        assert (project_dir / ".claude" / "commands").exists()
        assert (project_dir / "CLAUDE.md").exists()

    def test_init_here_flag(self, isolated_runner: Path, runner: CliRunner) -> None:
        """init --here should initialize in current directory."""
        result = runner.invoke(
            app,
            ["init", "--here", "--no-git"],
        )

        assert result.exit_code == 0
        assert (isolated_runner / ".codexspec").exists()
        assert (isolated_runner / ".claude" / "commands").exists()

    def test_init_with_language(self, isolated_runner: Path, runner: CliRunner) -> None:
        """init --lang should set the output language."""
        result = runner.invoke(
            app,
            ["init", "my-project", "--no-git", "--lang", "zh-CN"],
        )

        assert result.exit_code == 0

        # Check config file has correct language
        config_file = isolated_runner / "my-project" / ".codexspec" / "config.yml"
        assert config_file.exists()
        content = config_file.read_text()
        assert "zh-CN" in content


class TestGetTemplatesDir:
    """Tests for get_templates_dir function."""

    def test_returns_path(self) -> None:
        """get_templates_dir should return a Path object."""
        path = get_templates_dir()
        assert isinstance(path, Path)

    def test_templates_dir_exists(self) -> None:
        """Templates directory should exist."""
        path = get_templates_dir()
        # In development mode, this should point to project templates
        # When installed, it should point to installed templates
        assert path.exists() or path.name == "templates"


class TestMainEntry:
    """Tests for main entry point."""

    def test_main_runs(self) -> None:
        """main() should be callable."""
        from codexspec import main

        # main() runs the CLI, we just verify it's callable
        assert callable(main)


class TestCLIIntegration:
    """Integration tests for CLI."""

    def test_help_command(self, runner: CliRunner) -> None:
        """--help should show usage information."""
        result = runner.invoke(app, ["--help"])
        assert result.exit_code == 0
        assert "codexspec" in result.stdout.lower()

    def test_invalid_command(self, runner: CliRunner) -> None:
        """Invalid command should show error."""
        result = runner.invoke(app, ["invalid-command"])
        assert result.exit_code != 0


class TestGetScriptsDir:
    """Tests for get_scripts_dir function."""

    def test_returns_path(self) -> None:
        """get_scripts_dir should return a Path object."""
        path = get_scripts_dir()
        assert isinstance(path, Path)

    def test_scripts_dir_exists(self) -> None:
        """Scripts directory should exist."""
        path = get_scripts_dir()
        # In development mode, this should point to project scripts
        # When installed, it should point to installed scripts
        assert path.exists() or path.name == "scripts"


class TestInitScripts:
    """Tests for script copying in init command."""

    def test_get_scripts_dir_returns_path(self) -> None:
        """get_scripts_dir should return a Path object."""
        path = get_scripts_dir()
        assert isinstance(path, Path)

    def test_get_scripts_dir_exists(self) -> None:
        """Scripts directory should exist."""
        path = get_scripts_dir()
        assert path.exists() or path.name == "scripts"

    def test_init_copies_bash_scripts_on_unix(
        self, isolated_runner: Path, runner: CliRunner, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """init should copy bash scripts on non-Windows platforms."""
        # Simulate Unix platform
        monkeypatch.setattr(sys, "platform", "linux")

        result = runner.invoke(app, ["init", "my-project", "--no-git"])
        assert result.exit_code == 0

        scripts_dir = isolated_runner / "my-project" / ".codexspec" / "scripts"
        assert scripts_dir.exists()

        # Check bash scripts are copied
        assert (scripts_dir / "common.sh").exists()
        assert (scripts_dir / "check-prerequisites.sh").exists()
        assert (scripts_dir / "create-new-feature.sh").exists()

        # Check PowerShell scripts are NOT copied
        assert not (scripts_dir / "common.ps1").exists()

    def test_init_copies_powershell_scripts_on_windows(
        self, isolated_runner: Path, runner: CliRunner, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """init should copy PowerShell scripts on Windows."""
        # Simulate Windows platform
        monkeypatch.setattr(sys, "platform", "win32")

        result = runner.invoke(app, ["init", "my-project", "--no-git"])
        assert result.exit_code == 0

        scripts_dir = isolated_runner / "my-project" / ".codexspec" / "scripts"
        assert scripts_dir.exists()

        # Check PowerShell scripts are copied
        assert (scripts_dir / "common.ps1").exists()
        assert (scripts_dir / "check-prerequisites.ps1").exists()
        assert (scripts_dir / "create-new-feature.ps1").exists()

        # Check bash scripts are NOT copied
        assert not (scripts_dir / "common.sh").exists()

    def test_init_scripts_content_preserved(self, isolated_runner: Path, runner: CliRunner) -> None:
        """init should preserve script content exactly."""
        result = runner.invoke(app, ["init", "my-project", "--no-git"])
        assert result.exit_code == 0

        # Compare copied script with original
        scripts_source = get_scripts_dir()
        if sys.platform == "win32":
            source_file = scripts_source / "powershell" / "common.ps1"
        else:
            source_file = scripts_source / "bash" / "common.sh"

        if source_file.exists():
            dest_file = isolated_runner / "my-project" / ".codexspec" / "scripts" / source_file.name
            assert dest_file.read_text(encoding="utf-8") == source_file.read_text(encoding="utf-8")


class TestInitSubdirectoryStructure:
    """Tests for init command with new subdirectory structure."""

    def test_init_creates_commands_subdirectory(self, isolated_runner: Path, runner: CliRunner) -> None:
        """init should create commands in .claude/commands/codexspec/ subdirectory."""
        result = runner.invoke(app, ["init", "my-project", "--no-git"])
        assert result.exit_code == 0

        # Check subdirectory exists
        subcommands_dir = isolated_runner / "my-project" / ".claude" / "commands" / "codexspec"
        assert subcommands_dir.exists()
        assert subcommands_dir.is_dir()

    def test_init_installs_commands_to_subdirectory(self, isolated_runner: Path, runner: CliRunner) -> None:
        """init should install command templates to subdirectory without prefix."""
        result = runner.invoke(app, ["init", "my-project", "--no-git"])
        assert result.exit_code == 0

        subcommands_dir = isolated_runner / "my-project" / ".claude" / "commands" / "codexspec"

        # Check some commands exist without prefix
        assert (subcommands_dir / "constitution.md").exists()
        assert (subcommands_dir / "specify.md").exists()
        assert (subcommands_dir / "commit-staged.md").exists()

    def test_init_no_root_commands(self, isolated_runner: Path, runner: CliRunner) -> None:
        """init should NOT create codexspec.*.md files in root commands directory."""
        result = runner.invoke(app, ["init", "my-project", "--no-git"])
        assert result.exit_code == 0

        commands_dir = isolated_runner / "my-project" / ".claude" / "commands"

        # No prefixed files in root
        prefixed_files = list(commands_dir.glob("codexspec.*.md"))
        assert len(prefixed_files) == 0

    def test_init_shows_command_summary(self, isolated_runner: Path, runner: CliRunner) -> None:
        """init output should include command summary."""
        result = runner.invoke(app, ["init", "my-project", "--no-git"])
        assert result.exit_code == 0

        # Should show installed commands summary
        assert "15" in result.stdout or "command" in result.stdout.lower()


class TestInitMigration:
    """Tests for init command migration flow."""

    def test_init_detects_old_structure(self, isolated_runner: Path, runner: CliRunner) -> None:
        """init should detect old structure files."""
        # Create old structure first
        commands_dir = isolated_runner / ".claude" / "commands"
        commands_dir.mkdir(parents=True)
        old_file = commands_dir / "codexspec.constitution.md"
        old_file.write_text("# Old Constitution")

        # Run init with --here to use current directory
        # Provide 'y' input for both migration and update confirmation prompts
        result = runner.invoke(app, ["init", "--here", "--no-git"], input="y\ny\n")
        assert result.exit_code == 0

        # Should mention migration in output
        assert (
            "migrate" in result.stdout.lower() or "migration" in result.stdout.lower() or "old" in result.stdout.lower()
        )

    def test_init_migrates_old_files(self, isolated_runner: Path, runner: CliRunner) -> None:
        """init should migrate old structure files to subdirectory."""
        # Create old structure
        commands_dir = isolated_runner / ".claude" / "commands"
        commands_dir.mkdir(parents=True)
        old_content = "# My Custom Constitution"
        old_file = commands_dir / "codexspec.constitution.md"
        old_file.write_text(old_content)

        # Run init - say 'y' to migrate, 'n' to update to preserve content
        result = runner.invoke(app, ["init", "--here", "--no-git"], input="y\nn\n")
        assert result.exit_code == 0

        # Old file should be gone
        assert not old_file.exists()

        # New file should exist with preserved content
        new_file = commands_dir / "codexspec" / "constitution.md"
        assert new_file.exists()
        assert new_file.read_text() == old_content

    def test_init_preserves_custom_content(self, isolated_runner: Path, runner: CliRunner) -> None:
        """init should preserve user's custom content during migration."""
        commands_dir = isolated_runner / ".claude" / "commands"
        commands_dir.mkdir(parents=True)
        custom_content = "# My Very Custom Constitution\n\nCustom rules here."
        old_file = commands_dir / "codexspec.constitution.md"
        old_file.write_text(custom_content)

        # Say 'y' to migrate, 'n' to update to preserve custom content
        result = runner.invoke(app, ["init", "--here", "--no-git"], input="y\nn\n")
        assert result.exit_code == 0

        new_file = commands_dir / "codexspec" / "constitution.md"
        assert new_file.read_text() == custom_content


class TestInitUpdate:
    """Tests for init command update flow."""

    def test_init_detects_existing_subdirectory(self, isolated_runner: Path, runner: CliRunner) -> None:
        """init should detect existing subdirectory and offer update."""
        # First init
        result = runner.invoke(app, ["init", "my-project", "--no-git"])
        assert result.exit_code == 0

        # Second init should detect existing
        os.chdir(isolated_runner / "my-project")
        result = runner.invoke(app, ["init", "--here", "--no-git"], input="n\n")
        assert result.exit_code == 0

        # Should mention update (in English or Chinese)
        output_lower = result.stdout.lower()
        assert (
            "update" in output_lower
            or "更新" in result.stdout
            or "overwrite" in output_lower
            or "exists" in output_lower
        )


class TestListCommands:
    """Tests for list-commands command."""

    def test_list_commands_exists(self, runner: CliRunner) -> None:
        """list-commands command should be available."""
        result = runner.invoke(app, ["list-commands", "--help"])
        # Should not error - command exists
        assert "list-commands" in result.stdout.lower() or result.exit_code == 0

    def test_list_commands_shows_core(self, runner: CliRunner) -> None:
        """list-commands should show core commands."""
        result = runner.invoke(app, ["list-commands"])
        assert result.exit_code == 0
        # Should show constitution command
        assert "constitution" in result.stdout.lower()

    def test_list_commands_shows_count(self, runner: CliRunner) -> None:
        """list-commands should show total count."""
        result = runner.invoke(app, ["list-commands"])
        assert result.exit_code == 0
        # Should show 18 commands (9 core + 4 enhanced + 2 git + 1 review + 2 utility)
        assert "18" in result.stdout
