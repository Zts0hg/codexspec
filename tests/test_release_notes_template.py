"""Contract tests for the release-notes command template.

Scenario numbers (S-ids) refer to the Test Scenarios in
.codexspec/specs/2026-0813-1143el-release-notes/tasks.md.

release-notes behavior is a prose command template, so these assert the template's required
sections and rules (the same style as tests/test_debug_template.py and
tests/test_spec_to_design_templates.py).
"""

import json
from pathlib import Path

ROOT = Path(__file__).parent.parent
TEMPLATE = ROOT / "templates" / "commands" / "release-notes.md"
EN_CATALOG = ROOT / "templates" / "translations" / "en.json"


def content() -> str:
    return TEMPLATE.read_text(encoding="utf-8")


# --- T1.1: scaffold, frontmatter, house sections ---


def test_s1_1_frontmatter_allowed_tools() -> None:
    """S1.1: frontmatter allowed-tools include read-only git plus Read/Edit/Write."""
    c = content()
    assert "allowed-tools:" in c
    assert "Bash(git" in c
    for tool in ("Read", "Edit", "Write"):
        assert tool in c


def test_s1_2_language_and_constitution_sections() -> None:
    """S1.2."""
    c = content()
    assert "## Language Preference" in c
    assert "## Constitution Compliance" in c


def test_s1_3_parameters_documented() -> None:
    """S1.3."""
    c = content()
    assert "## Parameters" in c
    for param in ("--version", "--from", "--to", "--output", "--spec"):
        assert param in c


def test_s1_4_forbids_ai_attribution() -> None:
    """S1.4."""
    assert "AI attribution" in content()


def test_s1_5_edge_cases_section() -> None:
    """S1.5."""
    c = content()
    assert "## Edge Cases" in c
    assert "Not a git repository" in c
    assert "Empty range" in c
    assert "Detached HEAD" in c


def test_s1_6_unresolved_spec_degrades() -> None:
    """S1.6."""
    c = content()
    assert "Unresolved `--spec`" in c
    assert "proceed from git alone" in c


# --- T1.2: range resolution ---


def test_s2_1_default_range_latest_tag() -> None:
    """S2.1."""
    c = content()
    assert "## Range Resolution" in c
    assert "latest tag..HEAD" in c
    assert "git describe --tags --abbrev=0" in c


def test_s2_2_no_tag_falls_back_to_changelog() -> None:
    """S2.2."""
    assert "after the last version recorded in `CHANGELOG.md`" in content()


def test_s2_3_no_tag_no_changelog_full_history() -> None:
    """S2.3."""
    assert "full history" in content()


def test_s2_4_from_to_override() -> None:
    """S2.4."""
    c = content()
    assert "Explicit override" in c


def test_s2_5_no_merges() -> None:
    """S2.5."""
    assert "--no-merges" in content()


# --- T1.3: categorization, completeness, contributor split ---


def test_s3_1_keep_a_changelog_categories() -> None:
    """S3.1."""
    c = content()
    for category in ("### Added", "### Changed", "### Deprecated", "### Removed", "### Fixed", "### Security"):
        assert category in c


def test_s3_2_contributor_split() -> None:
    """S3.2."""
    c = content()
    assert "### For contributors" in c
    for kind in ("feat", "fix", "perf", "chore", "refactor"):
        assert kind in c


def test_s3_3_completeness_cross_check() -> None:
    """S3.3."""
    c = content()
    assert "must map to at least one bullet" in c


def test_s3_4_infer_without_conventional_commits() -> None:
    """S3.4."""
    c = content()
    assert "Conventional commits are used when present but are NOT required" in c
    assert "infer" in c.lower()


# --- T1.4: version handling ---


def test_s4_1_unreleased_default_no_date() -> None:
    """S4.1."""
    c = content()
    assert "## [Unreleased]" in c
    assert "no date" in c


def test_s4_2_version_stamps_and_short_circuits() -> None:
    """S4.2."""
    c = content()
    assert "## [X.Y.Z] - <YYYY-MM-DD>" in c
    assert "short-circuits all version inference" in c


def test_s4_3_guarded_advisory_gated() -> None:
    """S4.3."""
    assert "semver AND conventional commits" in content()


def test_s4_4_silent_otherwise() -> None:
    """S4.4."""
    assert "Otherwise stay silent" in content()


def test_s4_5_never_writes_version_to_file() -> None:
    """S4.5."""
    assert "never write a version number into the file on its own" in content()


def test_s4_6_malformed_version_rejected() -> None:
    """S4.6."""
    c = content()
    assert "Malformed `--version`" in c
    assert "write no malformed section" in c


# --- T1.5: CHANGELOG maintenance + release body ---


def test_s5_1_creates_standard_header() -> None:
    """S5.1."""
    c = content()
    assert "# Changelog" in c
    assert "Keep a Changelog" in c


def test_s5_2_additive_never_rewrite() -> None:
    """S5.2."""
    assert "Never rewrite, reorder, or delete" in content()


def test_s5_3_merge_into_existing_unreleased() -> None:
    """S5.3."""
    c = content()
    assert "into an existing `## [Unreleased]` section when one is present" in c
    assert "rather than duplicating" in c


def test_s5_4_never_write_overwrite() -> None:
    """S5.4."""
    assert "use `Write` to overwrite the whole" in content()


def test_s5_5_never_mutates_git_state() -> None:
    """S5.5."""
    c = content()
    assert "MUST NEVER modify the git staging area" in c
    assert "MUST NEVER create a commit" in c


# --- T3.3 / S7.1: no translation-catalog entry ---


def test_s7_1_no_translation_catalog_entry() -> None:
    """S7.1: release-notes installs with English frontmatter (no en.json entry)."""
    data = json.loads(EN_CATALOG.read_text(encoding="utf-8"))
    assert "release-notes" not in data
