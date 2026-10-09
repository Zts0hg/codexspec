---
name: codexspec:config
description: "以交互方式管理 CodexSpec 项目配置"
---

# CodexSpec Configuration Manager

## Language Preference

Read `.codexspec/config.yml`. Two independent language controls apply (each falls back to `language.output`, then English):

- **Interaction language** (`language.interaction`): language for all conversation with the user — questions, explanations, status messages, and `codexspec` CLI terminal output.
- **Document language** (`language.document`): language for generated artifact files (requirements/spec/plan/tasks).

Converse in the interaction language and author artifacts in the document language. Apply the project's translation standard to both: translate by meaning (not word-for-word), keep English for terms with no good native equivalent, and write as if originally in that language.

A fresh or reset config writes only `output`; `interaction` and `document` resolve to it via the fallback above, so an `output`-only config is fully functional (non-blocking). Set `interaction` or `document` individually only to make them differ from `output`. That is why the YAML examples below stay `output`-only.

## Expression Standard

**IMPORTANT**: Everything this command produces — documents, reviews, reports, commit messages, diagnostics, and replies — is written for a reader who cannot see your working context. Apply the rules below to every artifact and message you output:

- **Write for the reader at hand-off.** Every reference must resolve without access to this session: no session-only identifiers or section numbers, no narration of what changed during the conversation, no arguments with absent reviewers. State current reality and cite committed, reachable sources.
- **Preserve every proposition.** Before summarizing or trimming, list the facts a passage carries: actors, conditions, ordering, modalities (must, never), negative guarantees, and consequences. Remove only reasoning transcripts, repetition, and decoration. Shorter is not clearer if any fact is lost.
- **State what the surface requires.** Diagnostics name what failed, which rule was violated, and the correction. Problem reports carry the defect, its location, its impact, and the evidence. Decisions record the alternatives they beat. Rejections give the reason in one line. Shipped work is described in the present tense; plans and open questions are labeled as such.
- **Define terms before relying on them.** Prefer the concrete rule, field, or behavior over a coined label; give a project-specific term a plain-language definition at first use, then use it consistently.
- **Be honest, not agreeable.** Verify claims before accepting them; fix or rebut on technical grounds. One substantiated blocker is worth more than a list of nitpicks. When a decision is needed, present only viable options, recommend one, and state the real difference between them.
- **Declare what is binding.** Say explicitly which instructions are hard requirements and where judgment is required. Keep one explanation in one place and link to it, but keep at the point of use the contract a reader needs there.

## Workspace Routing Before Writes

This section governs the location of every later file, index, branch, and commit mutation.
Record `SOURCE_ROOT` as the explicitly selected checkout (otherwise the invoking checkout) before
changing working directories. Read its `.codexspec/config.yml`: `workflow.worktrees` defaults to
on; only the literal boolean `false` disables it. Configuration remains checkout-local. Read-only
inspection keeps its original source target and does not create a worktree merely to read files.

- With `CODEXSPEC_AUTO_DEV_DELEGATION`, use the dedicated worktree supplied by auto-dev as
  `OUTPUT_ROOT` throughout. `blueprint` and `auto-dev` themselves retain their existing fixed branch
  `codexspec/auto-dev` and worktree `worktree-for-codexspec-auto-dev`; they always use the new shared
  `<repository-name>-codexspec-worktrees` parent, irrespective of the ordinary isolation switch.
- With ordinary isolation disabled, `OUTPUT_ROOT` is `SOURCE_ROOT` and existing in-place behavior
  applies. `codexspec init`, both first-time setup and installation updates, is explicitly exempt:
  it operates on its selected checkout regardless of this switch.
- For a new ordinary feature (`specify`, `quick`, or another feature-creation entry), invoke the
  installed platform create-new-feature script or `codexspec _worktree-helper create --name
  <short-name>` before the first artifact write. Parse returned JSON rather than evaluating shell
  output. `workspace`, `feature_dir`, and `requirements_file` are absolute paths; `branch` is the
  full `<feature-id>-<feature-name>`. Set `OUTPUT_ROOT` to that workspace.
- For an existing ordinary feature, resolve its explicit feature path/name first, otherwise its
  current feature branch, using `codexspec _worktree-helper resolve --feature <full-feature-name>`.
  Reuse that returned worktree. Do not silently pick another feature or create a replacement
  from main. If an explicit feature path names another checkout, use that checkout's configuration
  and preserve the identity of its documents and code.
