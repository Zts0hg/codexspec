# Tasks: implement-tasks-code-review

<!--
Language: Generate this document in the language specified in .codexspec/config.yml
If not configured, use English.
-->

**Related Plan**: `.codexspec/specs/2026-0623-1658cw-implement-tasks-code-review/plan.md`
**Related Spec**: `.codexspec/specs/2026-0623-1658cw-implement-tasks-code-review/spec.md`
**Created**: 2026-06-23
**Status**: Implemented (T1–T3 complete; 841 tests pass, ruff clean) — see `issues.md` for the T3 sync deviation

> Each task carries `Covers: REQ/NFR; Plan: <Decision/Phase>`. Per the project's "conditional TDD", template/config changes are direct implementation plus a guard test (no forced test-first); the guard test is written after the template change, matching the plan's Phase 1 → 2 → 3 order. `[P]` marks tasks that can run in parallel once their dependencies are met — none apply here (strictly sequential).

---

## Phase 1 — Template edit

### T1 — Add Final Code Review Loop + restructure Completion in `implement-tasks.md` ✅

- **Outcome**: `templates/commands/implement-tasks.md` gains a **Final Code Review Loop** that runs once at end of run, after all tasks are implemented and the full test suite is green. The section must specify:
  1. **Review target (Decision 3)**: analyzable code files changed by this implementation — `git diff --name-only $(git merge-base HEAD <main>)..HEAD` ∪ uncommitted (`git diff --name-only` ∪ `git ls-files --others --exclude-standard`), filtered to `review-code`'s analyzable extensions (`.py .ts .tsx .js .jsx .go .rs .java .kt .kts .rb .sh .bash .zsh .c .h .cpp .hpp .cc .cxx .cs .swift .php`), excluding `.codexspec/specs/` and generated/vendored paths. `<main>` from config `git.main_branches` (default `main`/`master`/`develop`). If the filtered set is empty → report "no code to review", skip the loop, complete normally. Fallback (no git / not a feature branch): review the primary source directory and note the degraded fidelity.
  2. **Invocation**: invoke `/codexspec:review-code <paths>`.
  3. **Auto-fix scope (Decision 4)**: CRITICAL + HIGH + MEDIUM only; MEDIUM only when grounded in `.codexspec/memory/constitution.md` + the confirmed requirements/spec and focused on maintainability / readability / testability; LOW is report-only.
  4. **Test-safety (Decision 4)**: functional defects via TDD (red reproducer → green fix → green refactor); non-functional refactors run the suite before and after — if a change turns it red, revert, confirm green restored, re-attempt; never ship red, never silently skip; a fix that cannot be made green is unresolved. Fixes are applied by `implement-tasks` itself (full tool scope); `review-code` is read-only analysis.
  5. **Bounds / stop / status (Decision 5)**: max two fix-and-review rounds; stop on repeat / unresolved / user-or-architecture decision; never auto-fix advisories or design opportunities; never introduce a new product decision; commit fixes before reporting; residual CRITICAL/HIGH → "needs work", no false success; otherwise report scores + fixed/deferred + final test status.
  The current "### 6. Completion" is restructured into: confirm all tasks done + run full suite (green baseline) → Final Code Review Loop → commit any review changes + report. "### 3. TDD Workflow → Review & Refactor" (step 4) is left **unchanged** (additive, REQ-010).
- **Covers**: REQ-001; REQ-002; REQ-003; REQ-004; REQ-005; REQ-006; REQ-007; REQ-008; REQ-009; REQ-010; NFR-001; NFR-002; NFR-003 — Plan: Decisions 1–5 / Phase 1
- **Files**: `templates/commands/implement-tasks.md`
- **Deps**: —
- **Verification**: Read the edited file and confirm all five sub-behaviors and the restructured Completion are present, and that section 3.4 "Review & Refactor" is intact; the Feature-Resolution phrases required by `test_adjacent_commands_preserve_requirements_authority` (`requirements.md`, `explicit path`, `current branch`, `legacy spec-only`) remain. Structural assertions are pinned in T2.

---

## Phase 2 — Guard tests

### T2 — Add structural + preservation assertions for the new loop ✅

