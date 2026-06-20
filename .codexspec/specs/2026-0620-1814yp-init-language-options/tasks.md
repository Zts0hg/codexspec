# Tasks: init-language-options

<!--
Language: Generate this document in the language specified in .codexspec/config.yml
If not configured, use English.
-->

**Input**: `.codexspec/specs/2026-0620-1814yp-init-language-options/{requirements.md, spec.md, plan.md}`
**Prerequisites**: plan.md (required), spec.md (required)

**Tests**: The constitution requires tests for all new functionality; it does not mandate strict
test-first ordering, and the existing workflow co-locates tests with implementation. Verification is
therefore included as dedicated tasks (T2, T6) plus end-of-phase checkpoints, not imposed as TDD
throughout.

**Organization**: Grouped by the approved plan's technical phases (Phase 1 → Phase 5), since the
plan is layered by component (i18n → init input → init writes → `--force` → verification) rather
than by user story.

## Format

`[T-id] [P?] Description. Covers: REQ-xxx; Plan: <phase/PLD>. Files: … Depends: …`

- **[P]**: can run in parallel with the prior task (different file, no dependency).
- Exact paths are taken from `plan.md` / verified repository facts; none are invented.

---

## Phase 1: i18n layer (foundation)

**Purpose**: Refactor the config-generation and commit-resolution helpers that all later phases
depend on. Blocks the init write path (T4).

- [x] **T1** Refactor `generate_config_content` in `src/codexspec/i18n.py` to a sparse,
  per-dimension signature `(*, output=None, interaction=None, document=None, commit=None,
  created=None)` that emits only the non-`None` language keys (always keeping `templates: "en"`,
  `version`, `project`); no-arg defaults to `output="en"`. Also add an `output` fallback to
  `get_commit_language` (resolve `commit` → `output` → `"en"`), matching `commit-staged.md`.
  Update the single runtime caller at `src/codexspec/__init__.py:642` is handled in T4.
  Covers: REQ-002, REQ-003, REQ-004, REQ-005; Plan: PLD-1 / Phase 1.
  Files: `src/codexspec/i18n.py`. Depends: —.

- [x] **T2** Add unit tests in `tests/test_i18n.py` for T1: `generate_config_content` emits only
  the specified key(s) (sparse), including the no-arg `output="en"` case and a multi-key case; and
  `get_commit_language` resolves `commit` → `output` → `"en"`. (Updates the existing
  `TestGenerateConfigContent` assertions that assumed all four keys.)
  Covers: REQ-002, REQ-003, REQ-004; Plan: Phase 1, NFR-005.
  Files: `tests/test_i18n.py`. Depends: T1.

**Checkpoint**: i18n helpers produce sparse config and correct commit resolution; `uv run pytest
tests/test_i18n.py` passes.

---

## Phase 2: init CLI surface + base resolution

**Purpose**: Give `init` the new flags and the correct prompt/default logic.

- [x] **T3** [P] Extend the `init` command in `src/codexspec/__init__.py`:
  (a) add three long-only Typer options `--interaction-lang` / `--document-lang` / `--commit-lang`
  (`Optional[str]`, default `None`);
  (b) build a `{key: value}` map from the flags (no CLI precedence — each flag maps to its own key,
  `--lang`→`output`);
  (c) restructure base resolution (PLD-4): compute `target_dir` and whether `config.yml` exists
  before resolving the language; show the selection prompt **only** on first-time init when the base
  is undeterminable (`--lang` not given AND the three specific flags not all given) AND stdin is a
  TTY; when `config.yml` already exists and no flag is given, do not prompt and preserve all keys
  (use `get_interaction_language(config_file)` for message language); on first-time non-TTY with no
  determinable base, default `output` to `en`;
  (d) apply warn-not-error validation per flag reusing `normalize_locale` / `is_supported_language`
  (same pattern as the `config` command at `__init__.py:337-347`).
  This task does NOT yet write config (T4) or touch `--force` (T5); it produces the resolved key map
  and correct prompt gating.
  Covers: REQ-001, REQ-006, REQ-007, REQ-008, REQ-011; Plan: PLD-3, PLD-4 / Phase 2, NFR-001,
  NFR-002.
  Files: `src/codexspec/__init__.py`. Depends: — (parallel with T1/T2; different file, uses existing
  helpers).

**Checkpoint**: with any language flag supplied, `prompt_language_selection` is not called and no
language confirm appears; first-time TTY with no base still prompts; existing-config + no flag does
not prompt.

---

## Phase 3: Surgical config writes + notices

**Purpose**: Persist the resolved keys surgically and emit the required notices.

- [x] **T4** In `src/codexspec/__init__.py` `init`, consume the resolved key map from T3:
  (a) on fresh init (no `config.yml`), write only the resolved keys via the refactored
  `generate_config_content` (T1);
  (b) on re-init, write each resolved key with `update_language_field` (`src/codexspec/i18n.py:359`)
  so all unspecified language keys are preserved byte-for-byte; remove the old fan-out /
  `update_config_language` / `update_output_language` commit-diff branch (`__init__.py:639-685`);
  (c) print a non-blocking notice listing each key written and its value;
  (d) after a first-time interactive selection, print the discoverability notice naming the three
  new flags (and `config`).
  Add the two new message keys (e.g. `cli.init.language_dimensions_hint`,
  `cli.init.language_key_set`) to `src/codexspec/translator.py`, mirroring existing `cli.init.*`
  keys.
  Covers: REQ-002, REQ-005, REQ-009, REQ-010; Plan: PLD-1, PLD-2, PLD-6 / Phase 3, NFR-001.
  Files: `src/codexspec/__init__.py`, `src/codexspec/translator.py`. Depends: T1, T3.

