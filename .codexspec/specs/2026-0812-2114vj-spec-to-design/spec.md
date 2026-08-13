# Feature Specification: spec-to-design

**Feature ID**: `2026-0812-2114vj`
**Authority Mode**: Requirements-first
**Source of Truth**: `requirements.md` (all entries `Status: confirmed`)

## Context

CodexSpec's authoritative pipeline is `requirements → spec → plan → tasks`, with a per-stage
review gate and `auto_next` advancement. Today `spec-to-plan` conflates two concerns — *what
the system is* (architecture, components, data model, design decisions) and *how to build it*
(phases, ordering, verification). This is the identified "front-half design layer" gap.

This feature inserts a first-class **design** stage: the chain becomes
`requirements → spec → design → plan → tasks`. `design.md` is a traceable first-class artifact
(`Covers: REQ-xxx`) with its own review gate (`review-design`), and `spec-to-plan` narrows to
pure implementation planning that consumes `design.md`.

## Goals

- Add a producer command (`spec-to-design`) and a review command (`review-design`) symmetric
  with the existing pipeline stages.
- Give design a single, scale-to-complexity template and a place in the authority chain.
- Update the surrounding pipeline (generate-spec, spec-to-plan + its templates, plan-to-tasks,
  analyze, implement-tasks) so the inserted stage is coherent end to end, with no design/plan
  content overlap.

## Non-Goals

- Standalone `adr` / `api-design` / `data-model` commands (they are on-demand `design.md`
  sections; remain P1).
- Any change to `review-code` or to either constitution.

## User-Visible Scenarios

### Scenario 1 — Author runs the design stage

Given a feature with a confirmed `requirements.md` and generated `spec.md`, when the author
runs `/codexspec:spec-to-design <feature-dir>` (or reaches it via `auto_next` from
`generate-spec`), then a `design.md` is produced from `design-template.md`: the fixed core
(Architecture & Components, ADR-lite Key Design Decisions, Requirements Coverage) is always
present, optional sections appear only when the feature warrants them, and every design
component / interface / data change / decision carries `Covers: REQ-xxx`. The command then
runs its embedded review loop and, on a passing gate with `auto_next` enabled, advances to
`spec-to-plan`.

### Scenario 2 — Design stage reviewed by its own gate

Given a saved `design.md`, when `review-design` runs, then it reports Fidelity & Coverage and
Feasibility findings using the same Severity / Status / Compatibility Score taxonomy as the
other review commands, and saves `review-design.md`. Overall Status `PASS` /
`PASS_WITH_WARNINGS` allows `auto_next`; `NEEDS_REVISION` / `BLOCKED` halts the chain.

### Scenario 3 — Downstream stages consume design

Given a `design.md` in the feature directory, when `spec-to-plan` runs, then it acts as an
implementation planner: it reads `design.md`, produces a `plan.md` whose components carry
`Covers: REQ-xxx; Design: <design component>`, and does not re-emit design content (the plan
templates no longer contain Architecture / Component Structure / Data Models / API Contracts /
ADR-style Decisions). `plan-to-tasks` and `implement-tasks` treat `design.md` as authority
between `spec` and `plan`, and `analyze` validates the deepened chain
`confirmed → REQ → design → plan → task`.

### Scenario 4 — Trivial feature, thin design

Given a trivial feature with no significant design decisions, when `spec-to-design` runs, then
`design.md` may be a thin page recording "no significant design decisions" with only the fixed
core; no optional section is forced.

## Functional Requirements

### REQ-001: `spec-to-design` command

- **Statement**: `templates/commands/spec-to-design.md` exists as a distributed command. It
  reads `requirements.md` + `spec.md`, produces `<feature-dir>/design.md`, acts as a
  constrained system designer, and is structured symmetrically with `spec-to-plan`
  (Language Preference, Feature Resolution, Authority & Stop Conditions, planning/design rules,
  Required Output, Pre-Save Validation, Automatic Review Loop, Auto-Next Chain Advance, Output
  Summary).
- **Sources**: NEED-001, NEED-002, DEC-001
- **Acceptance**: The template exists under `templates/commands/`, is English with a
  `## Language Preference` section, and produces `design.md` from `design-template.md`.

### REQ-002: `design.md` content — fixed core plus on-demand sections

- **Statement**: `design.md` always contains Architecture & Components and ADR-lite Key Design
  Decisions and a Requirements Coverage table; Data Models / Key Entities, API / Interface
  Contracts, Sequence & Data Flow, cross-cutting (performance / security / availability)
  design, and Risks & Trade-offs appear only when warranted. No section is required merely
  because the template contains it.
- **Sources**: NEED-004, DEC-002, DEC-006
- **Acceptance**: `design-template.md` marks its optional sections as include-when-relevant;
  `spec-to-design` instructs scale-to-complexity output.

