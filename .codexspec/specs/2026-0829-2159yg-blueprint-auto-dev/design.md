# Design Document: blueprint and auto-dev

<!--
Language: document language en (.codexspec/config.yml).
This document defines architecture, components, interfaces, and design decisions.
-->

**Related Spec**: `.codexspec/specs/2026-0829-2159yg-blueprint-auto-dev/spec.md`
**Confirmed Requirements**:
`.codexspec/specs/2026-0829-2159yg-blueprint-auto-dev/requirements.md`
**Created**: 2026-08-30
**Status**: Draft

## Context

CodexSpec agent commands are distributed English Markdown templates installed as Claude slash
commands and Codex skills. Deterministic CLI behavior lives in the Python package, currently
registered through the root Typer application. This feature spans both surfaces:

- `blueprint` and `auto-dev` remain agent commands because they require requirements discussion,
  project interpretation, SDD artifact generation, repair, and code review.
- Repository discovery, worktree lifecycle, blueprint parsing, strict JSON validation, atomic
  persistence, lock ownership, and `show-blueprint` are Python responsibilities because their
  correctness cannot depend on free-form agent edits.

All new runtime Python remains inside `src/codexspec/`, which is already shipped in the wheel. New
distributed command source remains in `templates/commands/`; derived `.claude/commands/` and
`.agents/skills/` forms are regenerated through `codexspec init`, never edited directly. No new
top-level package path or runtime dependency is required.

## Architecture and Components

### C1. Repository and dedicated-worktree locator

- **Responsibility**: Resolve the caller's Git repository, its common Git directory, primary
  worktree, default branch, configured remote/default-tracking ref, fixed branch
  `codexspec/auto-dev`, repository-specific external worktree directory, and fixed blueprint path.
  Provide separate read-only `locate` and mutating `ensure` modes.
- **Interface**:
  - `locate_repository(cwd) -> RepositoryContext`
  - `locate_dedicated_workspace(context) -> WorkspaceContext | typed error`
  - `ensure_dedicated_workspace(context) -> WorkspaceContext | synchronization result`
  - Git calls use `git -C <target>` with repository-local environment variables removed.
- **Behavior**: Parse `git worktree list --porcelain` rather than assuming that a directory with the
  expected basename is registered correctly. `locate` never creates, fetches, or repairs. `ensure`
  creates missing state according to ancestry, rejects a registered path/branch mismatch, and
  excludes caller worktree changes by operating only on committed refs.
- **Covers**: REQ-003, REQ-020, REQ-023, REQ-024

### C2. Blueprint document model and parser

- **Responsibility**: Parse, validate, and serialize the complete blueprint as an ordered list of
  immutable value objects. Enforce the three-line prefix, separator placement, matching duplicated
  Feature IDs, exact status set, directory/status relationship, feature-name normalization, and
  reserved-line rules.
- **Interface**:
  - `BlueprintDocument.parse(bytes) -> BlueprintDocument`
  - `BlueprintDocument.serialize() -> bytes`
  - `BlueprintDocument.sha256(bytes) -> "sha256:<hex>"`
  - lookup only by permanent Feature ID; positions are calculated after parsing.
- **Behavior**: Accept supported CRLF/LF input, normalize model content to LF, and serialize one
  canonical terminal newline. Hash comparison uses the exact bytes read before normalization so any
  concurrent physical change is detectable; responses return the exact new serialized-byte hash.
- **Covers**: REQ-004, REQ-005, NFR-002

### C3. Strict blueprint operation protocol

- **Responsibility**: Decode one JSON request into one exact operation variant, validate allowed
  keys and cross-field relationships, apply a legal domain transition, and encode exactly one
  response variant.
- **Interface**: `apply_operation(request_bytes, current_bytes) -> OperationOutcome` where request
  variants are append, replace pending, delete pending, move pending, and update status. Response
  variants are applied, conflict, rejected, and invalid request.
- **Validation order**: JSON/schema/version, then expected hash/status, then blueprint business
  rules, then persistence. Unknown keys and nullable substitutes are rejected at schema validation;
  impossible relationships are validated in both directions.
