# Feature Specification: debug-command

<!--
Language: document language is English (.codexspec/config.yml → language.document: en).
Compiled from requirements.md. Only Status: confirmed entries are binding.
-->

**Feature Branch**: `2026-0811-1418yq-debug-command`
**Created**: 2026-08-11
**Status**: Draft
**Input**: Add a `/codexspec:debug` command carrying a four-phase root-cause discipline, referenced by a single conditional hook in `implement-tasks`.

## Context and Goals

CodexSpec has no systematic debugging capability. When a test fails or a defect is found, the current flow relies on ad-hoc guess-and-check. This feature adds a root-cause-first debugging discipline, delivered two ways from one definition:

- as a standalone `/codexspec:debug` command usable on-demand, and
- as a low-ceremony escalation that `implement-tasks` enters when a fix is not converging.

Goal: replace blind patching with a reproduce → root-cause → single-fix discipline, without adding a new pipeline stage, a config key, or any persistent artifact.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Standalone systematic debugging (Priority: P1)

A developer hits a bug (an error, a failing test, or unexpected behavior) and invokes `/codexspec:debug` with a free-form symptom. The command runs a four-phase root-cause discipline and returns a verified fix — refusing to propose a fix before the root cause is understood.

**Why this priority**: This is the core deliverable — the discipline itself and its on-demand entry point. It is a complete MVP on its own.

**Independent Test**: Invoke `/codexspec:debug` with a symptom; confirm it establishes a reproduction (or asks for one) before any fix, works through the four phases, and lands a single verified fix.

**Acceptance Scenarios**:

1. **Given** a failing test id passed as an argument, **When** `/codexspec:debug` runs, **Then** it reproduces the failure, investigates the root cause before proposing any fix, and applies a single fix verified green.
2. **Given** a thin symptom that cannot be reproduced as stated, **When** `/codexspec:debug` runs, **Then** it attempts reproduction and, failing that, asks for reproduction steps / expected-vs-actual / error text / onset before proposing any fix.
3. **Given** three fixes on the same problem have failed, **When** a fourth is considered, **Then** the command stops and questions the architecture instead of attempting another blind fix.

---

### User Story 2 - Escalation from implement-tasks (Priority: P2)

While `implement-tasks` is implementing or repairing, a fix is not converging. Instead of continuing to patch, it enters the same debug discipline in place, then resumes the task.

**Why this priority**: Integrates the discipline at the single point where all fixing happens (TDD + review-defect repair), preventing blind patching inside the pipeline. Depends on US1's definition.

**Independent Test**: Drive `implement-tasks` into a stuck red test (or a non-trivial correctness-defect repair) and confirm it references the debug discipline via a single `Invoke /codexspec:debug`, then resumes — with no notice ceremony and no user pause.

**Acceptance Scenarios**:

1. **Given** a TDD red test that the green loop cannot close after several attempts (or a fix that reddened a previously-passing test), **When** `implement-tasks` reaches its trip condition, **Then** it escalates into the debug discipline and, after root-cause+fix, resumes the task.
2. **Given** `implement-tasks` is repairing a non-trivial functional/correctness defect surfaced by its `review-code` call, **When** it applies the repair, **Then** it escalates into the debug discipline before patching.
3. **Given** a `review-code` finding in the idiomatic-clarity, architecture, or constitution dimension, or a trivial mechanical fix, **When** `implement-tasks` repairs it, **Then** it does NOT escalate into debug.

---

### Edge Cases

- **Thin / non-reproducible symptom** → Phase 1 reproduce-or-ask; no fix before a stable reproduction (REQ-004).
- **Flaky / non-deterministic failure** → Phase 1 must establish a stable reproduction before proceeding.
- **≥3 failed fixes** → architecture gate; stop and question the design (REQ-003).
- **Trip (b) on a non-correctness finding** (style/architecture/constitution) or a trivial fix → must NOT escalate (REQ-006).
- **Standalone `review-code` followed by a manual user fix** → no hook fires; the user invokes `/codexspec:debug` themselves if desired.
- **Debug cannot find a root cause** → returns control to the caller reporting the state; it does not silently patch.

