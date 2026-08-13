# Tasks: release-notes

<!--
Language: document language en (.codexspec/config.yml).
Expands plan.md into executable tasks. Each task: Covers: REQ-xxx; Plan: <phase/component>.
Testable tasks enumerate individually-identifiable Test Scenarios (S-ids) implemented by the
contract-test tasks. Behavior is a prose command template, so "tests" are contract tests asserting
the template's required sections/rules (mirrors tests/test_debug_template.py and
tests/test_spec_to_design_templates.py).
-->

**Feature**: `2026-0813-1143el-release-notes`
**Inputs**: requirements.md, spec.md, design.md, plan.md

## Phase 1 — Command template (`templates/commands/release-notes.md`, design C1–C6)

### T1.1 — Template scaffold + frontmatter + house sections

- **Outcome**: Create `templates/commands/release-notes.md` with frontmatter (`description` in
  English; `allowed-tools` = read-only git Bash + `Read`/`Edit`/`Write`), `## Constitution
  Compliance`, `## Language Preference`, `## Parameters`, `## Output Modes`, `## Edge Cases`, and the
  no-AI-attribution rule.
- **Covers**: REQ-001, REQ-004, REQ-005, REQ-009, NFR-003; Plan: Phase 1 (Decision 1, 2)
- **Depends on**: none
- **Test Scenarios** (implemented in T3.3):
  - **S1.1**: frontmatter has a `description` and `allowed-tools` that include read-only git plus
    `Read`, `Edit`, `Write`.
  - **S1.2**: contains `## Language Preference` and `## Constitution Compliance` sections.
  - **S1.3**: `## Parameters` documents `--version`, `--from`, `--to`, `--output`, `--spec`.
  - **S1.4**: explicitly forbids AI attribution in generated content.
  - **S1.5**: `## Edge Cases` covers not-a-git-repo, empty range, and detached HEAD.
  - **S1.6**: an unresolved `--spec <path>` degrades gracefully — proceeds from git alone and
    reports the unresolved path (does not fail).

### T1.2 — Range Resolution section

- **Outcome**: Author `## Range Resolution` implementing the tag-first fallback chain and overrides.
- **Covers**: REQ-007; Plan: Phase 1 (design C2, Decision 3)
- **Depends on**: T1.1
- **Test Scenarios** (implemented in T3.3):
  - **S2.1**: default range is `latest tag..HEAD`.
  - **S2.2**: with no reachable tag, falls back to "after the last version recorded in CHANGELOG.md".
  - **S2.3**: with no tag and no CHANGELOG.md, uses full history.
  - **S2.4**: `--from`/`--to` override the resolved range.
  - **S2.5**: merge commits are excluded (`--no-merges`).

### T1.3 — Change Categorization + Completeness + contributor split

- **Outcome**: Author `## Change Categorization` and `## Completeness Cross-Check`.
- **Covers**: REQ-002, REQ-008; Plan: Phase 1 (design C3)
- **Depends on**: T1.1
- **Test Scenarios** (implemented in T3.3):
  - **S3.1**: uses Keep a Changelog categories (Added, Changed, Deprecated, Removed, Fixed, Security).
  - **S3.2**: splits user-facing (`feat`/`fix`/`perf` + user-visible) vs a `### For contributors`
    subsection (`chore`/`refactor`/`test`/`ci`/`build`/internal docs).
  - **S3.3**: requires every non-merge commit in range to map to at least one bullet.
  - **S3.4**: when conventional commits are absent, infers categories from the diff and commit
    subjects (does not hard-require conventional commits).

### T1.4 — Version Handling section

- **Outcome**: Author `## Version Handling` (Unreleased default, `--version` short-circuit, guarded
  advisory).
- **Covers**: REQ-006; Plan: Phase 1 (design C4, Decision 4)
- **Depends on**: T1.1
- **Test Scenarios** (implemented in T3.3):
  - **S4.1**: default section is `## [Unreleased]` with no date.
  - **S4.2**: `--version X.Y.Z` stamps `## [X.Y.Z] - <ISO date>` and skips all inference/suggestion.
  - **S4.3**: prints a console-only suggested next version ONLY when semver AND conventional commits
    are detected.
  - **S4.4**: stays silent on version suggestions when that detection fails.
  - **S4.5**: never writes a version number into the file on its own (only `Unreleased` or
    `--version`).
  - **S4.6**: a malformed `--version` value is rejected with a clear validation message and no
    malformed section is written.

