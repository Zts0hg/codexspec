# Implementation Plan: Comprehensive English README Audit

## Context

Implement [design.md](design.md) against the confirmed requirements and spec.
The only product edit is README.md; workflow and audit records stay in this
feature directory. The worktree is `2026-1012-2306uu-readme-feature-audit`.

## Goals / Non-Goals

**Goals**: Complete the capability inventory and audit, repair and complete the
English README, verify coverage and navigability, and record real outcomes.

**Non-Goals**: Other language READMEs, reference-site rewrites, program or
template changes, and changes to historical feature records.

## Plan-Level Decisions

### Decision 1: Audit before editing and close coverage after editing

Establish current behavior and baseline coverage first, then use the completed
inventory to drive README changes. Close each row against a final README
section. This catches missing capabilities that a paragraph-only proofread misses.

Covers: REQ-001, REQ-002, REQ-003; Design: Capability inventory and audit record.

### Decision 2: Direct documentation implementation with existing verification

This feature adds no code functionality. Edit documentation directly and verify
with source/CLI-help comparisons, temporary coverage and link checks, Markdown
lint, whitespace/scope checks, and the existing suite required by the
implementation workflow. Use `uv sync --frozen --extra dev --extra docs` in this
worktree; select managed CPython rather than the known problematic Conda runtime.
Do not add tests that merely assert the wording of the edit.

Covers: REQ-004, REQ-005, NFR-001; Design: Verification evidence.

## Implementation Phases

### Phase 1: Inventory and evidence

Create audit.md with all six public CLI commands, all 28 distributed commands,
and shared integration/configuration/worktree/profile/history/review/automation
behaviors. Read current source and relevant confirmed history, then classify
baseline coverage and cite each issue.

Covers: REQ-001, REQ-002, NFR-001; Design: Capability inventory and audit record.

### Phase 2: README repair and completion

Update README.md introductions and navigation, both integration entry points,
standard/Quick/autonomous/existing-code workflows, review/debug/profile/history
behavior, Git delivery, complete command/options tables, configuration defaults,
workspace lifecycle, initialized structure, upgrade refresh, and contributor
commands. Retain the useful desktop installation guide and move misplaced
paragraphs to their relevant sections. Close audit resolutions against headings.

Covers: REQ-003, REQ-004, REQ-005, NFR-001; Design: README introduction and navigation;
Workflow and feature introductions; Configuration, workspace, and contributor reference.

### Phase 3: Verification and completion

Validate exact public command coverage, CLI option examples, Markdown links and
anchors, Markdown style, whitespace, and the product-file boundary. Run existing
required checks in this worktree and record commands/results in verification.md.
Complete tasks and use the isolated complete-feature defect review required by
implement-tasks; repair verified documentation defects with the same checks.

Covers: REQ-001, REQ-002, REQ-004, REQ-005, NFR-001; Design: Verification evidence.

## Verification Strategy

- Compare public CLI registrations and command metadata to final README tables.
- Compare defaults, invocation examples, and prose to implementation/templates.
- Check all local Markdown paths and GitHub-style heading anchors.
- Run Markdown lint on README and this feature's records; run git diff --check.
- Run the existing test suite and distribution consistency check in the selected
  worktree before final review. Do not manufacture documentation unit tests.
- Inspect the final diff: only README.md and this feature's records may change.

## Risks / Trade-offs

| Risk | Impact | Mitigation |
|------|--------|------------|
| Treating a command name as sufficient coverage | Missing usable introductions | Assess purpose, entry, defaults, and detailed-guide links |
| Copying stale references or aspirational claims | Incorrect README behavior | Prefer source and confirmed history; disclose unresolved differences |
| Excessive detail | Reader cannot find entry points | Feature introductions plus concise reference tables and links |
| Other languages remain older | Different README versions diverge | Explicit user-approved English-only scope; separate later tasks |

## Requirements Coverage

| Spec Requirement | Design Component | Plan Coverage |
|------------------|------------------|---------------|
| REQ-001 | Inventory; feature introductions; configuration | Phases 1–3 |
| REQ-002 | Inventory; verification | Phases 1 and 3 |
| REQ-003 | All README prose components | Phase 2 |
| REQ-004 | Navigation; configuration/reference; verification | Phases 2 and 3 |
| REQ-005 | Documentation boundaries; verification | All phases |
| NFR-001 | Inventory; prose; verification | All phases |
