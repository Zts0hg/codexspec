# Feature Specification: Context-Aware Requirement Discovery

**Feature ID**: 2026-1127-11329b
**Authority**: Confirmed requirements.md
**Status**: Reviewed — PASS (see review-spec.md)

## Context and Goals

At baseline commit b908ffa2f1f82ec2e5e23bc95ca1cc09cf2e6464, the specify command consults historical specs and the project profile, but does not explicitly require checking current functionality or independently collecting retrievable facts before asking the user. Its auto_next instruction governs completion-time advancement rather than the depth of discovery.

Improve the accuracy and usefulness of questions, reduce information-gathering work transferred to users, and resolve foreseeable user decisions before an enabled automatic chain reaches downstream design or implementation.

## ADDED Requirements

### REQ-001: Inspect current functionality before substantive questions

Sources: NEED-001, CON-001

Before substantive questioning, inspect the implementation relevant to the requested change, including actual behavior, callers, callees, and dependencies as needed to establish the question's premise. Use verified facts to answer factual matters already established by inspection and formulate only applicable questions.

Before deciding whether a question or option is applicable, verify the premises determining its applicability. Do not infer the existence, implementation status, relationships, or impact of functionality solely from surface descriptions. Treat unverified premises as unknown. Classifications such as placeholder, unused, or functional are conclusions established by inspection, not starting assumptions. Current behavior is evidence of the existing system, not authority over the user's desired change.

#### Scenario: Inspection establishes that requested frontend content is a placeholder

- WHEN a user asks to remove frontend content and inspection establishes that it is only a placeholder without a functional backend relationship,
- THEN explain that relevant fact and clarify only applicable intent or scope choices; do not ask whether nonexistent backend functionality should also be removed.

#### Scenario: A name or description suggests unverified functionality

- WHEN a request, interface, name, or document description suggests functionality, implementation status, a relationship, or an impact that current evidence has not established,
- THEN investigate the relevant implementation before deciding which question or option is applicable; retain any unresolved premise as unknown instead of presenting it as fact.

#### Scenario: Remove content with a real dependency

- WHEN inspection establishes a functional dependency whose treatment would materially affect scope or user outcomes,
- THEN explain the verified relationship and present the actual user decision rather than assuming either retention or removal.

### REQ-002: Independently collect accessible factual information

Sources: NEED-003, DEC-001

Before asking the user for factual information, determine whether relevant accessible code, documentation, configuration, historical records, logs, tests, or other available tools and sources can supply or establish it. Within the task's scope and existing authorization, obtain and investigate that information first.

Do not ask users to locate information or perform checks the agent can perform itself. Distinguish questions about user intent and choices from factual information retrieval.

#### Scenario: The requested information is accessible

- WHEN the location, configuration, behavior, or other needed fact can be established using available sources or targeted checks,
- THEN independently establish it and use the result instead of requesting that the user find the information or run the same check.

### REQ-003: Handle uncertainty without inventing facts or intent

Sources: NEED-001, NEED-003, CON-001, DEC-001

Distinguish verified implementation facts, confirmed intent, and unverified inferences. A failed search does not prove absence. If relevant code does not yet exist or cannot be inspected, state the available evidence and uncertainty and clarify from that basis.

If necessary information remains inaccessible, contradictory, or inconclusive after targeted investigation, briefly explain what is known and the specific gap, then request only the information needed to proceed. Autonomous fact-finding must not substitute for user decisions.

#### Scenario: Evidence remains insufficient

- WHEN targeted inspection cannot establish a required fact, including missing code, inaccessible sources, unresolved contradictions, or inconclusive checks,
- THEN state that limitation without claiming the feature does not exist and ask a focused question only if the missing fact is necessary for clarification.

### REQ-004: Bound investigation and reuse sufficient evidence

Sources: CON-003

Inspect sources and execution paths needed for the current judgment; do not require a repository-wide audit or exhaustive diagnosis. Stop when evidence supports that judgment. Reuse prepared evidence and supplement it only when scope changes, new evidence appears, or the existing evidence is insufficient.

Do not repeatedly perform the same failed checks or indefinitely expand retrieval instead of explaining the remaining gap.

#### Scenario: Existing evidence is adequate

- WHEN prepared evidence already answers the relevant factual question,
- THEN reuse it without repeating the investigation or transferring that work to the user.

#### Scenario: A source remains inaccessible

