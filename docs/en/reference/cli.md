# CLI Reference

## Commands

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
| `--ai` | `-a` | AI assistant to use (default: claude) |
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

# Fully non-interactive: zh-CN base, English commit messages
codexspec init my-project --lang zh-CN --commit-lang en

# Set every dimension explicitly (scriptable, no prompts)
codexspec init my-project \
  --interaction-lang zh-CN --document-lang en --commit-lang en
```

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

Each `--set-*-lang` updates one [language dimension](../user-guide/i18n.md); any dimension you do not set falls back to `output`, then `en`.
