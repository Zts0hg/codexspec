# Feature Specification: release-notes

<!--
Language: Generated in the document language from .codexspec/config.yml (document: en).
-->

**Feature Branch**: `2026-0813-1143el-release-notes`
**Created**: 2026-08-13
**Status**: Draft
**Input**: Confirmed `requirements.md` (Feature ID `2026-0813-1143el`)

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Cut release notes for a tagged release (Priority: P1)

A developer in an arbitrary project, at release time, runs `/codexspec:release-notes`. The command
determines the range since the last release, reads the commits and diff, updates `CHANGELOG.md`
with a new section (categorized Keep a Changelog style), and prints a user-facing Release body they
can paste into their release page — without touching git state or deciding the version.

**Why this priority**: This is the core deliverable and the reason the command exists; it is the
smallest slice that delivers value and is independently usable.

**Independent Test**: In a repo that has at least one tag and an existing `CHANGELOG.md`, run the
command with no arguments; verify a new categorized section is inserted above prior entries, prior
entries are untouched, a user-facing Release body is printed, and no commit or staging change
occurs.

**Acceptance Scenarios**:

1. **Given** a repo with a latest tag `vX` and commits after it, **When** the command runs with no
   arguments, **Then** the changelog range is `vX..HEAD`, a new `## [Unreleased]` section (dated only
   when `--version` is supplied) is inserted, and every commit in range maps to at least one bullet.
2. **Given** an existing `CHANGELOG.md` with prior versioned entries, **When** the command inserts
   the new section, **Then** it is added via a precise edit above existing entries and no existing
   entry is rewritten, reordered, or deleted.
3. **Given** the changes include both user-visible (`feat`/`fix`/`perf`) and internal
   (`chore`/`refactor`/`test`/`ci`/`build`) commits, **When** the outputs are produced, **Then** the
   user-facing Release body leads with user-visible changes and internal changes appear only under a
   `### For contributors` subsection.

---

### User Story 2 - First changelog: no tags and/or no CHANGELOG (Priority: P2)

A developer on an early-stage project with no tags and no `CHANGELOG.md` runs the command to produce
its first changelog and release body.

**Why this priority**: Adoption path for the large set of user projects that do not yet tag releases
or keep a changelog; the command must not error where release tooling normally would.

**Independent Test**: In a repo with no tags and no `CHANGELOG.md`, run the command; verify a new
`CHANGELOG.md` is created with the standard header, the range falls back to full history, and a
Release body is printed.

**Acceptance Scenarios**:

1. **Given** a repo with no reachable tag and an existing `CHANGELOG.md`, **When** the command runs,
   **Then** the range falls back to "after the last version recorded in `CHANGELOG.md`".
2. **Given** a repo with no reachable tag and no `CHANGELOG.md`, **When** the command runs, **Then**
   a `CHANGELOG.md` is created with the standard Keep a Changelog header and the range is the full
   history.
3. **Given** a non-semver / non-conventional-commit project, **When** the command runs, **Then** it
   still produces a categorized changelog by inferring from the diff and commit subjects, and emits
   no version suggestion.

---

### User Story 3 - Explicit version and range control (Priority: P2)

A developer who knows their version or the exact range passes `--version` and/or `--from`/`--to`.

**Why this priority**: Gives precise control and bypasses inference for users whose release process
the command cannot infer.

**Independent Test**: Run with `--version 1.4.0 --from v1.3.0 --to HEAD`; verify the section is
stamped `## [1.4.0] - <date>`, only commits in `v1.3.0..HEAD` are summarized, and no version
suggestion is printed.

**Acceptance Scenarios**:

1. **Given** `--version X.Y.Z`, **When** the command runs, **Then** the new section is stamped with
   that version and an ISO date, and all version inference/suggestion is skipped.
2. **Given** `--from <ref>` and/or `--to <ref>`, **When** the command runs, **Then** that range
   overrides the default resolution.
3. **Given** no `--version` on a project detected to use semver and conventional commits, **When**
   the command runs, **Then** a console-only suggested next version with its reasoning and an
   "override with `--version`" note is printed, while the file section stays `Unreleased`.

---

### User Story 4 - SDD-enriched notes via `--spec` (Priority: P3)

A codexspec SDD user passes `--spec <feature>` so the notes explain the "why" using the feature's
`tasks.md` / `spec.md`.

**Why this priority**: Nice-to-have enrichment that connects release notes to the SDD trail; opt-in
and non-essential to the core deliverable.

**Independent Test**: Run with `--spec <existing-feature-dir>`; verify the Release body incorporates
"why" context from that feature's spec/tasks, and that omitting `--spec` produces notes from git
alone.

