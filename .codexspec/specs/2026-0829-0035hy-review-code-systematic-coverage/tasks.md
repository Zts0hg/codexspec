# Tasks: Systematic Review Coverage

**Input**: Design documents from
`.codexspec/specs/2026-0829-0035hy-review-code-systematic-coverage/`
**Prerequisites**: `requirements.md`, `spec.md`, `design.md`, and approved `plan.md`

**Tests**: The approved plan requires test-first ordering for the command contracts, repair-loop
consumer, schema parser, evaluation corpus, and localized documentation contract.

## Format

Each task has one verifiable outcome, exact paths, dependencies, requirement coverage, and an
approved-plan reference. Testable tasks enumerate individually identifiable scenarios derived from
the specification.

## Phase 1: Failing Contract Tests

### T001 [US1] Define the five-pass review and schema-v2 producer contract

- [x] Update `tests/test_review_code_templates.py` with failing assertions for the ordered Scope,
  System Contract, Behavior, Risk, and Verification passes; contract and partition coverage;
  continued work after a finding; bounded related-defect searches; exact schema v2; target
  fingerprints; cross-field validation; and preserved target, audit, safety, and isolation rules.
- **Outcome**: The test module fails against the current four-pass/schema-v1 template only for the
  newly required behavior.
- **Paths**: `tests/test_review_code_templates.py`
- **Dependencies**: None
- **Covers**: REQ-001 through REQ-012, REQ-017 through REQ-022; NFR-001 through NFR-005; **Plan**:
  Phase 1, first unit

**Test Scenarios**:

- **T001-S1**: The defect branch declares exactly five ordered passes and places System Contract
  between Scope and Behavior.
- **T001-S2**: Direct review derives only source-backed contracts and does not require feature
  artifacts.
- **T001-S3**: A contract records sources, producers, propagation boundaries, consumers, entry
  surfaces, scenarios, evidence, and a terminal status.
- **T001-S4**: Behavior/contract partitions have semantic scope, legal ownership, references,
  evidence, and terminal status independent of file disposition.
- **T001-S5**: An admitted finding does not stop unfinished contract, behavior, risk, specialist,
  or verification work.
- **T001-S6**: A repeatable cause triggers a bounded search of applicable equivalent surfaces and
  validates all qualifying occurrences.
- **T001-S7**: No meaningful sibling scope is recorded as `not_applicable` with a reason; an
  incomplete required search blocks PASS.
- **T001-S8**: Exactly one defect envelope uses schema version `"2"` and includes every required
  v2 entity and target fingerprint.
- **T001-S9**: Duplicate IDs, broken references, inconsistent counts, missing completion evidence,
  unresolved follow-up, blocking gaps, or incomplete mandatory work cannot produce PASS.
- **T001-S10**: Target selectors, resolver schema independence, audit output, verification
  read-only safety, risk profiles, priorities, and reviewer isolation remain required.

### T002 [P] [US3] Define the schema-v2 repair-loop contract

- [x] Update `tests/test_sdd_workflow_templates.py` with failing assertions for strict schema-v2
  validation, schema-v1 rejection, objective handoff retention, original-target association, fresh
  independent re-review, and fail-closed unresolved obligations.
- **Outcome**: The workflow tests expose every repair-loop migration required by schema v2 without
  weakening the existing progress and isolation guards.
- **Paths**: `tests/test_sdd_workflow_templates.py`
- **Dependencies**: None
- **Covers**: REQ-013 through REQ-018, REQ-021, REQ-022; NFR-001, NFR-004, NFR-005; **Plan**:
  Phase 1, second unit

**Test Scenarios**:

- **T002-S1**: A valid schema-v2 FAIL result can enter finding reproduction and repair.
- **T002-S2**: Schema v1, a missing envelope, multiple envelopes, malformed references, and
  contradictory counts are rejected as unsupported or inconclusive.
- **T002-S3**: Applicable objective outgoing obligations and unresolved incoming obligations are
  retained with their original fingerprint; verified or superseded incoming obligations are
  retired.
- **T002-S4**: Repair reasoning, old conclusions, and claims that the repair is correct are not
  sent to the fresh reviewer.
- **T002-S5**: A fresh reviewer verifies incoming obligations against the changed target and still
  executes all five general passes.
- **T002-S6**: Unresolved, unvalidated, or unassociated obligations prevent completion and remain
  caller-owned across subsequent rounds.

### T003 [P] [US2] Define strict schema-v2 evaluation parsing and corpus expectations

