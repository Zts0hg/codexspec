# Requirements: reverse-spec (brownfield reverse specification and reconciliation)

Feature ID: `2026-0818-2053p5`
Feature directory: `.codexspec/specs/2026-0818-2053p5-reverse-spec/`
Status: Discovery complete — all entries confirmed
Last Confirmed: 2026-08-20

## Authority Rules

- Only entries with `Status: confirmed` are binding downstream inputs.
- `open` entries MUST NOT be converted into confirmed product requirements.
- Replaced entries remain in this file with `Status: superseded` and a link to the replacement.
- AI inferences must be labeled as assumptions and require user confirmation before becoming binding.

## Overview

`reverse-spec` is the last remaining P0 capability: it makes CodexSpec usable on
**brownfield** codebases. Today the toolkit only works forward
(`requirements → spec → design → plan → tasks → code`); a codebase that already
exists has no entry point into the pipeline, and a codebase whose SDD artifacts
exist has no mechanism to detect that the code has since diverged from them.

The command is **dual-mode by lifecycle**, not two competing features:

1. **Generate (day 1)** — no confirmed baseline exists. Read the code, draft
   `spec.md` (+ `design.md`, scaled to complexity) marked `inferred/open`. The
   user reviews and confirms, which promotes the draft into an authoritative
   **design baseline**.
2. **Reconcile (day 30 onward)** — a confirmed baseline exists. Re-read the code
   against it and report **drift**, so the implementation cannot silently
   diverge from the confirmed design.

Generation alone cannot serve the anti-drift goal: a spec derived from code is a
mirror of that code, so at the moment of generation the two are trivially
consistent and no deviation is detectable. Reconciliation alone cannot serve
brownfield: the defining property of a brownfield project is that no baseline
exists yet. The user's stated goals — higher process quality, better
understandability and maintainability, and assurance that the implementation has
not deviated from the design — require both, in that order.

### Boundary against existing capabilities

| Capability | Input | Output | Role |
|---|---|---|---|
| `onboard` (shipped) | code | `.codexspec/profile/` records | cold-starts the cross-feature **knowledge** store |
| `analyze` (shipped) | SDD artifacts | conforms spec/design/plan/tasks | consistency **between artifacts**; never reads code |
| **`reverse-spec`** (this feature) | **code** | **spec/design + `reconcile.md`** | cold-starts SDD **artifacts**; reconciles **code against spec** |

`reverse-spec` uniquely owns "code → SDD artifacts" and "code ↔ spec
reconciliation". The latter is not covered by `analyze` at all, which compares
artifacts to each other and never inspects the implementation.

---

## Needs (NEED)

### NEED-001 — Brownfield entry into the pipeline

- Statement: Read existing code and produce SDD artifacts (`spec.md`, and
  `design.md` scaled to complexity), so an existing codebase can enter and
  benefit from Requirements-First SDD.
- Rationale: Strategic — without it CodexSpec is only usable on greenfield work.
- Status: confirmed

### NEED-002 — Detect implementation drift from confirmed design

- Statement: Detect divergence between code and its **confirmed** spec/design,
  and report it as three kinds of drift: behavior present in code but absent
  from the spec; spec content with no implementation; and content present on
  both sides whose meaning disagrees.
- Rationale: The user's central quality goal — "确保代码实现没有偏离设计".
- User Evidence: "让整个开发过程更加高质量并且更加易于被理解和维护，确保代码实现没有偏离设计"
- Status: confirmed

### NEED-003 — One command, two modes, driven by lifecycle

- Statement: A single command switches mode based on whether a confirmed
  baseline exists for the target: no baseline → generate; baseline → reconcile.
  The lifecycle is generate → confirm → reconcile (repeatedly).
- Rationale: The two modes share the hard part (reading code into a
  spec-shaped understanding) and diverge only at the final step — what to
  compare against. They are two phases of one workflow, not two features.
- Status: confirmed

### NEED-004 — Slice-sized, independently maintainable output

