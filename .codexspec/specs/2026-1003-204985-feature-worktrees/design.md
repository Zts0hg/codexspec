# Design Document: Feature Worktrees

**Related Spec**: [spec.md](spec.md)
**Confirmed Requirements**: [requirements.md](requirements.md)
**Created**: 2026-10-03
**Status**: Reviewed — PASS

## Context

The specification defines three workspace roles: one worktree per ordinary feature, one dedicated
workspace for standalone project maintenance, and the existing fixed `blueprint/auto-dev` workspace.
They share an external parent. Ordinary isolation is configurable and defaults on; installation
is exempt. Ordinary baselines combine current available local and remote main-branch history.

This design records the target architecture. DEC-007 resolves configuration authority: settings
remain checkout-local, and a routed write takes effect in its destination checkout first.

## Architecture & Components

### C1. Repository locator and workspace identity

- **Responsibility**: Derive the primary repository location, common Git directory, invoking
  checkout, registered worktrees, main-branch refs, and shared external parent.
- **Repository fit**: Refine the existing `locate_repository`, worktree parser, and sanitized
  `GitRunner` in `src/codexspec/automation.py`; extract reusable discovery into a shipping module
  if necessary to avoid coupling ordinary workflows to auto-dev ownership.
- **Interface**: A read-only repository context, derived from Git registration rather than caller
  directory naming. An ordinary repository's primary checkout anchors the parent; a bare
  repository's registered repository directory anchors it. The directory basename plus
  `-codexspec-worktrees` yields the common parent. All linked callers resolve the same result.
- **Identity**: Ordinary branch/worktree identities use the existing full feature name. The fixed
  auto-dev branch and basename remain unchanged. The maintenance branch is `codexspec/maintenance`, with basename
  `worktree-for-codexspec-maintenance`, separate from every ordinary feature identity.
- **Covers**: REQ-003, REQ-004, REQ-006, REQ-012, NFR-002

### C2. Worktree configuration policy

- **Responsibility**: Read default-enabled isolation, expose its effective value, and write the
  user's selected value through existing CLI and agent configuration entry points.
- **Surface**: `workflow.worktrees` in `.codexspec/config.yml`, with a `codexspec config
  --worktrees on|off` option and the corresponding `/codexspec:config` selection. These names are
  design-level interface choices within the confirmed configurable-switch requirement.
- **Existing facts**: `config()` in `src/codexspec/__init__.py` currently reads and writes
  `Path.cwd() / '.codexspec' / 'config.yml'`. Agent templates also read checkout-local configuration.
- **Authority**: Read the switch from the invoking checkout before deciding whether to route. A
  routed configuration edit then reads and updates the destination's config, including toggling
  relative to the destination's current value. Print the exact destination and explain that other
  checkouts acquire the setting through Git integration. Do not add a shared override or modify
  the main checkout's configuration to make the toggle appear global.
- **Value contract**: Follow the existing opt-out convention: only literal YAML `false` disables;
  absent settings default on. CLI writes unquoted booleans and preserves unrelated configuration.
  Display-only config requests remain read-only in the invoking checkout.
- **Covers**: REQ-001, REQ-002, REQ-011, REQ-016

### C3. Ordinary and maintenance workspace manager

- **Responsibility**: Validate, create, or reuse the correct workspace without switching the main
  checkout or adopting unrelated occupied paths.
- **Interface**: A shipping Python service, exposed through a hidden helper like the existing
  automation helpers, accepts a validated role and optional full feature identity. It returns
  repository identity, workspace path, branch, artifact path, and preparation state.
- **Creation**: Use the existing feature-name contract. Check registration, expected path, and
  branch together before mutation. Serialize conflicting create operations using a short lock in
  the common Git directory; unrelated feature development remains independent.
- **Reuse**: A verified existing feature workspace is reused with its files and branch intact.
  Creation-time selection is not rerun as a reset of an existing feature. A directory alone is
  insufficient evidence of ownership or readiness.
