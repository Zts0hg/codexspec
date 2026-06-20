# Feature Specification: init-language-options

<!--
Language: Generate this document in the language specified in .codexspec/config.yml
If not configured, use English.
-->

**Feature Branch**: `2026-0620-1814yp-init-language-options`
**Created**: 2026-06-20
**Status**: Draft
**Input**: User description: "The project's language settings already control interaction / document / commit languages separately, but `init` has no corresponding command-line options. Extend `init` so users — and AI agents / tests — can set each dimension independently and non-interactively."

## Context

`codexspec` stores four independent language dimensions in `.codexspec/config.yml` under the
`language:` block: `output` (legacy base), `interaction`, `document`, and `commit` (plus
`templates`, always `en`). The per-project `config` command already exposes four setters
(`--set-lang`, `--set-interaction-lang`, `--set-document-lang`, `--set-commit-lang`), each
writing exactly one key.

The `init` command has **not** kept up. Today `init` exposes only `--lang` / `-l`, which is
treated as a single "output language" and — via `generate_config_content` — is written to
**all four** keys at once. There is no way to create a project whose interaction, document,
and commit languages differ. Additionally, `init` is not reliably non-interactive: in a TTY
with no `--lang` it shows a numbered language-selection prompt, and on re-init it can raise
confirmation dialogs, both of which block programmatic / CI use.

This specification brings `init` to the same "one flag = one key" model as `config`, and
makes flag-driven initialization fully non-interactive.

Affected components (verified repository facts, for context only — not implementation
prescription): the `init` command in `src/codexspec/__init__.py`; the i18n helpers
`generate_config_content`, `CONFIG_TEMPLATE`, `_resolve_language`, `get_interaction_language`,
`get_document_language`, `get_commit_language`, `update_language_field`, and `normalize_locale`
in `src/codexspec/i18n.py`; `should_update_commands` and `install_commands_to_subdir` in
`src/codexspec/commands/installer.py`; and the fallback wording in the
`templates/commands/commit-staged.md` template.

## Goals

- Let `init` set each of the four language dimensions independently from the command line.
- Make `init` fully non-interactive whenever language values are supplied via flags, so AI
  agents and automated tests can configure everything in one shot.
- Keep `--lang` as a convenient single-value shortcut for the common "one language
  everywhere" case.
- Make `init`'s language semantics consistent with the existing `config` command.
- Make `--force` a single, predictable "overwrite and don't ask" switch.

## Non-Goals

- Changing the `config` command (it already exposes the four setters).
- Adding or removing keys in `config.yml`.
- Introducing a new global `--non-interactive` / `--yes` flag.
- Suppressing `init`'s non-language prompts via language flags (that is `--force`'s job).

## User Scenarios & Testing

### User Story 1 - Set all language dimensions non-interactively (Priority: P1)

As an AI agent or test harness, I want to create a project with interaction, document, and
commit languages each specified explicitly on the command line, so that I can configure
everything in a single, deterministic invocation with no prompts.

**Why this priority**: This is the core gap — per-dimension control did not exist at
`init` time, and non-interactive use was blocked. It is independently shippable and delivers
the headline value.

**Independent Test**: Run `codexspec init proj --interaction-lang en --document-lang zh-CN
--commit-lang en` in a non-TTY subprocess and assert exit code 0, no prompt, and a
`config.yml` whose resolved languages match exactly.

**Acceptance Scenarios**:

1. **Given** an empty target directory and a non-TTY stdin, **When** I run `codexspec init
   proj --interaction-lang en --document-lang zh-CN --commit-lang en`, **Then** the command
   exits 0 with no interactive prompt and writes `interaction: "en"`, `document: "zh-CN"`,
   `commit: "en"` to `config.yml`.
2. **Given** the project from scenario 1, **When** the language accessors resolve each
   dimension, **Then** interaction resolves to `en`, document to `zh-CN`, and commit to `en`
   (explicit keys take precedence over `output`).

---

### User Story 2 - Set a single base language quickly (Priority: P1)

As a developer, I want `codexspec init proj --lang zh-CN` to set my project's default
language in one flag, so that interaction, document, and commit all default to that language
without me specifying each one.

**Why this priority**: The common case ("one language everywhere") must stay a single flag;
breaking it would regress the primary human workflow.

**Independent Test**: Run `codexspec init proj --lang zh-CN` (non-TTY) and assert the
resolved interaction, document, and commit languages are all `zh-CN`.

**Acceptance Scenarios**:

1. **Given** an empty target directory, **When** I run `codexspec init proj --lang zh-CN`,
   **Then** `config.yml` contains `output: "zh-CN"` and the resolved interaction, document,
   and commit languages are all `zh-CN` (via the `output` fallback chain).
