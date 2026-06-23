# Feature Specification: implement-tasks → review-code auto-review loop

<!--
Language: Generate this document in the language specified in .codexspec/config.yml
If not configured, use English.
-->

**Feature Branch**: `2026-0623-1658cw-implement-tasks-code-review`
**Created**: 2026-06-23
**Status**: Draft
**Input**: User description: "将 /codexspec:implement-tasks 命令也衔接上 /codexspec:review-code 进行代码的auto review和auto fix，来确保最终代码实现的质量"

## Context

CodexSpec's three artifact-generation commands each end with an **Automatic Review Loop**: after saving the artifact, they invoke the matching `/codexspec:review-*` command and automatically fix verified defects (bounded to two rounds), mirroring the pattern in `generate-spec` (→ `review-spec`), `spec-to-plan` (→ `review-plan`), and `plan-to-tasks` (→ `review-tasks`).

`/codexspec:implement-tasks` is the implementation step — the last quality gate before code reaches the user. It currently has **no** equivalent review loop: it executes the TDD workflow per task, commits, and reports completion. Defects in the generated code therefore reach the user unchecked, unlike the spec/plan/tasks artifacts.

This feature closes that gap by chaining `/codexspec:implement-tasks` to `/codexspec:review-code` for an automatic code review and test-safe auto-fix of the final implementation.

The "system" in this specification is the behavior of the `/codexspec:implement-tasks` slash-command template (`templates/commands/implement-tasks.md`). The change is purely behavioral template content; it introduces no new CLI command, no new package code, and no new configuration keys.

## Goals

- Add an end-of-run automatic review-and-fix loop to `/codexspec:implement-tasks` that invokes `/codexspec:review-code` on the code produced by the current implementation.
- Make that loop consistent with the existing spec/plan/tasks review loops (invocation, auto-fix scope, two-round bound, stop conditions).
- Make code auto-fix **test-safe by construction**, so the loop can never ship a regression or a fix that breaks tests.
- Keep the loop focused on code quality grounded in the project's constitution and confirmed requirements, avoiding subjective or stylistic churn.

## Non-Goals

- Per-task (incremental) `review-code` invocation — review happens once, after all tasks are implemented (see Out of Scope).
- Reviewing pre-existing or unchanged code — only the current implementation's diff is reviewed.
- Reviewing pure documentation, configuration, or asset changes with `review-code`.
- Auto-fixing LOW (suggestion) findings.
- Any change to the CLI (`src/codexspec/`), configuration schema, or other slash commands.

## User Scenarios

### Scenario 1 — Clean implementation (happy path)

- **Given** all tasks in `tasks.md` have been implemented and the test suite is green,
- **When** `implement-tasks` reaches the end of the run,
- **Then** it invokes `/codexspec:review-code` on the analyzable code files changed by this implementation (diff versus the feature-branch base, including test code),
- **And** any CRITICAL/HIGH/MEDIUM defects are auto-fixed test-safely, changes are committed, and the run reports success with the review outcome (scores, fixed items, deferred items).

### Scenario 2 — Implementation diff has no analyzable code

- **Given** the implementation produced only non-code changes (docs, config, assets),
- **When** the loop evaluates the review target,
- **Then** it reports "no code to review", skips the loop, and completes normally (no failure).

### Scenario 3 — Refactor that breaks tests is treated as an incorrect change

- **Given** a non-functional (refactor) finding is being auto-fixed,
- **When** applying the change turns any test red,
- **Then** the command reverts that change, confirms the suite is green again, and re-attempts the refactor; the broken change is never shipped and never silently skipped.

### Scenario 4 — Functional defect is fixed via TDD

- **Given** a functional finding (logic / correctness / security),
- **When** it is auto-fixed,
- **Then** a failing test reproducing the defect is added (red), the fix is applied (green), and any refactor keeps tests green; the finding is resolved only when the reproducing test passes.

### Scenario 5 — Ungrounded MEDIUM finding is reported only

- **Given** a MEDIUM finding that is not grounded in `.codexspec/memory/constitution.md` and the confirmed requirements/spec, or that is purely stylistic,
- **When** the loop processes it,
- **Then** it is reported only and is not auto-fixed.

### Scenario 6 — Residual high-severity defects after the round limit

- **Given** CRITICAL or HIGH defects remain unresolved after the maximum number of rounds,
- **When** the loop terminates,
- **Then** the command reports a "needs work" status and does NOT claim success.

## Requirements

### Functional Requirements

