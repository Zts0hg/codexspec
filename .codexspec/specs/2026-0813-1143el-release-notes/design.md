# Design Document: release-notes

<!--
Language: document language en (.codexspec/config.yml).
Design stage between spec.md and plan.md — WHAT the system is, not build phases.
-->

**Related Spec**: `.codexspec/specs/2026-0813-1143el-release-notes/spec.md`
**Confirmed Requirements**: `.codexspec/specs/2026-0813-1143el-release-notes/requirements.md`
**Created**: 2026-08-13
**Status**: Draft

## Context

The feature adds a new distributed, immediate-use git-family slash command `/codexspec:release-notes`
to codexspec. Like its siblings `commit-staged` and `pr`, its behavior is realized **entirely as an
LLM-executed markdown command template** (no Python runtime logic); the only Python touched is the
installer registration so `codexspec init` ships it. The command reads git history over a resolved
range and produces two outputs — a `CHANGELOG.md` entry (Keep a Changelog) and a user-facing Release
body — while owning no versioning and mutating no git state. This design describes the template's
internal component shape, the registration/distribution surface, and the material design decisions.

## Architecture & Components

### C1. `templates/commands/release-notes.md` — the command definition

- **Responsibility**: The whole runtime behavior, expressed as ordered template sections the agent
  executes: frontmatter; `## Constitution Compliance`; `## Language Preference`; `## Parameters`;
  `## Range Resolution`; `## Git Context Collection`; `## Change Categorization`;
  `## Version Handling`; `## CHANGELOG.md Maintenance`; `## Release Body Generation`;
  `## Completeness Cross-Check`; `## Output Modes`; `## Edge Cases`.
- **Interface**: Input `$ARGUMENTS` (see API / Interface Contracts); outputs a modified
  `CHANGELOG.md` and a printed/`--output` Release body.
- **Covers**: REQ-001, REQ-002, REQ-003, REQ-004, REQ-005, REQ-006, REQ-007, REQ-008, REQ-009,
  REQ-010, NFR-003

### C2. `## Range Resolution` section (within C1)

- **Responsibility**: Determine `<from>..<to>`: default `latest tag..HEAD`; fall back to "after the
  last version recorded in `CHANGELOG.md`", then full history; honor `--from`/`--to`; apply
  `--no-merges`; detect empty range / detached HEAD / not-a-repo and route to Edge Cases.
- **Interface**: reads `git describe --tags --abbrev=0`, `git tag`, `CHANGELOG.md`, `git rev-parse`,
  `git log --no-merges <range>`.
- **Covers**: REQ-007

### C3. `## Change Categorization` + `## Completeness Cross-Check` sections (within C1)

- **Responsibility**: Read commits + full diff over the range; group into Keep a Changelog
  categories (`Added`/`Changed`/`Deprecated`/`Removed`/`Fixed`/`Security`); split user-facing vs
  `For contributors`; verify every non-merge commit maps to ≥1 bullet. Uses conventional-commit
  types when present, else infers from diff + subjects.
- **Interface**: consumes C2's range; produces a structured category→bullets model used by C5/C6.
- **Covers**: REQ-002, REQ-008

### C4. `## Version Handling` section (within C1)

- **Responsibility**: Choose the section label: `--version X.Y.Z` → stamp `## [X.Y.Z] - <ISO date>`
  and skip inference; else default `## [Unreleased]` (no date). Guarded advisory: only when semver +
  conventional-commit signals are detected, print a console-only suggested next version + reasoning +
  "override with `--version`"; never write a version to the file.
- **Interface**: reads `--version`, the detection signals from C2/C3; emits console advisory text.
- **Covers**: REQ-006

### C5. `## CHANGELOG.md Maintenance` section (within C1)

- **Responsibility**: Create `CHANGELOG.md` with the standard Keep a Changelog header if absent;
  insert the new section via a precise, additive edit (into an existing `## [Unreleased]` if present,
  else above the latest version section, else after the header); **never** rewrite, reorder, or
  delete existing entries; never overwrite the whole file.
- **Interface**: reads full `CHANGELOG.md`, performs a targeted insertion edit.
- **Covers**: REQ-003, REQ-010 (file-mutation is limited to this safe insertion)

