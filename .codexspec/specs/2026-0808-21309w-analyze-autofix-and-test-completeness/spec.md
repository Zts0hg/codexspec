# Feature Specification: analyze-autofix-and-test-completeness

<!--
Language: Generated in the document language from .codexspec/config.yml (en).
-->

**Feature Branch**: `2026-0808-21309w-analyze-autofix-and-test-completeness`
**Created**: 2026-08-08
**Status**: Draft
**Input**: Confirmed requirements at `.codexspec/specs/2026-0808-21309w-analyze-autofix-and-test-completeness/requirements.md`

## Context & Goals

Two related enhancements to the CodexSpec SDD pipeline, scoped to three existing
distributed command templates only — `templates/commands/analyze.md`,
`plan-to-tasks.md`, and `implement-tasks.md`:

1. **Make `analyze` remediate, not just report.** `analyze` currently detects
   cross-artifact inconsistencies and only describes a fix. It must instead
   resolve them by repairing the downstream artifacts, bounded by the model that
   `requirements.md` is the single source of truth.
2. **Stop losing test detail between `tasks.md` and delivered code.** Test
   scenarios (especially boundary/error) implied by `tasks.md` are silently
   omitted during `implement-tasks`. This is fixed at both ends: `plan-to-tasks`
   enumerates explicit scenarios per testable task (front-load), and
   `implement-tasks` self-verifies scenario coverage before reporting success
   (back-load).

No new command is introduced; `review-code.md` is not modified.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - `analyze` auto-remediates cross-artifact inconsistencies (Priority: P1)

As a developer running the SDD pipeline, when `analyze` finds an inconsistency
between `spec.md`/`plan.md`/`tasks.md` and the confirmed `requirements.md`, it
repairs the downstream artifact automatically so I no longer have to apply every
fix by hand.

**Why this priority**: This is the user's primary complaint — a detector with no
repair action is low-value. It delivers standalone value even without Feature 2.

**Independent Test**: In a feature workspace with a seeded deterministic
inconsistency (e.g. a task missing its `Covers:` reference, a spec item with a
broken source link), run `analyze` and confirm the downstream artifact is
corrected while `requirements.md` is untouched.

**Acceptance Scenarios**:

1. **Given** a confirmed requirement uncovered downstream, **When** `analyze`
   runs, **Then** it adds the missing downstream coverage and leaves
   `requirements.md` unchanged.
2. **Given** a downstream entry that conflicts with the upstream truth source,
   **When** `analyze` runs, **Then** it conforms the lower-authority side with the
   minimal change needed to remove the conflict.
3. **Given** a downstream entry that adds derived detail but does not conflict
   with anything, **When** `analyze` runs, **Then** it is preserved untouched
   (not deleted, no escalation).
4. **Given** `workflow.auto_next: true`, **When** `analyze` runs inside the
   chain, **Then** it auto-applies deterministic fixes with no confirmation
   prompt.

---

### User Story 2 - `plan-to-tasks` enumerates explicit test scenarios (Priority: P1)

As a developer, when `plan-to-tasks` produces `tasks.md`, every testable task
carries an explicit, individually identifiable list of test scenarios (happy path
plus the boundary/error cases the behavior implies), so implementation can be
checked against them.

**Why this priority**: The front-load half of Feature 2; delivers value on its own
(clearer, checkable tasks) and is the source of truth the back-load check maps to.

**Independent Test**: Run `plan-to-tasks` on a plan with testable behavior and
confirm each testable task in `tasks.md` lists identifiable scenarios covering
boundary/error where implied, each traceable to a spec/requirement behavior.

**Acceptance Scenarios**:

1. **Given** a testable task, **When** `plan-to-tasks` generates it, **Then** it
   carries an explicit, individually identifiable scenario list including
   behavior-implied boundary/error cases.
2. **Given** a non-testable task (docs/config/assets/infra), **When**
   `plan-to-tasks` generates it, **Then** it keeps its deterministic verification
   and is not forced to carry test scenarios.
3. **Given** upstream behavior too underspecified to enumerate meaningful
   scenarios, **When** `plan-to-tasks` runs, **Then** it triggers its stop
   condition instead of inventing scenarios.
4. **Given** generated scenarios, **When** Pre-Save Validation / `review-tasks`
   runs, **Then** a testable task lacking sufficient scenarios is flagged.

---

### User Story 3 - `implement-tasks` self-verifies scenario coverage before success (Priority: P2)

As a developer, before `implement-tasks` reports success, its review loop confirms
that every enumerated scenario in `tasks.md` maps to a real, asserting test —
blocking and repairing any gap first.

**Why this priority**: The back-load half of Feature 2. Its value depends on
scenarios existing (US2), so it follows US2.

**Independent Test**: Run `implement-tasks` on a `tasks.md` whose testable task
lists a scenario for which no test is implemented; confirm the run does not report
success until a genuine covering test is added.

**Acceptance Scenarios**:

1. **Given** an enumerated scenario with no covering test, **When**
   `implement-tasks` reaches its review loop, **Then** it treats the gap as
   blocking and repairs it (red-green add test, re-verify, re-review) before
   success.
2. **Given** an enumerated scenario covered only by a hollow/non-asserting test,
   **When** the review loop runs, **Then** it is treated as uncovered and blocks.
3. **Given** all enumerated scenarios covered by genuine tests, **When** the
   review loop runs, **Then** the scenario self-check passes and does not block.

### Edge Cases

- A downstream entry lacking any upstream authority but not conflicting with
  anything → preserved, not a defect (completeness is not harmed).
- A conflict where the source-of-truth is silent → resolved against the
  authority hierarchy (the unauthorized/lower side yields); no human escalation.
- Upstream behavior too thin to derive scenarios → `plan-to-tasks` stops rather
  than inventing intent.
- A scenario listed but implemented by a hollow test → counted as uncovered.
- `analyze` invoked in the chain before code exists → it stays artifact-only and
  never attempts a `tasks → code` check.

## Requirements *(mandatory)*

### Functional Requirements

- **REQ-001**: `analyze` MUST resolve detected inconsistencies by repairing the
  affected downstream artifact(s), not only report a remediation.
  - Sources: NEED-001, DEC-001
- **REQ-002**: `analyze` MUST NOT modify `requirements.md`; every fix conforms a
  downstream artifact (`spec`/`plan`/`tasks`) to `requirements`, with the fix
  direction determined by the authority hierarchy (requirements > spec > plan >
  tasks).
  - Sources: CON-001, OUT-001
- **REQ-003**: `analyze` MUST auto-apply deterministic, authority-directed fixes
  by default in both manual runs and the `auto_next` chain run, with no
  confirmation prompt and no human-escalation path.
  - Sources: DEC-001
- **REQ-004**: For the completeness dimension, `analyze` MUST auto-add missing
  downstream coverage for any uncovered upstream authority, and MUST preserve a
  downstream entry that only adds derived detail (no upstream authority) when it
  does not conflict.
  - Sources: CON-002
- **REQ-005**: For the consistency dimension, `analyze` MUST act only on
  conflicts; on a conflict it MUST conform the unauthorized/lower-authority side
  with the minimal change needed to remove it, and take no action when there is
  no conflict.
  - Sources: CON-002
- **REQ-006**: `analyze` MUST remain artifact↔artifact only
  (`requirements`/`spec`/`plan`/`tasks`) and MUST NOT perform code-level
  (`tasks → code`) verification.
  - Sources: DEC-003, OUT-003
- **REQ-007**: `plan-to-tasks` MUST enumerate, for every testable task, an
  explicit, individually identifiable list of test scenarios covering the happy
  path plus the boundary/error cases the behavior implies.
  - Sources: NEED-002, DEC-004
- **REQ-008**: Scenario enumeration MUST apply only to testable tasks;
  non-testable tasks (docs, config, assets, infra) MUST retain their deterministic
  verification and MUST NOT be forced to carry test scenarios.
  - Sources: CON-003
- **REQ-009**: Enumerated scenarios MUST derive from `spec.md` acceptance criteria
  / the covered requirement's behavior; `plan-to-tasks` MUST expand rather than
  invent, and MUST trigger its stop condition when upstream behavior is too
  underspecified to enumerate meaningful scenarios.
  - Sources: DEC-005
- **REQ-010**: `plan-to-tasks` MUST enforce scenario enumeration in its Pre-Save
  Validation and via the `review-tasks` loop; scenarios MUST be individually
  identifiable/traceable to enable one-to-one downstream mapping, and enumeration
  MUST avoid padding (only behavior-implied scenarios).
  - Sources: DEC-004, CON-004
- **REQ-011**: Before reporting success, `implement-tasks` MUST self-verify,
  within its existing Final Code Review Loop, that every enumerated scenario in
  `tasks.md` maps to at least one implemented test that genuinely exercises and
  asserts it.
  - Sources: NEED-003, DEC-002, CON-004
- **REQ-012**: A missing or hollow scenario coverage MUST be treated as blocking
  and repaired through the existing repair loop (add the missing test red-green,
  re-verify, re-review) before `implement-tasks` may report success.
  - Sources: NEED-003, DEC-002
- **REQ-013**: The back-load check MUST be implemented inside `implement-tasks`;
  it MUST NOT extend `review-code`, MUST NOT be a new command, and MUST NOT be
  added to `analyze`.
  - Sources: DEC-002, OUT-002, OUT-004

### Non-Functional Requirements

- **NFR-001**: `analyze` auto-remediation MUST be deterministic — the fix
  direction MUST be uniquely determined by the authority hierarchy and MUST never
  require inventing user intent — so unattended auto-fix is safe in direction.
  - Sources: CON-001, CON-002, DEC-001
- **NFR-002**: All changes MUST be made in the source templates under
  `templates/commands/` (`analyze.md`, `plan-to-tasks.md`, `implement-tasks.md`);
  the derived copies under `.claude/commands/codexspec/` MUST NOT be hand-edited.
  - Sources: CON-005

