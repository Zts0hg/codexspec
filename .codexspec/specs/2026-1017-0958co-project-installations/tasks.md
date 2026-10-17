# Tasks: Project Installation Discovery and Upgrade

**Authority**: requirements.md → spec.md → design.md → plan.md.
**Workspace**: 2026-1017-0958co-project-installations.

Code tasks use test-first execution: write the listed behavioral tests, record the
initial failure, implement, then run focused tests and applicable regressions.
Documentation is edited directly. Every scenario below must map to executable
verification before completion. No task authorizes commits, releases or upgrades
of unrelated user projects.

## P1: Metadata schema and expected artifacts

- [x] T01: Metadata schema and expected artifacts.
- **Paths**: `src/codexspec/installations/{__init__,metadata,render}.py`; tests/test_installation_metadata.py.
- **Dependencies**: None.
- **Covers**: REQ-005, REQ-006, REQ-007, REQ-012, REQ-014, NFR-001; **Plan**: P1.
- **Verification**: test-first focused pytest cases for every scenario; relevant existing regressions.

### Test Scenarios

- T01-S01: Expected rendered artifacts match both integrations, language and platform.
- T01-S02: Metadata with a version and valid checksums verifies unchanged content.
- T01-S03: Missing or changed managed file reports its path.
- T01-S04: Missing version still checks available checksum entries.
- T01-S05: Absent metadata is legacy; malformed/unsafe/duplicate paths are invalid, never followed.
- T01-S06: Project-owned content and custom context body are not classified as corrupted toolkit files.
- T01-S07: Cannot publish a current-release baseline over actual files that differ from expected output.

## P1: Publish verified metadata from init

- [x] T02: Publish verified metadata from init.
- **Paths**: `src/codexspec/__init__.py`; tests/test_installation_metadata.py.
- **Dependencies**: T01.
- **Covers**: REQ-005, REQ-012, REQ-014; **Plan**: P1.
- **Verification**: test-first focused pytest cases for every scenario; relevant existing regressions.

### Test Scenarios

- T02-S01: Fresh init creates verified metadata for Claude, Codex and both.
- T02-S02: Force update publishes new baseline only on full expected-content success.
- T02-S03: Nonforce init preserving edited files does not bless them as the current release.
- T02-S04: Configuration and constitution/custom instruction content remain preserved.
- T02-S05: Failed or incomplete installation does not publish successful new metadata.

## P2: Offline recursive discovery and grouping

- [x] T03: Offline recursive discovery and grouping.
- **Paths**: src/codexspec/installations/discovery.py; tests/test_installation_discovery.py.
- **Dependencies**: T01.
- **Covers**: REQ-002, REQ-003, REQ-004, REQ-006, REQ-007; **Plan**: P2.
- **Verification**: test-first focused pytest cases for every scenario; relevant existing regressions.

### Test Scenarios

- T03-S01: Root, hidden and nested installation directories are found; .git/.codexspec internals are pruned.
- T03-S02: Symlink directories and .codexspec links are not followed.
- T03-S03: Linked Git worktrees are grouped without collapsing versions or expanding root scope.
- T03-S04: Legacy/no-Git projects remain visible with truthful version/baseline status.
- T03-S05: Invalid root fails; inaccessible descendant reports incomplete results and other paths continue.
- T03-S06: Scan makes no network calls or project file changes; empty inventory is valid.

## P3: Prepare update and protect affected files

- [x] T04: Prepare update and protect affected files.
- **Paths**: src/codexspec/installations/upgrade.py; tests/test_installation_upgrade.py.
- **Dependencies**: T01.
- **Covers**: REQ-009, REQ-010, REQ-011, REQ-012, REQ-014, NFR-001; **Plan**: P3.
- **Verification**: test-first focused pytest cases for every scenario; relevant existing regressions.

### Test Scenarios

