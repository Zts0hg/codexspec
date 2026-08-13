# Design Document: onboard command

<!--
Language: document language = en (per .codexspec/config.yml).
Design stage between spec.md and plan.md. Describes WHAT the system is, not build phases.
-->

**Related Spec**: `.codexspec/specs/2026-0813-1606fz-onboard/spec.md`
**Confirmed Requirements**: `.codexspec/specs/2026-0813-1606fz-onboard/requirements.md`
**Created**: 2026-08-13
**Status**: Draft

## Context

`onboard` is a standalone slash command that scans an existing codebase and batch-writes
`conventions` (plus narrow config-level `constraints`) into the shared `.codexspec/profile/`
store — the cold-start counterpart to `distill`. Like `distill`, `debug`, and the other
agent-driven commands, it is delivered as a **command template** interpreted by the agent, not as
Python runtime code. This design describes the template's internal structure, its reuse of the
distill store, the tiered safety gate, and the distribution registration. It resolves the two
Design Opportunities raised in `review-spec.md` (the code-sourced `evidence.facts` variant, and the
`/distill review` DRY question).

## Architecture & Components

### C1. `templates/commands/onboard.md` — the onboard command template

- **Responsibility**: The single source of truth for onboard's discipline. Encodes, as ordered
  instructions the agent follows: (a) prerequisite check + scaffold ensure; (b) the high-signal,
  whole-repo, streaming/resumable scan with optional `[path]`; (c) the extraction rules
  (conventions incl. architecture/stack facts + narrow config-level constraints; flexible judgment,
  not a fixed marker checklist; explicit evidence anchors; no-signal → no-constraint; never
  decisions/pitfalls); (d) the tiered gate (conventions written immediately as `candidate`;
  constraints held for an inline end-of-scan quick review before persistence); (e) integration with
  the existing store (read-first, dedup, conflict-adjudicate, never clobber); (f) the terminal
  summary; (g) the boundaries (read-only on code, write-only to `.codexspec/profile/`, standalone —
  no auto-next / no auto-hook).
- **Interface**: Slash command `/codexspec:onboard [path]`; reads the working tree; writes
  `.codexspec/profile/{conventions,constraints}/<id>.md`; prints a terminal summary.
- **Covers**: REQ-001, REQ-002, REQ-003, REQ-006, REQ-007, REQ-008, REQ-009, REQ-013, REQ-014, NFR-002

### C2. Profile store reuse (`.codexspec/profile/`)

- **Responsibility**: onboard reuses distill's store verbatim — one record per file under a category
  directory, ids namespaced by the source-feature id, `claim` physically separated from `evidence`.
  onboard populates only `conventions/` and `constraints/`. Its only store mutations are `add` (a new
  `<id>.md` file) and `replace`-within-its-own-candidate-file; it never overwrites or deletes an
  existing `vetted`, human, or `distill` record.
- **Interface**: `add` / `replace` file operations on `.codexspec/profile/{conventions,constraints}/`.
  Record fields per the distill format, with the onboard deltas defined in Decision 2.
- **Covers**: REQ-004, REQ-010, REQ-011, REQ-012

### C3. Inline high-risk constraint gate

- **Responsibility**: At end of scan, onboard presents the accumulated constraint candidates for a
  quick in-session review (approve / edit / drop), and persists only approved ones (as `candidate`).
  This is a **pre-persist** gate scoped to this scan's constraints — distinct from `/distill review`
  (Decision 3). When zero constraint candidates were found, there is no synchronous step.
- **Interface**: Inline interactive prompt reusing the `/distill review` vocabulary; input = this
  scan's pending constraint candidates; output = the approved subset written to `constraints/`.
- **Covers**: REQ-005, NFR-003

### C4. Installer registration + distribution-surface lockstep

