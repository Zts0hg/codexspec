# Feature Specification: Systematic Review Coverage

**Feature Branch**: `2026-0829-0035hy-review-code-systematic-coverage`
**Created**: 2026-08-29
**Status**: Draft
**Confirmed Requirements**: `.codexspec/specs/2026-0829-0035hy-review-code-systematic-coverage/requirements.md`

## Context

The change-scoped `review-code` defect gate already resolves a complete Git target, inventories
changed files, traces behavior, activates risk profiles, verifies findings, and fails closed when
required evidence is unavailable. Its result currently proves file disposition and reviewer
completion but does not make end-to-end contract coverage, related-defect searches, or repair
follow-up obligations machine-readable. A reviewer can therefore validate one occurrence of a
problem without establishing whether equivalent occurrences exist elsewhere in the selected
change.

This feature strengthens defect-gate mode for arbitrary repositories. It adds systematic
cross-module contract review, root-cause-based searches for related defects, complete review
partition tracking, and a read-only structured handoff between repair rounds.

## User Scenarios and Testing

### User Story 1: Review a cross-module change completely (Priority: P1)

As a developer reviewing a change that affects several modules or entry surfaces, I want the
reviewer to identify the consistency rules that connect those surfaces and verify the complete
flow, so a defect is not discovered one layer at a time across repeated reviews.

**Independent Test**: Run the defect gate against a synthetic change where one configuration
decision is produced once, propagated through multiple adapters, and consumed in multiple runtime
paths. The review result must identify the applicable contract and account for every relevant
producer, propagation boundary, consumer, entry surface, and scenario.

**Acceptance Scenarios**:

1. **Given** a selected change affects one value across several modules, **When** defect-gate mode
   builds its review coverage, **Then** it records the value's authoritative source, propagation
   boundaries, consumers, entry surfaces, and relevant normal and failure scenarios.
2. **Given** one mandatory surface cannot be inspected, **When** the review completes, **Then** the
   result is `INCONCLUSIVE` and names the uncovered surface instead of reporting `PASS`.
3. **Given** a repository has no CodexSpec feature artifacts, **When** a direct defect review has
   sufficient code and project evidence, **Then** the same contract analysis remains available
   without inventing requirements context.

### User Story 2: Find related defects in the same review (Priority: P1)

As a developer who receives a validated finding, I want the reviewer to search the bounded set of
equivalent callers, implementations, adapters, and symmetric paths before finalizing the report,
so related occurrences are reported together.

**Independent Test**: Run the defect gate against a synthetic change containing two defects caused
by the same duplicated default or propagation mistake. The result must record one root-cause search
and report every qualifying occurrence in that bounded search scope during the same review.

**Acceptance Scenarios**:

1. **Given** a candidate finding has a repeatable root cause, **When** the finding is validated,
   **Then** the reviewer records the root cause, derives a bounded search scope, searches equivalent
   locations, and records the result before emitting the final verdict.
2. **Given** the first qualifying finding is discovered before other review partitions finish,
   **When** the review continues, **Then** every mandatory contract, behavior, risk, and verification
   partition still reaches a terminal state.
3. **Given** no meaningful sibling scope exists, **When** variant analysis completes, **Then** the
   reviewer records the reason and completes the search without expanding into an unbounded
   repository-wide audit.

### User Story 3: Carry objective coverage through a repair loop (Priority: P1)

As a caller coordinating repair and re-review, I want a machine-readable record of what was checked
and what must be verified after repair, so a fresh reviewer can close the known obligations without
inheriting the previous reviewer's conclusions.

**Independent Test**: Feed an `implement-tasks` repair loop a schema-v2 FAIL result containing
coverage records and neutral follow-up obligations. The next fresh review must receive those
objective obligations, verify them against the updated target, repeat all mandatory general review
work, and emit a valid schema-v2 result.

**Acceptance Scenarios**:

1. **Given** a schema-v2 review reports one or more findings, **When** the caller verifies and repairs
   them, **Then** it retains the neutral follow-up obligations and supplies them to the next review.
2. **Given** a fresh reviewer receives prior coverage records, **When** it starts, **Then** it treats
   them as work to verify rather than evidence that the previous repair is correct.
