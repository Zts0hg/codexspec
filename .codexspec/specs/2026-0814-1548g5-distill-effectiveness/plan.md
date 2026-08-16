# Implementation Plan: distill Effectiveness Upgrade

## Context

Implements the confirmed `design.md` for `2026-0814-1548g5-distill-effectiveness`.
The design is realized by editing exactly two real surfaces — `src/codexspec/profile.py`
(the single-source category tuple + rendered managed block) and
`templates/commands/distill.md` (canonical record-format + discipline) — plus
small enumeration edits to `onboard.md` / `evolve.md` / `specify.md`, a derived-form
regeneration, and contract tests. No new module, command, or runtime state.

## Goals / Non-Goals

**Goals**: deliver C1–C10 from `design.md` — 6-category store, strategy/runbook
representation, active ambient recall, near-moment trigger + long-run/backstop,
debounce, human-gated consolidation, onboard exclusion, evolve/specify awareness,
and contract tests.

**Non-Goals**: usage-outcome reinforcement (OUT-001), any eval/metrics/lint engine
(OUT-002), evolve vetted-gate logic / constitution / new commands (OUT-003), the
`create-new-feature.sh` ID bug (OUT-004). No re-architecture beyond `design.md`.

## Tech Stack

Python 3.11+ (profile.py), Markdown command templates, pytest contract tests, ruff.
All existing; nothing added.

## Plan-Level Decisions

### Decision 1: Build order — Python core → templates → derived regen last

- Decision: implement `profile.py` (C1/C3/C4) first, then all `templates/commands/`
  edits (C2/C5–C9), and regenerate derived `.claude/`·`.agents/` forms + re-render
  the CLAUDE.md/AGENTS.md managed block **once at the end** (C-regen).
- Rationale: derived regeneration must reflect the final template + block state;
  regenerating mid-way is wasted work and risks a stale-but-tracked artifact.
- Evidence: pitfall `P-2026-0812-2114vj-1` — derived forms are refreshed only by
  `init`; editing a template alone leaves them stale, so the regen is a required
  in-feature step, not a release-time catch-all.
- Trade-off: none material; the regen is a single deterministic command.

### Decision 2: Category expansion is a lockstep edit across code + tests + docs

