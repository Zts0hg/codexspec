---
description: One-stop quick implementation for small requirements — auto spec, plan, tasks, and code
argument-hint: "Describe your requirement"
---

# Quick Implementation

## Configuration Check

**IMPORTANT**: Before proceeding, check if the project configuration exists.

### Execution Steps

1. **Check Configuration File**
   - Check if `.codexspec/config.yml` exists
   - This is a simple file existence check, no parsing needed at this stage

2. **If Configuration Does NOT Exist**
   - Display a one-time prompt:

     ```
     💡 检测到项目未配置语言设置。你可以使用 `/codexspec:config` 命令来创建配置文件。
     ```

   - Use default values for current session:
     - `language.output`: "en"
     - `language.commit`: "en"
     - `language.templates`: "en"
   - Continue with command execution normally

3. **If Configuration Exists**
   - Proceed to `## Language Preference` section
   - Read configuration and apply language settings as before

4. **Session State** (Implicit)
   - The prompt is shown only once per conversation session
   - Claude's conversation context naturally maintains this state
   - No additional mechanism needed

## Language Preference

**IMPORTANT**: Before proceeding, read the project's language configuration from `.codexspec/config.yml`.

- If `language.output` is set to a language other than "en", respond and generate all content in that language
- If not configured or set to "en", use English as default
- Technical terms (e.g., API, JWT, OAuth) may remain in English when appropriate
- All user-facing messages, questions, and generated documents should use the configured language

## User Input

$ARGUMENTS

## Git Branch Safety Check

**IMPORTANT**: Before proceeding with the quick implementation flow, perform the following branch safety check:

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

You are a **Flow Orchestrator** for the CodexSpec Spec-Driven Development (SDD) process. Your responsibility is to guide a small requirement from initial description through to code implementation, automating the entire SDD pipeline while keeping the user informed.

### Step 1: Complexity Assessment

Analyze the user's requirement input and assess its complexity before proceeding.

#### Empty or Insufficient Input

If `$ARGUMENTS` is empty or too short to assess (fewer than ~10 meaningful words):

- Use `AskUserQuestion` to ask the user to provide a more detailed requirement description
- Do not proceed until a substantive description is provided

#### Assessment Dimensions

Evaluate the requirement along these dimensions:

- **Estimated file changes**: How many files will likely need to be created or modified
- **Module span**: How many distinct modules or components are involved
- **External dependencies**: Whether new external dependencies need to be introduced

#### Reference Thresholds

| Complexity | File Changes | Module Span | External Dependencies | Recommendation |
|------------|-------------|-------------|----------------------|----------------|
| **Small** | ≤3 files | Single module | None | ✅ Suitable for quick |
| **Medium** | 4-8 files | 2 modules | Minor | ⚠️ Can try, but standard flow recommended |
| **Large** | >8 files | 3+ modules | New dependencies | ❌ Standard flow recommended |

> These thresholds are reference guidelines. Use your judgment based on the specific nature of the requirement — a change touching 5 config files may be simpler than one modifying 3 core logic files.

#### Output Assessment

Display the assessment result:

```
📊 Complexity Assessment: [Small/Medium/Large]
  - Estimated files: [N] files
  - Module span: [description]
  - External dependencies: [None/description]
  - Recommendation: [Suitable for quick / Standard flow recommended]
```

#### Medium/Large Requirement Handling

If the assessment is **medium** or **large**, use `AskUserQuestion` to let the user decide:

```json
{
  "questions": [{
    "question": "This requirement appears to be [medium/large] in complexity ([brief reason]). The quick command works best for small requirements. How would you like to proceed?",
    "header": "Complexity Warning",
    "options": [
      {"label": "Continue with quick", "description": "Proceed with the automated quick flow despite the complexity"},
      {"label": "Switch to standard flow", "description": "Use individual SDD commands for more control over each step"}
    ]
  }]
}
```

If the user chooses **"Switch to standard flow"**, output the recommended command sequence and stop:

```
💡 Recommended command sequence for standard SDD flow:
  1. /codexspec:specify — Clarify requirements interactively
  2. /codexspec:generate-spec — Generate specification
  3. /codexspec:spec-to-plan — Create technical plan
  4. /codexspec:plan-to-tasks — Break down into tasks
  5. /codexspec:implement-tasks — Execute implementation
```

### Step 2: Concise Clarification

Before generating the spec, identify and resolve key ambiguities in the requirement.

#### Skip Condition

If the requirement description is already sufficiently clear and complete — covering the what, why, scope boundaries, and key behavioral expectations — you may skip clarification and proceed directly to Step 3.

#### Clarification Guidelines

- Ask only about **critical ambiguities** that would materially impact implementation
- Limit to **2-5 questions** total
- Use `AskUserQuestion` with structured options to minimize user effort

**Question format example:**

```json
{
  "questions": [{
    "question": "[Specific question about an ambiguity in the requirement]",
    "header": "[Topic]",
    "options": [
      {"label": "Option A", "description": "[What this means] → [Implementation impact]"},
      {"label": "Option B", "description": "[What this means] → [Implementation impact]"}
    ]
  }]
}
```

#### Scope Re-evaluation

If the user's answers during clarification significantly expand the scope (e.g., adding multiple new features, cross-cutting concerns), **re-assess complexity** using the Step 1 thresholds. If the expanded scope pushes the requirement to medium/large, notify the user and offer to switch to the standard flow.

#### Requirement Summary

