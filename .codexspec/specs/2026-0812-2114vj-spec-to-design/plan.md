# Implementation Plan: spec-to-design

**Feature ID**: `2026-0812-2114vj`
**Authority Mode**: Requirements-first (`requirements.md` → `spec.md`)

## Context

Insert a first-class `design` stage into the pipeline (`requirements → spec → design → plan →
tasks`). This is a template/CLI feature: it adds two distributed command templates and one docs
template, edits five existing command templates and two plan docs templates, and registers the
new commands in the installer with lockstep count/doc/test/README updates. No runtime behavior
of the Python CLI changes beyond command registration.

## Goals / Non-Goals

- **Goals**: ship `spec-to-design` + `review-design` + `design-template.md`; make the
  surrounding pipeline consume/trace design; keep every count/doc/test/README site consistent.
- **Non-Goals**: standalone `adr`/`api-design`/`data-model` commands; any `review-code` or
  constitution change; any `pyproject.toml`/init code change.

## Repository Constraints (verified)

- **Self-bootstrap** (NFR-001): edit only `templates/` and `src/codexspec/`. The derived
  `.claude/commands/codexspec/` and `.agents/skills/codexspec-*/` are regenerated at release
  (publish → `codexspec init`) and are NOT touched in this feature.
- **init copies docs templates by glob** — `src/codexspec/__init__.py:744`
  `for template_file in docs_templates_dir.glob("*.md")`. Adding `templates/docs/design-template.md`
  is auto-copied; **no init or `pyproject.toml` change** (verifies DEC-010 / REQ-006).
- **Installer core list** — `src/codexspec/commands/installer.py:get_commands_metadata()`
  currently: core (9), Total 21. Count sites to bump in lockstep: docstring (L50-51 `core (9)`,
  `Total: 21`), inline `# Core Commands (9)` (L54), and the assertions in
  `tests/commands/test_installer.py` + `tests/test_cli.py`.
- **Templates are English + `## Language Preference`** (NFR-003).

## Technical Approach

Mirror existing pipeline commands rather than invent structure. `spec-to-design` is authored
against the shape of `spec-to-plan.md`; `review-design` against `review-plan.md` (copying the
Compatibility Score formula verbatim). `design-template.md`'s fixed core is lifted/adapted from
the existing `plan-template-simple.md` (which is literally titled "Design Document" and already
holds Architecture + ADR-style Decisions + Requirements Coverage); its optional sections are
lifted from `plan-template-detailed.md` (Data Models, API Contracts) and marked
include-when-relevant. The same design-only sections are then removed from the plan templates so
`plan.md` and `design.md` do not overlap.

## Plan-Level Decisions

### PLD-001: List placement follows chain + artifact order

- **Decision**: In the installer core list, place `spec-to-design` between `generate-spec` and
  `spec-to-plan`; place `review-design` between `review-spec` and `review-plan`. Core becomes 11,
  Total 23.
- **Rationale**: Matches the artifact/chain order (spec → design → plan → tasks) so the listed
  order reads as the pipeline.
- **Covers**: REQ-012, REQ-013

### PLD-002: Author `spec-to-design` by mirroring `spec-to-plan.md`

- **Decision**: Sections: Language Preference, User Input, Role ("constrained system designer"),
  Feature Resolution, Authority & Stop Conditions (authority `requirements > spec > design`),
  Design Rules (each component/interface/data change/decision `Covers: REQ`; scale-to-complexity;
  fixed core always, optional sections on demand), Required Output (`design.md` from
  `design-template.md`), Pre-Save Validation, Automatic Review Loop (`review-design`, max two
  rounds), Auto-Next Chain Advance (→ `spec-to-plan`), Output Summary. No Git Branch Safety Check.
- **Rationale**: Structural symmetry with the pipeline; reuse over invention.
- **Covers**: REQ-001, REQ-002, REQ-003, REQ-004, REQ-014

### PLD-003: Author `review-design` by mirroring `review-plan.md`

- **Decision**: Sections: Language Preference, User Input, Review Authority (authority order with
  `design` inserted below `spec`), Review Passes (1 Fidelity & Coverage — every REQ has design
  coverage, each component has `Covers:`; 2 Feasibility & Internal Quality; 3 Advisories),
  Finding Validation, Severity/Status, **Compatibility Score (copied verbatim)**, Report saving
  `review-design.md`.
- **Rationale**: Cross-review consistency (DEC-008).
- **Covers**: REQ-005

