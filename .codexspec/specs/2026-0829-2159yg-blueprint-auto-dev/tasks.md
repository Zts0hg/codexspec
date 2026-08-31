# Implementation Tasks: blueprint and auto-dev

**Related Plan**: `.codexspec/specs/2026-0829-2159yg-blueprint-auto-dev/plan.md`
**Related Design**: `.codexspec/specs/2026-0829-2159yg-blueprint-auto-dev/design.md`
**Status**: Draft

## Phase 1: Blueprint Document and Operation Protocol

### T001 [x]: Implement the canonical blueprint document model

**Outcome**: `src/codexspec/blueprint.py` can parse, validate, inspect, and canonically serialize an
ordered blueprint document without filesystem or Git access.

**Paths**:

- `src/codexspec/blueprint.py`
- `tests/test_blueprint.py`

**Dependencies**: None

**Covers**: REQ-004, REQ-005, NFR-002; Plan: Phase 1 pure blueprint model; Design: C2

**Implementation**:

- Add immutable blueprint document/block types, status values, Feature ID/name/directory
  validation, exact-byte SHA-256 hashing, lookup by Feature ID, and canonical LF serialization.
- Enforce the exact three-line managed prefix, standalone `---` separators, no inter-block prose,
  matching embedded and prefix Feature IDs, unique IDs, and the status/directory relationship.
- Preserve every line after the managed prefix as the complete requirements body so it is directly
  writable as `requirements.md`; do not detect it from a title, heading, or section keyword.

**Test Scenarios**:

- **T001-S01**: Parse and canonically round-trip one valid LF block.
- **T001-S02**: Parse multiple valid CRLF blocks and serialize with LF plus one terminal newline.
- **T001-S03**: Preserve the complete requirements body after the first three lines.
- **T001-S03a**: Parse and round-trip requirements content with no recognized title or section
  keyword.
- **T001-S04**: Reject missing, extra, or malformed managed prefix lines and inter-block prose.
- **T001-S05**: Reject a standalone `---` inside a requirements body or malformed separators.
- **T001-S06**: Reject duplicate Feature IDs or a prefix/embedded Feature ID mismatch.
- **T001-S07**: Reject unsupported statuses and invalid status/directory combinations.
- **T001-S08**: Reject invalid Feature IDs, feature names, or feature directory names.
- **T001-S09**: Hash exact source bytes so equivalent LF and CRLF inputs have different read hashes.

**Verification**: `uv run pytest tests/test_blueprint.py -k document`

### T002 [x]: Implement strict operation decoding and domain outcomes

**Outcome**: The pure protocol accepts only the five exact versioned request variants and emits one
of the four exact response variants with the required classification order and field shapes.

**Paths**:

- `src/codexspec/blueprint.py`
- `tests/test_blueprint.py`

**Dependencies**: T001

**Covers**: REQ-006, REQ-007, REQ-008, REQ-009, REQ-010, NFR-002; Plan: Phase 1 protocol and
operation rules; Design: C3

**Implementation**:

- Decode exact typed variants for `append_requirement`, `replace_pending_requirement`,
  `delete_pending_requirement`, `move_pending_requirement`, and `update_status`.
- Validate common and conditional keys in both directions, including append's omitted Feature ID,
  exact payload shapes, move position relationships, and status-transition directory rules.
- Apply legal operations to the pure document, generating an append Feature ID through an injected
  generator, and encode exact `invalid_request`, `conflict`, `rejected`, and `applied` responses.

**Test Scenarios**:

- **T002-S01**: Append generates a permanent Feature ID and returns exact applied fields/data.
- **T002-S02**: Replace updates only a pending block while preserving its Feature ID and order.
- **T002-S03**: Delete a pending block and return an empty `data` object.
- **T002-S04**: Move pending blocks to first/last or before/after another pending Feature ID.
- **T002-S05**: Transition pending to in-progress with the exact feature directory, then in-progress
  to completed while preserving the directory.
- **T002-S06**: Classify malformed JSON, wrong version, unknown operation, and missing/extra/null or
  wrong-typed keys as `invalid_request` with no hash fields.
