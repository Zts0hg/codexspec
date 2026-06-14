# Feature Name Validation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reject feature creation before side effects when the normalized short name contains no ASCII alphanumeric characters, and document the timestamp-only resolution contract.

**Architecture:** Keep normalization in each platform creation script and validate its result immediately. Use behavior tests for Bash and PowerShell plus a shared contract test for documentation and resolver intent.

**Tech Stack:** Bash, PowerShell, pytest, Markdown

---

## Task 1: Add Failing Regression Tests

**Files:**

- Modify: `tests/scripts/bash/test_create_new_feature.py`
- Modify: `tests/scripts/powershell/test_create_new_feature.py`
- Modify: `tests/test_sdd_workflow_templates.py`

- [ ] Add a Bash test that passes a CJK-only name and asserts non-zero exit, ASCII guidance, and no feature directory.
- [ ] Add an equivalent PowerShell test using `-ShortName`.
- [ ] Add contract assertions for timestamp-only naming, artifact-only legacy compatibility, and full-name workspace identity.
- [ ] Run the focused tests and confirm they fail for the missing behavior and documentation.

## Task 2: Implement Early Validation

**Files:**

- Modify: `scripts/bash/create-new-feature.sh`
- Modify: `scripts/powershell/create-new-feature.ps1`

- [ ] Normalize the Bash suffix before generating an ID and reject an empty result with ASCII guidance.
- [ ] Validate the PowerShell suffix before creating `.codexspec/specs` or generating an ID.
- [ ] Run the focused creation tests and confirm they pass.

## Task 3: Publish the Resolution Contract

**Files:**

- Modify: `scripts/bash/common.sh`
- Modify: `scripts/bash/check-prerequisites.sh`
- Modify: `scripts/powershell/common.ps1`
- Modify: `docs/en/development/scripts-architecture.md`

- [ ] Add concise comments stating that only timestamp feature names are supported.
- [ ] Document that legacy compatibility concerns artifacts, not directory naming.
- [ ] Document that full feature names identify workspaces and short-ID lookup rejects ambiguity.
- [ ] Run contract and script tests.

## Task 4: Verify

- [ ] Run Bash syntax checks.
- [ ] Run all Bash script tests and shared workflow-template tests.
- [ ] Run PowerShell tests when `pwsh` and the platform test conditions permit.
- [ ] Run `git diff --check` and inspect the final diff.
