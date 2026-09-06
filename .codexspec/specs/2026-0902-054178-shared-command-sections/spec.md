# Feature Specification: Shared Command Sections

<!--
Language: Generate this document in the language specified in .codexspec/config.yml
If not configured, use English.
-->

**Feature ID**: `2026-0902-054178`
**Created**: 2026-09-02
**Status**: Draft
**Input**: Confirmed requirements in `requirements.md`

## Context

CodexSpec maintainers currently repeat common literal text in multiple complete command templates. Manual duplication works, but a later change can require several coordinated edits and can leave copies inconsistent. The desired capability is an internal authoring and validation mechanism that centralizes such text without changing any command content delivered to users or making `codexspec init` aware of fragments.

## Goals

- Let maintainers define a literal command-text fragment once and reuse it from arbitrary command sources.
- Ensure every reference resolves consistently and cannot drift unnoticed.
- Detect fragment integrity problems in project validation and again before packaging or release.
- Preserve the complete command content and all user-visible behavior byte for byte.

## User Stories

### Story: Reuse literal command text

**As a** CodexSpec maintainer
**I want** arbitrary command sources to reuse centrally maintained literal fragments
**So that** I can change shared text once without maintaining independent handwritten copies.

**Acceptance Criteria:**

- [ ] A fragment can be referenced by any number of command sources without adding command- or section-specific mechanism code.
- [ ] A fragment is inserted literally and accepts no parameters.
- [ ] A command source can reference fragments, but a fragment cannot reference another fragment.

### Story: Prevent maintenance defects from reaching users

**As a** CodexSpec maintainer
**I want** fragment integrity and synchronization checked before distribution
**So that** users never discover a fragment defect while running `codexspec init`.

**Acceptance Criteria:**

- [ ] Normal project tests and CI reject missing fragments, forbidden nesting, stale synchronized content, and other fragment-integrity failures.
- [ ] Packaging or release validation independently rejects the same invalid state.
- [ ] Complete command content remains byte-for-byte identical to the equivalent manually duplicated form.
- [ ] `codexspec init` does not parse, expand, or validate fragment references and retains its existing observable behavior.

## Requirements

### Functional Requirements

- **REQ-001**: The project MUST provide a generic maintainer-side mechanism through which arbitrary command sources can reuse arbitrary shared command-text fragments.
  - Sources: NEED-001, DEC-001
- **REQ-002**: The mechanism MUST insert fragment content literally and MUST NOT support fragment parameters in its first version.
  - Sources: DEC-002
- **REQ-003**: Command sources MAY reference one or more fragments, but fragment content MUST NOT reference another fragment in the first version.
  - Sources: DEC-003
- **REQ-004**: The project MUST synchronize or validate every command location that references a shared fragment so that a fragment change cannot leave an accepted stale copy.
  - Sources: NEED-002
- **REQ-005**: Normal project tests and CI MUST reject missing fragments, forbidden nesting, stale synchronized content, and any other state in which fragment references cannot produce the required complete command content.
  - Sources: NEED-002, CON-003, DEC-003
- **REQ-006**: Packaging or release validation MUST independently reject every fragment-integrity failure covered by REQ-005 before producing or publishing a user distribution.
  - Sources: CON-003
- **REQ-007**: `codexspec init` and command execution MUST NOT parse, expand, or validate fragment references.
  - Sources: CON-001, OUT-002

### Non-Functional Requirements

- **NFR-001**: Complete command content produced through the fragment mechanism MUST be byte-for-byte identical to the equivalent complete command content maintained through manual duplication.
  - Sources: CON-002
- **NFR-002**: The feature MUST preserve the existing interface, workflow, error behavior, user experience, and observable effects of `codexspec init`.
  - Sources: CON-001
- **NFR-003**: A user invocation of `codexspec init` MUST NOT be the first point at which any fragment-integrity defect can be detected in a distributable CodexSpec version.
  - Sources: CON-003

## Acceptance Scenarios and Error Behavior

### Scenario: Reuse one fragment from multiple command sources

- **GIVEN** a valid literal fragment and multiple command sources that reference it
- **WHEN** the project-maintenance mechanism produces or validates the complete command content
- **THEN** every reference contributes exactly the fragment's literal bytes
- **AND** the complete command content is byte-for-byte identical to the corresponding manually duplicated form.

### Scenario: Use the mechanism with a previously unknown command or section

- **GIVEN** a command source and fragment that were not hard-coded into the mechanism
- **WHEN** the command source references that fragment
- **THEN** the generic mechanism handles the reference without requiring command- or section-specific implementation changes.

### Scenario: Reject a missing fragment before distribution

- **GIVEN** a command source that references a fragment that cannot be resolved
- **WHEN** normal project validation or packaging/release validation runs
- **THEN** the applicable gate fails
- **AND** no affected distribution is accepted or published.

### Scenario: Reject nested fragment use

- **GIVEN** a fragment whose content references another fragment
- **WHEN** normal project validation or packaging/release validation runs
- **THEN** the applicable gate fails because nested fragments are forbidden.

### Scenario: Reject stale complete command content

- **GIVEN** a fragment change whose corresponding complete command content has not been synchronized
- **WHEN** normal project validation or packaging/release validation runs
- **THEN** the applicable gate fails before the stale content can be distributed.

### Scenario: Initialize a user project

- **GIVEN** a valid CodexSpec distribution produced with the maintainer-side fragment mechanism
- **WHEN** a user runs `codexspec init`
- **THEN** initialization follows its existing path without parsing, expanding, or validating fragments
- **AND** its generated command content and observable behavior remain unchanged.

## Constraints and Confirmed Decisions

- The mechanism is generic across commands and section names.
- The first version supports literal, non-parameterized fragments only.
- The first version forbids fragments from referencing other fragments.
- Fragment handling remains entirely on the project-maintenance side and outside `codexspec init` and command execution.
- Both normal project validation and packaging/release validation are mandatory pre-distribution gates.

## Out of Scope

- Selecting which existing command text should become a fragment.
- Extracting any particular common text from existing command templates.
- Parameterized fragments.
- Nested fragment composition.
- Runtime or `codexspec init` fragment parsing, expansion, or validation.

## Open Questions

None.

## Requirements Traceability

| Confirmed Requirement | Spec Coverage | Notes |
|-----------------------|---------------|-------|
| NEED-001 | REQ-001; reuse story and scenarios | Central maintenance and arbitrary reuse |
| NEED-002 | REQ-004, REQ-005; prevention story and stale-content scenario | Synchronization and drift prevention |
| CON-001 | REQ-007, NFR-002; initialization scenario | `codexspec init` remains unaware and unchanged |
| CON-002 | NFR-001; byte-identical acceptance criteria and scenario | Exact compatibility |
| CON-003 | REQ-005, REQ-006, NFR-003; error scenarios | Two pre-distribution gates |
| DEC-001 | REQ-001; generic-use scenario | No command or section hard-coding |
| DEC-002 | REQ-002; literal-fragment acceptance criterion | No parameters in the first version |
| DEC-003 | REQ-003, REQ-005; nested-fragment error scenario | No nesting in the first version |
| OUT-001 | Out of Scope | Fragment selection and extraction excluded |
| OUT-002 | REQ-007; Out of Scope | No user-side parsing or expansion |