- **T002-S07**: Reject invalid move position/reference relationships in both directions.
- **T002-S08**: Return `conflict` before business-rule evaluation when the expected hash is stale.
- **T002-S09**: Return `rejected` for missing targets, non-pending edit/delete/move, illegal status
  transitions, and invalid reference targets.
- **T002-S10**: Ensure every error has exact `code`, `message`, and non-null `details`, and every
  applied response has previous/new hashes and operation/Feature ID fields.

**Verification**: `uv run pytest tests/test_blueprint.py -k protocol`

## Phase 2: Repository, Worktree, and Coordination Substrate

### T003 [x]: Implement sanitized Git execution and repository/worktree discovery

**Outcome**: `src/codexspec/automation.py` resolves repository facts and validates or creates the
fixed branch/worktree without reading caller worktree changes or inheriting foreign Git state.

**Paths**:

- `src/codexspec/automation.py`
- `tests/test_automation_git.py`

**Dependencies**: None

**Covers**: REQ-003, REQ-020, REQ-023, REQ-024, NFR-001; Plan: Phase 2 repository and worktree
substrate; Design: C1, C8

**Implementation**:

- Add one Git runner that fixes `cwd`, captures typed evidence, and removes all variables reported
  by `git rev-parse --local-env-vars` before targeting a repository.
- Resolve the common Git directory, primary/default refs, fixed `codexspec/auto-dev` branch,
  repository-specific sibling path ending in `worktree-for-codexspec-auto-dev`, and blueprint path.
- Parse `git worktree list --porcelain`; provide read-only locate and mutating ensure operations,
  selecting local/remote committed history by ancestry and merging divergence without rebase.

**Test Scenarios**:

- **T003-S01**: Resolve all paths and refs from a normal repository and from a linked worktree.
- **T003-S02**: Locate an existing correctly registered fixed worktree and branch.
- **T003-S03**: Read-only locate reports absent branch, worktree, mismatched registration, and
  non-repository without creating or repairing anything.
- **T003-S04**: Ensure creates missing fixed branch/worktree from local default when no remote exists.
- **T003-S05**: Ensure chooses the descendant when local and remote defaults have an ancestry
  relationship and merges when they diverge.
- **T003-S06**: Ensure rejects an occupied or registered expected path bound to the wrong branch.
- **T003-S07**: Caller staged/unstaged content is absent from the created dedicated worktree.
- **T003-S08**: Hostile inherited Git directory, worktree, index, and object variables do not affect
  target operations or mutate the caller index.

**Verification**: `uv run pytest tests/test_automation_git.py -k 'runner or repository or worktree'`

### T004 [x]: Implement locks and atomic blueprint commit transactions

**Outcome**: One operation can atomically replace and commit only `.codexspec/blueprint.md`, with
serialized writers and deterministic recovery after interruption.

**Paths**:

- `src/codexspec/automation.py`
- `tests/test_blueprint_store.py`

**Dependencies**: T001, T002, T003

**Covers**: REQ-007, REQ-011, REQ-019, NFR-001; Plan: Phase 2 locking and blueprint transaction;
Design: C4

**Implementation**:

- Add a cross-platform short lock abstraction and common-Git-directory paths with the global
  Git-write-then-blueprint-modification acquisition order.
- Implement re-read/revalidate, recovery-record creation, same-directory flush/atomic replace,
  path-limited blueprint-only commit, cleanup, and non-domain transport failure reporting.
- Recover a known interrupted replacement or prior state by old/new hash and pre-operation HEAD;
  fail closed on unrelated state.

**Test Scenarios**:

- **T004-S01**: A valid mutation produces one commit containing only the blueprint path and returns
  `applied` only after the commit succeeds.
- **T004-S02**: Concurrent stale writers serialize; one applies and the other receives `conflict`.
- **T004-S03**: Unrelated staged and unstaged files remain byte-for-byte and index-for-index intact.
- **T004-S04**: Failure before replacement leaves old bytes and no blueprint commit.
- **T004-S05**: Failure after replacement but before commit is recovered deterministically on the
  next helper call.
- **T004-S06**: Failure after commit but before record cleanup recognizes the completed transaction
  without creating a duplicate commit.
- **T004-S07**: A corrupt document or recovery record/hash/HEAD mismatch fails closed with stderr
  evidence and no domain response.