- [x] Update `tests/test_review_code_eval.py` with failing parser-validation cases and expected
  corpus entries for multi-surface contracts, multiple same-cause defects, continued partition
  completion, incomplete coverage, and clean PASS behavior.
- **Outcome**: Deterministic tests define the complete machine-result contract and the required
  source-independent evaluation corpus before runner or fixture changes.
- **Paths**: `tests/test_review_code_eval.py`
- **Dependencies**: None
- **Covers**: REQ-001 through REQ-018, REQ-022; NFR-002 through NFR-004; **Plan**: Phase 1, third
  unit; Phase 4

**Test Scenarios**:

- **T003-S1**: A fully populated, internally consistent schema-v2 PASS envelope parses.
- **T003-S2**: A schema-v1 or unknown-version envelope is rejected.
- **T003-S3**: Missing required entities, invalid enums, duplicate IDs, dangling references, count
  mismatches, or missing required evidence are rejected.
- **T003-S4**: PASS is rejected when a contract, partition, search, reviewer, verification,
  follow-up obligation, target fingerprint, or blocking coverage gap is incomplete.
- **T003-S5**: FAIL remains valid when an admitted finding exists and incomplete coverage is
  represented consistently.
- **T003-S6**: The corpus declares generic cases for multi-surface contract coverage, at least two
  related defect occurrences, continued coverage after an early finding, incomplete coverage, and
  clean PASS.

### T004 Verify the intentional red phase

- [x] Run
  `uv run pytest tests/test_review_code_templates.py tests/test_sdd_workflow_templates.py tests/test_review_code_eval.py -q`
  and confirm failures map to T001-T003 expectations rather than unrelated regressions.
- **Outcome**: The implementation begins from documented failures proving the new tests exercise
  missing behavior.
- **Paths**: No file changes
- **Dependencies**: T001, T002, T003
- **Covers**: REQ-022; NFR-004; **Plan**: Phase 1, fourth unit

**Test Scenarios**:

- **T004-S1**: The focused suite fails because the current review template has four passes and
  schema v1.
- **T004-S2**: The focused suite fails because the current repair loop consumes schema v1 and has
  no structured neutral handoff.
- **T004-S3**: The focused suite fails because the current parser and corpus lack required v2
  validation and evaluation cases.

## Phase 2: Command Producers and Consumers

### T005 [US1] Implement the five-pass defect gate and schema-v2 producer

- [x] Update only the defect-gate branch of `templates/commands/review-code.md` to implement the
  System Contract Pass, semantic partitions, continued mandatory review, bounded root-cause
  variant analysis, target fingerprinting, neutral follow-up output, coverage gaps, and strict v2
  completion checks while retaining six human sections and existing audit/target/safety behavior.
- **Outcome**: `tests/test_review_code_templates.py` passes and audit mode remains semantically
  unchanged.
- **Paths**: `templates/commands/review-code.md`
- **Dependencies**: T004
- **Covers**: REQ-001 through REQ-012, REQ-017 through REQ-021; NFR-001 through NFR-005; **Plan**:
  Phase 2

**Test Scenarios**:

- **T005-S1**: A cross-module change produces evidenced contracts and completed semantic
  partitions before PASS.
- **T005-S2**: A direct review with no feature artifacts limits contracts to verified code,
  project facts, and public boundaries.
- **T005-S3**: An early validated finding is reported only after every mandatory partition reaches
  a terminal state.
- **T005-S4**: A repeatable finding produces one root-cause record covering every qualifying
  occurrence in its bounded equivalent scope.
- **T005-S5**: A non-repeatable finding records why variant search is not applicable without
  expanding to an unrestricted audit.
- **T005-S6**: Missing fingerprint or incomplete contract, partition, search, follow-up, reviewer,
  or verification evidence yields INCONCLUSIVE unless a validated defect requires FAIL.
- **T005-S7**: A clean, fully evidenced review emits exactly one valid schema-v2 PASS result and six
  human report sections.
- **T005-S8**: `--audit` continues to emit its scorecard without a defect result envelope.

### T006 [P] [US3] Implement the schema-v2 repair-loop consumer

- [x] Update `templates/commands/implement-tasks.md` to validate only schema v2, reproduce findings,
  retain objective coverage and follow-up obligations with the originating fingerprint, exclude
  prior reasoning and conclusions, and require a fresh five-pass review of the updated target.
- **Outcome**: `tests/test_sdd_workflow_templates.py` passes with schema-v1 rejection and neutral
  handoff enforced.
- **Paths**: `templates/commands/implement-tasks.md`
- **Dependencies**: T004
- **Covers**: REQ-013 through REQ-018, REQ-021; NFR-001, NFR-004, NFR-005; **Plan**: Phase 3

