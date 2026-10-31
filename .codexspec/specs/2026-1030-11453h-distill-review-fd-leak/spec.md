# Feature Specification: Distill Review Descriptor Lifetime

## Context and goals

The POSIX session and exclusive profile writers retain one raw file descriptor (FD) per write because their streams borrow rather than own the FD. Fix this bounded defect without altering review persistence, concurrency protection or recovery. Authority: [confirmed requirements](requirements.md).

## User scenario

A reviewer repeatedly saves staged decisions and applies profile changes in one process. Successful persistence must not cumulatively consume file descriptors, and an unsuccessful operation must not leave its successfully opened descriptor unmanaged.

## ADDED Requirements

### REQ-001: Function-owned raw descriptors

**Sources: NEED-001, DEC-001**

Both `SessionStore._atomic_at` and `ProfileTransaction._install_exclusive_at` MUST retain `closefd=False` and remain the sole owners of their opened raw file descriptor. After a successful open, every exit MUST attempt exactly one close; a failed open MUST NOT close an unowned descriptor. The existing stream context exits before raw closure. Caller-owned directory descriptors MUST remain usable. Correctly managed read methods MUST remain unchanged.

**Acceptance:** Sixteen repeated session replacements and sixteen distinct exclusive installations in a fresh POSIX process leave zero additional FDs after each completed operation and after each sequence, with correct file contents. Existing targets remain protected. No double close or closure of a reused descriptor occurs.

### REQ-002: Exception-safe cleanup

**Sources: NEED-001, NEED-002, DEC-001**

An outer finally MUST attempt raw close, with temporary unlink in a nested finally so close failure cannot skip unlink. The implementation MUST NOT retry close. Only FileNotFoundError from temporary unlink is ignored. Other cleanup errors propagate; standard Python exception context preserves preceding failures even if a cleanup failure becomes the outermost exception. No new aggregation framework is introduced. Actual FD release is asserted when close succeeds, not when the operating system reports close failure.

**Acceptance:** Inject failure at fdopen construction, fchmod, write, flush, file fsync, replace/link, directory fsync and unlink. Verify one close attempt after successful open, continued caller-directory validity, and preserved failure visibility. Exercise pre-existing-target rejection without overwrite. For close failure, verify one attempt and subsequent unlink; for simultaneous operation/cleanup failures, verify the exception chain. Verify successful atomic replacement tolerates its now-absent temporary path.

### REQ-003: Integration and regression evidence

**Sources: NEED-002, CON-001**

Regression tests MUST cover real SessionStore persistence and relevant transaction paths, including journal persistence and existing prepare/apply/rollback/recovery checks. New tests MUST fail against the unmodified leaking writers and pass with the repair. FD observation must not count its own transient directory handle and must avoid contamination by a long-lived test runner; bounded success-path measurement runs in an independent process. Fault injection must not mistake unrelated runtime FDs for writer-owned FDs.

**Acceptance:** Real repeated draft/runtime persistence is bounded; relevant transaction success, conflict and rollback/recovery tests pass. Existing symlink/hardlink and concurrency protections remain covered. Report commands, outcomes and platforms actually run; unavailable platform execution is explicitly pending rather than claimed successful.

### NFR-001: Preserve filesystem and transaction semantics

**Sources: CON-001, DEC-001**

Preserve O_EXCL/O_NOFOLLOW, pinned directory operations, session mode 0o600 and profile mode 0o644, content flush/fsync, atomic replace or exclusive link and subsequent directory fsync. Do not overwrite concurrent targets, alter journal stages or reverse recovery, regress fallback platforms, or silently suppress non-expected errors. No template changes or transaction redesign are needed.

**Acceptance:** The production delta only adds raw FD cleanup in the two writers; installed contents/permissions, existing conflict refusal and security/recovery tests remain correct. Non-POSIX-specific tests remain runnable; POSIX-only resource tests skip explicitly where prerequisites are unavailable.

## Constraints and decisions

Explicit raw ownership and nested-finally cleanup are binding, not implementation alternatives. Normal Python exception chaining is the selected error policy. No assumptions or open questions block design.

## Out of Scope

**Sources: OUT-001**

Release publication, remote push, global installation modification and Git commits are not authorized. Template command formats, transaction architecture, FD limits, forced GC and periodic restart are not repair targets.

## Requirements Traceability

| Confirmed entry | Coverage |
| --- | --- |
| NEED-001 | REQ-001, REQ-002 |
| NEED-002 | REQ-002, REQ-003 |
| CON-001 | REQ-003, NFR-001 |
| DEC-001 | REQ-001, REQ-002, NFR-001 |
| OUT-001 | Out of Scope |
