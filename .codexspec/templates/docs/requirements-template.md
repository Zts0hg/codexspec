# Confirmed Requirements: [FEATURE NAME]

<!--
Language: Maintain this document in the language specified in .codexspec/config.yml.
This file is the authoritative, persistent record of user-confirmed intent.
Do not copy the full conversation. Keep only confirmed decisions and short evidence
quotes needed to resolve later interpretation disputes.
-->

**Feature ID**: `[feature-id]`
**Status**: Discovery
**Last Confirmed**: [DATE]

## Authority Rules

- Only entries with `Status: confirmed` are binding downstream inputs.
- `open` entries MUST NOT be converted into confirmed product requirements.
- Replaced entries remain in this file with `Status: superseded` and a link to the replacement.
- AI inferences must be labeled as assumptions and require user confirmation before becoming binding.

## Needs

### NEED-001: [User goal or required behavior]

- **Status**: open
- **Statement**: [What outcome the user confirmed]
- **Rationale**: [Why it matters]
- **User Evidence**: "[Short quote or concise paraphrase from the confirmed discussion]"
- **Confirmed At**: [DATE/TIME]

## Constraints

### CON-001: [Constraint name]

- **Status**: open
- **Statement**: [Boundary, compatibility, policy, timing, or technology constraint]
- **User Evidence**: "[Short supporting quote or paraphrase]"

## Decisions

### DEC-001: [Decision title]

- **Status**: open
- **Decision**: [Chosen option]
- **Alternatives Rejected**: [Only alternatives explicitly discussed]
- **Reason**: [User-confirmed reason]
- **User Evidence**: "[Short supporting quote or paraphrase]"

## Out of Scope

### OUT-001: [Excluded item]

- **Status**: open
- **Statement**: [What is excluded]
- **Reason**: [Why it is excluded]
- **User Evidence**: "[Short supporting quote or paraphrase]"

## Open Questions

### OPEN-001: [Question]

- **Status**: open
- **Why It Matters**: [Which downstream decision this blocks]
- **Owner**: User / Team / Research

## Superseded Entries

### DEC-000: [Previous decision]

- **Status**: superseded
- **Replaced By**: DEC-001
- **Historical Note**: [Why the decision changed]

## Confirmation Log

### Session [DATE/TIME]

- **Summary Presented**: [Concise stage summary shown to the user]
- **User Confirmation**: [Explicit confirmation]
- **Entries Confirmed**: NEED-001, CON-001, DEC-001, OUT-001
