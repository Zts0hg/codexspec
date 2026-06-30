# Implementation Plan: config-auto-next

<!--
Language: Generate this document in the language specified in .codexspec/config.yml.
Document language = en.
-->

**Related Spec**: `.codexspec/specs/2026-0630-1757v1-config-auto-next/spec.md`
**Confirmed Requirements**: `.codexspec/specs/2026-0630-1757v1-config-auto-next/requirements.md`
**Created**: 2026-06-30
**Status**: Draft

## Context

`workflow.auto_next` (in `.codexspec/config.yml`) controls whether the SDD pipeline auto-advances once a stage passes. Today it can only be changed by hand-editing the YAML. This plan implements a toggle command across two surfaces:

1. **CLI** — a new `--auto-next` option on the existing `codexspec config` command (`src/codexspec/__init__.py:177-385`), structurally parallel to the existing `--set-lang` / `--set-interaction-lang` / `--set-document-lang` / `--set-commit-lang` options.
2. **Interactive slash command** — an auto_next entry in the `/codexspec:config` menu (`templates/commands/config.md`), for Plugin users without the CLI.

The codebase already has the exact shape of helper we need: `_update_project_ai` (`src/codexspec/__init__.py:885-898`) does a comment-preserving, regex-based update of a non-language scalar key (`project.ai`), and `update_language_field` (`src/codexspec/i18n.py:383-418`) shows the update-or-insert-under-section pattern. We mirror these rather than introducing a YAML library (confirmed in CON-002 / REQ-006).

### Configuration surface (the only data touched)

```yaml
workflow:
  auto_next: true   # unquoted boolean; read rule: only literal `true` => enabled
```

**Read rule**: `true` only when the literal token `true` is present; absent key/section, `false`, or any malformed value ⇒ `false`.
**Write rule**: emit unquoted `true` / `false` on a bare line (no reconstructed comment — DEC-008 / REQ-011).

## Goals / Non-Goals

**Goals:**

- Let users flip or set `workflow.auto_next` via `codexspec config --auto-next` (bare = toggle; `on|off` = explicit) and via the `/codexspec:config` menu — without hand-editing YAML.
- Preserve all other config content byte-for-byte (only the `auto_next` value line changes, or new lines are inserted when the section/key is absent).
- Keep the change minimal, consistent with the existing `config` architecture, with no breaking changes to sibling options.

**Non-Goals:**

- No positional subcommand (`config auto-next`), no top-level command, no `--no-auto-next`, no `--show-auto-next` (viewing uses the existing no-arg panel).
- No localization of `config` CLI messages (English, matching status quo).
- No change to the SDD chain / template runtime semantics or the `/codexspec:config` "Reset to defaults" behavior.

## Tech Stack

- **Language**: Python 3.11+
- **CLI**: Typer 0.24.1 (on Click 8.3.1) — both support the optional-value `flag_value` pattern used here.
- **Packaging**: uv + Hatchling.
- **Testing**: pytest (CliRunner), ruff for lint.

## Architecture Overview

Two independent surfaces write the same key through equivalent read/write logic.

**Covers**: REQ-001, REQ-002, REQ-003, REQ-009

```
CLI surface                                   /codexspec:config surface
─────────────────                             ──────────────────────────
codexspec config --auto-next [on|off]         /codexspec:config  → "Modify config"
        │                                              │
        ▼                                              ▼
 config() handler  (src/codexspec/__init__.py)         Agent follows template
   ├─ resolve tri-state (None / TOGGLE / value)        (templates/commands/config.md)
   ├─ parse_auto_next_value() → bool | ValueError        ├─ read current workflow.auto_next
   ├─ _read_auto_next() → current bool                   ├─ ask Enable / Disable
   ├─ target = TOGGLE ? !current : parsed                └─ write workflow.auto_next
   └─ _write_auto_next(config_file, target)
        │  regex update-in-place OR insert `workflow:` section
        ▼
 .codexspec/config.yml   →   workflow.auto_next: <true|false>
```

Note: the CLI path MUST NOT call `_rerender_command_frontmatter()` (REQ-008 / DEC-005) — that function (`src/codexspec/__init__.py:857-877`) is interaction-language-only and unrelated to `auto_next`.

## Component Structure (files touched)

