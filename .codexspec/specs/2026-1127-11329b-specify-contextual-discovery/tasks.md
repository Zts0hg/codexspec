# Implementation Tasks: Context-Aware Requirement Discovery

**Feature**: 2026-1127-11329b
**Authority**: requirements.md > spec.md > design.md > plan.md
**Status**: Generic-premise correction and refreshed verification complete; final gate recorded externally

## P1: Instruction Contract and Authored Source

### T001: Add regression contracts and implement discovery instructions

- [x] Complete T001.
- **Covers**: REQ-001, REQ-002, REQ-003, REQ-004, REQ-005, REQ-006, REQ-007, REQ-008; Plan: P1.
- **Design**: D1, D2, D4.
- **Paths**: tests/test_sdd_workflow_templates.py; internal/command_templates/sources/specify.md.
- **Dependencies**: None.
- **Outcome**: Tests assert the complete new instruction obligations and ordering; the authored specify source satisfies them without changing scope or authority.
- **Execution**: Add the tests first, record expected failures against the old instructions, then change the source. Check the template and both installed forms using the same behavior assertions where practical. Regeneration in T002 is required before delivered-form tests turn green.
- **Verification**: New focused tests fail for missing rules before implementation and pass after T002; inspect the authored source against each scenario.

**Test Scenarios**:

| ID | Expected instruction contract |
|---|---|
| TS-001 | Automation-setting preparation, relevant current-implementation inspection, and accessible-fact gathering precede substantive questioning. |
| TS-002 | Verify the premises determining whether any question or option is applicable. Surface descriptions do not establish functionality, status, relationships, or impact; unverified premises remain unknown. Classifications follow inspection, and verified material relationships remain available for user scope decisions. |
| TS-003 | Accessible code/docs/config/history/logs/tests/tool facts and checks are obtained autonomously within scope/authorization; users are not asked to locate or check what the agent can establish. |
| TS-004 | Missing/uninspectable code, inaccessible sources, contradictions, and inconclusive evidence retain uncertainty; a failed search does not prove absence; only necessary gaps are asked about; facts do not establish user intent. |
| TS-005 | Investigation is targeted, stops when sufficient, reuses evidence, expands only for changed scope/new evidence/insufficiency, and does not repeat failed checks or search indefinitely. |
| TS-006 | The applicable automation setting is read before discovery; default disabled and only literal true enables it. |
| TS-007 | Enabled discovery checks foreseeable specification/design/planning/implementation user decisions; an item blocking a later automatic stage is not declared non-blocking merely because specification can proceed. |
| TS-008 | Disabled discovery retains staged clarification without frontloading every technical choice; both modes require current-state verification and autonomous fact-gathering. |
| TS-009 | Behavior/scope/compatibility/important cost or maintenance choices require user decisions; equivalent implementations remain autonomous, including architecture/dependency choices judged by actual consequences. |
| TS-010 | Enabled completion resolves foreseeable downstream user decisions; intermediate confirmation cannot advance; explicit final-summary confirmation and single notice/single successor remain; unforeseen downstream decisions still require asking. |

## P2: Delivered Forms and Verification

### T002: Regenerate specify's distributed and installed forms

- [x] Complete T002.
- **Covers**: REQ-001, REQ-002, REQ-003, REQ-004, REQ-005, REQ-006, REQ-007, REQ-008, REQ-009; Plan: P2.
- **Design**: D3, D4.
- **Paths**: templates/commands/specify.md; .claude/commands/codexspec/specify.md; .agents/skills/codexspec-specify/SKILL.md.
- **Dependencies**: T001.
- **Outcome**: All three delivered forms are generated from the authored source using the existing renderer and installation APIs.
- **Verification**: Run the renderer in write mode, then ClaudeIntegration.install and CodexIntegration.install_skills with force=True and the checkout's interaction language. Check real path containment before writes. Pass the existing exact distribution check and all T001 contract cases across delivered forms. Inspect Git scope for unrelated entry-point, runtime, configuration, registration, or frontmatter changes.
- **Type**: Generated documentation; deterministic checks apply, no separate runtime test scenarios.

### T003: Establish verification and scenario-coverage evidence

- [x] Complete T003.
- **Covers**: REQ-001, REQ-002, REQ-003, REQ-004, REQ-005, REQ-006, REQ-007, REQ-008, REQ-009; Plan: P2.
- **Design**: D4.
- **Paths**: This tasks.md; verification.md in this feature directory.
- **Dependencies**: T002.
- **Outcome**: Record exact check outcomes and a mapping from TS-001 through TS-010 to implemented tests. All required checks are green before independent review.
- **Verification**: Run the focused workflow/profile/worktree/fragment suites; exact distribution check; Ruff lint and format check for changed tests; repository Markdown rules and whitespace/link checks on changed authored artifacts; complete pytest suite. State skipped or unavailable native-platform coverage accurately. Confirm every scenario has meaningful assertions, not only a marker or a non-asserting test. Record static contract versus live-agent evaluation limits.
- **Type**: Verification evidence and task bookkeeping; no new runtime behavior or extra test scenarios.