3. **Given** the target fingerprint changed after repair, **When** the next review consumes prior
   coverage, **Then** it associates the prior records with their original target and re-establishes
   required evidence against the new target.
4. **Given** a caller cannot supply or validate a required follow-up obligation, **When** it requests
   completion, **Then** the final result remains `INCONCLUSIVE`.

### User Story 4: Preserve existing review modes and safety (Priority: P2)

As an existing CodexSpec user, I want target selection, risk review, read-only verification,
reviewer isolation, and advisory audit behavior to retain their established meanings while the
defect result format changes explicitly.

**Independent Test**: Run existing resolver, target-selection, audit, verification-safety, and
isolation contract tests together with schema-v2 tests. Existing behavior must remain green except
where the result-envelope version and required fields intentionally change.

**Acceptance Scenarios**:

1. **Given** any existing defect-gate target selector, **When** the command resolves its target,
   **Then** the resolver manifest remains independently versioned and target semantics are
   unchanged.
2. **Given** `review-code --audit`, **When** the audit completes, **Then** it retains its advisory
   scorecard and emits no defect-gate result envelope.
3. **Given** an old schema-v1 result reaches the updated `implement-tasks` gate, **When** it is
   validated, **Then** the caller rejects it as unsupported rather than inferring completion.

## Requirements

### Functional Requirements

- **REQ-001**: Defect-gate mode MUST provide the systematic review behavior in repositories of any
  supported language or structure and MUST NOT require CodexSpec feature artifacts unless the
  existing requirements-aware workflow requires them.
  - Sources: NEED-001, CON-003
- **REQ-002**: Before the Behavior Pass, the reviewer MUST derive the system-wide consistency rules
  and cross-module contracts implicated by confirmed requirements, project instructions, semantic
  change evidence, dependency relationships, and affected public behavior.
  - Sources: NEED-002, CON-003
- **REQ-003**: Each derived contract MUST record a stable review-local identifier, a plain-language
  statement, authoritative or evidentiary sources, applicable producers, propagation boundaries,
  consumers, entry surfaces, relevant scenarios, and completion state.
  - Sources: NEED-002, NEED-005
- **REQ-004**: Contract derivation MUST NOT invent product requirements. When authoritative intent
  is unavailable, the reviewer MUST limit the contract to behavior demonstrable from the selected
  change, verified project facts, and public compatibility boundaries.
  - Sources: NEED-001, NEED-002, CON-003, CON-005
- **REQ-005**: The reviewer MUST map every behavior or contract partition needed for the selected
  change to explicit scope, reviewer ownership, and one of the supported terminal states.
  - Sources: NEED-005, NEED-007
- **REQ-006**: A file inventory disposition MUST NOT by itself establish behavior or contract
  coverage.
  - Sources: NEED-002, NEED-007
- **REQ-007**: Discovery of a valid finding MUST NOT terminate unfinished mandatory review work;
  all selected contract, behavior, risk, specialist, and verification partitions MUST reach a
  terminal state before the round emits its final result.
  - Sources: NEED-004, CON-004
- **REQ-008**: For every admitted finding, the reviewer MUST record a root-cause identifier and one
  linked variant-search disposition. For a potentially repeatable cause, it MUST describe the
  cause, derive a reasonably bounded sibling search scope, inspect equivalent callers,
  implementations, adapters, entry surfaces, and symmetric paths as applicable, and record all
  qualifying occurrences.
  - Sources: NEED-003, NEED-005
- **REQ-009**: When a finding has no meaningful sibling search scope, the reviewer MUST record why
  and MUST NOT expand the defect gate into an unrelated whole-repository audit.
  - Sources: NEED-001, NEED-003, CON-003
- **REQ-010**: A root-cause variant search that is required but incomplete MUST prevent `PASS` and
  produce `INCONCLUSIVE` unless an attributable qualifying defect already requires `FAIL`.
  - Sources: NEED-003, CON-004
- **REQ-011**: Defect-gate mode MUST emit exactly one result envelope with
  `schema_version: "2"`.
  - Sources: NEED-005, DEC-001
- **REQ-012**: The schema-v2 envelope MUST contain structured contract coverage, review partitions,
  root-cause variant searches, neutral post-repair verification obligations, and a deterministic
  identifier for the reviewed target evidence.
  - Sources: NEED-005, NEED-006, DEC-001, DEC-002
