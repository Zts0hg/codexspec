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
        """@.codexspec/memory/constitution.md

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
    """Create a CLAUDE.md file with constitution import in a comment."""
    claude_md = temp_dir / "CLAUDE.md"
    claude_md.write_text(
        """# CLAUDE.md

<!-- Import: @.codexspec/memory/constitution.md -->

## Project Overview

Sample content.
""",
        encoding="utf-8",
    )
    return claude_md


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

    def test_returns_true_when_import_in_comment(self, path_in_comment_claude_md):
        """Test that returns True when @ import is in a comment (EC-003).

        The function detects the @ import statement even in comments.
        """
        from codexspec import has_compliance_section

        result = has_compliance_section(path_in_comment_claude_md)
        assert result is True


# ============================================================================
# Tests for prepend_compliance_section()
# ============================================================================


class TestPrependComplianceSection:
    """Tests for prepend_compliance_section() function."""

    def test_import_statement_prepended_to_beginning(self, sample_claude_md):
        """Test that @ import statement is prepended to the beginning."""
        from codexspec import prepend_compliance_section

        original_content = sample_claude_md.read_text(encoding="utf-8")
        prepend_compliance_section(sample_claude_md)
        new_content = sample_claude_md.read_text(encoding="utf-8")

        # Check that markdownlint-disable comment is at the very beginning
        assert new_content.startswith("<!-- markdownlint-disable MD041 -->")

        # Check that @ import statement follows
        assert "@.codexspec/memory/constitution.md" in new_content

        # Check that original content is still present
        assert original_content in new_content

    def test_blank_line_between_import_and_content(self, sample_claude_md):
        """Test that blank line exists between import and original content."""
        from codexspec import prepend_compliance_section

        prepend_compliance_section(sample_claude_md)
        content = sample_claude_md.read_text(encoding="utf-8")

        # Check for blank line after import statement
        assert "@.codexspec/memory/constitution.md\n\n" in content

    def test_markdownlint_disable_comment_present(self, sample_claude_md):
        """Test that markdownlint-disable MD041 comment is present."""
        from codexspec import prepend_compliance_section

        prepend_compliance_section(sample_claude_md)
        content = sample_claude_md.read_text(encoding="utf-8")

        # Check for markdownlint-disable comment
        assert "<!-- markdownlint-disable MD041 -->" in content

        # Check that it's on the first line
        first_line = content.split("\n")[0]
        assert first_line == "<!-- markdownlint-disable MD041 -->"

    def test_original_content_preserved(self, sample_claude_md):
        """Test that original content is preserved exactly."""
        from codexspec import prepend_compliance_section

        original_content = sample_claude_md.read_text(encoding="utf-8")
        prepend_compliance_section(sample_claude_md)
        new_content = sample_claude_md.read_text(encoding="utf-8")

        # The original content should be after the import statement
        # Find the position after the import prefix (including markdownlint-disable)
        import_prefix = "<!-- markdownlint-disable MD041 -->\n@.codexspec/memory/constitution.md\n\n"
        assert new_content.startswith(import_prefix)

        # Content after import should match original
        after_import = new_content[len(import_prefix) :]
        assert after_import == original_content


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
