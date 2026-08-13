# Tasks: onboard command

<!--
Language: document language = en. Expands plan.md into executable tasks. Does not redesign.
Each task: Covers: REQ-xxx; Plan: <phase/component>. Testable tasks enumerate Test Scenarios.
-->

**Feature**: `2026-0813-1606fz-onboard`
**Related**: requirements.md · spec.md · design.md · plan.md

## Group 1 — Command template (Plan Phase 1)

### T1.1 — Author `templates/commands/onboard.md` (core discipline)

- **Outcome**: New file `templates/commands/onboard.md` with: frontmatter (`description`,
  `argument-hint: "[path]"`); `## Language Preference` referencing both `language.interaction` and
  `language.document`; the scan model (high-signal-first, whole-repo, `.gitignore` + no-git fallback,
  streaming/resumable, optional `[path]`); extraction rules (conventions incl. architecture/stack
  facts + narrow config-level constraints, by flexible judgment, evidence anchors,
  no-signal→no-constraint, never decisions/pitfalls); the tiered gate (conventions immediate
  `candidate`; constraints inline end-of-scan quick review worded as **persist / don't-persist**, not
  "vet"); integration (read-existing, dedup, conflict-adjudicate, never clobber); terminal summary
  (deep-read vs sampled); boundaries (read-only code, write-only profile, standalone — no auto-next,
  no auto-hook, no Automatic Distillation section).
- **Path**: `templates/commands/onboard.md`
- **Covers**: REQ-001,002,003,004,005,006,007,008,009,010,013,014, NFR-002,003; Plan: Phase 1 (C1,C3,C5, Decisions 3,4,5,6)
- **Dependencies**: none
- **Verification**: satisfied by T3.1 contract scenarios; the specific asserted properties are enumerated there.

### T1.2 — Encode record-format reuse + onboard deltas within `onboard.md`

- **Outcome**: onboard.md reuses distill's store/format **by reference** and states its deltas:
  `derivation` always `inferred` → `status` always `candidate` (never `vetted` at onboard);
  `evidence.facts` = concrete code observation (path + snippet/config anchor); `provenance` = onboard
  scan; records go under `.codexspec/profile/{conventions,constraints}/<id>.md` with namespaced ids.
- **Path**: `templates/commands/onboard.md`
- **Covers**: REQ-011,012; Plan: Phase 1 (C2, Decision 2)
- **Dependencies**: T1.1
- **Verification**: T3.1 (S1.10)

### T1.3 — Encode prerequisite + canonical scaffold-ensure within `onboard.md`

- **Outcome**: onboard.md stops and directs to `codexspec init` when `.codexspec/` is absent; when
  present, ensures the **canonical 4-directory** profile scaffold (matching `ensure_profile_scaffold`)
  before writing; does not require git.
