# Implementation Plan: plan-to-tasks-auto-analyze

<!--
Language: Generate this document in the language specified in .codexspec/config.yml
If not configured, use English.
-->

**Related Spec**: `.codexspec/specs/2026-0629-1337a7-plan-to-tasks-auto-analyze/spec.md`
**Confirmed Requirements**: `.codexspec/specs/2026-0629-1337a7-plan-to-tasks-auto-analyze/requirements.md`
**Created**: 2026-06-29
**Status**: Draft

## Context

`plan-to-tasks` already ends with an **Automatic Review Loop** that invokes `/codexspec:review-tasks`, auto-fixes deterministic defects (max two rounds), and stops early when defects repeat, remain unresolved, or require a user/architecture decision. `review-tasks` reports an Overall Status of `PASS` / `PASS_WITH_WARNINGS` / `NEEDS_REVISION` / `BLOCKED`.

This feature adds one step after that loop: when it concludes in a passing state, `plan-to-tasks` automatically invokes `/codexspec:analyze` once for the end-to-end cross-artifact check. The change is a small, additive prose edit to a single command template — no code, API, schema, or infrastructure change.

## Goals / Non-Goals

**Goals** (inherited from `spec.md`):

- Remove the manual `/codexspec:analyze` step after successful task generation.
- Surface cross-artifact consistency issues at the moment tasks are produced.
- Keep analyze's role purely informational — no new gate before implementation.

**Non-Goals** (inherited — see `spec.md` Out of Scope):

- No changes to `review-tasks` or its auto-fix loop.
- No fix-and-reanalyze loop for analyze; analyze is not chained into any other command.
- No new "next step: implement-tasks" recommendation; no persisting analyze output to disk.

## Existing Repository Constraints (verified)

- **Source of truth**: `templates/commands/plan-to-tasks.md` is the authoritative template for the distributed `plan-to-tasks` command. The current insertion point is between the `## Automatic Review Loop` section (ends with the "Stop if defects repeat..." bullet, line 93) and `## Output Summary` (line 95).
- **Derived artifacts are generated, not hand-edited**: `codexspec init` (via `CodexIntegration().install_skills(...)` in `src/codexspec/__init__.py`) renders `templates/commands/*.md` into two install locations:
  - `.claude/commands/codexspec/plan-to-tasks.md` (Claude command form, `/codexspec:` prefix).
  - `.agents/skills/codexspec-plan-to-tasks/SKILL.md` (Codex skill form; the render transforms `/codexspec:` → `$codexspec:`).
  - Confirmed by `tests/test_codex_integration.py:13` ("Codex templates should render as SKILL.md files with $ invocations") and the `install_skills(target, templates_dir)` call.
- **Consequence**: editing the template is sufficient; both artifacts regenerate on the next `codexspec init --here --force --ai both`. Note `codexspec init` defaults to `ai=claude` (`src/codexspec/__init__.py:517`), which syncs only `.claude/commands/codexspec/`; `--ai both` is required to also resync the tracked `.agents/skills/` copy. This matches the project's Self-bootstrap rule (constitution) and DEC-001.
- **Test landscape (no regression expected)**:
  - `tests/test_sdd_workflow_templates.py::test_generation_commands_enforce_upstream_traceability` asserts `plan-to-tasks` contains `Covers:`, `confirmed`, `stop`, and `maximum of two` — all located in sections this change does **not** touch (Task Rules, Stop Conditions, the existing review-loop bullets). The new section is purely additive.
  - `tests/test_codex_integration.py` asserts the `/codexspec:` → `$codexspec:` render transform; the new `/codexspec:analyze` invocation is transformed automatically.

## Technical Approach

A single additive section is inserted into `templates/commands/plan-to-tasks.md`. The exact text to insert (between `## Automatic Review Loop` and `## Output Summary`):

