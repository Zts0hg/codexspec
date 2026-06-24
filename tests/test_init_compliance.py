"""Integration tests for init command's Constitution Compliance behavior.

This module contains integration tests for the init command's compliance-related
behavior as specified in the Constitution Compliance Enhancement spec.
"""

import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest
from typer.testing import CliRunner

from codexspec import app, has_compliance_section, prepend_compliance_section

_runner = CliRunner()

# ============================================================================
# Fixtures
# ============================================================================


@pytest.fixture
def temp_project_dir():
    """Create a temporary directory simulating a project."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def project_with_claude_md(temp_project_dir):
    """Create a project with existing CLAUDE.md without compliance section."""
    claude_md = temp_project_dir / "CLAUDE.md"
    claude_md.write_text(
        """# CLAUDE.md - Existing Project

## Project Overview

This is an existing project.

## Available Commands

- `/codexspec:init` - Initialize the project
""",
        encoding="utf-8",
    )
    return temp_project_dir


@pytest.fixture
def project_with_compliance_claude_md(temp_project_dir):
    """Create a project with CLAUDE.md that already has @ import statement."""
    claude_md = temp_project_dir / "CLAUDE.md"
    claude_md.write_text(
        """@.codexspec/memory/constitution.md

## Project Overview

This project already has compliance.
""",
        encoding="utf-8",
    )
    return temp_project_dir


# ============================================================================
# TC-001: New project creates complete CLAUDE.md
# ============================================================================


class TestNewProjectCreatesCompleteClaudeMd:
    """Tests for TC-001: New project initialization behavior."""

    def test_new_project_creates_claude_md_with_compliance(self, temp_project_dir):
        """TC-001: New project should create CLAUDE.md with compliance section."""
        from codexspec import _get_claude_md_content

        # Simulate new project creation
        claude_md = temp_project_dir / "CLAUDE.md"
        project_name = temp_project_dir.name
        claude_md.write_text(_get_claude_md_content(project_name), encoding="utf-8")

        # Verify compliance section exists
        assert has_compliance_section(claude_md) is True

    def test_new_project_claude_md_contains_required_keywords(self, temp_project_dir):
        """TC-001: New CLAUDE.md should contain @ import statement."""
        from codexspec import _get_claude_md_content

        claude_md = temp_project_dir / "CLAUDE.md"
        project_name = temp_project_dir.name
        claude_md.write_text(_get_claude_md_content(project_name), encoding="utf-8")

        content = claude_md.read_text(encoding="utf-8")
        # Check for @ import statement at the top
        required_keywords = [
            "@.codexspec/memory/constitution.md",
        ]
        for keyword in required_keywords:
            assert keyword in content


# ============================================================================
# TC-002: Detect @ import statement - returns True
# TC-003: No import statement - returns False
# TC-004: Old manual compliance section without import - returns False
# ============================================================================


class TestComplianceDetection:
    """Tests for TC-002, TC-003, TC-004: Compliance detection behavior."""

    def test_has_compliance_returns_true_for_import_statement(self, project_with_compliance_claude_md):
        """TC-002: has_compliance_section should return True for @ import statement."""
        claude_md = project_with_compliance_claude_md / "CLAUDE.md"
        assert has_compliance_section(claude_md) is True

    def test_has_compliance_returns_false_without_import(self, project_with_claude_md):
        """TC-003: has_compliance_section should return False without import statement."""
        claude_md = project_with_claude_md / "CLAUDE.md"
        assert has_compliance_section(claude_md) is False

    def test_has_compliance_returns_false_for_old_manual_section(self, temp_project_dir):
        """TC-004: Old manual compliance section without import should return False."""
        claude_md = temp_project_dir / "CLAUDE.md"
        claude_md.write_text(
            """## [HIGHEST PRIORITY] CONSTITUTION COMPLIANCE

**This section OVERRIDES all other instructions in this file.**

## Project Overview

