"""Tests for CodexSpec init with Codex CLI support."""

import os
from pathlib import Path
from typing import Generator

import pytest
from typer.testing import CliRunner

from codexspec import app


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


@pytest.fixture
def isolated_runner(runner: CliRunner, tmp_path: Path) -> Generator[Path, None, None]:
    original_cwd = os.getcwd()
    os.chdir(tmp_path)
    try:
        yield tmp_path
    finally:
        os.chdir(original_cwd)


class TestInitCodex:
    """Tests for init --ai codex."""

    def test_codex_creates_agents_md(self, isolated_runner: Path, runner: CliRunner) -> None:
        """TC-001: --ai codex should create AGENTS.md, not CLAUDE.md, no .claude/ dir."""
        result = runner.invoke(app, ["init", "test-project", "--ai", "codex", "--no-git"])
        assert result.exit_code == 0

        project_dir = isolated_runner / "test-project"
        assert (project_dir / "AGENTS.md").exists()
        assert not (project_dir / "CLAUDE.md").exists()
        assert not (project_dir / ".claude").exists()

    def test_codex_config_has_ai_codex(self, isolated_runner: Path, runner: CliRunner) -> None:
        """TC-006: config.yml should contain ai: 'codex'."""
        result = runner.invoke(app, ["init", "test-project", "--ai", "codex", "--no-git"])
        assert result.exit_code == 0

        config_file = isolated_runner / "test-project" / ".codexspec" / "config.yml"
        assert config_file.exists()
        content = config_file.read_text()
        assert 'ai: "codex"' in content

    def test_codex_creates_codexspec_structure(self, isolated_runner: Path, runner: CliRunner) -> None:
        """TC-007: .codexspec/ directory structure should be complete."""
        result = runner.invoke(app, ["init", "test-project", "--ai", "codex", "--no-git"])
        assert result.exit_code == 0

        codexspec_dir = isolated_runner / "test-project" / ".codexspec"
        assert (codexspec_dir / "memory").is_dir()
        assert (codexspec_dir / "specs").is_dir()
        assert (codexspec_dir / "templates").is_dir()
        assert (codexspec_dir / "scripts").is_dir()
        assert (codexspec_dir / "memory" / "constitution.md").exists()

    def test_codex_agents_md_size_limit(self, isolated_runner: Path, runner: CliRunner) -> None:
        """TC-008: AGENTS.md should be under 32 KiB."""
        result = runner.invoke(app, ["init", "test-project", "--ai", "codex", "--no-git"])
        assert result.exit_code == 0

        agents_md = isolated_runner / "test-project" / "AGENTS.md"
        content = agents_md.read_bytes()
        assert len(content) < 32768

    def test_codex_agents_md_content(self, isolated_runner: Path, runner: CliRunner) -> None:
        """AGENTS.md should contain constitution reference, workflow, and directory structure."""
        result = runner.invoke(app, ["init", "test-project", "--ai", "codex", "--no-git"])
        assert result.exit_code == 0

        content = (isolated_runner / "test-project" / "AGENTS.md").read_text()
        assert "constitution" in content.lower()
        assert ".codexspec/memory/constitution.md" in content
        assert "SDD" in content or "Spec-Driven" in content
        assert ".codex/skills/" in content
        assert "/skills" in content


