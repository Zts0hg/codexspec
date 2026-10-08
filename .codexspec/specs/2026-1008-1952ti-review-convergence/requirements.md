# Confirmed Requirements: review-convergence

<!--
Language: Maintain this document in the language specified in .codexspec/config.yml.
This file is the authoritative, persistent record of user-confirmed intent.
Do not copy the full conversation. Keep only confirmed decisions and short evidence
quotes needed to resolve later interpretation disputes.
-->

**Feature ID**: `2026-1008-1952ti`
**Status**: Confirmed
**Last Confirmed**: 2026-10-08

## Background

A Codex session in a downstream project ran the `implement-tasks` final code-review loop for 21+ rounds without reaching `PASS`. Each round re-reviewed the complete feature target (about 1,920–1,940 inventory entries, 799 of them binary) with a fresh isolated reviewer. Rounds were consumed by: re-reviewing unchanged evidence; admitting findings whose triggers fall outside the project's real operating context (for example, `ß`/`ẞ` filename aliasing in a Chinese/English-only project); review-environment overhead (a disposable mirror missing Git metadata, oversized output that the client could not display, thread limits, a platform content filter); repairs that fixed one instance or introduced regressions, while the same root-cause class reappeared in later rounds; and some reviewers spawned with the full implementation conversation forked in. The same protocol has converged successfully on many other features, including CodexSpec's own; the goal is to remove wasted review work, not to weaken the gate.

## Authority Rules

- Only entries with `Status: confirmed` are binding downstream inputs.
- `open` entries MUST NOT be converted into confirmed product requirements.
- Replaced entries remain in this file with `Status: superseded` and a link to the replacement.
- AI inferences must be labeled as assumptions and require user confirmation before becoming binding.

## Needs

### NEED-001: Converge without losing review completeness

- **Status**: confirmed
- **Statement**: The `review-code` defect gate, as driven by the `implement-tasks` final review loop, keeps complete-feature acceptance while reducing ineffective and redundant review work so that the loop converges well.
- **Rationale**: Complete acceptance prevents hidden defects from shipping; redundant rounds waste time and add churn without improving that guarantee.
- **User Evidence**: "如何在保留review-code的审查全面性的同时减少无效冗余的review让审查可以良好收敛"
- **Confirmed At**: 2026-10-08

### NEED-002: Incremental re-review after repairs

- **Status**: confirmed
- **Statement**: After a repair, intermediate re-review rounds cover only the repair delta, the contracts and call chains it affects, and the carried-over follow-up obligations. Evidence whose fingerprint is unchanged keeps the coverage established by the previous round. Once an incremental round passes, one fresh complete review runs as the final acceptance.
- **Rationale**: Most rounds re-reviewed nearly identical, already-covered evidence; a final complete review preserves full acceptance.
- **User Evidence**: Selected "Incremental, full final round".
- **Confirmed At**: 2026-10-08

### NEED-003: Configurable decision for out-of-context triggers

- **Status**: confirmed
- **Statement**: A parameter controls who decides about a finding whose trigger depends on inputs or environments outside the project's real operating context:
  - `reviewer` (default): the reviewer decides entirely, so `review-code` behaves exactly as it does today.
  - `ask`: the reviewer reports such a finding as needing a scenario decision instead of failing on it. The user decides once (fix or accept); the decision is recorded in the feature artifacts and later rounds follow it without re-raising the same issue.
- **Rationale**: Findings with unrealistic triggers caused out-of-scope repairs and extra rounds, but the default behavior must stay unchanged.
- **User Evidence**: "可以通过参数控制，可以设置为是交给用户决策一次，之后沿用。默认参数是完全由审查员判断能够触发，这样review-code的行为就与之前一样。"
- **Confirmed At**: 2026-10-08

### NEED-004: Cross-round root-cause escalation into debug

