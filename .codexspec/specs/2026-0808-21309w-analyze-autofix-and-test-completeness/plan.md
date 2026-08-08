# Implementation Plan: analyze-autofix-and-test-completeness

<!--
Language: Generated in the document language from .codexspec/config.yml (en).
-->

**Related Spec**: `.codexspec/specs/2026-0808-21309w-analyze-autofix-and-test-completeness/spec.md`
**Confirmed Requirements**: `.codexspec/specs/2026-0808-21309w-analyze-autofix-and-test-completeness/requirements.md`
**Created**: 2026-08-08
**Status**: Draft

## Context

CodexSpec commands are English Markdown prompt templates. The source of truth for
distributed commands is `templates/commands/*.md`; two derived distribution forms
are regenerated from it — `.claude/commands/codexspec/<cmd>.md` (slash form) and
`.agents/skills/codexspec-<cmd>/SKILL.md` ($mention form) — via `codexspec init`
(installer for the Claude form, `src/codexspec/integrations/codex.py` for the skill
form). Contract tests in `tests/test_sdd_workflow_templates.py` assert behavior on
the templates and guard cross-form sync drift.

This feature edits three command sources — `analyze.md`, `plan-to-tasks.md`,
`implement-tasks.md` — to (1) make `analyze` auto-remediate downstream artifacts,
and (2) close the test-scenario gap by enumerating scenarios in `plan-to-tasks`
and self-verifying them in `implement-tasks`.

## Goals / Non-Goals

**Goals:**

- `analyze` resolves inconsistencies by conforming downstream artifacts to
  `requirements.md` (never editing it), fully auto-applied. (REQ-001..006, NFR-001)
- `plan-to-tasks` enumerates explicit, traceable test scenarios for every testable
  task. (REQ-007..010)
- `implement-tasks` self-verifies scenario→test coverage inside its existing review
  loop before success. (REQ-011..013)

**Non-Goals:**

- No new command; `review-code.md` and `review-tasks.md` are not modified.
  (OUT-002, OUT-004, and PLD-2)
- `analyze` gains no code-level (`tasks → code`) check. (OUT-003, REQ-006)
- `requirements.md` is never modified by `analyze`. (OUT-001, REQ-002)

## Tech Stack

- **Artifacts changed**: Markdown command templates (`templates/commands/`).
- **Derived forms (regenerated, not hand-edited)**: `.claude/commands/codexspec/`,
  `.agents/skills/codexspec-*/SKILL.md`.
- **Sync path**: `codexspec init --ai both --force` (Typer CLI → installer +
  `integrations/codex.py`).
- **Verification**: `pytest` contract tests (`tests/test_sdd_workflow_templates.py`).

## Architecture Overview

Three edited sources, each regenerated into two derived forms, guarded by contract
tests. No runtime code path changes; the "logic" lives in the prompt templates.

**Covers**: REQ-001, REQ-007, REQ-011, NFR-002

```
templates/commands/{analyze,plan-to-tasks,implement-tasks}.md   (edit here)
        │  codexspec init --ai both --force
        ├─────────────► .claude/commands/codexspec/<cmd>.md      (slash form)
        └─────────────► .agents/skills/codexspec-<cmd>/SKILL.md  ($mention form)
                                   ▲
                 tests/test_sdd_workflow_templates.py guards content + sync
```

## Component Structure (files touched)

```
templates/commands/analyze.md            # REQ-001..006, NFR-001
templates/commands/plan-to-tasks.md      # REQ-007..010, + analyze-ripple REQ-003
templates/commands/implement-tasks.md    # REQ-011..013
.claude/commands/codexspec/{analyze,plan-to-tasks,implement-tasks}.md   # regenerated
.agents/skills/codexspec-{analyze,plan-to-tasks,implement-tasks}/SKILL.md # regenerated
tests/test_sdd_workflow_templates.py     # new + preserved contract assertions
```

## Design: per-template changes

