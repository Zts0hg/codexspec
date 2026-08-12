# Confirmed Requirements: profile-consumption

<!--
Language: document language is English (.codexspec/config.yml → language.document: en).
Authoritative, persistent record of user-confirmed intent. Keep only confirmed
decisions and short evidence; do not copy the full conversation.
-->

**Feature ID**: `2026-0812-14054p`
**Status**: Confirmed
**Last Confirmed**: 2026-08-12

## Authority Rules

- Only entries with `Status: confirmed` are binding downstream inputs.
- `open` entries MUST NOT be converted into confirmed product requirements.
- Replaced entries remain with `Status: superseded` and a link to the replacement.
- AI inferences must be labeled as assumptions and require user confirmation before becoming binding.

## Needs

### NEED-001: Make distilled profile knowledge take effect in the user's own project

- **Status**: confirmed
- **Statement**: Provide a "profile consumption" capability so that the reusable knowledge distilled into a user project's `.codexspec/profile/` actually influences that project's subsequent work — accumulating experience so pitfalls are not re-hit and prior decisions/conventions are not re-litigated.
- **Rationale**: 0.7.7 shipped distill (writes profile) + evolve (reads profile → upstream PR), but nothing consumes the profile *within the user's own project*. This closes that gap.
- **User Evidence**: "我希望distill的内容可以最大程度发挥作用"; "持续提取经验避免重复踩坑和重复走弯路"
- **Confirmed At**: 2026-08-12

### NEED-002: A-layer — ambient injection at init

- **Status**: confirmed
- **Statement**: `codexspec init` injects a **managed block** into the context file of each configured AI integration. The block contains (1) the project's **constraints**, delivered per the channel-adaptive method in DEC-005, and (2) a **pointer index** to `conventions.md` / `pitfalls.md` / `decisions.md` — naming each file, a one-line description, and when to consult it — so their content is read **on demand** (token cost only in the turn a file is actually read; independent of profile size).
- **Rationale**: Ambient context is loaded in every session (including plain chat), so the profile becomes discoverable everywhere, not only inside SDD commands.
- **User Evidence**: "A 层·常驻指针（处处可发现，含普通聊天）"; "按需检索内容而不是全量注入"
- **Confirmed At**: 2026-08-12

### NEED-003: Support both CLAUDE.md and AGENTS.md

- **Status**: confirmed
- **Statement**: The injection MUST support **both** `CLAUDE.md` (Claude Code) and `AGENTS.md` (Codex), driven by the project's configured integrations (`project.ai`). Do not presume a single fixed tool.
- **Rationale**: Users run Claude Code, Codex, or both; the capability must reach whichever they use.
- **User Evidence**: "需要支持对 CLAUDE.md 和 AGENTS.md 的内容注入，不要预设用户使用某一种固定的工具"
- **Confirmed At**: 2026-08-12

### NEED-004: B-layer — profile consulted during `specify` only

- **Status**: confirmed
- **Statement**: `specify.md` gains an embedded step: before requirements discovery, read `.codexspec/profile/` so the confirmed `requirements.md` is a synthesis that already incorporates the relevant constraints / pitfalls / conventions / decisions. No other SDD stage reads the profile.
- **Rationale**: `specify` is the pipeline source; once requirements incorporate the profile, downstream stages inherit that influence transitively by treating `requirements.md` as authority.
- **User Evidence**: "B层命令内显式读取我认为应该在specify里面做就可以，因为这个命令是sdd流程的源头...后续流程保持以REQUIREMENTS为权威即可"
- **Confirmed At**: 2026-08-12

### NEED-005: Immediate effect — init sets up the reference unconditionally and ensures the profile scaffold

- **Status**: confirmed
- **Statement**: `codexspec init` **unconditionally and idempotently** (a) ensures the managed block exists in each configured context file, and (b) ensures the profile **scaffold** exists — the `.codexspec/profile/` directory plus any file an injected reference resolves against (at minimum `constraints.md` for the Claude `@import`). Consequently, knowledge distilled *after* init takes effect immediately (the reference already points at an existing, live file) with **no re-init required** and **no dangling reference**.
- **Rationale**: Gating injection on profile-existence would mean a first-time user's later-distilled knowledge stays inert until the next init run. Decoupling "wire the reference" (init, always) from "profile has content" (distill, later) removes that latency.
- **User Evidence**: "为什么不是init的时候统一检查并注入CLAUDE.md/AGENTS.md，然后检查 profile目录是否存在，如果不存在可以先创建空目录来避免悬空引用？"
- **Confirmed At**: 2026-08-12

