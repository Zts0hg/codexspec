# Verification: Comprehensive English README Audit

## Scope and Environment

Product change: README.md. Supporting records: this feature directory only.
The source checkout remains on main; implementation and checks use the dedicated
`2026-1012-2306uu-readme-feature-audit` worktree. Checks use its own editable package and uv-managed
CPython 3.11.13, with dev/docs extras installed from the frozen lockfile.

## Checks

| Check | Command / Method | Status and Evidence |
|-------|------------------|---------------------|
| CLI syntax | `uv run --no-sync codexspec --help`, `init --help`, `config --help`, `codexspec version` | Exit 0 for all four calls; six public commands and documented options verified |
| Capability/options/local links | Temporary AST and link checker outside the repository | Exit 0: 28 agent commands, 6 public CLI commands, 9 init options, 10 config options, 152 local links/anchors and 12 Markdown files |
| Standard language codes | `codexspec config --list-langs`; temporary AST/list comparison | Exit 0: all 13 standard identifiers match current LANGUAGE_ALIASES, including `pt` |
| Knowledge capture descriptions | Profile guidance, distill Operating Model/Extraction/Debounce and confirmed NEED-005 | Ordinary-session, mid-task and wrap-up paths, policy scope, de-duplication and no-write early exit traced |
| PR specification argument | Current pr Spec Resolution and temporary README argument/file check | Exit 0: the documented returned-feature-path example resolves to readable spec.md text |
| Desktop guide preservation | Exact comparison with `git show a0ab7fa:README.md` | Guide between its heading and Prerequisites is byte-equivalent |
| Markdown rendering | `uv run --no-sync python` with Markdown tables/fenced-code extensions | Exit 0; 14 tables, all row widths match their headers |
| Markdown style | `npx --yes markdownlint-cli@0.42.0 README.md '.codexspec/specs/2026-1012-2306uu-readme-feature-audit/*.md'` | Exit 0 on final closure |
| Distribution consistency | `uv run --no-sync python internal/command_template_fragments.py --check-distribution` | Exit 0 |
| Existing test suite | `uv run --no-sync pytest -q` | PASS: all 85 test files rerun in three independent groups; 2347 passed, 54 skipped, all three exit 0 |
| Whitespace / product scope | `git diff --check`; status inventory comparison | Exit 0; only README.md outside this feature directory |

## Verification Method

The temporary checker derives command registrations and option names from Python
AST, compares them with README tables, resolves Markdown/HTML relative paths and
GitHub-style heading anchors, checks every audit inventory row, compares the
preserved desktop installation guide to the baseline, and rejects out-of-scope
Git changes. Source behavior and confirmed history are independently inspected
for prose/default semantics; a word-coverage check alone does not establish
correctness.

The repository declares markdownlint-cli 0.42.0 in its pre-commit configuration.
An initial latest markdownlint-cli2 invocation enabled newer table rules outside
that declared version; verification uses the declared version. Source-link labels
that were interpreted as Markdown emphasis were corrected before the passing run.
Read-only execution also established that the baseline's `codexspec --version`
example is unsupported (exit 2); the README now uses `codexspec version`.

## Final Review Boundary

The implementation workflow runs an isolated complete-feature defect gate after
required checks are green. Review state, fingerprints, envelopes, and any neutral
follow-up obligations are stored outside the repository as required by the review
protocol. This file records deterministic verification; the gate's terminal
verdict is emitted by the independent review and reported at handoff.

## Limitations

Documentation verification establishes inventory coverage, navigability, syntax,
and consistency with current source/contracts. It does not measure autonomous
agent effectiveness or execute mutating user workflows. Other-language READMEs
and reference-site drift remain outside the confirmed product scope.

## Complete Suite Recheck

The earlier complete invocation found a missing `--audit` token in the README
command-table row (one failed, 2346 passed, 54 skipped). That row now explicitly
documents the audit invocation, and the targeted 16 documentation-contract tests
pass. The complete recheck covers every test file, without omitting cases:

1. Sort all `tests/**/test_*.py` paths; the repository declares that discovery
   pattern and `testpaths = ["tests"]`.
2. Assign files to groups by their sorted index modulo three.
3. Run each group with `uv run --no-sync pytest -q -p no:cacheprovider
   --basetemp <external-fixtures> <group-files>`, using a distinct external fixture
   directory per group.