- For standalone project-level writes without a selected ordinary feature, use
  `codexspec _worktree-helper route` from `SOURCE_ROOT`. An active feature workspace is reused;
  otherwise the helper uses `worktree-for-codexspec-maintenance`. Use the returned absolute
  workspace as `OUTPUT_ROOT`. Revalidate both source and destination rather than interpreting an
  arbitrary existing directory as a managed workspace.

When creation is interrupted, retain the returned `branch` and `workspace` even in an error
response. Resume the same identity with `codexspec _worktree-helper create --feature
<full-feature-name>`; a `creating` response from resolve requires this recovery step before
merge verification. A new `--name` request never adopts an existing identity after a random
name collision; report that collision and retry a new identity only for a genuinely new feature.

A `ready` response is required before writing feature artifacts or continuing development. Exit
status 3 with `merge_requires_resolution` or `merge_requires_verification` is a preparation handoff,
not success. Resolve conflicts and complete the merge only in the returned worktree, run the
project's required checks, and call `codexspec _worktree-helper finish --feature <full-feature-name>
--verification <json-file>` (use `worktree-for-codexspec-maintenance` for maintenance preparation).
The temporary JSON contains the verified `head`, `tree`, and `checks` entries with `command` and
integer `exit_code`; never claim a check ran when it did not. If conflicts cannot be resolved or
verification fails, stop. Retain the returned feature identity for continuation; do not create a
second feature to bypass failed preparation. Fetch warnings mean remote information may be stale;
they do not authorize bypassing an invalid baseline or failed verification.

Every mutating tool call and later SDD invocation must explicitly use `OUTPUT_ROOT` or paths inside
it. Before each file write, verify real filesystem containment: refuse symbolic links in the
output path and existing destination files with multiple hard links. A lexical path beneath
`OUTPUT_ROOT` alone does not establish isolation; never write through a link into another checkout.
A `cd` in one shell subprocess does not change the agent's later tool working directories.
Carry the same absolute workspace across stage handoffs. If required installation assets are
absent in a new worktree, run normal installation explicitly against that destination, preserving
existing project-authored files; stop if the required runtime or setup is unavailable.

Preserve input provenance: artifact-only reviews/reverse specification can read `SOURCE_ROOT`
while writing reports to `OUTPUT_ROOT`; their artifact containment checks apply to `OUTPUT_ROOT`.
Source edits and executable checks use the selected feature workspace. `commit-staged` preview
reads the original index; execution must stop if routing would substitute a different index or
mutate the protected main checkout. Do not copy, stash, stage, reset, or discard caller-owned changes
to make routing appear successful. Report an incompatible input/workspace and the required target
instead. Existing command-specific prohibitions still apply.

For configuration edits, decide routing from `SOURCE_ROOT`'s setting, then read and modify the
configuration in `OUTPUT_ROOT`. A bare toggle uses the destination's value. Report the exact path
and explain that other checkouts receive the setting through Git integration; do not add a shared
override or imply immediate changes to main's effective value. Completion retains worktrees; it
does not automatically merge to main or delete them. Any occupied path, invalid identity, failed
creation, or unusable baseline is an explicit stop, never permission to fall back to main writes.

## Parameter Check

Check if `the text after the $codexspec:config skill mention` contains `--view`:

- **If `--view` is present**: View mode - display current configuration and exit
- **If no arguments**: Interactive mode - show configuration management menu

## Configuration File Path

All configuration operations target: `.codexspec/config.yml`

## Instructions

### Step 1: Check Configuration File Existence

First, check if `.codexspec/config.yml` exists:

- If the file exists: Read its contents and proceed to Step 2 or Step 3 (based on mode)
- If the file does not exist: Proceed to Step 4 (Create new configuration)

### Step 2: View Mode (--view flag)

If `--view` flag is provided:

1. If configuration exists, display it in a readable format:

```markdown
## Current Configuration

```yaml
{file contents}
```

**Configuration file**: `.codexspec/config.yml`

```

2. If configuration does not exist, display:

```markdown
## Configuration Not Found

No configuration file found at `.codexspec/config.yml`.

