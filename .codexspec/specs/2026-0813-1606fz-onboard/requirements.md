# Confirmed Requirements: onboard command

<!--
Language: document language = en (per .codexspec/config.yml). This file is the
authoritative, persistent record of user-confirmed intent. It does not copy the
full conversation. User Evidence quotes preserve the user's original words verbatim
(not translated), per the project convention.
-->

**Feature ID**: `2026-0813-1606fz`
**Status**: Discovery complete
**Last Confirmed**: 2026-08-13

## Authority Rules

- Only entries with `Status: confirmed` are binding downstream inputs.
- `open` entries MUST NOT be converted into confirmed product requirements.
- Replaced entries remain in this file with `Status: superseded` and a link to the replacement.
- AI inferences must be labeled as assumptions and require user confirmation before becoming binding.

## Summary

`onboard` is a standalone, user-invoked command that scans an existing codebase and
batch-writes reusable project knowledge that is **implicit in the code and not already
written down accessibly** into the shared `.codexspec/profile/` store. It is the
**cold-start / bulk counterpart to `distill`**: `distill` writes the profile incrementally
from interaction; `onboard` writes it in bulk from code. Its reliable extraction scope is
`conventions` (primary) plus a narrow, config-level `constraints`; it deliberately does
**not** mine `decisions` or `pitfalls`. Safety comes from a tiered gate — the bulk takes
effect immediately as `candidate` (reviewable later, asynchronously, via `/distill review`),
while the only high-risk category (`constraints`) passes a quick in-session human review
before it is persisted.

## Needs

### NEED-001: onboard as the cold-start / bulk profile writer

- **Status**: confirmed
- **Statement**: `onboard` scans an existing codebase and batch-writes reusable knowledge
  inferred **from the code itself** — knowledge that is implicit in the code and not already
  recorded accessibly — into `.codexspec/profile/` (the same store `distill` uses). It is the
  cold-start / bulk version of `distill` (distill = incremental from interaction; onboard =
  bulk from code).
- **Rationale**: A brownfield project's profile is empty until enough work has flowed through
  `distill`; onboard bootstraps it in one pass so accumulated project knowledge is grounded
  immediately.
- **User Evidence**: "onboard = distill 的冷启动/批量版"; direction confirmed across discussion.
- **Confirmed At**: 2026-08-13

### NEED-002: Output surface is profile-only

- **Status**: confirmed
- **Statement**: The output surface is exactly = `.codexspec/profile/` candidate records
  plus a terminal summary of what was written/updated this run. onboard produces no persistent
  document and performs no code walkthrough / explanation.
- **Rationale**: Keeps onboard pinned to the "profile cold-starter" definition with minimal
  surface and maintenance; a human-readable map or explanation, if ever wanted, is a separate
  future `explain` command.
- **User Evidence**: Q1 answer — "只写 profile(推荐)".
- **Confirmed At**: 2026-08-13

### NEED-003: Actual extraction scope = conventions + narrow constraints only

- **Status**: confirmed
- **Statement**: onboard actively extracts **`conventions`** (primary — including observable
  architecture / tech-stack facts, captured as fact + steering, not as ADR-style decisions) and
  a **narrow, config-level `constraints`**. It does **not** actively extract `decisions` or
  `pitfalls` (see OUT-001). The store still has four category directories (distill writes all
  four); onboard populates only these two.
- **Rationale**: Only these two have a reliable, non-redundant cold-scan source. Conventions are
  the observable regularities of the code (no marker needed). Config-level constraints exist in a
  machine-enforced, parseable form. `decisions`/`pitfalls` have no sweet spot: if documented they
  are redundant to copy; if undocumented they are unreliable (pitfalls are experiential; decision
  rationale would be fabricated).
- **User Evidence**: "本质上你OPEN-001给出的方案靠的是一些标记内容，比如TDO，比如adr目录这些，但是实际上这些decisions文档不存在，另外pitfalls观测的标记我认为是代码坏味道所以不会在代码里出现这些内容。所以这个方案可行性不够"; "如果有文档了，为什么还需要从其他文档中提取呢？"
- **Confirmed At**: 2026-08-13

### NEED-004: Safety model — quick in-session review for high-risk, immediate effect for the rest

- **Status**: confirmed
- **Statement**: `conventions` land as normal `candidate` records that take **local effect
  immediately** (weighted with caution) and are reviewable later, asynchronously and incrementally,
  via the existing `/distill review` channel. `constraints` (the only high-risk, highest-weight,
  honored-first category) are held for a **quick in-session human review at the end of the scan**
  and are written only if approved. This is the sole synchronous step and is intentionally minimal
  because config-level constraints are few.
