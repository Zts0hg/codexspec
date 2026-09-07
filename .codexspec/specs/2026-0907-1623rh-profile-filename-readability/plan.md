# Implementation Plan: profile-filename-readability

<!--
Language: en (.codexspec/config.yml language.document)
Delivers design.md of feature 2026-0907-1623rh.
-->

## Context

`design.md` defines the `<id>-<slug>.md` record filename convention for the `.codexspec/profile/` store: the unchanged record id stays the sole uniqueness carrier; a semantic slug (lowercase ASCII kebab, ≤50 chars, derived from the title, English when the title is not ASCII, omittable) adds readability. The change is template text only. This plan implements it in the opted-in maintainer sources, propagates through the fragment renderer and the self-bootstrap install, updates the repo's own documentation, and pins the taught-by-example convention with tests.

## Goals / Non-Goals

**Goals:**

- The naming rule, stated once in distill's record-format section, shows the `<id>[-<slug>].md` form everywhere it currently states `<id>.md` (id bullet, store-layout sentence, `add` mutation operation) plus the slug grammar, derivation, fallback, and the id-lookup boundary rule.
- The four worked examples, onboard's cross-note, the rendered distribution templates, the self-bootstrap copies, and the repo `CLAUDE.md` all reflect the new convention consistently.

**Non-Goals:**

- No runtime code, no migration of existing records, no central index, no type-letter normalization (design.md Non-Goals; DEC-002, OUT-001/002, OPEN-001).

## Plan-Level Decisions

### Decision 1: Author in the internal sources, propagate with the renderer plus a forced self-bootstrap reinstall

**Context**: distill and onboard are opted-in fragment-mechanism commands; their `templates/commands/` files are generated outputs, and `.claude/commands/codexspec/` + `.agents/skills/codexspec-*/` are install artifacts.
**Decision**: Edit `internal/command_templates/sources/*.md` only; run `uv run python internal/command_template_fragments.py --write`; then `uv tool install --force .` followed by `codexspec init --here --force --ai both` to regenerate the self-bootstrap copies from the updated templates (install first, because `init` copies templates from the installed package).
**Rationale**: This is the repository's mandated authoring path (constitution → "Workflow for Command Modifications"; `--ai both` per this repo's known re-init requirement); hand-editing generated copies would be silently overwritten and would fail `--check-distribution`.

### Decision 2: Strengthen the four example assertions to pin the new filenames

**Context**: `tests/test_distill_template.py` asserts the bare example ids as substrings (lines 49–50, 142–143); they survive the change but would not catch a silent reversion of the example filenames.
**Decision**: Extend those four assertions to the full new example filenames (e.g. `pitfalls/P-2026-0810-1330ab-1-re-sub-string-replacement-corruption.md`). Adopted from the review-design Design Opportunity.
**Rationale**: Four-line change that locks the taught-by-example convention; the design review verified no other assertion depends on the current wording.

### Decision 3: One commit for the whole interdependent set

