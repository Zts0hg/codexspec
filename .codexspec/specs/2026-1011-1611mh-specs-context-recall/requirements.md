# Confirmed Requirements: Specs Context Recall

**Feature ID**: `2026-1011-1611mh`
**Status**: Confirmed
**Last Confirmed**: 2026-10-11

## Authority Rules

- Only entries with `Status: confirmed` are binding downstream inputs.
- Open proposals and agent assumptions are not confirmed requirements.
- Preserve replaced confirmed entries as `superseded` with replacement references.
- The final stage summary was explicitly confirmed; all binding entries below form the approved requirements baseline.

## Needs

### NEED-001: Reconstruct decision history before asking the user

- **Status**: confirmed
- **Statement**: Discover relevant historical feature artifacts under `.codexspec/specs/` and reconstruct how related user decisions evolved across iterations. Prepare this background before asking questions about the current task, supporting reuse of experience and deliberate decision changes.
- **Rationale**: Finding related documents alone does not explain which decisions continued, which were supplemented, and which changed.
- **User Evidence**: The user described specs as a way to revisit designs and decisions during long-term iteration and confirmed organizing their evolution as background before questioning: "没错，就是这个意思".
- **Confirmed At**: 2026-10-11

### NEED-002: Reduce unnecessary questioning

- **Status**: confirmed
- **Statement**: Use applicable historical decisions to improve question precision and reduce unnecessary questioning. Do not ask users to reconstruct information already available in relevant history. When continued applicability needs confirmation, present the known background and ask a concise question. When the relationship between earlier and later decisions is unclear, expose the specific difference instead of silently choosing an interpretation.
- **User Evidence**: "作为问询之前的背景信息整理来提高问询的准确度和降低问询的繁琐程度（因为有些可以从历史经验中得到的就不需要问询，或者是可以简单问询快速确认）"; subsequent confirmation of the corrected decision-history summary.
- **Confirmed At**: 2026-10-11

### NEED-003: Apply recall across substantive work and both agent integrations

- **Status**: confirmed
- **Statement**: Apply on-demand historical recall in ordinary conversation and SDD workflows whenever work involves requirements, behavior, design, debugging, implementation, or review judgments. Provide consistent coverage through both Codex and Claude entry points.
- **User Evidence**: The user replied "确认" to the scenario summary covering ordinary conversation, SDD workflows, substantive judgments, and both agent integrations.
- **Confirmed At**: 2026-10-11

### NEED-004: Match retrieval depth to the scenario

- **Status**: confirmed
- **Statement**: Use the following scenario-specific depth when recalling relevant historical artifacts. The ordinary-conversation and integration coverage in NEED-003 applies throughout.

| Scenario | Required depth and purpose |
|---|---|
| Requirements discussion, specify, quick, and blueprint | Reconstruct the decision timeline from related requirements. Read design rationale when needed to explain a trade-off. Establish known background, current requirements, and differences needing confirmation. |
| Design and planning | Work from confirmed requirements and consult relevant historical designs, alternatives, and trade-offs. Read implementation plans when implementation experience is relevant. |
| Implementation and debugging | Establish expected behavior and its successive changes, then use relevant design, code, and tests to assess the current state. Historical plans alone do not establish that a behavior was implemented. |
| Code review | Trace concrete changes and concerns to relevant requirements and designs to assess divergence from current requirements, compatibility implications, or repetition of existing problems. |

- **User Evidence**: "确认" in response to the scenario-depth table and common retrieval rules.
- **Confirmed At**: 2026-10-11

### NEED-005: Select related features and trace their decision evolution

- **Status**: confirmed
- **Statement**: First identify related features, then examine their earlier and later additions and adjustments along the decision timeline. Do not stop at the first matching document when related decisions may have evolved. Retrieve the artifacts needed for the current scenario rather than loading all historical documents.
- **User Evidence**: Explicit confirmation of "先筛选，再沿时间线理解" and the requirement to inspect preceding and subsequent additions and changes instead of stopping at the first match.
- **Confirmed At**: 2026-10-11

## Constraints

### CON-001: Honor the user's latest explicit decision

- **Status**: confirmed
- **Statement**: Historical specs must never replace or overrule the user's latest explicit decision in the current interaction. Use history to explain changes from earlier decisions and identify implications. Do not repeatedly ask the user to decide the same matter merely because the new decision differs from historical requirements.
- **User Evidence**: "这些历史不应该在任何情况下取代最新的用户问询时给出的决策"; explicit confirmation of the corrected summary.

### CON-002: Stop when the background supports the current judgment

- **Status**: confirmed
- **Statement**: Stop extending retrieval when the relevant requirements, decision evolution, and applicability are sufficiently understood to support the current judgment. Do not expand into unrelated history. If a material ambiguity remains, present the specific difference in a concise question rather than silently choosing an interpretation.
- **User Evidence**: Explicit confirmation of the proposed stopping rule and targeted questioning for unresolved material ambiguity.

### CON-003: Reuse prepared background and supplement it when needed

- **Status**: confirmed
- **Statement**: Reuse background already assembled instead of rescanning at every workflow stage. Supplement retrieval when task scope changes, new evidence appears, or existing background no longer supports the judgment required. Reuse does not authorize treating incomplete background as sufficient.
- **User Evidence**: Explicit confirmation of "复用已经整理的背景" and the three triggers for additional retrieval.

## Decisions

### DEC-001: Requirements are authoritative records along a decision timeline