- **Covers**: REQ-006, REQ-007, REQ-008, REQ-009, REQ-010, NFR-002

### C4. Blueprint mutation and commit transaction

- **Responsibility**: Turn one valid operation into one durable blueprint-only Git commit without
  exposing partial content or mixing unrelated staged/worktree changes.
- **Interface**: `BlueprintStore.apply_and_commit(request, repository) -> response JSON`.
- **Transaction boundary**:
  1. Acquire the repository Git-write lock, then the blueprint-modification lock in that global
     order.
  2. Recover or reject any incomplete prior blueprint transaction.
  3. Re-read bytes, validate hash/state, compute canonical replacement, and write a small recovery
     record under the common Git directory.
  4. Write a same-directory temporary file, flush it, and atomically replace the blueprint.
  5. Commit only `.codexspec/blueprint.md` with a non-feature blueprint scope while preserving all
     unrelated staged and unstaged content.
  6. Clear the recovery record and return `applied` only after both file and commit succeed.
- **Recovery**: The record stores old/new hashes, operation identity, and pre-operation HEAD. A later
  helper call can finish a known replacement, restore the prior bytes when no commit occurred, or
  stop on an unrelated mismatch. An internal exception writes diagnostics to stderr and exits
  non-zero rather than falsely returning one of the four domain outcomes.
- **Covers**: REQ-007, REQ-011, REQ-019, NFR-001

### C5. Internal blueprint helper CLI

- **Responsibility**: Give both agent templates one deterministic tool without accepting a caller-
  supplied blueprint path.
- **Interface**: A hidden Typer command with two actions:
  - `inspect`: optionally ensure the dedicated workspace, then emit machine JSON containing the
    workspace path, blueprint existence, exact current hash, and complete content. This read is
    lock-free because C4 replaces atomically.
  - `apply`: read exactly one versioned operation request from stdin and emit exactly one versioned
    domain response to stdout; transport/internal failures use stderr plus non-zero exit.
- **Covers**: REQ-003, REQ-006, REQ-010, REQ-011

### C6. `templates/commands/blueprint.md`

- **Responsibility**: Orchestrate user-facing requirements discovery and pending blueprint
  maintenance. Read the project constitution/profile, inspect relevant implemented SDD artifacts
  and every blueprint block, follow `specify`'s one-question and explicit-confirmation discipline,
  then call C5 with exact JSON instead of editing the file directly.
- **Interface**: Natural-language command arguments may request a new requirement or identify
  pending work to replace, delete, or move. The command retains the inspected hash, handles
  conflict by re-inspecting and re-evaluating user intent, reports rejected/invalid requests, and
  never calls status update.
- **Covers**: REQ-001, REQ-002, REQ-006, REQ-007, REQ-008, REQ-010, REQ-011

### C7. Auto-dev run ownership coordinator

- **Responsibility**: Ensure one active automatic-development owner while allowing blueprint-only
  operations. Agent commands have no stable cross-platform host process of their own, so ownership
  is represented by a random run token plus a renewable activity record protected by a short OS
  lock in the common Git directory.
- **Interface**: Hidden helper actions `acquire`, `renew`, `release`, and `assert-owner`; all later
  auto-dev-specific helper calls require the token.
- **Behavior**: Normal completion releases ownership explicitly. Every stage and write renews and
  verifies ownership. A later invocation automatically reclaims an owner record that has ceased
  activity; fencing tokens make every call from the previous owner fail after reclamation. This
  provides automatic crash recovery without user deletion of a static lock file. The command must
  verify ownership immediately before every repository mutation.
- **Covers**: REQ-012, REQ-018, NFR-001

### C8. Git write and default-branch synchronization coordinator

- **Responsibility**: Serialize shared-worktree Git writes, synchronize committed default-branch
  refs, expose conflicts for autonomous repair, and create path-limited feature commits.
- **Interface**: Hidden token-validated actions:
  - `sync-default`: attempt fetch; compute local/remote ancestry; merge available history with
    `--no-rebase`; return clean, needs-resolution, or failed evidence.
  - `prepare-sync-verification`: require the exact complete conflict-path list, reject unresolved
    content, and stage only those literal paths as the project-check candidate.
  - `continue-sync` / `abort-sync`: finish a passing resolved merge or abort it.
  - `commit-feature`: validate a Conventional Commit whose exact scope is the Feature ID and commit
    only the supplied paths, rejecting the blueprint path.
