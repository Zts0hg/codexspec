# Requirements: Remove orphaned nested script copies

## Confirmed Scope

### NEED-001 — Establish whether the six old copies have active consumers

- Requirement: Check current repository references, installation sources, and execution
  paths before removing the six files listed below. Historical prose references are
  evidence, not executable consumers. A remaining active consumer blocks deletion.
- Status: confirmed

### NEED-002 — Remove only verified orphaned copies without breaking users

- Requirement: Delete the three named files in each nested directory after verification.
  Preserve installation and supported script execution behavior.
- Status: confirmed

| Directory | Files |
| --- | --- |
| `.codexspec/scripts/bash/` | `check-prerequisites.sh`, `common.sh`, `create-new-feature.sh` |
| `.codexspec/scripts/powershell/` | `check-prerequisites.ps1`, `common.ps1`, `create-new-feature.ps1` |

### NEED-003 — Record evidence and integrate the verified change

- Requirement: Complete concise Quick SDD artifacts and verification records, then merge
  into main and synchronize the code with the remote.
- Status: confirmed

### CON-001 — Verification precedes integration

- Constraint: Check installation and execution effects against current main, retain
  verification limitations, and do not merge or push a failing change.
- Status: confirmed

### DEC-001 — Use the Quick workflow

- Decision: Use compact requirements, specification, design, plan, tasks, reviews, and
  verification rather than expanding the scope into a script redesign.
- Status: confirmed

### OUT-001 — No unrelated functional or packaging changes

- Exclusion: No installer redesign, source-script changes, package-boundary changes,
  release/version bump, or cleanup of other files is part of this request.
- Status: confirmed

## User Evidence and Confirmation Log

- User confirmed the proposed scope: “quick 精简流程，先重新确认这 6 个文件现在确实无人引用、删除不会影响安装或执行，再补齐简短工件和验证记录。 然后合并到主分支中。”
- User added remote synchronization: “合并到主分支之后记得同步代码”.
- 2026-10-09: Both instructions explicitly authorize this bounded scope and integration;
  no repeated scope-approval question is needed.

## Open Questions

None. Safety of deletion is a verification obligation, not an assumed fact.
