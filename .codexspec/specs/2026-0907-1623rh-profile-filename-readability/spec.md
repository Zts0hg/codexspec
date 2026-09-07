# Feature Specification

<!--
Language: en (.codexspec/config.yml language.document)
-->

## ADDED Requirements

### Requirement: Record filename carries a semantic slug (REQ-001)

A profile record written after this feature MUST be stored as `<id>-<slug>.md`, where `<id>` is the existing record id (`{type}-{feature-id}-{seq}`, unchanged) and `<slug>` is a short semantic suffix derived from the record title. The id, the `### <id>: <title>` heading, and `[[id]]` cross-links are unchanged by the slug. Locating a record from its id stays mechanical: the record's file is exactly the one named `<id>.md` or the one named `<id>-<slug>.md`; because the slug grammar (REQ-002) admits only `[a-z0-9-]`, no other filename can begin with `<id>` followed by `-` or `.` — so a lookup by id is unambiguous even when one record's sequence number is a digit-prefix of another's.

Sources: NEED-001, NEED-002, DEC-001

#### Scenario: distill writes a new record

- **WHEN** distill writes a new pitfall record with id `P-2026-0902-054178-4` whose title is about pre-commit stashing unstaged changes
- **THEN** the file is stored as `pitfalls/P-2026-0902-054178-4-precommit-stash-untracked.md`, and the heading inside remains `### P-2026-0902-054178-4: <title>` with no slug in the heading or the id

#### Scenario: cross-links still resolve

- **WHEN** another record contains `[[P-2026-0902-054178-4]]`
- **THEN** the link still identifies the record (the id is the leading, unchanged portion of the filename), and nothing requires rewriting existing links

### Requirement: Slug grammar and derivation (REQ-002)

The slug MUST match `^[a-z0-9]+(-[a-z0-9]+)*$` (lowercase ASCII letters and digits, hyphens only as separators, no leading/trailing hyphen) and MUST NOT exceed 50 characters — DEC-001's recommended maximum, adopted here as the binding upper bound (see Assumptions). It is derived from the record title at write time by the distilling agent; when the title is not ASCII, the slug is derived as English (per the project translation standard). When no meaningful slug can be derived, the agent MAY fall back to the legacy bare form `<id>.md` — the same form legacy records already use, so the store stays uniform in what it accepts.

Sources: CON-002, DEC-001

#### Scenario: non-ASCII title

- **WHEN** a record title is in Chinese (a project with `language.document: zh-CN`) and distill writes the record
- **THEN** the slug is an English rendering of the title's subject (for example a title about line-ending corruption yields a slug like `write-text-crlf-copy`), never CJK characters in the filename

#### Scenario: no meaningful slug available

- **WHEN** distill cannot derive a meaningful ASCII slug for a record
- **THEN** it writes the legacy bare form `<id>.md`; the record remains a valid member of the store

### Requirement: Uniqueness stays independent of content (REQ-003)

The uniqueness portion of the filename MUST remain the existing id, whose feature-id embeds timestamp+random characters. Filename uniqueness MUST NOT depend on the slug: two records with identical slugs but different ids never collide, and records distilled on parallel feature branches never produce the same filename (preserving conflict-free merging).

Sources: CON-001, DEC-001

#### Scenario: parallel branches distill similar knowledge

- **WHEN** feature branch A and feature branch B each distill a record about the same underlying pitfall
- **THEN** the two records have different feature-ids in their id portions, so their filenames differ regardless of how similar the slugs are, and the merge adds two files with no conflict

### Requirement: Existing records are not migrated (REQ-004)

Records written before this feature keep their current `<id>.md` filenames. The new convention applies only to records written after it; a directory mixing bare-id and slug filenames is expected and valid. No batch rename, no link rewriting, no migration tooling.

Sources: DEC-002

#### Scenario: legacy record untouched

- **WHEN** this feature lands in a repository that already has `pitfalls/P-2026-0902-054178-4.md`
- **THEN** that file keeps its name and content; only records written afterwards use the slug form

### Requirement: The convention is authored once and reaches every writer of the store (REQ-005)

The filename rule is defined in distill's canonical record-format section (the single authority for the store's format). onboard, which reuses that format verbatim, writes its records under the same `<id>-<slug>.md` convention, and its format cross-note reflects the filename form. The worked examples inside the distill template (convention, pitfall, strategy, runbook) show the new filename form. The change is template-text only: no runtime code parses, generates, or validates record filenames before or after this feature.

Sources: NEED-001, DEC-001

#### Scenario: onboard writes a record

- **WHEN** onboard writes a convention record with id `Con-2026-0907-1623rh-1` about naming conventions it inferred from the codebase
- **THEN** the file is stored as `conventions/Con-2026-0907-1623rh-1-<slug>.md` under the same slug rules as distill records

## Context

