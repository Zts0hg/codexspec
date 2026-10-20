# Delivery verification: two CodexSpec example applications

Date: 2026-10-18 (Asia/Shanghai). This record distinguishes the application
commits from the later CodexSpec README commit.

## Todo List

- Public repository: https://github.com/Zts0hg/codexspec-example-todo
- Published `main`: `ad63bd27f3235320e931145d869a9e74bc1aca4e`.
- An independent `git clone --no-local` at that exact detached commit, with a
  Python 3.12 virtual environment, passed empty-database migrations `0001`–`0006`,
  all 164 tests, Django `check`, and migration dry-run. Its browser audit covered
  six empty-state routes at 375px/1280px without overflow, and actual task
  creation, completion, trashing, and restoration. JSON backup and CSV export
  passed real HTTP checks. The repo has ten separate feature directories.
- A later unauthenticated HTTPS clone resolved to the same commit. The
  chronological guide's local links and 40-character Git references resolved;
  the MIT license and `language.output: en` were present. GitHub Actions
  [CI run 39087590918](https://github.com/Zts0hg/codexspec-example-todo/actions/runs/39087590918)
  completed successfully for that exact commit.

## Personal bookkeeping

- Public repository: https://github.com/Zts0hg/codexspec-example-bookkeeping
- Published `main`: `e024882c120d023eb7e545af01f3943bccfec414`.
- An independent `git clone --no-local` at that exact detached commit, with a
  Python 3.12 virtual environment, passed empty-database migrations `0001`–`0005`,
  all 235 tests, Django `check`, and migration dry-run. The fresh clone first
  required the documented local `data/` directory; without it, SQLite could
  not open the database, and migration was rerun after directory creation.
- The product-code parent commit
  `7106fc38f91a77baf29af731957f6ba24e3c5e59` was independently audited
  in a separate fresh clone. Browser checks covered 0/1/2 category-budget
  pages at 360px/1280px, unique DOM IDs, labels, focus and invalid POSTs.
  Real HTTP checks covered JSON backup, five-file CSV ZIP, monthly-report
  reconciliation, and upload/restore with a one-time success notice. The
  final commit above changes only verification and guide documents after that
  code commit. Its repo has 15 separate feature directories.
- A later unauthenticated HTTPS clone resolved to the final `main` commit.
  The chronological guide's 31 local links and 31 distinct 40-character Git
  references resolved; the MIT license and `language.output: zh-CN` were
  present. GitHub Actions
  [CI run 39087598546](https://github.com/Zts0hg/codexspec-example-bookkeeping/actions/runs/39087598546)
  completed successfully for that exact commit.

## CodexSpec README entry points

Both public repository URLs are linked in the English root README and all
seven translations. `markdownlint` passed on the eight changed READMEs;
99 relevant translation/glossary tests passed with one skipped test using
Python 3.13. The local Python 3.12 pytest runtime segfaulted during pytest
initialization, before collecting tests. The repository's full README
translation verifier reports the same 42 pre-existing differences on the
unmodified main checkout and this feature worktree; none was added by these
links. The new paragraphs were checked for the two identical URLs, language
labels, per-feature specifications, chronological guides, and runnable apps.
The CodexSpec commit and its CI result are recorded separately when pushed.
