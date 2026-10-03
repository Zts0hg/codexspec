# Confirmed Requirements: Feature Worktrees

**Feature ID**: `2026-1003-204985`
**Status**: Confirmed
**Last Confirmed**: 2026-10-03

## Authority Rules

- Only entries with `Status: confirmed` are binding downstream inputs.
- Open questions and discussion proposals require explicit confirmation before becoming binding.
- Replaced entries remain with `Status: superseded` and a link to their replacement.
- The final stage summary was explicitly confirmed on 2026-10-03. Discovery is complete; all open questions below are resolved.

## Needs

### NEED-001: Use one worktree per ordinary feature

- **Status**: confirmed
- **Statement**: Under the proposed worktree feature, ordinary feature development MUST use one Git worktree per feature, enabling multiple features to be developed in separate working directories.
- **User Evidence**: "普通特性采用‘一特性一 worktree’"
- **Confirmed At**: 2026-10-03

### NEED-002: Enable worktree isolation by default with a configurable opt-out

- **Status**: confirmed
- **Statement**: Provide a configuration switch for worktree isolation through the existing configuration entry points. The switch MUST default to enabled, including when its configuration is absent. When disabled, ordinary feature development and project-maintenance operations MUST retain their existing current-checkout behavior. `blueprint/auto-dev` MUST continue using their dedicated shared worktree regardless of this switch.
- **User Evidence**: The initial request specified a switch enabled by default; the user confirmed the final summary including missing-setting and disabled behavior.
- **Confirmed At**: 2026-10-03

### NEED-003: Isolate the complete feature workflow and reuse its workspace

- **Status**: confirmed
- **Statement**: When isolation is enabled, create an ordinary feature's worktree before the first write to its requirements document. Subsequent feature documents, source code, tests, and repairs MUST be produced in that worktree rather than the main checkout. Continuing the same feature MUST reuse its existing worktree.
- **User Evidence**: The user confirmed the final summary: create the worktree before writing requirements, perform the full workflow there, and reuse it when continuing the feature.
- **Confirmed At**: 2026-10-03

### NEED-004: Start new worktrees from the newer local or remote main-branch version

- **Status**: confirmed
- **Statement**: A new ordinary feature worktree MUST start from the newer committed version of the remote repository's main branch and the local main branch. It MUST NOT select the invoking checkout's arbitrary feature branch as its default baseline.
- **User Evidence**: "从 远端仓库的主分支和本地主分支中最新的那个分支 切出worktree"
- **Confirmed At**: 2026-10-03
- **Baseline Rule**: DEC-002 defines ancestry comparison and divergent-history reconciliation. DEC-003 defines remote refresh and failure handling.

## Constraints

### CON-001: Preserve the shared blueprint and auto-dev workspace model

- **Status**: confirmed
- **Statement**: `blueprint` and `auto-dev` MUST retain their existing fixed branch and shared worktree model. The one-worktree-per-feature rule for ordinary development MUST NOT cause `auto-dev` to create a separate branch or worktree for each blueprint requirement.
- **Existing Authority**: [Blueprint/auto-dev requirements](../2026-0829-2159yg-blueprint-auto-dev/requirements.md), DEC-004 and DEC-014, confirmed on 2026-08-29 and 2026-08-30. These decisions place the shared blueprint and all automatic development in one fixed workspace on `codexspec/auto-dev`, with worktree basename `worktree-for-codexspec-auto-dev`.
- **User Evidence**: "blueprint/auto-dev 延续固定共享 worktree 的既有模型"
- **Confirmed At**: 2026-10-03

### CON-002: Stop on workspace failures without writing to the main checkout

- **Status**: confirmed
- **Statement**: When isolation is enabled, failure to create the workspace, an occupied target path, or inability to determine a valid baseline MUST produce an explicit error. Commands MUST NOT fall back to modifying the main checkout or overwrite an existing directory. If no remote is configured, use the local main branch as the baseline.
- **User Evidence**: The user confirmed the final summary's failure behavior and local-only repository fallback.
- **Confirmed At**: 2026-10-03

## Decisions

### DEC-001: Place ordinary and shared worktrees under one external parent

