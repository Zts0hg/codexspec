# Feature Specification: Review Convergence

**Feature Branch**: `2026-1008-1952ti-review-convergence`
**Created**: 2026-10-08
**Status**: Draft
**Input**: Confirmed requirements record `requirements.md` (Feature ID `2026-1008-1952ti`)

## Context and Goals

`review-code` is CodexSpec's strict pre-merge defect gate. `implement-tasks` drives it in a final review loop: review, verify findings, repair, re-review with a fresh isolated reviewer, until a valid `PASS`. The loop has converged on many features, but one observed run did not reach `PASS` after 21+ rounds. Its rounds were consumed by wasted work rather than by the gate's strictness:

- re-reviewing unchanged, already-covered evidence (about 1,900 inventory entries every round);
- findings whose trigger lies outside the project's real operating context;
- review-environment overhead that voided rounds without a product defect;
- different instances of the same root-cause class reappearing in successive rounds;
- reviewers spawned with the implementation conversation inherited.

**Goal**: keep complete-feature acceptance and reduce ineffective, redundant review work so the loop converges well (NEED-001). Default behavior keeps today's review standard (CON-002), and a final `PASS` still rests on one fresh, complete review (CON-001).

## User Scenarios & Testing

### User Story 1 - Incremental re-review between repairs (Priority: P1)

A developer runs `implement-tasks` on a large feature. The first complete review returns `FAIL` with a few findings. After each repair set, the next review covers only what the repair changed and what it affects, instead of the whole feature again. When an incremental round passes, one fresh complete review provides the final acceptance.

**Why this priority**: Repeated complete re-reviews of unchanged evidence were the largest source of wasted rounds.

**Independent Test**: On a feature target with an admitted finding, repair it and re-run the loop; observe that the intermediate round's scope is limited to the repair delta, its affected contracts and call chains, and carried-over obligations, and that a complete review runs after the incremental round passes.

**Acceptance Scenarios**:

1. **Given** a complete review returned `FAIL` and a repair set is green, **When** the loop re-reviews, **Then** the round reviews the repair delta, the contracts and call chains it affects, and the carried-over follow-up obligations, and reuses previous coverage for evidence whose fingerprint is unchanged.
2. **Given** an incremental round passes, **When** the loop continues, **Then** a fresh complete review runs, and only that complete review can produce the loop's final `PASS`.
3. **Given** the final complete review finds new defects, **When** they are repaired, **Then** the loop returns to incremental review, and after an incremental round passes, runs a new fresh complete review.

---

### User Story 2 - Deciding out-of-context findings once (Priority: P2)

A project owner sets `review.decided_by: ask`. A reviewer finds a defect whose trigger requires inputs or environments the project does not actually encounter (for example, `ß`/`ẞ` filename aliasing in a Chinese/English-only project). Instead of failing on it, the review presents it for a scenario decision. The owner chooses fix or accept once; later rounds follow that decision without raising the issue again.

**Why this priority**: Unrealistic-trigger findings caused out-of-scope repairs and extra rounds, but this behavior is opt-in.

**Independent Test**: With `review.decided_by: ask`, review a change containing such a finding; observe the scenario-decision prompt, record "accept", and confirm a subsequent round does not re-raise it. With the default, observe unchanged behavior.

**Acceptance Scenarios**:

1. **Given** `review.decided_by` is absent or `reviewer`, **When** a review runs, **Then** the reviewer decides on every finding exactly as today.
2. **Given** `review.decided_by: ask`, **When** the reviewer finds a defect whose trigger depends on inputs or environments outside the project's real operating context, **Then** the review reports it as needing a scenario decision instead of failing on it.
3. **Given** the user decides "fix", **When** the loop continues, **Then** the item is handled as a finding to repair.
4. **Given** the user decides "accept", **When** later rounds run, **Then** the decision is recorded in the feature artifacts and the same issue is not raised again.
5. **Given** `review.decided_by: ask` in configuration, **When** a single invocation passes `--decided-by reviewer`, **Then** that invocation uses `reviewer`.

