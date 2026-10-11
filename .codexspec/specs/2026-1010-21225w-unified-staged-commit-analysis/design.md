# Design Document: Unified Staged Commit Analysis

**Related Spec**: [spec.md](spec.md)
**Confirmed Requirements**: [requirements.md](requirements.md)
**Created**: 2026-10-10
**Status**: Reviewed

## Context

The agent owns semantic message generation. Deterministic helpers retain control
of staging preparation, ownership checks, and Git execution. The common analysis
surface remains commit-staged, including its preview mode. Preparation must
provide a real Git index, not a synthetic prose description of future changes.

## Architecture & Components

### A. Commit invocation instructions

- **Responsibility**: State that authorized agent commits use commit-staged,
  including plain conversation, implementation, auto-dev, and blueprint flows.
- **Interface**: A bounded, idempotent context block injected into both CLAUDE.md
  and AGENTS.md, plus instructions at actual workflow commit sites. Existing
  context content is retained during installation updates. Codex and Claude use
  their respective skill and slash-command spelling.
- **Covers**: REQ-001, REQ-004

### B. Staged analysis command

- **Responsibility**: Inspect only the explicitly selected staging area and
  generate a complete Conventional Commits message in the configured language.
  Use a body when the staged changes need one. Preview returns the message to a
  helper caller; direct execution retains the existing command entry point.
- **Interface**: Existing commit-staged and -p; helper calls supply the explicit
  workspace, prepared index, expected HEAD/tree, and required scope. Context
  constraints determine format, not unstaged intent. Capture HEAD and staged tree
  before and after analysis; stale content requires reanalysis. Hook retry
  preparation belongs to the caller, followed by fresh analysis.
- **Covers**: REQ-001, REQ-002, REQ-003, REQ-005, REQ-006

Direct execution uses a hidden deterministic commit-staged helper to snapshot
HEAD and the original index tree without staging anything, then to execute the
full message against that same index using component E. Preview never commits.
The snapshot interface accepts no replacement index for direct mode. Helper
preview explicitly uses the helper-owned prepared index from component C.
This distinguishes an explicit caller-supplied analysis input from silently
routing a user's index to another checkout. Unborn HEAD is represented explicitly
for direct first-commit use; feature and blueprint helpers require their existing
prepared baseline.

### C. Prepared staging support

- **Responsibility**: Prepare a helper-owned Git index for exactly the changes
  that its existing path-specific commit would include, leaving the caller's
  ordinary index and unrelated changes intact.
- **Interface**: New shared Python support under src/codexspec; it uses the
  existing GitRunner, extends that runner with a narrowly explicit index option,
  and never inherits arbitrary repository-local environment variables.
- **Data**: A versioned preparation record under the existing Git coordination
  directory contains a random preparation identifier, absolute workspace,
  operation kind, expected HEAD, analyzed tree, owned index path, selected paths,
  and operation-specific identity. Feature preparations are bound to an ownership
  token and feature ID. Blueprint preparations retain the exact request and the
  generated feature ID, avoiding a new ID at finalization.
- **Covers**: REQ-003, REQ-004, REQ-005, REQ-006

Preparation initializes an alternate Git index from HEAD and stages only the
selected feature paths. Blueprint preparation uses apply_operation to validate
and compute the proposed bytes, stores those bytes as a Git blob, and stages
that blob into the alternate index. Blueprint preparation does not publish the
new document into the working tree and does not report the mutation as applied.

The alternate index is the explicit analysis input from its creation through
finalization. Routing must never substitute a different workspace or index.
Preparation records and indexes are helper-owned, not caller-owned staging data.
Validate record schema, workspace binding, paths, links, expected object IDs, and
operation-specific identity before using them. Reject unknown or inconsistent
records. Do not accept an arbitrary external index path from a finalize request.

### D. Feature and blueprint orchestration

- **Responsibility**: Provide prepare -> analyze -> finalize without weakening
  existing execution locks, ownership validation, path restrictions, or recovery.
- **Interface**: Feature prepare takes token, feature_id, and paths; finalization
  takes token, preparation_id, analyzed_tree, and a full multiline message.
  Blueprint prepare takes the existing mutation request; finalization takes
  preparation_id, analyzed_tree, and message, with the existing auto-dev token
  requirement for status changes. Invalid, rejected, conflicting, and no-op
  blueprint operations retain their existing semantics and create no commit.
- **Covers**: REQ-002, REQ-003, REQ-004, REQ-005, REQ-006

