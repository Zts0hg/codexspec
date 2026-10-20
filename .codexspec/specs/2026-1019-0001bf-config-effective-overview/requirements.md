# Confirmed Requirements: Effective Configuration Overview

<!--
Language: Maintain this document in the language specified in .codexspec/config.yml.
This file is the authoritative, persistent record of user-confirmed intent.
-->

**Feature ID**: `2026-1019-0001bf`
**Status**: Discovery → Confirmed
**Last Confirmed**: 2026-10-19

## Authority Rules

- Only entries with `Status: confirmed` are binding downstream inputs.
- Open entries are not confirmed product requirements.
- A later explicit change supersedes the same matter while retaining unrelated earlier requirements.

## Background

The interactive `$codexspec:config` command currently asks which action to take before showing the configuration. Its view action prints the stored YAML. Sparse configuration files omit settings that nevertheless have effective defaults. The user wants the no-argument invocation to make the complete supported configuration understandable before choosing an action.

Relevant established contracts remain in force: `language.interaction` and `language.document` independently fall back to `language.output`, then `en` ([separate interaction and document language](../2026-0620-15087m-separate-interaction-doc-language/requirements.md)); `workflow.auto_next` defaults to `false` ([auto-next](../2026-0629-22061u-auto-next-command/requirements.md)); `workflow.worktrees` and `workflow.auto_maintenance` default to `true` ([feature worktrees](../2026-1003-204985-feature-worktrees/requirements.md), [review standards](../2026-1011-105126-review-code-standards/requirements.md)); and `review.decided_by` defaults to `reviewer` ([review convergence](../2026-1008-1952ti-review-convergence/requirements.md)).

## Needs

### NEED-001: Show a complete overview before action selection

- **Status**: confirmed
- **Statement**: When `$codexspec:config` is invoked without arguments and a project configuration exists, immediately show a readable configuration overview before presenting any action selection. Do not initially paste the raw contents of `.codexspec/config.yml` in place of the overview.
- **Rationale**: Users need to see the effective configuration, including omitted settings that use defaults, before deciding whether to change it.
- **User Evidence**: “不加任何内容的调用 codexspec:config 时，直接展示当前的配置。但需要注意的是，不是直接展示 config.yml 中的内容，因为 config.yml 中的内容可能缺失了某些未被配置的配置项，这些配置项使用着默认值。”
- **Confirmed At**: 2026-10-19

### NEED-002: Show all nine settings adjustable through config

- **Status**: confirmed
- **Statement**: One table lists every supported setting adjustable through the existing configuration entry points: `language.output`, `language.interaction`, `language.document`, `language.commit`, `workflow.auto_next`, `workflow.auto_distill`, `workflow.auto_maintenance`, `workflow.worktrees`, and `review.decided_by`. Each row gives the field name, its meaning, its default or fallback rule, and its current effective value.
- **Rationale**: A stored-only view hides absent settings and obscures what the command can manage.
- **User Evidence**: The user requested all configuration items with meaning, default and current value, reviewed the nine adjustable fields, and confirmed the revised two-table summary.
- **Confirmed At**: 2026-10-19

### NEED-003: Show project metadata separately

- **Status**: confirmed
- **Statement**: A separate metadata table lists `version`, `project.ai`, and `project.created`. Each row gives the field name, its meaning, its initialization or generation rule, and its current stored value. `project.created` has a creation-date rule rather than one fixed default date; `project.ai` has an init default but may be selected during initialization.
- **Rationale**: Metadata should be visible without implying that the interactive configuration modification flow can edit it.
- **User Evidence**: After reviewing the three metadata fields and the nine adjustable settings, the user said: “全部显示，但是元数据和可调整的配置项要作为两个表格分开展示。”
- **Confirmed At**: 2026-10-19

### NEED-004: Offer actions after the overview

- **Status**: confirmed
- **Statement**: Beneath the two tables, offer exactly these top-level choices: modify configuration, reset to defaults, and view only without changes. The view-only choice ends without writing. A host-supported structured choice may be used; otherwise present clear text choices and ask the user to select one.
- **Rationale**: The user can choose an action after seeing the complete overview.
- **User Evidence**: “然后在表格下方提示可以进行的操作（或者并询问用户希望进行哪项操作）：修改配置、恢复默认值、仅查看不需要改动。”
- **Confirmed At**: 2026-10-19

## Constraints

### CON-001: Calculate current values with established semantics

- **Status**: confirmed
- **Statement**: The settings table must display effective current values according to each setting's established fallback or absence rule, including settings omitted from YAML. The default column must describe dependent language fallbacks accurately rather than treating every language field as an independent fixed `en`. The overview must not claim an absent metadata field has a stored value.
- **User Evidence**: The user explicitly identified omitted configuration items using defaults as the defect to fix; the final summary confirmed calculation by existing fallback rules.

### CON-002: Preserve existing configuration operations and workspace routing

- **Status**: confirmed
- **Statement**: This feature changes the no-argument interactive `$codexspec:config` entry only. Existing modification and reset behavior, worktree write routing, `--view`, CLI `codexspec config`, and the missing-configuration wizard remain as they are. Read-only overview does not create a worktree or write configuration.
- **User Evidence**: The user confirmed the final summary stating these scope boundaries and the existing write rules.

## Decisions

### DEC-001: Use two tables with distinct purposes

- **Status**: confirmed
- **Decision**: Show metadata and adjustable settings in separate tables, each with field, meaning, default or generation rule, and current value columns. The metadata table contains only `version`, `project.ai`, and `project.created`; the adjustable-settings table contains the nine fields in NEED-002.
- **Alternatives Rejected**: One combined table; showing raw YAML as the initial overview.
- **Reason**: The user requested a complete but readable overview and explicitly separated metadata from configurable settings.
- **User Evidence**: “全部显示，但是元数据和可调整的配置项要作为两个表格分开展示。”

## Out of Scope

### OUT-001: Do not display `language.templates`

- **Status**: confirmed
- **Statement**: Omit `language.templates` from both overview tables. This fixed template-language field is neither one of the three requested metadata fields nor adjustable through the current configuration modification flow.
- **Reason**: The user explicitly excluded it after reviewing the complete field list.
- **User Evidence**: “language.templates 不需要显示。”

### OUT-002: Do not invent rows for unknown YAML keys

- **Status**: confirmed
- **Statement**: The overview covers the twelve supported fields named in NEED-002 and NEED-003, not arbitrary user-added YAML keys. Existing behavior for those other keys is unchanged.
- **Reason**: The confirmed summary defined “all fields” as the CodexSpec-defined fields within the selected two tables.
- **User Evidence**: The user confirmed the revised scope summary after this boundary was presented.

## Open Questions

_None blocking specification generation._

## Superseded Entries

_None._

## Confirmation Log

### Session 2026-10-19

- **Summary Presented**: No-argument interactive overview; two tables for three metadata fields and nine adjustable settings; meaning, default/generation rule and current value in each row; effective fallback values for omitted settings; three actions after the overview; existing `--view`, CLI, missing-config and write-routing behavior retained; unknown YAML keys excluded. `language.templates` was initially proposed as a non-adjustable field, then removed at the user's explicit request.
- **User Confirmation**: “全部显示，但是元数据和可调整的配置项要作为两个表格分开展示。” Then “language.templates 不需要显示.” The user confirmed the revised summary with “确认”.
- **Entries Confirmed**: NEED-001, NEED-002, NEED-003, NEED-004, CON-001, CON-002, DEC-001, OUT-001, OUT-002.
