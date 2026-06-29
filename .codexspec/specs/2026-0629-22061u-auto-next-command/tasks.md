# Tasks: workflow.auto_next — Auto-Advance the SDD Command Chain

<!--
Language: Generate this document in the language specified in .codexspec/config.yml.
Document language is English.
-->

**Input**: `.codexspec/specs/2026-0629-22061u-auto-next-command/{requirements.md, spec.md, plan.md}`
**Prerequisites**: plan.md (required), spec.md (required)

**Tests**: This change is primarily markdown template edits (non-TDD per the project's task-type classification) plus Python contract/compatibility tests. Test-first ordering is not mandated for the template edits; each template task carries its own verification checkpoint, and the contract tests (T006) plus compat test (T007) are the persistent automated guards.

**Organization**: Grouped by the approved plan's phases/components (not user stories), per the plan-to-tasks rule to preserve the plan's organization.

## Format: `[ID] [P?] Description`

- **[P]**: Can run in parallel (different files, no dependencies).
- Each task ends with `Covers: REQ-xxx; Plan: <component/phase>` for traceability.
- Each task produces a single verifiable outcome.

### Shared "Auto-Next Chain Advance" contract (applies to T001–T004)

Every template section added by T001–T004 MUST follow the same contract (Plan Decision 4), mirroring the existing "Automatic Cross-Artifact Analysis" block in `plan-to-tasks.md`:

1. Read `workflow.auto_next` from `.codexspec/config.yml` (default `false`; **only literal `true` enables** — Assumption A1).
2. Check the stage-passed precondition (see each task).
3. Stop (return control to user, do not invoke) when: disabled, or the review stopped at `NEEDS_REVISION` / `BLOCKED`, or stopped early.
4. Emit exactly one notice line in the interaction language (`language.interaction`) before invoking.
5. Invoke the next slash command exactly once, passing the resolved feature directory.
6. Leave the template **frontmatter byte-identical** (Plan Decision 3) — body-only edit.

---

## Phase 1: Template Auto-Next Sections

**Purpose**: Add the conditional auto-advance section to the four distributed command templates (source of truth = `templates/commands/`).

- [x] T001 [P] Add an `## Auto-Next Chain Advance` section to `templates/commands/specify.md`, placed after the `## Completion` section.
  - Gate: `workflow.auto_next: true` AND `specify` has reached Completion — all discovery criteria met and the user confirmed the **final** stage summary (NOT each intermediate topic confirmation).
  - Action: notice (e.g. `auto_next: requirements confirmed → invoking /codexspec:generate-spec <feature-dir>`) then invoke `/codexspec:generate-spec <feature-dir>` once.
  - Verify: section present; references `workflow.auto_next`, `generate-spec`, Completion/final confirmation, the notice, and the stop conditions; frontmatter unchanged.
  - Covers: REQ-003, REQ-005, REQ-006, REQ-010; Plan: C1 / Phase 1

- [x] T002 [P] Add the `## Auto-Next Chain Advance` section to `templates/commands/generate-spec.md`, placed after the `## Automatic Review Loop` section.
  - Gate: `workflow.auto_next: true` AND the review loop Overall Status is `PASS` or `PASS_WITH_WARNINGS`.
  - Action: notice then invoke `/codexspec:spec-to-plan <feature-dir>` once.
  - Verify: section present with `workflow.auto_next`, `spec-to-plan`, the PASS/PASS_WITH_WARNINGS gate, notice, and stop conditions; frontmatter unchanged.
  - Covers: REQ-002, REQ-004, REQ-005, REQ-006, REQ-010; Plan: C2 / Phase 1

- [x] T003 [P] Add the `## Auto-Next Chain Advance` section to `templates/commands/spec-to-plan.md`, placed after the `## Automatic Review Loop` section.
  - Gate/stop: identical to T002. Action: notice then invoke `/codexspec:plan-to-tasks <feature-dir>` once.
  - Verify: section present with `workflow.auto_next`, `plan-to-tasks`, gate, notice, stop conditions; frontmatter unchanged.
  - Covers: REQ-002, REQ-004, REQ-005, REQ-006, REQ-010; Plan: C3 / Phase 1

- [x] T004 [P] Add the `## Auto-Next Chain Advance` section to `templates/commands/plan-to-tasks.md`, placed AFTER the existing `## Automatic Cross-Artifact Analysis` (analyze) section and BEFORE `## Output Summary`.
  - Gate: `workflow.auto_next: true` AND the review loop passed (analyze has already run). State that analyze's findings do NOT block this advance (CON-005).
  - Action: notice then invoke `/codexspec:implement-tasks <feature-dir>` once, with NO confirmation prompt (DEC-001).
  - Verify: section present with `workflow.auto_next`, `implement-tasks`, the non-blocking analyze note, the no-prompt behavior, notice, and stop conditions; frontmatter unchanged.
  - Covers: REQ-002, REQ-004, REQ-005, REQ-006, REQ-008, REQ-009, REQ-010; Plan: C4 / Phase 1

**Checkpoint**: All four templates carry the auto-next section. `implement-tasks.md` is intentionally unchanged (terminal — REQ-007).

---

## Phase 2: Sync Derived Self-Bootstrap Copies

**Purpose**: Make the change live in this repo without violating the "never hand-edit `.claude/`" rule.

- [x] T005 Re-sync the four edited templates from `templates/commands/` into the derived `.claude/commands/codexspec/` (`specify.md`, `generate-spec.md`, `spec-to-plan.md`, `plan-to-tasks.md`). Regenerate from templates — re-run `codexspec init` or copy the four files; do NOT hand-edit the derived copies.
  - Depends: T001, T002, T003, T004.
  - Verify: `diff` between each `.claude/commands/codexspec/<name>.md` and `templates/commands/<name>.md` is empty for the four files.
  - Covers: REQ-010; Plan: C5 / Phase 2

---

## Phase 3: Tests

- [x] T006 Extend `tests/test_sdd_workflow_templates.py` with auto-next contract assertions using the existing `read_command(name)` helper:
  - For each of `specify`, `generate-spec`, `spec-to-plan`, `plan-to-tasks`: assert the auto-next section references `workflow.auto_next`, the correct next command, the notice, and the stop conditions (`NEEDS_REVISION` / `BLOCKED`).
  - Assert `specify`'s section gates on Completion (not intermediate confirmation).
  - Assert `plan-to-tasks` invokes `implement-tasks` and that analyze is non-blocking.
  - Assert `implement-tasks.md` contains NO auto-next advance (terminal — REQ-007).
  - Add a self-bootstrap drift guard: the four `.claude/commands/codexspec/*.md` are identical to their `templates/commands/*.md` sources.
  - Depends: T005 (needs templates + sync).
  - Verify: `uv run pytest tests/test_sdd_workflow_templates.py -q` passes.
  - Covers: REQ-001..010, NFR-002, NFR-004; Plan: C6 / Phase 3

- [x] T007 [P] Add a compatibility test (in `tests/`, alongside existing i18n/config tests): build a `config.yml` containing `workflow: { auto_next: true }`, parse it with `yaml.safe_load`, and confirm language resolution (`codexspec.i18n`) still returns correct values — proving an unknown `workflow` key does not break parsing or existing behavior.
  - Verify: the new test passes; existing i18n/config tests remain green.
  - Covers: NFR-001; Plan: C7 / Phase 3

---

## Phase 4: Documentation (OPTIONAL — non-blocking)

- [x] T008 Document the `workflow.auto_next` option alongside `git.main_branches` in `CLAUDE.md` (Configuration section) and/or `docs/en/user-guide/` config docs.
  - Depends: T001–T004.
  - Optional / non-blocking. Covers no REQ (discoverability / implementation support); Plan: Phase 4.

---

## Phase 5: Verification

- [x] T009 Final verification gate:
  - `uv run pytest` is fully green (incl. T006, T007) and `uv run ruff check src/ tests/` is clean.
  - Confirm the four `.claude/` copies match `templates/` (from T005).
  - Manual spot-check of spec acceptance scenarios: with `workflow.auto_next: true` the chain advances with notices; absent/`false` → unchanged; a `NEEDS_REVISION`/`BLOCKED` verdict halts the chain.
  - Depends: T001–T008.
  - Covers: all REQ/NFR (verification); Plan: Phase 5

---

## Dependencies & Execution Order

```
T001 ─┐
T002 ─┤
T003 ─┼─► T005 ─► T006 ─┐
T004 ─┤                 ├─► T009
       └─► T008 ─────────┘
T007 ─────────────────────► T009
```

- **T001–T004**: independent (`[P]`); different files, no deps. Can run in any order.
- **T005**: depends on T001–T004 (sync after templates exist).
- **T006**: depends on T005 (asserts template content + `.claude/` sync).
- **T007**: independent (`[P]`); pure config-parsing test.
- **T008** (optional): depends on T001–T004.
- **T009**: depends on all prior tasks.

Acyclic; no circular dependencies. Suggested sequence: T001–T004 (parallel) → T005 → T006 ∥ T007 ∥ T008 → T009.

---

## Requirements / Plan Coverage

| Spec Requirement | Plan Component | Task(s) | Notes |
|---|---|---|---|
| REQ-001 | C1–C4 | T001–T004, T006 | Option text; only-`true` |
| REQ-002 | C2, C3, C4 | T002, T003, T004, T006 | review-gated advance |
| REQ-003 | C1 | T001, T006 | Completion gate |
| REQ-004 | C2–C4 | T002–T004, T006 | stop conditions |
| REQ-005 | C1–C4 | T001–T004, T006 | notice (interaction lang) |
| REQ-006 | C1–C4 | T001–T004, T006, T007 | default false |
| REQ-007 | (terminal) | T006 | negative guard; implement-tasks unchanged |
| REQ-008 | C4 | T004 | analyze non-blocking |
| REQ-009 | C4 | T004 | no confirmation prompt |
| REQ-010 | C1–C5 | T001–T005, T006 | conditional section; source-of-truth sync |
| NFR-001 | C7 | T007 | compat / opt-in |
| NFR-002 | C1–C4 | T001–T004, T006 | snake_case `workflow.auto_next` |
| NFR-003 | C1–C4 | T001–T004 | single global boolean |
| NFR-004 | C1–C4 | T001–T004, T006 | observability via notice |

**Unmapped tasks**: T009 (verification gate) and T008 (optional docs) map to no individual REQ — T009 is consolidated verification across all REQs/NFRs; T008 is implementation support (discoverability) explicitly marked optional/non-blocking per the approved plan (Phase 4).

## Notes

- `[P]` tasks (T001–T004, T007) touch different files with no dependencies.
- Commit after each task or logical group.
- Do not modify template frontmatter (Plan Decision 3) — body-only edits avoid the en.json/translation-catalog sync requirement.
- The behavioral (LLM-driven) aspects of auto-next are verified manually in T009; they cannot be asserted by a unit test because the behavior is enacted by the agent at runtime.

## Implementation Log

- **T005 scope expansion (verified repo fact)**: each command exists in **three** distribution forms — `templates/commands/<name>.md` (source, slash form), `.claude/commands/codexspec/<name>.md` (Claude, translated frontmatter, slash body), and `.agents/skills/codexspec-<name>/SKILL.md` (Codex, `$codexspec:` skill-mention form). Following the #17 precedent, all three were synced. Derived forms were regenerated via the real installer functions (`install_commands_to_subdir` + `CodexIntegration.install_skills`, `language="zh-CN"`), which preserved the translated frontmatter exactly and changed only the 4 affected commands (the other 14 commands / 14 skills were byte-identical). `implement-tasks` was correctly left unchanged (terminal).
- **T006/T007**: 11 new tests added; full suite 859 passed / 37 skipped; `ruff check src/ tests/` clean.
- **Code review (step 7)**: the only analyzable code changed by this feature is the two test files (the feature itself is markdown templates). Self-review against `/codexspec:review-code` criteria found no CRITICAL/HIGH/MEDIUM defects; no auto-fix required.
