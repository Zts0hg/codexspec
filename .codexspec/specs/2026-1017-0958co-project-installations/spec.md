# Feature Specification: Project Installation Discovery and Upgrade

**Feature Branch**: `2026-1017-0958co-project-installations`
**Created**: 2026-10-17
**Status**: Draft
**Authority**: [Confirmed requirements](requirements.md)

## Context and Goals

A CLI package upgrade does not refresh toolkit files previously copied into other
projects. Users need to find those installations, see their recorded release and
actual consistency, and update eligible projects without visiting each directory
or first updating the global CLI. Project-specific content and uncommitted work
must remain protected. Git remains the user's change-inspection and version-
recovery mechanism.

An **installation directory** is a scanned directory containing a real .codexspec
directory. Its **installation metadata** records the last successful release,
paths of installed toolkit-managed files, and their content checksums. It is not
an installation log or backup. **Consistency** means agreement with that recorded
content; it does not prove freshness against a remote release or authorize writes.
A legacy installation can have all toolkit files while having no such metadata.

## User Scenarios and Testing

### Story 1: Find installations without changing them (P1)

A user runs `codexspec scan ~/projects` and sees installations, their paths,
recorded versions or unknown status, and content-consistency results. Worktrees
are grouped by their Git repository but retain separate rows and choices.

Independent test: build a directory tree with nested projects, hidden directories,
Git worktrees, and unrelated content; assert the complete bounded inventory,
zero network calls, and byte-identical project files after scanning.

### Story 2: Upgrade several eligible installations (P1)

The user runs scan with --upgrade, inspects the inventory, then chooses individual
projects or all remaining eligible projects. With --yes, no project-selection
questions are needed. One latest stable target is used throughout the invocation.

Independent test: supply a controlled target release and projects with both clean
and modified affected files; verify updates, skips and their reasons independently.

### Story 3: Detect partial discards and migrate legacy projects (P1)

A user keeps new metadata but discards a command update. A subsequent scan reports
inconsistent content even when the version label equals the target release. The
same upgrade entry supports safe reinstallation. Ordinary older installations
without metadata can migrate after passing the same safety checks.

Independent test: vary missing metadata, missing version only, changed or missing
managed files, and clean versus uncommitted content; assert accurate reporting
and that unsuccessful operations never claim a complete successful installation.

## Functional Requirements

### REQ-001: Public modes

Provide scan <path>, scan <path> --upgrade, and scan <path> --upgrade --yes.
Scan-only lists installations. Interactive upgrade scans first and supports each
project plus all remaining eligible projects. Automatic upgrade processes all
eligible discovered projects without selection prompts. --yes never bypasses safety.

Sources: DEC-004, CON-002, CON-003.

### REQ-002: Bounded recursive discovery

Inspect the starting directory and descendants for .codexspec installations,
including nested installations below another project. Do not descend into .git
or .codexspec or follow symbolic links. Reject an invalid starting path. Report
unreadable descendant paths, continue other traversal and mark results incomplete.

Sources: NEED-001.

### REQ-003: Independent working directories

Recognize Git worktrees through Git identity, not a requirement for a .git directory.
Group installations sharing a repository while reporting version and selection
per working directory. Do not add worktrees outside the selected scan tree.

Sources: DEC-002, NEED-001.

### REQ-004: Offline read-only inventory

Scan-only must not access the network, modify projects, create metadata, or label
a version the latest remote release. Report known installation and consistency
facts without treating unavailable evidence as success.

Sources: DEC-006, NEED-002, NEED-003.

### REQ-005: Version and content metadata

After complete successful installation or upgrade, automatically record the actual
installed release, managed-file paths and checksums. Cover the installed platform's
commands/skills, scripts, document templates and other shipped toolkit content.
Do not use project-authored requirements or constitutions as default-template
checks. Metadata storage and projection of generated/localized content are design
choices. Metadata is neither backup content nor proof of safe replacement.

Sources: DEC-005, NEED-002, NEED-003, CON-004.

