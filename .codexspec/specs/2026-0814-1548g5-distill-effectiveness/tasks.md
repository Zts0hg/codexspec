# Tasks: distill Effectiveness Upgrade

Feature: `2026-0814-1548g5-distill-effectiveness`
Derived from `plan.md` (Phases 1–5). Test scenarios trace to `spec.md` User
Stories US1–US4 acceptance scenarios. Contract-test assertions target
**emphasis-free spans** (pitfall `P-2026-0813-1606fz-1`).

---

## Phase 1 — Store core (`src/codexspec/profile.py`)

### T1.1 — Expand `PROFILE_CATEGORIES` to six + scaffold/docstrings

- Outcome: `PROFILE_CATEGORIES` = `("constraints","conventions","pitfalls","decisions","strategies","runbooks")`; module + `ensure_profile_scaffold` docstrings say "six category directories"; the two enumeration test sites updated.
- Paths: `src/codexspec/profile.py`; `tests/test_profile.py` (L21 set assertion); `tests/test_init_profile.py` (L34 docstring + scaffold loop).
- Covers: REQ-001, REQ-012, NFR-003; Plan: P1.1, P1.4.
- Dependencies: none.
- **Test Scenarios**:
  - T1.1-S1 (happy): `set(PROFILE_CATEGORIES) == {constraints, conventions, pitfalls, decisions, strategies, runbooks}`.
  - T1.1-S2 (happy): `ensure_profile_scaffold` on an empty project creates all six directories, each with a `.gitkeep`.
  - T1.1-S3 (boundary/idempotent): a second `ensure_profile_scaffold` call neither clobbers existing records nor errors.
  - T1.1-S4 (migration): a project with only the original four directories gains `strategies/` and `runbooks/` on re-scaffold, existing four untouched.
  - T1.1-S5 (ordering): `constraints` remains the first element (highest weight honored first).

### T1.2 — Rework `_PROFILE_BLOCK`: active recall + two pointers + near-moment trigger

- Outcome: rendered block (a) reframes on-demand reading into an **active recall** directive (scan `scope/when`, and `trigger` for strategies, before non-trivial work; read matching records), (b) adds `strategies/` and `runbooks/` pointers with `constraints` still the mandatory first pointer, (c) carries the terse near-moment distill trigger rule; block stays a fixed-size directive that inlines no records.
- Paths: `src/codexspec/profile.py` (`_PROFILE_BLOCK`); `tests/test_profile.py` / `tests/test_init_profile.py` (block-content assertions).
- Covers: REQ-005, REQ-007, NFR-004, NFR-005, CON-001, CON-007; Plan: P1.2, P1.3.
- Dependencies: T1.1 (categories exist).
- **Test Scenarios** (US2-1..3, US4-4):
  - T1.2-S1 (happy, US2-1): rendered block contains a `strategies/` pointer and a `runbooks/` pointer (`.codexspec/profile/strategies/`, `.codexspec/profile/runbooks/`).
  - T1.2-S2 (happy, US2-1): block contains the active-recall directive (an emphasis-free span such as `before` … `read every record` for constraints is retained, plus a scan-and-match directive for the on-demand categories).
  - T1.2-S3 (happy, US4-4): block contains the near-moment distill trigger rule (an emphasis-free span naming `/codexspec:distill` and "near" the moment reusable knowledge is produced, "non-blocking").
  - T1.2-S4 (boundary, NFR-004): block contains no record filenames/content and remains bounded — `constraints` is still the first pointer and the block is a fixed directive (assert the START/END markers wrap a small directive, no per-record text).
  - T1.2-S5 (boundary, NFR-005): injecting the block twice into a file yields exactly one block region (idempotent — existing `inject_profile_block` test extended).
  - T1.2-S6 (boundary, DEC-006): no code path injects the block into `constitution.md` — init/codex wiring targets only CLAUDE.md/AGENTS.md.

---

