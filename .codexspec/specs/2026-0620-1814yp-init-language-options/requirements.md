# Confirmed Requirements: init-language-options

<!--
Language: Maintain this document in the language specified in .codexspec/config.yml.
This file is the authoritative, persistent record of user-confirmed intent.
Do not copy the full conversation. Keep only confirmed decisions and short evidence
quotes needed to resolve later interpretation disputes.
-->

**Feature ID**: `2026-0620-1814yp`
**Status**: Confirmed
**Last Confirmed**: 2026-06-20

## Authority Rules

- Only entries with `Status: confirmed` are binding downstream inputs.
- `open` entries MUST NOT be converted into confirmed product requirements.
- Replaced entries remain in this file with `Status: superseded` and a link to the replacement.
- AI inferences must be labeled as assumptions and require user confirmation before becoming binding.

## Scope Summary

Extend the `codexspec init` command so each of the four language dimensions —
`output` (legacy base), `interaction`, `document`, `commit` — can be set independently
from the command line, and so `init` can run fully non-interactively when language values
are supplied via flags. The `config` command already exposes the four setters and is
unchanged; this work brings `init` to the same model.

## Needs

### NEED-001: Independent CLI control of each language dimension in `init`

- **Status**: confirmed
- **Statement**: `init` gains CLI options to control the interaction, document, and commit
  languages separately. Today `init` only has `--lang`, which forces all language dimensions
  to a single value.
- **Rationale**: The language configuration already supports four independent keys
  (`interaction` / `document` / `output` / `commit`), but `init` cannot set them
  independently, so the per-dimension control is unreachable at project-creation time.
- **User Evidence**: "The language settings can already control interaction / document /
  commit languages separately, but there are no corresponding command-line options; extend
  `init` for this."
- **Confirmed At**: 2026-06-20

### NEED-002: Fully non-interactive `init` for AI agents and tests

- **Status**: confirmed
- **Statement**: `init` must be completable end-to-end with zero language-related prompts
  when language values are supplied via flags, so AI agents and test cases can set every
  language dimension in one shot through parameters alone.
- **Rationale**: Programmatic / CI use cannot answer interactive prompts; the language
  selection prompt and any confirmation dialogs currently block non-interactive runs.
- **User Evidence**: "Achieve non-interactive initialization, convenient for program testing
  ... so AI agents or test cases can complete all settings in one shot via parameters."
- **Confirmed At**: 2026-06-20

### NEED-003: `--lang` stays convenient as the base language

- **Status**: confirmed
- **Statement**: `--lang` remains a single, easy shortcut for human users: it sets the
  `output` base language, and any dimension not explicitly overridden follows it via the
  existing fallback.
- **Rationale**: The common case ("I want everything in one language") should stay a single
  flag.
- **User Evidence**: "`--lang` should only set the output field; the other dimensions follow
  it via fallback."
- **Confirmed At**: 2026-06-20

## Constraints

### CON-001: Backward compatibility is functional equivalence, not byte-identical files

- **Status**: confirmed
- **Statement**: `codexspec init <proj> --lang zh-CN` must keep producing zh-CN as the
  effective language for interaction, document, and commit. The generated `config.yml`
  becomes sparse (writes only `output` rather than all four keys); tests that assert the
  presence of the now-omitted keys must be updated.
- **User Evidence**: "As long as output-only is sufficient (via fallback), `--lang` only
  needs to set output." (accepted the sparse-config consequence)
- **Confirmed At**: 2026-06-20

### CON-002: Scope is limited to the `init` command

- **Status**: confirmed
- **Statement**: Only `init` is changed. The `config` command already exposes
  `--set-lang` / `--set-interaction-lang` / `--set-document-lang` / `--set-commit-lang` and
  is not modified by this work (consistency with it is a goal, not a change to it).
- **User Evidence**: The gap identified is specifically "`init` has no corresponding
  command-line options"; `config` already has them.
- **Confirmed At**: 2026-06-20

### CON-003: No new global non-interactive flag