- **Path**: `templates/commands/onboard.md`
- **Covers**: REQ-015; Plan: Phase 1 (C6; review-design DO #2)
- **Dependencies**: T1.1
- **Verification**: T3.1 (S1.13)

### T1.4 — Add onboard cross-note to `templates/commands/distill.md`

- **Outcome**: A one-line note in distill.md's record-format section acknowledging the onboard
  code-sourced `evidence.facts` variant, keeping the canonical format single-sourced without
  appearing to conflict. No other change to distill's store/format.
- **Path**: `templates/commands/distill.md`
- **Covers**: REQ-011,012; Plan: Phase 1 (Decision 2; review-design DO #1)
- **Dependencies**: none — `[P]` with T1.1
- **Verification**: T3.1 (S1.17)

## Group 2 — Distribution registration (Plan Phase 2)

### T2.1 — Register onboard in the installer with lockstep counts

- **Outcome**: In `src/codexspec/commands/installer.py`: add the `onboard` `CommandMetadata` entry
  under the `enhanced` category (adjacent to `distill`/`evolve`), `display_name`
  `/codexspec:onboard`, `file_name` `onboard.md`, short zh-CN `description` (guard ruff E501); bump the
  docstring `enhanced (7)→(8)` and `Total: 24→25`; update the inline `# Enhanced Commands (7)` → `(8)`.
- **Path**: `src/codexspec/commands/installer.py`
- **Covers**: REQ-016; Plan: Phase 2 (C4, Plan Decision 2)
- **Dependencies**: T1.1
- **Verification**: T3.2

### T2.2 — Add onboard row to all 8 READMEs

- **Outcome**: An `onboard` command row added to every `README*.md`
  (`README.md`, `.de`, `.es`, `.fr`, `.ja`, `.ko`, `.pt-BR`, `.zh-CN`), placed in the same command
  section/position as the other enhanced commands, with a per-language description.
- **Path**: `README.md`, `README.de.md`, `README.es.md`, `README.fr.md`, `README.ja.md`, `README.ko.md`, `README.pt-BR.md`, `README.zh-CN.md`
- **Covers**: REQ-016, NFR-001; Plan: Phase 2 (C4)
- **Dependencies**: none — `[P]` with T1.x/T2.1
- **Verification**: manual inspection (docs); no automated per-row test required by the repo.

## Group 3 — Tests (Plan Phase 3)

### T3.1 — Contract tests `tests/test_onboard_template.py`

- **Outcome**: New pytest module asserting onboard.md's confirmed behavior contract.
- **Path**: `tests/test_onboard_template.py`
- **Covers**: REQ-001..015, NFR-002,003; Plan: Phase 3 (Plan Decision 4)
- **Dependencies**: T1.1, T1.2, T1.3, T1.4
- **Test Scenarios**:
  - **S1.1** Frontmatter has `description` and `argument-hint` including `[path]`. (REQ-007)
  - **S1.2** Language Preference references both `language.interaction` and `language.document`, and
    does **not** use the `language.commit` regime. (NFR-001)
  - **S1.3** Declares high-signal-first whole-repo scan respecting `.gitignore` with a no-git fallback. (REQ-007)
  - **S1.4** Declares streaming/resumable scan (does not block until the full scan completes). (REQ-006)
  - **S1.5** Declares optional `[path]` narrowing. (REQ-007)
  - **S1.6** Extraction scope = conventions + narrow constraints, and explicitly excludes decisions and pitfalls. (REQ-003, OUT-001)
  - **S1.7** Constraints only from config-level explicit prohibitions with an evidence anchor; no-signal → no-constraint. (REQ-009)
  - **S1.8** Conventions written immediately as `candidate`; async refinement via `/distill review`. (REQ-004)
  - **S1.9** Constraints held for an inline end-of-scan quick review before persistence, worded as persist/don't-persist (not "vet"). (REQ-005)
  - **S1.10** Records reuse the distill store/format; `derivation: inferred` → `status: candidate` always; `evidence.facts` = code observation; `provenance` = onboard scan. (REQ-011, REQ-012)
  - **S1.11** Never clobbers existing vetted/human/distill records; only add / edit-own-candidate. (REQ-010)
  - **S1.12** Reads the existing profile, de-duplicates, adjudicates conflicts; idempotent re-run. (REQ-008)
  - **S1.13** Prerequisite: stop → `codexspec init` when `.codexspec/` absent; else ensure the canonical 4-dir scaffold. (REQ-015)
  - **S1.14** Read-only on code; write-only to `.codexspec/profile/`; no source/test/git/constitution mutation. (REQ-014)
  - **S1.15** Standalone: no auto-next, no auto-hook, and no Automatic Distillation section. (REQ-013)
  - **S1.16** Terminal summary reports records written/updated and distinguishes deep-read from sampled coverage. (REQ-002, NFR-002)
  - **S1.17** `distill.md` contains the onboard code-sourced `evidence.facts` cross-note. (REQ-011)

### T3.2 — Installer registration + count tests in `tests/commands/test_installer.py`

- **Outcome**: Update existing count assertions and add onboard-specific tests.
- **Path**: `tests/commands/test_installer.py`
- **Covers**: REQ-016; Plan: Phase 3 (C4)
- **Dependencies**: T2.1
- **Test Scenarios**:
  - **S2.1** `get_commands_metadata()` contains an `onboard` entry with `category == "enhanced"`,
    `file_name == "onboard.md"`, `display_name == "/codexspec:onboard"`. (REQ-016)
  - **S2.2** Total command count == 25. (REQ-016)
  - **S2.3** Count of `enhanced` commands == 8, and the `onboard` entry appears within the enhanced
    group. (REQ-016)

### T3.3 — CLI list-commands count in `tests/test_cli.py`

- **Outcome**: Bump the list-commands count assertion `"24"` → `"25"`.
- **Path**: `tests/test_cli.py`
- **Covers**: REQ-016; Plan: Phase 3
- **Dependencies**: T2.1
- **Test Scenarios**:
  - **S3.1** `list-commands` output shows the total command count as 25. (REQ-016)

### T3.4 — Verify language-regime split test stays green (checkpoint)

- **Outcome**: Confirm `tests/test_sdd_workflow_templates.py::test_command_templates_split_interaction_and_document_language`
  passes with onboard present and **not** added to the `commit_templates` set. (No new test code; a
  verification checkpoint against a known-risk test.)
- **Path**: `tests/test_sdd_workflow_templates.py` (run only)
- **Covers**: NFR-001; Plan: Phase 3 (C5, Decision 6)
- **Dependencies**: T1.1
- **Verification**: run the named test; green required. Non-testable (executes an existing test).

## Group 4 — Derived sync, docs, verification (Plan Phase 4)

### T4.1 — Regenerate derived install artifacts

- **Outcome**: Run `uv run codexspec init . --force --ai both`; the derived
  `.claude/commands/codexspec/onboard.md` and `.agents/skills/codexspec-onboard/SKILL.md` are created
  and in sync with the template; no other derived/config churn.
- **Path**: `.claude/commands/codexspec/onboard.md`, `.agents/skills/codexspec-onboard/SKILL.md` (generated)
- **Covers**: REQ-016; Plan: Phase 4 (C4, Plan Decision 3)
- **Dependencies**: T1.1, T1.2, T1.3
- **Verification**: `git status` shows only the new onboard derived files as additions; `config.yml`
  and other derived artifacts unchanged.

### T4.2 — Update `CLAUDE.md`

- **Outcome**: Add onboard to the command tables and implementation-status table, plus a brief
  architecture subsection (onboard = distill cold-start; enhanced family; two extracted categories;
  tiered gate). Documentation support.
- **Path**: `CLAUDE.md`
- **Covers**: REQ-016 (documentation support); Plan: Phase 4
- **Dependencies**: T2.1
- **Verification**: manual inspection.

### T4.3 — Final verification

- **Outcome**: `uv run ruff check src/` clean; `uv run pytest` full suite green; reach a clean
  isolated review gate (spawn an isolated review subagent per [[P-2026-0811-1418yq-1]]).
- **Path**: — (verification support)
- **Covers**: all (verification support); Plan: Phase 4
- **Dependencies**: T1.1–T4.2
- **Verification**: ruff exit 0; full suite passed; isolated review PASS.

## Dependency Summary

- T1.1 → T1.2, T1.3, T2.1, T3.4, T4.1
- T1.4 `[P]` (independent)
- T1.1–T1.4 → T3.1
- T2.1 → T3.2, T3.3, T4.2
- T2.2 `[P]` (independent)
- all → T4.3
- Acyclic; dependents ordered after dependencies.

## Coverage Table

| Requirement / Plan Item | Tasks | Scenarios |
|---|---|---|
| REQ-001 | T1.1 | (contract via S1.16 summary/behavior) |
| REQ-002 | T1.1; T3.1 | S1.16 |
| REQ-003 | T1.1; T3.1 | S1.6 |
| REQ-004 | T1.1; T3.1 | S1.8 |
| REQ-005 | T1.1; T3.1 | S1.9 |
| REQ-006 | T1.1; T3.1 | S1.4 |
| REQ-007 | T1.1; T3.1 | S1.1, S1.3, S1.5 |
| REQ-008 | T1.1; T3.1 | S1.12 |
| REQ-009 | T1.1; T3.1 | S1.7 |
| REQ-010 | T1.1; T3.1 | S1.11 |
| REQ-011 | T1.2, T1.4; T3.1 | S1.10, S1.17 |
| REQ-012 | T1.2; T3.1 | S1.10 |
| REQ-013 | T1.1; T3.1 | S1.15 |
| REQ-014 | T1.1; T3.1 | S1.14 |
| REQ-015 | T1.3; T3.1 | S1.13 |
| REQ-016 | T2.1, T2.2, T4.1, T4.2; T3.2, T3.3 | S2.1, S2.2, S2.3, S3.1 |
| NFR-001 | T1.1, T2.2; T3.1, T3.4 | S1.2 |
| NFR-002 | T1.1; T3.1 | S1.16 |
| NFR-003 | T1.1; T3.1 | S1.9 |
| Plan Phase 1 | T1.1–T1.4 | — |
| Plan Phase 2 | T2.1, T2.2 | — |
| Plan Phase 3 | T3.1–T3.4 | — |
| Plan Phase 4 | T4.1–T4.3 | — |

## Unmapped Tasks

None. Every task maps to a requirement or is labeled documentation/verification implementation support.

## Implementation Status

- [x] T1.1 — `templates/commands/onboard.md` authored (core discipline)
- [x] T1.2 — record-format reuse + onboard deltas encoded in onboard.md
- [x] T1.3 — prerequisite + canonical scaffold-ensure encoded in onboard.md
- [x] T1.4 — onboard cross-note added to `templates/commands/distill.md`
- [x] T2.1 — onboard registered in `installer.py` (enhanced, after evolve); docstring 7→8/24→25; inline `# Enhanced Commands (8)`
- [x] T2.2 — onboard row added to all 8 `README*.md` (Self-Evolution table, after evolve)
- [x] T3.1 — `tests/test_onboard_template.py` (17 contract tests, S1.1–S1.17) — pass
- [x] T3.2 — `tests/commands/test_installer.py` counts 24→25 / 7→8 + `test_onboard_registered` + placement — pass
- [x] T3.3 — `tests/test_cli.py` list-commands count 24→25 — pass
- [x] T3.4 — `test_command_templates_split_interaction_and_document_language` green (onboard interaction+document, not in `commit_templates`)
- [x] T4.1 — derived artifacts regenerated via `codexspec init . --force --ai both` (onboard command + SKILL; distill cross-note propagated; no config/other churn)
- [x] T4.2 — `CLAUDE.md` updated (architecture subsection + Self-Evolution table (3) + status table)
- [x] T4.3 — verification: ruff clean; full suite 1165 passed / 50 skipped; isolated review gate **PASS** (§7.6, 0 P0–P3, requirements+verification complete, isolated topology)
