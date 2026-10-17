# Design: Project Installation Discovery and Upgrade

**Related Spec**: [spec.md](spec.md)
**Confirmed Requirements**: [requirements.md](requirements.md)
**Created**: 2026-10-17
**Status**: Draft

## Context

The current Typer init command writes scripts, templates, commands, context blocks
and configuration directly. It supports --no-git and has no installation version
or digest baseline. Calling it on a real project before protection checks would
violate the new whole-project unchanged-skip contract. Its existing renderers and
preservation behavior remain useful for producing a proposed update outside the
user project.

## Architecture & Components

### C1: Installation metadata and expected content

New package `src/codexspec/installations/` separates metadata, filesystem inventory,
upgrade planning, release acquisition and CLI presentation. `metadata.py` owns
schema validation, actual-content inspection and atomic publication of
`.codexspec/installation.json`. `render.py` composes existing command/skill,
context-block and helper installers in a temporary directory to derive expected
content for the current runtime, integration set and language. It never imports
maintainer-only modules.

Normal init gets a final metadata hook after its existing installation operations.
It publishes a baseline only if every selected managed artifact matches expected
output. An init that preserves modified/skipped old command files must not declare
the current release fully installed. Existing config semantics and user bodies
remain unchanged. The final hook does not turn arbitrary current bytes into an
expected baseline. Future install metadata is emitted without a manual user step.

Covers: REQ-005, REQ-006, REQ-007, REQ-012, REQ-014.

### C2: Offline discovery

`discovery.py` uses iterative os.scandir traversal with no link following, pruning
.git and .codexspec. Inspect the root itself; retain traversal below discovered
projects. A .codexspec link or non-directory is an inspection issue, not a reason
to follow it. Inventory includes installation path, independently optional version,
consistency status, changed/missing paths and scan issues. Resolve repository group
with read-only Git rev-parse --git-common-dir, without following worktree registry
entries outside scope. Use sanitized Git environment and disable optional locks.
Paths without usable Git remain visible and cannot receive an unsafe upgrade.

Covers: REQ-002, REQ-003, REQ-004, REQ-006, REQ-007.

### C3: Release acquisition

`release.py` uses existing httpx and packaging dependencies to resolve the highest
available non-prerelease, non-development, non-yanked stable release from the
CodexSpec PyPI metadata. Fetch once per invocation. Build a temporary virtual
environment using the running Python and its standard venv/pip support, install
exactly that release from the official index, and verify its installed version.
The environment and interpreter belong to temporary storage, never the global CLI
or a scanned project. Dependency/install/network errors abort before project writes.
Commands are argv arrays, not shell strings; run with no project PYTHONPATH and
sanitized Python, pip and Git environment. Network/install commands have timeouts.

The selected target runtime supplies its own installer behavior through a versioned
private worker module. Unsupported worker protocols or Python incompatibility are
explicit acquisition/preparation failures, never fallback to an older local CLI.

Covers: REQ-008, REQ-009, NFR-002.

### C4: Per-project isolated preparation

`upgrade.py` resolves the existing project.ai and effective interaction language
from configuration; when integration configuration is absent, inspect recognizable
Claude/Codex installed entry directories. Conflicting or unavailable integration
information produces an unchanged skip, not a guessed integration change.

Take a read-only snapshot of relevant managed installation surfaces and config/
context inputs into a temporary directory. Copy files, never hard-link or symlink
user data. Exclude .git, business code, specs, profile records and runtime caches.
Preserve context and runtime-ignore inputs in the snapshot; keep configuration and
constitution entirely outside the worker write scope. Pass resolved integration and
language as explicit arguments. The target worker uses the shared target-release
renderer, calling the same low-level command, integration and resource installers
as init with force enabled, without invoking project initialization or Git.
No target worker receives the real installation directory as a writable destination.

Comparing target output with actual project files produces an explicit update plan: relative path,
expected original state, proposed bytes/mode or deletion, plus final metadata.
Admit only supported managed installation surfaces. Preserve configuration values
and user bodies, and reject plans that alter protected data or unknown paths.
Compare against actual target content for legacy and same-version inconsistent
projects alike. A higher recorded release produces a no-downgrade skip.

Covers: REQ-009, REQ-010, REQ-012, REQ-014, NFR-001.

### C5: Git protection and application