```markdown
## Automatic Cross-Artifact Analysis

When the review loop above concludes in a passing state — the final `/codexspec:review-tasks` Overall Status is `PASS` or `PASS_WITH_WARNINGS` — invoke `/codexspec:analyze <feature-dir>` exactly once.

- Do not invoke analyze when the review loop stopped at `NEEDS_REVISION` or `BLOCKED`, or stopped early per the conditions above; in those cases end here, handing control back to the user as the review loop already does.
- analyze runs once and is read-only. Present its output as-is; do not auto-fix its findings and do not run a fix-and-reanalyze loop.
- If `requirements.md` is absent, analyze still runs and discloses its legacy limitation (it starts at `spec.md` and cannot verify fidelity to the original discussion) per its own behavior.
- analyze's results are informational only. They do not change whether tasks are ready for implementation and do not add a gate before `/codexspec:implement-tasks`.
- Do not modify the Output Summary for analyze, and do not save an additional analyze report file; analyze's own output is the report.
```

No frontmatter change is needed: the existing `handoffs` entry already targets the `claude` agent for task generation, and the new step runs within that same agent turn.

## Components

- **C1 — "Automatic Cross-Artifact Analysis" section in `templates/commands/plan-to-tasks.md`** (new, additive). The single source change that defines the gated auto-invocation, the read-only single-pass behavior, the informational role, the legacy handling, and the no-output-change / no-file constraints.
  - **Covers**: REQ-001, REQ-002, REQ-003, REQ-004, REQ-005, NFR-001, NFR-002, NFR-003, NFR-004
- **C2 — Regenerate derived install artifacts**. Run `codexspec init --here --force --ai both` (see Phase 2) so `.claude/commands/codexspec/plan-to-tasks.md` and `.agents/skills/codexspec-plan-to-tasks/SKILL.md` pick up C1 (the latter via the automatic `/codexspec:` → `$codexspec:` transform). This is propagation of C1, not a separate content authoring step.

## Plan-Level Decisions

### PLD-1: New `## Automatic Cross-Artifact Analysis` section (not appended bullets, not a new command)

**Context**: The behavior must live somewhere in the `plan-to-tasks` template.

**Options Considered**:

1. Append bullets to the existing `## Automatic Review Loop` section.
2. A new dedicated `## Automatic Cross-Artifact Analysis` section.
3. A new standalone command that `plan-to-tasks` calls.

**Decision**: Option 2.

**Rationale**: `analyze` is a distinct command from `review-tasks`; a dedicated section mirrors the existing `## Automatic Review Loop` pattern and keeps the gate logic visible at a glance. Option 1 would conflate two commands; Option 3 is out of scope (OUT-003) and contradicts the confirmed intent that `plan-to-tasks` itself chain the step.

**Covers**: REQ-001

**Decision Level**: Plan-level technical decision; does not change confirmed product scope.

### PLD-2: Gate on the review loop's terminal Overall Status (no fresh re-invocation of review-tasks)

**Context**: The step needs a deterministic "passing?" signal.

**Options Considered**:

1. Reuse the review loop's final `review-tasks` Overall Status.
2. Re-invoke `review-tasks` to obtain a fresh verdict before deciding.

**Decision**: Option 1.

**Rationale**: The loop already produces a terminal status; re-running `review-tasks` is redundant work and could yield a divergent result. The passing set is explicitly `PASS` / `PASS_WITH_WARNINGS` (no Critical/Warning); the non-passing set is `NEEDS_REVISION` / `BLOCKED` or an early stop.

**Covers**: REQ-002, REQ-003

### PLD-3: Delegate legacy-mode disclosure to analyze's own behavior

**Context**: `analyze` already discloses its legacy limitation when `requirements.md` is absent.

**Options Considered**:

1. Invoke analyze and rely on its existing disclosure.
2. Restate the disclosure prose inside `plan-to-tasks`.

**Decision**: Option 1.

**Rationale**: Duplicating the disclosure would violate DRY and risk drift between the two templates. REQ-005 is satisfied transitively by invoking analyze, whose template already states "if `requirements.md` is missing, state that the analysis starts at `spec.md` and cannot validate fidelity to the original discussion." The new section notes this delegation explicitly so the dependency is visible.

**Covers**: REQ-005

### PLD-4: Always-on, no configuration key or flag

**Context**: Whether the auto-analyze step should be opt-out.

**Options Considered**:

1. Always enabled, matching the existing review loop.
2. Add a config key / flag to disable.

**Decision**: Option 1.

**Rationale**: The existing Automatic Review Loop is unconditional; introducing an opt-out would add config-schema and documentation scope the user did not request (CON-004).

**Covers**: NFR-001

### PLD-5: No Output Summary change and no report file

