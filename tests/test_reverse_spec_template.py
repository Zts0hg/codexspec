"""Contract tests for the reverse-spec command template.

Scenario numbers refer to the T2.1 Test Scenarios in
.codexspec/specs/2026-0818-2053p5-reverse-spec/tasks.md.

reverse-spec is a pure agent-driven command template (like onboard/debug/distill);
these tests assert its written discipline — the behavior the template instructs —
not runtime execution.

Assertions run against ``prose()``: the template with whitespace runs collapsed and
inline emphasis stripped. A hard line wrap inside an asserted phrase, or a change to
which words carry bold or backticks, therefore cannot break a match (plan Decision 3,
pitfall P-2026-0813-1606fz-1).

Every assertion targets the sentence that carries the instruction, never a bare
occurrence of a term that also appears elsewhere in the file. A substring that
survives deleting the rule it is meant to guard proves nothing.
"""

import re
from pathlib import Path

from codexspec.translator import extract_frontmatter_fields

ROOT = Path(__file__).parent.parent
COMMANDS = ROOT / "templates" / "commands"


def read_command(name: str) -> str:
    return (COMMANDS / f"{name}.md").read_text(encoding="utf-8")


def prose(name: str) -> str:
    """Collapse whitespace and strip inline emphasis, so asserted spans are plain prose.

    Only ``**`` and backticks are stripped: this template uses no single-asterisk
    italics, and stripping ``*`` would mangle the glob ``.codexspec/specs/*/``.
    """
    collapsed = re.sub(r"\s+", " ", read_command(name))
    return collapsed.replace("**", "").replace("`", "")


# --- S1 frontmatter ---


def test_reverse_spec_frontmatter_has_description_and_path_hint() -> None:
    """S1 (REQ-001, REQ-019)."""
    fields = extract_frontmatter_fields(read_command("reverse-spec"))
    assert fields.get("description")
    assert "[path]" in (fields.get("argument-hint") or "")


def test_reverse_spec_receives_the_path_argument() -> None:
    """The command cannot see [path] without a User Input section carrying $ARGUMENTS
    (REQ-001, REQ-019). Previously uncovered: deleting the section left the suite green."""
    content = prose("reverse-spec")
    assert "## User Input" in content
    assert "$ARGUMENTS" in content


# --- S2 language regime is interaction/document, not commit ---


def test_reverse_spec_language_preference_interaction_and_document_not_commit() -> None:
    """S2 (REQ-021, NFR-001)."""
    content = read_command("reverse-spec")
    assert "## Language Preference" in content
    assert "language.interaction" in content
    assert "language.document" in content
    assert "language.commit" not in content


def test_verbatim_evidence_is_exempt_from_translation() -> None:
    """REQ-010 / design Decision 5 under the REQ-021 language regime: the reconcile
    report is authored in `language.document`, and translating a quote by meaning
    would destroy the both-side evidence rule's whole purpose — a translated quote
    cannot be checked against its source. Same carve-out onboard.md and distill.md
    carry for their own verbatim evidence."""
    content = prose("reverse-spec")
    assert "MUST NOT be translated" in content
    assert "quote the code and the baseline verbatim" in content
    # The sibling commands that established this convention must still carry it,
    # or the precedent this guard rests on has silently moved.
    for sibling in ("onboard", "distill"):
        assert "MUST NOT be translated" in prose(sibling)


# --- S3..S6 mode resolution ---


def test_bare_run_surveys_and_never_reconciles() -> None:
    """S3 (REQ-015, REQ-002): the bare run short-circuits before any baseline lookup."""
    content = prose("reverse-spec")
    assert "performs the architectural survey and never reconciles" in content
    assert "Do not perform a baseline lookup at all in this case." in content


def test_repository_root_path_is_the_bare_run() -> None:
    """DEC-014 / REQ-014 / REQ-015 / NFR-005: an explicit path resolving to the
    repository root takes the survey, not generate mode. Without this, `reverse-spec .`
    falls through the step-1 short-circuit and the overview skip into generate and
    drafts one whole-repository detailed spec.md, which NFR-005 forbids
    unconditionally."""
    content = prose("reverse-spec")
    assert "No path supplied, or a path that resolves to the repository root." in content
    assert "A bare reverse-spec and reverse-spec . are the same run" in content
    assert "the repository as a whole is never a slice" in content
    # And the slice definition itself excludes the root, not only mode resolution.
    assert "The repository root is not a slice" in content