Finalization reacquires existing locks and owner guards, checks preparation
identity, HEAD, and analyzed tree, and re-evaluates the selected content. A stale
result requires a new preparation and analysis, never message reuse. Blueprint
finalization re-evaluates the original operation against the current hash using
its reserved feature ID. It publishes bytes and commits within the existing
journaled transaction, retaining rollback and interruption recovery.

Use a full message rather than the previous type/description-only interface.
Validate the Conventional Commits subject and the workflow-required scope while
retaining the body verbatim. Pass messages as subprocess data, not shell text.
Missing analysis metadata must fail rather than use legacy fixed messages.

### E. Commit content verification

- **Responsibility**: Ensure Git commits the analyzed tree, including when hooks
  can modify staging during execution. Preserve existing hooks and propagate
  their failures; do not bypass checks to make a commit succeed.
- **Interface**: Shared guarded execution wraps the existing hook phases that
  run before a commit is created. Each wrapper delegates the original hook when
  present and validates the actual commit index tree afterward. Tree or HEAD
  drift aborts the attempt and requires new preparation and analysis. The helper
  continues to use path-limited commit behavior so unrelated index entries are
  preserved. Wrapper artifacts are temporary and preserve normal hook arguments,
  working directory, environment, and configured hook lookup.
- **Covers**: REQ-003, REQ-005, REQ-006

The implementation must validate this behavior against real Git hook fixtures
before relying on it. All original hooks, including post-commit behavior, remain
reachable. Hook-induced working-tree changes are never automatically included
without caller preparation and reanalysis. Successful results report the commit
ID and establish that its tree equals the analyzed tree. A post-commit mismatch
must be surfaced as an error, never presented as success or silently rewritten.

## Key Design Decisions

### Decision 1: Use preview analysis and retain deterministic execution

- **Context**: Helpers currently execute Git and do not call a model.
- **Decision**: The surrounding agent invokes commit-staged preview between
  helper preparation and finalization. Helpers accept the resulting full message.
- **Alternatives**: Embedding an LLM client introduces an unnecessary dependency;
  direct agent commits would bypass existing helper protection.
- **Trade-offs**: Hidden helper calls become multi-step, with explicit stale-state
  handling. There is one semantic analysis policy rather than a parallel helper
  message generator.
- **Covers**: REQ-001, REQ-002, REQ-004, REQ-006

### Decision 2: Use a dedicated prepared index for helper analysis

- **Context**: Tests explicitly require blueprint commits to preserve unrelated
  staged changes. Analyzing the whole caller index then committing selected
  working-tree paths would analyze different content.
- **Decision**: Helpers prepare an alternate real Git index scoped to the intended
  commit, and the agent explicitly selects it for analysis.
- **Alternatives**: Clearing/restaging the ordinary index violates caller staging
  ownership; refusing all unrelated staged changes loses existing supported
  behavior; analyzing an unstaged patch violates the confirmed input boundary.
- **Trade-offs**: Preparation metadata and cleanup are required. Direct commits
  still analyze the caller's ordinary index without index substitution.
- **Covers**: REQ-003, REQ-004, REQ-005, REQ-006

### Decision 3: Keep blueprint publication within finalization

- **Context**: apply_and_commit currently protects blueprint replacement and
  commit with locking and recovery. LLM analysis spans separate tool calls.
- **Decision**: Prepare proposed bytes in the alternate index; publish the real
  file only inside the existing finalization transaction after analysis.
- **Alternatives**: Leaving the blueprint mutated between calls exposes an
  uncommitted operation to readers and changes recovery semantics.
- **Trade-offs**: Revalidate the operation at finalization and reserve generated
  IDs in the preparation record.
- **Covers**: REQ-004, REQ-005, REQ-006

### Decision 4: Validate content across hook execution

- **Context**: A check before git commit alone cannot detect index modifications
  by a hook before Git creates the commit.
- **Decision**: Delegate existing hooks through a temporary verification wrapper
  and reject changed trees before commit creation; verify the resulting tree too.
- **Alternatives**: Skipping hooks weakens existing checks; checking only after
  commit reports a mismatch after the requirement has already been violated.
- **Trade-offs**: Cross-platform hook delegation requires real Git tests and
  careful preservation of original hook lookup and arguments.
- **Covers**: REQ-005, REQ-006

## API / Interface Contracts

**Covers**: REQ-002, REQ-003, REQ-004, REQ-005, REQ-006

