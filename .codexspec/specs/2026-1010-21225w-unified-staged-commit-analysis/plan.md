# Implementation Plan: Unified Staged Commit Analysis

## Context

Implement [design.md](design.md) on baseline b72c0c5 using Python 3.11+, Typer,
pytest, and the existing command-fragment renderer. Confirmed intent remains in
[requirements.md](requirements.md); this plan does not change it.

## Goals / Non-Goals

Deliver proactive staged analysis for direct, feature, and blueprint commits,
including full messages and content correspondence. No additional product scope,
LLM client dependency, remote publication, or automatic merge to main is planned.

## Plan-Level Decisions

### P1: Establish Git behavior before integrating workflows

Build and test the shared staging/execution support first, then migrate helpers
and templates. This makes real Git semantics the foundation for the integration
rather than relying on template assertions alone. Code changes use the existing
implement-tasks red-green workflow; document edits use deterministic inspection.

**Covers**: REQ-003, REQ-005, REQ-006; **Design**: C, E

### P2: Update internal callers and installation artifacts together

The helper APIs are hidden machine surfaces. Migrate their templates, CLI tests,
and service tests together. Keep action validation strict and reject legacy
message-only requests instead of retaining an analysis bypass. Render opted-in
command sources and regenerate both integrations through normal installation.

**Covers**: REQ-001, REQ-004, REQ-006; **Design**: A, B, D

## Implementation Phases

### Phase 1: Shared staged-content support and guarded execution

- Add src/codexspec/staged_commits.py for prepared index records, identity
  validation, multiline messages, original-index snapshots, and guarded Git
  execution. Extend GitRunner in src/codexspec/automation.py only for explicitly
  selected indexes and execution configuration required by the design.
- Add tests/test_staged_commits.py with real temporary repositories and hook
  fixtures. Cover snapshot equality, stale content, caller-index preservation,
  invalid records, full messages, hook delegation/failure, and initial commits.
- Validate hook behavior before building workflow integration on this executor.

**Covers**: REQ-002, REQ-003, REQ-005, REQ-006; **Design**: B, C, E

### Phase 2: Helper preparation and finalization

- Extend BlueprintStore and AutoDevGit in src/codexspec/automation.py with the
  design's preparation/finalization contracts. Preserve existing ownership,
  path validation, lock ordering, blueprint operation checks and journal recovery.
- Wire hidden actions in `src/codexspec/__init__.py`, including ordinary snapshot
  and commit, preparation discard, feature prepare/commit and blueprint
  prepare/apply. Supply actionable errors for stale or invalid requests.
- Migrate tests/test_auto_dev_git.py, tests/test_blueprint_store.py,
  tests/test_blueprint_cli.py and other affected helper tests to analyzed-message
  handoffs. Keep unrelated-index and interrupted-transaction regression tests.

**Covers**: REQ-002, REQ-003, REQ-004, REQ-005, REQ-006; **Design**: C, D, E

### Phase 3: Instructions and both integration entry points

- Update internal/command_templates/sources/commit-staged.md for full messages,
  selected-index analysis, explicit original-index execution, and reanalysis
  after content changes. Caller staging replaces command-owned hook restaging.
- Update sources/implement-tasks.md, sources/auto-dev.md and sources/blueprint.md
  to invoke the common analysis and follow the migrated helper APIs. Sweep other
  distributed commit instructions for equivalent bypasses.
- Add idempotent commit guidance injection using the existing managed-block
  pattern, wired into src/codexspec/integrations/codex.py and Claude context
  installation in `src/codexspec/__init__.py`. Use callable regex replacement.
- Add meaningful install/update and workflow contract tests, including existing
  custom context files and preservation of unrelated text.

**Covers**: REQ-001, REQ-002, REQ-003, REQ-004, REQ-005, REQ-006; **Design**: A, B, D

### Phase 4: Distribution and complete-feature verification

- Render command fragments with internal/command_template_fragments.py --write;
  regenerate installed copies through init against this worktree only.
- Update affected maintainer/user workflow documentation to reflect the actual
  final interfaces. Do not edit derived commands or skills directly.
- Run focused tests, relevant automation and CLI regressions, full pytest,
  ruff on changed Python, and --check-distribution. Keep pytest fixture roots
  outside Git checkouts. Use the destination's environment and source tree.
- Run the complete-feature review-code gate and repair verified findings;
  reconcile every task scenario with actual tests before reporting completion.

**Covers**: REQ-001, REQ-002, REQ-003, REQ-004, REQ-005, REQ-006; **Design**: A–E

## Risks / Trade-offs

| Risk | Impact | Delivery treatment |
|------|--------|--------------------|
| Hook index semantics differ from assumed behavior | Analyzed tree can diverge | Real Git fixtures before integration |
| Blueprint preparation leaks uncommitted state | Transaction behavior changes | Assert no working-tree publication before finalization |
| Hidden clients retain legacy payloads | Analysis bypass or broken flows | Sweep templates and tests with API migration |
| Generated artifacts drift | Users receive inconsistent rules | Renderer and installation/distribution checks |

## Requirements Coverage

| Spec Requirement | Design Component | Plan Coverage |
|------------------|------------------|---------------|
| REQ-001 | A, B | Phases 3, 4 |
| REQ-002 | B, D | Phases 1–4 |
| REQ-003 | B, C, D, E | Phases 1–4 |
| REQ-004 | A, C, D | Phases 2–4 |
| REQ-005 | B, C, D, E | Phases 1–4 |
| REQ-006 | B, C, D, E | Phases 1–4 |

## Open Items

None. Executable checks and their outcomes are implementation deliverables, not
claims that the design has already been exercised.

## Installation Compatibility Repair

**Covers**: REQ-006; **Design**: Decision 5, components B and E; **Source**: DEC-001.

Extract the deterministic runtime without changing prepared-index ownership or
blueprint transactions. Install byte-identical complete helpers in project and
plugin artifacts, update command entry resolution, and add CLI-free real-Git
regressions before implementation. Include distribution and archive checks, then
repeat full verification and the required incremental/complete review sequence.

## Merge Integration Repair

Implement DEC-002 through the shared runtime, auto-dev synchronization, ordinary
workspace finish, and initial fixed-workspace preparation. Keep durable pending
state until checks and guarded commit succeed. Extend command routing instructions
and all generated/install copies. Verify real Git merges, conflict resolutions,
history-only merges, hook mutations, stale parents, failed checks, ownership,
recovery, and caller checkout preservation before the final defect gate.
