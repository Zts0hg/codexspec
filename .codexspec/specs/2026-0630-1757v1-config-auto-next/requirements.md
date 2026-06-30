# Confirmed Requirements: config-auto-next

<!--
Language: Maintain this document in the language specified in .codexspec/config.yml.
This file is the authoritative, persistent record of user-confirmed intent.
Do not copy the full conversation. Keep only confirmed decisions and short evidence
quotes needed to resolve later interpretation disputes.
-->

**Feature ID**: `2026-0630-1757v1`
**Status**: Discovery → Confirmed
**Last Confirmed**: 2026-06-30

## Authority Rules

- Only entries with `Status: confirmed` are binding downstream inputs.
- `open` entries MUST NOT be converted into confirmed product requirements.
- Replaced entries remain in this file with `Status: superseded` and a link to the replacement.
- AI inferences must be labeled as assumptions and require user confirmation before becoming binding.

## Needs

### NEED-001: Toggle `workflow.auto_next` without hand-editing config.yml

- **Status**: confirmed
- **Statement**: Provide a command so users can switch or set the `workflow.auto_next` flag in `.codexspec/config.yml` without manually editing the file.
- **Rationale**: Manual YAML editing is error-prone and inconvenient; a purpose-built command removes that friction.
- **User Evidence**: "我只是需要有一个命令方便用户设置 auto_next 开关，免去手改的麻烦。"
- **Confirmed At**: 2026-06-30

## Constraints

### CON-001: Value validation and exit codes

- **Status**: confirmed
- **Statement**: An invalid explicit value (anything not in the accepted set) prints a red error message and exits with code 1; success exits with code 0.
- **User Evidence**: Derived from the confirmed "toggle + explicit" semantics (DEC-002).

### CON-002: Missing section/key handling and comment preservation

- **Status**: confirmed
- **Statement**: When the `workflow:` section or the `auto_next` key is absent, the current value is treated as `false` (constitution: "only literal `true` enables"). On toggle/set, create the section and/or key as needed. Continue using the existing line-by-line string-editing approach (no YAML library), preserving all other comments.
- **User Evidence**: Constitution rule + existing `config` command implementation pattern.

### CON-003: Typer tri-state option

- **Status**: confirmed
- **Statement**: The `--auto-next` option must distinguish three states — not passed, passed bare (toggle), and passed with a value (explicit set) — implemented via a sentinel default. Exact mechanism is deferred to the plan.
- **User Evidence**: Required to support the confirmed toggle + explicit semantics (DEC-002).

### CON-004: Documentation updates

- **Status**: confirmed
- **Statement**: The `README.*.md` config-options tables and examples (which currently list `--set-lang`, etc.) must be extended with `--auto-next` across all language versions. Any CLI help text for the `config` command must also list the new option.
- **User Evidence**: README files already enumerate config options; the new option must be discoverable.

## Decisions

### DEC-001: Add an option to the existing `config` command (no subcommand refactor)

- **Status**: confirmed
- **Decision**: Implement as a new `--auto-next` option on the existing `codexspec config` command, structurally parallel to `--set-lang` / `--set-interaction-lang` / `--set-document-lang` / `--set-commit-lang`. Do NOT refactor `config` into a Typer sub-app and do NOT introduce a positional subcommand.
- **Alternatives Rejected**: (a) Refactor `config` into a nested Typer sub-app so `config auto-next` is a real subcommand — rejected as invasive (would force migration/breaking change of existing options); (b) add an independent top-level `codexspec auto-next` command — rejected as disjoint from the `config` system and less discoverable.
- **Reason**: Lowest risk, no breaking change, consistent with the existing architecture. The user is indifferent to command form.
- **User Evidence**: "我只是需要有一个命令方便用户设置 auto_next 开关…并不要求命令的形式。"

### DEC-002: Toggle + explicit semantics

- **Status**: confirmed
- **Decision**: `codexspec config --auto-next` (bare) flips the current value; `codexspec config --auto-next on|off` sets it explicitly. Explicit values accept `on/off`, `true/false`, `1/0`, `yes/no` (case-insensitive). A missing key is treated as `false`.
- **Alternatives Rejected**: (a) pure toggle only (no explicit value) — less scriptable; (b) explicit value only — too verbose for ad-hoc use.
- **Reason**: Most flexible; supports both interactive use and scripting.
- **User Evidence**: User selected "切换+显式(推荐)".