The ordinary hidden helper exposes snapshot and commit actions. Snapshot returns
the original workspace/index identity, HEAD (nullable for an unborn branch), and
tree; commit accepts those exact values and message, revalidates the original
index, and uses component E. It performs no staging or path selection.

Feature helper actions are prepare-feature and commit-feature. Blueprint helper
actions are prepare and apply. Prepare returns a preparation; the existing commit
or apply name finalizes with analysis metadata. A no-op prepare returns the
existing unchanged result and does not ask for a message. Add discard actions
for helper-owned preparations; they never mutate caller files or indexes.

A ready preparation reports preparation_id, workspace, index_file, head, tree,
and required_scope. The response represents staged content awaiting analysis,
not a completed commit or applied blueprint mutation. The caller invokes
commit-staged -p with that exact workspace and index, then submits the full
message and the tree it analyzed. The helper revalidates rather than trusting
an analysis-success boolean. It cannot prove that an LLM ran; invocation is
mandated and verified at the instruction/workflow layer.

Stale HEAD, changed tree, lost ownership, invalid preparation, empty non-merge changes,
unavailable analysis, and hook failures do not produce a successful commit
response. Refreshing a preparation requires another analysis. No code path
silently falls back to fixed operation messages or legacy free-form descriptions.

Preparation cleanup removes only validated helper-owned state. Incomplete
blueprint finalizations use existing recovery rules. Existing hidden CLI clients
and tests must migrate together with shipped command templates; legacy request
shapes fail with an actionable message rather than bypassing the analysis step.

## Verification Considerations

**Covers**: REQ-001, REQ-002, REQ-003, REQ-004, REQ-005, REQ-006

Use real temporary Git repositories for index and commit semantics. Check
unrelated staged changes, partial staging in direct mode, file deletion and
renaming, multiline messages, stale HEAD/tree, wrong tokens, concurrent blueprint
changes, no-op operations, failed hooks, hooks that stage and exit successfully,
and interruption recovery. Verify both install integrations and idempotent
updates of existing context files. Validate generated complete command templates
and tracked installation copies through existing maintainer checks.

## Requirements Coverage

| Spec Requirement | Design Coverage |
|------------------|-----------------|
| REQ-001 | A, B; Decision 1 |
| REQ-002 | B, D; Decision 1 |
| REQ-003 | B, C, D, E; Decision 2 |
| REQ-004 | A, C, D; Decisions 1, 2, 3 |
| REQ-005 | B, C, D, E; Decisions 2, 3, 4 |
| REQ-006 | B, C, D, E; Decisions 1, 2, 3, 4 |

## Decision 5: Distribute the Shared Commit Runtime

**Covers**: REQ-006; **Source**: DEC-001; **Components**: B, E.

`src/codexspec/commit_runtime.py` owns AutomationError, sanitized GitRunner,
message validation, direct snapshots, guarded execution and the standalone JSON
entry point. It imports only the standard library. Automation and staged
preparations import this shared runtime; the hidden CLI delegates to its strict
request dispatcher. Hook wrappers invoke the same absolute Python file using
isolated mode, independent of package installation or Python import paths.

Initialization copies the module byte-for-byte to
`.codexspec/scripts/commit-staged-helper.py`. Claude command installation also
copies it beside the commands, inside the marketplace's declared plugin root.
The loaded plugin uses its own helper; initialized projects use their local
helper; an installed CLI remains available as an alternate entry. No helper
performs semantic generation or stages caller files. Updating the installation
refreshes these copies; command-distribution and package tests detect drift.

Requiring a permanent CLI would remove documented plugin/uvx functionality.
Maintaining a second standalone implementation would risk inconsistent guards;
shipping one complete stdlib module preserves the same implementation everywhere.

## Decision 6: Prepare and Analyze Merge Commits Before Finalization

Use `git merge --no-commit` for synchronization and divergent baseline creation.
Fast-forwards retain the existing post-update check handoff. A pending merge
keeps MERGE_HEAD and the original index; callers resolve/stage conflicts and run
checks before previewing commit-staged. Runtime snapshots bind merge parents as
well as HEAD/tree/index. Empty-diff merges include the default MERGE_MSG in their
snapshot and accept a null message; ordinary empty staging is rejected.

