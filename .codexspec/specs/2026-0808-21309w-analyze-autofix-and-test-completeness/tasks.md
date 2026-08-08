# Tasks: analyze-autofix-and-test-completeness

**Related Plan**: `plan.md`
**Confirmed Requirements**: `requirements.md`
**Spec**: `spec.md`
**Created**: 2026-08-08

Task types: template edits are documentation-like (direct edit + deterministic
content checks); `T004` (pytest contract tests) is code (TDD applies). All edits
are made in `templates/commands/` source only; derived forms are regenerated, never
hand-edited (CON-005 / NFR-002).

---

## Group 1 — `analyze` auto-remediation (Plan Design A / Phase 1)

### T001 — Rewrite `analyze.md` to a detect + auto-remediation model

- **Covers**: REQ-001, REQ-002, REQ-003, REQ-004, REQ-005, REQ-006, NFR-001; Plan: Design A / Phase 1
- **Path**: `templates/commands/analyze.md`
- **Outcome**: `analyze` is no longer read-only; it auto-applies deterministic,
  authority-directed remediations, bounded by the requirements-as-truth model.
- **Details**:
  - Replace the `## Operating Constraints` "This command is read-only. Do not
    modify artifacts." with an auto-remediation operating model (REQ-001, REQ-003).
  - State `requirements.md` is the source of truth and is **never** modified; all
    fixes conform `spec`/`plan`/`tasks` to it; direction follows the authority
    hierarchy (REQ-002, NFR-001).
  - **Completeness**: auto-add missing downstream coverage; preserve non-conflicting
    derived detail (REQ-004). **Consistency**: act only on conflicts; conform the
    unauthorized/lower side with the minimal change; no conflict → no action (REQ-005).
  - Add the PLD-5 tie-break (nearest common upstream; report the pathological
    ungrounded-mutual-conflict without gating).
  - Keep it artifact-only (no `tasks → code`, REQ-006) and preserve the literal
    markers `requirements.md` and "end-to-end traceability".
- **Verification**: deterministic content check (see T004 assertions for analyze).
- **Dependencies**: none.

---

## Group 2 — `plan-to-tasks` front-load + analyze ripple (Plan Design B / Phase 2)

### T002 — Add scenario enumeration and update the analyze description in `plan-to-tasks.md`

- **Covers**: REQ-003, REQ-007, REQ-008, REQ-009, REQ-010, CON-003, CON-004, DEC-004, DEC-005; Plan: Design B / Phase 2
- **Path**: `templates/commands/plan-to-tasks.md`
- **Outcome**: `plan-to-tasks` mandates explicit, traceable test scenarios for
  every testable task, and its description of `analyze` reflects auto-remediation.
- **Details**:
  - **Task Rules**: every testable task must carry an individually identifiable
    **Test Scenarios** list (happy path + behavior-implied boundary/error), derived
    from `spec` acceptance criteria / covered requirement behavior (expand, never
    invent); non-testable tasks keep deterministic verification; no padding
    (REQ-007, REQ-008, REQ-009, CON-003, DEC-004, DEC-005).
  - **Required Output**: per-testable-task scenarios; coverage table gains a
    scenario↔task column (REQ-010, CON-004).
  - **Pre-Save Validation**: add the scenario-sufficiency + traceability +
    stop-on-underspecified check (REQ-009, REQ-010).
  - **Automatic Cross-Artifact Analysis** section: change the `analyze` description
    from "read-only / informational / do not auto-fix its findings" to
    "auto-remediates deterministically, runs once, still non-blocking for
    implement-tasks, no re-review loop"; keep the section name and its position
    **before** "Auto-Next Chain Advance" (REQ-003, PLD-3).
  - **Preserve test-guarded phrases** in this file (asserted by
    `test_plan_to_tasks_auto_next_runs_after_analyze_and_is_nonblocking`): the exact
    strings `do NOT block this advance` and `no confirmation prompt` must remain
    (analyze's auto-fixes are still non-blocking and the jump to implement-tasks
    still needs no confirmation). Reword "informational only" without dropping them.
- **Verification**: deterministic content check (see T004 assertions for plan-to-tasks).
- **Dependencies**: none (independent file from T001; `[P]` with T001, T003).

---

## Group 3 — `implement-tasks` back-load (Plan Design C / Phase 3)