- **Status**: confirmed
- **Decision**: Ordinary feature worktrees and the fixed `blueprint/auto-dev` worktree MUST reside under a common `<project-or-repository-name>-codexspec-worktrees` directory beside the main checkout. The shared worktree MUST retain the basename `worktree-for-codexspec-auto-dev` and the development model in CON-001.
- **Alternatives Rejected**: Retaining the existing shared-worktree parent while using the new parent only for ordinary features.
- **User Evidence**: The user selected option A: use the unified parent directory while retaining `worktree-for-codexspec-auto-dev` and its existing development model.
- **Confirmed At**: 2026-10-03
- **Compatibility Note**: The new parent-directory convention applies directly. OUT-001 excludes compatibility with and migration from the old directory convention.

### DEC-002: Select by ancestry and merge diverged main-branch histories

- **Status**: confirmed
- **Decision**: Compare the local and remote main-branch commits by ancestry, not commit timestamps. If one tip contains the other, use the descendant as the new ordinary feature's baseline; equal tips provide the same baseline. If both sides have unique commits, merge both histories inside the new feature worktree and use the verified merge result as the development baseline. Stop if merge conflicts cannot be resolved or required project verification fails.
- **Alternatives Rejected**: Stop on every divergence and require the user to reconcile the main branches before creating a feature workspace.
- **Existing Authority**: [Blueprint/auto-dev requirements](../2026-0829-2159yg-blueprint-auto-dev/requirements.md), DEC-014, supplies the existing ancestry-aware selection and merge precedent.
- **User Evidence**: The user selected option A: merge both histories in the new worktree, consistent with `auto-dev`, and stop on unresolved conflicts or failed verification.
- **Confirmed At**: 2026-10-03

### DEC-003: Continue from available local refs after a failed fetch

- **Status**: confirmed
- **Decision**: Before creating an ordinary feature worktree, attempt to fetch the configured remote main branch. If fetching fails, report the failure and compare the locally available local main-branch and remote-tracking main-branch commits under DEC-002. The diagnostic MUST make clear that the remote information may be stale. A failed fetch MUST NOT prevent another fetch attempt on the next worktree creation.
- **Alternatives Rejected**: Require a successful fetch before every ordinary feature worktree creation and stop whenever the remote cannot be refreshed.
- **User Evidence**: The user selected option A: continue with available local refs after reporting fetch failure, allow offline development, and retry fetching on the next creation.
- **Confirmed At**: 2026-10-03

### DEC-004: Isolate project-level changes in a feature or maintenance worktree

- **Status**: confirmed
- **Decision**: With worktree isolation enabled, project-level changes such as configuration, constitution, and profile updates MUST also occur outside the main checkout. When an ordinary feature worktree is the active workspace, perform these changes there. When such an operation is invoked independently from the main checkout without an active feature workspace, use a dedicated maintenance worktree.
- **Relationship to Existing Automation**: CON-001 continues to govern operations owned by `blueprint/auto-dev` in their fixed shared worktree.
- **Alternatives Rejected**: Isolate only feature-development artifacts and code while allowing project-level changes directly in the main checkout.
- **User Evidence**: The user selected option A: include project-level writes, use the active feature worktree when available, and use a dedicated maintenance worktree for standalone operations from the main checkout.
- **Confirmed At**: 2026-10-03

### DEC-005: Allow initialization and installation updates in the selected checkout

- **Status**: confirmed
- **Decision**: Both first-time initialization and subsequent installation updates through `codexspec init` MAY write to the checkout explicitly selected by the user. Worktree isolation governs development and project-maintenance operations after installation; it MUST NOT redirect these installation operations to a feature or maintenance worktree.
- **Alternatives Rejected**: Exempt only first-time initialization while requiring subsequent installation updates to run in a worktree.
- **User Evidence**: The user selected option A: allow both first-time initialization and installation updates in the selected checkout, and apply isolation to subsequent development and project maintenance.
- **Confirmed At**: 2026-10-03

### DEC-006: Resolve one repository-wide parent and use complete feature names

- **Status**: confirmed
- **Decision**: Invocations from any worktree of the same repository MUST resolve the same repository-wide external parent directory. An ordinary feature worktree directory MUST use the full `<feature-id>-<feature-name>` as its basename. Support both ordinary repositories and bare repositories with multiple linked worktrees, including the layout used by the CodexSpec repository.
- **User Evidence**: The user confirmed the final summary's repository-wide location, complete feature directory names, and bare-repository support.
- **Confirmed At**: 2026-10-03

### DEC-007: Keep the isolation switch local to each checkout