Auto-dev `continue-sync` accepts the exact analysis object and message, fences
ownership, and finalizes through the shared guard. Ordinary workspace `finish`
receives the same fields alongside verified head/tree/checks. Initial fixed
workspace preparation persists `initial-merge.json`; acquisition/blueprint setup
returns a structured pending handoff. `_worktree-helper finish-initial` finalizes
under Git and ownership locks, then setup resumes the same workspace. No lock or
ownership lease is held while the agent analyzes the diff or runs checks.

Merge journals retain whether preparation completed automatically or required
conflict resolution. Finalizing an automatic merge invokes the original
`pre-merge-commit` hook through the guarded pre-commit adapter; that hook may
itself invoke `pre-commit`, so the adapter does not invoke it a second time.
Conflict-resolution commits retain Git's `pre-commit` behavior. Both paths keep
hook refusal, revalidate staged content afterward, and preserve the selection
across pending-state recovery. History-only automatic merges use the same hooks.

Automatic merge adapters also preserve both message-hook arguments: the message
file is MERGE_MSG, and prepare-commit-msg receives the source `merge`. The
adapter copies the proposed message into MERGE_MSG before each message hook and
propagates hook edits back to Git's internal commit message file afterward.
Automatic merge completion invokes `post-merge 0` instead of `post-commit`;
Git retains its native treatment of post-hook exit status. Direct commits and
conflict-resolution commits keep their normal commit hook protocol.

Automatic finalization also supplies the merge invocation's GIT_REFLOG_ACTION
using the pinned merge parent identities. An explicit caller-provided value is
retained, matching native Git. The same environment reaches every delegated
hook and Git's reflog update.

### Plugin-only proactive commit guidance

NEED-001, REQ-001 and DEC-001 also apply before project initialization. The
marketplace explicitly declares its flat command directory. Normal Claude
installation emits `hooks/hooks.json` in that plugin root. An unfiltered
SessionStart command prints the exact shared commit rule used by CLAUDE.md;
startup, resume, clear and compact sessions receive it through Claude's context
injection. This is agent guidance, not a global Git interceptor.

The hook uses exec-form `command`/`args` to call Git with a static, safely quoted
printf alias. Git supplies its shell on every supported Git platform, avoiding
host-shell quoting differences and Python/CLI discovery during session startup.
The command uses no plugin path, project data or hook input and makes no writes.
Git on PATH and Claude's exec-form command-hook support are required. The helper
retains its separate Python 3.11+ requirement when a commit is actually executed.
Installation refuses linked/shared hook destinations; distribution checks compare
the generated hook bytes with normal installation output.

### Automatic-merge hook environment

The automatic-merge adapter preserves pre-creation Git overrides, but restores
the original invocation's GIT_EDITOR and GIT_INDEX_FILE context for completion
and reference-transaction hooks. A configured editor therefore still runs from
post-merge when Git's temporary noninteractive editor setting was only needed
to create the commit. All three merge callers retain this behavior for contentful
and history-only merges.

The guard records the invocation environment before starting Git. Its literal
path mode remains active for helper-selected commit paths, while original hooks
receive the caller's original GIT_LITERAL_PATHSPECS value or absence. Wildcard
and magic-pathspec validation therefore retains native semantics. Automatic
merge hooks also receive the original GIT_AUTHOR_NAME, GIT_AUTHOR_EMAIL and
GIT_AUTHOR_DATE values or absence in every phase; author values synthesized by
the internal git-commit process must not leak into foreign-repository hook work.
Direct and conflict-resolution commit hooks retain Git's normal author context.

### Direct-commit configuration

Direct snapshot and commit execution preserve the invoking repository's
GIT_CONFIG, GIT_CONFIG_COUNT and GIT_CONFIG_PARAMETERS configuration. This keeps
environment-selected hook paths, hook policy values and signing requirements
effective. GitRunner's default remains fully sanitized for foreign/helper-owned
repositories; managed-workspace snapshots and finalizers retain that default.
Repository location and object-directory overrides remain removed, and only the
explicit caller index is restored for direct execution.

### Deferred merge signing and signoff

Automatic finalization carries the current branch's mergeOptions signing and
signoff flags into git commit, in their native order. Git remains responsible
for signatures, signing-key selection, disabling a configured signature, and
committer trailers. Native Git tokenization preserves quoted option values;
message and strategy arguments cannot become commit options accidentally.
Other merge options continue to apply during preparation. Manual and
conflict-resolution commits retain normal git-commit configuration semantics.
A refused signature leaves HEAD unchanged and the prepared merge recoverable.
This preserves CON-002 and REQ-006 for all three automatic merge entry points,
including history-only merges that retain Git's default message.
