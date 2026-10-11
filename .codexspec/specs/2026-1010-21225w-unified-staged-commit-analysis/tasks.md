# Tasks: Unified Staged Commit Analysis

Code tasks use red-green verification. Mark complete only after the listed
scenarios have meaningful assertions and relevant regressions pass. All paths
are relative to the selected feature worktree.

## Phase 1: Shared staged-content support

- [x] **T01: Implement prepared indexes and content identity.** Add
  src/codexspec/staged_commits.py and tests/test_staged_commits.py; extend the
  existing GitRunner as needed for explicit indexes. Outcome: real prepared
  indexes preserve caller state and can be validated against their preparation.
  **Covers**: REQ-003, REQ-005, REQ-006; **Plan**: Phase 1. Dependencies: none.

  **Test Scenarios**:
  - S01: Selected feature changes produce the expected tree while unrelated
    staged content remains unchanged in the ordinary index.
  - S02: A blueprint proposal can be staged without publishing its working file.
  - S03: Changed HEAD, changed prepared tree, malformed or foreign preparation,
    and empty changes are rejected without a commit.
  - S04: Selected deletion and rename content matches the prepared tree.

- [x] **T02: Implement guarded full-message commit execution.** Extend shared
  support and its tests. Outcome: direct and helper execution preserve the
  analyzed tree, messages, and original hook behavior.
  **Covers**: REQ-002, REQ-003, REQ-005, REQ-006; **Plan**: Phase 1.
  Dependencies: T01.

  **Test Scenarios**:
  - S05: A multiline message is retained and the resulting tree equals analysis.
  - S06: Direct execution respects partial staging and supports an unborn HEAD.
  - S07: Original hooks run with expected arguments, including custom hooksPath;
    a failed hook creates no successful commit result.
  - S08: A successful hook that changes staging is detected before committing;
    retry requires reanalysis and never silently includes working-tree fixes.
  - S09: Ordinary index and unrelated staged content survive path-limited commits.

## Phase 2: Helper workflows

- [x] **T03: Migrate feature commits to prepare/analyze/finalize.** Update
  src/codexspec/automation.py and tests/test_auto_dev_git.py.
  **Covers**: REQ-002, REQ-003, REQ-004, REQ-005, REQ-006; **Plan**: Phase 2.
  Dependencies: T02.

  **Test Scenarios**:
  - S10: Valid analyzed feature content commits with its feature scope and body.
  - S11: Wrong or lost ownership, forbidden blueprint paths, and stale analysis
    fail without bypassing existing protections.

- [x] **T04: Migrate blueprint commits to prepare/analyze/finalize.** Update
  src/codexspec/automation.py and tests/test_blueprint_store.py.
  **Covers**: REQ-002, REQ-003, REQ-004, REQ-005, REQ-006; **Plan**: Phase 2.
  Dependencies: T02.

  **Test Scenarios**:
  - S12: Blueprint prepare leaves the published file unchanged; finalization
    applies exactly the analyzed proposal with its generated message.
  - S13: Stale hash, invalid/rejected requests, no-op operations, and ownership
    failure do not create an unanalysed commit or consume a fresh feature ID.
  - S14: Unrelated staged content survives, and interrupted finalization recovers
    through the existing journal semantics.

- [x] **T05: Wire strict machine interfaces.** Update `src/codexspec/__init__.py`,
  tests/test_blueprint_cli.py, and focused hidden-helper CLI tests.
  **Covers**: REQ-003, REQ-004, REQ-005, REQ-006; **Plan**: Phase 2.
  Dependencies: T03, T04.

  **Test Scenarios**:
  - S15: Ordinary, feature, and blueprint actions pass complete analysis metadata
    and full messages through to the guarded executor.
  - S16: Missing analysis, legacy payloads, invalid field types, and foreign
    preparation identifiers fail explicitly; discard touches only owned state.

## Phase 3: Instructions and integration entry points