---

### User Story 3 - Escalating a recurring root-cause class (Priority: P2)

During the loop, a finding in a later round belongs to a root-cause class already recorded in an earlier round (for example, symlink-ancestor writes outside the repository at a new location). `implement-tasks` escalates into `debug` and handles the whole class as one defect: shared root cause, uniform repair, and a codebase-wide search for every location of that class.

**Why this priority**: Instance-by-instance patching let the same class reappear round after round, and no round cap is wanted.

**Independent Test**: Simulate two rounds whose verified findings share a root-cause class at different locations; observe that the second occurrence enters `debug` with class-wide scope.

**Acceptance Scenarios**:

1. **Given** a verified finding, **When** `implement-tasks` records it, **Then** it assigns a root-cause class using the reviewer's root-cause description and its own verification.
2. **Given** a later round's verified finding matches an already-recorded class, **When** the repair starts, **Then** `implement-tasks` escalates into `debug` and treats the whole class as one defect.
3. **Given** a class-level repair fails three times, **When** `debug` evaluates it, **Then** its existing rule of questioning the architecture applies.

---

### User Story 4 - Review rounds not voided by the environment (Priority: P3)

A review runs on a large target in a host with output and thread limits. Verification mirrors still have the Git metadata tests need, complete inventory and coverage records go to files outside the repository with only a summary and the envelope in the conversation, and specialist nesting stays within a bound.

**Why this priority**: These failures voided rounds without any product defect.

**Independent Test**: Run a review whose verification requires Git metadata in a disposable mirror and whose inventory is large; observe that verification succeeds, that the conversation output contains only the summary and envelope, and that specialist nesting stays within the bound.

**Acceptance Scenarios**:

1. **Given** a check must run in a disposable mirror, **When** the mirror is created, **Then** it preserves the Git metadata the check needs.
2. **Given** a large inventory, **When** the review reports, **Then** complete inventory and coverage records are written to files outside the repository and the conversation receives only a summary and the result envelope.
3. **Given** specialists are required, **When** they are spawned, **Then** their nesting depth does not exceed the defined bound.

---

### User Story 5 - Unambiguous reviewer isolation on every host (Priority: P3)

Whether the host is Codex or Claude Code, the coordinator spawns each reviewer and specialist in a fresh context that does not inherit the implementation conversation.

**Why this priority**: Some observed rounds forked the full implementation conversation into the reviewer, which the isolation rule forbids.

**Independent Test**: Inspect the instructions on both host forms and confirm they state concretely that reviewers start in a fresh context and must not inherit the implementation conversation (for example, no full-conversation fork).

**Acceptance Scenarios**:

1. **Given** the coordinator spawns a reviewer on Codex, **When** it chooses spawn options, **Then** the instructions explicitly forbid inheriting the implementation conversation.
2. **Given** the same on Claude Code, **When** it delegates review, **Then** the same constraint is equally explicit.

### Edge Cases

- **Incremental round finds a defect in an unchanged area**: the defect is reported normally; coverage reuse never suppresses an admitted finding.
- **Reused coverage would be stale**: evidence whose fingerprint changed is never covered by reuse; only unchanged-fingerprint evidence keeps previous coverage.
- **Scenario decision pending**: while a scenario decision is unanswered, the result is not `PASS` (CON-001).
- **`ask` mode without feature context** (direct `review-code` run): the scenario-decision item is still surfaced and the result is not `PASS` until decided; how a decision is persisted without a feature directory is a design concern and must not weaken this.
- **Invalid `review.decided_by` or `--decided-by` value**: reported as an error; the invalid value is not silently treated as `ask`.
- **Root-cause class ambiguous**: classification is `implement-tasks`' judgment backed by its verification; a mis-classification never removes a finding from repair.

## Requirements

### Functional Requirements

- **REQ-001**: After a repair, intermediate re-review rounds MUST cover the repair delta, the contracts and call chains it affects, and the carried-over follow-up obligations.
  - Sources: NEED-002, DEC-001
