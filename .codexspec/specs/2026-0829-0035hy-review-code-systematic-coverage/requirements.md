# Confirmed Requirements: review-code-systematic-coverage

<!--
Language: Maintain this document in the language specified in .codexspec/config.yml.
This file is the authoritative, persistent record of user-confirmed intent.
Do not copy the full conversation. Keep only confirmed decisions and short evidence
quotes needed to resolve later interpretation disputes.
-->

**Feature ID**: `2026-0829-0035hy`
**Status**: Confirmed
**Last Confirmed**: 2026-08-29 00:35 CST

## Authority Rules

- Only entries with `Status: confirmed` are binding downstream inputs.
- `open` entries MUST NOT be converted into confirmed product requirements.
- Replaced entries remain in this file with `Status: superseded` and a link to the replacement.
- AI inferences must be labeled as assumptions and require user confirmation before becoming binding.

## Needs

### NEED-001: Source-independent systematic review

- **Status**: confirmed
- **Statement**: Improve the `review-code` defect gate for use across arbitrary projects without depending on a particular repository, programming language, framework, directory layout, or CodexSpec feature workspace.
- **Rationale**: The improvement must prevent repeated shallow review cycles as a general review capability rather than encode one project's incidents.
- **User Evidence**: "我不希望是跟当前项目绑定，应该是让 review-code 可以在各个项目中都能够不再出现我们现在遇到的这种每复审一次才发现一些之前问题的相关问题。"
- **Confirmed At**: 2026-08-29 00:35 CST

### NEED-002: System-wide consistency and cross-module contract review

- **Status**: confirmed
- **Statement**: Before assessing individual defects, defect-gate mode must identify the system-wide consistency rules and cross-module contracts implicated by the selected change, then verify each rule across its sources, propagation boundaries, consumers, entry surfaces, and relevant scenarios.
- **Rationale**: File-level inspection can miss a broken contract at a different point in the same end-to-end flow.
- **User Evidence**: The user confirmed adding "系统级一致性约束 / 跨模块契约" review behavior.
- **Confirmed At**: 2026-08-29 00:35 CST

### NEED-003: Root-cause variant analysis

- **Status**: confirmed
- **Statement**: After validating a candidate defect, the reviewer must identify its root cause and inspect all reasonably bounded sibling occurrences, including equivalent callers, implementations, entry surfaces, adapters, and symmetric execution paths, before finalizing that review round.
- **Rationale**: Reporting only the first observed occurrence allows related defects to surface one per subsequent review.
- **User Evidence**: The user confirmed adding "同根因缺陷的变体分析".
- **Confirmed At**: 2026-08-29 00:35 CST

### NEED-004: Complete the selected review before reporting

- **Status**: confirmed
- **Statement**: An admitted finding must not terminate the remaining planned review work. The reviewer must complete every selected contract, behavior, risk, and verification partition before emitting the round's final result.
- **Rationale**: Early termination after the first valid finding turns later reviews into incremental discovery rather than a complete defect gate.
- **User Evidence**: The user confirmed the proposed requirement that one defect must not stop the rest of the review.
- **Confirmed At**: 2026-08-29 00:35 CST

### NEED-005: Structured review coverage

- **Status**: confirmed
- **Statement**: Each defect-gate result must record the reviewed system rules, covered and uncovered surfaces and scenarios, completed root-cause variant searches, review partitions, and evidence needed after repair.
- **Rationale**: A file inventory and an empty finding list do not show which behaviors were actually established.
- **User Evidence**: The user confirmed adding "缺陷闭环和审查覆盖跟踪".
- **Confirmed At**: 2026-08-29 00:35 CST

### NEED-006: Read-only cross-round handoff

- **Status**: confirmed
- **Statement**: A caller performing a repair loop must carry the structured coverage and neutral post-repair verification obligations from one review round into the next while preserving independent judgment by the next reviewer.
- **Rationale**: Review knowledge must survive repair rounds without telling a fresh reviewer that a repair is already correct.
- **User Evidence**: "我也认为应该保持只读，采用你建议的第一种方案。"
- **Confirmed At**: 2026-08-29 00:35 CST

### NEED-007: Complete partition ownership for large changes

- **Status**: confirmed
- **Statement**: When the selected change requires partitioning, each behavior or contract partition must have explicit scope, reviewer ownership, and completion state, and every mandatory partition must complete before PASS.
- **Rationale**: Marking a file as reviewed is not equivalent to verifying every changed behavior that crosses that file.
- **User Evidence**: The user confirmed the proposed complete-partition requirement for large reviews.
- **Confirmed At**: 2026-08-29 00:35 CST

### NEED-008: Repair-loop integration

- **Status**: confirmed
- **Statement**: `implement-tasks` must consume the new review result, verify admitted defects, preserve neutral coverage obligations, perform repairs under its existing safety rules, and request a fresh complete review of the updated target.
- **Rationale**: The review command and its standard repair-loop caller must agree on completion and handoff semantics.
- **User Evidence**: The user confirmed migrating `implement-tasks` together with the review result contract.
- **Confirmed At**: 2026-08-29 00:35 CST

## Constraints

### CON-001: Review-code remains read-only

- **Status**: confirmed
- **Statement**: `review-code` must not create, update, or delete repository files or persistent review-state artifacts. Structured cross-round state is returned to the caller in the result.
- **User Evidence**: "我也认为应该保持只读，采用你建议的第一种方案。"

