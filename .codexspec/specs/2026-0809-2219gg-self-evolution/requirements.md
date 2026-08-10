# Confirmed Requirements: self-evolution

<!--
Language: Maintain this document in the language specified in .codexspec/config.yml.
This file is the authoritative, persistent record of user-confirmed intent.
Do not copy the full conversation. Keep only confirmed decisions and short evidence
quotes needed to resolve later interpretation disputes.
-->

**Feature ID**: `2026-0809-2219gg`
**Status**: Confirmed
**Last Confirmed**: 2026-08-09

## Overview

Add a **self-evolution** capability to CodexSpec as two new distributed commands plus
one storage substrate:

- **`distill`** — extract reusable, cross-feature knowledge from an interaction and
  persist it to a project-level store (`.codexspec/profile/`).
- **`evolve`** — package vetted profile sediment into a SKILL.md / command-template
  draft and contribute it back to CodexSpec itself via a reviewed PR.
- **`.codexspec/profile/`** — the storage substrate distill writes and evolve reads
  (not a command).

The capability turns what today is lost in conversation scrollback into durable,
auditable, reusable assets, and gives users a governed path to contribute capability
back to the toolkit.

Scope ladder (the only one; there is no feature-local tier):
`session context` →(distill)→ `project .codexspec/profile/` →(evolve)→ `upstream templates/`.

## Authority Rules

- Only entries with `Status: confirmed` are binding downstream inputs.
- `open` entries MUST NOT be converted into confirmed product requirements.
- Replaced entries remain in this file with `Status: superseded` and a link to the replacement.
- AI inferences must be labeled as assumptions and require user confirmation before becoming binding.

## Needs

### NEED-001: `distill` — extract reusable knowledge from interactions

- **Status**: confirmed
- **Statement**: A `distill` capability must read a segment of interaction and extract
  the reusable knowledge scattered across it (conventions, negative constraints,
  pitfalls, cross-feature decisions) into a durable, structured, project-level store.
- **Rationale**: Key intent is usually spread across many turns and lost after the
  session; without structured extraction it is forgotten or misremembered.
- **User Evidence**: "如何将交互过程中的内容进行整理抽取的能力" (the ability to
  organize/extract the content of the interaction process).
- **Confirmed At**: 2026-08-09

### NEED-002: `evolve` — contribute distilled capability back to the project

- **Status**: confirmed
- **Statement**: An `evolve` capability must package vetted profile sediment into a
  SKILL.md / command-template draft and open a reviewed PR to contribute it back
  upstream to CodexSpec, so a user's local sediment can become a shared capability.
- **Rationale**: Knowledge that only lives in one user's project is a private memory;
  the differentiating value is a governed path that feeds it back into the toolkit.
- **User Evidence**: "用户整理出来的场景和能力是否能够贡献回本项目的能力" (whether the
  scenarios/capabilities a user organizes can be contributed back to this project's
  capabilities).
- **Confirmed At**: 2026-08-09

### NEED-003: `distill` must be auto-triggerable, not manual-only

- **Status**: confirmed
- **Statement**: Beyond a manual invocation, `distill` must be triggerable
  automatically by other flows, so capture does not depend on the user remembering to
  run it. Manual invocation is a fallback, not the primary path.
- **Rationale**: The whole value of distillation is capturing what the user would
  otherwise lose; relying on manual invocation defeats it.
- **User Evidence**: "我希望是除了用户主动触发之外，可以被其他流程自动触发 distill
  命令" (besides the user actively triggering it, I want distill to be auto-triggerable
  by other flows).
- **Confirmed At**: 2026-08-09

### NEED-004: distilled records must carry evidence and be auditable

- **Status**: confirmed
- **Statement**: Every distilled record must carry the evidence it was derived from, so
  distill quality can be audited later and, when a distillation is wrong, the point of
  misunderstanding can be located.
- **Rationale**: A bare assertion cannot be reviewed or corrected; separating the claim
  from its evidence lets an audit tell misread-evidence from over-generalization from
  stale-evidence.
- **User Evidence**: "依旧要保证整个 distill 要给出 evidence facts / evidence state，
  后期才可以追溯 distill 的质量和在 distill 出现偏差时找出理解偏差的地方".
