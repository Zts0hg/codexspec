# Feature Specification: blueprint and auto-dev

<!--
Language: document language = en (per .codexspec/config.yml).
Compiled from requirements.md (Feature ID 2026-0829-2159yg). Only confirmed entries are binding.
-->

**Feature Branch**: `2026-0829-2159yg-blueprint-auto-dev`
**Created**: 2026-08-30
**Status**: Draft
**Input**: Confirmed requirements record
`.codexspec/specs/2026-0829-2159yg-blueprint-auto-dev/requirements.md`

## Context and Goals

CodexSpec already supports autonomous development of one confirmed requirement through the
Requirements-First SDD stages. This feature adds two final agent command names, `blueprint` and
`auto-dev`, plus one read-only CLI command, `codexspec show-blueprint`.

`blueprint` prepares an ordered set of complete, confirmed requirements before implementation.
`auto-dev` consumes that ordered document one requirement at a time in one fixed branch and
worktree, while `blueprint` may continue appending future work. The shared document is
`.codexspec/blueprint.md` in the dedicated worktree. Automatic development remains resumable,
preserves feature-specific Git history, synchronizes the evolving default branch before each new
requirement, and can continue after completed work is integrated into the default branch.

The goals are:

1. Let users refine multiple mutually consistent requirements without starting development.
2. Continuously develop confirmed requirements in document order without normal user handoffs.
3. Make planning and development safe when they run concurrently against one physical blueprint.
4. Preserve recoverable SDD and Git state across interruption, failed verification, and repeated
   integration into the default branch.
5. Let developers inspect the shared blueprint directly from the CodexSpec CLI.

## User Scenarios and Testing

### User Story 1 - Build an ordered blueprint (Priority: P1)

A user invokes `blueprint`, discusses a requirement through the same requirements discovery and
explicit confirmation approach as `specify`, and appends the confirmed result as `pending`. The
discussion accounts for implemented features and every existing blueprint requirement. The user
may later replace, delete, or move pending requirements, while in-progress and completed entries
remain visible but read-only.

**Independent Test**: Start with implemented feature records and a blueprint containing completed
and pending blocks. Append a new requirement, edit and move a pending block, and attempt the same
operations on a completed block. Verify context was consulted, permitted changes persist in the
requested order, and the completed block is rejected unchanged.

**Acceptance Scenarios**:

1. **Given** existing implemented and planned functionality, **when** a new requirement is
   confirmed through `blueprint`, **then** one complete pending block is appended without creating
   a feature directory or starting SDD development.
2. **Given** a pending block, **when** the user replaces, deletes, or moves it, **then** the helper
   applies exactly that operation if the expected blueprint state is still current.
3. **Given** an `in_progress` or `completed` block, **when** `blueprint` attempts to edit, delete, or
   move it, **then** the helper rejects the operation and preserves the document.

### User Story 2 - Develop the blueprint autonomously (Priority: P1)

A user invokes `auto-dev`. It resumes existing in-progress work when present; otherwise it selects
the first pending block, creates its correctly named feature directory and `requirements.md`, and
runs specification, design, planning, task generation, implementation, testing, code review, and
review-driven repair without normal user decisions. After completion it re-reads the blueprint and
continues until no pending requirement remains.

**Independent Test**: Provide two pending requirements while `workflow.auto_next` is false. Invoke
`auto-dev` and verify both requirements independently pass every SDD gate in document order, use
separate feature directories, become completed, and require no global configuration change.

**Acceptance Scenarios**:

1. **Given** no in-progress requirement and two pending blocks, **when** `auto-dev` runs, **then** it
   completes the first block before starting the second and ends only after a fresh read finds no
   pending block.
2. **Given** `workflow.auto_next: false`, **when** `auto-dev` runs, **then** its invocation still
   advances all required stages without reading or modifying that setting.
3. **Given** a product-neutral implementation detail absent from requirements, **when** development
   reaches that detail, **then** `auto-dev` selects an established engineering practice and
   continues without asking the user.

### User Story 3 - Plan while auto-dev is running (Priority: P1)

While one `auto-dev` process develops the current feature, one or more `blueprint` invocations may
append or revise pending work in the same dedicated worktree. Each document mutation is validated
against the latest content and each Git mutation is serialized, so neither workflow overwrites the
other.

