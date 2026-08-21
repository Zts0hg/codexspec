# Feature Specification: reverse-spec

**Feature Branch**: `2026-0818-2053p5-reverse-spec`
**Created**: 2026-08-20
**Status**: Draft
**Input**: Confirmed `requirements.md` (NEED-001..005, DEC-001..014, CON-001..005 and CON-007, OUT-001..007; CON-006 superseded by CON-007)

## Context & Goals

`reverse-spec` is the last remaining P0 capability: it makes CodexSpec usable on
**brownfield** codebases. Today the toolkit runs one way only
(`requirements → spec → design → plan → tasks → code`). A codebase that already
exists has no entry point into the pipeline, and a codebase whose SDD artifacts
exist has no mechanism to detect that its code has since diverged from them.

The command is **dual-mode by lifecycle**, not two competing features:

1. **Generate** — no confirmed baseline exists for the target slice. Read the
   code and draft `spec.md` (plus `design.md`, scaled to complexity), all marked
   `inferred/open`. The user reviews and confirms, which promotes the draft into
   an authoritative **design baseline**.
2. **Reconcile** — a confirmed baseline exists. Re-read the code against it and
   report **drift**, so the implementation cannot silently diverge from the
   confirmed design.

Neither half suffices alone. A specification derived from code is a mirror of
that code, so at the moment of generation the two are trivially consistent and no
deviation is detectable — generation alone cannot serve the anti-drift goal.
Conversely the defining property of a brownfield project is that no baseline
exists — reconciliation alone cannot serve brownfield. The confirmed goals
(process quality, understandability and maintainability, and assurance that the
implementation has not deviated from the design) require both, in that order.

Two structural principles carry through the whole specification:

- **Two axes.** The **authority axis** (requirements > spec > design > plan >
  tasks) governs which artifact wins a conflict. The **reconcilability axis**
  (design ≳ spec ≫ requirements) governs which artifact can be compared to code.
  Reconciliation compares against spec/design and adjudicates with requirements.
- **Report, never repair.** When code and a confirmed spec disagree, the code may
  carry a bug or the spec may be stale. The direction is not derivable by the
  tool, so it is always reported and never applied. This is deliberately the
  opposite of `analyze`, whose auto-remediation is sound only because its fix
  direction is uniquely fixed by the authority hierarchy.

### Boundary against existing capabilities

| Capability | Input | Output | Role |
|---|---|---|---|
| `onboard` (shipped) | code | `.codexspec/profile/` records | cold-starts the cross-feature **knowledge** store |
| `analyze` (shipped) | SDD artifacts | conforms spec/design/plan/tasks | consistency **between artifacts**; never reads code |
| **`reverse-spec`** (this feature) | **code** | **spec/design + `reconcile.md`** | cold-starts SDD **artifacts**; reconciles **code against spec** |

## User Scenarios

### User Story 1 — A brownfield module gains a specification (Priority: P1)

A maintainer points `reverse-spec` at an existing module that has no SDD
artifacts. The command scans it and seeds a feature workspace containing a
drafted `spec.md` and a `design.md` sized to the module's real complexity, every
statement marked as inferred. The maintainer reviews the draft, corrects what the
code got wrong, and confirms it — at which point it becomes the module's
authoritative design baseline.

**Independent Test**: run the command on a module with no existing workspace;
verify a new workspace is created containing `spec.md` and `design.md` marked
`inferred/open`, a fully `open` `requirements.md` stub, and a recorded slice path.

**Acceptance Scenarios**:

1. **Given** a slice path with no existing workspace, **When** the command runs,
   **Then** it enters generate mode and creates a workspace whose id follows the
   `{YYYY-MMDD-HHMM}{rr}` convention.
2. **Given** generate mode completes, **When** the artifacts are inspected,
   **Then** `spec.md` and `design.md` carry a file-level `Status: inferred/open`
   header and state explicitly that they are not a reconciliation baseline until
   confirmed.
3. **Given** generate mode completes, **When** `requirements.md` is inspected,
   **Then** it is a thin stub whose entries are all `open` and none of which
   asserts an inferred intent as confirmed.