- **Status**: confirmed
- **Statement**: No new global `--non-interactive` / `--yes` switch is introduced. Language
  flags suppress only language-related prompts (the selection prompt). `init`'s other
  confirmation prompts (migration, command-update) are suppressed via the existing `--force`
  flag — not via language flags and not via a new global switch (see CON-005 / DEC-008).
- **User Evidence**: User selected the language-only suppression option and declined a
  dedicated global `--non-interactive` flag, later choosing to extend `--force` instead.
- **Confirmed At**: 2026-06-20

### CON-004: The `config.yml` key set is unchanged

- **Status**: confirmed
- **Statement**: No new keys are added or removed from `config.yml`. The recognized
  language keys remain `interaction` / `document` / `output` / `commit` / `templates`.
- **Confirmed At**: 2026-06-20

### CON-005: `--force` is a unified "overwrite + don't ask" switch (axes A and B)

- **Status**: confirmed
- **Statement**: `--force` covers both of `init`'s overwrite axes. (A) File overwrite: it
  allows initializing into an already-existing directory and overwrites existing files
  (e.g. CLAUDE.md — pre-existing axis-A behavior, unchanged here); config writes remain
  surgical (per flag → key) and preserve any language key the user did not specify, so
  `--force` no longer triggers full `config.yml` regeneration. (B) Prompt suppression:
  `--force` auto-confirms `init`'s confirmation prompts — the old-structure migration prompt
  and the command-update prompt — so they do not block. (The CLAUDE.md compliance prompt is
  already unreachable under `--force`, because `--force` regenerates CLAUDE.md.) Net effect:
  `init --force <language flags>` runs fully non-interactively even on an already-initialized
  project.
- **Rationale**: Removes the prior inconsistency where `--force` silently overwrote
  config/CLAUDE.md but still prompted for command overwrites; makes the flag match the
  universal "force = overwrite and don't ask" expectation; gives a non-interactive re-init
  path without adding a new flag.
- **User Evidence**: "Confirmed: `--force` no longer triggers full regeneration"; later,
  after reviewing that `--force` had only covered axis A: "Unify; fold the migration prompt
  into `--force` too."
- **Confirmed At**: 2026-06-20

## Decisions

### DEC-001: Four independent flag → key mapping (mirrors `config`)

- **Status**: confirmed
- **Decision**: Each flag maps to exactly one config key, with no CLI-level precedence or
  override logic: `--lang` → `output`, `--interaction-lang` → `interaction`,
  `--document-lang` → `document`, `--commit-lang` → `commit`. `output` is the base; the
  other three override it at read time via the existing fallback chain. This makes `init`
  consistent with the existing `config` command (where `--set-lang` sets `output`).
- **Alternatives Rejected**: Layered override model (rejected) — `--lang` would have been a
  CLI-time base fanned out to all dimensions with the three flags overriding it, and `init`
  would write resolved concrete values. Rejected because it introduces CLI precedence rules
  and is inconsistent with `config`'s "one flag = one key" behavior.
- **Reason**: Simplest CLI semantics; stable `--lang` meaning (= `output`); reuses the
  existing fallback infrastructure; aligns `init` with `config`.
- **User Evidence**: "`--lang` should only set the output field; 4 language params each
  independently set one of the 4 language config items." User chose "4-independent mapping
  (recommended)" over the layered model.
- **Confirmed At**: 2026-06-20

### DEC-002: The only language interaction is the selection prompt, shown only when the base is undeterminable

- **Status**: confirmed
- **Decision**: The interactive language selection prompt appears only on **first-time
  initialization** (no `config.yml` exists yet) when the `output` base cannot be determined
  — i.e. `--lang` is not given AND the three specific flags are not all given AND stdin is
  a TTY; the chosen value is written to `output`. If `config.yml` already exists and no
  language flag is given, **no prompt is shown and all language keys are preserved
  unchanged** (per CON-005). In a first-time non-TTY run with no determinable base,
  `output` defaults to `en`. Whenever any language flag is supplied, no confirmation dialogs
  of any kind are shown (the four-independent model has no fan-out, hence no conflicts to
  confirm).
- **Alternatives Rejected**: Keeping a per-setting confirmation dialog when only `--lang` is
  passed (rejected) — that dialog existed only because the layered model fanned `--lang` out
  and could clash with existing per-dimension values; under the four-independent model
  `--lang` only touches `output`, so there is nothing to confirm.