### T003 — Add a Scenario Coverage Self-Check to `implement-tasks.md` §7

- **Covers**: REQ-011, REQ-012, REQ-013; Plan: Design C / Phase 3
- **Path**: `templates/commands/implement-tasks.md`
- **Outcome**: before reporting success, `implement-tasks` self-verifies that every
  enumerated scenario in `tasks.md` maps to a genuine, asserting test.
- **Details**:
  - Add a "Scenario Coverage Self-Check" step inside `## 7. Final Code Review Loop`:
    read `tasks.md` scenarios; a scenario with no covering test, or covered only by
    a hollow/non-asserting test (operational rule: the test must assert the
    scenario's expected outcome), is a blocking obligation (REQ-011).
  - Route gaps through the existing repair path 7.4–7.6 (red-green add test →
    fresh re-review → terminal status); success impossible while any scenario is
    uncovered (REQ-012).
  - Do **not** extend `review-code`, add a command, or add to `analyze`; keep the
    command terminal (no Auto-Next section) (REQ-013).
- **Verification**: deterministic content check (see T004 assertions for implement-tasks).
- **Dependencies**: none (independent file; `[P]` with T001, T002).

---

## Group 4 — Contract tests (Plan Phase 4)

### T004 — Extend `tests/test_sdd_workflow_templates.py` with contract assertions

- **Covers**: REQ-001..REQ-013, NFR-001, SC-001..SC-005; Plan: Phase 4
- **Path**: `tests/test_sdd_workflow_templates.py`
- **Outcome**: new contract tests encode the new behaviors; all existing assertions
  (analyze markers, implement-tasks §7 gate/terminal, plan-to-tasks ordering,
  cross-form sync) stay green.
- **Test Scenarios** (individually identifiable; incl. boundary/error):
  - **TS-1 (analyze, auto-fix)**: `analyze.md` no longer asserts "read-only" and
    states it auto-applies/repairs remediations. (REQ-001, REQ-003)
  - **TS-2 (analyze, never-modify-requirements — critical boundary)**: `analyze.md`
    states `requirements.md` is the source of truth and is never modified. (REQ-002)
  - **TS-3 (analyze, conflict-only)**: `analyze.md` describes completeness
    (preserve non-conflicting detail) and consistency (act only on conflicts).
    (REQ-004, REQ-005)
  - **TS-4 (analyze, markers preserved)**: `analyze.md` still contains
    `requirements.md` and "end-to-end traceability". (REQ-006, regression guard)
  - **TS-5 (plan-to-tasks, scenarios mandated)**: `plan-to-tasks.md` requires test
    scenarios for testable tasks (e.g. a "Test Scenarios" marker + boundary/error).
    (REQ-007, DEC-004)
  - **TS-6 (plan-to-tasks, testable-only — boundary)**: enumeration is scoped to
    testable tasks; non-testable tasks keep deterministic verification. (REQ-008)
  - **TS-7 (plan-to-tasks, derive-not-invent)**: scenarios derive from
    spec/requirement behavior; stop when underspecified. (REQ-009)
  - **TS-8 (plan-to-tasks, analyze ripple + ordering)**: the section no longer
    calls analyze "read-only"; "Automatic Cross-Artifact Analysis" still precedes
    "Auto-Next Chain Advance"; the guarded strings `do NOT block this advance` and
    `no confirmation prompt` are still present. (REQ-003, PLD-3, regression guard)
  - **TS-9 (implement-tasks, self-check)**: `implement-tasks.md` contains a
    scenario-coverage self-check tied to the repair loop. (REQ-011, REQ-012)
  - **TS-10 (implement-tasks, terminal + review-code untouched — boundary)**:
    `implement-tasks.md` has no "Auto-Next Chain Advance" and still invokes
    `review-code --feature` unchanged; `review-code.md` and `review-tasks.md` are
    not modified. (REQ-013, regression guard)
  - **TS-11 (cross-form sync — drift boundary)**: new markers for the 3 commands
    appear in all three distribution forms (template, `.claude`, `.agents/skills`);
    the existing sync test still passes. (NFR-002, SC-005)
  - **TS-12 (no new command — negative)**: no new command file added under
    `templates/commands/`. (OUT-002, SC-005)
- **Dependencies**: T001, T002, T003 (assertions target their content; TDD:
  assertions may be authored first and observed red, then confirmed green).

---

## Group 5 — Sync derived distribution forms (Plan Phase 4)

### T005 — Regenerate `.claude` and `.agents/skills` forms for the 3 commands

- **Covers**: NFR-002, CON-005; Plan: PLD-1 / Phase 4
- **Command**: `codexspec init --ai both --force` (run from repo root)
- **Outcome**: `.claude/commands/codexspec/{analyze,plan-to-tasks,implement-tasks}.md`
  and `.agents/skills/codexspec-{analyze,plan-to-tasks,implement-tasks}/SKILL.md`
  regenerated to match the edited sources.
- **Details**: pass `--ai both` (not the default `claude`) so both forms regenerate;
  `project.ai` in `config.yml` is already `both`, so the field is unchanged.
- **Verification**: `git diff --stat` shows only the 3 commands' derived forms
  changed (plus the intended source edits); the cross-form sync test in T004 passes.
- **Dependencies**: T001, T002, T003.

---

## Group 6 — Full verification (Plan Verification Strategy / Phase 4)

### T006 — Run the contract suite and confirm green

- **Covers**: SC-001, SC-002, SC-003, SC-004, SC-005; Plan: Verification Strategy
- **Command**: `uv run pytest tests/test_sdd_workflow_templates.py -q` then the
  broader suite `uv run pytest -q`.
- **Outcome**: all new and preserved assertions pass; no regression.
- **Dependencies**: T004, T005.

---

## Coverage Table

| Plan item / Requirement | Task(s) |
|-------------------------|---------|
| REQ-001 | T001, T004 |
| REQ-002 | T001, T004 |
| REQ-003 | T002, T004 |
| REQ-004 | T001, T004 |
| REQ-005 | T001, T004 |
| REQ-006 | T001, T004 |
| REQ-007 | T002, T004 |
| REQ-008 | T002, T004 |
| REQ-009 | T002, T004 |
| REQ-010 | T002, T004 |
| REQ-011 | T003, T004 |
| REQ-012 | T003, T004 |
| REQ-013 | T003, T004 |
| NFR-001 | T001, T004 |
| NFR-002 | T005, T004 |
| Design A / Phase 1 | T001 |
| Design B / Phase 2 | T002 |
| Design C / Phase 3 | T003 |
| Phase 4 (tests) | T004 |
| Phase 4 (sync) | T005 |
| SC-001..005 | T004, T006 |
| PLD-1 | T005 |
| PLD-2 | T002 (no review-tasks edit) |
| PLD-3 | T002 |
| PLD-4 | T003 |
| PLD-5 | T001 |

## Dependency Summary

- T001, T002, T003 are independent (`[P]`).
- T004 depends on T001–T003.
- T005 depends on T001–T003.
- T006 depends on T004, T005.
- Acyclic; dependents ordered after dependencies.

## Unmapped Tasks

None. Every task maps to a confirmed requirement or required implementation support
(sync T005 and verification T006 are necessary support for NFR-002 and SC-*).

## Implementation Progress

- [x] **T001** — `analyze.md` rewritten to detect + auto-remediate (markers preserved).
- [x] **T002** — `plan-to-tasks.md` scenario enumeration + analyze-description ripple (guarded phrases kept).
- [x] **T003** — `implement-tasks.md` §7.3a Scenario Coverage Self-Check + 7.6 success condition.
- [x] **T004** — `tests/test_sdd_workflow_templates.py` extended (TS-1…TS-12); all pass.
- [x] **T005** — derived forms regenerated via `codexspec init . --ai both --force` (footprint: 3 commands × 3 forms; governance files untouched).
- [x] **T006** — full suite green: **1001 passed, 50 skipped** (pwsh tests skipped).

**Note**: analyze's frontmatter `description` was reverted to its original string to
avoid drifting from the `en.json` translation catalog (behavior lives in the body);
this keeps the change within the confirmed 3-template scope.

**Final gate (implement-tasks §7)**: `/codexspec:review-code --feature` under a fresh
**isolated** reviewer → `PASS` (schema 1, requirements `complete`, verification
`complete`, P0–P3 = 0, coverage gaps = 0, baseline green). Terminal status: **SUCCESS**.