2. **Given** the project from scenario 1, **When** I inspect `config.yml`, **Then** it is
   sparse — it does **not** contain explicit `interaction`, `document`, or `commit` keys.

---

### User Story 3 - Change one dimension without losing the others (Priority: P2)

As a developer, I want to re-run `init` to change a single language dimension (e.g.,
`--commit-lang en`) and have all my other language settings preserved exactly, so that
re-initialization never silently overwrites settings I did not ask to change.

**Why this priority**: Guarantees data preservation on re-init; directly enables safe
scripted re-configuration.

**Independent Test**: Seed a `config.yml` with all four keys, run `codexspec init .
--document-lang ja`, and assert only the `document` key changed and the other three are
byte-identical.

**Acceptance Scenarios**:

1. **Given** an existing project whose `config.yml` sets all four language keys, **When** I
   run `codexspec init . --document-lang ja`, **Then** only `document` becomes `ja`;
   `interaction`, `commit`, and `output` are unchanged.
2. **Given** an existing project with a `config.yml`, **When** I run `codexspec init .`
   with **no** language flag, **Then** no language prompt is shown and no language key is
   modified.

---

### User Story 4 - First-time user picks a language and learns about per-dimension control (Priority: P2)

As a first-time user running `init` interactively, I want to pick one language quickly and
then be told that I can control interaction, document, and commit separately, so that I am
not unaware of the per-dimension capability.

**Why this priority**: Preserves low-friction onboarding while making the advanced capability
discoverable.

**Independent Test**: Run `init` in a TTY with no flags, select a language, and assert the
chosen language is written to `output` and an informational notice about the three flags is
printed.

**Acceptance Scenarios**:

1. **Given** a first-time init (no `config.yml`) in a TTY with no language flags, **When**
   the user selects a language from the prompt, **Then** that value is written to `output`
   and the other dimensions follow it via fallback.
2. **Given** the same flow, **When** selection completes, **Then** `init` prints a
   non-blocking notice that interaction/document/commit can be set separately via
   `--interaction-lang` / `--document-lang` / `--commit-lang` (or the `config` command).

---

### User Story 5 - Force a fully non-interactive re-init (Priority: P3)

As a developer or agent, I want `codexspec init . --force <language flags>` to re-initialize
an existing project end-to-end with zero prompts, so that re-init is scriptable.

**Why this priority**: Completes the non-interactive story for the re-init case; depends on
the unified `--force` behavior.

**Independent Test**: Initialize a project, then run `codexspec init . --force
--interaction-lang en --document-lang en --commit-lang en` in a TTY and assert exit 0 with
no confirmation prompts.

**Acceptance Scenarios**:

1. **Given** an already-initialized project, **When** I run `codexspec init . --force
   --interaction-lang en --document-lang en --commit-lang en`, **Then** the command completes
   with no confirmation prompts (migration and command-update dialogs are auto-confirmed).
2. **Given** the same invocation, **When** it finishes, **Then** the three supplied language
   keys are written and no other language key is destroyed by full-config regeneration.

---

### Edge Cases

- **Unrecognized language code** (e.g., `--interaction-lang xx`): `init` accepts it, prints a
  warning that it is not in the commonly-supported list, and continues (no hard error).
- **Mixed flags** (e.g., `--lang zh-CN --commit-lang en`): each flag writes its own key
  independently — `output: zh-CN`, `commit: en`; `interaction` and `document` are absent and
  fall back to `output`.
- **First-time init, non-TTY, no flags**: `output` defaults to `en` with no prompt.
- **Ctrl+C during the selection prompt**: existing behavior is retained (falls back to the
  default language); not changed by this feature.
- **`--force` overwrites CLAUDE.md**: this is pre-existing axis-A behavior and remains; it is
  noted here as a known destructive consequence but is out of scope to change.

## Requirements

### Functional Requirements

- **REQ-001**: `init` MUST accept three new language options — `--interaction-lang`,
  `--document-lang`, and `--commit-lang` — as long-form options only (no short aliases).
  Each option MUST map to exactly one `config.yml` key (`interaction`, `document`, `commit`
  respectively) and MUST be independent of the others, with no CLI-level precedence between
  them.
  - Sources: NEED-001, DEC-001, DEC-006

- **REQ-002**: `--lang` MUST set only the `output` key. It MUST NOT write or overwrite the
  `interaction`, `document`, or `commit` keys.
  - Sources: NEED-003, DEC-001, CON-001

- **REQ-003**: Language resolution at read time MUST follow the fallback chain: for each of
  `interaction`, `document`, and `commit`, an explicitly set key takes precedence over
  `output`; an absent key falls back to `output`; an absent `output` defaults to `en`.
  - Sources: DEC-001, NEED-003