4. **Given** a structurally trivial slice, **When** the design is produced,
   **Then** it scales down rather than padding sections that the code does not
   warrant.

### User Story 2 — Confirmed design catches an implementation that drifted (Priority: P1)

Weeks later the module's code has changed. The maintainer re-runs `reverse-spec`
on the same slice. Because a confirmed baseline now exists, the command
reconciles instead of regenerating: it compares the current code against the
confirmed spec/design and produces a report listing behavior the code has that
the spec never described, spec content with no implementation, and places where
the two disagree in meaning. Nothing is changed automatically; the maintainer
decides each item's direction.

**Independent Test**: with a confirmed baseline whose spec states a behavior the
code implements differently, run the command; verify a `reconcile.md` is written
listing that item as a semantic mismatch with both-side evidence and a suggested
but unapplied direction, and verify no source file or artifact was modified.

**Acceptance Scenarios**:

1. **Given** a slice whose workspace holds a confirmed `spec.md`, **When** the
   command runs, **Then** it enters reconcile mode rather than regenerating.
2. **Given** code implements behavior absent from the spec, **When** reconcile
   runs, **Then** the report records it with kind `undocumented-behavior`.
3. **Given** the spec states behavior the code lacks, **When** reconcile runs,
   **Then** the report records it with kind `unimplemented-spec`.
4. **Given** code and spec both cover a behavior but disagree, **When** reconcile
   runs, **Then** the report records it with kind `semantic-mismatch`, citing the
   code location and the spec text side by side.
5. **Given** any drift item, **When** the report is produced, **Then** it carries
   a suggested direction that is **not** applied, and no code, spec, design, or
   other artifact has been modified.
6. **Given** the code fully matches the baseline, **When** reconcile runs,
   **Then** it reports `IN_SYNC` with zero drift items — a valid outcome.

### User Story 3 — An unconfirmed draft is refused as a baseline (Priority: P1)

A maintainer generates a draft but has not yet reviewed it, then immediately
re-runs the command hoping for a drift check. The command refuses: comparing code
against a draft derived from that same code would compare the code with itself
and report zero drift by construction. It reports that the baseline is
unconfirmed and directs the maintainer to confirm spec/design first.

**Independent Test**: run the command twice in a row without confirming between
runs; verify the second run performs no reconciliation, writes no `reconcile.md`,
and reports the unconfirmed-baseline condition.

**Acceptance Scenarios**:

1. **Given** a workspace whose artifacts are still `Status: open`, **When** the
   command runs, **Then** it does not reconcile and does not write `reconcile.md`.
2. **Given** that condition, **When** the command reports, **Then** it states that
   the baseline is unconfirmed and that spec/design must be confirmed first.
3. **Given** the maintainer confirms by flipping the file-level status and adding
   a Confirmation Log entry, **When** the command is re-run, **Then** it
   reconciles — with no additional command or mechanism required to confirm.

### User Story 4 — A whole repository gets a map, not a monolith (Priority: P2)

A maintainer runs the command on an unfamiliar repository with no path argument.
Rather than emitting one unreadable repository-wide specification, the command
produces a thin architecture-level map and a list of candidate slices worth
specifying, giving an orientation plus a deepening plan.

**Independent Test**: run the command with no path on a multi-module repository;
verify an overview workspace is produced containing a thin architecture-level
`design.md` and a `slices.md` list, and containing neither `spec.md` nor
`reconcile.md`.

**Acceptance Scenarios**:

1. **Given** no path argument, **When** the command runs, **Then** it performs a
   high-signal architectural survey and writes an overview workspace.
2. **Given** the overview workspace, **When** inspected, **Then** it contains a
   thin architecture-level `design.md` marked `inferred/open` and a `slices.md`
   listing candidate slices with path, one-line description, and rough
   size/priority.
3. **Given** the overview workspace, **When** inspected, **Then** it contains no
   `spec.md` and no `reconcile.md`.

## Functional Requirements

### REQ-001 — Standalone command surface

Provide `/codexspec:reverse-spec [path]` as a distributed command template with an
optional path argument. It is invoked directly by the user, like `onboard` and
`debug`.

**Sources**: NEED-005, DEC-009, CON-001, CON-003