- [x] **T06: Install proactive commit instructions on both integrations.** Add
  bounded context injection and wire Codex/Claude installation; extend
  tests/test_codex_integration.py and relevant tests/test_cli.py cases.
  **Covers**: REQ-001, REQ-004; **Plan**: Phase 3. Dependencies: T05.

  **Test Scenarios**:
  - S17: Fresh Claude and Codex installs include correct invocation spelling and
    a commit trigger that covers conversation and SDD work.
  - S18: Reinstallation updates existing custom context files idempotently while
    preserving unrelated content, including backslashes.

- [x] **T07: Connect command templates to staged analysis.** Edit only authoring
  sources under internal/command_templates/sources/ for commit-staged,
  implement-tasks, auto-dev, and blueprint; sweep other commit sites. Update
  tests/test_auto_dev_template.py, tests/test_blueprint_template.py and focused
  commit-staged workflow contract assertions. Outcome: shipped instructions use
  the exact implemented helper contracts and no legacy analysis bypass.
  **Covers**: REQ-001, REQ-002, REQ-003, REQ-004, REQ-005, REQ-006;
  **Plan**: Phase 3. Dependencies: T05, T06.

  **Test Scenarios**:
  - S19: Direct, feature, and blueprint instructions all invoke commit-staged;
    full-message, explicit-index, and reanalysis rules are present and consistent.
  - S20: Instructions do not let commit-staged select/stage files, reuse a stale
    hook-retry message, or fall back to fixed helper-generated descriptions.

## Phase 4: Distribution and verification

- [x] **T08: Regenerate distribution and document the final workflow.** Run the
  fragment renderer, regenerate both integrations through init in this worktree,
  and update relevant documentation. Verify --check-distribution and inspect the
  diff for unrelated edits. **Covers**: REQ-001, REQ-004, REQ-006;
  **Plan**: Phase 4. Dependencies: T07. Non-code verification task.

- [x] **T09: Complete regression, scenario, and defect gates.** Run focused and
  full pytest, ruff on changed Python, distribution checks, and the complete
  review-code gate. Map S01–S20 to concrete passing tests and resolve verified
  findings before marking complete. **Covers**: REQ-001, REQ-002, REQ-003,
  REQ-004, REQ-005, REQ-006; **Plan**: Phase 4. Dependencies: T08.
  Verification task; it verifies existing scenarios instead of inventing new ones.

## Coverage

| Plan Component | Requirements | Tasks | Scenarios |
|----------------|--------------|-------|-----------|
| Phase 1 | REQ-002, REQ-003, REQ-005, REQ-006 | T01, T02 | S01–S09 |
| Phase 2 | REQ-002–REQ-006 | T03, T04, T05 | S10–S16 |
| Phase 3 | REQ-001–REQ-006 | T06, T07 | S17–S20 |
| Phase 4 | REQ-001–REQ-006 | T08, T09 | Verifies S01–S20 and distribution |

## Dependencies and Unresolved Items

T01 -> T02 -> (T03, T04) -> T05 -> T06 -> T07 -> T08 -> T09.
T03 and T04 share automation.py and execute sequentially; no parallel marker is
assigned. No unmapped tasks or unresolved user decisions.

## Scenario Verification Record

The scenario mappings below cover the implementation and compatibility cases.
The final verification record below covers S01–S39 and the complete-feature gate.

