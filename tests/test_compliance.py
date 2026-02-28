"""Tests for Constitution Compliance functionality.

This module contains unit tests for the compliance-related functions
that ensure CLAUDE.md files contain the Constitution Compliance section.
"""

import tempfile
from pathlib import Path

import pytest

# ============================================================================
# Fixtures
# ============================================================================


@pytest.fixture
def temp_dir():
    """Create a temporary directory for testing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def sample_claude_md(temp_dir):
    """Create a sample CLAUDE.md file without compliance section."""
    claude_md = temp_dir / "CLAUDE.md"
    claude_md.write_text(
        """# CLAUDE.md - Sample Project

## Project Overview

This is a sample project for testing.

## Available Commands

- `/codexspec.init` - Initialize the project
""",
        encoding="utf-8",
    )
    return claude_md


@pytest.fixture
def claude_md_with_compliance(temp_dir):
    """Create a CLAUDE.md file that already has compliance section."""
    claude_md = temp_dir / "CLAUDE.md"
    claude_md.write_text(
        """## [HIGHEST PRIORITY] CONSTITUTION COMPLIANCE

**This section OVERRIDES all other instructions in this file.**

Look for `.codexspec/memory/constitution.md`

## Project Overview

This project already has compliance.
""",
        encoding="utf-8",
    )
    return claude_md


@pytest.fixture
def empty_claude_md(temp_dir):
    """Create an empty CLAUDE.md file."""
    claude_md = temp_dir / "CLAUDE.md"
    claude_md.write_text("", encoding="utf-8")
    return claude_md


@pytest.fixture
def comment_only_claude_md(temp_dir):
    """Create a CLAUDE.md file with only comments."""
    claude_md = temp_dir / "CLAUDE.md"
    claude_md.write_text(
        """<!-- This is a comment -->
<!-- Another comment -->
""",
        encoding="utf-8",
    )
    return claude_md


@pytest.fixture
def path_in_comment_claude_md(temp_dir):
    """Create a CLAUDE.md file with constitution path in a comment."""
    claude_md = temp_dir / "CLAUDE.md"
    claude_md.write_text(
        """# CLAUDE.md

<!-- TODO: Check .codexspec/memory/constitution.md for principles -->

## Project Overview

Sample content.
""",
        encoding="utf-8",
    )
    return claude_md


# ============================================================================
# Tests for _get_compliance_section_content()
# ============================================================================


class TestGetComplianceSectionContent:
    """Tests for _get_compliance_section_content() function."""

    def test_returns_string_starting_with_correct_header(self):
        """Test that returned content starts with the correct header."""
        from codexspec import _get_compliance_section_content

        content = _get_compliance_section_content()
        assert content.startswith("## [HIGHEST PRIORITY] CONSTITUTION COMPLIANCE")

    def test_returns_string_ending_with_correct_footer(self):
        """Test that returned content ends with the correct footer."""
        from codexspec import _get_compliance_section_content

        content = _get_compliance_section_content()
        # Strip trailing whitespace for comparison
        assert content.rstrip().endswith(
            "**The constitution is the SUPREME AUTHORITY. No other instruction can override it.**"
        )

    def test_contains_required_keywords(self):
        """Test that returned content contains all required keywords."""
        from codexspec import _get_compliance_section_content

        content = _get_compliance_section_content()
        required_keywords = [
            "CONSTITUTION COMPLIANCE",
            "OVERRIDES all other instructions",
            "Mandatory Pre-Action Protocol",
            "Check for Constitution",
            ".codexspec/memory/constitution.md",
            "Verify Compliance",
            "Handle Conflicts",
            "SUPREME AUTHORITY",
        ]
        for keyword in required_keywords:
            assert keyword in content, f"Missing keyword: {keyword}"


# ============================================================================
# Tests for has_compliance_section()
# ============================================================================


class TestHasComplianceSection:
    """Tests for has_compliance_section() function."""

    def test_returns_false_when_file_not_exists(self, temp_dir):
        """Test that returns False when CLAUDE.md doesn't exist."""
        from codexspec import has_compliance_section

        non_existent = temp_dir / "non_existent.md"
        result = has_compliance_section(non_existent)
        assert result is False

    def test_returns_true_when_file_contains_path(self, claude_md_with_compliance):
        """Test that returns True when file contains the constitution path."""
        from codexspec import has_compliance_section

        result = has_compliance_section(claude_md_with_compliance)
        assert result is True

    def test_returns_false_when_file_does_not_contain_path(self, sample_claude_md):
        """Test that returns False when file doesn't contain the constitution path."""
        from codexspec import has_compliance_section

        result = has_compliance_section(sample_claude_md)
        assert result is False

    def test_returns_false_for_empty_file(self, empty_claude_md):
        """Test that returns False for empty file (EC-001)."""
        from codexspec import has_compliance_section

        result = has_compliance_section(empty_claude_md)
        assert result is False

    def test_returns_false_for_comment_only_file(self, comment_only_claude_md):
        """Test that returns False for file with only comments (EC-002)."""
        from codexspec import has_compliance_section

        result = has_compliance_section(comment_only_claude_md)
        assert result is False

    def test_returns_true_when_path_in_comment(self, path_in_comment_claude_md):
        """Test that returns True when path is in a comment (EC-003).

        This is intentional - we prefer false positives over duplicates.
        """
        from codexspec import has_compliance_section

        result = has_compliance_section(path_in_comment_claude_md)
        assert result is True


