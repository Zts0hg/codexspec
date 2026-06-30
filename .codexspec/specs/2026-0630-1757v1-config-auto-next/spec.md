# Feature Specification: config-auto-next

<!--
Language: Generate this document in the language specified in .codexspec/config.yml.
Document language = en.
-->

**Feature Branch**: `2026-0630-1757v1-config-auto-next`
**Created**: 2026-06-30
**Status**: Draft
**Input**: Feature directory `.codexspec/specs/2026-0630-1757v1-config-auto-next` (compiled from `requirements.md`).

## Context and Goals

CodexSpec's `workflow.auto_next` flag (in `.codexspec/config.yml`) controls whether the SDD pipeline auto-advances to the next command once a stage passes. Today the only way to change it is to hand-edit the YAML — error-prone and inconvenient.

This feature adds a purpose-built toggle so users can flip or set `workflow.auto_next` without touching the file by hand. It is delivered through **two surfaces**, both using the same toggle + explicit-value semantics:

1. **CLI**: a new `--auto-next` option on the existing `codexspec config` command.
2. **Interactive slash command**: an auto_next entry in the `/codexspec:config` menu (for Plugin users who lack the CLI).

### Configuration Surface

The only data this feature reads or writes is the `workflow.auto_next` key:

```yaml
workflow:
  auto_next: true   # unquoted boolean; only literal `true` enables
```

- **Read rule**: the current value is `true` only when the literal token `true` is present; every other value (absent key, `false`, or any malformed token) is treated as `false`. This mirrors the runtime semantics already used by the command templates (constitution: "only literal `true` enables").
- **Write rule**: the command emits an unquoted `true` or `false`.

## User Scenarios & Testing

### User Story 1 - Flip auto_next from the CLI (Priority: P1)

A CLI user wants to quickly turn the auto-advance chain on or off without remembering the exact YAML path.

**Why this priority**: This is the core convenience the feature exists for — the bare-toggle is the primary interaction.

**Independent Test**: Run `codexspec config --auto-next` twice; assert `workflow.auto_next` flips `true → false → true` and the printed message reports the new state each time.

**Acceptance Scenarios**:

1. **Given** `workflow.auto_next: true`, **When** the user runs `codexspec config --auto-next`, **Then** the file becomes `auto_next: false` and a success message reports it disabled.
2. **Given** `workflow.auto_next: false`, **When** the user runs `codexspec config --auto-next`, **Then** the file becomes `auto_next: true` and a success message reports it enabled.
3. **Given** `auto_next` is absent, **When** the user runs `codexspec config --auto-next`, **Then** the key is created as `auto_next: true` (absent is treated as `false`, so toggle yields `true`).

---

### User Story 2 - Set auto_next explicitly from the CLI (Priority: P1)

A user (or a script) wants to force a known state regardless of the current value.

**Why this priority**: Explicit set makes the command scriptable and idempotent — equal priority to the toggle because both were confirmed in DEC-002.

**Independent Test**: From any starting state, run `codexspec config --auto-next off` then `codexspec config --auto-next on`; assert the final value is `true` in both `on`/`off` and `=` forms.

**Acceptance Scenarios**:

1. **Given** any current value, **When** the user runs `codexspec config --auto-next off`, **Then** the file becomes `auto_next: false`.
2. **Given** any current value, **When** the user runs `codexspec config --auto-next on`, **Then** the file becomes `auto_next: true`.
3. **Given** the user passes `--auto-next TRUE` (or `Yes`, `1`), **Then** it is accepted case-insensitively and sets `true`. Likewise `false`/`no`/`0` set `false`.

---

### User Story 3 - Toggle auto_next via the interactive slash command (Priority: P2)

A Plugin user (no CLI installed) wants to change auto_next through the `/codexspec:config` menu.

**Why this priority**: Delivers the same capability to the non-CLI audience; lower priority only because the CLI path already covers the primary need.

**Independent Test**: Run `/codexspec:config`, choose the auto_next entry, toggle it, and confirm `workflow.auto_next` changed in `.codexspec/config.yml`.

**Acceptance Scenarios**:

