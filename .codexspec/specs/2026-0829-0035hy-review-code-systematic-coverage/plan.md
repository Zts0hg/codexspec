# Implementation Plan: Systematic Review Coverage

**Related Spec**: `.codexspec/specs/2026-0829-0035hy-review-code-systematic-coverage/spec.md`
**Related Design**: `.codexspec/specs/2026-0829-0035hy-review-code-systematic-coverage/design.md`
**Confirmed Requirements**: `.codexspec/specs/2026-0829-0035hy-review-code-systematic-coverage/requirements.md`
**Created**: 2026-08-29
**Status**: Draft

## Context

CodexSpec distributes `review-code` and `implement-tasks` from Markdown command templates and
protects their behavior with template contract tests plus a source-independent behavioral
evaluation runner. The current defect gate has four passes and a schema-v1 result envelope. This
plan implements the confirmed design by changing the source templates, migrating every in-repo
consumer to schema v2, extending the evaluation corpus, updating localized command documentation,
and regenerating derived Claude Code and Codex command artifacts.

The Git target resolver and audit branch remain unchanged. All implementation work is performed in
the dedicated feature worktree created from the latest `origin/main`.

## Goals / Non-Goals

**Goals:**

- Make system-wide consistency rules and cross-module contracts a mandatory, evidenced review
  pass before behavior inspection.
- Require bounded searches for related occurrences of every validated repeatable root cause while
  completing all other mandatory review work.
- Upgrade the defect result and repair-loop consumer atomically to strict schema v2 with neutral,
  caller-owned follow-up obligations.
- Verify the new behavior with prompt contract tests and source-independent behavioral evaluation
  cases, while retaining existing target, audit, safety, and isolation behavior.
- Keep distributed templates, generated command artifacts, tests, and localized documentation in
  sync.

**Non-Goals:**

- Changing Git target resolution or the resolver manifest schema.
- Changing advisory `--audit` scoring or output.
- Persisting review history in the reviewed repository.
- Guaranteeing discovery of every possible defect or requiring a fixed number of clean reviews.
- Adding project-, language-, or framework-specific review rules.

## Tech Stack and Repository Constraints

- **Source format**: Markdown command templates under `templates/commands/`.
- **Implementation and test language**: Python 3.11+ with pytest.
- **Behavioral evaluation**: `tests/evals/review_code/run_eval.py` and synthetic Git fixtures.
- **Documentation**: MkDocs source under `docs/<locale>/user-guide/commands.md`.
- **Package and tooling**: `uv`, Ruff, pytest, MkDocs, and the existing CodexSpec initializer.
- `templates/commands/` is the source of truth. Generated `.claude/commands/codexspec/` and
  `.agents/skills/` copies are regenerated; they are not edited by hand.
- Existing source layout and dependencies are sufficient; no new runtime dependency is planned.

## Assumptions

- The existing Markdown commands remain the executable specification for reviewer behavior; no
  separate runtime schema library is required by the confirmed design.
- The evaluation harness can validate schema-v2 structure deterministically and use canned or live
  reviewer output according to its existing modes.
- Localized documentation can be updated without changing translation frontmatter because command
  semantics, not document identity, change.
- The initializer can regenerate both Claude Code and Codex distributions from the modified source
  templates without altering the feature artifacts.

## Plan-Level Decisions

### Decision 1: Lock behavior with failing contract and evaluation tests before template changes

**Context**: The feature changes a large prompt contract and an intentionally incompatible result
schema. Editing prose first would make omissions difficult to distinguish from intended migration.

**Options Considered**:

1. Change templates and update tests afterward.
2. Add focused failing assertions and evaluation cases first, then implement until they pass.

**Decision**: Add the schema-v2, five-pass, repair-handoff, and behavioral evaluation expectations
before changing command behavior. Keep tests focused on externally required prompt semantics and
machine-validatable results rather than incidental paragraph wording.

**Rationale**: This makes the explicit format upgrade and every new completion condition visible
as a deliberate contract change, and it reduces the chance that a later prose edit silently drops
one required behavior.