**Context**: Source edits, rendered outputs, self-bootstrap copies, tests, and CLAUDE.md are one consistent tree; the repository's profile pitfall P-2026-0902-054178-4 documents that splitting interdependent sets makes pre-commit's repo-level test run judge a self-inconsistent tree and fail.
**Decision**: Commit all plan outputs together in a single commit (message in English, per this repo's `language.commit`).

### Decision 4: Slug strings for the four worked examples are fixed here

**Context**: The examples must model the convention; leaving slug choice to implementation invites inconsistent style.
**Decision** (all conform to `^[a-z0-9]+(-[a-z0-9]+)*$`, ≤50 chars):

- `conventions/Con-2026-0809-2219gg-1-prefer-absolute-imports.md`
- `pitfalls/P-2026-0810-1330ab-1-re-sub-string-replacement-corruption.md`
- `strategies/S-2026-0813-1606fz-1-suspect-markdown-emphasis-first.md`
- `runbooks/R-2026-0813-1143el-1-release-a-new-codexspec-version.md`

## Implementation Notes / Phases

**Phase 1 — Author and propagate**

- [ ] Rewrite the naming rule in `internal/command_templates/sources/distill.md`: the `id` bullet (heading/filename split, slug grammar `^[a-z0-9]+(-[a-z0-9]+)*$`, ≤50 chars, English rendering for non-ASCII titles, bare-`<id>.md` fallback, id-lookup boundary rule "the file is exactly `<id>.md` or `<id>-<slug>.md`; uniqueness never depends on the slug"), the store-layout sentence ("one record per file (`<id>.md`)" → `(<id>.md` or `<id>-<slug>.md)`), and the `add` operation's path pattern — **Covers**: REQ-001, REQ-002, REQ-003, REQ-004; Design: Filename convention definition
- [ ] Update the four worked examples to the Decision-4 filenames (heading and ids unchanged) — **Covers**: REQ-001, REQ-005; Design: Worked examples
- [ ] Update the onboard cross-note in `internal/command_templates/sources/onboard.md` (line ~59: `conventions/<id>.md`, `constraints/<id>.md` → `conventions/<id>-<slug>.md`, `constraints/<id>-<slug>.md`) — **Covers**: REQ-005; Design: onboard.md format cross-note
- [ ] Extend the four assertions in `tests/test_distill_template.py` (lines 49–50, 142–143) to the full new filenames — **Covers**: REQ-005; Design: Worked examples (Decision 2)
- [ ] Run `uv run python internal/command_template_fragments.py --write`; `--check-distribution` must exit 0 — **Covers**: REQ-005; Design: Distribution propagation
- [ ] `uv tool install --force .` then `codexspec init --here --force --ai both`; inspect `git diff` and keep only the expected regenerated copies (`.claude/commands/codexspec/distill.md`, `onboard.md`; `.agents/skills/codexspec-distill/SKILL.md`, `codexspec-onboard/SKILL.md`) — **Covers**: REQ-005; Design: Distribution propagation

**Phase 2 — Documentation and verification**

- [ ] Update `CLAUDE.md` line ~349: "one record per file (`<id>.md`, the id also being the filename)" → the id-plus-slug filename form — **Covers**: REQ-001; Design: Repo CLAUDE.md store documentation
- [ ] Verification battery (below); then commit everything as one commit — **Covers**: REQ-001…REQ-005; Design: all components

**Verification battery**

1. `uv run pytest` — full suite green, including the strengthened assertions.
2. `uv run python internal/command_template_fragments.py --check-distribution` — exit 0, and `git status --porcelain` identical before/after (the check must not mutate the tree).
3. Stale-wording sweep: `grep -n '<id>.md' internal/command_templates/sources/distill.md internal/command_templates/sources/onboard.md` returns only intended mentions (the fallback rule and legacy-form references), no remaining bare-form rule statements.
4. Init idempotence: a second `codexspec init --here --force --ai both` produces no diff.

## Risks / Trade-offs

| Risk | Impact | Mitigation |
|------|--------|------------|
| Re-init touches files beyond the expected copies | Unexpected diff noise in the commit | Inspect `git diff` after init; revert anything outside the four expected derived copies |
| Renderer rewrites more than the two sources | Hidden churn | `--check-distribution` plus the pre/post `git status` comparison in the battery |
| A stale `<id>.md` rule statement survives somewhere | Convention stated inconsistently | Stale-wording sweep (battery step 3) over both sources |

## Requirements Coverage

| Spec Requirement | Design Component | Plan Coverage |
|------------------|------------------|---------------|
| REQ-001 | Filename convention definition; Worked examples; CLAUDE.md doc | Phase 1 steps 1–2; Phase 2 CLAUDE.md step |
| REQ-002 | Filename convention definition (grammar/derivation/fallback) | Phase 1 step 1 |
| REQ-003 | Decision 1, Decision 2 (design) | Phase 1 step 1 (resolution + uniqueness wording) |
| REQ-004 | Filename convention definition; Decision 1 (design) | Phase 1 step 1 (uniqueness statement) |
| REQ-005 | Worked examples; onboard cross-note; Distribution propagation; Decision 4 (design) | Phase 1 steps 2–6; battery steps 2 & 4 |