### DEC-003: No-project behavior

- **Status**: confirmed
- **Decision**: If `.codexspec/config.yml` does not exist, print `No CodexSpec project found` and exit with code 1, mirroring the existing `config` command's behavior.
- **User Evidence**: Consistency with the existing `config` command.

### DEC-004: Scope limited to `workflow.auto_next`

- **Status**: confirmed
- **Decision**: The command touches only `workflow.auto_next`. It must not modify `language.*` or any other configuration section, and must not alter the SDD chain / template runtime behavior (auto_next's chain-advance semantics already exist in the command templates).
- **User Evidence**: Feature scope is the auto_next switch only.

### DEC-005: No command-frontmatter re-render

- **Status**: confirmed
- **Decision**: Do NOT call `_rerender_command_frontmatter()` after editing config. That function exists solely for the language options (verified: only two call sites, both in language paths); `auto_next` does not appear in command frontmatter.
- **User Evidence**: Code inspection of `src/codexspec/__init__.py` (call sites at lines 277, 356; definition at 857).

### DEC-006: Also update the interactive `/codexspec:config` slash command

- **Status**: confirmed
- **Decision**: In addition to the CLI option, update the interactive slash command `/codexspec:config` so its menu can also toggle auto_next, using the same toggle + on/off semantics as the CLI. The source of truth is `templates/commands/config.md` (the distributed command template); `.claude/commands/codexspec/config.md` and the `.agents/skills/codexspec-config-*` forms are regenerated from it and must not be hand-edited (per the Self-bootstrap / template-modification rules).
- **Alternatives Rejected**: CLI-only — rejected by the user.
- **Reason**: Plugin users (who lack the CLI) also need a way to toggle auto_next without hand-editing config.
- **User Evidence**: "OPEN-001 同步更新交互式斜杠命令 /codexspec:config".

### DEC-007: Output messages in English (hardcoded)

- **Status**: confirmed
- **Decision**: Success/error messages are hardcoded in English (e.g. `auto_next enabled (workflow.auto_next = true)`), matching the four existing `config` option messages ("Language set to:", etc.).
- **Reason**: Internal consistency within the `config` command.
- **Note**: This perpetuates a pre-existing inconsistency with the documented rule that `language.interaction` governs CLI terminal output; this feature follows the status quo rather than expanding scope to localize all config messages.
- **User Evidence**: "接受 ASSUME-001".

### DEC-008: Bare-line insertion for a new key

- **Status**: confirmed
- **Decision**: When creating the `auto_next` key, write a bare line `auto_next: <bool>`; do not reconstruct the original multi-line explanatory comment.
- **Reason**: Avoids comment-maintenance burden; the command edits only the value line.
- **User Evidence**: "接受 ASSUME-002".

## Out of Scope

### OUT-001: No subcommand, no top-level command, no auxiliary flags

- **Status**: confirmed
- **Statement**: This feature does NOT add: a positional subcommand (`config auto-next`), a top-level command (`codexspec auto-next`), a `--no-auto-next` flag (redundant with `--auto-next off`), or a `--show-auto-next` flag (viewing the current value is served by the existing `codexspec config` no-argument panel).
- **Reason**: Keep the change minimal and consistent.
- **User Evidence**: DEC-001 + scope minimization.

## Open Questions

_None._ All material questions are resolved.

## Superseded Entries

_None._

## Confirmation Log

### Session 2026-06-30

- **Summary Presented**: Stage summary grouped by candidate IDs (NEED-001; DEC-001…DEC-005; CON-001…CON-004; OUT-001), plus open items OPEN-001 (slash-command scope), ASSUME-001 (output language), ASSUME-002 (insert comment).
- **User Confirmation**: Explicit confirmation. OPEN-001 resolved to "also update `/codexspec:config`" (→ DEC-006). ASSUME-001 and ASSUME-002 accepted (→ DEC-007, DEC-008).
- **Entries Confirmed**: NEED-001, CON-001, CON-002, CON-003, CON-004, DEC-001, DEC-002, DEC-003, DEC-004, DEC-005, DEC-006, DEC-007, DEC-008, OUT-001.
