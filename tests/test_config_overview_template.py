"""Contracts for the no-argument interactive configuration overview."""

import re
from pathlib import Path

SOURCE = Path(__file__).resolve().parents[1] / "internal/command_templates/sources/config.md"


def _section(content: str, start: str, end: str) -> str:
    return content.split(start, 1)[1].split(end, 1)[0]


def _overview() -> str:
    return _section(SOURCE.read_text(encoding="utf-8"), "### Step 3: Interactive Mode", "#### Option: Modify config")


def test_s001_two_tables_precede_action_selection() -> None:
    overview = _overview()
    metadata = overview.index("#### Project metadata table")
    settings = overview.index("#### Adjustable settings table")
    actions = overview.index("#### Choose an action")
    assert metadata < settings < actions
    assert "Do not show raw YAML before the tables" in " ".join(overview.split())


def test_s002_exact_field_inventory() -> None:
    overview = _overview()
    metadata = _section(overview, "#### Project metadata table", "#### Adjustable settings table")
    settings = _section(overview, "#### Adjustable settings table", "#### Choose an action")

    def fields(text: str) -> list[str]:
        return re.findall(r"^\| `([^`]+)` \|", text, re.MULTILINE)

    assert fields(metadata) == ["version", "project.ai", "project.created"]
    assert fields(settings) == [
        "language.output",
        "language.interaction",
        "language.document",
        "language.commit",
        "workflow.auto_next",
        "workflow.auto_distill",
        "workflow.auto_maintenance",
        "workflow.worktrees",
        "review.decided_by",
    ]
    assert "language.templates" not in fields(metadata) + fields(settings)
    assert "unknown YAML" in overview


def test_s003_effective_fallback_rules() -> None:
    overview = _overview()
    for token in (
        "interaction/document/commit: explicit value → language.output → en",
        "workflow.auto_next: only literal true enables",
        "workflow.auto_distill: only literal false disables",
        "workflow.auto_maintenance: absent means true",
        "workflow.worktrees: only literal false disables",
        "review.decided_by: absent means reviewer",
    ):
        assert token in overview


def test_s004_actions_follow_tables_and_view_only_exits() -> None:
    overview = _overview()
    actions = _section(overview, "#### Choose an action", "Then handle each option:")
    assert actions.count('"label":') == 3
    for label in ("Modify config", "Reset to defaults", "View only"):
        assert f'"label": "{label}"' in actions
    assert "View only: exit without writing or creating a worktree" in overview


def test_s005_other_entry_paths_remain_separate() -> None:
    content = SOURCE.read_text(encoding="utf-8")
    view = _section(content, "### Step 2: View Mode", "### Step 3: Interactive Mode")
    assert "{file contents}" in view
    assert "### Step 4: Create New Configuration" in content
    assert "#### Option: Modify config" in content
    assert "#### Option: Reset to defaults" in content


def test_s006_metadata_absence_and_creation_rule() -> None:
    overview = _overview()
    metadata = _section(overview, "#### Project metadata table", "#### Adjustable settings table")
    assert "creation date" in metadata
    assert "If a metadata key is absent, show not set" in overview
