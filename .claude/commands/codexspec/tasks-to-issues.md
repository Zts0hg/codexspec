---
description: 将现有任务转换为该功能的可操作 GitHub Issues
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

Read `.codexspec/config.yml`. Two independent language controls apply (each falls back to `language.output`, then English):

- **Interaction language** (`language.interaction`): language for all conversation with the user — questions, explanations, status messages, and `codexspec` CLI terminal output.
- **Document language** (`language.document`): language for generated artifact files (requirements/spec/plan/tasks).

Converse in the interaction language and author artifacts in the document language. Apply the project's translation standard to both: translate by meaning (not word-for-word), keep English for terms with no good native equivalent, and write as if originally in that language.

## Expression Standard

**IMPORTANT**: Everything this command produces — documents, reviews, reports, commit messages, diagnostics, and replies — is written for a reader who cannot see your working context. Apply the rules below to every artifact and message you output:

- **Write for the reader at hand-off.** Every reference must resolve without access to this session: no session-only identifiers or section numbers, no narration of what changed during the conversation, no arguments with absent reviewers. State current reality and cite committed, reachable sources.
- **Preserve every proposition.** Before summarizing or trimming, list the facts a passage carries: actors, conditions, ordering, modalities (must, never), negative guarantees, and consequences. Remove only reasoning transcripts, repetition, and decoration. Shorter is not clearer if any fact is lost.
- **State what the surface requires.** Diagnostics name what failed, which rule was violated, and the correction. Problem reports carry the defect, its location, its impact, and the evidence. Decisions record the alternatives they beat. Rejections give the reason in one line. Shipped work is described in the present tense; plans and open questions are labeled as such.
- **Define terms before relying on them.** Prefer the concrete rule, field, or behavior over a coined label; give a project-specific term a plain-language definition at first use, then use it consistently.
- **Be honest, not agreeable.** Verify claims before accepting them; fix or rebut on technical grounds. One substantiated blocker is worth more than a list of nitpicks. When a decision is needed, present only viable options, recommend one, and state the real difference between them.
- **Declare what is binding.** Say explicitly which instructions are hard requirements and where judgment is required. Keep one explanation in one place and link to it, but keep at the point of use the contract a reader needs there.

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
>
> - UNDER NO CIRCUMSTANCES CREATE ISSUES IN REPOSITORIES THAT DO NOT MATCH THE REMOTE URL
> - Always verify the repository before creating issues
> - Do not create duplicate issues

## Prerequisites

- Git repository with GitHub remote
- GitHub CLI (`gh`) installed and authenticated
- Tasks file (`tasks.md`) exists

> [!NOTE]
> This command requires GitHub CLI to be installed and authenticated. Run `gh auth login` first.
