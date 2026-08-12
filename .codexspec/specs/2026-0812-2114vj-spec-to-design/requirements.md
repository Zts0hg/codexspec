# Confirmed Requirements: spec-to-design

<!--
Language: Maintain this document in the language specified in .codexspec/config.yml.
This file is the authoritative, persistent record of user-confirmed intent.
Do not copy the full conversation. Keep only confirmed decisions and short evidence
quotes needed to resolve later interpretation disputes.
-->

**Feature ID**: `2026-0812-2114vj`
**Status**: Confirmed
**Last Confirmed**: 2026-08-12

## Authority Rules

- Only entries with `Status: confirmed` are binding downstream inputs.
- `open` entries MUST NOT be converted into confirmed product requirements.
- Replaced entries remain in this file with `Status: superseded` and a link to the replacement.
- AI inferences must be labeled as assumptions and require user confirmation before becoming binding.

## Summary

Insert a first-class **design** stage between `spec` and `plan` so the CodexSpec pipeline
becomes `requirements → spec → design → plan → tasks`. This closes the "front-half design
layer" gap: today `spec-to-plan` silently conflates *what the system is* (architecture,
components, data model, design decisions) with *how to build it* (phases, ordering,
verification). The new stage gives design a first-class, traceable artifact (`design.md`)
with its own review gate, and narrows `spec-to-plan` to pure implementation planning.

## Needs

### NEED-001: First-class design stage inserted into the pipeline

- **Status**: confirmed
- **Statement**: Add a dedicated design stage so the authoritative chain becomes
  `requirements → spec → design → plan → tasks`, with `design.md` a first-class artifact
  in the authority order (`requirements > spec > design > plan > tasks`).
- **Rationale**: Closes the largest identified front-half gap (design layer), reinforcing
  CodexSpec's traceable-pipeline core rather than branching into new territory.
- **User Evidence**: Chose "A 拆分(设计升为一等阶段)" as the architectural basis.
- **Confirmed At**: 2026-08-12

### NEED-002: New `spec-to-design` command

- **Status**: confirmed
- **Statement**: Add `templates/commands/spec-to-design.md`. It reads `requirements.md` +
  `spec.md`, produces `design.md`, acts as a **constrained system designer** (refines
  implementation design without changing product intent), and embeds an automatic review
  loop (`review-design`) plus an Auto-Next Chain Advance section — mirroring the structure
  of `spec-to-plan`.
- **Rationale**: The design stage needs a producer command symmetric with the other
  pipeline stages.
- **User Evidence**: Confirmed feature framing as a pipeline extension (not a standalone
  utility command).
- **Confirmed At**: 2026-08-12

### NEED-003: New `review-design` command

- **Status**: confirmed
- **Statement**: Add `templates/commands/review-design.md`, structurally symmetric with
  `review-spec` / `review-plan` / `review-tasks`: Fidelity & Coverage pass, Feasibility &
  Internal Quality pass, Risk Advisories / Design Opportunities, the same Severity / Status
  taxonomy, and a Compatibility Score. It saves `<feature-dir>/review-design.md`.
- **Rationale**: Keeps every pipeline stage's per-stage review gate consistent.
- **User Evidence**: Chose "新增 review-design" over "不单独出 review".
- **Confirmed At**: 2026-08-12

### NEED-004: `design.md` content — fused core plus on-demand sections

- **Status**: confirmed
- **Statement**: `design.md` always contains a fixed core — Architecture & Components
  (system shape + component/interface responsibilities) and ADR-lite Key Design Decisions
  (decision + alternatives + trade-offs). Additional sections — Data Models / Key Entities,
  API / Interface Contracts, Sequence & Data Flow, cross-cutting (performance / security /
  availability) design, Risks & Trade-offs — appear **only when the feature warrants them**
  (scale-to-complexity; a trivial feature may be a thin "no significant design decisions"
  page). No section is required merely because the template contains it.
- **Rationale**: Realizes "融合 + 按需成章" and matches the existing review-side rule that
  never forces template sections.
- **User Evidence**: Chose "融合+按需成章" over "只做骨架" / "一次做全".
- **Confirmed At**: 2026-08-12

### NEED-005: Design carries traceability into the authority chain

- **Status**: confirmed
- **Statement**: Every design component / interface / data change / design decision carries
  `Covers: REQ-xxx`, placing design on the authoritative traceability chain. See DEC-005 for
  the exact downstream `Covers` notation.