- **Reason**: Deterministic, prompt-free behavior whenever the caller supplies flags; this
  is the contract automation relies on.
- **User Evidence**: "Only by fully providing the three specific language settings can the
  selection prompt be skipped ... so AI agents or test cases can complete all settings in
  one shot via parameters." (Refined under the four-independent model: any flag suppresses
  prompts.)
- **Confirmed At**: 2026-06-20

### DEC-003: Unrecognized language codes warn, never error

- **Status**: confirmed
- **Decision**: A language code that is not in the commonly-supported list is still
  accepted (Claude may support it); `init` prints a warning and continues, matching the
  existing `config` command behavior.
- **User Evidence**: User selected "warn, do not error (recommended)".
- **Confirmed At**: 2026-06-20

### DEC-004: Non-blocking notice on language-key writes

- **Status**: confirmed
- **Decision**: When `init` writes or overwrites a language key, it prints a single
  non-blocking notice line stating which key(s) were set and to what value (including when
  an existing value is overwritten). This is informational output only — it never prompts
  and never blocks.
- **Alternatives Rejected**: A blocking confirmation prompt before overwriting (rejected) —
  it would break the deterministic, prompt-free path required by NEED-002.
- **Reason**: Preserves determinism for automation while keeping changes observable for
  humans and parseable for agents/tests.
- **User Evidence**: "I don't mean a confirmation prompt for the user to confirm — I mean
  adding notice text in the terminal output so the user can directly observe the changes."
- **Confirmed At**: 2026-06-20

### DEC-005: Align `get_commit_language` to fall back to `output`

- **Status**: confirmed
- **Decision**: `get_commit_language` is changed to fall back to `output` when `commit` is
  absent, matching the behavior already encoded in the `commit-staged.md` template
  ("If `language.commit` is set, use it; otherwise use `language.output` as fallback").
- **Reason**: Closes a pre-existing inconsistency (interaction/document fall back to
  `output` in Python, but commit did not), and makes `output` the true base for all four
  dimensions — which is what allows `--lang` (→ `output`) alone to set the default commit
  language.
- **User Evidence**: Derived from confirming that `--lang` (= `output`) should suffice as
  the base for every dimension.
- **Confirmed At**: 2026-06-20

### DEC-006: The three new flags are long-option only

- **Status**: confirmed
- **Decision**: `--interaction-lang`, `--document-lang`, and `--commit-lang` are provided
  as long options only, with no short aliases. `--lang` / `-l` is unchanged.
- **Reason**: Avoids collision with the existing `-l` (`--lang`) and keeps the option set
  uncluttered; the common case is the single `--lang` flag.
- **User Evidence**: User selected "long options only (recommended)".
- **Confirmed At**: 2026-06-20

### DEC-007: First-time interactive selection is single-base, with a discoverability notice

- **Status**: confirmed
- **Decision**: The first-time interactive flow uses a single base-language selection (the
  chosen language is written to `output`; the other dimensions follow it via fallback).
  Immediately after, `init` prints a short informational notice telling the user that
  interaction, document, and commit languages can be controlled separately via the
  `--interaction-lang` / `--document-lang` / `--commit-lang` flags (or the `config`
  command), so the per-dimension mechanism is discoverable rather than hidden.
- **Alternatives Rejected**: (a) Prompting for all four languages on first init (rejected)
  — excessive friction for the common "one language everywhere" case and inconsistent with
  the `--lang` shortcut. (b) A hybrid base-then-optional-refinement prompt (rejected) — adds
  a conditional dialog branch for little gain over the explicit flag-based path.
- **Reason**: Minimal friction for the majority while still making the per-dimension
  capability visible to users who would otherwise never learn it exists.
- **User Evidence**: "Use the recommended single base-language selection, but print a notice
  reminding users they can control languages separately via the multi-language options, so
  they aren't unaware of this mechanism."
- **Confirmed At**: 2026-06-20

### DEC-008: Unify `--force` to cover both overwrite axes (A + B)

