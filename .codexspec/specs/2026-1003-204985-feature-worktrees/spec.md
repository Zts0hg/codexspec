# Feature Specification: Feature Worktrees

**Feature Branch**: `2026-1003-204985-feature-worktrees`
**Created**: 2026-10-03
**Status**: Reviewed — PASS
**Authority**: [Confirmed requirements](requirements.md), final confirmation on 2026-10-03

## Context and Goals

CodexSpec's ordinary feature creation currently writes a requirements directory and switches the
invoking checkout to a new branch. Separate features therefore compete for that checkout. The
existing `blueprint/auto-dev` workflow already uses one dedicated branch and external worktree.

This feature makes worktree isolation the default for ordinary development and project maintenance.
Each ordinary feature gets its own worktree before any feature artifact is written. Project-level
changes use the active feature worktree or a dedicated maintenance worktree. The existing automatic
development workflow keeps its fixed shared workspace, under the new common parent directory.

The intended outcome is simultaneous ordinary feature development without switching or editing the
main checkout, while retaining the existing sequential automatic development model.

### Terms

- **Main branch**: The repository's default development branch, which need not be named `main`.
  Local and remote versions are compared by commit ancestry.
- **Main checkout**: The primary checkout of an ordinary non-bare repository, independent of which
  branch it currently has checked out. A bare repository has a repository directory and linked
  worktrees rather than a primary working checkout.
- **Worktree parent**: The external `<project-or-repository-name>-codexspec-worktrees` directory
  beside the main checkout, or beside the repository directory in a bare-repository layout.
- **Feature workspace**: The ordinary feature's worktree and its
  `.codexspec/specs/<feature-id>-<feature-name>/` artifact directory. The worktree basename is the
  same full feature name; these two directories have different roles and are not interchangeable.
- **Maintenance worktree**: A dedicated worktree for standalone configuration, constitution, profile,
  and other project-level modifications that have no active ordinary feature workspace.
- **Shared automatic-development worktree**: `worktree-for-codexspec-auto-dev`, on the existing fixed
  branch `codexspec/auto-dev`, containing the shared blueprint and all automatic development.

## User Scenarios and Testing

### User Story 1 — Develop independent ordinary features (P1)

A developer starts two ordinary features from the same repository. Each feature has its own working
directory, branch context, requirements, later documents, code, and tests.

**Independent Test**: Start two features from one checkout and compare their worktree registrations,
artifact locations, and the invoking checkout's branch, index, and working files before and after.

**Acceptance Scenarios**:

1. **Given** an initialized Git project without the new setting, **when** a developer starts an
   ordinary feature, **then** isolation is enabled, its worktree exists before the first requirements
   write, and the full workflow writes there.
2. **Given** two distinct feature identities, **when** both are developed, **then** their worktrees
   have distinct `<feature-id>-<feature-name>` basenames under one worktree parent.
3. **Given** an existing feature workspace, **when** development continues from another checkout,
   **then** the same registered workspace is reused without restarting it from the main branch.
4. **Given** uncommitted changes in the main checkout, **when** a new feature is created,
   **then** its baseline comes from committed main-branch history and the invoking checkout's
   existing changes and checked-out branch are preserved.

### User Story 2 — Start from current available main-branch history (P1)

A developer starts a feature from the newer local or remote main-branch history without manually
coordinating those branches.

**Independent Test**: Use temporary local repositories and a local remote with equal, ancestor,
descendant, and diverged branch histories, including deliberately misleading commit timestamps.

**Acceptance Scenarios**:

1. **Given** a configured remote, **when** creating a new feature, **then** CodexSpec attempts to
   fetch before selecting the baseline.
2. **Given** one main-branch tip contains the other, **when** selecting the baseline, **then** the
   descendant is used regardless of commit timestamps. Equal tips select the same commit.
3. **Given** diverged main branches, **when** preparing the feature, **then** both histories are
   merged inside the new feature worktree and required project verification passes before feature
   development begins.
4. **Given** unresolved merge conflicts or failed baseline verification, **when** preparing the
   feature, **then** development stops with an explicit diagnostic.
5. **Given** a failed fetch and usable local refs, **when** preparing a feature, **then** CodexSpec
   reports the failure and potentially stale remote information, and applies the same ancestry
   comparison to the locally available refs. The next creation attempts fetch again.
6. **Given** no configured remote, **when** preparing a feature, **then** the local main branch is
   used. If no valid baseline can be determined, creation stops explicitly.

