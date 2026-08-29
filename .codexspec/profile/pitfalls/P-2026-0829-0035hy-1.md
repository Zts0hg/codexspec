## P-2026-0829-0035hy-1: Foreign-repository Git subprocesses must clear repository-local environment variables

- claim: Git subprocesses that target a temporary or foreign repository must not inherit repository-local Git environment variables from the caller.
- type: pitfall
- scope/when: invoking Git against synthetic or external repositories from tests, hooks, or Git-launched tooling
- root-cause: Git hooks export variables such as `GIT_INDEX_FILE`, `GIT_DIR`, `GIT_WORK_TREE`, and object-directory overrides for the repository that launched the hook. Changing only the subprocess `cwd` does not override those variables, so a nested `git add` or `git init` can mutate the caller's index or common configuration, while even read-only commands can resolve evidence from the wrong repository.
- workaround: copy the process environment, remove every variable reported by `git rev-parse --local-env-vars`, and pass the sanitized environment to every Git subprocess that targets the foreign repository. Route both setup and assertion-time Git commands through the same helper, and keep a regression test that supplies a hostile caller-owned index and verifies it remains byte-for-byte unchanged.
- lesson: `cwd` selects a repository only when stronger Git environment variables are absent; repository isolation requires clearing the caller's local Git environment across all sibling subprocess call sites.
- evidence.facts: During the schema-v2 review evaluation change, a pre-commit pytest run caused a nested fixture `git add` to replace the linked worktree index and a nested `git init` to set the shared repository's `core.bare=true`; after the main helper was sanitized, remaining direct `git show` calls still failed under the same hook environment. Routing every foreign-repository Git call through the sanitized helper made the full pre-commit suite pass, and the regression test confirmed the caller-owned index was unchanged.
- evidence.state: observed and outcome-verified at feature 2026-0829-0035hy-review-code-systematic-coverage, commit 317fb43; still valid for Git 2.x hook environments.
- provenance: distill @commit-staged, 2026-08-29, derivation: inferred, confidence: high
- status: candidate
