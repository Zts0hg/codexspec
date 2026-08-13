# Implementation Plan: release-notes

<!--
Language: document language en (.codexspec/config.yml).
HOW to build the confirmed design in phases. Architecture/components live in design.md — referenced, not restated.
-->

**Related Spec**: `.codexspec/specs/2026-0813-1143el-release-notes/spec.md`
**Related Design**: `.codexspec/specs/2026-0813-1143el-release-notes/design.md`
**Confirmed Requirements**: `.codexspec/specs/2026-0813-1143el-release-notes/requirements.md`
**Created**: 2026-08-13
**Status**: Draft

## Context

Deliver the `/codexspec:release-notes` git-family command against `design.md`. The behavior is a
single markdown command template (design C1–C6); the rest is installer registration (C7) and the
distribution surface — 8 READMEs, two test-count sites, contract tests, and regenerated derived
artifacts (C8). No Python runtime logic implements the command behavior (Decision 1); Python changes
are limited to registration and tests.

## Goals / Non-Goals

**Goals:**

- Author `templates/commands/release-notes.md` realizing design components C1–C6.
- Register the command in `installer.py` under category `git` with lockstep count/doc updates.
- Update all distribution surfaces (READMEs, test counts, contract tests) and regenerate derived
  install artifacts, all green under the full suite + ruff.

**Non-Goals:**

- Any Python implementation of changelog/release-body generation (Decision 1; design C1).
- Versioning ownership, publishing, monorepo scoping, auto-distill hook, per-platform variants
  (spec Out of Scope).

## Tech Stack

- **Language**: Python 3.11 (installer + pytest), Markdown (command template).
- **Framework/Tooling**: Typer CLI, pytest, ruff; `codexspec init` for self-bootstrap regeneration.
- **Distribution**: `templates/commands/` → derived `.claude/commands/codexspec/` + `.agents/skills/`.

## Plan-Level Decisions

### Decision 1: Model the template on `pr.md` / `commit-staged.md` house structure

**Context**: The command must match the git-family house style and safety discipline.

**Options Considered**:

1. Author from scratch with a bespoke section layout.
2. Mirror `pr.md` (git context collection, parameters, output modes, edge cases) + `commit-staged.md`
   (Forbidden Operations / never-mutate discipline).

**Decision**: Option 2 — reuse the `pr.md` + `commit-staged.md` section patterns and safety wording.

**Rationale**: Proven house patterns; least surprise; carries the never-mutate-git discipline the
design requires.

**Covers**: REQ-001, REQ-009, REQ-010; Design: C1, Decision 1

**Decision Level**: Plan-level implementation decision; does not change confirmed product scope or the confirmed design.

### Decision 2: `allowed-tools` provision both Edit (CHANGELOG) and Write (`--output` / CHANGELOG creation) plus read-only git

**Context**: Review advisory A-1 — the command edits `CHANGELOG.md` additively AND may write a
`--output` file; new-CHANGELOG creation also needs a file write.

**Options Considered**:

1. Only Edit (would block `--output` and first-time CHANGELOG creation).
2. Edit + Write + read-only git Bash, with safety wording separating "never overwrite CHANGELOG /
   never touch git state" from "write the user's `--output` path".

**Decision**: Option 2.

**Rationale**: Matches REQ-003/REQ-004; keeps git strictly read-only while allowing the two intended
file writes.

**Covers**: REQ-003, REQ-004; Design: C5, C6, Cross-Cutting

**Decision Level**: Plan-level implementation decision; does not change confirmed product scope or the confirmed design.

### Decision 3: Regenerate derived artifacts during the feature via `codexspec init`

**Context**: Self-bootstrap — the derived `.claude/commands/codexspec/release-notes.md` and
`.agents/skills/` forms must exist so `init` installs the command; regenerating via `init` is the
legitimate sync, not a hand-edit (profile pitfall [[P-2026-0812-2114vj-1]]).

**Options Considered**:

1. Defer derived regeneration to release.
2. Regenerate during the feature with `uv run codexspec init . --force --ai both`.

**Decision**: Option 2.

**Rationale**: Keeps the tree self-consistent and lets any template-presence/derived checks pass in
the same commit; avoids a drifted snapshot.

**Covers**: NFR-001; Design: C8

**Decision Level**: Plan-level implementation decision; does not change confirmed product scope or the confirmed design.

### Decision 4: Contract tests assert the template's required sections/rules

**Context**: Behavior is prose-specified (Decision 1); it is not code-unit-testable.

**Options Considered**:

1. No dedicated tests (rely only on count assertions).
2. A `tests/test_release_notes_template.py` asserting required sections, parameters, safety rules,
   and installer registration — mirroring `tests/test_debug_template.py` and
   `tests/test_spec_to_design_templates.py`.

**Decision**: Option 2.

**Rationale**: Guards the design's key rules (never-clobber, Unreleased default, `--version`
short-circuit, guarded advisory, range fallback, `For contributors` split) against regression.

**Covers**: REQ-002, REQ-003, REQ-006, REQ-007, REQ-008, NFR-001; Design: C1–C7, D1

**Decision Level**: Plan-level implementation decision; does not change confirmed product scope or the confirmed design.