- **Rationale**: Design is only first-class if it is traceable to and from requirements.
- **User Evidence**: Confirmed design as a first-class artifact "带 Covers 进权威链".
- **Confirmed At**: 2026-08-12

### NEED-006: Single `design-template.md` in `templates/docs/`

- **Status**: confirmed
- **Statement**: Add a **single** `templates/docs/design-template.md` (fixed core + optional
  sections per NEED-004). No `simple`/`detailed` two-tier split. `codexspec init` copies it
  into `.codexspec/templates/docs/` via the existing docs-copy logic.
- **Rationale**: A single template with fixed-core + optional-sections directly implements
  scale-to-complexity, avoids the "pick the wrong tier" risk, and is not unprecedented
  (`requirements` / `checklist` / `constitution` templates are already single-file). The
  two-tier split is a coarser, older scaling mechanism largely superseded by the review-side
  "don't force sections" rule.
- **User Evidence**: Chose "单模板(固定核心+可选章节)" over "两档 simple/detailed"; asked to
  examine why the two-tier templates exist before deciding.
- **Confirmed At**: 2026-08-12

### NEED-007: Downstream pipeline artifacts updated for the inserted stage

- **Status**: confirmed
- **Statement**: Update the existing pipeline templates so the inserted design stage is
  coherent end-to-end:
  - `generate-spec.md`: Auto-Next Chain Advance invokes `/codexspec:spec-to-design` instead
    of `/codexspec:spec-to-plan`.
  - `spec-to-plan.md`: role narrowed from "constrained technical designer" to
    **implementation planner**; reads `design.md`; plan components use
    `Covers: REQ-xxx; Design: <design component>` (per DEC-005); authority order gains
    `design`. The **plan templates** (`plan-template-detailed.md`, and the "Design Document"
    `plan-template-simple.md`) are slimmed: the design-only sections that migrate to
    `design.md` (Architecture / Component Structure / Data Models / API Contracts / ADR-style
    Decisions) are removed, leaving plan as Tech Stack + Implementation Phases + Verification
    - Requirements Coverage — so `plan.md` and `design.md` do not overlap.
  - `plan-to-tasks.md`: reads `design.md` as context; authority order gains `design`.
  - `analyze.md`: traceability chain deepened to `confirmed → REQ → design → plan → task`;
    completeness/consistency remediation covers `design.md` (still conforming downstream to
    `requirements.md`, never editing it).
  - `implement-tasks.md`: input documents and authority order gain `design.md`.
- **Rationale**: Inserting a first-class stage requires the surrounding stages to consume and
  trace it; otherwise the chain is broken or design/plan content duplicates.
- **User Evidence**: Confirmed the change list including "spec-to-plan 收窄"; confirmed the
  plan-template slimming ripple during the design-template analysis.
- **Confirmed At**: 2026-08-12

### NEED-008: Installer registration and lockstep count/doc/test/README updates

- **Status**: confirmed
- **Statement**: Register `spec-to-design` and `review-design` in
  `src/codexspec/commands/installer.py` (`get_commands_metadata()`, category `core`), and
  update, in lockstep: the function's docstring total; the inline `# <Category> Commands (N)`
  count; the command-count assertions in **both** `tests/commands/test_installer.py` and
  `tests/test_cli.py`; and a row in every `README*.md` (translated per language). The derived
  `.claude/commands/` and `.agents/skills/` artifacts are regenerated at release
  (publish → init), never hand-edited.
- **Rationale**: Adding distributed commands without updating every count/doc/test/README site
  drifts a check or ships an inconsistent command list.
- **User Evidence**: Profile record `Con-2026-0811-1418yq-1` (adding a distributed command
  requires lockstep count/doc updates), confirmed applicable here for two new commands.
- **Confirmed At**: 2026-08-12

## Constraints

### CON-001: Self-bootstrap — edit only `templates/`

- **Status**: confirmed
- **Statement**: Author all command/template changes under `templates/`. The derived install
  artifacts `.claude/commands/codexspec/` and `.agents/skills/codexspec-*/` are regenerated
  from templates via publish → `codexspec init` and MUST NOT be hand-edited.
- **User Evidence**: "遵循 self-bootstrap(只改 templates/…不得手改)".

### CON-002: Constitution untouched