- **Status**: confirmed
- **Decision**: The isolation switch MUST follow each checkout's own configuration. A change written in a feature or maintenance worktree takes effect there first; other checkouts receive it through subsequent Git integration. Do not introduce a repository-wide immediate override for this switch.
- **User Evidence**: "沿用各 checkout 的配置（推荐）：修改在哪个 worktree 就先在那里生效，合并后再影响其他 checkout。"
- **Confirmed At**: 2026-10-03

## Out of Scope

### OUT-001: No compatibility with or migration from the old worktree directory

- **Status**: confirmed
- **Statement**: This feature MUST NOT include compatibility handling or migration support for the previous `blueprint/auto-dev` worktree directory convention. It uses the unified location in DEC-001 directly.
- **Reason**: The user stated that the previously released functionality has not been used by users, so old-directory compatibility is unnecessary.
- **User Evidence**: "可以不考虑兼容旧目录的事情，这个功能上线之后还没有被用户使用。"
- **Confirmed At**: 2026-10-03

### OUT-002: No automatic integration or worktree deletion on completion

- **Status**: confirmed
- **Statement**: Retain worktrees after feature completion. This feature MUST NOT add automatic merging back into the main branch or automatic worktree deletion on completion.
- **User Evidence**: The user confirmed the final summary's lifecycle boundary.
- **Confirmed At**: 2026-10-03

## Open Questions

No unresolved questions block specification generation.

### OPEN-001: Parent directory for the existing shared worktree

- **Status**: resolved
- **Resolution**: DEC-001 confirms the unified parent directory. Migration of an existing worktree is tracked separately in OPEN-003.
- **Blocks Specification**: no

### OPEN-002: Final confirmation of configuration and ordinary-feature boundaries

- **Status**: resolved
- **Resolution**: Final confirmation establishes NEED-002, NEED-003, DEC-006, CON-002, and OUT-002, including the default switch behavior, full-workflow isolation, stable location and feature naming, explicit failure handling, local-only baseline, and retained worktree lifecycle.
- **Blocks Specification**: no

### OPEN-003: Migration of an existing shared worktree

- **Status**: resolved
- **Resolution**: OUT-001 excludes old-directory compatibility and migration from this feature.
- **Blocks Specification**: no

### OPEN-004: Starting commit for a new ordinary feature

- **Status**: resolved
- **Resolution**: NEED-004 selects the newer committed version of the remote and local main branches. DEC-002 resolves divergent-history behavior; DEC-003 resolves fetch failure behavior.
- **Blocks Specification**: no

### OPEN-005: Comparing and reconciling local and remote main-branch histories

- **Status**: resolved
- **Resolution**: DEC-002 confirms ancestry-aware comparison and merging both histories in the new worktree when diverged.
- **Blocks Specification**: no

### OPEN-006: Remote refresh and failure handling

- **Status**: resolved
- **Resolution**: DEC-003 requires a fetch attempt and permits continuation with available local refs on failure, with a diagnostic and a new attempt on the next creation.
- **Blocks Specification**: no

### OPEN-007: Project-level writes outside an ordinary feature

- **Status**: resolved
- **Resolution**: DEC-004 extends isolation to project-level writes and assigns standalone operations to a dedicated maintenance worktree.
- **Blocks Specification**: no

### OPEN-008: Initialization and installation boundary

- **Status**: resolved
- **Resolution**: DEC-005 permits both first-time initialization and subsequent installation updates in the checkout explicitly selected by the user.
- **Blocks Specification**: no

## Superseded Entries

None.

## Confirmation Log

### Session 2026-10-03: Ordinary features and automatic development

- **Summary Presented**: Ordinary features use one worktree per feature; `blueprint/auto-dev` retain their fixed shared worktree model, as established by the previous feature's confirmed decisions.
- **User Confirmation**: "普通特性采用‘一特性一 worktree’；blueprint/auto-dev 延续固定共享 worktree 的既有模型"
- **Entries Confirmed**: NEED-001, CON-001
- **Stage**: Intermediate scope confirmation; directory policy and final discovery confirmation remain pending.

### Session 2026-10-03: Unified worktree parent directory

- **Summary Presented**: Put the fixed `blueprint/auto-dev` worktree under the same new external parent as ordinary feature worktrees, retaining its basename and development model.
- **User Confirmation**: "A"
- **Entries Confirmed**: DEC-001
- **Questions Resolved**: OPEN-001; existing-worktree migration is tracked in OPEN-003.
- **Stage**: Intermediate directory confirmation; final discovery confirmation remains pending.

### Session 2026-10-03: Exclude old-directory compatibility

