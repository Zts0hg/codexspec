# Design Document: profile-filename-readability

**Related Spec**: `.codexspec/specs/2026-0907-1623rh-profile-filename-readability/spec.md`
**Confirmed Requirements**: `.codexspec/specs/2026-0907-1623rh-profile-filename-readability/requirements.md`
**Created**: 2026-09-07
**Status**: Draft

## Context

`/codexspec:distill` stores each reusable-knowledge record as one file under `.codexspec/profile/<category>/`, named today by the bare record id (`{type}-{feature-id}-{seq}.md`, e.g. `P-2026-0902-054178-4.md`). The id is unique by construction but carries no content meaning, so directory listings do not reveal what a record is about.

This design adds a semantic slug to the filename — `<id>-<slug>.md` — following the researched Codex CLI pattern (`<timestamp>-<hash>-<slug>` in `rollout_summaries/`, `codex-rs/memories/write/src/storage.rs`): uniqueness stays carried entirely by the unchanged id; readability comes from the trailing slug. Claude Code's alternative (free `{type}_{topic}` naming backed by a `MEMORY.md` index and nightly consolidation) is not applicable: distill forbids a central index and CodexSpec has no resident runtime.

The convention is pure template text. Verified repository facts this design relies on: no runtime code parses, generates, or validates record filenames (`src/codexspec/profile.py` only scaffolds the six category directories); the naming rule is stated only in `internal/command_templates/sources/distill.md` (the opted-in maintainer source, rendered to `templates/commands/distill.md` by `internal/command_template_fragments.py --write`); `internal/command_templates/sources/onboard.md` reuses distill's format verbatim via a cross-note; the four worked examples in the distill template (`Con-2026-0809-2219gg-1`, `P-2026-0810-1330ab-1`, `S-2026-0813-1606fz-1`, `R-2026-0813-1143el-1`) show filenames; the substring assertions in `tests/test_distill_template.py` (lines 49–50, 142–143) test those example ids and remain valid when a slug suffix is appended, so no test change is mandatory; and the repo's `CLAUDE.md` (Profile Consumption section, line 349) documents the store with the now-stale phrase "the id also being the filename".

## Architecture & Components

### Filename convention definition (distill.md record-format section)

- **Responsibility**: The single authoritative statement of the store's naming: a record written after this feature is stored as `<category>/<id>-<slug>.md`. The revised `id` bullet replaces "the record's `### <id>: <title>` heading and its filename" wording with: the heading and id are unchanged; the filename is `<id>-<slug>.md`; the slug is derived from the record title, matches `^[a-z0-9]+(-[a-z0-9]+)*$`, is at most 50 characters, is rendered in English when the title is not ASCII, and may be omitted (bare `<id>.md`) when no meaningful slug can be derived. The section also states the id-lookup rule (a record's file is exactly `<id>.md` or `<id>-<slug>.md`; no other filename begins with `<id>` followed by `-` or `.`) and that the slug never participates in uniqueness. The store-layout sentence ("one record per file (`<id>.md`)") and the `add` mutation operation's path pattern (`<category>/<id>.md`) gain the same `<id>[-<slug>]` form.
- **Interface**: Template text executed by the distilling agent at record-write time; no runtime code reads it.
- **Covers**: REQ-001, REQ-002, REQ-003, REQ-004

### Worked examples in the distill template

- **Responsibility**: The four example record blocks show the new filename form (e.g. `pitfalls/P-2026-0810-1330ab-1-re-sub-string-replacement-corruption.md`) so the convention is taught by example, the same way the current filenames are.
- **Interface**: Markdown example blocks inside the same template section.
- **Covers**: REQ-001, REQ-005

### onboard.md format cross-note

- **Responsibility**: The sentence that delegates to distill's canonical format ("one record per file under a category directory (`conventions/<id>.md`, `constraints/<id>.md`)") reflects the `<id>-<slug>.md` form, so onboard-written records follow the identical convention.
- **Interface**: One template sentence in `internal/command_templates/sources/onboard.md`; no behavioral divergence from distill.
- **Covers**: REQ-005

### Distribution propagation via the fragment mechanism

- **Responsibility**: The rule reaches every distribution surface through the repository's established authoring path: edit the opted-in internal sources, run `uv run python internal/command_template_fragments.py --write` to regenerate `templates/commands/distill.md` and `templates/commands/onboard.md`, then the self-bootstrap install (`codexspec init`) regenerates `.claude/commands/codexspec/` and `.agents/skills/codexspec-*/`. The `--check-distribution` gate validates source/output consistency in CI and release.
- **Interface**: `internal/command_template_fragments.py --write` / `--check-distribution`; no fragment content changes (the slug rule does not become a shared fragment — it is specific to distill/onboard).
- **Covers**: REQ-005