### CON-002: Neutral handoff preserves reviewer independence

- **Status**: confirmed
- **Statement**: A fresh reviewer may receive objective coverage records and verification obligations but must not inherit implementation reasoning, prior correctness conclusions, or assertions that a repair succeeded.
- **User Evidence**: The user confirmed the proposed read-only structured handoff while retaining independent review.

### CON-003: No project-specific coupling

- **Status**: confirmed
- **Statement**: Product requirements, command behavior, result fields, tests, and examples must use source-independent concepts and must not refer to the incident, repository, or implementation details that motivated the feature.
- **User Evidence**: The user required the product change to remain independent from the separate project whose review experience motivated the discussion.

### CON-004: Fail closed on incomplete coverage

- **Status**: confirmed
- **Statement**: If a mandatory system rule, review partition, root-cause variant search, or post-repair verification obligation cannot be completed, the defect-gate verdict must be `INCONCLUSIVE`, never `PASS`.
- **User Evidence**: The user confirmed the proposed fail-closed coverage rule.

### CON-005: Existing defect-gate safety remains effective

- **Status**: confirmed
- **Statement**: Existing Git target selection, requirement-awareness, risk profiles, read-only verification, finding admission, and reviewer-isolation protections must remain effective unless a confirmed requirement explicitly replaces them.
- **User Evidence**: The user confirmed preserving the existing defect-gate protections.

## Decisions

### DEC-001: Upgrade the result envelope to schema version 2

- **Status**: confirmed
- **Decision**: The `review-code` result envelope will use `schema_version: "2"` and treat the change as an explicit result-format upgrade.
- **Alternatives Rejected**: Keeping schema version 1 with optional fields that older callers may silently ignore; recording the new evidence only in prose.
- **Reason**: Coverage and repair handoff must be machine-checkable rather than advisory.
- **User Evidence**: "确认采用推荐的 schema v2，并将其作为一次明确的结果格式升级。"

### DEC-002: Callers own cross-round state

- **Status**: confirmed
- **Decision**: `review-code` emits structured coverage and follow-up obligations, while its caller retains and supplies the relevant neutral records during a repair loop. The command does not own persistent storage.
- **Alternatives Rejected**: Automatically writing `.codexspec/reviews/` or another state file into the reviewed repository.
- **Reason**: The review remains read-only and does not contaminate the Git target it is evaluating.
- **User Evidence**: The user selected the recommended read-only structured-result handoff.

### DEC-003: Result and resolver schemas remain separate

- **Status**: confirmed
- **Decision**: Schema version 2 applies to the `review-code` result envelope. The Git review-context resolver manifest remains an independent protocol and changes only if implementation evidence demonstrates a separate need.
- **Alternatives Rejected**: Bumping unrelated protocols solely to give all schemas the same version number.
- **Reason**: Git target resolution and review evidence are separate compatibility boundaries.
- **User Evidence**: The user confirmed the proposed scope of the result-format upgrade.

### DEC-004: Apply systematic coverage to defect-gate mode

- **Status**: confirmed
- **Decision**: The new system-rule analysis, root-cause variant analysis, coverage tracking, and repair handoff apply to defect-gate mode. The advisory `--audit` quality scorecard keeps its separate purpose and output.
- **Alternatives Rejected**: Expanding the advisory path audit into a stateful repair gate.
- **Reason**: The reported inefficiency occurs in repeated change review and repair, not in path-level quality scoring.
- **User Evidence**: The user confirmed the proposed defect-gate-only scope.

## Out of Scope

### OUT-001: Guaranteed exhaustive defect discovery

- **Status**: confirmed
- **Statement**: The feature does not claim mathematical proof that one review will find every possible defect.
- **Reason**: It improves systematic coverage and first-round recall without making an unverifiable completeness promise.
- **User Evidence**: The user confirmed this exclusion in the stage summary.

### OUT-002: Requiring repeated clean reviews

- **Status**: confirmed
- **Statement**: The feature does not require a fixed number of consecutive no-finding reviews before completion.
- **Reason**: Completion is based on explicit coverage and verification evidence rather than repetition count.
- **User Evidence**: The user confirmed this exclusion in the stage summary.

### OUT-003: Repository-local review state

- **Status**: confirmed
- **Statement**: The feature does not automatically persist cross-round review state inside the reviewed repository.
- **Reason**: Persistent repository mutation would violate the confirmed read-only boundary and alter subsequent Git targets.
- **User Evidence**: The user confirmed the recommended read-only handoff design.

### OUT-004: Source-incident examples in product artifacts

- **Status**: confirmed
- **Statement**: Product requirements and downstream artifacts will not name or encode the source incident used to motivate the feature.
- **Reason**: Such references would be semantically irrelevant and would undermine the source-independent product requirement.
- **User Evidence**: The user explicitly rejected naming or binding the product requirement to the separate source incident.

## Open Questions

None.

## Superseded Entries

None.

## Confirmation Log

### Session 2026-08-29 00:35 CST

- **Summary Presented**: Eight needs, five constraints, four decisions, and four exclusions covering source-independent systematic review, system-wide consistency rules, root-cause variant analysis, complete review execution, schema-v2 coverage tracking, and read-only repair handoff.
- **User Confirmation**: Confirmed, with the correction that product artifacts must not mention or depend on the source incident or repository.
- **Entries Confirmed**: NEED-001 through NEED-008; CON-001 through CON-005; DEC-001 through DEC-004; OUT-001 through OUT-004.