- Decision: adding `"strategies"`/`"runbooks"` to `PROFILE_CATEGORIES` is done
  together with every site that enumerates the category set: `tests/test_profile.py:21`
  (`== {…}` exact-set assertion), `tests/test_init_profile.py:34` ("four category
  dirs" docstring / scaffold assertions), the `distill.md` store-layout list, and
  the `specify.md` "Consult Project Profile" enumeration.
- Rationale: the exact-set assertion in `test_profile.py` fails immediately on a
  partial edit; enumerating the sites up front prevents drift.
- Evidence: `PROFILE_CATEGORIES` is imported by both test files;
  `test_profile.py:21` asserts the full set literally.
- Trade-off: none; this is the established lockstep discipline (cf.
  `Con-2026-0811-1418yq-1`).

### Decision 3: Extend the existing distill contract-test file

- Decision: add new assertions to `tests/test_distill_template.py` (9 tests today)
  rather than create a parallel file.
- Rationale: co-locates all distill-template contract assertions; matches the
  existing `test_onboard_template.py` single-file-per-command pattern.
- Trade-off: none.

## Risks / Trade-offs

- **Substring-contract test fragility.** New assertions over `distill.md` prose
  must target emphasis-free spans (pitfall `P-2026-0813-1606fz-1`: markdown `**`
  inside an asserted phrase breaks naive substring tests).
- **Ambient block footprint.** The active-recall reframe + 2 new pointers + trigger
  rule must stay a fixed small directive (NFR-004); verify the rendered block does
  not inline records and its length is bounded.
- **onboard dual exclusion sites.** The exclusion must be extended at both
  `onboard.md:53` and `onboard.md:88` (review-design advisory).

## Implementation Phases

### Phase 1: Store core — profile.py (foundation)

- **P1.1** Add `"strategies"`, `"runbooks"` to `PROFILE_CATEGORIES` (after
  `decisions`; `constraints` stays first). Update the module docstring's "four
  category directories" wording to six. Covers: REQ-001, REQ-012, NFR-003; Design: C1.
- **P1.2** Rework `_PROFILE_BLOCK`: (a) reframe the on-demand section into an
  **active recall** directive (before non-trivial work, scan `scope/when` — and
  `trigger` for strategies — across the relevant category dirs and read matching
  records); (b) add `strategies/` and `runbooks/` pointers; keep `constraints`
  the mandatory first pointer; keep the block a fixed-size directive that never
  inlines records. Covers: REQ-005, NFR-004, CON-001, CON-007; Design: C3, Decision 1.
- **P1.3** Add the terse **near-moment distill trigger rule** to the same block
  (produce reusable cross-feature knowledge → run `/codexspec:distill` near that
  moment; non-blocking, early-exits). Covers: REQ-007, NFR-005; Design: C4, Decision 1.
- **P1.4** Update `ensure_profile_scaffold` docstring/behavior expectations to six
  dirs (loop already category-driven — no logic change, only doc + tests).
  Covers: REQ-001, NFR-003; Design: C1.
- **Verification**: `tests/test_profile.py` set assertion → six; `tests/test_init_profile.py`
  scaffold assertion + docstring → six; new assertions that the block contains the
  two new pointers, the active-recall framing, and the trigger rule, and that
  injection stays idempotent (existing test) and never targets constitution.md.

### Phase 2: distill.md — representation + discipline (core)

- **P2.1** Store-layout section: document `strategies/` and `runbooks/` categories.
  Covers: REQ-001, REQ-012; Design: C2.
- **P2.2** Record-format: define the strategy anti-hollow body (**trigger / action /
  evidence**) and self-model `scope: self`; define the runbook body (ordered
  **steps / failure-recovery / evidence**); state that an unstatable triple is not
  recorded. Add one strategy example and one runbook example alongside the existing
  convention/pitfall examples. Covers: REQ-002, REQ-003, REQ-004, CON-003; Design: C2, Decision 4.
- **P2.3** Operating Model: add near-moment invocation in any session + long-run
  along-the-way distillation with end `auto_distill` backstop. Covers: REQ-008; Design: C5.
- **P2.4** Debounce discipline: session-local already-distilled boundary in
  conversation context (no persistent state), delta-only, light early-exit;
  cross-session read-profile fallback. Covers: REQ-009, CON-009, NFR-002; Design: C6, Decision 3.
- **P2.5** Consolidation: distill **marks** clusters via a per-record
  `cluster:`/`consolidation:` field (no central index; non-destructive); add a
  `/distill review` merge step that, on confirmation, merges into "general rule +
  exceptions" (cross-category promotion allowed) and `remove`s superseded members
  incl. the transient marker. Covers: REQ-006, CON-005, CON-001; Design: C7, Decision 2.
- **Verification**: extend `tests/test_distill_template.py` — assert new categories
  documented, both anti-hollow bodies + examples present, operating-model additions,
  debounce discipline, consolidation section + per-record marker + review merge step;
  all assertions target emphasis-free spans.

### Phase 3: Peripheral template enumeration edits

- **P3.1** `onboard.md`: extend the exclusion at **both** line 53 and line 88 to
  "never `decisions`, `pitfalls`, `strategies`, `runbooks`". Covers: REQ-010, CON-004; Design: C8.
- **P3.2** `evolve.md`: note `strategies`/`runbooks` are vetted-eligible material;
  vetted gate unchanged. Covers: REQ-011, CON-008; Design: C9.
- **P3.3** `specify.md`: add `strategies`/`runbooks` to the "Consult Project Profile"
  enumeration. Covers: REQ-005 (requirements-time read surface); Design: C9.
- **Verification**: `tests/test_onboard_template.py` exclusion assertion updated to
  the extended phrase (emphasis-free span); existing specify/evolve tests still green.

### Phase 4: Derived regeneration + dogfood (self-bootstrap)

- **P4.1** Run `uv run codexspec init . --force --ai both` to regenerate
  `.claude/commands/codexspec/{distill,onboard,evolve,specify}.md` and
  `.agents/skills/codexspec-*/SKILL.md`, and re-render the CLAUDE.md/AGENTS.md
  managed profile block from the edited `profile.py`. Covers: NFR-003; Design: C-regen (C1/C3/C4 propagation).
- **Verification**: `git status` shows only the intended derived + source changes;
  `config.yml` unchanged (auto_next/auto_distill/language/project.ai preserved);
  managed block in CLAUDE.md/AGENTS.md now carries the six pointers + active recall +
  trigger rule; constitution.md untouched.

### Phase 5: Integration verification

- **P5.1** `uv run ruff check src/ tests/` → 0. Covers: NFR-003.
- **P5.2** `uv run pytest -q` full suite green (no regression from the current
  baseline). Covers: verification for all REQ/NFR; Design: C10.
- **Verification**: full suite + ruff clean; profile-category enumeration lockstep
  confirmed consistent across code, tests, and docs.

## Requirements Coverage

| Requirement | Plan Phase(s) | Design |
|---|---|---|
| REQ-001 (6-category store) | P1.1, P1.4, P2.1 | C1 |
| REQ-002 (strategy body; scope:self) | P2.2 | C2, D4 |
| REQ-003 (runbook body) | P2.2 | C2 |
| REQ-004 (reuse format + anti-hollow) | P2.2 | C2 |
| REQ-005 (active ambient retrieval) | P1.2, P3.3 | C3 |
| REQ-006 (consolidation mark + confirm) | P2.5 | C7, D2 |
| REQ-007 (near-moment trigger injection) | P1.3 | C4, D1 |
| REQ-008 (long-run + backstop) | P2.3 | C5 |
| REQ-009 (debounce/dedup) | P2.4 | C6, D3 |
| REQ-010 (onboard exclusion, both sites) | P3.1 | C8 |
| REQ-011 (evolve vetted-only) | P3.2 | C9 |
| REQ-012 (no facts/) | P1.1, P2.1 | C1 |
| NFR-001 (conflict-free) | P1.2, P2.5 | C1, C7, D2 |
| NFR-002 (non-blocking/judgment) | P2.4, P2.5 | C6, D3 |
| NFR-003 (self-bootstrap) | P1.1, P4.1, P5.1 | C1, C10 |
| NFR-004 (fixed ambient footprint) | P1.2 | C3, D1 |
| NFR-005 (idempotent block, no constitution) | P1.3, P4.1 | C4, D1 |

## Assumptions

- `tests/test_distill_template.py` and `tests/test_onboard_template.py` are the
  canonical contract-test homes (verified present); new assertions extend them.
- The current full-suite baseline is green before this feature starts; Phase 5
  must not regress it.