**Test Scenarios**:

- **T006-S1**: A valid v2 FAIL result is independently reproduced before repair.
- **T006-S2**: Schema v1 and malformed or contradictory v2 results cannot be treated as a passed
  gate.
- **T006-S3**: Required objective obligations survive repair and preserve the old target
  fingerprint and source IDs.
- **T006-S4**: The next reviewer receives no repair narrative or old correctness conclusion.
- **T006-S5**: The next reviewer re-establishes incoming obligations against a new fingerprint and
  completes all five passes.
- **T006-S6**: Unresolved obligations or incomplete general review work yield INCONCLUSIVE rather
  than loop completion.

## Phase 3: Parser and Behavioral Evaluation

### T007 [US2] Migrate the evaluation runner to strict schema v2

- [x] Update `tests/evals/review_code/run_eval.py` and its canned-result construction in
  `tests/test_review_code_eval.py` to parse and validate the design's required schema-v2 entities,
  references, counts, evidence, statuses, fingerprints, follow-up records, coverage gaps, and
  verdict consistency. Keep case-file and aggregate-record versioning independent unless their own
  format changes.
- **Outcome**: Parser tests T003-S1 through T003-S5 pass without accepting schema v1.
- **Paths**: `tests/evals/review_code/run_eval.py`, `tests/test_review_code_eval.py`
- **Dependencies**: T003, T005
- **Covers**: REQ-011 through REQ-019, REQ-022; NFR-004; **Plan**: Phase 4, first unit

**Test Scenarios**:

- **T007-S1**: A complete v2 PASS result parses and evaluates against case expectations.
- **T007-S2**: v1, missing-field, invalid-enum, duplicate-ID, dangling-reference, and count-mismatch
  envelopes raise deterministic parse errors.
- **T007-S3**: Completed records without evidence and incomplete/not-applicable searches without a
  reason raise deterministic parse errors.
- **T007-S4**: PASS with unresolved obligations, blocking gaps, incomplete coverage, or admitted
  findings is rejected.
- **T007-S5**: A structurally consistent FAIL result with findings and represented coverage gaps is
  accepted for expectation evaluation.

### T008 [US1] [US2] Add generic systematic-coverage evaluation cases

- [x] Add source-independent case directories under `tests/evals/review_code/cases/` for
  multi-surface contract propagation, multiple related same-cause defects, continued partition
  completion after the first defect, required incomplete coverage, and clean complete coverage;
  update corpus expectations and `tests/evals/review_code/README.md` accordingly.
- **Outcome**: The corpus contract test recognizes every new case, every fixture is a valid
  synthetic Git change, and its expectations correspond to the intended review outcome.
- **Paths**: `tests/evals/review_code/cases/*/case.json`, `tests/test_review_code_eval.py`,
  `tests/evals/review_code/README.md`
- **Dependencies**: T007
- **Covers**: REQ-001 through REQ-010, REQ-017, REQ-018, REQ-022; NFR-002, NFR-003; **Plan**:
  Phase 4, second unit

**Test Scenarios**:

- **T008-S1**: One generic value crosses a producer, multiple propagation boundaries, consumers,
  and entry surfaces, and all applicable contract fields are expected.
- **T008-S2**: Two or more qualifying defects caused by one propagation or duplicated-default
  mistake are expected in the same result and linked to one root-cause search.
- **T008-S3**: A defect encountered early still leaves every mandatory partition in a terminal
  state.
- **T008-S4**: An uninspectable mandatory surface expects INCONCLUSIVE with a blocking gap.
- **T008-S5**: A clean multi-surface change expects PASS with complete coverage and no findings or
  open follow-up.
- **T008-S6**: Fixture names, descriptions, files, and expectations contain no motivating-project
  or motivating-incident dependency.

### T009 [US3] Verify deterministic multi-round handoff behavior

- [x] Complete the deterministic workflow assertions in `tests/test_sdd_workflow_templates.py` and
  evaluation-parser fixtures in `tests/test_review_code_eval.py` so a FAIL-to-repair-to-fresh-review
  sequence preserves neutral obligations, rejects v1, and does not transmit conclusions.
- **Outcome**: Multi-round behavior not exercisable by the one-shot live corpus has explicit,
  passing contract coverage.
- **Paths**: `tests/test_sdd_workflow_templates.py`, `tests/test_review_code_eval.py`
- **Dependencies**: T006, T007
- **Covers**: REQ-013 through REQ-016, REQ-022; NFR-001, NFR-004; **Plan**: Phase 4, third unit

