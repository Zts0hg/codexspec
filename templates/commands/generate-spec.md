---
description: Generate spec.md document after requirements have been clarified
---

# Specification Generator

## Language Preference

**IMPORTANT**: Before proceeding, read the project's language configuration from `.codexspec/config.yml`.
- If `language.output` is set to a language other than "en", respond and generate all content in that language
- If not configured or set to "en", use English as default
- Technical terms (e.g., API, JWT, OAuth) may remain in English when appropriate
- All user-facing messages, questions, and generated documents should use the configured language

## Prerequisite

**All requirements should already be clarified through `/codexspec.specify` before running this command.**

## Instructions

You are now acting as a "Requirement Compiler". Execute the following operations:

### Steps

1. **Determine Feature ID**: List directories in `.codexspec/specs/` using `ls` command to find existing spec directories (each spec is a directory named `{NNN}-{feature-name}/`). Determine the next sequential number (e.g., if `001-*` directory exists, use `002-`).

   > **IMPORTANT**: Do NOT use Glob to detect existing specs - Glob only matches files, not directories. Use `ls` or `Bash` tool instead.

2. **Create Feature Directory**: Create a new directory `.codexspec/specs/{NNN}-{feature-name}/` where:
   - `NNN` is the sequential number (001, 002, etc.)
   - `feature-name` is a kebab-case description of the feature

3. **Generate spec.md**: Create a comprehensive specification document including:

   - **Feature Overview**: High-level description and goals
   - **User Stories**: With acceptance criteria
   - **Functional Requirements**: All discussed requirement details
   - **Non-Functional Requirements**: Performance, security, scalability, etc.
   - **Acceptance Criteria**: Specific test cases
   - **Edge Cases**: Identified edge cases and handling approaches
   - **Output Format Examples**: If applicable
   - **Out of Scope**: Items explicitly excluded

4. **Review Constitution**: Ensure alignment with `.codexspec/memory/constitution.md`

### Spec Template Structure

```markdown
# Feature: [Feature Name]

## Overview
[High-level description]

## Goals
- [Goal 1]
- [Goal 2]

## User Stories

### Story 1: [Title]
**As a** [user type]
**I want** [goal]
**So that** [benefit]

**Acceptance Criteria:**
- [ ] [Criterion 1]
- [ ] [Criterion 2]

## Functional Requirements
- [REQ-001] [Description]
- [REQ-002] [Description]

## Non-Functional Requirements
- [NFR-001] [Description]

## Acceptance Criteria (Test Cases)
- [TC-001] [Test case description]
- [TC-002] [Test case description]

## Edge Cases
- [Edge case]: [Handling approach]

## Output Examples
[If applicable, provide example outputs]

## Out of Scope
- [Item 1]
- [Item 2]
```

### Quality Checklist

Before saving, verify:
- [ ] All user stories have acceptance criteria
- [ ] Functional requirements are specific and testable
- [ ] Non-functional requirements are measurable
- [ ] Test cases are concrete and executable
- [ ] Edge cases are documented
- [ ] Out of scope items are listed

### Output

Save the specification to: `.codexspec/specs/{NNN}-{feature-name}/spec.md`

> [!IMPORTANT]
> This command should be called after `/codexspec.specify` has clarified all requirements. It focuses on document generation, not requirement exploration.