- **Behavior**: All Git subprocesses are routed through one environment-sanitizing runner. A fetch
  error is reported as a warning while locally available refs continue. A merge-in-progress record
  prevents blueprint commits and other Git writers until the owning auto-dev resolves or aborts it;
  a concurrent blueprint command waits and retries its confirmed intent after that short ownership
  ends. The fixed branch is never rebased or reconstructed.
- **Covers**: REQ-019, REQ-020, REQ-021, REQ-022, NFR-001

### C9. `templates/commands/auto-dev.md`

- **Responsibility**: Own the continuous SDD control loop. Acquire C7 ownership, ensure C1, resume
  in-progress work first, otherwise synchronize through C8 before claiming the first pending block,
  create/reuse the exact feature workspace, and invoke each existing SDD stage under auto-dev
  delegation until every pass gate succeeds or an existing stop guard is reached.
- **Stage state resolution**: Inspect current artifacts and their review outputs rather than relying
  on an extra blueprint stage field. A missing or stale downstream artifact selects the earliest
  stage requiring work. `requirements.md` is created from the selected block; subsequent artifacts
  are owned by existing commands.
- **Loop behavior**: Renew ownership before every mutation; use C5 for status transitions; use C8
  for merges/commits; repair verified findings autonomously; mark completed only after the final
  gate; then re-inspect blueprint and repeat. Always release ownership in normal finalization.
- **Execution location**: Use C7's returned dedicated worktree as the working directory for all
  direct artifact/code changes, SDD stage invocations, checks, tests, reviews, and conflict edits;
  never apply feature work in the invoking checkout.
- **Covers**: REQ-012, REQ-013, REQ-015, REQ-016, REQ-017, REQ-018, REQ-019, REQ-021, NFR-003

### C10. Auto-dev delegation in existing SDD templates

- **Responsibility**: Prevent the nested SDD stage commands from consulting or firing global
  `workflow.auto_next` while C9 owns advancement.
- **Interface**: Each chain command recognizes an explicit run-local auto-dev delegation statement
  in its invocation context. In that mode it executes its normal stage and pass gate, returns the
  result to `auto-dev`, and skips only its `Auto-Next Chain Advance` section. Direct invocations are
  unchanged.
- **Covers**: REQ-014, NFR-003

### C11. Public `codexspec show-blueprint` CLI

- **Responsibility**: Use C1 read-only location checks and stream the exact current blueprint bytes
  to standard output. Send a translated, check-specific diagnostic to standard error and exit
  non-zero on not-a-repository, missing branch, missing/mismatched worktree, or missing file.
- **Interface**: `codexspec show-blueprint` has no mutation or synchronization options. It does not
  use Rich decoration on stdout and does not call C4/C7/C8.
- **Covers**: REQ-023, REQ-024, NFR-004

### C12. Distribution, documentation, and contract-test surfaces

- **Responsibility**: Register both new distributed templates as core commands; update core and
  total counts in installer metadata/comments/tests; document both agent commands and the CLI in
  every maintained language surface; add translated CLI diagnostics; update managed Claude/Codex
  context guidance; regenerate derived command/skill forms through `codexspec init --force --ai
  both`; and add focused Python/template/packaging tests.
- **Repository fit**: Brand-new command frontmatter need not enter translation catalogs, while CLI
  diagnostics belong in the existing `cli` translation namespace. Both templates use interaction
  and document language, not commit-language priority.
- **Covers**: REQ-001, REQ-014, REQ-023, NFR-004

## Key Design Decisions

### Decision 1: Split interpretive agent behavior from deterministic Python state management

- **Context**: Requirements discovery and SDD repair need agent judgment, while parsing, locking,
  exact JSON, worktrees, and raw CLI output need deterministic behavior.
- **Decision**: Keep `blueprint` and `auto-dev` as Markdown command coordinators and implement their
  shared state/Git substrate in Python modules exposed through hidden helper CLI actions.