### User Story 3 — Maintain project settings without editing the main checkout (P1)

A developer updates project configuration, constitution, or accumulated profile knowledge while
keeping all development and maintenance writes outside the main checkout.

**Independent Test**: Run a representative project-level write from a feature worktree and from the
main checkout, and verify the destination and the main checkout's preserved contents.

**Acceptance Scenarios**:

1. **Given** an active ordinary feature worktree, **when** a project-level document or setting is
   modified, **then** the change is made in that feature worktree.
2. **Given** a standalone project-level write invoked from the main checkout, **when** isolation is
   enabled, **then** a dedicated maintenance worktree is used under the worktree parent.
3. **Given** `codexspec init` explicitly targets a checkout, **when** it initializes or updates the
   installation, **then** it writes to that selected checkout without worktree redirection.

### User Story 4 — Configure isolation while retaining automatic development (P2)

A developer can opt out of ordinary worktree isolation without changing the existing shared
`blueprint/auto-dev` model.

**Independent Test**: Exercise absent, enabled, and disabled settings through existing configuration
entry points and invoke ordinary, maintenance, installation, and automatic-development operations.

**Acceptance Scenarios**:

1. **Given** isolation is explicitly disabled, **when** an ordinary feature or project-maintenance
   command writes, **then** it follows its existing current-checkout behavior.
2. **Given** either switch state, **when** `blueprint/auto-dev` runs, **then** it uses its fixed
   shared branch/worktree, with basename `worktree-for-codexspec-auto-dev` under the new parent.
3. **Given** isolation is enabled in main, **when** a disable request from main is routed to
   maintenance, **then** maintenance becomes disabled while main remains enabled until its own
   configuration receives the change. The result identifies the destination and local scope.
4. **Given** completed feature development, **when** the workflow finishes, **then** the worktree is
   retained without an automatic merge back to the main branch or automatic deletion.

### Edge Cases

- An occupied target directory is not overwritten or silently adopted as a feature workspace.
- A failed workspace creation does not activate the previous in-place creation fallback.
- A call from a nested directory or another linked worktree resolves the same repository-wide parent.
- Bare repositories with multiple linked worktrees are supported; no fictitious main working
  checkout is required for that layout.
- A failed fetch does not make an absent or unusable baseline valid; the explicit baseline failure
  rule still applies.
- Old shared-worktree locations receive no compatibility lookup or migration support.

## Requirements

All requirements below describe the target behavior. The isolation-specific rules apply while the
new switch is enabled, except that the shared `blueprint/auto-dev` workspace and its new location
apply regardless of that switch, and installation remains explicitly exempt.

### Functional Requirements

- **REQ-001**: Provide a configurable worktree-isolation switch through the existing configuration
  entry points. It MUST default to enabled when absent and support explicit enabling and disabling.
  - Sources: NEED-002
- **REQ-002**: When the switch is disabled, ordinary development and project maintenance MUST use
  their existing current-checkout behavior. Disabling MUST NOT disable or split the fixed shared
  `blueprint/auto-dev` worktree.
  - Sources: NEED-002, CON-001
- **REQ-003**: Resolve one repository-wide worktree parent named
  `<project-or-repository-name>-codexspec-worktrees`, outside and beside the main checkout. For a
  bare repository, resolve the equivalent location beside its repository directory. The result MUST
  be consistent across calls from any linked worktree.
  - Sources: DEC-001, DEC-006
- **REQ-004**: Each ordinary feature MUST have its own worktree whose basename is the full
  `<feature-id>-<feature-name>`. Distinct features MUST use distinct workspaces under REQ-003.
  - Sources: NEED-001, DEC-006
- **REQ-005**: Create the ordinary feature worktree before the first write to its requirements
  document. All later feature documents, code, tests, and repairs MUST be produced in that worktree.
  Workspace selection MUST remain effective across subsequent SDD stages and their write operations.
  - Sources: NEED-003
- **REQ-006**: Continuing an ordinary feature MUST resolve and reuse its existing valid worktree,
  including when invoked from another checkout. A continuation MUST NOT be treated as a new feature
  created from the main branch.
  - Sources: NEED-003, DEC-006
- **REQ-007**: New ordinary feature baselines MUST come from committed local and remote main-branch
  history, not the invoking checkout's arbitrary feature branch or uncommitted changes.
  - Sources: NEED-004
