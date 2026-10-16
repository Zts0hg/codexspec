# Scripts and Installation Architecture

## Runtime and authoring layers

The Python CLI in `src/codexspec/` installs complete command templates from `templates/commands/`, document templates, and shared review standards. Claude Code receives slash commands; Codex receives native skills rendered from the same command sources. The 28 public commands share their workflow contracts across both hosts.

## Installation and project context

`codexspec init` selects platform helpers and the requested assistant integration. Shared resources live under `.codexspec/`; Claude commands live under `.claude/commands/codexspec/`, and Codex skills under `.agents/skills/`. The installed CLI also supports workspace routing and guarded helper operations used by the workflows.

Initialization updates managed CodexSpec blocks in existing `AGENTS.md` and `CLAUDE.md`, preserving project-authored content outside those blocks. `--force` refreshes installed artifacts and confirms update prompts; it does not replace the entire context file or discard unrelated configuration. Installing the CLI alone does not initialize a project.

## Platform helpers

Unix projects receive the Bash scripts from `scripts/bash/`; Windows projects receive the PowerShell scripts from `scripts/powershell/`. Feature creation and prerequisite checks resolve the selected feature and return machine-readable context. `common.sh` and `common.ps1` hold shared platform utilities; `review-context` supports review target collection. The standalone commit runtime is copied from `src/codexspec/commit_runtime.py` to `.codexspec/scripts/commit-staged-helper.py` on both platforms.

## Feature identity and artifact compatibility

Feature names follow `YYYY-MMDD-HHMMss-name`: a minute timestamp, two lowercase alphanumeric suffix characters, and an ASCII name. The full feature name identifies a workspace; continue using its explicit path or branch. Sequential `NNN-name` identifiers are not supported. Legacy compatibility applies to artifacts: older features may lack `requirements.md` or `design.md`, and commands disclose the resulting traceability limitations instead of inventing original confirmation.

## Contributor maintenance

Edit authoritative sources, regenerate derived copies, and verify the distribution. Commands that opt into fragments are authored under `internal/command_templates/sources/`; their complete `templates/commands/` files are generated. Other command templates remain directly authored. Do not hand-edit installed Claude or Codex copies.

Packaging includes public templates and the two platform script directories. Maintainer tooling in `internal/`, site sources in `docs/`, tests, and workflow diagram sources/assets stay outside the installed package. Do not widen the script inclusion boundary to all of `scripts/`.

<a id="extension-materials"></a>

## Extension Materials

The repository includes an extension manifest template, example command, and
[Extension Development Guide](https://github.com/Zts0hg/codexspec/blob/main/extensions/EXTENSION-DEVELOPMENT-GUIDE.md).
These are authoring materials. The current CLI has no extension install/list/remove
commands and does not automatically load `extension.yml` commands or hooks.
Shared review resources support project-specific additions under
`.codexspec/review-code/`; initialization preserves existing resource edits
and additional files unless replacement is requested.
