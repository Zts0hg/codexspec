# Design Document: distill Effectiveness Upgrade

## Context

Realizes `spec.md` for feature `2026-0814-1548g5-distill-effectiveness`. The
change extends CodexSpec's profile subsystem along four axes — representation
(D3), retrieval (D1), consolidation (D2), and the trigger surface (D5) — while
preserving the store's HARD invariants: conflict-free one-record-per-file storage
(CON-001/NFR-001) and non-blocking, judgment-driven behavior (CON-002/NFR-002).

The subsystem has exactly two moving parts today, and both are reused rather than
replaced:

- **`src/codexspec/profile.py`** — `PROFILE_CATEGORIES` (single source of truth
  for both the scaffold and the rendered block), the rendered managed block
  (`_PROFILE_BLOCK` / `render_profile_block`), and the idempotent injector
  (`inject_profile_block`, already using the safe `re.sub(lambda …)` form).
- **`templates/commands/distill.md`** — the canonical record-format + operating
  discipline document; `onboard.md` / `evolve.md` / `specify.md` reference it.

No new module, no new command, no runtime state store, no central index is
introduced. All behavior changes are expressed as (a) a small Python edit to the
single-source category tuple + rendered block, and (b) template discipline text.

## Architecture & Components

### C1 — Store category expansion (6 categories)

`PROFILE_CATEGORIES` in `profile.py` gains `"strategies"` and `"runbooks"`,
appended after `decisions` (ordering: `constraints` stays first as highest
weight). Because this tuple drives both `ensure_profile_scaffold` (directory +
`.gitkeep`) and the rendered block, one edit scaffolds the two new directories and
lists them in the pointer block. `ensure_profile_scaffold` is already idempotent,
so re-`init` adds the two directories to existing (brownfield) projects with no
manual step and never touches existing records.

- Covers: REQ-001, REQ-012, NFR-003, and the migration path noted in review-spec.

### C2 — Record representation: strategies & runbooks bodies

`distill.md` documents the two new categories and their structured anti-hollow
bodies, reusing the existing record format verbatim (claim/evidence separated, id
namespaced by source-feature id, `status`, `scope/when`, `provenance`):

- **strategy** record MUST spell out **trigger**, **action**, **evidence**. The
  self-model is a strategy marked `scope: self` (no seventh directory).
- **runbook** record MUST spell out ordered **steps**, explicit
  **failure-recovery** branch(es), **evidence**.
