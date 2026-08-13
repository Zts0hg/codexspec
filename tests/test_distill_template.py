"""Contract tests for the distill command template's record format.

Covers the distill design-defect fixes D1-D5 (pitfall three-part body, the vetted
gate decoupled from derivation, the status enum, the confidence field, and the
pitfall example). Assertions target emphasis-free spans of the raw template text
(per pitfall P-2026-0813-1606fz-1: markdown emphasis inside a phrase breaks naive
substring assertions).
"""

from pathlib import Path

ROOT = Path(__file__).parent.parent
COMMANDS = ROOT / "templates" / "commands"


def read_command(name: str) -> str:
    return (COMMANDS / f"{name}.md").read_text(encoding="utf-8")


# --- D1: pitfall records require root-cause / workaround / lesson ---


def test_distill_pitfall_requires_three_part_body() -> None:
    content = read_command("distill")
    assert "root-cause" in content
    assert "workaround" in content
    assert "lesson" in content
    assert "spell out three body parts" in content


def test_distill_has_anti_hollow_rule() -> None:
    content = read_command("distill")
    assert "If you cannot state all three" in content
    assert "the next person just re-hits it" in content


# --- D6: a pitfall example exists alongside the convention example ---


def test_distill_has_both_a_convention_and_a_pitfall_example() -> None:
    content = read_command("distill")
    assert "Con-2026-0809-2219gg-1" in content  # convention example
    assert "P-2026-0810-1330ab-1" in content  # pitfall example
    # the pitfall example demonstrates the three-part body inside the fenced block
    assert "- root-cause:" in content
    assert "- workaround:" in content
    assert "- lesson:" in content


# --- D2: the vetted gate is decoupled from derivation (option A) ---


def test_distill_vetted_gate_decoupled_from_derivation() -> None:
    content = read_command("distill")
    # human endorsement can come from explicit words OR /distill review approval
    assert "the user approved it in" in content
    assert "outcome-verified and human-approved becomes" in content
    # derivation is explicitly not a gate
    assert "not** itself a gate" in content or "is **not** a gate" in content
    # the old blocking rule is gone
    assert "every `inferred` item stays `candidate`" not in content


def test_distill_review_supplies_human_endorsement() -> None:
    content = read_command("distill")
    assert "human endorsement half" in content
    assert "/codexspec:onboard" in content  # names onboard as the inferred-knowledge path to vetted


# --- D4: status enum includes conflict/needs-adjudication ---


def test_distill_status_enum_lists_conflict_value() -> None:
    content = read_command("distill")
    assert "`candidate` | `vetted` | `conflict/needs-adjudication`" in content


# --- D5: provenance carries a confidence field ---


def test_distill_provenance_has_confidence() -> None:
    content = read_command("distill")
    assert "confidence = high | medium | low" in content


# --- D3: lightweight self-check before finishing ---


def test_distill_has_self_check_section() -> None:
    content = read_command("distill")
    assert "## Self-check before finishing" in content
    assert "Not hollow" in content
    assert "Links resolve" in content


# --- D2 cross-file: onboard.md aligned (inferred origin is not a permanent barrier) ---


def test_onboard_records_are_vettable_later() -> None:
    content = read_command("onboard")
    assert "requires an explicit source" not in content  # old, now-wrong claim removed
    assert "can later be promoted to `vetted` via `/distill review`" in content