**Independent Test**: Pause `auto-dev` between feature commits, concurrently apply blueprint
operations using the same initial hash, and verify one operation applies while stale operations
report conflict. Resume development and verify newly appended requirements join the same run in
their current document order.

**Acceptance Scenarios**:

1. **Given** two operations based on the same blueprint hash, **when** one persists first, **then**
   the other reports `conflict` instead of overwriting it.
2. **Given** a requirement appended while another requirement is in progress, **when** the current
   feature completes, **then** `auto-dev` re-reads the document and eventually processes the newly
   appended pending block in document order.
3. **Given** one active `auto-dev`, **when** another `auto-dev` starts for the same repository,
   **then** the second invocation reports the active run and exits immediately while `blueprint`
   remains usable.

### User Story 4 - Resume unfinished automatic development (Priority: P1)

If the process is interrupted or an SDD stage cannot pass its existing progress guards, the
current requirement remains `in_progress` with its feature directory and evidence intact. The next
`auto-dev` invocation inspects existing artifacts and resumes the first unfinished or no-longer-
passing stage before considering pending work.

**Independent Test**: Interrupt a run after creating intermediate SDD artifacts and again after an
unsuccessful review. Reinvoke `auto-dev` and verify it reuses the same directory, preserves status,
resumes from current evidence, and does not start a later pending requirement first.

**Acceptance Scenarios**:

1. **Given** an `in_progress` requirement with existing artifacts, **when** `auto-dev` starts,
   **then** it resumes that directory without resetting the requirement or creating another one.
2. **Given** autonomous repairs reach an existing no-progress or retry stop condition, **when** the
   run ends, **then** the requirement remains `in_progress`, later pending work is untouched, and
   the exact evidence needed for a later retry remains available.
3. **Given** an unexpected process exit, **when** a later invocation starts, **then** the prior run
   lock no longer prevents recovery.

### User Story 5 - Continue after default-branch integration (Priority: P2)

Developers or their general-purpose agents may integrate the fixed branch at any selected committed
point. `auto-dev` keeps the same branch and worktree, synchronizes locally available default-branch
history before each later requirement, and preserves a later PR or MR file diff that contains only
code not already in the target branch.

**Independent Test**: Integrate one completed requirement using merge, squash, rebase, and
cherry-pick variants. Merge the resulting default branch back into the fixed branch, develop
another requirement, and verify the next file diff excludes the previously integrated code even
when the commit list still includes old fixed-branch commits.

**Acceptance Scenarios**:

1. **Given** a configured remote whose fetch fails, **when** a pending requirement is about to
   start, **then** development continues using locally available refs and fetch is attempted again
   before the next requirement.
2. **Given** a synchronization merge conflict, **when** `auto-dev` can resolve it and restore the
   required passing baseline, **then** development continues; otherwise the merge is aborted, the
   next requirement remains pending, and the run stops.
3. **Given** earlier work entered the target through squash, rebase, or cherry-pick, **when** the
   latest target history is merged into the fixed branch, **then** a later file diff excludes that
   code although the commits view may retain earlier hashes.

### User Story 6 - Inspect the current blueprint from the CLI (Priority: P2)

A developer runs `codexspec show-blueprint` from any directory inside the current Git project. The
command finds the fixed worktree and prints its current `.codexspec/blueprint.md` exactly, without
creating, fetching, locking, or modifying project state.

**Independent Test**: Run the command from a nested directory with a valid shared blueprint and
compare standard output with the file. Then independently remove or mismatch each prerequisite and
verify a specific diagnostic on standard error and a non-zero exit status.

**Acceptance Scenarios**:

1. **Given** the expected repository, branch, worktree, and blueprint, **when** the CLI runs,
   **then** standard output is the complete current file content and the exit status is zero.
2. **Given** the current directory is not in a Git repository, or the expected branch, worktree, or
   file is absent or mismatched, **when** the CLI runs, **then** it emits the specific failed check
   on standard error and exits non-zero without changing anything.
3. **Given** a concurrent atomic blueprint replacement, **when** the lock-free CLI reads, **then**
   it observes either the complete prior file or the complete replacement, never partial content.

### Edge Cases