- WHEN a targeted check fails and repeating the same check adds no evidence,
- THEN identify the remaining gap rather than looping or searching unrelated areas.

### REQ-005: Read the automation setting before discovery

Sources: NEED-002

Read workflow.auto_next from the applicable workspace's configuration before substantive discovery. Preserve existing semantics: default disabled; only the literal boolean true enables automatic advancement. An absent setting, false, or another value is disabled.

Current-functionality verification and autonomous fact-gathering remain mandatory regardless of this setting.

#### Scenario: Automation is disabled

- WHEN auto_next is absent, false, or non-true,
- THEN perform code-grounded discovery and autonomous fact-gathering normally, without forcing every downstream technical choice into specify.

### REQ-006: Resolve foreseeable downstream user decisions in enabled mode

Sources: NEED-002, CON-002, DEC-001

When auto_next is enabled, examine foreseeable specification, design, planning, and implementation consequences before final discovery confirmation. Ask for the user decisions those stages would otherwise need, using evidence-backed viable choices.

Do not treat an unresolved item as non-blocking merely because specification generation can proceed. A foreseeable item that still requires a user decision during the automatic downstream work must be resolved before discovery is declared complete.

#### Scenario: A choice blocks design but not specification

- WHEN specification could be written but two downstream approaches create materially different user outcomes or important trade-offs,
- THEN obtain the user's choice during specify rather than deferring it as non-blocking.

### REQ-007: Preserve user decisions and equivalent engineering autonomy

Sources: DEC-001, NEED-002, NEED-003

Ask the user to decide choices affecting behavior, scope, compatibility, or important cost or maintenance trade-offs. Independently select equivalent technical implementations satisfying the same confirmed requirements.

Architecture and dependency choices are judged by their actual consequences; do not require separate approval for every purely technical choice. Do not infer user goals or preferences from collected facts.

#### Scenario: Equivalent implementation choices

- WHEN multiple technical implementations satisfy the same confirmed requirements without materially different outcomes or important trade-offs,
- THEN leave the choice to downstream engineering judgment instead of asking an unnecessary discovery question.

### REQ-008: Preserve confirmation and downstream stop conditions

Sources: CON-002, NEED-002

Retain explicit final-stage-summary confirmation, the existing completion report, and automatic-advancement gates and successor. Intermediate topic confirmation must not start the chain.

In enabled mode, discovery completion also requires resolution of the foreseeable downstream user decisions in REQ-006. After completion and explicit final confirmation, retain exactly one notice and one invocation of generate-spec. Frontloaded clarification does not authorize guessing about a previously unforeseeable material decision discovered later; downstream stop-and-ask rules remain applicable.

#### Scenario: Intermediate confirmation or unresolved foreseeable decision

- WHEN a topic alone is confirmed, or an enabled chain still has a foreseeable downstream user decision,
- THEN do not declare final discovery completion or automatically advance.

#### Scenario: A new decision appears downstream

- WHEN later evidence reveals a previously unforeseeable material choice,
- THEN retain the existing requirement to ask the user rather than treating discovery as blanket authority to choose.

### REQ-009: Keep the change within specify's existing scope and distribution

Sources: OUT-001

Apply the behavior to specify and its corresponding distributed template and installed Claude/Codex forms. Do not extend other command entry points, introduce configuration switches, or make specify produce full design or implementation-plan artifacts.

## Acceptance and Verification

Review the complete instruction contract against the scenarios above and verify source-to-template-to-installed-form consistency. Contract tests protect required rules and ordering; they do not prove universal model compliance during real conversations.

## Out of Scope

Changes to quick, blueprint, auto-dev, or other entry points; new configuration; full design or implementation plans produced within specify; changes to downstream authority or stop conditions.

## Open Questions and Assumptions

None. All binding behavior derives from confirmed requirements; no product assumptions are promoted to authority.

## Requirements Traceability

| Confirmed Entry | Specification Coverage |
|---|---|
| NEED-001 | REQ-001, REQ-003 |
| NEED-002 | REQ-005, REQ-006, REQ-007, REQ-008 |
| NEED-003 | REQ-002, REQ-003, REQ-007 |
| CON-001 | REQ-001, REQ-003 |
| CON-002 | REQ-006, REQ-008 |
| CON-003 | REQ-004 |
| DEC-001 | REQ-002, REQ-003, REQ-006, REQ-007 |
| OUT-001 | REQ-009 |
