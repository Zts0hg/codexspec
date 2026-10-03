### P-2026-1003-204985-5: Mutation tests need explicit timestamp changes

- claim: A test that requires a changed file signature must establish that change explicitly instead of relying on elapsed filesystem clock ticks.
- type: pitfall
- scope/when: testing stat-signature checks with rapid same-size in-place file rewrites
- root-cause: Filesystems can report the same modification and change timestamps for two adjacent writes; unchanged inode, mode, size, and timestamps leave the signature identical even though bytes differ.
- workaround: When the test contract requires signature drift, explicitly advance mtime with os.utime and assert the changed-signature premise before exercising the check. Keep same-signature mutation contracts separate; a stat signature is not a content hash. Do not add sleeps or weaken the expected rejection.
- lesson: Nanosecond timestamp fields do not guarantee nanosecond clock resolution. Make race-test prerequisites deterministic across filesystems.
- evidence.facts: A fresh Linux/Python 3.12 container failed test_check_outputs_binds_content_to_returned_output_signature; a matching 1000-rewrite probe produced 936 unchanged signatures. Explicitly advancing mtime preserves the same-size mutation and makes the test premise observable.
- evidence.state: Reproduced during feature 2026-1003-204985 CI investigation; the fragment module passes locally with the deterministic fixture.
- provenance: distill during PR CI investigation, 2026-10-04; derivation: inferred; confidence: high
- status: candidate