```
src/codexspec/__init__.py
  ├─ config()                       # add --auto-next option + handler  (L177-385)
  ├─ parse_auto_next_value()        # NEW: value -> bool | ValueError
  ├─ _read_auto_next()              # NEW: config_file -> bool
  └─ _write_auto_next()             # NEW: config_file, bool -> bool (success)
templates/commands/config.md        # /codexspec:config menu: add auto_next entry
.claude/commands/codexspec/config.md        # regenerated (do NOT hand-edit)
.agents/skills/codexspec-config/          # regenerated (do NOT hand-edit)
README.md, README.{de,es,fr,ja,ko,pt-BR,zh-CN}.md   # config-options table + example
tests/test_cli.py                   # TestConfig: add auto_next tests
```

## Plan-Level Decisions

### PLD-1: Tri-state `--auto-next` via Click optional-value (`flag_value`)

**Context**: The handler must distinguish *not passed* (do nothing), *bare* (`--auto-next` → toggle), and *with value* (`--auto-next off` → explicit). `Optional[str]` alone cannot express bare-toggle because Click then requires a value.

**Options Considered**:

1. Click optional-value: `typer.Option(None, "--auto-next", is_flag=False, flag_value=SENTINEL)`.
2. Two options: a bool `--auto-next` (toggle) + `--set-auto-next <v>` (explicit).
3. `Optional[str]` only (no bare-toggle).

**Decision**: Option 1 — a single `--auto-next` with `is_flag=False, flag_value="__TOGGLE__"`. Absent ⇒ `None`; bare ⇒ `"__TOGGLE__"`; with-value ⇒ the value.

**Rationale**: Keeps a single option (DEC-001 parallelism, DEC-002 unified semantics). Typer 0.24.1 + Click 8.3.1 support this pattern. Accepted trade-off: relies on Click optional-value behavior; verified early in Phase 2 (Risk R1).

**Covers**: REQ-001, CON-003

**Decision Level**: Plan-level technical decision; does not change confirmed product scope.

### PLD-2: Boolean parsing helper `parse_auto_next_value`

**Context**: Explicit values must accept a fixed, case-insensitive token set and reject everything else.

**Decision**: `parse_auto_next_value(raw: str) -> bool` maps `on/true/1/yes` → `True`, `off/false/0/no` → `False` (case-insensitive); any other token raises `ValueError`. The caller catches it, prints a red error listing the accepted tokens, and exits 1.

**Rationale**: Matches the confirmed set in DEC-002 exactly; centralizes validation (NFR-001).

**Covers**: REQ-003, NFR-001

### PLD-3: Read/write helpers mirroring `_update_project_ai` / `update_language_field`

**Context**: We need comment-preserving, line-based edits and must handle an absent section/key (REQ-005).

**Decision**:

- `_read_auto_next(config_file: Path) -> bool`: regex under the `workflow:` section for `auto_next:\s*(\S+)`; literal `true` ⇒ `True`, everything else (incl. absent) ⇒ `False`.
- `_write_auto_next(config_file: Path, value: bool) -> bool`: if an `auto_next:` line exists, regex-replace its value in place; otherwise **append a `workflow:` section at the end of the file** as:

  ```
  workflow:
    auto_next: <bool>
  ```

  (ensuring exactly one blank line before it; 2-space indent; bare line, no comment). Returns `True` on success, `False` on I/O error.

**Rationale**: Reuses the proven regex pattern of `_update_project_ai` (L885) and the update-or-insert shape of `update_language_field` (i18n.py:383). Append-at-end resolves review advisory RA-1 — simplest placement that is always valid YAML and yields minimal, predictable diffs.

**Covers**: REQ-004, REQ-005, REQ-006, REQ-011

### PLD-4: Handler wiring and ordering inside `config()`

**Context**: The new option must coexist with the existing options and the no-project guard.

**Decision**: Add `auto_next` as a parameter to `config()`. Handle it **immediately after the `config_file` existence check** (`src/codexspec/__init__.py:233-236`, which already prints `No CodexSpec project found` and exits 1) and **before** the `set_lang` branch, then `return`. Do NOT call `_rerender_command_frontmatter()`.

**Rationale**: Placing it after the existence check satisfies REQ-012; early return keeps it orthogonal to the language options (REQ-007). Skipping the frontmatter re-render satisfies REQ-008.