### PLD-004: `design-template.md` structure

- **Decision**: Single file. Fixed core: `# Design Document: [FEATURE]`, Context (inherited,
  brief), Architecture & Components (with `Covers: REQ`), Key Design Decisions (ADR-lite:
  Decision / Alternatives / Trade-offs, with `Covers: REQ`), Requirements Coverage table.
  Optional (marked `*(include if …)*`): Data Models / Key Entities, API / Interface Contracts,
  Sequence & Data Flow, Cross-Cutting Design (performance / security / availability), Risks &
  Trade-offs.
- **Rationale**: One-file scale-to-complexity (DEC-006/DEC-007); reuses the existing
  "Design Document" simple-plan structure and the detailed-plan optional sections.
- **Covers**: REQ-002, REQ-003, REQ-006

### PLD-005: Plan-template slimming boundary

- **Decision**: Remove design-only sections from `plan-template-detailed.md` (Architecture
  Overview, Component Structure, Data Models, API Contracts, architecture/ADR-style Decisions,
  and the cross-cutting NFR design sections Security/Performance/Observability that are design
  concerns) and from `plan-template-simple.md` (Architecture, ADR-style Decisions). Plan retains:
  Context, Goals/Non-Goals, Tech Stack, Implementation Phases, Verification, delivery
  Risks/Trade-offs, Requirements Coverage. A plan "Plan-Level Decisions" section is retained but
  re-scoped to implementation-level choices (ordering, tooling), not architecture/design ADRs.
- **Rationale**: Prevent `plan.md`/`design.md` overlap; enact "design = what, plan = how".
- **Covers**: REQ-008

### PLD-006: Test placement

- **Decision**: Add `tests/test_spec_to_design_templates.py` (mirroring
  `tests/test_debug_template.py` / `tests/test_profile_templates.py`) for template presence,
  required-section, and init-copy assertions. Update the command-count assertions in
  `tests/commands/test_installer.py` and `tests/test_cli.py`.
- **Rationale**: Reuse the established template-test pattern; satisfy the lockstep count discipline.
- **Covers**: REQ-012

## Components

### C1: `templates/docs/design-template.md` (new)

- Fixed core + optional sections per PLD-004. **Covers**: REQ-002, REQ-003, REQ-006

### C2: `templates/commands/spec-to-design.md` (new)

- Producer command per PLD-002. **Covers**: REQ-001, REQ-002, REQ-003, REQ-004, REQ-013, REQ-014

### C3: `templates/commands/review-design.md` (new)

- Review command per PLD-003. **Covers**: REQ-005, REQ-013

### C4: `templates/commands/generate-spec.md` (edit)

- Auto-Next Chain Advance retargets to `/codexspec:spec-to-design`. **Covers**: REQ-007

### C5: `templates/commands/spec-to-plan.md` (edit)

- Role narrowed to implementation planner; reads `design.md`; plan components
  `Covers: REQ-xxx; Design: <design component>`; authority order gains `design`. **Covers**:
  REQ-008, REQ-013

### C6: `templates/docs/plan-template-detailed.md` + `plan-template-simple.md` (edit)

- Slimmed per PLD-005. **Covers**: REQ-008

### C7: `templates/commands/plan-to-tasks.md` (edit)

- Reads `design.md` as context; authority order gains `design`; task notation unchanged.
  **Covers**: REQ-009, REQ-013

### C8: `templates/commands/analyze.md` (edit)

- Traceability chain `confirmed → REQ → design → plan → task`; remediation covers `design.md`,
  never edits `requirements.md`. **Covers**: REQ-010

### C9: `templates/commands/implement-tasks.md` (edit)

- Input documents + authority order gain `design.md`. **Covers**: REQ-011, REQ-013

### C10: `src/codexspec/commands/installer.py` (edit)

- Register `spec-to-design` + `review-design` (category `core`, per PLD-001); bump docstring
  `core (9)→(11)` / `Total 21→23` and inline `# Core Commands (9)→(11)`. **Covers**: REQ-012

### C11: `tests/commands/test_installer.py` + `tests/test_cli.py` (edit)

- Update command-count assertions. **Covers**: REQ-012

### C12: `README*.md` (8 files, edit)

- Add a `spec-to-design` and a `review-design` row to each command list (translated per
  language). **Covers**: REQ-012

### C13: `tests/test_spec_to_design_templates.py` (new)

- Presence/structure/init-copy tests per PLD-006. **Covers**: REQ-001..006 (verification),
  REQ-012

