# Feature Specification: plan-to-tasks-auto-analyze

<!--
Language: Generate this document in the language specified in .codexspec/config.yml
If not configured, use English.
-->

**Feature Branch**: `2026-0629-1337a7-plan-to-tasks-auto-analyze`
**Created**: 2026-06-29
**Status**: Draft
**Input**: `.codexspec/specs/2026-0629-1337a7-plan-to-tasks-auto-analyze` (compiled from `requirements.md`)

## Context

CodexSpec's `plan-to-tasks` command already ends with an **Automatic Review Loop**: after generating `tasks.md` it invokes `/codexspec:review-tasks`, auto-fixes defects whose corrections are deterministic, and runs at most two fix-and-review rounds. `review-tasks` reports an Overall Status of `PASS`, `PASS_WITH_WARNINGS`, `NEEDS_REVISION`, or `BLOCKED`, and the loop stops early when defects repeat, remain unresolved, or require a user or architecture decision.

A separate command, `/codexspec:analyze`, performs a read-only, end-to-end traceability and consistency check across `requirements.md` → `spec.md` → `plan.md` → `tasks.md`. Today, after `plan-to-tasks` finishes its review loop, the user must remember to run `/codexspec:analyze` manually to get this cross-artifact check before implementation.

This feature closes that gap: when the review loop concludes in a passing state, `plan-to-tasks` automatically invokes `/codexspec:analyze` once, removing the manual step. The analyze result remains purely informational — it does not add a new gate before implementation.

## Goals

- Remove the manual `/codexspec:analyze` step after successful task generation.
- Surface cross-artifact traceability and consistency issues at the moment tasks are produced, before implementation begins.
- Preserve analyze's role as an informational check — no new blocking gate is introduced.

## User Scenarios & Testing

This feature is a single cohesive behavior, so it is captured as one prioritized user story with multiple acceptance scenarios rather than artificially split into independently deployable stories.

### User Story 1 - Automatic cross-artifact check after task generation (Priority: P1)

As a developer running `/codexspec:plan-to-tasks`, I want the end-to-end consistency between my requirements, spec, plan, and tasks to be checked automatically once my tasks are generated and pass review, so that I do not have to remember to run `/codexspec:analyze` manually and can catch chain breaks before I start implementing.

**Why this priority**: The entire feature is this behavior; it has no subordinate slice that delivers value on its own.

**Independent Test**: Run `/codexspec:plan-to-tasks` on a feature whose review loop ends in `PASS`; observe that `/codexspec:analyze` is invoked automatically and its output appears without any manual command.

**Acceptance Scenarios**:

1. **Given** the Automatic Review Loop concludes with Overall Status `PASS`, **When** `plan-to-tasks` finishes the loop, **Then** it invokes `/codexspec:analyze` exactly once and presents analyze's own output inline.
2. **Given** the Automatic Review Loop concludes with Overall Status `PASS_WITH_WARNINGS` (Minor defects only, no Critical/Warning), **When** `plan-to-tasks` finishes the loop, **Then** it invokes `/codexspec:analyze` exactly once.
3. **Given** the Automatic Review Loop stops at `NEEDS_REVISION` or `BLOCKED`, or stops early because defects repeat, remain unresolved, or require a user/architecture decision, **When** `plan-to-tasks` stops, **Then** it does NOT invoke `/codexspec:analyze`, and control returns to the user exactly as it does today.
4. **Given** `requirements.md` is absent (legacy compatibility mode), **When** the review loop concludes in a passing state, **Then** `plan-to-tasks` still invokes `/codexspec:analyze` once, and the analyze output discloses that the analysis starts at `spec.md` and cannot verify fidelity to the original discussion.
5. **Given** the auto-invoked analyze reports Critical cross-artifact defects, **When** its output is presented, **Then** tasks are still considered ready for implementation (tasks passing the review loop remains the readiness signal) and no new gate blocks `/codexspec:implement-tasks`.

### Edge Cases & Expected Error Behavior

- **Non-passing review**: If the review loop's terminal status is `NEEDS_REVISION` or `BLOCKED`, or the loop stops early, analyze is not invoked at all. There is no error; the existing hand-back-to-user behavior is unchanged.
- **Legacy mode**: With no `requirements.md`, analyze still runs but explicitly discloses its limitation. This is expected behavior, not an error.
- **analyze finds zero defects**: Valid result; analyze reports zero defects and the flow completes normally.
- **analyze finds Critical defects**: Reported inline only. Per the informational role, these do not block implementation and are not auto-fixed.

## Requirements

### Functional Requirements

- **REQ-001**: After generating `tasks.md` and completing its existing Automatic Review Loop, the `plan-to-tasks` command MUST automatically invoke `/codexspec:analyze` exactly once.
  - Sources: NEED-001, DEC-001
