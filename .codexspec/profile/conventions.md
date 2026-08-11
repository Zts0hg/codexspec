# Conventions

Positive cross-feature conventions / steering. Current-effective only; git history is the ledger.

## Con-001: Adding a distributed command requires lockstep count/doc updates

- claim: When adding a new distributed slash command, update all of these together or a check drifts: (1) a `get_commands_metadata()` entry in `src/codexspec/commands/installer.py`; (2) the total in that function's docstring; (3) the inline `# <Category> Commands (N)` comment for the category; (4) the command-count assertions in BOTH `tests/commands/test_installer.py` AND `tests/test_cli.py`; (5) a row in all 8 `README*.md` files (translated per language). The derived `.claude/commands/` and `.agents/skills/` artifacts are regenerated at release (publish → init), never hand-edited.
- type: convention
- scope/when: adding a new command template under `templates/commands/` in the codexspec repo
- evidence.facts: The inline comment `# Enhanced Commands (4)` was already stale (actual enhanced count was 6) before this feature; the docstring count and two separate test files (`test_installer.py`, `test_cli.py`) each carried an independent `20`/`6` assertion that had to be bumped; the `test_cli.py` one was only caught when the full suite failed after the others were fixed.
- evidence.state: observed at feature 2026-0811-1418yq-debug-command (adding `debug`), base commit 8e69f51. Verified — full suite green (1064 passed) only after every count site was updated in lockstep.
- provenance: distill @implement-tasks, 2026-08-11, derivation: inferred
- status: candidate