- **Maintenance**: Standalone project-level modifications resolve a dedicated maintenance worktree
  under the same parent. Repeated operations reuse it; active ordinary feature operations remain
  in their current feature workspace.
- **Lifecycle**: No completion-triggered merge or deletion. Failed preparation must remain
  distinguishable from a ready workspace on subsequent calls.
- **Covers**: REQ-004, REQ-005, REQ-006, REQ-011, REQ-014, REQ-015, NFR-001

### C4. Baseline selection and verification handoff

- **Responsibility**: Fetch when configured, compare available main-branch histories by ancestry,
  create the workspace on the selected committed baseline, and reconcile divergence there.
- **Repository fit**: Reuse applicable behavior from `_select_initial_refs` and the sanitized Git
  runner. Do not reuse fixed-workspace cleanup that force-removes a worktree after a failed initial
  merge; ordinary workspace failures must not discard user work.
- **Interface**: Preparation reports `ready`, `merge_requires_resolution`,
  `merge_requires_verification`, or `blocked`, together with selected commit identities and any
  fetch warning. An agent-owned continuation handles project-specific conflict repair and required
  verification before declaring a merged baseline ready.
- **Ref handling**: Fetch updates remote-tracking history, not the caller's checked-out branch.
  Fetch errors leave a warning and permit use of still-valid local refs. No remote uses the local
  main branch. No usable baseline produces an explicit failure. A failed fetch never permanently
  disables later attempts.
- **Readiness**: Feature artifact creation follows successful baseline preparation. A merge result
  is not ready solely because `git merge` exits successfully: required project verification must
  pass. Interrupted or failed preparation cannot masquerade as a ready feature on reuse.
- **Covers**: REQ-007, REQ-008, REQ-009, REQ-010, REQ-014, NFR-001, NFR-003

### C5. Command and script workspace handoff

- **Responsibility**: Carry the resolved absolute workspace through artifact writes, source edits,
  tests, repairs, and later SDD stages.
- **Authoring locations**: Update opted-in command sources in
  `internal/command_templates/sources/` and shared fragments under
  `internal/command_templates/fragments/`; render complete distribution templates with the existing
  maintainer renderer. Bash and PowerShell entry scripts are authored under `scripts/bash/` and
  `scripts/powershell/`. Derived `.agents` and `.claude` copies are regenerated, not hand-edited.
- **Execution contract**: A shell subprocess changing directory cannot change the agent session's
  working directory. Helpers must return an absolute workspace path; callers explicitly use it
  for subsequent tool invocations and resolve artifact paths relative to that workspace.
- **Entry routing**: Ordinary feature creation resolves/prepares the worktree before publishing
  requirements. Continuation uses feature identity to locate the existing worktree. Project-level
  writes use C3's maintenance routing. Auto-dev delegation retains its existing dedicated workspace
  and must not trigger a second ordinary feature workspace.
- **Input validation**: Commands that depend on the caller's staged or uncommitted state must retain
  that source identity through routing. A generic change of working directory is not sufficient.
  The write router does not itself authorize staging, stashing, copying, or discarding caller work;
  existing command-specific input contracts remain applicable.
- **Covers**: REQ-005, REQ-006, REQ-011, REQ-012, REQ-014, NFR-001, NFR-003

### C6. Installation, automation, and distribution integration

- **Responsibility**: Apply the new parent to the existing shared automatic-development locator,
  preserve its fixed branch/worktree and sequential model, and preserve the explicit installation
  exemption for both first-time and update `init` runs.
- **Configuration integration**: Extend existing configuration display/set entry points and fresh
  project defaults, preserving unrelated settings during installation updates. Effective switch
  lookup follows C2 and DEC-007.
- **Distribution**: All runtime code belongs in `src/codexspec/` or existing shipping scripts and
  complete templates. Internal fragments and rendering tools remain maintainer-only. Existing
  installer paths do not gain awareness of fragment expansion.
- **Covers**: REQ-001, REQ-002, REQ-012, REQ-013, NFR-001

## Key Design Decisions

