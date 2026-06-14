# Review Follow-up Fixes Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make implementation-stage resolution, generated requirements metadata, PowerShell output, and localized documentation consistent with the requirements-first workflow.

**Architecture:** Encode workflow invariants in shared template contract tests and platform-specific creation tests. Apply minimal edits to the command template, creation scripts, and affected localized documentation without changing unrelated workflows.

**Tech Stack:** Markdown command templates, Bash, PowerShell, pytest

---

## Task 1: Add Failing Contract Tests

**Files:**

- Modify: `tests/test_sdd_workflow_templates.py`
- Modify: `tests/scripts/bash/test_create_new_feature.py`
- Modify: `tests/scripts/powershell/test_create_new_feature.py`

- [ ] Assert `implement-tasks` uses explicit-path/current-branch resolution, rejects latest selection, and reads `requirements.md`.
- [ ] Assert six localized command guides describe `requirements.md` creation and do not claim `specify` creates no files.
- [ ] Assert six localized workflow guides include `requirements.md` as the `specify` output.
- [ ] Assert created requirements files replace feature-name and feature-ID placeholders.
- [ ] Assert PowerShell creation output omits `SPEC_FILE`.
- [ ] Run focused tests and observe failures caused by the current behavior.

## Task 2: Fix Creation Script Contracts

**Files:**

- Modify: `scripts/bash/create-new-feature.sh`
- Modify: `scripts/powershell/create-new-feature.ps1`

- [ ] Replace `[FEATURE NAME]` and `[feature-id]` after copying the requirements template.
- [ ] Add equivalent metadata to fallback requirements content.
- [ ] Remove `SPEC_FILE` from PowerShell JSON and text output.
- [ ] Run focused script and static contract tests.

## Task 3: Align Implementation Command

**Files:**

- Modify: `templates/commands/implement-tasks.md`

- [ ] Replace latest-directory auto-detection with explicit path, then current branch, then user selection.
- [ ] Load `requirements.md` before derived artifacts.
- [ ] Document legacy spec-only mode and authority order.
- [ ] Run the workflow contract test.

## Task 4: Synchronize Localized Documentation

**Files:**

- Modify: `docs/de/user-guide/commands.md`
- Modify: `docs/es/user-guide/commands.md`
- Modify: `docs/fr/user-guide/commands.md`
- Modify: `docs/ja/user-guide/commands.md`
- Modify: `docs/ko/user-guide/commands.md`
- Modify: `docs/pt-BR/user-guide/commands.md`
- Modify: `docs/de/user-guide/workflow.md`
- Modify: `docs/es/user-guide/workflow.md`
- Modify: `docs/fr/user-guide/workflow.md`
- Modify: `docs/ja/user-guide/workflow.md`
- Modify: `docs/ko/user-guide/workflow.md`
- Modify: `docs/pt-BR/user-guide/workflow.md`

- [ ] Update `specify`, `generate-spec`, and `clarify` descriptions to the requirements-first model.
- [ ] Add `requirements.md` to each workflow sequence and authority description.
- [ ] Preserve each document's existing language and command-prefix convention.
- [ ] Run localized documentation contract tests and Markdown checks.

## Task 5: Verify and Publish

- [ ] Run Bash syntax checks and focused tests.
- [ ] Run the complete pytest suite.
- [ ] Run pre-commit on all files.
- [ ] Inspect the final diff, commit, and push the PR branch.