To create a new configuration, run `$codexspec:config` without arguments.
```

3. Exit after displaying.

### Step 3: Interactive Mode (Configuration Exists)

If configuration exists and no `--view` flag, present the management menu using the host agent's structured-question tool (e.g., `AskUserQuestion` or `request_user_input`):

```json
{
  "questions": [{
    "question": "Configuration file found. What would you like to do?",
    "header": "Config Action",
    "options": [
      {"label": "View current config", "description": "Display the current configuration settings"},
      {"label": "Modify config", "description": "Change specific configuration values"},
      {"label": "Reset to defaults", "description": "Reset all settings to default values"},
      {"label": "Cancel", "description": "Exit without making changes"}
    ]
  }]
}
```

> **Note**: The field schema above follows the `AskUserQuestion` convention. Under `request_user_input`, each question additionally requires an `id` (snake_case) and accepts 2–3 options — follow the host tool's actual schema rather than copying this example verbatim.

Then handle each option:

#### Option: View current config

Display the configuration as in Step 2, then exit.

#### Option: Modify config

1. Ask which setting to modify:

```json
{
  "questions": [{
    "question": "Which setting would you like to modify?",
    "header": "Modify",
    "options": [
      {"label": "Interaction language", "description": "Language for conversing with you (LLM dialogue + codexspec CLI terminal output) (currently: {current value})"},
      {"label": "Document language", "description": "Language for generated artifact files (requirements/spec/plan/tasks) (currently: {current value})"},
      {"label": "Output language (legacy)", "description": "Fallback language used when interaction/document are not set (currently: {current value})"},
      {"label": "Commit language", "description": "Language for commit messages (currently: {current value})"},
      {"label": "Auto-next chain", "description": "Auto-advance the SDD pipeline once a stage passes (workflow.auto_next) (currently: {current value})"},
      {"label": "Auto-distill", "description": "Run $codexspec:distill on completion of wrap-up commands to capture reusable knowledge (workflow.auto_distill) (currently: {current value})"},
      {"label": "Review decision mode", "description": "Who decides about review-code findings whose trigger lies outside the project's real operating context (review.decided_by) (currently: {current value})"},
      {"label": "Back", "description": "Return to main menu"}
    ]
  }]
}
```

2. For language settings, show language selection:

```json
{
  "questions": [{
    "question": "Select the language:",
    "header": "Language",
    "options": [
      {"label": "English (en)", "description": "Default language"},
      {"label": "简体中文 (zh-CN)", "description": "Simplified Chinese"},
      {"label": "繁體中文 (zh-TW)", "description": "Traditional Chinese"},
      {"label": "日本語 (ja)", "description": "Japanese"}
    ]
  }]
}
```

3. For "Auto-next chain", ask whether to enable or disable:

```json
{
  "questions": [{
    "question": "Set workflow.auto_next:",
    "header": "Auto-next",
    "options": [
      {"label": "Enable", "description": "Auto-advance the SDD pipeline once a stage passes"},
      {"label": "Disable", "description": "Do not auto-advance; advance to the next command manually"},
      {"label": "Back", "description": "Return without changing"}
    ]
  }]
}
```

   Then read `.codexspec/config.yml`. The current value is enabled only when
   `workflow.auto_next` is the literal `true`; an absent key/section, `false`,
   or any other value is disabled. Write `workflow.auto_next` as an unquoted
   `true`/`false` (update the value in place when the key exists; otherwise add
   a `workflow:` section with `auto_next: <bool>`), preserving every other
   line and comment.

3b. For "Auto-distill", ask whether to enable or disable:

```json
{
  "questions": [{
    "question": "Set workflow.auto_distill:",
    "header": "Auto-distill",
    "options": [
      {"label": "Enable", "description": "Run $codexspec:distill on completion of wrap-up commands"},
      {"label": "Disable", "description": "Do not auto-distill; run $codexspec:distill manually"},
      {"label": "Back", "description": "Return without changing"}
    ]
  }]
}
```

   Then read `.codexspec/config.yml`. `auto_distill` is enabled by default; the
   current value is disabled only when `workflow.auto_distill` is the literal
   `false` (an absent key/section, `true`, or any other value is enabled). Write
   `workflow.auto_distill` as an unquoted `true`/`false` (update the value in place
   when the key exists; otherwise add `auto_distill: <bool>` under the `workflow:`
   section, creating that section if absent), preserving every other line and comment.

3c. For "Review decision mode", ask who decides:

```json
{
  "questions": [{
    "question": "Set review.decided_by:",
    "header": "Decided by",
    "options": [
      {"label": "reviewer (default)", "description": "The reviewer decides every finding; review-code behaves exactly as before"},
      {"label": "ask", "description": "A finding whose trigger lies outside the project's real operating context is presented to you once to fix or accept; your decision is recorded in requirements.md"},
      {"label": "Back", "description": "Return without changing"}
    ]
  }]
}
```

   Then read `.codexspec/config.yml`. `reviewer` is the default: an absent key/section means `reviewer`.
   Write `review.decided_by` as an unquoted `reviewer` or `ask` (update the value in place when the key
   exists; otherwise add `decided_by: <value>` under the `review:` section, creating that section if
   absent), preserving every other line and comment. Never write any other value. If the stored value is
   neither `reviewer` nor `ask`, report it as invalid (review-code rejects it as an argument error) and
   offer to correct it.

4. Update the configuration file with the new value
5. Display the updated configuration
6. Exit

#### Option: Reset to defaults

1. Confirm the reset action:

```json
{
  "questions": [{
    "question": "Are you sure you want to reset all settings to default values?",
    "header": "Confirm Reset",
    "options": [
      {"label": "Yes, reset", "description": "Reset all settings to defaults"},
      {"label": "No, cancel", "description": "Keep current settings"}
    ]
  }]
}
```

2. If confirmed, create default configuration:

```yaml
version: "1.0"
language:
  output: "en"
  commit: "en"
  templates: "en"
