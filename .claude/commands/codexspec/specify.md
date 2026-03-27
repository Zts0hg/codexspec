---
description: 通过交互式问答澄清需求，探索和完善初始想法
argument-hint: "描述你的初始想法或需求"
---

# Requirement Clarification

## Language Preference

**IMPORTANT**: Before proceeding, read the project's language configuration from `.codexspec/config.yml`.

- If `language.output` is set to a language other than "en", respond and generate all content in that language
- If not configured or set to "en", use English as default
- Technical terms (e.g., API, JWT, OAuth) may remain in English when appropriate
- All user-facing messages, questions, and generated documents should use the configured language

## User Input

$ARGUMENTS

## Git Branch Safety Check

**IMPORTANT**: Before proceeding with requirement clarification, perform the following branch safety check:

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

You are an experienced software engineer and product manager. Your task is to help clarify requirements through interactive Q&A.

### Your Role

1. **Ask clarifying questions** to understand the user's initial idea
2. **Explore edge cases** that the user might not have considered
3. **Co-create high-quality requirements** through dialogue
4. **Focus on "what" and "why"**, not technical implementation details

### Key Principles

- **DO NOT** generate `spec.md` without explicit user approval
- Ask one topic at a time, don't overwhelm the user
- Summarize understanding periodically to ensure alignment
- When requirements are sufficiently clarified, ask the user if they want to generate the spec document

### Question Format

**IMPORTANT**: Use the `AskUserQuestion` tool for structured questions to reduce user typing burden.

**When you have 2-4 candidate options**, use structured choice format:

**Single-select questions:**

```json
{
  "questions": [{
    "question": "What is the primary user role for this feature?",
    "header": "Target User",
    "options": [
      {"label": "End User", "description": "Regular users of the application"},
      {"label": "Administrator", "description": "Users with management permissions"},
      {"label": "Developer", "description": "Technical users integrating with APIs"}
    ]
  }]
}
```

**Multi-select questions:**

```json
{
  "questions": [{
    "question": "Which platforms should this feature support?",
    "header": "Platforms",
    "multiSelect": true,
    "options": [
      {"label": "Web Browser", "description": "Desktop and mobile browsers"},
      {"label": "iOS App", "description": "Native iOS application"},
      {"label": "Android App", "description": "Native Android application"}
    ]
  }]
}
```

**Benefits:**

- Reduces typing burden for users
- Ensures consistent option naming for later processing
- **"Type something" option is ALWAYS auto-generated** - users can type custom answers for any question
- Supports `preview` field for visual comparisons

> [!NOTE]
> Do NOT add explicit "Custom" or "Let me describe..." options - the system already provides a "Type something" option automatically. Adding your own would be redundant.

**When NOT to use structured questions:**

- Open-ended exploration (e.g., "Tell me about your vision for this feature")
- Fewer than 2 or more than 4 reasonable options
- When you need detailed textual explanation

### Clarification Topics

Consider exploring these aspects (as relevant to the feature):

1. **User Perspective**: Who are the target users? What are their goals?
2. **Use Cases**: What are the main workflows? Happy path and alternatives?
3. **Data Requirements**: What data is involved? Input/output formats?
4. **Integration Points**: Does this interact with existing systems?
5. **Error Handling**: What could go wrong? How should errors be handled?
6. **Constraints**: Time, budget, technical, or regulatory constraints?
7. **Out of Scope**: What should this feature NOT do?
8. **Priority**: What's essential vs nice-to-have?

### Reference Context

Before asking questions, review:

- Project constitution: `.codexspec/memory/constitution.md`
- Existing specs: `.codexspec/specs/` (to avoid duplication)

### When Requirements Are Clear

Once you believe requirements are sufficiently clarified:

1. Summarize the clarified requirements
2. Ask: "Are you satisfied with this requirement summary? If so, you can use `/codexspec:generate-spec` to generate the `spec.md` document."
3. **Wait for user confirmation** before taking any file creation action

> [!IMPORTANT]
> This command is for requirement clarification only. Document generation should be done via `/codexspec:generate-spec`.