**Covers**: REQ-001, REQ-007, REQ-008, REQ-012

### PLD-5: English output messages, consistent with sibling options

**Context**: DEC-007 requires English messages matching the existing style (`[green]Language set to:[/green] …`).

**Decision**:

- Success: `[green]auto_next enabled[/green] (workflow.auto_next = true)` / `[green]auto_next disabled[/green] (workflow.auto_next = false)`.
- Invalid value: `[red]Invalid --auto-next value '<v>'[/red]` + a line listing accepted tokens; exit 1.

**Rationale**: Consistent with the four existing `config` success messages; scoped to the CLI only (REQ-010).

**Covers**: REQ-010, NFR-001

### PLD-6: `/codexspec:config` menu entry

**Context**: Plugin users need a non-CLI path (DEC-006).

**Decision**: In `templates/commands/config.md`, add an option to the existing "Modify config" submenu (L93-132): `{"label": "Auto-next chain", "description": "Auto-advance the SDD pipeline once a stage passes (workflow.auto_next) (currently: {current})"}`. When chosen, present `AskUserQuestion`: **Enable** / **Disable** / **Back**. On Enable/Disable, the agent reads the current value, writes the new unquoted boolean (same read/write semantics as the CLI), preserves all other content, and displays the updated config. The source edit is in `templates/commands/config.md`; `.claude/commands/codexspec/config.md` and `.agents/skills/codexspec-config` are regenerated (never hand-edited).

**Rationale**: Same surface and semantics as the CLI; lives in the template source of truth per the Self-bootstrap rule.

**Covers**: REQ-009, DEC-006

### PLD-7: Documentation across 8 READMEs + help text

**Context**: The `config` options are enumerated in every README's "config Options" table (CON-004).

**Decision**: Add a row `| \`--auto-next\` | Toggle/set \`workflow.auto_next\` (bare toggles; or on\|off) |` to the table in `README.md` and `README.{de,es,fr,ja,ko,pt-BR,zh-CN}.md` (table at `README.md:505-511`), and add`codexspec config --auto-next`to the examples block (`README.md:631-634`). Also extend the`config()`docstring examples (`src/codexspec/**init**.py:212-216`) so`codexspec config --help` lists the option.

**Rationale**: Keeps the new option discoverable everywhere the others are documented.

**Covers**: NFR-002, CON-004

### PLD-8: Test placement and cases

**Context**: Constitution mandates tests for all new functionality.

**Decision**: Add cases to `tests/test_cli.py` `TestConfig` (fixtures `runner` / `isolated_runner` at L14-20): write a `.codexspec/config.yml` directly, then assert via `runner.invoke(app, ["config", "--auto-next", ...])`. Cases: toggle `true→false` and `false→true`; explicit `on`/`off` (incl. `TRUE`/`1`/`yes` and `false`/`0`/`no`); create-when-missing (key absent; whole `workflow:` section absent); invalid value ⇒ exit 1 and file unchanged; no-project ⇒ exit 1; coexistence (sibling options unaffected).

**Rationale**: Mirrors the existing `TestConfig` and language-config test style; covers NFR-003.

**Covers**: NFR-003, REQ-002, REQ-003, REQ-004, REQ-005, REQ-012

## Risks / Trade-offs

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| R1 — Typer/Click `flag_value` optional-value behaves unexpectedly in this Typer version | Low | Medium | Verify bare-vs-value resolution in Phase 2 first. Fallback: parse the raw token from `sys.argv`, or (last resort) make bare-toggle a documented minor UX change and request user confirmation. |
| R2 — Self-bootstrap drift: derived `.claude/commands/codexspec/config.md` not regenerated after template edit | Medium | Low | Phase 4 explicitly runs the regeneration/sync step; verify the derived file contains the new menu entry before finishing. |
| R3 — Section insertion produces invalid YAML (no trailing newline / duplicate `workflow:`) | Low | Medium | `_write_auto_next` appends only when no `workflow:`/`auto_next` exists; ensures a preceding blank line; covered by the "section absent" test. |

## Implementation Phases

### Phase 1: Helpers (TDD)

