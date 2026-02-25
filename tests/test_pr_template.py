"""
Tests for PR template (templates/commands/pr.md).

This module validates the structure and content of the PR description generator template.
"""

from pathlib import Path

import pytest

# Template file path
TEMPLATE_PATH = Path(__file__).parent.parent / "templates" / "commands" / "pr.md"


class TestTemplateExists:
    """Test that the template file exists and is accessible."""

    def test_template_file_exists(self):
        """Verify the template file exists at the expected path."""
        assert TEMPLATE_PATH.exists(), f"Template file not found at {TEMPLATE_PATH}"

    def test_template_file_is_not_empty(self):
        """Verify the template file is not empty."""
        content = TEMPLATE_PATH.read_text(encoding="utf-8")
        assert len(content) > 0, "Template file is empty"


class TestYAMLFrontmatter:
    """Test the YAML frontmatter structure."""

    @pytest.fixture
    def template_content(self):
        """Load template content."""
        return TEMPLATE_PATH.read_text(encoding="utf-8")

    def test_has_yaml_frontmatter(self, template_content):
        """Verify the template starts with YAML frontmatter."""
        assert template_content.startswith("---"), "Template must start with YAML frontmatter"

    def test_has_description_field(self, template_content):
        """Verify the frontmatter contains a description field."""
        # Find the frontmatter section
        frontmatter_end = template_content.find("---", 3)
        assert frontmatter_end != -1, "YAML frontmatter not properly closed"
        frontmatter = template_content[:frontmatter_end]

        assert "description:" in frontmatter, "Frontmatter must contain 'description' field"

    def test_has_allowed_tools_field(self, template_content):
        """Verify the frontmatter contains allowed-tools field."""
        frontmatter_end = template_content.find("---", 3)
        frontmatter = template_content[:frontmatter_end]

        assert "allowed-tools:" in frontmatter, "Frontmatter must contain 'allowed-tools' field"

    def test_allowed_tools_includes_git_commands(self, template_content):
        """Verify allowed-tools includes necessary git commands."""
        frontmatter_end = template_content.find("---", 3)
        frontmatter = template_content[:frontmatter_end]

        required_commands = ["git branch", "git diff", "git log", "git remote"]
        for cmd in required_commands:
            assert cmd in frontmatter, f"allowed-tools must include '{cmd}'"


class TestRequiredSections:
    """Test that all required sections are present in the template."""

    @pytest.fixture
    def template_content(self):
        """Load template content."""
        return TEMPLATE_PATH.read_text(encoding="utf-8")

    def test_has_language_preference_section(self, template_content):
        """Verify the template has a Language Preference section."""
        assert "## Language Preference" in template_content, "Template must have Language Preference section"

    def test_has_git_context_section(self, template_content):
        """Verify the template has a Git Context Collection section."""
        assert "## Git Context Collection" in template_content, "Template must have Git Context Collection section"

    def test_has_platform_detection_section(self, template_content):
        """Verify the template has a Platform Detection section."""
        assert "## Platform Detection" in template_content, "Template must have Platform Detection section"

    def test_has_parameters_section(self, template_content):
        """Verify the template has a Parameters section."""
        assert "## Parameters" in template_content, "Template must have Parameters section"

    def test_has_spec_integration_section(self, template_content):
        """Verify the template has a Spec.md Integration section."""
        assert "## Spec.md Integration" in template_content, "Template must have Spec.md Integration section"

    def test_has_pr_title_generation_section(self, template_content):
        """Verify the template has a PR Title Generation section."""
        assert "## PR Title Generation" in template_content, "Template must have PR Title Generation section"

    def test_has_test_file_discovery_section(self, template_content):
        """Verify the template has a Test File Discovery section."""
        assert "## Test File Discovery" in template_content, "Template must have Test File Discovery section"

    def test_has_project_command_detection_section(self, template_content):
        """Verify the template has a Project Command Detection section."""
        assert "## Project Command Detection" in template_content, (
            "Template must have Project Command Detection section"
        )

    def test_has_section_generation_section(self, template_content):
        """Verify the template has a Section Generation section."""
        assert "## Section Generation" in template_content, "Template must have Section Generation section"

    def test_has_output_format_section(self, template_content):
        """Verify the template has an Output Format section."""
        assert "## Output Format" in template_content, "Template must have Output Format section"

    def test_has_edge_cases_section(self, template_content):
        """Verify the template has an Edge Cases section."""
        assert "## Edge Cases" in template_content, "Template must have Edge Cases section"


