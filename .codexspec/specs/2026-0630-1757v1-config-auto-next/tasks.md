# Tasks: config-auto-next

<!--
Language: Generate this document in the language specified in .codexspec/config.yml.
Document language = en.
-->

**Input**: `.codexspec/specs/2026-0630-1757v1-config-auto-next/{requirements,spec,plan}.md`
**Prerequisites**: plan.md (required), spec.md (required for user stories)
**Organization**: Grouped by the approved plan's technical phases (the plan is phase-organized). User-story mapping is noted per task: US1/US2 = CLI toggle/explicit; US3 = `/codexspec:config` menu.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: can run in parallel with its declared dependencies satisfied (different files, no blocking relation).
- **[Story]**: user-story mapping (US1/US2 = CLI, US3 = slash menu).
- Each task has exact paths, `Covers: REQ-xxx; Plan: <component/phase>`, and a single verifiable outcome.

---

## Phase 1: Helpers (test-first)

**Purpose**: Pure functions for parsing and read/write, with unit tests written first (plan Phase 1 is TDD).

- [x] **T001** [US1/US2] Implement `parse_auto_next_value(raw: str) -> bool` in `src/codexspec/__init__.py`, mapping `on/true/1/yes` → `True` and `off/false/0/no` → `False` (case-insensitive); any other token raises `ValueError`.
  - Write unit tests first (truthy, falsy, case variants, invalid → `ValueError`) in `tests/test_cli.py` (or a new `tests/test_config_auto_next.py`); confirm they fail, then implement.
  - **Verify**: the unit tests pass; `uv run ruff check src/` stays clean.
  - **Covers**: REQ-003, NFR-001; **Plan**: PLD-2 / Phase 1
- [x] **T002** [US1/US2] Implement `_read_auto_next(config_file: Path) -> bool` and `_write_auto_next(config_file: Path, value: bool) -> bool` in `src/codexspec/__init__.py`, mirroring `_update_project_ai` (L885) / `update_language_field` (i18n.py:383).
  - `_read_auto_next`: scoped to the `workflow:` section; literal token `true` ⇒ `True`; absent key/section, `false`, or malformed ⇒ `False`.
  - `_write_auto_next`: regex-update the `auto_next:` value in place when present; otherwise append a `workflow:` section at end of file as `workflow:\n  auto_next: <bool>` (one preceding blank line, 2-space indent, bare line — no reconstructed comment); return `False` on I/O error.
  - Write unit tests first (existing key, absent key, absent `workflow:` section, malformed value, comment preservation, idempotent write); confirm they fail, then implement.
  - **Verify**: unit tests pass; a config with comments is byte-preserved outside the value line.
  - **Covers**: REQ-004, REQ-005, REQ-006, REQ-011; **Plan**: PLD-3 / Phase 1

---

## Phase 2: Wire the CLI option

**Purpose**: Expose `--auto-next` on the `config` command (US1 toggle + US2 explicit).

- [x] **T003** [US1/US2] Add the `--auto-next` option and handler to `config()` in `src/codexspec/__init__.py` (L177-385). Depends on T001, T002.
  - Option: `typer.Option(None, "--auto-next", is_flag=False, flag_value="__TOGGLE__", help=...)` — tri-state: `None` (not passed) / `"__TOGGLE__"` (bare) / value (explicit).
  - Handler placed **immediately after** the existing no-project guard (L233-236) and **before** `set_lang`, then `return`.
  - Resolve: bare ⇒ `target = not _read_auto_next(config_file)`; explicit ⇒ `target = parse_auto_next_value(value)` (catch `ValueError` → red error listing accepted tokens + `raise typer.Exit(1)`). Then `_write_auto_next(config_file, target)` and print `[green]auto_next enabled/disabled[/green] (workflow.auto_next = <bool>)`.
  - Do NOT call `_rerender_command_frontmatter()`.
  - Extend the `config()` docstring examples (L212-216) with `codexspec config --auto-next`.
  - **Verify**: `uv run codexspec config --help` lists `--auto-next`; bare toggle flips the value; `on/off` set it; bad value exits 1 with the file unchanged; sibling options still work; the no-project case prints `No CodexSpec project found in current directory.` and exits 1.
  - **Covers**: REQ-001, REQ-002, REQ-007, REQ-008, REQ-010, REQ-012; **Plan**: PLD-1, PLD-4, PLD-5 / Phase 2

---

## Phase 3: CLI integration tests

**Purpose**: End-to-end coverage through the CLI (NFR-003).

- [ ] **T004** [US1/US2] Add cases to `TestConfig` in `tests/test_cli.py` (fixtures `runner` / `isolated_runner`, L14-20, L66): write a `.codexspec/config.yml` directly and assert via `runner.invoke(app, ["config", "--auto-next", ...])`. Depends on T003.
  - Cases: toggle `true→false` and `false→true`; explicit `on`/`off` (incl. `TRUE`/`1`/`yes` and `false`/`0`/`no`); create-when-key-absent; create-when-`workflow:`-section-absent; invalid value ⇒ exit 1 and file unchanged; no-project ⇒ exit 1; coexistence with `--set-lang` (sibling option unaffected).
  - **Verify**: `uv run pytest tests/test_cli.py -k "config or auto_next"` is green; existing `TestConfig` tests still pass.
  - **Covers**: NFR-003, REQ-002, REQ-003, REQ-004, REQ-005, REQ-012; **Plan**: PLD-8 / Phase 3