| Scenario | Concrete tests |
|----------|----------------|
| S01 | test_preparation_preserves_unrelated_staging |
| S02 | test_blueprint_preparation_does_not_publish |
| S03 | test_preparation_rejects_changed_tree_head_and_owner; test_empty_and_foreign_preparations_are_rejected; test_preparation_rejects_foreign_workspace_and_linked_record |
| S04 | test_preparation_captures_deletion_and_rename |
| S05 | test_direct_commit_preserves_partial_staging_and_body |
| S06 | test_direct_commit_preserves_partial_staging_and_body; test_direct_initial_commit; test_direct_commit_uses_callers_explicit_index |
| S07 | test_hooks_keep_arguments_failures_and_post_commit; test_reference_transaction_hook_preserves_stdin_and_denial (three workflows) |
| S08 | test_hooks_that_stage_changes_abort_before_commit; test_hooks_keep_arguments_failures_and_post_commit |
| S09 | test_guarded_path_commit_preserves_unrelated_index |
| S10 | test_feature_commit_requires_current_staged_analysis |
| S11 | test_feature_changed_content_and_lost_owner_reject_analysis; test_commit_feature_rejects_blueprint_and_wrong_owner |
| S12 | test_blueprint_analysis_precedes_publication_and_preserves_message; test_blueprint_preparation_applies_path_clean_filter |
| S13 | test_blueprint_stale_analysis_never_publishes; test_store_returns_conflict_for_stale_request_without_commit; test_status_update_requires_current_auto_dev_token; test_noop_operation_applies_without_creating_a_commit |
| S14 | test_store_commits_only_blueprint_and_preserves_unrelated_index; test_store_recovers_replacement_interrupted_before_commit; test_store_recognizes_commit_interrupted_before_record_cleanup; test_blueprint_post_commit_failure_preserves_published_file_and_recovery |
| S15 | test_direct_snapshot_and_commit_cli; test_feature_machine_handoff_and_legacy_rejection; test_hidden_inspect_and_apply_use_machine_json |
| S16 | test_blueprint_legacy_apply_is_rejected; test_feature_machine_handoff_and_legacy_rejection; test_invalid_analysis_fields_and_discard_preserve_caller_state |
| S17 | test_commit_guidance_installed_and_updated_without_clobber (both integrations) |
| S18 | test_commit_guidance_installed_and_updated_without_clobber (both integrations) |
| S19 | test_all_commit_workflows_invoke_common_analysis; test_commit_analysis_owns_no_staging_and_requires_reanalysis |
| S20 | test_commit_analysis_owns_no_staging_and_requires_reanalysis |

Additional compatibility regressions cover custom project message formats and
preservation of a blueprint file's executable mode. Template assertions validate
instruction contracts, not empirical model obedience or semantic writing quality.

## Confirmed Installation Compatibility Repair

- [x] T10 **Preserve CLI-free commit analysis and execution.** Implement design
  Decision 5 and plan Installation Compatibility Repair. **Covers**: REQ-006;
  **Source**: DEC-001. Dependencies: T08; T09 requires T10 verification.
  S21: installed Claude/Codex and marketplace plugin helpers run without CLI or
  Python site packages; preserve partial staging, full messages and hooks.
  S22: changed staging rejects stale analysis without advancing HEAD.
  S23: project/plugin distribution and built archives contain the same runtime.

S21 is covered by test_cli_free_snapshot_commit_and_hooks (Claude, Codex,
marketplace plugin) and test_standalone_json_protocol_is_utf8_under_ascii_locale.
S22 is covered by test_standalone_helper_rejects_stale_analysis and malformed
request cases. S23 is covered by test_tracked_runtime_copies_match,
test_runtime_install_updates_and_rejects_shared_destination,
test_built_archives_contain_resolvers_and_all_current_command_templates, and
normal installation from the built wheel.

## Confirmed Merge Integration Repair

- [x] T11 **Analyze and validate merge commits at every creation entry.** Covers
  REQ-001, REQ-002, REQ-005, REQ-006 and DEC-002; implements Decision 6 and Merge
  Integration Repair. T09 requires this repair and its independent review.
  S24: clean and conflict synchronization merges wait for analysis; actual commits
  preserve the full message, analyzed tree and both parents.
  S25: history-only merges retain the default message; changed merge parents or
  hook-staged contents reject stale analysis; ordinary empty staging is rejected.
  S26: ordinary and fixed initial workspaces retain pending state until checked,
  analyzed finalization, including conflict resolution and interruption recovery.
  S27: CLI and installed command instructions carry analysis to each finalizer.
  S28: original Git hooks retain subdirectory GIT_PREFIX and refusal outcomes.

