# Implementation Plan: profile-consumption

<!--
Language: document language is English (.codexspec/config.yml → language.document: en).
Authority: requirements.md (confirmed) > spec.md > constitution/repo facts > plan decisions.
-->

**Feature Branch**: `2026-0812-14054p-profile-consumption`
**Created**: 2026-08-12
**Status**: Draft

## Context, Goals, Non-Goals

- **Goal**: Make a user project's distilled `.codexspec/profile/` take effect locally, via (A) ambient injection into context files at `init` and (B) a `specify`-time read.
- **Non-Goals** (spec Out of Scope): no constitution change; no `evolve`/upstream change; no downstream-stage profile reads; no metric/eval optimization.

## Existing Repository Constraints (verified)

- **init integration dispatch**: `get_integrations(ai)` yields the configured integrations; `integration_keys = {i.key for i in integrations}` (`src/codexspec/__init__.py`).
- **CLAUDE.md is managed inline in `__init__.py`** under `if "claude" in integration_keys:` (creates when absent via `_get_claude_md_content`; else ensures the compliance `@import`; never overwrites the body). `ClaudeIntegration.install()` installs commands only and does **not** touch CLAUDE.md.
- **AGENTS.md is managed by `CodexIntegration.ensure_context_file()`** via a bounded `<!-- CODEXSPEC START/END -->` block produced by `_context_section()` and replaced idempotently with a `re.sub`.
- **`@import` syntax** is a standalone line `@<relative-path>` (e.g. the existing `@.codexspec/memory/constitution.md`), expanded fully into Claude Code context.
- **distill contract**: writes only under `.codexspec/profile/`, never touches other tracked files (must remain true — DEC-005 relies on it).
- **Self-bootstrap**: edit `templates/` + `src/codexspec/`; derived command artifacts regenerate at release; never hand-edit `.claude/commands/` or `.agents/skills/`.

## Technical Approach

One new shared module renders and injects a bounded, channel-adaptive **profile block**, plus an unconditional **scaffold**; two call sites (CLAUDE.md inline in init; AGENTS.md in the Codex integration) reuse it; and `specify.md` gains the B-layer read.

## Plan-Level Decisions

- **PLAN-DEC-001 (shared module)**: Add `src/codexspec/profile.py` holding: `PROFILE_DIR`/`PROFILE_FILES` constants; `ensure_profile_scaffold(target_dir)`; `render_profile_block(channel)` (`channel` ∈ {"claude","codex"}); `inject_profile_block(context_path, channel)`. Keeps the block content DRY across both call sites and unit-testable in isolation. *Covers: REQ-002, REQ-004, REQ-006, REQ-007, NFR-002, NFR-004.*
- **PLAN-DEC-002 (separate bounded block)**: Use a dedicated marker pair `<!-- CODEXSPEC PROFILE START -->` / `<!-- CODEXSPEC PROFILE END -->` in **both** context files, distinct from the Codex skills block and the CLAUDE.md compliance import. Injection = regex-replace within markers if present, else append the block; never touch content outside the markers. *Covers: REQ-003, CON-005.*
- **PLAN-DEC-003 (scaffold = dir + four header-only files; resolves review RA-1)**: `ensure_profile_scaffold` creates `.codexspec/profile/` and, if absent, `constraints.md` / `conventions.md` / `pitfalls.md` / `decisions.md` as header-only placeholders (e.g. `# Constraints\n`). This makes the Claude `@import` AND every pointer resolve to a real file (no dangling reference on any channel), and distill later appends into them (its "create on first write" still works on an existing header-only file). *Covers: REQ-004, SC-003.*
- **PLAN-DEC-004 (channel-adaptive constraints in `render_profile_block`)**: `channel="claude"` emits a line `@.codexspec/profile/constraints.md` (guaranteed-present + auto-fresh). `channel="codex"` emits a strong mandatory imperative ("Before non-trivial work you MUST read `.codexspec/profile/constraints.md` — highest-priority prohibitions") and NO `@import`. Both channels then emit the same pointer index for conventions/pitfalls/decisions (name + one-line purpose + when-to-consult), instructing on-demand reads. *Covers: REQ-006, NFR-004, SC-006.*
- **PLAN-DEC-005 (call sites)**: `ensure_profile_scaffold` is called **unconditionally** in init (independent of integrations). CLAUDE.md injection is added to the existing inline `if "claude" in integration_keys:` block in `__init__.py`; AGENTS.md injection is added inside `CodexIntegration.ensure_context_file()`. Both call the shared `inject_profile_block`. *Covers: REQ-001, REQ-003, REQ-004.*
- **PLAN-DEC-006 (no Codex `@import` dependency)**: The Codex path never emits `@import`; correctness relies only on Codex reading AGENTS.md text + the agent reading a file on demand. OPEN-001 stays a non-blocking optional-enhancement note. *Covers: NFR-004.*
- **PLAN-DEC-007 (specify B-layer)**: Add a `## Consult Project Profile` step to `templates/commands/specify.md` instructing, before finalizing requirements, to read `.codexspec/profile/` (constraints first, then the other files as relevant) and factor it into discovery — degrading silently when the profile is empty/absent. No other SDD-stage template is modified. *Covers: REQ-005, CON-003.*

