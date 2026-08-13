# Feature Specification: onboard command

<!--
Language: document language = en (per .codexspec/config.yml).
Compiled from requirements.md (Feature ID 2026-0813-1606fz). Only confirmed entries are binding.
-->

**Feature Branch**: `2026-0813-1606fz-onboard`
**Created**: 2026-08-13
**Status**: Draft
**Input**: Confirmed requirements record `.codexspec/specs/2026-0813-1606fz-onboard/requirements.md`

## Context & Goals

`onboard` is a standalone, user-invoked slash command that scans an existing codebase and
batch-writes reusable project knowledge — knowledge that is **implicit in the code and not
already recorded accessibly** — into the shared `.codexspec/profile/` store. It is the
**cold-start / bulk counterpart to `distill`**: `distill` writes the profile incrementally from
interaction; `onboard` writes it in bulk from code, so a brownfield project's profile is grounded
immediately instead of only after enough work has flowed through `distill`.

Its reliable extraction scope is `conventions` (primary, including observable architecture /
tech-stack facts) plus a narrow, config-level `constraints`. It deliberately does **not** mine
`decisions` or `pitfalls`. Safety is tiered: the bulk (`conventions`) takes local effect
immediately as `candidate` records reviewable later — asynchronously and incrementally — via the
existing `/distill review` channel, while the only high-risk category (`constraints`) passes a
quick in-session human review before it is persisted.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Cold-start the profile from an existing codebase (Priority: P1)

A developer adopts CodexSpec in an existing (brownfield) project whose `.codexspec/profile/` is
empty. They run `onboard`. It scans the repository, and — streaming as it goes — writes the
`conventions` it can infer from the code (structure, naming, import style, tech stack, lint/format
config, test layout, repeated patterns, architecture/stack facts) as `candidate` records that
take effect immediately. At the end it prints a summary of everything written/updated.

**Why this priority**: This is onboard's core value and a viable MVP on its own — it bootstraps the
profile so downstream work (e.g. `specify`) is grounded in the project's real conventions.

**Independent Test**: Run `onboard` in a repo with a clear, consistent convention (e.g. absolute
imports, a `tests/` layout, a known package manager). Verify matching `conventions` records are
created under `.codexspec/profile/conventions/`, each with a precise evidence anchor, and that the
terminal summary lists them.

**Acceptance Scenarios**:

1. **Given** a codexspec-initialized repo with an empty profile and consistent code conventions,
   **When** `onboard` runs to completion, **Then** each inferred convention is written as a
   `candidate` record (one file per record) with `derivation: inferred`, `provenance` marking the
   onboard scan, and `evidence.facts` holding the concrete code observation (path + snippet).
2. **Given** the scan completed, **When** the run ends, **Then** a terminal summary lists every
   record written or updated, and no persistent document or code walkthrough is produced.
3. **Given** an empty repo or a repo with no inferable high-signal knowledge, **When** `onboard`
   runs, **Then** it writes nothing and reports "nothing to onboard" without blocking on the user.

---

### User Story 2 - Quick in-session review gates high-risk constraints (Priority: P1)

While scanning, onboard also detects a small number of **config-level explicit hard prohibitions**
(e.g. lint/type rules set to *error* that ban imports/APIs, `do not edit` / generated-file markers,
CODEOWNERS / protected paths). Because `constraints` are honored first and carry the highest
weight, onboard does **not** persist them silently. At the end of the scan it presents the
accumulated constraint candidates for a quick human review; approved ones are written, rejected
ones are dropped. The `conventions` already written are unaffected.

**Why this priority**: The safety-defining behavior. It is what makes "write all inferable
knowledge" safe: a wrong, top-weighted constraint can never take local effect unreviewed.

**Independent Test**: Run `onboard` in a repo whose lint config sets a banned-import rule to error.
Verify the candidate constraint is presented for review, that approving it writes a
`constraints/` record and rejecting it writes nothing, and that neither choice alters the
`conventions` written earlier.

**Acceptance Scenarios**:

1. **Given** the scan found one or more constraint candidates, **When** the scan completes,
   **Then** onboard presents them for a quick in-session review (approve / edit / drop) before any
   `constraints/` record is persisted.
2. **Given** the reviewer approves a constraint candidate, **When** the review resolves, **Then**
   it is written as a `candidate` constraint record with a precise evidence anchor; **Given** it is
   rejected, **Then** no record is written for it.
3. **Given** the scan found zero constraint candidates, **When** the scan completes, **Then** there
   is no synchronous review step and the run finishes without blocking on the user.

---

### User Story 3 - Non-destructive re-run and integration with an existing store (Priority: P2)