def test_path_outside_the_repository_is_refused() -> None:
    """REQ-002 / REQ-004 / NFR-005: `..`, `../sibling`, and `/` exist yet resolve
    outside. Without this branch they reach generate mode and draft one detailed spec
    for a tree strictly containing the repository -- the monolith NFR-005 forbids
    unconditionally -- and their Slice: header could not be written at all, since it
    is defined as repo-relative with no `..` segment and never absolute."""
    content = prose("reverse-spec")
    assert "The path exists but lies outside the repository." in content
    assert "Report that a slice must be inside the repository and stop, creating no workspace." in content
    assert "scanning a tree that strictly contains the repository would produce" in content


def test_survey_workspace_is_identified_by_marker_not_directory_name() -> None:
    """REQ-002 / REQ-004: the bare run performs no baseline lookup, so the directory
    name was its only stated way to find an earlier survey. A slice whose final path
    segment is `overview` produces the same directory name, so a bare run would write
    the repository map over that slice's draft -- and once slices.md is in it, the
    step-5 skip hides that slice's baseline from every later lookup, permanently."""
    content = prose("reverse-spec")
    assert "look for a workspace holding slices.md" in content
    assert "never go by the directory name" in content
    assert "whose final path segment is overview produces an identically named directory" in content
    # The naming rule itself must say the directory name is not an identifier.
    assert "The directory name is a convenience for humans" in content
    assert "never how a workspace is identified" in content


def test_nested_overlap_is_disclosed_in_every_mode() -> None:
    """REQ-002 states the overlap disclosure without qualification. Confining it to
    the generate branch leaves reconcile silent: a src/auth baseline compared against
    code including src/auth/tokens reports that subtree as undocumented-behavior with
    nothing in the report explaining where those items came from."""
    content = prose("reverse-spec")
    assert "Whichever mode you resolved, if any existing workspace records a slice nested inside" in content
    assert "This disclosure is not confined to generate mode." in content
    assert "It matters most in reconcile" in content


def test_invalid_or_empty_path_creates_no_workspace() -> None:
    """Regression for the review's P3 finding: spec.md's two input-validation
    boundary rows (REQ-001, REQ-019) must be realized in the template."""
    content = prose("reverse-spec")
    assert "Report the invalid path and stop. Create no workspace." in content
    assert "nothing to reverse-derive and stop, creating no workspace and no artifacts" in content


def test_no_matching_workspace_enters_generate_mode() -> None:
    """S4 (REQ-002)."""
    assert "Enter generate mode — but first check that the slice contains analyzable code" in prose("reverse-spec")


def test_ambiguous_match_asks_the_user() -> None:
    """S5 (REQ-002): never silently pick the newest workspace."""
    content = prose("reverse-spec")
    assert "Ask the user to select one. Never silently pick the most recent workspace." in content


def test_slice_path_is_normalized_before_any_comparison() -> None:
    """DEC-013 (REQ-002, REQ-004): the write side was pinned to a repo-relative path
    but the read side defined no normalization, so `src/auth/`, `./src/auth`, or an
    absolute path missed the workspace the slice already had and silently created a
    second one."""
    content = prose("reverse-spec")
    assert "Normalize it before comparing anything" in content
    assert "make it repo-relative, resolve ., .., and absolute forms, and drop any trailing slash" in content
    assert "are one slice rather than four" in content
    # Normalization must apply on the way in, not only on the way out.
    assert "Record every Slice: header in exactly this normalized form and compare in it too" in content
    assert "an unnormalized comparison silently misses the workspace a slice already has" in content


def test_only_an_exact_match_selects_a_mode() -> None:
    """DEC-013 (REQ-002): a covering (proper-ancestor) workspace must not drive mode
    selection. Otherwise `reverse-spec src/auth/tokens` against a confirmed `src/auth`
    workspace yields exactly one match, never reaches the multiple-match branch, and
    reconciles into the wider slice's workspace -- overwriting a reconcile.md that
    holds the user's recorded adjudications."""
    content = prose("reverse-spec")
    assert "matches exactly when its normalized Slice: equals the normalized path" in content
    assert "covers the path when its Slice: is a proper ancestor of it" in content
    assert "Only an exact match selects a mode on its own." in content
    assert "A covering match never does" in content
    assert "its reconcile.md belongs to that wider slice" in content


def test_covering_match_asks_instead_of_guessing() -> None:
    """DEC-013 (REQ-002): the same never-guess discipline REQ-002 already mandates for
    multiple matches -- report the covering workspace and let the user choose."""
    content = prose("reverse-spec")
    assert "No exact match, but one or more workspaces cover the slice." in content
    assert "Never pick one silently and never quietly start a nested workspace." in content
    assert "reconcile or continue that workspace at its own wider boundary, or create a new workspace" in content
    assert "Proceed only on their answer." in content
    # A workspace nested inside the given slice is disclosed but does not block.
    assert "records a slice nested inside the one you were given, say so before proceeding" in content