- **Alternatives**: All-prose shell orchestration was rejected because it cannot enforce one parser,
  cross-platform locking, exact response variants, or atomic replacement. A fully Python auto-dev
  runner was rejected because the package does not own or embed Claude/Codex agent execution.
- **Trade-offs**: More internal CLI surface, but one testable source of truth and no new runtime
  dependency.
- **Covers**: REQ-001, REQ-006, REQ-011, REQ-013, REQ-023

### Decision 2: Use strict typed variants and canonical serialization

- **Context**: The protocol rejects extra and conditionally invalid fields and the blueprint has a
  deliberately mechanical format.
- **Decision**: Parse JSON into explicit per-operation/per-result variants with exact-key and
  relationship validation. Parse the whole blueprint into value objects and serialize canonically;
  never patch strings in place.
- **Alternatives**: Generic dictionaries and regular-expression replacement were rejected because
  independent field validity would not enforce cross-field relationships or full-document
  invariants.
- **Trade-offs**: Protocol additions require a new explicit version/variant, which is intentional.
- **Covers**: REQ-004, REQ-006, REQ-008, REQ-009, REQ-010, NFR-002

### Decision 3: Store coordination state under the common Git directory

- **Context**: Calls may originate from any linked checkout, while all must coordinate one
  repository and state must not be committed.
- **Decision**: Put short lock files, auto-dev ownership, merge ownership, and recovery records under
  `<git-common-dir>/codexspec/`. Use OS advisory locks only for short critical sections; use a
  renewable owner token with fencing for the long agent-run lifetime.
- **Alternatives**: Worktree-local locks would not coordinate callers from other checkouts. A static
  long-lived lock file would survive crashes and require manual cleanup. Holding an OS descriptor
  for the whole agent command is unavailable because distributed Markdown commands do not own a
  stable process.
- **Trade-offs**: Crash reclamation is activity-based rather than tied to a single agent host PID;
  fencing prevents an old owner from resuming writes after reclamation.
- **Covers**: REQ-011, REQ-018, REQ-019, NFR-001

### Decision 4: Couple atomic replacement and blueprint-only commit with recovery evidence

- **Context**: A blueprint change must be both an atomic file update and its own Git commit while
  unrelated feature work may be present.
- **Decision**: Use same-directory atomic replacement plus a common-directory recovery record around
  a path-limited commit. Return applied only after the commit succeeds; recover a known interrupted
  transaction before accepting another operation.
- **Alternatives**: Releasing the document lock before a separate agent commit allows later changes
  to collapse into one commit. Committing all staged changes can mix feature and blueprint history.
- **Trade-offs**: Recovery logic is more involved, but it makes crash outcomes inspectable and
  prevents ambiguous applied responses.
- **Covers**: REQ-007, REQ-011, REQ-019, NFR-001

### Decision 5: Merge committed default-branch history; never rewrite fixed history

- **Context**: The fixed branch must keep stable feature commit hashes while remaining current after
  arbitrary default-branch integration methods.
- **Decision**: Resolve local and remote refs by ancestry, attempt fetch at every required boundary,
  and merge available target history into the fixed branch. Treat file diff against the merged
  target as the review surface, even when old commit hashes remain listed.
- **Alternatives**: Rebase/reset/reconstruction was rejected because it rewrites or discards the
  continuous branch history. Timestamp-based selection was rejected because timestamps do not
  establish ancestry.
- **Trade-offs**: Merge commits and old commit-list entries are accepted; file changes remain clean.
- **Covers**: REQ-020, REQ-021, REQ-022

### Decision 6: Add explicit auto-dev delegation to every chain stage

- **Context**: Existing stage templates independently evaluate `workflow.auto_next`; invoking them
  unchanged from auto-dev can either stop or duplicate advancement depending on project config.
- **Decision**: Add one uniform delegation clause to chain templates. Auto-dev invokes each stage
  with that run-local clause and alone selects the successor after validating the stage result.
- **Alternatives**: Temporarily editing config is forbidden. Letting nested auto-next fire and then
  detecting duplicates is race-prone and violates ownership.
