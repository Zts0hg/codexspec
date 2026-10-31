# Tasks: Distill Review FD Lifetime

## Execution order

T1 → T2 → T3. All work belongs to the selected feature worktree. No parallel writers, release, push or commit.

## T1: Regression tests and failing baseline

- [x] Add tests/test_distill_review_fd_lifetime.py and demonstrate expected failures against the unmodified writers.
- **Covers: REQ-001, REQ-002, REQ-003, NFR-001; Plan: P0, P1**
- **Dependencies:** None.
- **Outcome:** Executable tests distinguish raw-FD retention from correct contents and temporary-file cleanup.
- **Verification:** Run the new pytest module before production edits; record failures attributable to missing close. Clean probe-owned descriptors without masking assertions.

### Test Scenarios

- S01: Sixteen atomic replacements and sixteen exclusive installations in a fresh process restore FD baseline, preserve contents and 0o600/0o644 modes, and leave the directory FD usable.
- S02: Failed initial open owns no descriptor and does not close the directory.
- S03: fdopen construction failure closes the raw FD once and cleans the temporary path.
- S04: fchmod failure closes the raw FD once and cleans the temporary path.
- S05: write failure closes the raw FD once and cleans the temporary path.
- S06: flush failure closes the raw FD once and cleans the temporary path.
- S07: file fsync failure closes the raw FD once and cleans the temporary path.
- S08: replace/link failure closes the raw FD once and cleans the temporary path.
- S09: directory fsync failure closes the raw FD once; installed content and cleanup reflect the already completed install.
- S10: Existing exclusive target raises AtomicWriteConflictError, preserves original bytes and releases the raw FD.
- S11: Unexpected unlink failure propagates after raw closure; ordinary missing temporary path is tolerated.
- S12: Close failure is attempted once, still attempts unlink, preserves error visibility, and never closes a sentinel reusing the same FD number.
- S13: Simultaneous operation and cleanup failures preserve their Python exception context.
- S14: Repeated real draft/active/journal persistence restores FD baseline and remains readable.
- S15: Real transaction prepare/apply and rollback/recover paths do not retain writer FDs; existing conflict, source protection and recovery assertions remain satisfied.

## T2: Repair both writer finally blocks

- [x] Implement nested close/unlink in src/codexspec/distill_review/session.py and src/codexspec/distill_review/transaction.py.
- **Covers: REQ-001, REQ-002, NFR-001; Plan: P2**
- **Dependencies:** T1.
- **Outcome:** Both writers preserve explicit raw ownership and pass the regression matrix.
- **Test Scenarios:** S01–S13 from T1 exercise this same production change; each scenario applies to both writers except the exclusive-only S10.
- **Verification:** New tests green; production diff contains only the two cleanup changes, with existing read/fallback code unchanged.

## T3: Integration baseline, scenario self-check and independent review

- [x] Complete regression checks and the independent complete-feature review gate. Execution evidence is in verification.md; the completed code-state review is recorded under fingerprint `sha256:b582c822444392b3bc56e7fa826d1c0bab79600c9b683d474d8829a7b1440640` in the external review store.
- **Covers: REQ-001, REQ-002, REQ-003, NFR-001; Plan: P3**
- **Dependencies:** T2.
- **Outcome:** Verified feature, or explicit recorded blocker rather than an unsupported completion claim.
- **Test Scenarios:** S01 and S14–S15 plus existing core/persistence/interface conflict, symlink and recovery cases. Map S01–S15 to concrete tests in the completion evidence.
- **Verification:** New tests; existing distill-review suites; full pytest baseline; changed-file ruff; git diff --check; external bounded repro with explicit worktree import; independent review-code complete feature gate. Record actual platform and any unavailable checks.

## Coverage

| Plan | Requirements | Tasks | Scenarios |
| --- | --- | --- | --- |
| P0, P1 | REQ-001/002/003, NFR-001 | T1 | S01–S15 |
| P2 | REQ-001/002, NFR-001 | T2 | S01–S13 |
| P3 | REQ-001/002/003, NFR-001 | T3 | S01–S15 and existing regressions |

No unmapped tasks or open product questions.