### REQ-003: Design traceability into the authority chain

- **Statement**: Every design component / interface / data change / design decision carries
  `Covers: REQ-xxx`, and `design.md` includes a Requirements Coverage table mapping REQ/NFR to
  design coverage.
- **Sources**: NEED-005, DEC-005
- **Acceptance**: `spec-to-design` and `design-template.md` require the `Covers:` field and the
  coverage table.

### REQ-004: Embedded review loop and auto_next in `spec-to-design`

- **Statement**: `spec-to-design` invokes `/codexspec:review-design <feature-dir>/design.md`
  in an automatic fix-and-review loop (max two rounds; only verified, upstream-determined
  fixes; never auto-fix advisories; never introduce a new product decision), and includes an
  Auto-Next Chain Advance section that invokes `/codexspec:spec-to-plan <feature-dir>` when
  `workflow.auto_next` is `true` and the review concluded `PASS` / `PASS_WITH_WARNINGS`.
- **Sources**: NEED-002, DEC-003
- **Acceptance**: The command mirrors `spec-to-plan`'s review-loop and auto_next sections.

### REQ-005: `review-design` command

- **Statement**: `templates/commands/review-design.md` exists as a distributed command,
  structurally symmetric with `review-spec` / `review-plan` / `review-tasks`: Review Authority
  (authority order including `design`), Fidelity & Coverage pass, Feasibility & Internal
  Quality pass, Risk Advisories / Design Opportunities, the same Severity / Status taxonomy,
  the **identical** Compatibility Score formula, and it saves `<feature-dir>/review-design.md`.
  It does not add a Git Branch Safety Check.
- **Sources**: NEED-003, DEC-003, DEC-008, DEC-009
- **Acceptance**: The Compatibility Score formula text matches the other review commands
  verbatim; the report file is `review-design.md`.

### REQ-006: Single `design-template.md`

- **Statement**: A single `templates/docs/design-template.md` is added (fixed core + optional
  sections; no simple/detailed split) and copied into `.codexspec/templates/docs/` by
  `codexspec init` via the existing docs-copy logic. No `pyproject.toml` include change is
  required.
- **Sources**: NEED-006, DEC-007, DEC-010
- **Acceptance**: `init` produces `.codexspec/templates/docs/design-template.md`; no
  `-simple`/`-detailed` design template exists; `pyproject.toml` is unchanged.

### REQ-007: `generate-spec` retargets auto_next to `spec-to-design`

- **Statement**: `generate-spec.md`'s Auto-Next Chain Advance invokes
  `/codexspec:spec-to-design <feature-dir>` instead of `/codexspec:spec-to-plan`.
- **Sources**: NEED-007, NEED-001
- **Acceptance**: The auto_next notice/invocation in `generate-spec.md` names `spec-to-design`.

### REQ-008: `spec-to-plan` narrowed to implementation planner

- **Statement**: `spec-to-plan.md` is narrowed: role changes from "constrained technical
  designer" to implementation planner; it reads `design.md`; plan components carry
  `Covers: REQ-xxx; Design: <design component>`; its authority order gains `design`
  (requirements > spec > design > plan). The plan templates
  (`plan-template-detailed.md` and the "Design Document" `plan-template-simple.md`) are slimmed
  so the design-only sections that migrate to `design.md` (Architecture / Component Structure /
  Data Models / API Contracts / ADR-style Decisions) are removed, leaving plan as Tech Stack +
  Implementation Phases + Verification + Requirements Coverage.
- **Sources**: NEED-007, DEC-004, DEC-005
- **Acceptance**: `spec-to-plan.md` reads `design.md` and uses the `Design:` pointer notation;
  the slimmed plan templates contain no design-only sections; `plan.md` and `design.md` do not
  overlap.

### REQ-009: `plan-to-tasks` consumes design

- **Statement**: `plan-to-tasks.md` reads `design.md` as context; its authority order gains
  `design`. Task notation is unchanged (`Covers: REQ-xxx; Plan: <component/phase>`).
- **Sources**: NEED-007, DEC-005
- **Acceptance**: `plan-to-tasks.md` lists `design.md` among its inputs/authority; task notation
  is unchanged.

### REQ-010: `analyze` deepens the traceability chain

- **Statement**: `analyze.md`'s end-to-end chain becomes
  `confirmed → REQ → design → plan → task`; completeness/consistency detection and
  authority-directed remediation cover `design.md` (still conforming downstream artifacts to
  `requirements.md`, never editing `requirements.md`).
- **Sources**: NEED-007, DEC-005
- **Acceptance**: `analyze.md` names `design.md` in its inputs and chain; remediation direction
  still flows from requirements downward and never edits `requirements.md`.

### REQ-011: `implement-tasks` treats design as authority