- **Status**: confirmed
- **Statement**: `implement-tasks` records a root-cause class for each verified finding across rounds. When a finding of an already-recorded class reappears in a later round, it escalates into `debug` and treats the whole class as one defect: identify the shared root cause, repair it uniformly, and search the codebase for every location of that class. The existing `debug` rule of questioning the architecture after three failed fixes applies.
- **Rationale**: `debug` already handles one defect that survives repeated fixes, but it does not catch a different instance of the same class appearing in each round (for example, symlink-ancestor writes outside the repository found in several rounds at different locations).
- **User Evidence**: Selected "Extend the debug trigger conditions"; "你说的这种情况是否是我们之前增加 codexspec:debug 命令希望解决的？"
- **Confirmed At**: 2026-10-08

### NEED-005: Reduce rounds lost to the review environment

- **Status**: confirmed
- **Statement**: `review-code` prevents environment overhead from invalidating rounds:
  - A disposable verification mirror preserves the Git metadata that verification needs.
  - Complete inventory and coverage records are written to files outside the repository; the conversation receives only a summary and the result envelope.
  - The nesting depth of specialist reviewers is bounded so reviews do not hit thread limits.
- **Rationale**: Mirrors missing Git metadata, output too large to display, a platform content filter and thread limits all voided rounds without any product defect.
- **User Evidence**: "R3和R5都纳入"
- **Confirmed At**: 2026-10-08

### NEED-006: Make reviewer isolation unambiguous to every host

- **Status**: confirmed
- **Statement**: The key reviewer-isolation constraints are written as concrete instructions that both Codex and Claude Code can follow unambiguously. For example, a reviewer must be spawned in a fresh context and must not inherit the implementation conversation.
- **Rationale**: Some rounds spawned reviewers with the full implementation conversation forked in (`fork_turns: "all"`), which the isolation rule forbids.
- **User Evidence**: "R3和R5都纳入"
- **Confirmed At**: 2026-10-08

## Constraints

### CON-001: Final acceptance completeness is not reduced

- **Status**: confirmed
- **Statement**: A final `PASS` still rests on one fresh, complete review. The rule that any admitted P0–P3 finding produces `FAIL` is unchanged.
- **User Evidence**: "我们就是希望在验收阶段可以对功能进行完整验收，以避免隐藏bug上线带来的负面影响。"

### CON-002: Default configuration keeps today's review standard

- **Status**: confirmed
- **Statement**: With default configuration, `review-code` applies the same review standard as it does today.
- **User Evidence**: "默认参数是完全由审查员判断能够触发，这样review-code的行为就与之前一样。"

### CON-003: Affected surfaces

- **Status**: confirmed
- **Statement**: Changes are made in the source templates: mainly `templates/commands/review-code.md` and `templates/commands/implement-tasks.md`, with minor adjustments to `templates/commands/debug.md` where needed. `auto-dev` inherits the behavior through `implement-tasks`. The new configuration key is added to the configuration CLI and the related templates. Derived `.claude/commands/codexspec/` and `.agents/skills/codexspec-*/` copies are not edited by hand.
- **User Evidence**: Confirmed assumption A-1.

## Decisions

### DEC-001: Incremental intermediate rounds, complete final round

- **Status**: confirmed
- **Decision**: Intermediate rounds are incremental, and acceptance always ends with a fresh complete review (NEED-002).
- **Alternatives Rejected**: Fully incremental review that never re-runs a complete review; keeping a complete re-review every round.
- **Reason**: Removes repeated full reviews while keeping complete acceptance.
- **User Evidence**: Selected "Incremental, full final round".

### DEC-002: Out-of-context trigger handling is a parameter; the default is the reviewer

- **Status**: confirmed
- **Decision**: NEED-003's behavior is selected by a parameter whose default (`reviewer`) preserves current behavior.
- **Alternatives Rejected**: Making reachability judgment mandatory for the reviewer; keeping `FAIL` and allowing user waivers.
- **Reason**: The user wants the stricter current behavior by default and an opt-in to decide such findings once.
- **User Evidence**: "可以通过参数控制……默认参数是完全由审查员判断能够触发"

