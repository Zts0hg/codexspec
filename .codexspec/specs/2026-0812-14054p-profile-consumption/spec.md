# Feature Specification: profile-consumption

<!--
Language: document language is English (.codexspec/config.yml → language.document: en).
Compiled from requirements.md. Only Status: confirmed entries are binding.
-->

**Feature Branch**: `2026-0812-14054p-profile-consumption`
**Created**: 2026-08-12
**Status**: Draft
**Input**: Make a user project's distilled `.codexspec/profile/` take effect in that project's subsequent work, via ambient injection into context files (init) plus a specify-time read.

## Context and Goals

CodexSpec 0.7.7 shipped `distill` (writes `.codexspec/profile/`) and `evolve` (reads vetted profile → upstream PR), but **nothing consumes the profile inside the user's own project** — the store is write-only from distill and read-only by evolve. This feature adds a local **consumption** path so distilled knowledge influences later work: pitfalls are not re-hit, prior conventions/decisions are not re-litigated.

Two complementary layers, one product feature shipped via `codexspec init` + command templates:

- **A-layer (ambient)**: init injects a managed block into each configured integration's context file (CLAUDE.md / AGENTS.md), making the profile discoverable in every session including plain chat.
- **B-layer (requirements-time)**: `specify` reads the profile so `requirements.md` synthesizes past constraints/pitfalls/conventions/decisions; downstream stays requirements-authoritative.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Ambient profile injection at init (Priority: P1)

A user runs `codexspec init` in a project configured for Claude and/or Codex. Init writes an identical managed profile block into each context file: a strong mandatory pointer to `constraints/` plus a pointer index to conventions/pitfalls/decisions (no `@import`). It also ensures the profile scaffold exists. From then on, every session in that project surfaces the constraints pointer and can consult the pointed-to directories on demand.

**Why this priority**: This is the core ambient mechanism and the delivery vehicle; it is the MVP.

**Independent Test**: Run init in a temp project with `project.ai` = claude / codex / both; assert the correct context file(s) receive an idempotent managed block with constraints delivered per channel + the pointer index, and that the profile scaffold exists.

**Acceptance Scenarios**:

1. **Given** `project.ai: claude`, **When** init runs, **Then** CLAUDE.md gains a bounded managed block with a strong mandatory pointer to `.codexspec/profile/constraints/` plus a pointer index to conventions/pitfalls/decisions (no `@import`), and the profile scaffold exists.
2. **Given** `project.ai: codex`, **When** init runs, **Then** AGENTS.md gains the identical bounded managed block (uniform pointer, no `@import`).
3. **Given** `project.ai: both`, **When** init runs, **Then** both files receive their channel-appropriate block.
4. **Given** init has already injected the block, **When** init runs again, **Then** the block is updated idempotently and no other user content in the file is altered.
5. **Given** an existing context file with user content, **When** init injects, **Then** only the bounded managed block is added/updated; the user's other content is preserved.

---

### User Story 2 - Distilled knowledge takes effect immediately, no re-init (Priority: P1)

A first-time user's project has no profile content yet. Init still wires the reference and creates the scaffold. Later, `distill` writes a pitfall. In the very next session the agent can consult it — without re-running init and with no dangling reference.

**Why this priority**: Immediacy is the point of decoupling "wire the reference" from "profile has content"; without it, distilled knowledge is inert until the next init.

**Independent Test**: init on an empty project → confirm scaffold + managed block exist; add a record to a profile file → confirm the reference already resolves to the now-non-empty file (no init re-run needed).

**Acceptance Scenarios**:

1. **Given** a project with no prior profile, **When** init runs, **Then** the managed block and the profile scaffold (four category directories, each with a `.gitkeep`) are created; no reference dangles.
2. **Given** init already ran and later `distill` adds a record file under `pitfalls/`, **When** the next session consults the pointer, **Then** it reads the live record with no init re-run.

---

### User Story 3 - Profile consulted during specify (Priority: P2)

While discovering requirements for a new feature, `specify` reads `.codexspec/profile/` so the confirmed `requirements.md` already reflects the project's constraints/pitfalls/conventions/decisions. Downstream stages do not read the profile.

**Why this priority**: Bakes profile influence into the pipeline's source of truth; depends on the profile existing (US1/US2).

**Independent Test**: Confirm `specify.md` instructs reading the profile during discovery; confirm no other SDD-stage template reads the profile.

**Acceptance Scenarios**:

