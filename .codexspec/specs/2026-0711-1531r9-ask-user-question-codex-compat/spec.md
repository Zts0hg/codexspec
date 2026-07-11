# Feature Specification: ask-user-question-codex-compat

<!--
Language: Generate this document in the language specified in .codexspec/config.yml
If not configured, use English.
-->

**Feature Branch**: `2026-0711-1531r9-ask-user-question-codex-compat`
**Created**: 2026-07-11
**Status**: Draft
**Input**: Confirmed requirements record `requirements.md` in this feature directory.

## Context

CodexSpec now supports Codex CLI in addition to Claude Code (`.codexspec/config.yml` → `project.ai: "both"`). Two command templates currently hardcode the Claude Code tool name `AskUserQuestion`:

- `templates/commands/constitution.md:56` — `**IMPORTANT**: Use the \`AskUserQuestion\` tool to present structured choices.`
- `templates/commands/config.md:70` — `If configuration exists and no \`--view\` flag, present the management menu using \`AskUserQuestion\`:`

`AskUserQuestion` is a Claude Code tool. Codex CLI does not expose it; Codex's equivalent built-in tool is `request_user_input` (`codex-rs/core/src/tools/handlers/request_user_input_spec.rs:8`), with a different name and schema. Under Codex, the two hardcoded references name a tool the agent does not possess, so the structured-choice intent can silently fail.

Other templates use prose "ask the user" instructions that do not name a tool; those are already agent-brand-agnostic and are out of scope for this change.

### Key tool differences (Claude Code `AskUserQuestion` vs Codex `request_user_input`)

| Dimension | Claude Code `AskUserQuestion` | Codex `request_user_input` |
|---|---|---|
| Tool name | `AskUserQuestion` | `request_user_input` |
| Questions per call | 1–4 | 1–3 (prefer 1) |
| Required per question | `question`, `header`, `options` | adds `id` (snake_case) |
| Options per question | 2–4 | 2–3 |
| `multiSelect` | yes | no |
| `autoResolutionMs` | no | yes (60–240 s) |
| Availability | unrestricted | root thread only; Plan mode (or Default mode behind `DefaultModeRequestUserInput` flag) |

## Goals

- Make the 2 explicit `AskUserQuestion` references work correctly under both Claude Code and Codex by naming the known tool names without attributing them to specific agent brands.
- Keep the change minimal and forward-compatible with future agents (Gemini, Copilot, etc.).

## Non-Goals

- Rewriting prose "ask the user" instructions in other templates.
- Making the maintainer-internal auto-responder (`scripts/python/`) recognize Codex events.
- Retroactively editing historical spec archives.

## User Scenarios & Testing

### User Story 1 - Structured prompt works under Codex (Priority: P1)

As a developer running codexspec under Codex CLI, when I invoke `/codexspec:constitution` (no args) or `/codexspec:config` (interactive mode), I want the command to present a structured-choice prompt using Codex's native `request_user_input` tool, so that I can select an option interactively — instead of the command silently failing because it referenced a Claude Code-only tool.

**Why this priority**: This is the entire point of the change; without it the two commands are broken under Codex.

**Independent Test**: Run `/codexspec:constitution` under Codex (Plan mode) and confirm a structured prompt with selectable options appears.

**Acceptance Scenarios**:

1. **Given** `templates/commands/constitution.md` has been rewritten per REQ-004, **When** `/codexspec:constitution` is invoked under Codex, **Then** the agent calls `request_user_input` (its native tool) and presents the exploration-depth choices.
2. **Given** `templates/commands/config.md` has been rewritten per REQ-005, **When** `/codexspec:config` is invoked under Codex with an existing config and no `--view`, **Then** the management menu is presented via `request_user_input`.

### User Story 2 - No regression under Claude Code (Priority: P2)

As a developer running codexspec under Claude Code, when I invoke the same commands, I want the same structured-choice behavior as before, so the Codex compatibility change does not break the existing Claude Code experience.

**Why this priority**: Regression protection; must not be lost while fixing Codex.

**Independent Test**: Run `/codexspec:constitution` under Claude Code and confirm `AskUserQuestion` is still invoked with the same choices.

**Acceptance Scenarios**:

1. **Given** the rewritten templates, **When** `/codexspec:constitution` and `/codexspec:config` are invoked under Claude Code, **Then** the agent calls `AskUserQuestion` and the structured choices match the prior behavior.

### Edge Cases

- **Codex non-Plan mode / sub-agent**: `request_user_input` is unavailable. Because the rewrite does not exclusively force a single tool, the agent degrades naturally to a plain-text numbered list and waits for the user's selection (NFR-003). No crash, no silent no-op.
- **JSON example schema mismatch**: Each rewrite site is followed by a JSON example in Claude Code `AskUserQuestion` schema (no `id`). A Codex agent pointed at `request_user_input` may copy that schema and fail validation on the missing `id`. Handling is an open question (OPEN-003), not yet a confirmed requirement.

## Requirements

### Functional Requirements

- **REQ-001**: The 2 explicit `AskUserQuestion` references at `templates/commands/constitution.md:56` and `templates/commands/config.md:70` MUST be rewritten to an agent-brand-agnostic form that names the known structured-question tool names.
  - Sources: NEED-001, DEC-001, DEC-002
- **REQ-002**: The rewritten instruction MUST name both `AskUserQuestion` and `request_user_input` as a soft, non-exhaustive list (e.g., "e.g., `AskUserQuestion` or `request_user_input`") so each host agent selects the tool it possesses.
  - Sources: DEC-002
- **REQ-003**: The rewritten instruction MUST NOT contain the agent-brand strings "Claude Code" or "Codex".
  - Sources: DEC-002