### DEC-003: Configuration key plus per-invocation override

- **Status**: confirmed
- **Decision**: The project-level default lives in `.codexspec/config.yml` as `review.decided_by: reviewer | ask`, and a single `review-code` invocation may override it with `--decided-by reviewer|ask`. `implement-tasks` and `auto-dev` pick up the configured value without changing their fixed `review-code` invocation.
- **Alternatives Rejected**: Configuration key only; command argument only; the names `review.trigger_context`, `review.scenario_decision`, `review.reachability_decision` and `review.edge_case_decision`, which were not plain enough.
- **Reason**: Callers that use a fixed invocation inherit the setting, ad-hoc runs can override it, and the name states plainly who decides.
- **User Evidence**: Selected "Configuration key + command argument override"; "名称还是不够直白，为什么你不认可或者不推荐 review.decided_by 之类的参数名"

### DEC-004: Cross-round root-cause escalation instead of a round cap

- **Status**: confirmed
- **Decision**: Non-convergence is handled by escalating a recurring root-cause class into `debug` (NEED-004), not by limiting the number of rounds.
- **Alternatives Rejected**: A round threshold that pauses and reports; trend-based pausing; class-wide repair only from variant-search results.
- **Reason**: The user does not want a round cap; `debug` is the existing mechanism for repairs that do not converge.
- **User Evidence**: "我不希望增加轮次上限。"

### DEC-005: Resume incrementally after a failed final review

- **Status**: confirmed
- **Decision**: If the final complete review finds new defects, the repairs are re-reviewed incrementally first. Once an incremental round passes, a new fresh complete review runs as the final acceptance.
- **Alternatives Rejected**: Running a complete review again immediately after each repair.
- **Reason**: Consistent with DEC-001; acceptance always ends with a complete review without reintroducing repeated full reviews.
- **User Evidence**: Selected "Back to incremental, then a complete review".

### DEC-006: implement-tasks classifies cross-round root causes

- **Status**: confirmed
- **Decision**: `implement-tasks` assigns the cross-round root-cause class. It combines the reviewer's root-cause description with its own independent verification of each finding. `review-code`'s output schema and reviewer isolation are unchanged by this.
- **Alternatives Rejected**: A class label emitted by `review-code` (a schema change, and labels would not be stable across isolated reviewers); combining both.
- **Reason**: The reviewer's `root_cause_id` is local to one round, and `implement-tasks` already verifies findings and maintains cross-round records.
- **User Evidence**: Selected "implement-tasks classifies".

## Out of Scope

### OUT-001: No review round cap

- **Status**: confirmed
- **Statement**: No maximum number of review rounds is introduced.
- **Reason**: The user explicitly rejected a round cap; convergence is addressed by NEED-002 to NEED-006.
- **User Evidence**: "我不希望增加轮次上限。"

## Open Questions

None.

## Confirmation Log

### Session 2026-10-08

- **Summary Presented**: Stage summary covering NEED-001 to NEED-006, CON-001 to CON-002, DEC-001 to DEC-004, OUT-001, assumptions A-1 (affected surfaces) and A-2 (new workspace based on `main`), and open questions OPEN-001 to OPEN-003.
- **User Confirmation**: "确认A-1 和A-2"; then "全部确认，先定 OPEN".
- **Entries Confirmed**: NEED-001, NEED-002, NEED-003, NEED-004, NEED-005, NEED-006, CON-001, CON-002, CON-003 (from A-1), DEC-001, DEC-002, DEC-003, DEC-004, OUT-001
- **Open Questions Resolved**: OPEN-001 → DEC-005; OPEN-002 → DEC-003 (key name `review.decided_by`); OPEN-003 → DEC-006.

### Session 2026-10-08 (final)

- **Summary Presented**: Final record with DEC-005, DEC-006 and the `review.decided_by` / `--decided-by` naming added.
- **User Confirmation**: "都不是，当前内容确认"
- **Entries Confirmed**: DEC-005, DEC-006, DEC-003 (final naming)