## Phase 2 — `templates/commands/distill.md` (representation + discipline)

### T2.1 — Document `strategies/` + `runbooks/` categories, bodies, examples

- Outcome: store-layout section lists the two new categories; record-format defines the **strategy** anti-hollow body (`trigger` / `action` / `evidence`) with self-model `scope: self`, and the **runbook** body (ordered `steps` / `failure-recovery` / `evidence`); an unstatable triple is not recorded; one strategy example and one runbook example added.
- Paths: `templates/commands/distill.md`; `tests/test_distill_template.py`.
- Covers: REQ-001, REQ-002, REQ-003, REQ-004, REQ-012, CON-003; Plan: P2.1, P2.2.
- Dependencies: none (template text).
- **Test Scenarios** (US1-1..4):
  - T2.1-S1 (happy, US1-1): distill.md documents a `runbooks/` category and requires ordered steps + failure-recovery + evidence.
  - T2.1-S2 (happy, US1-2): distill.md documents a `strategies/` category and requires trigger + action + evidence.
  - T2.1-S3 (happy, US1-3): distill.md states the self-model is a strategy marked `scope: self`.
  - T2.1-S4 (boundary, US1-4): distill.md states a strategy/runbook whose required parts cannot be stated is not recorded (anti-hollow extends to the new types).
  - T2.1-S5 (happy): a worked `strategies/` example and a worked `runbooks/` example are present, each showing its required body parts.
  - T2.1-S6 (boundary, REQ-012): the documented category set is exactly the six; no `facts/` category appears.

### T2.2 — Operating Model: near-moment + long-run + backstop

- Outcome: Operating Model documents near-moment invocation in any session (incl. plain-chat/non-SDD) and long-run along-the-way distillation with end `auto_distill` retained as backstop.
- Paths: `templates/commands/distill.md`; `tests/test_distill_template.py`.
- Covers: REQ-007, REQ-008; Plan: P2.3.
- Dependencies: none.
- **Test Scenarios** (US4-1,2):
  - T2.2-S1 (happy, US4-1): distill.md states it may be invoked near the moment reusable knowledge is produced, in any session including plain-chat / non-SDD fixes.
  - T2.2-S2 (happy, US4-2): distill.md states long-running `implement-tasks` distills along the way, with end-of-task `auto_distill` as a backstop.

### T2.3 — Debounce / session-boundary discipline

- Outcome: a discipline section defines the session-local already-distilled boundary (in conversation context, no persistent state), delta-only processing, light early-exit, and cross-session read-profile fallback.
- Paths: `templates/commands/distill.md`; `tests/test_distill_template.py`.
- Covers: REQ-009, CON-009, NFR-002; Plan: P2.4.
- Dependencies: none.
- **Test Scenarios** (US4-3):
  - T2.3-S1 (happy, US4-3): distill.md documents a session-local already-distilled boundary held in conversation context with no persistent runtime state.
  - T2.3-S2 (happy, US4-3): distill.md states consecutive triggers process only the substantive new delta and early-exit when nothing is new.
  - T2.3-S3 (boundary): distill.md states cross-session dedup falls back to reading the profile and skipping covered records.

### T2.4 — Consolidation: mark clusters + `/distill review` merge

- Outcome: a consolidation section states distill **marks** narrow-record clusters via a per-record field (e.g. `cluster:` / `consolidation: candidate`), never a central index, non-destructively; `/distill review` gains a step that, on human confirmation, merges a cluster into one general record ("general rule + exceptions"), supports cross-category promotion (pitfalls → strategy), and `remove`s superseded members incl. the marker.
- Paths: `templates/commands/distill.md`; `tests/test_distill_template.py`.
- Covers: REQ-006, CON-005, CON-001; Plan: P2.5.
- Dependencies: none.
- **Test Scenarios** (US3-1..3):
  - T2.4-S1 (happy, US3-1): distill.md states consolidation marks candidate clusters via a per-record field and does not auto-rewrite or delete records.
  - T2.4-S2 (boundary, CON-001): distill.md states no central index/manifest file is created for consolidation (marking is per-record).
  - T2.4-S3 (happy, US3-2): distill.md's `/distill review` documents a human-confirmed merge into "general rule + exceptions".
  - T2.4-S4 (happy, US3-3): distill.md states cross-category promotion (e.g. several `pitfalls` → one `strategy`) is supported on confirmation.