### Repo CLAUDE.md store documentation

- **Responsibility**: The Profile Consumption section's "one record per file (`<id>.md`, the id also being the filename)" wording is updated to the id-plus-slug filename so the repo's own documentation states the store truthfully.
- **Interface**: Maintainer documentation only; no shipped artifact.
- **Covers**: REQ-001

## Key Design Decisions

### Decision 1: The slug lives in the filename only — id, heading, and `[[id]]` links unchanged

- **Context**: The id is the store's addressing anchor: headings, cross-links, dedup, and replace/remove operations all use it. Readability must not disturb that anchor.
- **Decision**: The slug is a filename suffix. `### <id>: <title>` keeps the bare id; `[[id]]` links keep working; nothing existing is rewritten.
- **Alternatives**: Folding the slug into the id itself (rejected: changes every heading and link, breaking NEED-002 for no readability gain); Claude Code-style free naming without ids (rejected: loses uniqueness-by-construction and source traceability — CON-001).
- **Trade-offs**: Filenames get longer (~15–65 extra characters); accepted — POSIX filename limits are far away and the slug cap bounds growth.
- **Covers**: REQ-001, REQ-003

### Decision 2: Id lookup stays mechanical via an exact boundary rule

- **Context**: With slug suffixes, "find the file for id X" can no longer mean "the file named `X.md`". The rule must stay deterministic without an index.
- **Decision**: A record's file is exactly `<id>.md` or `<id>-<slug>.md`; since the slug grammar admits only `[a-z0-9-]`, no filename other than the record's own can begin with `<id>` followed by `-` or `.`. Verified boundary cases: a sequence number that is a digit-prefix of another (`-4` vs `-40`), an all-digit slug, and legacy bare-id files coexisting with slug files all resolve uniquely and never collide.
- **Alternatives**: A maintained index mapping ids to files (rejected: OUT-001); fuzzy prefix matching (rejected: ambiguous exactly at the digit-prefix boundary).
- **Trade-offs**: The rule is one more sentence agents must follow; accepted — it is stated once in the canonical section and taught by the worked examples.
- **Covers**: REQ-001, REQ-003

### Decision 3: Bare `<id>.md` remains a valid fallback

- **Context**: A slug is derived by agent judgment; a record may occasionally have no meaningful ASCII rendering of its subject.
- **Decision**: When no meaningful slug can be derived, the agent writes the legacy bare form `<id>.md`. The store accepts both forms indefinitely (legacy records already make bare form permanent).
- **Alternatives**: Requiring a slug always (rejected: invents a failure mode with no compensating benefit; a forced bad slug is worse than none).
- **Trade-offs**: Directory listings can still contain occasional opaque names; accepted — this is the same state legacy records already produce, and DEC-002 keeps them.
- **Covers**: REQ-002

### Decision 4: Template text only — no runtime code

- **Context**: The convention is executed by the agent at record-write time; the repository has no code that touches record filenames today.
- **Decision**: No generator, validator, or migration tooling is added. The only executable artifact touched is the existing fragment renderer, invoked in its existing role.
- **Alternatives**: A code-level filename validator (rejected: contradicts the spec's REQ-005 statement and the toolkit's convention-driven pattern; adds a moving part with no failure to prevent that the `--check-distribution` gate does not already cover).
- **Trade-offs**: Nothing mechanically enforces the grammar; accepted — identical trust model to every other record-format rule in the template.
- **Covers**: REQ-005

## Requirements Coverage

| Spec Requirement | Design Coverage |
|------------------|-----------------|
| REQ-001 | Filename convention definition; Worked examples; Decision 1, Decision 2; Repo CLAUDE.md store documentation |
| REQ-002 | Filename convention definition (slug grammar, derivation, fallback); Decision 3 |
| REQ-003 | Decision 1, Decision 2 |
| REQ-004 | Filename convention definition (uniqueness statement); Decision 1 |
| REQ-005 | Worked examples; onboard.md cross-note; Distribution propagation; Decision 4 |

No NFR requirements exist in the spec. No optional design sections (data models, API contracts, sequence/data flow, cross-cutting design, risks) are warranted: the feature changes one naming rule in template text and introduces no new runtime behavior, interfaces, or data.
