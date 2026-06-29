# Confirmed Requirements: auto-next-command

<!--
Language: Maintain this document in the language specified in .codexspec/config.yml.
This file is the authoritative, persistent record of user-confirmed intent.
Do not copy the full conversation. Keep only confirmed decisions and short evidence
quotes needed to resolve later interpretation disputes.
-->

**Feature ID**: `2026-0629-22061u`
**Status**: Confirmed
**Last Confirmed**: 2026-06-29

## Authority Rules

- Only entries with `Status: confirmed` are binding downstream inputs.
- `open` entries MUST NOT be converted into confirmed product requirements.
- Replaced entries remain in this file with `Status: superseded` and a link to the replacement.
- AI inferences must be labeled as assumptions and require user confirmation before becoming binding.

## Needs

### NEED-001: Auto-advance the SDD command chain

- **Status**: confirmed
- **Statement**: Add a `workflow.auto_next` option in `.codexspec/config.yml`. When enabled, once the current pipeline stage is "passed", automatically invoke the next command in the SDD chain instead of requiring the user to manually trigger it.
- **Rationale**: The user wants a higher degree of automation so the SDD pipeline runs end-to-end without manual hand-offs between stages.
- **User Evidence**: "我希望为 codexspec 增加一个机制，可以设置auto-next……如果任务状态是pass且设置了auto-next，则自动触发下一个命令。" / "我希望自动化的程度高一些"
- **Confirmed At**: 2026-06-29

### NEED-002: Full core pipeline coverage; implement-tasks is terminal

- **Status**: confirmed
- **Statement**: `auto_next` governs the complete core pipeline `specify → generate-spec → spec-to-plan → plan-to-tasks → implement-tasks`. `implement-tasks` is the terminal command; nothing is auto-invoked after it.
- **Rationale**: Matches the user's stated chain; `implement-tasks` has no natural successor and `review-code` already runs inside it.
- **User Evidence**: "specify 也自动触发 generate-spec，implement-tasks 是终点"
- **Confirmed At**: 2026-06-29

## Constraints

### CON-001: Two distinct "pass" gates

- **Status**: confirmed
- **Statement**: (a) For `generate-spec` / `spec-to-plan` / `plan-to-tasks`, "passed" = the command's built-in review loop Overall Status is `PASS` or `PASS_WITH_WARNINGS`. (b) `specify` has no review loop; its gate is the user's explicit confirmation that requirements discovery is complete (the Stage Summary Confirmation step).
- **User Evidence**: Confirmed in discussion. `specify` lacks a review loop, so its "pass" equivalent is explicit user confirmation of requirements completion; the other three commands reuse the existing review-loop verdict.

### CON-002: Chain stops on non-pass review status

- **Status**: confirmed
- **Statement**: When the review Overall Status is `NEEDS_REVISION` or `BLOCKED`, `auto_next` does NOT fire; control returns to the user.
- **User Evidence**: Confirmed as part of the consolidated stage summary ("其他都同意"); consistent with the existing analyze auto-invoke stopping behavior.

### CON-003: Default false, opt-in, backwards compatible

- **Status**: confirmed
- **Statement**: `workflow.auto_next` defaults to `false`. When absent or `false`, existing behavior is unchanged — every command ends and the next is triggered manually by the user.
- **User Evidence**: Confirmed as part of the consolidated stage summary ("其他都同意").

### CON-004: Single global boolean under a `workflow` section

- **Status**: confirmed
- **Statement**: The option is a single global boolean `workflow.auto_next` (snake_case, mirroring `git.branch_check_enabled`), governing all transitions uniformly. No per-step / per-transition granularity in this iteration.
- **User Evidence**: "用 workflow.auto_next"

### CON-005: analyze remains informational and non-blocking

- **Status**: confirmed
- **Statement**: With `auto_next` on, after `plan-to-tasks` passes the order is `plan-to-tasks (pass) → analyze (read-only) → implement-tasks`. analyze's findings do NOT block `implement-tasks`, since analyze already declares itself informational / non-gating.
- **User Evidence**: Confirmed as part of the consolidated stage summary ("其他都同意").

## Decisions

### DEC-001: Fully automatic; no confirmation prompt before implement-tasks

