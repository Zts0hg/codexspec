# Confirmed Requirements: Context-Aware Requirement Discovery

**Feature ID**: `2026-1127-11329b`
**Status**: Confirmed
**Last Confirmed**: 2026-11-27

## Authority Rules

- Only entries with `Status: confirmed` are binding downstream inputs.
- Open entries are discovery candidates, not confirmed requirements. AI inferences require explicit confirmation.
- Preserve replaced confirmed entries as `superseded`, with replacement references.
- The user explicitly confirmed the consolidated final summary on 2026-11-27. Discovery is complete; all needs, constraints, decisions, and exclusions below are confirmed.

## Relevant Background

- [Historical recall requirements](../2026-1011-1611mh-specs-context-recall/requirements.md), NEED-001/002 and CON-002/003, require preparing decision history before questioning, reusing knowledge, and stopping retrieval when sufficient.
- [Automatic advancement requirements](../2026-0629-22061u-auto-next-command/requirements.md), DEC-001, retain automatic entry into implementation after stage gates, without an additional implementation confirmation prompt.
- At baseline commit b908ffa2f1f82ec2e5e23bc95ca1cc09cf2e6464, the [specify source](../../../internal/command_templates/sources/specify.md) has no explicit requirement to verify current functionality or independently obtain retrievable information. Its auto_next instruction controls completion-time advancement rather than discovery depth.
- [Current design rules](../../../internal/command_templates/sources/spec-to-design.md) require user decisions for materially different outcomes and changes to confirmed intent, while allowing technical refinement that preserves intent.

## Needs

### NEED-001: Ground clarification in current functionality

- **Status**: confirmed
- **Statement**: Before substantive questioning, inspect the relevant current implementation, actual functionality, calls, and dependencies. Use verified facts to formulate applicable questions and answer factual matters already established by inspection. Do not ask questions premised on functionality or relationships the inspected implementation does not have.
- **Rationale**: Questions must follow verified implementation evidence rather than assumptions about names, descriptions, implementation status, or relationships. In the user's illustrative removal scenario, content may be classified as a placeholder only after inspection establishes that result.
- **User Evidence**: The initial request asks for clarification based on current code functionality, using removal of placeholder frontend content as the example.

### NEED-002: Adjust discovery to the automatic advancement setting

- **Status**: confirmed
- **Statement**: Read the applicable workspace's workflow.auto_next before substantive discovery; it defaults to disabled and only literal true enables it. When enabled, identify foreseeable user decisions affecting subsequent specification, design, planning, or implementation and resolve them before final confirmation. An item is not non-blocking merely because specification generation can proceed if automated downstream work still requires a user decision. When disabled, retain normal staged clarification without moving every later technical choice into specify. Current-state verification and autonomous information gathering apply in both modes.
- **User Evidence**: The initial request asks specify to account for auto_next and confirm details requiring user decisions before autonomously advancing subsequent stages.

### NEED-003: Obtain retrievable information before requesting it from the user

- **Status**: confirmed
- **Statement**: Before requesting factual information, determine whether relevant available code, documentation, configuration, history, logs, tests, or other accessible tools and sources can supply or establish it. Within the task's scope and existing authorization, collect and investigate it first. Do not ask users to locate information or perform checks the agent can perform itself. If necessary information remains unavailable, contradictory, or inconclusive after targeted investigation, briefly state what is known and the specific evidence gap, then ask only for the missing information. Apply DEC-001 to questions about intent and choices; collected facts do not substitute for user decisions.
- **Rationale**: Reduce user effort and improve the evidence supporting clarification.
- **User Evidence**: The user reports that specify asks users for information that autonomous collection and investigation could obtain, and explicitly requests optimizing this behavior.

## Constraints

### CON-001: Distinguish verified facts, user intent, and inference

- **Status**: confirmed
- **Statement**: Distinguish implementation facts, confirmed intent, and unverified assumptions. An unsuccessful search does not prove absence. When relevant code does not exist or cannot be inspected, state the available evidence and uncertainty. Existing behavior does not automatically become a requirement to preserve it.
- **Basis**: Boundary for NEED-001, confirmed in the consolidated final summary.

### CON-002: Preserve confirmation and downstream stop conditions

