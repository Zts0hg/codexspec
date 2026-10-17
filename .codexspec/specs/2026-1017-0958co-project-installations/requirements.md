# Confirmed Requirements: Project Installation Discovery and Upgrade

**Feature ID**: `2026-1017-0958co`
**Status**: Confirmed
**Last Confirmed**: 2026-10-17

## Authority Rules

- Only entries with `Status: confirmed` are binding downstream inputs.
- Open questions and AI proposals are not confirmed requirements.
- Replaced decisions remain as superseded entries with links to their replacements.
- Discovery is complete. The final legacy-project clarification is confirmed; no blocking product questions remain.

## Needs

### NEED-001: Discover installations recursively within the selected directory

- **Status**: confirmed
- **Statement**: Inspect the starting directory and its descendants for directories
  containing .codexspec. Continue discovery below a detected project to find nested
  installations. Do not traverse inside .git or .codexspec, and do not follow
  symbolic links. Include discovered worktrees according to DEC-002.
- **Errors**: Reject an invalid starting path. Report unreadable descendant
  directories, continue scanning other directories, and explicitly indicate that
  the results are incomplete.
- **User Evidence**: “其他内容没有问题” in response to the final-summary table,
  with only the legacy-project version/integrity row excepted.
- **Confirmed At**: 2026-10-17

### NEED-002: Show installation provenance and actual content consistency

- **Status**: confirmed
- **Statement**: Show both the release used for the last successful installation
  and whether the currently installed toolkit content matches that installation.
  Do not present a project as fully up to date solely because its recorded version
  equals the upgrade target. Identify affected paths when content is inconsistent.
- **User Evidence**: The user described retaining the updated version record while
  discarding individual command changes, then agreed to separate version reporting
  from file-content consistency checks.
- **Confirmed At**: 2026-10-17

### NEED-003: Upgrade existing installations without a manual migration

- **Status**: confirmed
- **Statement**: Existing initialized projects commonly contain actual toolkit
  files but no stored installation version, managed-file list, or content digests.
  Discover and report them normally. Missing version information means unknown
  version; missing file-list/digest information means no historical content
  baseline, not proof of corruption, completeness, or being up to date. Perform
  content checks whenever their baseline is available independently of whether
  the version number is present.
- **Scan-only behavior**: Remain offline and read-only. Do not backfill metadata or
  bless current file content as a historical installation baseline.
- **Upgrade behavior**: Obtain the target stable release, generate expected content
  for the project's existing installation options, and compare with actual files.
  Missing old version/digest information alone is not an upgrade blocker. Apply
  CON-002, CON-003 and DEC-003 before any modification, including protection of
  staged, unstaged and potentially overwritten untracked files. On complete
  success, automatically establish the actual installed version, managed-file
  list and content digests for later scanning. Failure or partial completion must
  not be recorded as success.
- **User workflow**: Use scan --upgrade without manually supplying metadata,
  generating a file list, or running a separate init migration. Do not introduce
  backup, undo or toolkit-owned version-history management.
- **Definitions**: A managed-file list names the toolkit files installed into the
  project; a content digest is a checksum of each installed file's content, not
  the file itself. A version/list/digest record is installation metadata, not an
  installation log, backup, or history database. Existing projects can have all
  toolkit files without having any such metadata.
- **User Evidence**: “确认” in response to the seven-item final legacy-project
  checklist, after clarification with actual paths and SHA-256 examples.
- **Confirmed At**: 2026-10-17

## Constraints

### CON-001: Safety and compatibility must not add user burden

- **Status**: confirmed
- **Statement**: Design the discovery and upgrade workflow for safety, robustness,
  and compatibility without adding backup-management or recovery procedures that
  users must learn or perform as part of routine upgrades.
- **User Evidence**: “你在设计的时候可以考虑安全、稳健和兼容，但是不能增加用户负担”.
- **Confirmed At**: 2026-10-17

