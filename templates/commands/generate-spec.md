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

**All requirements should already be clarified through `/codexspec:specify` before running this command.**

## Git Branch Safety Check

**IMPORTANT**: Before proceeding with spec generation, perform the following branch safety check:

### Execution Steps

1. **Check Git Environment**
   - Run: `git rev-parse --is-inside-work-tree 2>/dev/null`
   - If the result is not "true", skip this check and continue with the command

2. **Get Current Branch**
   - Run: `git branch --show-current`
   - Store the result as the current branch name

3. **Check Main Branch**
   - Read main branch names from `.codexspec/config.yml` (key: `git.main_branches`)
   - Default main branches: `["main", "master"]`
   - If the current branch is in the main branches list, proceed to step 4
   - Otherwise, skip to `## Instructions` and continue with the command

4. **Interactive Prompt**
   Use the `AskUserQuestion` tool with the following structure:

   ```json
   {
     "questions": [{
       "question": "You are currently on the main branch '{current_branch}'. It is recommended to create a separate branch for new features. Please select:",
       "header": "Branch Choice",
       "options": [
         {"label": "Create new feature branch (Recommended)", "description": "Create and switch to a new feature branch"},
         {"label": "Continue on current branch", "description": "Work directly on the main branch without creating a new branch"},
         {"label": "Cancel operation", "description": "Stop the current command execution"}
       ]
     }]
   }
   ```

   **Note**: Adjust the question text based on the project's language configuration (`.codexspec/config.yml` → `language.output`).

5. **Branch Creation** (if user chose "Create new feature branch")
   - Ask for feature name using `AskUserQuestion` tool
   - Generate branch name format: `{YYYY-MMDD-HHMM}{random}-{feature-name}`

     ```bash
     TIMESTAMP=$(date +"%Y-%m%d-%H%M")
     RANDOM_SUFFIX=$(head /dev/urandom | LC_ALL=C tr -dc 'a-z0-9' | head -c 2)
     BRANCH_NAME="${TIMESTAMP}${RANDOM_SUFFIX}-${feature_name}"
     ```

   - Run: `git checkout -b {BRANCH_NAME}`
   - Confirm success message: "✅ Branch created successfully: {BRANCH_NAME}"

6. **Handle User Choice**
   - If user chose "Continue on current branch": Continue with the command without creating a branch
   - If user chose "Cancel operation": Stop execution and return control to the user

7. **Continue Command**
   After branch handling (or if skipped), proceed with the `## Instructions` section.

## Instructions

You are now acting as a "Requirement Compiler". Execute the following operations:

### Steps

1. **Determine Feature ID**: Generate a unique prefix using timestamp + random suffix:

   ```bash
   # Get current timestamp
   TIMESTAMP=$(date +"%Y-%m%d-%H%M")

   # Generate 2-character random suffix from [a-z0-9]
   RANDOM_SUFFIX=$(head /dev/urandom | LC_ALL=C tr -dc 'a-z0-9' | head -c 2)

   # Full prefix: 16 characters (e.g., "2025-0321-1430k7")
   PREFIX="${TIMESTAMP}${RANDOM_SUFFIX}"
   ```

   **Format Specification**:
   - `YYYY`: 4-digit year (e.g., 2025)
   - `MM`: 2-digit month (01-12)
   - `DD`: 2-digit day (01-31)
   - `HH`: 2-digit hour (00-23)
   - `MM`: 2-digit minute (00-59)
   - `{random}`: 2 random characters from [a-z0-9] (36 characters, 1296 combinations)

   > **Format**: `{YYYY-MMDD-HHMM}{random}-{feature-name}`
   > **Example**: `2025-0321-1430k7-user-authentication`
   > **Regex**: `^\d{4}-\d{4}-\d{4}[a-z0-9]{2}-[a-z0-9-]+$`

2. **Create Feature Directory**: Create a new directory `.codexspec/specs/{YYYY-MMDD-HHMM}{random}-{feature-name}/` where:
   - `{YYYY-MMDD-HHMM}{random}` is the 16-character unique prefix (e.g., `2025-0321-1430k7`)
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

5. **Auto-Review Generated Spec**: After saving the spec, automatically run the review process:
   - Execute the same quality checks as `/codexspec:review-spec`
   - Generate a review report at `.codexspec/specs/{YYYY-MMDD-HHMM}{random}-{feature-name}/review-spec.md`
   - If issues are found, present a summary and ask if user wants to fix them now or proceed

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

Save the specification to: `.codexspec/specs/{YYYY-MMDD-HHMM}{random}-{feature-name}/spec.md`

A review report will also be generated at: `.codexspec/specs/{YYYY-MMDD-HHMM}{random}-{feature-name}/review-spec.md`

> [!IMPORTANT]
> This command should be called after `/codexspec:specify` has clarified all requirements. It focuses on document generation, not requirement exploration.

## Available Follow-up Commands

After generating and reviewing the specification, the user may consider:

- **Fix Issues**: If review found issues, describe the changes to fix them (e.g., "Fix SPEC-001")
- `/codexspec:clarify` - to address any ambiguities or gaps identified
- `/codexspec:spec-to-plan` - to proceed with technical implementation planning