- The blueprint is empty: `auto-dev` exits successfully after a fresh read finds no pending work.
- A pending block changes after an agent reads it: its hash-guarded mutation reports `conflict` and
  the agent must re-read before constructing another request.
- A request is malformed or has an unsupported protocol version: it returns `invalid_request`
  without beginning blueprint processing.
- A structurally valid operation targets a protected status or mismatched directory: it returns
  `rejected` without modifying the blueprint.
- A pending requirement is renamed before development: its Feature ID remains stable and its final
  directory uses the current normalized feature name.
- The main checkout has uncommitted changes: fixed-worktree creation and synchronization ignore
  those changes and use committed refs only.
- No remote is configured: local default-branch history is sufficient. A configured but unavailable
  remote does not stop development.
- A fetch fails repeatedly in one run: each later requirement still makes its own fetch attempt.
- A previous integration included only some fixed-branch requirements: a direct later PR or MR
  includes every remaining target-branch file difference, not only the newest feature.
- An unsuccessful review reports `BLOCKED`, `FAIL`, or `INCONCLUSIVE`: that result remains in stage
  evidence while blueprint `Development Status` remains `in_progress`.

## Requirements

### Functional Requirements

- **REQ-001**: The final agent command names MUST be `blueprint` and `auto-dev`. `blueprint` MUST
  use the same interactive discovery and explicit confirmation approach as `specify`, append the
  result as a pending requirements block, and MUST NOT create a feature directory or start
  development.
  - Sources: NEED-002, CON-001, DEC-017
- **REQ-002**: During discovery, `blueprint` MUST consider relevant implemented features under
  `.codexspec/specs/` and every existing blueprint block. Blueprint document order MUST be
  implementation order; users MAY replace, delete, or reorder only pending blocks, and
  `in_progress` or `completed` blocks MUST remain visible and immutable.
  - Sources: NEED-002, CON-002, DEC-003
- **REQ-003**: Both agent commands MUST resolve the repository's one fixed local branch
  `codexspec/auto-dev`, its external worktree with basename
  `worktree-for-codexspec-auto-dev`, and that worktree's `.codexspec/blueprint.md`, regardless of
  the invoking checkout. They MUST NOT use a caller-checkout blueprint copy or per-feature
  branch/worktree.
  - Sources: NEED-003, DEC-004, DEC-014, DEC-016
- **REQ-004**: The blueprint MUST contain only confirmed requirements blocks separated by an
  independent `---` line. After trimming, every block MUST begin with `Feature ID`, `Development
  Status`, and `Feature Directory` in that order; every remaining line MUST be treated as the
  requirements content and be directly writable as `requirements.md` after trimming. A standalone
  `---` MUST NOT occur inside a block, and no free-form inter-block content is permitted. The helper
  MUST normalize supported line endings before applying these parsing rules and MUST NOT require or
  interpret a requirements title, heading, section name, or other content keyword. The `blueprint`
  agent, rather than the parser, MUST ensure confirmed content follows `specify`'s complete
  requirements document organization before persistence.
  - Sources: DEC-001, DEC-012
- **REQ-005**: Each appended block MUST receive one permanent Feature ID generated by the helper.
  The blueprint prefix and embedded requirements content MUST contain the same ID. Pending blocks
  MUST use status `pending` and directory `not-created`. At development start the directory MUST be
  `.codexspec/specs/<feature-id>-<feature-name>/`; the ID remains unchanged across pending edits,
  renames, and moves.
  - Sources: CON-006, DEC-001, DEC-005, DEC-008, DEC-012
- **REQ-006**: Every agent-to-helper request MUST be a strictly validated versioned JSON object with
  `protocol_version`, `operation`, `expected_blueprint_hash`, and an operation-specific `payload`.
  Existing-block operations MUST also carry top-level `feature_id`; `append_requirement` MUST omit
  it. The helper MUST resolve the fixed blueprint itself and MUST NOT accept an arbitrary path,
  whole-document replacement, unrestricted patch, missing fields, extra fields, or invalid field
  combinations.
  - Sources: DEC-007