## Requirements *(mandatory)*

### Functional Requirements

- **REQ-001**: The system MUST provide a standalone `/codexspec:debug` command that accepts a free-form symptom via `$ARGUMENTS` (plain description, error text, stack trace, or failing-test id) or reads error output already present in the session.
  - Sources: NEED-001, NEED-005
- **REQ-002**: The command MUST run a four-phase root-cause discipline: (1) Root-Cause Investigation as a hard gate — no fix may be proposed until the root cause is understood (read the error, reproduce consistently, check recent changes, trace data flow backward); (2) Pattern Analysis; (3) Hypothesis & Verification — a single written hypothesis, one variable changed at a time, verified; (4) Fix — a failing test written first, a single fix applied, verified without breaking other tests.
  - Sources: NEED-002
- **REQ-003**: After ≥3 failed fixes on the same problem, the command MUST stop and question the architecture rather than attempt a fourth blind fix.
  - Sources: NEED-002
- **REQ-004**: When the symptom is insufficient to reproduce, Phase 1 MUST reproduce-or-ask — attempt reproduction, or request reproduction steps / expected-vs-actual / error text / onset — before proposing any fix.
  - Sources: NEED-005
- **REQ-005**: `implement-tasks` MUST carry exactly one conditional, reference-style escalation into debug, firing on either trip condition — (a) the TDD green loop cannot close a red test after several attempts, a fix breaks a previously-passing test, or guess-and-check is detected (§3 TDD Workflow); (b) while repairing a non-trivial functional/correctness defect surfaced by its own `review-code` call (§7.4 Apply Test-Safe Repairs) — and MUST explicitly resume the task on completion.
  - Sources: NEED-003, DEC-001, DEC-003
- **REQ-006**: Trip condition (b) MUST be limited to functional/correctness (or robustness) defects whose fix is non-trivial (requires tracing across call chains, state, or data flow — not a mechanical local edit). It MUST NOT trigger for idiomatic-clarity, architecture, constitution-alignment, style, or trivial mechanical fixes. `review-code` MUST remain strictly review-only and MUST NOT be modified by this feature.
  - Sources: CON-003, DEC-003

### Non-Functional Requirements

- **NFR-001**: The discipline MUST be authored exactly once in `templates/commands/debug.md`. The `implement-tasks` hook MUST reach it via the single existing command-to-command primitive — a `Invoke /codexspec:debug` line (the same verb as `review-spec`/`review-plan`/`review-tasks`) — and MUST NOT duplicate the discipline text.
  - Sources: NEED-004, CON-001
- **NFR-002**: The hook MUST be conditional (`IF <trip>`), non-gating (produce no PASS/FAIL that gates the chain), and low-ceremony (no forced notice line, no user pause); "return" MUST be an explicit written resume instruction, since there is no runtime stack.
  - Sources: CON-002
- **NFR-003**: The feature MUST NOT add `workflow.auto_debug` or any new configuration key.
  - Sources: DEC-002
- **NFR-004**: `debug` MUST NOT create any persistent artifact — no SDD artifact and no debug trace/journal file. Reusable root causes are captured through the existing `distill` → `.codexspec/profile/pitfalls.md` channel, which is not modified.
  - Sources: CON-005
- **NFR-005**: All changes MUST be made under `templates/commands/` (a new `debug.md` and edits to `implement-tasks.md`); derived artifacts (`.claude/commands/`, `.agents/skills/`) are regenerated via publish → `codexspec init`; templates MUST be authored in English with a `## Language Preference` section.
  - Sources: CON-004

### Open Questions (non-blocking)