- **Summary Presented**: Determine whether an existing shared worktree at the old location needs automatic or manual migration support.
- **User Confirmation**: "可以不考虑兼容旧目录的事情，这个功能上线之后还没有被用户使用。"
- **Entries Confirmed**: OUT-001
- **Questions Resolved**: OPEN-003
- **Stage**: Intermediate scope confirmation; final discovery confirmation remains pending.

### Session 2026-10-03: Source branch for new ordinary worktrees

- **Summary Presented**: Choose the starting branch for a new ordinary feature worktree.
- **User Confirmation**: "从 远端仓库的主分支和本地主分支中最新的那个分支 切出worktree"
- **Entries Confirmed**: NEED-004
- **Questions Resolved**: OPEN-004; ancestry comparison, divergent histories, and remote refresh behavior remain pending.
- **Stage**: Intermediate baseline confirmation; final discovery confirmation remains pending.

### Session 2026-10-03: Diverged main-branch histories

- **Summary Presented**: Compare commits by ancestry and, when histories diverge, merge both in the new feature worktree; stop on unresolved conflicts or failed verification.
- **User Confirmation**: "A"
- **Entries Confirmed**: DEC-002
- **Questions Resolved**: OPEN-005
- **Stage**: Intermediate reconciliation confirmation; remote-refresh policy and final discovery confirmation remain pending.

### Session 2026-10-03: Fetch failure behavior

- **Summary Presented**: Attempt fetching before creation; on failure, report potentially stale remote information and continue with locally available refs; retry on the next creation.
- **User Confirmation**: "A"
- **Entries Confirmed**: DEC-003
- **Questions Resolved**: OPEN-006
- **Stage**: Intermediate failure-policy confirmation; remaining boundaries and final discovery confirmation remain pending.

### Session 2026-10-03: Project-level change isolation

- **Summary Presented**: Configuration, constitution, and profile changes use the active feature worktree; standalone project-level writes invoked from the main checkout use a dedicated maintenance worktree.
- **User Confirmation**: "A"
- **Entries Confirmed**: DEC-004
- **Questions Resolved**: OPEN-007
- **Stage**: Intermediate write-scope confirmation; initialization boundary and final discovery confirmation remain pending.

### Session 2026-10-03: Initialization and installation updates

- **Summary Presented**: Permit both first-time initialization and installation updates through `codexspec init` in the explicitly selected checkout; apply worktree isolation to subsequent development and project maintenance.
- **User Confirmation**: "A"
- **Entries Confirmed**: DEC-005
- **Questions Resolved**: OPEN-008
- **Stage**: Intermediate installation-boundary confirmation; final stage summary remains pending.

### Session 2026-10-03: Final stage confirmation

- **Summary Presented**: Ordinary features use one worktree each; `blueprint/auto-dev` retain their fixed shared model; all worktrees use the new external parent without old-directory migration; baseline selection uses refreshed local/remote main-branch ancestry with merge-on-divergence and local continuation after fetch failure; project-level writes use feature or maintenance worktrees; initialization and installation updates may write to the selected checkout. Additional defaults: isolation is on when configuration is absent, opt-out preserves current-checkout behavior for ordinary development and maintenance, feature documents and code are isolated from the first requirements write, continuation reuses the workspace, location is consistent across linked worktrees and supports bare repositories, failures never fall back to main-checkout writes, local-only repositories use their local main branch, and completion retains worktrees without automatic integration or deletion.
- **User Confirmation**: "确认"
- **Entries Confirmed**: NEED-001, NEED-002, NEED-003, NEED-004, CON-001, CON-002, DEC-001, DEC-002, DEC-003, DEC-004, DEC-005, DEC-006, OUT-001, OUT-002
- **Questions Resolved**: OPEN-002; OPEN-001 through OPEN-008 are all resolved.
- **Stage**: Final. Discovery is complete and specification generation may proceed.

### Session 2026-10-03: Configuration authority during design

- **Summary Presented**: Decide whether an isolation-switch change affects its destination checkout first or immediately affects every checkout of the repository; existing configuration reads are checkout-local and standalone main-checkout writes route to maintenance.
- **User Confirmation**: "沿用各 checkout 的配置（推荐）：修改在哪个 worktree 就先在那里生效，合并后再影响其他 checkout。"
- **Entries Confirmed**: DEC-007
- **Stage**: Design clarification confirmed; all previous final-stage decisions remain binding.