**Checkpoint**: `init proj --interaction-lang en --document-lang zh-CN --commit-lang en` writes
exactly those three keys; `init proj --lang zh-CN` writes only `output`; re-init with one flag
changes only that key.

---

## Phase 4: Unify `--force`

**Purpose**: Make `--force` a single "overwrite + don't ask" switch.

- [x] **T5** In `src/codexspec/__init__.py` `init`:
  (a) gate the three `Confirm.ask` calls — migration (`__init__.py:594`) and command-update
  (`__init__.py:606`, `__init__.py:613`) — as `if force or Confirm.ask(...)` so `--force`
  auto-proceeds;
  (b) remove `or force` from the config regeneration condition (`__init__.py:641` →
  `if not config_file.exists():`) so `--force` no longer regenerates config (writes stay surgical per
  T4).
  Also update the `--force` help text to state it suppresses prompts and no longer resets config.
  Covers: REQ-012, REQ-013; Plan: PLD-5 / Phase 4, DEC-008, CON-005.
  Files: `src/codexspec/__init__.py`. Depends: T3, T4.

**Checkpoint**: `init . --force <language flags>` on an already-initialized project exits 0 with
zero confirmation prompts and preserves unspecified language keys.

---

## Phase 5: Test updates + verification

**Purpose**: Update coupled tests and verify the full behavior matrix.

- [x] **T6** Tests and verification:
  (a) update `tests/test_i18n.py::TestGenerateConfigContent` for the sparse shape/signature (already
  started in T2; finalize any remaining assertions);
  (b) update `tests/test_init_language.py` prompt tests for first-time-only behavior, and add tests
  for: per-dimension flags, surgical preservation on re-init, non-interactive non-TTY runs,
  `--force` prompt suppression;
  (c) add subprocess (non-TTY) command-level tests asserting SC-001..SC-004 from `spec.md`;
  (d) verify backward compatibility — `init --lang zh-CN` resolves interaction/document/commit to
  zh-CN (REQ-014) — and determinism — same flags ⇒ identical `config.yml` language content
  (NFR-003);
  (e) run `uv run pytest`, then `uv run ruff check src/`.
  Covers: REQ-014; Plan: Phase 5; NFR-003, NFR-004, NFR-005.
  Files: `tests/test_i18n.py`, `tests/test_init_language.py` (+ new subprocess test module if
  needed). Depends: T1, T2, T3, T4, T5.

**Checkpoint**: full suite green; ruff clean; SC-001..SC-004 pass.

---

## Dependencies & Execution Order

```
T1 (i18n) ──► T2 (i18n tests)
   │
   └──► T4 (writes) ◄── T3 (input/resolution)
            │
            └──► T5 (--force)
                     │
                     └──► T6 (tests + verification) ◄── (T1, T2, T3)
```

- T1 is the foundation; T2 validates it.
- T3 is parallel with T1/T2 (`__init__.py` vs `i18n.py`, no code dependency) — marked **[P]**.
- T4 depends on T1 (sparse `generate_config_content`) and T3 (resolved key map).
- T5 depends on T3 and T4 (same `init` function).
- T6 depends on all implementation tasks.
- Dependency graph is acyclic; every dependent is ordered after its dependencies.

## Parallel Opportunities

- T3 can run concurrently with T1/T2 (different file, uses only existing helpers).
- Within `__init__.py`, T3 → T4 → T5 are sequential (same function).

## Unmapped Tasks

None. Every task maps to a plan phase/PLD and at least one requirement. No polish, documentation,
monitoring, or abstraction tasks were added (none required by the approved plan).

## Coverage

| Plan component / Requirement | Task(s) | Notes |
|------------------------------|---------|-------|
| Phase 1 / PLD-1 | T1, T2 | i18n sparse + commit fallback |
| Phase 2 / PLD-3, PLD-4 | T3 | init options + base resolution |
| Phase 3 / PLD-1, PLD-2, PLD-6 | T4 | surgical writes + notices |
| Phase 4 / PLD-5 | T5 | unified `--force` |
| Phase 5 | T6 | test updates + verification |
| REQ-001 | T3 | |
| REQ-002 | T1, T4 | |
| REQ-003 | T1 | existing resolution retained; commit fallback added |
| REQ-004 | T1 | |
| REQ-005 | T1, T4 | |
| REQ-006 | T3 | |
| REQ-007 | T3 | |
| REQ-008 | T3 | |
| REQ-009 | T4 | |
| REQ-010 | T4 | |
| REQ-011 | T3 | |
| REQ-012 | T5 | |
| REQ-013 | T5 | |
| REQ-014 | T6 | backward-compat verification |
| NFR-001 | T1, T3, T4 | reuse helpers / `config` patterns |
| NFR-002 | T3 | |
| NFR-003 | T6 | determinism check |
| NFR-004 | T6 | subprocess non-TTY tests |
| NFR-005 | T2, T6 | test updates + new coverage |

## Notes

- T3, T4, T5 all edit the `init` function in `src/codexspec/__init__.py`; they are sequenced, not
  parallel.
- Commit after each task or logical group; validate at each checkpoint before proceeding.
- T4 removes init's fan-out branch, which is the **only** caller of `update_config_language` and
  `update_output_language` (verified: `config` does its own inline replacement and does not call
  them; the `tests/scripts/python/fixtures/real_messages.py` matches are chat-message fixture
  strings, not code). Both helpers become dead code and should be removed (and de-imported) as part
  of T4.
