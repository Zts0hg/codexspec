"""Contract tests for the debug command and its implement-tasks escalation.

Scenario numbers refer to the T-005 Test Scenarios in
.codexspec/specs/2026-0811-1418yq-debug-command/tasks.md.
"""

from pathlib import Path

from codexspec.translator import extract_frontmatter_fields

ROOT = Path(__file__).parent.parent
COMMANDS = ROOT / "templates" / "commands"


def read_command(name: str) -> str:
    return (COMMANDS / f"{name}.md").read_text(encoding="utf-8")


# --- Standalone debug command (debug.md) ---


def test_debug_frontmatter_has_description_and_argument_hint() -> None:
    """Scenario 1."""
    fields = extract_frontmatter_fields(read_command("debug"))
    assert fields.get("description")
    assert fields.get("argument-hint")


def test_debug_contains_four_phases_and_iron_law() -> None:
    """Scenario 2 (REQ-002)."""
    content = read_command("debug")
    assert "NO FIX BEFORE ROOT CAUSE" in content
    for phase in [
        "Phase 1 — Root-Cause Investigation",
        "Phase 2 — Pattern Analysis",
        "Phase 3 — Hypothesis & Verification",
        "Phase 4 — Fix",
    ]:
        assert phase in content


def test_debug_contains_architecture_gate() -> None:
    """Scenario 3 (REQ-003)."""
    content = read_command("debug")
    assert "Architecture Gate" in content
    assert "three fixes" in content.lower()


def test_debug_symptom_intake_reproduce_or_ask() -> None:
    """Scenario 4 (REQ-004 / SC-005): no fix before a stable reproduction."""
    content = read_command("debug")
    assert "## Symptom Intake" in content
    assert "reproduce-or-ask" in content
    assert "unreproduced symptom" in content


def test_debug_has_language_preference() -> None:
    """Scenario 5."""
    assert "## Language Preference" in read_command("debug")


# --- implement-tasks escalation (implement-tasks.md) ---


def _escalation_section() -> str:
    content = read_command("implement-tasks")
    assert "## Systematic Debugging Escalation" in content
    return content.split("## Systematic Debugging Escalation", 1)[1].split("\n## ", 1)[0]


def test_implement_tasks_escalation_references_debug_with_resume() -> None:
    """Scenario 6 (REQ-005 / SC-002)."""
    section = _escalation_section()
    assert "Invoke /codexspec:debug" in section
    assert "Resume" in section
    assert "return here and continue" in section


def test_implement_tasks_escalation_states_both_trips_and_narrowing() -> None:
    """Scenario 7 (REQ-006)."""
    section = _escalation_section()
    assert "(a) During the TDD" in section
    assert "(b) During a test-safe repair" in section
    assert "non-trivial" in section
    for excluded in ["idiomatic-clarity", "architecture", "constitution", "style", "trivial"]:
        assert excluded in section


def test_discipline_not_duplicated_in_implement_tasks() -> None:
    """Scenario 8 (NFR-001 / SC-001): the four-phase discipline lives only in debug.md."""
    impl = read_command("implement-tasks")
    assert "Root-Cause Investigation" not in impl
    assert "Pattern Analysis" not in impl
    assert "Hypothesis & Verification" not in impl


# --- review-code stays review-only; no config key ---


def test_review_code_does_not_reference_debug() -> None:
    """Scenario 9 (REQ-006 / SC-004): review-code stays review-only, unmodified."""
    assert "/codexspec:debug" not in read_command("review-code")


def test_no_auto_debug_config_key_introduced() -> None:
    """Scenario 10 (NFR-003 / SC-003)."""
    for cmd in ["config", "debug", "implement-tasks"]:
        assert "auto_debug" not in read_command(cmd)
