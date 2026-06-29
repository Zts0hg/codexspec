# Tasks: plan-to-tasks-auto-analyze

<!--
Language: Generate this document in the language specified in .codexspec/config.yml
If not configured, use English.
-->

**Input**: `.codexspec/specs/2026-0629-1337a7-plan-to-tasks-auto-analyze/` (`requirements.md`, `spec.md`, `plan.md`)
**Prerequisites**: `plan.md` (approved, review-plan PASS)

**Organization**: Grouped by the three phases in `plan.md` (Edit source → Regenerate artifacts → Verify). The feature is a single cohesive change, so each phase is one task with a single verifiable outcome; no further splitting.

## Format: `[ID] Description — Covers: REQ-xxx; Plan: <component/phase>`

- Exact file paths are used; no paths are invented.
- `Covers:` lists the spec requirements the task implements, propagates, or verifies, plus the `plan.md` component/phase.
- Tasks 2.1 and 3.1 are necessary implementation support (propagation and verification of task 1.1), not new product behavior.

---

## 1. Edit the source template

**Purpose**: Author the new behavior once, in the source-of-truth template.

- [x] 1.1 Insert a new `## Automatic Cross-Artifact Analysis` section into `templates/commands/plan-to-tasks.md`, placed between the existing `## Automatic Review Loop` section (immediately after its last bullet, "Stop if defects repeat, remain unresolved, or require a user or architecture decision.") and the `## Output Summary` section. Use the exact section text quoted in `plan.md` → *Technical Approach* verbatim. Do not alter any other section (Task Rules, Stop Conditions, Pre-Save Validation, Output Summary, frontmatter).
  - **Verify**: the heading `## Automatic Cross-Artifact Analysis` and the `/codexspec:analyze <feature-dir>` invocation each appear exactly once in `templates/commands/plan-to-tasks.md`; the new section sits between `## Automatic Review Loop` and `## Output Summary`; the existing markers `Covers:`, `maximum of two`, and `Stop if defects repeat` are still present and unchanged.
  - **Covers**: REQ-001, REQ-002, REQ-003, REQ-004, REQ-005, NFR-001, NFR-002, NFR-003, NFR-004; Plan: C1 / Phase 1

---

## 2. Regenerate derived artifacts

**Purpose**: Propagate the source change into both git-tracked install artifacts.

- [x] 2.1 Run `codexspec init --here --force --ai both` from the repository root to resync both derived artifacts from the updated template. (Plain `codexspec init` defaults to `ai=claude` and syncs only `.claude/commands/`; `--ai both` is required to also resync `.agents/skills/`; `--force` overwrites the existing tracked files.)
  - **Depends on**: 1.1
  - **Verify**: `.claude/commands/codexspec/plan-to-tasks.md` contains the new section with `/codexspec:analyze` (slash form); `.agents/skills/codexspec-plan-to-tasks/SKILL.md` contains it with `$codexspec:analyze` (skill form, produced by the automatic `/codexspec:` → `$codexspec:` transform).
  - **Covers**: REQ-001, REQ-002, REQ-003, REQ-004, REQ-005, NFR-001, NFR-002, NFR-003, NFR-004 (propagation of 1.1); Plan: C2 / Phase 2

---

## 3. Verify

**Purpose**: Confirm no regression and cross-copy consistency.

- [x] 3.1 Run the regression suite and the cross-copy consistency check:
  1. `uv run pytest tests/test_sdd_workflow_templates.py tests/test_codex_integration.py tests/commands/test_installer.py -v` — expect all green; in particular `test_generation_commands_enforce_upstream_traceability[plan-to-tasks]` and the Codex render-transform tests pass.
  2. Static check: the new section is present and consistent across all three files — `templates/commands/plan-to-tasks.md` (slash form), `.claude/commands/codexspec/plan-to-tasks.md` (slash form), `.agents/skills/codexspec-plan-to-tasks/SKILL.md` (`$` form) — and none of the required existing markers (`Covers:`, `maximum of two`, `Stop if defects repeat`) were removed.
  - **Depends on**: 2.1
  - **Optional manual spot check** (not blocking): run `/codexspec:plan-to-tasks` on a throwaway feature whose review loop ends `PASS` → observe `/codexspec:analyze` auto-invoked once; and on one ending `NEEDS_REVISION`/`BLOCKED` → observe it not invoked.
  - **Covers**: REQ-001, REQ-002, REQ-003, REQ-004, REQ-005, NFR-001, NFR-002, NFR-003, NFR-004 (verification of 1.1/2.1); Plan: Phase 3

---

## Dependencies

```
1.1 -> 2.1 -> 3.1
```

Linear and acyclic: edit the source, then propagate, then verify.

## Coverage

| Plan Component / Requirement | Task | Notes |
|------------------------------|------|-------|
| C1 / Phase 1 | 1.1 | Authors the new section (source of truth) |
| C2 / Phase 2 | 2.1 | Regenerates both tracked artifacts |
| Phase 3 | 3.1 | Regression tests + cross-copy consistency |
| REQ-001 | 1.1 (authored), 2.1 (propagated), 3.1 (verified) | Auto-invoke analyze once |
| REQ-002 | 1.1, 2.1, 3.1 | Gate on PASS / PASS_WITH_WARNINGS |
| REQ-003 | 1.1, 2.1, 3.1 | Non-invocation on NEEDS_REVISION / BLOCKED / early stop |
| REQ-004 | 1.1, 2.1, 3.1 | Single read-only pass, no fix loop |
| REQ-005 | 1.1, 2.1, 3.1 | Legacy mode runs analyze (disclosure delegated to analyze) |
| NFR-001 | 1.1, 2.1, 3.1 | Always-on (no flag) |
| NFR-002 | 1.1, 2.1, 3.1 | Output Summary unchanged |
| NFR-003 | 1.1, 2.1, 3.1 | No report file |
| NFR-004 | 1.1, 2.1, 3.1 | Informational, no implement gate |

**Unmapped tasks**: None.

## Notes

- This is a documentation/template change (Markdown prose), not code; no unit tests are authored for the template content itself — verification relies on the existing template/transform test suite plus static cross-copy checks (task 3.1).
- Commit after task 2.1 (source + regenerated artifacts together) so the three copies never drift in history.
- No polish, monitoring, abstraction, or hardening tasks are included — none are required by the plan, constitution, or a verified implementation need.