## P3: Final Acceptance Gate

The implementation command's mandatory final acceptance gate implements plan P3 after T001-T003 are complete. Invoke review-code --feature <absolute-feature-directory> in a fresh isolated reviewer context against the complete feature target, validate the schema-v3 defect envelope and target-bound maintenance companion, and follow the existing repair/review loop if necessary.

Keep review records, loop state, and final verdict outside the repository. Finish all source edits, generation, checks, scenario mapping, and task bookkeeping before freezing the target. Completing this gate must not require changing the frozen feature documents solely to record its result.

Covers: REQ-001, REQ-002, REQ-003, REQ-004, REQ-005, REQ-006, REQ-007, REQ-008, REQ-009; Plan: P3; Design: D1, D2, D3, D4.

## Coverage

| Plan Item | Task or Gate |
|---|---|
| P1: Instruction contracts and source | T001 |
| P2: Generation | T002 |
| P2: Verification and evidence | T003 |
| P3: Independent complete-feature review | Final acceptance gate |

| Requirements | Implementation and Verification |
|---|---|
| REQ-001 | T001 / TS-001, TS-002; T002, T003 |
| REQ-002 | T001 / TS-001, TS-003; T002, T003 |
| REQ-003 | T001 / TS-004; T002, T003 |
| REQ-004 | T001 / TS-005; T002, T003 |
| REQ-005 | T001 / TS-001, TS-006, TS-008; T002, T003 |
| REQ-006 | T001 / TS-007, TS-010; T002, T003 |
| REQ-007 | T001 / TS-009; T002, T003 |
| REQ-008 | T001 / TS-010; T002, T003 |
| REQ-009 | T002 distribution/scope checks; T003 |

## Dependency and Scope Check

T001 -> T002 -> T003 -> Final acceptance gate. No parallel task marker is used because generation and verification depend on the preceding output. No task changes other entry points, adds configuration, or performs full design/planning within specify. There are no unmapped tasks or unresolved upstream items.

## Implemented Scenario Coverage

All tests below are in tests/test_sdd_workflow_templates.py and run against the template, Claude command, and Codex skill forms (30 new cases).

| Scenario | Implemented Test |
|---|---|
| TS-001 | test_specify_prepares_facts_and_automation_before_questions |
| TS-002 | test_specify_verifies_question_premises_before_classifying_functionality |
| TS-003 | test_specify_obtains_accessible_facts_without_transferring_checks_to_users |
| TS-004 | test_specify_preserves_uncertainty_and_asks_only_necessary_gaps |
| TS-005 | test_specify_bounds_investigation_and_reuses_evidence |
| TS-006 | test_specify_reads_the_applicable_literal_true_setting_during_preparation |
| TS-007 | test_specify_frontloads_foreseeable_downstream_user_decisions_when_enabled |
| TS-008 | test_specify_keeps_staged_clarification_when_disabled_and_fact_finding_in_both_modes |
| TS-009 | test_specify_reserves_material_choices_for_users_and_equivalent_implementations_for_agents |
| TS-010 | test_specify_requires_final_confirmation_and_resolved_downstream_choices_before_advancing |

The implementer inspected each assertion against its expected scenario. Source and delivered-form contracts are tested; no live-model execution evaluation is claimed.

## Execution Evidence

Initial baseline before the generic-premise correction: T001 and T002 observed expected red, then 220 focused tests passed with 1 skipped; exact distribution, Ruff lint/format, and scope checks passed. T003: full suite 2644 passed and 60 skipped; deterministic document checks passed. See verification.md for commands, limits, and source walkthroughs. Final gate state is maintained outside the repository.

### Generic-Premise Correction

The user identified an overly specific frontend/backend rule and a premature placeholder classification. T001 and T002 correct that wording under REQ-001/REQ-003, D1/D4, and plan P1/P2. Updated TS-002 observed 3 failing cases before the fix and 3 passing cases afterward; the focused suite remains 220 passed/1 skipped. Source, all delivered forms, and the scenario mapping are synchronized. T003 is reopened for refreshed complete verification; the earlier final review applies only to its original frozen target.

### Refreshed Complete Verification

Four disjoint pytest test-file groups passed with 2644 passed/60 skipped in aggregate. All 2703 collected node IDs and the one collection-skip module match the original whole-suite collection exactly, with no duplicate or omitted node. Focused, distribution, Ruff, Markdown, and complete-diff semantic checks pass. The final complete-feature review is recorded externally against the corrected target.
