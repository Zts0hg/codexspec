# Feature Specification: Comprehensive English README Audit

**Feature Branch**: `2026-1012-2306uu-readme-feature-audit`
**Created**: 2026-10-12
**Status**: Ready for Design
**Authority**: [Confirmed requirements](requirements.md)

## Context and Goals

The English README must describe current user-facing functionality accurately
and completely. The audit starts from implementation, not from the features
already mentioned in the README. Installation-guide changes alone do not
establish feature coverage.

## User Scenarios

### Discover an appropriate workflow

A Claude Code or Codex user can identify the standard feature pipeline, small
change workflow, autonomous blueprint workflow, and entry points for existing
code. The README provides purpose, suitable use, invocation, and key defaults
or links to current detailed guidance.

### Understand configured behavior

A reader can distinguish human confirmation of requirements from automatic
stage advancement, automatic knowledge capture, maintenance repair policy,
review scenario decisions, and checkout-local workspace isolation.

### Verify the documentation audit

A maintainer can inspect a complete capability inventory and evidence-backed
audit results, including capabilities previously absent from the README, and
trace each resolved issue to the revised document.

## Requirements

### REQ-001: Inventory current user-facing functionality

Inventory the six public CLI commands, 28 distributed agent commands, and
cross-command behavior covering integrations, configuration, automation,
worktrees, project knowledge, and historical requirements recall. Establish
each item's behavior from current source and relevant confirmed decision
history; historical plans alone do not prove implementation.

Sources: NEED-001.

### REQ-002: Assess accuracy and completeness with evidence

For every inventory item, record the baseline README coverage and whether it
is accurate, outdated/incorrect, absent, or insufficiently explained. Cite
implementation or command sources for every issue and identify its resolution
in the final README. Distinguish implementation uncertainty from a documentation
defect instead of inventing behavior.

Sources: NEED-002.

### REQ-003: Repair descriptions and explain available capabilities

Correct inaccurate or stale statements and introduce missing or insufficiently
explained capabilities. Readers must understand purpose, suitable use,
invocation entry, and important defaults. Concise command tables and existing
detailed documentation links may complete coverage; every internal mechanism
or command argument need not be reproduced as a full reference manual.

Sources: NEED-003.

### REQ-004: Synchronize the complete README

Keep the introduction, advantages, quick start, workflows, command lists,
configuration, initialized project structure, and development examples
consistent. Fix broken links, misleading counts, repeated explanations, and
misplaced paragraphs. Preserve useful existing installation guidance.

Sources: NEED-004, NEED-003.

### REQ-005: Restrict the product change to English README.md

Only README.md may change outside this feature's own workflow records.
Other language READMEs, program behavior, templates, reference documentation,
and historical requirement records remain outside the product change.

Sources: CON-001.

### NFR-001: Use evidence and readable English

Use established terminology, explain project-specific concepts, and retain
meaning and critical conditions when making the README concise. Do not present
unimplemented behavior as available or promise measured agent effectiveness
from instruction-delivery tests.

Sources: NEED-002, NEED-003, NEED-004, CON-001.

## Acceptance Criteria

- The audit accounts for all six public CLI commands and all 28 distributed
  commands, plus the cross-command mechanisms in REQ-001.
- Every inventory item has an explicit coverage assessment and source reference;
  identified accuracy and coverage defects have a documented resolution.
- Claude and Codex readers have valid setup/invocation entry points, and all
  standard pipeline explanations include the design stage.
- Workflow and review defaults agree with implementation. The optional Quick
  workflow is described from its own current contract.
- README relative links and in-page anchors resolve; command names and option
  examples match current sources; Markdown and whitespace checks pass.
- A final diff shows no product-file change outside README.md. Workflow records
  are confined to this feature directory.

## Boundaries and Expected Error Behavior

If a capability's behavior cannot be established, record that uncertainty in
the audit and avoid unsupported README claims. Fix documentation from verified
behavior; report any independently discovered implementation discrepancy
without changing program behavior. Read-only command help can verify public
syntax without running mutating user workflows.

## Out of Scope

Other README languages, implementation changes, command-template changes,
reference-document rewrites, and changes to historical requirement records.

## Assumptions and Open Questions

No blocking product assumptions or open questions. Documentation placement and
verification tooling are implementation choices within the confirmed scope.

## Requirements Traceability

| Confirmed Entry | Spec Coverage |
|-----------------|---------------|
| NEED-001 | REQ-001 |
| NEED-002 | REQ-002, NFR-001 |
| NEED-003 | REQ-003, REQ-004, NFR-001 |
| NEED-004 | REQ-004, NFR-001 |
| CON-001 | REQ-005, Out of Scope |
