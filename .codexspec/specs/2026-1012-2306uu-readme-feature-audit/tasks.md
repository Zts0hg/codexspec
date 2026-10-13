# Tasks: Comprehensive English README Audit

## 1. Inventory and Evidence

- [x] T001 Inventory all six public CLI commands, 28 distributed commands, and
  shared user-facing mechanisms in audit.md; record current source behavior.
  Covers: REQ-001, NFR-001; Plan: Phase 1.
- [x] T002 Assess every inventory item's baseline README accuracy/completeness
  with source evidence, including entirely absent functionality.
  Covers: REQ-002, NFR-001; Plan: Phase 1. Depends on T001.

## 2. README Repair and Completion

- [x] T003 Complete README.md introductions and entry examples for Claude/Codex,
  standard and Quick workflows, blueprint/auto-dev, existing-code entry points,
  review/debug, project knowledge/manual review/history, and Git delivery.
  Covers: REQ-003, REQ-004, NFR-001; Plan: Phase 2. Depends on T002.
- [x] T004 Synchronize README.md navigation, six public CLI and 28 command tables,
  language/workflow/review configuration, worktree and initialized structure,
  upgrade refresh, development examples, and paragraph placement.
  Covers: REQ-003, REQ-004, REQ-005, NFR-001; Plan: Phase 2. Depends on T003.

## 3. Verification and Completion

- [x] T005 Close every audit row against a final README section and verify exact
  command coverage, important options/defaults, examples, relative links, anchors,
  and the English-only product-file boundary.
  Covers: REQ-001, REQ-002, REQ-004, REQ-005, NFR-001; Plan: Phase 3.
  Depends on T004.
- [x] T006 Run Markdown/whitespace checks, distribution consistency, and the
  existing suite in this worktree; record actual commands/results in
  verification.md. The isolated complete-feature defect review is the mandatory
  completion checkpoint below, after implementation tasks and baseline checks.
  Repair verified documentation defects and reverify as required.
  Covers: REQ-002, REQ-004, REQ-005, NFR-001; Plan: Phase 3.
  Depends on T005.

## Paths

- Product: README.md.
- Evidence: audit.md and verification.md in this feature directory.
- Workflow: requirements.md, spec.md, design.md, plan.md, tasks.md and their
  review reports in this feature directory.
- Temporary checks and external review state remain outside tracked product files.

## Dependencies and Checkpoints

T001 → T002 → T003 → T004 → T005 → T006.

- Before editing: all current inventory items have baseline assessments.
- Before review: coverage, links, scope, Markdown and required checks are green.
- Completion: valid complete-feature PASS and completed mandatory verification.

## Coverage

| Plan Item / Requirement | Task References |
|-------------------------|-----------------|
| Phase 1 | T001, T002 |
| Phase 2 | T003, T004 |
| Phase 3 | T005, T006 |
| REQ-001 | T001, T005 |
| REQ-002 | T002, T005, T006 |
| REQ-003 | T003, T004 |
| REQ-004 | T003, T004, T005, T006 |
| REQ-005 | T004, T005, T006 |
| NFR-001 | All tasks |

## Notes

All tasks are documentation work with deterministic verification. No new code
behavior or testable implementation task is introduced; no enumerated code-test
scenario requires a new test. All task paths and dependencies are defined.