## Components / Interfaces

- **C1 — `src/codexspec/profile.py`** (new): scaffold + channel-adaptive block render + idempotent inject. *Covers: REQ-002, REQ-003, REQ-004, REQ-006, REQ-007, NFR-002, NFR-004.*
- **C2 — `src/codexspec/__init__.py`** (edit): call `ensure_profile_scaffold(target_dir)` unconditionally; call `inject_profile_block(CLAUDE.md, "claude")` inside the existing claude block. *Covers: REQ-001, REQ-003, REQ-004.*
- **C3 — `src/codexspec/integrations/codex.py`** (edit): in `ensure_context_file`, also inject the `"codex"` profile block. *Covers: REQ-001, REQ-006.*
- **C4 — `templates/commands/specify.md`** (edit): `## Consult Project Profile` B-layer step. *Covers: REQ-005.*
- **C5 — derived artifacts** (`.claude/commands/codexspec/specify.md`, `.agents/skills/codexspec-specify/`): regenerate at release via publish → init; NOT hand-edited. *Supports: NFR-001.*
- **Unchanged (enforced)**: constitution; `evolve`; downstream-stage templates; `distill` (keeps its no-touch-tracked-files contract). *Enforces: NFR-003, CON-003, DEC-005.*

## Implementation Phases

1. **Phase 1 — `profile.py`** (C1): constants, `ensure_profile_scaffold`, `render_profile_block`, `inject_profile_block`; unit tests (TDD).
2. **Phase 2 — init wiring** (C2): unconditional scaffold + CLAUDE.md injection; init tests.
3. **Phase 3 — Codex wiring** (C3): AGENTS.md injection; codex-integration tests.
4. **Phase 4 — specify template** (C4): B-layer section; template test + the no-other-stage-reads assertion.
5. **Phase 5 — gates**: full suite + ruff; dogfood sanity (`init . --ai both` produces both blocks + scaffold without clobbering this repo's CLAUDE.md/AGENTS.md bodies).

(Derived-artifact regeneration and version bump are the standard release tail, not feature tasks.)

## Verification Strategy

- **profile.py unit tests**: `render_profile_block("claude")` contains `@.codexspec/profile/constraints.md` and the three pointers; `render_profile_block("codex")` contains the strong constraints imperative and **no** `@import`; `inject_profile_block` is idempotent (second call → identical file) and non-destructive (content outside markers byte-identical); `ensure_profile_scaffold` creates the dir + four header-only files and is safe when they already exist.
- **init tests**: `project.ai` = claude → CLAUDE.md has the PROFILE block; codex → AGENTS.md has it; both → both; re-init idempotent; a pre-existing context-file body is preserved (SC-002); scaffold exists after init on an empty project (SC-003).
- **specify template test**: `specify.md` contains the `## Consult Project Profile` step (SC-004a); **no other** SDD-stage template (`generate-spec`/`spec-to-plan`/`plan-to-tasks`/`implement-tasks`/`review-*`) reads `.codexspec/profile/` (SC-004b).
- **Invariants**: constitution file unchanged; `evolve.md` unchanged (SC-005); no literal copy of constraints content in any context file — Claude uses `@import`, Codex uses a pointer (SC-006, grep-style test).
- **Suite/lint**: `uv run python -m pytest` green; `uv run ruff check src/` clean.

## Risks & Trade-offs

- **Idempotency / non-destruction across re-init** — mitigated by bounded-marker regex replace (same pattern as the existing AGENTS.md block) and never editing outside markers (PLAN-DEC-002).
- **Header-only `constraints.md` @import'd** injects a tiny header into Claude context — harmless; content grows as distill appends.
- **Constraint presence weaker on Codex** (pointer vs @import) — accepted trade-off (DEC-005), mitigated by a strong imperative + small file + the specify B-layer.
- **scaffold vs distill "create on first write"** — pre-creating header-only files is compatible (distill appends to an existing file); verified by test.

## Requirements Coverage

| Requirement | Plan Reference |
|-------------|----------------|
| REQ-001 | C2, C3; PLAN-DEC-005 |
| REQ-002 | C1; PLAN-DEC-001, PLAN-DEC-004 |
| REQ-003 | C1, C2, C3; PLAN-DEC-002 |
| REQ-004 | C1, C2; PLAN-DEC-003 |
| REQ-005 | C4; PLAN-DEC-007 |
| REQ-006 | C1, C3; PLAN-DEC-004 |
| REQ-007 | C1 (block instructs on-demand read of full record incl. status); PLAN-DEC-001 |
| NFR-001 | C1–C4 under `templates/` + `src/`; C5 regenerated (self-bootstrap) |
| NFR-002 | C1; PLAN-DEC-004 (only constraints + pointers always-present) |
| NFR-003 | Unchanged constitution / evolve (enforced; SC-005) |
| NFR-004 | C3; PLAN-DEC-004, PLAN-DEC-006 (no `@import` on Codex) |
