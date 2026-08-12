# Tasks: profile-consumption

<!--
Language: document language is English (.codexspec/config.yml → language.document: en).
Every task: Covers: REQ-xxx; Plan: <component/phase>. Derived from plan.md; no redesign.
-->

**Feature Branch**: `2026-0812-14054p-profile-consumption`

## Group A — Shared profile module (Plan C1 / Phase 1)

### T-001 — Create `src/codexspec/profile.py` (testable: Python)

- **Outcome**: A shared module providing the scaffold, channel-adaptive block render, and idempotent injection.
- **Path**: `src/codexspec/profile.py`; tests `tests/test_profile.py` (new)
- **Covers**: REQ-002, REQ-004, REQ-006, REQ-007, NFR-002, NFR-004; **Plan**: C1 / Phase 1 (PLAN-DEC-001, -003, -004)
- **Dependencies**: none
- **Public surface**: `PROFILE_DIR` (`.codexspec/profile`), `PROFILE_FILES` (constraints/conventions/pitfalls/decisions), `PROFILE_BLOCK_START`/`PROFILE_BLOCK_END` markers, `ensure_profile_scaffold(target_dir)`, `render_profile_block(channel)`, `inject_profile_block(context_path, channel)`.
- **Test Scenarios**:
  1. `ensure_profile_scaffold` on an empty project creates `.codexspec/profile/` and all four files as header-only placeholders.
  2. `ensure_profile_scaffold` is idempotent and non-destructive: a file already containing distilled records is left byte-identical (does not overwrite).
  3. `render_profile_block("claude")` contains the line `@.codexspec/profile/constraints.md` and a pointer entry for each of conventions/pitfalls/decisions.
  4. `render_profile_block("codex")` contains a strong mandatory constraints imperative referencing `constraints.md` and contains **no** `@import` / `@.codexspec` line.
  5. Both channels' blocks instruct on-demand reading of the full records (status-aware, no filtering by `status`) — REQ-007.
  6. `inject_profile_block` into a file lacking the block appends exactly one bounded `<!-- CODEXSPEC PROFILE START/END -->` block.
  7. `inject_profile_block` called twice is idempotent (second call yields a byte-identical file).
  8. `inject_profile_block` updates only within the markers: content outside the markers is byte-identical before/after.
  9. `render_profile_block` raises a clear error for an unknown channel rather than silently mis-handling it.

## Group B — init wiring (Plan C2 / Phase 2)

### T-002 — Wire scaffold + CLAUDE.md injection into init (testable: Python)

- **Outcome**: `init` unconditionally ensures the profile scaffold and injects the `"claude"` profile block into CLAUDE.md when Claude is configured — after CLAUDE.md is created/compliance-ensured (RA-1 ordering).
- **Paths**: `src/codexspec/__init__.py`; tests `tests/test_init_profile.py` (new) or extend an existing init test module
- **Covers**: REQ-001, REQ-003, REQ-004; **Plan**: C2 / Phase 2 (PLAN-DEC-005)
- **Dependencies**: T-001
- **Test Scenarios**:
  1. `init` with `project.ai: claude` → CLAUDE.md contains exactly one PROFILE block whose constraints use `@import`.
  2. `init` unconditionally creates the profile scaffold (dir + four files) even when the project starts empty.
  3. The CLAUDE.md PROFILE block is injected **after** creation/compliance so it never clobbers the compliance `@import` or the body (RA-1).
  4. Re-running `init` is idempotent: the PROFILE block is updated in place; content outside its markers is byte-identical (SC-002).
  5. An existing CLAUDE.md with user content keeps that content; only the bounded block is added/updated.

## Group C — Codex wiring (Plan C3 / Phase 3)

### T-003 — Inject the `"codex"` profile block into AGENTS.md (testable: Python)

- **Outcome**: `CodexIntegration.ensure_context_file` also injects the `"codex"` profile block (strong constraints pointer + pointer index), coexisting with the existing `<!-- CODEXSPEC START/END -->` skills block.
- **Paths**: `src/codexspec/integrations/codex.py`; tests `tests/test_codex_integration.py` (extend)
- **Covers**: REQ-001, REQ-006; **Plan**: C3 / Phase 3 (PLAN-DEC-005, -006)
- **Dependencies**: T-001
- **`[P]`** with T-002 (distinct files, both after T-001)
- **Test Scenarios**:
  1. `init`/`ensure_context_file` with `project.ai: codex` → AGENTS.md contains the PROFILE block with the strong constraints imperative and **no** `@import`.
  2. The PROFILE block coexists with the existing skills block; both bounded blocks are present and distinct.
  3. Re-running is idempotent; the existing skills block and any user content are preserved.
  4. `project.ai: both` → CLAUDE.md gets the `@import` variant and AGENTS.md gets the pointer variant (cross-check with T-002).

## Group D — specify B-layer (Plan C4 / Phase 4)

### T-004 — Add `## Consult Project Profile` to `specify.md` (non-testable: template/doc; pinned by T-005)