### CON-002: Skip projects with local modifications and report why

- **Status**: confirmed
- **Statement**: When local modifications trigger the upgrade protection rule,
  skip the entire affected project rather than overwrite the user's changes.
  Explicitly report that the project was skipped because of local modifications.
  This protection also applies when the user selects bulk upgrade; selecting all
  projects does not authorize overwriting local modifications.
- **Reason**: Uncommitted user changes may not be recoverable through Git history
  if the upgrade overwrites them.
- **User Evidence**: “用户自己改了内容未提交，如果我们直接覆盖会覆盖用户的内容并且无法找回。”
  “遇到本地修改就跳过该项目，并且要报告这一情况明确告知用户”.
- **Confirmed At**: 2026-10-17
- **Scope**: DEC-003 limits this protection to paths the upgrade could affect;
  unrelated business-code changes do not trigger a skip.

### CON-003: Do not modify a project when preservation cannot be established

- **Status**: confirmed
- **Statement**: Before modifying any project, establish reliably that the upgrade
  will not overwrite the user's existing local modifications under CON-002 and
  DEC-003. If that cannot be established, leave the entire project unchanged and
  only report the project and the reason it was not upgraded. Uncertainty must
  never be treated as a clean state or permission to overwrite.
- **Coverage**: Apply this rule to all upgrade modes, including automatic bulk
  upgrade. It covers missing or unusable Git state, untracked or ignored affected
  files whose preservation cannot be established, inspection errors, and any
  other case where the required safety determination is unavailable.
- **Boundary**: Unrelated business-code modifications remain outside the blocking
  scope under DEC-003. Do not initialize Git, stage, commit, stash, reset, create
  project metadata, or make other project changes merely to bypass this rule.
- **User Evidence**: “那么我们无法确保是否会误伤用户原有修改时，就不应该修改，只进行报告”.
- **Confirmed At**: 2026-10-17

### CON-004: Preserve project content, configuration, and enabled integrations

- **Status**: confirmed
- **Statement**: Preserve the project's existing Claude/Codex installation choice
  and configuration, project-authored requirements, constitution, knowledge
  records, and the user-authored body of project instruction files.
- **User Evidence**: “其他内容没有问题”, excluding only the legacy-project row.
- **Confirmed At**: 2026-10-17

### CON-005: Report failures accurately and isolate project failures

- **Status**: confirmed
- **Statement**: If the target release cannot be obtained, do not modify projects.
  Report a per-project upgrade failure explicitly and continue with the remaining
  projects. Do not record failed or partially completed upgrades as successful.
- **User Evidence**: “其他内容没有问题”, excluding only the legacy-project row.
- **Confirmed At**: 2026-10-17

## Decisions

### DEC-001: Fetch the latest stable release for project upgrades

- **Status**: confirmed
- **Decision**: When upgrading selected projects, the command obtains the latest
  stable CodexSpec release and uses that release to update their installed toolkit.
  Users do not have to upgrade their locally installed CLI beforehand.
- **Alternatives Rejected**: Updating projects only from the currently installed
  CLI's bundled version after asking users to upgrade that CLI themselves.
- **Reason**: Let users bring multiple project installations up to date through
  one command without a separate prerequisite CLI upgrade.
- **User Evidence**: The user selected option A: “命令获取最新稳定发行版，再更新项目”.
- **Confirmed At**: 2026-10-17
- **Boundary**: This decision specifies the release used to update project files.
  OUT-002 excludes replacing the global CLI; CON-005 governs retrieval failures.
  The package retrieval mechanism remains a design choice.

### DEC-002: Treat each discovered installation directory independently

- **Status**: confirmed
- **Decision**: Within the requested scan scope, list the primary working
  directory and each Git worktree containing a CodexSpec installation separately,
  with its own installed version. Group entries belonging to the same Git
  repository for display, while allowing each installation to be upgraded
  independently. The bulk-upgrade selection includes all discovered installation
  directories within that scope, including worktrees.