### C14: `CLAUDE.md` (edit)

- Add an architecture section for the design stage, the command tables, and implementation
  status. (Project doc; not shipped to users.) **Covers**: implementation support for NEED-007
  documentation.

### C15: `templates/commands/review-plan.md` + `review-tasks.md` (edit)

- `review-plan.md`: authority order gains `design` (below `spec`); Fidelity & Coverage pass
  becomes design-aware — verify the plan covers `design` components (which cover REQ) and that
  the narrowed plan does not re-emit design content. `review-tasks.md`: authority order gains
  `design` (below `spec`). `review-spec.md` is unaffected (its authority order does not state
  the plan/tasks chain). **Covers**: REQ-013

## Implementation Phases

### Phase 1 — New design-stage artifacts (additive)

Create C1 (`design-template.md`), C2 (`spec-to-design.md`), C3 (`review-design.md`). Covers
REQ-001..006, REQ-014.

### Phase 2 — Downstream pipeline edits

Edit C4 (generate-spec auto_next), C5 (spec-to-plan narrow), C6 (plan templates slim), C7
(plan-to-tasks), C8 (analyze), C9 (implement-tasks), C15 (review-plan + review-tasks authority
order). Covers REQ-007..011, REQ-013.

### Phase 3 — Registration, docs, tests

Edit C10 (installer), C11 (count assertions), C12 (READMEs), C14 (CLAUDE.md); add C13 (new
tests). Covers REQ-012.

### Phase 4 — Verification

Run the full test suite to green (both count assertions; new template tests). Confirm no changes
under `.claude/commands/` or `.agents/skills/` (NFR-001) and none to either constitution
(NFR-002).

## Verification Strategy

- **Automated**: `tests/test_spec_to_design_templates.py` asserts the three new files exist with
  required sections (spec-to-design has Automatic Review Loop → review-design + Auto-Next →
  spec-to-plan; review-design saves `review-design.md` and contains the verbatim score formula;
  design-template has the fixed-core headings and `Covers:` usage). An init-copy test asserts
  `codexspec init <tmp> --force` produces `.codexspec/templates/docs/design-template.md`.
  Updated count assertions in `test_installer.py` + `test_cli.py`. Full suite green.
- **Deterministic doc checks**: every `README*.md` contains both new command rows; installer
  metadata length matches the new total.
- **Guard checks**: `git diff --name-only` for the feature shows no `.claude/commands/` /
  `.agents/skills/` / constitution changes.

## Risks / Trade-offs

- **R1 — Wide edit surface**: nine command templates (2 new + 7 edited) + three doc templates
  (1 new design + 2 slimmed plan) + installer + tests + 8 READMEs. Miss
  a count site → suite fails (caught by Phase 4; test_cli.py assertion only surfaces on the full
  suite — see profile `Con-2026-0811-1418yq-1`). Mitigation: lockstep checklist in Phase 3.
- **R2 — Plan/design boundary ambiguity**: the exact section split (esp. cross-cutting NFR
  design) is a judgment call. Mitigation: PLD-005 fixes the boundary; residual is documented,
  not blocking.
- **R3 — Derived artifacts not synced in this feature**: intended (self-bootstrap); the
  `.claude/commands` / `.agents/skills` and marketplace sync happen at release, out of scope here.

## Requirements Coverage

| REQ / NFR | Plan reference |
|---|---|
| REQ-001 | C2, C13, Phase 1 |
| REQ-002 | C1, C2, PLD-004, Phase 1 |
| REQ-003 | C1, C2, PLD-004, Phase 1 |
| REQ-004 | C2, PLD-002, Phase 1 |
| REQ-005 | C3, PLD-003, Phase 1 |
| REQ-006 | C1, PLD-004, verified init glob, Phase 1 |
| REQ-007 | C4, Phase 2 |
| REQ-008 | C5, C6, PLD-005, Phase 2 |
| REQ-009 | C7, Phase 2 |
| REQ-010 | C8, Phase 2 |
| REQ-011 | C9, Phase 2 |
| REQ-012 | C10, C11, C12, C13, PLD-001, PLD-006, Phase 3 |
| REQ-013 | C2, C3, C5, C7, C9, C15, Phase 2 |
| REQ-014 | C2, PLD-002, Phase 1 |
| NFR-001 | Repository Constraints, Phase 4 guard check |
| NFR-002 | Phase 4 guard check |
| NFR-003 | C2, C3 (English + Language Preference) |