**Context**: How analyze's result is surfaced.

**Decision**: Leave `plan-to-tasks`'s Output Summary unchanged (it still reports tasks path, coverage, dependency summary, unresolved items, and auto-review status). Do not save an analyze report file. analyze's own inline output is the report.

**Rationale**: Avoids duplicating analyze's output and preserves analyze's current no-file behavior (DEC-002, DEC-003, OUT-005).

**Covers**: NFR-002, NFR-003

## Implementation Phases

The design calls for a three-step sequence, not a standard multi-phase build.

### Phase 1: Edit the source template

- [ ] Insert the `## Automatic Cross-Artifact Analysis` section (text quoted in *Technical Approach*) into `templates/commands/plan-to-tasks.md`, between `## Automatic Review Loop` and `## Output Summary`.

### Phase 2: Regenerate derived artifacts

- [ ] Re-run init in place with both AI targets so the two tracked artifacts resync from the updated template: `codexspec init --here --force --ai both`. The default `codexspec init` resolves to `ai=claude` (`src/codexspec/__init__.py:517`) and would only update `.claude/commands/codexspec/plan-to-tasks.md`, leaving the tracked `.agents/skills/codexspec-plan-to-tasks/SKILL.md` stale; `--ai both` installs both, and `--force` overwrites the existing tracked files.

### Phase 3: Verify

- [ ] Static checks and tests (see *Verification Strategy*).
- [ ] Optional manual end-to-end spot check.

## Verification Strategy

- **Template content**: confirm the new heading `## Automatic Cross-Artifact Analysis` and the `/codexspec:analyze` invocation are present in `templates/commands/plan-to-tasks.md`.
- **Derived-artifact sync**: confirm `.claude/commands/codexspec/plan-to-tasks.md` contains `/codexspec:analyze` (slash form) and `.agents/skills/codexspec-plan-to-tasks/SKILL.md` contains `$codexspec:analyze` (skill form).
- **Existing tests**: `uv run pytest tests/test_sdd_workflow_templates.py tests/test_codex_integration.py tests/commands/test_installer.py -v` — expect green; these guard the upstream-traceability markers and the render transform, none of which this change removes.
- **Manual spot check (optional)**: run `/codexspec:plan-to-tasks` on a throwaway feature whose review loop ends `PASS` → observe analyze auto-invoked once; and on one that ends `NEEDS_REVISION`/`BLOCKED` → observe analyze not invoked.

## Risks / Trade-offs

| Risk / Trade-off | Likelihood | Impact | Mitigation |
|------------------|------------|--------|------------|
| Executing agent misjudges "passing terminal status" | Low | Medium | The new section explicitly enumerates the passing set (`PASS`/`PASS_WITH_WARNINGS`) and the non-passing set (`NEEDS_REVISION`/`BLOCKED`/early stop), aligned with the review loop's existing stop bullets. |
| Always-on analyze adds latency to every successful `plan-to-tasks` | Medium | Low | Accepted per CON-004/NFR-001; analyze is read-only and runs exactly once. |
| Cross-copy drift if someone edits a derived artifact directly | Low | Medium | Constitution already forbids editing `.claude/commands/codexspec/`; regeneration via `codexspec init` keeps all three copies in sync. |
| A real cross-artifact break will not block implementation (informational only) | — | — | Accepted trade-off per CON-003/NFR-004; the user explicitly chose a non-gating role for analyze. |

## Requirements Coverage

| Spec Requirement | Plan Coverage | Reference |
|------------------|---------------|-----------|
| REQ-001 | Full | C1 / PLD-1 / Phase 1 |
| REQ-002 | Full | C1 / PLD-2 |
| REQ-003 | Full | C1 / PLD-2 |
| REQ-004 | Full | C1 |
| REQ-005 | Full | C1 / PLD-3 |
| NFR-001 | Full | C1 / PLD-4 |
| NFR-002 | Full | C1 / PLD-5 |
| NFR-003 | Full | C1 / PLD-5 |
| NFR-004 | Full | C1 |

All 9 binding spec requirements (REQ-001..005, NFR-001..004) have plan coverage. No plan-level decision redefines confirmed product intent. File paths and the template→artifact generation path are verified against `src/codexspec/__init__.py` and the test suite.