- **Boundary**: Repository grouping does not expand the scan scope to worktrees
  outside the requested directory tree.
- **Alternatives Rejected**: Scan and upgrade only the primary working directory
  by default, requiring an explicit --include-worktrees option for other worktrees.
- **Reason**: Installed toolkit files belong to individual working directories;
  updating one directory does not immediately update the others.
- **User Evidence**: The user selected option A: “每个安装目录独立处理”, including
  per-directory versions, repository grouping, independent upgrades, and all
  discovered installation directories in the bulk-upgrade selection.
- **Confirmed At**: 2026-10-17

### DEC-003: Check local modifications only in paths affected by the upgrade

- **Status**: confirmed
- **Decision**: Determine which paths an upgrade could affect and check those
  paths for local modifications. Include staged changes, unstaged changes, and
  untracked files that could be overwritten. If such modifications are found,
  skip the entire project under CON-002 and report the reason. Changes to unrelated
  business code do not prevent the toolkit upgrade.
- **Coverage**: Affected paths include toolkit files and any configuration or
  project instruction files the upgrade could modify; the protection is not
  limited to files inside .codexspec.
- **Alternatives Rejected**: Skip any repository with any uncommitted change,
  regardless of whether the upgrade could affect it.
- **Reason**: Protect user content while avoiding unnecessary upgrade restrictions
  caused by unrelated ongoing development.
- **User Evidence**: The user selected option B: “仅升级可能影响的文件存在本地修改时跳过”,
  including staged, unstaged, and potentially overwritten untracked files.
- **Confirmed At**: 2026-10-17

### DEC-004: Use scan with explicit upgrade and automatic-confirmation options

- **Status**: confirmed
- **Decision**: Provide these public CLI forms:
  - codexspec scan <path>: scan and display installation information only.
  - codexspec scan <path> --upgrade: scan first, then ask whether to upgrade each
    project, with an option to upgrade all remaining eligible projects.
  - codexspec scan <path> --upgrade --yes: automatically upgrade all eligible
    discovered projects and summarize upgraded, skipped, and failed results.
- **Default**: The scan command without --upgrade does not update projects.
- **Protection**: --yes suppresses project-selection confirmations only; it never
  bypasses CON-002, CON-003, or the affected-path scope in DEC-003.
- **Reason**: scan describes discovery as the default action; --upgrade explicitly
  requests updates, and --yes enables the automatic bulk workflow.
- **User Evidence**: The user replied “采用” to the three-command table above.
- **Confirmed At**: 2026-10-17

### DEC-005: Record installed file fingerprints and detect incomplete updates

- **Status**: confirmed
- **Decision**: Automatically record the successfully installed release, the
  toolkit-managed file inventory, and content digests. During scanning, compare
  actual installed content with that recorded installation. Cover distributed
  commands, scripts, templates, and other toolkit installation content; do not
  compare project-authored requirements or constitutions with default templates.
- **Meaning**: The version identifies installation provenance. Content digests
  establish consistency with the recorded installation; they are not backups,
  proof of the absence of user modifications, or authority to overwrite files.
- **Partial Discard Behavior**: If the installation record remains updated but
  individual toolkit files have been reverted or otherwise differ, display the
  recorded version together with an inconsistent-content status and affected
  paths. Do not classify the project as requiring no action solely on version.
- **Upgrade Behavior**: A project with inconsistent installation content remains
  eligible for consideration by scan --upgrade, including reinstallation of the
  same release. Apply CON-002, CON-003, and DEC-003 before every write; skip the
  entire project and report when local modifications or uncertainty prevent safe
  updating. Inconsistency alone does not authorize replacement.
- **User Workflow**: Explain the inconsistency and direct users to the existing
  scan --upgrade entry point. Do not require them to discover a separate manual
  init recovery procedure or introduce a backup/restore command.