- **Status**: confirmed
- **Decision**: The jump into `implement-tasks` (which writes and commits real code) proceeds without a yes/no confirmation prompt.
- **Alternatives Rejected**: "Auto-fire but confirm before implement-tasks"; "Never auto-fire implement-tasks" (both presented and declined).
- **Reason**: The user wants high automation. The risk is mitigated by the per-stage review gates (`PASS` / `PASS_WITH_WARNINGS`) that must be cleared before each auto-advance.
- **User Evidence**: "我希望自动化的程度高一些，所以implement-tasks是希望能够自动进行"

### DEC-002: Threshold is PASS or PASS_WITH_WARNINGS

- **Status**: confirmed
- **Decision**: `auto_next` treats both `PASS` and `PASS_WITH_WARNINGS` as "passed" (not strict `PASS` only).
- **Alternatives Rejected**: Require strict `PASS` for the implement-tasks jump; require strict `PASS` everywhere (both presented and declined).
- **Reason**: Maximize automation, keep the rule uniform, and stay consistent with the existing analyze auto-invoke mechanism.
- **User Evidence**: "PASS_WITH_WARNINGS 也算过"

### DEC-003: Implement via conditional auto-invoke in each command template

- **Status**: confirmed
- **Decision**: Each command's template gains a conditional section: when `workflow.auto_next` is enabled and the stage passed, the agent invokes the next slash command (e.g. `/codexspec:spec-to-plan <feature-dir>`).
- **Alternatives Rejected**: None explicitly discussed.
- **Reason**: The mechanism is identical to the existing "auto-invoke analyze after plan-to-tasks" precedent (commit #17), reusing the proven pattern.
- **User Evidence**: Confirmed as part of the consolidated stage summary ("其他都同意").

### DEC-004: Emit a one-line transparency notice before auto-invoking

- **Status**: confirmed
- **Decision**: Before auto-invoking the next command, the agent prints a one-line notice, e.g. `auto_next: review passed → invoking /codexspec:spec-to-plan`, so the chain is observable.
- **Alternatives Rejected**: Fully silent chaining (minimal output) — presented and declined.
- **Reason**: Observability of an otherwise hands-off chain; very low cost.
- **User Evidence**: "要" (in response to the DEC-004 proposal).

## Out of Scope

### OUT-001: Optional / helper commands are not part of the auto chain

- **Status**: confirmed
- **Statement**: `clarify`, `checklist`, and `tasks-to-issues` are never auto-invoked by `auto_next`; they remain manual/optional. `review-code` already runs internally within `implement-tasks` and is not a separate `auto_next` hop.
- **Reason**: `auto_next` covers only the core SDD pipeline; optional helpers stay user-driven.
- **User Evidence**: Confirmed as part of the consolidated stage summary ("其他都同意").

### OUT-002: No per-transition configuration in this iteration

- **Status**: confirmed
- **Statement**: Users cannot selectively enable/disable individual transitions (e.g., only the implement-tasks jump). `workflow.auto_next` is all-or-nothing.
- **Reason**: A single global boolean satisfies the stated goal; per-step granularity is deferred.
- **User Evidence**: Confirmed as part of the consolidated stage summary ("其他都同意").

## Open Questions

_None — all material decisions are confirmed. No blocking open questions remain for specification generation._

## Superseded Entries

_None._

## Confirmation Log

### Session 2026-06-29

- **Summary Presented**: Consolidated stage summary grouped by candidate IDs (NEED-001/002, CON-001..005, DEC-001..004, OUT-001/002), preceded by point-by-point discussion of automation level, the "pass" threshold, chain boundaries, and the parameter-naming convention.
- **User Confirmation**: Explicit confirmation of each decision across the discussion. Final confirmations: automation level + implement-tasks auto-fires ("我希望自动化的程度高一些，所以implement-tasks是希望能够自动进行"); threshold ("PASS_WITH_WARNINGS 也算过"); chain boundaries ("specify 也自动触发 generate-spec，implement-tasks 是终点"); parameter name ("用 workflow.auto_next"); transparency notice ("要").
- **Entries Confirmed**: NEED-001, NEED-002, CON-001, CON-002, CON-003, CON-004, CON-005, DEC-001, DEC-002, DEC-003, DEC-004, OUT-001, OUT-002
