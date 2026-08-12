# Design Document: [FEATURE NAME]

<!--
Language: Generate this document in the language specified in .codexspec/config.yml
If not configured, use English.

This is the design stage between spec.md and plan.md. It describes WHAT the system is
(architecture, components, interfaces, key design decisions) — NOT how to build it in
phases (that belongs in plan.md).

Scale to complexity: the fixed core below is always present; the optional sections appear
ONLY when the feature warrants them. A trivial feature may be a thin page whose Key Design
Decisions section simply records "no significant design decisions". Do not add a section
merely because the template contains it.
-->

**Related Spec**: `.codexspec/specs/{feature-id}/spec.md`
**Confirmed Requirements**: `.codexspec/specs/{feature-id}/requirements.md`
**Created**: [DATE]
**Status**: Draft

<!-- ===================== FIXED CORE (always present) ===================== -->

## Context

<!-- Brief background inherited from the spec: what this design serves, current state. -->

## Architecture & Components

<!--
The shape of the system and the responsibility of each component/interface.
Every component or interface carries a Covers line tracing it to the requirement(s)
it realizes. Keep this at the design level (what each piece is and does), not an
implementation phase plan.
-->

### [Component / Interface name]

- **Responsibility**: <!-- what this component/interface is responsible for -->
- **Interface**: <!-- inputs/outputs, contracts, or collaborators (as relevant) -->
- **Covers**: REQ-xxx

<!-- Repeat per component. Add a diagram only if it materially aids understanding. -->

## Key Design Decisions

<!--
ADR-lite. One entry per material design decision. For a trivial feature with none,
state "No significant design decisions." explicitly.
-->

### Decision 1: [Title]

- **Context**: <!-- why this decision was needed -->
- **Decision**: <!-- the chosen option -->
- **Alternatives**: <!-- options considered, when material -->
- **Trade-offs**: <!-- what is accepted/given up -->
- **Covers**: REQ-xxx

<!-- ===================== OPTIONAL SECTIONS (include only if warranted) ===================== -->

## Data Models / Key Entities *(include if the feature involves data)*

<!-- Entities, fields, relationships, constraints. Each entity Covers a requirement. -->

| Entity | Field | Type | Constraints | Covers |
|--------|-------|------|-------------|--------|
| [Name] | [field] | [type] | [constraints] | REQ-xxx |

## API / Interface Contracts *(include if the feature exposes an API or CLI surface)*

<!-- Request/response shapes, commands, error behavior. Each contract Covers a requirement. -->

## Sequence & Data Flow *(include if control/data flow across components is non-obvious)*

<!-- Ordered interactions or a data-flow description; a diagram is optional. -->

## Cross-Cutting Design *(include if performance / security / availability shape the design)*

<!-- Design-level treatment of non-functional concerns (not an implementation checklist). -->

## Risks & Trade-offs *(include if design carries material risk)*

| Risk | Impact | Mitigation |
|------|--------|------------|
| [risk] | [impact] | [mitigation] |

<!-- ===================== REQUIREMENTS COVERAGE (always present) ===================== -->

## Requirements Coverage

| Spec Requirement | Design Coverage |
|------------------|-----------------|
| REQ-xxx | Component / Decision reference |
| NFR-xxx | Component / Decision reference |