- [ ] Implement `parse_auto_next_value` (`src/codexspec/__init__.py`)
- [ ] Implement `_read_auto_next` and `_write_auto_next` (regex update + append-section)
- [ ] Unit-test parsing (truthy/falsy/invalid) and read/write (existing key, absent key, absent section, comment preservation)
- **Covers**: REQ-003, REQ-004, REQ-005, REQ-006, REQ-011, NFR-001 (parse), NFR-003 (helpers)

### Phase 2: Wire the CLI option

- [ ] Add `--auto-next` option (`is_flag=False, flag_value="__TOGGLE__"`) to `config()` (PLD-1/PLD-4)
- [ ] Add handler after the no-project check: resolve tri-state → parse/toggle → read current → write → print English message (PLD-5); do NOT call `_rerender_command_frontmatter`
- [ ] Verify R1 (bare vs. explicit) with `codexspec config --help` and a manual smoke run
- **Covers**: REQ-001, REQ-002, REQ-007, REQ-008, REQ-010, REQ-012, CON-003

### Phase 3: CLI integration tests

- [ ] Add `TestConfig` cases: toggle both directions; explicit on/off + aliases; missing-key and missing-section creation; invalid value (exit 1, file unchanged); no-project (exit 1); sibling-option coexistence
- **Covers**: NFR-003, REQ-002, REQ-003, REQ-004, REQ-005, REQ-012

### Phase 4: `/codexspec:config` template + regenerate

- [ ] Edit `templates/commands/config.md` "Modify config" submenu + Enable/Disable flow (PLD-6)
- [ ] Regenerate `.claude/commands/codexspec/config.md` and `.agents/skills/codexspec-config`; verify the entry appears (mitigates R2)
- **Covers**: REQ-009, DEC-006

### Phase 5: Documentation

- [ ] Add `--auto-next` row + example to all 8 READMEs (PLD-7)
- [ ] Extend the `config()` docstring examples
- **Covers**: NFR-002, CON-004

### Phase 6: Verification & regression

- [ ] `uv run pytest` (full suite green; existing `TestConfig` and language tests unchanged)
- [ ] `uv run ruff check src/`
- [ ] Manual smoke: toggle, explicit, missing-section, invalid, no-project; `codexspec config --help`
- **Covers**: all (regression guard)

## Verification Strategy

- **Automated**: pytest (`tests/test_cli.py` + helper unit tests) and `ruff check src/`.
- **Manual smoke** (in a scratch project): `codexspec config --auto-next` flips the value; `--auto-next off`/`on` set it; missing `workflow:` is created; bad value exits 1 with the file untouched; `codexspec config` (no args) still shows the panel; sibling options still work.
- **Template check**: after regeneration, the `/codexspec:config` derived file shows the new menu entry.
- **Regression**: all pre-existing `config` and language tests remain green.

## Security Considerations

- Minimal surface: the command writes one local file (`.codexspec/config.yml`) using a bounded, validated boolean; the only untrusted input is the CLI token, validated by `parse_auto_next_value` (reject-by-default). No network, no shell, no template expansion.

## Requirements Coverage

| Spec Requirement | Plan Coverage | Reference |
|------------------|---------------|-----------|
| REQ-001 | Full | PLD-1, PLD-4 / Phase 2 |
| REQ-002 | Full | PLD-4 / Phase 2-3 |
| REQ-003 | Full | PLD-2 / Phase 1, 3 |
| REQ-004 | Full | PLD-3 (`_read_auto_next`) / Phase 1, 3 |
| REQ-005 | Full | PLD-3 (`_write_auto_next` insert) / Phase 1, 3 |
| REQ-006 | Full | PLD-3 (line-based, comment-preserving) / Phase 1 |
| REQ-007 | Full | PLD-4 (scope) / Phase 2 |
| REQ-008 | Full | PLD-4 (no `_rerender_command_frontmatter`) / Phase 2 |
| REQ-009 | Full | PLD-6 / Phase 4 |
| REQ-010 | Full | PLD-5 / Phase 2 |
| REQ-011 | Full | PLD-3 (bare line) / Phase 1 |
| REQ-012 | Full | PLD-4 (existing guard) / Phase 2-3 |
| NFR-001 | Full | PLD-2, PLD-5 / Phase 1-3 |
| NFR-002 | Full | PLD-7 / Phase 5 |
| NFR-003 | Full | PLD-8 / Phase 3 |
