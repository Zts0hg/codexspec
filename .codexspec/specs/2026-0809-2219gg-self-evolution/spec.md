# Feature Specification: self-evolution

<!--
Language: Generate this document in the language specified in .codexspec/config.yml
If not configured, use English.
-->

**Feature Branch**: `2026-0809-2219gg-self-evolution`
**Created**: 2026-08-09
**Status**: Draft
**Input**: `.codexspec/specs/2026-0809-2219gg-self-evolution` (compiled from `requirements.md`)

## Context

CodexSpec's strength is the front half of the lifecycle (requirements → spec → plan →
tasks → implement) with strong traceability. Knowledge produced *during* that work —
reusable conventions, negative constraints, recurring pitfalls, cross-feature
architectural decisions — is not captured anywhere and is lost to conversation
scrollback. There is also no governed path for a user's accumulated project knowledge to
flow back and improve CodexSpec itself.

This feature adds a **self-evolution** capability as two new distributed commands plus a
storage substrate:

- **`distill`** — extracts reusable, cross-feature knowledge from an interaction into a
  project-level store, `.codexspec/profile/`.
- **`evolve`** — compiles vetted profile sediment into a SKILL.md / command-template
  draft and contributes it upstream via a reviewed PR.
- **`.codexspec/profile/`** — the storage substrate (not a command).

## Goals

- Turn what is today lost in conversation into durable, structured, **auditable** reusable
  knowledge at the project level.
- Give users a governed, human-reviewed path to contribute capability back to CodexSpec.
- Make capture **mostly automatic** (embedded in existing wrap-up commands), not
  dependent on the user remembering to run it.
- Stay within CodexSpec's LLM-instruction-markdown positioning — no runtime engine.

## User Scenarios & Testing

### User Story 1 — Automatic, evidence-backed knowledge capture (`distill`) (Priority: P1)

As a developer using CodexSpec, I want reusable knowledge from my work to be captured
automatically into a durable project store, with each item traceable to its evidence, so
that conventions/constraints/pitfalls are not lost and can be trusted and audited later.

**Why this priority**: `distill` is the foundation; `evolve` consumes its output, so
distill delivers standalone value first.

**Independent Test**: Complete an `implement-tasks` run in which a reusable convention and
a pitfall surfaced; observe that `distill` runs at completion (with `workflow.auto_distill`
enabled) and writes evidence-backed records to `.codexspec/profile/`, while feature-level
requirement rationale is NOT copied there.

**Acceptance Scenarios**:

1. **Given** `workflow.auto_distill: true` and an interaction that produced a reusable
   cross-feature convention, **When** a wrap-up command (`implement-tasks` completion, or
   `commit-staged`/`pr`) finishes, **Then** `distill` runs once on the delta and appends
   an evidence-backed record to `.codexspec/profile/conventions.md`.