- **REQ-007**: `append_requirement` payload MUST contain exactly `feature_name` and
  `requirements_markdown`. The agent Markdown MUST omit helper-managed fields. Under exclusive
  modification access, the helper MUST generate and insert both Feature ID occurrences, initialize
  status and directory, add the separator as needed, persist the complete document atomically, and
  return the generated ID.
  - Sources: CON-003, CON-008, DEC-007, DEC-008, DEC-012
- **REQ-008**: Pending-document operations MUST have these exact payload forms:
  `replace_pending_requirement` contains exactly `feature_name` and `requirements_markdown` while
  preserving ID, pending status, and `not-created` and rejecting helper-managed metadata inside the
  Markdown; `delete_pending_requirement` contains an empty object; and
  `move_pending_requirement` contains exactly `{"position": "first_pending"}`,
  `{"position": "last_pending"}`, or `position` set to `before`/`after` plus the required
  `reference_feature_id`. A reference MUST be absent for first/last and present for before/after.
  Moved and referenced blocks MUST both be pending.
  - Sources: CON-002, DEC-007, DEC-009
- **REQ-009**: Status changes MUST use `update_status`. `pending` to `in_progress` requires
  `expected_status`, `new_status`, and the exact complete feature directory. `in_progress` to
  `completed` requires only both statuses and preserves the directory. Every other transition,
  stale expected state, mismatched path, extra field, or conditionally missing field MUST fail.
  - Sources: DEC-001, DEC-010
- **REQ-010**: Helper responses MUST classify requests in this order: malformed or schema-invalid
  input as `invalid_request`; stale hash or expected state as `conflict`; structurally valid but
  forbidden behavior as `rejected`; and a persisted operation as `applied`. Applied responses MUST
  include version, result, operation, feature ID, previous and current hashes, and operation data.
  Conflict and rejected responses MUST include version, result, operation, feature ID, current hash,
  and error. Invalid-request responses MUST include only version, result, and error at top level.
  Every error MUST have `code`, `message`, and an object `details`; `details` MUST be `{}` when no
  additional information exists and MUST never be null. A successful delete MUST return an empty
  operation `data` object.
  - Sources: DEC-011
- **REQ-011**: Every blueprint read-state-and-modify operation MUST acquire the same short-lived
  exclusive modification lock, then re-read and revalidate before writing. Helper persistence MUST
  use atomic file replacement. A successfully applied mutation MUST become a blueprint-only commit
  containing only `.codexspec/blueprint.md`.
  - Sources: CON-003, CON-005, CON-008, DEC-013
- **REQ-012**: `auto-dev` MUST first resume an existing `in_progress` block when present. It MUST
  reuse the recorded directory, inspect existing SDD artifacts, code, and verification evidence,
  and continue from the first unfinished or no-longer-passing stage without reverting to pending or
  creating another directory. Only after completion may it select pending work.
  - Sources: NEED-007, CON-004
- **REQ-013**: With no in-progress work, `auto-dev` MUST select the first pending block, remove its
  three blueprint-managed lines, write the remaining confirmed content directly to a newly created
  correctly named `requirements.md`, transition the block to `in_progress`, and execute the
  existing Requirements-First SDD sequence and pass gates through specification, design, plan,
  tasks, implementation, tests, code review, and review-driven repair.
  It MUST transition the block from `in_progress` to `completed` only after every required pass gate
  succeeds.
  - Sources: NEED-001, NEED-006, CON-006, DEC-010, DEC-012
- **REQ-014**: Invoking `auto-dev` MUST itself enable automatic stage advancement and MUST NOT read,
  modify, enable, disable, depend on, or duplicate `workflow.auto_next`. Ordinary direct SDD
  commands MUST retain their existing configuration behavior.
  - Sources: DEC-015
- **REQ-015**: `auto-dev` MUST make non-product implementation choices autonomously by tracing from
  task to plan, design, specification, and requirements without contradicting higher-level intent,
  then applying established engineering practice when requirements are silent. It MUST NOT perform
  interactive requirements discovery or request normal user decisions.
  - Sources: NEED-001, CON-001, DEC-002, OUT-001