A project already has profile records — some from `distill`, some `vetted`, some hand-authored.
The developer re-runs `onboard` (whole repo, or a narrowed `onboard src/newmodule/`). onboard reads
the existing profile first, skips what is already covered, adjudicates conflicts, and appends only
new records as new files. It never overwrites or deletes an existing `vetted`, human, or `distill`
record.

**Why this priority**: Onboarding is not a one-shot; safe, idempotent re-runs are required for the
command to be usable over a project's life. The no-clobber guarantee protects accumulated knowledge.

**Independent Test**: Populate the profile with a `vetted` record and a `distill` record, then
re-run `onboard`. Verify those files are byte-for-byte unchanged, that already-covered knowledge is
not re-asserted, and that only new, non-duplicate records are added.

**Acceptance Scenarios**:

1. **Given** existing `vetted` / human / `distill` records, **When** `onboard` re-runs, **Then**
   none of them is modified or deleted; new knowledge is appended as new files only.
2. **Given** knowledge already captured in the profile, **When** `onboard` re-runs, **Then** it is
   de-duplicated (not re-asserted).
3. **Given** a new finding conflicts with an existing record, **When** onboard integrates it,
   **Then** the conflict is adjudicated (recency / specificity / scenario-decoupling / defer) and a
   `vetted` record is never clobbered.

---

### User Story 4 - Scoped, resumable scan on a large repository (Priority: P2)

On a large repository the developer scopes the run with `onboard [path]`, or lets a whole-repo run
prioritize high-signal sources and shallow-sample the bulk. Findings stream to disk as the scan
proceeds, so the scan is interruptible and resumable and the developer is never made to wait for a
full scan before anything happens or is shown.

**Why this priority**: Real repositories exceed the context budget; without prioritization + streaming
the command is unusable at scale. Important, but layered on top of the P1 core behavior.

**Independent Test**: Run `onboard some/subdir` and verify only that subtree is scanned; interrupt a
whole-repo run and verify already-streamed `conventions` persist and a resumed run continues.

**Acceptance Scenarios**:

1. **Given** `onboard [path]`, **When** it runs, **Then** only that subdirectory/module is scanned.
2. **Given** a whole-repo run, **When** it scans, **Then** it prioritizes high-value sources
   (structure, build/dependency/lint config, entry points, existing docs, test layout,
   frequently-imported core modules) and only shallow-samples the bulk of business code,
   respecting `.gitignore`.
3. **Given** the scan is interrupted before completion, **When** it is re-run, **Then** already
   written `conventions` remain and pending constraint candidates are presented on the resumed run
   (none are silently lost).

### Edge Cases

- **Not codexspec-initialized (`.codexspec/` absent)**: onboard stops and directs the user to
  `codexspec init`; it does not scaffold a whole project. (REQ-015)
- **Profile scaffold missing but `.codexspec/` present**: onboard ensures the four category
  directories before writing. (REQ-015)
- **Not a git repository (no `.gitignore`)**: onboard still runs (git is not required); lacking
  `.gitignore` it falls back to sensible defaults to avoid vendored/build/dependency directories,
  and states this in its summary. (REQ-007, REQ-015)
- **Repository too large to read fully**: onboard deep-reads high-signal sources and shallow-samples
  the rest, and its summary distinguishes what was deep-read from what was sampled — it never claims
  full coverage silently. (REQ-007, NFR-002)
- **All constraint candidates rejected in review**: no `constraints/` record is written; the
  `conventions` written earlier are unaffected. (REQ-005)
- **A finding conflicts with an existing record**: adjudicated per the store's conflict rules; a
  `vetted` record is never clobbered; genuinely unresolvable conflicts are deferred, not guessed.
  (REQ-008, REQ-010)
- **Interruption during the constraint review**: unreviewed constraint candidates are not persisted
  and are re-presented on the next run; nothing high-risk is written without review. (REQ-005, REQ-006)

## Requirements *(mandatory)*

### Functional Requirements

- **REQ-001**: onboard MUST scan an existing codebase and batch-write reusable knowledge inferred
  from the code into `.codexspec/profile/`, acting as the bulk / cold-start counterpart to
  `distill`.
  - Sources: NEED-001
- **REQ-002**: The output surface MUST be exactly the profile candidate records plus a terminal
  summary of what was written/updated; onboard MUST NOT produce a persistent document or a code
  walkthrough.
  - Sources: NEED-002, DEC-001, OUT-003
- **REQ-003**: onboard MUST actively extract only `conventions` (including observable architecture /
  tech-stack facts) and narrow, config-level `constraints`; it MUST NOT actively extract `decisions`
  or `pitfalls`.
  - Sources: NEED-003, DEC-002, OUT-001