### C6. `## Release Body Generation` + `## Output Modes` sections (within C1)

- **Responsibility**: Derive the user-facing Release body (benefit-first, "You can now…", internal
  changes under `### For contributors`) from C3's model; print to terminal by default or write to
  `--output <file>`; body is generic platform-agnostic markdown; never publishes.
- **Covers**: REQ-004, REQ-002

### C7. `installer.py` registration

- **Responsibility**: One `CommandMetadata` entry (`name: "release-notes"`, category `"git"`,
  zh-CN description matching sibling entries, `file_name: "release-notes.md"`) placed with the other
  `git` entries; update the docstring total (`23 → 24`, `git (2) → git (3)`) and the inline
  `# Git ... (N)` comment.
- **Covers**: NFR-001, REQ-001

### C8. Distribution surfaces (docs, tests, derived artifacts)

- **Responsibility**: Add a command row to all 8 `README*.md`; bump the command-count assertions in
  both `tests/commands/test_installer.py` and `tests/test_cli.py`; add feature contract tests;
  regenerate the derived `.claude/commands/codexspec/` and `.agents/skills/` forms via
  `codexspec init` (self-bootstrap). **No** `templates/translations/*.json` entry (installs with
  English frontmatter).
- **Covers**: NFR-001, NFR-002

## Key Design Decisions

### Decision 1: Realize all behavior in the markdown template; no Python logic

- **Context**: codexspec commands are either LLM-executed templates or Python CLI. `release-notes`
  is behavioral/generative and platform-agnostic.
- **Decision**: Implement entirely as `templates/commands/release-notes.md`, executed by the agent,
  exactly like `commit-staged`/`pr`. Python only registers it.
- **Alternatives**: A Python subcommand (e.g. `codexspec release-notes`) — rejected: it would need
  to reimplement diff summarization deterministically, cannot produce natural-language notes, and
  breaks parity with the git-family commands.
- **Trade-offs**: Behavior is prose-specified (not unit-testable as code); mitigated by contract
  tests that assert the template's required sections/rules (the debug/spec-to-design test precedent).
- **Covers**: REQ-001, REQ-010

### Decision 2: Never-clobber CHANGELOG maintenance via additive insertion only

- **Context**: gstack recorded a real incident where an agent overwrote existing CHANGELOG entries.
- **Decision**: Read the whole file, locate a single insertion point, and add only new content via a
  precise edit; forbid whole-file rewrite and any reorder/delete of existing entries; when an
  `## [Unreleased]` section already exists, merge into it rather than duplicating.
- **Alternatives**: Regenerate the changelog from history each run — rejected: destroys
  hand-curated prose and violates NEED-003.
- **Trade-offs**: Requires careful insertion-point logic against varied existing formats; mitigated
  by falling back to "insert after header" when structure is unrecognized.
- **Covers**: REQ-003

### Decision 3: Range resolution order — tag → CHANGELOG last version → full history

- **Context**: The command must find "since last release" in a release-process-agnostic way
  (CON-005).
- **Decision**: Prefer the latest reachable tag; if none, use the last version anchored in
  `CHANGELOG.md`; if neither, use full history. `--from/--to` always override; `--no-merges` default.
- **Alternatives**: CHANGELOG-first — rejected (DEC-004): the version→commit mapping is fragile,
  especially when the prior top entry is `Unreleased` with no commit anchor.
- **Trade-offs**: A tag that is not a release could mis-anchor the range; mitigated by the explicit
  `--from/--to` override.
- **Covers**: REQ-007

### Decision 4: Guarded advisory gated on detected semver + conventional commits

- **Context**: A confidently-wrong bump on a non-semver project is worse than none (DEC-002).
- **Decision**: Emit the console-only version suggestion only when both signals are present
  (semver-shaped existing tags/version AND conventional-commit prefixes across the range); otherwise
  stay silent. Never write it to a file.
- **Alternatives**: Always suggest (rejected — misleads CalVer/non-conventional projects); never
  suggest (rejected — foregoes a safe, friendly signal).
- **Trade-offs**: Detection is heuristic and may stay silent on projects that do use semver
  loosely; acceptable because silence is the safe failure mode.
- **Covers**: REQ-006

### Decision 5: Register under installer category `"git"`