- **Confirmed At**: 2026-08-09

## Constraints

### CON-001: `distill` must not duplicate existing SDD artifacts

- **Status**: confirmed
- **Statement**: `distill` only captures cross-feature reusable knowledge that the
  per-feature SDD artifacts structurally cannot accumulate. Feature-level "why" already
  has homes: requirement rationale → `requirements.md` (specify/clarify already extract
  it); approach rationale → plan/design. The boundary test is one question: **"would a
  single feature's `requirements`/`spec`/`plan` record this?"** — yes → leave it there,
  distill does not touch it; no / it spans features → it may enter the profile.
- **User Evidence**: "关于你的残留问题，不是有 requirements 吗？" (regarding the residual
  problem, isn't there requirements?).

### CON-002: The profile is project-level only — no feature-local tier

- **Status**: confirmed
- **Statement**: Distilled knowledge lands at project level (`.codexspec/profile/`).
  There is no feature-local sediment tier: a feature's durable memory is already its
  existing spec directory; anything reusable beyond a feature goes straight to project
  level.
- **User Evidence**: "feature-local 只作用在 feature 的话，feature 的生命周期比较短，是否
  有必要沉淀……如果一个沉淀不止在 feature 内有用，那么为什么不直接沉淀成项目级？"

### CON-003: Each record separates `claim` from `evidence`

- **Status**: confirmed
- **Statement**: Every profile record physically separates the distilled `claim` from
  its `evidence` (`evidence.facts` quoting the original words, `evidence.state` for the
  context/validity, plus `provenance` and `status`). This separation is what makes the
  three failure modes — misread / overreach / stale — individually locatable (NEED-004).
- **User Evidence**: See NEED-004.

### CON-004: Store current-effective only; mutate via add/replace/remove; git is the ledger

- **Status**: confirmed
- **Statement**: Profile files hold only the **current effective** knowledge and stay
  dense. They are never freely edited; all change follows a three-operation discipline —
  `add` (append a new verified item), `replace` (supersede an outdated/wrong item),
  `remove` (drop an invalidated item). Because the profile is version-controlled
  markdown, **git history is the audit ledger** (every replace/remove is a traceable
  diff; `git blame` recovers the claim+evidence as of when a rule was added). The files
  therefore keep no in-file "retired" section.
- **User Evidence**: Hermes memory mechanism cited by the user — two clean local
  markdown files mutated only through atomic `Add` / `replace` / `remove`, "严禁任意
  修改，严格要求原子操作", to maintain high information density.

### CON-005: `distill` trigger = command-embedding + manual; no hook

- **Status**: confirmed
- **Statement**: The primary auto-trigger is **command-embedding** (a distill section in
  terminal / wrap-up commands, mirroring the existing `auto_next` / auto-analyze
  pattern), gated by `workflow.auto_distill`; the fallback is manual `/distill`. Hooks
  are **not** used: at the high-value boundaries a command is already running (embedding
  is strictly better — live context, cross-Codex, ships via `init`), and where a hook
  would be unique (mid-session exit / PreCompact) it costs headless context-rebuild,
  Claude-Code-only lock-in (breaks `project.ai: both`), and an `init` settings.json
  write.
- **User Evidence**: "那么 hook 就不适合作为触发方式" (then hook is not suitable as a
  trigger mechanism).

### CON-006: Contribution is unified PR + human review; identity is not tiered

- **Status**: confirmed
- **Statement**: All upstream contribution goes through PR + human review, identically
  for everyone. "Repo owner vs external user" is only a **git mechanics** difference
  (push a branch vs fork), auto-detected by `evolve`; it is not a permission or policy
  tier. Human review is mandatory; there is no fully-automated merge.
- **User Evidence**: "我自己也是 issue+pr 的方式将自己的改动合并到主分支，那么这跟外部用户
  的行为是否没有差别，那么是否所有人都 pr 回流即可？"

### CON-007: Self-bootstrap — evolve edits `templates/` only

- **Status**: confirmed
- **Statement**: `evolve`'s output only ever modifies source under `templates/`
  (or a standalone skill package), synced to users via `publish` → `init`. It never
  hand-edits the `.claude/commands/codexspec/` install artifacts. `add`/`replace`/
  `remove` on the profile are append-oriented and human-reviewed, which aligns naturally
  with the self-bootstrap rule.
- **User Evidence**: Project governance (constitution / repository-layout).

### CON-008: LLM-instruction positioning — no runtime engine

- **Status**: confirmed
- **Statement**: These commands are LLM-instruction markdown, not a runtime engine.
  Anything the LLM naturally judges at runtime given good instructions is expressed as
  an instruction, never engineered: `replace` is a conceptual discipline (the agent edits
  markdown semantically, not a substring-match tool primitive); `scope/when` is a
  natural-language condition string (no DSL); dedup is a runtime instruction ("read the
  current profile first, skip what is covered, replace what changed"). No matching
  algorithm, no expression grammar, no metric engine is built.
- **User Evidence**: "我在担心过度设计或者与当前 codexspec 的定位无法承载和契合的问题" —
  necessity check that cut the over-engineered open items.

### CON-009: i18n consistency

- **Status**: confirmed
- **Statement**: New command templates stay in English with the standard
  `## Language Preference` section, following the project's dynamic-translation convention.
- **User Evidence**: Project i18n architecture.

## Decisions

### DEC-001: Two commands + one substrate (not three co-equal commands)

- **Status**: confirmed
- **Decision**: The capability is `distill` (writes) + `evolve` (reads → packages → PR)
  - the `.codexspec/profile/` substrate. `project-memory` is the substrate, not a third
  command.
- **Alternatives Rejected**: Three co-equal commands (rejected: `project-memory` is
  distill's product/storage, not a user command).
- **Reason**: Matches the actual data flow; avoids inventing a command for a store.
- **User Evidence**: "如果是这样的话，新增 evolve 感觉没有复杂到需要单独一步" — clarified
  that the substrate is not a co-equal command.

### DEC-002: Profile = four files; `decisions.md` cross-feature only; constraints in their own file

- **Status**: confirmed
- **Decision**: `.codexspec/profile/` holds four markdown files: `constraints.md` (negative
  constraints — highest weight, honored first), `conventions.md` (positive cross-feature
  conventions/steering), `pitfalls.md` (cross-feature traps/workarounds), `decisions.md`
  (**only** cross-feature/architectural ADR-lite; never single-feature requirement
  rationale). Records carry `type`, optional `scope/when`, evidence, provenance, and a
  `candidate`/`vetted` status. The name avoids `.codexspec/memory/` (constitution lives
  there). Hermes's `USER.md`/`MEMORY.md` subject-split is deliberately not adopted.
- **Alternatives Rejected**: A monolithic single file (rejected: read-pattern mismatch +
  unbounded growth); one-file-per-fact (rejected: too granular); folding constraints into
  `conventions.md` (rejected: a file named "conventions" holding prohibitions is confusing —
  constraints get their own file); a `decisions.md` that duplicates requirement rationale
  (rejected: CON-001).
- **Reason**: Read-pattern grouping + density; negative constraints deserve top priority and
  a self-evident home.
- **User Evidence**: "这个 PROFILE 是一个文件还是一组文件？"; "单开 constraints.md（更直白）".

### DEC-003: Trigger at terminal/wrap-up commands + manual; gated by `workflow.auto_distill`

- **Status**: confirmed
- **Decision**: Embed distill at terminal/wrap-up commands (`implement-tasks` on
  completion, and `commit-staged`/`pr`) plus manual `/distill`; the routine early-exits
  when the delta has nothing worth capturing. It is **not** fired at every chain boundary
  — feature-level early corrections are already caught by `requirements.md` (CON-001) and
  cross-feature knowledge mostly surfaces after implementation. `auto_distill` defaults to
  **enabled** (opt-out) — disabled only when explicitly set to the literal `false` — unlike
  `auto_next` (opt-in); this is safe because distill is non-blocking, never mutates SDD
  artifacts, and early-exits.
- **Alternatives Rejected**: Hooks (CON-005); per-chain-boundary incremental capture
  (rejected: over-mechanism given `requirements.md` already covers early feature-level
  loss); opt-in default (rejected: capture should happen unless deliberately turned off).
- **Reason**: Highest-value, lowest-cost trigger points; portable across Claude Code and
  Codex.
- **User Evidence**: NEED-003; "那么 hook 就不适合作为触发方式"; "auto-distill 我希望默认是开启的，只有用户手动设置关闭才关闭".

### DEC-004: Conflict adjudication — recency / specificity / scenario-decoupling / defer

- **Status**: confirmed
- **Decision**: When new distilled constraints conflict with existing ones, distill
  adjudicates by: (1) **recency** — newer corrections win (usually a `replace`);
  (2) **specificity** — a specific instruction overrides the general one only in its
  local scope; (3) **scenario-decoupling** — if neither wins, keep both under a
  `scope/when` condition instead of forcing a winner; (4) **defer, don't guess** — if
  genuinely unresolvable, record `status: conflict/needs-adjudication` and surface it at
  the next interactive point or at evolve time; distill never blocks and never guesses.
- **Alternatives Rejected**: Asking the user inline (rejected: distill runs
  non-interactively at a command boundary).
- **Reason**: Adapts the user-provided 4-stage adjudication to a non-interactive
  auto-run while honoring "don't falsely automate a semantic judgment".
- **User Evidence**: User-provided SKILL 4-stage method, stage 2「冲突裁决」(近时性 /
  具体化 / 场景解耦 / 冲突确认).

### DEC-005: `evolve` compile rules — priority order, logic-clean, imperative wording

- **Status**: confirmed
- **Decision**: When `evolve` compiles profile sediment into a SKILL.md / template draft:
  core needs first, **negative constraints immediately after (highest weight)**, then the
  rest; superseded rules are cleaned via `replace`/`remove` so the output carries no
  contradictions; wording is imperative (必须 / 始终 / 严禁 / 仅允许 over 可以考虑 / 尽量
  / 最好不要 / 或许), consistent with the project's existing Prefer/Avoid rule style.
- **Alternatives Rejected**: Suggestion-style wording (rejected: weaker execution
  accuracy).
- **Reason**: Directly adopts the 4-stage method's「整合优化」principles.
- **User Evidence**: User-provided SKILL 4-stage method, stage 3「整合优化」(优先级排序 /
  逻辑清洗 / 指令化表达).

### DEC-006: Evolution retrospect one-liner + value gate (lightweight eval replacement)

- **Status**: confirmed
- **Decision**: Each `evolve` produces a one-sentence value statement as the PR summary
  ("this resolves <pain>, by <added/revised constraint>, achieving <quality/efficiency
  gain>"). **Value gate**: if no crisp value statement can be written, no PR is opened
  (the batch of corrections was not worth promoting). A worse post-evolve result is
  rolled back via `remove`/`replace` (git-traceable), not a manual file edit.
- **Alternatives Rejected**: eval / GEPA metric-driven optimization (see OUT-001).
- **Reason**: A human-readable value signal is a lightweight substitute for a metric.
- **User Evidence**: User-provided SKILL 4-stage method, stage 4「进化复盘」.

### DEC-007: Vetting rule + interactive review (no manual file editing)

- **Status**: confirmed
- **Decision**: `distill` sets `status: vetted` when a record's `derivation = explicit` (the
  user's own words) AND it was verified by an outcome; every `inferred` record stays
  `candidate`. Auto-distill writes candidates non-interactively and never prompts. Candidates
  are promoted through an **interactive review mode** — manual `/distill review` — which lists
  pending candidates compactly and applies vet/edit/drop on the user's inline approval by
  editing `status`. The user never hand-edits the profile files.
- **Alternatives Rejected**: (a) all vetting by human only (rejected: too much friction for
  explicit+verified items); a separate review command (rejected: fold into distill's manual
  mode); manual hand-editing of files (rejected: unfriendly).
- **Reason**: Auto-promote the safe class (explicit+verified); keep a friendly inline gate for
  the rest without breaking distill's non-interactive auto path.
- **User Evidence**: "(b)：用户原话 + 已验证 → 直接 vetted，推断类留 candidate 等人点头";
  "这个等人点头难道是要人翻出文档内容手动改吗还是其他更加方便友好方式？"

### DEC-008: `evolve` confirms with the user before any push / PR

- **Status**: confirmed
- **Decision**: `evolve` MUST present the compiled draft and the value statement to the user
  and obtain explicit approval **before** any `git push` or PR creation; it never pushes or
  opens a PR unattended. Writing a local draft under `templates/` is git-reversible; the
  outward action is what is gated.
- **Alternatives Rejected**: Opening the PR immediately after compiling (rejected: push/PR is
  an outward, hard-to-reverse action).
- **Reason**: Outward actions need a human checkpoint.
- **User Evidence**: "在 evolve 真正 push/开 PR 之前先跟用户确认一次".

## Out of Scope

### OUT-001: No eval / metric-driven optimization (DSPy / GEPA)

- **Status**: confirmed
- **Statement**: No evaluation harness or genetic/metric-driven prompt optimization is
  built.
- **Reason**: Too heavy for this stage; the value-statement gate (DEC-006) is the
  lightweight substitute. "回流本体必须过人眼" — human review, not a metric, is the gate.

### OUT-002: No feature-local sediment tier

- **Status**: confirmed
- **Statement**: There is no feature-local profile layer (CON-002).
- **Reason**: A feature's memory is its existing spec directory; reusable knowledge goes
  straight to project level.

### OUT-003: No hook-based triggering

- **Status**: confirmed
- **Statement**: distill is not triggered by Claude Code hooks (CON-005).
- **Reason**: Portability (breaks `project.ai: both`) and `init` distribution cost;
  command-embedding covers the high-value boundaries.

### OUT-004: `distill` does not recapture feature-level requirement rationale

- **Status**: confirmed
- **Statement**: Feature-scoped "why" stays in `requirements.md` / plan; distill does not
  copy it into the profile.
- **Reason**: CON-001 boundary — avoid duplicating existing SDD artifacts.

### OUT-005: Hermes `USER.md`/`MEMORY.md` subject-split not adopted

- **Status**: confirmed
- **Statement**: The profile is project-level and typed (convention/constraint/pitfall/
  decision), not split by subject into user vs system memory.
- **Reason**: User identity / preferences / language already have homes in CodexSpec
  (`config.yml`, constitution, Claude Code's own memory).

### OUT-006: No fully-automated upstream contribution

- **Status**: confirmed
- **Statement**: `evolve` never merges to the toolkit unattended; a human review always
  gates the PR.
- **Reason**: CON-006 — human review is mandatory.

## Open Questions

### OPEN-001: Exact wrap-up commands that embed `distill`

- **Status**: resolved
- **Resolved By**: DEC-003 — `implement-tasks` (on completion) plus `commit-staged`/`pr`,
  with an early-exit when there is nothing to capture.
- **Why It Matters**: Determines which existing templates gain a distill section.
- **Owner**: User

## Confirmation Log

### Session 2026-08-09

- **Summary Presented**: Self-evolution as two new commands + one substrate —
  `distill` (auto-triggerable via command-embedding + manual; extracts cross-feature,
  evidence-backed, claim/evidence-separated records into project-level
  `.codexspec/profile/`; bounded by the requirements-as-truth boundary test; conflicts
  adjudicated by recency/specificity/scenario-decoupling and otherwise deferred) and
  `evolve` (compiles vetted sediment into imperative-worded SKILL.md/template drafts and
  contributes upstream via a unified, human-reviewed PR; identity is not tiered). Storage
  is current-effective-only markdown mutated via add/replace/remove with git as the audit
  ledger. No hooks, no feature-local tier, no eval/GEPA, no runtime engine.
- **User Confirmation**: Approved the converged design across the 2026-08-09 discussion
  ("按这三处把文档收敛掉" for the doc; then "将敲定好的先实现，每一个主题一个 feature 目录"
  and chose seed-based authoring on a new feature branch). During implementation, confirmed
  three refinements: vetting rule (b), a separate `constraints.md`, and `evolve` confirming
  before push/PR — recorded as revised DEC-002 and new DEC-007, DEC-008.
- **Entries Confirmed**: NEED-001..004, CON-001..009, DEC-001..008, OUT-001..006;
  OPEN-001 resolved by DEC-003.