- **REQ-004**: `conventions` records MUST be written as `candidate` records that take local effect
  immediately (weighted with caution) and are reviewable later, asynchronously and incrementally,
  via the existing `/distill review` channel.
  - Sources: NEED-004, DEC-003
- **REQ-005**: `constraints` candidates MUST be held for a quick in-session human review at the end
  of the scan; only approved candidates are persisted, rejected ones are dropped, and this is the
  only synchronous review step. onboard MUST NOT persist a constraint without this review.
  - Sources: NEED-004, DEC-003, OUT-005
- **REQ-006**: onboard MUST write findings as it scans (streaming) and the scan MUST be
  interruptible and resumable; onboard MUST NOT block until the whole scan finishes before any
  interaction or output.
  - Sources: NEED-005
- **REQ-007**: The scan MUST cover the whole repository respecting `.gitignore`, prioritize by
  signal density (deep-read high-value sources, shallow-sample the bulk of business code), and MUST
  accept an optional `onboard [path]` argument to narrow the scan to a subdirectory/module.
  - Sources: NEED-006, DEC-004
- **REQ-008**: onboard MUST read the existing profile first, de-duplicate against records already
  present, adjudicate conflicts, and be safe to re-run idempotently (refresh / augment). v1 refresh
  granularity is `[path]` narrowing plus idempotent re-run; per-record management is delegated to
  `/distill review`.
  - Sources: NEED-007, DEC-006
- **REQ-009**: Extraction MUST rely on the agent's flexible judgment over what the code actually
  shows, not a fixed file/marker checklist. `conventions` derive from observable regularities plus
  architecture/stack facts; `constraints` derive only from config-level explicit hard prohibitions,
  each carrying a precise evidence anchor (file:line / config snippet); absent an explicit
  prohibition signal, onboard proposes no constraint.
  - Sources: NEED-008
- **REQ-010**: onboard MUST NOT overwrite or delete any existing `vetted`, human, or `distill`
  record; new knowledge is appended as new files; onboard's only store mutations are add and
  edit-within-its-own-candidate-file.
  - Sources: CON-001
- **REQ-011**: onboard MUST reuse `distill`'s store and record format — one record per file, ids
  namespaced by the source-feature id, `claim` physically separated from `evidence` — and MUST NOT
  create a second store or a divergent format.
  - Sources: CON-002
- **REQ-012**: Every onboard record MUST have `derivation: inferred` and be written as `candidate`
  (never promoted to `vetted` at the onboard stage); `evidence.facts` MUST record the concrete code
  observation (path + snippet), and `provenance` MUST mark the onboard scan as the source (distinct
  from distill).
  - Sources: CON-003
- **REQ-013**: onboard MUST be a standalone, user-invoked command — not an SDD pipeline stage: no
  auto-next and no auto-hook.
  - Sources: CON-004
- **REQ-014**: onboard MUST be read-only against the codebase and write only to
  `.codexspec/profile/`; it MUST NOT modify source, tests, git state, or the constitution.
  - Sources: CON-005, OUT-004
- **REQ-015**: onboard MUST require a codexspec-initialized project (`.codexspec/` present),
  stopping and directing the user to `codexspec init` when absent, and MUST ensure the profile
  scaffold (the four category directories) when it is missing; it MUST NOT strictly require git.
  - Sources: CON-006
- **REQ-016**: onboard MUST be registered as a distributed command in the installer under the
  `enhanced` category (alongside `distill` / `evolve`), with the enhanced count and total updated in
  lockstep across every distribution-surface site.
  - Sources: DEC-005

### Non-Functional Requirements

- **NFR-001**: onboard is a distributed command: its template MUST stay in English with a
  `## Language Preference` section (interaction / document language split), following the dynamic
  translation convention.
  - Sources: CON-007
- **NFR-002**: onboard MUST remain usable on a large repository within the context budget via
  high-signal prioritization plus streaming/resumable scanning; it is not required to read the
  repository fully, and it MUST NOT claim full coverage when it sampled.
  - Sources: NEED-005, NEED-006
- **NFR-003**: The synchronous human interaction in a run MUST be minimal — only the small high-risk
  constraint set is gated; the bulk (`conventions`) MUST require no synchronous audit.
  - Sources: NEED-004, DEC-003

### Key Entities

- **Profile record**: one markdown file per record under a category directory
  (`.codexspec/profile/{conventions,constraints}/<id>.md` for onboard). Fields: `id` (namespaced by
  the source-feature id), `claim`, `type`, optional `scope/when`, `evidence.facts` (code observation
  for onboard), `evidence.state`, `provenance` (onboard scan), `status` (`candidate`),
  `derivation` (`inferred`).