### A. `analyze.md` — detect + tiered auto-remediation

- Replace the current `## Operating Constraints` "This command is read-only. Do not
  modify artifacts." with an operating model that **auto-applies** deterministic,
  authority-directed remediations. (REQ-001, REQ-003, DEC-001) — **Covers**: REQ-001, REQ-003
- State `requirements.md` is the source of truth and is **never** modified; all
  fixes conform `spec`/`plan`/`tasks` to it; fix direction follows the authority
  hierarchy. (REQ-002, NFR-001) — **Covers**: REQ-002, NFR-001
- Two dimensions:
  - **Completeness**: auto-add missing downstream coverage for uncovered upstream
    authority; **preserve** non-conflicting downstream derived detail. — **Covers**: REQ-004
  - **Consistency**: act **only on conflicts**; conform the unauthorized/lower side
    with the minimal change; no conflict → no action. — **Covers**: REQ-005
- Preserve existing detection content, incl. the literal "requirements.md" and
  "end-to-end traceability" markers (guarded by tests); keep it artifact-only, no
  `tasks → code`. — **Covers**: REQ-006
- Conflict tie-break per PLD-5.

### B. `plan-to-tasks.md` — front-load scenario enumeration (+ analyze ripple)

- **Task Rules**: every **testable** task must carry an explicit, individually
  identifiable **Test Scenarios** list (happy path + behavior-implied
  boundary/error), derived from `spec` acceptance criteria / covered requirement
  behavior (expand, never invent); non-testable tasks keep deterministic
  verification; no padding. — **Covers**: REQ-007, REQ-008, REQ-009, REQ-010, CON-003, CON-004
- **Required Output**: `tasks.md` per-testable-task scenarios; coverage table gains
  a scenario↔task column for one-to-one downstream mapping. — **Covers**: REQ-010, CON-004
- **Pre-Save Validation**: add "every testable task has sufficient, traceable
  scenarios incl. behavior-implied boundary/error; none invented beyond upstream;
  underspecified upstream triggers the existing stop condition." — **Covers**: REQ-009, REQ-010
- **Automatic Cross-Artifact Analysis** section: update the description of `analyze`
  from "read-only / informational, do not auto-fix its findings" to
  "auto-remediates deterministically, still runs once, still **non-blocking** for
  `implement-tasks`, no re-review loop" (deterministic conforming fixes need no
  re-review). Keep the section name and its position **before** "Auto-Next Chain
  Advance" (guarded by test). — **Covers**: REQ-003 (ripple), REQ-001

### C. `implement-tasks.md` — back-load scenario self-check

- Add a **Scenario Coverage Self-Check** step inside `## 7. Final Code Review Loop`
  (the implementer owns verification; `review-code` is not extended): read the
  enumerated scenarios in `tasks.md`, verify each maps to ≥1 implemented test that
  genuinely exercises and asserts it; a missing **or hollow/non-asserting** test is
  a blocking obligation. — **Covers**: REQ-011
- Route gaps through the existing repair path (7.4 add reproducing/covering test
  red-green → 7.5 fresh re-review → 7.6 terminal status): success is impossible
  while any scenario is uncovered. — **Covers**: REQ-012
- Do **not** modify `review-code`, add a command, or add to `analyze`; keep
  implement-tasks terminal (no Auto-Next). — **Covers**: REQ-013

## Decisions

### PLD-1: "Three templates" scope = 3 command sources + mandatory synced forms + tests

**Context**: SC-005 measures "only the three source templates," but the repo's
sync contract regenerates two derived forms per command, and the constitution
requires tests for new behavior.

**Decision**: The deliverable is the 3 command **sources**, their regenerated
derived forms (`.claude`, `.agents/skills`) for those same 3 commands, and
contract tests. SC-005 is evaluated at the command-source level: **no new command
file**, and `review-code.md` / `review-tasks.md` unchanged. Regenerating derived
copies via `codexspec init` is the sanctioned sync path (CON-005), not
hand-editing a derived copy.

