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

## Context

<!-- Background and current state. What does this plan deliver, and against which design? -->

## Goals / Non-Goals

**Goals:**

- [What this implementation aims to achieve]
- [Specific outcomes]

**Non-Goals:**

- [What is explicitly out of scope]
- [What will be deferred to future iterations]

## Tech Stack

- **Language**: [e.g., Python 3.11]
- **Framework**: [e.g., FastAPI]
- **Database**: [e.g., PostgreSQL]
- **Frontend**: [e.g., React]
- **Infrastructure**: [e.g., Docker, AWS]

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

<!-- Each phase/unit carries Covers: REQ-xxx; Design: <design component>. -->

### Phase 1: Foundation

- [ ] [Task] — **Covers**: REQ-xxx; Design: [component]
- [ ] Configure dependencies / project structure

### Phase 2: Core Implementation

- [ ] [Task] — **Covers**: REQ-xxx; Design: [component]

### Phase 3: Testing

- [ ] Write unit tests
- [ ] Write integration tests

### Phase 4: Documentation & Polish

- [ ] Update documentation
- [ ] Final verification

## Requirements Coverage

| Spec Requirement | Design Component | Plan Coverage |
|------------------|------------------|---------------|
| REQ-001 | [design component] | Decision 1 / Phase 2 |
