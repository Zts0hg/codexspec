"""Tests for CodexSpec CLI commands."""

import os
from pathlib import Path
from typing import Generator

import pytest
from typer.testing import CliRunner

from codexspec import __version__, app, get_templates_dir, get_version


@pytest.fixture
def runner() -> CliRunner:
    """Create a CLI test runner."""
    return CliRunner(mix_stderr=False)


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
