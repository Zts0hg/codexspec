# Tasks: ask-user-question-codex-compat

<!--
Language: Generate this document in the language specified in .codexspec/config.yml
If not configured, use English.
-->

**Input**: `.codexspec/specs/2026-0711-1531r9-ask-user-question-codex-compat/` (requirements.md, spec.md, plan.md)
**Prerequisites**: plan.md (required), spec.md (required for user stories)
**Tests**: No code changes; verification is grep/string assertions + manual agent runs (per plan PLD-003). No TDD ordering applies.

**Organization**: Grouped by the plan's 3 phases (Edit sources → Regenerate → Verify), not by the template's user-story phases. User stories (US1 = Codex structured prompt works; US2 = no Claude Code regression) are both validated by the manual verification task (T005).

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel with siblings after its declared dependencies.
- Each task includes `Covers: REQ-xxx; Plan: <component/phase>`.
- Exact replacement text is embedded verbatim so the implementer need not re-derive it.

---

## Phase 1: Edit template sources (C1, C2)

**Purpose**: Rewrite the 2 hardcoded `AskUserQuestion` references and add the PLD-002 schema note.

### ✅ T001 [P] [US1] Edit `templates/commands/constitution.md`

- **Outcome**: Line 56 reads the REQ-004 text; the PLD-002 schema note is added immediately after the closing ` ``` ` of the `json` code block that follows line 56.
- **Path**: `templates/commands/constitution.md`
- **Replace** (line 56):
  - from: `**IMPORTANT**: Use the \`AskUserQuestion\` tool to present structured choices.`
  - to:   `**IMPORTANT**: Use the host agent's structured-question tool (e.g., \`AskUserQuestion\` or \`request_user_input\`) to present structured choices.`