### REQ-006: Actual content checks

Read actual files and compare with available recorded file-list/checksum evidence.
Report missing or changed managed files and their paths. A missing version alone
must not disable checks with an available content baseline. A matching version
alone must not suppress inconsistency reporting or upgrade consideration.

Sources: NEED-002, NEED-003, DEC-005.

### REQ-007: Honest legacy status

Discover projects without metadata normally. Report unknown version separately
from missing historical content baseline. Do not call absent metadata corruption,
proof of completeness, or proof of latest version. Do not infer a successful
historical installation by hashing arbitrary current files during scan.

Sources: NEED-003, DEC-006.

### REQ-008: Fetch one latest stable target

For upgrade, obtain the latest stable CodexSpec release and use that same target
for all projects in the invocation. Do not require a prior manual global CLI
upgrade and do not replace the globally installed CLI. If acquisition fails,
leave all projects unchanged and report the error.

Sources: DEC-001, DEC-007, CON-005, OUT-002.

### REQ-009: Compare target content for each project

Prepare the content expected from the target release using that project's existing
integration and installation options, then compare with actual project content.
Absence of old metadata alone is not a blocker. Existing metadata/content
inconsistency remains a candidate for safe same-release reinstallation. Skip and
report a recorded version newer than the target rather than downgrade automatically.

Sources: NEED-003, DEC-005, DEC-007, CON-004.

### REQ-010: Protect the complete affected set before writing

Establish every path the proposed project upgrade could modify, including toolkit
files, configuration, instruction files and metadata. Inspect affected staged and
unstaged changes and untracked content that could be overwritten. When relevant
local modifications are present, leave the entire project unchanged and report
its path and the reason. Unrelated business-code modifications must not block it.

Sources: CON-002, CON-003, DEC-003, NEED-003.

### REQ-011: Uncertain safety is not consent

If preservation of existing user modifications cannot be reliably established,
leave the entire project unchanged and report the specific reason. This includes
missing/unusable Git state, affected ignored/untracked content with no reliable
preservation basis, and inspection errors. Do not initialize Git, stage, commit,
stash, reset or create project metadata to bypass protection. Apply this rule to
every upgrade mode, including --yes and same-version reinstallation.

Sources: CON-003, DEC-003, NEED-003, OUT-001.

### REQ-012: Preserve project-owned content and choices

Retain existing Claude/Codex integration choices, project configuration,
requirements, constitution, knowledge records and user-authored instruction-file
body. Updating toolkit-managed portions must not replace user-owned content.
Installation updates operate in the selected installation directory, including
worktrees, without redirecting to a new development or maintenance worktree.

Sources: CON-004, DEC-002, NEED-003.

### REQ-013: Accurate completion and continuation

Report upgraded, skipped and failed project results, including explanatory paths
where applicable. A per-project failure does not prevent remaining projects from
being processed. Failed or partially completed upgrades must not publish successful
new installation metadata. Do not promise automatic rollback or obscure partial
failure as success. User-declined projects remain unchanged.

Sources: CON-005, DEC-004, NEED-003.

### REQ-014: One user workflow

Use scan --upgrade to bring older installations into the metadata-aware workflow
and to address detected content inconsistency. Do not require manual metadata
entry, file-list generation, or separate init recovery knowledge. Report the
applicable next step when differences or safety conditions require user attention.

Sources: CON-001, NEED-003, DEC-005.

## Nonfunctional Requirements

### NFR-001: Observable preservation

Validation must prove that scan-only operations and safety-based skips leave
project files unchanged, and that permitted upgrades preserve user-owned content.
No absence/error result may be interpreted as permission to replace unknown content.

Sources: CON-002, CON-003, CON-004, DEC-006.

### NFR-002: No additional recovery administration

Do not introduce user-managed backups, an undo interface, toolkit version-history
management or global CLI replacement. Users continue to inspect and recover through
Git; routine scan/upgrade must not require learning extra migration procedures.

Sources: CON-001, OUT-001, OUT-002, NEED-003.