project:
  ai: "claude"
  created: "{current_date}"
```

3. Display confirmation and exit

#### Option: Cancel

Exit without making any changes.

### Step 4: Create New Configuration

If configuration does not exist, guide the user through creating one:

1. Welcome message:

```markdown
## Welcome to CodexSpec Configuration

This wizard will help you set up your project configuration.

Let's configure your language preferences.
```

2. Ask for output language:

```json
{
  "questions": [{
    "question": "Select your project's base language (sets `output`; interaction and document inherit it unless set individually):",
    "header": "Output Lang",
    "options": [
      {"label": "English (en)", "description": "Default, recommended for international projects"},
      {"label": "简体中文 (zh-CN)", "description": "Simplified Chinese"},
      {"label": "繁體中文 (zh-TW)", "description": "Traditional Chinese"},
      {"label": "日本語 (ja)", "description": "Japanese"}
    ]
  }]
}
```

3. Ask for commit message language:

```json
{
  "questions": [{
    "question": "Select your preferred language for git commit messages:",
    "header": "Commit Lang",
    "options": [
      {"label": "Same as output", "description": "Use the same language as output ({selected output language})"},
      {"label": "English (en)", "description": "Use English for commit messages regardless of output language"}
    ]
  }]
}
```

4. Create the configuration file:

```yaml
version: "1.0"
language:
  output: "{selected_output}"
  commit: "{selected_commit}"
  templates: "en"
project:
  ai: "claude"
  created: "{current_date}"
```

5. Save to `.codexspec/config.yml`

6. Display success message:

```markdown
## Configuration Created Successfully

Your configuration has been saved to `.codexspec/config.yml`.

```yaml
{configuration content}
```

You can modify this configuration anytime by running `$codexspec:config`.

```

## Default Configuration Values

When creating or resetting configuration, use these defaults:

```yaml
version: "1.0"
language:
  output: "en"
  commit: "en"
  templates: "en"
project:
  ai: "claude"
  created: "{current_date}"
```

## Supported Languages

| Code | Language | Notes |
|------|----------|-------|
| en | English | Default |
| zh-CN | 简体中文 | Simplified Chinese |
| zh-TW | 繁體中文 | Traditional Chinese |
| ja | 日本語 | Japanese |
| ko | 한국어 | Korean |
| es | Español | Spanish |
| fr | Français | French |
| de | Deutsch | German |
| pt | Português | Portuguese |
| ru | Русский | Russian |

> [!NOTE]
> Users can also type custom language codes via the "Type something" option.

## Error Handling

- **File read error**: If configuration file exists but cannot be read, inform the user and suggest recreating
- **Invalid YAML**: If configuration file contains invalid YAML, offer to reset or let user fix manually
- **Permission error**: If cannot write to `.codexspec/` directory, inform user of permission requirements

## Output Format

Converse in the interaction language and author generated artifacts in the document language. If either is unset, it falls back to `output`, then English.

Technical terms and file paths should remain in English for clarity.

## Worktree Isolation Setting

Offer `workflow.worktrees` in the workflow settings menu. It is enabled by default, including when
absent; only literal boolean `false` disables it. Use `codexspec config --worktrees on|off` (bare
`--worktrees` toggles) for the CLI surface. Apply Workspace Routing Before Writes before any setting
creation, edit, or command-frontmatter regeneration, including language and other workflow changes.
Read and toggle the destination checkout's setting, preserve all unrelated fields, and report the
actual configuration path. Changes affect that checkout first; other checkouts receive them through
Git integration. The switch does not disable the fixed shared blueprint/auto-dev workspace, and
both first-time and update `codexspec init` installations remain exempt.