---

## Phase 4: `/codexspec:config` template + regenerate

**Purpose**: Non-CLI surface (US3 / DEC-006).

- [ ] **T005** [P] [US3] Update the interactive menu in `templates/commands/config.md` and regenerate the derived copies. No code dependency; may run in parallel with Phase 1-3.
  - In the "Modify config" submenu (L93-132) add an option, e.g. `{"label": "Auto-next chain", "description": "Auto-advance the SDD pipeline once a stage passes (workflow.auto_next) (currently: {current})"}`.
  - When chosen, present `AskUserQuestion`: **Enable** / **Disable** / **Back**; on Enable/Disable, read the current value, write the new unquoted boolean (same read/write semantics), preserve all other content, and display the updated config.
  - Sync the change to the derived copies: `.claude/commands/codexspec/config.md` and `.agents/skills/codexspec-config` (re-run `codexspec init`, or copy `templates/commands/config.md` to both). Do not hand-edit the derived files.
  - **Verify**: both derived files contain the new menu entry; the template's other options are unchanged.
  - **Covers**: REQ-009, DEC-006; **Plan**: PLD-6 / Phase 4

---

## Phase 5: Documentation

**Purpose**: Discoverability across all READMEs + help text (CON-004).

- [ ] **T006** [US1/US2] Document `--auto-next` in all 8 READMEs and the CLI help. Depends on T003 (document the finalized option).
  - Add a row to the "config Options" table (e.g. `README.md:505-511`): `` | `--auto-next` | Toggle/set `workflow.auto_next` (bare toggles; or on\|off) | `` — in `README.md`, `README.de.md`, `README.es.md`, `README.fr.md`, `README.ja.md`, `README.ko.md`, `README.pt-BR.md`, `README.zh-CN.md`.
  - Add `codexspec config --auto-next` to the examples block (`README.md:631-634`) in each README that has one.
  - Confirm the `config()` docstring example added in T003 renders in `codexspec config --help`.
  - **Verify**: `codexspec config --help` shows `--auto-next`; each of the 8 READMEs lists it.
  - **Covers**: NFR-002, CON-004; **Plan**: PLD-7 / Phase 5

---

## Phase 6: Final verification

**Purpose**: Regression gate before the feature is considered done.

- [ ] **T007** Run the full suite and a manual smoke. Depends on T004, T005, T006.
  - `uv run pytest` (full suite green; pre-existing `config` and language tests unchanged).
  - `uv run ruff check src/` clean.
  - Manual smoke in a scratch project: `codexspec config --auto-next` (toggle), `--auto-next off`/`on` (explicit), missing `workflow:` (created), invalid value (exit 1, file unchanged), no-project (exit 1), `codexspec config` (no args → panel still works), `/codexspec:config` menu shows the new entry.
  - **Verify**: all green; no regressions.
  - **Covers**: all (regression guard); **Plan**: Phase 6

---

## Dependencies & Execution Order

- **Phase 1** — T001, T002: both edit `src/codexspec/__init__.py`, so sequence them (order between them is arbitrary); test-first.
- **Phase 2** — T003: depends on T001 + T002.
- **Phase 3** — T004: depends on T003.
- **Phase 4** — T005: no code dependency (`[P]`); may run alongside Phase 1-3.
- **Phase 5** — T006: depends on T003.
- **Phase 6** — T007: depends on T004 + T005 + T006 (final gate).

Dependency graph (acyclic): `T001,T002 → T003 → {T004, T006}`; `T005` independent; `T004, T005, T006 → T007`.

---

## Coverage Table

| Plan component / REQ | Tasks | Notes |
|----------------------|-------|-------|
| REQ-001 (`--auto-next` option) | T003 | PLD-1 |
| REQ-002 (bare toggle) | T003, T004 | PLD-4 |
| REQ-003 (explicit values) | T001, T003, T004 | PLD-2 |
| REQ-004 (read rule) | T002, T004 | PLD-3 |
| REQ-005 (create section/key) | T002, T004 | PLD-3 |
| REQ-006 (line-based, comments) | T002 | PLD-3 |
| REQ-007 (scope) | T003, T004 | PLD-4 |
| REQ-008 (no frontmatter re-render) | T003 | PLD-4 |
| REQ-009 (`/codexspec:config` menu) | T005 | PLD-6 |
| REQ-010 (English messages) | T003 | PLD-5 |
| REQ-011 (bare-line insert) | T002 | PLD-3 |
| REQ-012 (no-project) | T003, T004 | PLD-4 |
| NFR-001 (validation/exit codes) | T001, T003, T004 | PLD-2/5 |
| NFR-002 (READMEs + help) | T006 | PLD-7 |
| NFR-003 (tests) | T001, T002, T004 | PLD-8 |

## Unmapped Tasks

None. All seven tasks trace to a plan component/requirement or to necessary implementation support (T007 verification gate).