- **REQ-001**: After all tasks in `tasks.md` have been implemented, `/codexspec:implement-tasks` MUST invoke `/codexspec:review-code` on the code produced by this implementation (this run's diff versus the feature-branch base, including test code) and run an automatic review-and-fix loop.
  - Sources: NEED-001, CON-001, CON-002

- **REQ-002**: The review target MUST be limited to analyzable source files (e.g. `.py`, `.ts`, `.go`, `.rs`, …) within this implementation's diff. Pure documentation, configuration, and asset files MUST be excluded. If the diff contains no analyzable code, the command MUST skip the loop, report "no code to review", and complete normally.
  - Sources: CON-002, CON-003

- **REQ-003**: Auto-fix MUST cover only CRITICAL, HIGH, and MEDIUM findings. LOW (suggestion) findings MUST be reported only and never auto-fixed.
  - Sources: CON-004

- **REQ-004**: A MEDIUM finding MUST be auto-fixed only when it is grounded in `.codexspec/memory/constitution.md` and the confirmed requirements/spec, and it concerns maintainability, readability, or testability. Ungrounded or purely stylistic MEDIUM findings MUST be reported only.
  - Sources: DEC-001

- **REQ-005**: For functional findings (logic, correctness, security), auto-fix MUST follow TDD — add a failing test that reproduces the defect, apply the fix until that test passes, then refactor while tests stay green. The finding is resolved only when the reproducing test is green.
  - Sources: DEC-002

- **REQ-006**: For non-functional findings (refactors for maintainability, readability, testability), auto-fix MUST preserve behavior: tests MUST be run before and after the change. If a change breaks any test, the command MUST treat it as an incorrect change — revert it, confirm the suite returns to green, and re-attempt. A fix MUST NOT be shipped with failing tests and MUST NOT be silently skipped.
  - Sources: DEC-002

- **REQ-007**: The automatic review-and-fix loop MUST run at most two fix-and-review rounds. It MUST stop when a defect repeats, remains unresolved, or requires a user/architecture decision. It MUST NOT auto-fix advisories or design opportunities, and MUST NOT introduce a new product decision during auto-fix. The per-fix TDD retry (REQ-005/REQ-006) occurs within a round; the two-round limit bounds overall effort.
  - Sources: DEC-003

- **REQ-008**: Changes produced by the auto-fix loop MUST be committed before the command reports completion, consistent with `implement-tasks`' existing incremental-commit behavior.
  - Sources: DEC-005

- **REQ-009**: If CRITICAL or HIGH findings remain unresolved after the maximum number of rounds, the command MUST report a "needs work" status and MUST NOT claim success. Otherwise it MUST report the review outcome (scores, items fixed, items deferred, final test status).
  - Sources: DEC-006

- **REQ-010**: The new end-of-run review loop MUST NOT remove or replace `implement-tasks`' existing per-task "Review & Refactor" step (TDD workflow step 4). It is additive.
  - Sources: DEC-004

### Non-Functional Requirements

- **NFR-001** (Consistency): The loop's invocation style, auto-fix scope rules, two-round bound, and stop conditions MUST be consistent with the existing `generate-spec` / `spec-to-plan` / `plan-to-tasks` Automatic Review Loops.
  - Sources: DEC-003, NEED-001

- **NFR-002** (Cost bound): The loop MUST run exactly once at end of run, scoped to the current implementation's analyzable code only — never the whole repository and never per task.
  - Sources: CON-001, CON-002, DEC-003

- **NFR-003** (Safety): No auto-fix may land that turns the test suite red, and residual high-severity defects MUST NOT be masked as success.
  - Sources: DEC-002, DEC-006

## Confirmed Constraints

- **Timing**: `review-code` runs once, after ALL tasks are implemented — not per task (CON-001).
- **Scope**: Only the current implementation's diff (vs the feature-branch base), including test code; pre-existing/unchanged code is not reviewed (CON-002).
- **Non-code exclusion**: Only analyzable source files are reviewed; docs/config/assets are skipped; "no code to review" is a graceful skip (CON-003).
- **Severity gate**: Auto-fix = CRITICAL + HIGH + MEDIUM; LOW is report-only (CON-004).

## Confirmed Decisions

- **DEC-001**: MEDIUM auto-fix requires grounding in constitution + confirmed requirements/spec and focus on maintainability / readability / testability.
- **DEC-002**: Auto-fix is test-safe by construction — TDD for functional defects; behavior-preserving refactors with revert-and-retry on any test breakage; unfixable items stop and report.
- **DEC-003**: Max two fix-and-review rounds; stop on repeat / unresolved / user-or-architecture decision; no advisory/design-opportunity auto-fix; no new product decisions.
- **DEC-004**: Additive to the existing per-task Review & Refactor step, not a replacement.
- **DEC-005**: Auto-fix changes are committed before completion is reported.
- **DEC-006**: Residual CRITICAL/HIGH after the round limit yields "needs work", never false success.

## Acceptance Criteria

1. Running `/codexspec:implement-tasks` on a feature that produces code changes triggers exactly one `/codexspec:review-code` invocation at end of run on the implementation's analyzable code (Scenario 1).
2. A feature whose diff has no analyzable code skips the loop with a "no code to review" report and completes normally (Scenario 2).
3. No auto-fix is committed while any test is failing; a refactor that breaks tests is reverted, the suite is confirmed green, and the refactor is re-attempted (Scenario 3).
4. Functional defects are fixed via TDD (red → green) (Scenario 4).
5. Ungrounded/stylistic MEDIUM and all LOW findings are reported only (Scenario 5; REQ-003, REQ-004).
6. The loop runs at most two rounds and stops on repeat/unresolved/decision-needed defects (REQ-007).
7. Residual CRITICAL/HIGH after the round limit produces a "needs work" status with no success claim (Scenario 6; REQ-009).
8. The existing per-task Review & Refactor step is still present and unchanged (REQ-010).

### Expected Error / Edge Behavior

- **No analyzable code in diff**: graceful skip + "no code to review" report; not an error.
- **Auto-fix breaks tests**: revert the change, restore green, retry; if it cannot be made green, treat as unresolved and stop with the evidence.
- **Defect repeats or requires a decision**: stop and report; do not loop indefinitely and do not invent a resolution.
- **Round limit reached with residual CRITICAL/HIGH**: report "needs work"; do not claim success.

## Open Questions

- **OPEN-001** *(non-blocking, deferred to plan/implementation)*: `review-code`'s frontmatter restricts `allowed-tools` to `Read, Grep, Glob` plus a specific set of linters/type-checkers. When `implement-tasks` invokes `/codexspec:review-code` mid-run, the nested-command tool-permission mechanics (whether it inherits `implement-tasks`' broader tool access or is scoped to `review-code`'s list) determine whether real static analysis can run inside the loop. This is an implementation detail and does not change the requirement intent above.

## Out of Scope

- **OUT-001**: Per-task incremental `review-code` invocation — review runs once at end of run.
- **OUT-002**: Reviewing pre-existing or unchanged code.
- **OUT-003**: Reviewing pure documentation, configuration, or asset changes with `review-code`.
- **OUT-004**: Auto-fixing LOW (suggestion) findings.
- Any change to the CLI (`src/codexspec/`), configuration schema, or other slash commands.

## Assumptions

- **A-1**: `implement-tasks` operates in a git repository so "this implementation's diff versus the feature-branch base" is well-defined. (Consistent with `implement-tasks`' existing commit behavior.) The exact diff-determination mechanism is a plan-level decision.
- **A-2**: "Analyzable code" is defined by `review-code`'s language-detection table (Python, TypeScript/JavaScript, Go, Rust, Java, Kotlin, Ruby, Shell, C/C++, C#, Swift, PHP, plus content-inferred languages). This is relied upon, not redefined here.

## Dependencies

- `/codexspec:review-code` — invoked by the new loop; its inputs (paths), severity model (CRITICAL/HIGH/MEDIUM/LOW), and rubric are consumed as-is.

## Requirements Traceability

| Confirmed Requirement | Spec Coverage | Notes |
|-----------------------|---------------|-------|
| NEED-001 | REQ-001, NFR-001 | Core goal — end-of-run review+fix loop |
| CON-001 | REQ-001, NFR-002 | Runs once at end of run |
| CON-002 | REQ-001, REQ-002, NFR-002 | Scope = this implementation's diff incl. tests |
| CON-003 | REQ-002 | Skip non-code; graceful "no code to review" |
| CON-004 | REQ-003 | Severity gate CRITICAL+HIGH+MEDIUM |
| DEC-001 | REQ-004 | MEDIUM grounding rule |
| DEC-002 | REQ-005, REQ-006, NFR-003 | Test-safe TDD-aligned auto-fix |
| DEC-003 | REQ-007, NFR-001 | Two-round bound + stop conditions |
| DEC-004 | REQ-010 | Additive, not replacing per-task step |
| DEC-005 | REQ-008 | Commit fixes before reporting |
| DEC-006 | REQ-009, NFR-003 | "needs work" on residual high-severity |
| OUT-001 | Out of Scope | No per-task review |
| OUT-002 | Out of Scope | No review of pre-existing code |
| OUT-003 | Out of Scope | No review-code on docs/config/assets |
| OUT-004 | Out of Scope | No LOW auto-fix |
| OPEN-001 | Open Questions | Nested tool-permission mechanics (non-blocking) |
