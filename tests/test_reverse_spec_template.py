"""Contract tests for the reverse-spec command template.

Scenario numbers refer to the T2.1 Test Scenarios in
.codexspec/specs/2026-0818-2053p5-reverse-spec/tasks.md.

reverse-spec is a pure agent-driven command template (like onboard/debug/distill);
these tests assert its written discipline — the behavior the template instructs —
not runtime execution.

Assertions target spans free of inline markdown emphasis (pitfall
P-2026-0813-1606fz-1), and run against a whitespace-normalized copy so a hard line
wrap inside an asserted phrase cannot break the match.
"""

import re
from pathlib import Path

from codexspec.translator import extract_frontmatter_fields

ROOT = Path(__file__).parent.parent
COMMANDS = ROOT / "templates" / "commands"


def read_command(name: str) -> str:
    return (COMMANDS / f"{name}.md").read_text(encoding="utf-8")


def normalized(name: str) -> str:
    """Collapse every whitespace run to a single space, so asserted phrases may wrap."""
    return re.sub(r"\s+", " ", read_command(name))


# --- S1 frontmatter ---


def test_reverse_spec_frontmatter_has_description_and_path_hint() -> None:
    """S1 (REQ-001, REQ-019)."""
    fields = extract_frontmatter_fields(read_command("reverse-spec"))
    assert fields.get("description")
    assert "[path]" in (fields.get("argument-hint") or "")


# --- S2 language regime is interaction/document, not commit ---


def test_reverse_spec_language_preference_interaction_and_document_not_commit() -> None:
    """S2 (REQ-021, NFR-001)."""
    content = read_command("reverse-spec")
    assert "## Language Preference" in content
    assert "language.interaction" in content
    assert "language.document" in content
    assert "language.commit" not in content


# --- S3..S6 mode resolution ---


def test_bare_run_surveys_and_never_reconciles() -> None:
    """S3 (REQ-015, REQ-002): the bare run short-circuits before any baseline lookup."""
    content = normalized("reverse-spec")
    assert "performs the architectural survey and never reconciles" in content
    assert "Do not perform a baseline lookup at all in this case." in content


def test_invalid_or_empty_path_creates_no_workspace() -> None:
    """Regression for the review's P3 finding: spec.md's two input-validation
    boundary rows (REQ-001, REQ-019) must be realized in the template."""
    content = normalized("reverse-spec")
    assert "Report the invalid path and stop. Create no workspace." in content
    assert "nothing to reverse-derive and stop, creating no workspace and no artifacts" in content


def test_no_matching_workspace_enters_generate_mode() -> None:
    """S4 (REQ-002)."""
    assert "Enter generate mode — but first check that the slice contains analyzable code" in normalized("reverse-spec")


def test_ambiguous_match_asks_the_user() -> None:
    """S5 (REQ-002): never silently pick the newest workspace."""
    content = normalized("reverse-spec")
    assert "Ask the user to select one. Never silently pick the most recent workspace." in content


def test_unconfirmed_baseline_refuses_to_reconcile() -> None:
    """S6 (REQ-008): an unconfirmed baseline blocks reconciliation and produces no report.

    It does not block all output — an open workspace resumes its draft instead
    (see test_interrupted_generate_resumes_instead_of_refusing).
    """
    content = normalized("reverse-spec")
    assert "artifacts are still open.** Do not reconcile" in content
    assert "compare the code with itself" in content
    assert "continuing the draft rather than reconciling" in content


# --- S7/S8 baseline selection ---


def test_baseline_is_confirmed_spec_and_design_only() -> None:
    """S7 (REQ-007): requirements/plan/tasks are excluded as comparison baselines."""
    content = normalized("reverse-spec")
    assert "The baseline is the slice's confirmed" in content
    # Assert the exclusion sentence itself. A bare `"requirements.md" in content`
    # is tautological: the filename appears several times for unrelated reasons,
    # so dropping it from this sentence would leave such a check green.
    assert "Never use `requirements.md`, `plan.md`, or `tasks.md` as a comparison baseline." in content


def test_reconciles_against_spec_alone_when_design_absent() -> None:
    """S8 (REQ-007)."""
    assert "reconcile against the spec alone" in normalized("reverse-spec")


# --- S9..S12 drift classification and evidence ---


def test_three_drift_kinds_are_named() -> None:
    """S9 (REQ-009)."""
    content = read_command("reverse-spec")
    for kind in ("undocumented-behavior", "unimplemented-spec", "semantic-mismatch"):
        assert kind in content


def test_severity_comes_from_impact_not_from_kind() -> None:
    """S10 (REQ-011)."""
    content = normalized("reverse-spec")
    assert "from the item's actual impact" in content
    assert "Severity is not fixed by its kind" in content


def test_report_gates_nothing() -> None:
    """S11 (REQ-011, REQ-018)."""
    content = normalized("reverse-spec")
    assert "They are not a gate" in content
    assert "emits no pass/fail verdict" in content


def test_semantic_mismatch_requires_both_side_evidence() -> None:
    """S12 (REQ-009, REQ-010)."""
    content = normalized("reverse-spec")
    assert "quote both sides as evidence" in content
    assert "cannot evidence on both sides is not reported as a mismatch" in content


# --- S13/S14 direction discipline ---