- **Alternatives Rejected**: Treat a matching version record as sufficient to
  skip upgrade; use only a version marker without content verification; require
  users to infer that they should rerun init to repair partial updates.
- **User Evidence**: The user replied “同意” to the version-plus-file-inventory-and-
  digests proposal, actual-content checks, inconsistent-state reporting, and the
  same-version upgrade path subject to the established safety checks.
- **Confirmed At**: 2026-10-17
- **Design Boundary**: The record filename, schema, digest implementation, and
  treatment of generated or localized content remain design choices. Legitimate
  project-authored content is not an installation-corruption signal.

### DEC-006: Scan-only operation is offline and read-only

- **Status**: confirmed
- **Decision**: Without --upgrade, scan does not access the network or write project
  files. Display recorded installation version and content-consistency information
  where supported by available evidence; do not claim a version is the latest
  remote release. NEED-003 defines legacy-project verification.
- **User Evidence**: “其他内容没有问题”, excluding only the legacy-project row.
- **Confirmed At**: 2026-10-17

### DEC-007: Use one stable target release and do not downgrade automatically

- **Status**: confirmed
- **Decision**: Use the same latest stable target release for all projects in one
  upgrade invocation. If a project's recorded version is higher than that target,
  skip automatic downgrade and report the situation.
- **User Evidence**: “其他内容没有问题”, excluding only the legacy-project row.
- **Confirmed At**: 2026-10-17

## Out of Scope

### OUT-002: Replacement of the globally installed CLI

- **Status**: confirmed
- **Statement**: This workflow updates project-local toolkit installations. It does
  not replace the globally installed CodexSpec CLI.
- **User Evidence**: “其他内容没有问题”, excluding only the legacy-project row.
- **Confirmed At**: 2026-10-17

### OUT-001: Toolkit-owned backup, undo, and version-history management

- **Status**: confirmed
- **Statement**: Do not add a user-facing backup/restore system, an undo command,
  or toolkit-owned version-history management for project upgrades. Users inspect
  upgrade differences through Git changes and use their existing Git history to
  restore a desired project version.
- **Reason**: Existing Git workflows already provide change inspection and version
  recovery; duplicating them expands the command's responsibilities and user burden.
- **User Evidence**: “不存在你说的用户想要回退还需要靠我们的情况，用户自己看git changes就可以
  [知道]每次版本更新的差异，以及可以选择某一个git 历史来覆盖掉某一个仓库的当前版本”.
- **Confirmed At**: 2026-10-17
- **Boundary**: This exclusion does not authorize the upgrade command to create
  commits, reset repositories, or restore user files through Git. CON-005 governs failure handling; no automatic rollback promise is confirmed.

## Historical Background

- `../2026-1003-204985-feature-worktrees/requirements.md`, DEC-005 permits initial
  installation and subsequent installation updates in the selected checkout;
  development-worktree routing must not redirect those installation operations.
- `../2026-0620-1814yp-init-language-options/requirements.md` requires surgical
  configuration updates that preserve unspecified language settings during init.
- `../2026-1011-105126-review-code-standards/requirements.md`, DEC-006 establishes
  that project initialization or installation update copies shared review
  resources; installing the CLI alone does not update project files.

### Verified initialization behavior — 2026-10-17

This is implementation evidence, not a confirmed upgrade policy.

- `src/codexspec/__init__.py`, init: --no-git defaults to false. When the selected
  target has no .git entry and --no-git is not supplied, init runs git init after
  installing project resources. With --no-git, it skips Git initialization.
- A git init nonzero exit is caught as CalledProcessError and reported as a
  warning; previously installed CodexSpec files are not removed. This does not
  imply every Git-launch failure is caught.
- Two CLI probes using this feature checkout's source in fresh directories outside
  a Git repository both exited 0. Default init produced both .codexspec and .git
  directories; init --no-git produced .codexspec without a .git directory.