def test_unconfirmed_baseline_refuses_to_reconcile() -> None:
    """S6 (REQ-008): an unconfirmed baseline blocks reconciliation and produces no report.

    It does not block all output — an open workspace resumes its draft instead
    (see test_resume_completes_only_what_is_missing).
    """
    content = prose("reverse-spec")
    assert "artifacts are still open. Do not reconcile" in content
    assert "compare the code with itself" in content
    assert "continuing the draft rather than reconciling" in content


# --- S7/S8 baseline selection ---


def test_baseline_is_confirmed_spec_and_design_only() -> None:
    """S7 (REQ-007): requirements/plan/tasks are excluded as comparison baselines."""
    content = prose("reverse-spec")
    assert "The baseline is the slice's confirmed" in content
    # Assert the exclusion sentence itself. A bare `"requirements.md" in content`
    # is tautological: the filename appears several times for unrelated reasons,
    # so dropping it from this sentence would leave such a check green.
    assert "Never use requirements.md, plan.md, or tasks.md as a comparison baseline." in content


def test_reconciles_against_spec_alone_when_design_absent() -> None:
    """S8 (REQ-007)."""
    assert "reconcile against the spec alone" in prose("reverse-spec")


# --- S9..S12 drift classification and evidence ---


def test_three_drift_kinds_are_classified() -> None:
    """S9 (REQ-009).

    Asserts the classification instruction and each kind's defining clause, not the
    bare kind literals: those also appear in the Reconcile Report block and in mode
    resolution, so a literal-only check stayed green with the whole REQ-009
    classification instruction deleted.
    """
    content = prose("reverse-spec")
    assert "Re-read the slice's current code and classify each finding as exactly one of" in content
    assert "undocumented-behavior — the code does something the baseline never describes" in content
    assert "unimplemented-spec — the baseline states something the code does not do" in content
    assert "semantic-mismatch — both sides address the same thing and disagree about it" in content


def test_severity_comes_from_impact_not_from_kind() -> None:
    """S10 (REQ-011)."""
    content = prose("reverse-spec")
    assert "from the item's actual impact" in content
    assert "Severity is not fixed by its kind" in content


def test_report_gates_nothing() -> None:
    """S11 (REQ-011, REQ-018)."""
    content = prose("reverse-spec")
    assert "They are not a gate" in content
    assert "emits no pass/fail verdict" in content


def test_semantic_mismatch_requires_both_side_evidence() -> None:
    """S12 (REQ-009, REQ-010)."""
    content = prose("reverse-spec")
    assert "quote both sides as evidence" in content
    assert "cannot evidence on both sides is not reported as a mismatch" in content


# --- S13/S14 direction discipline ---


def test_direction_is_never_guessed() -> None:
    """S13 (REQ-013): needs-your-judgment instead of a guess, and drift is never suppressed."""
    content = prose("reverse-spec")
    assert "needs-your-judgment" in content
    assert "Never guess a direction" in content
    assert "never suppress a drift item" in content


def test_direction_is_suggested_but_never_applied() -> None:
    """S14 (REQ-012)."""
    content = prose("reverse-spec")
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
    content = prose("reverse-spec")
    assert "Status: inferred/open" in content
    assert "not a reconciliation baseline until confirmed" in content


# --- S17 safety boundary ---


def test_workspace_creation_never_touches_git() -> None:
    """Regression for the review's P2 finding (CON-007, REQ-017): the workspace is a
    plain directory, and the branch-creating script is explicitly not invoked."""
    content = prose("reverse-spec")
    assert "Create the directory only." in content
    assert "create and switch a git branch, which this command must never do" in content
    assert "Creating a workspace changes no git state" in content


def test_read_only_on_code_and_never_writes_the_profile() -> None:
    """S17 (REQ-017)."""
    content = prose("reverse-spec")
    assert "Read-only on the codebase" in content
    assert "Writes are confined to the feature workspace" in content
    # Assert the boundary sentence itself, not a bare occurrence of the path:
    # the literal `.codexspec/profile/` also appears in the Scan Discipline
    # override, so a substring check on it alone stays green even if this
    # boundary clause is deleted.
    assert "Never writes to .codexspec/profile/. That store belongs to" in content


# --- S18 scan discipline is referenced, not restated ---


def test_scan_discipline_references_onboard() -> None:
    """S18 (REQ-016)."""
    content = prose("reverse-spec")
    assert "/codexspec:onboard" in content
    assert "rather than a restatement here" in content