- **REQ-016**: A non-passing SDD stage MUST trigger autonomous revision, repair, and re-check under
  existing progress and retry rules. When an existing stop condition is reached, `auto-dev` MUST
  stop, preserve the current `in_progress` status, directory, artifacts, code, and evidence, and
  MUST NOT start later pending work. Stage results such as `BLOCKED`, `FAIL`, or `INCONCLUSIVE`
  MUST NOT become blueprint statuses.
  - Sources: NEED-008, DEC-001, OUT-004
- **REQ-017**: After completing a requirement, `auto-dev` MUST re-read the shared blueprint and
  process the first currently pending block. Requirements appended during the run MUST join the
  same run in current document order. The run MUST end successfully only when a fresh read finds no
  pending requirement.
  - Sources: NEED-004, CON-004, DEC-003
- **REQ-018**: Only one `auto-dev` process MAY run per repository. It MUST hold one process-bound
  exclusive run lock for the complete invocation; a second invocation MUST report the active run
  and exit immediately. The lock MUST release on normal or unexpected process exit and MUST NOT
  prevent concurrent `blueprint` work.
  - Sources: CON-007
- **REQ-019**: Git staging, committing, merging, and other shared-worktree Git mutations MUST be
  serialized. Feature commits MUST stage only intended paths and every feature-specific commit
  created by `auto-dev` MUST use Conventional Commits with the exact Feature ID as scope. Multiple
  commits MUST remain in Git order without squash or a duplicate hash list; blueprint-only commits
  MUST not use a feature ID scope.
  - Sources: CON-005, DEC-013
- **REQ-020**: On first setup, the commands MUST identify the default branch, attempt a configured
  remote fetch, compare locally available local and remote-tracking commits by ancestry rather than
  time, initialize from the descendant when one contains the other, or merge both committed
  histories when they diverge. They MUST create or reuse fixed branch `codexspec/auto-dev` and the
  repository-specific external worktree basename `worktree-for-codexspec-auto-dev`, excluding
  uncommitted caller-checkout changes and never rebasing fixed history.
  - Sources: DEC-014
- **REQ-021**: Before every new pending requirement, `auto-dev` MUST attempt to fetch a configured
  remote and merge locally available new local and remote-tracking default-branch history into the
  fixed branch. A fetch failure MUST not stop development or suppress later per-requirement fetch
  attempts. Merge conflicts MUST be resolved autonomously and required checks rerun; if resolution
  or a passing baseline cannot be restored, `auto-dev` MUST abort that merge, stop, and leave the
  next requirement pending.
  - Sources: DEC-014
- **REQ-022**: A developer or general-purpose agent MAY integrate the fixed branch at any selected
  committed point. `auto-dev` MUST continue on the same branch and worktree and merge later target
  history back at the next synchronization point. After synchronization, later PR or MR file
  changes MUST exclude code already present in the target, while earlier fixed-branch commits MAY
  remain listed after squash, rebase, or cherry-pick. A direct fixed-branch comparison MUST include
  all remaining target-branch differences when only some requirements were integrated.
  - Sources: NEED-009, DEC-014, DEC-018, OUT-003
- **REQ-023**: `codexspec show-blueprint` MUST discover the current Git repository, validate fixed
  branch `codexspec/auto-dev`, validate that `worktree-for-codexspec-auto-dev` exists on that branch,
  and validate its `.codexspec/blueprint.md`. On success it MUST write the complete current file
  directly to standard output with a zero status. Each failed check MUST produce a specific
  standard-error diagnostic and non-zero status.
  - Sources: NEED-010
- **REQ-024**: `codexspec show-blueprint` MUST be read-only and lock-free. It MUST NOT create or
  modify branches, worktrees, or files; fetch or merge history; acquire the blueprint modification
  lock; or acquire a read lock. Concurrent safety MUST rely on helper-side atomic replacement, so
  the command observes one complete snapshot.
  - Sources: CON-008

### Non-Functional Requirements

- **NFR-001**: Concurrent blueprint operations and Git operations MUST be deterministic and must
  not lose an applied update, combine a feature commit with blueprint-only changes, or expose a
  partially written blueprint.
  - Sources: CON-003, CON-005, CON-008
- **NFR-002**: Requirement identity, feature directory naming, helper response classification, and
  commit scope MUST remain machine-verifiable without interpreting mutable titles or prose.
  - Sources: CON-006, DEC-005, DEC-007, DEC-010, DEC-011, DEC-013