- **REQ-013**: Each post-repair verification obligation MUST state the objective behavior or
  evidence to re-establish, its source finding or incomplete contract, partition, variant search,
  or coverage gap, and its completion state, without asserting that a repair is correct.
  - Sources: NEED-006, CON-002
- **REQ-014**: The next fresh reviewer in a repair loop MUST receive applicable neutral coverage and
  follow-up obligations, MUST associate them with their original target identifier, and MUST
  independently verify them against the updated target.
  - Sources: NEED-006, CON-002, DEC-002
- **REQ-015**: Prior coverage MUST supplement rather than replace the next round's complete Scope,
  Behavior, Risk, and Verification passes.
  - Sources: NEED-004, NEED-006, CON-002, CON-005
- **REQ-016**: `implement-tasks` MUST accept only a valid schema-v2 result for this gate, retain
  neutral coverage and follow-up obligations across verified repair rounds, and reject schema-v1,
  malformed, incomplete, or contradictory results.
  - Sources: NEED-008, DEC-001, DEC-002
- **REQ-017**: `PASS` MUST require complete inventory accounting, complete mandatory contract and
  partition coverage, complete required root-cause variant searches, complete verification,
  complete reviewer topology, no blocking follow-up obligation, no blocking coverage gap, and zero
  admitted P0-P3 findings. Requirements coverage MUST be consistent with the selected target;
  `partial` or `not_evaluated` may support only a code-level `PASS`, never whole-feature readiness.
  - Sources: NEED-004, NEED-005, NEED-007, CON-004
- **REQ-018**: Missing or incomplete mandatory contract coverage, partition coverage, root-cause
  search, follow-up verification, reviewer output, or target identity MUST produce `INCONCLUSIVE`
  unless a validated defect independently requires `FAIL`.
  - Sources: CON-004, CON-005
- **REQ-019**: The Git review-context resolver manifest MUST remain independently versioned and
  retain its existing schema unless a separate resolver requirement is established.
  - Sources: DEC-003, CON-005
- **REQ-020**: Advisory `--audit` mode MUST retain its current path-oriented scorecard semantics and
  MUST NOT emit or consume the schema-v2 defect-gate envelope.
  - Sources: DEC-004, CON-005
- **REQ-021**: Existing defect target selectors, requirement-coverage rules, risk profiles,
  verification-safety rules, finding priorities, and reviewer-isolation requirements MUST remain
  effective.
  - Sources: CON-005
- **REQ-022**: Contract tests and source-independent behavioral evaluation cases MUST verify
  multi-surface contract coverage, multiple related defects found in one review, continuation after
  the first finding, neutral repair handoff, schema-v1 rejection, incomplete-coverage failure, and
  clean-change PASS behavior.
  - Sources: NEED-001, NEED-003, NEED-004, NEED-005, NEED-006, NEED-008, CON-003

### Non-Functional Requirements

- **NFR-001: Read-only operation**: Review execution MUST NOT create, update, or delete repository
  files, Git state, dependencies, or persistent review-state artifacts.
  - Sources: CON-001, DEC-002
- **NFR-002: Source independence**: Command instructions, schemas, fixtures, and documentation MUST
  describe generic review behavior without naming or encoding the motivating source incident.
  - Sources: NEED-001, CON-003
- **NFR-003: Bounded analysis**: Contract and root-cause searches MUST be broad enough to cover
  semantically equivalent surfaces and bounded enough to avoid turning every change review into an
  unrestricted repository audit.
  - Sources: NEED-001, NEED-003
- **NFR-004: Deterministic result validation**: Schema-v2 required fields, enums, counts,
  relationships, completion states, and target identity MUST be machine-validatable, and malformed
  or contradictory data MUST fail closed.
  - Sources: NEED-005, CON-004, DEC-001
- **NFR-005: Clear communication**: Contract statements, root causes, search scopes, and follow-up
  obligations MUST use common, precise developer terminology and concrete behavior descriptions.
  - Sources: NEED-002, NEED-003

## Expected Error Behavior