After clarification is complete (or skipped), produce a brief **requirement summary** that captures:

- What is being built
- Key decisions made during clarification
- Scope boundaries

This summary will serve as context for the spec generation step.

### Step 3: Automated SDD Flow

Execute the full SDD pipeline by calling existing commands via the Skill tool. Each generation command includes built-in auto-review, so quick only calls 4 commands (not 7).

**Skill Call Principle**:
> Call all sub-commands **as-is** via the Skill tool. Do not pass any special prefixes, skip instructions, or mode flags. Do not modify any existing command templates. Each sub-command handles its own Language Preference check (silent config read, idempotent) and auto-review internally.

#### [1/4] Generate and Review Spec

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 [1/4] Generating and reviewing spec ...
```

Invoke the Skill tool:

```
Skill("codexspec:generate-spec", args="Based on the clarified requirements above, generate the spec")
```

- `generate-spec` will create the spec directory (using timestamp+random naming) and `spec.md`
- `generate-spec` internally auto-calls `review-spec` to review the generated spec
- Small issues are auto-corrected by the review; major issues trigger fallback (see Step 4)
- **After this step completes**, note the spec directory path from the conversation context (e.g., `.codexspec/specs/{prefix}-{name}/`) — this path is needed for subsequent steps

```
✅ spec.md generated and reviewed
```

#### [2/4] Generate and Review Plan

```
📐 [2/4] Generating and reviewing plan ...
```

Invoke the Skill tool:

```
Skill("codexspec:spec-to-plan", args="{spec_dir}/spec.md")
```

- `spec-to-plan` internally auto-calls `review-plan`
- Small issues auto-corrected / major issues trigger fallback (see Step 4)

```
✅ plan.md generated and reviewed
```

#### [3/4] Generate and Review Tasks

```
📝 [3/4] Generating and reviewing tasks ...
```

Invoke the Skill tool:

```
Skill("codexspec:plan-to-tasks", args="{spec_dir}/spec.md {spec_dir}/plan.md")
```

- `plan-to-tasks` internally auto-calls `review-tasks`
- Small issues auto-corrected / major issues trigger fallback (see Step 4)

```
✅ tasks.md generated and reviewed
```

#### [4/4] Implement Code

```
🚀 [4/4] Implementing code ...
```

Invoke the Skill tool:

```
Skill("codexspec:implement-tasks", args="{spec_dir}/tasks.md")
```

```
✅ Code implementation complete
```

#### Spec Directory Path

`generate-spec` creates the spec directory autonomously using its standard naming scheme (`{YYYY-MMDD-HHMM}{random}-{feature-name}`). After step [1/4] completes, extract the directory path from the conversation context and use it for `{spec_dir}` in subsequent Skill calls.

### Step 4: Major Issue Fallback

During the automated flow (Step 3), reviews may identify issues. Handle them based on severity:

#### Small Issues (Auto-correct)

The following are considered small issues that the agent should fix autonomously without interrupting the user:

- Format deficiencies (missing sections, incorrect heading levels)
- Imprecise wording or terminology
- Minor omissions that can be reasonably inferred from context
- Light structural adjustments

#### Major Issues (Pause and Ask User)

The following are considered major issues that require pausing and asking the user for input:

- **Logical contradictions**: Requirements that conflict with each other
- **Scope creep >50%**: Scope has expanded significantly beyond the initial description
- **Technical infeasibility**: Requirements that cannot be implemented as described
- **Missing critical information**: Key details that cannot be inferred and must come from the user

#### Judgment Principle

> If the agent can confidently make a correction based on context and best practices → **small issue** (auto-fix).
> If the correction requires a user decision or involves a change in requirement direction → **major issue** (pause and ask).

#### Fallback Flow

When a major issue is detected during any step:

1. Pause the current flow
2. Use `AskUserQuestion` to describe the issue clearly:

```json
{
  "questions": [{
    "question": "A major issue was found during [step name]: [clear description of the issue]. How would you like to proceed?",
    "header": "Issue Found",
    "options": [
      {"label": "Option A", "description": "[Resolution approach A]"},
      {"label": "Option B", "description": "[Resolution approach B]"}
    ]
  }]
}
```

3. After receiving user feedback, apply the resolution and continue from the point where the issue was found

### Step 5: Completion Summary

After all 4 steps complete successfully, provide a final summary:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎉 Quick flow complete!

📁 Artifact directory: {spec_dir}/
  - spec.md ✅
  - plan.md ✅
  - tasks.md ✅
  - review-spec.md ✅
  - review-plan.md ✅
  - review-tasks.md ✅

💻 Code changes:
  - [List of new/modified files from implementation]

💡 Next steps:
  - /codexspec:commit-staged — Commit your changes
  - /codexspec:pr — Generate a PR description
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

> **Note**: Do NOT automatically execute git commit. Leave that decision to the user.

### Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or too-short input | Ask user to provide a more detailed requirement description (Step 1) |
| Sub-command execution fails | Report the failure reason to the user, suggest manual continuation with the specific command that failed |
| Scope expands during clarification | Re-assess complexity, offer switch to standard flow if now medium/large (Step 2) |
| Project has no `.codexspec/` directory | Prompt user to run `codexspec init` first |
| `config.yml` does not exist | Use default language settings (en), show one-time configuration prompt (Configuration Check section) |
| Context window approaching limit | Streamline intermediate output — omit verbose review report details, keep only key findings and correction summaries |