- **Context**: `commit-staged` and `pr` are category `"git"`; `release-notes` is their delivery-time
  sibling.
- **Decision**: Add to the `git` category (git 2→3, total 23→24), not `enhanced`.
- **Alternatives**: `enhanced` — rejected: semantically it is a git/delivery workflow command.
- **Trade-offs**: None material.
- **Covers**: NFR-001

## API / Interface Contracts

CLI surface via `$ARGUMENTS` (all optional):

| Parameter | Default | Meaning | Covers |
|-----------|---------|---------|--------|
| `--version X.Y.Z` | (none) | Stamp this version + ISO date; short-circuits all inference/suggestion | REQ-006 |
| `--from <ref>` / `--to <ref>` | resolved (see C2) | Explicit range override; `--to` defaults to HEAD | REQ-007 |
| `--output <file>` | (terminal) | Write the Release body to a file instead of stdout | REQ-004 |
| `--spec <feature>` | (none) | Enrich the "why" from that feature's `spec.md`/`tasks.md`; unresolved → degrade gracefully | REQ-005 |

Outputs:

1. **`CHANGELOG.md`** — created-if-absent; a new categorized section inserted additively (REQ-003).
2. **Release body** — generic markdown, user-facing with a `### For contributors` subsection, to
   stdout or `--output` (REQ-002, REQ-004).

Error/degrade behavior: not-a-git-repo → report & stop; empty range → "no changes to release";
detached HEAD → report & stop; malformed `--version` → validation error; unresolved `--spec` →
proceed from git alone with a note.

## Sequence & Data Flow

1. Parse `$ARGUMENTS`; validate `--version` shape if present.
2. **Range Resolution** (C2) → `<from>..<to>` (or an Edge-Case exit).
3. **Git Context Collection** → `git log --no-merges` + full diff over the range (+ optional `--spec`
   read).
4. **Change Categorization** (C3) → category→bullets model; user-facing vs contributor split.
5. **Version Handling** (C4) → section label (`Unreleased` / `--version`) + optional console advisory.
6. **CHANGELOG.md Maintenance** (C5) → additive insertion (create header if absent).
7. **Release Body Generation** (C6) → emit to stdout / `--output`.
8. **Completeness Cross-Check** (C3) → assert every non-merge commit is represented; if not, augment.

## Cross-Cutting Design

- **Safety invariants** (span C5/C6): never modify git staging, never commit, never overwrite
  `CHANGELOG.md`, never reorder/delete existing entries. (REQ-003, REQ-010)
- **i18n**: generated content language follows `language.commit` → `language.output` → English, per
  `pr.md`; the template itself is English with `## Language Preference`. (REQ-009)
- **No AI attribution** in any generated changelog/release content. (REQ-009)

## Risks & Trade-offs

| Risk | Impact | Mitigation |
|------|--------|------------|
| Unrecognized existing CHANGELOG structure | Insertion point ambiguous | Fall back to "insert after header"; never rewrite existing content (D2) |
| Heuristic semver/conventional detection false-negative | No version suggestion where one was possible | Silence is the safe mode; `--version` always available (D4) |
| Tag that is not a release mis-anchors range | Wrong range summarized | `--from/--to` override; `--no-merges` (D3) |
| Prose-specified behavior not code-testable | Regressions slip past unit tests | Contract tests assert required sections/rules (D1) |

## Requirements Coverage

| Spec Requirement | Design Coverage |
|------------------|-----------------|
| REQ-001 | C1, C7; Decision 1 |
| REQ-002 | C3, C6; API Contracts |
| REQ-003 | C5; Decision 2; Cross-Cutting |
| REQ-004 | C6; API Contracts |
| REQ-005 | C1 (`--spec`); API Contracts |
| REQ-006 | C4; Decision 4; API Contracts |
| REQ-007 | C2; Decision 3 |
| REQ-008 | C3 (Completeness Cross-Check) |
| REQ-009 | Cross-Cutting Design |
| REQ-010 | C5; Cross-Cutting (safety invariants) |
| NFR-001 | C7, C8; Decision 5 |
| NFR-002 | C8 (no translation-catalog entry) |
| NFR-003 | C1, C2, C4 (release-process-agnostic behavior) |