- **Rationale**: Reconciles "content must pass human eyes" with "do not trap the user in a long
  synchronous audit." A wrong `candidate` constraint would otherwise take top-weighted local effect
  before any human sees it; gating only that small set contains the risk without a heavy audit.
- **User Evidence**: Q3 answer — "高危当场速审、其余即时生效(推荐)"; "我倾向于内容要过人工，但是也担心落盘前过人工这种方式用户体验太差"; "扫描慢、要等扫描完才审计。代码库大可能内容多审计要很久，用户要坐在电脑前审计很久".
- **Confirmed At**: 2026-08-13

### NEED-005: Streaming persistence and resumable scan

- **Status**: confirmed
- **Statement**: onboard writes findings as it scans (streaming) and the scan is
  interruptible / resumable; it does not block until the whole scan finishes before any
  interaction or output.
- **Rationale**: Removes the "slow scan + wait-for-full-scan before anything happens" UX failure
  the user raised.
- **User Evidence**: "扫描慢、要等扫描完才审计".
- **Confirmed At**: 2026-08-13

### NEED-006: Scan strategy — high-signal-first, whole-repo single pass

- **Status**: confirmed
- **Statement**: onboard scans the whole repository (respecting `.gitignore`) but prioritizes by
  signal density and deep-reads only high-value sources (directory structure; build / dependency /
  lint config; entry points; existing docs; test layout; frequently-imported core modules), while
  only shallow-sampling the bulk of business code. An optional `onboard [path]` narrows the scan to
  a subdirectory / module.
- **Rationale**: A real repository is too large to read fully; this balances breadth against the
  context budget and remains usable in a single run.
- **User Evidence**: Q4 answer — "高信号优先 + 全仓一遍(推荐)".
- **Confirmed At**: 2026-08-13

### NEED-007: Integrate with the existing store; idempotent re-runs

- **Status**: confirmed
- **Statement**: onboard reads the existing profile first, de-duplicates against records already
  present (skip what is already covered), and adjudicates conflicts. It is safe to re-run
  (refresh / augment) idempotently.
- **Rationale**: Onboarding a project that already has profile records (from distill or a prior
  onboard) must add without destroying, and must not re-assert what is already captured.
- **User Evidence**: Follows from the store design [[D-2026-0812-14054p-2]] and the no-clobber rule (CON-001).
- **Confirmed At**: 2026-08-13

### NEED-008: Extraction is flexible agent judgment, not a fixed file/marker checklist

- **Status**: confirmed
- **Statement**: Extraction relies on the agent's flexible judgment over whatever the code
  actually shows, **not** a hard-coded list of filenames or markers. Guidance on what counts:
  - `conventions` ← the code's observable regularities (structure, naming, import style, tech stack
    from manifests, lint/format/type config, test layout, repeated patterns) plus architecture /
    stack facts.
  - `constraints` ← config-level explicit hard prohibitions (lint/type rules set to *error* such as
    banned / no-restricted-imports; codegen / "do not edit" / managed-block markers; CODEOWNERS /
    protected paths). Every constraint candidate carries a precise evidence anchor (file:line /
    config snippet); absent such an explicit signal, onboard proposes no constraint.
- **Rationale**: Addresses the rigidity of depending on specific named documents; onboard reads and
  generalizes rather than grepping fixed paths.
- **User Evidence**: "依赖灵活性很差".
- **Confirmed At**: 2026-08-13

## Constraints

### CON-001: Never clobber existing vetted / human / distill records

- **Status**: confirmed
- **Statement**: onboard MUST NOT overwrite or delete any existing `vetted` record or any
  pre-existing human/distill record. New knowledge is always appended as a new file (namespaced
  ids merge without conflict). onboard's only store mutations are add, and edit-within-its-own-
  candidate-file; it never touches records it did not author.
- **User Evidence**: Hard safety rule; aligns with the one-file-per-record store [[D-2026-0812-14054p-2]].

### CON-002: Reuse distill's store and record format (no second store)

- **Status**: confirmed
- **Statement**: onboard reuses distill's store and record format — one record per file,
  ids namespaced by the source-feature id, `claim` physically separated from `evidence`. It does
  not create a second store or a divergent format.
- **User Evidence**: Aligns with [[D-2026-0812-14054p-1]] and [[D-2026-0812-14054p-2]].

### CON-003: onboard records are always inferred → always candidate

