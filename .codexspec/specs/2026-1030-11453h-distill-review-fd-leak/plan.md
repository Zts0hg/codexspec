# Implementation Plan: Distill Review FD Leak

## Context and goals

Deliver design.md D1–D3 and K1–K2. Fix only the two confirmed writers and add resource regressions. No release, global installation update, remote push, commit, template change or architectural redesign.

## Plan-Level Decisions

### P0: Reproduce before modifying production code

**Covers: REQ-003; Design: D3, K2**

Use a worktree-local Python environment and existing pytest/ruff dev dependencies. Add regression tests first and observe the expected raw-FD failures, then implement the cleanup. This establishes that tests detect the reported defect, not merely successful file writes. Keep test fixtures outside Git checkouts and normalize temporary roots on macOS. No dependency or packaging changes are needed.

## Implementation Phases

### P1: Resource tests and red evidence

**Covers: REQ-001, REQ-002, REQ-003, NFR-001; Design: D3, K2**

Add tests/test_distill_review_fd_lifetime.py. Cover fresh-process repeated primitives and real persistence, targeted error injection, close/reuse behavior and transaction resource lifetime. Reuse existing record/transaction fixtures. Run new tests against the unchanged writers and record expected failures. Tests must clean their own leak observations safely even when testing the unfixed implementation.

### P2: Local cleanup repair

**Covers: REQ-001, REQ-002, NFR-001; Design: D1, D2, K1**

Change only the two finally blocks in session.py and transaction.py to the confirmed nested close/unlink structure. Run the new regression file until green, inspect the production diff to ensure permissions, conflict handling and synchronization remain untouched.

### P3: Integration verification and review

**Covers: REQ-001, REQ-002, REQ-003, NFR-001; Design: D1, D2, D3, K1, K2**

Run core, persistence and interface distill-review suites; run ruff on changed Python files, git diff --check, and broader applicable checks where available. Rerun the bounded external reproduction against the explicit worktree source. Map each task scenario to test evidence. Obtain the implement-tasks independent code review required by project policy; report unavailable review capability as a blocker, never as a pass. Do not claim Linux/Windows execution from local macOS results.

## Risks and trade-offs

| Risk | Mitigation |
| --- | --- |
| Test machinery opens unrelated FDs | Fresh process counts, targeted raw-FD observation for faults |
| Failure injection itself leaks or closes reused FDs | Save real OS functions and track ownership; explicit sentinel checks |
| Cleanup changes obscure the original failure | Assert Python exception context and no broad suppression |
| New worktree lacks dependencies | Create a local environment; never relink a moved environment |

## Requirements Coverage

| Requirement | Design | Plan |
| --- | --- | --- |
| REQ-001 | D1, D2, D3, K1 | P1, P2, P3 |
| REQ-002 | D1, D2, D3, K1, K2 | P1, P2, P3 |
| REQ-003 | D3, K2 | P0, P1, P3 |
| NFR-001 | D1, D2, D3, K1 | P1, P2, P3 |

No unresolved product decisions.