- **OPEN-001**: The exact `debug.md` template skeleton (frontmatter / section layout) is not finalized. Suggested starting point: frontmatter `description` + `argument-hint` + `allowed-tools`; sections `## Language Preference` → `## User Input` → `## Role and Iron Law` → `## Symptom Intake` → `## Investigation Protocol` (Phase 1–4 + Architecture Gate as `###` subsections) → `## Completion`.

> This open item is a design detail resolved during planning/implementation. It does NOT block downstream work and MUST NOT be rewritten as a confirmed requirement.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: The four-phase discipline appears in exactly one file (`templates/commands/debug.md`); no copy of the protocol exists in `implement-tasks.md` (verifiable by inspection/test).
- **SC-002**: `implement-tasks.md` references debug through a single `Invoke /codexspec:debug` and contains an explicit resume instruction (verifiable in template text and template tests).
- **SC-003**: No new configuration key is introduced (config schema and `.codexspec/config.yml` unchanged for this feature); `debug` creates no new persistent artifact type.
- **SC-004**: `templates/commands/review-code.md` is unchanged by this feature.
- **SC-005**: Given a thin symptom, standalone `/codexspec:debug` asks for reproduction (or reproduces) before proposing a fix (verifiable via the command instructions / an eval case).

## Out of Scope

- **OUT-001**: Making `debug` a mandatory/dedicated pipeline stage inserted into `specify → … → implement-tasks`. Reason: debug is reached only conditionally (the hook) or on-demand (standalone).
- Attaching the escalation to any command other than `implement-tasks` (including `review-code`). Reason: `implement-tasks` is the single locus of all fixing.
- A debug trace/journal file or root-cause note. Reason: non-automatic persistence is low value; reusable knowledge flows through `distill`.
- A `workflow.auto_debug` or any config gate. Reason: strictly-better default behavior needs no opt-out.
- Metric/eval-driven prompt or discipline optimization. Reason: out of scope for v1.

## Assumptions

- `implement-tasks.md` retains its current structure: a TDD workflow (§3, Red→Green→Refactor) and a Final Code Review Loop that calls `review-code` and applies test-safe repairs (§7.4). The two trip points attach at these locations.
- `review-code` remains a strict review-only defect gate whose findings are repaired by the outer caller.

## Dependencies

- Existing `templates/commands/implement-tasks.md` (§3 TDD; §6–7 review loop; §7.4 test-safe repairs) — edited to add the hook.
- Existing `distill` → `.codexspec/profile/pitfalls.md` channel — the persistence path for reusable root causes (referenced, not modified).
- Existing `templates/commands/review-code.md` — unmodified, review-only.
- Release tail (per NFR-005): derived-artifact regeneration via publish → `codexspec init`, installer registration of the new command, and README updates.

## Requirements Traceability

| Confirmed Requirement | Spec Coverage | Notes |
|-----------------------|---------------|-------|
| NEED-001 | REQ-001; US1 | Standalone command + intake |
| NEED-002 | REQ-002, REQ-003; US1 | Four-phase discipline + architecture gate |
| NEED-003 | REQ-005; US2 | Single implement-tasks hook, two trips, resume |
| NEED-004 | NFR-001 | DRY: one definition, referenced |
| NEED-005 | REQ-001, REQ-004 | Free-form intake + reproduce-or-ask |
| CON-001 | NFR-001 | Single `Invoke` handoff primitive |
| CON-002 | NFR-002 | Conditional / non-gating / low-ceremony / explicit resume |
| CON-003 | REQ-006 | Trip (b) narrowed; review-code review-only |
| CON-004 | NFR-005 | Self-bootstrap governance |
| CON-005 | NFR-004; Out of Scope | No persistent artifact |
| DEC-001 | REQ-005, NFR-002 | Reference-style handoff |
| DEC-002 | NFR-003; Out of Scope | No `auto_debug` key |
| DEC-003 | REQ-005, REQ-006 | Attach surface = implement-tasks only |
| OUT-001 | Out of Scope | Not a mandatory pipeline stage |
| OPEN-001 | Open Questions | `debug.md` skeleton, non-blocking |