- **REQ-002**: In an intermediate round, evidence whose fingerprint is unchanged MUST keep the coverage established by the previous round, unless it lies within the contracts and call chains affected by the repair, which REQ-001 requires to be reviewed; evidence whose fingerprint changed MUST be reviewed again.
  - Sources: NEED-002, DEC-001
- **REQ-003**: After an incremental round passes, the loop MUST run a fresh complete review, and only that complete review MAY produce the loop's final `PASS`.
  - Sources: NEED-002, DEC-001, CON-001
- **REQ-004**: If the final complete review finds new defects, the loop MUST re-review their repairs incrementally first and, once an incremental round passes, run a new fresh complete review.
  - Sources: DEC-005, DEC-001
- **REQ-005**: `review-code` MUST support a decision mode with values `reviewer` and `ask`, configured as `review.decided_by` in `.codexspec/config.yml` and overridable per invocation with `--decided-by reviewer|ask`. The default is `reviewer`.
  - Sources: NEED-003, DEC-002, DEC-003
- **REQ-006**: In `reviewer` mode, `review-code` MUST behave exactly as it does today.
  - Sources: NEED-003, DEC-002, CON-002
- **REQ-007**: In `ask` mode, a finding whose trigger depends on inputs or environments outside the project's real operating context MUST be reported as needing a scenario decision instead of producing `FAIL` by itself, and the user decides once: fix or accept.
  - Sources: NEED-003, DEC-002
  - Such a scenario-decision item is a distinct state, not an admitted P0–P3 finding, so it does not conflict with NFR-001; it becomes an admitted finding only when the user decides "fix", and while its decision is pending the result is not `PASS`.
  - Sources: NEED-003, CON-001
- **REQ-008**: A user's scenario decision MUST be recorded in the feature artifacts, and later rounds MUST follow it without re-raising the same issue. A "fix" decision makes the item a finding to repair.
  - Sources: NEED-003
- **REQ-009**: `implement-tasks` and `auto-dev` MUST apply the configured `review.decided_by` without changing their fixed `review-code` invocation.
  - Sources: DEC-003
- **REQ-010**: The `review.decided_by` key MUST be manageable through the project configuration tooling (the `codexspec config` CLI and the `/codexspec:config` command).
  - Sources: DEC-003, CON-003
- **REQ-011**: `implement-tasks` MUST assign a cross-round root-cause class to each verified finding, combining the reviewer's root-cause description with its own verification, and keep these classes across rounds.
  - Sources: NEED-004, DEC-006
- **REQ-012**: When a verified finding's class matches a class recorded in an earlier round, `implement-tasks` MUST escalate into `debug`, treating the whole class as one defect: identify the shared root cause, repair it uniformly, and search the codebase for every location of that class. The `debug` three-failed-fixes rule applies.
  - Sources: NEED-004, DEC-004
- **REQ-013**: A disposable verification mirror MUST preserve the Git metadata that the verification needs.
  - Sources: NEED-005
- **REQ-014**: Complete inventory and coverage records MUST be written to files outside the repository; the conversation MUST receive only a summary and the result envelope.
  - Sources: NEED-005
- **REQ-015**: The nesting depth of specialist reviewers MUST be bounded so reviews do not hit host thread limits.
  - Sources: NEED-005
- **REQ-016**: Reviewer-isolation instructions MUST state concretely, for both Codex and Claude Code, that reviewers and specialists are spawned in a fresh context and must not inherit the implementation conversation.
  - Sources: NEED-006

### Non-Functional Requirements

- **NFR-001**: The final acceptance completeness MUST NOT be reduced: a final `PASS` rests on one fresh complete review, and any admitted P0–P3 finding still produces `FAIL`.
  - Sources: CON-001, NEED-001
- **NFR-002**: With default configuration, `review-code` MUST apply the same review standard as today.
  - Sources: CON-002
- **NFR-003**: No maximum number of review rounds is introduced; convergence relies on REQ-001 to REQ-016.
  - Sources: OUT-001, DEC-004