1. **Given** a non-empty profile, **When** `specify` runs, **Then** it consults the profile before finalizing requirements.
2. **Given** the profile is empty or absent, **When** `specify` runs, **Then** it proceeds normally (nothing to apply), no error.
3. **Given** any downstream stage (`generate-spec`/`spec-to-plan`/`plan-to-tasks`/`implement-tasks`/reviews), **When** it runs, **Then** it does not read the profile.

---

### Edge Cases

- **Empty/absent profile** → init still wires + scaffolds (US2-1); specify and ambient reads degrade to "nothing to apply", no error.
- **Re-run init** → idempotent block update, user content preserved (US1-4/5).
- **Parallel feature branches both distill** → each adds differently-named `<id>.md` files under the category directories, so git merges them with no conflict (DEC-007).
- **Large conventions/pitfalls/decisions files** → always-loaded footprint unchanged (content read on demand only) (NFR-002).
- **Profile file grows after init** → reference reads live file; no re-sync, no staleness.

## Requirements *(mandatory)*

### Functional Requirements

- **REQ-001**: `codexspec init` MUST inject a managed profile block into the context file of each configured AI integration (`project.ai`): CLAUDE.md for Claude, AGENTS.md for Codex, both when configured for both.
  - Sources: NEED-002, NEED-003
- **REQ-002**: The managed block MUST contain (a) a strong mandatory pointer to the `constraints/` directory (per REQ-006), and (b) a pointer index to `conventions/` / `pitfalls/` / `decisions/` — each named, with a one-line description and a "when to consult" note — whose records are read on demand rather than inlined.
  - Sources: NEED-002, DEC-006
- **REQ-003**: init MUST inject **unconditionally and idempotently** (not gated on whether the profile has content), using recognizable boundary markers, updating in place on re-run, and MUST NOT clobber any other content in the context file.
  - Sources: NEED-005, DEC-004, CON-005
- **REQ-004**: init MUST ensure the profile **scaffold** exists — the four category directories `constraints/` / `conventions/` / `pitfalls/` / `decisions/`, each kept by a `.gitkeep` so an empty category is tracked and every pointer resolves. This makes later-distilled content effective with no re-init and no dangling reference.
  - Sources: NEED-005, DEC-004, DEC-007
- **REQ-005**: `specify.md` MUST read the `.codexspec/profile/` directories during requirements discovery so `requirements.md` incorporates the relevant constraints/pitfalls/conventions/decisions. No other SDD-stage template may read the profile.
  - Sources: NEED-004, DEC-002, CON-003
- **REQ-006**: Constraints delivery MUST be a **uniform strong mandatory pointer on both channels** — CLAUDE.md and AGENTS.md get the identical block instructing the agent to read every record under `.codexspec/profile/constraints/` before non-trivial work. **No `@import` on any channel.**
  - Sources: DEC-006
- **REQ-007**: Local consumption MUST NOT filter by `status`: both `candidate` and `vetted` records are surfaced; the full record (including `status`) is read on demand so the agent can weight `candidate` lower. `vetted` remains only the `evolve` gate.
  - Sources: DEC-003
- **REQ-008**: The store MUST be one record per file (`<id>.md`, the id also being the filename) under a per-category directory, so parallel feature branches add differently-named files that git merges without conflict. distill's add/replace/remove are create/edit/delete of a single file.
  - Sources: DEC-007

### Non-Functional Requirements

- **NFR-001**: All changes MUST be confined to `templates/` and `src/codexspec/` (init logic + integrations). Derived artifacts sync via publish → `codexspec init`; CodexSpec's own repo obtains the capability by dogfooding init (self-bootstrap).
  - Sources: CON-001
- **NFR-002**: The always-loaded context footprint MUST be independent of the size of the profile; only the pointer block (constraints pointer + the pointer index) is always-present — record content is read on demand.
  - Sources: CON-004, DEC-006
- **NFR-003**: The feature MUST NOT modify the constitution or use it as an injection surface; it MUST NOT alter `evolve` or the upstream-contribution path.
  - Sources: CON-002, OUT-001, OUT-002
- **NFR-004**: The design MUST NOT depend on Codex expanding `@import`; with the uniform pointer block (DEC-006) no channel uses `@import`, so this is satisfied by construction.
  - Sources: DEC-006

### Open Questions (non-blocking)

- **OPEN-001**: RESOLVED (moot). The uniform pointer block (REQ-006/DEC-006) uses no `@import` on any channel, so Codex `@import` support is irrelevant.
- **OPEN-003**: Exact managed-block text, pointer-index entries, and the Codex constraints imperative — a drafting detail resolved during implementation.