- **Status**: confirmed
- **Statement**: An onboard record's `derivation` is always `inferred` (sourced from code, not the
  user's own words), so at write time it is always `candidate` and is never promoted to `vetted` at
  the onboard stage (the quick in-session review is a sanity check, not outcome verification;
  vetting still goes through the normal path). `evidence.facts` records the concrete code
  observation (path + snippet/signal); `provenance` marks the onboard scan as the source,
  distinct from distill.
- **User Evidence**: Follows from the vetted = explicit + outcome-verified rule; onboard is neither.

### CON-004: Standalone, manually-invoked command — not a pipeline stage

- **Status**: confirmed
- **Statement**: onboard is a standalone, user-invoked command; it is not an SDD pipeline stage —
  no auto-next, no auto-hook (positioned like `debug` / `distill`).
- **User Evidence**: Direction confirmed in discussion (onboard 是独立命令).

### CON-005: Read-only on code; writes only the profile

- **Status**: confirmed
- **Statement**: onboard is read-only against the codebase; it writes only to
  `.codexspec/profile/`; it does not modify source, run tests, or touch git.
- **User Evidence**: Boundary confirmed in discussion.

### CON-006: Prerequisite — codexspec-initialized project; ensures scaffold

- **Status**: confirmed
- **Statement**: The project must be codexspec-initialized (`.codexspec/` present) since onboard
  writes into `.codexspec/profile/`; when the profile scaffold is missing onboard ensures it. It
  does not strictly require git.
- **User Evidence**: Follows from writing into the profile store.

### CON-007: Distributed command — English template + Language Preference

- **Status**: confirmed
- **Statement**: onboard is a distributed command: its template stays in English with a
  `## Language Preference` section (interaction / document language split), following the dynamic
  translation convention.
- **User Evidence**: Standard for distributed command templates.

## Decisions

### DEC-001: Output surface writes profile only

- **Status**: confirmed
- **Decision**: onboard writes only the profile store (no map document, no walkthrough).
- **Alternatives Rejected**: profile + persistent project-map document; profile + in-session
  explanation; all three.
- **Reason**: Focus and minimal maintenance surface; explanation/map deferred to a future `explain`.
- **User Evidence**: Q1 — "只写 profile(推荐)".

### DEC-002: Extraction scope converges to conventions + narrow constraints

- **Status**: confirmed
- **Decision**: onboard actively extracts `conventions` + narrow config-level `constraints`;
  `decisions` and `pitfalls` are excluded because they have no reliable, non-redundant cold-scan
  source (not because constraints were narrowed away).
- **Alternatives Rejected**: actively mining all four categories; extracting decisions/pitfalls
  opportunistically by scraping specific documents; mining git history / bug patterns for
  decisions / pitfalls (violates the high-signal, single-pass, lightweight choice and reintroduces
  fabrication risk).
- **Reason**: Documented decisions/pitfalls are redundant to copy; undocumented ones are
  unreliable (pitfalls experiential; decision rationale fabricated).
- **User Evidence**: "如果有文档了，为什么还需要从其他文档中提取呢？"; "pitfalls观测的标记我认为是代码坏味道所以不会在代码里出现".

### DEC-003: Safety model = quick high-risk review + immediate effect for the rest

- **Status**: confirmed
- **Decision**: conv/(the bulk) take immediate `candidate` effect with async `/distill review`;
  `constraints` pass a quick in-session review before write. No new dormant/quarantine status tier
  is introduced.
- **Alternatives Rejected**: block-before-write full synchronous audit of everything; a fully
  dormant "quarantine" status drained asynchronously; distill-parity (all immediate-effective with
  no gate at all).
- **Reason**: Balances "content must pass human eyes" with "do not force a long synchronous audit";
  only the small high-risk set is gated.
- **User Evidence**: Q3 — "高危当场速审、其余即时生效(推荐)".

### DEC-004: Scan = high-signal-first, whole-repo single pass

- **Status**: confirmed
- **Decision**: high-signal-first, one pass over the whole repo, with optional `[path]` narrowing.
- **Alternatives Rejected**: by-area incremental scanning (needs multi-run + onboarded-area state);
  reading only explicit high-signal documents (misses code-embedded conventions).
- **Reason**: Single-run usability; balances breadth against the context budget.
- **User Evidence**: Q4 — "高信号优先 + 全仓一遍(推荐)".

### DEC-005: Installer category = enhanced