- **Status**: confirmed
- **Statement**: Neither `.codexspec/memory/constitution.md` nor `_get_default_constitution()`
  is modified by this feature. (The two constitutions are independent and must not be synced.)
- **User Evidence**: "constitution 完全不动(两部宪法不混淆)".

### CON-003: English templates with `## Language Preference`

- **Status**: confirmed
- **Statement**: New command templates are authored in English and carry the standard
  `## Language Preference` section, following the LLM dynamic-translation i18n convention.
- **User Evidence**: "模板英文 + `## Language Preference` 段".

### CON-004: Design refines implementation design, never redefines product intent

- **Status**: confirmed
- **Statement**: `spec-to-design` may make plan-level/implementation design decisions but must
  not change confirmed scope, behavior, constraints, or trade-offs — analogous to the existing
  constraint on `spec-to-plan`'s plan-level decisions. It stops and requests a user decision
  when a design choice would alter product intent.
- **User Evidence**: "acts as 受约束的系统设计者(不改产品意图)".

### CON-005: Lockstep count discipline for new distributed commands

- **Status**: confirmed
- **Statement**: The count/doc/test/README sites in NEED-008 must be updated together; a full
  test-suite run must be green before release, since `tests/test_cli.py`'s independent count
  assertion is only caught by the full suite.
- **User Evidence**: Profile `Con-2026-0811-1418yq-1`: the `test_cli.py` count assertion "was
  only caught when the full suite failed after the others were fixed."

## Decisions

### DEC-001: Option A — split, design elevated to a first-class stage

- **Status**: confirmed
- **Decision**: Split design out of `spec-to-plan` into its own first-class stage.
- **Alternatives Rejected**: B (optional insert, backward-compatible) — leaves the design/plan
  conflation on the default path and adds a bimodal `spec-to-plan`; C (standalone reference
  artifact) — design escapes the authority chain, not closing the gap.
- **Reason**: Only A properly separates *what the system is* from *how to build it*, gives
  design a traceable first-class artifact with its own review gate, and matches the
  requirements/design/tasks decomposition. Existing artifacts are not broken (spec.md
  unchanged; plan just also consumes design.md) — the cost is mostly template authoring.
- **User Evidence**: Selected A over B and C.

### DEC-002: `design.md` content = fused core + on-demand sections

- **Status**: confirmed
- **Decision**: See NEED-004 (fixed architecture/components + ADR-lite; data-model / API /
  sequence / cross-cutting appear on demand).
- **Alternatives Rejected**: "只做骨架" (architecture/components only, everything else deferred
  to separate P1 commands); "一次做全" (build adr + api-design + data-model as standalone
  commands now — scope too large for a single P0).
- **Reason**: Fused + on-demand gives a complete-but-scalable design artifact without new
  commands.
- **User Evidence**: Chose "融合+按需成章".

### DEC-003: Add a dedicated `review-design` command

- **Status**: confirmed
- **Decision**: Ship `review-design` symmetric with the other three review commands.
- **Alternatives Rejected**: Inline validation inside `spec-to-design` with no separate review
  command (asymmetric with the pipeline; weaker gate).
- **Reason**: Keeps per-stage traceable-review + auto_next gating uniform across the pipeline.
- **User Evidence**: Chose "新增 review-design".

### DEC-004: Division of concerns — design = what, plan = how

- **Status**: confirmed
- **Decision**: `design.md` = *what the system is* (components / interfaces / data model /
  key design decisions / flows). `plan.md` = *how to build it* (implementation phases /
  ordering / verification strategy / tech stack).
- **Reason**: A clean, non-overlapping split of the two concerns currently conflated in the
  plan templates (see NEED-007 plan-template slimming).
- **User Evidence**: Confirmed the AI-proposed division ("确认提案的三项").

### DEC-005: Covers notation — extend the existing `Covers: REQ; Plan:` pattern

- **Status**: confirmed
- **Decision**: Extend the traceability notation that `tasks` already uses (ultimate REQ
  anchor + immediate-upstream pointer):
  - design component: `Covers: REQ-xxx`
  - plan component: `Covers: REQ-xxx; Design: <design component>`
  - tasks: unchanged (`Covers: REQ-xxx; Plan: <component/phase>`)
  Every artifact keeps its ultimate REQ anchor plus a direct upstream pointer; `analyze` can
  both aggregate by REQ and validate the chain level by level.