- **REQ-002**: The command MUST invoke analyze only when the Automatic Review Loop concludes in a passing terminal status — `PASS` or `PASS_WITH_WARNINGS` (no Critical/Warning defects).
  - Sources: CON-001
- **REQ-003**: The command MUST NOT invoke analyze when the Automatic Review Loop stops at `NEEDS_REVISION` or `BLOCKED`, or stops early because defects repeat, remain unresolved, or require a user or architecture decision; in these cases control MUST return to the user unchanged from today.
  - Sources: CON-001
- **REQ-004**: The auto-invoked analyze MUST execute a single, read-only pass that only reports findings; the command MUST NOT auto-fix analyze findings and MUST NOT run a fix-and-reanalyze loop.
  - Sources: CON-002, OUT-002
- **REQ-005**: In legacy compatibility mode (no `requirements.md`), the command MUST still auto-invoke analyze, and the analyze output MUST disclose that the analysis starts at `spec.md` and cannot verify fidelity to the original discussion.
  - Sources: CON-005

### Non-Functional Requirements

- **NFR-001**: The auto-analyze step MUST be always enabled; it MUST NOT be gated behind a configuration key or command-line flag.
  - Sources: CON-004
- **NFR-002**: The command's Output Summary MUST NOT be modified to summarize analyze; analyze's own inline output is the sole report surfaced to the user.
  - Sources: DEC-002
- **NFR-003**: The auto-invoked analyze MUST NOT persist a report file to disk.
  - Sources: DEC-003, OUT-005
- **NFR-004**: analyze's results MUST be purely informational: they MUST NOT change whether tasks are considered ready for implementation, MUST NOT introduce a new gate before `/codexspec:implement-tasks`, and the command MUST NOT add a new explicit "next step: implement-tasks" recommendation as part of this feature.
  - Sources: CON-003, OUT-004

## Confirmed Constraints and Decisions

- **DEC-001 — Implementation location**: The change is made in `templates/commands/plan-to-tasks.md` (the source-of-truth template), by extending the existing "Automatic Review Loop" section with a "passing terminal status → invoke `/codexspec:analyze`" step. It is NOT made in `.claude/commands/codexspec/` (a self-bootstrap install artifact). Rationale: the project's Self-bootstrap / Slash Command Template Modification Rules require distributed-command edits to go through `templates/commands/` so they reach end users.

## Out of Scope

- **OUT-001**: No changes to the `review-tasks` command or its auto-fix logic — the existing review loop is taken as given.
- **OUT-002**: No fix-and-reanalyze loop for analyze (enforced by REQ-004).
- **OUT-003**: `/codexspec:analyze` is not auto-chained into any command other than `plan-to-tasks`.
- **OUT-004**: No new explicit "next step: `/codexspec:implement-tasks`" recommendation (enforced by NFR-004).
- **OUT-005**: No persisting analyze results to disk (enforced by NFR-003).

## Assumptions

- **ASMP-S1**: "Passing terminal status" is observed from the review loop's final `review-tasks` Overall Status. The loop is treated as concluding in a passing state when it did not stop early (per its existing stop conditions) and that final status is `PASS` or `PASS_WITH_WARNINGS`. This restates how the CON-001 threshold is observed; it is not a new product decision.

## Dependencies

- `/codexspec:review-tasks` — produces the terminal Overall Status that gates the analyze step.
- `/codexspec:analyze` — the command auto-invoked by this feature.
- `templates/commands/plan-to-tasks.md` — the file modified by this feature.
- The existing Automatic Review Loop behavior — assumed unchanged (see OUT-001).

## Requirements Traceability

| Confirmed Requirement | Spec Coverage | Notes |
|-----------------------|---------------|-------|
| NEED-001 | REQ-001 | Core behavior |
| CON-001 | REQ-002, REQ-003 | Trigger threshold + non-invocation cases |
| CON-002 | REQ-004 | Single read-only pass, no fix loop |
| CON-003 | NFR-004 | Purely informational, no implement gate |
| CON-004 | NFR-001 | Always-on |
| CON-005 | REQ-005 | Legacy mode still runs analyze |
| DEC-001 | Confirmed Constraints and Decisions | Template source-of-truth location |
| DEC-002 | NFR-002 | Output Summary unchanged |
| DEC-003 | NFR-003 | No report file |
| OUT-001 | Out of Scope | review-tasks unchanged |
| OUT-002 | REQ-004, Out of Scope | No analyze fix loop |
| OUT-003 | Out of Scope | Not chained into other commands |
| OUT-004 | NFR-004, Out of Scope | No implement recommendation |
| OUT-005 | NFR-003, Out of Scope | No disk persistence |

**Open items**: None blocking. All material questions were resolved during discovery; no `OPEN-*` entry is promoted to a requirement.
