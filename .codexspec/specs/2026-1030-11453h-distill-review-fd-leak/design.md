# Design: Distill Review Descriptor Lifetime

## Context

Implement [spec.md](spec.md) under [requirements.md](requirements.md). Public APIs, stored data and command templates remain unchanged.

## Architecture & Components

### D1: Session atomic writer

- **Covers: REQ-001, REQ-002, NFR-001**
- `src/codexspec/distill_review/session.py`, SessionStore._atomic_at retains its signature and operation ordering. The existing finally becomes try-close/finally-unlink, with the existing narrow missing-path suppression inside unlink. os.open remains outside this try: no descriptor is owned when open fails. Borrowed streams exit before raw closure. No change to _read_at or path fallback.

### D2: Exclusive profile writer

- **Covers: REQ-001, REQ-002, NFR-001**
- `src/codexspec/distill_review/transaction.py`, ProfileTransaction._install_exclusive_at uses the same cleanup structure. FileExistsError translation to AtomicWriteConflictError and exclusive link remain unchanged; directory sync still precedes raw close.

### D3: Resource-lifetime regression suite

- **Covers: REQ-001, REQ-002, REQ-003, NFR-001**
- Add `tests/test_distill_review_fd_lifetime.py`. Parametrize both writers for local fault injection. Track the actual raw descriptor produced by the writer, rather than relying on global process counts in pytest. Assert it becomes invalid after closure, close occurs once, the directory stays valid, and temporary paths receive the required cleanup attempt. Test stream stages through a borrowing wrapper around the real stream; use saved real OS functions for observation and cleanup.
- A fresh subprocess uses a bounded fcntl(F_GETFD) scan without allocating enumeration handles. Run 16 repeated atomic writes, 16 exclusive installs and repeated real SessionStore draft/active/journal persistence; assert baseline after operations, contents and modes. Add transaction prepare/apply and rollback/recover resource observation using established fixtures. Imports and setup precede measurements. POSIX-only checks skip where directory-FD capabilities are absent; no new dependency is introduced.
- Run existing core, persistence and interface suites, including concurrency, symlink and recovery cases. Existing tests remain the regression authority for fallback behavior.

## Key Design Decisions

### K1: One explicit owner; no shared cleanup abstraction

- **Covers: REQ-001, REQ-002, NFR-001**
- **Context:** both readers already use explicit raw closure, while these two writers omit it.
- **Decision:** implement the confirmed DEC-001 literally in each writer, using nested finally. Do not extract a new helper for two short blocks.
- **Alternatives:** closefd=True introduces ownership-transfer handling; broader refactoring adds unrelated risk.
- **Trade-off:** retain two small identical cleanup blocks for local clarity and minimal scope. A close error is not retried. An unlink error may become outermost, preserving preceding errors through **context**.

### K2: Separate FD counts from failure instrumentation

- **Covers: REQ-002, REQ-003**
- **Context:** pytest and subprocess helpers may open unrelated descriptors.
- **Decision:** use a new process for bounded counts and targeted descriptor observation for fault injection. Simulated close failure must explicitly clean up any probe-owned resource afterward. A close-then-reuse test can reuse the numeric FD for a sentinel to detect a second close.
- **Trade-off:** POSIX resource assertions are skipped on Windows; existing portable regressions remain runnable. Platform execution claims track commands actually run.

## Requirements Coverage

| Requirement | Design |
| --- | --- |
| REQ-001 | D1, D2, D3, K1 |
| REQ-002 | D1, D2, D3, K1, K2 |
| REQ-003 | D3, K2 |
| NFR-001 | D1, D2, D3, K1 |

## Open items

None. No new product decisions or data formats are introduced.