- **Add** (after the JSON block's closing ` ``` `):
  > **Note**: The field schema above follows the `AskUserQuestion` convention. Under `request_user_input`, each question additionally requires an `id` (snake_case) and accepts 2–3 options — follow the host tool's actual schema rather than copying this example verbatim.
- **Verify**: grep line 56 matches the new text; note present; line contains no `Claude Code`/`Codex`; line contains both `AskUserQuestion` and `request_user_input`.
- **Covers**: REQ-001, REQ-002, REQ-003, REQ-004, NFR-001, NFR-002; Plan: C1 / Phase 1

### ✅ T002 [P] [US1] Edit `templates/commands/config.md`

- **Outcome**: Line 70 reads the REQ-005 text; the PLD-002 schema note is added immediately after the closing ` ``` ` of the `json` code block that follows line 70.
- **Path**: `templates/commands/config.md`
- **Replace** (line 70):
  - from: `If configuration exists and no \`--view\` flag, present the management menu using \`AskUserQuestion\`:`
  - to:   `If configuration exists and no \`--view\` flag, present the management menu using the host agent's structured-question tool (e.g., \`AskUserQuestion\` or \`request_user_input\`):`
- **Add** (after the JSON block's closing ` ``` `): the same Note text as T001.
- **Verify**: grep line 70 matches the new text; note present; line contains no `Claude Code`/`Codex`; line contains both `AskUserQuestion` and `request_user_input`.
- **Covers**: REQ-001, REQ-002, REQ-003, REQ-005, NFR-001, NFR-002; Plan: C2 / Phase 1

**Checkpoint**: Both source templates carry the agent-brand-agnostic wording and schema note.

---

## Phase 2: Regenerate derived copies (C3)

**Purpose**: Sync the 4 derived copies from the edited templates (PLD-001). Derived copies must not be hand-edited (CON-002).

### ✅ T003 [US1] Regenerate derived copies and confirm sync

- **Outcome**: `.claude/commands/codexspec/constitution.md`, `.claude/commands/codexspec/config.md`, `.agents/skills/codexspec-constitution/SKILL.md`, `.agents/skills/codexspec-config/SKILL.md` all reflect the new wording.
- **Command**: `uv run codexspec init --force --here`
  - `uv run` ensures the local `templates/` source is used (`get_templates_dir()` resolves to repo-root `templates/` in the dev tree).
  - `--force` overwrites regenerable command/skill files while preserving user-authored content (`src/codexspec/__init__.py:510-521`).
  - Optional: append `--no-git` to skip the redundant `git init` (advisory DO-001; not required for correctness).
- **Depends on**: T001, T002
- **Verify (SC-004)**: grep each of the 4 derived files for the new prose line (`Use the host agent's structured-question tool (e.g., \`AskUserQuestion\` or \`request_user_input\`)`); confirm present and matches the source.
- **Covers**: REQ-006, CON-002, SC-004; Plan: C3 / Phase 2 / PLD-001

**Checkpoint**: Derived copies match the template source at the rewritten lines.

---

## Phase 3: Verify (Phase 3 / PLD-003)

**Purpose**: Deterministic checks (T004) and manual agent-behavior checks (T005).

### ✅ T004 [P] [US1] Deterministic verification (grep + git diff)

- **Outcome**: All string assertions pass; diff is scoped to the expected files.
- **Depends on**: T001, T002 (source checks; independent of T003)
- **Verify**:
  - SC-001: neither rewritten line (in `templates/commands/constitution.md:56` nor `config.md:70`) contains `Claude Code` or `Codex`.
  - SC-002: both rewritten lines contain both `AskUserQuestion` and `request_user_input`.
  - REQ-004/005: the two lines match the exact target text.
  - SC-003 / REQ-007: `git diff` confirms no OTHER template's prose `ask the user` changed — among `templates/commands/*.md`, only `constitution.md` and `config.md` are modified. Expected non-template changes: the 4 regenerated derived files, and possibly `.codexspec/scripts/` (T003's `codexspec init --force` regenerates commands AND scripts per `src/codexspec/__init__.py:510-521`; script changes are expected regeneration output, not a feature defect — if scripts were already in sync, none appear).
- **Covers**: REQ-002, REQ-003, REQ-004, REQ-005, REQ-007, NFR-002, SC-001, SC-002, SC-003; Plan: Phase 3

### ⏳ T005 [US1, US2] Manual verification under Codex + Claude Code

- **Outcome**: Both commands present a structured-choice prompt under each agent; no regression under Claude Code.
- **Depends on**: T003 (the running commands use the regenerated derived copies in `.claude/commands/codexspec/`)
- **Verify**:
  - Under **Codex (Plan mode)**: run `/codexspec:constitution` (no args) and `/codexspec:config` (interactive); confirm a structured prompt with selectable options appears (the agent calls `request_user_input`). Validates NFR-001 and Assumption 1.
  - Under **Claude Code**: run the same two commands; confirm `AskUserQuestion` is still invoked with the same choices (no regression). Validates US2 / NFR-001.
  - Optional: under Codex non-Plan mode, confirm graceful degradation to a plain-text question (NFR-003).
- **Covers**: NFR-001, NFR-003; Plan: Phase 3 / PLD-003
- **Note**: This is the task that validates Assumption 1. If the Codex agent does not invoke `request_user_input`, stop and escalate per RA-001 (reconsider DEC-002) — a user decision, not an auto-fix.

**Checkpoint**: Change verified under both agents; Assumption 1 validated.

---

## Dependencies & Execution Order

```
T001 [P] ─┐
          ├──► T003 ──► T005
T002 [P] ─┤
          └──► T004 [P]   (parallel with T003)
```

- T001, T002: no dependencies; run in parallel ([P]).
- T003: depends on T001 + T002 (templates must be edited before regeneration).
- T004: depends on T001 + T002 (checks source files); runs in parallel with T003 ([P]).
- T005: depends on T003 (manual runs use the regenerated derived copies).
- Acyclic: T001/T002 → {T003, T004} → T005.

---

## Coverage Table

| Plan Component / Requirement | Task(s) | Notes |
|---|---|---|
| C1 — `constitution.md` source edit | T001 | REQ-001/002/003/004 |
| C2 — `config.md` source edit | T002 | REQ-001/002/003/005 |
| C3 — derived copy regeneration | T003 | REQ-006, CON-002, SC-004 |
| Phase 3 — deterministic verify | T004 | REQ-002/003/004/005/007, NFR-002, SC-001/002/003 |
| Phase 3 — manual verify | T005 | NFR-001, NFR-003, Assumption 1, US1 + US2 |
| REQ-006 | T003 | |
| REQ-007 | T004 | git diff scope check |
| NFR-001 | T001, T002, T005 | intent preserved; verified manually |
| NFR-002 | T001, T002, T004 | no agent-brand hardcoding |
| NFR-003 | T003 (note), T005 | degradation note + manual non-Plan check |

## Unmapped Tasks

None. No polish, documentation, monitoring, or hardening tasks — none are required by the approved plan or repository policy for a template-text change.

## Unresolved Items

- **OPEN-001** → resolved by T003 (regenerate within this change, PLD-001).
- **OPEN-002** → resolved by T004 + T005 (PLD-003).
- **OPEN-003** → resolved by the schema note in T001/T002 (PLD-002, post-fix wording).
- **Assumption 1** → validated by T005; if it fails, escalate as a user decision (RA-001).