**Test Scenarios**:

- **T009-S1**: A FAIL result creates open objective obligations tied to finding/contract IDs and the
  old fingerprint.
- **T009-S2**: The repair coordinator carries those obligations into the next isolated invocation
  without prior conclusions.
- **T009-S3**: The fresh result records each received obligation as verified, unresolved, or
  superseded with required evidence.
- **T009-S4**: A schema-v1 prior result is explicitly rejected rather than migrated or ignored.

## Phase 4: Documentation and Distribution

### T010 [P] Define the localized documentation contract

- [x] Update `tests/test_review_code_docs.py` to require every configured locale to describe five
  passes, contract/partition coverage, bounded related-defect analysis, schema v2, neutral
  caller-owned handoff, and unchanged advisory audit semantics.
- **Outcome**: Documentation tests fail against stale four-pass/schema-v1 text and cover all locale
  command guides.
- **Paths**: `tests/test_review_code_docs.py`
- **Dependencies**: T004
- **Covers**: REQ-001, REQ-002, REQ-008, REQ-011 through REQ-016, REQ-020, REQ-022; NFR-002,
  NFR-005; **Plan**: Phase 5, second unit

**Test Scenarios**:

- **T010-S1**: Every configured locale names or unambiguously describes all five passes in order.
- **T010-S2**: Every locale describes schema v2 coverage and neutral repair follow-up semantics.
- **T010-S3**: Every locale keeps `--audit` advisory and separate from the defect envelope.
- **T010-S4**: A stale four-pass or schema-v1 locale description fails the contract test.

### T011 Localize the systematic review behavior

- [x] Update every `docs/<locale>/user-guide/commands.md` review-code section to satisfy T010 while
  preserving each document's language and translation metadata.
- **Outcome**: All localized command guides accurately describe the confirmed generic behavior and
  `tests/test_review_code_docs.py` passes.
- **Paths**: `docs/*/user-guide/commands.md`
- **Dependencies**: T005, T006, T010
- **Covers**: REQ-001, REQ-002, REQ-008, REQ-011 through REQ-016, REQ-020; NFR-002, NFR-005;
  **Plan**: Phase 5, first unit
- **Verification**: Run `uv run pytest tests/test_review_code_docs.py -q`; inspect all locale diffs
  for semantic equivalence and unchanged frontmatter.

### T012 Regenerate supported command distributions

- [x] Run `uv run codexspec init . --force --ai both` and inspect generated Claude Code and Codex
  artifacts so they match the modified source templates without unrelated output.
- **Outcome**: Distributed `review-code` and `implement-tasks` copies are reproducibly synchronized
  with `templates/commands/`.
- **Paths**: Generated `.claude/commands/codexspec/`, `.agents/skills/`, and initializer-managed
  artifacts only
- **Dependencies**: T005, T006, T008, T009, T011
- **Covers**: REQ-001, REQ-011, REQ-016, REQ-020, REQ-021; NFR-002; **Plan**: Phase 5, third unit
- **Verification**: Compare source and generated semantics and run CodexSpec's own
  installer/integration tests. The generic standalone skill validator is not applicable because it
  rejects the repository's established `codexspec:<command>` namespaced skill names.

## Phase 5: Delivery Verification

### T013 Run focused and integration verification

- [x] Run the four focused test modules and relevant installer/integration tests after generation;
  resolve only failures attributable to this feature.
- **Outcome**: Template, repair-loop, parser, corpus, documentation, and generation integration
  checks all pass together.
- **Paths**: Test-driven corrections only in paths already owned by T001-T012
- **Dependencies**: T012
- **Covers**: REQ-019 through REQ-022; NFR-004; **Plan**: Phase 6, first unit

**Test Scenarios**:

- **T013-S1**: Review template contract suite passes.
- **T013-S2**: SDD workflow template suite passes.
- **T013-S3**: Review evaluation parser and corpus suite passes.
- **T013-S4**: Every localized command documentation contract passes.
- **T013-S5**: Installer and generated-command integration checks pass.

### T014 Run full quality and scope gates

- [x] Run the full pytest suite, Ruff, strict MkDocs build, package build, CodexSpec generation and
  installer validation, and `git diff --check`; then inspect the final status/diff and search changed product
  artifacts for motivating-project or incident references.
- **Outcome**: The branch is fully verified, source-independent, read-only in review behavior, and
  limited to the confirmed feature scope.
