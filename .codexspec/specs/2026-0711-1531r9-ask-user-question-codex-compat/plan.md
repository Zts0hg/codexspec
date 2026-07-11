# Implementation Plan: ask-user-question-codex-compat

<!--
Language: Generate this document in the language specified in .codexspec/config.yml
If not configured, use English.
-->

**Related Spec**: `.codexspec/specs/2026-0711-1531r9-ask-user-question-codex-compat/spec.md`
**Confirmed Requirements**: `.codexspec/specs/2026-0711-1531r9-ask-user-question-codex-compat/requirements.md`
**Created**: 2026-07-11
**Status**: Draft

## Context

CodexSpec templates `constitution.md` and `config.md` hardcode the Claude Code tool name `AskUserQuestion`. Under Codex (now supported via `project.ai: "both"`), that tool does not exist; Codex's equivalent is `request_user_input`. The confirmed decision (DEC-002) is to rewrite the 2 explicit references so they name both tool names in a soft list but do **not** name agent brands, leaving each host agent to call the tool it possesses.

This is a small, surgical text change to 2 source templates, plus regeneration of the 4 derived copies, plus verification. No code, no data, no API surface.

### Verified repository facts

- Current text — `templates/commands/constitution.md:56`: `**IMPORTANT**: Use the \`AskUserQuestion\` tool to present structured choices.`
- Current text — `templates/commands/config.md:70`: `If configuration exists and no \`--view\` flag, present the management menu using \`AskUserQuestion\`:`
- Both lines are immediately followed by a JSON example in Claude Code `AskUserQuestion` schema (fields `question`/`header`/`options`; no `id`).
- Derived copies (must not be hand-edited): `.claude/commands/codexspec/constitution.md`, `.claude/commands/codexspec/config.md`, `.agents/skills/codexspec-constitution/SKILL.md`, `.agents/skills/codexspec-config/SKILL.md`.
- Regeneration mechanism: `codexspec init --force` overwrites regenerable command/skill files from `templates/commands/` while preserving user-authored content (config language updated surgically; existing CLAUDE.md body and constitution never overwritten) — `src/codexspec/__init__.py:510-521`, comment at `:899-903`.

## Goals / Non-Goals

**Goals:**

- Replace the 2 hardcoded `AskUserQuestion` references with agent-brand-agnostic wording that names both `AskUserQuestion` and `request_user_input`.
- Keep the change confined to the 2 source templates; regenerate derived copies.
- Preserve structured-choice behavior under both Claude Code and Codex.

**Non-Goals:**

- Rewriting prose "ask the user" instructions in other templates (DEC-001).
- Making `scripts/python/` auto-responder recognize Codex events (OUT-001).
- Editing historical archives (OUT-002).

## Component Structure

```
templates/commands/
├── constitution.md   ← C1: rewrite line 56 (+ optional schema note after JSON block)
└── config.md         ← C2: rewrite line 70 (+ optional schema note after JSON block)

Derived (regenerated, not hand-edited):
.claude/commands/codexspec/{constitution,config}.md
.agents/skills/codexspec-{constitution,config}/SKILL.md
```

### Component C1: `templates/commands/constitution.md` source edit

- Rewrite line 56 to the REQ-004 exact text.
- Add a one-line schema note after the JSON example block (PLD-002).
- **Covers**: REQ-001, REQ-002, REQ-003, REQ-004, NFR-001, NFR-002

### Component C2: `templates/commands/config.md` source edit

- Rewrite line 70 to the REQ-005 exact text.
- Add a one-line schema note after the JSON example block (PLD-002).
- **Covers**: REQ-001, REQ-002, REQ-003, REQ-005, NFR-001, NFR-002

### Component C3: Derived copy regeneration

- Run `codexspec init --force --here` (via `uv run` so the local `templates/` source is used) to regenerate the 4 derived copies.
- **Covers**: REQ-006, CON-002, SC-004

## Decisions

### PLD-001: Regenerate derived copies within this change (adopts OPEN-001 default)

**Context**: CON-002 forbids hand-editing derived copies; they must be regenerated via `codexspec init`. OPEN-001 asked whether regeneration happens in this change or is deferred.

**Options Considered**:

1. Regenerate within this change (via `codexspec init --force`).
2. Edit templates only; defer sync to the next `codexspec init`.

**Decision**: Regenerate within this change.