### Decision 1: Reuse deterministic Git services and agent-owned interpretation

- **Context**: Worktree identity and ancestry require deterministic Git behavior; project-specific
  conflict resolution and verification are already agent-owned in automatic development.
- **Decision**: Put ordinary workspace discovery and preparation in shipping Python services, while
  command templates coordinate interpretation, verification, and stage handoff.
- **Alternatives**: Duplicating all Git logic independently in Bash, PowerShell, and each agent
  template would create different identity and baseline rules. A fully autonomous Python developer
  would exceed the package's existing responsibilities.
- **Trade-offs**: A helper interface and explicit preparation states are necessary, but platform
  wrappers can remain thin and share behavior.
- **Covers**: REQ-003, REQ-004, REQ-008, REQ-009, REQ-010, REQ-014, NFR-002

### Decision 2: Identify repositories and workspaces through Git registration

- **Context**: The project supports both ordinary checkouts and bare repositories with linked
  worktrees; the invoking directory cannot determine the parent or role by itself.
- **Decision**: Derive the parent from the primary registered repository location and validate the
  expected worktree path and branch against the repository's worktree registration.
- **Alternatives**: Appending a suffix to every invoking checkout produces nested or inconsistent
  workspace parents. Accepting any existing directory risks writing into an unrelated checkout.
- **Trade-offs**: Invalid or ambiguous registration must fail explicitly, preserving the user's
  confirmed no-fallback rule.
- **Covers**: REQ-003, REQ-004, REQ-006, REQ-014, NFR-002

### Decision 3: Separate initial baseline preparation from continuation

- **Context**: New features require ancestry-aware main-branch preparation; existing features may
  contain committed and uncommitted work that must be preserved.
- **Decision**: Select/merge the initial baseline only for creation. Reuse validates identity and
  unfinished preparation state without resetting completed feature work to main.
- **Trade-offs**: Readiness must survive interruption so a failed merge or verification is not
  incorrectly accepted as an existing ready workspace.
- **Covers**: REQ-006, REQ-007, REQ-009, REQ-010, REQ-014, REQ-015

### Decision 4: Keep configuration authority checkout-local

- **Context**: Main-checkout project writes route to maintenance, but the existing settings are
  checkout-local. The user explicitly confirmed this behavior in requirements DEC-007.
- **Decision**: Route using the invoking checkout's switch, then perform the config operation on
  the destination's own file. Report the destination and effective scope. Future invocations read
  their own checkout again; do not persist a shared effective override.
- **Alternatives**: An immediately effective repository-wide setting was rejected by the user.
- **Trade-offs**: Disabling from main modifies maintenance; main remains enabled until its own
  versioned configuration receives the change. This is an intentional, confirmed behavior.
- **Covers**: REQ-001, REQ-002, REQ-011, REQ-016

### Decision 5: Preserve state-dependent command inputs rather than silently moving them

- **Context**: `commit-staged` forbids changes to what is staged, while reviews and reverse
  specification can read caller-owned uncommitted state. Worktree routing must not substitute
  another checkout's input or transfer changes without authorization.
- **Decision**: Read-only operations retain their original read target. An artifact-only report may
  be written to the resolved output workspace while keeping explicit original input paths. An
  executable operation such as committing the caller's staged changes cannot be redirected to a
  different index; if it would violate checkout isolation, stop with the original source and
  required target identified. Source-code repairs must operate on the selected feature workspace;
  any incompatible caller-owned state is reported instead of implicitly copied or stashed.
- **Trade-offs**: Some operations launched against main's existing uncommitted state require the
  user to establish the intended feature workspace first. This preserves both the confirmed
  no-main-write constraint and existing command input contracts.
- **Covers**: REQ-005, REQ-006, REQ-011, REQ-014, NFR-001, NFR-003

## Interface and State Contracts

### Internal workspace helper

The shipping `src/codexspec/worktrees.py` service is exposed as `codexspec _worktree-helper`.
Use structured JSON output, never shell fragments that callers must evaluate. Python owns feature
name normalization/identity generation for enabled creation; platform wrappers preserve existing
short-name arguments and explicit disabled behavior.

