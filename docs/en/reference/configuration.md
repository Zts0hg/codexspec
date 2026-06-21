# Configuration

## Config File Location

`.codexspec/config.yml`

## Configuration Schema

```yaml
version: "1.0"

language:
  output: "zh-CN"        # Base language; the three below fall back to it, then "en"
  interaction: "zh-CN"   # LLM dialogue + codexspec CLI output (optional → defaults to output)
  document: "en"         # Generated requirements/spec/plan/tasks (optional → defaults to output)
  commit: "en"           # Git commit messages (optional → defaults to output)
  templates: "en"        # Template language (keep as "en")

project:
  ai: "claude"      # AI assistant
  created: "2025-02-15"
```

## Language Settings

CodexSpec splits language into four independently-configurable dimensions. `output` is the base; `interaction`, `document`, and `commit` override it and fall back to it (then `en`) when unset. This lets you, for example, converse with Claude in one language while keeping generated artifacts or commit messages in another.

| Dimension | Key | Set at init | Set later | Controls | Falls back to |
|-----------|-----|-------------|-----------|----------|---------------|
| Output (base) | `output` | `--lang` | `config --set-lang` | base for the other three | `en` |
| Interaction | `interaction` | `--interaction-lang` | `config --set-interaction-lang` | LLM dialogue + CLI output | output → `en` |
| Document | `document` | `--document-lang` | `config --set-document-lang` | generated spec/plan/tasks | output → `en` |
| Commit | `commit` | `--commit-lang` | `config --set-commit-lang` | git commit messages | output → `en` |
| Templates | `templates` | — | — | command template source (always `en`) | — |

**Supported values:** See [Internationalization](../user-guide/i18n.md#supported-languages)

### `language.output`

The base output language. The other dimensions fall back to it when they are not set explicitly.

### `language.interaction`

Language for the conversation between you and the LLM, plus `codexspec` CLI terminal output. Optional — defaults to `output`.

### `language.document`

Language for generated artifact files (requirements/spec/plan/tasks). Optional — defaults to `output`.

### `language.commit`

Language for git commit messages. Optional — defaults to `output`.

### `language.templates`

Template language. Should remain as `"en"` for compatibility.

## Project Settings

### `project.ai`

The AI assistant being used. Currently supports:

- `claude` (default)

### `project.created`

Date when the project was initialized.