- **NFR-004**: Changes MUST be made in source templates (`templates/commands/review-code.md`, `templates/commands/implement-tasks.md`, minor `templates/commands/debug.md` adjustments where needed) plus the configuration CLI and related templates; `auto-dev` inherits behavior through `implement-tasks`; derived `.claude/commands/codexspec/` and `.agents/skills/codexspec-*/` copies are not hand-edited.
  - Sources: CON-003

### Key Entities

- **Coverage record**: per-evidence review coverage bound to a fingerprint; reusable only while the fingerprint is unchanged.
- **Scenario decision**: a user's fix/accept decision on an out-of-context finding, recorded in feature artifacts and binding on later rounds.
- **Root-cause class**: `implement-tasks`' cross-round grouping of verified findings sharing one underlying cause.
- **`review.decided_by`**: configuration key (`reviewer` | `ask`, default `reviewer`) with per-invocation override `--decided-by`.

## Success Criteria

- **SC-001**: In a loop with repairs, every intermediate round's scope is limited to REQ-001's scope, and the loop's terminal `PASS` always comes from a fresh complete review.
- **SC-002**: With default configuration, `review-code` verdicts and admission behavior are unchanged on existing review scenarios.
- **SC-003**: In `ask` mode, an accepted out-of-context issue is not re-raised in any later round of the same feature.
- **SC-004**: A root-cause class recurring in a later round always triggers a class-level `debug` escalation.
- **SC-005**: No review round is voided by a mirror lacking Git metadata, by conversation output too large to display, or by exceeding specialist nesting bounds.

## Confirmed Constraints and Decisions

- CON-001 → NFR-001; CON-002 → NFR-002, REQ-006; CON-003 → NFR-004, REQ-010.
- DEC-001 → REQ-001 to REQ-003; DEC-002 → REQ-005 to REQ-007; DEC-003 → REQ-005, REQ-009, REQ-010; DEC-004 → REQ-012, NFR-003; DEC-005 → REQ-004; DEC-006 → REQ-011.

## Open Questions

None. All `OPEN` entries were resolved in `requirements.md` (OPEN-001 → DEC-005, OPEN-002 → DEC-003, OPEN-003 → DEC-006).

## Out of Scope

- **Review round cap** (OUT-001): no maximum number of review rounds is introduced.

## Assumptions

- **A-1 (understanding aid, not scope)**: "Feature artifacts" in REQ-008 means the feature's confirmed CodexSpec artifacts that later reviewers already read as authoritative context; the exact artifact and record format are design decisions.

## Dependencies

- `templates/commands/review-code.md`, `templates/commands/implement-tasks.md`, `templates/commands/debug.md`, `templates/commands/config.md`, and the `codexspec config` command in `src/codexspec/__init__.py`.

## Requirements Traceability

| Confirmed Requirement | Spec Coverage | Notes |
|-----------------------|---------------|-------|
| NEED-001 | Goals, NFR-001 | Full |
| NEED-002 | REQ-001, REQ-002, REQ-003 | Full |
| NEED-003 | REQ-005, REQ-006, REQ-007, REQ-008 | Full |
| NEED-004 | REQ-011, REQ-012 | Full |
| NEED-005 | REQ-013, REQ-014, REQ-015 | Full |
| NEED-006 | REQ-016 | Full |
| CON-001 | NFR-001, REQ-003 | Constraint preserved |
| CON-002 | NFR-002, REQ-006 | Constraint preserved |
| CON-003 | NFR-004, REQ-010 | Constraint preserved |
| DEC-001 | REQ-001, REQ-002, REQ-003 | Decision preserved |
| DEC-002 | REQ-005, REQ-006, REQ-007 | Decision preserved |
| DEC-003 | REQ-005, REQ-009, REQ-010 | Decision preserved, naming `review.decided_by` / `--decided-by` |
| DEC-004 | REQ-012, NFR-003 | Decision preserved |
| DEC-005 | REQ-004 | Decision preserved |
| DEC-006 | REQ-011 | Decision preserved |
| OUT-001 | Out of Scope, NFR-003 | Exclusion preserved |
