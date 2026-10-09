### P-2026-1009-2311d1-1: Keep pytest fixture roots outside Git checkouts

- claim: Put repository-sensitive test fixtures outside every Git checkout, including disposable review mirrors.
- type: pitfall
- scope/when: choosing pytest --basetemp while verifying CodexSpec in a temporary mirror or running tests that distinguish repositories from plain directories
- root-cause: Git discovers a repository by walking parent directories. A fixture directory inside the mirror inherits its Git root even after Git environment variables are cleared. Tests intended to exercise non-repository behavior then use the mirror as their repository; configuration routing can write into that disposable mirror and invalidate later verification.
- workaround: create one dedicated external temporary parent with sibling repo/ and fixtures/ directories; run pytest in repo/ with --basetemp pointing to fixtures/. Before running, verify a plain fixture directory is outside a Git worktree and imported CodexSpec code resolves inside repo/. Keep caches and outputs outside the selected project. If a faulty run changes the disposable mirror, recreate it from the exact selected state before retrying; never repair or restore the caller checkout as part of review.
- lesson: clearing inherited Git environment and isolating parent-directory discovery are separate requirements. Changing cwd alone does not establish repository isolation. See [[P-2026-0829-0035hy-1]] and [[P-2026-1008-1952ti-1]].
- evidence.facts: During independent review, placing --basetemp inside the copied checkout produced `45 failed, 1926 passed, 55 skipped`; failures included `test_locate_rejects_non_repository`, `test_show_blueprint_reports_not_repository`, and configuration-routing tests. A fresh mirror with sibling fixture storage passed `1972 passed, 54 skipped in 80.83s`, without a production-code repair.
- evidence.state: observed while reviewing cleanup commit 94a1aab, feature 2026-1009-2311d1-remove-orphan-scripts; independent report and failed/successful logs retained under review fingerprint sha256:103b3619399aa9cc40c6020b8643321652d235f621c0e682866d883a9f6659db. The selected checkout stayed unchanged. Native-platform and installing smoke exclusions remain separately disclosed in the review.
- provenance: distill @implement-tasks, 2026-10-09, derivation: inferred, confidence: high
- status: candidate