- **Constraint candidate (pending review)**: a proposed `constraints/` record accumulated during the
  scan, not yet persisted, awaiting the end-of-scan quick review.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Running `onboard` on a brownfield project with an empty profile produces `conventions`
  records for the conventions observable in the code, each with a precise evidence anchor, and a
  terminal summary listing every record written/updated.
- **SC-002**: Across any `onboard` run, no existing `vetted`, human, or `distill` record is modified
  or deleted (verifiable: those files' content is unchanged; only new files are added).
- **SC-003**: The only synchronous user interaction in a run is the high-risk constraint review; a
  run with zero constraint candidates completes without blocking on the user.
- **SC-004**: Re-running `onboard` (whole repo or a narrowed `[path]`) adds only new, non-duplicate
  records and never re-asserts already-covered knowledge.
- **SC-005**: onboard never writes a `decisions/` or `pitfalls/` record.
- **SC-006**: Every onboard-written record has `status: candidate` and `derivation: inferred` (no
  onboard-written record is `vetted`).

## Out of Scope

- **No active extraction of `decisions` or `pitfalls`** (OUT-001): documented ones are redundant to
  copy; undocumented ones are unreliable (pitfalls experiential, decision rationale fabricated). Both
  remain `distill`'s channels.
- **No feature-scoped SDD artifacts** (OUT-002): onboard does not produce `requirements.md` /
  `spec.md` or any per-feature artifact — that is the job of a future `reverse-spec`.
- **No persistent map document or walkthrough** (OUT-003): deferred to a possible future `explain`.
- **No constitution / source / test / git mutation** (OUT-004).
- **No autonomous `--yes` / headless mode that skips the high-risk review in v1** (OUT-005).
- **No `--only <category>` per-category refresh filter in v1** (OUT-006): per-record management is
  handled by `/distill review`.

## Assumptions

- The agent executing onboard has read access to the full working tree.
- `distill`'s store format and the `/distill review` vetting channel already exist; onboard reuses
  them rather than defining new ones.

## Dependencies

- The `.codexspec/profile/` store and distill's one-file-per-record, namespaced-id record format.
- The `/distill review` channel for asynchronous vetting of `candidate` records.
- The installer plus the distribution-surface lockstep sites (installer entry, docstring counts,
  inline category comment, `test_installer.py` / `test_cli.py` counts, READMEs).

## Requirements Traceability

| Confirmed Requirement | Spec Coverage | Notes |
|-----------------------|---------------|-------|
| NEED-001 | REQ-001 | Full |
| NEED-002 | REQ-002 | Full |
| NEED-003 | REQ-003 | Full |
| NEED-004 | REQ-004, REQ-005, NFR-003 | Tiered safety model |
| NEED-005 | REQ-006, NFR-002 | Streaming/resumable |
| NEED-006 | REQ-007, NFR-002 | High-signal single pass |
| NEED-007 | REQ-008 | Integration + idempotent re-run |
| NEED-008 | REQ-009 | Flexible extraction, no fixed marker list |
| CON-001 | REQ-010 | No-clobber |
| CON-002 | REQ-011 | Reuse distill store/format |
| CON-003 | REQ-012 | inferred → candidate |
| CON-004 | REQ-013 | Standalone, no auto-next/hook |
| CON-005 | REQ-014 | Read-only code / write-only profile |
| CON-006 | REQ-015 | Init prerequisite + scaffold |
| CON-007 | NFR-001 | Distributed command i18n |
| DEC-001 | REQ-002 | Output surface = profile only |
| DEC-002 | REQ-003 | Scope = conventions + narrow constraints |
| DEC-003 | REQ-004, REQ-005, NFR-003 | Quick high-risk review + immediate rest |
| DEC-004 | REQ-007 | High-signal, whole-repo single pass |
| DEC-005 | REQ-016 | Installer category = enhanced |
| DEC-006 | REQ-008, OUT-006 | `[path]` + idempotent re-run; no `--only` |
| OUT-001 | REQ-003, Out of Scope | No decisions/pitfalls extraction |
| OUT-002 | Out of Scope | No feature-scoped SDD artifacts |
| OUT-003 | REQ-002, Out of Scope | No map/walkthrough |
| OUT-004 | REQ-014, Out of Scope | No source/test/git/constitution mutation |
| OUT-005 | REQ-005, Out of Scope | No `--yes`/headless skip of review |
| OUT-006 | REQ-008, Out of Scope | No per-category refresh filter |

## Open Questions

None. All open questions from discovery were resolved before compilation.