- Statement: Output is produced per **slice**, and each slice's artifacts must
  be independently readable, independently maintainable, and independently
  reconcilable.
- Rationale: A single repository-wide specification is unreadable and
  unmaintainable, which would defeat the understandability/maintainability goal
  the feature exists to serve.
- Status: confirmed

### NEED-005 — Standalone command, read-only on code

- Statement: Provide `/codexspec:reverse-spec [path]` as a standalone command
  that is read-only with respect to the codebase and writes only into the
  feature workspace it creates.
- Status: confirmed

---

## Decisions (DEC)

### DEC-001 — Output boundary is spec + design; requirements stays a thin open stub

- Decision: Reverse-derive `spec.md` and `design.md` (design scaled to
  complexity). `requirements.md` is created only as a **very thin, entirely
  `open` stub**.
- Reason: Reverse-derivation fidelity decreases as it moves up the chain.
  Structure (design) is literally present in the code; behavior (spec) is
  derivable from public API, tests, and code paths; **intent (requirements) is
  not in the code at all** and would have to be fabricated. This mirrors the
  established judgment in `onboard`, which deliberately never infers `decisions`
  because decision rationale would be fabricated.
- Alternatives Rejected: (a) stop at `spec.md` only — loses the structural
  anchor that best serves the anti-drift goal, and `design.md` already scales
  down to near-nothing for trivial code, so it costs little; (b) also fill in
  requirements intent — crosses the fabrication line and would pollute the
  "requirements = confirmed intent = truth" foundation.
- User Evidence: "选 B(spec + design,design 按复杂度伸缩)"
- Status: confirmed

### DEC-002 — All reverse-derived content is `inferred/open` until a human confirms it

- Decision: Everything `reverse-spec` produces is marked `inferred / open` and
  becomes authoritative **only** after explicit human confirmation.
- Reason: Derived content is inference, not confirmed user intent. This matches
  how `specify` already handles legacy artifacts (extract → mark `open` →
  require confirmation).
- User Evidence: "权威性处理:所有反推内容一律标 inferred / open,必须人工确认才升为权威"
- Status: confirmed

### DEC-003 — Reconciliation reports only; it never auto-fixes, and direction is decided by a human

- Decision: Reconciliation **reports drift and never modifies anything**. For
  each drift item the resolution direction is decided by the user.
- Reason: When code and a confirmed spec disagree, neither side can be presumed
  correct: the code may carry a bug (implementation deviated from correct
  design) **or** the spec may be stale (design evolved without being updated).
  The direction is genuinely undecidable by the tool. This is deliberately the
  **opposite** of `analyze`, whose auto-remediation is valid only because its
  fix direction is uniquely determined by the authority hierarchy.
- Status: confirmed

### DEC-004 — Reconciliation baseline is confirmed spec + design, never requirements

- Decision: The baseline that code is compared against is the target slice's
  **confirmed** `spec.md` + `design.md`. Code is **not** mechanically compared
  against `requirements.md`.
- Reason: Authority and reconcilability are two different axes running in
  opposite directions. The **authority axis** (requirements > spec > design >
  plan > tasks) governs *which artifact wins a conflict*. The **reconcilability
  axis** (design ≳ spec ≫ requirements) governs *which artifact can be compared
  to code line by line*. Reconciliation consumes the reconcilability axis.
  A requirement such as "the account must resist brute force" cannot mechanically
  adjudicate code: locking after 3 attempts, 5 attempts, or rate-limiting all
  "satisfy" it. Requirements deliberately withhold verifiable contracts; pinning
  contracts is the job of spec and design. The forward chain interposes spec and
  design between requirements and code precisely because requirements cannot
  attach to code directly.
- Corollary — where requirements' supreme authority *is* used: reconciliation has
  two steps. Step 1 (mechanical comparison, finding drift) uses spec/design.
  Step 2 (**deciding which side to change**) appeals to `requirements.md` intent.
  So: **spec/design for comparison, requirements for adjudication.**
- Corollary: `plan.md` / `tasks.md` are never baselines — they are build
  scaffolding, irrelevant to whether code conforms to its design.