**Rationale**: CON-005 exists precisely to describe the edit-source→sync workflow;
`test_auto_next_section_synced_across_distribution_forms` fails if derived copies
drift. Tests live in `tests/`, not `templates/commands/`, so they are not new
command files.

**Covers**: CON-005, NFR-002, OUT-002, OUT-004, SC-005
**Decision Level**: Plan-level; does not change confirmed product scope.

### PLD-2: REQ-010 "via review-tasks" needs no edit to `review-tasks.md`

**Context**: REQ-010 says enforcement happens "in Pre-Save Validation and via the
review-tasks loop," but NFR-002 restricts edits to the 3 templates.

**Decision**: `plan-to-tasks`' own Pre-Save Validation is the hard, deterministic
gate. The existing `review-tasks` pass-2 criterion — "Verification is insufficient
for an actual requirement" — already catches a testable task missing its now-
required scenarios (once REQ-007 makes enumeration a requirement and `tasks.md`
carries scenarios). No change to `review-tasks.md`.

**Rationale**: Smallest architecture; honors NFR-002 while satisfying REQ-010's
enforcement intent.

**Covers**: REQ-010, NFR-002

### PLD-3: `analyze` stays non-blocking in the chain despite auto-fixing

**Context**: `plan-to-tasks` invokes `analyze` once before `implement-tasks`; today
that call is described as read-only/informational.

**Decision**: In-chain `analyze` auto-applies its deterministic conforming fixes
but remains **non-blocking** and runs **once** (no fix-and-reanalyze loop, no new
gate before `implement-tasks`). Deterministic conforming fixes only increase
consistency, so they need no re-review; `implement-tasks`' own final gate still
runs afterward.

**Rationale**: Preserves the existing chain shape and the ordering guarded by
`test_plan_to_tasks_auto_next_runs_after_analyze_and_is_nonblocking`, while
delivering REQ-003 (auto-fix in the chain).

**Covers**: REQ-003, REQ-001

### PLD-4: Back-load self-check lives in `implement-tasks` §7, reusing the repair loop

**Context**: DEC-002 folds the completeness check into the review loop without
extending `review-code`.

**Decision**: `implement-tasks` performs the scenario self-check itself as a §7
step and treats gaps as blocking findings fed into the existing 7.4–7.6 repair /
re-review / terminal-status machinery.

**Rationale**: `implement-tasks` already "owns verification and edits"; reuses
existing blocking machinery; keeps `review-code` untouched (REQ-013).

**Covers**: REQ-011, REQ-012, REQ-013

### PLD-5: Conflict tie-break for equally-ungrounded entries

**Context**: REQ-005 conforms "the lower-authority side"; review-spec RA-1 noted
this is undefined when two conflicting entries share no adjudicating upstream.

**Decision**: Resolve by tracing both entries to their **nearest common upstream
authority** (resolves essentially all real cases). If genuinely none exists,
`analyze` leaves both untouched and **reports** the unresolved conflict in its
output (it still completes and stays non-blocking). This is a report, not a
user-decision gate — it does not reintroduce an escalation path (preserves
DEC-001) and does not invent intent (CON-002).

**Rationale**: Keeps remediation deterministic-first while giving a principled,
non-escalating fallback for a pathological edge.

**Covers**: REQ-005, CON-002, DEC-001

## Risks / Trade-offs

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Derived forms drift from edited sources | Medium | High (tests fail; users get stale commands) | Run `codexspec init --ai both --force`; sync test guards it (PLD-1) |
| Editing `analyze`'s read-only line breaks existing analyze contract markers | Low | Medium | Preserve "requirements.md" + "end-to-end traceability"; keep artifact-only |
| Updating `plan-to-tasks` analyze wording breaks ordering test | Low | Medium | Keep "Automatic Cross-Artifact Analysis" name + position before Auto-Next (PLD-3) |
| Scenario enumeration adds ceremony / padding | Medium | Low | Anti-padding rule: only behavior-implied scenarios; testable tasks only (REQ-008, REQ-010) |
| "Hollow test" detection is judgment-based | Medium | Medium | Operational rule: test must assert the scenario's expected outcome (addresses review-spec DO-1) |