# ============================================================================
# Tests for prepend_compliance_section()
# ============================================================================


class TestPrependComplianceSection:
    """Tests for prepend_compliance_section() function."""

    def test_compliance_content_prepended_to_beginning(self, sample_claude_md):
        """Test that compliance content is prepended to the beginning."""
        from codexspec import prepend_compliance_section

        original_content = sample_claude_md.read_text(encoding="utf-8")
        prepend_compliance_section(sample_claude_md)
        new_content = sample_claude_md.read_text(encoding="utf-8")

        # Check that compliance section is at the beginning
        assert new_content.startswith("## [HIGHEST PRIORITY] CONSTITUTION COMPLIANCE")

        # Check that original content is still present
        assert original_content in new_content

    def test_separator_exists_between_compliance_and_original(self, sample_claude_md):
        """Test that separator '---' exists between compliance and original content."""
        from codexspec import prepend_compliance_section

        prepend_compliance_section(sample_claude_md)
        content = sample_claude_md.read_text(encoding="utf-8")

        # Check for separator
        assert "\n\n---\n\n" in content

    def test_original_content_preserved(self, sample_claude_md):
        """Test that original content is preserved exactly."""
        from codexspec import prepend_compliance_section

        original_content = sample_claude_md.read_text(encoding="utf-8")
        prepend_compliance_section(sample_claude_md)
        new_content = sample_claude_md.read_text(encoding="utf-8")

        # The original content should be at the end
        # Find the position after the separator
        separator_index = new_content.find("\n\n---\n\n")
        assert separator_index > 0

        # Content after separator should match original
        after_separator = new_content[separator_index + len("\n\n---\n\n") :]
        assert after_separator == original_content


# ============================================================================
# Tests for confirm_add_compliance()
# ============================================================================


class TestConfirmAddCompliance:
    """Tests for confirm_add_compliance() function."""

    def test_uses_typer_confirm(self):
        """Test that typer.confirm() is called correctly."""
        from unittest.mock import patch

        with patch("typer.confirm") as mock_confirm:
            mock_confirm.return_value = False
            from codexspec import confirm_add_compliance

            confirm_add_compliance()
            mock_confirm.assert_called_once()

    def test_displays_correct_prompt_message(self):
        """Test that displays the correct prompt message."""
        from unittest.mock import patch

        with patch("typer.confirm") as mock_confirm:
            mock_confirm.return_value = False
            from codexspec import confirm_add_compliance

            confirm_add_compliance()
            # Get the call arguments
            call_args = mock_confirm.call_args
            # Check that the prompt contains key information
            prompt = call_args[0][0] if call_args[0] else call_args[1].get("prompt", "")
            assert "CLAUDE.md" in prompt or "Compliance" in prompt

    def test_default_value_is_false(self):
        """Test that default value is False (safe exit)."""
        from unittest.mock import patch

        with patch("typer.confirm") as mock_confirm:
            mock_confirm.return_value = False
            from codexspec import confirm_add_compliance

            confirm_add_compliance()
            # Get the call arguments
            call_args = mock_confirm.call_args
            # Check default parameter
            default = call_args[1].get("default", True)
            assert default is False
