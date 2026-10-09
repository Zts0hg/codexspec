### P-2026-1008-1952ti-1: Relocated Python environments retain checkout paths

- claim: After moving a worktree or copying its Python environment into a verification mirror, verify executable and import locations before trusting checks.
- type: pitfall
- scope/when: moving a development worktree or preparing a disposable verification clone with an already-installed Python environment
- root-cause: console-script shebangs and editable-install path files retain absolute locations from the old checkout; a copied macOS interpreter can also depend on a relative libpython library absent from the destination. Git worktree relocation does not rewrite these environment references.
- workaround: for implementation, recreate the destination environment from the project dependency configuration when available; for read-only review, copy already-installed dependencies and required runtime files without installing, redirect editable imports and launch paths into the mirror, and verify `sys.executable`, `sys.prefix`, and `codexspec.__file__` before executing checks. Reject verification if the selected code still resolves outside the mirror. Keep PATH aligned with the chosen interpreter as described in [[P-2026-1003-204985-6]].
- lesson: filesystem relocation preserves bytes, not the runtime meaning of embedded paths; prove executable and import provenance independently of Git checkout identity.
- evidence.facts: moving the feature worktree left console scripts pointing at its former path. Destination imports and launchers were repaired, then the full suite passed. In an independent specialist mirror, the copied macOS executable initially failed to find relative libpython; copying the installed library restored execution, and 346 targeted tests passed with import locations proven inside the mirror.
- evidence.state: observed on macOS during feature 2026-1008-1952ti at reviewed commit abe030a; applies to relocated environments, not unchanged installations.
- provenance: distill @implement-tasks, 2026-10-09, derivation: inferred, confidence: high
- status: candidate