- **REQ-008**: Before creating an ordinary feature worktree, attempt to fetch the configured remote
  main branch. On fetch failure, report the failure and potentially stale remote information,
  continue using valid locally available main-branch refs, and retry fetch on the next creation.
  - Sources: DEC-003
- **REQ-009**: Compare the available local and remote main-branch tips by ancestry, not commit
  timestamps. Use the descendant if one contains the other, or the common tip if equal. With no
  remote configured, use the local main branch. If a valid baseline cannot be determined, stop.
  - Sources: NEED-004, DEC-002, CON-002
- **REQ-010**: When both main-branch histories have unique commits, merge both inside the new feature
  worktree. Use the merge result as the development baseline only after required project
  verification passes. Stop if conflicts cannot be resolved or verification fails.
  - Sources: DEC-002
- **REQ-011**: Project-level modifications, including configuration, constitution, and profile
  updates, MUST use the active ordinary feature worktree when one exists. Standalone modifications
  invoked from the main checkout without an active feature MUST use a dedicated maintenance
  worktree under the common worktree parent.
  - Sources: DEC-004, DEC-001
- **REQ-012**: `blueprint/auto-dev` MUST retain the fixed branch `codexspec/auto-dev` and shared
  worktree basename `worktree-for-codexspec-auto-dev`, located under REQ-003's parent. They MUST NOT
  create or switch to per-requirement worktrees or branches. Preserve their existing shared
  blueprint and sequential automatic-development model.
  - Sources: CON-001, DEC-001
- **REQ-013**: First-time initialization and subsequent installation updates through `codexspec init`
  MAY write to the checkout explicitly selected by the user. They MUST NOT be redirected by the
  worktree-isolation rule.
  - Sources: DEC-005
- **REQ-014**: Workspace-creation failure, an occupied target path, or inability to determine a valid
  baseline MUST produce an explicit error. Do not overwrite an existing directory or fall back to
  modifying the main checkout. Valid reuse under REQ-006 is distinct from adopting an occupied path.
  - Sources: CON-002, NEED-003
- **REQ-015**: Retain feature worktrees after completion. Do not automatically merge feature work
  back into the main branch or delete worktrees as part of completion.
  - Sources: OUT-002

- **REQ-016**: Resolve the isolation switch from the invoking checkout's configuration. A routed
  configuration write changes the destination worktree's configuration and takes effect there
  first; other checkouts receive the setting through Git integration. Do not introduce an immediate
  repository-wide override. Configuration results MUST identify the actual destination and scope
  so that a routed write is not reported as changing the main checkout's effective setting.
  - Sources: DEC-007, NEED-002, DEC-004

### Non-Functional Requirements

- **NFR-001 — Main-checkout isolation**: Enabled development and maintenance operations MUST preserve
  the main checkout's working files, staged content, and checked-out branch. Creating worktrees and
  fetching may update shared Git metadata and refs; these are necessary Git operations rather than
  edits to the main checkout's working files. REQ-013 is the explicit installation exception.
  - Sources: NEED-003, DEC-004, CON-002, DEC-005
- **NFR-002 — Repository-layout consistency**: Ordinary repositories and bare repositories with
  linked worktrees MUST satisfy the same feature identity, shared-parent, and reuse behavior.
  - Sources: DEC-006
- **NFR-003 — Actionable failures**: A stopped operation MUST identify the failed creation, occupied
  path, missing/invalid baseline, unresolved merge, or failed verification sufficiently for the
  user to understand why development did not start. Fetch fallback MUST disclose stale remote
  information and remain distinguishable from successful refresh.
  - Sources: CON-002, DEC-002, DEC-003

### Key Entities

- **Repository identity**: The Git repository shared by its registered worktrees, used to resolve
  one external parent independent of the invoking directory.
- **Feature identity**: The existing Feature ID plus normalized feature name, used to associate an
  ordinary feature's artifacts and worktree.
- **Workspace role**: Ordinary feature, standalone project maintenance, or shared automatic
  development. Roles determine which confirmed routing rule applies.
- **Baseline**: A committed main-branch tip or verified merge of local and remote main-branch
  histories, used only when starting new ordinary feature development.

## Confirmed Constraints and Decisions

- Worktree isolation is enabled by default and covers feature artifacts as well as source changes.
- Configuration opt-out affects ordinary development and maintenance, while automatic development
  retains its existing fixed shared workspace.