- **Status**: confirmed
- **Decision**: `--force` is extended from axis A only (file overwrite) to also cover axis B
  (suppressing `init`'s confirmation prompts: migration + command-update). With this,
  `--force` is a single, predictable "overwrite and don't ask" switch, and
  `init --force <language flags>` is fully non-interactive on existing projects.
- **Alternatives Rejected**: (a) Keep the split (`--force` = axis A only, prompts still
  fire) — rejected as internally inconsistent: `--force` already silently overwrote
  config/CLAUDE.md, so prompting only for command overwrites had no principled basis and
  contradicted the name "force". (b) Add a separate global `--non-interactive` / `--yes`
  flag — rejected by CON-003; the existing `--force` already conveys the intent and avoids
  flag proliferation.
- **Reason**: One unified switch; satisfies NEED-002 for re-init; resolves OPEN-001 without
  a new flag.
- **User Evidence**: Asked "Is the design where `--force` only handles axis A reasonable?";
  after discussion, chose to unify, including the migration prompt.
- **Confirmed At**: 2026-06-20

## Out of Scope

### OUT-001: A separate global `--non-interactive` / `--yes` flag

- **Status**: confirmed
- **Statement**: Introducing a NEW global `--non-interactive` / `--yes` switch is out of
  scope. Non-interactive re-init is achieved instead by the unified `--force` (see
  CON-005 / DEC-008), which suppresses `init`'s confirmation prompts without adding a flag.
- **Reason**: Avoid flag proliferation; `--force` already conveys the needed intent.
- **User Evidence**: User declined a dedicated global non-interactive flag; chose to extend
  `--force` instead.
- **Confirmed At**: 2026-06-20

## Open Questions

### OPEN-001: re-init confirmation prompts (RESOLVED)

- **Status**: resolved (by DEC-008 / CON-005)
- **Why It Matters**: Originally flagged that re-`init` on an existing project could still
  surface the command-update (and migration) confirmation prompts, which would block
  non-interactive runs.
- **Resolution**: Resolved by unifying `--force` to suppress those prompts —
  `init --force <language flags>` is now fully non-interactive on existing projects.
- **Owner**: User (resolved 2026-06-20)

## Superseded Entries

<!-- No persisted entries have been superseded. The earlier "layered override" model was
proposed during discovery but replaced by DEC-001 (four-independent mapping) before any
entry was written to this file, so it is recorded only as a rejected alternative under
DEC-001, not as a superseded entry. -->

## Confirmation Log

### Session 2026-06-20

- **Summary Presented**: Final Model B (four-independent flag→key mapping) decision set
  covering: NEED-001..003, CON-001..005, DEC-001..006, OUT-001, and the non-blocking
  OPEN-001. Key points confirmed across the session: (1) `--lang`→`output` with each
  specific flag mapping to its own key, mirroring `config`; (2) the only language prompt is
  the selection prompt, shown only when the base is undeterminable; (3) unrecognized codes
  warn, never error; (4) a non-blocking notice (not a confirmation) on writes; (5)
  `get_commit_language` aligned to fall back to `output`; (6) new flags are long-option
  only; (7) `--force` no longer regenerates config and unspecified language keys are always
  preserved.
- **User Confirmation**: Each decision was confirmed explicitly, including the
  `--force` behavior ("Confirmed: `--force` no longer triggers full regeneration") and the
  preservation guarantee for unspecified language keys on re-init. Follow-up in the same
  session refined DEC-002 (selection prompt is first-time-only; an existing `config.yml`
  with no language flag is left untouched) and added DEC-007 (first-time single-base
  selection plus a discoverability notice for the per-dimension flags). A further
  refinement upgraded CON-005 and added DEC-008: `--force` is unified to cover both
  overwrite axes (file overwrite + suppression of the migration / command-update
  confirmation prompts), which resolves OPEN-001.
- **Entries Confirmed**: NEED-001, NEED-002, NEED-003, CON-001, CON-002, CON-003, CON-004,
  CON-005, DEC-001, DEC-002, DEC-003, DEC-004, DEC-005, DEC-006, DEC-007, DEC-008, OUT-001
- **Open (non-blocking)**: none — OPEN-001 resolved by DEC-008 / CON-005
