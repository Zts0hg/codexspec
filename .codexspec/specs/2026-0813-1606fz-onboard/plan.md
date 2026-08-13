# Implementation Plan: onboard command

<!--
Language: document language = en. Implementation-planning stage AFTER design.md — HOW to build
the confirmed design in phases. Architecture/components/interfaces live in design.md; referenced
here, not restated.
-->

**Related Spec**: `.codexspec/specs/2026-0813-1606fz-onboard/spec.md`
**Related Design**: `.codexspec/specs/2026-0813-1606fz-onboard/design.md`
**Confirmed Requirements**: `.codexspec/specs/2026-0813-1606fz-onboard/requirements.md`
**Created**: 2026-08-13
**Status**: Draft

## Context

Deliver the `onboard` command as defined in `design.md`. Per Design Decision 1, onboard is a pure
agent-driven **command template** (like `distill` / `debug`) — no new Python runtime module. The
build therefore touches: the new template `templates/commands/onboard.md`, a one-line cross-note in
`templates/commands/distill.md`, the installer registration in `src/codexspec/commands/installer.py`
with its lockstep distribution-surface sites, tests, the 8 READMEs, CLAUDE.md, and the regenerated
derived install artifacts. It reuses the existing `.codexspec/profile/` store and `/distill review`
channel verbatim.

## Goals / Non-Goals

**Goals:**

- Ship `/codexspec:onboard [path]` implementing the confirmed design (scan → conventions immediate
  candidate + constraints inline pre-persist gate → integrate → summary).
- Register it as a distributed `enhanced` command with every distribution-surface count in lockstep.
- Full contract-test coverage; green full suite; clean isolated review gate.

**Non-Goals:**

- No new Python runtime module (Decision 1); no CLI `codexspec onboard` subcommand.
- No `decisions`/`pitfalls` extraction, no map document, no `--yes`/`--only` flags (OUT-001/003/005/006).
- No change to `distill`'s store/format beyond a one-line cross-note (Decision 2).

## Tech Stack

- **Language**: Python 3.11 (installer registration + tests only)
- **Delivery**: Markdown command template under `templates/commands/` (agent-interpreted)
- **Test**: pytest (template contract tests + installer/CLI count tests)
- **Lint**: ruff (line-length 120)

## Plan-Level Decisions

### Decision 1: Template + installer registration only; no new src module

**Context**: Design Decision 1 fixes onboard as a pure command template.

**Options Considered**:

1. Template + one `installer.py` entry (+ lockstep sites).
2. Add a Python scanner module under `src/codexspec/`.

**Decision**: Option 1. Author the template; register it; update the lockstep sites, tests, READMEs,
CLAUDE.md, and regenerate derived artifacts. No new `src/codexspec/` module.

**Rationale**: The scan/extraction/gate is agent work; a Python scanner cannot do the semantic
inference and would duplicate the agent. Mirrors the `distill`/`debug` delivery model.

**Covers**: REQ-001, REQ-013, REQ-016; Design: C1, C4, Decision 1

### Decision 2: Follow the distribution-surface lockstep checklist to avoid count drift

**Context**: Adding a distributed command requires updating several count sites together, or a test
drifts ([[Con-2026-0811-1418yq-1]]).

**Options Considered**:

1. Update every count site in one lockstep change, verified by full suite.
2. Update piecemeal.

**Decision**: Option 1. Update in lockstep: installer entry; docstring total + per-category
(`enhanced (7)→(8)`, `Total: 24→25`); inline `# Enhanced Commands (7)`→`(8)` (note the wording is
`# Enhanced Commands (N)`, not `# Enhanced`); `tests/commands/test_installer.py` (total + per-category

- new registration/placement tests); `tests/test_cli.py` list-commands `"24"`→`"25"`; a row in all 8
`README*.md`. A brand-new command needs **no** translation-catalog entry (the catalog is a subset).

**Rationale**: The known drift trap; the `test_cli.py` count in particular only fails under the full
suite. Keeps the release safe.

**Covers**: REQ-016, NFR-001; Design: C4

### Decision 3: Regenerate derived install artifacts mid-feature

