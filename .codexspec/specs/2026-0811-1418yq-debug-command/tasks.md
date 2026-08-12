# Tasks: debug-command

<!--
Language: document language is English (.codexspec/config.yml → language.document: en).
Every task: Covers: REQ-xxx; Plan: <component/phase>. Derived from plan.md; no redesign.
-->

**Feature Branch**: `2026-0811-1418yq-debug-command`

## Group A — The debug command (Plan C1)

### T-001 — Author `templates/commands/debug.md` (non-testable: template/doc)

- **Outcome**: A new command template carrying the four-phase root-cause discipline (the single definition).
- **Path**: `templates/commands/debug.md`
- **Covers**: REQ-001, REQ-002, REQ-003, REQ-004; NFR-001, NFR-004; **Plan**: C1 / Phase 1 (PLAN-DEC-001, -004, -005)
- **Dependencies**: none
- **Deterministic verification**: file exists with frontmatter (`description`, `argument-hint`, `allowed-tools: Read, Grep, Glob, Bash, Edit, Write`); sections `## Language Preference` → `## User Input` → `## Role and Iron Law` (no fix before root cause) → `## Symptom Intake` (free-form intake + reproduce-or-ask before any fix) → `## Investigation Protocol` with `### Phase 1 Root-Cause Investigation` (hard gate), `### Phase 2 Pattern Analysis`, `### Phase 3 Hypothesis & Verification`, `### Phase 4 Fix` (failing test first, or closest reproducing check for non-code symptoms — PLAN-DEC-004), `### Architecture Gate` (≥3 fixes → stop, question architecture) → `## Completion`. Instructs writing no persistent artifact (NFR-004).

## Group B — implement-tasks integration (Plan C2)

### T-002 — Add `## Systematic Debugging Escalation` to `implement-tasks.md` (non-testable: template/doc)

- **Outcome**: One escalation section plus two in-context pointers, referencing the discipline by `Invoke` (no duplication).
- **Path**: `templates/commands/implement-tasks.md`
- **Covers**: REQ-005, REQ-006; NFR-002; **Plan**: C2 / Phase 2 (PLAN-DEC-002)
- **Dependencies**: T-001 (the referenced command must exist)
- **Deterministic verification**: a `## Systematic Debugging Escalation` section exists that (a) names the two trigger points by **semantic location** (the TDD Verify/green loop; the test-safe repair of a functional defect) — not brittle section numbers; (b) states trip (a) and the narrowed trip (b); (c) issues `Invoke /codexspec:debug`; (d) declares it non-gating and low-ceremony; (e) ends with an explicit resume. Two one-line pointers added at the TDD Verify step and the §7.4 functional-defect bullet. The four-phase discipline text is NOT copied here.

## Group C — Registration & docs (Plan C3, C4)

### T-003 — Register `debug` in installer metadata (testable: Python)

- **Outcome**: `debug` appears as a distributed command; count tests updated.
- **Paths**: `src/codexspec/commands/installer.py`; `tests/commands/test_installer.py`
- **Covers**: NFR-005; **Plan**: C3 / Phase 3 (PLAN-DEC-003)
- **Dependencies**: T-001
- **Test Scenarios**:
  1. `get_commands_metadata()` includes an entry `name="debug"`, `display_name="/codexspec:debug"`, `file_name="debug.md"`, `category="enhanced"`.
  2. Total command count increased by exactly 1 versus the prior assertion.
  3. The `enhanced` category count increased by exactly 1.
  4. No duplicate `debug` entry exists.

### T-004 — Add `debug` to the command listing in all READMEs (non-testable: docs)

- **Outcome**: Each README documents the new command.
- **Paths**: `README.md`, `README.zh-CN.md`, `README.ja.md`, `README.ko.md`, `README.es.md`, `README.fr.md`, `README.de.md`, `README.pt-BR.md`
- **Covers**: NFR-005; **Plan**: C4 / Phase 4
- **Dependencies**: T-001
- **`[P]`** with T-002, T-003 (distinct files, after T-001)
- **Deterministic verification**: every listed README includes a `debug` command row consistent with the existing listing style.

