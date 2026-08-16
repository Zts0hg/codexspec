# Feature Specification: distill Effectiveness Upgrade

**Feature Branch**: `2026-0814-1548g5-distill-effectiveness`
**Created**: 2026-08-16
**Status**: Draft
**Input**: Confirmed `requirements.md` (NEED-001..005, DEC-001..007, CON-001..009, OUT-001..004)

## Context & Goals

`distill` is the write side of CodexSpec's self-evolution base; its purpose is
**cross-cycle agent capability growth**. Examined through the lens of how humans
grow (factual / procedural-experiential / metacognitive knowledge), the current
design has five defects. This feature fixes four — **representation (D3),
retrieval (D1), consolidation (D2), and the trigger surface (D5)** — and defers
usage-outcome reinforcement (D4).

The store today is four category directories (`constraints/`, `conventions/`,
`pitfalls/`, `decisions/`), one record per file, consumed by CLAUDE.md and
AGENTS.md through an identical pointer block (no `@import`), written by `distill`
and (for a narrow slice) `onboard`. This feature extends the store to six
categories, changes the ambient consumption from passive to active recall, adds a
human-in-the-loop consolidation capability, and widens + deduplicates the
auto-trigger surface — all without breaking the store's conflict-free,
non-blocking, judgment-driven character.

## User Scenarios

### User Story 1 — Procedural & metacognitive knowledge finds a fitting home (Priority: P1)