- All managed workspace roles use the unified external parent; the ordinary basename is the full
  feature identity, and the automatic-development basename remains fixed.
- Initial feature baselines use ancestry, with fetch fallback and merge-on-divergence as specified.
- Installation is permitted in the explicitly selected checkout.
- Creation failures do not authorize a fallback to main-checkout edits.
- Old-directory migration, automatic integration back to main, and completion-time deletion are
  excluded.

## Success Criteria

- **SC-001**: Two ordinary features can complete document/code writes in separate worktrees while a
  before/after comparison shows no changes to the main checkout's files, index, or branch.
- **SC-002**: Every confirmed baseline case (equal, ahead on either side, diverged, offline fetch
  failure, no remote, unavailable baseline) produces its specified outcome in controlled Git tests.
- **SC-003**: Calls from the primary checkout and different linked worktrees resolve the same parent
  and the same existing feature workspace, including for a bare repository.
- **SC-004**: Configuration opt-out, project-maintenance routing, installation exemption, and shared
  automatic-development routing satisfy their acceptance scenarios without bypassing isolation.
- **SC-005**: Every confirmed requirement entry maps to specification coverage below.

## Out of Scope

- **OUT-001**: Compatibility with or migration from the previous shared-worktree directory
  convention. Use the new location directly; no compatibility migration workflow is added.
- **OUT-002**: Automatic merging back to the main branch or automatic worktree deletion on feature
  completion. Worktrees remain available for explicitly requested integration or cleanup.

## Assumptions and Design Responsibilities

No unconfirmed product assumption is promoted to a binding requirement. The design must select the
configuration key and CLI syntax, concrete maintenance-worktree identity, repository discovery
mechanism, and workspace handoff mechanism within the contracts above. Naming a repository's main
branch, remote, and valid baseline must not silently select an arbitrary feature branch; unresolved
identity is handled by REQ-014 rather than an invented product default.

The precise mechanics of preserving command inputs while redirecting a write, including staged
changes and commands that inspect uncommitted files, require design attention. Isolation does not
by itself authorize copying, stashing, committing, or discarding caller-owned changes.

## Dependencies

- Git worktree registration, branches, refs, fetch, ancestry comparison, and merge operations.
- Existing configuration entry points, ordinary feature creation, SDD command templates, and
  project-maintenance write entry points.
- Existing automatic-development locator and fixed-workspace behavior. Its new location is a
  required change; its fixed development model remains authoritative.
- The project's required verification procedure for a newly merged baseline.

## Open Questions

None from requirements discovery: OPEN-001 through OPEN-008 are resolved in `requirements.md`.
Design responsibilities above are implementation choices within confirmed scope; any newly found
product-policy conflict must be reported rather than silently resolved by adding requirements.

## Requirements Traceability

| Confirmed Entry | Spec Coverage | Result |
|---|---|---|
| NEED-001 | REQ-004; Story 1 | One worktree per ordinary feature |
| NEED-002 | REQ-001, REQ-002; Story 4 | Default on, configuration, opt-out boundary |
| NEED-003 | REQ-005, REQ-006, REQ-014; NFR-001; Story 1 | Full workflow and continuation |
| NEED-004 | REQ-007, REQ-009; Story 2 | Local/remote main-branch baseline |
| CON-001 | REQ-002, REQ-012; Story 4 | Fixed shared automatic development |
| CON-002 | REQ-009, REQ-014; NFR-001, NFR-003 | Failures, local-only baseline, no fallback |
| DEC-001 | REQ-003, REQ-011, REQ-012 | Unified external parent |
| DEC-002 | REQ-009, REQ-010; NFR-003; Story 2 | Ancestry and verified merge |
| DEC-003 | REQ-008; NFR-003; Story 2 | Fetch attempt, warning, fallback, retry |
| DEC-004 | REQ-011; NFR-001; Story 3 | Feature/maintenance write routing |
| DEC-005 | REQ-013; NFR-001; Story 3 | Both installation exceptions |
| DEC-006 | REQ-003, REQ-004, REQ-006; NFR-002 | Stable location, names, bare support |
| DEC-007 | REQ-016; Story 4 | Checkout-local switch authority and routed-write scope |
| OUT-001 | Out of Scope; Edge Cases | No old-directory compatibility or migration |
| OUT-002 | REQ-015; Out of Scope; Story 4 | Retention without automatic integration |