**Covers**: REQ-002 through REQ-018, REQ-022; NFR-002, NFR-004; Design: Distributed Review Command,
System Contract Mapper, Review Partition Coordinator, Root-Cause Variant Analyzer, Schema-v2 Result
and Handoff, Repair-Loop Consumer, Contract and Behavioral Evaluation

**Decision Level**: Plan-level implementation decision; does not change confirmed product scope or
the confirmed design

### Decision 2: Migrate producer, consumer, parser, fixtures, and documentation in one branch

**Context**: Schema v2 is intentionally incompatible with schema v1. A partial migration would
leave some distributed workflows accepting or emitting an unsupported format.

**Options Considered**:

1. Temporarily accept both schema versions.
2. Update every in-repository producer and consumer together and explicitly reject schema v1.

**Decision**: Update `review-code`, `implement-tasks`, the evaluation parser and fixtures, template
tests, and documentation in the same implementation sequence. Do not add a compatibility shim.

**Rationale**: This implements the confirmed explicit format upgrade, keeps invalid intermediate
states confined to the feature branch, and preserves fail-closed behavior.

**Covers**: REQ-011 through REQ-020, REQ-022; NFR-004; Design: Schema-v2 Result and Handoff,
Repair-Loop Consumer, Contract and Behavioral Evaluation

**Decision Level**: Plan-level implementation decision; does not change confirmed product scope or
the confirmed design

### Decision 3: Use generic synthetic repositories for behavior evaluation

**Context**: The new review behavior must work across projects and must not encode the incident
that motivated the improvement.

**Options Considered**:

1. Reuse a real application repository as the fixture.
2. Add compact synthetic changes with generic producers, propagation boundaries, consumers, and
   symmetric paths.

**Decision**: Extend the existing source-independent evaluation corpus with generic fixtures that
isolate multi-surface contract propagation, multiple related occurrences, continued coverage after
an early finding, incomplete coverage, and clean completion.

**Rationale**: Small synthetic changes make the expected behavior observable without coupling the
command to one repository, language-specific architecture, or prior defect.

**Covers**: REQ-001, REQ-004, REQ-007 through REQ-010, REQ-022; NFR-002, NFR-003; Design: System
Contract Mapper, Root-Cause Variant Analyzer, Contract and Behavioral Evaluation

**Decision Level**: Plan-level implementation decision; does not change confirmed product scope or
the confirmed design

### Decision 4: Regenerate distributed artifacts only after source templates and tests converge

**Context**: Derived Claude Code and Codex files must match the source templates but hand-editing
them would create multiple authorities.

**Options Considered**:

1. Edit generated files alongside source templates.
2. Complete source changes, then regenerate both distributions with the existing initializer.

**Decision**: Treat `templates/commands/` as the only editable command source and run
`uv run codexspec init . --force --ai both` after source-level tests converge. Validate the
generated `review-code` skill with the repository and skill validation checks.

**Rationale**: This follows repository ownership rules and gives one reproducible synchronization
step for all distributed copies.

**Covers**: REQ-001, REQ-011, REQ-016, REQ-020 through REQ-022; NFR-002; Design: Distributed Review
Command, Repair-Loop Consumer, Contract and Behavioral Evaluation

**Decision Level**: Plan-level implementation decision; does not change confirmed product scope or
the confirmed design

## Risks / Trade-offs

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Prompt assertions become coupled to incidental wording | Medium | Medium | Assert required concepts, ordering, enum values, and cross-field rules; avoid whole-paragraph snapshots |
| Schema migration misses an in-repo consumer | Medium | High | Search all schema-version references, update producer/consumer/parser together, and run full tests |
| New live evaluation cases are nondeterministic | Medium | Medium | Keep fixtures minimal, assert required observable properties, and retain deterministic canned parser tests |
| Contract or variant instructions encourage unbounded review | Low | High | Require source-backed contract scope and cause-derived bounded searches with explicit terminal states |
| Generated artifacts drift from source templates | Low | High | Regenerate through the initializer and run integration, package, and skill validation checks |
| Localized documentation describes stale four-pass behavior | Medium | Medium | Update all locale copies and keep documentation contract tests exhaustive over configured locales |

## Implementation Phases

### Phase 1: Establish failing schema-v2 and workflow contracts