- **Trade-offs**: Several existing templates and their contract tests change, but ordinary direct
  behavior remains byte-for-behavior compatible.
- **Covers**: REQ-014, NFR-003

### Decision 7: Keep show-blueprint a raw, lock-free read

- **Context**: The CLI is intended for humans and shell pipelines, and helper writes are atomic.
- **Decision**: Reuse only read-only repository location and then write file bytes directly to
  stdout. Use stderr/non-zero for diagnostics; do not acquire any lock or initialize missing state.
- **Alternatives**: A read lock was rejected as unnecessary coupling. Rich panels or a JSON wrapper
  were rejected because they break exact output and pipelines.
- **Trade-offs**: A concurrent invocation may see the complete old or new snapshot; both are valid
  at a read instant.
- **Covers**: REQ-023, REQ-024, NFR-004

### Decision 8: Register blueprint and auto-dev as core distributed commands

- **Context**: They define a first-class planning/execution path built from the core SDD stages.
- **Decision**: Place both in installer category `core`, adjacent to the requirements and execution
  commands; update all command-count and documentation surfaces in lockstep and regenerate derived
  artifacts.
- **Alternatives**: `enhanced` was rejected because these commands own the primary multi-feature SDD
  workflow rather than an optional analysis utility.
- **Trade-offs**: Core count grows from 11 to 13 and total from 25 to 27.
- **Covers**: REQ-001, REQ-013

## Data Models and Key Entities

### Blueprint document and block

| Entity | Field | Type | Constraints | Covers |
|--------|-------|------|-------------|--------|
| BlueprintDocument | blocks | ordered list | No inter-block prose; canonical `---` separators | REQ-004 |
| BlueprintBlock | feature_id | string | Existing Feature ID format; unique; duplicated embedded value equal | REQ-005 |
| BlueprintBlock | development_status | enum | `pending`, `in_progress`, `completed` only | REQ-005, REQ-009 |
| BlueprintBlock | feature_directory | string | `not-created` iff pending; otherwise exact project-relative full path | REQ-005, REQ-009 |
| BlueprintBlock | requirements_markdown | string | All content after the three managed fields; no standalone `---`; no title or section keyword is interpreted | REQ-004, REQ-007 |

### Operation envelope

| Entity | Field | Type | Constraints | Covers |
|--------|-------|------|-------------|--------|
| Request | protocol_version | string | Required supported version | REQ-006 |
| Request | operation | enum | One of five operation names | REQ-006 |
| Request | expected_blueprint_hash | string | Exact `sha256:<hex>` returned by inspect/prior response | REQ-006, REQ-010 |
| Existing-target request | feature_id | string | Required only for existing block; sole locator | REQ-006 |
| Request | payload | exact variant object | Missing/extra/nullable/relationship-invalid fields rejected | REQ-006, REQ-008, REQ-009 |
| Response | result | enum | `invalid_request`, `conflict`, `rejected`, `applied` | REQ-010 |
| Response | error | object | Required only when not applied; exact code/message/details shape | REQ-010 |

### Coordination records

| Entity | Field | Type | Constraints | Covers |
|--------|-------|------|-------------|--------|
| AutoDevOwnership | token | cryptographically random string | Required by all auto-dev-specific mutations | REQ-018 |
| AutoDevOwnership | activity | monotonic/wall-clock evidence | Renewed at stage/write boundaries; stale record reclaimable | REQ-018 |
| MergeOwnership | token and refs | object | Blocks other Git writers during unresolved merge | REQ-021 |
| BlueprintTransaction | old/new hashes, HEAD, operation | object | Exists only while atomic write+commit may need recovery | REQ-011 |
| WorkspaceContext | repository/common-dir/worktree/refs | paths and refs | Derived from Git, never caller-supplied blueprint path | REQ-003, REQ-020 |

## API and Interface Contracts

### Public CLI

```text
codexspec show-blueprint
```

- Success: exact blueprint bytes on stdout, no decoration, exit 0.
- Failure: one translated diagnostic on stderr, no stdout content, non-zero exit.
- No flags that create, synchronize, repair, lock, or select another path.
- **Covers**: REQ-023, REQ-024, NFR-004

### Internal blueprint inspection