**Rationale**: Keeps the self-bootstrap repo immediately consistent (the repo's own `.claude/commands/codexspec/` and `.agents/skills/` reflect the fix right away). `codexspec init --force` is verified safe — it preserves user-authored content (`__init__.py:510-521`).

**Covers**: REQ-006, SC-004

**Decision Level**: Plan-level technical decision; does not change confirmed product scope. (Adopts the OPEN-001 proposed default confirmed at the requirements stage.)

### PLD-002: Add a one-line schema note after each JSON example (adopts OPEN-003 default)

**Context**: Each rewrite site is followed by a JSON example in Claude Code `AskUserQuestion` schema (no `id`). Since DEC-002 now explicitly names `request_user_input`, a Codex agent may copy that schema and fail `request_user_input` validation (missing `id`, wrong option count). OPEN-003 proposed adding a schema note.

**Options Considered**:

1. Keep the example as-is, add a one-line schema note.
2. Rewrite the JSON example to include `id` (Codex-valid).
3. Leave the example untouched.

**Decision**: Option 1 — keep the example, add a one-line note.

**Rationale**: Option 2 would make the example Codex-valid but Claude-Code-invalid (Claude `AskUserQuestion` does not require `id`) — trading one break for another. Option 3 leaves the mismatch that DEC-002 makes more likely. Option 1 is the smallest change that warns the agent without picking a side.

**Note text** (identical in both files, placed immediately after the closing ` ``` ` of the JSON block):
> **Note**: The field schema above follows the `AskUserQuestion` convention. Under `request_user_input`, each question additionally requires an `id` (snake_case) and accepts 2–3 options — follow the host tool's actual schema rather than copying this example verbatim.

**Covers**: supports NFR-003, CON-001

**Decision Level**: Plan-level technical decision; does not change confirmed product scope. (Adopts the OPEN-003 proposed default. Reversible — if the user vetoes, omit the note and the core rewrite still stands.)

### PLD-003: Verification = grep assertions + manual run under both agents (adopts OPEN-002 default)

**Context**: There is no unit-test coverage for template content (OPEN-002).

**Decision**: Verify via (a) grep/string assertions for SC-001..004 and (b) manual runs of `/codexspec:constitution` and `/codexspec:config` under Codex (Plan mode) and Claude Code.

**Rationale**: Grep covers the deterministic checks; manual runs cover the agent-behavior checks (NFR-001, NFR-003) that cannot be asserted by string matching.

**Covers**: NFR-001, NFR-003, SC-001, SC-002, SC-003, SC-004

**Decision Level**: Plan-level technical decision; does not change confirmed product scope.

## Risks / Trade-offs

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Assumption 1 fails: Codex GPT-5 does not invoke `request_user_input` from the soft-list wording | Medium | Medium (structured intent lost under Codex) | Manual verification under Codex in Phase 3; if it fails, escalate per RA-001 (reconsider DEC-002) — a user decision, not auto-fixed |
| `codexspec init --force` regenerates from a stale installed package instead of the local `templates/` edit | Low | Medium (derived copies don't reflect the fix) | Run via `uv run codexspec init --force --here` so the local source is used; confirm via SC-004 grep that derived copies match |
| PLD-002 schema note slightly expands the edit beyond the pure prose line | Low | Low | Marked as adopting OPEN-003 default; reversible; does not touch other templates |

## Implementation Phases

### Phase 1: Edit template sources (C1, C2)

- [ ] `templates/commands/constitution.md:56` → replace with REQ-004 exact text
- [ ] `templates/commands/config.md:70` → replace with REQ-005 exact text
- [ ] Add the PLD-002 schema note after the JSON block in `constitution.md`
- [ ] Add the PLD-002 schema note after the JSON block in `config.md`

### Phase 2: Regenerate derived copies (C3)

- [ ] Run `uv run codexspec init --force --here` to sync `.claude/commands/codexspec/{constitution,config}.md` and `.agents/skills/codexspec-{constitution,config}/SKILL.md`
- [ ] Confirm via grep that the 4 derived files now contain the new wording (SC-004)

### Phase 3: Verify

- [ ] Grep: `constitution.md:56` and `config.md:70` match REQ-004/REQ-005 exact text
- [ ] Grep: neither rewritten line contains `Claude Code` or `Codex` (SC-001)
- [ ] Grep: both rewritten lines contain both `AskUserQuestion` and `request_user_input` (SC-002)
- [ ] `git diff` scoped to only `templates/commands/constitution.md` and `templates/commands/config.md` (plus regenerated derived files) — no other template's prose changed (SC-003)
- [ ] Manual: under Codex (Plan mode), `/codexspec:constitution` and `/codexspec:config` present a structured prompt (NFR-001)
- [ ] Manual: under Claude Code, same commands invoke `AskUserQuestion` with no regression (NFR-001)
- [ ] (Optional) Manual: under Codex non-Plan mode, confirm graceful degradation to plain-text question (NFR-003)

## Verification Strategy

Two-tier:

1. **Deterministic (grep/string)** — covers SC-001..004, REQ-002, REQ-003, REQ-004, REQ-005, REQ-007. These can be checked by `grep`/`git diff` and are repeatable.
2. **Manual (agent behavior)** — covers NFR-001 (intent preserved under both agents) and NFR-003 (degradation under Codex non-Plan). These require running the two commands under each agent and observing the prompt.

## Requirements Coverage

| Spec Requirement | Plan Coverage | Reference |
|---|---|---|
| REQ-001 | Full | C1, C2 / Phase 1 |
| REQ-002 | Full | C1, C2 (prose names both tools) / Phase 3 grep |
| REQ-003 | Full | C1, C2 (no agent brands) / Phase 3 grep (SC-001) |
| REQ-004 | Full | C1 exact text / Phase 1, Phase 3 grep |
| REQ-005 | Full | C2 exact text / Phase 1, Phase 3 grep |
| REQ-006 | Full | C3 / PLD-001 / Phase 2 |
| REQ-007 | Full | Phase 1 scope (only 2 source files) / Phase 3 git diff (SC-003) |
| NFR-001 | Full | Phase 3 manual (both agents) |
| NFR-002 | Full | Phase 3 grep (SC-001, no agent brands) |
| NFR-003 | Full | PLD-002 schema note + Phase 3 manual (Codex non-Plan) |

## Unresolved Items

- **OPEN-001** — resolved by PLD-001 (regenerate within this change). Adopted default; reversible.
- **OPEN-002** — resolved by PLD-003 (grep + manual verification). Adopted default.
- **OPEN-003** — resolved by PLD-002 (add schema note). Adopted default; reversible — if the user vetoes, omit the note and the core rewrite (REQ-001..005) still stands.
- **Assumption 1** (Codex agent recognizes `request_user_input`) — not resolved by plan; validated by Phase 3 manual verification. If it fails, escalate as a user decision (RA-001).