- **NFR-003**: Automatic development MUST never report a requirement completed unless every reused
  SDD pass condition, required test, and final code review gate has passed.
  - Sources: NEED-001, NEED-008, DEC-015
- **NFR-004**: `codexspec show-blueprint` standard output MUST remain suitable for shell redirection
  and pipelines by containing the blueprint content rather than status decoration; diagnostics
  belong on standard error.
  - Sources: NEED-010, CON-008

### Key Entities

- **Blueprint document**: The single `.codexspec/blueprint.md` in the dedicated worktree, composed
  only of ordered confirmed requirements blocks.
- **Blueprint requirements block**: Three helper-managed prefix fields plus one complete embedded
  `specify` requirements document. Its permanent Feature ID is duplicated and equal in both parts.
- **Feature workspace**: `.codexspec/specs/<feature-id>-<feature-name>/`, created only when its
  blueprint block begins development and containing that feature's independent SDD artifacts.
- **Blueprint operation request**: The versioned, hash-guarded, operation-specific JSON object sent
  by an agent to the helper.
- **Blueprint operation response**: One strictly shaped `applied`, `conflict`, `rejected`, or
  `invalid_request` JSON result.
- **Dedicated development workspace**: Fixed local branch `codexspec/auto-dev` plus the external
  worktree whose basename is `worktree-for-codexspec-auto-dev`.
- **Development Status**: Exactly `pending`, `in_progress`, or `completed`; stage-level failure
  verdicts are not additional values.

## Success Criteria

- **SC-001**: A confirmed `blueprint` interaction appends exactly one parseable pending block while
  creating no feature directory and starting no SDD stage.
- **SC-002**: Under concurrent mutations based on the same starting hash, exactly one incompatible
  update can apply; stale updates report conflict and no accepted document content is lost.
- **SC-003**: Given multiple pending blocks and passing project checks, one `auto-dev` invocation
  completes every block in document order, including blocks appended before its final fresh read.
- **SC-004**: After interruption at any SDD stage, the next invocation reuses the same Feature ID
  and directory and does not repeat a previously passing stage unless current evidence invalidates
  it.
- **SC-005**: No blueprint produced or accepted by the helper contains an invalid status, duplicate
  or mismatched embedded Feature ID, malformed separator layout, or partial file content.
- **SC-006**: After prior work is merged to the default branch and synchronized back, the next PR or
  MR file diff contains zero lines attributable only to code already present in that target branch.
- **SC-007**: `codexspec show-blueprint` emits byte-equivalent complete blueprint content on standard
  output for a valid project and performs no filesystem or Git mutation.
- **SC-008**: Every feature-specific auto-dev commit is selectable by its exact Feature ID scope,
  while every blueprint-only commit changes only `.codexspec/blueprint.md`.

## Expected Error Behavior

- Schema or JSON errors return `invalid_request` before blueprint processing and omit operation,
  feature ID, and blueprint hash from the response top level.
- Stale blueprint hash or expected status returns `conflict` with the current hash so the agent can
  re-read and retry.
- Protected-status edits, invalid move references, unsupported status transitions, and mismatched
  feature directories return `rejected` without changing the document.
- A second `auto-dev` exits immediately with an already-running diagnostic; it does not wait or
  share feature development.
- Unavailable remote fetch is reported but is non-blocking. Unresolvable synchronization or a
  non-passing baseline aborts the merge and stops before a pending requirement starts.
- Persistent SDD failure stops with preserved `in_progress` state and evidence; it does not skip to
  later work or introduce a new blueprint status.
- `show-blueprint` reports the first failed repository/branch/worktree/file validation on standard
  error and exits non-zero without attempting repair or initialization.

## Confirmed Constraints and Decisions

- Blueprint order is the only implementation order; there is no priority or dependency scheduler.
- All user-owned product decisions are resolved during blueprint discovery.
- Planning and automatic development share one physical blueprint and may run concurrently.
- Pending requirements are mutable; in-progress and completed requirements are read-only.
- One fixed branch and worktree preserve continuous development history across all requirements.
- Synchronization uses merge, never rebase, and happens before every new pending requirement.
- Helper mutation schemas and response classes are strict and versioned.
- The three blueprint statuses are exhaustive.
- File differences, not a clean commit list, define correctness after repeated integration.
- `show-blueprint` is a read-only display command and has no read lock.