## Constraints

### CON-001: Governance / self-bootstrap

- **Status**: confirmed
- **Statement**: Edit only `templates/` and `src/codexspec/` (init logic + integrations). Derived artifacts sync via publish → `codexspec init`; CodexSpec's own repo obtains the capability by dogfooding init. Follow self-bootstrap.
- **User Evidence**: "仅改 templates/ 与 src/codexspec/...遵循 self-bootstrap；codexspec 自身靠 dogfood init 获得"

### CON-002: Constitution untouched

- **Status**: confirmed
- **Statement**: This feature MUST NOT modify the constitution or use it as an injection surface. The constitution stays high-authority and concise.
- **User Evidence**: "同意不写consititution, consititution应该保持高权威且简洁"

### CON-003: Downstream stages do not read the profile

- **Status**: confirmed
- **Statement**: `generate-spec` / `spec-to-plan` / `plan-to-tasks` / `implement-tasks` and the review commands MUST NOT read the profile. Profile influence reaches them only transitively through `requirements.md`.
- **User Evidence**: "后续流程保持以REQUIREMENTS为权威即可"

### CON-004: Constant ambient cost

- **Status**: confirmed
- **Statement**: Only the constraints (per DEC-005) plus the pointer index are always-present in context. The content of `conventions.md` / `pitfalls.md` / `decisions.md` costs tokens only in the turn it is actually read; the always-loaded footprint MUST be independent of how large those files grow.
- **User Evidence**: "注入索引或者说引用/路径/句柄...按需检索内容而不是全量注入...是否就是可以...路径都写入而不用担心token占用了"

### CON-005: Idempotent, non-destructive managed block

- **Status**: confirmed
- **Statement**: The managed block MUST use recognizable boundary markers (e.g. `<!-- CODEXSPEC PROFILE START/END -->`), be updated idempotently, and MUST NOT clobber any other content the user has in the context file. This follows init's existing discipline (never overwrite the CLAUDE.md body; regex-replace the AGENTS.md managed block).
- **User Evidence**: Derived from NEED-003/NEED-005 and existing init behavior; confirmed under the reviewed stage summary.

## Decisions

### DEC-001: Constraints guaranteed-present; the other three via pointer

- **Status**: confirmed
- **Decision**: Deliver `constraints` so they are guaranteed/near-guaranteed present (highest-weight negative red-lines); deliver `conventions` / `pitfalls` / `decisions` via pointer + on-demand read.
- **Alternatives Rejected**: All-pointer (hard red-lines then rely on the model choosing to read them); all-inline (token weight grows with the profile).
- **Reason**: Missing a hard prohibition is the exact recurrence the feature prevents; the negative-constraint set is small, so guaranteeing its presence is cheap.
- **User Evidence**: "采用(i) 内联 constraints + 指针其余三类"

### DEC-002: B-layer only in `specify`

- **Status**: confirmed
- **Decision**: Embed the profile-read only in `specify`.
- **Alternatives Rejected**: Read the profile at every SDD stage.
- **Reason**: Requirements propagate downstream as authority, so re-reading is redundant; the A-layer covers implementation-time discoverability.
- **User Evidence**: "B层命令内显式读取我认为应该在specify里面做就可以"

### DEC-003: No vetted filter for local consumption

- **Status**: confirmed
- **Decision**: Local consumption surfaces all records regardless of `status`; the on-demand read exposes the full record (including `status`), letting the agent weight `candidate` lower. `candidate` takes effect locally; `vetted` remains only the gate for `evolve` (upstream contribution).
- **Alternatives Rejected**: Require `vetted` for local consumption.
- **Reason**: Requiring vetting for local use contradicts "let distilled knowledge take maximum effect"; claim/evidence/status separation lets status inform weight without a hard filter.
- **User Evidence**: "如果我不关系回流上游，只关心能否持续distill出可以作用与当前项目...candidate的条目是否能够在后续的项目开发环节生效"

### DEC-004: Unconditional injection + init-created scaffold

