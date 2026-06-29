# Confirmed Requirements: plan-to-tasks-auto-analyze

<!--
Language: Maintain this document in the language specified in .codexspec/config.yml.
This file is the authoritative, persistent record of user-confirmed intent.
Do not copy the full conversation. Keep only confirmed decisions and short evidence
quotes needed to resolve later interpretation disputes.
-->

**Feature ID**: `2026-0629-1337a7`
**Status**: Confirmed
**Last Confirmed**: 2026-06-29

## Authority Rules

- Only entries with `Status: confirmed` are binding downstream inputs.
- `open` entries MUST NOT be converted into confirmed product requirements.
- Replaced entries remain in this file with `Status: superseded` and a link to the replacement.
- AI inferences must be labeled as assumptions and require user confirmation before becoming binding.

## Summary

Extend `plan-to-tasks` so that, after its existing Automatic Review Loop finishes in a passing state, it automatically invokes `/codexspec:analyze` once to check end-to-end traceability and consistency across requirements → spec → plan → tasks. The step removes a manual user action; analyze's result is purely informational and does not gate implementation.

## Needs

### NEED-001: Auto-invoke analyze after the plan-to-tasks review loop passes

- **Status**: confirmed
- **Statement**: After `plan-to-tasks` generates tasks and the Automatic Review Loop finishes in a passing state, it automatically invokes `/codexspec:analyze` once to check end-to-end traceability and consistency across requirements → spec → plan → tasks, so the user does not have to run it manually.
- **Rationale**: Removes a manual step and surfaces cross-artifact consistency issues at the moment tasks are produced, before implementation begins.
- **User Evidence**: "I want to automatically invoke the analyze command after the plan-to-tasks command... auto-invoke analyze when the tasks content is correct, to save the user trouble."
- **Confirmed At**: 2026-06-29

## Constraints

### CON-001: Trigger threshold for the auto-analyze step

- **Status**: confirmed
- **Statement**: analyze is auto-invoked only when the review loop's terminal status is `PASS` or `PASS_WITH_WARNINGS` (i.e., no Critical/Warning defects). If the loop stops at `NEEDS_REVISION`/`BLOCKED`, or hits the existing stop conditions (defects repeat, remain unresolved, or a user/architecture decision is required), analyze is NOT invoked and control returns to the user unchanged from today.
- **User Evidence**: User accepted the proposed threshold: PASS or PASS_WITH_WARNINGS (no Critical/Warning) → run analyze; NEEDS_REVISION/BLOCKED → stop and hand back to user.

### CON-002: analyze runs once and is read-only

- **Status**: confirmed
- **Statement**: The auto-invoked analyze executes a single pass and is read-only. `plan-to-tasks` does NOT auto-fix analyze findings and does NOT run a fix-and-reanalyze loop (unlike the review-tasks loop).
- **User Evidence**: Follows from the user's choice that analyze is "purely informational"; analyze is read-only by definition.

### CON-003: analyze results are purely informational

- **Status**: confirmed
- **Statement**: analyze's output does NOT change whether tasks are considered ready for implementation and does NOT add a new gate before `/codexspec:implement-tasks`. Tasks passing the review loop remains the readiness signal.
- **User Evidence**: User selected "purely informational (recommended)".

### CON-004: The auto-analyze step is always-on

- **Status**: confirmed
- **Statement**: The auto-analyze step is always enabled — it is not placed behind a config key or CLI flag — matching the existing always-on Automatic Review Loop.
- **User Evidence**: User confirmed ASMP-A.

### CON-005: Legacy mode (no requirements.md) still auto-runs analyze

- **Status**: confirmed
- **Statement**: When `requirements.md` is absent, the auto-analyze step still runs, and analyze discloses its existing legacy limitation (analysis starts at spec.md; fidelity to the original discussion cannot be verified).
- **User Evidence**: User confirmed ASMP-B.

## Decisions

### DEC-001: Change location — extend the template's Automatic Review Loop

- **Status**: confirmed
- **Decision**: The change is made in `templates/commands/plan-to-tasks.md` (the source-of-truth template), by extending the existing "Automatic Review Loop" section with a "passing state → invoke `/codexspec:analyze`" step. It is NOT made in `.claude/commands/codexspec/` (a self-bootstrap install artifact).
- **Reason**: The project's Self-bootstrap / Slash Command Template Modification Rules require distributed-command edits to go through `templates/commands/` so they reach end users.
- **Alternatives Rejected**: Editing `.claude/commands/codexspec/plan-to-tasks.md` directly — rejected because it is a derived install artifact that would be silently overwritten on reinstall and would never reach end users.

