# Tasks: Specs Context Recall

## Shared Guidance and Context Installation

- [x] **T-001**: Deliver the shared specs guidance and non-destructive installation into Claude/Codex project context.
  - **Covers**: REQ-001, REQ-002, REQ-003, REQ-004, REQ-005, REQ-006, REQ-007, REQ-008, NFR-001; **Plan**: P1.
  - **Paths**: `src/codexspec/specs_context.py`, `src/codexspec/__init__.py`, `src/codexspec/integrations/codex.py`, `tests/test_specs_context.py`.
  - **Dependencies**: None.
  - **Outcome**: Fresh and repeated init deliver the same complete bounded policy in selected integrations without damaging authored context or other managed blocks.
  - **Verification**: Write failing Python tests, observe failure, implement, then run focused pytest.
  - **Test Scenarios**:
    - T-001-S1: claude, codex, and both install the rule into exactly the selected context surfaces.
    - T-001-S2: repeated init produces one specs block and preserves user prose and other managed blocks.
    - T-001-S3: updating an existing specs block preserves its surrounding text, including backslashes.
    - T-001-S4: the rendered policy carries the timeline, confirmed-authority, current-user-decision, scenario-depth, ambiguity, stopping, reuse, and mechanical-edit rules without embedded historical records.

## Plugin Delivery

- [x] **T-002**: Extend plugin startup output with the same specs policy while retaining commit guidance and CLI-free execution.
  - **Covers**: REQ-001, REQ-002, REQ-003, REQ-004, REQ-005, REQ-006, REQ-007, REQ-008, NFR-001; **Plan**: P2.
  - **Paths**: `src/codexspec/commit_guidance.py`, `tests/test_plugin_commit_guidance.py`; generated plugin hook through installation.
  - **Dependencies**: T-001.
  - **Outcome**: Startup emits both guidance blocks and leaves the host project untouched.
  - **Verification**: Extend failing expectations first; implement composition and regenerate the hook through the existing installer.
  - **Test Scenarios**:
    - T-002-S1: a freshly installed command tree emits both exact blocks without a CodexSpec CLI from repository and non-repository working directories.
    - T-002-S2: the marketplace plugin tree provides the same output from a path containing spaces, quotes, and a dollar sign.
    - T-002-S3: startup preserves host files, HEAD, and staging; linked hook destinations remain rejected by existing tests.

## Workflow and Distribution

- [x] **T-003**: Deliver workflow reminders and user documentation, regenerating all affected artifacts normally.
  - **Covers**: REQ-001, REQ-004, REQ-005, REQ-006, REQ-008, NFR-001; **Plan**: P3.
  - **Paths**: `internal/command_templates/fragments/specs-recall.md`; the 15 source commands in design C3; generated `templates/commands/`, `.claude/commands/codexspec/`, `.agents/skills/`; installed `AGENTS.md`/`CLAUDE.md`; `docs/en/user-guide/workflow.md`.
  - **Dependencies**: T-001, T-002.
  - **Outcome**: Substantive command entries reinforce recall without changing selected authority or input/write boundaries; user documentation explains its behavior.
  - **Verification**: Source/template contract checks; renderer write then check; feature-local init for both integrations; inspect generated diffs. Documentation/configuration task: no artificial TDD requirement.

## Verification and Review

- [x] **T-004**: Verify packaged delivery and document decision-scenario outcomes.
  - **Covers**: REQ-001, REQ-002, REQ-003, REQ-004, REQ-005, REQ-006, REQ-007, REQ-008, NFR-001; **Plan**: P4.
  - **Paths**: `tests/test_package_contents.py`, `tests/test_specs_context.py`, feature-local `verification.md`.
  - **Dependencies**: T-003.
  - **Outcome**: Package contents include the new module and complete templates; semantic scenarios demonstrate what the installed policy prescribes, with no unsupported claim of measured agent effectiveness.
  - **Verification**: Build wheel/sdist, run package tests, directly reason through design scenarios against emitted policy, and map outcomes to the scenario IDs below.
  - **Test Scenarios**:
    - T-004-S1: both archive types contain the runtime module and complete, source-matching templates, with maintainer fragments excluded.
    - T-004-S2: old unchanged requirement plus unrelated later feature retains the old requirement.
    - T-004-S3: later addition combines with existing requirements.
    - T-004-S4: later explicit change updates the same matter while preserving earlier rationale and unrelated requirements.
    - T-004-S5: latest user decision overrides history without re-questioning the same choice.
    - T-004-S6: an unclear decision relationship leads to a specific clarification instead of invented expiration.
    - T-004-S7: debugging distinguishes an intended plan from actual implementation evidence.
    - T-004-S8: sufficient background is reused; new scope, evidence, or insufficient support triggers supplemental retrieval.
    - T-004-S9: mechanical edits may skip recall; empty or incomplete history cannot manufacture decisions.
  - S2-S9 each map to a policy-contract test asserting the required and forbidden interpretation in the emitted instructions, plus direct semantic reasoning in the verification record. They are not automated LLM measurements; report that distinction.

- [x] **T-005**: Complete repository quality gates and prepare the stable implementation-review target.
  - **Covers**: REQ-001, REQ-002, REQ-003, REQ-004, REQ-005, REQ-006, REQ-007, REQ-008, NFR-001; **Plan**: P4.
  - **Paths**: feature-local verification/review records; fixes only in the feature's authorized source and generated paths.
  - **Dependencies**: T-004.
  - **Outcome**: Stable diff with focused/full tests, lint/format, distribution check, strict docs build, and package inspection complete. The implement-tasks final defect gate reviews this target after the checkpoint; its result is recorded outside the repository.
  - **Verification**: Use the workspace's own Python environment and external pytest temporary roots; preserve hooks. Record exact outcomes. This is a verification checkpoint, not a new runtime behavior task.

## Dependencies

T-001 → T-002 → T-003 → T-004 → T-005. No concurrent task markers: these tasks
share installation and generated artifacts. Python changes use the plan's TDD
ordering; prose, documentation, and generated files use direct deterministic checks.

## Coverage

| Plan / Requirement | Tasks | Scenarios |
|---|---|---|
| P1 / REQ-001..REQ-008, NFR-001 | T-001 | T-001-S1..S4 |
| P2 / REQ-001..REQ-008, NFR-001 | T-002 | T-002-S1..S3 |
| P3 / REQ-001, REQ-004..REQ-006, REQ-008, NFR-001 | T-003 | Source/render/install consistency |
| P4 / REQ-001..REQ-008, NFR-001 | T-004, T-005 | T-004-S1..S9 and repository gates |

No unmapped tasks or unresolved implementation decisions.
