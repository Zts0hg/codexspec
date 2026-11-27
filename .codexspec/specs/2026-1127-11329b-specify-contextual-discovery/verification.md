# Verification: Context-Aware Requirement Discovery

**Feature**: 2026-1127-11329b
**Date**: 2026-11-27
**Scope**: Current generic-premise correction pre-review baseline, with initial baseline history retained below. Final independent review records live outside the repository.

## Delivered Changes

- internal/command_templates/sources/specify.md: preparation before questions; autonomous factual investigation; automation-aware clarification; enabled-mode completion condition.
- templates/commands/specify.md: generated complete distribution template.
- .claude/commands/codexspec/specify.md: generated Claude command.
- .agents/skills/codexspec-specify/SKILL.md: generated Codex skill.
- tests/test_sdd_workflow_templates.py: ten scenario contracts parameterized across all three delivered forms.

Git scope inspection confirms these five implementation files plus this feature's SDD artifacts. Other command sources, shared fragments, runtime code, configuration, registration, and frontmatter descriptions have no changes.

## Environment and Provenance

- macOS, CPython 3.11.13, pytest 9.0.2.
- Environment prepared with uv sync --extra dev --python 3.11.
- The selected interpreter and codexspec import resolve inside this feature workspace.
- Commands below run from this feature workspace with uv's matching CLI PATH.
- Skipped tests are not claimed as executed; this local run does not claim a remote operating-system/Python matrix result.

## Red-Green Evidence

The implementer ran the following before changing the authored instructions:

    uv run --extra dev pytest tests/test_sdd_workflow_templates.py -k 'specify and not creates' -q --tb=short

Observed exit 1: 30 failed, 2 passed, 62 deselected in 0.64s. All thirty new cases failed because the preparation or automation-mode instruction section was absent. The original red/green output was observed in tool results; no separate raw red log file was created.

After source edits and regeneration:

    uv run --extra dev pytest tests/test_sdd_workflow_templates.py tests/test_profile_templates.py tests/test_worktrees_template.py tests/test_command_template_fragments.py -q --tb=short

Observed exit 0: 220 passed, 1 skipped in 0.80s.

## Initial Complete Baseline Before the Generic-Premise Correction

    uv run --extra dev pytest -q

Observed exit 0: 2644 passed, 60 skipped in 1735.89 seconds. The thirty new delivered-form cases pass within this complete suite. The source and test files remained stable throughout the complete run; later feature-document edits only complete verification evidence and task bookkeeping.

## Deterministic Checks

| Check | Result |
|---|---|
| uv run --extra dev ruff check tests/test_sdd_workflow_templates.py | PASS; all checks passed |
| uv run --extra dev ruff format --check tests/test_sdd_workflow_templates.py | PASS; already formatted |
| uv run --extra dev python internal/command_template_fragments.py --check-distribution --root <workspace> | PASS; exit 0 |
| npm exec --offline --package=markdownlint-cli@0.42.0 -- markdownlint <changed command and feature Markdown files> | PASS; exit 0 |
| git diff --check | PASS; exit 0 |
| UTF-8/LF, final newline, trailing whitespace, local feature hyperlinks | PASS |

The final Markdown/whitespace checks cover the completed verification and task records before freezing the feature for review. Potential generation destinations were checked for real containment, symlink components, and multiple hard links before generation. The generation snapshot confirmed other delivered files retained their bytes.

## Scenario Self-Check

The complete TS-001 through TS-010 mapping is recorded in tasks.md. Each named test contains assertions of the corresponding obligation and is parameterized over template, Claude, and Codex forms. No listed scenario lacks a covering test.

Instruction walkthroughs supplement the contract tests:

| Specification Scenario | Inspected Instruction Outcome |
|---|---|
| Question premises and inspection conclusions | Verify relevant functionality/relationships first; only then classify content (including an inspected frontend placeholder) or present a verified material relationship for user choice. |
| Accessible fact versus unavailable or contradictory evidence | Collect accessible facts autonomously; state a necessary remaining gap without declaring absence or inferring intent. |
| A choice blocks design but not specification | Enabled-mode guidance resolves it during discovery and Completion prevents deferral as non-blocking; equivalent implementation choices remain autonomous. |
| Intermediate confirmation and a later unforeseen decision | Intermediate confirmation cannot advance; final confirmation retains one successor invocation; later material decisions retain stop-and-ask behavior. |

These are static instruction-contract tests and source walkthroughs, not a live-model conversation evaluation. They verify the shipped contract and generation fidelity without claiming universal model compliance.

## Final Gate

After this baseline and completed task bookkeeping are frozen, the implement-tasks complete-feature defect gate evaluates the complete selected target in a fresh isolated context. Its schema-v3 envelope, maintenance companion, inventory, and final verdict are retained in the repository's external review state store.

## Generic-Premise Correction and Complete-Diff Semantic Audit

The user identified that the frontend/backend-specific sentence narrowed a general requirement and could preclassify a placeholder before inspection. The authoring source and all three generated forms now verify any premise determining a question or option, retain unknown premises as unknown, and classify implementation status only after inspection.

Updated TS-002 is test_specify_verifies_question_premises_before_classifying_functionality. Its new assertions first failed in all three delivered forms (3 failed, 91 deselected), then passed (3 passed, 91 deselected). The refreshed focused suite passes 220 tests with 1 skipped; exact distribution, Ruff lint/format, command Markdown and diff checks pass.

A separate read-only semantic audit inspected all five implementation files and all ten feature artifacts against the confirmed requirements and relevant historical recall decisions. It checked example-to-rule overfitting, unverified existence/status/relationship/impact assumptions, conclusions used as preconditions, overly narrow source lists or mandatory tool rituals, and factual evidence replacing user intent. No additional substantive defect was found. Explicit frontend examples remain conditional on inspection establishing their facts. The audit does not replace the final complete-feature defect gate.

Refreshed complete verification collects the whole configured suite once, then runs four disjoint groups of collected test files with separate external fixture directories. Completion requires the union of shard node IDs and collection-skip modules to match the original collection exactly, with no duplicates or omissions. The completed aggregate is 2644 passed/60 skipped, with zero failures or errors. All 2703 collected test node IDs and the one collection-skip module match exactly, with no duplicate or omitted node. The earlier single-process run applies to its original target; this refreshed complete collection applies to the corrected target.

## Refreshed Complete-Suite Results

| Disjoint Group | Passed | Skipped | Failed / Errors |
|---|---|---|---|
| 0 | 667 | 10 | 0 / 0 |
| 1 | 671 | 5 | 0 / 0 |
| 2 | 660 | 16 | 0 / 0 |
| 3 | 646 | 29 | 0 / 0 |
| Aggregate | 2644 | 60 | 0 / 0 |

Whole-suite collection produces 2703 executable node IDs and one collection-level skip across 95 files. The four file groups are disjoint; an exact Counter comparison of all collected node IDs and collection-skip modules succeeds. Each group exits 0 with isolated fixture storage outside the checkout. Skipped coverage is not claimed as executed.

Raw collect/group manifests, the verification runner, four test logs, per-group counts, and log SHA-256 digests are retained under /Users/xiaoming/.cache/codexspec/review/797fd308835574ea54a57974956066b8573c8b3d70922981ed7081842e60bc75/loops/2026-1127-11329b-generic-premises; aggregate.json contains the exact coverage comparison. Reproduction uses the same selected .venv and PYTHONPATH with run_suite.py collect, then run_suite.py shard-0 through shard-3. This partitioning changes test scheduling, not suite membership or assertions.

The corrected instructions are verified through static contracts, source walkthroughs, and exact distribution consistency. No live-model conversation evaluation is claimed.