### REQ-002 — Mode is auto-detected from baseline presence

Resolve the target slice, locate any existing feature workspace covering that
slice, and select the mode: a **confirmed** baseline present → reconcile mode;
otherwise → generate mode.

Normalize the slice path before any comparison — **symbolic links resolved to the
real directory**, repo-relative, `.` / `..` / absolute forms resolved, trailing
slash dropped — and record the `Slice:` header in that same normalized form. The
governing rule is that **one directory reached by any spelling is one slice**; the
listed forms are that rule's examples, not its limit.

Only an **exact** match (normalized slice equal) selects a mode on its own. When
more than one workspace matches exactly, ask the user to select one; never silently
pick the most recent. When no workspace matches exactly but one or more **cover**
the slice (a recorded slice that is a proper ancestor of the given path), report
each and ask whether to use that wider workspace at its own boundary or create one
for the narrower path; never pick silently and never quietly nest. Choosing the
wider workspace selects a **workspace, not a mode**: its own `Status:` then decides
between reconciling and resuming its draft, so this path can never reconcile
against an unconfirmed baseline (REQ-008). A workspace recording a slice *inside*
the given one is disclosed as an overlap but does not block.

Only a file-level `Status: confirmed` counts as confirmed. A missing, unreadable,
or other status reads as **not confirmed** — a workspace an interrupted run left
half-written has no status line yet, and reading confirmation into that silence
would reconcile against a draft.

A slice must lie **inside** the repository. A `[path]` that exists but resolves
outside it (`..`, `../sibling`, `/`) is reported and refused; it could not be
recorded in the repo-relative `Slice:` form at all, and scanning a tree that
strictly contains the repository would produce the monolithic specification
NFR-005 forbids.

Baseline-driven mode detection applies **only when a `[path]` slice is supplied**.
A bare whole-repository run (no `[path]`), **or a `[path]` that resolves to the
repository root**, always performs the architectural survey of REQ-015 and never
reconciles, regardless of whether the overview workspace's artifacts have since
been confirmed. The survey workspace is identified by the `slices.md` marker its
artifacts carry, **never by its directory name** — a slice whose final path segment
is `overview` yields the same directory name, and going by name would let a bare
run overwrite that slice's draft and then hide its baseline from every later
lookup.

**Sources**: NEED-003, DEC-005, DEC-006, DEC-011, DEC-013, DEC-014

### REQ-003 — Generate mode output boundary

In generate mode, produce `spec.md` and `design.md` (design scaled to the slice's
actual complexity), plus a **thin, entirely `open`** `requirements.md` stub. Do
not reverse-derive requirement intent.

**Sources**: NEED-001, DEC-001, OUT-003

### REQ-004 — Generated workspace records the slice it covers

A workspace generated **for a slice** records the slice path its artifacts
describe, in the normalized form REQ-002 defines, so a later run can locate the
baseline for that slice and satisfy REQ-002 even when the user spells the path
differently. The survey workspace (REQ-015) is the exception: it describes the
whole repository, which is not a slice, so it records no slice path and is
identified by its `slices.md` instead.

**Sources**: DEC-005, DEC-006, DEC-013, DEC-014

### REQ-005 — All derived content is marked inferred and open

Generated `spec.md` and `design.md` carry a file-level `Status: inferred/open`
header, mark principal entries `[inferred]`, and state explicitly that they do not
serve as a reconciliation baseline until confirmed. Nothing derived is presented
as confirmed intent.

**Sources**: DEC-002, DEC-012, OUT-003

### REQ-006 — Confirmation reuses the existing convention

Promotion to baseline is performed by the user flipping the file-level
`Status: open → confirmed` and appending a **Confirmation Log** entry, reusing the
convention already established for `requirements.md`. This feature introduces **no
new command and no new confirmation mechanism**.

**Sources**: DEC-012, DEC-002

### REQ-007 — Reconciliation baseline is confirmed spec and design only

In reconcile mode, compare code against the slice's **confirmed** `spec.md` and
`design.md`. Never use `requirements.md`, `plan.md`, or `tasks.md` as a comparison
baseline. When the slice's confirmed baseline contains a `spec.md` but no
`design.md` (the design was legitimately scaled away, or predates it), reconcile
against the spec alone.