---

## Phase 3 — Peripheral enumeration edits

### T3.1 — onboard exclusion extended (both sites)

- Outcome: `onboard.md` exclusion at **both** L53 and L88 extended to "never `decisions`, `pitfalls`, `strategies`, `runbooks`"; onboard still writes only `conventions` + narrow `constraints`.
- Paths: `templates/commands/onboard.md`; `tests/test_onboard_template.py`.
- Covers: REQ-010, CON-004; Plan: P3.1.
- Dependencies: none.
- **Test Scenarios**:
  - T3.1-S1 (happy): onboard.md states it never extracts `decisions`, `pitfalls`, `strategies`, or `runbooks` (emphasis-free span).
  - T3.1-S2 (boundary): both occurrences (extraction-scope paragraph and Boundaries bullet) carry the extended exclusion — no site still says only "decisions or pitfalls".
  - T3.1-S3 (happy): onboard.md still states it writes only `conventions` and `constraints`.

### T3.2 — evolve category awareness

- Outcome: `evolve.md` notes `strategies`/`runbooks` are vetted-eligible material; the vetted gate is unchanged.
- Paths: `templates/commands/evolve.md`.
- Covers: REQ-011, CON-008; Plan: P3.2.
- Dependencies: none.
- Verification (deterministic): `evolve.md` still requires `status: vetted` (existing `tests/test_profile_templates.py::test_evolve_still_reads_vetted_profile` stays green); the enumeration now includes `strategies`/`runbooks` (grep-confirmed). Non-testable enumeration edit — no new behavior, gate unchanged.

### T3.3 — specify profile-consultation enumeration

- Outcome: `specify.md` "Consult Project Profile" enumerates the two new categories.
- Paths: `templates/commands/specify.md`.
- Covers: REQ-005 (requirements-time read surface); Plan: P3.3.
- Dependencies: none.
- Verification (deterministic): `specify.md` enumeration includes `strategies`/`runbooks` (grep-confirmed); existing specify template tests stay green. Non-testable enumeration edit.

---

## Phase 4 — Derived regeneration + dogfood (self-bootstrap)

### T4.1 — Regenerate derived forms + re-render managed block

- Outcome: `uv run codexspec init . --force --ai both` regenerates
  `.claude/commands/codexspec/{distill,onboard,evolve,specify}.md` and
  `.agents/skills/codexspec-*/SKILL.md`, and re-renders the CLAUDE.md/AGENTS.md
  managed profile block from the edited `profile.py`.
- Paths: derived `.claude/commands/codexspec/`, `.agents/skills/`; `CLAUDE.md`, `AGENTS.md` (managed block only).
- Covers: NFR-003; Plan: P4.1.
- Dependencies: T1.1, T1.2, T2.1–T2.4, T3.1–T3.3 (regen must reflect final source).
- Verification (deterministic): `git status` shows only intended source + derived changes; `.codexspec/config.yml` unchanged (`workflow.auto_next`, `workflow.auto_distill`, `language.*`, `project.ai=both` preserved); CLAUDE.md/AGENTS.md managed block now shows six pointers + active-recall + trigger rule; `constitution.md` untouched. Non-testable infrastructure step.

---

## Phase 5 — Integration verification

### T5.1 — ruff + full suite green