**Acceptance Scenarios**:

1. **Given** `--spec <feature>` pointing at an existing feature, **When** the command runs, **Then**
   the Release body is enriched with intent/why from that feature's `spec.md`/`tasks.md`.
2. **Given** `--spec <path>` that does not resolve, **When** the command runs, **Then** it degrades
   gracefully (proceeds from git alone, reports the unresolved path) rather than failing.

---

### Edge Cases

- **Not a git repository**: report a clear message and take no action (mirrors `pr.md`).
- **Empty range** (no commits since the last release boundary): inform "no changes to release";
  do not fabricate entries and do not error.
- **Detached HEAD**: inform and stop rather than guessing a branch (mirrors `pr.md`).
- **Existing `## [Unreleased]` section**: augment/merge into it; never duplicate it and never
  clobber its existing bullets.
- **CHANGELOG last entry is `Unreleased` only (no commit anchor)**: the range resolution cannot map
  it to a commit, so fall back to the tag boundary or full history instead of crashing.
- **Malformed `--version`**: reject with a clear validation message; do not write a malformed
  section.
- **Merge commits**: excluded by default (`--no-merges`).

## Requirements *(mandatory)*

### Functional Requirements

- **REQ-001**: The system MUST provide a distributed slash command named `/codexspec:release-notes`,
  installed into user projects by `codexspec init`, that summarizes "what changed since the last
  release" from git; it is a standalone, immediate-use git-family command and is not an SDD
  pipeline stage.
  - Sources: NEED-001, DEC-001, DEC-003
- **REQ-002**: The command MUST produce two layered outputs: (a) a developer CHANGELOG entry
  organized into Keep a Changelog categories (`Added`/`Changed`/`Deprecated`/`Removed`/`Fixed`/
  `Security`); (b) a derived user-facing Release body written benefit-first. Internal / contributor
  changes MUST appear only under a `### For contributors` subsection, classified as user-facing =
  `feat`/`fix`/`perf` (and any user-visible change) vs contributors = `chore`/`refactor`/`test`/
  `ci`/`build`/internal-only docs (inferred from the diff when commit types are absent).
  - Sources: NEED-002, DEC-007
- **REQ-003**: The command MUST maintain `CHANGELOG.md`: create it with the standard Keep a
  Changelog header when absent; insert a new version/`Unreleased` section; and MUST NEVER rewrite,
  reorder, or delete existing entries — insertion is a precise edit, never a whole-file overwrite.
  - Sources: NEED-003, CON-004
- **REQ-004**: The command MUST emit the user-facing Release body as plain markdown to the terminal
  by default, or to a file via `--output <file>`. The body MUST be platform-agnostic; the command
  MUST NOT itself publish it.
  - Sources: NEED-004, DEC-008, OUT-001
- **REQ-005**: The command MUST default its input to the commits and diff over the resolved range,
  and MUST support an opt-in `--spec <feature>` that enriches the "why" from that feature's
  `tasks.md` / `spec.md`.
  - Sources: NEED-005
- **REQ-006**: The command MUST handle versioning as follows: default the changelog section to
  `## [Unreleased]`; when `--version X.Y.Z` is given, stamp that version with an ISO date and skip
  all inference/suggestion; when `--version` is absent, apply a guarded advisory — print a
  console-only suggested next version (with reasoning and an "override with `--version`" note) ONLY
  when the project is detected to use semver AND conventional commits, otherwise stay silent. The
  command MUST NEVER write a version number into the file on its own.
  - Sources: NEED-006, DEC-002, DEC-005
- **REQ-007**: The command MUST resolve the default range as `latest tag..HEAD`, falling back to
  "after the last version recorded in `CHANGELOG.md`", then to full history; `--from <ref>` /
  `--to <ref>` MUST override; merge commits MUST be excluded (`--no-merges`); empty ranges and
  detached HEAD MUST be handled gracefully.
  - Sources: NEED-007, DEC-004
- **REQ-008**: The command MUST cross-check that every commit in the selected range maps to at least
  one changelog bullet. Conventional commits MUST be used when present but MUST NOT be required —
  when absent, categories and wording are inferred from the diff and commit subjects.
  - Sources: NEED-008
- **REQ-009**: The command template MUST follow house conventions: written in English with a
  `## Language Preference` section and a `## Constitution Compliance` section; generated content
  language follows `language.commit` → `language.output` → English; generated content MUST NEVER
  contain AI attribution.
  - Sources: CON-002, CON-003
- **REQ-010**: The command MUST have generator semantics: it MUST NEVER modify the git staging area
  and MUST NEVER create a commit; its only file mutation is the safe `CHANGELOG.md` insertion of
  REQ-003.
  - Sources: CON-004, OUT-002