- A .git directory is not the only valid Git representation: linked worktrees use
  a .git file. Git membership must not be inferred from .git.is_dir().
- CON-003 subsequently confirms that inability to establish preservation of
  user modifications requires leaving the project unchanged and reporting why;
  OPEN-005 is resolved by that explicit user decision.

## Open Questions

### OPEN-001: Command name and invocation forms

- **Status**: resolved
- **Resolution**: DEC-004 confirms scan, --upgrade, and --yes with the three
  invocation forms and their protection boundaries.
- **Blocks Specification Generation**: No.

### OPEN-002: Discovery boundaries and worktrees

- **Status**: resolved
- **Resolution**: NEED-001 defines recursive discovery and scan errors; DEC-002
  defines worktree grouping and selection; CON-003 prevents unsafe modifications
  where reliable preservation checks are unavailable.
- **Blocks Specification Generation**: No.

### OPEN-003: Legacy-project verification behavior

- **Status**: resolved
- **Resolution**: NEED-003 distinguishes missing version information from a missing
  content baseline, preserves available checks, and confirms safe migration through
  scan --upgrade with automatic metadata creation only after complete success.
- **Blocks Specification Generation**: No.

### OPEN-004: Scope of local modifications that prevents upgrade

- **Status**: resolved
- **Resolution**: DEC-003 selects affected upgrade paths only and covers staged,
  unstaged, and potentially overwritten untracked files. CON-002 requires skipping
  the whole project and clearly reporting the reason.
- **Blocks Specification Generation**: No.

### OPEN-005: Projects without reliable Git tracking

- **Status**: resolved
- **Resolution**: CON-003 requires leaving the project unchanged and only reporting
  when preservation of user modifications cannot be reliably established. Missing
  or unusable Git state cannot silently bypass the modification protection.
- **Blocks Specification Generation**: No.

## Superseded Entries

None.

## Confirmation Log

### Latest stable release source — 2026-10-17

- **Summary Presented**: Option A obtains the latest stable release and updates
  projects without requiring a manual CLI upgrade first. Option B uses the locally
  installed CLI's bundled version and requires users to update it themselves.
- **User Confirmation**: “A”.
- **Entries Confirmed**: DEC-001.
- **Stage**: Intermediate topic confirmation. Command naming, other proposals,
  and the final discovery summary remain unconfirmed.

### Independent worktree installations — 2026-10-17

- **Summary Presented**: Option A lists the primary working directory and all
  discovered worktrees separately, groups them by repository for display, permits
  independent upgrades, and includes all discovered installations in bulk upgrade.
  Option B excludes other worktrees unless explicitly requested.
- **User Confirmation**: “A”.
- **Entries Confirmed**: DEC-002.
- **Stage**: Intermediate topic confirmation; final discovery confirmation remains
  pending.

### Existing Git workflow owns change inspection and version recovery — 2026-10-17

- **User Direction**: Safety, robustness, and compatibility must not increase user
  burden. The user rejected the proposed toolkit backup/undo workflow because Git
  changes and Git history already provide inspection and version recovery.
- **Entries Confirmed**: CON-001 and OUT-001.
- **Proposal Disposition**: Backup-before-overwrite, a retained recovery snapshot,
  an undo command, and automatic rollback were assistant proposals, never confirmed
  decisions. They must not be treated as downstream requirements.
- **Stage**: Explicit scope correction; final discovery confirmation remains pending.

### Skip locally modified projects — 2026-10-17

- **User Direction**: Uncommitted local content can be lost when overwritten;
  adopt skipping the project on local modifications and explicitly report it.
- **Entries Confirmed**: CON-002.
- **Open Boundary**: OPEN-004 records the remaining definition of local
  modifications; the decision to skip the whole project is settled.
- **Stage**: Intermediate topic confirmation; final discovery confirmation remains
  pending.

