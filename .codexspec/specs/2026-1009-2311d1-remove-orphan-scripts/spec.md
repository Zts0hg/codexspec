# Specification: Remove orphaned nested script copies

## Context and Goals

Main at `d7f0533` contains six old nested copies. The existing cleanup commit
`7fdfe17` deletes them but lacks a dedicated SDD record. A maintainer needs to
establish that current installation and execution use the supported sources and
flat installed paths before integrating that deletion.

## Requirements and Acceptance

### REQ-001 — Account for consumers before deletion

Sources: NEED-001, CON-001.

Search tracked repository content, classify historical mentions separately, and inspect
indirect source selection and relative script loading. Acceptance: no active consumer
requires a listed nested copy; any contrary evidence stops deletion and integration.

### REQ-002 — Preserve installation and execution while deleting six copies

Sources: NEED-002, CON-001, OUT-001.

Delete exactly the six files enumerated in requirements.md. Keep authoritative
`scripts/bash/`, `scripts/powershell/`, flat `.codexspec/scripts/` files, installer,
templates, and package configuration unchanged. Acceptance: Unix and Windows-path
installation tests pass, installed Bash helpers resolve and run, existing prerequisite
success/error cases pass, and built archives preserve the supported script sources.
Native platform skips must be disclosed, not counted as executions.

### REQ-003 — Supply traceable evidence and integrate

Sources: NEED-003, CON-001, DEC-001.

Produce compact requirements/spec/design/plan/tasks and review/verification records.
Run relevant checks and the project full-suite baseline, complete the independent
defect gate, merge to main, then push and verify remote synchronization. Record any
CI path-filter exclusion honestly. Failed required checks block integration.

## Constraints and Out of Scope

Preserve packaging boundaries and current supported behavior. No unrelated functional
changes, new dependencies, release, or version bump (OUT-001). Do not rewrite historical
requirements merely because they mention a removed file. Unknown external manual use
of undocumented nested copies cannot be proven absent by repository inspection.

## Requirements Traceability

| Confirmed entry | Coverage |
| --- | --- |
| NEED-001 | REQ-001 |
| NEED-002 | REQ-002 |
| NEED-003 | REQ-003 |
| CON-001 | REQ-001, REQ-002, REQ-003 |
| DEC-001 | REQ-003 |
| OUT-001 | REQ-002; Constraints and Out of Scope |

## Open Questions

None. No new runtime error behavior or API is introduced.
