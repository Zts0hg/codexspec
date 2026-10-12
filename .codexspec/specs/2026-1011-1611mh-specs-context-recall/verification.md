# Specs Context Recall: Verification

## Scope and Method

This feature delivers agent instructions through project context, command
templates, and plugin startup. The checks below distinguish deterministic
installation/policy tests from direct interpretation of the policy. They do not
measure an autonomous agent's recall rate or prove compliance in every session.

## Deterministic Checks

- Red baseline: `tests/test_specs_context.py` and
  `tests/test_plugin_commit_guidance.py` produced 32 expected failures and 3 passes
  before the new module, installation wiring, reminders, and combined startup
  output existed.
- Focused green baseline: specs context, plugin guidance, existing profile init,
  and profile tests: 55 passed.
- Wheel/sdist build and archive/installed-wheel checks: 18 passed, including the
  new runtime module, exact template contents, no internal authoring files, and
  matching guidance in both contexts of a wheel-initialized project.
- `internal/command_template_fragments.py --check-distribution`: passed after
  normal rendering and feature-local `codexspec init . --force --ai both`.
- Strict MkDocs build: passed with output outside the repository.
- Full repository pre-commit verification: passed, including the complete pytest suite, Ruff, formatting, mypy, Bandit, Markdown/YAML/shell checks, and pip-audit. No hooks were bypassed.

The first full hook attempt found a low-confidence SQL-pattern false positive in
an interpolated prose literal and applied Markdown formatting. That superseded
test attempt was interrupted; it is not counted as a successful full-suite run.
The guidance now joins a static literal with its markers, retaining its semantics,
and includes the required Markdown spacing. The subsequent complete hook run passed without bypasses. A final focused context/plugin run also passed all 35 cases.

## Scenario-to-Test Mapping

| Task scenario | Executed test / evidence |
|---|---|
| T-001-S1, T-001-S2 | `test_t001_s1_s2_init_installs_once_and_preserves_project_content` for claude, codex, both |
| T-001-S3 | `test_t001_s3_replace_only_own_block_and_preserve_backslashes` |
| T-001-S4 | `test_t001_s4_fresh_context_is_bounded_and_complete` |
| T-002-S1, T-002-S2, T-002-S3 | `test_session_start_emits_commit_rule_without_cli`, all four installation/repository combinations; existing linked-destination tests |
| T-003 consistency | `test_workflow_reminder_preserves_current_authority_and_scope`, all 15 commands; distribution check |
| T-004-S1 | `test_built_archives_contain_resolvers_and_all_current_command_templates`, `test_s034_installed_worktree_runtime_and_templates` |
| T-004-S2 through T-004-S9 | `test_history_scenario_policy_contract`, individually parameterized by task scenario |

## Direct Semantic Scenario Checks

The following are constructed decision cases checked against the emitted policy,
not transcripts of a separate agent being asked to perform each task.

| Scenario | Input situation | Required interpretation and policy result |
|---|---|---|
| T-004-S2 | January confirms retaining an API; March adds an unrelated UI feature | Retain the API requirement. The policy explicitly retains older unchanged requirements and rejects replacement by an unrelated later feature. |
| T-004-S3 | January confirms authentication; March adds a session timeout | Apply both. The policy combines later additions with earlier requirements. |
| T-004-S4 | January chooses one export format; March explicitly changes that format | Apply March's change to that matter, retaining the earlier rationale and unaffected requirements. The policy states all three parts. |
| T-004-S5 | The current user explicitly chooses a different format again | Apply the user's latest explicit decision and explain implications without asking the same choice again. Both constraints are present. |
| T-004-S6 | Two confirmed records differ without a clear replacement relationship | Explain the exact difference and ask a concise question; do not assume expiry. The policy explicitly requires this. |
| T-004-S7 | An old plan promises retries, but current code has none | Inspect actual design/code/test evidence; the plan alone cannot establish implementation or a later user decision. The policy distinguishes these sources. |
| T-004-S8 | A task moves from design to planning with sufficient background, then adds a new integration | Reuse the background for the unchanged transition and supplement it for new scope. Scope, evidence, and insufficiency are explicit triggers. |
| T-004-S9 | A spelling fix, or a substantive task with incomplete legacy artifacts | A mechanical edit may omit recall; missing history does not establish a user decision. Material uncertainty remains eligible for targeted questioning. |

## Review Handoff

The final implementation defect review runs after the repository baseline is green.
Its manifest, target fingerprint, inventory, coverage, result, and verification
logs belong in the external review state store prescribed by review-code. This
file records implementation verification, not the final review verdict.