`/codexspec:distill` persists reusable cross-feature knowledge as one record per file under `.codexspec/profile/<category>/`. Today the filename equals the record id: `{type}-{feature-id}-{seq}.md` (for example `P-2026-0902-054178-4.md`). The id is deliberately unique-by-construction — the feature-id embeds timestamp+random characters so parallel feature branches never collide — but it carries no content meaning: a reader scanning the directory must open each file to learn its subject.

Research grounding (source-tree studies of both reference implementations, recorded during discovery):

- **Codex CLI** names rollout summary files `<timestamp>-<hash>-<slug>.md` — uniqueness by unique prefix, readability by trailing slug, no index file. Its slug is model-generated, lowercase ASCII, hyphenated, length-capped.
- **Claude Code** names memory files `{type}_{topic}.md` with no id or uniqueness guarantee, and compensates with an always-loaded `MEMORY.md` index plus a nightly consolidation pass — mechanisms CodexSpec deliberately lacks (distill forbids a central index as a merge-conflict magnet and has no resident runtime).

Codex's combination is the design that satisfies both of CodexSpec's hard constraints (conflict-free merging, no index), and CodexSpec's existing id already provides the unique prefix — only the slug is new.

Surfaces touched: the id rule in `internal/command_templates/sources/distill.md` (the opted-in maintainer source; rendered to `templates/commands/distill.md` and regenerated into `.claude/commands/codexspec/` and `.agents/skills/codexspec-distill/`), the format cross-note in `internal/command_templates/sources/onboard.md`, the worked example filenames in the distill template, the example-id assertions in `tests/test_distill_template.py`, and the stale "the id also being the filename" wording in the repo's `CLAUDE.md` profile-consumption section.

## Goals

- Make a record's topic readable from its filename without opening the file.
- Preserve, unchanged, the properties the store depends on: conflict-free parallel merges, id-based addressing (`### <id>:` headings, `[[id]]` links), and the template-text-only nature of the convention.

## Non-Goals

- No central index file (`MEMORY.md`-style). distill forbids one; readability comes from the filename itself. (OUT-001)
- No background consolidation or automated rename/reconciliation machinery. (OUT-002)
- No migration or batch rename of existing records. (DEC-002)
- No normalization of the type-letter inconsistency (`C-` for constraints vs `Con-` for conventions). This is OPEN-001, unresolved and non-blocking; the current letters are kept unless the user decides otherwise.

## User Stories

### Story: Scan the profile at a glance

**As a** developer or agent consulting the project profile
**I want** each record's filename to name its subject
**So that** I can find the relevant knowledge by listing the directory instead of opening every file.

**Acceptance Criteria:**

- [ ] A directory listing of `.codexspec/profile/pitfalls/` shows each record's subject (for example `P-2026-0902-054178-3-write-text-crlf-copy.md`) without opening files
- [ ] Newly written records across all six categories follow the same filename form

### Story: Distill on a parallel branch without merge fear

**As a** contributor distilling knowledge on a feature branch
**I want** record filenames to remain unique by construction
**So that** merging my branch never produces filename conflicts in the profile store.

**Acceptance Criteria:**

- [ ] Two branches writing records about the same topic still produce distinct filenames
- [ ] The id remains the sole uniqueness carrier; the slug never participates in uniqueness

## Constraints

- The unique portion of the filename must not be derived from record content (CON-001).
- Slug character set: lowercase ASCII letters/digits with hyphen separators only; no spaces, uppercase, or CJK (CON-002).
- The naming rule lives in template text executed by the agent at runtime; no code-level filename generator, validator, or migration is introduced.
- OPEN-001 (type-letter normalization) remains open and non-blocking; current letters are kept.

## Assumptions

- The 50-character slug cap instantiates the "recommended maximum 50 characters" from DEC-001 as the working upper bound; the recommendation did not state a hard limit.
- The fallback to bare `<id>.md` when no meaningful slug can be derived extends the legitimacy that DEC-002 already grants to bare-id filenames in the store; it adds no new store membership rule.

## Requirements Traceability

| Confirmed Requirement | Spec Coverage |
|-----------------------|---------------|
| NEED-001 (filename reveals topic) | REQ-001, REQ-002, REQ-005; Story: Scan the profile at a glance |
| NEED-002 (filename ↔ id resolvable) | REQ-001 (heading/cross-link unchanged; id-lookup resolution rule) |
| CON-001 (conflict-free merging) | REQ-003 |
| CON-002 (ASCII charset) | REQ-002 |
| DEC-001 (`{id}-{slug}.md`) | REQ-001, REQ-002, REQ-003, REQ-005 |
| DEC-002 (no migration) | REQ-004 |
| OUT-001 (no central index) | Non-Goals |
| OUT-002 (no consolidation machinery) | Non-Goals |
| OPEN-001 (type letters, open) | Non-Goals + Constraints (kept as-is, non-blocking) |