- T04-S01: Clean affected tracked files produce a complete applicable plan; unrelated dirty business code is allowed.
- T04-S02: Affected staged, unstaged, deleted tracked, unmerged and untracked files block the entire project.
- T04-S03: Affected ignored content or missing/unusable Git evidence cannot silently authorize replacement.
- T04-S04: Assume-unchanged and skip-worktree flags cannot hide affected local edits.
- T04-S05: Nested projects and linked worktrees inspect the correct Git repository under hostile inherited Git environment.
- T04-S06: Configuration, integration choice and custom context body are preserved; unknown choices skip.
- T04-S07: Links, hardlinks, nonfile targets, traversal/unknown worker outputs are rejected before project writes.
- T04-S08: Legacy metadata absence alone permits safe migration; same-version mismatch remains eligible.
- T04-S09: Recorded newer version is not automatically downgraded.

## P3: Apply checked plans and report partial failures

- [x] T05: Apply checked plans and report partial failures.
- **Paths**: src/codexspec/installations/upgrade.py; tests/test_installation_upgrade.py.
- **Dependencies**: T04.
- **Covers**: REQ-010, REQ-011, REQ-012, REQ-013, NFR-001, NFR-002; **Plan**: P3.
- **Verification**: test-first focused pytest cases for every scenario; relevant existing regressions.

### Test Scenarios

- T05-S01: Successful apply writes only planned outputs and publishes verified metadata last.
- T05-S02: Stale input, Git state or destination after preparation yields no-write refusal before application.
- T05-S03: Failure during application reports partial failure and never publishes successful new metadata.
- T05-S04: Skips make no directories, metadata, Git/index mutations or backup artifacts.
- T05-S05: Explicit planned retirement does not delete unrelated extension files.

## P4: Acquire isolated target runtime and render with worker

- [x] T06: Acquire isolated target runtime and render with worker.
- **Paths**: src/codexspec/installations/{release,worker}.py; tests/test_installation_release.py.
- **Dependencies**: T01, T04.
- **Covers**: REQ-008, REQ-009, REQ-012, REQ-013, NFR-002; **Plan**: P4.
- **Verification**: test-first focused pytest cases for every scenario; relevant existing regressions.

### Test Scenarios

- T06-S01: Resolver chooses one non-yanked stable version and pins it for the invocation.
- T06-S02: Network, invalid release data, Python/dependency and install failures precede all project writes.
- T06-S03: Global CLI and original projects are not used as worker output destinations.
- T06-S04: Actual target worker renders supported integrations and language with config/body preservation.
- T06-S05: Wrong version, unsupported protocol, corrupt result or nonzero worker result is refused.
- T06-S06: Temporary runtime/snapshot cleanup does not remove or modify user content.

## P5: Wire scan CLI, selection and results

- [x] T07: Wire scan CLI, selection and results.
- **Paths**: src/codexspec/installations/cli.py; `src/codexspec/__init__.py`; src/codexspec/translator.py; tests/test_scan_cli.py.
- **Dependencies**: T02, T03, T05, T06.
- **Covers**: REQ-001, REQ-004, REQ-013, REQ-014, NFR-001, NFR-002; **Plan**: P5.
- **Verification**: test-first focused pytest cases for every scenario; relevant existing regressions.

### Test Scenarios

- T07-S01: Scan-only displays inventory offline without invoking release acquisition.
- T07-S02: Interactive yes/no/all/quit selection follows discovery; all still respects safety.
- T07-S03: --upgrade --yes runs without prompts and summarizes success/skip/failure.
- T07-S04: --yes without --upgrade and noninteractive --upgrade without --yes reject explicitly.
- T07-S05: One project failure or unsafe skip does not stop remaining projects.
- T07-S06: No matches, incomplete scan, unknown version and content mismatch have distinct truthful messages.
- T07-S07: Language and exit-code behavior follow the invoking configuration with English fallback.

## P6: Document and validate complete feature