- Status: confirmed

### DEC-005 — Mode is auto-detected; no confirmed baseline means no reconciliation

- Decision: Mode is selected by whether the target slice has a **confirmed**
  baseline. Absent → generate. Present → reconcile.
- Degradation: If artifacts exist but are still `Status: open` (unconfirmed),
  reconciliation MUST NOT run. Report clearly that the baseline is unconfirmed
  and that the user should confirm spec/design first.
- Reason: An unconfirmed draft is a mirror of the code; using it as a baseline
  compares the code with itself, yields zero drift by construction, and is
  meaningless. Human confirmation is precisely the act that injects intent and
  converts a description of *what is* into a specification of *what ought to be*.
- Lifecycle consequence: a brownfield project's first run is generate + confirm
  only; reconciliation becomes meaningful from the second run onward.
- Status: confirmed

### DEC-006 — Slice is the unit of work; each run seeds its own feature workspace

- Decision: The unit is a **slice** given by `[path]`. Each run produces its own
  `.codexspec/specs/<id>-<slice>/` workspace.
- Reason: Keeps every artifact independently readable, maintainable, and
  reconcilable, and matches the repository's existing one-feature-one-spec-directory
  model. This is the "pipeline extension" shape: each run seeds a workspace that
  the forward chain can then continue from for new work.
- Status: confirmed

### DEC-007 — Reuse `onboard`'s scanning discipline (DRY)

- Decision: Reuse the scanning discipline already established by `onboard`:
  high-signal-first, streaming and resumable, honoring `.gitignore` with a
  sensible fallback when there is no git.
- Reason: The scanning problem is identical; duplicating the discipline would
  create a second source of truth for it.
- Status: confirmed

### DEC-008 — Reconciliation output is a persistent `reconcile.md` plus a session briefing

- Decision: Reconciliation writes a persistent `reconcile.md` into the slice
  workspace, and additionally gives a short in-session briefing.
- Reason: Follows directly from DEC-003. `analyze` can report inline without
  persisting because it **auto-fixes**, so the repaired artifacts plus git
  history *are* the durable record. `reverse-spec` deliberately does not fix
  anything, so there is no repair to serve as the record — the report itself is
  the only deliverable and therefore must be persisted.
- Naming: `reconcile.md`. `drift.md` was rejected because "drift" presupposes the
  two sides were once aligned (untrue on a first brownfield reconciliation, where
  they may never have agreed), reads awkwardly when there are zero findings, and
  names only the negative half. `conflict.md` was rejected because it accurately
  describes only one of the three finding kinds (the other two are gaps, not
  contradictions), because "conflict" is already reserved vocabulary in this
  project (`status: conflict/needs-adjudication` in the profile store, and
  artifact conflicts in `analyze`), and because it implies two peer versions in
  contention rather than an asymmetric check of code against an authoritative
  contract. `conformance.md` was considered a viable alternative and not chosen.
- User Evidence: "使用\"reconcile.md\""
- Status: confirmed

### DEC-009 — Standalone invocation; seeds or reports, never chains

- Decision: `reverse-spec` is invoked directly (like `onboard` / `debug`). It
  seeds a workspace or emits a report; whether to continue into the forward
  chain and whether to change code are the user's decisions.
- Status: confirmed

### DEC-010 — `reconcile.md` structure and drift severity

- Decision: `reconcile.md` has this shape:

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

- Per-item fields:
  - `kind` — `undocumented-behavior` (code does it, spec omits it) |
    `unimplemented-spec` (spec states it, code lacks it) |
    `semantic-mismatch` (both present, meanings disagree).
  - `severity` — `Critical | Warning | Minor`, assessed from the **actual impact
    of that item** against confirmed intent, **not fixed per `kind`**. An
    undocumented behavior can be a security-grade finding (a hidden endpoint);
    a semantic mismatch can be trivial.
  - `location` — code `path:line` plus the corresponding spec/design reference.
  - `evidence` — the code observation and the spec/design text, side by side.
  - `direction` — `fix-code | update-spec | needs-your-judgment`, with reasoning;
    **suggestion only, never executed** (per DEC-003).
  - `status` — `open`, awaiting the user's adjudication.