**Sources**: NEED-002, DEC-004, OUT-004

### REQ-008 — Unconfirmed baseline blocks reconciliation

When artifacts for the slice exist but are still `Status: open`, do not
reconcile and do not write `reconcile.md`. Report that the baseline is unconfirmed
and that spec/design must be confirmed first.

**Sources**: DEC-005

### REQ-009 — Detect three kinds of drift

Reconciliation detects and classifies each finding as exactly one of:
`undocumented-behavior` (present in code, absent from the baseline),
`unimplemented-spec` (stated in the baseline, absent from code), or
`semantic-mismatch` (present on both sides with disagreeing meaning).

**Sources**: NEED-002, DEC-010

### REQ-010 — Reconciliation output is a persistent report plus a session briefing

Write a persistent `reconcile.md` into the slice's workspace and additionally give
a short in-session briefing. The report has this shape:

```text
# Reconcile Report — <slice>
## Summary
- Baseline: <spec.md / design.md compared against, and their confirmed status>
- Code scope: <path/slice>
- Status: IN_SYNC | DRIFT_DETECTED        # summary only; gates nothing
- Counts: undocumented N1 / unimplemented N2 / mismatch N3, plus severity spread
## Drift Items                            # one entry per finding
- id / kind / severity / location / evidence / direction / status
## Notes
```

