# Implementation Plan: design-to-plan

## Context, Goals, and Non-Goals

Implement the reviewed design.md. Replace the public planning command identity,
preserve its planning behavior, update active consumers, and remove old installed
entries. No aliases, planner redesign, package-boundary changes, or historical
record rewriting.

## Repository Constraints

Use Python 3.11+ and existing pytest/ruff tooling. Author commands in internal
sources and regenerate complete templates and install copies. All work stays in
this feature worktree. Fixture repositories live outside Git checkouts.

## Plan-Level Decisions

- PLD-001: Write focused regression tests for installation retirement and command
  identity before production changes; existing planner/translation/workflow tests
  verify unchanged behavior. Documentation and template renames are direct edits.
- PLD-002: Use the checkout's src through PYTHONPATH or its local environment for
  regeneration and tests, so the globally installed old version cannot restore the
  retired command. Run the existing full quality gates after focused checks.

## Implementation Phases

### P1: Regression coverage and canonical rename

**Covers: REQ-001, REQ-002, REQ-003; Design: C1, C4**

Add focused identity/fresh-install tests and update workflow/catalog assertions.
Observe expected failures with the old distribution. Rename the internal source
and complete output, change the planner title, update registry/catalog keys,
workflow consumers, context templates, helper guidance, and current documentation.
Keep historical SDD/profile/release records untouched. Validate the planner body
against the old source, allowing only the title/name change.

### P2: Installed entry retirement

**Covers: REQ-001, REQ-004; Design: C2, C4**

Test selected integrations on existing installations before implementing cleanup:
force and non-force installs, repeated updates, unrelated file preservation,
replacement-install failure, removal failure, and linked-parent refusal. Implement
exact-entry retirement after replacement presence using existing installer paths.
Avoid recursive deletion; remove only an empty Codex skill directory.

### P3: Regeneration and release-surface validation

**Covers: REQ-001, REQ-002, REQ-003, REQ-004; Design: C3, C4**

Render complete command templates, run normal init --force --ai both against this
worktree, and inspect all generated changes. Run focused tests, full pytest, ruff,
fragment --check-distribution, documentation checks/build, and diff whitespace
checks. Inspect current surfaces for stale instructions and test built package
contents when needed by repository gates. Finish the implement-tasks review gate.

## Verification Strategy

- Fresh and update installer tests assert the new entry and absence of the old.
- Behavioral retirement tests assert errors, repeated execution, preservation, and
  selected-integration behavior rather than merely matching source text.
- Existing template contract tests assert design inputs, traceability, review-plan,
  auto-next, translation coverage, and unchanged distributed command counts.
- Distribution check verifies complete templates and Claude/Codex copies agree.
- Broad checks run only after focused checks pass, then rerun affected checks if
  implementation changes in response to evidence.

## Risks and Delivery

Renaming only the template leaves old commands runnable after updates. P2 covers
this explicitly. Bulk replacement could alter historical evidence or generated
files directly; P1 scopes editable files and P3 regenerates derived forms.
The prepared worktree is retained; merging/pushing is not part of this plan.

## Requirements Coverage

| Requirement | Plan | Design |
| --- | --- | --- |
| REQ-001 | P1, P2, P3 | C1-C4 |
| REQ-002 | P1, P3 | C1, C4 |
| REQ-003 | P1, P3 | C1, C3, C4 |
| REQ-004 | P2, P3 | C2, C4 |

## Open Items

None.