- **T004-S08**: Multiprocess lock tests enforce Git-write-before-blueprint ordering without deadlock.

**Verification**: `uv run pytest tests/test_blueprint_store.py`

### T005 [x]: Implement renewable auto-dev ownership

**Outcome**: Exactly one active auto-dev run owns a repository through a renewable fenced token,
while interrupted ownership is automatically reclaimable.

**Paths**:

- `src/codexspec/automation.py`
- `tests/test_auto_dev_ownership.py`

**Dependencies**: T003

**Covers**: REQ-012, REQ-018, NFR-001; Plan: Phase 2 auto-dev ownership; Design: C7

**Implementation**:

- Add acquire, renew, assert-owner, release, and stale-reclaim operations around an activity record
  and short OS lock in the common Git directory.
- Use cryptographically random fencing tokens, injectable clocks, and atomic record replacement.
- Require owner assertion immediately before every auto-dev repository mutation adapter.

**Test Scenarios**:

- **T005-S01**: First acquire returns a token and a second live acquire exits immediately as busy.
- **T005-S02**: Renew and assert succeed only for the current token and update activity.
- **T005-S03**: Normal release removes ownership and permits the next run.
- **T005-S04**: A stale activity record is reclaimed automatically without manual cleanup.
- **T005-S05**: Every call from the old token fails after takeover, including immediately before a
  simulated mutation.
- **T005-S06**: Concurrent acquire/reclaim subprocesses still produce exactly one current owner.

**Verification**: `uv run pytest tests/test_auto_dev_ownership.py`

### T006 [x]: Implement default synchronization and feature-scoped commits

**Outcome**: Token-validated Git operations synchronize the fixed branch before each pending
requirement, expose resolvable conflicts, abort unrecoverable merges, and create only correctly
scoped feature commits.

**Paths**:

- `src/codexspec/automation.py`
- `tests/test_auto_dev_git.py`

**Dependencies**: T003, T005

**Covers**: REQ-019, REQ-020, REQ-021, REQ-022, NFR-001; Plan: Phase 2 Git synchronization and
feature commit helpers; Design: C8

**Implementation**:

- Add token-validated `sync-default`, `prepare-sync-verification`, `continue-sync`, `abort-sync`, and
  `commit-feature` service operations under serialized Git ownership.
- Fetch when configured, continue after fetch failure using locally available refs, compare refs by
  ancestry, merge divergence without rebase, and retain merge ownership through conflict repair.
- Build `type(<feature-id>): description` commit messages and stage only explicit allowed paths,
  always rejecting the blueprint path.

**Test Scenarios**:

- **T006-S01**: Local-only repository synchronizes from its local default and begins cleanly.
- **T006-S02**: Configured remote fetches before each new pending requirement; fetch failure returns
  a warning, continues locally, and is attempted again on the next sync call.
- **T006-S03**: Ancestor/descendant refs produce no rewrite, while diverged refs produce a merge.
- **T006-S04**: A clean merge passes project-check handoff and releases merge ownership.
- **T006-S05**: Conflict state blocks other Git writers until owner continuation or abort.
- **T006-S06**: Resolved conflicts continue only after passing checks; failed/unrecoverable results
  abort to the pre-merge state and leave the next requirement pending.
- **T006-S07**: Feature commits require the exact Feature ID scope, include only supplied paths, and
  reject blueprint or unrelated staged paths.
- **T006-S08**: After merge, fast-forward, squash, rebase, or cherry-pick integration into the
  target, a later target merge leaves file changes containing only unintegrated work even when old
  fixed-branch commits remain visible.
- **T006-S09**: A conflicted merge cannot continue before the helper prepares the resolved index;
  preparation returns a verification candidate, after which passing checks allow the helper to
  commit the merge and failed checks still roll back to the recorded pre-merge commit.

**Verification**: `uv run pytest tests/test_auto_dev_git.py`

## Phase 3: CLI Adapters

### T007 [x]: Add hidden automation helpers and public show-blueprint CLI

**Outcome**: Agent templates have exact machine-oriented hidden CLI actions, and users can print the
latest blueprint through a strictly read-only public command with localized errors.

