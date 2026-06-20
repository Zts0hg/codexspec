# Implementation Plan: init-language-options

<!--
Language: Generate this document in the language specified in .codexspec/config.yml
If not configured, use English.
-->

**Related Spec**: `.codexspec/specs/2026-0620-1814yp-init-language-options/spec.md`
**Confirmed Requirements**: `.codexspec/specs/2026-0620-1814yp-init-language-options/requirements.md`
**Created**: 2026-06-20
**Status**: Draft

## Context

`codexspec init` currently exposes only `--lang` / `-l`, treated as a single "output language"
and written to **all four** `config.yml` language keys via `generate_config_content`
(`src/codexspec/i18n.py:228`). The sibling `config` command already implements the target model:
four independent setters (`--set-lang` / `--set-interaction-lang` / `--set-document-lang` /
`--set-commit-lang`), each writing one key via `update_language_field`
(`src/codexspec/__init__.py:337-373`). `init` also cannot run fully non-interactively: it shows a
numbered selection prompt whenever `--lang` is absent in a TTY (`__init__.py:482-494`) and raises
confirmation dialogs on re-init (`__init__.py:594, 606, 613`).

This plan brings `init` to the same one-flag-per-key model as `config`, makes flag-driven init
non-interactive, and unifies `--force` into a single "overwrite + don't ask" switch. It reuses the
existing i18n helpers and the `config` command's validation/write patterns rather than introducing
new abstractions.

## Goals / Non-Goals

**Goals:**

- Add `--interaction-lang`, `--document-lang`, `--commit-lang` to `init`; make `--lang` set only
  `output`.
- Make `init` non-interactive whenever language flags are supplied (incl. re-init via `--force`).
- Preserve unspecified language keys on every write (surgical), including under `--force`.
- Keep `init` and `config` language behavior identical for the same code.

**Non-Goals:**

- Changing the `config` command (CON-002).
- Adding/removing `config.yml` keys (CON-004), or adding a global `--non-interactive` flag (OUT-001).
- Revisiting `--force`'s CLAUDE.md overwrite (pre-existing axis-A behavior).

## Tech Stack

- **Language**: Python 3.11+
- **CLI Framework**: Typer (Rich for output), existing `translate()` message system
- **Test Runner**: pytest (subprocess + `monkeypatch`/`patch` patterns already in
  `tests/test_init_language.py`, `tests/test_i18n.py`)
- **No new dependencies.**

## Architecture Overview

The change is localized to two layers: the i18n helpers (`src/codexspec/i18n.py`) and the `init`
command (`src/codexspec/__init__.py`). No new modules. The core data flow:

**Covers**: REQ-001, REQ-002, REQ-003, REQ-005

```
 init flags                          keys to write              config.yml effect
 ─────────────────                   ────────────────           ──────────────────
 --lang X          ─┐                output: X        ─┐        output set;
 --interaction-lang A │  resolve →   interaction: A     │        others preserved
 --document-lang B   │  (flag→key,   document: B       │  ──►    (fresh: create sparse;
 --commit-lang C   ─┘    no CLI      commit: C         ─┘         re-init: update_language_field)
                        precedence)
                                                          read-time resolution (unchanged for
                                                          interaction/document; NEW for commit):
                                                          key → output → "en"
```

Language-base resolution order inside `init` (replaces the current early unconditional prompt):

```
target_dir + config.yml existence known first
  │
  ├─ base determinable? (--lang given OR all three specific flags given)
  │       ── yes ──► write resolved keys (output from --lang if given);
  │                   no prompt, no confirm                            [REQ-006]
  │
  └─ base NOT determinable (no --lang and not all three flags):
        ├─ config.yml exists ──► preserve all keys (NO prompt)         [REQ-007]
        └─ first-time:
              ├─ TTY    ──► selection prompt → sets output              [REQ-007, REQ-009]
              └─ non-TTY ──► output defaults "en"                       [REQ-008]
        (any specific flags that WERE given are still written, alongside
         the resolved/prompted/default output)
```

## Component Structure

Files touched (all pre-existing; no new files except tests):

