### P-2026-0902-054178-4: pre-commit stashes unstaged tracked changes but leaves untracked files in the hook-time tree

- claim: Splitting a feature into commits whose new untracked files must pair with tracked-file modifications that land in a later commit makes pre-commit hooks run against a self-inconsistent tree; commit interdependent new+modified sets together.
- type: pitfall
- scope/when: splitting a large change into multiple commits in a repo whose pre-commit hooks run repo-level consistency tests (here: a full pytest suite)
- root-cause: pre-commit temporarily stashes unstaged modifications to tracked files (restoring them afterwards) but does not remove untracked files. A tree where new sources exist (untracked, present) while the files they render into are reverted to an older state (tracked modifications stashed) is self-inconsistent, so repo-level tests fail inside the hook even though every final commit would be consistent.
- workaround: commit interdependent new-file + modified-file sets in one commit, or temporarily move the untracked counterparts out of the working tree for the earlier commit. Before committing a split, enumerate the exact tree state each hook will see: staged changes applied, unstaged tracked changes stashed, untracked files still present.
- lesson: repo-level tests judge the hook-time working tree, not the final commit; a commit split must be validated against the tree state each hook observes, not against the end state of the series.
- evidence.facts: two attempts to split the fragment-mechanism commit from the opt-in commit failed the repository self-bootstrap test inside pre-commit (`1 failed, 829 passed`) while the identical combined tree passed the full suite; the single combined commit passed the hooks.
- evidence.state: confirmed at feature 2026-0902-054178 rollout (2026-09-06); the final combined commit passed all hooks. Still valid.
- provenance: distill @release v0.7.15, 2026-09-07, derivation: inferred, confidence: high
- status: candidate
- consolidation: candidate; cluster: precommit-hook-behavior
