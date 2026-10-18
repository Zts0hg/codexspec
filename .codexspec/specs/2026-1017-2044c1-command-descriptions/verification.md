# Verification: Command Descriptions

## Scope and semantic checks

- Reviewed all 28 current command bodies and relevant referenced instructions;
  evidence is recorded in inventory.md.
- Compared all 56 English/Chinese strings against the approved table in
  description-proposals.md: exact equality in sources, catalogs, Chinese fallback
  descriptions and generated host entries.
- Read all 168 translations in Japanese, Korean, German, French, Spanish and
  Brazilian Portuguese against the approved meaning and compact wording rule.
- Compared each of the 112 changed Markdown command surfaces against HEAD after
  excluding the description line: all other content, including argument hints,
  is byte-identical.
- Compared all eight JSON catalogs against HEAD after removing the 28 description
  values: every other field and command key is unchanged.
- Compared installer Python ASTs after replacing description constants: identical,
  so installer logic, ordering and membership remain unchanged.
- Version, README/site, packaging configuration and repository-only command
  descriptions are unchanged.

## Executed checks

- `.venv/bin/python internal/command_template_fragments.py --check-distribution`:
  passed.
- `.venv/bin/pytest tests/test_translation_files.py tests/test_translator.py
  tests/test_codex_integration.py tests/test_review_code_templates.py
  tests/test_sdd_workflow_templates.py tests/commands/test_installer.py -q`:
  252 passed. Updated existing wording expectations and parsed Codex YAML to
  verify its description without assuming whether the renderer quotes the scalar.
- Installed 28 commands in both integrations for all eight languages using normal
  `ClaudeIntegration.install` and `CodexIntegration.install_skills`: all 448
  installed frontmatter values equal their locale catalogs.
- Ran `codexspec init . --force --ai both --no-git --lang zh-CN` in a temporary
  project, followed by `codexspec list-commands`: both passed; all 28 commands
  and the updated Chinese descriptions appear. Temporary paths were resolved
  to avoid macOS `/var` symlink rejection by the existing helper safety check.

- `.venv/bin/pytest tests/test_installation_metadata.py
  tests/test_installation_release.py -q --tb=short`: 35 passed after updating two
  existing assertions that still expected the old specify description.
- `.venv/bin/python -m internal.maintainer_doc_skills --check`: passed without
  changes; feature artifact links also resolve.

## Full-suite baseline

The complete `pre-commit run --files <all changed and new files>` check passed
with the workspace virtual environment and `PYTEST_ADDOPTS="-n 4 --dist loadfile"`.
All applicable hooks passed: Ruff lint/format, mypy, Bandit, whitespace/EOF,
large-file and conflict checks, debug statements, Markdown lint, pip-audit and
the full pytest suite. Hooks without matching file types were not applicable.

The first full-suite attempt identified a stale Chinese specify assertion in the
installation release test. Both remaining old Chinese assertions were updated;
the targeted installation tests and the subsequent full-suite hook passed.
No runtime repair was necessary.

Raw successful check log:
`/private/var/folders/km/2hlzbxcj4d39bwq69wrxm9_c0000gp/T/codexspec-description-checks-hj5i8lie/pre-commit.log`.
The external review state retains verification evidence alongside its final result.

## Scenario self-check

These tasks only revise descriptive metadata; tasks.md contains no implementation
scenario requiring a new runtime test. The existing installation and parsing
checks above exercise both supported hosts and every supported language.

## Pre-push package verification

A fresh wheel and sdist exposed one additional packaging assertion that expected
the old review-code description. The archive's command bytes already matched
the current source. Updated only that assertion to the approved description.
With `CODEXSPEC_DIST_DIR` set to the fresh build,
`pytest tests/test_package_contents.py tests/test_distill_review_packaging.py -q`
passes all 18 tests. The strict MkDocs build also passed in an isolated environment.