class TestInitCodexCommands:
    """Tests for skill installation with --ai codex."""

    def test_codex_installs_skills_to_codex_dir(self, isolated_runner: Path, runner: CliRunner) -> None:
        """Skill templates should be installed to .codex/skills/."""
        result = runner.invoke(app, ["init", "test-project", "--ai", "codex", "--no-git"])
        assert result.exit_code == 0

        skills_dir = isolated_runner / "test-project" / ".codex" / "skills"
        assert skills_dir.is_dir()
        skill_files = list(skills_dir.glob("codexspec-*/SKILL.md"))
        assert len(skill_files) == 18

    def test_codex_skill_templates_have_content(self, isolated_runner: Path, runner: CliRunner) -> None:
        """Installed skills should have non-empty SKILL.md content with required frontmatter."""
        result = runner.invoke(app, ["init", "test-project", "--ai", "codex", "--no-git"])
        assert result.exit_code == 0

        skills_dir = isolated_runner / "test-project" / ".codex" / "skills"
        for skill_file in skills_dir.glob("codexspec-*/SKILL.md"):
            content = skill_file.read_text()
            assert len(content) > 100, f"{skill_file} is too small"
            assert "name:" in content, f"{skill_file} missing skill name"
            assert "description:" in content, f"{skill_file} missing description"

    def test_codex_no_claude_dir(self, isolated_runner: Path, runner: CliRunner) -> None:
        """.claude/ must NOT exist for codex projects."""
        result = runner.invoke(app, ["init", "test-project", "--ai", "codex", "--no-git"])
        assert result.exit_code == 0

        project_dir = isolated_runner / "test-project"
        assert not (project_dir / ".claude").exists()
        assert not (project_dir / ".codex" / "commands").exists()
        assert (project_dir / ".codex" / "skills").is_dir()

    def test_codex_has_key_skill_files(self, isolated_runner: Path, runner: CliRunner) -> None:
        """Key CodexSpec skills should exist."""
        result = runner.invoke(app, ["init", "test-project", "--ai", "codex", "--no-git"])
        assert result.exit_code == 0

        skills_dir = isolated_runner / "test-project" / ".codex" / "skills"
        for name in [
            "codexspec-specify",
            "codexspec-constitution",
            "codexspec-quick",
            "codexspec-implement-tasks",
            "codexspec-review-spec",
        ]:
            assert (skills_dir / name / "SKILL.md").exists(), f"Missing skill file: {name}"


class TestInitCodexLanguage:
    """Tests for init --ai codex with language options."""

    def test_codex_with_language(self, isolated_runner: Path, runner: CliRunner) -> None:
        """TC-002: --ai codex --lang zh-CN should set language correctly."""
        result = runner.invoke(app, ["init", "test-project", "--ai", "codex", "--no-git", "--lang", "zh-CN"])
        assert result.exit_code == 0

        config_file = isolated_runner / "test-project" / ".codexspec" / "config.yml"
        content = config_file.read_text()
        assert "zh-CN" in content
        assert 'ai: "codex"' in content


class TestInitAiValidation:
    """Tests for --ai parameter validation."""

    def test_invalid_ai_shows_error(self, isolated_runner: Path, runner: CliRunner) -> None:
        """TC-005: --ai invalid should show error with supported options."""
        result = runner.invoke(app, ["init", "test-project", "--ai", "invalid", "--no-git"])
        assert result.exit_code == 1
        assert "claude" in result.stdout.lower()
        assert "codex" in result.stdout.lower()


class TestInitClaudeRegression:
    """Regression tests: --ai claude behavior must remain unchanged."""

    def test_explicit_claude(self, isolated_runner: Path, runner: CliRunner) -> None:
        """TC-003: --ai claude should create CLAUDE.md and .claude/ (same as before)."""
        result = runner.invoke(app, ["init", "test-project", "--ai", "claude", "--no-git"])
        assert result.exit_code == 0

        project_dir = isolated_runner / "test-project"
        assert (project_dir / "CLAUDE.md").exists()
        assert (project_dir / ".claude" / "commands").exists()
        assert not (project_dir / "AGENTS.md").exists()
        assert not (project_dir / ".codex").exists()

    def test_default_ai_is_claude(self, isolated_runner: Path, runner: CliRunner) -> None:
        """TC-004: Default (no --ai) should behave as --ai claude."""
        result = runner.invoke(app, ["init", "test-project", "--no-git"])
        assert result.exit_code == 0

        project_dir = isolated_runner / "test-project"
        assert (project_dir / "CLAUDE.md").exists()
        assert (project_dir / ".claude" / "commands").exists()
        assert not (project_dir / "AGENTS.md").exists()

        config_content = (project_dir / ".codexspec" / "config.yml").read_text()
        assert 'ai: "claude"' in config_content
