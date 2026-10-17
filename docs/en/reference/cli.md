# CLI Reference

<a id="cli-commands"></a>

## CLI Commands

| Command | Purpose |
|---------|---------|
| `codexspec init` | Initialize or refresh a project for Claude, Codex, or both |
| `codexspec scan <path>` | Find installed projects and optionally upgrade them safely |
| `codexspec check` | Check installed tools and dependencies |
| `codexspec version` | Display version and system information |
| `codexspec config` | View or modify project configuration |
| `codexspec list-commands` | List available agent commands by category |
| `codexspec show-blueprint` | Print the shared worktree's blueprint without changing it |

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

### Discover and upgrade installed projects

```bash
codexspec scan ~/code                  # Offline, read-only inventory
codexspec scan ~/code --upgrade        # Ask for each eligible project; choose all or quit
codexspec scan ~/code --upgrade --yes  # Upgrade every eligible project without prompts
```

Upgrade mode obtains one newest stable release in a temporary environment; it does
not require a separate CLI upgrade and does not replace the global CLI. It preserves
each project's Claude/Codex integration, configuration, requirements, constitution,
profile and custom context content. Linked Git worktrees are listed separately and
grouped by repository; only directories under the chosen root are scanned, including
hidden and nested projects. Symbolic links, `.git` and `.codexspec` internals are not
traversed. Unreadable descendants are reported as an incomplete scan.

The inventory separates recorded version from actual content verification. New
installations save `.codexspec/installation.json` with a version, managed-file list
and content checksums. A current version label does not hide missing or changed
files. Older installations have unknown versions and no saved checksum baseline;
this does not mean their directories are empty or corrupt. Upgrade compares their
actual files with the target release and creates metadata after successful completion.
No manual migration is required. The saved file list covers toolkit commands,
helpers, templates, review resources and managed context blocks, not user documents.

An upgrade skips a project if files it would change have staged, unstaged, untracked
or ignored changes, or if Git/filesystem evidence cannot establish safe replacement.
Unrelated business-file changes do not block it. `--yes` never bypasses these checks;
no-Git projects remain report-only. The output names skipped/failed projects and their
reasons. Inspect the reported files and Git changes, resolve the local edits as you
choose, and rerun the same scan command. Same-version content mismatches can be
repaired through this flow; newer recorded versions are never automatically downgraded.

Use Git changes and history to inspect or recover updates. There is no separate backup
or undo workflow. A failed application can leave partial changes; it is reported as
failed and never records a successful new installation. Exit status is `0` for a
complete successful run, `1` for incomplete scans, safety skips, upgrade failures or
cancellation, and `2` for invalid arguments or an invalid scan root. Noninteractive
upgrade requires `--yes`; choosing to skip an individual project is not an error.

<details>
<summary>CLI initialization options</summary>

| Option | Meaning |
|--------|---------|
| `PROJECT_NAME` | New directory name; use `.` for the current directory |
| `--here`, `-h` | Initialize the current directory |
| `--ai`, `-a` | `claude`, `codex`, or `both`; default `claude` |
| `--lang`, `-l` | Set the base output language |
| `--interaction-lang` | Set interaction language |
| `--document-lang` | Set document language |
| `--commit-lang` | Set commit-message language |
| `--force`, `-f` | Regenerate installed artifacts and auto-confirm migration/update/compliance prompts; preserve project-authored context and unrelated configuration |
| `--no-git` | Skip Git repository initialization |
| `--debug`, `-d` | Show detailed debug output |

</details>

<details>
<summary>CLI configuration options</summary>

| Option | Meaning |
|--------|---------|
| `--set-lang`, `-l` | Set the base output language |
| `--set-interaction-lang` | Set interaction language |
| `--set-document-lang` | Set document language |
| `--set-commit-lang`, `-c` | Set commit-message language |
| `--list-langs` | List supported language codes |
| `--auto-next` | Toggle/set automatic stage advancement |
| `--auto-distill` | Toggle/set automatic knowledge capture |
| `--auto-maintenance` | Toggle/set automatic incremental maintenance |
| `--worktrees` | Toggle/set checkout-local worktree isolation |
| `--decided-by` | Set `reviewer` or `ask` review decision mode |

</details>

## `codexspec show-blueprint`

Print the complete `.codexspec/blueprint.md` from the fixed `codexspec/auto-dev` branch and
`worktree-for-codexspec-auto-dev`. Output is raw file content on standard output. Missing repository,
branch, worktree, or file prerequisites are reported on standard error with a non-zero status. The
command is read-only and performs no fetch, merge, write, or lock operation.

```bash
codexspec show-blueprint
```