### Non-Functional Requirements

- **NFR-001**: Authoring MUST follow self-bootstrap: edit `templates/commands/release-notes.md`
  only; derived `.claude/commands/` and `.agents/skills/` forms regenerate via publish → init.
  Registration MUST update in lockstep the `installer.py` metadata entry, its docstring total, the
  inline category-count comment, the command-count assertions in both
  `tests/commands/test_installer.py` and `tests/test_cli.py`, and a row in all 8 `README*.md` files.
  - Sources: CON-001
- **NFR-002**: The new command MUST require no entry in `templates/translations/*.json`; it installs
  with English frontmatter, matching the `debug`/`distill`/`evolve`/`config` precedent.
  - Sources: CON-006
- **NFR-003**: Every behavior MUST be release-process-agnostic: it MUST degrade gracefully when
  there is no `publish.sh`, no CI, no known hosting platform, and no known versioning scheme
  (semver / CalVer / date tags all possible).
  - Sources: CON-005

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of commits in the selected range are represented by at least one changelog
  bullet (completeness cross-check passes).
- **SC-002**: Across runs, zero pre-existing `CHANGELOG.md` entries are rewritten, reordered, or
  deleted (no-clobber invariant).
- **SC-003**: On a repo with no tags and no `CHANGELOG.md`, the command produces a valid changelog
  and Release body with zero errors (first-run path works).
- **SC-004**: On a non-semver / non-conventional-commit project, the command produces a changelog
  and emits zero version suggestions (no misleading advisory).
- **SC-005**: Across runs, zero git staging changes and zero commits are created by the command.

## Out of Scope

- **OUT-001**: Deciding or owning version bumps, auto-writing a version into any file, and tagging /
  publishing / creating a GitHub or GitLab release via `gh` or an API — versioning and publishing
  belong to the user's own release mechanism.
- **OUT-002**: Any git staging mutation or commit creation.
- **OUT-003**: Monorepo / path-scoping of the changelog to a subdirectory or package.
- **OUT-004**: Acting as an SDD pipeline stage or reading `requirements.md` as an authority
  (`--spec` is enrichment only).
- **No Automatic Distillation hook** (DEC-006): the command is a generator, not a
  knowledge-producing interaction, so it carries no `## Automatic Distillation` section.

## Assumptions

- The command runs inside a git repository with git available; otherwise it reports and stops.
- The user pastes the emitted Release body into their release platform manually.
- Conventional-commit / semver detection is heuristic (e.g. presence of `type:` prefixes across the
  range and semver-shaped existing tags/versions); when the signal is weak the command stays silent
  on version suggestions rather than guessing.

## Dependencies

- House style and safety discipline of the existing git-family commands (`commit-staged`, `pr`).
- codexspec build/distribution surfaces for registering a new command (`installer.py`, the two
  test-count sites, the 8 `README*.md` files) — see NFR-001.

## Requirements Traceability

| Confirmed Requirement | Spec Coverage | Notes |
|-----------------------|---------------|-------|
| NEED-001 | REQ-001 | Full |
| NEED-002 | REQ-002 | Full |
| NEED-003 | REQ-003 | Full |
| NEED-004 | REQ-004 | Full |
| NEED-005 | REQ-005 | Full |
| NEED-006 | REQ-006 | Full |
| NEED-007 | REQ-007 | Full |
| NEED-008 | REQ-008 | Full |
| CON-001 | NFR-001 | Distribution lockstep |
| CON-002 | REQ-009 | House conventions |
| CON-003 | REQ-009 | No AI attribution |
| CON-004 | REQ-003, REQ-010 | Never clobber / never mutate git |
| CON-005 | NFR-003 | Release-process-agnostic |
| CON-006 | NFR-002 | No translation-catalog entry |
| DEC-001 | REQ-001 | Command name `release-notes` |
| DEC-002 | REQ-006 | Guarded advisory |
| DEC-003 | REQ-001, OUT-004 | Standalone, not pipeline |
| DEC-004 | REQ-007 | tag-first fallback chain |
| DEC-005 | REQ-006 | `--version` short-circuits inference |
| DEC-006 | Out of Scope | No auto-distill hook |
| DEC-007 | REQ-002 | Contributor split heuristic |
| DEC-008 | REQ-004 | Single generic Release body |
| OUT-001 | Out of Scope OUT-001 | Preserved |
| OUT-002 | Out of Scope OUT-002, REQ-010 | Preserved |
| OUT-003 | Out of Scope OUT-003 | Preserved |
| OUT-004 | Out of Scope OUT-004 | Preserved |