### Protect only upgrade-affected paths — 2026-10-17

- **Summary Presented**: Option A skips repositories with any uncommitted change.
  Option B checks only upgrade-affected paths, including staged, unstaged, and
  potentially overwritten untracked files, and skips the whole project if those
  paths have local modifications. Unrelated business-code changes are allowed.
- **User Confirmation**: “B”.
- **Entries Confirmed**: DEC-003; CON-002 now references its confirmed scope.
- **Open Question Resolved**: OPEN-004. OPEN-005 retains cases without reliable Git
  tracking for further clarification.
- **Stage**: Intermediate topic confirmation; final discovery confirmation remains
  pending.

### Report without modifying when preservation is uncertain — 2026-10-17

- **Background Presented**: Actual init probes verified that --no-git produces a
  CodexSpec installation without a Git repository; default init initializes Git.
  Linked worktrees use a .git file rather than a .git directory.
- **User Confirmation**: “那么我们无法确保是否会误伤用户原有修改时，就不应该修改，只进行报告”.
- **Entries Confirmed**: CON-003.
- **Open Question Resolved**: OPEN-005.
- **Stage**: Intermediate protection-policy confirmation; final discovery
  confirmation remains pending.

### Public scan and upgrade interface — 2026-10-17

- **Summary Presented**: scan <path> lists installations; adding --upgrade asks
  per project with an upgrade-all-remaining option; adding --upgrade --yes upgrades
  all eligible projects automatically and summarizes upgraded, skipped, and failed
  results. Safety checks apply in every mode.
- **User Confirmation**: “采用”.
- **Entries Confirmed**: DEC-004.
- **Open Question Resolved**: OPEN-001.
- **Stage**: Intermediate command-interface confirmation; final discovery
  confirmation remains pending.

### Verify content independently of recorded version — 2026-10-17

- **Summary Presented**: Automatically record release, managed-file inventory,
  and content digests. Scan compares actual files, reports inconsistent content
  and affected paths even at the target version, and offers the same scan
  --upgrade workflow for safe same-version reinstallation. Content differences
  never bypass local-modification protection. Project-authored requirements and
  constitutions are not compared with default templates. No backup system or
  manual-init recovery dependency is added.
- **User Confirmation**: “同意”.
- **Entries Confirmed**: NEED-002 and DEC-005.
- **Proposal Disposition**: The earlier suggestion to skip solely on equal version
  was never confirmed and must not be used downstream.
- **Stage**: Intermediate version-and-consistency confirmation; final discovery
  confirmation remains pending.

### Final-summary acceptance except legacy-project verification — 2026-10-17

- **User Confirmation**: “其他内容没有问题”, followed by questions about the legacy-
  project row's “完整性未验证” and “安装记录” wording and whether a missing version
  prevents content checks.
- **Entries Confirmed**: NEED-001, CON-004, CON-005, DEC-006, DEC-007, OUT-002.
- **Open Question Resolved**: OPEN-002.
- **Remaining Clarification**: OPEN-003. The legacy-project row is not confirmed;
  do not advance the chain until it is resolved and discovery is confirmed complete.

### Final discovery confirmation — 2026-10-17

- **Summary Presented**: Existing projects remain discoverable; missing version
  and missing checksum baseline are reported separately. Scan-only stays offline
  and read-only. Upgrade compares actual files with the fetched target release,
  applies affected-path protection including uncertain states, and establishes
  metadata only after complete success. No manual migration or backup system is
  required. All other previously confirmed rules remain in effect.
- **User Confirmation**: “确认”.
- **Entries Confirmed**: NEED-003, completing the combined final summary with
  NEED-001–002, CON-001–005, DEC-001–007 and OUT-001–002.
- **Open Question Resolved**: OPEN-003. OPEN-001–005 are all resolved.
- **Stage**: Final discovery confirmation. No blocking open questions remain.