- `create --name <short-name>` allocates an ordinary feature identity, prepares its worktree, and
  creates the requirements skeleton only after readiness. Return absolute `workspace`,
  `feature_dir`, `requirements_file`, full `branch`, `feature_id`, `status`, and `warnings`.
- `resolve --feature <full-feature-name>` validates and returns an existing ordinary workspace.
  No new baseline selection, branch switching, fetch, or reset is performed for ready reuse.
- `maintenance` resolves or creates the dedicated maintenance worktree. Existing maintenance state
  is preserved. A new maintenance worktree uses the same committed-history preparation service;
  a standalone CLI cannot autonomously repair conflicts, so it reports the required continuation.
- `finish --feature <full-feature-name> --verification <json-file>` completes interrupted divergent
  baseline preparation only when both recorded baseline commits are ancestors of HEAD, no merge
  or unresolved index remains, and successful project-verification evidence matches the current
  HEAD and tracked-tree state. It then publishes requirements if absent. Maintenance preparation
  uses its explicit role instead of a feature ID.
- Errors return an explicit code and diagnostic; a partial preparation result is not reported as
  ready. There is no implicit `--force`, old-directory migration, or main-checkout fallback.

Verification evidence carries the checked commit/tree identity and commands with exit codes. It is
an agent handoff record, not a mechanism to run arbitrary commands from JSON. The agent performs
conflict repair, merge completion, and project verification in the returned workspace before asking
the helper to validate readiness. Configuration CLI writes stop on non-ready preparation and report
that path rather than inventing project-specific verification.

**Covers**: REQ-004 through REQ-011, REQ-014, REQ-015, NFR-003

### Durable preparation metadata

Store minimal preparation records under `<git-common-dir>/codexspec-workspaces/`, outside working
files. Key by validated workspace identity; record role, expected path, branch, selected baseline
commit(s), and preparation state. Use atomic replacement and a short common-directory lock. Record
intent before creating the branch/worktree so retry can distinguish owned partial creation from an
unrelated occupied path. Git registration and actual branch/commit state remain authoritative;
metadata never licenses overwriting an unrelated checkout. A ready registered feature requires no
baseline refresh. A partially created workspace must resume the original preparation rather than
silently declaring success or allocating a duplicate feature on retry.

**Covers**: REQ-004, REQ-006, REQ-010, REQ-014, NFR-001

### Runtime configuration and installed assets

A new Git worktree contains committed files only. Helpers are invoked through the installed
CodexSpec executable, so they do not depend on the new checkout containing a copied shell script.
If installation assets or project scaffolding required by a later stage are absent, use the normal
installer targeted explicitly at the new worktree, preserving any existing project-authored files.
Do not copy arbitrary uncommitted source/configuration from the invoking checkout as a substitute
for committed baseline selection. After setup, commands use the destination's configuration, with
the documented default behavior when the isolation setting is absent. An unavailable required
runtime or unusable setup stops with a diagnostic rather than reverting to main writes.

**Covers**: REQ-001, REQ-005, REQ-007, REQ-013, REQ-014, REQ-016

### Mutating entry-point inventory

- CLI `config`: read-only display stays in place; setters resolve the write destination before
  changing config or regenerating command frontmatter.
- CLI `_distill-review-helper`: resolve project write destination before creating drafts, runtime
  files, or a mutable review session; display the resolved project to the user.
- Bash/PowerShell feature creation: enabled creation delegates to the helper and returns absolute
  paths; explicit disabled mode preserves current-checkout feature creation.
- All distributed command sources: a shared workspace section applies before any write. New
  `specify`/`quick` features create a workspace; explicit feature paths and branch matches resolve
  continuation; standalone project writes use maintenance. Read-only inputs keep their provenance.
- `blueprint`/`auto-dev` and delegated stages: use the fixed shared workspace; only their parent
  location changes. No new ordinary feature worktree is created for a delegated requirement.
