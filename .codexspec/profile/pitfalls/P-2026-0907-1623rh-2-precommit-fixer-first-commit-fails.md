### P-2026-0907-1623rh-2: pre-commit fixer hooks fail the first commit attempt by rewriting the newly staged files

- claim: In a repo whose pre-commit config includes format-fixing hooks (markdown whitespace/header formatters, end-of-file fixers), a commit's first attempt fails whenever the staged files need fixes — the hook rewrites the files in the worktree and exits non-zero; the correct response is to re-stage and commit again, not to investigate a defect.
- type: pitfall
- scope/when: committing newly added markdown/config files in a repo with pre-commit fixer hooks (here: this repository's markdown hooks)
- root-cause: fixer hooks modify files in place during the hook run and report "files were modified by this hook", which aborts the commit so fixes are never silently swallowed; the working tree then already holds the corrected content while the index still holds the original.
- workaround: after the failed attempt, re-run `git add` on the hook-modified paths (they show as staged-with-local-modifications, `AM`, in `git status`) and repeat the commit; the second pass succeeds because nothing needs fixing anymore. Hook-time tree consistency is a separate trap: [[P-2026-0902-054178-4]].
- lesson: a first-attempt commit failure from a fixer hook is the tool working as designed, not a blocker; distinguish fixer failures (content was corrected for you — re-stage) from genuine test failures (content is wrong — fix it) before reacting.
- evidence.facts: the feature commit `feat(distill): append semantic slug to profile record filenames` failed its first attempt ("files were modified by this hook") on the newly added spec markdown artifacts; re-adding the spec directory and re-committing passed all hooks including the full pytest run (commit 5e00015).
- evidence.state: confirmed at feature 2026-0907-1623rh (2026-09-07). Still valid.
- provenance: distill @implement-tasks, 2026-09-07, derivation: inferred, confidence: high
- status: candidate
- consolidation: candidate; cluster: precommit-hook-behavior
