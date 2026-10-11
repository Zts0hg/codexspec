### P-2026-1010-21225w-1: Nested Git shell aliases reset a hook's invocation prefix

- claim: A Git hook adapter using a nested Git shell alias must preserve the original GIT_PREFIX explicitly to retain subdirectory-dependent validation.
- type: pitfall
- scope/when: delegating an existing Git hook through a nested Git shell alias while preserving the original hook contract
- root-cause: Git runs commit hooks at the repository root but provides the caller's subdirectory in GIT_PREFIX. A nested Git invocation recalculates that variable from its own working directory, replacing the caller's prefix even when the process inherits the environment.
- workaround: Capture whether GIT_PREFIX was present and its exact value before launching the nested Git process. Pass both as positional arguments to a static shell program, restore or unset GIT_PREFIX there, then exec the original hook with quoted arguments. Verify both root and subdirectory invocations against native Git, including hooks that refuse the subdirectory.
- lesson: Environment inheritance does not guarantee environment preservation when an intermediate executable rewrites variables. For same-repository hook delegation, preserve the hook contract; the separate foreign-repository environment-clearing rule still applies to unrelated Git subprocesses.
- evidence.facts: test_hook_prefix_refusal_matches_git_from_subdirectory in tests/test_commit_runtime_distribution.py reproduces a hook accepting a guarded subdirectory commit that native Git refuses. All six imported/standalone and pre-commit/prepare-commit-msg/commit-msg variants failed before preservation and passed afterward.
- evidence.state: Outcome-verified in feature 2026-1010-21225w on macOS; the 35-test runtime suite passed after the change. Native Windows/Linux validation remains outside that local evidence.
- provenance: distill @implement-tasks, 2026-10-11, derivation: inferred, confidence: high
- status: candidate
