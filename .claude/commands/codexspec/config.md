---
description: Manage CodexSpec project configuration interactively
argument-hint: "[--view] View current configuration without modification"
---

# CodexSpec Configuration Manager

## Language Preference

Read `.codexspec/config.yml`. Two independent language controls apply (each falls back to `language.output`, then English):

- **Interaction language** (`language.interaction`): language for all conversation with the user — questions, explanations, status messages, and `codexspec` CLI terminal output.
- **Document language** (`language.document`): language for generated artifact files (requirements/spec/plan/tasks).

Converse in the interaction language and author artifacts in the document language. Apply the project's translation standard to both: translate by meaning (not word-for-word), keep English for terms with no good native equivalent, and write as if originally in that language.

A fresh or reset config writes only `output`; `interaction` and `document` resolve to it via the fallback above, so an `output`-only config is fully functional (non-blocking). Set `interaction` or `document` individually only to make them differ from `output`. That is why the YAML examples below stay `output`-only.

## Parameter Check

Check if `$ARGUMENTS` contains `--view`:

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

To create a new configuration, run `/codexspec:config` without arguments.
```

3. Exit after displaying.

### Step 3: Interactive Mode (Configuration Exists)

If configuration exists and no `--view` flag, present the management menu using `AskUserQuestion`:

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

3. Update the configuration file with the new value
4. Display the updated configuration
5. Exit

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

You can modify this configuration anytime by running `/codexspec:config`.

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
