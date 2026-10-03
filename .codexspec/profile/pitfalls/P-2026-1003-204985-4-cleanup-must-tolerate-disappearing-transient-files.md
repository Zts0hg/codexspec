### P-2026-1003-204985-4: Cleanup must tolerate disappearing transient files

- claim: Recursive cleanup of a temporary Git repository must tolerate transient files disappearing between enumeration, permission repair, and deletion.
- type: pitfall
- scope/when: removing temporary repositories or implementing shutil.rmtree permission-error callbacks
- root-cause: Git maintenance can remove maintenance.lock while shutil.rmtree is traversing it. A callback that unconditionally chmods and retries deletion raises FileNotFoundError even though the intended removal has already completed.
- workaround: Handle FileNotFoundError around both permission adjustment and deletion retry. Preserve PermissionError and other I/O failures. Exercise both disappearance windows deterministically instead of relying on a flaky CI reproduction or accepting a successful rerun as a fix.
- lesson: Distinguish completed cleanup from genuine inability to remove a file; retries alone do not eliminate a race.
- evidence.facts: CI run 34039054363 and attempt 1 of run 34115315777 both failed in tests/evals/review_code/run_eval.py::_retry_remove_writable on maintenance.lock. The callback was still unchanged during the PR #57 investigation. Two deterministic disappearance tests failed before the correction and passed afterward; a separate permission-failure test verifies that real errors still propagate.
- evidence.state: Historical logs and current-source reproduction agree; the evaluation runner's 32 tests pass after the correction.
- provenance: distill during PR CI investigation, 2026-10-03; derivation: inferred; confidence: high
- status: candidate