- **Status**: confirmed
- **Statement**: Preserve explicit final-summary confirmation, existing advancement gates, and downstream requests for newly discovered user decisions. Frontloading foreseeable questions does not authorize guessing when an unforeseeable material decision appears later. Topic confirmation must not start the automatic chain.
- **Basis**: Existing advancement and design rules, retained by the consolidated final confirmation.

### CON-003: Keep information gathering proportionate and reusable

- **Status**: confirmed
- **Statement**: Investigate sources and execution paths needed for the current judgment, without requiring a repository-wide audit or exhaustive diagnosis. Stop when evidence is sufficient. Reuse collected evidence; supplement it when scope changes, new evidence appears, or existing evidence is insufficient. Do not repeatedly perform the same failed checks or indefinitely expand retrieval instead of identifying the remaining gap.
- **Basis**: Boundary for NEED-001 and NEED-003, consistent with historical-recall stopping and reuse rules and confirmed in the final summary.

## Decisions

### DEC-001: Reserve material outcome and trade-off choices for the user

- **Status**: confirmed
- **Decision**: The user decides choices affecting behavior, scope, compatibility, and important cost or maintenance trade-offs. The agent may independently select equivalent technical implementations that satisfy the same confirmed requirements.
- **Alternatives Rejected**: Requiring individual user confirmation for every architecture or dependency choice, including equivalent implementations without material differences in outcomes or trade-offs.
- **Reason**: Obtain user decisions where they affect intended outcomes while retaining autonomy over equivalent engineering choices.
- **User Evidence**: "确认DEC-001。"
- **Confirmed At**: 2026-11-27

## Out of Scope

### OUT-001: Limit the change to specify's discovery behavior

- **Status**: confirmed
- **Statement**: Focus on specify and its corresponding distributed and installed forms. Do not extend the behavior to other entry points, add configuration switches, or produce complete design and implementation plans during specify.
- **Basis**: Scope boundary confirmed in the consolidated final summary.

## Open Questions

### OPEN-001: Confirm the complete discovery baseline

- **Status**: resolved
- **Question**: Does the user confirm NEED-001 through NEED-003, CON-001 through CON-003, and OUT-001 as the complete baseline, including autonomous information gathering?
- **Why It Matters**: DEC-001 alone has explicit topic confirmation. The full baseline and final-stage completion still require confirmation.
- **Owner**: User
- **Blocks Specification**: no

- **Resolution**: The user confirmed the complete final summary, including all three needs, all three constraints, DEC-001, and OUT-001.

## Superseded Entries

None.

## Confirmation Log

### 2026-11-27 — User decision boundary

- **Summary Presented**: Choices affecting behavior, scope, compatibility, and important cost or maintenance trade-offs belong to the user; equivalent technical implementations may be selected autonomously.
- **User Confirmation**: "确认DEC-001。"
- **Entries Confirmed**: DEC-001.
- **Additional Request**: Collect and investigate independently retrievable information before asking the user to provide it; captured as NEED-003 for consolidated confirmation.
- **Stage**: Intermediate. Discovery remains open; no automatic advancement.

### 2026-11-27 — Final requirements baseline

- **Summary Presented**: The complete list covers code-grounded clarification; early auto_next-aware discovery across downstream stages; autonomous collection and investigation before requesting facts; fact/intent/inference separation; preserved final confirmation and downstream stop conditions; proportionate, reusable investigation; the confirmed user-decision boundary; and specify-only scope without new configuration or full design/planning during discovery.
- **User Confirmation**: "确认" in direct response to the complete requirements list.
- **Entries Confirmed**: NEED-001, NEED-002, NEED-003, CON-001, CON-002, CON-003, OUT-001. DEC-001 remains confirmed.
- **Questions Resolved**: OPEN-001.
- **Stage**: Final. Discovery is complete; no blocking open questions remain.

### 2026-11-27 — General question premises and inspection conclusions

- **User Correction**: "不一定是以\"前端\"或者\"前端标签\"作为推断起点，但是仍可能存在无依据的推断"; "\"占位内容\"是一个核查之后的结果而无法事先得知".
- **Interpretation**: NEED-001 and CON-001 already apply to any relevant question premise. Verify the premises determining a question or option before treating them as facts; keep unverified premises unknown; implementation-status classifications follow inspection. The frontend example illustrates a verified outcome and does not limit the rule.
- **Authority**: This corrects the implementation and specification wording to the existing confirmed requirements; no new product decision or superseding entry is introduced.