Each drift item carries: `id`; `kind` (per REQ-009); `severity`; `location` (code
`path:line` plus the corresponding baseline reference); `evidence` (the code
observation and the baseline text side by side); `direction`
(`fix-code | update-spec | needs-your-judgment`, with reasoning); and `status`
(`open`, awaiting the user's adjudication).

`reconcile.md` is the command's own output, so a later reconcile of the same slice
regenerates it. Regeneration replaces the previous report and does not carry over
adjudications the user recorded by editing item statuses; the command says so
before overwriting, so the user can resolve or copy out an earlier report's open
items first.

**Sources**: DEC-008, DEC-010

### REQ-011 — Severity reflects impact and gates nothing

Assign each drift item a severity of `Critical`, `Warning`, or `Minor` based on
that item's **actual impact** against confirmed intent — **not** fixed by its
`kind`. An undocumented behavior may be security-grade; a semantic mismatch may be
trivial. The report `Status` and item severities exist to help the user prioritize
and MUST NOT act as a PASS/FAIL gate on any workflow.

**Sources**: DEC-010

### REQ-012 — Report only; never repair

Reconciliation modifies nothing. The `direction` field is a suggestion that is
never executed; resolving each item is the user's decision.

**Sources**: NEED-002, DEC-003, OUT-001

### REQ-013 — Direction reasoning appeals to requirements intent

When suggesting a direction for a drift item, reason from the confirmed
`requirements.md` intent where it exists — requirements adjudicate which side
should change, even though they are never the mechanical comparison baseline.
When no confirmed intent covers the item, mark the direction
`needs-your-judgment` rather than guessing.

**Sources**: DEC-004

### REQ-014 — Slice unit and workspace creation

The unit of work is a slice identified by `[path]` — a directory, module, or
package path (or a file set within one). **The repository root is not a slice**: a
path resolving to it is the bare run of REQ-015. Each generate run produces its own
feature workspace directory `.codexspec/specs/<id>-<slice>/`, whose id reuses the
project's `{YYYY-MMDD-HHMM}{rr}` timestamp-plus-random convention. Creating a
workspace MUST NOT create or switch a git branch. Do not implement a separate ID
generator and do not introduce sequential numbering. Perform no "intelligent
auto-partitioning" of the codebase.

**Sources**: NEED-004, DEC-006, DEC-011, CON-007, DEC-014

### REQ-015 — Bare whole-repository run yields a map, not a specification

With no `[path]` argument, or with a `[path]` that resolves to the repository root,
perform a high-signal architectural survey and write an
overview workspace containing (a) a thin architecture-level `design.md`
(components, responsibilities, relationships; marked `inferred/open`, scaled to
complexity) and (b) `slices.md`, a candidate slice list with path, one-line
description, and rough size or priority. The bare run produces **no `spec.md` and
no `reconcile.md`**.

**Sources**: DEC-011, NEED-004, OUT-005, DEC-014

### REQ-016 — Scanning discipline reused from onboard

Scanning is high-signal-first, streaming and resumable, and honors `.gitignore`
with a sensible fallback when the target is not a git repository. Do not block
until the whole scan finishes before producing any output.

**Sources**: DEC-007, NEED-001

### REQ-017 — Read-only on code; writes confined to the feature workspace

The command is read-only with respect to the codebase and writes only into the
feature workspace it creates or resolves. It MUST NOT modify source, tests, or git
state; MUST NOT write to `.codexspec/profile/`; and MUST NOT automatically modify
code or any pre-existing artifact.

**Sources**: NEED-005, CON-004, OUT-001, OUT-002

### REQ-018 — No pipeline coupling

The command template carries **no** `## Auto-Next Chain Advance` section, no
automatic hook from any other command, and no `## Automatic Distillation` section.
It is neither auto-triggered by an upstream stage nor auto-triggers a downstream
one.

**Sources**: DEC-009, OUT-006

### REQ-019 — Slice input is path-based only

Accept a path as the slice input. A diff or pull-request changeset is not a
supported slice source in this feature.

**Sources**: OUT-007

### REQ-020 — Command registration and distribution lockstep

Register the command and update every dependent site together:

1. a `get_commands_metadata()` entry in `src/codexspec/commands/installer.py`
   under the **enhanced** category (adjacent to `onboard`);
2. that function's docstring **total** and **per-category** counts;
3. the category's inline `# <Category> Commands (N)` comment;
4. the command-count assertions in **both** `tests/commands/test_installer.py`
   (total and per-category) **and** `tests/test_cli.py`;
5. a row in **all 8** `README*.md` files, translated per language.

Keep the zh-CN installer description short enough to stay within the 120-column
ruff budget.

**Sources**: CON-002

### REQ-021 — Language regime is interaction plus document

The command's `## Language Preference` section references **both**
`language.interaction` and `language.document` and MUST NOT reference
`language.commit`. The command MUST NOT be added to the `commit_templates` set. As
a brand-new command it requires **no** entry in `templates/translations/*.json`
and installs with English frontmatter.

**Sources**: CON-002, CON-003

## Non-Functional Requirements

### NFR-001 — English template with a Language Preference section

The command template is authored in English and carries a `## Language
Preference` section, consistent with every other distributed command.

**Sources**: CON-003

### NFR-002 — Self-bootstrap discipline

The command is authored only in `templates/commands/reverse-spec.md`. The forms
under `.claude/commands/codexspec/` and `.agents/skills/codexspec-*/` are derived
install artifacts regenerated by `codexspec init` and MUST NOT be hand-edited.

**Sources**: CON-001

### NFR-003 — The two constitutions remain separate

This feature does not modify `_get_default_constitution()` and does not propagate
project-governance rules into the shipped default constitution.

**Sources**: CON-005

### NFR-004 — Scales to large codebases without blocking

Because scanning is high-signal-first, streaming, and resumable, a large or
interrupted scan degrades into partial progress that can be resumed rather than
an all-or-nothing failure.

**Sources**: DEC-007, NEED-004

### NFR-005 — Output stays independently readable and maintainable

Each slice's artifacts are independently readable, independently maintainable, and
independently reconcilable. No output aggregates the whole repository into a
single detailed specification.

**Sources**: NEED-004, OUT-005

### NFR-006 — No fabricated intent

Derived content never asserts unverified intent as fact. The `requirements.md`
stub is never presented as confident authority.

**Sources**: OUT-003, DEC-001

## Expected Error / Boundary Behavior

| Condition | Expected behavior |
|---|---|
| `[path]` does not exist | Report the invalid path and stop; create no workspace. |
| `[path]` exists but resolves outside the repository (`..`, `../sibling`, `/`) | Report that a slice must be inside the repository and stop; create no workspace (REQ-002, REQ-004, NFR-005). |
| `[path]` is an in-repo symlink pointing outside the tree (`packages/shared` → `../../shared`) | Containment is decided on the resolved real path, so it is refused like any other outside path; the scan never follows it out (REQ-002, NFR-005). |
| `[path]` is a symlink to a directory that already has a workspace | Resolves to the same slice, finds the existing workspace, and creates no duplicate (REQ-002, REQ-004). |
| A covering workspace is chosen but its artifacts are still `Status: open` | Resume its draft; never reconcile and never write `reconcile.md` (REQ-008). |
| A workspace has a `Slice:` header but no readable `Status:` line | Treated as not confirmed; resume the draft rather than reconciling (REQ-008, DEC-012). |
| A slice whose final path segment is `overview` | Produces the same directory name as the survey workspace; identity comes from the `slices.md` marker, never the directory name, so neither workspace shadows the other (REQ-002, REQ-004). |
| `[path]` exists but contains no analyzable code | Report that there is nothing to reverse-derive; create no workspace or artifacts. |
| Target is not a git repository | Continue scanning with a sensible ignore fallback (REQ-016); do not fail. |
| Scan is interrupted mid-run | Partial progress is preserved and the scan is resumable (REQ-016, NFR-004). |
| Workspace exists but artifacts are `Status: open` | Refuse reconciliation and write no `reconcile.md`; resume the draft in generate mode and report the unconfirmed baseline (REQ-008, REQ-016). |
| Generate or survey interrupted, then re-run | Continue the existing workspace rather than creating a second one for the same slice (REQ-016, NFR-004). |
| Reconciling a slice that already has a `reconcile.md` | Regenerate the report, announcing that prior adjudications are not carried over (REQ-010). |
| Confirmed baseline has `spec.md` but no `design.md` | Reconcile against the spec alone (REQ-007). |
| Multiple workspaces match the slice exactly | Ask the user to select; never silently pick the latest (REQ-002). |
| The same directory given in another spelling (`src/auth/`, `./src/auth`, absolute) | Normalizes to the same slice and finds the existing workspace; no duplicate is created (REQ-002, REQ-004). |
| No exact match, but a workspace covers the slice (e.g. `src/auth` given `src/auth/tokens`) | Report the covering workspace and ask whether to use it at its own wider boundary or create one for the narrower path; never reconcile against it silently (REQ-002). |
| A workspace records a slice nested inside the given one | Disclose the overlap and proceed; it does not block (REQ-002). |
| `[path]` resolves to the repository root | Treated as the bare run: perform the architectural survey; never produce a repository-wide detailed spec (REQ-014, REQ-015, NFR-005). |
| Bare run repeated after the overview design was confirmed | Perform the architectural survey again; never reconcile (REQ-002, REQ-015). |
| Code matches the baseline exactly | Report `IN_SYNC` with zero drift items — a valid, non-error outcome (REQ-010). |
| A drift item has no confirmed intent to adjudicate it | Mark direction `needs-your-judgment`; do not guess (REQ-013). |
| A diff or PR range is supplied as the slice | Not supported in this feature; report the path-only contract (REQ-019). |

## Confirmed Constraints & Decisions

- **Template governance / self-bootstrap** — author only in `templates/commands/`;
  derived forms are regenerated, never hand-edited (CON-001, NFR-002).
- **Distribution lockstep** — installer entry and counts, two independent test
  files, and 8 README files update together (CON-002, REQ-020).
- **Language regime** — interaction + document, never commit; not in
  `commit_templates`; no translation-catalog entry (CON-002, CON-003, REQ-021).
- **Read-only on code** — writes confined to the feature workspace; the profile
  store belongs to `onboard` (CON-004, REQ-017).
- **Two constitutions** — kept separate and untouched (CON-005, NFR-003).
- **Workspace creation without git mutation** — reuse the existing timestamp+random
  ID and directory conventions; no separate ID generator; creating a workspace
  never creates or switches a git branch (CON-007, REQ-014, REQ-017).
- **Report-only reconciliation** — the defining trade-off: drift direction is not
  derivable by the tool, so it is always surfaced and never applied (DEC-003,
  REQ-012).
- **Two axes** — spec/design for mechanical comparison, requirements for
  adjudication (DEC-004, REQ-007, REQ-013).
- **Naming** — the reconciliation report is `reconcile.md`; `drift.md`,
  `conflict.md`, and `conformance.md` were considered and rejected or not chosen
  for the reasons recorded in DEC-008.

## Out of Scope

- **No automatic code changes and no automatic drift resolution** — report only
  (OUT-001, REQ-012).
- **No writes to `.codexspec/profile/`** — that is `onboard`'s channel (OUT-002,
  REQ-017).