### DEC-002: Do not modify plan-to-tasks Output Summary for analyze

- **Status**: confirmed
- **Decision**: `plan-to-tasks`'s Output Summary is NOT changed to summarize analyze. analyze's own output is the report (presented inline). The only template change is the new invoke-analyze step in the Automatic Review Loop.
- **Reason**: Avoids duplicating analyze's output; consistent with the existing convention where `plan-to-tasks` only references "auto-review status" and lets the sub-command produce the detail.
- **Alternatives Rejected**: Appending an analyze summary to `plan-to-tasks`'s Output Summary — rejected as redundant with analyze's own output.
- **User Evidence**: User asked "is it necessary to modify plan-to-tasks's output rather than rely on analyze's own output?", which led to this decision.

### DEC-003: analyze does not save a separate report file

- **Status**: confirmed
- **Decision**: The auto-invoked analyze is not required to persist a report file; its inline output is the report, preserving analyze's current (no-file) behavior.
- **Reason**: Sufficient for a purely informational check; the user did not request a persisted file.
- **Alternatives Rejected**: Saving an `analyze.md` report — explicitly out of scope for now; see OUT-005.

## Out of Scope

### OUT-001: No changes to review-tasks itself

- **Status**: confirmed
- **Statement**: The `review-tasks` command and its auto-fix logic (as orchestrated by `plan-to-tasks`'s existing loop) are not modified.
- **Reason**: The auto-fix review loop already exists; this feature only adds the analyze step after it.

### OUT-002: No auto-fix loop for analyze

- **Status**: confirmed
- **Statement**: No fix-and-reanalyze loop is added for analyze; it runs once and only reports.
- **Reason**: analyze is read-only and the user chose a purely informational role for it.

### OUT-003: analyze is not chained into other commands

- **Status**: confirmed
- **Statement**: Auto-invoking analyze is scoped to `plan-to-tasks` only; no other command auto-chains analyze.
- **Reason**: The user's request is specific to the plan-to-tasks flow.

### OUT-004: No new "next step: implement-tasks" recommendation

- **Status**: confirmed
- **Statement**: `plan-to-tasks` does not gain a new explicit "next step: `/codexspec:implement-tasks`" recommendation as part of this feature; the Output Summary is not changed (per DEC-002).
- **Reason**: User chose "do not add" — minimal change, no scope creep.

### OUT-005: Persisting analyze results to disk is out of scope

- **Status**: confirmed
- **Statement**: Saving the auto-invoked analyze output to a file on disk (e.g., an `analyze.md` report) is out of scope for now. analyze's inline output remains the report.
- **Reason**: User explicitly marked this behavior as not considered for the current effort.
- **User Evidence**: "Mark 'saving analyze results to disk' as OUT — not considered for now."

## Open Questions

None blocking. All material questions were resolved during discovery.

Persisting analyze results to disk is no longer a deferred option — it is explicitly out of scope for now (see OUT-005).

## Superseded Entries

<!-- None. No confirmed entry has been replaced. -->

## Confirmation Log

### Session 2026-06-29

- **Summary Presented**: Stage summary containing NEED-001; CON-001/002/003; DEC-001; OUT-001; assumptions ASMP-A (always-on), ASMP-B (legacy mode), ASMP-C (revised: no Output Summary change, rely on analyze's own output); and OPEN-001 (whether to add an implement recommendation).
- **User Confirmation**: User confirmed the trigger threshold (PASS / PASS_WITH_WARNINGS), the purely-informational role of analyze, ASMP-A and ASMP-B, the revised ASMP-C (do not modify plan-to-tasks output), and resolved OPEN-001 as "do not add an implement recommendation".
- **Entries Confirmed**: NEED-001; CON-001, CON-002, CON-003, CON-004, CON-005; DEC-001, DEC-002, DEC-003; OUT-001, OUT-002, OUT-003, OUT-004.

### Session 2026-06-29 (follow-up)

- **Change Requested**: User asked to record "persisting analyze results to disk" explicitly as out of scope.
- **Action Taken**: Added OUT-005; tightened DEC-003's rejected alternative to reference OUT-005; updated Open Questions to drop the deferred-option framing.
- **Entries Confirmed**: OUT-005 added (confirmed); DEC-003 reaffirmed.