- Outcome: `uv run ruff check src/ tests/` → 0; `uv run pytest -q` full suite green with no regression from baseline.
- Covers: NFR-003; verification for all REQ/NFR; Plan: P5.1, P5.2.
- Dependencies: all prior tasks.
- Verification (deterministic): ruff clean; full suite green; profile-category enumeration lockstep consistent across `profile.py`, `tests/test_profile.py`, `tests/test_init_profile.py`, `distill.md`, `specify.md`. Non-testable verification task.

---

## Coverage Table

| REQ / NFR | Task(s) | Plan | Design |
|---|---|---|---|
| REQ-001 | T1.1, T2.1 | P1.1/P1.4/P2.1 | C1 |
| REQ-002 | T2.1 | P2.2 | C2/D4 |
| REQ-003 | T2.1 | P2.2 | C2 |
| REQ-004 | T2.1 | P2.2 | C2 |
| REQ-005 | T1.2, T3.3 | P1.2/P3.3 | C3 |
| REQ-006 | T2.4 | P2.5 | C7/D2 |
| REQ-007 | T1.2, T2.2 | P1.3/P2.3 | C4/D1 |
| REQ-008 | T2.2 | P2.3 | C5 |
| REQ-009 | T2.3 | P2.4 | C6/D3 |
| REQ-010 | T3.1 | P3.1 | C8 |
| REQ-011 | T3.2 | P3.2 | C9 |
| REQ-012 | T1.1, T2.1 | P1.1/P2.1 | C1 |
| NFR-001 | T1.2, T2.4 | P1.2/P2.5 | C1/C7/D2 |
| NFR-002 | T2.3, T2.4 | P2.4/P2.5 | C6/D3 |
| NFR-003 | T1.1, T4.1, T5.1 | P1.1/P4.1/P5.1 | C1/C10 |
| NFR-004 | T1.2 | P1.2 | C3/D1 |
| NFR-005 | T1.2, T4.1 | P1.3/P4.1 | C4/D1 |

## Scenario → Task Map (testable tasks)

| Task | Scenarios | Upstream (spec) |
|---|---|---|
| T1.1 | S1–S5 | REQ-001/012 behavior |
| T1.2 | S1–S6 | US2-1..3, US4-4 |
| T2.1 | S1–S6 | US1-1..4 |
| T2.2 | S1–S2 | US4-1,2 |
| T2.3 | S1–S3 | US4-3 |
| T2.4 | S1–S4 | US3-1..3 |
| T3.1 | S1–S3 | REQ-010 behavior |

Non-testable tasks (deterministic verification, no scenarios): T3.2, T3.3, T4.1, T5.1.

## Dependency Summary

- T1.1 → T1.2 (categories before block).
- T1.1, T1.2, T2.1–T2.4, T3.1–T3.3 → T4.1 (regen reflects final source).
- all → T5.1 (final gate).
- T2.x and T3.x are mutually independent (different files) and may proceed in any order after their trivial deps; `[P]` not asserted since they share the review/verify gate.

## Unmapped Tasks

None. Every task maps to a REQ/NFR + plan phase + design component.

## Implementation Status

All tasks complete (2026-08-16):

- [x] T1.1 — `PROFILE_CATEGORIES` → 6 + scaffold/docstrings (test_profile.py, test_init_profile.py)
- [x] T1.2 — `_PROFILE_BLOCK` active recall + 2 pointers + near-moment trigger
- [x] T2.1 — distill.md strategies/runbooks categories + bodies + examples + no-facts
- [x] T2.2 — distill.md operating model near-moment + long-run + backstop
- [x] T2.3 — distill.md debounce / session-boundary discipline
- [x] T2.4 — distill.md consolidation mark + `/distill review` merge
- [x] T3.1 — onboard exclusion extended at both sites
- [x] T3.2 — evolve category awareness (gate unchanged)
- [x] T3.3 — specify profile-consultation enumeration
- [x] T4.1 — derived regen via `init --force --ai both`; config/constitution unchanged
- [x] T5.1 — ruff clean; full suite 1198 passed / 50 skipped

Baseline green established for the Final Code Review Loop.
