# Tasks: design-to-plan command rename

## P1: Canonical identity and distribution consumers

### T1: Rename the command and active references

- [x] Complete
- **Covers: REQ-001, REQ-002, REQ-003; Plan: P1**
- **Dependencies**: None.
- **Outcome**: design-to-plan replaces the old identity without changing behavior.
- **Paths**: internal/command_templates/sources/, templates/commands/,
  templates/translations/, src/codexspec/commands/installer.py,
  src/codexspec/integrations/codex.py, `src/codexspec/__init__.py`, tests/.
- **Test Scenarios**:
  - S1: Registry and fresh Claude/Codex installs expose the new name only.
  - S2: Planner inputs, legacy-artifact handling, review-plan and next stage remain.
  - S3: Auto-next, auto-dev and localized catalogs use the new identity.
- **Verification**: New regression tests first fail on old identity; existing
  workflow, planner and translation contract tests pass after the rename.

## P2: Installed entry retirement

### T2: Remove the old runnable entry on selected integration updates

- [x] Complete
- **Covers: REQ-001, REQ-004; Plan: P2**
- **Dependencies**: T1.
- **Outcome**: Successful repeated updates retain only the new runnable entry.
- **Paths**: src/codexspec/commands/installer.py,
  src/codexspec/integrations/codex.py, tests/test_planning_command_rename.py.
- **Test Scenarios**:
  - S4: Existing Claude/Codex entries are retired with force true and false;
    repeated installs are safe and unrelated commands/resources survive.
  - S5: Missing new template does not trigger retirement.
  - S6: New-entry write failure preserves the old entry and propagates failure.
  - S7: Old-entry removal failure propagates failure.
  - S8: Linked retirement parent is refused without changing external files;
    terminal entry symlinks are removed without touching their targets.
  - S9: CLI init --ai claude/codex/both retires only selected integrations.
- **Verification**: Red-green regression tests for each behavior and integration.

## P3: Current guidance, generation, and verification

### T3: Synchronize current guidance and generated copies

- [x] Complete
- **Covers: REQ-001, REQ-003; Plan: P3**
- **Dependencies**: T1, T2.
- **Outcome**: Active documentation and generated commands agree with the new name.
- **Paths**: README*.md, docs/*/{reference,user-guide,getting-started}/,
  docs/*/index.md, current case-study instructions, CLAUDE.md, AGENTS.md,
  scripts/powershell/check-prerequisites.ps1, .codexspec/config.yml,
  extensions/EXTENSION-DEVELOPMENT-GUIDE.md; generated .claude/commands/codexspec/
  and .agents/skills/ via normal init.
- **Verification**: Scoped stale-reference inspection, renderer --check-distribution,
  docs build/checks. Retain historical SDD/profile/release evidence.

### T4: Complete validation

- [x] Complete
- **Covers: REQ-001, REQ-002, REQ-003, REQ-004; Plan: P3**
- **Dependencies**: T1, T2, T3.
- **Outcome**: Required deterministic checks pass and scenario coverage is complete.
- **Paths**: All selected changes and this feature's artifacts.
- **Verification**: Focused tests, full pytest, pre-commit gates, distribution
  check, package checks, docs build, diff check; map S1-S9 to actual tests and
  provide the baseline for the implement-tasks isolated review-code gate.

The isolated review-code gate runs after task completion as required by
implement-tasks; only its valid complete-feature PASS establishes final success.

## Coverage

| Plan / Requirement | Tasks | Scenarios |
| --- | --- | --- |
| P1 / REQ-001, REQ-002, REQ-003 | T1 | S1-S3 |
| P2 / REQ-001, REQ-004 | T2 | S4-S9 |
| P3 / REQ-001..004 | T3, T4 | Revalidate S1-S9 |

No unmapped tasks or unresolved questions. Dependencies are sequential and acyclic.

## Scenario Evidence

- S1: tests/test_planning_command_rename.py registry/fresh-install cases.
- S2: tests/test_spec_to_design_templates.py downstream planner contracts and
  tests/test_sdd_workflow_templates.py planning input/authority/review contracts.
- S3: tests/test_sdd_workflow_templates.py auto-next cases,
  tests/test_auto_dev_template.py, tests/test_translation_files.py.
- S4: test_update_retires_entry_and_preserves_unrelated_files (both integrations,
  force true/false, two invocations).
- S5: test_partial_distribution_does_not_retire_entry.
- S6: test_replacement_write_failure_preserves_old_entry.
- S7: test_retirement_failure_is_not_silenced.
- S8: test_linked_retirement_parent_is_refused,
  test_retirement_entry_symlink_does_not_delete_target; the additional
  test_alias_above_installation_root_is_supported guards OS path aliases.
- S9: test_cli_update_retires_only_selected_integrations (claude/codex/both).

Initial regression run: 16 failed, 4 passed (expected missing behavior). After
implementation: 22 rename regression cases pass. Full suite: 1994 passed,
54 skipped. Strict MkDocs build and command distribution check pass.

Package archive checks: 18 passed. Ruff, formatting, mypy, bandit, YAML, shellcheck,
dependency audit and whitespace checks pass. Markdown normalization was reapplied
and checked. Final isolated review is reported in the external review state store.

Review regressions cover non-empty replacement directory collisions, replacement
links to old entries, and linked replacement skill directories under both force
modes. The 10 added cases initially produced 8 expected failures and 2 passing
forced-directory error cases. Quick documentation follows its existing explicit
short sequence; the full SDD chain continues to include spec-to-design.