**Paths**:

- `src/codexspec/__init__.py`
- `src/codexspec/blueprint.py`
- `src/codexspec/automation.py`
- `src/codexspec/i18n.py`
- `templates/translations/*.json`
- `tests/test_blueprint_cli.py`
- `tests/test_cli_i18n.py`

**Dependencies**: T002, T004, T005, T006

**Covers**: REQ-003, REQ-006, REQ-010, REQ-011, REQ-018, REQ-019, REQ-020, REQ-021, REQ-023,
REQ-024, NFR-004; Plan: Phase 3 CLI and helper adapters; Design: C5, C7, C8, C11, C12

**Implementation**:

- Register hidden inspect/apply and ownership/Git actions as thin stdin/stdout adapters with no
  caller-selectable blueprint path; keep domain outcomes separate from transport failures.
- Add `codexspec show-blueprint`, writing exact bytes to stdout and translated prerequisite-specific
  diagnostics to stderr without Rich decoration, lock, fetch, mutation, or repair.
- Add all CLI message keys to the English baseline and every supported translation JSON file.

**Test Scenarios**:

- **T007-S01**: Hidden inspect optionally ensures the workspace and returns exact identity, existence,
  hash, and complete-content JSON.
- **T007-S02**: Hidden apply consumes one request and emits one exact domain response with exit zero.
- **T007-S03**: Malformed transport or internal persistence failure emits no domain JSON, writes
  stderr, and exits non-zero.
- **T007-S04**: Ownership and Git helper actions reject missing, stale, or wrong tokens and return
  machine evidence for successful calls.
- **T007-S05**: `show-blueprint` emits the file byte-for-byte on stdout with exit zero and no extra
  newline or decoration.
- **T007-S06**: Not-a-repository, missing branch, missing/mismatched worktree, and missing blueprint
  each produce a specific stderr diagnostic, empty stdout, and non-zero exit.
- **T007-S07**: `show-blueprint` performs no create/fetch/merge/write/lock operation and can only see
  an old or new complete atomic snapshot during a concurrent replacement.
- **T007-S08**: Every supported language resolves the new diagnostics, with English fallback and
  stdout/stderr separation intact.

**Verification**: `uv run pytest tests/test_blueprint_cli.py tests/test_cli_i18n.py`

## Phase 4: Agent Command Templates and Delegation

### T008 [x]: Add the blueprint agent-command template

**Outcome**: `blueprint` performs specify-style confirmed requirements discovery and pending-only
maintenance against the dedicated blueprint exclusively through the helper protocol.

**Paths**:

- `templates/commands/blueprint.md`
- `tests/test_blueprint_template.py`

**Dependencies**: T007

**Covers**: REQ-001, REQ-002, REQ-006, REQ-007, REQ-008, REQ-010, REQ-011; Plan: Phase 4 blueprint
template and contract tests; Design: C6

**Implementation**:

- Add standard frontmatter and interaction/document language rules; require constitution/profile,
  implemented specs, and all current blueprint blocks as context.
- Reuse specify's iterative one-question, requirements quality, and explicit final confirmation
  discipline before append/replace; define confirmed delete/move flows for pending blocks.
- Specify exact inspect/apply JSON construction, conflict re-inspection, response handling, and the
  prohibition on direct file edits, status updates, or immediate feature development.

**Test Scenarios**:

- **T008-S01**: Append discussion consults implemented and planned context, resolves all user-owned
  choices, confirms once, and sends exactly feature name plus complete requirements Markdown.
- **T008-S02**: Replace, delete, and move identify targets only by Feature ID and operate only on
  pending blocks with exact payload variants.
- **T008-S03**: In-progress/completed blocks are view-only and the command never calls update-status.
- **T008-S04**: A stale hash causes re-inspection and intent re-evaluation before one retry.
- **T008-S05**: Rejected, invalid-request, and transport failures are reported distinctly without a
  direct blueprint write.
- **T008-S06**: The requirements body follows specify organization, contains no standalone reserved
  separator, and the command ends without entering SDD implementation.

**Verification**: `uv run pytest tests/test_blueprint_template.py`

### T009 [x]: Add the auto-dev agent-command template