The hidden helper emits one JSON object containing a supported protocol version, repository and
worktree identity, `blueprint_exists`, exact `blueprint_hash`, and complete content. Agent commands
use this result to construct a mutation request; end users use `show-blueprint` instead.

- **Covers**: REQ-003, REQ-006

### Internal blueprint mutation

The helper reads exactly one JSON object from stdin. Domain responses follow REQ-010 exactly.
Malformed transport or persistence failure is not misclassified as a domain response: the process
uses stderr and a non-zero status, after which the agent re-inspects before retrying.

- **Covers**: REQ-006, REQ-007, REQ-008, REQ-009, REQ-010

### Auto-dev helper actions

All mutation actions take the opaque run token and return machine JSON. `sync-default` additionally
returns attempted refs, fetch warning when applicable, merge state, and conflict paths. Feature
commit accepts an exact Feature ID, allowed Conventional Commit type/description, and explicit path
list; it constructs the scope itself rather than trusting a complete caller message.

After the agent edits conflicted files, `prepare-sync-verification` accepts the exact complete list
of resolved conflict paths, rejects missing/additional paths or remaining conflict markers, and
stages only those literal paths while holding the shared Git lock. It also verifies that the index
has no unresolved entries. The agent then runs the required checks. `continue-sync` may commit a
conflict resolution only after that prepared state and a passing check result; `abort-sync` restores
the recorded pre-merge commit.

- **Covers**: REQ-018, REQ-019, REQ-020, REQ-021

## Sequence and Data Flow

### Blueprint append or pending edit

1. C6 calls C5 inspect/ensure and reads implemented feature records plus all blueprint blocks.
2. C6 conducts discovery or confirms the requested pending mutation.
3. C6 sends one exact request with the inspected hash to C5.
4. C4 acquires locks, re-reads, and routes through C3.
5. Invalid/stale/forbidden input returns without a write. Applied input is atomically replaced and
   committed, then returns the new hash and operation data.
6. On conflict C6 re-inspects and reapplies the confirmed user intent to current state.

### Auto-dev start, resume, and loop

1. C9 acquires C7 ownership and obtains a run token; a live owner causes immediate exit.
2. C9 inspects blueprint. An in-progress block goes directly to artifact-based recovery.
3. With no in-progress block, C8 synchronizes committed default history and establishes a passing
   baseline. A fetch warning continues. For conflicts, the agent edits files, asks C8 to stage and
   validate the resolution, then runs checks before C8 commits or aborts the merge. An unresolvable
   merge aborts and stops before status change.
4. C9 re-inspects after synchronization, selects the first pending block, and sends the exact
   pending-to-in-progress operation with its planned full directory.
5. C9 creates/reuses the directory, extracts the embedded requirements content, and invokes each
   SDD stage with C10 delegation. Existing stage review loops and progress guards remain gates.
6. C9 uses C8 for each path-limited feature commit and renews C7 ownership before mutations.
7. Final passing review permits in-progress-to-completed. C9 re-inspects and returns to step 3 for
   the first current pending block.
8. No pending block ends successfully and releases ownership. A stop guard preserves current
   evidence and releases normal ownership; an interrupted run is reclaimed on the next invocation.

### Default-branch integration and later comparison

1. External delivery integrates any selected committed point by any supported Git strategy.
2. Before the next pending requirement, C8 fetches when configured and merges the latest locally
   available target history into the fixed branch.
3. The target commit becomes an ancestor of the later fixed-branch head. File comparison therefore
   excludes content already in the target even if original fixed-branch commit objects remain in
   the commits view.

## Cross-Cutting Design

- **Lock order**: Git-write lock, then blueprint-modification lock. No component may acquire these
  in reverse. Read-only inspection/show acquires neither. (REQ-011, REQ-019, NFR-001)
- **Git environment isolation**: Before every `git -C` against the resolved repository, copy the
  environment and remove every variable reported by `git rev-parse --local-env-vars`, including
  caller index/worktree/object overrides. Setup and assertion helpers share the same runner.
  (REQ-020, NFR-001)