1. **Given** the user runs `/codexspec:config` on an existing config, **When** they select the auto_next option, **Then** they can toggle or explicitly enable/disable `workflow.auto_next`.
2. **Given** the auto_next menu action completes, **Then** `.codexspec/config.yml` reflects the new unquoted boolean and all other content is preserved.

---

### Edge Cases

- **Missing `workflow:` section entirely**: the command creates the section and writes `auto_next: <bool>` under it.
- **Malformed existing value** (e.g. `auto_next: maybe`): treated as `false` on read; a toggle writes `true`, overwriting the malformed token.
- **Invalid explicit value** (e.g. `--auto-next yep`): rejected with a red error message and exit code 1; the file is not modified.
- **No project**: `.codexspec/config.yml` absent → `No CodexSpec project found`, exit 1 (matches existing `config` behavior).
- **Coexistence with other options**: passing `--auto-next` alongside `--set-lang` etc. must not break the sibling options; only the `--auto-next` path executes the auto_next edit.

## Requirements

### Functional Requirements

- **REQ-001**: The `codexspec config` command MUST accept a new `--auto-next` option that distinguishes three states — not passed, passed bare, and passed with a value — via a Typer sentinel default, structurally parallel to the existing `--set-lang` / `--set-interaction-lang` / `--set-document-lang` / `--set-commit-lang` options.
  - Sources: NEED-001, DEC-001, CON-003
- **REQ-002**: A bare `codexspec config --auto-next` MUST flip the current value of `workflow.auto_next` (`true → false`, `false → true`).
  - Sources: NEED-001, DEC-002
- **REQ-003**: `codexspec config --auto-next <value>` MUST set the value explicitly, accepting `on/off`, `true/false`, `1/0`, `yes/no` (case-insensitive), in both space-separated and `--auto-next=value` forms.
  - Sources: DEC-002, CON-001
- **REQ-004**: Reading the current state MUST treat only the literal token `true` as enabled; an absent key, an absent `workflow:` section, `false`, or any malformed value MUST be treated as `false`.
  - Sources: DEC-002, CON-002
- **REQ-005**: When the `workflow:` section and/or `auto_next` key is absent, the command MUST create the section/key as needed and write the resulting unquoted boolean.
  - Sources: CON-002
- **REQ-006**: All edits MUST be performed via line-based string manipulation (no YAML library), preserving every other line and comment byte-for-byte.
  - Sources: CON-002