```
src/codexspec/
├── __init__.py        # init command: new options, flag→key resolution, surgical writes,
│                      #   first-time-only prompt, --force prompt suppression, notices
└── i18n.py            # generate_config_content (sparse), get_commit_language (output fallback)
tests/
├── test_i18n.py       # update generate_config_content tests; add commit-fallback test
└── test_init_language.py  # update prompt/shape tests; add per-dimension, preservation,
                           #   non-interactive, --force tests
```

## Data Model (config.yml schema — unchanged key set)

**Covers**: CON-004, REQ-003, REQ-004

| Key | Set by `init` flag | Read-time resolution | Notes |
|-----|--------------------|----------------------|-------|
| `language.output` | `--lang` (or selection / non-TTY default) | base; fallback for all others | sparse: written alone when only `--lang` given |
| `language.interaction` | `--interaction-lang` | `interaction` → `output` → `en` | overrides `output` when present (existing) |
| `language.document` | `--document-lang` | `document` → `output` → `en` | overrides `output` when present (existing) |
| `language.commit` | `--commit-lang` | `commit` → `output` → `en` (**NEW** fallback) | REQ-004 aligns with `commit-staged.md` |
| `language.templates` | — (always `en`) | — | not flag-settable |

## CLI Surface (init options)

**Covers**: REQ-001, REQ-002, REQ-006, REQ-011, NFR-002

New options (long-form only, Typer `typer.Option`, type `Optional[str]`, default `None`):

| Option | Maps to key | Validation |
|--------|-------------|------------|
| `--lang` / `-l` (existing) | `output` | `is_supported_language` else warn (DEC-003) |
| `--interaction-lang` (new) | `interaction` | same warn-not-error pattern |
| `--document-lang` (new) | `document` | same |
| `--commit-lang` (new) | `commit` | same |

Behavior contract: supplying any of these writes **only** its key and suppresses all language
prompts/confirms (REQ-006). `--lang` no longer fans out to the other three (REQ-002).

## Plan-Level Decisions

### PLD-1: Refactor `generate_config_content` to emit only specified keys (sparse)

**Context**: `generate_config_content(language="en", created=None)` (`i18n.py:228`) currently
writes all four language keys. REQ-002/CON-001 require `--lang` to produce a sparse config
(only `output`).

**Options Considered**:

1. New per-dimension signature: `generate_config_content(*, output=None, interaction=None,
   document=None, commit=None, created=None)`, emitting only non-`None` keys (plus `templates`,
   `version`, `project`); no-arg defaults to `output="en"`.
2. Keep `language=` and add a sparse boolean — rejected: two ways to express the same thing,
   error-prone.

**Decision**: Option 1.

**Rationale**: Smallest change that directly yields sparse output; `generate_config_content` is an
internal helper with one runtime caller (`__init__.py:642`) and five test call sites — all updated
under NFR-005.

**Covers**: REQ-002, REQ-005, CON-001, NFR-005
**Decision Level**: Plan-level technical decision; does not change confirmed product scope.
**Accepted trade-off**: Breaking signature change to an internal helper (tests updated, no external
consumers).

### PLD-2: Reuse `update_language_field` for surgical re-init writes

**Context**: REQ-005 requires that re-init change only the specified key(s). The `config` command
already does exactly this via `update_language_field(config_file, key, language)`
(`i18n.py:359`, used at `__init__.py:348, 367`).

**Decision**: Re-init writes loop over the resolved `{key: value}` map calling
`update_language_field` per key; fresh-init (no `config.yml`) uses the refactored
`generate_config_content` (PLD-1).

**Rationale**: Reuses an existing, already-tested helper; guarantees the same preservation
semantics as `config`; no new abstraction. (NFR-001)

**Covers**: REQ-005, REQ-013, NFR-001

### PLD-3: Reuse the `config` command's warn-not-error validation

**Context**: REQ-011/DEC-003 require unrecognized codes to warn and continue, consistent with
`config`.

**Decision**: For each new flag (and `--lang`), apply the existing pattern from
`__init__.py:337-347`: `normalized = normalize_locale(value)`; if
`not is_supported_language(normalized)`, print the same warning; proceed.

**Rationale**: Behavioral consistency between `init` and `config` (NFR-001); no new validation code.

**Covers**: REQ-011, NFR-001

### PLD-4: Resolve the language base after `target_dir`/config existence is known