- **Fail closed**: Strict JSON accepts exact keys and validates relationships; corrupt blueprint,
  unknown transaction state, mismatched registered worktree, or lost run ownership stops mutation
  with evidence. (REQ-004, REQ-006, REQ-010, NFR-002)
- **No new dependencies**: Standard library JSON, dataclasses/enums, hashlib, tempfile/os.replace,
  subprocess, and platform-specific advisory lock primitives are sufficient. (NFR-001)
- **Language**: Agent templates retain the interaction/document split. CLI diagnostics use existing
  interaction-language resolution and translation fallback; raw blueprint stdout is never
  translated. (REQ-023, NFR-004)
- **Backward compatibility**: Existing direct SDD commands behave exactly as before unless their
  invocation explicitly declares auto-dev delegation. Existing projects without a dedicated
  workspace are unaffected until one of the new agent commands is invoked. (REQ-014)

## Risks and Trade-offs

| Risk | Impact | Mitigation |
|------|--------|------------|
| Agent commands have no stable host PID | A static long lock can survive interruption | Renewable owner record, fencing token, explicit release, and automatic stale-owner reclamation (C7/D3) |
| Crash between file replace and Git commit | Blueprint file and history can disagree | Recovery record plus pre-operation HEAD and old/new hashes (C4/D4) |
| Git merge leaves conflicted index | Blueprint commit could enter a merge accidentally | Merge ownership blocks all other Git writers until continue/abort (C8) |
| Existing worktree path is occupied or registered to another branch | Silent reuse could corrupt an unrelated checkout | Validate porcelain registry, basename, canonical path, and branch; fail closed (C1) |
| Squash/rebase/cherry-pick changes commit identity | Older commits remain in later commit lists | Merge target back and define acceptance by file diff, not commits view (D5) |
| Auto-dev nested command sees global auto-next | Stages can duplicate or skip | Uniform explicit delegation clause and contract tests across every chain template (C10/D6) |
| Platform lock behavior differs | Concurrent mutation safety can diverge on Windows/POSIX | One lock abstraction with process/multiprocess tests on supported CI platforms (C4/C7) |
| Large blueprint grows over product lifetime | Repeated full parse becomes slower | Full parse remains required for invariants; measure before optimizing and keep canonical linear parsing |

## Requirements Coverage

| Spec Requirement | Design Coverage |
|------------------|-----------------|
| REQ-001 | C6, C12; Decision 1, Decision 8 |
| REQ-002 | C6; blueprint sequence |
| REQ-003 | C1, C5; Decision 3 |
| REQ-004 | C2; Decision 2; fail-closed cross-cutting |
| REQ-005 | C2; data model |
| REQ-006 | C3, C5; Decision 1, Decision 2; internal mutation contract |
| REQ-007 | C3, C4, C6; Decision 4 |
| REQ-008 | C3, C6; Decision 2 |
| REQ-009 | C3, C9; Decision 2 |
| REQ-010 | C3, C5; Decision 2; internal mutation contract |
| REQ-011 | C4, C5; Decision 3, Decision 4; lock order |
| REQ-012 | C7, C9; auto-dev sequence |
| REQ-013 | C9; Decision 1, Decision 8; auto-dev sequence |
| REQ-014 | C10, C12; Decision 6; backward compatibility |
| REQ-015 | C9; auto-dev sequence |
| REQ-016 | C9; auto-dev sequence |
| REQ-017 | C9; auto-dev sequence |
| REQ-018 | C7, C9; Decision 3; coordination model |
| REQ-019 | C4, C8, C9; Decision 4; lock order |
| REQ-020 | C1, C8; Decision 5; Git isolation |
| REQ-021 | C8, C9; Decision 5; synchronization sequence |
| REQ-022 | C8; Decision 5; integration sequence |
| REQ-023 | C1, C11, C12; Decision 7; public CLI contract |
| REQ-024 | C11; Decision 7; public CLI contract |
| NFR-001 | C4, C7, C8; Decision 3, Decision 4; cross-cutting locks/isolation |
| NFR-002 | C2, C3; Decision 2; fail-closed validation |
| NFR-003 | C9, C10; Decision 6 |
| NFR-004 | C11, C12; Decision 7; language/output cross-cutting |