- **Responsibility**: Register onboard as a distributed command so `codexspec init` installs it.
- **Interface**: A `CommandMetadata` entry in `src/codexspec/commands/installer.py` under the
  `enhanced` category, placed adjacent to `distill` / `evolve`. Requires lockstep updates across
  every distribution-surface site: the docstring total and per-category count (`enhanced (7) → (8)`,
  `Total: 24 → 25`), the inline `# Enhanced Commands (7)` → `(8)` comment, the count assertions in
  `tests/commands/test_installer.py` (total and per-category) and `tests/test_cli.py`, and a row in
  all 8 `README*.md` files. A brand-new command needs no translation-catalog entry.
- **Covers**: REQ-016

### C5. Language Preference section (interaction/document regime)

- **Responsibility**: onboard's template carries a `## Language Preference` section referencing
  **both** `language.interaction` and `language.document` (the same regime as `distill`), because its
  generated content is not commit-message content. onboard MUST NOT be added to the
  `commit_templates` set in `tests/test_sdd_workflow_templates.py`.
- **Interface**: The standard interaction/document Language Preference block.
- **Covers**: NFR-001

### C6. Prerequisite check + scaffold ensure

- **Responsibility**: Before scanning, onboard verifies `.codexspec/` is present; if absent it stops
  and directs the user to `codexspec init` (it does not scaffold a whole project). If `.codexspec/`
  is present but the profile category directories are missing, onboard ensures them before writing.
  git is not required.
- **Interface**: A template pre-step; directory existence check + `mkdir` of the two category
  directories as needed.
- **Covers**: REQ-015

## Key Design Decisions

### Decision 1: onboard is a pure command template — no new Python runtime code

- **Context**: onboard could be implemented as a CLI subcommand (Python) or as an agent-driven
  command template. The behavior (read files, infer knowledge, write markdown records, converse for
  the gate) is inherently agentic.
- **Decision**: Deliver onboard as a command template only (like `distill` / `debug`). The sole
  code/config change is the installer registration (C4). No new module under `src/codexspec/`.
- **Alternatives**: A Python CLI `codexspec onboard` — rejected: the extraction/gate is agent work,
  and a Python scanner cannot do the semantic inference; it would duplicate what the agent already does.
- **Trade-offs**: onboard runs only inside an agent session (not as a headless CLI), which is
  consistent with OUT-005 (no headless mode in v1).
- **Covers**: REQ-001, REQ-013, REQ-016

### Decision 2: Reuse distill's store/format; onboard states only its deltas

- **Context**: `distill.md` is the canonical definition of the profile record format, and it says
  `evidence.facts` quotes the user's original words — but onboard's evidence is a code observation,
  and onboard records are always inference from code.
- **Decision**: The record format stays single-sourced in `distill.md`. `onboard.md` references it
  and states only its deltas: (1) `derivation` is always `inferred` → `status` is always `candidate`
  (never `vetted` at the onboard stage); (2) `evidence.facts` holds the concrete code observation
  (path + snippet/config anchor) instead of a user quote; (3) `provenance` marks the onboard scan as
  the source. A one-line cross-note is added to `distill.md`'s format section acknowledging the
  onboard (code-sourced) `evidence.facts` variant so the two channels do not appear to conflict.
- **Alternatives**: Duplicate the full record-format spec into `onboard.md` — rejected (drift risk,
  violates DRY). Introduce a second store/format for onboard — rejected by CON-002.
- **Trade-offs**: A reader of `onboard.md` must follow the reference to `distill.md` for the full
  format; accepted, in exchange for a single canonical format.
