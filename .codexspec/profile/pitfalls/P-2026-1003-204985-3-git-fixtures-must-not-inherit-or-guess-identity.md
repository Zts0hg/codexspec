### P-2026-1003-204985-3: Git fixtures must not inherit or guess commit identity

- claim: Temporary Git repositories that commit must configure their own identity, and tests must prohibit identity inherited or inferred from the developer machine.
- type: pitfall
- scope/when: adding tests that create repositories, bare clones, or worktrees and execute commits or merges
- root-cause: A bare clone does not copy the source repository's local user.name/user.email. Local tests can still pass using global configuration or Git's inferred name/email, while a clean runner rejects the same commit. Clearing global configuration alone is insufficient when the local hostname permits inference.
- workaround: Set identity explicitly in every committing repository fixture, including bare remotes. Use the shared pytest isolation fixture, which selects a temporary global config with user.useConfigOnly=true, disables system config, and removes inherited author/committer identity variables. Do not add a universal test identity to the global config: that would conceal incomplete fixtures again.
- lesson: Repeated runs on one developer environment do not test environmental independence. Missing fixture prerequisites must fail locally as well as on CI.
- evidence.facts: PR #57 CI run 37134247115 failed while committing from a bare remote's linked worktree. An isolated probe returned exit 128 without local identity and exit 0 after setting it. Tests test_unconfigured_repository_cannot_inherit_or_guess_commit_identity and test_bare_fixture_worktree_has_explicit_commit_identity failed before the fix and passed afterward.
- evidence.state: Independently reproduced and verified during feature 2026-1003-204985; the shared pytest guard covers direct pytest and hook/CI invocations.
- provenance: distill during PR CI investigation, 2026-10-03; derivation: inferred; confidence: high
- status: candidate