- [x] T08: Document and validate complete feature.
- **Paths**: README.md; docs/en/reference/cli.md; CLAUDE.md; feature tasks.md.
- **Dependencies**: T01–T07.
- **Covers**: REQ-001–014, NFR-001, NFR-002; **Plan**: P6.
- **Verification**: Document the three invocation forms, independent version/content
  status, legacy migration, scope and skip behavior. Run all new scenario tests,
  relevant init/worktree/i18n tests, full pytest suite, Ruff, distribution consistency,
  package inclusion and git diff --check. Complete the scenario coverage self-check
  and record actual results below. The independent complete-feature code-review gate
  follows implementation verification and remains mandatory for workflow completion;
  its reports and repair-loop state belong in the external review store.

## Coverage and Dependencies

| Plan | Design | Tasks |
| --- | --- | --- |
| P1 | C1, D1, D4 | T01, T02 |
| P2 | C2 | T03 |
| P3 | C4, C5, D2–D4 | T04, T05 |
| P4 | C3, C4, D2 | T06 |
| P5 | C6 | T07 |
| P6 | C1–C6 | T08 |

Scenario ownership is one-to-one with its Txx prefix. Requirements map through
individual task Covers lines and the plan coverage table. No unmapped tasks.
Dependencies are acyclic: T01 → T02/T03/T04 → T05/T06 → T07 → T08.

## Execution Evidence

Implementation uses the new installation modules and existing runtime installers.
T01–T08 implementation and deterministic verification are complete. These checkboxes do not assert the final review verdict: workflow completion additionally requires the independent complete-feature review gate, whose results are kept in the external review store.

Initial focused tests for T01–T07 failed before their modules/hooks/command existed; subsequent focused runs passed. Additional red/green checks caught incomplete renderer inventories, inaccessible scan roots, symlink ancestors, legacy planning-entry retirement, malformed integration configuration, Git inspection timeout handling, long-path display and edits made during interactive selection. Each was reproduced before its corresponding correction.

Checks already completed: all 108 new focused cases; Ruff source/new-test lint and formatting; mypy with the project YAML stubs; Bandit; Markdown lint; eight-language scan catalog key/placeholder parity; command distribution consistency; wheel/sdist build; 18 package-content tests; a fresh wheel-only environment exercised both integrations with zh-CN, offline scan and the private worker (104 managed files). The first full regression run found one missing translation-key failure (2543 passed, 60 skipped); all eight catalogs now include the new messages, and the 77 catalog tests pass. Initial complete implementation regression command: `uv run --no-sync --python 3.11 python -m pytest -q -n 4 --dist loadfile` — **2553 passed, 60 skipped**, exit 0. Python, pytest and the CodexSpec CLI use the same project virtual environment. Final review results are stored outside the repository.

### Review-driven regression coverage

Independent review identified two verified boundary defects. Git byte-layout output
was insufficient proof of allowed CRLF conversion; effective text/eol attributes
and autocrlf now govern normalization, with explicit -text retaining byte-level
protection. JSON/YAML recursion failures are translated at each new parsing
boundary into existing invalid-project, skip, or acquisition diagnostics.

Seven new denial/exception cases failed before these repairs; six clean-conversion
controls already passed. All 13 cases pass after repair. A subsequent binary-content control exposed three
additional automatic-conversion bypasses; all 18 text/binary policy combinations
now pass, using Git content classification only after conversion policy is established. The shared refusal snapshot
now verifies directory structure, file modes/content, and Git metadata as well as
project files. Existing protocol/version tests use otherwise valid payloads;
localized rendering and declined-project content have direct assertions.

A further independent review found that parent-component starting paths and a
project named `result.json` collided with temporary worker paths. Both public CLI
regressions failed before correction. Project snapshots now use a separate
subdirectory and a canonical basename; actual project reads retain their original
path validation. The two cases verify successful installation and unchanged
sibling projects through the real worker.

The 45 enumerated scenarios remain covered. Added executable assertions:

- T06-S04/T07-S03: `test_t06_s04_t07_s03_valid_project_paths` (parent path and protocol-filename basename).
- T04-S02/S04: `test_t04_s02_s04_crlf_protection_follows_git_policy` (nine policies, each with text and binary content).
- T06-S02/S05: `test_t06_s02_s05_deep_json_is_reportable` (provider and worker).
- T07-S05: `test_t07_s05_deep_project_input_does_not_abort_siblings`
  (metadata and configuration; valid later projects are upgraded).