- **Status**: confirmed
- **Decision**: User-confirmed content in each feature's `requirements.md` is an authoritative record of decisions established through user interaction. Feature-directory timestamps express the chronology of long-term iteration and help identify older and newer decisions. Do not conflate a decision's age with its authority or reduce the authority of a requirement merely because it is old.
- **Reason**: Recall must reconstruct the evolution of authoritative user decisions over time.
- **User Evidence**: "specs中requirements是用户直接问询交互记录下了的直接需求确定内容，都具有权威性。而时间顺序代表在长期迭代过程中的时间线上，决策的新旧。"; "没错，就是这个意思".

### DEC-002: Distinguish continuations, additions, and explicit changes

- **Status**: confirmed
- **Decision**: Earlier requirements remain applicable when later decisions have not changed them. Combine supplementary decisions with earlier requirements to understand the complete requested behavior. When a later decision explicitly changes the same matter, use it to determine the updated requirement and retain the earlier record to explain the prior rationale. If the relationship is unclear, ask a targeted question rather than assuming an earlier requirement expired. The user's latest explicit decision in the current interaction takes precedence over historical specs.
- **User Evidence**: Explicit confirmation of the summary distinguishing unchanged earlier requirements, later additions, explicit changes, unclear relationships, and current-interaction decisions: "没错，就是这个意思".

## Out of Scope

### OUT-001: Mechanical edits need not trigger historical recall

- **Status**: confirmed
- **Statement**: Purely mechanical edits, such as formatting or spelling corrections, may omit historical recall when they involve none of the substantive judgments covered by NEED-003.
- **Reason**: Avoid unnecessary retrieval when historical requirements and design decisions cannot affect the task's judgment.
- **User Evidence**: The user replied "确认" to the scope summary explicitly allowing this exemption.

## Open Questions

### OPEN-001: Scenarios and coverage boundaries

- **Status**: resolved
- **Question**: Which ordinary conversations and SDD stages must perform historical recall, and which tasks may omit it?
- **Resolution**: NEED-003 confirms substantive-work coverage in ordinary conversation and SDD workflows for Codex and Claude. OUT-001 permits omission for purely mechanical edits.
- **User Evidence**: "确认" in response to the scope summary.
- **Blocks Specification**: no

### OPEN-002: Retrieval depth, stopping, and repeated use

- **Status**: resolved
- **Question**: For each confirmed scenario, how far must recall proceed, when is the background sufficient, and when must an agent revisit it?
- **Resolution**: NEED-004 specifies scenario-dependent depth; NEED-005 requires selection and decision-history tracing; CON-002 defines stopping and clarification; CON-003 defines background reuse and additional-retrieval triggers.
- **User Evidence**: "确认" in response to the complete retrieval-depth and stopping-rule proposal.
- **Blocks Specification**: no

## Superseded Entries

None. The corrected wording about chronology was an unconfirmed discussion proposal, not a previously confirmed requirement.

## Confirmation Log

### 2026-10-11 — Decision authority and chronology

- **Summary Presented**: Reconstruct the evolution of authoritative requirements along the specs timeline before questioning. Older unchanged decisions remain applicable; later additions complement them; later explicit changes update the same matter. Clarify ambiguous relationships and honor the user's latest explicit decision.
- **User Confirmation**: "没错，就是这个意思".
- **Entries Confirmed**: NEED-001, NEED-002, CON-001, DEC-001, DEC-002.
- **Remaining Discovery**: OPEN-001 and OPEN-002. This is an intermediate confirmation; do not auto-advance to specification generation.

### 2026-10-11 — Scenario coverage

- **Summary Presented**: Apply on-demand recall to requirements, behavior, design, debugging, implementation, and review judgments in ordinary conversation and SDD workflows, consistently across Codex and Claude. Purely mechanical edits may omit recall.
- **User Confirmation**: "确认".
- **Entries Confirmed**: NEED-003, OUT-001.
- **Questions Resolved**: OPEN-001.
- **Remaining Discovery**: OPEN-002. Retrieval depth and stopping conditions still require discussion; this is not final discovery approval.

### 2026-10-11 — Retrieval depth and stopping conditions

- **Summary Presented**: Match retrieval depth to requirements discussion, design/planning, implementation/debugging, and code review. Select related features and trace earlier/later decisions instead of stopping at the first match. Stop when the background supports the current judgment, clarify material ambiguity, and supplement existing background only when scope, evidence, or judgment needs change.
- **User Confirmation**: "确认".
- **Entries Confirmed**: NEED-004, NEED-005, CON-002, CON-003.
- **Questions Resolved**: OPEN-002.
- **Remaining Discovery**: No unresolved product questions from the discussion. Present the consolidated final stage summary for confirmation before automatic specification generation.

### 2026-10-11 — Final stage summary

- **Summary Presented**: Recall related decisions before questioning to reuse experience and reduce repeated inquiry. Cover substantive ordinary conversation and SDD work in Codex and Claude, with an exemption for mechanical edits. Respect authoritative requirements along their decision timeline and the user's latest explicit decision. Retrieve to scenario-appropriate depth, stop when sufficient, and reuse or supplement prepared background as needed.
- **User Confirmation**: "确认" in direct response to the final requirements baseline and advancement to specification generation.
- **Entries Confirmed**: NEED-001 through NEED-005; CON-001 through CON-003; DEC-001 and DEC-002; OUT-001.
- **Open Questions**: None; OPEN-001 and OPEN-002 are resolved.
- **Completion**: Discovery complete. Advance to generate-spec under the enabled auto_next setting.
