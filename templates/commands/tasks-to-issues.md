---
description: Convert existing tasks into actionable GitHub issues for the feature
scripts:
  sh: .codexspec/scripts/check-prerequisites.sh --json --require-tasks --include-tasks
  ps: .codexspec/scripts/check-prerequisites.ps1 -Json -RequireTasks -IncludeTasks
---

# Tasks to GitHub Issues Converter

## Constitution Compliance (MANDATORY)

**Before converting tasks to issues:**

1. **Check for Constitution File**: Look for `.codexspec/memory/constitution.md`
2. **If Constitution Exists**:
   - Load and read project principles
   - Ensure issue descriptions align with project principles
   - Include relevant constitutional context in issues if applicable
3. **If No Constitution Exists**: Proceed with standard issue generation

## Language Preference

**IMPORTANT**: Before proceeding, read the project's language configuration from `.codexspec/config.yml`.
- If `language.output` is set to a language other than "en", respond and generate all content in that language
- If not configured or set to "en", use English as default
- Technical terms (e.g., API, JWT, OAuth) may remain in English when appropriate
- All user-facing messages, questions, and generated documents should use the configured language

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Goal

Convert the task breakdown from `tasks.md` into GitHub issues for project tracking and collaboration.

## Execution Steps

### 1. Initialize Context

Run `{SCRIPT}` from repo root and parse JSON for:
- `FEATURE_DIR` - Feature directory path
- `AVAILABLE_DOCS` - Available documents list
- `TASKS` - Path to tasks.md

### 2. Get Git Remote

Run the following command to get the repository remote URL:

```bash
git config --get remote.origin.url
```

> [!CAUTION]
> ONLY PROCEED IF THE REMOTE IS A GITHUB URL

### 3. Parse Tasks

Load and parse the tasks file:
- Extract task IDs
- Extract task descriptions
- Extract task dependencies
- Extract file paths
- Identify parallelizable tasks

### 4. Create Issues

For each task in the list:

1. **Generate Issue Title**: Use the task description as the title
2. **Generate Issue Body**: Include:
   - Task description
   - Related files
   - Dependencies (link to other issues if already created)
   - Acceptance criteria if specified
   - Labels (based on task type: `setup`, `implementation`, `testing`, `documentation`)

3. **Create Issue**: Use the GitHub CLI or API to create the issue

### 5. Issue Template

```markdown
## Task: {Task ID}

### Description
{Task description}

### Files
- {File path 1}
- {File path 2}

### Dependencies
- Depends on: #{Issue number for dependency}

### Acceptance Criteria
- [ ] {Criterion 1}
- [ ] {Criterion 2}

### Type
{setup|implementation|testing|documentation}
```

### 6. Report

Output:
- Number of issues created
- List of issue URLs
- Any tasks that could not be converted

## Safety Constraints

> [!CAUTION]
> - UNDER NO CIRCUMSTANCES CREATE ISSUES IN REPOSITORIES THAT DO NOT MATCH THE REMOTE URL
> - Always verify the repository before creating issues
> - Do not create duplicate issues

## Prerequisites

- Git repository with GitHub remote
- GitHub CLI (`gh`) installed and authenticated
- Tasks file (`tasks.md`) exists

> [!NOTE]
> This command requires GitHub CLI to be installed and authenticated. Run `gh auth login` first.