### Merge scenario coverage

| Scenario | Concrete verification |
|----------|-----------------------|
| S24 | test_sync_waits_for_analysis_before_creating_merge; test_resolved_merge_hook_cannot_change_analyzed_content; test_resolved_conflict_is_prepared_before_verification_and_commit |
| S25 | test_empty_merge_snapshot_binds_parents_and_uses_default_message; test_sync_rejects_analyzed_merge_with_replaced_target; test_resolved_merge_hook_cannot_change_analyzed_content |
| S26 | test_initial_workspace_merge_waits_for_staged_analysis (ordinary/fixed, clean/conflict); test_initial_merge_failure_retains_journal_and_can_retry; test_s019_interrupted_merge_keeps_verification_obligation |
| S27 | test_initial_merge_cli_retains_workspace_and_releases_owner; test_sync_cli_requires_analysis_and_preserves_pending_on_refusal; test_s020_finish_cli; command distribution checks |
| S28 | test_hook_prefix_refusal_matches_git_from_subdirectory (six cases) |

### Native merge hook verification

S29: automatic synchronization and ordinary/fixed initial merges invoke
`pre-merge-commit`; conflict-resolution commits retain `pre-commit`. Hook
refusal retains pending state, staged mutations invalidate analysis, and a
pre-merge hook delegating to pre-commit invokes each once. Tests in
`tests/test_merge_hooks.py` cover these outcomes, including history-only merges
and ownership recovery. This preserves REQ-006 under T02/T11. Six regressions
failed before the repair; the initial focused repair run passed 43 tests.

S30: automatic merges preserve the complete native hook sequence, the `merge`
message source, MERGE_MSG arguments, message edits by hooks, and `post-merge 0`
completion. Source- or path-based refusal leaves HEAD unchanged and the merge
pending. The full-lifecycle test covers three entry points, contentful/history-
only merges, and both message hook phases. A conflict-resolution control retains
normal commit hooks. Before repair, 21 of 24 automatic-merge cases failed; the
three history-only source-refusal controls passed. This extends T02/T11 coverage
of REQ-006.

S30 is covered by `test_automatic_merge_preserves_full_hook_lifecycle` (24 cases),
`test_conflict_resolution_keeps_native_pre_commit_hook`, and
`test_automatic_merge_preserves_reflog_action` (native/caller-supplied environment
controls). The default-action control failed before restoring the merge
environment; both environment controls now pass.

S31: `test_automatic_merge_completion_keeps_native_environment` compares native
Git with each of the three automatic merge callers, contentful/history-only
trees, and caller-specified/default editors (12 cases). Post-merge editor actions
and post-merge/reference-transaction index context match native behavior.

S32: `test_session_start_emits_commit_rule_without_cli` executes the marketplace
and freshly installed SessionStart hook in repositories and plain directories.
The exact shared rule is emitted, the commit-staged command is discoverable, no
CLI is available, and project/index/HEAD bytes remain unchanged. Linked and
hardlinked hook outputs are refused. Seven regressions initially failed and
158 related tests passed with one platform skip after implementation. This
completes T01/T08/T10 coverage of NEED-001, REQ-001 and DEC-001.

S33: `test_hook_glob_policy_matches_native_git` compares native and guarded
direct, standalone and automatic-merge execution at all three pre-creation
hook phases. Both successful unchanged-tree wildcard staging and rejection of
forbidden staged content must match; refusal keeps HEAD and the analyzed index
unchanged (18 cases). Helper-selected paths remain literal.

