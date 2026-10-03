# Scenario Verification

Each enumerated scenario is checked by the assertions below. PowerShell execution requires its
platform interpreter; this macOS run uses the distribution and ordering/JSON contract assertions
for S029, and the platform tests remain in the suite for Windows.

| Scenario | Asserting tests |
|---|---|
| S001 | `tests/test_worktrees.py::test_s001_setting_default_and_optout` |
| S002 | `tests/test_worktrees.py::test_s002_s003_write_preserves_independent_config` |
| S003 | `tests/test_worktrees.py::test_s002_s003_write_preserves_independent_config` |
| S004 | `tests/test_worktrees.py::test_s004_s006_parent_and_fixed_automation`; `tests/test_worktrees_cli.py::test_s004_nested_helper_honors_checkout_optout` |
| S005 | `tests/test_worktrees.py::test_s005_bare_parent` |
| S006 | `tests/test_worktrees.py::test_s004_s006_parent_and_fixed_automation` |
| S007 | `tests/test_worktrees.py::test_s007_s008_s009_s012_independent_creation_and_reuse` |
| S008 | `tests/test_worktrees.py::test_s007_s008_s009_s012_independent_creation_and_reuse` |
| S009 | `tests/test_worktrees.py::test_s007_s008_s009_s012_independent_creation_and_reuse` |
| S010 | `tests/test_worktrees.py::test_s010_occupied_and_invalid_destinations` |
| S011 | `tests/test_worktrees.py::test_s011_maintenance_routing_and_reuse` |
| S012 | `tests/test_worktrees.py::test_s007_s008_s009_s012_independent_creation_and_reuse` |
| S013 | `tests/test_worktrees.py::test_s013_concurrent_same_feature_reuses_one_registration`; `tests/test_worktrees.py::test_s013_invalid_preparation_metadata_is_not_adopted`; `tests/test_worktrees.py::test_s013_interrupted_creation_resumes_owned_state`; `tests/test_worktrees.py::test_s013_interrupted_creation_cannot_adopt_changed_head` |
| S014 | `tests/test_worktrees.py::test_s014_ancestry_selection` |
| S015 | `tests/test_worktrees.py::test_s015_fetch_failure_fallback_and_retry` |
| S016 | `tests/test_worktrees.py::test_s016_missing_baseline_stops` |
| S017 | `tests/test_worktrees.py::test_s017_s019_merge_requires_verification_and_resumes` |
| S018 | `tests/test_worktrees.py::test_s018_conflict_must_be_resolved_before_finish` |
| S019 | `tests/test_worktrees.py::test_s017_s019_merge_requires_verification_and_resumes`; `tests/test_worktrees.py::test_s019_interrupted_merge_keeps_verification_obligation` |
| S020 | `tests/test_worktrees_cli.py::test_s020_helper_paths_and_finish`; `tests/test_worktrees_cli.py::test_s020_finish_cli`; `tests/test_worktrees_cli.py::test_s020_resume_interrupted_creation_by_returned_identity` |
| S021 | `tests/test_worktrees_cli.py::test_s021_checkout_local_routed_config_and_toggle` |
| S022 | `tests/test_worktrees_cli.py::test_s022_display_optout_and_feature_config` |
| S023 | `tests/test_worktrees_cli.py::test_s023_mutable_review_is_routed_before_session` |
| S024 | `tests/test_worktrees_cli.py::test_s024_init_first_and_update_are_exempt` |
| S025 | `tests/test_worktrees_cli.py::test_s025_missing_repository_cannot_write`; `tests/test_worktrees_cli.py::test_s025_nonready_maintenance_blocks_config_and_review` |
| S026 | `tests/scripts/bash/test_create_new_feature.py::test_s026_default_isolated_script` |
| S027 | `tests/scripts/bash/test_create_new_feature.py::TestCreateNewFeature` (explicit opt-out fixture; branch, paths, requirements, and supported arguments) |
| S028 | `tests/scripts/bash/test_create_new_feature.py::test_s028_missing_helper_never_falls_back_to_main` |
| S029 | `tests/test_worktrees_template.py::test_s029_powershell_checks_setting_before_mutation` |
| S030 | `tests/test_worktrees_template.py::test_s030_all_commands_include_routing` |
| S031 | `tests/test_worktrees_template.py::test_s031_s032_s033_common_contract_has_exceptions_and_provenance` |
| S032 | `tests/test_worktrees_template.py::test_s031_s032_s033_common_contract_has_exceptions_and_provenance` |
| S033 | `tests/test_worktrees_template.py::test_s031_s032_s033_common_contract_has_exceptions_and_provenance` |
| S034 | `tests/test_package_contents.py::test_s034_installed_worktree_runtime_and_templates` |
| S035 | `tests/test_worktrees_cli.py::test_s035_end_to_end_shared_parent_and_retained_feature` |