- **REQ-004**: `get_commit_language` MUST fall back to `output` when `commit` is absent
  (matching the fallback already documented in `commit-staged.md`), so that `output` is the
  base for all four dimensions.
  - Sources: DEC-005

- **REQ-005**: When any language flag is supplied, `init` MUST write only the corresponding
  key(s) and MUST preserve every other existing language key unchanged (surgical update).
  This MUST hold both for fresh init and re-init, and regardless of `--force`.
  - Sources: DEC-001, CON-005, CON-001

- **REQ-006**: Whenever any language flag is supplied, `init` MUST NOT display any language
  confirmation dialog; the run MUST be completable end-to-end with no language prompts.
  - Sources: NEED-002, DEC-002

- **REQ-007**: The interactive language selection prompt MUST be shown only when ALL of the
  following hold: (a) it is a first-time init (no `config.yml` exists yet), (b) `--lang` is
  not given, (c) the three specific flags are not all given, and (d) stdin is a TTY. When a
  `config.yml` already exists and no language flag is given, `init` MUST NOT prompt and MUST
  leave all language keys unchanged.
  - Sources: DEC-002, CON-005

- **REQ-008**: On a first-time init in a non-TTY context with no determinable base language,
  `init` MUST set `output` to `en` without prompting.
  - Sources: DEC-002, NEED-002

- **REQ-009**: After a first-time interactive single-base selection, `init` MUST print one
  non-blocking informational notice stating that `interaction`, `document`, and `commit` can
  be controlled separately via `--interaction-lang` / `--document-lang` / `--commit-lang` (or
  the `config` command). The notice MUST NOT prompt or block.
  - Sources: DEC-007

- **REQ-010**: Whenever `init` writes or overwrites a language key, it MUST print a single
  non-blocking notice line stating which key(s) were set and to what value (including when an
  existing value is overwritten). The notice MUST NOT prompt or block.
  - Sources: DEC-004

- **REQ-011**: A language code that is not in the commonly-supported list MUST be accepted;
  `init` MUST print a warning and continue rather than failing. This MUST be consistent with
  the `config` command's behavior.
  - Sources: DEC-003

- **REQ-012**: `--force` MUST auto-confirm `init`'s confirmation prompts — specifically the
  old-structure migration prompt and the command-update prompt — so they do not block. In
  combination with language flags, `codexspec init --force <language flags>` MUST run fully
  non-interactively, including on an already-initialized project.
  - Sources: DEC-008, CON-005, NEED-002

- **REQ-013**: `--force` MUST NOT trigger full `config.yml` regeneration. Config writes MUST
  remain surgical (per flag → key) and MUST preserve any language key the user did not
  specify.
  - Sources: CON-005, CON-001

- **REQ-014**: `codexspec init <proj> --lang zh-CN` MUST keep producing `zh-CN` as the
  effective (resolved) language for interaction, document, and commit, even though the
  generated `config.yml` is sparse (only `output`).
  - Sources: CON-001, NEED-003, DEC-005

### Non-Functional Requirements

- **NFR-001**: Language code normalization, validation, and the supported-language set MUST
  be shared with the `config` command (reuse `normalize_locale` / `is_supported_language`)
  so that `init` and `config` behave identically for the same code.
  - Sources: DEC-001, DEC-003, CON-002

- **NFR-002**: The new options MUST be declared with Typer using the same conventions as the
  existing `--lang` option (absolute imports, type hints, help text), long-form only.
  - Sources: DEC-006

- **NFR-003**: The flag-driven path MUST be deterministic and reproducible — identical flags
  MUST produce identical `config.yml` language content with no state-dependent prompts.
  - Sources: NEED-002, DEC-002, DEC-008

- **NFR-004**: The non-interactive path MUST be exercisable by subprocess-based tests without
  a TTY (stdin not a TTY): the command MUST terminate with a defined exit code (0 on success)
  and MUST NOT hang waiting for input.
  - Sources: NEED-002

- **NFR-005**: Existing tests that assert the old "all four keys present" config shape MUST
  be updated for the sparse (`output`-only) shape produced by `--lang`; new tests MUST cover
  per-dimension flags, surgical preservation on re-init, the non-interactive paths, and
  `--force` prompt suppression.
  - Sources: CON-001, NEED-002

### Key Entities

- **`language.output`**: the base/default language. Set by `--lang` or the interactive
  selection. Acts as the fallback for every other dimension.
- **`language.interaction`**: language for user↔LLM conversation and CLI terminal output.
  Set by `--interaction-lang`; overrides `output` when present.
- **`language.document`**: language for generated artifact files. Set by `--document-lang`;
  overrides `output` when present.
- **`language.commit`**: language for git commit messages. Set by `--commit-lang`; overrides
  `output` when present (REQ-004 adds the `output` fallback).
- **`language.templates`**: always `en`; not user-settable via these flags.