- **REQ-004**: The exact replacement text at `templates/commands/constitution.md:56` MUST be:
  `**IMPORTANT**: Use the host agent's structured-question tool (e.g., \`AskUserQuestion\` or \`request_user_input\`) to present structured choices.`
  - Sources: NEED-001, DEC-002
- **REQ-005**: The exact replacement text at `templates/commands/config.md:70` MUST be:
  `If configuration exists and no \`--view\` flag, present the management menu using the host agent's structured-question tool (e.g., \`AskUserQuestion\` or \`request_user_input\`):`
  - Sources: NEED-001, DEC-002
- **REQ-006**: The fix MUST be applied to `templates/commands/` (the source of truth). The derived copies in `.claude/commands/codexspec/` and `.agents/skills/codexspec-*/` MUST NOT be hand-edited; when synced, they MUST be regenerated via `codexspec init`. This requirement states the *mechanism* (regenerate via `init`, never hand-edit); the *timing* of that regeneration — within this change or deferred — is governed by OPEN-001 and is not decided by this requirement.
  - Sources: CON-002
- **REQ-007**: Prose "ask the user" instructions in all other templates MUST remain unchanged.
  - Sources: DEC-001

### Non-Functional Requirements

- **NFR-001** (Intent preservation): The structured-choice behavior MUST be preserved under both Claude Code and Codex; the rewrite changes only how the tool is named, not the choices presented.
  - Sources: NEED-001, DEC-002
- **NFR-002** (Forward compatibility): The rewrite MUST NOT hardcode agent brands, so supporting a future agent (Gemini, Copilot, etc.) does not require another template rewrite.
  - Sources: DEC-002
- **NFR-003** (Graceful degradation): Under Codex modes/contexts where `request_user_input` is unavailable (non-Plan mode, sub-agent), the instruction MUST NOT force an unavailable tool; the agent MUST fall back to a plain-text question. Because no single tool is named exclusively, this degradation is intrinsic to the chosen wording.
  - Sources: CON-001, DEC-002

## Success Criteria

### Measurable Outcomes

- **SC-001**: 0 occurrences of the strings "Claude Code" or "Codex" in the 2 rewritten lines.
- **SC-002**: Both `AskUserQuestion` and `request_user_input` appear in each of the 2 rewritten lines.
- **SC-003**: 0 unintended changes to prose "ask the user" instructions in any other template.
- **SC-004**: After regeneration, the derived copies in `.claude/commands/codexspec/{constitution,config}.md` and `.agents/skills/codexspec-{constitution,config}/SKILL.md` match the `templates/commands/` source byte-for-byte at the rewritten lines.

## Out of Scope

- **Auto-responder system** (`scripts/python/`: `claude_monitor.py`, `claude_auto_responder.py`, `notify_telegram.py`): detects `AskUserQuestion` by name to drive the SDD pipeline. Excluded — separate follow-up concern. (OUT-001)
- **Historical spec archives** under `.codexspec/specs/2026-*/`: references to `AskUserQuestion` are historical snapshots and must not be retroactively edited. (OUT-002)
- **Prose "ask the user" instructions** in other templates: already agent-brand-agnostic, unchanged. (DEC-001)

## Assumptions

- **Assumption 1**: Under the DEC-002 wording, a Codex GPT-5 agent recognizes `request_user_input` as its native structured-question tool and calls it. If it misreads the instruction as a prose question, the structured-choice intent is lost. This risk was accepted by the user when choosing the "name the tools" mechanism over pure neutral wording. (Not used to expand scope.)
- **Assumption 2**: `codexspec init` regenerates both `.claude/commands/codexspec/` and `.agents/skills/codexspec-*/` from `templates/commands/` (verified: `src/codexspec/__init__.py` references both derivation targets).

## Open Questions

- **OPEN-001**: Are the 4 derived copies regenerated and synced within this change, or is sync deferred to the next `codexspec init`? Proposed default: regenerate within this change. (Affects deliverable boundary: 2 files vs 6 files.)
- **OPEN-002**: Verification approach, given no unit-test coverage for template content. Proposed default: manually run `/codexspec:constitution` and `/codexspec:config` under Codex (Plan mode) and under Claude Code to confirm structured prompts and no regression.
- **OPEN-003**: The JSON example following each rewrite site uses the Claude Code schema (no `id`). A Codex agent may copy it and fail `request_user_input` validation. Proposed default: keep the example as a structural illustration and add a one-line note that the field schema depends on the host tool (Codex `request_user_input` requires `id` per question and accepts 2–3 options). This open item may refine REQ-004/REQ-005 at implementation time but does not block the core rewrite.

> Open items remain questions. They MUST NOT be rewritten as confirmed REQ items.

## Dependencies

- None external. The change is confined to template text.

## Requirements Traceability

| Confirmed Requirement | Spec Coverage | Notes |
|-----------------------|---------------|-------|
| NEED-001 | REQ-001, REQ-004, REQ-005, NFR-001 | Core need: 2 refs rewritten, intent preserved |
| CON-001 | Context table, NFR-003 | Codex tool differences drive degradation behavior |
| CON-002 | REQ-006, SC-004, Assumption 2 | Templates are source of truth; derived copies regenerated |
| DEC-001 | REQ-001 (scope), REQ-007, SC-003, Out of Scope | Minimal scope; prose unchanged |
| DEC-002 | REQ-002, REQ-003, REQ-004, REQ-005, NFR-001, NFR-002, NFR-003 | Name tools, not agent brands |
| OUT-001 | Out of Scope | Auto-responder excluded |
| OUT-002 | Out of Scope | Historical archives not retro-edited |
