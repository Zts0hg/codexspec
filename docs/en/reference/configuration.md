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
  templates: "en"        # Keep as "en"

project:
  ai: "claude"
  created: "2025-02-15"

workflow:
  auto_next: false       # Auto-advance between workflow stages (opt-in)
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

The AI assistant being used. Controls which agent context files `codexspec init` lays down:

- `claude` (default) — writes `CLAUDE.md` (and `.claude/commands/`).
- `codex` — writes `AGENTS.md` and `.agents/skills/` instead.
- `both` — writes all of the above so the project is ready for both Claude Code and Codex CLI.

`CLAUDE.md` is always created (so the project stays usable from Claude Code); `AGENTS.md` and `.agents/skills/` are created only when `project.ai` is `codex` or `both`.

### `project.created`

Date when the project was initialized.

## Workflow Settings

### `workflow.auto_next`

Controls whether the Requirements-First SDD pipeline **auto-advances** to the next workflow stage once the current stage passes, instead of requiring you to manually trigger the next command.

- **Default:** `false` (opt-in). Only the literal value `true` enables auto-advance.
- **Toggle / set with:** `codexspec config --auto-next` (bare flag toggles the current value; pass `on`/`off` to set it explicitly).

**Chain:**

```
specify → generate-spec → spec-to-plan → plan-to-tasks → implement-tasks
```

**Pass gate:**

- `generate-spec`, `spec-to-plan`, `plan-to-tasks`: the command's built-in review loop must report an Overall Status of `PASS` or `PASS_WITH_WARNINGS`.
- `specify`: there is no review loop, so the gate is your explicit confirmation that requirements discovery is complete (the **final** stage summary, not each intermediate one).
- `implement-tasks`: terminal stage — nothing auto-fires after it.

When the review loop reports `NEEDS_REVISION` or `BLOCKED`, the chain halts and control returns to you. Before each advance the agent emits one notice line (for example: `auto_next: review passed → invoking /codexspec:spec-to-plan`).