Determine the Git working directory and project-relative prefix through Git, so
nested projects and linked worktrees work. Inspect only paths in the update plan,
including metadata. Stage/index and worktree modifications block the whole project;
existing untracked or ignored affected files also block when they would be
replaced. Missing new destinations are permitted only when the plan can safely
create them. Detect deleted tracked files as local modifications. Missing Git,
unmerged paths, command failure or undecidable filesystem identity means skip.

Do not rely on a broad Git status alone: verify affected tracked content against
the index/HEAD so assume-unchanged or skip-worktree flags cannot hide modifications.
Retain the source/index/HEAD evidence used for the plan. Preflight the complete
set before creating directories or writing anything, including metadata. Repeat
checks after interactive delay and immediately before application. Revalidate
path ancestors and originals before individual writes; links, special files,
shared hard links or changes since preparation are refused.

Application writes prepared bytes with per-file replacement and appropriate
permission preservation, and applies only explicit safe deletions. It never runs
Git mutations. Publish installation metadata last after verifying installed outputs.
An application I/O failure is a failed/possibly partial update, not a safety skip
or a rollback claim; do not publish successful new metadata, report and continue.
There is no user backup/undo system. Remove only tool-owned temporary preparation
artifacts when their invocation finishes.

Covers: REQ-010, REQ-011, REQ-012, REQ-013, NFR-001, NFR-002.

### C6: Public CLI and diagnostics

Expose scan in `src/codexspec/__init__.py` through a small import/delegation function;
`cli.py` handles Rich tables and prompts. Inventory is printed before selection.
Each installation has an independent row, grouped by repository. Without --upgrade,
return immediately after offline inventory. With --upgrade obtain the one target,
then process deterministic path order. Interactive choices are yes/no/all/quit;
all means all remaining eligible projects, never override protection. Noninteractive
--upgrade without --yes reports the missing selection mode rather than silently
consenting or hanging. --yes without --upgrade is an argument error.

Report recorded version, content status, target when known and per-project outcome.
Statuses distinguish unknown version, absent checksum baseline, consistent,
inconsistent, and unreadable/invalid metadata. Corrupt metadata is not absence.
Upgrade outcomes are upgraded, already current, user skipped, protected/uncertain
skip, newer-version skip and failed; summarize upgraded/skipped/failed counts.
An empty result is successful with a clear no-installations message. Exit 2 for
invalid invocation/root, 1 for scan incompleteness, safety skips, acquisition or
project failures, and 0 for successful/no-op/user-declined processing. User-selected
quit reports completed results without implying all projects were processed.
Diagnostics follow the invoking project's interaction language with English fallback,
and include actionable paths/reasons. No new public recovery command is added.

Covers: REQ-001, REQ-004, REQ-013, REQ-014.

## Key Design Decisions

### D1: One metadata document with independent version and checksums

Use `.codexspec/installation.json`, schema 1, storing `installed_version`, `ai`,
`interaction_language`, and a nonempty file/projection list with SHA-256. A missing
version field leaves usable checksum entries verifiable. Missing whole metadata
is legacy; malformed content is explicit uncertainty. Paths are unique normalized
relative POSIX paths beneath approved managed surfaces; reject absolute, parent,
link-escaping, duplicate and self-referential metadata entries. Validate before
reading referenced files. JSON size and entry count are bounded.

The record stores only expected successfully installed artifact digests. Exclude
project-owned specs, profile records, config and constitution from baseline
content. For mixed-ownership CLAUDE.md/AGENTS.md and .codexspec/.gitignore, store
only explicit managed projections, not the entire user-authored file; update
safety still examines the full file if it would change. Complete managed files
use content bytes, with a specified newline-normalized representation for text
installed with platform-specific line endings. The representation is named in the
schema, not guessed by readers. A full update refreshes the complete applicable
inventory; it does not retain stale entries merely because they were once present.

Alternatives: a single version string cannot catch partial discards; hashing all
project files misclassifies user edits. The structured inventory increases internal
implementation work without creating a user-managed workflow.

Covers: REQ-005, REQ-006, REQ-007, REQ-012, REQ-014.

### D2: Prepare in an isolated snapshot; apply a checked plan

