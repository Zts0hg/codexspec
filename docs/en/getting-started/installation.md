# Installation

## Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) (recommended) or pip

## Option 1: Install with uv (Recommended)

The easiest way to install CodexSpec is using uv:

```bash
uv tool install codexspec
```

## Option 2: Install with pip

Alternatively, you can use pip:

```bash
pip install codexspec
```

## Option 3: One-time Usage

Run directly without installing:

```bash
# Create a new project
uvx codexspec init my-project

# Initialize in an existing project for Claude Code
cd your-existing-project
uvx codexspec init . --ai claude

# Initialize for Codex CLI
uvx codexspec init . --ai codex

# Initialize for both Claude Code and Codex CLI (writes both .claude/ and .agents/)
uvx codexspec init . --ai both
```

## Option 4: Install from GitHub

For the latest development version:

```bash
# Using uv
uv tool install git+https://github.com/Zts0hg/codexspec.git

# Using pip
pip install git+https://github.com/Zts0hg/codexspec.git

# Specific branch or tag
uv tool install git+https://github.com/Zts0hg/codexspec.git@main
uv tool install git+https://github.com/Zts0hg/codexspec.git@v0.5.6
```

## Option 5: Plugin Marketplace Installation (Alternative)

CodexSpec is also available as a Claude Code plugin. This method is ideal if you want to use CodexSpec's slash commands directly in Claude Code without installing the CLI tool. The CLI is the full Requirements-First SDD experience; the plugin ships the slash-command set on top of Claude Code.

### Installation Steps

In Claude Code:

```bash
# Add the marketplace
> /plugin marketplace add Zts0hg/codexspec

# Install the plugin
> /plugin install codexspec@codexspec-market
```

### Language Configuration for Plugin Users

After installing via the Plugin Marketplace, configure your preferred language using the `/codexspec:config` slash command (the CLI `codexspec config` command is not available without the CLI install):

```bash
# Start interactive configuration
> /codexspec:config

# Or view current configuration
> /codexspec:config --view
```

The config command walks you through selecting the output language (for generated documents) and the commit-message language, then writes `.codexspec/config.yml`. Multi-language support uses the same LLM dynamic translation as the CLI.

### Comparison of Installation Methods

| Method | Best For | Features |
|--------|----------|----------|
| **CLI Installation** (`uv tool install` or `pip install`) | Full development workflow | CLI commands (`init`, `check`, `config`, `version`) + slash commands |
| **Plugin Marketplace** | Quick start, existing projects | Slash commands only (use `/codexspec:config` for language setup) |

**Note**: The plugin uses `strict: false` mode and reuses the existing multi-language support via LLM dynamic translation.

## Verify Installation

```bash
codexspec --help
codexspec version
```

(For Plugin Marketplace installs, verify by running any slash command such as `/codexspec:config --view` inside Claude Code.)

## Upgrading

```bash
# Using uv
uv tool install codexspec --upgrade

# Using pip
pip install --upgrade codexspec
```

(Plugin Marketplace installs are updated by Claude Code's plugin manager.)

## Next Steps

[Quick Start](quick-start.md)