2. **Given** the interaction contained only feature-level requirement rationale (the kind
   `requirements.md` already records), **When** `distill` runs, **Then** it writes nothing
   to the profile for that content (boundary test: "would a single feature's
   requirements/spec/plan record it?").
3. **Given** the delta contains nothing reusable, **When** `distill` runs, **Then** it
   early-exits and writes nothing.
4. **Given** a new correction conflicts with an existing profile rule, **When** `distill`
   adjudicates, **Then** it applies recency/specificity/scenario-decoupling; if still
   unresolvable it records `status: conflict/needs-adjudication` and neither guesses nor
   blocks.
5. **Given** the user invokes `/distill` manually, **When** it runs, **Then** it performs
   the same extraction on the supplied/most-recent interaction segment.
6. **Given** a new verified fact supersedes an outdated rule, **When** `distill` writes,
   **Then** it uses a `replace` (not a duplicate append), keeping the file dense; the prior
   version remains recoverable from git history.
7. **Given** an extracted item with `derivation = explicit` verified by an outcome, **When**
   `distill` writes it, **Then** `status = vetted`; an `inferred` item is written
   `status = candidate`.
8. **Given** pending `candidate` records, **When** the user runs `/distill review`, **Then**
   distill lists them compactly and applies vet/edit/drop by editing `status`; the user never
   hand-edits the files.

### User Story 2 — Governed contribution back to CodexSpec (`evolve`) (Priority: P1)

As a user who has accumulated vetted project knowledge, I want to contribute a generalized
capability back to CodexSpec through a reviewed PR, so that my sediment can become a shared
capability without me hand-crafting a template.

**Why this priority**: This is the differentiating capability; it depends on distill's
output existing and being vetted.

**Independent Test**: With vetted, generally-useful sediment in `.codexspec/profile/`, run
`evolve`; observe an imperative-worded SKILL.md/template draft targeting `templates/` and a
PR (branch or fork, auto-selected) with a one-sentence value summary — never an unattended
merge.

**Acceptance Scenarios**:

1. **Given** vetted sediment general enough for the toolkit, **When** `evolve` runs, **Then**
   it compiles a SKILL.md / command-template draft under `templates/` (never
   `.claude/commands/codexspec/`) and opens a PR for human review.
2. **Given** the caller has upstream write access, **When** `evolve` prepares the PR, **Then**
   it pushes a branch in-repo; **Given** no write access, **Then** it auto-forks and opens a
   cross-repo PR — identical review path either way.
3. **Given** the compiled draft, **When** it is produced, **Then** wording is imperative
   (必须/始终/严禁/仅允许), negative constraints are ordered right after core needs, and no
   superseded/contradictory rule remains.
4. **Given** `evolve` cannot state a crisp one-sentence value, **When** it evaluates the
   batch, **Then** it opens no PR (value gate).
5. **Given** a promoted change later proves worse, **When** the user rolls back, **Then** the
   rollback is a `remove`/`replace` (git-traceable), not a manual file edit.
6. **Given** a compiled draft ready to contribute, **When** `evolve` is about to push/open a
   PR, **Then** it first presents the draft + value statement and proceeds only on explicit
   user approval.

### Edge Cases & Expected Error Behavior

- **`auto_distill` set to `false`**: no automatic capture; manual `/distill` still works.
  (Default is on; only an explicit `false` disables.) Not an error.
- **Empty/again-run delta**: `distill` early-exits and reports nothing captured.
- **Unresolvable conflict**: recorded as `status: conflict`; surfaced later, never guessed.
- **No profile yet**: first `distill` creates `.codexspec/profile/` and the relevant file.
- **Nothing worth promoting**: `evolve` opens no PR and says why (value gate).

## Requirements

### Functional Requirements

- **REQ-001**: `distill` MUST read a segment of interaction and extract reusable,
  cross-feature knowledge into `.codexspec/profile/`.
  - Sources: NEED-001
- **REQ-002**: `distill` MUST apply the boundary test — "would a single feature's
  `requirements`/`spec`/`plan` record this?" — and MUST NOT capture content that belongs in
  per-feature SDD artifacts (esp. requirement rationale).
  - Sources: CON-001, OUT-004
- **REQ-003**: `distill` MUST write only to the project-level profile; it MUST NOT create a
  feature-local sediment tier.
  - Sources: CON-002, OUT-002
- **REQ-004**: Every profile record MUST separate `claim` from `evidence` — with
  `evidence.facts` (quoting the original words), `evidence.state` (context/validity),
  `provenance` (source/derivation `explicit|inferred`), and `status` (`candidate`/`vetted`).
  - Sources: NEED-004, CON-003
- **REQ-005**: `distill` MUST be auto-triggerable via command-embedding in wrap-up commands
  and MUST also support manual `/distill`; the embedded trigger MUST be gated by
  `workflow.auto_distill` — **enabled by default, disabled only when explicitly set to the
  literal `false`** — and MUST early-exit when the delta has nothing to capture.
  - Sources: NEED-003, DEC-003
- **REQ-006**: `distill` MUST NOT be triggered via Claude Code hooks.
  - Sources: CON-005, OUT-003
- **REQ-007**: `.codexspec/profile/` MUST consist of `constraints.md` (negative constraints,
  highest-weight, honored first), `conventions.md` (positive conventions/steering),
  `pitfalls.md`, and `decisions.md` (cross-feature/architectural ADR-lite only).
  - Sources: DEC-002
- **REQ-008**: On conflict, `distill` MUST adjudicate by recency, then specificity, then
  scenario-decoupling (`scope/when`), and otherwise defer (`status: conflict`) without
  guessing or blocking.
  - Sources: DEC-004
- **REQ-009**: Profile files MUST hold only current-effective knowledge and be mutated only
  by the `add`/`replace`/`remove` discipline; git history is the audit ledger; no in-file
  retired section.
  - Sources: CON-004
- **REQ-010**: `evolve` MUST compile vetted sediment into a SKILL.md / command-template draft
  and open a PR; it MUST auto-detect branch (write access) vs fork (no access) and MUST NOT
  merge unattended.
  - Sources: NEED-002, CON-006, OUT-006
- **REQ-011**: `evolve`'s compiled output MUST use imperative wording, order negative
  constraints right after core needs, and carry no superseded/contradictory rules.
  - Sources: DEC-005
- **REQ-012**: `evolve` MUST write only under `templates/` (or a standalone skill package),
  never `.claude/commands/codexspec/`; changes reach users via `publish` → `init`.
  - Sources: CON-007
- **REQ-013**: `evolve` MUST produce a one-sentence value statement as the PR summary and
  MUST open no PR when no crisp value can be stated (value gate).
  - Sources: DEC-006
- **REQ-014**: `distill` MUST set `status: vetted` only for records with `derivation = explicit`
  that were verified by an outcome; all `inferred` records stay `candidate`. Candidate
  promotion MUST be available through an interactive review mode (manual `/distill review`)
  that edits status on the user's inline approval; the user MUST NOT need to hand-edit profile
  files.
  - Sources: DEC-007
- **REQ-015**: `evolve` MUST present the compiled draft and value statement and obtain explicit
  user approval before any `git push` or PR creation; it MUST NOT push or open a PR unattended.
  - Sources: DEC-008

### Non-Functional Requirements

- **NFR-001**: The commands MUST be LLM-instruction markdown only — no runtime engine: no
  substring-match tool primitive (`replace` is a semantic-edit discipline), no `scope/when`
  DSL, no dedup algorithm, no metric engine.
  - Sources: CON-008, OUT-001
- **NFR-002**: New templates MUST stay in English with the standard `## Language Preference`
  section.
  - Sources: CON-009
- **NFR-003**: No eval / metric-driven (DSPy/GEPA) optimization is implemented; the
  value-statement gate is the sole lightweight quality signal.
  - Sources: OUT-001
- **NFR-004**: The profile MUST be project-level and typed (convention/constraint/pitfall/
  decision); Hermes's `USER.md`/`MEMORY.md` subject-split MUST NOT be adopted.
  - Sources: OUT-005

## Confirmed Constraints and Decisions

- **DEC-A — Implementation location**: New commands are authored as
  `templates/commands/distill.md` and `templates/commands/evolve.md` (source of truth).
  `workflow.auto_distill` is added to config handling. The distill trigger section is
  embedded into the existing wrap-up templates (`implement-tasks.md`, `commit-staged.md`,
  `pr.md`). The `.claude/commands/codexspec/` copies are regenerated by reinstall, never
  hand-edited (self-bootstrap; CON-007).
- **DEC-B — Substrate is documented, files are runtime-created**: `.codexspec/profile/` and
  its record format are specified in the templates; the actual files are created by `distill`
  at runtime, not shipped empty.

## Out of Scope

- **OUT-001**: No eval / GEPA metric-driven optimization (NFR-003).
- **OUT-002**: No feature-local sediment tier (REQ-003).
- **OUT-003**: No hook-based triggering (REQ-006).
- **OUT-004**: `distill` does not recapture feature-level requirement rationale (REQ-002).
- **OUT-005**: Hermes `USER.md`/`MEMORY.md` subject-split not adopted (NFR-004).
- **OUT-006**: No fully-automated upstream contribution; human review always gates (REQ-010).
- **OUT-007**: The other five P0 themes (`spec-to-design`, `debug`, `release-notes`,
  `onboard`, `reverse-spec`) are separate features, not part of this one.

## Assumptions

- **ASMP-S1**: "Reusable / cross-feature" and "general enough for the toolkit" are semantic
  judgments the LLM makes at runtime from the instructions; no scoring mechanism is built
  (restates CON-008, not a new decision).
- **ASMP-S2**: The wrap-up commands chosen for embedding (`implement-tasks`, `commit-staged`,
  `pr`) are the natural session end-points where cross-feature knowledge has surfaced
  (restates DEC-003).

## Dependencies

- `templates/commands/implement-tasks.md`, `commit-staged.md`, `pr.md` — gain an embedded
  distill trigger section.
- `.codexspec/config.yml` handling — gains the `workflow.auto_distill` key.
- Anthropic Agent Skills (SKILL.md) format + existing CodexSpec command-template conventions
  — the shape of `evolve`'s output.
- `templates/commands/` governance (self-bootstrap, i18n, Language Preference).

## Requirements Traceability

| Confirmed Requirement | Spec Coverage | Notes |
|-----------------------|---------------|-------|
| NEED-001 | REQ-001 | distill extraction |
| NEED-002 | REQ-010 | evolve contribution |
| NEED-003 | REQ-005 | auto-trigger + manual |
| NEED-004 | REQ-004 | evidence-backed records |
| CON-001 | REQ-002 | boundary test |
| CON-002 | REQ-003 | project-level only |
| CON-003 | REQ-004 | claim/evidence separation |
| CON-004 | REQ-009 | add/replace/remove + git ledger |
| CON-005 | REQ-005, REQ-006 | embed + manual, no hook |
| CON-006 | REQ-010 | unified PR, branch/fork mechanics |
| CON-007 | REQ-012 | self-bootstrap templates only |
| CON-008 | NFR-001 | LLM-instruction, no runtime engine |
| CON-009 | NFR-002 | i18n + Language Preference |
| DEC-001 | REQ-001, REQ-010 | two commands + substrate |
| DEC-002 | REQ-007 | three files, constraints elevated |
| DEC-003 | REQ-005, DEC-A | trigger points + gate |
| DEC-004 | REQ-008 | conflict adjudication |
| DEC-005 | REQ-011 | evolve compile rules |
| DEC-006 | REQ-013 | value gate |
| DEC-007 | REQ-014 | vetting rule + review mode |
| DEC-008 | REQ-015 | evolve pre-PR confirmation |
| OUT-001..006 | OUT-001..006 | mirrored |

**Open items**: None blocking. All material questions were resolved during discovery
(OPEN-001 resolved by DEC-003).