- Explicit non-gate: `Status` and `severity` exist to help the user prioritize
  and MUST NOT act as a PASS/FAIL gate.
- Status: confirmed

### DEC-011 — Slice = directory/module path; a bare whole-repo run yields only a coarse map plus a slice list

- Decision:
  - A slice is **a directory / module / package path** (or a file set within
    one), bounded by `[path]`. No "intelligent auto-partitioning".
  - **Bare whole-repo run (no `[path]`)**: perform a high-signal architectural
    survey and write `.codexspec/specs/<id>-overview/` containing (a) a **thin,
    architecture-level `design.md`** (components, responsibilities, relationships;
    marked `inferred/open`, scaled to complexity) — the coarse map; and (b)
    `slices.md`, a candidate slice list (path + one-line description + rough size
    or priority) — the deepening plan.
  - The bare run produces **no `spec.md` and no `reconcile.md`**: it is a map and
    a TODO list, not a detailed specification.
- Reason: A single repository-wide detailed spec is unreadable and
  unmaintainable, directly contradicting the goal this feature serves.
- User Evidence: "以切片为单元、整库裸跑只给粗图+切片清单"
- Status: confirmed

### DEC-012 — "Confirmed baseline" means a file-level `Status: confirmed`, reusing the existing convention

- Decision:
  - Generated `spec.md` / `design.md` carry a **file-level** `Status: inferred/open`
    header, mark principal entries `[inferred]`, and state explicitly that they
    do not serve as a reconciliation baseline until confirmed. The
    `requirements.md` stub is likewise fully `open`.
  - Confirmation **reuses the convention already used by `requirements.md`**: the
    user flips the file-level `Status: open → confirmed` and appends a
    **Confirmation Log** entry. **No new command and no new mechanism.**
  - Reconcile mode accepts **only** `Status: confirmed` spec/design as a baseline
    (paired with the degradation in DEC-005).
- Status: confirmed

---

## Constraints (CON)

### CON-001 — Template governance / self-bootstrap

- Statement: As a distributed command, `reverse-spec` is authored **only** in
  `templates/commands/reverse-spec.md`. The forms under
  `.claude/commands/codexspec/` and `.agents/skills/codexspec-*/` are derived
  install artifacts, regenerated by `codexspec init`, and MUST NOT be hand-edited.
- Status: confirmed

### CON-002 — Lockstep updates required when adding a distributed command

- Statement: The following sites MUST be updated together (per profile record
  `Con-2026-0811-1418yq-1`):
  1. the `get_commands_metadata()` entry in `src/codexspec/commands/installer.py`,
     registered under the **enhanced** category (adjacent to `onboard`);
  2. that function's docstring **total** and **per-category** counts;
  3. the category's inline `# <Category> Commands (N)` comment (note the wording
     varies between categories);
  4. the command-count assertions in **both** `tests/commands/test_installer.py`
     (total and per-category `len(...)`) **and** `tests/test_cli.py` (the number
     in list-commands output);
  5. a row in **all 8** `README*.md` files, translated per language.
  6. Installer descriptions are zh-CN; keep them short to avoid ruff `E501`
     (120-column budget).
- Language family (per `Con-2026-0813-1143el-1`): `reverse-spec` is **not** in the
  commit-language family. Its Language Preference section MUST reference **both**
  `language.interaction` and `language.document`, MUST NOT use `language.commit`,
  and the command MUST NOT be added to the `commit_templates` set.
- Translation catalogs (per `Con-2026-0812-2114vj-1`): a brand-new command needs
  **no** entry in `templates/translations/*.json` (the catalog is a subset); it
  installs with English frontmatter, following the `debug` / `distill` / `onboard`
  precedent.
- Status: confirmed

### CON-003 — English template with a Language Preference section

