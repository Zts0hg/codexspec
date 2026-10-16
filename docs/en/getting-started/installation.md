<a id="installation"></a>

# Installation

<a id="install-with-the-codex-desktop-app"></a>

## Install with the Codex Desktop App

You can ask Codex to install CodexSpec and set up your project directly from the desktop app.

1. Add a local project in the Codex desktop app and select the folder where you want to work.
2. Start a chat in that project and paste the prompt below.
3. If the app requests permission to download or install dependencies, approve the requested action to continue.

```text
Please install and initialize CodexSpec in the current project.
Project: https://github.com/Zts0hg/codexspec

Complete the setup directly instead of asking me to run terminal commands.

Check the environment. If uv or Python 3.11+ is missing, install the required
tools in my user directory using their official installation instructions.
Install the latest stable release of CodexSpec.

For a new setup, initialize the current project for Codex in English:
codexspec init . --ai codex --lang en

If CodexSpec is already configured, check its version and configuration before
updating. Preserve existing requirements, project principles, user files,
and configuration settings.

Verify that the CLI works and that AGENTS.md and the CodexSpec skill files
under .agents/skills/ are installed. Explain the result and how to start
describing my requirements in plain English. If the skills are not yet
available in this chat, tell me whether to start a new chat or restart the app.
```

For Chinese replies and documents, replace `--lang en` with `--lang zh-CN` and ask Codex to explain the result in Chinese.

Codex installs the same CLI and project skills used by the manual setup below. You can start using them with a prompt such as `$codexspec:specify I want to build a todo application`. See [OpenAI's skills guide](https://learn.chatgpt.com/docs/build-skills) for local skill discovery and refresh behavior.

<a id="prerequisites"></a>

## Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) (recommended), or pip
- The assistant you intend to use: Claude Code or Codex
- Git for worktree development and Git workflows

<a id="cli-installation"></a>

## CLI Installation

```bash
uv tool install codexspec

# Or use pip
pip install codexspec

# Verify the CLI and inspect available commands
codexspec version
codexspec --help
codexspec list-commands
```

Initialize a new project with `codexspec init my-project --ai claude`,
or the current directory with `codexspec init . --ai codex`. Use `--ai both`
for both integrations. The assistant selection defaults to `claude`; choose
the value explicitly for Codex or both.

<details>
<summary>Alternative installation methods</summary>

<a id="one-time-initialization"></a>

### One-time initialization

```bash
uvx codexspec init my-project --ai claude
uvx codexspec init . --ai codex
```

One-time initialization installs project commands and the standalone commit
runtime. Worktree routing, blueprint/auto-dev, and manual profile review still
invoke the CodexSpec CLI; make it available for those workflows.

<a id="development-versions"></a>

### Development versions

```bash
uv tool install git+https://github.com/Zts0hg/codexspec.git
uv tool install git+https://github.com/Zts0hg/codexspec.git@main

# Replace <tag> with the version you want
uv tool install git+https://github.com/Zts0hg/codexspec.git@<tag>
```

</details>

<details>
<summary>Windows installation</summary>

Use PowerShell:

```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
# Restart PowerShell, then:
uv tool install codexspec
codexspec version
```

See the [Windows Troubleshooting Guide](../WINDOWS-TROUBLESHOOTING.md)
for PATH and installation troubleshooting.

</details>

<a id="upgrade-and-refresh-a-project"></a>

## Upgrade and Refresh a Project

Updating the CLI and refreshing a project's installed commands are separate steps:

```bash
uv tool install codexspec --upgrade
# Or: pip install --upgrade codexspec

# In the project you want to refresh; select its desired integration(s)
codexspec init . --force --ai both
```

Use `--ai claude` or `--ai codex` when only that integration is wanted.
`--force` regenerates distributed commands/scripts and refreshes review resources;
it also auto-confirms migration, command-update, and constitution-compliance prompts. Existing requirements and project
principles are retained, existing context-file bodies are preserved while managed
guidance is updated, and configuration keys you did not explicitly set are kept.

The planning command is `design-to-plan`; installation updates retire the old
`spec-to-plan` entry without an alias.

<a id="plugin-marketplace-installation"></a>

## Plugin Marketplace Installation

For Claude Code, install the plugin from its marketplace:

```text
/plugin marketplace add Zts0hg/codexspec
/plugin install codexspec@codexspec-market
/codexspec:config
```

The plugin supplies commands and session-start guidance for staged commit
analysis and historical requirements recall, including resumed sessions.
Plugin installation does not initialize a project. Use `/codexspec:config`
to create or modify language, workflow, and review settings; use CLI initialization
when you need the full project scaffold.

Direct commit preview and authorized in-place commits can use the bundled
runtime with Python 3.11+ and Git, without a persistent CodexSpec CLI.
Worktree routing, blueprint/auto-dev, and manual profile review retain their CLI
requirements. The plugin startup hook requires Git on PATH and a Claude Code
version supporting command-hook `args` (exec form). Its guidance is for the agent;
it does not intercept manual Git commands.

See [Installation](installation.md) for detailed setup.
