# Confirmed Requirements: Distill Review File Descriptor Leak Fix

**Feature**: `2026-1030-11453h-distill-review-fd-leak`
**Status**: Confirmed

## Context and evidence

The POSIX writers `SessionStore._atomic_at` in `src/codexspec/distill_review/session.py` and `ProfileTransaction._install_exclusive_at` in `src/codexspec/distill_review/transaction.py` open raw file descriptors and wrap them with `closefd=False`, but omit raw descriptor closure. The two corresponding `_read_at` methods already close their borrowed-stream descriptors correctly.

Independent bounded reproduction against installed CodexSpec 0.7.27 and repository commit `ec0d940932d71a10dacd862dd0aad765dca19d6a` on macOS with Python 3.11.13 retained 16 descriptors after 16 session writes and another 16 after 16 exclusive installations. Contents were correct. Sixteen real `SessionStore.save` calls also retained 16 descriptors. Injected fdopen construction failure and file fsync failure each retained one descriptor in each writer; an exclusive-install target conflict retained one descriptor without overwriting the target. Resource exhaustion, production data loss, Linux execution and Windows execution were not demonstrated. Descriptor accumulation is within a process; process exit releases descriptors.

Historical authority: `../2026-0927-2310d6-html-distill-review/requirements.md` NEED-005, CON-003 and DEC-004 establish recoverable persistence and conflict-safe transactions. `../2026-1001-2205zz-distill-review-interface-design/requirements.md` CON-003 preserves their safety semantics. This fix does not replace those decisions.

## Confirmed entries

### NEED-001: Release writer-owned descriptors

- **Status**: confirmed
- **Statement**: Fix both named writers so every exit after a successful open attempts to close the raw descriptor exactly once, on success and failure, without double-closing or closing a caller-owned directory descriptor. If close itself fails, follow DEC-001 rather than promising successful release by the operating system.
- **User Evidence**: The user explicitly requested repair of the verified defect and accepted the final scope and ownership proposal with “采用”.

### NEED-002: Detect resource regressions

- **Status**: confirmed
- **Statement**: Add regression coverage for repeated successful writes; stream construction, permission setting, write, flush and file synchronization failures; replace/link and directory synchronization failures; existing-target conflicts; and cleanup failures. Verify descriptor counts return to baseline when closure succeeds, correct contents and permissions, and continued usability of the caller's directory descriptor. Include real session persistence and relevant transaction paths rather than only private primitives; retain relevant prepare/apply/rollback/recovery and security regression checks. Tests must detect double close and erroneous closure of reused descriptors. Report actual platform execution separately from checks awaiting CI; do not claim unavailable platform tests ran.

### CON-001: Preserve security and transaction contracts

- **Status**: confirmed
- **Statement**: Preserve existing session 0o600 and profile 0o644 permissions, directory-descriptor anchoring, O_EXCL/O_NOFOLLOW protections, atomic replacement, exclusive installation, flush/fsync ordering, conflict rejection, journal stages and recovery behavior. Do not swallow errors to obtain passing tests or regress the non-POSIX fallback. Do not alter the two correctly managed read functions.

### DEC-001: Keep explicit raw descriptor ownership

- **Status**: confirmed
- **Decision**: Retain `closefd=False`. Each writer owns its opened raw descriptor for the whole operation. After stream handling and existing replacement/link/directory-sync operations, an outer finally attempts `os.close(descriptor)` exactly once. A nested finally attempts temporary-path unlink even when close raises. Ignore only FileNotFoundError from temporary-path cleanup; propagate other cleanup failures. Never retry close, because its numeric descriptor may have been reused. Preserve Python exception context: a cleanup error may become the outermost exception while preceding errors remain chained. Do not add a new exception-aggregation framework.
- **Alternatives Rejected**: Transferring ownership with closefd=True requires special handling of stream-construction failure and transfer state to avoid double close. Explicit ownership is smaller and consistent with the existing readers. Raising FD limits, forced garbage collection and periodic restart do not repair ownership.

### OUT-001: Keep delivery and architecture outside scope

- **Status**: confirmed
- **Statement**: Complete the source fix and validation, but do not publish a release, push remotely or modify the user's global installation without separate authorization. Do not change template command formats or redesign the transaction architecture. This confirmation does not authorize a Git commit.

## Open questions

None. No blocking assumptions remain.

## Confirmation log

### 2026-10-30

The final summary proposed repair of both writers, success/error/integration regression tests, unchanged safety and transaction semantics, and exclusion of release, push and global-package modification. The user requested that ownership be decided immediately. The refined proposal retained closefd=False with function-owned descriptors, nested-finally close/unlink, no close retry, narrow FileNotFoundError suppression and standard Python exception chaining. Asked to accept that direction together with the repair scope, the user replied “采用”. NEED-001, NEED-002, CON-001, DEC-001 and OUT-001 are confirmed. No superseded confirmed entry exists.