- Statement: The command template is written in English and carries a
  `## Language Preference` section, consistent with every other command.
- Status: confirmed

### CON-004 — Read-only on code; writes only into the feature workspace

- Statement: `reverse-spec` is read-only with respect to the codebase and writes
  only into the feature workspace it creates. It MUST NOT modify source, tests,
  or git state; MUST NOT write to `.codexspec/profile/` (that is `onboard`'s
  channel); and MUST NOT automatically modify code or pre-existing artifacts.
- Status: confirmed

### CON-005 — The two constitutions stay separate

- Statement: This feature does not touch `_get_default_constitution()` and does
  not propagate project-governance rules into the shipped default constitution.
- Status: confirmed

### CON-007 — Reuse the workspace ID and directory convention without creating a git branch

- Statement: Slice workspaces reuse the project's existing
  `{YYYY-MMDD-HHMM}{rr}` timestamp-plus-random ID convention and the
  `.codexspec/specs/<id>-<slice>/` directory convention, but creating a workspace
  MUST NOT create or switch a git branch. Inventing a separate ID generator and
  introducing sequential numbering remain prohibited.
- Reason: `create-new-feature.sh` unconditionally runs `git checkout -b` when git
  is present, which contradicts CON-004's prohibition on modifying git state. The
  two confirmed constraints were in genuine conflict; the user adjudicated in
  favor of strict read-only behavior, because `reverse-spec` is an analysis tool a
  maintainer runs on their normal working branch — reconcile mode especially must
  be purely read-only — and because the nearest sibling command `onboard` creates
  no branch either.
- Supersedes: CON-006
- User Evidence: "不建分支,收窄 CON-006"
- Status: confirmed

### CON-006 — Create slice workspaces with the authoritative script and existing ID convention

- Status: superseded
- Replaced By: CON-007
- Historical Note: This entry mandated calling
  `.codexspec/scripts/create-new-feature.sh` outright. An isolated code review
  found that the script unconditionally creates and switches a git branch
  (`create-new-feature.sh:130`), putting this constraint in direct conflict with
  CON-004. CON-007 keeps the ID and directory conventions this entry protected
  while dropping the mandatory script invocation.
- Original Statement: Slice workspaces are created using the existing authoritative
  script `.codexspec/scripts/create-new-feature.sh` (`.ps1` on Windows) and its
  `{YYYY-MMDD-HHMM}{rr}` timestamp-plus-random ID convention. Do not invent a
  separate ID generator and do not introduce sequential numbering.
- Earlier historical note (retained): an earlier draft of this constraint assumed
  the script carried a sequential-ID bug. That premise was investigated and found
  **false**: the authoritative source `scripts/bash/create-new-feature.sh`
  generates correct timestamp+random IDs, and the flat copy users actually invoke
  is byte-identical to it. The file that emitted `2027` was an unreferenced dead
  copy under `.codexspec/scripts/bash/`, removed in commit `7fdfe17`. The
  constraint was rewritten from "avoid the bug" to "reuse the authoritative
  script and convention" — and has since been superseded entirely by CON-007.

---

## Out of Scope (OUT)

### OUT-001 — No automatic code changes and no automatic drift resolution

- Statement: The command never edits code and never resolves drift on its own; it
  reports only.
- Reason: The resolution direction is genuinely undecidable by the tool (DEC-003).
- Status: confirmed

### OUT-002 — Does not write cross-feature knowledge to the profile

- Statement: `reverse-spec` does not write to `.codexspec/profile/`.
- Reason: That is `onboard`'s channel; duplicating it would create two writers
  for one store.
- Status: confirmed

### OUT-003 — Does not fabricate requirements intent

- Statement: `requirements.md` remains a thin, fully `open` stub and is never
  presented as confident authority.
- Reason: Intent is not present in code (DEC-001).
- Status: confirmed

### OUT-004 — Does not mechanically compare code against requirements

- Statement: Comparison targets confirmed spec/design only.
- Reason: Requirements are not reconcilable against code (DEC-004).
- Status: confirmed

