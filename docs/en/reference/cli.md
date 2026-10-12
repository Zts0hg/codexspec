# CLI Reference

## Commands

### `codexspec show-blueprint`

Print the complete `.codexspec/blueprint.md` from the fixed `codexspec/auto-dev` branch and
`worktree-for-codexspec-auto-dev`. Output is raw file content on standard output. Missing repository,
branch, worktree, or file prerequisites are reported on standard error with a non-zero status. The
command is read-only and performs no fetch, merge, write, or lock operation.

```bash
codexspec show-blueprint
```

---

### `codexspec init`

Initialize a new CodexSpec project.

```bash
codexspec init [PROJECT_NAME] [OPTIONS]
```

**Arguments:**

| Argument | Description |
|----------|-------------|
| `PROJECT_NAME` | Name for your new project directory (use `.` or `--here` for the current dir) |

**Options:**

| Option | Short | Description |
|--------|-------|-------------|
| `--here` | `-h` | Initialize in the current directory |
| `--ai` | `-a` | AI assistant to use: `claude`, `codex`, or `both` (default: claude) |
| `--lang` | `-l` | Output (base) language; interaction/document/commit fall back to it (e.g., en, zh-CN, ja) |
| `--interaction-lang` | | Interaction language (LLM dialogue + `codexspec` CLI output); overrides `--lang` |
| `--document-lang` | | Document language (generated requirements/spec/plan/tasks); overrides `--lang` |
| `--commit-lang` | | Commit-message language; overrides `--lang` |
| `--force` | `-f` | Overwrite existing files and auto-confirm prompts; never regenerates `config.yml` |
| `--no-git` | | Skip git repository initialization |
| `--debug` | `-d` | Enable debug output |

`--lang` sets the `output` base language; `--interaction-lang`, `--document-lang`, and `--commit-lang` override it for their dimension (each falls back to `output`, then `en`). See [Internationalization](../user-guide/i18n.md) for the full model.

First-time init in a TTY without `--lang` (and without all three dimension flags) prompts for a base language; in a non-TTY (CI/scripts) it defaults to `en` — **fully non-interactive**. Re-running `init` preserves any language key you did not specify; `--force` never regenerates `config.yml`.

**Examples:**

```bash
# Create new project
codexspec init my-project

# Initialize in current directory
codexspec init . --ai claude

# One-time usage (no installation) — initialize for Codex CLI or both
uvx codexspec init . --ai codex
uvx codexspec init . --ai both

# Fully non-interactive: zh-CN base, English commit messages
codexspec init my-project --lang zh-CN --commit-lang en

# Set every dimension explicitly (scriptable, no prompts)
codexspec init my-project \
  --interaction-lang zh-CN --document-lang en --commit-lang en
```

`codexspec init` installs shared review resources into `.codexspec/review-code/` for Claude Code and Codex. `--force` refreshes shipped resources while preserving extension files with different paths. Installing the CLI alone does not create project files. Plugin-only review uses the same resources from the host-resolved plugin root when the project has no installed resource tree.

---

### `codexspec check`

Check for installed tools.

```bash
codexspec check
```

---

### `codexspec version`

Display version information.

```bash
codexspec version
```

---

### `codexspec config`

View or modify project configuration.

```bash
codexspec config [OPTIONS]
```

**Options:**

| Option | Short | Description |
|--------|-------|-------------|
| `--set-lang` | `-l` | Set the output (base) language |
| `--set-interaction-lang` | | Set the interaction language (LLM dialogue + CLI output) |
| `--set-document-lang` | | Set the document language (generated spec/plan/tasks) |
| `--set-commit-lang` | `-c` | Set the commit-message language |
| `--list-langs` | | List all supported languages |
| `--auto-next` | | Toggle/set `workflow.auto_next` (bare toggles; or on/off) |
| `--auto-maintenance` |  | Toggle/set `workflow.auto_maintenance` (default on; bare toggles; or on/off) |
| `--decided-by` | | Set `review.decided_by` to `reviewer` (default) or `ask` |

Each `--set-*-lang` updates one [language dimension](../user-guide/i18n.md); any dimension you do not set falls back to `output`, then `en`.

`codexspec config --auto-maintenance on|off` persists `workflow.auto_maintenance` as a YAML boolean in `.codexspec/config.yml`; an absent key means `true`. Both workflow switches accept case-insensitive `on/true/1/yes` and `off/false/0/no`. `implement-tasks` reads this setting when it automatically repairs reviewed code: `on` includes substantiated incremental maintenance improvements; `off` still reports them. Actual defects and required verification remain mandatory. This setting is independent of `auto-next` and is not an `implement-tasks` invocation parameter.

```bash
codexspec config --auto-maintenance on
codexspec config --auto-maintenance off
```