- `init`: both first-time and update installation retain their explicitly selected target.

**Covers**: REQ-001, REQ-002, REQ-005, REQ-006, REQ-011, REQ-012, REQ-013, REQ-016

## Sequence and Data Flow

### Ordinary feature creation

1. Resolve repository identity and read the effective isolation switch (checkout-local authority).
2. If disabled, retain the existing ordinary creation behavior. Installation and automatic
   development use their explicit routing exceptions.
3. If enabled, allocate the full feature identity and validate its external destination.
4. Fetch if configured, warn on failure, and select available main-branch history by ancestry.
5. Create the feature branch/worktree. Reconcile divergence and verify the resulting baseline.
6. Only when ready, create feature requirements and return absolute workspace/artifact paths.
7. Subsequent stages execute in the same worktree. Completion retains it.

**Covers**: REQ-001 through REQ-010, REQ-014, REQ-015, NFR-001, NFR-003

### Project maintenance

1. Resolve the invoking context and effective switch (checkout-local authority).
2. Use the active feature workspace when present; otherwise ensure the dedicated maintenance
   worktree for an isolated standalone write.
3. Apply the operation against that target and report its actual destination.
4. Report the destination. Read-after-write uses that destination's configuration; the next
   independent invocation reads its own checkout, in accordance with DEC-007.

**Covers**: REQ-001, REQ-002, REQ-011, NFR-001

## Risks and Trade-offs

| Risk | Concrete consequence | Design treatment | Covers |
|---|---|---|---|
| Routed config write and config read use different checkouts | A reported toggle may appear ineffective from main | Use DEC-007 and show destination plus checkout-local scope | REQ-001, REQ-002, REQ-011 |
| Command reads caller state after redirecting to another worktree | Staged diff or uncommitted-code meaning changes | Preserve source identity and validate command-specific input before writes | REQ-005, REQ-011, NFR-001 |
| Worktree exists after failed baseline preparation | Continuation bypasses unresolved merge or failed checks | Track and revalidate readiness | REQ-006, REQ-010, REQ-014 |
| Shell changes cwd but agent tools do not | Later writes return to main checkout | Absolute workspace handoff through every stage | REQ-005, NFR-001 |
| Existing fixed-workspace helper assumes a non-bare invoking checkout | Direct bare-repository invocation cannot locate the project | Test discovery from linked worktrees and bare repository roots where applicable | REQ-003, NFR-002 |

## Open Questions

None. The user resolved OPEN-DESIGN-001 by confirming checkout-local configuration in DEC-007.

## Requirements Coverage

| Spec Requirement | Design Coverage | State |
|---|---|---|
| REQ-001 | C2, C6, Decision 4 | Defined by DEC-007 |
| REQ-002 | C2, C6, Decision 4 | Defined by DEC-007 |
| REQ-003 | C1, C3, Decision 2 | Drafted |
| REQ-004 | C1, C3, Decision 1 | Drafted |
| REQ-005 | C3, C5, creation flow | Drafted |
| REQ-006 | C1, C3, C5, Decision 3 | Drafted |
| REQ-007 | C4, Decision 3 | Drafted |
| REQ-008 | C4, Decision 1 | Drafted |
| REQ-009 | C4, Decision 1 | Drafted |
| REQ-010 | C4, Decision 3 | Drafted |
| REQ-011 | C2, C3, C5, maintenance flow | Defined by DEC-007 |
| REQ-012 | C1, C5, C6 | Drafted |
| REQ-013 | C6 | Drafted |
| REQ-014 | C3, C4, C5, Decisions 2–3 | Drafted |
| REQ-015 | C3, Decision 3 | Drafted |
| REQ-016 | C2, Decision 4, runtime configuration contract | Defined by DEC-007 |
| NFR-001 | C3–C6, creation and maintenance flows | Drafted |
| NFR-002 | C1, Decisions 1–2 | Drafted |
| NFR-003 | C4, C5 | Drafted |