- **Statement**: `implement-tasks.md`'s input documents and authority order gain `design.md`
  (requirements > spec > design > plan > tasks).
- **Sources**: NEED-007, DEC-005
- **Acceptance**: `implement-tasks.md` reads `design.md` and places it in the authority order.

### REQ-012: Installer registration and lockstep updates

- **Statement**: `src/codexspec/commands/installer.py` registers `spec-to-design` and
  `review-design` (category `core`) in `get_commands_metadata()`. Updated in lockstep: the
  function docstring total; the inline `# <Category> Commands (N)` count; the command-count
  assertions in both `tests/commands/test_installer.py` and `tests/test_cli.py`; and a row in
  every `README*.md` (translated per language).
- **Sources**: NEED-008, CON-005
- **Acceptance**: The full test suite is green (both count assertions updated); every
  `README*.md` lists the two new commands; the derived `.claude/commands/` / `.agents/skills/`
  are not hand-edited.

### REQ-013: Authority order includes design across affected commands

- **Statement**: Every affected command that states an authority order uses
  `requirements > spec > design > plan > tasks` (or the applicable subset), inserting `design`
  immediately below `spec`.
- **Sources**: NEED-001, DEC-005
- **Acceptance**: `spec-to-plan`, `plan-to-tasks`, `implement-tasks`, and the review commands
  that state an authority order place `design` directly below `spec`.

### REQ-014: `spec-to-design` does not redefine product intent

- **Statement**: `spec-to-design` makes design/implementation decisions but must not change
  confirmed scope, behavior, constraints, or trade-offs; it stops and requests a user decision
  when a design choice would alter product intent, mirroring `spec-to-plan`'s Stop Conditions.
- **Sources**: CON-004, NEED-002
- **Acceptance**: The command has Authority & Stop Conditions equivalent to `spec-to-plan`'s.

## Non-Functional Requirements

### NFR-001: Self-bootstrap authoring boundary

- **Statement**: All changes are authored under `templates/` and `src/codexspec/`; the derived
  `.claude/commands/codexspec/` and `.agents/skills/codexspec-*/` are regenerated via
  publish → `codexspec init` and are never hand-edited.
- **Sources**: CON-001

### NFR-002: Constitution untouched

- **Statement**: Neither `.codexspec/memory/constitution.md` nor `_get_default_constitution()`
  is modified.
- **Sources**: CON-002

### NFR-003: English templates with dynamic-translation i18n

- **Statement**: New command templates are English and carry the standard
  `## Language Preference` section.
- **Sources**: CON-003

## Constraints and Decisions (carried from requirements)

- Option A split, design first-class (DEC-001); fused + on-demand content (DEC-002);
  dedicated review-design (DEC-003); design=what / plan=how (DEC-004); Covers shift-over
  (DEC-005); always-in-chain scalable output (DEC-006); single design template (DEC-007);
  identical score formula (DEC-008); no branch check (DEC-009); no pyproject change (DEC-010).

## Out of Scope

- **OUT-001**: No standalone `adr` / `api-design` / `data-model` commands (on-demand
  `design.md` sections instead).
- **OUT-002**: `review-code` is unchanged.

## Open Questions

- **OPEN-001** (non-blocking): whether design components use a formal ID prefix (e.g.
  `DES-xxx`) or stable named references. The `Covers` notation (DEC-005) is fixed regardless;
  resolved during `spec-to-plan`/`analyze` authoring. Does not block specification.

## Requirements Traceability

| Requirements entry | Spec coverage |
|---|---|
| NEED-001 | REQ-001, REQ-007, REQ-013 |
| NEED-002 | REQ-001, REQ-004, REQ-014 |
| NEED-003 | REQ-005 |
| NEED-004 | REQ-002 |
| NEED-005 | REQ-003 |
| NEED-006 | REQ-006 |
| NEED-007 | REQ-007, REQ-008, REQ-009, REQ-010, REQ-011 |
| NEED-008 | REQ-012 |
| CON-001 | NFR-001 |
| CON-002 | NFR-002 |
| CON-003 | NFR-003 |
| CON-004 | REQ-014 |
| CON-005 | REQ-012 |
| DEC-001 | REQ-001 |
| DEC-002 | REQ-002 |
| DEC-003 | REQ-004, REQ-005 |
| DEC-004 | REQ-008 |
| DEC-005 | REQ-003, REQ-008, REQ-009, REQ-010, REQ-011, REQ-013 |
| DEC-006 | REQ-002 |
| DEC-007 | REQ-006 |
| DEC-008 | REQ-005 |
| DEC-009 | REQ-005 |
| DEC-010 | REQ-006 |
| OUT-001 | Out of Scope OUT-001 |
| OUT-002 | Out of Scope OUT-002 |
| OPEN-001 | Open Questions (non-blocking) |
