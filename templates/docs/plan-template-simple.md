# Implementation Plan: [FEATURE NAME]

<!--
Language: Generate this document in the language specified in .codexspec/config.yml
If not configured, use English.

This is the implementation-planning stage AFTER design.md. It describes HOW to build the
confirmed design — NOT what the system is. Architecture, components, interfaces, and design
decisions live in design.md; reference them here, do not restate them.
-->

Use the smallest structure that delivers the approved design. Add phases, decisions, or
support work only when the design, repository policy, or verified implementation needs them.

## Context

<!-- Background and current state; which design this plan delivers. -->

## Goals / Non-Goals

**Goals:**

- <!-- What this implementation aims to achieve -->

**Non-Goals:**

- <!-- What is explicitly out of scope -->

## Plan-Level Decisions

<!-- Implementation-level choices only (build ordering, tooling, sequencing). Architecture and
design decisions belong to design.md. -->

### Decision 1: [Title]

**Context**: <!-- Why this implementation decision was needed -->
**Decision**: <!-- The chosen option -->
**Rationale**: <!-- Why this option was chosen -->

## Implementation Notes / Phases

<!-- Ordered implementation steps, each tracing to design. -->

- [ ] [Step] — **Covers**: REQ-xxx; Design: [component]

## Verification Strategy

- **Covers**: [requirement or acceptance criterion and planned step]
- **Check and expected result**: [existing test, command, or deterministic inspection and observable outcome]
- **Prerequisites**: [environment, fixtures, or dependencies only when needed]

Keep this section about planned checks. Report actual commands, results, and the tested
revision during implementation and review; a planned check is not evidence that it passed.
Use test-first ordering only when required by the constitution, specification, plan, or
established repository workflow.

## Risks / Trade-offs

| Risk | Impact | Mitigation |
|------|--------|------------|
| <!-- risk --> | <!-- impact --> | <!-- mitigation --> |

## Requirements Coverage

| Spec Requirement | Design Component | Plan Coverage | Planned Verification |
|------------------|------------------|---------------|----------------------|
| REQ-xxx / NFR-xxx | [design component] | Decision/step reference | Check and expected result reference |