- **REQ-007**: The command MUST scope its writes to `workflow.auto_next` only. It MUST NOT modify `language.*` or any other section, and MUST NOT alter the SDD chain / template runtime behavior (auto_next's chain-advance semantics already exist in the command templates).
  - Sources: DEC-004
- **REQ-008**: The command MUST NOT call `_rerender_command_frontmatter()` (that function serves only the language options; auto_next does not appear in command frontmatter).
  - Sources: DEC-005
- **REQ-009**: The `/codexspec:config` interactive menu MUST offer an auto_next entry (in the existing "Modify config" submenu) that toggles or explicitly sets `workflow.auto_next` using the same semantics as the CLI. The edit is made to the source template at `templates/commands/config.md`; the derived `.claude/commands/codexspec/config.md` and `.agents/skills/codexspec-config-*` forms are regenerated from it and must not be hand-edited.
  - Sources: DEC-006
- **REQ-010**: The CLI `codexspec config` command's terminal success and error messages MUST be hardcoded in English and stylistically consistent with the existing `config` option messages (e.g. `Language set to:`). The `/codexspec:config` slash command (REQ-009) is unaffected and continues to converse in the interaction language.
  - Sources: DEC-007
- **REQ-011**: When inserting a new `auto_next` key, the command MUST write a bare line (`auto_next: <bool>`) and MUST NOT reconstruct the original multi-line explanatory comment.
  - Sources: DEC-008
- **REQ-012**: When `.codexspec/config.yml` does not exist, the command MUST print `No CodexSpec project found` and exit with code 1.
  - Sources: DEC-003

### Non-Functional Requirements

- **NFR-001**: An invalid explicit value MUST print a red error message and exit with code 1; a successful edit MUST exit with code 0.
  - Sources: CON-001
- **NFR-002**: The `README.*.md` config-options tables and the CLI-examples block MUST be extended with `--auto-next` across all language versions (`README.md` plus `de`, `es`, `fr`, `ja`, `ko`, `pt-BR`, `zh-CN`). The `codexspec config --help` text MUST also list the new option.
  - Sources: CON-004
- **NFR-003**: Tests MUST cover: toggle `true → false` and `false → true`; explicit `on`/`off`; missing-key/missing-section creation; invalid-value rejection; and the no-project error — added alongside the existing `TestConfig` suite per the constitution's testing standards.
  - Sources: CON-001, CON-002, DEC-003

## Success Criteria

### Measurable Outcomes

- **SC-001**: A user can flip or set `workflow.auto_next` with a single command; re-reading `.codexspec/config.yml` shows the new unquoted boolean, and no manual YAML editing is required.
- **SC-002**: Existing lines and comments outside the `auto_next` value line are preserved (not altered); when the `workflow:` section/key must be created, only new lines are inserted.
- **SC-003**: All existing `config` options (`--set-lang`, `--set-interaction-lang`, `--set-document-lang`, `--set-commit-lang`, `--list-langs`) and the no-argument panel continue to behave exactly as before (no regressions).
- **SC-004**: A Plugin user without the CLI can change `workflow.auto_next` end-to-end via `/codexspec:config`.

## Out of Scope

- A positional subcommand form (`codexspec config auto-next`) and a top-level command (`codexspec auto-next`): excluded to keep the change minimal and consistent with the option-flag architecture. *(OUT-001)*
- A `--no-auto-next` flag: redundant with `--auto-next off`. *(OUT-001)*
- A `--show-auto-next` flag: viewing the current value is already served by the existing `codexspec config` no-argument panel. *(OUT-001)*
- Localizing the new (or existing) `config` messages to `language.interaction`: the new messages follow the existing English status quo; expanding localization is a separate effort. *(DEC-007)*
- Changing the `/codexspec:config` "Reset to defaults" behavior: it already produces a config without a `workflow:` section (auto_next absent = `false`), which is the correct safe default and remains unchanged.

## Assumptions

- The new `--auto-next` option coexists with the existing options on the same `config` command; only the `--auto-next` path performs the auto_next edit (the others retain their current behavior).
- "Literal `true`" means the unquoted YAML token `true`; the command writes unquoted booleans to match the existing `auto_next: true` style in this repo's config.

## Dependencies

- Existing `codexspec config` command in `src/codexspec/__init__.py` (the new option is added here).
- `templates/commands/config.md` (the `/codexspec:config` menu source of truth for REQ-009).
- The eight `README.*.md` files (documentation surface for NFR-002).
- Negative dependency: `_rerender_command_frontmatter()` is intentionally NOT invoked (REQ-008).

## Requirements Traceability

| Confirmed Requirement | Spec Coverage | Notes |
|-----------------------|---------------|-------|
| NEED-001 | REQ-001, REQ-002, US1, US2 | Core convenience goal |
| CON-001 | REQ-003, NFR-001 | Value validation + exit codes |
| CON-002 | REQ-004, REQ-005, REQ-006, NFR-003 | Missing-key handling, comment preservation |
| CON-003 | REQ-001 | Typer tri-state option |
| CON-004 | NFR-002 | Multilingual README + help updates |
| DEC-001 | REQ-001, Out of Scope | Option on existing command; alternatives rejected |
| DEC-002 | REQ-002, REQ-003, REQ-004 | Toggle + explicit semantics |
| DEC-003 | REQ-012, NFR-003 | No-project behavior |
| DEC-004 | REQ-007 | Scope limited to workflow.auto_next |
| DEC-005 | REQ-008 | No frontmatter re-render |
| DEC-006 | REQ-009, US3, SC-004 | /codexspec:config menu update |
| DEC-007 | REQ-010, Out of Scope | English hardcoded messages |
| DEC-008 | REQ-011 | Bare-line insertion |
| OUT-001 | Out of Scope | No subcommand / top-level / auxiliary flags |