**Context**: The selection prompt currently fires unconditionally when `--lang` is absent
(`__init__.py:482-494`), before `target_dir` is computed (`__init__.py:499`). REQ-007 requires the
prompt to be first-time-only and suppressed when `config.yml` already exists.

**Options Considered**:

1. Compute `target_dir` and `config_file` existence early (they depend only on `here`/
   `project_name`, available at function entry), then resolve the base per the flow in
   *Architecture Overview*.
2. Resolve lazily at config-write time — rejected: `normalized_lang` is consumed earlier by
   `translate()` in the migration/command-install messages (`__init__.py:589+`).

**Decision**: Option 1. `normalized_lang` stays available for all `translate()` calls; on
existing-config + no-flag, `normalized_lang` is taken from `get_interaction_language(config_file)`
for message language and no key is written.

**Rationale**: Satisfies REQ-007/REQ-008 while preserving message localization.

**Covers**: REQ-007, REQ-008, REQ-006

### PLD-5: Unify `--force` (suppress prompts; stop config regeneration)

**Context**: REQ-012 requires `--force` to auto-confirm the migration prompt (`__init__.py:594`)
and the two command-update prompts (`__init__.py:606, 613`); REQ-013 requires `--force` to stop
triggering full config regeneration (`__init__.py:641`).

**Decision**:

- Gate the three `Confirm.ask` calls as `if force or Confirm.ask(...)` so `--force` auto-proceeds.
- Change `__init__.py:641` from `if not config_file.exists() or force:` to
  `if not config_file.exists():` (config writes are surgical per PLD-2, so `--force` no longer
  regenerates).

**Rationale**: Removes the axis-A/axis-B split (DEC-008); `--force` becomes one predictable switch;
re-init becomes non-interactive when combined with language flags.

**Covers**: REQ-012, REQ-013, DEC-008, CON-005
**Accepted trade-off**: `--force` no longer resets `config.yml` to defaults — intentional per
CON-005; users wanting a reset edit/remove the file.

### PLD-6: Add two `translate()` message keys for notices

**Context**: REQ-009 (discoverability) and REQ-010 (key-write notice) need user-facing strings,
and `init` localizes all output via `translate(..., normalized_lang)`.

**Decision**: Add message keys (e.g. `cli.init.language_dimensions_hint` and
`cli.init.language_key_set`) to the translator source (`src/codexspec/translator.py`), mirroring
existing `cli.init.*` keys. The key-write notice lists each key and its value; it is printed via
`console.print` (dim) and never prompts.

**Rationale**: Keeps localization consistent with the rest of `init`; notices are non-blocking by
construction.

**Covers**: REQ-009, REQ-010

## Risks / Trade-offs

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| `generate_config_content` signature change breaks an overlooked caller | Low | Medium | Grep confirmed only `__init__.py:642` + tests call it; update all in Phase 5 |
| Existing `test_init_language.py` prompt tests assume unconditional prompting | High | Low | Update in Phase 5 (NFR-005); prompt is now first-time-only (PLD-4) |
| `--force` no longer regenerating config surprises a user expecting a reset | Low | Low | Intentional (CON-005); document in `--force` help text |
| Selection-prompt relocation changes message-language on re-init no-flag path | Low | Low | Use `get_interaction_language` for `normalized_lang` (PLD-4) |

## Implementation Phases

### Phase 1: i18n layer

- [ ] Refactor `generate_config_content` to per-dimension sparse signature (PLD-1).
- [ ] Add `output` fallback to `get_commit_language` (REQ-004); final default `"en"` when neither
      commit nor output is set (matches the existing accessor convention — stated as an Assumption
      in `spec.md`).
- [ ] Unit-test both: sparse emission per key; commit → output → en resolution.

**Covers**: REQ-002, REQ-003, REQ-004

### Phase 2: init CLI surface + base resolution

- [ ] Add `--interaction-lang` / `--document-lang` / `--commit-lang` options (long-only) to `init`
      (REQ-001, NFR-002).
- [ ] Implement flag→key resolution (no CLI precedence) and the first-time-only selection-prompt
      gating (PLD-4); non-TTY first-time default `en` (REQ-008).
- [ ] Apply warn-not-error validation per flag (PLD-3, REQ-011).
- [ ] With any flag supplied, no language prompt/confirm (REQ-006).

