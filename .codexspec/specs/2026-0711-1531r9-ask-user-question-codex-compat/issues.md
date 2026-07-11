# Implementation Issues: ask-user-question-codex-compat

## Issue: T005 manual verification cannot be autonomously executed

- **Task**: T005 (Manual verification under Codex + Claude Code)
- **Error**: T005 requires running `/codexspec:constitution` and `/codexspec:config` under both Codex CLI (Plan mode) and Claude Code, and observing that a structured-choice prompt appears. This cannot be executed autonomously from the current implementation session:
  - Codex CLI is not invocable from this Claude Code session.
  - Re-invoking the skills within this session would load their instructions, not render a clean structured prompt for observation.
- **Attempted**: All deterministic checks (T004) pass — the template wording is exact (REQ-004/005), contains no agent brands (SC-001), includes both tool names (SC-002), no other templates changed (SC-003), and the 4 derived copies are synced (SC-004). The remaining validation is inherently manual agent-behavior observation (NFR-001, NFR-003, Assumption 1).
- **Status**: Needs Discussion (user action required)

### User action to close T005

1. Under **Codex CLI (Plan mode)**: run `/codexspec:constitution` (no args) and `/codexspec:config` (interactive mode); confirm a structured prompt with selectable options appears (the agent calls `request_user_input`).
2. Under **Claude Code**: run the same two commands; confirm `AskUserQuestion` is still invoked with the same choices (no regression).
3. (Optional) Under Codex non-Plan mode: confirm graceful degradation to a plain-text question (NFR-003).

This also validates **Assumption 1** (the Codex GPT-5 agent invokes `request_user_input` from the soft-list wording). If it fails — i.e., the Codex agent treats the instruction as prose and does not present a structured prompt — stop and escalate per spec RA-001 / plan RA-001: reconsider DEC-002 (e.g., escalate to a more directive instruction). That is a user decision, not an auto-fix.

## Issue: T003 `codexspec init --force` could have reset project.ai

- **Task**: T003 (Regenerate derived copies)
- **Error**: `codexspec init` calls `_update_project_ai(config_file, ai)` unconditionally when `config.yml` exists (`src/codexspec/__init__.py:825-826`), which rewrites `project.ai` to the `--ai` value. The `--ai` default is `claude`, which would have changed `project.ai: "both"` → `"claude"` and broken the Codex config.
- **Attempted**: Mitigated by running `uv run codexspec init --force --here --ai both --no-git` (passing `--ai both` to preserve the setting; `--no-git` to skip redundant git init). Verified `project.ai` is `"both"` before and after, and `git diff .codexspec/config.yml` is empty.
- **Status**: Workaround Found — resolved by passing `--ai both`. (Surfaced as a plan/tasks note: future `codexspec init` re-runs on this repo must pass `--ai both`, or `project.ai` will be silently reset to `claude`.)