def test_direction_is_never_guessed() -> None:
    """S13 (REQ-013): needs-your-judgment instead of a guess, and drift is never suppressed."""
    content = normalized("reverse-spec")
    assert "needs-your-judgment" in content
    assert "Never guess a direction" in content
    assert "never suppress a drift item" in content


def test_direction_is_suggested_but_never_applied() -> None:
    """S14 (REQ-012)."""
    content = normalized("reverse-spec")
    assert "The suggested direction is never applied." in content
    assert "Reconciliation modifies no code" in content


# --- S15 report structure ---


def test_reconcile_report_documents_every_item_field() -> None:
    """S15 (REQ-010)."""
    content = read_command("reverse-spec")
    assert "reconcile.md" in content
    for field in ("kind:", "severity:", "location:", "evidence:", "direction:", "status:"):
        assert field in content


# --- S16 inference marking ---


def test_generated_artifacts_are_marked_inferred_and_open() -> None:
    """S16 (REQ-005)."""
    content = normalized("reverse-spec")
    assert "Status: inferred/open" in content
    assert "not a reconciliation baseline until confirmed" in content


# --- S17 safety boundary ---


def test_workspace_creation_never_touches_git() -> None:
    """Regression for the review's P2 finding (CON-007, REQ-017): the workspace is a
    plain directory, and the branch-creating script is explicitly not invoked."""
    content = normalized("reverse-spec")
    assert "Create the directory only." in content
    assert "create and switch a git branch, which this command must never do" in content
    assert "Creating a workspace changes no git state" in content


def test_read_only_on_code_and_never_writes_the_profile() -> None:
    """S17 (REQ-017)."""
    content = normalized("reverse-spec")
    assert "Read-only on the codebase" in content
    assert "Writes are confined to the feature workspace" in content
    # Assert the boundary sentence itself, not a bare occurrence of the path:
    # the literal `.codexspec/profile/` also appears in the Scan Discipline
    # override, so a substring check on it alone stays green even if this
    # boundary clause is deleted.
    assert "Never writes to `.codexspec/profile/`. That store belongs to" in content


# --- S18 scan discipline is referenced, not restated ---


def test_scan_discipline_references_onboard() -> None:
    """S18 (REQ-016)."""
    content = normalized("reverse-spec")
    assert "/codexspec:onboard" in content
    assert "rather than a restatement here" in content


# --- S19 path-only slice input ---


def test_diff_or_pr_range_is_not_a_slice_source() -> None:
    """S19 (REQ-019)."""
    assert "A diff or pull-request range is not a slice source." in normalized("reverse-spec")


# --- S20 no pipeline coupling ---


def test_reverse_spec_has_no_autonext_and_no_auto_distillation() -> None:
    """S20 (REQ-018)."""
    content = read_command("reverse-spec")
    assert "Auto-Next Chain Advance" not in content
    assert "Automatic Distillation" not in content


# --- regressions from the second isolated review ---


def test_scan_delegation_overrides_the_profile_write_directive() -> None:
    """Review F1: onboard's scan section streams findings into the profile store;
    delegating to it must explicitly not import that write directive (OUT-002, REQ-017)."""
    content = normalized("reverse-spec")
    assert "this command writes nothing to `.codexspec/profile/`" in content
    assert "create a second writer for a store this command does not own" in content


def test_generate_and_overview_write_incrementally() -> None:
    """Review F4: REQ-016/NFR-004 require streaming output, not scan-then-write."""
    content = normalized("reverse-spec")
    assert "writing as you go rather than holding everything until the scan completes" in content
    assert "an interrupted run leaves usable partial output" in content


def test_diff_range_is_rejected_before_path_existence() -> None:
    """Review F5: the path-only contract must be reachable for a diff/PR argument."""
    content = normalized("reverse-spec")
    assert "Test this before testing path existence" in content


def test_empty_code_gate_is_generate_only() -> None:
    """Review F6: an emptied slice is the maximal unimplemented-spec case, not a no-op."""
    content = normalized("reverse-spec")
    assert "This check belongs to generate mode alone." in content
    assert "maximal `unimplemented-spec` case" in content


def test_overview_workspace_is_never_a_baseline() -> None:
    """Review F7: an explicit `.` path must not match the overview workspace."""
    content = normalized("reverse-spec")
    assert "is an overview workspace, never a baseline: skip it during this search" in content


def test_repeat_reconcile_regeneration_is_announced() -> None:
    """Review F3: regenerating the report must not silently discard adjudications."""
    content = normalized("reverse-spec")
    assert "Regeneration replaces the previous report" in content
    assert "Say so before overwriting" in content


def test_interrupted_generate_resumes_instead_of_refusing() -> None:
    """Review round 3 P2: an open workspace means resume the draft, not refuse and
    write nothing — otherwise REQ-016/NFR-004 resumability is unreachable."""
    content = normalized("reverse-spec")
    assert "resume generate mode into that existing workspace" in content
    assert "Never create a second workspace for a slice that already has one." in content
    assert "If an `<id>-overview` workspace already exists, continue it" in content


def test_overview_workspace_identified_by_positive_marker() -> None:
    """Review round 3 P2: identifying an overview workspace by the absence of spec.md
    misclassifies a generate run interrupted before spec.md was written."""
    content = normalized("reverse-spec")
    assert "A workspace containing `slices.md` is an overview workspace" in content
    assert "not by the absence of a `spec.md`" in content