## Out of Scope

- Interactive requirements discovery or user confirmation during `auto-dev`. (OUT-001)
- Priority-based scheduling or automatic dependency reordering. (OUT-002)
- A dedicated command, mode, or prescribed workflow for delivery-branch creation, commit analysis,
  or cherry-picking. General-purpose agents may perform those operations. (OUT-003)
- Additional blueprint statuses for failed, blocked, paused, or retrying work. (OUT-004)

## Assumptions

*None.*

## Dependencies

- Existing CodexSpec Requirements-First SDD commands, their review loops, progress guards, and pass
  conditions.
- Existing Feature ID and normalized feature-name conventions.
- Git branch, worktree, merge, and remote-tracking behavior.
- CodexSpec's source-template distribution and CLI registration mechanisms.

## Open Questions

*None.*

## Requirements Traceability

| Confirmed Requirement | Spec Coverage | Notes |
|-----------------------|---------------|-------|
| NEED-001 | REQ-013, REQ-015, NFR-003 | Autonomous SDD development |
| NEED-002 | REQ-001, REQ-002 | Contextual blueprint discovery |
| NEED-003 | REQ-003 | Shared location from any checkout |
| NEED-004 | REQ-017 | Fresh read and live queue |
| NEED-006 | REQ-013 | Repeated Requirements-First SDD chain |
| NEED-007 | REQ-012, SC-004 | Interrupted-run recovery |
| NEED-008 | REQ-016, NFR-003 | Unsuccessful run preservation |
| NEED-009 | REQ-022, SC-006 | Repeated default-branch integration |
| NEED-010 | REQ-023, NFR-004, SC-007 | Read-only CLI display |
| CON-001 | REQ-001, REQ-015 | Blueprint is the user decision boundary |
| CON-002 | REQ-002, REQ-008 | Status-based mutation rules |
| CON-003 | REQ-007, REQ-011, NFR-001 | Serialized document mutation |
| CON-004 | REQ-012, REQ-017 | One requirement at a time |
| CON-005 | REQ-011, REQ-019, NFR-001 | Serialized Git writes |
| CON-006 | REQ-005, REQ-013, NFR-002 | Complete feature directory name |
| CON-007 | REQ-018 | Single auto-dev process |
| CON-008 | REQ-007, REQ-011, REQ-024, NFR-001, NFR-004 | Atomic writes and lock-free CLI |
| DEC-001 | REQ-004, REQ-005, REQ-009, REQ-016 | Three statuses and directory field |
| DEC-002 | REQ-015 | Autonomous implementation choices |
| DEC-003 | REQ-002, REQ-017 | Document order is implementation order |
| DEC-004 | REQ-003 | Fixed shared branch and worktree |
| DEC-005 | REQ-005, NFR-002 | Permanent Feature ID |
| DEC-007 | REQ-006, REQ-007, REQ-008, NFR-002 | Versioned operation contract |
| DEC-008 | REQ-005, REQ-007 | Agent/helper field ownership |
| DEC-009 | REQ-008 | Pending operation payloads |
| DEC-010 | REQ-009, NFR-002 | Status transition payloads |
| DEC-011 | REQ-010, NFR-002 | Response classification |
| DEC-012 | REQ-004, REQ-005, REQ-007, REQ-013 | Blueprint block format and extraction |
| DEC-013 | REQ-011, REQ-019, SC-008 | Git commit identity |
| DEC-014 | REQ-003, REQ-020, REQ-021, REQ-022 | Fixed workspace and synchronization |
| DEC-015 | REQ-014, NFR-003 | Run-local automatic advancement |
| DEC-016 | REQ-003 | Blueprint path |
| DEC-017 | REQ-001 | Final agent command names |
| DEC-018 | REQ-022, SC-006 | File-diff-based repeated integration |
| OUT-001 | REQ-015, Out of Scope | No auto-dev discovery |
| OUT-002 | REQ-002, Out of Scope | No automatic scheduler |
| OUT-003 | REQ-022, Out of Scope | No delivery-branch command |
| OUT-004 | REQ-016, Out of Scope | No additional blueprint status |