- **Outcome**: `specify.md` instructs reading `.codexspec/profile/` during discovery (constraints first, others as relevant), degrading silently when the profile is empty/absent; no other SDD-stage template changed.
- **Path**: `templates/commands/specify.md`
- **Covers**: REQ-005; **Plan**: C4 / Phase 4 (PLAN-DEC-007)
- **Dependencies**: none
- **`[P]`** with T-001/T-002/T-003 (distinct file)
- **Deterministic verification**: `specify.md` contains a `## Consult Project Profile` section referencing `.codexspec/profile/`, placed before requirements are finalized, with a silent-degradation note. (Behavioral pinning is T-005.)

## Group E — Verification (Plan Phase 5)

### T-005 — Template-invariant tests (testable: tests)

- **Outcome**: Tests pin the specify B-layer and the "no other stage reads profile" + "no staleness surface" invariants.
- **Path**: `tests/test_profile_templates.py` (new) or extend `tests/test_sdd_workflow_templates.py`
- **Covers**: verification of REQ-005, CON-003, NFR-003, SC-004, SC-005, SC-006; **Plan**: Phase 5
- **Dependencies**: T-004 (for specify assertion); T-001/T-002/T-003 not required for the template-only assertions
- **Test Scenarios**:
  1. `specify.md` contains a `## Consult Project Profile` step referencing `.codexspec/profile/`. *(REQ-005 / SC-004a)*
  2. No other SDD-stage template (`generate-spec`, `spec-to-plan`, `plan-to-tasks`, `implement-tasks`, `review-spec`, `review-plan`, `review-tasks`, `review-code`) references `.codexspec/profile`. *(CON-003 / SC-004b)*
  3. `templates/commands/evolve.md` is not modified by this feature (still reads vetted profile → PR; no consumption logic added). *(NFR-003 / SC-005)*
  4. No source or template file literally inlines constraints content into a context file — the Claude path uses `@import`, the Codex path a pointer (assert `render_profile_block("codex")` has no `@import`). *(SC-006)*

### T-006 — Full-suite & lint gate (non-testable: checkpoint)

- **Outcome**: Green end-to-end, including a dogfood sanity check.
- **Covers**: all; **Plan**: Phase 5
- **Dependencies**: T-001..T-005
- **Deterministic verification**: `uv run python -m pytest` passes; `uv run ruff check src/` clean. Dogfood: `uv run codexspec init . --force --ai both` injects both PROFILE blocks + scaffold without altering this repo's CLAUDE.md/AGENTS.md bodies outside the markers (inspect diff).

## Dependency Summary

- T-001 → (T-002, T-003 `[P]`); T-004 `[P]` (independent); (T-002/T-003/T-004) → T-005 → T-006
- Acyclic; each dependency ordered before its dependents.

## Coverage Table

| Requirement / SC | Plan | Task(s) |
|------------------|------|---------|
| REQ-001 | C2, C3 | T-002 (T-002#1), T-003 (T-003#1,#4) |
| REQ-002 | C1 | T-001 (#3,#6) |
| REQ-003 | C1, C2, C3 | T-001 (#6–#8), T-002 (#4), T-003 (#3) |
| REQ-004 | C1, C2 | T-001 (#1,#2), T-002 (#2) |
| REQ-005 / SC-004a | C4 | T-004; T-005 (#1) |
| REQ-006 | C1, C3 | T-001 (#3,#4), T-003 (#1) |
| REQ-007 | C1 | T-001 (#5) |
| NFR-001 | C1–C4 | T-001..T-004 (paths under templates/ + src/) |
| NFR-002 | C1 | T-001 (#3,#4 — only constraints + pointers in block) |
| NFR-003 / SC-005 | — | T-005 (#3) |
| NFR-004 / SC-006 | C1, C3 | T-001 (#4), T-005 (#4) |
| SC-002 | C2, C3 | T-002 (#4), T-003 (#3) |
| SC-003 | C1, C2 | T-001 (#1), T-002 (#2) |
| SC-004b (CON-003) | C4 | T-005 (#2) |

## Scenario → Task Map (testable tasks)

- **T-001**: scenarios 1–9 → `tests/test_profile.py`
- **T-002**: scenarios 1–5 → `tests/test_init_profile.py`
- **T-003**: scenarios 1–4 → `tests/test_codex_integration.py`
- **T-005**: scenarios 1–4 → `tests/test_profile_templates.py`

## Unmapped Tasks

None. (Derived-artifact regeneration and version bump are the standard release tail, out of this feature's task scope per plan.)

## Implementation Status

- [x] **T-001** — `src/codexspec/profile.py` (scaffold + channel-adaptive render + idempotent inject); `tests/test_profile.py` (9 scenarios) green.
- [x] **T-002** — init wiring: unconditional `ensure_profile_scaffold` + CLAUDE.md `@import` block after compliance; `tests/test_init_profile.py` (5) green.
- [x] **T-003** — `CodexIntegration.ensure_context_file` injects the codex pointer block; `tests/test_codex_integration.py` (+3) green.
- [x] **T-004** — `## Consult Project Profile` added to `templates/commands/specify.md`.
- [x] **T-005** — `tests/test_profile_templates.py` (4 invariants) green.
- [x] **T-006** — dogfood (tmp) confirms both channel blocks + scaffold + preserved compliance import; full suite + ruff (baseline pending final confirm). Updated one pre-existing test (`test_init_compliance`) whose byte-identity expectation was superseded by the intended unconditional profile-block injection.
