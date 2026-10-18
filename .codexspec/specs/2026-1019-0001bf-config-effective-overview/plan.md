# Implementation Plan: Effective Configuration Overview

**Related Design**: [design.md](design.md)

## Context

Deliver the design through CodexSpec's authored config command and its existing derived distribution files. The command's current no-argument branch selects an action before showing stored YAML. The change inserts a read-only overview ahead of that choice.

## Goals / Non-Goals

**Goals:** Render two accurate tables for the selected checkout, then offer the three confirmed actions.

**Non-Goals:** Change the CLI config panel, `--view`, the no-project wizard, the configuration schema, or existing write routing.

## Repository Constraints

- Edit `internal/command_templates/sources/config.md`, not derived command copies. Run the fragment renderer to update `templates/commands/config.md`, then use the established installer to refresh the repository's Claude and Codex copies.
- Preserve the project's two-constitution distinction and packaging boundary; no new runtime or package path is needed.
- Execute mutations only in this feature worktree. The overview itself reads the invoked checkout without acquiring a write worktree.

## Plan-Level Decisions

### Decision 1: Verify the no-argument contract before distribution rendering

- **Context**: The behavior is encoded in Markdown instructions and multiple copies are derived from the authored source.
- **Decision**: Add a focused template contract check for the two tables, supported fields, exclusions, default rules, and action order; edit the authored source; then regenerate and run the distribution consistency check.
- **Rationale**: The test guards the user-visible command contract while the existing distribution check catches copy drift.
- **Covers**: REQ-001, REQ-002, REQ-003, REQ-004, REQ-005; **Design**: No-argument command flow; supported-field overview definition; effective-value resolution; distribution outputs

## Implementation Phases

1. Add focused assertions for the no-argument overview's field inventory, two-table presentation, fallback guidance, and three action choices. Use representative sparse and overridden configuration examples in the command instructions, or a focused executable fixture where the existing test harness supports it. — **Covers**: REQ-001, REQ-002, REQ-003, REQ-004, REQ-005; **Design**: Supported-field overview definition; effective-value resolution
2. Update the no-argument branch in `internal/command_templates/sources/config.md` to render metadata and adjustable settings before the action prompt. Keep `--view`, missing-file handling, and existing modify/reset handlers separate. — **Covers**: REQ-001, REQ-002, REQ-003, REQ-004, REQ-005; **Design**: No-argument command flow; supported-field overview definition; effective-value resolution
3. Regenerate the complete command and both repository install copies using established tooling. Verify the installed forms contain the same overview contract. — **Covers**: REQ-001, REQ-005; **Design**: Distribution outputs
4. Run focused tests, the distribution check, and applicable repository lint/documentation checks. Inspect the final diff for accidental CLI, `--view`, or missing-config changes. — **Covers**: REQ-001, REQ-002, REQ-003, REQ-004, REQ-005; **Design**: No-argument command flow; distribution outputs

## Verification Strategy

- Focused tests validate the exact inventory of three metadata and nine adjustable fields, the omission of `language.templates`, effective-default instructions, and action order.
- `uv run python internal/command_template_fragments.py --check-distribution` validates authored, complete and installed command consistency.
- Run relevant existing config template and installer tests; run broader required quality gates if shared generation paths change.
- Review the Git diff and confirm no changes to `src/codexspec/__init__.py` or unrelated configuration flows.

## Risks / Trade-offs

| Risk | Impact | Mitigation |
|---|---|---|
| A displayed default diverges from the runtime rule | Users make decisions from incorrect values | Validate each rule against current code and historical confirmed requirements; keep focused contract assertions |
| Derived command copies drift | Hosts show different prompts | Regenerate with existing tooling and run distribution consistency check |

## Requirements Coverage

| Spec requirement | Design component | Plan coverage |
|---|---|---|
| REQ-001 | No-argument command flow | Phases 1–4 |
| REQ-002 | Supported-field overview definition; effective-value resolution | Phases 1–2, 4 |
| REQ-003 | Supported-field overview definition; effective-value resolution | Phases 1–2, 4 |
| REQ-004 | No-argument command flow | Phases 1–2, 4 |
| REQ-005 | No-argument command flow; distribution outputs | Phases 1–4 |
