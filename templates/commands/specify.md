---
description: Create a new feature specification describing what to build and why
handoffs:
  - agent: claude
    step: Generate feature specification from user requirements
---

# Feature Specification Generator

## Language Preference

**IMPORTANT**: Before proceeding, read the project's language configuration from `.codexspec/config.yml`.
- If `language.output` is set to a language other than "en", respond and generate all content in that language
- If not configured or set to "en", use English as default
- Technical terms (e.g., API, JWT, OAuth) may remain in English when appropriate
- All user-facing messages, questions, and generated documents should use the configured language

## User Input

$ARGUMENTS

## Instructions

You are tasked with creating a detailed feature specification. Focus on the **what** and **why**, not the technical implementation.

### Steps

1. **Understand Requirements**: Parse the user's input to understand what feature they want to build.

2. **Review Constitution**: Read `.codexspec/memory/constitution.md` to understand project principles.

3. **Create Feature Branch**: Create a new feature branch using the naming convention `NNN-feature-name` (e.g., `001-user-authentication`).

4. **Create Feature Directory**: Create `.codexspec/specs/{feature-id}/` directory.

5. **Generate Specification**: Create a comprehensive spec document including:
   - Feature overview and goals
   - User stories with acceptance criteria
   - Functional requirements
   - Non-functional requirements
   - Edge cases and constraints
   - Out of scope items

6. **Save Specification**: Write to `.codexspec/specs/{feature-id}/spec.md`

### Reference Templates

Use the following templates as reference for generating the specification:

- **Detailed**: `.codexspec/templates/docs/spec-template-detailed.md` - Full format with user stories, acceptance criteria, requirements, and success metrics
- **Simple**: `.codexspec/templates/docs/spec-template-simple.md` - Lightweight format for simpler features

Choose the appropriate template based on feature complexity.

### Template Structure

```markdown
# Feature: [Feature Name]

## Overview
[High-level description of the feature]

## Goals
- [Goal 1]
- [Goal 2]

## User Stories

### Story 1: [Story Title]
**As a** [user type]
**I want** [goal]
**So that** [benefit]

**Acceptance Criteria:**
- [ ] [Criterion 1]
- [ ] [Criterion 2]

## Functional Requirements
- [REQ-001] [Requirement description]
- [REQ-002] [Requirement description]

## Non-Functional Requirements
- [NFR-001] [Requirement description]
- [NFR-002] [Requirement description]

## Edge Cases
- [Edge case 1]: [Handling approach]
- [Edge case 2]: [Handling approach]

## Constraints
- [Constraint 1]
- [Constraint 2]

## Out of Scope
- [Item 1]
- [Item 2]
```

### Quality Criteria

- [ ] All user stories have acceptance criteria
- [ ] Functional requirements are specific and testable
- [ ] Non-functional requirements are measurable
- [ ] Edge cases are identified
- [ ] Constraints are documented
- [ ] Out of scope items are clearly listed

> [!NOTE]
> This is a placeholder command. The full implementation will be added in future versions.
