# Design Document: Effective Configuration Overview

**Related Spec**: [spec.md](spec.md)
**Confirmed Requirements**: [requirements.md](requirements.md)
**Created**: 2026-10-19
**Status**: Draft

## Context

`$codexspec:config` is an agent-driven command distributed as Markdown. Its authored source is `internal/command_templates/sources/config.md`; `templates/commands/config.md` and the repository's Claude and Codex install copies are derived artifacts. The current no-argument path asks for an action before showing stored YAML. The required change is an overview before that choice; configuration writes remain in the existing flow.

## Architecture & Components

### No-argument command flow

- **Responsibility**: After verifying that `.codexspec/config.yml` exists, read the selected checkout's file, build the two overview tables, render them, then offer the three top-level actions. The view-only action exits without routing to a write workspace. Modify and reset reuse their existing branches.
- **Interface**: No-argument invocation of `$codexspec:config`; no new CLI option or config file format.
- **Covers**: REQ-001, REQ-004, REQ-005

### Supported-field overview definition

- **Responsibility**: The command source explicitly enumerates the three metadata rows and nine adjustable-setting rows, their user-facing meanings, and their default or fallback rules. It excludes `language.templates` and unknown YAML keys.
- **Interface**: Two Markdown tables with field, meaning, default or generation rule, and current value columns. All prose uses `language.interaction`.
- **Covers**: REQ-002, REQ-003, REQ-005

### Effective-value resolution

- **Responsibility**: Interpret stored values by the established rule for each row, including sparse YAML. Language rows use explicit value → `language.output` → `en`; `workflow.auto_next` enables only on literal `true`; `workflow.auto_distill` and `workflow.worktrees` disable only on literal `false`; absent `workflow.auto_maintenance` is `true`; absent `review.decided_by` is `reviewer`. Metadata rows report stored values, or absence, without synthesizing a stored value.
- **Interface**: Read-only interpretation of `.codexspec/config.yml` before the action prompt.
- **Covers**: REQ-002, REQ-003

### Distribution outputs

- **Responsibility**: Publish the edited authored command through the existing fragment renderer and command installer, keeping the complete public command and both repository install copies aligned. No new runtime component is installed.
- **Interface**: `internal/command_templates/sources/config.md` → `templates/commands/config.md` → `.claude/commands/codexspec/config.md` and `.agents/skills/codexspec-config/SKILL.md`.
- **Covers**: REQ-001, REQ-005

## Key Design Decisions

### Decision 1: Keep the overview in the existing command definition

- **Context**: The interactive behavior is specified in Markdown and executed by the host agent. A new Python CLI renderer would also change the excluded CLI surface.
- **Decision**: Add the two-table rendering contract to the existing command source and retain the existing action handlers.
- **Alternatives**: A shared Python renderer used by CLI and the agent command; a new config schema registry.
- **Trade-offs**: The field list and effective rules remain explicit instructions in the command source; tests must check them against established runtime defaults. This avoids a new packaged runtime and keeps CLI behavior unchanged.
- **Covers**: REQ-001, REQ-002, REQ-003, REQ-005

### Decision 2: Read before routing writes

- **Context**: The configured worktree policy routes mutations, while the overview is read-only and must describe the selected checkout's current configuration.
- **Decision**: Render tables from the invoked checkout. Only a later modify or reset selection enters the established write-routing path.
- **Alternatives**: Acquire a maintenance worktree before showing the overview.
- **Trade-offs**: The overview may describe a different checkout than the later write destination when isolation is enabled; the existing write flow must continue to report the destination path and its checkout-local setting before mutation.
- **Covers**: REQ-001, REQ-004, REQ-005

## Requirements Coverage

| Spec requirement | Design coverage |
|---|---|
| REQ-001 | No-argument command flow; overview definition; Decision 1 |
| REQ-002 | Supported-field overview definition; effective-value resolution |
| REQ-003 | Supported-field overview definition; effective-value resolution |
| REQ-004 | No-argument command flow; Decision 2 |
| REQ-005 | No-argument command flow; overview definition; distribution outputs; Decisions 1–2 |