**Outcome**: `auto-dev` autonomously processes the shared blueprint in document order, resumes
unfinished work, and stops or completes according to existing SDD gates without user questions.

**Paths**:

- `templates/commands/auto-dev.md`
- `tests/test_auto_dev_template.py`

**Dependencies**: T007

**Covers**: REQ-012, REQ-013, REQ-015, REQ-016, REQ-017, REQ-018, REQ-019, REQ-021, NFR-003;
Plan: Phase 4 auto-dev template and contract tests; Design: C9

**Implementation**:

- Define ownership acquire/renew/assert/release, fixed-workspace inspection, in-progress-first resume,
  synchronization-before-pending, pending claim, exact requirements extraction, and directory reuse.
- Define delegated requirements-to-review stage progression, artifact/review-based resume resolution,
  autonomous best-practice choices and repair, feature-scoped commits, and completion gate.
- Re-read after every completion, process the first current pending block, include newly appended
  requirements in the same run, and preserve state/evidence on stop or interruption.

**Test Scenarios**:

- **T009-S01**: A second live auto-dev exits immediately while blueprint remains independently usable.
- **T009-S02**: Existing in-progress work resumes from its recorded Feature Directory and earliest
  incomplete artifact/review gate without resetting status or creating another directory.
- **T009-S03**: With no in-progress block, sync runs before selecting and changing the first pending
  block to in-progress.
- **T009-S04**: The block body after exactly three managed lines becomes the new directory's
  `requirements.md`, and the directory is `<feature-id>-<feature-name>`.
- **T009-S05**: All SDD stages run in order under delegation, unspecified neutral details use sound
  engineering practice, and no user question is introduced.
- **T009-S06**: Completion occurs only after implementation checks and final code review pass, then
  a fresh read selects the first current pending requirement.
- **T009-S07**: Newly appended pending work joins the same run; no pending work ends the run and
  releases ownership.
- **T009-S08**: Existing stop guards preserve in-progress state/artifacts/evidence and stop before
  later pending work; unexpected termination is resumable through stale ownership recovery.
- **T009-S09**: Failed fetch continues locally, while unrecoverable merge/check failure aborts the
  merge, stops, and leaves the next requirement pending.
- **T009-S10**: Every direct artifact/code operation and nested SDD stage runs from the returned
  dedicated worktree rather than the checkout that invoked `auto-dev`.

**Verification**: `uv run pytest tests/test_auto_dev_template.py`

### T010 [x]: Add run-local auto-dev delegation to every SDD chain stage

**Outcome**: Nested stages return control to auto-dev without consulting global auto-next, while
every direct command retains its existing behavior.

**Paths**:

- `templates/commands/generate-spec.md`
- `templates/commands/spec-to-design.md`
- `templates/commands/spec-to-plan.md`
- `templates/commands/plan-to-tasks.md`
- `templates/commands/implement-tasks.md`
- `tests/test_sdd_workflow_templates.py`
- `tests/test_auto_dev_template.py`

**Dependencies**: T009

**Covers**: REQ-014, NFR-003; Plan: Phase 4 auto-dev delegation; Design: C10

**Implementation**:

- Add one uniform invocation-context rule to each successor stage: execute the ordinary stage and
  pass gates, then return to auto-dev and skip only that stage's global auto-next section.
- Keep ordinary direct invocation and `workflow.auto_next` behavior unchanged.
- Add source-template contract tests that require the clause at every stage and prohibit accidental
  recursive or duplicate advancement.

**Test Scenarios**:

- **T010-S01**: Each delegated stage executes its normal work/review gate and returns to auto-dev
  without reading or firing global auto-next.
- **T010-S02**: Delegated terminal implementation returns its pass/stop result exactly once.
- **T010-S03**: Direct invocation with auto-next true still advances through the existing chain.
- **T010-S04**: Direct invocation with auto-next false still stops at the existing boundary.
- **T010-S05**: Every source and regenerated derived stage contains equivalent delegation semantics.

**Verification**: `uv run pytest tests/test_sdd_workflow_templates.py tests/test_auto_dev_template.py`

## Phase 5: Distribution and Documentation

### T011 [x]: Register, distribute, and regenerate the two commands