- **Status**: confirmed
- **Decision**: onboard registers under the installer `enhanced` category (the self-evolution /
  knowledge family, alongside `distill` / `evolve`); enhanced count 7 → 8 and total 24 → 25, updated
  in lockstep across every distribution-surface site.
- **Alternatives Rejected**: `utility` (onboard is a substantive knowledge command, not a helper);
  `core` (not a pipeline stage); `git` / `review` (wrong family).
- **Reason**: Semantic fit and co-location with the distill/evolve knowledge family.
- **User Evidence**: OPEN-002 resolution; lockstep sites per [[Con-2026-0811-1418yq-1]].

### DEC-006: v1 refresh granularity = `[path]` + idempotent re-run

- **Status**: confirmed
- **Decision**: v1 granularity is `onboard [path]` narrowing plus idempotent re-run (dedup /
  no-clobber); per-record management is handled by the async `/distill review` channel.
- **Alternatives Rejected**: a `--only <category>` per-category refresh filter (YAGNI; expands the
  CLI surface for marginal benefit).
- **Reason**: The no-clobber + dedup discipline already makes re-running safe and additive; `[path]`
  gives spatial narrowing.
- **User Evidence**: OPEN-003 resolution.

## Out of Scope

### OUT-001: No active extraction of decisions or pitfalls

- **Status**: confirmed
- **Statement**: onboard does not actively extract `decisions` or `pitfalls`.
- **Reason**: Documented ones are redundant to copy (already readable in the repo); undocumented
  ones are unreliable to infer — pitfalls are experiential and decision rationale would be
  fabricated. Both remain `distill`'s channels, where rationale/experience is live.
- **User Evidence**: "如果有文档了，为什么还需要从其他文档中提取呢？".

### OUT-002: No feature-scoped SDD artifacts

- **Status**: confirmed
- **Statement**: onboard does not produce `requirements.md` / `spec.md` or any feature-scoped SDD
  artifact.
- **Reason**: That is the job of a separate future `reverse-spec` command; onboard writes only
  project-level profile knowledge.
- **User Evidence**: Boundary established in the prior onboard-vs-reverse-spec discussion.

### OUT-003: No persistent map document, no walkthrough

- **Status**: confirmed
- **Statement**: onboard produces no persistent human-readable project-map document and performs
  no code explanation / walkthrough.
- **Reason**: Kept out of scope to preserve focus; deferred to a possible future `explain` command.
- **User Evidence**: Q1 — "只写 profile".

### OUT-004: No constitution / source / test / git mutation

- **Status**: confirmed
- **Statement**: onboard does not modify `.codexspec/memory/constitution.md`, source code, tests,
  or git state.
- **Reason**: Read-only-on-code / write-only-profile boundary (CON-005).
- **User Evidence**: Boundary confirmed in discussion.

### OUT-005: No autonomous mode that skips the high-risk review (v1)

- **Status**: confirmed
- **Statement**: v1 does not provide a fully-autonomous `--yes` / headless mode that skips the
  quick in-session review of high-risk (constraint) candidates.
- **Reason**: Such a mode would defeat the safety gate.
- **User Evidence**: Follows from DEC-003.

### OUT-006: No per-category refresh filter (v1)

- **Status**: confirmed
- **Statement**: v1 does not provide a `--only <category>` per-category refresh filter.
- **Reason**: YAGNI; per-record management is handled by `/distill review`.
- **User Evidence**: DEC-006.

## Open Questions

None. All open questions raised during discovery (extraction rules, installer category, refresh
granularity) were resolved and folded into NEED-008 / DEC-005 / DEC-006 at the user's request.

## Confirmation Log

### Session 2026-08-13

- **Summary Presented**: Final consolidated entry set — NEED-001..008, CON-001..007, DEC-001..006,
  OUT-001..006 — reflecting four locked design forks (output surface = profile-only; extraction
  scope converged to conventions + narrow constraints after the marker-feasibility critique;
  tiered safety gate = quick high-risk review + immediate effect for the rest; high-signal
  single-pass scan) and the three resolved OPENs (extraction rules, enhanced category, `[path]`+
  idempotent-re-run granularity).
- **User Confirmation**: "确认".
- **Entries Confirmed**: NEED-001, NEED-002, NEED-003, NEED-004, NEED-005, NEED-006, NEED-007,
  NEED-008, CON-001, CON-002, CON-003, CON-004, CON-005, CON-006, CON-007, DEC-001, DEC-002,
  DEC-003, DEC-004, DEC-005, DEC-006, OUT-001, OUT-002, OUT-003, OUT-004, OUT-005, OUT-006.