def test_onboard_still_carries_the_delegated_scan_section() -> None:
    """The delegation in S18 is a live cross-command reference: if onboard's scan
    section is renamed or its overridden directive removed, reverse-spec silently
    points at nothing and its two overrides describe text that no longer exists
    (REQ-016). Same guard shape as tests/test_distill_template.py's onboard check."""
    onboard = prose("onboard")
    assert "## Codebase Scan" in onboard
    # The directive reverse-spec's first override exists to neutralize.
    assert "Stream findings to the store as you go" in onboard
    # The directive its second override reinterprets.
    assert "argument (from $ARGUMENTS) narrows the scan" in onboard


# --- S19 path-only slice input ---


def test_diff_or_pr_range_is_not_a_slice_source() -> None:
    """S19 (REQ-019)."""
    assert "A diff or pull-request range is not a slice source." in prose("reverse-spec")


# --- S20 no pipeline coupling ---


def test_reverse_spec_has_no_autonext_and_no_auto_distillation() -> None:
    """S20 (REQ-018)."""
    content = read_command("reverse-spec")
    assert "Auto-Next Chain Advance" not in content
    assert "Automatic Distillation" not in content


# --- REQ-004 slice binding, and REQ-015 overview output ---


def test_workspace_records_the_slice_it_covers() -> None:
    """REQ-004 / Decision 2: the Slice: header is the entire baseline-lookup
    mechanism, and nothing previously failed if it disappeared."""
    content = prose("reverse-spec")
    assert "carries a Slice: header holding the repo-relative path its content describes" in content
    assert "This field is the whole baseline-lookup mechanism: there is no index file" in content
    assert "for workspaces whose recorded Slice: value matches the normalized path" in content
    assert "search .codexspec/specs/*/" in content


def test_generate_output_boundary_is_three_artifacts() -> None:
    """REQ-003 / OUT-003 / NFR-006. Previously uncovered: a mirror with the whole
    three-artifact boundary deleted from `## Generate Mode` left the suite green."""
    content = prose("reverse-spec")
    assert "spec.md — the behavior and contracts the code exhibits" in content
    assert "design.md — the structure the code has" in content
    assert "requirements.md — a thin stub whose entries are all open" in content
    # Design scales to the slice; intent is never reverse-derived.
    assert "Scale it to the slice's real complexity" in content
    assert "do not reverse-derive why a feature exists" in content


def test_confirmation_action_is_stated_at_the_end_of_generate() -> None:
    """REQ-006: confirmation is manual, so a generate run that does not state the
    exact action leaves the user with a draft that never becomes a baseline -- and
    the drift checking the feature exists for never activates."""
    content = prose("reverse-spec")
    assert "End generate mode by stating the exact confirmation action" in content
    assert "including the file paths and the status line to change" in content
    assert "adds no separate confirmation command, no flag, and no state file" in content


def test_overview_mode_produces_a_map_and_a_slice_list() -> None:
    """REQ-015 / User Story 4 scenarios 1-2. Previously uncovered: deleting the whole
    Overview Mode section left the suite green."""
    content = prose("reverse-spec")
    assert "a thin architecture-level map: components, their responsibilities, and how they relate" in content
    assert "the candidate slice list. One row per slice: path, a one-line description, and a rough size" in content


def test_overview_mode_writes_no_spec_and_no_reconcile_report() -> None:
    """REQ-015 / OUT-005 / User Story 4 scenario 3 — the bare run is a map, never a
    repository-wide specification."""
    content = prose("reverse-spec")
    assert "Overview mode writes no spec.md and no reconcile.md." in content
    assert "It is a map and a deepening plan, not a specification." in content


# --- regressions from the second isolated review ---


def test_scan_delegation_overrides_the_profile_write_directive() -> None:
    """Review F1: onboard's scan section streams findings into the profile store;
    delegating to it must explicitly not import that write directive (OUT-002, REQ-017)."""
    content = prose("reverse-spec")
    assert "this command writes nothing to .codexspec/profile/" in content
    assert "create a second writer for a store this command does not own" in content


def test_generate_and_overview_write_incrementally() -> None:
    """Review F4: REQ-016/NFR-004 require streaming output, not scan-then-write."""
    content = prose("reverse-spec")
    assert "writing as you go rather than holding everything until the scan completes" in content
    assert "an interrupted run leaves usable partial output" in content


def test_diff_range_is_rejected_before_path_existence() -> None:
    """Review F5: the path-only contract must be reachable for a diff/PR argument."""
    content = prose("reverse-spec")
    assert "Test this before testing path existence" in content


