# AGENTS.md

<!-- CODEXSPEC START -->
## CodexSpec

This project uses CodexSpec for requirements-first spec-driven development.

Use these Codex skills when working on CodexSpec workflows:

- `$codexspec:constitution` to create or update project principles.
- `$codexspec:specify` to capture confirmed requirements.
- `$codexspec:generate-spec` to produce `spec.md`.
- `$codexspec:spec-to-plan` to produce `plan.md`.
- `$codexspec:plan-to-tasks` to produce `tasks.md`.
- `$codexspec:implement-tasks` to implement approved tasks.
- `$codexspec:distill` to capture reusable cross-feature knowledge into `.codexspec/profile/`.
- `$codexspec:evolve` to contribute vetted profile knowledge back upstream via a reviewed PR.

Before making workflow decisions, read `.codexspec/memory/constitution.md`.
<!-- CODEXSPEC END -->

## Maintainer Guide (developing CodexSpec itself)

This section is hand-authored (outside the managed block above) and applies whether you use Codex or Claude Code — the two context files are equal-status entry points.

The full maintainer development guide lives in **`CLAUDE.md`**: architecture and per-feature design notes, the self-bootstrap rule (edit `templates/` and `src/codexspec/`, never the derived `.claude/commands/` or `.agents/skills/`), and the two-constitutions distinction. It imports the project constitution (`.codexspec/memory/constitution.md`) and the repository layout / packaging boundary (`docs/internal/repository-layout.md`).

Read `CLAUDE.md` and `docs/internal/repository-layout.md` before changing templates, packaging, or `init` behavior.