- **Alternatives Rejected**: Cite only the immediate upstream (plan → design → REQ) — most DRY
  but forces `analyze` to walk the chain and is inconsistent with the existing tasks notation.
- **Reason**: Minimal churn, consistent with existing style, self-tracing artifacts.
- **User Evidence**: Chose "认可平移方案". Whether design components get a formal ID prefix
  (e.g. `DES-xxx`) is deferred to spec (OPEN-001).

### DEC-006: Design stage always in the chain; output scales with complexity

- **Status**: confirmed
- **Decision**: The design stage always runs as part of the chain; its output scales with
  complexity (a trivial feature may produce a thin "no significant design decisions" page).
- **Reason**: A uniform chain with a first-class stage, without forcing heavy design content on
  trivial features — consistent with "not padding template sections".
- **User Evidence**: Confirmed the AI-proposed default ("确认提案的三项").

### DEC-007: Single design template (not two-tier)

- **Status**: confirmed
- **Decision**: One `design-template.md` (fixed core + optional sections), no simple/detailed
  split. See NEED-006.
- **Alternatives Rejected**: Two-tier `design-template-simple.md` + `-detailed.md` (consistent
  with spec/plan/tasks but reintroduces the coarse, error-prone tier pre-selection).
- **Reason**: In-file on-demand sections already realize scale-to-complexity; two-tier is
  redundant with it.
- **User Evidence**: Chose "单模板(固定核心+可选章节)".

### DEC-008: `review-design` Compatibility Score formula copied verbatim

- **Status**: confirmed
- **Decision**: `review-design` uses the exact Severity / Status / Compatibility Score formula
  of the other review commands, unchanged.
- **Reason**: Cross-review consistency.
- **User Evidence**: OPEN-003 answered "保持一致".

### DEC-009: No Git Branch Safety Check on the design stage

- **Status**: confirmed
- **Decision**: `spec-to-design` does not add a Git Branch Safety Check section.
- **Reason**: The design stage runs inside an already-created feature branch.
- **User Evidence**: OPEN-004 answered "不加".

### DEC-010: No `pyproject.toml` include change

- **Status**: confirmed
- **Decision**: Adding `templates/docs/design-template.md` and the new command templates
  requires no change to `pyproject.toml` include/force-include.
- **Reason**: `templates/` is already force-included in the wheel and listed in the sdist; the
  new files land under existing shipped paths.
- **User Evidence**: OPEN-005 answered "不需要".

## Out of Scope

### OUT-001: No standalone `adr` / `api-design` / `data-model` commands

- **Status**: confirmed
- **Statement**: This feature does not add standalone `adr`, `api-design`, or `data-model`
  commands. Those capabilities exist as on-demand sections of `design.md`.
- **Reason**: Keeps the P0 focused; those remain P1/future.
- **User Evidence**: "本次不做 adr/api-design/data-model 独立命令(留 P1/后续)".

### OUT-002: `review-code` unchanged

- **Status**: confirmed
- **Statement**: `review-code` is not modified by this feature.
- **Reason**: It is a defect gate, orthogonal to the design stage.
- **User Evidence**: "不改 review-code(缺陷门禁,与 design 阶段正交)".

## Open Questions

### OPEN-001: Formal ID scheme for design components

- **Status**: open
- **Why It Matters**: Determines how `plan.md`'s `Design:` pointer and `analyze` reference
  design components. Non-blocking: the `Covers` notation (DEC-005) is fixed; only whether
  design components get a formal ID prefix (e.g. `DES-xxx`) versus stable named references is
  left for `spec` to decide.
- **Owner**: Research (resolve in `generate-spec` / `spec-to-plan` design)

## Confirmation Log

### Session 2026-08-12

- **Summary Presented**: spec-to-design as a first-class pipeline stage (Option A split);
  design.md fused + on-demand sections; dedicated review-design; single design template;
  Covers notation shift-over; downstream updates to generate-spec / spec-to-plan (+ plan
  template slimming) / plan-to-tasks / analyze / implement-tasks; installer + lockstep
  count/doc/test/README updates.
- **User Confirmation**: Confirmed the three AI proposals (division of concerns, always-in-chain
  scalable output, `spec-to-design` naming); resolved OPEN items — accepted the Covers
  shift-over, chose the single design template, "保持一致" (score formula), "不加" (branch
  check), "不需要" (pyproject).
- **Entries Confirmed**: NEED-001..008, CON-001..005, DEC-001..010, OUT-001..002.