### Scenario-to-test mapping

Test names contain their owning task/scenario IDs. Additional regression tests in `test_init_compliance.py`, `test_init_profile.py`, `test_init_language.py` and `test_codex_integration.py` verify preserved context/configuration and platform renderers.

| Scenario | Executable assertions |
| --- | --- |
| T01-S01 | `tests/test_installation_metadata.py::test_t01_s01_s02_render_and_verify` |
| T01-S02 | `tests/test_installation_metadata.py::test_t01_s01_s02_render_and_verify` |
| T01-S03 | `tests/test_installation_metadata.py::test_t01_s03_s04_missing_version_still_checks_content` |
| T01-S04 | `tests/test_installation_metadata.py::test_t01_s03_s04_missing_version_still_checks_content` |
| T01-S05 | `tests/test_installation_metadata.py::test_t01_s05_reject_invalid_metadata_paths`; `tests/test_installation_metadata.py::test_t01_s05_duplicate_metadata_keys_rejected` |
| T01-S06 | `tests/test_installation_metadata.py::test_t01_s06_custom_context_does_not_change_projection` |
| T01-S07 | `tests/test_installation_metadata.py::test_t01_s07_refuse_baseline_over_changed_files` |
| T02-S01 | `tests/test_installation_metadata.py::test_t02_s01_s02_init_records_real_release` |
| T02-S02 | `tests/test_installation_metadata.py::test_t02_s01_s02_init_records_real_release`; `tests/test_installation_metadata.py::test_t02_s02_force_replaces_and_records_expected` |
| T02-S03 | `tests/test_installation_metadata.py::test_t02_s03_s04_nonforce_does_not_bless_edits` |
| T02-S04 | `tests/test_installation_metadata.py::test_t02_s03_s04_nonforce_does_not_bless_edits` |
| T02-S05 | `tests/test_installation_metadata.py::test_t02_s05_incomplete_install_does_not_publish` |
| T03-S01 | `tests/test_installation_discovery.py::test_t03_s01_s04_s06_recursive_readonly` |
| T03-S02 | `tests/test_installation_discovery.py::test_t03_s02_links_not_followed`; `tests/test_installation_discovery.py::test_t03_s02_root_through_symlink_ancestor_rejected` |
| T03-S03 | `tests/test_installation_discovery.py::test_t03_s03_worktrees_grouped_within_scope` |
| T03-S04 | `tests/test_installation_discovery.py::test_t03_s01_s04_s06_recursive_readonly` |
| T03-S05 | `tests/test_installation_discovery.py::test_t03_s05_invalid_root_and_unreadable_child`; `tests/test_installation_discovery.py::test_t03_s05_unreadable_root_fails` |
| T03-S06 | `tests/test_installation_discovery.py::test_t03_s01_s04_s06_recursive_readonly` |
| T04-S01 | `tests/test_installation_upgrade.py::test_t04_s01_s08_clean_legacy_and_unrelated_changes` |
| T04-S02 | `tests/test_installation_upgrade.py::test_t04_s02_s03_s04_modified_paths_are_unchanged`; `tests/test_installation_upgrade.py::test_t04_s02_unmerged_index_refused` |
| T04-S03 | `tests/test_installation_upgrade.py::test_t04_s02_s03_s04_modified_paths_are_unchanged`; `tests/test_installation_upgrade.py::test_t04_s03_missing_git_is_not_permission` |
| T04-S04 | `tests/test_installation_upgrade.py::test_t04_s02_s03_s04_modified_paths_are_unchanged` |
| T04-S05 | `tests/test_installation_upgrade.py::test_t04_s05_inherited_git_environment_is_ignored`; `tests/test_installation_upgrade.py::test_t04_s05_nested_and_worktree_scope` |
| T04-S06 | `tests/test_installation_upgrade.py::test_t04_s06_options_preserved_and_unknown_rejected`; `tests/test_installation_upgrade.py::test_t04_s06_context_body_cannot_be_replaced`; `tests/test_installation_upgrade.py::test_t04_s06_malformed_integration_choice_is_reportable` |
| T04-S07 | `tests/test_installation_upgrade.py::test_t04_s07_invalid_destination` |
| T04-S08 | `tests/test_installation_upgrade.py::test_t04_s01_s08_clean_legacy_and_unrelated_changes`; `tests/test_installation_upgrade.py::test_t04_s08_same_version_discard_is_repairable` |
| T04-S09 | `tests/test_installation_upgrade.py::test_t04_s09_no_downgrade` |
| T05-S01 | `tests/test_installation_upgrade.py::test_t05_s01_success_publishes_metadata_last` |
| T05-S02 | `tests/test_installation_upgrade.py::test_t05_s02_s04_stale_plan_is_no_write`; `tests/test_installation_upgrade.py::test_t05_s02_stale_input_or_index` |
| T05-S03 | `tests/test_installation_upgrade.py::test_t05_s03_failure_does_not_publish_metadata` |
| T05-S04 | `tests/test_installation_upgrade.py::test_t05_s02_s04_stale_plan_is_no_write` |
| T05-S05 | `tests/test_installation_upgrade.py::test_t05_s05_retirement_preserves_extensions`; `tests/test_installation_upgrade.py::test_t05_s05_legacy_retired_planning_command` |
| T06-S01 | `tests/test_installation_release.py::test_t06_s01_resolve_stable`; `tests/test_installation_release.py::test_t06_s01_s02_s06_pinned_runtime_and_cleanup` |
| T06-S02 | `tests/test_installation_release.py::test_t06_s02_acquisition_failure_no_project_mutation`; `tests/test_installation_release.py::test_t06_s02_invalid_release_data`; `tests/test_installation_release.py::test_t06_s02_network_error`; `tests/test_installation_release.py::test_t06_s01_s02_s06_pinned_runtime_and_cleanup` |
| T06-S03 | `tests/test_installation_release.py::test_t06_s03_s04_real_worker_renders_outside_project` |
| T06-S04 | `tests/test_installation_release.py::test_t06_s03_s04_real_worker_renders_outside_project`; `tests/test_installation_release.py::test_t06_s04_s06_worker_integrations_and_cleanup` |
| T06-S05 | `tests/test_installation_release.py::test_t06_s05_refuse_worker_results`; `tests/test_installation_release.py::test_t06_s05_nonzero_worker_and_corrupt_result` |
| T06-S06 | `tests/test_installation_release.py::test_t06_s04_s06_worker_integrations_and_cleanup`; `tests/test_installation_release.py::test_t06_s01_s02_s06_pinned_runtime_and_cleanup` |
| T07-S01 | `tests/test_scan_cli.py::test_t07_s01_s06_scan_offline` |
| T07-S02 | `tests/test_scan_cli.py::test_t07_s02_selection`; `tests/test_scan_cli.py::test_t07_s02_all_still_protects_dirty_project` |
| T07-S03 | `tests/test_scan_cli.py::test_t07_s03_s05_real_bulk_upgrade_and_skip` |
| T07-S04 | `tests/test_scan_cli.py::test_t07_s04_invalid_modes` |
| T07-S05 | `tests/test_scan_cli.py::test_t07_s03_s05_real_bulk_upgrade_and_skip`; `tests/test_scan_cli.py::test_t07_s05_failure_continues`; `tests/test_scan_cli.py::test_t07_s05_input_changed_during_render_is_not_applied` |
| T07-S06 | `tests/test_scan_cli.py::test_t07_s01_s06_scan_offline`; `tests/test_scan_cli.py::test_t07_s06_s07_empty_and_language`; `tests/test_scan_cli.py::test_t07_s06_incomplete_and_content_mismatch` |
| T07-S07 | `tests/test_scan_cli.py::test_t07_s06_s07_empty_and_language` |