def test_empty_code_gate_is_generate_only() -> None:
    """Review F6: an emptied slice is the maximal unimplemented-spec case, not a no-op."""
    content = prose("reverse-spec")
    assert "This check belongs to generate mode alone." in content
    assert "maximal unimplemented-spec case" in content


def test_overview_workspace_is_never_a_baseline() -> None:
    """Review F7: an explicit `.` path must not match the overview workspace."""
    content = prose("reverse-spec")
    assert "is an overview workspace, never a baseline: skip it during this search" in content


def test_repeat_reconcile_regeneration_is_announced() -> None:
    """Review F3: regenerating the report must not silently discard adjudications."""
    content = prose("reverse-spec")
    assert "Regeneration replaces the previous report" in content
    assert "Say so before overwriting" in content


# --- regressions from rounds 3 and 4: workspace recognition and write boundaries ---
#
# Rounds 3 and 4 each found that the previous round's repair had introduced the
# next round's worst defect, both times in mode resolution and write boundaries.
# The three findings were one defect: the command inferred a workspace's identity
# and state from artifacts that are themselves written incrementally during the
# run, so mid-run a partial state was indistinguishable from a different state,
# and its own interrupted output was indistinguishable from the maintainer's
# corrections. design.md Decision 7 settles it with two rules, guarded below.


def test_workspace_writes_its_identifying_artifact_at_creation() -> None:
    """Decision 7 rule 1 (REQ-002, REQ-004): no window exists in which a created
    workspace is invisible to the lookup, so an interruption cannot strand the first
    workspace and have the next run create a second one for the same slice."""
    content = prose("reverse-spec")
    assert "Creating a workspace is one indivisible act" in content
    assert "write the artifact that identifies it" in content
    assert "before scanning anything and before writing any derived content" in content
    assert "Do not create the directory and defer the header until the scan has something to say" in content


def test_both_modes_are_identifiable_from_their_first_moment() -> None:
    """Decision 7 rule 1 applied per mode: generate writes spec.md with the Slice:
    header first (REQ-004), overview writes slices.md first so an interrupted survey
    keeps the marker that excludes it from the baseline lookup (REQ-015)."""
    content = prose("reverse-spec")
    assert "writing its spec.md with the Slice: header as the creating act" in content
    assert "workspace by writing its slices.md as the creating act" in content
    assert "an interrupted survey can never be mistaken for a slice workspace" in content
    # The lookup relies on that guarantee rather than on a missing-file heuristic.
    assert "workspace writes its identifying artifact as the act that creates it" in content


def test_resume_completes_only_what_is_missing() -> None:
    """Decision 7 rule 2 (REQ-016, NFR-004, REQ-017): resuming an open workspace
    appends what was never written and rewrites nothing, so a complete draft causes
    no write and the behavior degenerates to User Story 3's report-only outcome."""
    content = prose("reverse-spec")
    assert "resume generate mode into that existing workspace" in content
    assert "Never create a second workspace for a slice that already has one." in content
    assert "Resuming means completing only what is missing" in content
    assert "leave everything already written exactly as it stands" in content
    assert "If the draft is already complete, write nothing at all" in content


def test_overview_resume_follows_the_same_completion_only_rule() -> None:
    """Decision 7 rule 2 is mode-independent: the interruption hole closed for slice
    workspaces must not stay open on the overview side (REQ-015)."""
    content = prose("reverse-spec")
    assert "When the <id>-overview workspace already exists from an interrupted survey" in content
    assert "complete only what is missing, and leave what is already written untouched" in content


def test_generate_appends_and_never_rewrites() -> None:
    """Decision 7 rule 2 at the point of writing (REQ-017)."""
    content = prose("reverse-spec")
    assert "Append; never rewrite." in content
    assert "Content already in an artifact stays as it is" in content


def test_workspace_write_boundary_is_a_rule_not_a_closed_exception_set() -> None:
    """Round 4 I-1: the boundary declared regenerating reconcile.md 'the one
    exception' while mode resolution added a second, so the two instructions could
    not both be followed. It is now stated as a rule (REQ-017), and existing content
    is treated as the maintainer's because provenance is not knowable."""
    content = prose("reverse-spec")
    assert "Rewrites only what it wrote during the current run, and never without notice." in content
    assert "belongs to the maintainer" in content
    assert "you cannot tell the two apart, so treat both as theirs" in content
    assert "A resumed draft is therefore appended to, never overwritten." in content
    assert "report the discrepancy and leave the decision to the user rather than correcting it yourself" in content
    # reconcile.md remains the single wholesale regeneration, tied to its notice rule.
    assert "The one artifact this command regenerates wholesale is its own reconcile.md" in content