class TestParameterDocumentation:
    """Test that all parameters are documented."""

    @pytest.fixture
    def template_content(self):
        """Load template content."""
        return TEMPLATE_PATH.read_text(encoding="utf-8")

    def test_target_branch_parameter_documented(self, template_content):
        """Verify --target-branch parameter is documented with default value."""
        assert "--target-branch" in template_content, "--target-branch parameter must be documented"
        assert "origin/main" in template_content, "Default value 'origin/main' must be documented"

    def test_output_parameter_documented(self, template_content):
        """Verify --output parameter is documented."""
        assert "--output" in template_content, "--output parameter must be documented"

    def test_sections_parameter_documented(self, template_content):
        """Verify --sections parameter is documented with valid values."""
        assert "--sections" in template_content, "--sections parameter must be documented"
        # Check for valid section values
        valid_sections = ["context", "implementation", "testing", "verify", "all"]
        for section in valid_sections:
            assert section in template_content.lower(), f"Section value '{section}' must be documented"

    def test_spec_parameter_documented(self, template_content):
        """Verify --spec parameter is documented as opt-in."""
        assert "--spec" in template_content, "--spec parameter must be documented"
        # Verify opt-in behavior is mentioned
        assert "opt-in" in template_content.lower() or "Opt-in" in template_content, (
            "--spec opt-in behavior must be documented"
        )


class TestLanguagePriority:
    """Test that language priority is correctly specified."""

    @pytest.fixture
    def template_content(self):
        """Load template content."""
        return TEMPLATE_PATH.read_text(encoding="utf-8")

    def test_language_commit_priority(self, template_content):
        """Verify language.commit has highest priority."""
        # Find the Language Preference section
        lang_section_start = template_content.find("## Language Preference")
        assert lang_section_start != -1, "Language Preference section not found"

        # Get the language preference section (until next ## heading)
        lang_section_end = template_content.find("\n## ", lang_section_start + 1)
        if lang_section_end == -1:
            lang_section = template_content[lang_section_start:]
        else:
            lang_section = template_content[lang_section_start:lang_section_end]

        # Check priority order
        assert "language.commit" in lang_section, "language.commit must be mentioned"
        assert "language.output" in lang_section, "language.output must be mentioned"

        # Verify commit comes before output (priority)
        commit_pos = lang_section.find("language.commit")
        output_pos = lang_section.find("language.output")
        assert commit_pos < output_pos, "language.commit should have higher priority than language.output"


class TestPlatformDetection:
    """Test platform detection logic."""

    @pytest.fixture
    def template_content(self):
        """Load template content."""
        return TEMPLATE_PATH.read_text(encoding="utf-8")

    def test_github_detection_documented(self, template_content):
        """Verify GitHub detection is documented."""
        assert "github.com" in template_content.lower(), "GitHub detection must be documented"
        assert "Pull Request" in template_content, "GitHub terminology must be documented"

    def test_gitlab_detection_documented(self, template_content):
        """Verify GitLab detection is documented."""
        assert "gitlab.com" in template_content.lower(), "GitLab detection must be documented"
        assert "Merge Request" in template_content, "GitLab terminology must be documented"

    def test_no_remote_handling_documented(self, template_content):
        """Verify handling of no remote is documented."""
        assert "no remote" in template_content.lower() or "No Remote" in template_content, (
            "No remote handling must be documented"
        )


class TestEdgeCases:
    """Test edge case handling documentation."""

    @pytest.fixture
    def template_content(self):
        """Load template content."""
        return TEMPLATE_PATH.read_text(encoding="utf-8")

    def test_no_changes_edge_case(self, template_content):
        """Verify EC-001 (no changes) is documented."""
        assert "No changes detected" in template_content or "no changes" in template_content.lower(), (
            "EC-001 (no changes) must be documented"
        )

    def test_invalid_branch_edge_case(self, template_content):
        """Verify EC-002 (invalid branch) is documented."""
        assert "Target branch" in template_content or "Invalid target" in template_content, (
            "EC-002 (invalid branch) must be documented"
        )

    def test_not_git_repo_edge_case(self, template_content):
        """Verify EC-003 (not a git repo) is documented."""
        assert "Not a git repository" in template_content, "EC-003 must be documented"

    def test_detached_head_edge_case(self, template_content):
        """Verify EC-005 (detached HEAD) is documented."""
        assert "detached HEAD" in template_content.lower() or "Detached HEAD" in template_content, (
            "EC-005 (detached HEAD) must be documented"
        )
