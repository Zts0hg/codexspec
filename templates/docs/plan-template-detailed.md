# Implementation Plan: [FEATURE NAME]

<!--
Language: Generate this document in the language specified in .codexspec/config.yml
If not configured, use English.

This is the implementation-planning stage AFTER design.md. It describes HOW to build the
confirmed design in phases — NOT what the system is. Architecture, components, interfaces,
data models, and API contracts live in design.md; reference them here, do not restate them.
-->

**Related Spec**: `.codexspec/specs/{feature-id}/spec.md`
**Related Design**: `.codexspec/specs/{feature-id}/design.md`
**Confirmed Requirements**: `.codexspec/specs/{feature-id}/requirements.md`
**Created**: [DATE]
**Status**: Draft

Scale this template to the approved design. Use its organization rather than imposing a
fixed set of phases. Include setup, migrations, documentation, or other support work only
when required by that design, repository policy, or a verified implementation need.

## Context

<!-- Background and current state. What does this plan deliver, and against which design? -->

## Goals / Non-Goals

**Goals:**

- [What this implementation aims to achieve]
- [Specific outcomes]

**Non-Goals:**

- [What is explicitly out of scope]
- [What will be deferred to future iterations]

## Relevant Repository Constraints

- [Verified implementation constraint, existing pattern, or reusable dependency and its source]
- [Reference the approved design's technology choices; do not introduce a stack here]

## Plan-Level Decisions

<!--
Implementation-level choices only: build ordering, tooling, sequencing, test strategy.
Architecture / interface / data-model / ADR-style decisions belong to design.md — do not
duplicate them here.
-->

### Decision 1: [Title]

**Context**: [Why this implementation decision was needed]

**Options Considered**:

1. [Option A]
2. [Option B]

**Decision**: [Chosen option]

**Rationale**: [Why this option was chosen]

**Covers**: REQ-001; Design: [design component]

**Decision Level**: Plan-level implementation decision; does not change confirmed product scope or the confirmed design

## Risks / Trade-offs

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| [Risk 1] | High/Medium/Low | High/Medium/Low | [How to mitigate] |
| [Risk 2] | ... | ... | ... |

## Implementation Phases

### [Phase or implementation unit from the approved design]

- **Outcome**: [One independently verifiable result]
- **Covers**: REQ-xxx; Design: [component]
- **Changes**: [Known paths and implementation steps; do not invent paths]
- **Dependencies**: [Required predecessor and the result it supplies, or none]
- **Verification**: [Reference the planned check below]

Repeat only for the units the feature needs. Order verification with the work it checks;
use test-first ordering only when required by the constitution, specification, plan, or
established repository workflow.

## Verification Strategy

| Requirement / Acceptance Criterion | Plan Unit | Check and Expected Result | Prerequisites |
|------------------------------------|-----------|---------------------------|---------------|
| REQ-xxx / NFR-xxx / [criterion] | [unit] | [Existing test, command, or deterministic inspection and observable outcome] | [Environment / fixture / dependency, or none] |

Reference existing checks before planning new ones. Include applicable boundary, failure,
compatibility, and recovery checks derived from the confirmed behavior. Documentation and
configuration work use their appropriate deterministic checks rather than invented code tests.

These are planned checks, not execution evidence. Actual commands, results, tested revision,
and remaining coverage gaps are reported during implementation and review.

## Requirements Coverage

| Spec Requirement | Design Component | Plan Coverage | Planned Verification |
|------------------|------------------|---------------|----------------------|
| REQ-xxx / NFR-xxx | [design component] | Decision / implementation unit reference | Check and expected result reference |
