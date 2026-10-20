# Tasks: Effective Configuration Overview

**Plan**: [plan.md](plan.md)

## 1. Guard the user-visible command contract

### [x] T001 — Focused overview contract checks

- **Outcome**: `tests/test_config_overview_template.py` detects missing or extra overview rows, incorrect fallback rules, misplaced action choices, and accidental changes to the read-only and excluded paths.
- **Paths**: `tests/test_config_overview_template.py`; read `internal/command_templates/sources/config.md`.
- **Depends on**: None.
- **Covers**: REQ-001, REQ-002, REQ-003, REQ-004, REQ-005; **Plan**: Phase 1, contract verification.
- **Verification**: Run the focused pytest module before and after T002; the new contract checks should fail before the source change and pass afterward.
- **Test Scenarios**:
  - **S001**: The no-argument path instructs rendering the metadata table and the adjustable-settings table before action selection, without an initial raw-YAML substitute.
  - **S002**: The tables enumerate exactly three metadata and nine adjustable fields, and omit `language.templates` and unknown-key expansion.
  - **S003**: Language defaults use the explicit → `output` → `en` fallback; absent worktrees, maintenance, and review-decision settings show their effective defaults.
  - **S004**: After both tables, only modify, reset, and view-only appear as top-level choices; view-only exits without writing.
  - **S005**: `--view`, CLI, and missing-config behavior remain outside the changed no-argument branch.
  - **S006**: Missing metadata is shown as absent rather than given a fabricated stored value; `project.created` is described as generated on the creation date.

### [x] T002 — Author the two-table no-argument flow

- **Outcome**: The authored config command renders the confirmed overview before offering actions while retaining existing handlers.
- **Paths**: `internal/command_templates/sources/config.md`.
- **Depends on**: T001.
- **Covers**: REQ-001, REQ-002, REQ-003, REQ-004, REQ-005; **Plan**: Phase 2, command source update.
- **Verification**: T001 scenarios S001–S006 pass; inspect source diff for unchanged `--view`, missing-config, modify, and reset behavior. This command-template edit is verified by the T001 contract checks.

## 2. Distribute and verify

### [x] T003 — Regenerate all command forms

- **Outcome**: The authored source, complete public template, and repository Claude/Codex install copies all contain the same overview contract.
- **Paths**: `internal/command_templates/sources/config.md`, `templates/commands/config.md`, `.claude/commands/codexspec/config.md`, `.agents/skills/codexspec-config/SKILL.md`.
- **Depends on**: T002.
- **Covers**: REQ-001, REQ-005; **Plan**: Phase 3, distribution outputs.
- **Verification**: Run the established fragment renderer and command installer in the feature worktree, then `uv run python internal/command_template_fragments.py --check-distribution`.

### [x] T004 — Run applicable quality checks and inspect scope

- **Outcome**: Focused and applicable existing checks pass, and the final diff contains no CLI or unrelated configuration behavior change.
- **Paths**: `tests/test_config_overview_template.py`, existing config/installer test modules, generated command forms, feature artifacts.
- **Depends on**: T003.
- **Covers**: REQ-001, REQ-002, REQ-003, REQ-004, REQ-005; **Plan**: Phase 4, final verification.
- **Verification**: Run focused pytest, distribution check, applicable lint/documentation checks, and `git diff --check`; inspect changed paths and diff against REQ-005.

## Dependencies

`T001 → T002 → T003 → T004`

## Coverage

| Plan phase | Requirements | Tasks and scenarios |
|---|---|---|
| Phase 1 | REQ-001–REQ-005 | T001, S001–S006 |
| Phase 2 | REQ-001–REQ-005 | T002; verified with T001 scenarios S001–S006 |
| Phase 3 | REQ-001, REQ-005 | T003 |
| Phase 4 | REQ-001–REQ-005 | T004 |

No unmapped tasks.
