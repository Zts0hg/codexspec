# Requirements: distill Effectiveness Upgrade

Feature ID: `2026-0814-1548g5`
Feature directory: `.codexspec/specs/2026-0814-1548g5-distill-effectiveness/`

## Overview

`distill` is the write side of CodexSpec's self-evolution base: its purpose is
**cross-cycle agent capability growth** — accumulating reusable, cross-feature
knowledge so the agent gets better over time rather than re-hitting the same
traps and re-litigating the same decisions each session.

Reviewed through the lens of how humans grow (factual, procedural/experiential,
and metacognitive knowledge), the current design has five defects. **This
feature fixes four of them — retrieval, consolidation, representation, and the
trigger surface — and explicitly defers the fifth (usage-outcome
reinforcement).** The overriding priority is **effectiveness of the outcome, not
minimal code change** (per the user's explicit direction).

The store today has four category directories (`constraints/`, `conventions/`,
`pitfalls/`, `decisions/`), one record per file, consumed by both CLAUDE.md and
AGENTS.md through an identical pointer block (no `@import`), and written by
`distill` (and, for a narrow slice, `onboard`).

## Diagnosed defects (context)

- **D1 — Retrieval paradox (fixed here):** knowledge is filed by the situation
  that triggers it, but retrieval depends on the agent already recognizing that
  situation — the very capability the record was meant to supply. Records carry
  a `scope/when` field, yet nothing on the read side uses it to filter. Only
  `specify` reads the profile, and it reads broadly.
- **D2 — No consolidation / generalization (fixed here):** the store only grows
  flat. There is no operation to compress N narrow records into one general rule
  plus exceptions, so over time it accumulates 60 narrow traps instead of 8
  mental models. `distill` can remember but cannot *learn* in the compression
  sense.
- **D3 — Record representation too flat (fixed here):** the record model is
  built for static assertions (`claim` + `evidence`). The two highest-value
  kinds of reusable knowledge are not assertions: **runbooks** (ordered,
  multi-step procedures with failure recovery) and **strategies** (metacognitive
  `trigger → action` rules, including a self-model about the agent's own
  recurring failures). Both exist already but are squashed into ill-fitting
  containers.
- **D4 — No reinforcement from usage outcomes (DEFERRED — see OUT-001).**
- **D5 — Trigger surface too narrow / untimely (fixed here):** `auto_distill`
  fires only on three wrap-up commands; plain-chat / non-SDD fixes never trigger
  it, and in a long-running `implement-tasks` the single end-of-task distillation
  loses mid-task evidence to context compaction.

---

## Needs (NEED)

### NEED-001 — Cross-cycle capability growth is the goal

- Statement: `distill` must actually deliver cross-cycle agent capability growth:
  compress one-off episodic experience into reusable general rules, and surface
  the right knowledge at the right moment, instead of piling records into a flat
  heap.
- Status: confirmed
- User Evidence: "我们使用distill的本质是为了跨越周期实现agent能力的增长，类似于人的成长。人的成长大多来源于知识，而知识大致分为三类：事实类知识 程序类/经验类知识 元认知类知识"; "我更希望 功能实现的效果好，而不是片面追求代码最小改动"

### NEED-002 — Represent runbooks and strategies as first-class knowledge (D3)

- Statement: The store gains two first-class category directories:
  - `strategies/` — metacognitive `trigger → action` rules. The **self-model**
    (knowledge about the agent's own recurring failure modes in this project)
    folds in as a strategy marked `scope: self`.
  - `runbooks/` — ordered multi-step procedures with explicit failure-recovery
    branches.
  Each has a structured body (see CON-003). This is the representation layer that
  D1 (retrieval) and D2 (consolidation) build on.
- Status: confirmed
- User Evidence: "认同\"runbook 形态、strategy 形态值得被单独表征\"。我们现在来讨论具体的文件存放结构，不要等到design"
- Supporting evidence (live samples in this repo's own profile): `Con-2026-0811-1418yq-1`
  is a multi-step lockstep **runbook** crushed into a single run-on `convention`
  sentence; the `lesson` lines of `P-2026-0811-1418yq-1` and `P-2026-0813-1606fz-1`
  are transferable **strategies** buried under one specific pitfall each.

### NEED-003 — Active retrieval on the ambient consumption side (D1)

- Statement: Change ambient consumption from passive "read on demand" to active:
  before starting non-trivial work, the agent matches the current task's
  signature against records' own `trigger` / `scope` fields and pulls the
  relevant records. This applies to **all sessions** (plain chat, `implement`,
  `debug`), because the retrieval paradox bites in day-to-day implement/debug,
  not in `specify`. Matching scans the records' self-carried fields; it must not
  build a central index (see CON-001).
- Status: confirmed

### NEED-004 — Consolidation with human-in-the-loop confirmation (D2)

- Statement: `distill` gains a consolidation capability. On each run it may
  **automatically identify and mark** clusters of narrow records as
  consolidation candidates (it does not auto-rewrite them); the human confirms
  the merge into "general rule + exceptions" during `/distill review`.
  Cross-category promotion is supported (e.g. several `pitfalls` → one
  `strategy`). Consolidation stays judgment-driven, not an algorithm (CON-002).
- Status: confirmed

### NEED-005 — Complete and de-duplicate the auto-trigger surface (D5)

- Statement: Complete `distill`'s automatic triggering along three points:
  - **(a) Ambient global trigger:** an injected behavior rule makes the agent
    distill **near the moment** reusable cross-feature knowledge is produced, in
    **any session** — including plain-chat / non-SDD adjustments and fixes — not
    only inside the three wrap-up commands.
  - **(b) Long-run timeliness:** in a long-running `implement-tasks`, distill
    **along the way, near each event**, rather than once at the very end;
    end-of-task `auto_distill` remains as a backstop. This avoids losing mid-task
    evidence to context compaction.
  - **(c) De-duplication / debounce across the widened trigger surface:** distill
    keeps a session-local "already-distilled boundary" awareness; on overlapping
    or consecutive triggers it processes only the substantive new delta and
    lightly early-exits when there is nothing new; across sessions it falls back
    to read-profile dedup.
- Status: confirmed
- User Evidence (b): "在长程的impletement-tasks任务中因为从任务开始到任务完成跨度较大导致distill不及时。如果不是sdd流程或者是implement-tasks结束之后单独直接对话做出的调整和修复也不能触发distill，我们需要在这次优化distill中也把自动化机制也完善"
- User Evidence (a): "在 init 的时候将 distill 命令的使用 注入 CLAUDE.md / AGENT.md ... 中" (constitution.md excluded — see DEC-006)
- User Evidence (c): "另外 implement-tasks 和 commit-staged 都会触发distill，是否需要考虑避免重复冗余触发？"

---

## Decisions (DEC)

### DEC-001 — Store final shape is 6 categories

- Decision: Add `strategies/` and `runbooks/` to the existing four, for six
  category directories total. The self-model is a `strategies/` record with
  `scope: self` (no seventh directory).
- Status: confirmed
- Rationale: `strategies/` is near-forced — it is orthogonal to all four existing
  categories, and both D1 retrieval (recall by signal) and D2 consolidation
  (pitfalls → strategy is the generalization target) require "strategy" to be a
  separately addressable set. `runbooks/` earns its own directory for the same
  reason `pitfalls` is distinct from `conventions`: distinct usage (executed
  step-by-step, has failure branches, surfaced whole at task start) and it is a
  named consolidation target (scattered release fragments → one ordered runbook).

### DEC-002 — Active retrieval applies ambient-globally

- Decision: The active recall in NEED-003 is wired into the ambient consumption
  layer for all sessions, not scoped to `specify` only.
- Status: confirmed

### DEC-003 — Consolidation uses hybrid triggering

- Decision: `distill` marks clusters as candidates automatically; the human
  confirms the merge in `/distill review`. Neither fully-automatic merging nor
  purely-manual discovery.
- Status: confirmed
- Rationale: automatic merging risks over-generalization into unfalsifiable
  platitudes (same root risk as the deferred D4); purely manual discovery of
  clusters almost never happens in practice.

### DEC-004 — Scope: fix D1/D2/D3/D5; defer D4

- Decision: This feature fixes retrieval (D1), consolidation (D2),
  representation (D3), and the trigger surface (D5). Usage-outcome reinforcement
  (D4) is out of scope (OUT-001).
- Status: confirmed

### DEC-005 — Do NOT add a `facts/` category

- Decision: No `facts/` directory. A bare fact with no "therefore do X" is
  rejected by distill's own requirements-as-truth boundary test and would turn a
  `facts/` directory into a dumping ground overlapping docs/decisions. Reusable
  facts land as a `convention`/`constraint` with an evidence anchor, or stay in
  user auto-memory.
- Status: confirmed
- Rationale: this is the deliberate outcome of examining the store through the
  "three kinds of knowledge" lens — the factual layer already has homes; only the
  procedural (runbook) and metacognitive (strategy) layers lacked a fitting one.

### DEC-006 — Trigger rule injection targets CLAUDE.md + AGENTS.md, excludes constitution.md

- Decision: The NEED-005(a) behavior rule is injected only into the ambient
  context files (CLAUDE.md and/or AGENTS.md, following `project.ai`), reusing the
  existing profile managed-block infrastructure. **constitution.md is excluded.**
- Status: confirmed
- Rationale: an end user's constitution is a governance baseline they customize
  themselves; injecting operational trigger instructions there is a level error
  (operational guidance ≠ governing principle), pollutes the governance document,
  and would conflict with the user's hand-edits on re-init. "When to distill" is
  an ambient behavior rule, naturally paired with the profile pointer block
  ("when to read the profile") — read/write two sides of the same block.

### DEC-007 — Long-run timeliness via event-driven near-distillation + end backstop

- Decision: Solve NEED-005(b) with an event-driven "distill near the moment"
  ambient rule plus the retained end-of-task `auto_distill` backstop. Do NOT hard-
  code milestone-forced incremental distillation into `implement-tasks`.
- Status: confirmed
- Rationale: event-driven near-distillation covers both plain-chat and long-run
  mid-task cases and fits the judgment-not-algorithm / non-blocking / pure-prompt
  architecture, without adding a heavy scheduling mechanism to `implement-tasks`.

---

## Constraints (CON)

### CON-001 — [HARD] Preserve conflict-free storage

- Constraint: The one-record-per-file, differently-named-files-per-branch,
  git-is-the-ledger, zero-merge-conflict store must not be broken. Retrieval
  (NEED-003) and consolidation (NEED-004) MUST NOT introduce a central index or
  manifest file — matching relies on records' self-carried `trigger` / `scope`
  fields.
- Status: confirmed
- User Evidence: "把解空间硬约束（conflict-free 一文件一记录存储、non-blocking/判断非算法）写进 CON"

### CON-002 — [HARD] Preserve non-blocking / judgment-not-algorithm character

- Constraint: `distill` stays non-blocking and non-interactive. Retrieval,
  consolidation, and near-distillation are all judgment-driven — not
  deterministic algorithms or heavy engines.
- Status: confirmed
- User Evidence: "把解空间硬约束（conflict-free 一文件一记录存储、non-blocking/判断非算法）写进 CON"

### CON-003 — Reuse record format + anti-hollow triple discipline for the new categories

- Constraint: `strategies/` and `runbooks/` reuse the existing record format
  (claim/evidence separated, ids namespaced by source-feature id,
  `status: candidate | vetted`) plus a structured anti-hollow discipline: a
  strategy must spell out **trigger / action / evidence**; a runbook must spell
  out **steps / failure-recovery / evidence**. If the parts cannot be stated, the
  item is not yet worth recording (mirrors the pitfall root-cause/workaround/
  lesson triple).
- Status: confirmed

### CON-004 — onboard does not write strategies/runbooks

- Constraint: `onboard` never extracts `strategies` or `runbooks` (same reasoning
  as its existing "never decisions/pitfalls": a cold code scan cannot reliably
  infer experiential or metacognitive knowledge). onboard still writes only
  `conventions` + narrow `constraints`.
- Status: confirmed

### CON-005 — Consolidation auto-part only marks candidates

- Constraint: The automatic part of consolidation only **marks** candidate
  clusters; it never auto-rewrites or deletes existing records. The merge is
  human-in-the-loop (holds the line against the same over-generalization risk as
  the deferred D4).
- Status: confirmed

### CON-006 — Self-bootstrap

- Constraint: Edit `templates/commands/` and `src/codexspec/profile.py`
  (`PROFILE_CATEGORIES` is the single source of truth for both the scaffold and
  the rendered block). Derived `.claude/commands/codexspec/` and
  `.agents/skills/codexspec-*/` forms are regenerated by `codexspec init`, never
  hand-edited.
- Status: confirmed

### CON-007 — Ambient always-loaded footprint stays fixed and small

- Constraint: Active recall is a runtime, on-demand scan performed before work.
  The always-loaded ambient block stays a fixed small size and does not grow with
  profile size.
- Status: confirmed

### CON-008 — evolve still reads only vetted

- Constraint: `evolve` still compiles only `vetted` records. `strategies` and
  `runbooks` are prime evolve candidates, but the vetted gate is unchanged.
- Status: confirmed

### CON-009 — Injection is an idempotent bounded managed block; triggering is deduplicated

- Constraint: The NEED-005(a) trigger rule is injected as an idempotent, bounded
  managed block (same mechanism as the profile block), excluding constitution.md.
  Beyond the existing "read current profile, skip covered" dedup, distill
  maintains a session-local already-distilled boundary (via conversation context,
  **introducing no persistent runtime state**) so that consecutive
  `implement → commit → pr` triggers plus near-distillation and the end backstop
  do not re-distill, do not produce near-duplicate records, and let later
  triggers lightly early-exit. Across sessions (no shared context), it falls back
  to read-profile dedup.
- Status: confirmed

---

## Out of Scope (OUT)

### OUT-001 — Usage-outcome reinforcement / decay (D4)

- Exclusion: Reinforcement or decay driven by usage outcomes (hit-rate, utility
  counters, automatic staleness decay) is deferred to a separate later feature.
- Status: confirmed
- Rationale: mutable per-record counters conflict HARD with the conflict-free
  one-record-per-file store (CON-001), and this is the defect most prone to
  degenerating into an unfalsifiable counting game / "divination-style"
  knowledge. Defer until it can be shown not to degrade.

### OUT-002 — No eval / metrics / GEPA / engineered lint engine

- Exclusion: No evaluation harness, scoring metric, GEPA, or engineered lint
  engine. Consolidation and anti-hollow checks stay judgment-based.
- Status: confirmed

### OUT-003 — Do not change evolve's vetted gate, the constitution, or add commands

- Exclusion: This feature does not alter evolve's vetted-gate logic, does not
  modify the constitution, and adds no new command (the work is store + format +
  distill/consumption template + profile.py changes).
- Status: confirmed

### OUT-004 — create-new-feature.sh legacy sequential-ID bug not fixed here

- Exclusion: `.codexspec/scripts/bash/create-new-feature.sh` still uses legacy
  sequential numbering and, against existing `2026-…` directories, treats the
  year as a counter and emits a garbage ID (it produced `2027` for this feature,
  corrected by hand to `2026-0814-1548g5`). Recorded as a separate bug; not fixed
  in this feature.
- Status: confirmed

---

## Open Questions (OPEN)

None blocking. The exact expression/granularity of the "task signature" match is
deferred to the design stage; the direction (scan records' self-carried fields,
judgment-based matching, no central index) is settled and non-blocking.

---

## Confirmation Log

- 2026-08-16 — User explicitly confirmed the full stage summary ("确认"). All
  NEED-001..005, DEC-001..007, CON-001..009, OUT-001..004 set to `confirmed`.
  Discussion spanned: knowledge-triptych lens on distill's purpose → diagnosis of
  five design defects → scope (fix D1/D2/D3/D5, defer D4) → 6-category store shape
  (+strategies +runbooks, self-model as scope:self) → ambient-global active
  retrieval → hybrid consolidation triggering → widened trigger surface
  (ambient-global near-distillation + long-run timeliness + end backstop, excl.
  constitution.md) → de-dup/debounce across the widened surface.