S34: `test_automatic_merge_hook_environment_matches_native_git` compares every
GIT_* variable across five hook phases with absent/explicit caller author
values. It normalizes equivalent index paths and excludes wrapper-only config
plumbing, then asserts exact environment and foreign-repository author identity.
Both cases initially failed, alongside all 18 S33 cases. These scenarios extend
T02/T11 coverage of REQ-006.

S35: `test_current_repository_hook_configuration_is_preserved` compares native
Git and direct/imported or installed standalone execution with both environment
configuration formats, all three pre-creation hooks, and acceptance/refusal
(24 cases). Hooks must run and observe their configured policy; refusal leaves
HEAD and the staged tree unchanged.

S36: `test_current_repository_signing_configuration_is_preserved` confirms that
both runtime forms invoke the environment-configured signer and retain HEAD
when signing fails (four cases). S37:
`test_foreign_repository_runner_still_clears_caller_configuration` confirms that
foreign-repository runners still ignore caller-local configuration (two cases).
These scenarios extend T02/T10 coverage of REQ-006. Native-control fixture checks
use Git's quoted parameter format, staged-tree identity rather than index cache
bytes, and an explicit signer invocation marker. Against the prior runtime,
28 configuration cases failed and the two isolation controls passed; all 30
pass with the current runtime.

S38: `test_merge_options_match_native_finalization` compares native Git with
synchronization and ordinary/fixed initial-workspace finalization for contentful
and history-only merges. The 24 cases assert required signing, selected key,
explicitly disabled signing, signoff, retained pending state on refusal, and
unchanged analyzed trees and parents.

S39: `test_merge_option_parsing_matches_git` exercises native option ordering,
negation, short bundles, long abbreviations, quoted keys and option-looking
message/strategy values. `test_manual_merge_commit_does_not_inherit_merge_options`
retains normal manual-commit behavior. These 11 cases extend T02/T11 coverage
of CON-002 and REQ-006.

## Verification Before Remote CI

The implementation at the initial feature commit passed **2211 tests, with 54 skipped**. Ruff
lint/format, mypy, Bandit, Markdown lint, distribution consistency, strict MkDocs
and diff whitespace checks passed. Wheel/sdist verification passed 18 tests.
These are local macOS results; native Windows/Linux execution is not claimed.
A fresh isolated complete-feature primary review and command/process execution
specialist review passed with no admitted defects or unresolved follow-up.
The reviewed implementation fingerprint is `sha256:e6094e50a83d18df8b654ab01a2822031be2d68bc6faabf53cab2978b4edfeac`.
At that point only this task-completion record changed after review. The
subsequent CI correction below changes the runtime and installation artifacts;
the earlier fingerprint and isolated reviews describe the pre-correction state.
Empirical agent adherence remains an unexecuted evidence limit.

## Windows CI Correction

CI run 38104143348 passed lint and both Python versions on Linux/macOS, but
both Windows jobs failed the same 14 cases. Text-mode subprocess stdin changed
LF to CRLF even with explicit UTF-8, causing blueprint preparation/publication
trees to disagree. Default-codec fixture reads and text writes to MERGE_HEAD
caused the remaining failures.

S40: tests/test_git_transport.py executes real Git with emulated Windows text
transport and checks exact UTF-8 input bytes, both core.autocrlf values, and
fixture output under a non-UTF-8 locale. Four cases failed and three controls
passed before the fix; all seven pass with binary Git stdin and explicit UTF-8
fixture decoding. This extends T02/T10/T11 coverage of REQ-006. Merge fixtures
preserve Git metadata bytes, and context fixtures use explicit UTF-8/LF.

The focused verification passed 90 tests. Ruff lint/format, mypy, Bandit,
Markdown lint, distribution consistency, strict MkDocs and whitespace checks
passed. Rebuilt wheel/sdist verification passed 18 tests. The full pre-commit
suite and a fresh native CI matrix remain the gates before merging this
correction; the initial Windows failures are not treated as successful checks.