- **Paths**: Repository-wide verification; corrections remain limited to feature-owned paths
- **Dependencies**: T013
- **Covers**: REQ-001, REQ-019 through REQ-022; NFR-001 through NFR-004; **Plan**: Phase 6, second
  through fourth units

**Test Scenarios**:

- **T014-S1**: Full pytest and Ruff complete successfully.
- **T014-S2**: Strict MkDocs and package builds complete successfully.
- **T014-S3**: CodexSpec generation/installer validation for the namespaced review-code skill and
  whitespace checks complete successfully.
- **T014-S4**: Final diff contains no resolver schema change, audit semantic change, dependency
  change, persistent review-state write, or unrelated generated output.
- **T014-S5**: Changed product artifacts, fixtures, generated commands, and documentation contain no
  motivating-project or motivating-incident references.

## Dependencies and Execution Order

- T001, T002, and T003 may run in parallel because they modify separate test modules.
- T004 depends on all three failing-test tasks and establishes the red checkpoint.
- T005 and T006 may run in parallel after T004 because they modify separate source templates.
- T007 depends on the parser tests and the completed schema-v2 producer contract.
- T008 depends on the migrated parser; T009 depends on both the repair-loop consumer and parser.
- T010 may start after the red checkpoint because it modifies a separate documentation test.
- T011 depends on implemented command semantics and the documentation contract.
- T012 waits for all source templates, evaluation cases, workflow coverage, and docs to converge.
- T013 and T014 are sequential delivery gates after regeneration.

The graph is acyclic:

`(T001, T002, T003) -> T004 -> (T005, T006, T010) -> T007 -> (T008, T009, T011) -> T012 -> T013 -> T014`

## Checkpoints

- **Red checkpoint (T004)**: New contract tests fail only on absent feature behavior.
- **Producer/consumer checkpoint (T005-T006)**: Both source templates satisfy schema-v2 contracts.
- **Behavior checkpoint (T007-T009)**: Parser, corpus, and multi-round handoff are deterministic.
- **Distribution checkpoint (T010-T012)**: Documentation and generated copies match source.
- **Delivery checkpoint (T013-T014)**: Focused and full quality gates pass; final scope is clean.

## Coverage Matrix

| Requirement / Plan Item | Task and Scenario References |
|---|---|
| REQ-001, REQ-002, REQ-003, REQ-004; Plan Phases 1-2 | T001-S1 through T001-S3; T005-S1 through T005-S2; T008-S1, T008-S6 |
| REQ-005, REQ-006, REQ-007; Plan Phases 1-2 | T001-S4 through T001-S5; T005-S1, T005-S3; T008-S3 |
| REQ-008, REQ-009, REQ-010; Plan Phases 1-2 and 4 | T001-S6 through T001-S7; T005-S4 through T005-S6; T008-S2, T008-S4 |
| REQ-011, REQ-012; Plan Phases 1-2 and 4 | T001-S8 through T001-S9; T003-S1 through T003-S5; T005-S6 through T005-S7; T007-S1 through T007-S5 |
| REQ-013, REQ-014, REQ-015, REQ-016; Plan Phases 1, 3-5 | T002-S1 through T002-S6; T006-S1 through T006-S6; T009-S1 through T009-S4 |
| REQ-017, REQ-018; Plan Phases 1-4 | T001-S9; T003-S4 through T003-S5; T005-S3, T005-S6 through T005-S7; T007-S4 through T007-S5; T008-S3 through T008-S5 |
| REQ-019, REQ-020, REQ-021; Plan Phases 1-3 and 5-6 | T001-S10; T005-S8; T006-S1 through T006-S6; T013-S5; T014-S4 |
| REQ-022; Plan Phases 1 and 4-6 | T001-T004; T007-T010; T013-T014 |
| NFR-001 | T001-S10; T002-S3 through T002-S5; T005-S6; T006-S3 through T006-S5; T014-S4 |
| NFR-002 | T001-S2; T005-S2; T008-S1 through T008-S6; T010-T012; T014-S5 |
| NFR-003 | T001-S6 through T001-S7; T003-S6; T005-S4 through T005-S5; T008-S2 |
| NFR-004 | T001-S8 through T001-S9; T002-S1 through T002-S6; T003-S1 through T003-S5; T007-S1 through T007-S5; T013-T014 |
| NFR-005 | T001-S2 through T001-S7; T002-S3 through T002-S4; T005-S1 through T005-S5; T010-T011 |
| Plan Phase 5 | T010-T012 |
| Plan Phase 6 | T013-T014 |

## Unmapped Tasks

None. Every task implements or verifies an approved plan unit and traces to confirmed requirements.