## Implementation Phases

### Phase 1: `analyze` auto-remediation

- [ ] Rewrite `## Operating Constraints` → auto-remediation model; add source-of-
      truth + never-modify-requirements; add completeness/consistency dimensions;
      add tie-break; keep artifact-only + existing markers. — **Covers**: REQ-001..006, NFR-001, PLD-5

### Phase 2: `plan-to-tasks` front-load + analyze ripple

- [ ] Add scenario enumeration to Task Rules / Required Output / Pre-Save
      Validation (testable-only, traceable, boundary/error, no padding). — **Covers**: REQ-007..010, CON-003, CON-004, DEC-004, DEC-005
- [ ] Update the "Automatic Cross-Artifact Analysis" section wording per PLD-3
      (keep name + position). — **Covers**: REQ-003, PLD-3

### Phase 3: `implement-tasks` back-load

- [ ] Add "Scenario Coverage Self-Check" step in §7 routing gaps through 7.4–7.6;
      keep review-code untouched and command terminal. — **Covers**: REQ-011..013, PLD-4

### Phase 4: Sync + tests

- [ ] Regenerate both derived forms: `codexspec init --ai both --force`. — **Covers**: NFR-002, CON-005, PLD-1
- [ ] Extend `tests/test_sdd_workflow_templates.py`: assert analyze auto-fix +
      never-modify-requirements + conflict-only; plan-to-tasks scenario
      enumeration; implement-tasks scenario self-check; keep all existing
      assertions and the cross-form sync test green. — **Covers**: REQ-001..013, NFR-001, SC-001..005

## Verification Strategy

- **Automated**: `uv run pytest tests/test_sdd_workflow_templates.py -q` (plus the
  broader suite) — all existing assertions stay green; new assertions encode
  REQ-001..013 and the SC-* outcomes; the cross-form sync test proves derived
  forms match sources (SC-005 at command-source granularity).
- **Contract markers preserved**: analyze "requirements.md" / "end-to-end
  traceability"; implement-tasks §7 gate/envelope/topology/progress-guards/TDD;
  implement-tasks terminal (no Auto-Next); plan-to-tasks Covers + analyze/auto-next
  ordering.
- **Manual/agent spot check**: run `/codexspec:analyze` on a workspace with a
  seeded deterministic inconsistency (SC-001/002) and `/codexspec:plan-to-tasks`
  on a testable plan (SC-003); confirm behavior matches the acceptance scenarios.

## Requirements Coverage

| Spec Requirement | Plan Coverage | Reference |
|------------------|---------------|-----------|
| REQ-001 | Full | Design A / Phase 1 |
| REQ-002 | Full | Design A / Phase 1 |
| REQ-003 | Full | Design A + B (PLD-3) / Phases 1–2 |
| REQ-004 | Full | Design A / Phase 1 |
| REQ-005 | Full | Design A + PLD-5 / Phase 1 |
| REQ-006 | Full | Design A / Phase 1 |
| REQ-007 | Full | Design B / Phase 2 |
| REQ-008 | Full | Design B / Phase 2 |
| REQ-009 | Full | Design B / Phase 2 |
| REQ-010 | Full | Design B + PLD-2 / Phase 2 |
| REQ-011 | Full | Design C / Phase 3 |
| REQ-012 | Full | Design C / Phase 3 |
| REQ-013 | Full | Design C (PLD-4) / Phase 3 |
| NFR-001 | Full | Design A / Phase 1 |
| NFR-002 | Full | PLD-1 / Phase 4 |
| SC-001..005 | Full | Verification Strategy / Phase 4 |