- [ ] Extend `tests/test_review_code_templates.py` to require the ordered Scope, System Contract,
  Behavior, Risk, and Verification passes; source-backed contract mapping; behavior partitions;
  completion after the first finding; bounded variant searches; target fingerprinting; and strict
  schema-v2 completion rules. — **Covers**: REQ-002 through REQ-012, REQ-017 through REQ-019,
  REQ-021, REQ-022; NFR-003, NFR-004, NFR-005; Design: Distributed Review Command, System Contract
  Mapper, Review Partition Coordinator, Root-Cause Variant Analyzer, Schema-v2 Result and Handoff,
  Contract and Behavioral Evaluation
- [ ] Extend `tests/test_sdd_workflow_templates.py` to require schema-v2 validation and rejection of
  v1, preservation of objective coverage and follow-up records, original-target association,
  exclusion of repair reasoning and correctness conclusions, and a fresh complete five-pass
  re-review. — **Covers**: REQ-013 through REQ-018, REQ-021, REQ-022; NFR-001, NFR-004; Design:
  Schema-v2 Result and Handoff, Repair-Loop Consumer, Contract and Behavioral Evaluation
- [ ] Extend parser-level evaluation tests with valid and invalid schema-v2 envelopes, including
  identifier uniqueness, references, count consistency, evidence requirements, terminal states,
  target fingerprint, follow-up status, coverage gaps, and verdict consistency. — **Covers**:
  REQ-011 through REQ-018, REQ-022; NFR-004; Design: Schema-v2 Result and Handoff, Contract and
  Behavioral Evaluation
- [ ] Run the focused contract tests and record the expected failures before implementation. —
  **Covers**: REQ-022; NFR-004; Design: Contract and Behavioral Evaluation

### Phase 2: Implement the five-pass defect gate and schema-v2 producer

- [ ] Update only the defect-gate branch of `templates/commands/review-code.md` to add the System
  Contract Pass before Behavior, derive contracts from authoritative or verified evidence, and keep
  direct reviews independent of feature artifacts. — **Covers**: REQ-001 through REQ-004,
  REQ-020, REQ-021; NFR-001, NFR-002, NFR-005; Design: Distributed Review Command, System Contract
  Mapper
- [ ] Add explicit behavior/contract partition ownership and terminal-state accounting that is
  distinct from the file inventory and continues after findings are admitted. — **Covers**:
  REQ-005 through REQ-007, REQ-017, REQ-018; Design: Review Partition Coordinator
- [ ] Add finding identifiers and the bounded root-cause variant-analysis loop inside Verification,
  including justified `not_applicable` handling and fail-closed incomplete searches. — **Covers**:
  REQ-007 through REQ-010, REQ-017, REQ-018; NFR-003, NFR-005; Design: Root-Cause Variant Analyzer
- [ ] Replace the defect result example and validation protocol with the exact schema-v2 entities,
  target fingerprint semantics, cross-reference and count checks, neutral follow-up records,
  coverage-gap records, and verdict consistency rules from `design.md`. Preserve the existing six
  human report sections. — **Covers**: REQ-011 through REQ-018, REQ-019, REQ-021; NFR-001,
  NFR-004, NFR-005; Design: Distributed Review Command, Schema-v2 Result and Handoff
- [ ] Confirm that the audit branch, target selectors, resolver manifest schema, risk profiles,
  verification safety, and reviewer isolation text retain their existing semantics. — **Covers**:
  REQ-019 through REQ-021; NFR-001; Design: Distributed Review Command

### Phase 3: Migrate the repair-loop consumer

- [ ] Update `templates/commands/implement-tasks.md` to require and validate schema v2, reject schema
  v1 and contradictory results, and independently reproduce admitted findings before repair. —
  **Covers**: REQ-011, REQ-016 through REQ-018, REQ-021; NFR-004; Design: Repair-Loop Consumer
- [ ] Retain only objective contract coverage and neutral follow-up obligations, associate them with
  the originating target fingerprint, and pass them to a fresh isolated reviewer without repair
  reasoning, previous conclusions, or an assertion of correctness. — **Covers**: REQ-013 through
  REQ-016; NFR-001, NFR-005; Design: Schema-v2 Result and Handoff, Repair-Loop Consumer