**Covers**: REQ-001, REQ-006, REQ-007, REQ-008, REQ-011, NFR-001, NFR-002

### Phase 3: Surgical config writes + notices

- [ ] Fresh init: emit only resolved keys via `generate_config_content` (PLD-1); re-init: per-key
      `update_language_field` (PLD-2); preserve all unspecified keys (REQ-005).
- [ ] Print the key-write non-blocking notice (REQ-010, PLD-6).
- [ ] After first-time interactive selection, print the per-dimension discoverability notice
      (REQ-009, PLD-6).

**Covers**: REQ-002, REQ-005, REQ-009, REQ-010

### Phase 4: Unify `--force`

- [ ] Gate the three `Confirm.ask` calls on `force` (PLD-5, REQ-012).
- [ ] Remove `or force` from the config regeneration condition (PLD-5, REQ-013).

**Covers**: REQ-012, REQ-013, DEC-008, CON-005

### Phase 5: Test updates + verification

- [ ] Update `tests/test_i18n.py::TestGenerateConfigContent` for the sparse shape/signature
      (NFR-005).
- [ ] Update `tests/test_init_language.py` prompt tests for first-time-only behavior; add tests for
      per-dimension flags, surgical preservation on re-init, non-interactive (non-TTY) runs, and
      `--force` prompt suppression (NFR-004, NFR-005).
- [ ] Verify backward compatibility: `init --lang zh-CN` resolves interaction/document/commit to
      zh-CN (REQ-014); determinism: same flags → same config (NFR-003).

**Covers**: REQ-014, NFR-003, NFR-004, NFR-005

## Verification Strategy

- **Unit (pytest)**: `generate_config_content` sparseness; `get_commit_language` fallback;
  `update_language_field` preservation; per-flag normalization + warn behavior.
- **Command-level (subprocess, non-TTY)**:
  - `init proj --interaction-lang en --document-lang zh-CN --commit-lang en` → exit 0, no prompt,
    exactly those three keys (SC-001).
  - `init proj --lang zh-CN` → sparse config, resolved languages all zh-CN (SC-002, REQ-014).
  - Re-init with one flag → only that key changes, others byte-identical (SC-003).
  - `init . --force <flags>` on an existing project → exit 0, zero prompts (SC-004).
- **Existing suite**: `uv run pytest tests/test_i18n.py tests/test_init_language.py`; then full
  `uv run pytest`; `uv run ruff check src/`.

## Requirements Coverage

| Spec Requirement | Plan Coverage | Reference |
|------------------|---------------|-----------|
| REQ-001 | Full | CLI Surface / PLD-3 / Phase 2 |
| REQ-002 | Full | PLD-1 / Phase 1, 3 |
| REQ-003 | Full | Data Model / Phase 1 (existing resolution retained) |
| REQ-004 | Full | PLD-1 (commit fallback) / Phase 1 |
| REQ-005 | Full | PLD-2 / Phase 3 |
| REQ-006 | Full | PLD-4 / Phase 2 |
| REQ-007 | Full | PLD-4 / Phase 2 |
| REQ-008 | Full | PLD-4 / Phase 2 |
| REQ-009 | Full | PLD-6 / Phase 3 |
| REQ-010 | Full | PLD-6 / Phase 3 |
| REQ-011 | Full | PLD-3 / Phase 2 |
| REQ-012 | Full | PLD-5 / Phase 4 |
| REQ-013 | Full | PLD-5 / Phase 4 |
| REQ-014 | Full | Phase 5 (verification) |
| NFR-001 | Full | PLD-2, PLD-3 (reuse helpers/patterns) |
| NFR-002 | Full | CLI Surface / Phase 2 |
| NFR-003 | Full | Phase 5 (determinism check) |
| NFR-004 | Full | Phase 5 (subprocess non-TTY tests) |
| NFR-005 | Full | Phase 5 (test updates + new coverage) |

## Assumptions

- `get_commit_language`, when neither `commit` nor `output` is set, resolves to `"en"` — the same
  final default the other accessors use (extends DEC-005; stated in `spec.md`). Not converted into
  a requirement.
- The existing `prompt_language_selection` label ("Select output language") remains accurate since
  the selection sets the `output` base; only the surrounding gating and the added discoverability
  notice change.