## Risks / Trade-offs

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| A count site is missed → suite drift | Medium | Medium | Follow the [[Con-2026-0811-1418yq-1]] checklist for the `git` category: installer entry + inline `# Git Workflow Commands (2)→(3)` comment + docstring (`Total` + `git` count) + `test_installer.py` (`== 23→24`, `git == 2→3`) + `test_cli.py` (`"23"→"24"`) + 8 READMEs |
| Derived artifacts not regenerated | Medium | Medium | Decision 3 — run `codexspec init --force --ai both` before final verification |
| markdownlint reformats the new `.md` on commit | Medium | Low | Author the template markdownlint-clean; re-stage if a hook reformats |
| Template prose regressions slip past unit tests | Low | Medium | Decision 4 — contract tests assert required sections/rules |

## Implementation Phases

### Phase 1: Command template (design C1–C6)

- [ ] Author `templates/commands/release-notes.md` — frontmatter (description EN; `allowed-tools`:
  read-only git Bash + Read/Edit/Write), `## Constitution Compliance`, `## Language Preference`,
  `## Parameters` (`--version`, `--from`/`--to`, `--output`, `--spec`) — **Covers**: REQ-001,
  REQ-004, REQ-005, REQ-009; Design: C1
- [ ] Author `## Range Resolution` (tag → CHANGELOG-last-version → full history; `--from/--to`;
  `--no-merges`; empty/detached/not-a-repo edge routing) — **Covers**: REQ-007; Design: C2
- [ ] Author `## Change Categorization` + `## Completeness Cross-Check` (Keep a Changelog categories;
  user-facing vs `For contributors`; every non-merge commit → ≥1 bullet; infer when no conventional
  commits) — **Covers**: REQ-002, REQ-008; Design: C3
- [ ] Author `## Version Handling` (Unreleased default; `--version` stamp + ISO date short-circuit;
  guarded advisory gated on semver + conventional detection; never write version to file) —
  **Covers**: REQ-006; Design: C4
- [ ] Author `## CHANGELOG.md Maintenance` (create-if-absent standard header; additive insertion;
  never rewrite/reorder/delete; merge into existing `Unreleased`) — **Covers**: REQ-003, REQ-010;
  Design: C5, Decision 2
- [ ] Author `## Release Body Generation` + `## Output Modes` + `## Edge Cases` (benefit-first body;
  stdout/`--output`; no AI attribution; graceful degradation) — **Covers**: REQ-002, REQ-004,
  REQ-009, NFR-003; Design: C6

### Phase 2: Installer registration (design C7)

- [ ] Add a `CommandMetadata` entry for `release-notes` (category `git`, zh-CN description matching
  siblings, `file_name: "release-notes.md"`) among the `git` entries (after `pr`); update the
  `get_commands_metadata` docstring — both the `Total: 23 → 24` line and the `git (2) → git (3)`
  count in the category-priority line — AND the inline count comment
  `# Git Workflow Commands (2) → (3)` above the git entries. (The git category DOES have an inline
  count comment; its wording is `# Git Workflow Commands (N)`, matching the
  `# Code Review Commands (N)` form for review.) — **Covers**: NFR-001, REQ-001; Design: C7,
  Decision 5

### Phase 3: Distribution surfaces + derived regeneration (design C8)

- [ ] Add a `release-notes` row to all 8 `README*.md` (translated per language) — **Covers**:
  NFR-001; Design: C8
- [ ] Bump command-count assertions in `tests/commands/test_installer.py` and `tests/test_cli.py`
  (and add a registration/placement assertion for `release-notes`) — **Covers**: NFR-001; Design: C8
- [ ] Add `tests/test_release_notes_template.py` (required sections, parameters, safety rules,
  version/range behavior, `For contributors` split, no-catalog-entry) — **Covers**: REQ-002,
  REQ-003, REQ-006, REQ-007, REQ-008, NFR-002; Design: C1–C7, Decision 4
- [ ] Regenerate derived artifacts: `uv run codexspec init . --force --ai both` (creates
  `.claude/commands/codexspec/release-notes.md` + `.agents/skills/codexspec-release-notes/`) —
  **Covers**: NFR-001; Design: C8, Decision 3
- [ ] Confirm NO `templates/translations/*.json` entry is added (new command installs EN frontmatter)
  — **Covers**: NFR-002; Design: C8

### Phase 4: Verification

- [ ] `uv run ruff check src/ tests/` clean — **Covers**: NFR-001
- [ ] `uv run pytest` full suite green (counts, registration, template contract tests) — **Covers**:
  NFR-001, NFR-002

## Requirements Coverage

| Spec Requirement | Design Component | Plan Coverage |
|------------------|------------------|---------------|
| REQ-001 | C1, C7, D1 | Phase 1, Phase 2; Decision 1 |
| REQ-002 | C3, C6 | Phase 1 (Categorization, Release Body); Decision 4 |
| REQ-003 | C5, D2 | Phase 1 (CHANGELOG Maintenance); Decision 2 |
| REQ-004 | C6 | Phase 1 (Output Modes); Decision 2 |
| REQ-005 | C1 | Phase 1 (Parameters `--spec`) |
| REQ-006 | C4, D4 | Phase 1 (Version Handling); Decision 4 |
| REQ-007 | C2, D3 | Phase 1 (Range Resolution); Decision 4 |
| REQ-008 | C3 | Phase 1 (Completeness Cross-Check); Decision 4 |
| REQ-009 | Cross-Cutting | Phase 1; Decision 1 |
| REQ-010 | C5 | Phase 1 (CHANGELOG Maintenance); Decision 2 |
| NFR-001 | C7, C8, D5 | Phase 2, Phase 3, Phase 4; Decisions 3, 4 |
| NFR-002 | C8 | Phase 3 (no catalog entry) |
| NFR-003 | C1, C2, C4 | Phase 1 |