## Acceptance Cases and Error Behavior

| Case | Expected result | Coverage |
| --- | --- | --- |
| Root itself and a nested directory both have .codexspec | Both appear; metadata internals are not traversed | REQ-002 |
| Hidden project directory inside root | Included unless traversal is prohibited by the stated rules | REQ-002 |
| Linked directory or worktree outside root | No traversal beyond the requested tree | REQ-002, REQ-003 |
| Worktree with .git file | Separate installation grouped with its repository | REQ-003 |
| Invalid root / inaccessible descendant | Root error / explicit incomplete inventory while continuing | REQ-002 |
| Legacy installation without all metadata | Unknown version and unavailable historical baseline, no writes | REQ-004, REQ-007 |
| Missing version with otherwise usable checksum data | Version unknown, content checks still performed | REQ-006 |
| New version label but discarded command content | Inconsistent content and affected path, not latest-only skip | REQ-006, REQ-009 |
| Upgrading legacy installation with safely replaceable files | Target comparison, safe update and new metadata on full success | REQ-005, REQ-009 |
| Affected staged/unstaged/untracked modification | Whole project unchanged, explicit skip reason, including --yes | REQ-010 |
| Unrelated modified business source | Does not block an otherwise safe update | REQ-010 |
| No Git, unreadable safety evidence, unsafe affected ignored content | No project changes; explain uncertainty | REQ-011 |
| Acquisition failure | No project writes | REQ-008 |
| One project fails during application | Report failed/partial state, no successful metadata, continue others | REQ-013 |
| Recorded version exceeds target stable release | Report and skip automatic downgrade | REQ-009 |
| Existing configuration or custom context body | Preserve values/body while updating managed portions | REQ-012 |

## Success Criteria

- The three CLI forms cover discovery, selective upgrade and automatic eligible-
  project upgrade without requiring directory-by-directory visits.
- Fixtures demonstrate all acceptance cases with filesystem and network assertions.
- Partial discards cannot be hidden solely by retaining a newer version label.
- Legacy projects require no manual metadata migration.

## Confirmed Constraints and Out of Scope

Safety and preservation take precedence over bulk selection. Scope is bounded by
the requested filesystem tree and by project-local toolkit installation updates.
OUT-001 excludes backup/restore/undo and toolkit-owned version history; OUT-002
excludes replacing the global CLI. Automatic Git staging, commits, resets or
stashes are not authorized. No automatic rollback guarantee is specified.

## Open Questions and Design Boundaries

OPEN-001 through OPEN-005 are resolved in requirements.md. No blocking product
questions remain. Design determines metadata filename/schema and digest algorithm,
release acquisition and execution isolation, generated/localized content handling,
concrete Git checks, mutation strategy, diagnostic wording and exit codes. These
choices must preserve the safety, offline-scan and compatibility contracts above.

## Requirements Traceability

| Confirmed Entry | Spec Coverage |
| --- | --- |
| NEED-001 | REQ-002, REQ-003 |
| NEED-002 | REQ-004, REQ-005, REQ-006 |
| NEED-003 | REQ-004–007, REQ-009–014, NFR-002 |
| CON-001 | REQ-014, NFR-002 |
| CON-002 | REQ-001, REQ-010, NFR-001 |
| CON-003 | REQ-001, REQ-010, REQ-011, NFR-001 |
| CON-004 | REQ-005, REQ-009, REQ-012, NFR-001 |
| CON-005 | REQ-008, REQ-013 |
| DEC-001 | REQ-008 |
| DEC-002 | REQ-003, REQ-012 |
| DEC-003 | REQ-010, REQ-011 |
| DEC-004 | REQ-001, REQ-013 |
| DEC-005 | REQ-005, REQ-006, REQ-009, REQ-014 |
| DEC-006 | REQ-004, REQ-007, NFR-001 |
| DEC-007 | REQ-008, REQ-009 |
| OUT-001 | REQ-011, NFR-002, Out of Scope |
| OUT-002 | REQ-008, NFR-002, Out of Scope |