## Local Verification

- Full pytest baseline before final review: 1822 passed, 54 skipped, including interrupted-creation recovery and boundary regressions.
- Built wheel and sdist inspections plus independent installed-runtime tests: 18 passed.
- Ruff lint/format, mypy, shellcheck, bandit, strict MkDocs build, Markdown lint, and
  command distribution checks passed.
- No PowerShell interpreter is available locally. Cross-platform execution remains a CI responsibility.
- The initial Conda Python environment crashed importing native `readline` before collection;
  recreating this worktree's development environment with uv-managed Python 3.11 resolved it.
  No source change or runtime pin was used to conceal that environmental failure.

## Additional Boundary Regressions

- Configuration preservation: `test_worktree_setting_preserves_yaml_aliases_and_document_boundaries`
  asserts scalar and mapping aliases, unrelated values, comments, and explicit YAML document ends.
- Workspace identity: `test_stale_worktree_registration_cannot_adopt_replacement` rejects missing,
  ordinary replacement, and foreign-repository directories through both create and resolve.
- Secondary writes: `test_language_routing_includes_command_frontmatter` checks both language setters
  update destination commands while preserving the source checkout.
- Containment: `test_config_rejects_destination_symlinks` checks every config setter with both a
  directory link and final-file link; `test_routed_frontmatter_rejects_symlink_targets_before_any_write`
  covers command-directory and command-file links before any configuration write.
- Artifact entry points: `test_feature_entry_points_reject_redirected_artifact_paths` checks all
  four artifact path boundaries through create, resolve, and finish. The companion
  `test_feature_entry_points_reject_hardlinked_requirements` rejects shared requirement-file inodes.
- Shared file inodes: `test_routed_config_rejects_hardlinks_before_writing` covers every configuration
  setter; `test_routed_frontmatter_rejects_hardlinks_before_any_write` covers both command-description
  setters and verifies that neither source nor destination configuration changes on rejection.

These regressions are part of S002, S010, S021, S022, and S025, respectively. The worktree and CLI
suite passes all 95 cases after these checks were added.

## Final Review

The third isolated complete-feature review returned a valid schema-v2 **PASS** with zero P0–P3
findings, seven complete contracts, eight complete review partitions, and a completed independent
filesystem risk specialist. Both received follow-up obligations were verified; no open obligations
or blocking coverage gaps remain. The only coverage limitation is native PowerShell/Windows execution.

The first two reviews identified six independently reproduced defects: secondary writes using the
source working directory, stale worktree registrations, redirected configuration paths, YAML alias
and document-boundary preservation, redirected continuation artifacts, and shared file inodes.
Regression tests cover each repair. No finding was refuted or waived. All 35 planned scenarios
have asserting coverage, and the final reviewer independently repeated the 1822-test baseline and
18 package checks successfully.

The reviewed 148-file target fingerprint was
`sha256:1b74bef011a6a4feb65fb5da534350d2c430fadaf269e0e080fe3ca4dbc8a954`.
Before the initial feature commit, only task completion bookkeeping and this final verification
record changed after that gate. The CI follow-up below changes test infrastructure and is outside
that original review fingerprint; feature runtime, templates, generated copies, and user
documentation retain the reviewed bytes.

## CI Follow-up Verification

The initial PR CI exposed a bare-remote fixture without a local commit identity. The fixture now
sets its own identity, and the entire pytest suite disables inherited and inferred Git identities.
Two regression tests failed before this repair and pass afterward, including a bare repository's
attached worktree committing successfully.

Historical PR CI logs also exposed an unfixed cleanup race: a Git maintenance lock can disappear
before chmod or before the removal retry. Both cases now pass deterministic regressions, while
real permission failures remain visible. The evaluation module passes all 32 cases.

A fresh Linux/Python 3.12 container exposed a separate test prerequisite: same-size writes can
retain identical timestamps. The fragment test now explicitly advances mtime and asserts signature
drift; the implementation's rejection contract is unchanged. All 119 fragment tests pass locally
with one platform skip.

Local full-suite validation after Git-identity and cleanup repairs passed 1827 tests with 54 skips;
all pre-commit gates passed. The final timestamp-fixture adjustment also passed its complete module
and the full hook-run suite. A fresh Linux/Python 3.12 container with pip-installed development
dependencies passed all 1827 tests with 54 skips after that adjustment.
CI runs lint and all six OS/Python combinations independently; package building requires both lint
and the entire test matrix to pass. Native platform results remain required before merging.

The plain Git commit hook additionally exposed a mixed-environment PATH: pytest used the selected
virtual environment while Bash tests found an older globally installed CodexSpec. The test launcher
now prepends the selected interpreter's scripts directory for child commands. A nested pytest probe
outside the repository reproduces the missing PATH entry and verifies the correct CLI is selected.