- **Status**: confirmed
- **Decision**: init injects the managed block unconditionally (not gated on whether the profile has content) and creates the profile scaffold if absent.
- **Alternatives Rejected**: Gate injection on profile-existence.
- **Reason**: Gating causes later-distilled knowledge to stay inert until the next init and forces init to re-check content every run; unconditional wiring + a scaffold makes new knowledge live immediately.
- **User Evidence**: "为什么不是init的时候统一检查并注入...如果不存在可以先创建空目录来避免悬空引用"

### DEC-005: Channel-adaptive constraints delivery

- **Status**: confirmed
- **Decision**: Deliver constraints per channel capability — **Claude/CLAUDE.md** via `@import .codexspec/profile/constraints.md` (guaranteed present + auto-fresh from the live file); **Codex/AGENTS.md** via a **strong mandatory pointer** ("before non-trivial work you MUST read constraints.md — highest-priority red-lines"), which is auto-fresh and depends on no `@import` support.
- **Alternatives Rejected**: Codex literal-inline of constraints + a sync mechanism.
- **Reason**: Literal inline goes stale when `constraints.md` changes; the only component that knows it changed is `distill`, but making distill rewrite context files breaks its contract ("only writes to `.codexspec/profile/`, never touches other tracked files"); re-syncing via init re-run reintroduces latency. Pointers read the live file, so there is no staleness anywhere and no dependency on unverified Codex `@import` behavior.
- **User Evidence**: "需要进一步解决 codex 中注入内容陈旧的问题？所以CODEX应该还是全部使用指针的方式吗"; "认可"

## Out of Scope

### OUT-001: No constitution changes

- **Status**: confirmed
- **Statement**: The constitution is neither modified nor used as an injection surface.
- **Reason**: Keep it high-authority and concise (CON-002).

### OUT-002: No changes to evolve / upstream contribution

- **Status**: confirmed
- **Statement**: This feature is purely local consumption; it does not alter `evolve` or the upstream-PR path.
- **Reason**: Local consumption and upstream contribution are deliberately decoupled (DEC-003).

### OUT-003: No metric/eval-driven profile optimization

- **Status**: confirmed
- **Statement**: No DSPy/GEPA-style measured optimization of the profile or prompts.
- **Reason**: Out of scope for this capability.

## Open Questions

### OPEN-001: Whether Codex AGENTS.md supports `@import` (non-blocking, downgraded)

- **Status**: open (non-blocking)
- **Why It Matters**: The confirmed design (DEC-005) deliberately does NOT depend on it — Codex uses a pointer regardless. If verification shows Codex expands `@import`, upgrading Codex constraints to `@import` is an optional enhancement, not a requirement.
- **Owner**: Team (verify during spec/plan)

### OPEN-003: Exact managed-block and pointer wording

- **Status**: open (non-blocking)
- **Why It Matters**: Final text of the managed block, the pointer index entries, and the Codex constraints imperative — a drafting detail resolved during implementation.
- **Owner**: Team

<!--
Resolved during discovery:
- OPEN-002 (freshness of inlined constraints) is CLOSED by DEC-005: nothing is literally inlined; @import (Claude) and pointers (both channels) read the live files, so no staleness exists.
- An earlier NEED-005 framing ("degrade gracefully when the profile does not exist") was superseded by the unconditional-injection + scaffold approach (DEC-004): init makes the profile exist rather than gating on its absence.
-->

## Confirmation Log

### Session 2026-08-12

- **Summary Presented**: A managed profile block injected by init into CLAUDE.md and AGENTS.md (constraints delivered channel-adaptively — @import on Claude, strong pointer on Codex — plus a pointer index to conventions/pitfalls/decisions read on demand); a specify-only read of the profile at requirements time; unconditional injection + init-created scaffold for immediate effect; no vetted filter for local use; constitution untouched.
- **User Confirmation**: "认可"
- **Entries Confirmed**: NEED-001..005, CON-001..005, DEC-001..005, OUT-001..003
- **Open (non-blocking)**: OPEN-001, OPEN-003
- **Notable rejected alternatives**: gating injection on profile-existence (DEC-004); Codex literal-inline + sync (DEC-005); requiring vetted for local consumption (DEC-003); reading profile at every SDD stage (DEC-002).
