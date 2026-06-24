# Issues: implement-tasks-code-review

## Issue: T3 sync command (`codexspec init . --force`) is destructive — clobbers CLAUDE.md

- **Task**: T3
- **Error**: The plan's Decision 1 / T3 specified the self-bootstrap sync as `uv run codexspec init . --force`. Verified repository fact: `src/codexspec/__init__.py:776` writes `CLAUDE.md` whenever `force` is set (`if not claude_md.exists() or force:`), using the generic `_get_claude_md_content(...)`. Running it would overwrite this repo's hand-maintained `CLAUDE.md` (and would re-render all 21 commands). Constitution (line 724) and config (line 732) are preserved even under `--force`, but `CLAUDE.md` is not.
- **Attempted / Resolution**: Deviated per authority order (verified repository facts > approved plan). Regenerated **only** `.claude/commands/codexspec/implement-tasks.md` via the same helper `init` uses internally — `codexspec.translator.translate_template_frontmatter(content, "implement-tasks", "zh-CN", cache)` — which produces byte-identical output to `install_commands_to_subdir(force=True)` for that single file, touching nothing else.
- **Verification**: `git status` confirms only the expected files changed (template, test, derived `implement-tasks.md`, spec artifacts); `CLAUDE.md`, `config.yml`, constitution, scripts, and the other 20 commands untouched. Derived body matches the template (awk body-extraction diff = identical); frontmatter localized to `zh-CN` as expected.
- **Status**: Workaround Found — follow-up recommended: amend `plan.md` Decision 1 / T3 (and `CLAUDE.md` self-bootstrap guidance) to use the surgical per-command render instead of full `init --force`, OR teach `init` a non-destructive command-only sync path. Out of scope for this feature.