> Open items remain questions and MUST NOT be rewritten as confirmed requirements.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: After init with `project.ai` = claude / codex / both, the correct context file(s) contain exactly one bounded managed profile block, constraints delivered per REQ-006, plus the pointer index (verifiable by inspection/test).
- **SC-002**: Re-running init leaves user content outside the managed block byte-identical and updates the block idempotently.
- **SC-003**: After init, the `.codexspec/profile/` scaffold exists such that every injected reference resolves (no dangling reference), with no re-init required for later-distilled content to be readable.
- **SC-004**: `specify.md` reads the profile; no other SDD-stage template contains a profile read.
- **SC-005**: The constitution file is unchanged by this feature, and no `evolve`/upstream logic is modified.
- **SC-006**: No `@import` appears in the profile block on any channel; both CLAUDE.md and AGENTS.md get the identical pointer block. The store is one-file-per-record directories, so parallel-branch distill merges are conflict-free.

## Out of Scope

- **OUT-001**: Modifying the constitution or using it as an injection surface. Reason: keep it high-authority and concise.
- **OUT-002**: Any change to `evolve` or the upstream-PR path. Reason: pure local consumption, decoupled from contribution.
- **OUT-003**: Metric/eval-driven (DSPy/GEPA) optimization of the profile or prompts. Reason: out of scope.
- Reading the profile in downstream SDD stages. Reason: requirements.md carries the influence transitively (CON-003).

## Assumptions

- `codexspec init` already creates/maintains CLAUDE.md (creating it when absent; never overwriting an existing body, only prepending the constitution compliance `@import`) and, via `CodexIntegration`, maintains the AGENTS.md `<!-- CODEXSPEC START/END -->` managed block. The new profile block reuses these injection points and their idempotent, non-destructive discipline.
- `distill` continues to own profile writes and keeps its contract of not touching other tracked files; nothing in this feature makes distill write to context files.

## Dependencies

- `src/codexspec/__init__.py` init flow (CLAUDE.md creation/compliance-import; profile scaffold creation; managed-block injection).
- `src/codexspec/integrations/codex.py` (`CodexIntegration.ensure_context_file` / `_context_section`) for the AGENTS.md managed block.
- `templates/commands/specify.md` for the B-layer read.
- Existing `.codexspec/profile/` store written by `distill` (referenced, not modified here).
- Release tail: derived-artifact regeneration via publish → init; tests for init/integration behavior.

## Requirements Traceability

| Confirmed Entry | Spec Coverage | Notes |
|-----------------|---------------|-------|
| NEED-001 | Context/Goals; US1–US3 | Local consumption capability |
| NEED-002 | REQ-001, REQ-002; US1 | Ambient injection at init |
| NEED-003 | REQ-001; US1 | Both CLAUDE.md and AGENTS.md |
| NEED-004 | REQ-005; US3 | specify-only read |
| NEED-005 | REQ-003, REQ-004; US2 | Unconditional inject + scaffold, immediate effect |
| CON-001 | NFR-001 | templates/ + src/ only; self-bootstrap |
| CON-002 | NFR-003; OUT-001 | Constitution untouched |
| CON-003 | REQ-005 (last sentence); Out of Scope | Downstream doesn't read profile |
| CON-004 | NFR-002 | Constant ambient footprint |
| CON-005 | REQ-003 | Idempotent, non-destructive block |
| DEC-001 | (superseded by DEC-006) | Constraints guaranteed — reversed |
| DEC-006 | REQ-002, REQ-006, NFR-002 | Uniform pointer block, no @import |
| DEC-007 | REQ-004, REQ-008, SC-006 | One-file-per-record store |
| DEC-002 | REQ-005 | B-layer only in specify |
| DEC-003 | REQ-007 | No vetted filter for local use |
| DEC-004 | REQ-003, REQ-004; US2 | Unconditional inject + scaffold |
| DEC-005 | (superseded by DEC-006) | Channel-adaptive constraints — reversed to uniform pointer |
| OUT-001 | OUT-001; NFR-003 | No constitution changes |
| OUT-002 | OUT-002; NFR-003 | No evolve changes |
| OUT-003 | OUT-003 | No metric optimization |
| OPEN-001 | Open Questions; NFR-004 | Non-blocking; design independent of it |
| OPEN-003 | Open Questions | Wording, non-blocking |