- **No fabricated requirement intent** — the stub stays thin and `open` (OUT-003,
  REQ-003, NFR-006).
- **No mechanical comparison of code against `requirements.md`** (OUT-004,
  REQ-007).
- **No repository-wide monolithic specification** — a bare run yields a map and a
  slice list (OUT-005, REQ-015).
- **No participation in `auto_next` or `auto_distill`** (OUT-006, REQ-018).
- **No diff / pull-request changeset as a slice source** — deferred to a later
  enhancement (OUT-007, REQ-019).

## Traceability

| Confirmed entry | Spec coverage |
|---|---|
| NEED-001 brownfield entry | REQ-003, REQ-016, User Story 1 |
| NEED-002 detect drift | REQ-009, REQ-010, REQ-012, User Story 2 |
| NEED-003 one command, two modes | REQ-002, User Stories 1–3 |
| NEED-004 slice-sized output | REQ-014, REQ-015, NFR-004, NFR-005 |
| NEED-005 standalone, read-only | REQ-001, REQ-017 |
| DEC-001 output boundary | REQ-003, NFR-006 |
| DEC-002 inferred/open until confirmed | REQ-005, REQ-006 |
| DEC-003 report only, human direction | REQ-012, Confirmed Constraints |
| DEC-004 baseline is spec/design, not requirements | REQ-007, REQ-013 |
| DEC-005 mode detection and degradation | REQ-002, REQ-004, REQ-008, User Story 3 |
| DEC-006 slice unit, own workspace | REQ-002, REQ-004, REQ-014 |
| DEC-007 reuse onboard scanning discipline | REQ-016, NFR-004 |
| DEC-008 persistent report plus briefing; naming | REQ-010, Confirmed Constraints |
| DEC-009 standalone, no chaining | REQ-001, REQ-018 |
| DEC-010 report structure and severity | REQ-009, REQ-010, REQ-011 |
| DEC-011 slice definition, whole-repo map | REQ-002, REQ-014, REQ-015, User Story 4 |
| DEC-012 confirmed baseline mechanism | REQ-005, REQ-006 |
| DEC-013 path normalization; exact match selects, covering asks | REQ-002, REQ-004 |
| DEC-014 repository root is not a slice | REQ-014, REQ-015, NFR-005 |
| CON-001 template governance | REQ-001, NFR-002 |
| CON-002 distribution lockstep, language family | REQ-020, REQ-021 |
| CON-003 English template, Language Preference | REQ-001, REQ-021, NFR-001 |
| CON-004 read-only, workspace-confined writes | REQ-017 |
| CON-005 two constitutions separate | NFR-003 |
| CON-007 ID/directory convention, no branch creation | REQ-014, REQ-017 |
| CON-006 authoritative script (superseded by CON-007) | historical only; no binding coverage |
| OUT-001 no auto code change / drift resolution | REQ-012, Out of Scope |
| OUT-002 no profile writes | REQ-017, Out of Scope |
| OUT-003 no fabricated intent | REQ-003, REQ-005, NFR-006 |
| OUT-004 no code-vs-requirements comparison | REQ-007, Out of Scope |
| OUT-005 no monolithic repo spec | REQ-015, NFR-005 |
| OUT-006 no auto_next / auto_distill | REQ-018 |
| OUT-007 no diff/PR slice source | REQ-019 |

## Open Questions

None. `requirements.md` records no open entries: every question raised during
discovery was resolved and confirmed at the user's explicit direction before this
specification was compiled.

## Assumptions

- **A-1 (derived, not new intent)**: because mode selection depends on locating an
  existing baseline for a slice (DEC-005) while each generate run creates its own
  workspace (DEC-006), the workspace must record which slice it covers. REQ-004
  states this requirement; the concrete lookup mechanism is a design-stage detail
  and introduces no new product decision.
