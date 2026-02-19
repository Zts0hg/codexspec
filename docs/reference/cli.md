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
| `PROJECT_NAME` | Name for your new project directory |

**Options:**

| Option | Short | Description |
|--------|-------|-------------|
| `--here` | `-h` | Initialize in current directory |
| `--ai` | `-a` | AI assistant to use (default: claude) |
| `--lang` | `-l` | Output language (e.g., en, zh-CN, ja) |
| `--force` | `-f` | Force overwrite existing files |
| `--no-git` | | Skip git initialization |
| `--debug` | `-d` | Enable debug output |

**Examples:**

```bash
# Create new project
codexspec init my-project

# Initialize in current directory
codexspec init . --ai claude

# With Chinese output
codexspec init my-project --lang zh-CN
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
| `--set-lang` | `-l` | Set the output language |
| `--list-langs` | | List all supported languages |