- Invalid, missing, duplicated, or unsupported result envelopes are `INCONCLUSIVE`.
- A required contract or partition with no owner or terminal state is `INCONCLUSIVE`.
- A required root-cause variant search with incomplete scope or evidence is `INCONCLUSIVE` unless
  another validated finding already makes the round `FAIL`.
- A prior coverage record whose target identifier cannot be matched to its originating evidence is
  not treated as current proof; applicable obligations must be re-established.
- A schema-v1 result presented to the updated repair loop is rejected with an explicit schema
  migration error.
- Environment or reviewer-capability failures remain evidence failures and are never converted to
  `PASS`.

## Success Criteria

- **SC-001**: Template contract tests establish every required schema-v2 field and every new review
  stage obligation.
- **SC-002**: A source-independent evaluation change with at least two related defect occurrences
  reports all qualifying occurrences in one completed review result.
- **SC-003**: A source-independent evaluation change with an early finding still records terminal
  states for every mandatory review partition.
- **SC-004**: A repair-loop contract test proves that neutral obligations survive into a fresh
  review while prior correctness conclusions do not.
- **SC-005**: Existing target resolution, risk-profile, audit, verification-safety, and clean-change
  tests remain green after the intentional result-schema migration.
- **SC-006**: No distributed command, schema field, fixture, or user documentation names or depends
  on the motivating source incident.

## Out of Scope

- Mathematical proof that one review finds every possible defect.
- A fixed number of consecutive clean reviews as a completion requirement.
- Automatic creation of repository-local review history or state files.
- Changes to advisory path-audit scoring.
- Changes to Git target resolution or its manifest schema without a separate demonstrated need.
- Product artifacts, fixtures, or examples tied to the motivating source incident.

## Assumptions

- A caller that performs repairs can retain the prior schema-v2 result in its execution context and
  supply the neutral coverage and follow-up records to the next review.
- Stable review-local identifiers need only be deterministic within the result and its direct
  repair handoff; they are not global repository identifiers.

## Dependencies

- Existing `review-code` resolver and defect-gate protocol.
- Existing `implement-tasks` final repair loop.
- Existing template contract and source-independent review evaluation infrastructure.

## Requirements Traceability

| Confirmed Entry | Spec Coverage | Notes |
|---|---|---|
| NEED-001 | REQ-001, REQ-004, REQ-009, REQ-022; NFR-002, NFR-003 | Source-independent behavior |
| NEED-002 | REQ-002 through REQ-004, REQ-006 | Cross-module contract review |
| NEED-003 | REQ-008 through REQ-010, REQ-022; NFR-003 | Root-cause variant analysis |
| NEED-004 | REQ-007, REQ-015, REQ-017, REQ-022 | Complete the round |
| NEED-005 | REQ-003, REQ-005, REQ-008, REQ-011, REQ-012, REQ-017, REQ-022; NFR-004 | Structured coverage |
| NEED-006 | REQ-012 through REQ-015, REQ-022 | Read-only repair handoff |
| NEED-007 | REQ-005 through REQ-007, REQ-017 | Partition completion |
| NEED-008 | REQ-016, REQ-022 | Repair-loop integration |
| CON-001 | NFR-001 | Review remains read-only |
| CON-002 | REQ-013 through REQ-015 | Independent verification |
| CON-003 | REQ-001, REQ-002, REQ-004, REQ-009, REQ-022; NFR-002 | No project-specific coupling |
| CON-004 | REQ-007, REQ-010, REQ-017, REQ-018; NFR-004 | Fail closed |
| CON-005 | REQ-004, REQ-015, REQ-018 through REQ-021 | Existing safety retained |
| DEC-001 | REQ-011, REQ-012, REQ-016; NFR-004 | Schema-v2 result |
| DEC-002 | REQ-012, REQ-014, REQ-016; NFR-001 | Caller-owned handoff |
| DEC-003 | REQ-019 | Resolver schema remains independent |
| DEC-004 | REQ-020 | Defect-gate-only improvement |
| OUT-001 | Out of Scope | No exhaustive-proof claim |
| OUT-002 | Out of Scope | No repeated-clean-round requirement |
| OUT-003 | NFR-001; Out of Scope | No repository-local state |
| OUT-004 | NFR-002; Out of Scope | No source-incident examples |