## Group D — Verification (Plan Phase 5)

### T-005 — Add template-structure tests (testable: tests)

- **Outcome**: Automated tests pin the feature's structural guarantees and success criteria.
- **Path**: `tests/test_debug_template.py` (new) or extend `tests/test_sdd_workflow_templates.py`
- **Covers**: verification of REQ-001..006, NFR-001..004, SC-001..005; **Plan**: Phase 5 / Verification
- **Dependencies**: T-001, T-002
- **Test Scenarios**:
  1. `debug.md` exists and its frontmatter has `description` and `argument-hint`.
  2. `debug.md` body contains all four phases and the iron-law "no fix before root cause understood" gate. *(REQ-002)*
  3. `debug.md` contains the ≥3-fix architecture gate. *(REQ-003)*
  4. `debug.md` `## Symptom Intake` instructs reproduce-or-ask — no fix proposed before a stable reproduction is established or requested. *(REQ-004 / SC-005)*
  5. `debug.md` contains `## Language Preference`. *(CON-004/NFR-005 convention)*
  6. `implement-tasks.md` contains `## Systematic Debugging Escalation` referencing `Invoke /codexspec:debug` with an explicit resume instruction. *(REQ-005 / SC-002)*
  7. The escalation states trip (a), trip (b), and the (b) narrowing (functional/correctness or robustness + non-trivial; excludes idiomatic-clarity/architecture/constitution/style/trivial). *(REQ-006)*
  8. The four-phase discipline text does NOT appear in `implement-tasks.md` (single definition). *(NFR-001 / SC-001)*
  9. `review-code.md` contains no `/codexspec:debug` reference and is otherwise untouched by this feature. *(REQ-006 / SC-004)*
  10. No `auto_debug` key appears in the config template/handlers. *(NFR-003 / SC-003)*

### T-006 — Full-suite & lint gate (non-testable: checkpoint)

- **Outcome**: The change is green end-to-end.
- **Covers**: all; **Plan**: Phase 5
- **Dependencies**: T-001..T-005
- **Deterministic verification**: `uv run python -m pytest` passes; `uv run ruff check src/` clean.

## Dependency Summary

- T-001 → (T-002, T-003, T-004 `[P]`) → T-005 → T-006
- Acyclic; each dependency is ordered before its dependents.

## Coverage Table

| Requirement / SC | Plan | Task(s) |
|------------------|------|---------|
| REQ-001 | C1 | T-001 (verified by T-005 #1) |
| REQ-002 | C1 | T-001 (T-005 #2) |
| REQ-003 | C1 | T-001 (T-005 #3) |
| REQ-004 / SC-005 | C1 | T-001 (T-005 #4) |
| REQ-005 / SC-002 | C2 | T-002 (T-005 #6) |
| REQ-006 / SC-004 | C2 | T-002 (T-005 #7, #9) |
| NFR-001 / SC-001 | C1 | T-001, T-002 (T-005 #8) |
| NFR-002 | C2 | T-002 (T-005 #6) |
| NFR-003 / SC-003 | — | T-005 #10 |
| NFR-004 | C1 | T-001 |
| NFR-005 | C3, C4 | T-003, T-004 |

## Scenario → Task Map (testable tasks)

- **T-003**: scenarios 1–4 → `tests/commands/test_installer.py`
- **T-005**: scenarios 1–10 → `tests/test_debug_template.py`

## Unmapped Tasks

None. (Derived-artifact regeneration and version bump are the standard release tail, out of this feature's task scope per plan.)

## Implementation Status

- [x] **T-001** — `templates/commands/debug.md` authored.
- [x] **T-002** — `## Systematic Debugging Escalation` + two pointers added to `templates/commands/implement-tasks.md`.
- [x] **T-003** — `debug` registered in `installer.py`; count assertions updated (`test_installer.py`, `test_cli.py`).
- [x] **T-004** — `debug` row added to all 8 READMEs.
- [x] **T-005** — `tests/test_debug_template.py` (10 scenarios) added and passing.
- [x] **T-006** — full suite green (1064 passed, 50 skipped); `ruff check src/` clean.