The target release owns rendering and compatibility; the invoking release owns
inventory, selection and write protection. Running target init directly against
real projects is rejected because it writes before the affected-set gate. A local
renderer using only new target templates is also rejected: future installer and
skill transformations can change independently of templates. Worker protocol 1
is a hidden compatibility surface, not a public subcommand. Temporary files are
preparation inputs/outputs, not retained recovery snapshots.

Covers: REQ-008–012, REQ-014, NFR-001, NFR-002.

### D3: Git evidence and content consistency answer different questions

The manifest detects missing or changed installation content; Git protects local
work. A checksum difference alone is not an unsafe user modification and never
authorizes overwrite. A clean tracked file differing from target can be updated;
an affected staged/unstaged/untracked modification blocks. A clean same-version
partial discard can therefore be reinstalled. Metadata changes themselves join
the affected-set check if the update would overwrite them.

Covers: REQ-006, REQ-009–011.

### D4: Compatibility comes from current project choices

Select integration and language per project, not per caller or global CLI default.
Keep configuration bytes/values and custom context text. Installed-artifact metadata
is refreshed by init only after expected-content verification, including cases
where init's existing nonforce behavior preserves files. Do not automatically add
missing integrations, recreate deleted user-owned content, or remove unrelated
extension files. Unknown ownership leads to a report-only skip.

Covers: REQ-005, REQ-010–012, REQ-014.

## Data and Private Worker Contracts

Covers: REQ-005, REQ-008–013.

- `Installation`: path, repository group or none, optional recorded Version,
  consistency state, issues, changed/missing managed paths.
- `PreparedChange`: relative path, original existence/kind/content/mode, resulting
  bytes or deletion, ownership category. Metadata is explicit and ordered last.
- `UpgradePlan`: protocol 1, target release, integration/language, project input
  snapshots, complete changes, expected resulting metadata.
- Worker receives only an isolated snapshot and output directory, validates
  protocol and reports success/failure plus its own installed release. Parent
  requires matching release/protocol and validates every returned path and byte
  payload before turning it into a real-project plan.
- `Result`: path, outcome, reason, relevant paths, target release, partial flag.

## Sequence and Boundaries

Covers: REQ-001–014, NFR-001, NFR-002.

1. Discover and report offline installation facts.
2. If upgrade requested, resolve and prepare one isolated target runtime.
3. For each selected project, snapshot inputs and prepare target output outside it.
4. Build/validate the complete plan; inspect all affected Git/filesystem states.
5. On unsafe/unknown state report skip without project writes; otherwise apply.
6. Verify final artifacts and publish metadata last; summarize all results.

This is not a whole-repository snapshot, Git worktree creation or automatic Git
commit. If an external process changes inputs, revalidation refuses stale plans;
application failures after writes report partial completion. No system can promise
multi-file atomicity against arbitrary concurrent filesystem writers without a
shared locking discipline; the implementation must not claim one.

## Verified Dependencies and References

Covers: REQ-005, REQ-008, REQ-012.

- Existing PyPI dependencies include httpx, packaging and PyYAML; no new network
  dependency is required. Standard-library venv/pip isolation is the execution
  mechanism; unavailable environment preparation is reported before writes.
- Existing `commands/installer.py`, `integrations/codex.py`, `commit_runtime.py`,
  `review_standards.py` and managed-block injectors provide rendering behavior.
- [PyPI JSON API](https://docs.pypi.org/api/json/) documents release metadata,
  distribution digests and yanked flags; release acquisition uses HTTPS and exact
  version pinning. [pip install](https://pip.pypa.io/en/stable/cli/pip_install/)
  documents installing a pinned package through the selected environment.

## Requirements Coverage

| Spec Requirement | Design Coverage |
| --- | --- |
| REQ-001 | C6 |
| REQ-002 | C2 |
| REQ-003 | C2 |
| REQ-004 | C2, C6 |
| REQ-005 | C1, D1, D4 |
| REQ-006 | C1, C2, D1, D3 |
| REQ-007 | C1, C2, D1 |
| REQ-008 | C3, D2 |
| REQ-009 | C3, C4, D2, D3 |
| REQ-010 | C4, C5, D2–4 |
| REQ-011 | C5, D2–4 |
| REQ-012 | C1, C4, C5, D1, D2, D4 |
| REQ-013 | C5, C6 |
| REQ-014 | C1, C4, C6, D1, D2, D4 |
| NFR-001 | C4, C5, D2 |
| NFR-002 | C3, C5, D2 |