The agent finishes a piece of work that produced a multi-step procedure (e.g. the
release flow) or a `trigger → action` rule (e.g. "substring contract test failed
→ suspect markdown emphasis"). Today the procedure is crushed into a one-line
`convention` and the rule is buried under one specific `pitfall`. After this
feature, the procedure is a `runbooks/` record with ordered steps + failure
recovery, and the rule is a `strategies/` record with trigger/action.

**Independent Test**: distill a segment containing a multi-step procedure and a
conditional rule; verify a `runbooks/` record with ordered steps + failure branch
and a `strategies/` record with trigger/action are written, each with the
anti-hollow triple present.

**Acceptance Scenarios**:

1. **Given** a segment describing an ordered procedure with a failure-recovery
   step, **When** distill runs, **Then** a `runbooks/<id>.md` record is written
   with steps, failure-recovery, and evidence.
2. **Given** a segment describing a "when I see signal X, do Y" rule, **When**
   distill runs, **Then** a `strategies/<id>.md` record is written with trigger,
   action, and evidence.
3. **Given** a rule about the agent's own recurring failure, **When** distill
   runs, **Then** it is written as a `strategies/` record marked `scope: self`.
4. **Given** a candidate strategy/runbook whose triple cannot be fully stated,
   **When** distill evaluates it, **Then** it is not recorded (anti-hollow).

### User Story 2 — The right knowledge surfaces at the right moment (Priority: P1)

Across many features the store grows to dozens of records. When the agent starts
non-trivial work in any session, it actively matches the task against records'
own `trigger`/`scope` fields and pulls the relevant ones, instead of passively
hoping to remember to look.

**Independent Test**: with a populated profile, start a task whose signature
matches a record's `trigger`/`scope`; verify the ambient guidance directs an
active scan-and-pull of that record, driven only by record-carried fields (no
central index file exists).

**Acceptance Scenarios**:

1. **Given** a populated profile and a task matching a record's `scope`/`trigger`,
   **When** the agent begins work in a plain-chat / implement / debug session,
   **Then** the ambient rule directs it to actively recall the matching record.
2. **Given** the store grows large, **When** the ambient block is loaded, **Then**
   its always-loaded footprint stays a fixed small size (recall is a runtime scan,
   not an inlined dump).
3. **Given** the retrieval mechanism, **When** inspected, **Then** no central
   index/manifest file is introduced; matching scans per-record fields only.

### User Story 3 — Narrow records consolidate into general rules (Priority: P2)

Over time several narrow records about the same theme accumulate. distill flags
them as a consolidation candidate cluster; during `/distill review` the human
confirms merging them into one general rule plus exceptions, including promoting
several `pitfalls` into one `strategy`.

**Independent Test**: seed several narrow related records; run distill and verify
it marks a consolidation candidate cluster without rewriting them; run
`/distill review` and verify the human can confirm the merge into general
rule + exceptions.

**Acceptance Scenarios**:

1. **Given** several narrow records on one theme, **When** distill runs, **Then**
   it marks them as a consolidation candidate cluster and does not auto-rewrite or
   delete any of them.
2. **Given** marked consolidation candidates, **When** the human runs
   `/distill review`, **Then** they can confirm the merge into a general
   rule + exceptions, and only then are records changed.
3. **Given** a cluster of several `pitfalls` sharing a generalization, **When**
   consolidation is confirmed, **Then** cross-category promotion to a `strategy`
   is supported.

### User Story 4 — distill triggers when and only as often as it should (Priority: P1)

The agent produces reusable knowledge in a plain-chat / non-SDD fix, or midway
through a long-running `implement-tasks`. distill fires near that moment, not only
at wrap-up commands and not lost to context compaction. Across the widened
surface (near-distillation, end backstop, `implement → commit → pr`), overlapping
triggers do not re-distill or produce near-duplicate records.

**Independent Test**: (a) a plain-chat fix produces a reusable convention →
verify the ambient rule directs a near-moment distill; (b) simulate consecutive
triggers over the same segment → verify only the first does substantive work and
the rest lightly early-exit.

**Acceptance Scenarios**:

1. **Given** a plain-chat / non-SDD fix that produced reusable cross-feature
   knowledge, **When** the work reaches a natural point, **Then** the ambient rule
   directs the agent to distill near that moment (not only at wrap-up commands).
2. **Given** a long-running `implement-tasks`, **When** reusable knowledge is
   produced mid-task, **Then** distill happens along the way near the event, with
   the end-of-task `auto_distill` retained as a backstop.
3. **Given** consecutive `implement → commit → pr` triggers plus near-distillation
   over the same work, **When** they fire, **Then** only the substantive new delta
   is distilled and later triggers lightly early-exit — no re-distillation, no
   near-duplicate records.
4. **Given** the injected trigger rule, **When** injection runs, **Then** it lands
   as an idempotent bounded managed block in CLAUDE.md/AGENTS.md following
   `project.ai`, and never in constitution.md.

## Functional Requirements

- **REQ-001** — The profile store gains two first-class category directories,
  `strategies/` and `runbooks/`, for six categories total. `PROFILE_CATEGORIES`
  in `src/codexspec/profile.py` is the single source of truth for both the
  scaffold (directory + `.gitkeep`) and the rendered ambient block; both new
  categories are scaffolded and appear in the pointer block.
  Sources: NEED-002, DEC-001, CON-006, CON-007
- **REQ-002** — A `strategies/` record captures a metacognitive `trigger → action`
  rule with a structured anti-hollow body: **trigger**, **action**, and
  **evidence** must all be present. The self-model (knowledge about the agent's
  own recurring failure modes) is a `strategies/` record marked `scope: self`; no
  separate directory is added for it.
  Sources: NEED-002, DEC-001, CON-003
- **REQ-003** — A `runbooks/` record captures an ordered multi-step procedure with
  a structured anti-hollow body: ordered **steps**, explicit **failure-recovery**
  branch(es), and **evidence** must all be present.
  Sources: NEED-002, DEC-001, CON-003
- **REQ-004** — The new categories reuse the existing record format verbatim
  (claim/evidence separated, ids namespaced by source-feature id,
  `status: candidate | vetted`, `scope/when`). An anti-hollow rule applies: a
  strategy/runbook whose required triple cannot be stated is not recorded.
  Sources: NEED-002, CON-003
- **REQ-005** — Ambient consumption changes from passive "read on demand" to
  active recall: before non-trivial work, the agent matches the current task
  signature against records' self-carried `trigger`/`scope` fields and pulls the
  relevant records. This applies to all sessions (plain chat, implement, debug).
  Matching scans per-record fields only and MUST NOT introduce a central index or
  manifest file.
  Sources: NEED-003, DEC-002, CON-001, CON-007
- **REQ-006** — `distill` gains a consolidation capability: on a run it may
  automatically identify and **mark** clusters of narrow records as consolidation
  candidates without auto-rewriting or deleting them; the human confirms the merge
  into "general rule + exceptions" during `/distill review`. Cross-category
  promotion (e.g. several `pitfalls` → one `strategy`) is supported.
  Sources: NEED-004, DEC-003, CON-005
- **REQ-007** — A behavior rule for near-moment distillation is injected into the
  ambient context files (CLAUDE.md and/or AGENTS.md, following `project.ai`),
  reusing the existing managed-block infrastructure, as an idempotent bounded
  block. It is NOT injected into constitution.md. The rule directs the agent to
  distill near the moment reusable cross-feature knowledge is produced, in any
  session including plain-chat / non-SDD fixes.
  Sources: NEED-005, DEC-006, CON-009
- **REQ-008** — Long-run timeliness: in a long-running `implement-tasks`, distill
  happens along the way near each event rather than only at the very end; the
  end-of-task `auto_distill` remains as a backstop. No milestone-forced
  incremental mechanism is hard-coded into `implement-tasks`.
  Sources: NEED-005, DEC-007
- **REQ-009** — De-duplication / debounce across the widened trigger surface:
  distill maintains a session-local "already-distilled boundary" via conversation
  context (introducing no persistent runtime state); on overlapping or consecutive
  triggers it processes only the substantive new delta and lightly early-exits
  when there is nothing new. Across sessions it falls back to the existing
  read-profile dedup. Consecutive `implement → commit → pr` plus near-distillation
  and the end backstop must not re-distill or produce near-duplicate records.
  Sources: NEED-005, CON-009
- **REQ-010** — `onboard` never writes `strategies` or `runbooks` (same reasoning
  as its existing "never decisions/pitfalls"); it still writes only `conventions`
  - narrow `constraints`. Its documentation is updated to state the extended
  exclusion.
  Sources: CON-004
- **REQ-011** — `evolve` still compiles only `vetted` records; `strategies` and
  `runbooks` are eligible evolve candidates once vetted, but the vetted gate is
  unchanged.
  Sources: CON-008
- **REQ-012** — No `facts/` category is added. The category set is exactly
  `constraints, conventions, pitfalls, decisions, strategies, runbooks`.
  Sources: DEC-005

## Non-Functional Requirements

- **NFR-001** — Conflict-free storage is preserved: one record per file,
  differently-named files per branch, git as the ledger, zero merge conflict.
  Neither retrieval (REQ-005) nor consolidation (REQ-006) introduces a central
  index/manifest.
  Sources: CON-001
- **NFR-002** — Non-blocking / judgment-not-algorithm is preserved: distill stays
  non-blocking and non-interactive; retrieval, consolidation, and near-moment
  distillation are judgment-driven, not deterministic algorithms or heavy engines.
  Sources: CON-002
- **NFR-003** — Self-bootstrap: changes are made in `templates/commands/` and
  `src/codexspec/profile.py`; derived `.claude/commands/codexspec/` and
  `.agents/skills/codexspec-*/` forms are regenerated by `codexspec init`, never
  hand-edited.
  Sources: CON-006
- **NFR-004** — The always-loaded ambient block stays a fixed small size and does
  not grow with profile size; active recall is a runtime on-demand scan.
  Sources: CON-007
- **NFR-005** — The trigger-rule injection is an idempotent, bounded managed block
  (same mechanism as the profile block); re-injection does not duplicate or drift,
  and it never touches constitution.md.
  Sources: CON-009

## Expected Error / Boundary Behavior

- An empty or absent profile degrades silently: active recall finds nothing and
  does not block; the scaffold ensures all six category directories exist so every
  pointer resolves.
- A consolidation candidate the human does not confirm leaves all source records
  untouched (marking is non-destructive).
- When there is nothing new since the session's already-distilled boundary, a
  trigger early-exits without deep-reading the profile.
- Injection into a file that already contains the managed block replaces the block
  in place (idempotent), never appends a second copy.

## Confirmed Constraints & Decisions

All CON-001..009 and DEC-001..007 from `requirements.md` are binding. Highlights:
conflict-free store (CON-001) and non-blocking/judgment (CON-002) are HARD
constraints; the store is exactly six categories with self-model as
`strategies/ scope:self` (DEC-001, DEC-005); retrieval is ambient-global
(DEC-002); consolidation is hybrid-triggered (DEC-003); trigger injection excludes
constitution.md (DEC-006); long-run timeliness is event-driven + end backstop
(DEC-007).

## Out of Scope

- **OUT-001** — Usage-outcome reinforcement / decay (hit-rate, utility counters,
  automatic staleness decay) — deferred (conflicts with conflict-free store; most
  prone to degenerating into unfalsifiable counting).
- **OUT-002** — No eval / metrics / GEPA / engineered lint engine.
- **OUT-003** — No change to evolve's vetted-gate logic, no constitution change,
  no new command.
- **OUT-004** — The `create-new-feature.sh` legacy sequential-ID bug is not fixed
  here (recorded separately).

## Traceability

| Requirements entry | Spec coverage |
|---|---|
| NEED-001 (cross-cycle growth goal) | Context & Goals; realized transitively by REQ-001..009 |
| NEED-002 (represent runbooks/strategies) | REQ-001, REQ-002, REQ-003, REQ-004; US1 |
| NEED-003 (active retrieval) | REQ-005; US2 |
| NEED-004 (consolidation) | REQ-006; US3 |
| NEED-005 (trigger surface: a/b/c) | REQ-007, REQ-008, REQ-009; US4 |
| DEC-001 (6 categories, self-model scope:self) | REQ-001, REQ-002 |
| DEC-002 (ambient-global retrieval) | REQ-005 |
| DEC-003 (hybrid consolidation) | REQ-006 |
| DEC-004 (scope: fix D1/D2/D3/D5, defer D4) | Context & Goals; Out of Scope OUT-001 |
| DEC-005 (no facts/) | REQ-012 |
| DEC-006 (inject CLAUDE/AGENTS, not constitution) | REQ-007; NFR-005 |
| DEC-007 (event-driven + end backstop) | REQ-008 |
| CON-001 (conflict-free) | NFR-001; REQ-005, REQ-006 |
| CON-002 (non-blocking/judgment) | NFR-002 |
| CON-003 (format + anti-hollow triple) | REQ-002, REQ-003, REQ-004 |
| CON-004 (onboard exclusion) | REQ-010 |
| CON-005 (consolidation marks only) | REQ-006 |
| CON-006 (self-bootstrap) | NFR-003; REQ-001 |
| CON-007 (fixed ambient footprint) | NFR-004; REQ-005 |
| CON-008 (evolve reads vetted) | REQ-011 |
| CON-009 (idempotent block + dedup) | REQ-007, REQ-009; NFR-005 |
| OUT-001..004 | Out of Scope |

## Open Questions

None blocking. Task-signature match granularity is a design-stage detail; the
direction (scan per-record fields, judgment-based, no central index) is settled.