**Context**: The derived `.claude/commands/codexspec/onboard.md` and
`.agents/skills/codexspec-onboard/SKILL.md` are produced from the template by `init`
([[P-2026-0812-2114vj-1]], [[Con-2026-0813-1143el-1]]).

**Options Considered**:

1. Run `uv run codexspec init . --force --ai both` during the feature.
2. Defer derived sync to release.

**Decision**: Option 1. Regenerate during the feature (self-bootstrap sync, not a hand-edit). `init`
preserves `config.yml` keys and leaves in-sync derived files untouched.

**Rationale**: Keeps the derived forms present and consistent; onboard is not a chain command so the
auto_next sync test does not apply, but any test reading derived forms stays green.

**Covers**: REQ-016; Design: C4

### Decision 4: Test strategy — template contract tests + installer/CLI count tests

**Context**: Precedent `tests/test_debug_template.py` / `tests/test_release_notes_template.py` assert
a template's discipline by structure/string checks.

**Options Considered**:

1. A `tests/test_onboard_template.py` contract suite + installer/CLI count updates.
2. Rely only on installer count tests.

**Decision**: Option 1. Contract tests assert: interaction+document Language Preference (not commit);
scan model (high-signal/whole-repo/streaming/`[path]`); extraction scope (conventions + narrow
constraints; no decisions/pitfalls; no-signal→no-constraint); tiered gate (conventions immediate
candidate; constraints inline pre-persist gate worded as persist/don't-persist, not "vet"); reuse of
distill store/format with the inferred→candidate + code-sourced evidence.facts deltas; no-clobber;
standalone (no auto-next/hook); read-only-code/write-only-profile.

**Rationale**: Locks the confirmed behavior against future template edits.

**Covers**: REQ-001..016, NFR-001..003; Design: all components

## Risks / Trade-offs

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| zh-CN installer description trips ruff E501 | Medium | Low | Keep the description short (≤ ~80 CJK chars) ([[Con-2026-0811-1418yq-1]]) |
| A count site missed → suite drift | Medium | Medium | Decision 2 lockstep checklist; run full suite before done |
| Derived-form test fails if not regenerated | Low | Medium | Decision 3 regenerate mid-feature |
| Isolated review gate not reached → auto_distill won't fire | Medium | Low | Spawn an isolated review subagent for the §7.6 gate ([[P-2026-0811-1418yq-1]]) |

## Implementation Phases

### Phase 1: Command template (the discipline)

- [ ] Author `templates/commands/onboard.md`: frontmatter (`description`, `argument-hint: "[path]"`);
  `## Language Preference` referencing **both** `language.interaction` and `language.document`;
  the scan model (high-signal-first, whole-repo, `.gitignore` + no-git fallback, streaming/resumable,
  optional `[path]`); extraction rules (conventions incl. architecture/stack facts + narrow
  config-level constraints, by flexible judgment, evidence anchors, no-signal→no-constraint, never
  decisions/pitfalls); the tiered gate (conventions immediate `candidate`; constraints inline
  end-of-scan quick review, worded as **persist / don't-persist**, not "vet"); integration
  (read-existing, dedup, conflict-adjudicate, never clobber vetted/human/distill); terminal summary
  (deep-read vs sampled); boundaries (read-only code, write-only profile, standalone — no auto-next,
  no auto-hook, no Automatic Distillation section). — **Covers**: REQ-001,002,003,004,005,006,007,
  008,009,010,013,014, NFR-002,003; Design: C1,C2,C3,C5, Decisions 3,4,5,6
- [ ] Encode the record-format delta by **reference** to `distill.md` (reuse store/format; onboard
  deltas: `derivation` always `inferred` → `status` always `candidate`; `evidence.facts` = code
  observation; `provenance` = onboard scan). — **Covers**: REQ-011,012; Design: C2, Decision 2
- [ ] Encode the prerequisite + scaffold-ensure step: stop→`codexspec init` when `.codexspec/` absent;
  otherwise ensure the **canonical 4-directory** profile scaffold (matching `init`'s
  `ensure_profile_scaffold`) before writing. — **Covers**: REQ-015; Design: C6 (+ review-design DO #2)
- [ ] Add a one-line cross-note to `templates/commands/distill.md` acknowledging the onboard
  code-sourced `evidence.facts` variant, so the canonical format doc stays single-sourced without
  appearing to conflict. — **Covers**: REQ-011,012; Design: Decision 2 (+ review-design DO #1)

### Phase 2: Distribution registration (lockstep)

- [ ] `src/codexspec/commands/installer.py`: add the `onboard` `CommandMetadata` entry under
  `enhanced`, adjacent to `distill`/`evolve`, with a short zh-CN description (guard ruff E501). —
  **Covers**: REQ-016; Design: C4
- [ ] `installer.py`: docstring `enhanced (7)→(8)` and `Total: 24→25`; inline `# Enhanced Commands (7)`
  → `(8)`. — **Covers**: REQ-016; Design: C4
- [ ] Add an `onboard` row to all 8 `README*.md` files (translated per language). — **Covers**:
  REQ-016, NFR-001; Design: C4

### Phase 3: Tests

- [ ] `tests/test_onboard_template.py`: contract tests per Plan Decision 4 (scan model; extraction
  scope + no-decisions/pitfalls + no-signal→no-constraint; tiered gate wording; record-format deltas;
  no-clobber; standalone/no-auto-next; read-only/write-only; interaction+document Language
  Preference). — **Covers**: REQ-001..015, NFR-002,003; Design: C1,C2,C3,C5,C6
- [ ] `tests/commands/test_installer.py`: bump total `24→25` and `enhanced 7→8`; add
  `test_onboard_registered` and a placement test (onboard in `enhanced`, adjacent to distill/evolve).
  — **Covers**: REQ-016; Design: C4
- [ ] `tests/test_cli.py`: bump list-commands count `"24"`→`"25"`. — **Covers**: REQ-016
- [ ] Verify `tests/test_sdd_workflow_templates.py::test_command_templates_split_interaction_and_document_language`
  passes (onboard references interaction+document; **not** added to `commit_templates`). — **Covers**:
  NFR-001; Design: C5, Decision 6

### Phase 4: Derived sync, docs, verification

- [ ] Run `uv run codexspec init . --force --ai both` to regenerate
  `.claude/commands/codexspec/onboard.md` and `.agents/skills/codexspec-onboard/SKILL.md`. —
  **Covers**: REQ-016; Design: C4, Plan Decision 3
- [ ] Update `CLAUDE.md`: add onboard to the command tables + implementation-status table, and a brief
  architecture subsection (onboard = distill cold-start; enhanced family). — Documentation support
- [ ] Verification: `uv run ruff check src/` clean; `uv run pytest` full suite green; reach a clean
  isolated review gate. — Verification support

## Requirements Coverage

| Spec Requirement | Design Component | Plan Coverage |
|------------------|------------------|---------------|
| REQ-001 | C1; Decision 1 | Phase 1; PLD-1 |
| REQ-002 | C1 | Phase 1; Phase 3 (contract) |
| REQ-003 | C1; Decision 4 | Phase 1; Phase 3 |
| REQ-004 | C2; Decision 3 | Phase 1; Phase 3 |
| REQ-005 | C3; Decision 3 | Phase 1; Phase 3 |
| REQ-006 | C1; Decision 5 | Phase 1; Phase 3 |
| REQ-007 | C1; Decision 5 | Phase 1; Phase 3 |
| REQ-008 | C2 | Phase 1; Phase 3 |
| REQ-009 | C1; Decision 4 | Phase 1; Phase 3 |
| REQ-010 | C2; Decision 2 | Phase 1; Phase 3 |
| REQ-011 | C2; Decision 2 | Phase 1 (distill cross-note); Phase 3 |
| REQ-012 | C2; Decision 2 | Phase 1; Phase 3 |
| REQ-013 | C1; Decision 1 | Phase 1; Phase 3 |
| REQ-014 | C1 | Phase 1; Phase 3 |
| REQ-015 | C6 | Phase 1; Phase 3 |
| REQ-016 | C4; Decision 1 | Phase 2; Phase 3; Phase 4; PLD-2,3 |
| NFR-001 | C5; Decision 6 | Phase 1; Phase 2; Phase 3 |
| NFR-002 | C1; Decision 5 | Phase 1; Phase 3 |
| NFR-003 | C3; Decision 3 | Phase 1; Phase 3 |