**Outcome**: Both new core commands are installed for Claude and Codex, metadata/counts remain
consistent at 13 core and 27 total, and generated project integrations match source templates.

**Paths**:

- `src/codexspec/commands/installer.py`
- `tests/commands/test_installer.py`
- `tests/test_cli.py`
- `tests/test_codex_integration.py`
- `tests/test_init_compliance.py`
- `templates/claude/CLAUDE.md`
- `templates/codex/AGENTS.md`
- `.claude/commands/codexspec.*.md`
- `.agents/skills/codexspec-*/SKILL.md`

**Dependencies**: T008, T009, T010

**Covers**: REQ-001, REQ-013, REQ-014, NFR-004; Plan: Phase 5 registration and self-bootstrap;
Design: C10, C12

**Implementation**:

- Register `blueprint` and `auto-dev` as core command metadata; update installer comments/docstrings,
  category and total assertions, list output, and both known count-test sites.
- Update managed context guidance where the core workflow is enumerated without adding unnecessary
  frontmatter translation catalog entries.
- Run `uv run codexspec init . --force --ai both` once after source tests pass and verify source to
  Claude/Codex parity.

**Test Scenarios**:

- **T011-S01**: Metadata lists 13 core and 27 total commands with unique names/files and expected
  category placement.
- **T011-S02**: Init installs blueprint and auto-dev for Claude and Codex with both language sections.
- **T011-S03**: List/init summaries include both commands and the corrected counts.
- **T011-S04**: Derived commands preserve helper contracts, auto-dev delegation, and source behavior.
- **T011-S05**: Re-running forced init is idempotent and produces no derived drift.

**Verification**: `uv run pytest tests/commands/test_installer.py tests/test_cli.py tests/test_codex_integration.py tests/test_init_compliance.py`

### T012 [x]: Document all public commands in every maintained language

**Outcome**: All maintained README and documentation language surfaces describe the two agent
commands and the read-only CLI consistently with the confirmed contracts.

**Paths**:

- `README*.md`
- `docs/*/user-guide/commands.md`
- `docs/*/reference/cli.md`

**Dependencies**: T007, T008, T009, T011

**Covers**: REQ-001, REQ-013, REQ-023, NFR-004; Plan: Phase 5 multilingual documentation;
Design: C11, C12

**Implementation**:

- Add translated command-table entries to all eight README variants.
- Document `blueprint` and `auto-dev` in all eight command guides.
- Document `codexspec show-blueprint`, raw output, prerequisites, and failure behavior in all eight
  CLI references.

**Verification**:

- `rg -l 'blueprint' README*.md docs/*/user-guide/commands.md docs/*/reference/cli.md` returns every
  required language file.
- Documentation command names, fixed branch/worktree, and status names match the implementation.

## Phase 6: Verification and Review

### T013 [x]: Run focused and full quality gates, then complete code review

**Outcome**: All focused and repository-wide checks pass, the implementation satisfies every task
scenario, and the final code review contains no unresolved verified defect.

**Paths**:

- `tests/`
- `.codexspec/specs/2026-0829-2159yg-blueprint-auto-dev/tasks.md`
- `.codexspec/specs/2026-0829-2159yg-blueprint-auto-dev/review-code.md`

**Dependencies**: T001-T012

**Covers**: REQ-001 through REQ-024, NFR-001 through NFR-004; Plan: Phase 6 end-to-end verification
and review; Design: C1-C12

**Implementation**:

- Run every focused verification command from T001-T012 and map each scenario to a passing test.
- Run `uv run ruff check src/ tests/`, `uv run pytest`, `git diff --check`, translation completeness,
  command-count/documentation sweeps, and package-content inspection for all shipping paths.
- Invoke the complete-feature code review, repair every verified defect, rerun affected focused
  checks and the full suite, and record final evidence.

**Verification**: Every command above exits zero and the final review status passes.

**Evidence (2026-08-31)**:

- Focused suites: `uv run pytest tests/test_blueprint.py` 36 passed; `tests/test_automation_git.py`
  14 passed; `tests/test_blueprint_store.py` 10 passed; `tests/test_auto_dev_ownership.py`
  4 passed; `tests/test_auto_dev_git.py` 18 passed; `tests/test_blueprint_cli.py` +
  `tests/test_cli_i18n.py` 27 passed; `tests/test_blueprint_template.py` 3 passed;
  `tests/test_auto_dev_template.py` 4 passed; `tests/test_sdd_workflow_templates.py` +
  `tests/test_auto_dev_template.py` 62 passed; `tests/commands/test_installer.py` +
  `tests/test_cli.py` + `tests/test_codex_integration.py` + `tests/test_init_compliance.py`
  129 passed. All 85 task scenarios map to passing tests (T001-S08 feature-name evidence added).
- Repository gates: `uv run ruff check src/ tests/` all checks passed; `uv run pytest`
  **1327 passed / 50 skipped (exit 0)**; `git diff --check` clean; translation completeness
  19 new keys × 8 languages (full catalogs 113 × 8, zero missing/extra); `blueprint` present in
  8/8 READMEs, 8/8 `docs/*/user-guide/commands.md`, 8/8 `docs/*/reference/cli.md` with fixed
  branch/worktree identifiers matching `automation.py`; `uv build` wheel ships only
  `scripts/bash` + `scripts/powershell` under `scripts/` and includes both new command templates;
  sdist contains no `docs/`, `tests/`, `internal/`, or `scripts/python` content.
- Code review: three-round defect-gate review recorded in `review-code.md` (round 1: primary +
  specialist, 10 findings; round 2: fresh isolated reviewer, 3 findings, round-1 repairs
  independently confirmed; round 3: coordinator repair verification, 1 in-repair defect found and
  fixed). All 14 findings repaired with regression tests; final verdict **PASS**, fingerprint
  `sha256:21bd698d7ecd20d641b8bacdc4df92fb502e2aaf0f78d9e2b8e9010ac2b8281c`; five non-blocking
  coverage gaps recorded as open follow-ups.

## Dependency Summary

```text
T001 -> T002 -> T004 -> T007 -> T008 -> T011 -> T012 -> T013
  |               ^       |       `-> T009 -> T010 -'
  `---------------'       |
T003 -> T004              |
  `-> T005 -> T006 -------'
```

- T001 and T003 can begin independently.
- Protocol, repository coordination, and CLI adapters must be stable before agent templates depend
  on their machine contracts.
- Source templates and delegation must pass before the single derived regeneration step.
- Documentation can follow stable public surfaces; full review runs after all prior tasks.

## Coverage Matrix

| Authority | Tasks | Scenario Coverage |
|-----------|-------|-------------------|
| C1 / REQ-003, REQ-020, REQ-023, REQ-024 | T003, T007 | T003-S01-S08; T007-S05-S07 |
| C2 / REQ-004, REQ-005, NFR-002 | T001 | T001-S01-S09 |
| C3 / REQ-006-REQ-010, NFR-002 | T002 | T002-S01-S10 |
| C4 / REQ-007, REQ-011, REQ-019, NFR-001 | T004 | T004-S01-S08 |
| C5 / REQ-003, REQ-006, REQ-010, REQ-011 | T007 | T007-S01-S03 |
| C6 / REQ-001, REQ-002, REQ-006-REQ-008, REQ-010-REQ-011 | T008 | T008-S01-S06 |
| C7 / REQ-012, REQ-018, NFR-001 | T005, T007 | T005-S01-S06; T007-S04 |
| C8 / REQ-019-REQ-022, NFR-001 | T003, T006, T007 | T003-S04-S08; T006-S01-S09; T007-S04 |
| C9 / REQ-012-REQ-013, REQ-015-REQ-019, REQ-021, NFR-003 | T009 | T009-S01-S10 |
| C10 / REQ-014, NFR-003 | T010, T011 | T010-S01-S05; T011-S04-S05 |
| C11 / REQ-023-REQ-024, NFR-004 | T007, T012 | T007-S05-S08; documentation verification |
| C12 / REQ-001, REQ-013-REQ-014, REQ-023, NFR-004 | T007, T011, T012 | T007-S08; T011-S01-S05; documentation verification |
| Phase 6 / all requirements | T013 | All T001-T011 scenarios plus full-suite evidence |

## Unmapped Tasks

None.