### OUT-005 — Does not emit a single repository-wide monolithic spec

- Statement: A bare whole-repo run yields a coarse map plus a slice list, never
  one giant detailed specification.
- Reason: Unreadable and unmaintainable (DEC-011).
- Status: confirmed

### OUT-006 — Does not participate in auto_next or auto_distill

- Statement: The template carries **no** `## Auto-Next Chain Advance` section, no
  automatic hook, and no `## Automatic Distillation` section. It is neither
  auto-triggered by an upstream stage nor auto-triggers a downstream one.
- Reason: It only seeds a workspace or produces a report; whether to continue
  into the forward chain or change code is the user's decision, consistent with
  DEC-003.
- Status: confirmed

### OUT-007 — diff / PR range as a slice source is excluded from this feature

- Statement: Slice input is **path-based only** (directory / module / package).
  A diff or pull-request changeset is not a supported slice input.
- Reason: "Reverse-derive a spec for one change" is a different workflow axis
  (change review) from brownfield cold-start and anti-drift; deferred to a later
  enhancement to avoid scope expansion.
- Status: confirmed

---

## Open Questions

None. All questions raised during discovery (`reconcile.md` structure and drift
severity; slice definition and whole-repo output; the confirmed-baseline
mechanism) were resolved during requirement discovery at the user's explicit
direction, and are recorded as DEC-010, DEC-011, and DEC-012 respectively.

- User Evidence: "OPEN-001..003都要在requirement阶段确认，不要等到design"

## Confirmation Log

### Session 2026-08-18 — positioning

- Summary Presented: three candidate positionings (generation-led, reconciliation-led,
  dual-mode), evaluated against process quality, understandability/maintainability,
  and prevention of implementation drift.
- User Confirmation: "认同"
- Entries Confirmed: NEED-001, NEED-002, NEED-003, DEC-003 (report-only, direction decided by a human)

### Session 2026-08-19 — output boundary and authority handling

- Summary Presented: output boundary options A (spec only) / B (spec + design) /
  C (including requirements intent), with the reverse-derivation fidelity argument.
- User Confirmation: "选 B(spec + design,design 按复杂度伸缩)。权威性处理:所有反推内容一律标 inferred / open,必须人工确认才升为权威"
- Entries Confirmed: DEC-001, DEC-002
- Follow-up discussion: the user asked whether code could be reconciled directly
  against `requirements.md`; resolved as DEC-004 (authority axis vs. reconcilability
  axis).

### Session 2026-08-19 — scale, output form, and naming

- Summary Presented: slice granularity options and reconciliation output form;
  then a comparison of `reconcile` / `drift` / `conformance` / `conflict` as names.
- User Confirmation: "以切片为单元、整库裸跑只给粗图+切片清单;对账产出一份持久文件,落成 reconcile.md 持久文件 + 会话简报" and "使用\"reconcile.md\""
- Entries Confirmed: NEED-004, DEC-006, DEC-007, DEC-008

### Session 2026-08-20 — resolving all open questions and final confirmation

- Summary Presented: full restatement of DEC-004, DEC-005, DEC-010, DEC-011,
  DEC-012, CON-002, the rewritten CON-006, OUT-006, and OUT-007.
- User Confirmation: "确认"
- Entries Confirmed: all entries in this document (NEED-001..005, DEC-001..012,
  CON-001..006, OUT-001..007). Discovery is complete with no blocking open questions.

### Session 2026-08-20 — CON-004 / CON-006 conflict adjudicated during implementation

- Summary Presented: an isolated code review found that CON-006's mandated script
  unconditionally runs `git checkout -b` (`create-new-feature.sh:130`),
  contradicting CON-004's prohibition on modifying git state. Both were confirmed
  entries and the script offers no way to create a workspace without the branch
  side effect, so the conflict required a user decision rather than an
  implementation choice.
- User Confirmation: "不建分支,收窄 CON-006"
- Entries Confirmed: CON-007, replacing CON-006 (now superseded). CON-004 and the
  read-only intent it protects stand unchanged.