### T1.5 — CHANGELOG.md Maintenance + Release Body Generation

- **Outcome**: Author `## CHANGELOG.md Maintenance` and `## Release Body Generation` (never-clobber
  insertion + benefit-first body).
- **Covers**: REQ-003, REQ-010, REQ-002; Plan: Phase 1 (design C5, C6, Decision 2)
- **Depends on**: T1.1
- **Test Scenarios** (implemented in T3.3):
  - **S5.1**: creates `CHANGELOG.md` with the standard Keep a Changelog header when absent.
  - **S5.2**: inserts additively and never rewrites, reorders, or deletes existing entries.
  - **S5.3**: merges into an existing `## [Unreleased]` section rather than duplicating it.
  - **S5.4**: forbids whole-file `Write` overwrite of CHANGELOG.md (precise `Edit` insertion only).
  - **S5.5**: never modifies git staging and never creates a commit.

## Phase 2 — Installer registration (`src/codexspec/commands/installer.py`, design C7)

### T2.1 — Register command + update docstring counts

- **Outcome**: Add a `CommandMetadata` entry for `release-notes` (category `git`, zh-CN description
  matching siblings, `file_name: "release-notes.md"`) after `pr`; update the `get_commands_metadata`
  docstring `Total: 23 → 24` and `git (2) → git (3)`; and update the inline count comment
  `# Git Workflow Commands (2) → (3)`. (Correction: the `git` category **does** carry an inline count
  comment — its wording is `# Git Workflow Commands (N)`, so review-plan M-1's "no inline comment"
  premise was wrong; verified repo facts prevail.)
- **Covers**: NFR-001, REQ-001; Plan: Phase 2 (design C7, Decision 5)
- **Depends on**: T1.1
- **Test Scenarios** (implemented in T3.2):
  - **S6.1**: `get_commands_metadata()` includes `release-notes` with category `git` and
    `file_name` `release-notes.md`.
  - **S6.2**: `len([c for c in result if c["category"] == "git"]) == 3`.
  - **S6.3**: `len(result) == 24`.
  - **S6.4**: `release-notes` appears immediately after `pr` within the `git` group.

## Phase 3 — Distribution surfaces + derived regeneration (design C8)

### T3.1 — Add command row to all 8 READMEs

- **Outcome**: Add a `release-notes` row to the command list/table in `README.md`, `README.de.md`,
  `README.es.md`, `README.fr.md`, `README.ja.md`, `README.ko.md`, `README.pt-BR.md`,
  `README.zh-CN.md` (translated per language).
- **Covers**: NFR-001; Plan: Phase 3 (design C8)
- **Depends on**: T1.1
- **Verification** (non-testable/docs): each README contains a `release-notes` command row;
  `grep -l release-notes README*.md` returns all 8.

### T3.2 — Bump command-count assertions + add registration test

- **Outcome**: Update `tests/commands/test_installer.py` (`== 23 → 24`, `git == 2 → 3`, add a
  `release-notes` registration/placement assertion) and `tests/test_cli.py` (`"23" → "24"` at the
  list-commands count assertion).
- **Covers**: NFR-001; Plan: Phase 3 (implements S6.1–S6.4)
- **Depends on**: T2.1
- **Test Scenarios**: implements S6.1–S6.4 (see T2.1).

### T3.3 — Add template contract tests

- **Outcome**: Add `tests/test_release_notes_template.py` asserting S1.1–S5.5 against
  `templates/commands/release-notes.md`, plus a `test_no_translation_catalog_entry` asserting
  `release-notes` is absent from `templates/translations/en.json`.
- **Covers**: REQ-002, REQ-003, REQ-006, REQ-007, REQ-008, NFR-002; Plan: Phase 3 (Decision 4)
- **Depends on**: T1.1, T1.2, T1.3, T1.4, T1.5
- **Test Scenarios**: implements S1.1–S1.6, S2.1–S2.5, S3.1–S3.4, S4.1–S4.6, S5.1–S5.5; plus
  - **S7.1**: `release-notes` has no key in `templates/translations/en.json` (installs with English
    frontmatter).