- A strategy/runbook whose required parts cannot be stated is not recorded (same
  anti-hollow rule already applied to pitfalls' root-cause/workaround/lesson).
Two worked examples (one strategy, one runbook) are added alongside the existing
convention and pitfall examples.
- Covers: REQ-002, REQ-003, REQ-004, CON-003.

### C3 — Active retrieval framing in the ambient block

`_PROFILE_BLOCK` is reworked from passive "consult on demand" to an active
recall instruction: *before non-trivial work, scan the `scope/when` (and, for
strategies, `trigger`) lines across the relevant category directories and read the
records whose signature matches the current task.* The two new categories are
added as pointers (`strategies/`, `runbooks/`), constraints stays the mandatory
first pointer. The instruction is a fixed-size runtime directive — it names the
directories and the matching procedure, never inlines records — so the
always-loaded footprint stays constant regardless of profile size.

- Covers: REQ-005, NFR-004, CON-001, CON-007.

### C4 — Near-moment distill trigger rule in the ambient block

The same managed block gains a terse write-side rule (read/write are two halves
of one profile-consumption concern; see Decision 1): *when this session produces
reusable cross-feature knowledge — even in plain chat or a non-SDD fix — run
`/codexspec:distill` near that moment; it is non-blocking and early-exits when
there is nothing new.* Injected only into CLAUDE.md/AGENTS.md following
`project.ai` (never constitution.md), via the existing idempotent injector.

- Covers: REQ-007, DEC-006, NFR-005, CON-009.

### C5 — distill operating model: near-moment + long-run + backstop

`distill.md`'s Operating Model is extended: besides the three wrap-up hooks,
distill may be invoked near-moment in any session (driven by C4). In a
long-running `implement-tasks`, distillation happens along the way near each
knowledge-producing event; the end-of-task `auto_distill` remains a backstop. No
milestone-forced loop is hard-coded into `implement-tasks` (the ambient rule is
the driver).

- Covers: REQ-008, DEC-007.

### C6 — Debounce / session-boundary discipline

`distill.md` gains a debounce discipline: distill maintains a **session-local
already-distilled boundary** in conversation context (no persistent runtime
state); on overlapping/consecutive triggers it processes only the substantive new
delta and lightly early-exits when nothing is new. Across sessions (no shared
context) it falls back to the existing read-profile dedup. This makes consecutive
`implement → commit → pr` plus near-distillation and the backstop non-duplicating.

- Covers: REQ-009, CON-009, NFR-002.

### C7 — Consolidation capability

`distill.md` gains a consolidation section: on a run distill may **mark** clusters
of narrow related records as consolidation candidates by writing a
**per-record field** (e.g. `consolidation: candidate; cluster: <theme-key>`) into
each member's own file — no central list, preserving conflict-free storage
(Decision 2). It never auto-rewrites or deletes. `/distill review` gains a step
that surfaces marked clusters and, on human confirmation, merges them into one
general record ("general rule + exceptions"), supporting cross-category promotion
(e.g. several `pitfalls` → one `strategy`) and removing the superseded members via
the existing `remove` mutation.

- Covers: REQ-006, DEC-003, CON-005, CON-001.

### C8 — onboard exclusion extension

`onboard.md`'s "never extracts `decisions` or `pitfalls`" is extended to
"never `decisions`, `pitfalls`, `strategies`, or `runbooks`" (a cold code scan
cannot reliably infer experiential/metacognitive/procedural-experiential
knowledge); onboard still writes only `conventions` + narrow `constraints`.

- Covers: REQ-010, CON-004.

### C9 — evolve & specify category awareness

`evolve.md` recognizes `strategies`/`runbooks` as vetted-eligible material with the
vetted gate unchanged; `specify.md`'s "Consult Project Profile" enumeration adds
the two new categories so requirements-time consultation sees them too. Both are
small enumeration edits, not logic changes.

- Covers: REQ-011, CON-008; supporting REQ-005 (requirements-time read surface).

### C10 — Contract tests

`tests/` gains/updates: `profile.py` tests (scaffold makes 6 directories; block
lists the two new pointers, carries active-recall framing and the near-moment
trigger rule; injection stays idempotent and excludes constitution); `distill`
template-contract tests (new categories + bodies + examples, consolidation
section, debounce discipline); `onboard` template test (extended exclusion); and
any existing profile-category enumeration/count assertions updated in lockstep.

- Covers: verification for all REQ/NFR; NFR-003.

## Key Design Decisions

### Decision 1: One managed block carries both active recall and the near-moment trigger

- Context: REQ-005 (read side) and REQ-007 (write side) both target the ambient
  context files. The options were one combined block or two parallel blocks
  (`PROFILE` + a new `DISTILL` block).
- Decision: extend the **single existing** `<!-- CODEXSPEC PROFILE START/END -->`
  block. Reading the profile and distilling into it are two halves of the same
  profile-consumption concern; one bounded block means one injection path, one
  idempotency guarantee, and the smallest always-loaded footprint.
- Alternatives: a separate `DISTILL` managed block — rejected: a second
  injector/idempotency surface and marker pair for no semantic gain.
- Trade-offs: the block grows by a few fixed lines; acceptable under NFR-004
  (footprint is independent of profile size, which remains true).
- Covers: REQ-005, REQ-007, NFR-004, NFR-005, CON-009.

### Decision 2: Consolidation candidates are marked per-record, never in a central list

- Context: REQ-006 needs distill to flag clusters for later human-confirmed merge;
  CON-001 forbids anything that reintroduces merge conflicts.
- Decision: mark each cluster member by writing a field **inside that member's own
  record file**; `/distill review` discovers a cluster by scanning for the shared
  `cluster:` key. No index/manifest file is created.
- Alternatives: a `consolidation-queue.md` index — rejected: a single shared file
  is a merge-conflict magnet across parallel branches, violating CON-001.
- Trade-offs: discovering a cluster is an O(N) field scan at review time; N is
  small and this runs only in the interactive review, so it is acceptable.
- Covers: REQ-006, CON-001, CON-005.

### Decision 3: The debounce boundary lives in conversation context, not on disk

- Context: REQ-009/CON-009 require dedup across a widened trigger surface without a
  persistent runtime state store (CON-002).
- Decision: the "already-distilled boundary" is the agent's own
  conversation-context memory of what it has distilled this session; cross-session
  dedup falls back to the existing read-profile skip-covered judgment.
- Alternatives: a `.codexspec/.distill-state` marker file — rejected: introduces
  persistent runtime state and another non-versioned surface, against CON-002.
- Trade-offs: the boundary is lost when context is compacted; the read-profile
  dedup backstop covers that case (worst case: one extra early-exiting scan).
- Covers: REQ-009, CON-002, CON-009.

### Decision 4: Self-model is a strategy with `scope: self`, not a new category

- Context: DEC-001 confirmed six categories; self-model is metacognitive knowledge
  about the agent's own recurring failures.
- Decision: represent it as a `strategies/` record marked `scope: self`; a
  self-model is structurally a `trigger → action` rule whose trigger is
  self-referential.
- Trade-offs: none material; avoids a seventh directory and its lockstep cost.
- Covers: REQ-002, DEC-001.

## Risks & Trade-offs

- **Retrieval scan cost at scale (REQ-005).** Active recall reads record
  `scope/when` / `trigger` lines; at large N this is O(N) reads per task. Mitigation
  (planned as guidance, not an engine): match against the compact heading/`scope`
  lines first and read full records only on a hit. Consistent with
  judgment-not-algorithm (CON-002); no index is added (CON-001).
- **Debounce reliability (REQ-009).** "Substantive new delta" is a judgment; the
  discipline gives the agent a concrete boundary definition (records written +
  segment covered this session) to keep it dependable without persistent state.
- **Consolidation over-generalization.** Held by the human-in-the-loop gate
  (CON-005): distill only marks; merges happen on explicit confirmation in
  `/distill review`.

## Requirements Coverage

| Requirement | Design coverage |
|---|---|
| REQ-001 (6-category store, single source) | C1 |
| REQ-002 (strategy body; self-model scope:self) | C2, Decision 4 |
| REQ-003 (runbook body) | C2 |
| REQ-004 (reuse format + anti-hollow) | C2 |
| REQ-005 (active ambient retrieval) | C3, Decision 1; risk noted |
| REQ-006 (consolidation mark + confirm) | C7, Decision 2 |
| REQ-007 (near-moment trigger injection) | C4, Decision 1 |
| REQ-008 (long-run + backstop) | C5 |
| REQ-009 (debounce/dedup) | C6, Decision 3 |
| REQ-010 (onboard exclusion) | C8 |
| REQ-011 (evolve vetted-only) | C9 |
| REQ-012 (no facts/) | C1 |
| NFR-001 (conflict-free) | C1, C7, Decision 2 |
| NFR-002 (non-blocking/judgment) | C6, C7, Decision 3; risks |
| NFR-003 (self-bootstrap) | C1, C10 |
| NFR-004 (fixed ambient footprint) | C3, Decision 1 |
| NFR-005 (idempotent bounded block, no constitution) | C4, Decision 1 |

## Assumptions

- The CLAUDE.md/AGENTS.md profile block in this repo is the init-regenerated
  managed block (verified: its text matches `_PROFILE_BLOCK`), so it is updated by
  editing `profile.py` + re-running `init`, never by hand (NFR-003). The
  hand-written architecture prose in CLAUDE.md is documentation, updated as a
  docs task, not a managed surface.