## Success Criteria

### Measurable Outcomes

- **SC-001**: `codexspec init proj --interaction-lang en --document-lang zh-CN --commit-lang en`
  in a non-TTY exits 0 with no prompt and writes exactly those three keys (plus `templates`).
- **SC-002**: `codexspec init proj --lang zh-CN` produces a `config.yml` whose resolved
  interaction, document, and commit languages are all `zh-CN` (functional equivalence to
  today).
- **SC-003**: Re-running `init` with a single dimension flag changes only that key; the other
  language keys are byte-identical before and after.
- **SC-004**: `codexspec init . --force <language flags>` on an existing project exits 0 with
  zero confirmation prompts.
- **SC-005**: All pre-existing `init` language tests pass after their assertions are updated
  for the sparse-config shape; new tests cover the per-dimension, preservation,
  non-interactive, and `--force` paths.

## Constraints

- Backward compatibility is defined as **functional equivalence**, not byte-identical
  `config.yml` files (CON-001).
- Scope is limited to the `init` command; `config` is unchanged (CON-002).
- No new global `--non-interactive` / `--yes` flag is introduced (CON-003, OUT-001).
- The `config.yml` key set is unchanged: `interaction` / `document` / `output` / `commit` /
  `templates` (CON-004).
- `--force` is a unified "overwrite + don't ask" switch covering both file overwrite and
  prompt suppression (CON-005, DEC-008).

## Assumptions

- When neither `commit` nor `output` is set, `get_commit_language` resolves to `en`, matching
  the default the other accessors already use (consistent with REQ-003/REQ-004). This extends
  DEC-005's "fall back to `output`" with the same final default and does not change product
  intent.
- The existing command-install and migration code paths remain structurally as-is; only their
  prompt gating under `--force` changes (per REQ-012).

## Dependencies

- `src/codexspec/i18n.py` helpers (`generate_config_content`, `CONFIG_TEMPLATE`,
  `_resolve_language`, `get_commit_language`, `update_language_field`, `normalize_locale`).
- `src/codexspec/commands/installer.py` (`should_update_commands`,
  `install_commands_to_subdir`) — only for the `--force` prompt-suppression behavior.
- The fallback wording in `templates/commands/commit-staged.md` (the reference behavior
  REQ-004 aligns to).

## Out of Scope

- **A new global `--non-interactive` / `--yes` flag** (OUT-001): non-interactive re-init is
  achieved via the unified `--force` instead.
- **Changing the `config` command**: it already exposes the four setters.
- **Suppressing non-language prompts via language flags**: that is `--force`'s role, not the
  language flags'.
- **Revisiting `--force`'s CLAUDE.md overwrite** (axis A): pre-existing behavior, unchanged.

## Open Questions

- **OPEN-001 (resolved)**: Re-init could previously surface the command-update / migration
  confirmation prompts, blocking non-interactive runs. Resolved by DEC-008 / CON-005:
  `--force` now suppresses those prompts. No blocking open items remain.

## Requirements Traceability

| Confirmed Requirement | Spec Coverage | Notes |
|-----------------------|---------------|-------|
| NEED-001 | REQ-001, REQ-002 | Per-dimension flags added to `init` |
| NEED-002 | REQ-006, REQ-008, REQ-012, NFR-003, NFR-004 | Fully non-interactive init |
| NEED-003 | REQ-002, REQ-003, REQ-014 | `--lang` stays the easy base shortcut |
| CON-001 | REQ-002, REQ-005, REQ-013, REQ-014, NFR-005 | Functional equivalence; sparse config |
| CON-002 | NFR-001 | Scope = `init`; consistency with `config` |
| CON-003 | REQ-012, Out of Scope (OUT-001) | No new global flag |
| CON-004 | REQ-001, REQ-002, Key Entities | Key set unchanged |
| CON-005 | REQ-005, REQ-007, REQ-012, REQ-013 | Unified `--force` |
| DEC-001 | REQ-001, REQ-002, REQ-003, REQ-005 | Four-independent flag→key mapping |
| DEC-002 | REQ-006, REQ-007, REQ-008 | Selection prompt only when base undeterminable |
| DEC-003 | REQ-011, NFR-001 | Unrecognized codes warn, never error |
| DEC-004 | REQ-010 | Non-blocking write notice |
| DEC-005 | REQ-004 | `get_commit_language` → `output` fallback |
| DEC-006 | REQ-001, NFR-002 | New flags are long-option only |
| DEC-007 | REQ-009 | First-time single-base selection + discoverability notice |
| DEC-008 | REQ-012 | Unified `--force` (axes A + B) |
| OUT-001 | Out of Scope | No new global non-interactive flag |
| OPEN-001 | Open Questions (resolved) | Resolved by DEC-008 / CON-005; not a requirement |
