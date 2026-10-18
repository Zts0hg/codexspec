# Feature Specification: Effective Configuration Overview

**Feature Branch**: `2026-1019-0001bf-config-effective-overview`
**Created**: 2026-10-19
**Status**: Draft
**Input**: [Confirmed requirements](requirements.md)

## Context and Goal

The interactive `$codexspec:config` command currently asks users to select an action before they can inspect settings. Its view action prints the stored YAML, which may omit settings whose effective values come from defaults. A no-argument invocation must instead show the complete supported overview first, then offer actions.

## User Scenarios

1. A user invokes `$codexspec:config` in a project whose YAML omits `workflow.worktrees`, `workflow.auto_maintenance`, and `review.decided_by`. The settings table still shows their effective values as `true`, `true`, and `reviewer`, respectively. The user can then choose an action.
2. A user has `language.output: zh-CN` and no explicit interaction, document, or commit language. The table identifies `output` as the fallback and shows the effective language for each omitted setting as `zh-CN`.
3. A user chooses “view only.” The command ends without writing configuration or creating a worktree.

## Functional Requirements

### REQ-001: Overview before actions

On a no-argument `$codexspec:config` invocation with an existing configuration, the command MUST display the two tables defined below before offering any action. The initial overview MUST NOT substitute a raw YAML dump for these tables.

- **Sources**: NEED-001, DEC-001

### REQ-002: Adjustable settings table

The adjustable settings table MUST contain exactly the following supported field rows. Each row MUST display the field name, plain-language meaning, default or fallback rule, and current effective value. Current values MUST use the same rules that control the corresponding behavior when a setting is omitted.

| Field | Default or fallback rule |
|---|---|
| `language.output` | `en` |
| `language.interaction` | Explicit value, then `language.output`, then `en` |
| `language.document` | Explicit value, then `language.output`, then `en` |
| `language.commit` | Explicit value, then `language.output`, then `en` |
| `workflow.auto_next` | `false`; only literal `true` enables |
| `workflow.auto_distill` | `true`; only literal `false` disables |
| `workflow.auto_maintenance` | `true` when absent; explicit value must be a YAML boolean |
| `workflow.worktrees` | `true`; only literal `false` disables |
| `review.decided_by` | `reviewer`; permitted values are `reviewer` and `ask` |

- **Sources**: NEED-002, CON-001

### REQ-003: Metadata table

A separate metadata table MUST contain exactly `version`, `project.ai`, and `project.created`, with field name, meaning, initialization or generation rule, and current stored value. It MUST describe `version` as the configuration format version initialized to `1.0`; `project.ai` as the AI integration selected at initialization, with `claude` as the init default; and `project.created` as the creation date generated at initialization, without claiming a fixed calendar-date default. If a metadata field is absent, the table MUST not present an invented stored value.

- **Sources**: NEED-003, CON-001, DEC-001

### REQ-004: Actions below the tables

After both tables, the command MUST offer only these top-level choices: modify configuration, reset to defaults, and view only without changes. It MAY use a host-supported structured question; a clear text prompt with these choices is acceptable when that tool is unavailable. The view-only choice MUST end without writing configuration or creating a worktree. The existing modify and reset flows continue after their respective selections.

- **Sources**: NEED-004, CON-002

### REQ-005: Scope and exclusions

The two tables MUST omit `language.templates` and MUST NOT add rows for arbitrary user-added YAML keys. This feature MUST leave the behavior of `$codexspec:config --view`, CLI `codexspec config`, and the no-config creation wizard unchanged. Existing configuration write routing MUST remain in force for modify and reset actions; producing the no-argument overview itself is read-only.

- **Sources**: CON-002, OUT-001, OUT-002

## Acceptance Criteria

1. With the repository's sparse `.codexspec/config.yml`, the no-argument command shows 3 metadata rows and 9 setting rows in two tables, including effective `true` for absent `workflow.auto_maintenance` and `workflow.worktrees`, and `reviewer` for absent `review.decided_by`.
2. If `language.output` is `zh-CN` while interaction, document and commit fields are absent, their current values show `zh-CN`; the default column explains the fallback chain rather than saying each field independently defaults to English.
3. The metadata table describes `project.created` as a date generated at initialization, displays its stored date when present, and indicates absence when missing.
4. `language.templates` and an unknown YAML key appear in neither table.
5. The three action choices appear after both tables. Choosing view only leaves the configuration and Git worktree state unchanged. Choosing modify or reset enters the existing respective flow.
6. `--view`, CLI `codexspec config`, and the missing-configuration wizard retain their existing behavior.

## Error and Boundary Behavior

- A missing `.codexspec/config.yml` follows the existing creation wizard rather than showing fabricated current values.
- A missing metadata field is shown as absent, because initialization values are not runtime fallbacks for stored metadata.

## Confirmed Constraints and Decisions

- Two separate tables distinguish metadata from adjustable settings (DEC-001).
- Current setting values follow the established runtime semantics, including omitted keys (CON-001).
- Only the no-argument interactive entry changes; read-only display does not route to a write workspace (CON-002).

## Out of Scope

- Displaying `language.templates` (OUT-001).
- Displaying arbitrary unknown YAML keys (OUT-002).
- Changing the CLI config panel, `--view`, the missing-config wizard, or existing modification and reset semantics (CON-002).

## Open Questions

None block design.

## Requirements Traceability

| Confirmed entry | Spec coverage |
|---|---|
| NEED-001 | REQ-001 |
| NEED-002 | REQ-002 |
| NEED-003 | REQ-003 |
| NEED-004 | REQ-004 |
| CON-001 | REQ-002, REQ-003 |
| CON-002 | REQ-004, REQ-005 |
| DEC-001 | REQ-001, REQ-003 |
| OUT-001 | REQ-005 |
| OUT-002 | REQ-005 |