- **Outcome**: `tests/test_sdd_workflow_templates.py` gains assertions that `read_command("implement-tasks")` contains the new loop's key markers: invokes `/codexspec:review-code`; the CRITICAL+HIGH+MEDIUM severity gate (LOW report-only); MEDIUM grounding in constitution + requirements focused on maintainability/readability/testability; test-safe revert-and-retry on a broken refactor (no shipping of red tests); the two-round bound; the "needs work" outcome on residual high-severity defects; and commit-before-reporting. Also add a REQ-010 preservation assertion that "Review & Refactor" is still present. The existing `test_adjacent_commands_preserve_requirements_authority` must still pass.
- **Covers**: REQ-001; REQ-003; REQ-004; REQ-006; REQ-007; REQ-009; REQ-010; NFR-001; NFR-003 — Plan: Phase 2 (verification of Phase 1 behavior)
- **Files**: `tests/test_sdd_workflow_templates.py`
- **Deps**: T1
- **Verification**: `uv run pytest tests/test_sdd_workflow_templates.py -v` — new assertions pass and existing assertions remain green.

---

## Phase 3 — Self-bootstrap sync + full regression

### T3 — Regenerate derived command and run full verification ✅

- **Outcome**: `.claude/commands/codexspec/implement-tasks.md` is regenerated from the updated template (not hand-edited) via `uv run codexspec init . --force`; its **body** matches `templates/commands/implement-tasks.md` (frontmatter is expected to differ — localized to `zh-CN` by the installer). The full test suite is green and `ruff` is clean.
- **Covers**: Plan: Decision 1 / Phase 3 — *implementation support* (constitution-mandated self-bootstrap propagation; no direct REQ/NFR mapping)
- **Files**: `.claude/commands/codexspec/implement-tasks.md` (derived, regenerated by `init`)
- **Deps**: T2 (T3 runs the full suite, which includes T2's new tests)
- **Actual method (deviation — see `issues.md`)**: `uv run codexspec init . --force` was **not** used — verified that `init --force` overwrites `CLAUDE.md` (`src/codexspec/__init__.py:776`). Instead regenerated only the one derived file via the same internal helper: `translate_template_frontmatter(template_content, "implement-tasks", "zh-CN", cache)` → byte-identical to `install_commands_to_subdir(force=True)` for that file, touching nothing else.
- **Verification**:
  - Body match (compare only the body, after the closing frontmatter `---`, so the localized frontmatter does not create false differences):
    `diff <(awk 'BEGIN{c=0} /^---[[:space:]]*$/ {c++; if(c==2){p=1; next}} p' templates/commands/implement-tasks.md) <(awk 'BEGIN{c=0} /^---[[:space:]]*$/ {c++; if(c==2){p=1; next}} p' .claude/commands/codexspec/implement-tasks.md)` — result: **BODY IDENTICAL**
  - Frontmatter localization sanity (derived only): `grep -q "执行实现任务" .claude/commands/codexspec/implement-tasks.md` — present
  - `uv run pytest` — **841 passed, 37 skipped**
  - `uv run ruff check src/` — **All checks passed**

---

## Dependencies

```
T1 (template) -> T2 (guard tests) -> T3 (sync + full verify)
```

Strictly sequential; no `[P]` opportunities (each task depends on the prior task's output).

## Coverage

| Plan Component / Requirement | Task | Notes |
|------------------------------|------|-------|
| Decision 1 (source edit + self-bootstrap sync) | T1, T3 | T1 edits source; T3 syncs derived |
| Decision 2 (loop placement, additive) | T1 | 3.4 Review & Refactor preserved |
| Decision 3 (review target = this run's diff) | T1 | git-based with graceful fallback |
| Decision 4 (auto-fix scope + tool split; resolves OPEN-001) | T1 | review-code read-only; fixes by implement-tasks |
| Decision 5 (bounds / stop / status) | T1 | max 2 rounds; "needs work" on residual |
| Phase 1 | T1 | |
| Phase 2 | T2 | guard tests |
| Phase 3 | T3 | sync + regression |
| REQ-001 … REQ-010 | T1 (behavior), T2 (verification) | REQ-010 also via T2 preservation assertion |
| NFR-001 … NFR-003 | T1 (behavior), T2 (verification) | |
| OPEN-001 | T1 (Decision 4) | Resolved at plan level |

## Unmapped Tasks

None. Every plan deliverable (Phase 1–3, Decisions 1–5) has task coverage. No separate documentation/CLAUDE.md update task is added — it is not required by the approved plan (optional maintainer follow-up only).

## Notes

- The change is confined to one template file, one test file, and one derived file regenerated by `init` — no CLI, package code, or config-schema changes.
- Commit after each task per the repo's incremental-commit convention.
- When this feature is itself implemented via `/codexspec:implement-tasks`, the diff will be non-code (`.md`/`.py` test is code) — note `tests/*.py` IS analyzable code, so the new loop would review the test file added in T2; the template edit itself (`.md`) is excluded as non-code (CON-003), which is the intended behavior.