## Confirmed Constraints & Decisions

- **CON-001 / DEC-001**: `requirements.md` is the single source of truth; fixes
  are always downstream-conforming and fully auto-applied. → REQ-002, REQ-003,
  NFR-001
- **CON-002**: "No upstream authority" is not a defect; act on conflicts only. →
  REQ-004, REQ-005
- **CON-003**: Front-load applies to testable tasks only. → REQ-008
- **CON-004**: Front and back are coupled; scenarios must be individually
  traceable. → REQ-010, REQ-011
- **CON-005**: Edit source templates, never the self-bootstrap install artifact. →
  NFR-002
- **DEC-002**: Back-load lives in `implement-tasks`' review loop (not
  `review-code`, not a new command, not `analyze`). → REQ-011, REQ-012, REQ-013
- **DEC-003 / OUT-003**: `analyze` stays artifact-only because it runs before code
  exists in the chain. → REQ-006
- **DEC-004**: Every testable task must enumerate scenarios incl. boundary/error,
  no padding. → REQ-007, REQ-010
- **DEC-005**: Scenarios derive from spec/requirement behavior; expand, never
  invent. → REQ-009

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: For a workspace with a seeded deterministic downstream inconsistency,
  running `analyze` resolves it with zero manual edits and leaves `requirements.md`
  unchanged.
- **SC-002**: A non-conflicting downstream derived-detail entry survives an
  `analyze` run unmodified (zero false deletions).
- **SC-003**: After `plan-to-tasks`, 100% of testable tasks in `tasks.md` carry an
  explicit scenario list that includes boundary/error cases wherever the behavior
  implies them.
- **SC-004**: `implement-tasks` never reports success while any enumerated scenario
  lacks a genuine covering test — a seeded missing-scenario case is caught and
  blocks.
- **SC-005**: The change set touches only the three source templates; no new
  command file is added and `review-code.md` is unchanged.

## Out of Scope

- **`analyze` modifying `requirements.md`** (OUT-001): it is the user-confirmed
  source of truth; only the user changes it via `/codexspec:specify` or
  `/codexspec:clarify`.
- **New standalone commands** (OUT-002): both enhancements are changes to existing
  commands.
- **`analyze` performing code-level (`tasks → code`) checks** (OUT-003): in the
  chain, `analyze` runs after `plan-to-tasks` and before `implement-tasks`, when no
  code exists, so such a check is structurally impossible there; code-level
  verification belongs to `implement-tasks`.
- **Modifying `review-code.md`** (OUT-004): the back-load check stays inside
  `implement-tasks`.

## Assumptions

- New user-visible output (fix notices, scenario enumeration) follows the existing
  two-language convention (interaction vs document language). This is a project
  convention, not a scope expansion.
- Existing behaviors that are not explicitly changed — `auto_next` chaining, legacy
  spec-only mode, existing gates and stop conditions — are preserved.

## Dependencies

- Relies on the existing authority hierarchy and the requirements-as-source-of-truth
  model already present across the pipeline.
- The back-load check (REQ-011/012) depends on the front-load enumeration
  (REQ-007/010) producing individually identifiable scenarios; a `tasks.md` without
  enumerated scenarios yields nothing for the back-load check to verify.

## Open Questions

- None blocking. OPEN-001 (origin of test scenarios) was resolved by DEC-005 and is
  captured in REQ-009.

## Requirements Traceability

| Confirmed Requirement | Spec Coverage | Notes |
|-----------------------|---------------|-------|
| NEED-001 | REQ-001 | analyze remediates, not just reports |
| NEED-002 | REQ-007 | scenario enumeration per testable task |
| NEED-003 | REQ-011, REQ-012 | back-load self-check + blocking repair |
| CON-001 | REQ-002, NFR-001 | requirements = source of truth |
| CON-002 | REQ-004, REQ-005 | conflict-only remediation |
| CON-003 | REQ-008 | testable tasks only |
| CON-004 | REQ-010, REQ-011 | traceable scenarios, coupled ends |
| CON-005 | NFR-002 | edit source templates only |
| DEC-001 | REQ-001, REQ-003, NFR-001 | full auto-fix by default |
| DEC-002 | REQ-011, REQ-012, REQ-013 | back-load inside implement-tasks |
| DEC-003 | REQ-006 | analyze stays artifact-only |
| DEC-004 | REQ-007, REQ-010 | mandatory enumeration, no padding |
| DEC-005 | REQ-009 | scenarios derive from spec/requirements |
| OUT-001 | REQ-002, Out of Scope | never modify requirements.md |
| OUT-002 | REQ-013, Out of Scope | no new commands |
| OUT-003 | REQ-006, Out of Scope | no code-level checks (timing) |
| OUT-004 | REQ-013, Out of Scope | review-code.md unchanged |
| OPEN-001 | REQ-009 | resolved by DEC-005 |
