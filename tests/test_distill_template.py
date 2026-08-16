"""Contract tests for the distill command template's record format.

Covers the distill design-defect fixes D1-D5 (pitfall three-part body, the vetted
gate decoupled from derivation, the status enum, the confidence field, and the
pitfall example). Assertions target emphasis-free spans of the raw template text
(per pitfall P-2026-0813-1606fz-1: markdown emphasis inside a phrase breaks naive
substring assertions).
"""

from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
COMMANDS = ROOT / "templates" / "commands"


def read_command(name: str) -> str:
    return (COMMANDS / f"{name}.md").read_text(encoding="utf-8")


@pytest.fixture
def distill() -> str:
    return read_command("distill")


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


# --- T2.1: strategies/ and runbooks/ categories, bodies, examples (US1) ---


def test_distill_documents_runbooks_category(distill: str) -> None:
    """T2.1-S1 (US1-1): runbooks category with ordered steps + failure recovery."""
    assert "`runbooks/`" in distill
    assert "ordered multi-step procedures" in distill
    assert "failure-recovery" in distill


def test_distill_documents_strategies_category(distill: str) -> None:
    """T2.1-S2 (US1-2): strategies category with trigger + action body."""
    assert "`strategies/`" in distill
    assert "metacognitive" in distill
    assert "trigger" in distill
    assert "action" in distill


def test_distill_self_model_is_scope_self_strategy(distill: str) -> None:
    """T2.1-S3 (US1-3): the self-model is a strategy marked scope: self."""
    assert "is a strategy marked `scope: self`" in distill


def test_distill_anti_hollow_extends_to_new_types(distill: str) -> None:
    """T2.1-S4 (US1-4): an unstatable strategy/runbook is not recorded."""
    assert "the strategy or runbook is not yet worth recording" in distill


def test_distill_has_strategy_and_runbook_examples(distill: str) -> None:
    """T2.1-S5: worked strategy and runbook examples showing their body parts."""
    assert "S-2026-0813-1606fz-1" in distill  # strategy example
    assert "R-2026-0813-1143el-1" in distill  # runbook example
    assert "- trigger:" in distill
    assert "- action:" in distill
    assert "- steps:" in distill


def test_distill_has_no_facts_category(distill: str) -> None:
    """T2.1-S6 (REQ-012): no facts/ category is introduced.

    Verified by intent, not raw-substring absence: the store explicitly documents
    the deliberate exclusion, and `fact` is not one of the `type` enum values.
    """
    assert "There is **no** `facts/` category" in distill
    # `fact` is not a record type
    assert "| `fact`" not in distill
    assert "| `fact` " not in distill


# --- T2.2: operating model — near-moment + long-run + backstop (US4) ---


def test_distill_documents_near_moment_invocation(distill: str) -> None:
    """T2.2-S1 (US4-1): near-moment distill in any session incl. plain-chat/non-SDD."""
    assert "near the moment" in distill
    assert "any session" in distill
    assert "non-SDD fix" in distill


def test_distill_documents_longrun_along_the_way_with_backstop(distill: str) -> None:
    """T2.2-S2 (US4-2): long-running implement-tasks distills along the way; end backstop."""
    assert "along the way" in distill
    assert "backstop" in distill


# --- T2.3: debounce / session-boundary discipline (US4-3) ---


def test_distill_debounce_session_boundary_no_persistent_state(distill: str) -> None:
    """T2.3-S1: session-local already-distilled boundary held in context, no persistent state."""
    assert "session-local already-distilled boundary" in distill
    assert "no persistent runtime state" in distill


def test_distill_debounce_delta_only_early_exit(distill: str) -> None:
    """T2.3-S2: consecutive triggers process only the new delta and early-exit."""
    assert "substantive new delta" in distill
    assert "early-exit" in distill


def test_distill_debounce_cross_session_fallback(distill: str) -> None:
    """T2.3-S3: cross-session dedup falls back to reading the profile."""
    assert "falls back to reading the profile and skipping covered records" in distill


# --- T2.4: consolidation — mark clusters + /distill review merge (US3) ---


def test_distill_consolidation_marks_per_record_non_destructive(distill: str) -> None:
    """T2.4-S1 (US3-1): consolidation marks candidate clusters per-record, non-destructively."""
    assert "consolidation candidates" in distill
    assert "per-record field" in distill
    assert "does not auto-rewrite or delete" in distill


def test_distill_consolidation_no_central_index(distill: str) -> None:
    """T2.4-S2 (US3-1, CON-001): no central index/manifest is created."""
    assert "no central index" in distill


def test_distill_consolidation_merge_on_confirm(distill: str) -> None:
    """T2.4-S3 (US3-2): /distill review merges a cluster into general rule + exceptions."""
    assert "general rule plus its exceptions" in distill
    assert "/distill review" in distill


def test_distill_consolidation_cross_category_promotion(distill: str) -> None:
    """T2.4-S4 (US3-3): cross-category promotion (pitfalls -> strategy) is supported."""
    assert "promoting several" in distill
    assert "into one" in distill
