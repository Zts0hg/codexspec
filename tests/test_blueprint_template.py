"""Contract tests for the blueprint agent command."""

import re
from pathlib import Path

TEMPLATE = (Path(__file__).parents[1] / "templates/commands/blueprint.md").read_text(encoding="utf-8")


def test_blueprint_uses_language_profile_and_product_context() -> None:
    for phrase in (
        "language.interaction",
        "language.document",
        ".codexspec/memory/constitution.md",
        ".codexspec/profile/",
        ".codexspec/specs/",
        "Ask one material question at a time",
        "explicit user confirmation",
    ):
        assert phrase in TEMPLATE
    assert re.search(r"every current\s+blueprint block", TEMPLATE)


def test_blueprint_mutates_only_through_exact_helper_operations() -> None:
    assert "codexspec _blueprint-helper inspect --ensure" in TEMPLATE
    assert "codexspec _blueprint-helper apply" in TEMPLATE
    for operation in (
        "append_requirement",
        "replace_pending_requirement",
        "delete_pending_requirement",
        "move_pending_requirement",
    ):
        assert operation in TEMPLATE
    assert "must never send `update_status`" in TEMPLATE
    assert "never write `.codexspec/blueprint.md` directly" in TEMPLATE


def test_blueprint_defines_pending_boundaries_and_conflict_retry() -> None:
    assert "Never modify, delete, or move" in TEMPLATE
    assert "`in_progress` and `completed`" in TEMPLATE
    assert "`conflict`: inspect again" in TEMPLATE
    assert "Do not reuse the stale hash" in TEMPLATE
    assert "`merge_in_progress` transport failure" in TEMPLATE
    assert "retry the same confirmed intent" in TEMPLATE
    assert "never creates a feature directory" in TEMPLATE
