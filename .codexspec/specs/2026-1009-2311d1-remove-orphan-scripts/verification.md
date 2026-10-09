# Verification: Remove orphaned nested script copies

## Scope and Baseline

- Baseline: `d7f053329f4582053d102935ca5f6fee5a69393e` (main, v0.7.19).
- Original cleanup: `7fdfe17ed6adc9181b39db2b5d90bf72aa666b4d`.
- Production delta: exactly six deleted nested copies listed in requirements.md.
- Environment: macOS, uv-managed Python 3.11.13, fresh feature-local environment.
- Imported editable code was checked against this feature checkout; wheel smoke imports
  were checked against an independent temporary installation outside the repository.

## Reference and Boundary Audit — T1 / REQ-001

Tracked-file searches covered slash and backslash spellings of both nested directories.
Before adding this feature's evidence, only two historical requirements files matched:

1. `.codexspec/specs/2026-0814-1548g5-distill-effectiveness/requirements.md`, OUT-004:
   records the legacy sequential-ID problem and excludes its repair from that feature.
2. `.codexspec/specs/2026-0818-2053p5-reverse-spec/requirements.md`, historical note:
   distinguishes the source/flat scripts from the obsolete copy and cites `7fdfe17`.
   That note described the branch-local removal; main still retained the files before
   this integration. The historical record was not rewritten.

No current executable consumer was found. Dynamic paths were inspected independently:

- `src/codexspec/__init__.py::get_scripts_dir` selects packaged `codexspec/scripts/`
  or repository `scripts/`; `init` selects `bash/*.sh` or `powershell/*.ps1` and copies
  by `script_file.name` into flat `.codexspec/scripts/`.
- `specify`, `checklist`, and `tasks-to-issues` templates and install copies reference
  flat helpers. Bash helpers source adjacent `common.sh`; PowerShell prerequisites
  load adjacent `common.ps1`.
- `pyproject.toml` includes authoritative `scripts/bash/` and `scripts/powershell/`
  in distributions; the deleted project-local copies are not packaging inputs.

Repository inspection cannot prove absence of unknown external manual invocations of
undocumented paths. No supported source or documented command path changed.

## Deterministic Results — T2/T3 / REQ-002–003

| Check | Command / method | Result |
| --- | --- | --- |
| Deletion scope | `git diff --name-only d7f0533` before staging feature docs | Exactly the six intended deletions |
| Supported bytes | Compare source trees and retained flat scripts against `git show d7f0533:<path>` | All byte-identical |
| Build | `uv build` | Wheel and sdist built successfully |
| Package bytes | Inspect ZIP/tar members and compare each supported script with its source | 20 comparisons passed: 10 scripts in each archive; no `.codexspec/` members |
| Installed execution | Temporary wheel install and Bash smoke sequence below | All success/error assertions passed |
| Full quality gate | `CODEXSPEC_DIST_DIR="$PWD/dist" uv run --no-sync pre-commit run --all-files --verbose` | All applicable hooks passed; pytest: 1976 passed, 50 skipped in 86.81s (0:01:26) |
| Staged-document gate | `uv run --no-sync pre-commit run --verbose` | Exit 0; all applicable hooks passed, including markdownlint |
| Distribution | `uv run --no-sync python internal/command_template_fragments.py --check-distribution` | Exit 0 |

The full quality gate includes Ruff, formatting, mypy, Bandit, whitespace/YAML/merge
checks, markdownlint, ShellCheck, the configured pip-audit hook, and pytest. The
configured pip-audit hook audits its selected tool environment; this change does not
modify dependency manifests. Newly added feature documents are checked separately
after staging because the first all-files hook invocation enumerated tracked files.

## Installed Smoke Procedure and Scenario Coverage

The temporary probe installed the freshly built wheel with
`uv pip install --target <temporary-install> --no-index --no-deps <wheel>`, put that
installation first on PYTHONPATH/PATH, and asserted `codexspec.__file__` resolved there.
It then performed these checks with explicit exit-code and content assertions:

1. Run `codexspec init <temporary-project> --no-git --ai both --lang en`.
   Assert all five installed Bash scripts match their supported sources byte-for-byte,
   and no nested `bash` or `powershell` destination directory exists (S1).
2. Set `workflow.worktrees: false` only in that disposable project. Run
   `bash .codexspec/scripts/create-new-feature.sh --name orphan-smoke`.
   Assert exactly one feature directory and its requirements.md are created (S3).
3. Run the installed `check-prerequisites.sh --json --paths-only --feature <feature>`;
   assert returned FEATURE_DIR matches. Run without `--paths-only` before plan.md
   exists; assert nonzero status and the missing-plan diagnostic (S3 error case).
4. Add a temporary plan.md, then run with `--require-tasks`; assert nonzero status and
   the missing-tasks diagnostic. Add tasks.md and run with `--require-tasks
   --include-tasks`; assert success and tasks.md in AVAILABLE_DOCS (S3).

S2 is covered by `tests/test_cli.py::TestInitScripts::test_init_copies_powershell_scripts_on_windows`
and the resolver-byte tests. S4 is covered by archive byte inspection and
`tests/test_package_contents.py`, including the installed-wheel worktree test with
CODEXSPEC_DIST_DIR set. S5 is covered by the full gate above. No new executable
functionality was added, so existing behavior tests and the direct smoke assertions
were used instead of a unit test that merely restates deleted filenames.

Native Windows/PowerShell execution was not performed on this Mac (pwsh is absent).
Platform-specific pytest skips remain skips; simulated Windows installation and exact
PowerShell archive bytes do not claim native execution.

## Review and Delivery Gates — T4 / REQ-003

The implementation evidence is prepared for the mandatory independent complete-feature
review. Its report/envelope are stored outside the repository under the review skill's
state-store contract. A valid complete PASS is required before main integration.

After PASS: commit the reviewed evidence/deletions, fast-forward local main where
possible, push without force, and compare local main, origin/main, and the remote
advertised ref. Check runs are inspected for the delivered SHA. CI's configured path
filters omit `.codexspec/scripts/**` and `.codexspec/specs/**`; no remote platform run
is claimed when that workflow is not triggered. Actual commit and synchronization
outcomes are reported at delivery, rather than predicted here.
