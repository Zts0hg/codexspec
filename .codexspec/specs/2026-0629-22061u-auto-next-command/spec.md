# Feature Specification: workflow.auto_next — Auto-Advance the SDD Command Chain

<!--
Language: Generate this document in the language specified in .codexspec/config.yml.
Document language is English.
-->

**Feature Branch**: `2026-0629-22061u-auto-next-command`
**Created**: 2026-06-29
**Status**: Draft
**Input**: Confirmed requirements at `.codexspec/specs/2026-0629-22061u-auto-next-command/requirements.md`

## Context

CodexSpec's Spec-Driven Development (SDD) pipeline is a sequence of slash commands:

`/codexspec:specify → /codexspec:generate-spec → /codexspec:spec-to-plan → /codexspec:plan-to-tasks → /codexspec:implement-tasks`

Today every transition is triggered manually by the user. Three of the generation commands (`generate-spec`, `spec-to-plan`, `plan-to-tasks`) already conclude with an internal **Automatic Review Loop** that invokes the matching `/codexspec:review-*` command and yields an Overall Status: `PASS`, `PASS_WITH_WARNINGS`, `NEEDS_REVISION`, or `BLOCKED`. A precedent for conditional auto-invocation already exists: `plan-to-tasks.md` contains an "Automatic Cross-Artifact Analysis" section that invokes `/codexspec:analyze` exactly once when its review loop ends in `PASS` / `PASS_WITH_WARNINGS` (commit #17).

This feature generalizes that precedent into an opt-in **auto-advance** mode controlled by a new `workflow.auto_next` option in `.codexspec/config.yml`. When enabled, the pipeline advances to the next command automatically once the current stage has "passed", so a feature can flow from confirmed requirements all the way through implementation without manual hand-offs.

## Goals

- Let a developer run the SDD pipeline end-to-end with no manual triggering between stages, when they opt in.
- Reuse the existing per-stage review verdict as the gate for advancement, so quality is not bypassed.
- Preserve current manual behavior by default; change nothing for projects that do not opt in.

## Non-Goals

See **Out of Scope**. In particular: no auto-invocation of optional helpers (`clarify`, `checklist`, `tasks-to-issues`); no per-transition granularity; no confirmation prompt before `implement-tasks`.

## User Scenarios & Testing

### User Story 1 — Hands-off pipeline run (Priority: P1)

As a developer who has just confirmed requirements, I want the pipeline to run from `specify` through `implement-tasks` automatically, so that I can step away and return to a finished implementation.

**Why this priority**: This is the core value of the feature — maximum automation of the SDD chain.

**Independent Test**: Enable `workflow.auto_next: true`, run `/codexspec:specify` for a feature, confirm the requirements, and observe each subsequent command (`generate-spec`, `spec-to-plan`, `plan-to-tasks`, `implement-tasks`) invoke in order, each preceded by a one-line `auto_next:` notice.

**Acceptance Scenarios**:

1. **Given** `workflow.auto_next: true` and the user has confirmed `specify` requirements completion, **When** `specify` finishes, **Then** `/codexspec:generate-spec <feature-dir>` is invoked automatically after a one-line `auto_next:` notice.
2. **Given** `workflow.auto_next: true` and `generate-spec`'s review loop returns `PASS`, **When** the review loop ends, **Then** `/codexspec:spec-to-plan <feature-dir>` is invoked automatically.
3. **Given** `workflow.auto_next: true` and `plan-to-tasks`'s review loop returns `PASS_WITH_WARNINGS`, **When** the review loop ends, **Then** `/codexspec:analyze` runs once, then `/codexspec:implement-tasks <feature-dir>` is invoked automatically, with no confirmation prompt.

### User Story 2 — Default behavior unchanged (Priority: P2)

As a developer who has not opted in, I want the pipeline to behave exactly as before, so existing workflows and automation are not affected.

**Why this priority**: Backwards compatibility is a hard constraint; it must not regress.

**Independent Test**: Leave `.codexspec/config.yml` unchanged (no `workflow.auto_next` key); run each command and confirm each ends without invoking the next.

**Acceptance Scenarios**:

1. **Given** `workflow.auto_next` is absent or `false`, **When** any command completes, **Then** no next command is auto-invoked and the user triggers the next one manually.
2. **Given** `workflow.auto_next: false` explicitly, **When** `generate-spec` review returns `PASS`, **Then** the command ends without invoking `spec-to-plan`.

### User Story 3 — Chain stops on a failed review (Priority: P2)

As a developer, when a stage's review does not pass, I want the chain to stop and hand control back to me, so I can fix the artifact before any further stages run.

**Why this priority**: Prevents bad upstream artifacts from being carried into code automatically.

**Independent Test**: Enable `workflow.auto_next: true`; cause a review to return `NEEDS_REVISION` (or `BLOCKED`); confirm the chain stops and no next command runs.

**Acceptance Scenarios**:

1. **Given** `workflow.auto_next: true` and a review loop returns `NEEDS_REVISION`, **When** the review loop ends, **Then** no next command is invoked and control returns to the user.
2. **Given** `workflow.auto_next: true` and a review loop returns `BLOCKED`, **When** the review loop ends, **Then** control returns to the user with no auto-advance.

### Edge Cases

- `workflow.auto_next` set to a non-boolean value (e.g. `"yes"`, `1`): treated as **not enabled** (see Assumptions) — manual behavior.
- `implement-tasks` completes (success or "needs work"): the chain **ends**; nothing is auto-invoked afterward.
- `plan-to-tasks` passes but `analyze` reports critical cross-artifact issues: `implement-tasks` is **still** auto-invoked — `analyze` is informational and non-gating (CON-005).
- A command is invoked manually mid-chain by the user while `auto_next` is on: it behaves normally and, on pass, continues the chain. Auto-next is evaluated at each stage's pass, not locked in at the start.
- `requirements.md` is absent (legacy spec-only mode) for a downstream command: auto-next still applies based on that command's own review verdict; the legacy limitation is disclosed by each command as today.

## Requirements

### Functional Requirements

- **REQ-001**: The system MUST provide a boolean configuration option `workflow.auto_next` in `.codexspec/config.yml`. Only the literal value `true` enables auto-advance.
  - Sources: NEED-001, CON-003, CON-004

- **REQ-002**: When `workflow.auto_next` is `true` and a generation command's (`generate-spec`, `spec-to-plan`, `plan-to-tasks`) Automatic Review Loop concludes with Overall Status `PASS` or `PASS_WITH_WARNINGS`, the system MUST automatically invoke the next chain command for the same feature directory: `generate-spec → spec-to-plan`, `spec-to-plan → plan-to-tasks`, `plan-to-tasks → implement-tasks`.
  - Sources: NEED-001, NEED-002, CON-001, CON-002, DEC-002

- **REQ-003**: When `workflow.auto_next` is `true` and `specify` has reached its Completion step — i.e., all discovery criteria are met and the user has explicitly confirmed the **final** stage summary (not each intermediate topic confirmation) — the system MUST automatically invoke `/codexspec:generate-spec <feature-dir>`.
  - Sources: NEED-002, CON-001, DEC-001

- **REQ-004**: When a generation command's review Overall Status is `NEEDS_REVISION` or `BLOCKED`, the system MUST NOT auto-invoke the next command; control MUST return to the user, regardless of `workflow.auto_next`.
  - Sources: CON-002

- **REQ-005**: The system MUST emit a single one-line transparency notice immediately before auto-invoking the next command (e.g. `auto_next: review passed → invoking /codexspec:spec-to-plan`), written in the interaction language (`language.interaction`).
  - Sources: DEC-004

- **REQ-006**: When `workflow.auto_next` is absent or `false`, the system MUST preserve existing behavior — each command ends and the next is triggered manually by the user.
  - Sources: CON-003

- **REQ-007**: `implement-tasks` MUST be the terminal stage of the auto-next chain; after it completes, nothing is auto-invoked.
  - Sources: NEED-002, OUT-001

- **REQ-008**: With `workflow.auto_next` enabled, after `plan-to-tasks` passes, the existing `/codexspec:analyze` auto-invocation MUST still run exactly once (read-only) before `implement-tasks`; `analyze`'s findings MUST NOT block the auto-invocation of `implement-tasks`.
  - Sources: CON-005

- **REQ-009**: The transition into `implement-tasks` MUST proceed automatically without any confirmation prompt when `workflow.auto_next` is `true` and `plan-to-tasks` has passed.
  - Sources: DEC-001

- **REQ-010**: The auto-next behavior MUST be implemented as a conditional section added to each affected distributed command template that, when `workflow.auto_next` is `true` and the stage has passed, invokes the next slash command — mirroring the existing "Automatic Cross-Artifact Analysis" conditional auto-invoke pattern already present in `plan-to-tasks.md`.
  - Sources: DEC-003

### Non-Functional Requirements

- **NFR-001** (Backwards compatibility): The feature MUST be opt-in. Projects without a `workflow.auto_next` key, or with it set to anything other than literal `true`, MUST behave identically to the current product.
  - Sources: CON-003

- **NFR-002** (Config convention): The key MUST be snake_case and grouped under a thematic `workflow` section, consistent with the existing `git.branch_check_enabled` toggle.
  - Sources: CON-004

- **NFR-003** (Uniformity): A single global boolean MUST govern all transitions uniformly; per-transition configuration is excluded.
  - Sources: CON-004, OUT-002

- **NFR-004** (Observability): Every auto-advancement MUST be observable via the one-line notice (REQ-005), so a hands-off run remains auditable.
  - Sources: DEC-004

## Constraints

- **Source-of-truth location**: Distributed command changes MUST be made in `templates/commands/` (`specify.md`, `generate-spec.md`, `spec-to-plan.md`, `plan-to-tasks.md`). The `.claude/commands/codexspec/` copies are self-bootstrap install artifacts and MUST NOT be edited directly — they are regenerated from `templates/commands/` on reinstall. (Project constitution / repository-layout fact; reinforces DEC-003 and REQ-010.)
- **Default off**: `workflow.auto_next` defaults to `false` (CON-003).
- **Single boolean**: No per-step or per-transition switches in this iteration (CON-004, OUT-002).
- **analyze is non-gating**: `analyze` findings never block `implement-tasks` (CON-005).
- **Quality gate reused**: Advancement uses each command's existing review-loop verdict; no new gate is introduced (CON-001, CON-002).

## Decisions (preserved from requirements.md)

- **DEC-001**: Fully automatic; no confirmation prompt before `implement-tasks`. Risk is mitigated by the per-stage review gates.
- **DEC-002**: Advancement threshold is `PASS` or `PASS_WITH_WARNINGS` (not strict `PASS`).
- **DEC-003**: Implemented as a conditional auto-invoke section in each affected command template, reusing the `plan-to-tasks → analyze` precedent (#17).
- **DEC-004**: A one-line transparency notice is emitted before each auto-invocation.

## Success Criteria

- **SC-001**: With `workflow.auto_next: true`, a feature flows from a confirmed `specify` through `implement-tasks` with zero manual `/codexspec:*` invocations between stages (other than the initial `specify`).
- **SC-002**: With `workflow.auto_next` absent or `false`, the pipeline is behaviorally equivalent to the current product (no auto-invocations).
- **SC-003**: A `NEEDS_REVISION` or `BLOCKED` review verdict halts the chain 100% of the time, regardless of the `auto_next` setting.
- **SC-004**: Every auto-advancement is preceded by exactly one observable notice line.

## Out of Scope

- **OUT-001**: Optional/helper commands (`clarify`, `checklist`, `tasks-to-issues`) are never auto-invoked by `auto_next`. `review-code` already runs inside `implement-tasks` and is not a separate auto-next hop.
- **OUT-002**: No per-transition / per-step configuration. `workflow.auto_next` is all-or-nothing in this iteration.

## Assumptions

- **A1**: A non-boolean or unrecognized value for `workflow.auto_next` (e.g. `"yes"`, `1`, `null`) is treated as **not enabled** (`false`), consistent with the opt-in / default-off semantics in CON-003. Only literal `true` enables auto-advance. This is a parsing-robustness assumption, not a product decision; it does not expand scope.

## Dependencies

- The existing Automatic Review Loop in `generate-spec`, `spec-to-plan`, and `plan-to-tasks` (which produces the `PASS` / `PASS_WITH_WARNINGS` / `NEEDS_REVISION` / `BLOCKED` verdict).
- The existing "Automatic Cross-Artifact Analysis" section in `plan-to-tasks.md` (the pattern to mirror).
- The config-reading convention already used by command templates ("Read `.codexspec/config.yml`") and the `git.main_branches` / `git.branch_check_enabled` grouping precedent.

## Requirements Traceability

| Confirmed Requirement | Spec Coverage | Notes |
|---|---|---|
| NEED-001 | REQ-001, REQ-002 | Core auto-advance behavior |
| NEED-002 | REQ-002, REQ-003, REQ-007 | Full chain coverage; implement-tasks terminal |
| CON-001 | REQ-002, REQ-003 | Two distinct pass gates |
| CON-002 | REQ-002, REQ-004 | Stop on NEEDS_REVISION / BLOCKED |
| CON-003 | REQ-001, REQ-006, NFR-001 | Default false, opt-in, backwards compatible |
| CON-004 | REQ-001, NFR-002, NFR-003 | Single global boolean under `workflow` |
| CON-005 | REQ-008 | analyze non-blocking |
| DEC-001 | REQ-003, REQ-009 | No confirm before implement-tasks |
| DEC-002 | REQ-002 | PASS_WITH_WARNINGS counts |
| DEC-003 | REQ-010, Constraints | Conditional section in `templates/commands/` |
| DEC-004 | REQ-005, NFR-004 | One-line transparency notice |
| OUT-001 | REQ-007, Out of Scope | Helpers not in chain |
| OUT-002 | NFR-003, Out of Scope | No per-transition config |
