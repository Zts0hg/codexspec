"""Contract tests for the onboard command template.

Scenario numbers refer to the T3.1 Test Scenarios in
.codexspec/specs/2026-0813-1606fz-onboard/tasks.md.

onboard is a pure agent-driven command template (like distill/debug); these tests assert its
written discipline — the behavior the template instructs — not runtime execution.
"""

from pathlib import Path

from codexspec.translator import extract_frontmatter_fields

ROOT = Path(__file__).parent.parent
COMMANDS = ROOT / "templates" / "commands"


def read_command(name: str) -> str:
    return (COMMANDS / f"{name}.md").read_text(encoding="utf-8")


# --- S1.1 frontmatter ---


def test_onboard_frontmatter_has_description_and_path_hint() -> None:
    """S1.1 (REQ-007)."""
    fields = extract_frontmatter_fields(read_command("onboard"))
    assert fields.get("description")
    assert "[path]" in (fields.get("argument-hint") or "")


# --- S1.2 language regime is interaction/document, not commit ---


def test_onboard_language_preference_interaction_and_document_not_commit() -> None:
    """S1.2 (NFR-001)."""
    content = read_command("onboard")
    assert "## Language Preference" in content
    assert "language.interaction" in content
    assert "language.document" in content
    assert "language.commit" not in content


# --- S1.3 / S1.4 / S1.5 scan model ---


def test_onboard_scan_high_signal_and_gitignore_with_no_git_fallback() -> None:
    """S1.3 (REQ-007)."""
    content = read_command("onboard")
    assert "high-signal" in content.lower()
    assert ".gitignore" in content
    assert "no git" in content.lower()


def test_onboard_scan_is_streaming_and_resumable() -> None:
    """S1.4 (REQ-006)."""
    content = read_command("onboard")
    assert "resumable" in content.lower()
    assert "block until the whole scan finishes" in content


def test_onboard_supports_path_narrowing() -> None:
    """S1.5 (REQ-007)."""
    content = read_command("onboard")
    assert "`[path]`" in content
    assert "narrow" in content.lower()


# --- S1.6 extraction scope; never decisions/pitfalls ---


def test_onboard_extracts_only_conventions_and_constraints() -> None:
    """S1.6 (REQ-003, OUT-001); T3.1-S1: exclusion extended to strategies/runbooks."""
    content = read_command("onboard")
    assert "onboard **never** extracts `decisions`, `pitfalls`, `strategies`, or `runbooks`" in content
    assert "`conventions`" in content
    assert "`constraints`" in content


def test_onboard_exclusion_extended_at_both_sites() -> None:
    """T3.1-S2: both the extraction-scope paragraph and the Boundaries bullet exclude the four.

    Neither site may still name only the old two-category exclusion.
    """
    content = read_command("onboard")
    # both occurrences carry strategies + runbooks
    assert content.count("`strategies`, or `runbooks`") == 2
    # no site still stops at the old "decisions or pitfalls" phrasing
    assert "never `decisions` or `pitfalls`" not in content
    assert "extracts `decisions` or `pitfalls`" not in content


def test_onboard_still_writes_only_conventions_and_constraints() -> None:
    """T3.1-S3: onboard still writes only conventions + constraints."""
    content = read_command("onboard")
    assert "Writes only `conventions` and `constraints`" in content


def test_onboard_category_count_is_six_everywhere() -> None:
    """T3.1: no stale four-category total survives (extracts two of the SIX)."""
    content = read_command("onboard")
    assert "two** of the six profile categories" in content
    # no reference frames the store as four total categories
    assert "of the four profile categories" not in content


# --- S1.7 constraints only from explicit config-level prohibitions ---


def test_onboard_constraints_need_explicit_signal_and_anchor() -> None:
    """S1.7 (REQ-009)."""
    content = read_command("onboard")
    assert "explicit hard prohibitions" in content
    assert "propose no constraint" in content
    assert "evidence anchor" in content


# --- S1.8 conventions immediate candidate + async /distill review ---


def test_onboard_conventions_take_immediate_effect_async_review() -> None:
    """S1.8 (REQ-004)."""
    content = read_command("onboard")
    assert "written immediately as `candidate`" in content
    assert "/distill review" in content


# --- S1.9 constraints inline pre-persist gate, not vet ---


def test_onboard_constraints_gate_is_persist_decision_not_vet() -> None:
    """S1.9 (REQ-005)."""
    content = read_command("onboard")
    assert "persist / do-not-persist" in content
    assert "not** a promotion to `vetted`" in content
    assert "not** an invocation of `/distill review`" in content


# --- S1.10 record format reuse + onboard deltas ---


def test_onboard_reuses_distill_format_with_deltas() -> None:
    """S1.10 (REQ-011, REQ-012)."""
    content = read_command("onboard")
    assert "reuses `distill`'s profile store and record format" in content
    assert "derivation: inferred" in content
    assert "always **`candidate`**" in content
    assert "onboard **never** writes `vetted`" in content
    assert "concrete code observation" in content
    assert "provenance" in content


# --- S1.11 never clobber ---


def test_onboard_never_clobbers_existing_records() -> None:
    """S1.11 (REQ-010)."""
    content = read_command("onboard")
    assert "Never clobber" in content
    assert "vetted" in content
    assert "hand-authored" in content


# --- S1.12 integration / dedup / idempotent ---


def test_onboard_integrates_dedups_idempotent() -> None:
    """S1.12 (REQ-008)."""
    content = read_command("onboard")
    assert "read the existing profile" in content
    assert "De-duplicate" in content
    assert "idempotent" in content


# --- S1.13 prerequisite + scaffold ---


def test_onboard_prerequisite_and_scaffold() -> None:
    """S1.13 (REQ-015); scaffold matches init's six categories, not the stale four."""
    content = read_command("onboard")
    assert "codexspec init" in content
    assert "six category directories" in content
    # the scaffold-prerequisite line must name the two new categories so its
    # rebuild matches init and leaves no dangling pointer-block reference
    assert "strategies,runbooks" in content


# --- S1.14 read-only code / write-only profile ---


def test_onboard_read_only_code_write_only_profile() -> None:
    """S1.14 (REQ-014)."""
    content = read_command("onboard")
    assert "read-only on the codebase" in content
    assert "write-only to `.codexspec/profile/`" in content
    assert "never modifies source, tests, git state, or the constitution" in content


# --- S1.15 standalone, no auto-next, no auto-distill ---


def test_onboard_is_standalone_no_autonext_no_autodistill() -> None:
    """S1.15 (REQ-013)."""
    content = read_command("onboard")
    assert "no auto-next" in content
    assert "no automatic hook" in content
    assert "no Automatic Distillation" in content


# --- S1.16 summary distinguishes deep-read vs sampled ---


def test_onboard_summary_reports_deepread_vs_sampled() -> None:
    """S1.16 (REQ-002, NFR-002)."""
    content = read_command("onboard")
    assert "deep-read versus sampled" in content
    assert "nothing to onboard" in content


# --- S1.17 distill.md carries the onboard cross-note ---


def test_distill_has_onboard_variant_crossnote() -> None:
    """S1.17 (REQ-011)."""
    content = read_command("distill")
    assert "onboard variant" in content
    assert "code observation" in content