4. Verify all group exit codes and that passed plus skipped totals the original
   2401 collected cases.

| Group | Passed | Skipped | Exit |
|-------|--------|---------|------|
| 0 | 867 | 14 | 0 |
| 1 | 602 | 15 | 0 |
| 2 | 878 | 25 | 0 |
| Total | 2347 | 54 | All 0 |

The fixture directories are outside any Git checkout. Full command lists and
logs are retained by the temporary test runner; no source or test files changed.
Verification completed on 2026-10-13.

## Initialization Prompt Verification

The README distinguishes first-time language selection from migration, update,
and constitution-compliance confirmations. `--force` auto-confirms the latter;
it does not bypass a first-time TTY language selection when the language base
cannot be determined. This matches the current init predicates and confirmed
language-init requirements CON-003, CON-005 and DEC-002.

`.venv/bin/python -B /private/tmp/codexspec-readme-language-probe.py` exits 0.
The temporary probe intercepts init before any project write and verifies six
conditions: first-time TTY with force, explicit base language, all three language
dimensions, a partial dimension, non-TTY input, and existing configuration.
The first and partial-dimension cases reach language selection; the others do
not. External fixture contents remain unchanged in every case.

The applicable documentation tests (16 passed), Markdown style, local links,
capability/options/scope checks, distribution consistency and whitespace checks
all pass after the wording correction. The complete 85-file suite is also
repeated using the method above: groups report 867/14, 602/15 and 878/25
passed/skipped, all exit 0, totaling 2347 passed and 54 skipped. Exact commands
and logs are retained in the external test runner's manifest. No new source or
test files are introduced.

## Knowledge Capture and Language Code Verification

The Project Knowledge introduction covers installed guidance to capture reusable
knowledge during ordinary conversations, fixes outside SDD, and long
implementation runs, separately from the configurable wrap-up hooks. Repeated
triggers process new material only; across sessions, the existing profile is
checked to avoid duplicate records. No reusable material causes a no-write early
exit. These claims are traced to `src/codexspec/profile.py`, the distill template's
Operating Model/Extraction/Debounce, and confirmed distill-effectiveness NEED-005.
No autonomous-capture effectiveness claim is tested or introduced.

`uv run --no-sync codexspec config --list-langs` confirms 13 standard codes with
`pt`. The temporary language-code checker initially exits 1 with missing `pt`
and extra `pt-BR`; after correction it exits 0, comparing every documented code
with LANGUAGE_ALIASES. The README also distinguishes localized documentation and
translation-resource `pt-BR` from the standard CLI identifier.

The checker invocation is `.venv/bin/python -B
/private/tmp/codexspec-readme-language-codes-check.py <workspace>`. Relevant
existing documentation tests report 16 passed. Local-link/options/scope checks,
Markdown lint, distribution consistency, whitespace, the six-condition init
probe and 14-table render check all exit 0. The complete 85-file suite is rerun
using the same three-group method: 867/14, 602/15 and 878/25 passed/skipped,
all exit 0, totaling 2347 passed and 54 skipped. Commands and logs remain in the
external test runner's manifest; no source or test files change.

## PR Specification Input Verification

The Git Workflow example passes `<feature-dir>/spec.md` to `pr --spec`.
The accompanying prose distinguishes specification file paths from feature
directory names or prefixes, which the command resolves to spec.md. This matches
the current PR template's Spec Resolution contract: explicit paths are read
directly as specification files; directory paths alone do not supply that text.
The other feature-directory examples are inspected against their own command
contracts and do not share this mismatch.

`.venv/bin/python -B /private/tmp/codexspec-readme-pr-spec-file-check.py
<workspace>` exits 0: it extracts the current README example, substitutes the
actual returned feature directory, resolves a regular file and reads 5592 bytes
of specification text. Source contract inspection establishes the name/prefix
lookup behavior. Verification does not execute PR publication or an agent's
best-effort Context extraction.

The corrected example passes the existing 16 documentation tests, Markdown lint,
local-link/capability/options/scope and 13-language-code comparisons, distribution
consistency and whitespace checks. The complete 85-file suite is rerun using
the documented three-group method: 867/14, 602/15 and 878/25 passed/skipped,
all exit 0, totaling 2347 passed and 54 skipped. Exact commands/logs are retained
in the external test runner's manifest; no program or test files change.