### T3.4 — Regenerate derived install artifacts

- **Outcome**: Run `uv run codexspec init . --force --ai both`; confirm
  `.claude/commands/codexspec/release-notes.md` and `.agents/skills/codexspec-release-notes/SKILL.md`
  are created; confirm no `templates/translations/*.json` entry was added.
- **Covers**: NFR-001, NFR-002; Plan: Phase 3 (design C8, Decision 3)
- **Depends on**: T1.1, T1.2, T1.3, T1.4, T1.5, T2.1
- **Verification** (non-testable/build): both derived paths exist; `git status` shows the derived
  files; `grep -L release-notes templates/translations/en.json` confirms absence.

## Phase 4 — Verification

### T4.1 — Full suite + lint green

- **Outcome**: `uv run ruff check src/ tests/` clean and `uv run pytest` green.
- **Covers**: NFR-001, NFR-002; Plan: Phase 4
- **Depends on**: T3.1, T3.2, T3.3, T3.4
- **Verification** (non-testable/gate): ruff exits 0; pytest exits 0 with the new count/registration/
  template contract tests passing.

## Coverage Table

| Requirement / Plan item | Design | Task(s) |
|-------------------------|--------|---------|
| REQ-001 | C1, C7 | T1.1, T2.1 |
| REQ-002 | C3, C6 | T1.3, T1.5 |
| REQ-003 | C5 | T1.5 |
| REQ-004 | C6 | T1.1, T1.5 |
| REQ-005 | C1 | T1.1 |
| REQ-006 | C4 | T1.4 |
| REQ-007 | C2 | T1.2 |
| REQ-008 | C3 | T1.3 |
| REQ-009 | Cross-Cutting | T1.1 |
| REQ-010 | C5 | T1.5 |
| NFR-001 | C7, C8 | T2.1, T3.1, T3.2, T3.4, T4.1 |
| NFR-002 | C8 | T3.3, T3.4 |
| NFR-003 | C1, C2, C4 | T1.1, T1.2, T1.4 |

## Scenario → Task / Test Mapping

| Scenario | Behavior task | Implemented in |
|----------|---------------|----------------|
| S1.1–S1.6 | T1.1 | T3.3 (`tests/test_release_notes_template.py`) |
| S2.1–S2.5 | T1.2 | T3.3 |
| S3.1–S3.4 | T1.3 | T3.3 |
| S4.1–S4.6 | T1.4 | T3.3 |
| S5.1–S5.5 | T1.5 | T3.3 |
| S6.1–S6.4 | T2.1 | T3.2 (`tests/commands/test_installer.py`, `tests/test_cli.py`) |
| S7.1 | T3.3 | T3.3 |

## Dependency Summary

- T1.1 → (T1.2, T1.3, T1.4, T1.5, T2.1, T3.1)
- T2.1 → T3.2
- (T1.2, T1.3, T1.4, T1.5) → T3.3
- (T1.*, T2.1) → T3.4
- (T3.1, T3.2, T3.3, T3.4) → T4.1
- Acyclic; behavior tasks precede their contract-test and verification tasks.

## Implementation Status (2026-08-13)

All tasks implemented and verified against a green baseline (`ruff` clean; `uv run pytest` →
1146 passed, 50 skipped).

- [x] T1.1–T1.5 — `templates/commands/release-notes.md` authored (all sections, all rules).
- [x] T2.1 — installer entry (category `git`) + docstring `Total 23→24`, `git (2)→(3)` + inline
  `# Git Workflow Commands (2)→(3)`.
- [x] T3.1 — `release-notes` row added to all 8 `README*.md`.
- [x] T3.2 — count assertions bumped in `test_installer.py` (`24`, `git 3`) + `test_cli.py` (`"24"`)
  - registration/placement tests.
- [x] T3.3 — `tests/test_release_notes_template.py` (27 scenarios S1.1–S5.5, S7.1) all green.
- [x] T3.4 — derived `.claude/commands/codexspec/release-notes.md` + `.agents/skills/`
  regenerated via `codexspec init --force --ai both`; no translation-catalog entry.
- [x] T4.1 — ruff clean + full suite green.

Note: `test_sdd_workflow_templates.py::commit_templates` extended to include `release-notes`
(git-family, language.commit priority per pr.md / REQ-009).