- **Covers**: REQ-011, REQ-012 (resolves review-spec Design Opportunity #1)

### Decision 3: Tiered gate — immediate `candidate` for conventions, inline pre-persist review for constraints; `/distill review` remains the async channel

- **Context**: `candidate` records take local effect immediately (weighted with caution); vetting via
  `/distill review` only gates `evolve`, not local effect. A wrong, top-weighted constraint from cold
  inference must not take effect unreviewed, but the user must not be trapped in a long synchronous
  audit.
- **Decision**: Conventions are written immediately as `candidate` (take effect, async-reviewable).
  Constraints are accumulated and pass an **inline end-of-scan quick review** (approve/edit/drop)
  **before** they are persisted at all. This pre-persist gate is scoped to the current scan's
  constraints and is **not** an invocation of `/distill review`. `/distill review` remains the
  separate, async, backlog-wide channel that promotes any `candidate` (conventions or approved
  constraints) toward `vetted`. onboard reuses `/distill review`'s interaction vocabulary but not its
  operation.
- **Alternatives**: (a) Block-before-write full synchronous audit of everything — rejected (bad UX on
  large repos). (b) A dormant/quarantine status tier drained asynchronously — rejected (new
  consumption semantics; profile inert until drained). (c) All-immediate with no gate — rejected
  (top-weighted false positives take effect unreviewed). (d) Invoke `/distill review` for the gate —
  rejected: `/distill review` is async, backlog-wide, and promotes to `vetted`; the gate is
  synchronous, this-scan-scoped, and a persist/no-persist decision.
- **Trade-offs**: A small synchronous step remains for constraints; minimized because config-level
  constraints are few. Conventions may briefly carry unreviewed noise (weighted with caution),
  accepted for immediate cold-start utility.
- **Covers**: REQ-004, REQ-005, NFR-003 (resolves review-spec Design Opportunity #2)

### Decision 4: Extraction scope = conventions + narrow constraints, by flexible judgment

- **Context**: Cold static scanning reliably yields conventions (observable regularities) and
  config-level constraints (machine-enforced prohibitions), but not decisions (rationale absent
  without ADRs, redundant with them) or pitfalls (experiential, not self-announced).
- **Decision**: onboard actively extracts only `conventions` (incl. architecture/stack facts) and
  config-level `constraints`, using the agent's flexible judgment over what the code actually shows —
  not a fixed file/marker checklist. Every constraint candidate carries an explicit config-level
  prohibition evidence anchor; absent such a signal, no constraint is proposed. onboard never writes
  `decisions/` or `pitfalls/`.
- **Alternatives**: Mine all four categories, opportunistically scrape named doc files, or mine git
  history — all rejected (redundant or unreliable/fabrication-prone), per DEC-002.
- **Trade-offs**: decisions/pitfalls coverage from onboard is intentionally zero; those remain
  distill's channels.
- **Covers**: REQ-003, REQ-009

### Decision 5: Scan model — high-signal-first whole-repo single pass, streaming/resumable

- **Context**: Real repositories exceed the context budget.
- **Decision**: Scan the whole repo (respecting `.gitignore`; sensible defaults to skip
  vendor/build/dependency dirs when there is no git), prioritize by signal density (deep-read
  structure, build/dependency/lint config, entry points, existing docs, test layout,
  frequently-imported core modules; shallow-sample the bulk), stream findings to disk as it goes so
  the scan is interruptible/resumable, and accept optional `onboard [path]` narrowing. The terminal
  summary distinguishes deep-read from sampled; onboard never claims full coverage silently.
- **Alternatives**: By-area incremental scanning (needs onboarded-area state); doc-only shallow scan
  (misses code-embedded conventions) — both rejected by DEC-004.
- **Trade-offs**: A single pass may under-cover a very large repo; mitigated by `[path]` + idempotent
  re-run and honest coverage reporting.
- **Covers**: REQ-006, REQ-007, NFR-002

### Decision 6: Language regime is interaction/document, not commit

- **Context**: `tests/test_sdd_workflow_templates.py` splits templates into a `commit_templates` set
  (which must reference `language.commit`) and all others (which must reference both
  `language.interaction` and `language.document`).
- **Decision**: onboard's generated content is profile records, not commit messages, so it references
  both `language.interaction` and `language.document` and is **not** added to `commit_templates`.
- **Alternatives**: Treat it as a commit-family command — rejected (wrong content type; would fail
  the split test in the opposite direction).
- **Trade-offs**: None.
- **Covers**: NFR-001

## API / Interface Contracts

### Command surface

| Element | Contract | Covers |
|---|---|---|
| `/codexspec:onboard` | Whole-repo scan; high-signal-first; writes conventions + reviewed constraints. | REQ-001, REQ-007 |
| `/codexspec:onboard [path]` | Narrow the scan to the given subdirectory/module. | REQ-007, DEC-006 |
| (no `--yes` / headless) | Not provided in v1; the constraint gate cannot be skipped. | REQ-005, OUT-005 |
| (no `--only <category>`) | Not provided in v1; refresh granularity is `[path]` + re-run. | REQ-008, OUT-006 |

### Behavior & error contract

| Situation | Behavior | Covers |
|---|---|---|
| `.codexspec/` absent | Stop; direct user to `codexspec init`. | REQ-015 |
| profile scaffold missing | Ensure the `conventions/` and `constraints/` directories, then proceed. | REQ-015 |
| no git / no `.gitignore` | Proceed; skip vendor/build/deps via defaults; note this in the summary. | REQ-007 |
| nothing inferable | Write nothing; report "nothing to onboard"; no gate. | REQ-002, REQ-005 |
| constraint candidate found | Held; presented at end-of-scan review; written only if approved. | REQ-005 |
| all constraints rejected | No `constraints/` record written; conventions unaffected. | REQ-005 |
| finding conflicts with existing record | Adjudicate (recency/specificity/scenario-decoupling/defer); never clobber `vetted`. | REQ-008, REQ-010 |
| scan interrupted | Streamed conventions persist; pending constraints re-presented on resume. | REQ-006 |

## Sequence & Data Flow

1. **Prerequisite** — verify `.codexspec/` present (else stop → init); ensure profile scaffold (C6).
2. **Read existing profile** — load current records for dedup/conflict adjudication (C2, REQ-008).
3. **Scan** — high-signal-first traversal (optionally scoped by `[path]`), streaming (C1, Decision 5).
4. **Per convention finding** — dedup vs existing; if new, `add` a `candidate` `conventions/<id>.md`
   immediately (takes local effect); adjudicate any conflict without clobbering (C2, REQ-004/010).
5. **Per constraint finding** — accumulate as a pending candidate with its evidence anchor; do **not**
   persist yet (C3, REQ-005).
6. **End-of-scan gate** — if any constraint candidates: present the inline quick review; write the
   approved subset as `candidate` `constraints/<id>.md` (C3, Decision 3). If none: skip.
7. **Terminal summary** — report records added/updated per category, and deep-read vs sampled
   coverage (C1, REQ-002, NFR-002).
8. Async, later, at the user's pace: `/distill review` refines/vets any `candidate` (Decision 3).

## Risks & Trade-offs

| Risk | Impact | Mitigation |
|---|---|---|
| False-positive conventions take immediate effect | Mildly wrong steering (weighted with caution) | `candidate` + async `/distill review`; conventions are low-risk vs constraints |
| Large repo under-covered by a single pass | Missed conventions | Honest deep-read-vs-sampled reporting (NFR-002); `[path]` + idempotent re-run (REQ-008) |
| Over-detection of constraints | Noise in the high-risk category | Inline pre-persist gate (REQ-005); no-signal → no-constraint (REQ-009) |
| onboard record format drifts from distill's | Two channels appear to conflict | Single-sourced format in `distill.md` + cross-note (Decision 2) |

## Requirements Coverage

| Spec Requirement | Design Coverage |
|------------------|-----------------|
| REQ-001 | C1; Decision 1 |
| REQ-002 | C1 (terminal summary); Behavior contract |
| REQ-003 | C1; Decision 4 |
| REQ-004 | C2; Decision 3; Sequence step 4 |
| REQ-005 | C3; Decision 3; API/Behavior contract |
| REQ-006 | C1; Decision 5; Sequence |
| REQ-007 | C1; Decision 5; API contract |
| REQ-008 | C2; Sequence steps 2/4; DEC-006 row |
| REQ-009 | C1; Decision 4 |
| REQ-010 | C2; Decision 2; Sequence step 4 |
| REQ-011 | C2; Decision 2 |
| REQ-012 | C2; Decision 2 |
| REQ-013 | C1; Decision 1 |
| REQ-014 | C1 |
| REQ-015 | C6; Behavior contract |
| REQ-016 | C4; Decision 1 |
| NFR-001 | C5; Decision 6 |
| NFR-002 | C1; Decision 5; Risks |
| NFR-003 | C3; Decision 3 |