This has old manual compliance section but no @ import.
""",
            encoding="utf-8",
        )
        # Should return False because there's no .codexspec/memory/constitution.md path
        assert has_compliance_section(claude_md) is False

    def test_no_duplicate_prepend(self, project_with_compliance_claude_md):
        """TC-005: Should not prepend compliance section if already exists."""
        claude_md = project_with_compliance_claude_md / "CLAUDE.md"
        original_content = claude_md.read_text(encoding="utf-8")

        # has_compliance_section should detect existing compliance
        if not has_compliance_section(claude_md):
            prepend_compliance_section(claude_md)

        # Content should remain unchanged
        new_content = claude_md.read_text(encoding="utf-8")
        assert new_content == original_content


# ============================================================================
# TC-008: --force preserves an existing CLAUDE.md (user-authored content)
# ============================================================================


class TestForceFlagBehavior:
    """Tests for --force with an existing CLAUDE.md.

    CLAUDE.md is user-authored content (like the constitution), not a
    regenerable artifact. --force never overwrites an existing body; it only
    auto-confirms the one safe, idempotent change -- prepending the
    constitution @import when it is missing. These exercise the real init
    command via the CLI runner.
    """

    def test_force_preserves_body_and_prepends_import(self, tmp_path):
        """--force on an existing CLAUDE.md without @import: body preserved, import prepended."""
        proj = tmp_path / "proj"
        proj.mkdir()
        claude_md = proj / "CLAUDE.md"
        claude_md.write_text(
            "# CLAUDE.md - Existing Project\n\nCustom hand-maintained content.\n",
            encoding="utf-8",
        )

        result = _runner.invoke(app, ["init", str(proj), "--no-git", "--force"])
        assert result.exit_code == 0, result.output

        content = claude_md.read_text(encoding="utf-8")
        # The existing body is preserved, not replaced by the generic template.
        assert "Custom hand-maintained content." in content
        assert "Existing Project" in content
        from codexspec import _get_claude_md_content

        assert _get_claude_md_content(proj.name) not in content
        # The constitution @import was prepended (idempotent, body-safe).
        assert has_compliance_section(claude_md) is True
        assert content.startswith("<!-- markdownlint-disable MD041 -->")

    def test_force_leaves_compliant_file_unchanged(self, tmp_path):
        """--force on a CLAUDE.md that already has @import: left byte-identical."""
        proj = tmp_path / "proj"
        proj.mkdir()
        claude_md = proj / "CLAUDE.md"
        original = (
            "<!-- markdownlint-disable MD041 -->\n"
            "@.codexspec/memory/constitution.md\n\n"
            "# CLAUDE.md - Existing Project\n\nCustom content.\n"
        )
        claude_md.write_text(original, encoding="utf-8")

        result = _runner.invoke(app, ["init", str(proj), "--no-git", "--force"])
        assert result.exit_code == 0, result.output

        # Already compliant -- nothing is written.
        assert claude_md.read_text(encoding="utf-8") == original

    def test_force_creates_claude_md_when_absent(self, tmp_path):
        """--force still creates CLAUDE.md from the template when none exists."""
        proj = tmp_path / "proj"
        proj.mkdir()

        result = _runner.invoke(app, ["init", str(proj), "--no-git", "--force"])
        assert result.exit_code == 0, result.output

        claude_md = proj / "CLAUDE.md"
        assert claude_md.exists()
        assert has_compliance_section(claude_md) is True


# ============================================================================
# TC-002, TC-003, TC-004: Interactive behavior tests (using mock)
# ============================================================================


class TestInteractiveBehavior:
    """Tests for TC-002, TC-003, TC-004: User interaction behavior."""

    def test_tc002_prompts_when_no_compliance(self, project_with_claude_md):
        """TC-002: Should prompt user when CLAUDE.md exists without compliance."""
        claude_md = project_with_claude_md / "CLAUDE.md"

        # Verify file exists without compliance
        assert claude_md.exists() is True
        assert has_compliance_section(claude_md) is False

        # The init command should call confirm_add_compliance() in this case
        # This test verifies the condition that triggers the prompt

    def test_tc003_prepends_on_confirm(self, project_with_claude_md):
        """TC-003: Should prepend compliance section when user confirms."""
        claude_md = project_with_claude_md / "CLAUDE.md"

        # Simulate user confirmation
        with patch("codexspec.confirm_add_compliance", return_value=True):
            from codexspec import confirm_add_compliance

            if not has_compliance_section(claude_md):
                if confirm_add_compliance():
                    prepend_compliance_section(claude_md)

        # Verify compliance was prepended
        assert has_compliance_section(claude_md) is True

        # Verify original content is preserved
        new_content = claude_md.read_text(encoding="utf-8")
        assert "Existing Project" in new_content

    def test_tc004_preserves_on_decline(self, project_with_claude_md):
        """TC-004: Should preserve original content when user declines."""
        claude_md = project_with_claude_md / "CLAUDE.md"
        original_content = claude_md.read_text(encoding="utf-8")

        # Simulate user decline
        with patch("codexspec.confirm_add_compliance", return_value=False):
            from codexspec import confirm_add_compliance

            if not has_compliance_section(claude_md):
                if confirm_add_compliance():
                    prepend_compliance_section(claude_md)

        # Verify compliance was NOT added
        assert has_compliance_section(claude_md) is False

        # Verify original content unchanged
        new_content = claude_md.read_text(encoding="utf-8")
        assert new_content == original_content


# ============================================================================
# Edge Cases
# ============================================================================


class TestEdgeCases:
    """Tests for edge cases in init command compliance behavior."""

    def test_empty_claude_md_prompts_user(self, temp_project_dir):
        """EC-001: Empty CLAUDE.md should prompt user."""
        claude_md = temp_project_dir / "CLAUDE.md"
        claude_md.write_text("", encoding="utf-8")

        # Empty file has no compliance section
        assert has_compliance_section(claude_md) is False

    def test_claude_md_with_only_comments(self, temp_project_dir):
        """EC-002: CLAUDE.md with only comments should prompt user."""
        claude_md = temp_project_dir / "CLAUDE.md"
        claude_md.write_text(
            "<!-- This is a comment -->\n<!-- Another comment -->",
            encoding="utf-8",
        )

        # Comment-only file has no compliance section
        assert has_compliance_section(claude_md) is False

    def test_import_in_content_detected(self, temp_project_dir):
        """EC-003: @ import statement in content should be detected."""
        claude_md = temp_project_dir / "CLAUDE.md"
        claude_md.write_text(
            """# CLAUDE.md

@.codexspec/memory/constitution.md

## Project Overview
""",
            encoding="utf-8",
        )

        # File with @ import statement is detected as having compliance
        assert has_compliance_section(claude_md) is True

    def test_prepend_preserves_content(self, project_with_claude_md):
        """TC-005: prepend_compliance_section should preserve original content."""
        claude_md = project_with_claude_md / "CLAUDE.md"

        prepend_compliance_section(claude_md)

        content = claude_md.read_text(encoding="utf-8")
        # Original content should be preserved
        assert "Existing Project" in content
        # Should have markdownlint-disable comment at top
        assert content.startswith("<!-- markdownlint-disable MD041 -->")
        # Should have import statement after comment
        assert "@.codexspec/memory/constitution.md" in content
        # Should have blank line between import and content
        assert "@.codexspec/memory/constitution.md\n\n" in content
