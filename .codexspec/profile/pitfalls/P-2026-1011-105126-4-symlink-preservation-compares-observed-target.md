### P-2026-1011-105126-4: Symlink preservation compares the observed target

- claim: A test proving that a reader preserves a symbolic link must compare the observed link target before and after the read.
- type: pitfall
- scope/when: cross-platform tests that create symbolic links and assert a read operation leaves them unchanged
- root-cause: Windows can return an extended-length path prefix from `Path.readlink()` even when `symlink_to()` received an ordinary drive path. Comparing the returned path directly with the creation argument confuses representation with mutation.
- workaround: Capture `readlink()` after fixture creation, verify the intended readable/unreadable behavior, then compare the post-operation link target with the captured value. Keep the separate symlink-type and target-content preservation assertions.
- lesson: An immutability assertion compares actual before/after state; fixture construction syntax is not necessarily the filesystem's stored representation.
- evidence.facts: CI run 38192250056 at PR head 82ef10a failed four policy link preservation assertions on Windows with `//?/C:/...` versus `C:/...`; policy behavior assertions had already passed. Both representations are unequal as `PureWindowsPath` values.
- evidence.state: The affected policy and plugin runtime/guidance suites pass locally (54 tests). CI run 38196483598 at PR head cc5247bef2e8eadc1b1deb83b2d3aec5331b8783 passed both native Windows Python 3.11/3.12 jobs and the complete six-platform matrix on 2026-10-12.
- provenance: distill @PR CI investigation, 2026-10-12, derivation: inferred, confidence: high
- status: candidate