- [ ] Require each fresh review to verify incoming obligations against the updated fingerprint and
  still complete all five general passes; treat unresolved or unvalidated obligations as
  `INCONCLUSIVE`. — **Covers**: REQ-014 through REQ-018; NFR-004; Design: Repair-Loop Consumer

### Phase 4: Implement source-independent behavioral evaluation

- [ ] Migrate `tests/evals/review_code/run_eval.py` and canned envelopes to strict schema-v2 parsing
  and validation without changing resolver-manifest versioning. — **Covers**: REQ-011 through
  REQ-019, REQ-022; NFR-004; Design: Schema-v2 Result and Handoff, Contract and Behavioral
  Evaluation
- [ ] Add generic synthetic evaluation cases for one contract crossing multiple surfaces, two or
  more defects sharing a root cause, completion of every partition after an early finding, a
  required but incomplete coverage path, and a clean complete review. — **Covers**: REQ-001 through
  REQ-010, REQ-017, REQ-018, REQ-022; NFR-002, NFR-003; Design: System Contract Mapper, Review
  Partition Coordinator, Root-Cause Variant Analyzer, Contract and Behavioral Evaluation
- [ ] Add deterministic workflow coverage for neutral repair handoff and schema-v1 rejection where
  live one-shot review evaluation cannot exercise the multi-round caller. — **Covers**: REQ-013
  through REQ-016, REQ-022; NFR-004; Design: Repair-Loop Consumer, Contract and Behavioral
  Evaluation

### Phase 5: Synchronize documentation and generated distributions

- [ ] Update every localized `docs/<locale>/user-guide/commands.md` review-code description to
  describe five passes, system contract and partition coverage, bounded related-defect analysis,
  schema v2, and caller-owned neutral follow-up while preserving audit semantics. — **Covers**:
  REQ-001, REQ-002, REQ-008, REQ-011 through REQ-016, REQ-020; NFR-002, NFR-005; Design:
  Distributed Review Command, Schema-v2 Result and Handoff, Repair-Loop Consumer
- [ ] Update documentation contract tests so every configured locale rejects stale four-pass or
  schema-v1 descriptions. — **Covers**: REQ-011, REQ-020, REQ-022; NFR-002; Design: Contract and
  Behavioral Evaluation
- [ ] Regenerate Claude Code and Codex command artifacts from source templates with
  `uv run codexspec init . --force --ai both`; inspect the diff to ensure only intended derived
  command changes occur. Validate the namespaced generated skill through CodexSpec's own
  generation and installer integration tests; the generic standalone skill validator rejects the
  repository's established `codexspec:<command>` names and is not applicable. — **Covers**:
  REQ-001, REQ-011, REQ-016, REQ-020, REQ-021; NFR-002;
  Design: Distributed Review Command, Repair-Loop Consumer

### Phase 6: Verify delivery and source independence

- [ ] Run focused tests for review templates, workflow templates, evaluation parsing, and localized
  documentation; then run relevant installer/integration tests. — **Covers**: REQ-019 through
  REQ-022; NFR-004; Design: Contract and Behavioral Evaluation
- [ ] Run the full pytest suite, Ruff, strict MkDocs build, `git diff --check`, package build, and
  generated skill validation. — **Covers**: REQ-001, REQ-020 through REQ-022; NFR-001, NFR-002,
  NFR-004; Design: Distributed Review Command, Contract and Behavioral Evaluation
- [ ] Search all changed product artifacts, fixtures, generated commands, and documentation for
  references to the motivating repository or incident and fail delivery if any are present. —
  **Covers**: REQ-001, REQ-022; NFR-002; Design: System Contract Mapper, Contract and Behavioral
  Evaluation
- [ ] Inspect the final diff for resolver changes, audit semantic changes, persistent review-state
  writes, dependency changes, or unrelated generated output. — **Covers**: REQ-019 through
  REQ-021; NFR-001, NFR-003; Design: Distributed Review Command, Schema-v2 Result and Handoff

## Verification Strategy

1. **Red phase**: run focused template and evaluation tests after adding expectations; confirm they
   fail specifically because the current command has four passes, emits schema v1, and lacks the
   structured coverage and handoff fields.
2. **Green phase**: rerun the same focused tests after each source-template or parser migration.
3. **Behavior evaluation**: run the source-independent evaluation corpus in deterministic test mode;
   run live cases when reviewer credentials and the existing harness mode are available.
4. **Distribution verification**: regenerate both supported AI targets and run CodexSpec's
   generation and installer integration tests against the namespaced derived copies.
5. **Repository verification**: run full tests, lint, strict documentation build, package build, and
   whitespace validation.
6. **Scope verification**: inspect Git status and diff; confirm no resolver schema, audit contract,
   dependency, persistent-state, or project-specific content was introduced.

## Requirements Coverage

| Spec Requirement | Design Component | Plan Coverage |
|---|---|---|
| REQ-001 | Distributed Review Command; System Contract Mapper | Decisions 3-4; Phases 2, 4-6 |
| REQ-002 | System Contract Mapper | Decision 1; Phases 1-2, 5 |
| REQ-003 | System Contract Mapper | Decision 1; Phases 1-2, 4 |
| REQ-004 | System Contract Mapper | Decision 3; Phases 2, 4 |
| REQ-005 | Review Partition Coordinator | Decision 1; Phases 1-2, 4 |
| REQ-006 | Review Partition Coordinator | Decision 1; Phases 1-2, 4 |
| REQ-007 | Review Partition Coordinator; Root-Cause Variant Analyzer | Decisions 1 and 3; Phases 1-2, 4 |
| REQ-008 | Root-Cause Variant Analyzer | Decisions 1 and 3; Phases 1-2, 4-5 |
| REQ-009 | Root-Cause Variant Analyzer | Decisions 1 and 3; Phases 1-2, 4 |
| REQ-010 | Root-Cause Variant Analyzer | Decisions 1 and 3; Phases 1-2, 4 |
| REQ-011 | Schema-v2 Result and Handoff | Decisions 1-2 and 4; Phases 1-6 |
| REQ-012 | Schema-v2 Result and Handoff | Decisions 1-2; Phases 1-4 |
| REQ-013 | Schema-v2 Result and Handoff; Repair-Loop Consumer | Decisions 1-2; Phases 1, 3-5 |
| REQ-014 | Schema-v2 Result and Handoff; Repair-Loop Consumer | Decisions 1-2; Phases 1, 3-5 |
| REQ-015 | Repair-Loop Consumer | Decisions 1-2; Phases 1, 3-5 |
| REQ-016 | Repair-Loop Consumer | Decisions 1-2 and 4; Phases 1, 3-6 |
| REQ-017 | Review Partition Coordinator; Schema-v2 Result and Handoff | Decisions 1-2; Phases 1-4 |
| REQ-018 | Schema-v2 Result and Handoff; Repair-Loop Consumer | Decisions 1-2; Phases 1-4 |
| REQ-019 | Distributed Review Command; Schema-v2 Result and Handoff | Decisions 2 and 4; Phases 1-2, 4, 6 |
| REQ-020 | Distributed Review Command | Decisions 2 and 4; Phases 2, 5-6 |
| REQ-021 | Distributed Review Command; Repair-Loop Consumer | Decisions 1-2 and 4; Phases 1-3, 5-6 |
| REQ-022 | Contract and Behavioral Evaluation | Decisions 1-4; Phases 1, 4-6 |
| NFR-001 | Schema-v2 Result and Handoff; Repair-Loop Consumer | Phases 1-3, 6 |
| NFR-002 | System Contract Mapper; Contract and Behavioral Evaluation | Decisions 1, 3-4; Phases 2, 4-6 |
| NFR-003 | Root-Cause Variant Analyzer | Decisions 1 and 3; Phases 1-2, 4, 6 |
| NFR-004 | Schema-v2 Result and Handoff; Contract and Behavioral Evaluation | Decisions 1-2; Phases 1, 3-4, 6 |
| NFR-005 | System Contract Mapper; Root-Cause Variant Analyzer | Decisions 1 and 3; Phases 1-3, 5 |

## Unresolved Items

None. The implementation sequence does not require a product decision beyond the confirmed
requirements and design.
