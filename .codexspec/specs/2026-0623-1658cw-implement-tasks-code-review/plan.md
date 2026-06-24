# Design Document: implement-tasks → review-code auto-review loop

<!--
Language: Generate this document in the language specified in .codexspec/config.yml
If not configured, use English.
-->

**Related Spec**: `.codexspec/specs/2026-0623-1658cw-implement-tasks-code-review/spec.md`
**Confirmed Requirements**: `.codexspec/specs/2026-0623-1658cw-implement-tasks-code-review/requirements.md`
**Created**: 2026-06-23
**Status**: Draft

## Context

The three artifact-generation commands each end with an **Automatic Review Loop** section that invokes the matching `/codexspec:review-*` and auto-fixes verified defects (max two rounds). `/codexspec:implement-tasks` has no such loop. This plan adds one, chaining `implement-tasks` to `/codexspec:review-code` for a test-safe auto-review/fix of the final implementation.

**Verified repository facts** (authority: constitution + verified facts):

- The single source of truth is `templates/commands/implement-tasks.md` (English). Tests read this path (`tests/test_sdd_workflow_templates.py` → `read_command()` resolves to `templates/commands/`). The constitution's "Self-Bootstrap" and "Slash Command Template Modification Rules" forbid editing `.claude/commands/codexspec/` for distributed commands.
- `.claude/commands/codexspec/implement-tasks.md` is a **derived** install artifact: `codexspec init` renders its frontmatter in the interaction language (`zh-CN`) and copies the body from the English template. A live `diff` confirms the two differ only in frontmatter localization.
- `implement-tasks.md` frontmatter declares **no `allowed-tools`** restriction, so the command runs with full tool access. `/codexspec:review-code` is **review-only** (its `allowed-tools` allowlist covers `Read, Grep, Glob` + linters/type-checkers and excludes `Edit`/`Write`).
- `test_adjacent_commands_preserve_requirements_authority` pins Feature-Resolution phrases in implement-tasks (`requirements.md`, `explicit path`, `current branch`, `legacy spec-only`, absence of `latest feature`/`latest/only`). These sections must be preserved.

## Goals / Non-Goals

**Goals:**

- Add an end-of-run **Final Code Review Loop** to `templates/commands/implement-tasks.md` that invokes `/codexspec:review-code` on this implementation's analyzable code and applies test-safe auto-fixes.
- Make the loop consistent with the existing spec/plan/tasks review loops (invocation, two-round bound, stop conditions).
- Resolve OPEN-001 (nested-invocation tool mechanics) at the plan level so the requirement can proceed.

**Non-Goals:**

- Any CLI/package-code change (`src/codexspec/`), config-schema change, or change to other commands.
- Per-task review; reviewing pre-existing code; reviewing docs/config/assets; auto-fixing LOW findings (all confirmed Out of Scope).

## Decisions

### Decision 1: Edit the source template, then self-bootstrap-sync the derived artifact

**Context**: Constitution mandates `templates/commands/` as the source of truth; `.claude/commands/codexspec/` is a derived artifact that must not be hand-edited.

**Decision**: Implement by editing `templates/commands/implement-tasks.md` only. After the edit, sync the derived artifact by running `uv run codexspec init . --force` (repo code against the repo's own templates; `--force` overwrites existing command files). Note the propagation mechanics, verified in `src/codexspec/__init__.py` and `src/codexspec/commands/installer.py`: when `.claude/commands/codexspec/` already exists, `init` enters **update mode** and overwrites command files only with `--force` (or an interactive confirm that defaults to Yes); `install_commands_to_subdir(force=False)` otherwise **skips existing files**. `uv tool install --force .` only refreshes the installed package's template source and does **not** itself refresh `.claude/commands/codexspec/`. The `init` step re-renders frontmatter in the interaction language and copies the updated body.

**Rationale**: Matches the documented propagation path and keeps the file tests actually assert on as the source.

**Covers**: REQ-001, REQ-002, REQ-003, REQ-004, REQ-005, REQ-006, REQ-007, REQ-008, REQ-009, REQ-010

**Decision Level**: Plan-level technical decision; does not change confirmed product scope.

### Decision 2: Loop placement and additive preservation

**Context**: The loop must run after all tasks are implemented and the suite is green, but its auto-fixes produce further changes that must be committed before reporting.

**Decision**: Restructure the current "### 6. Completion" flow into:
(6) confirm all tasks done + run the full test suite to establish a **green baseline** →
(7) **Final Code Review Loop** (new) →
(8) commit any review-driven changes + final report.

Preserve "### 3. TDD Workflow → Review & Refactor" (step 4) **unchanged** (REQ-010: additive, not a replacement).

**Rationale**: Mirrors how generate-spec/spec-to-plan/plan-to-tasks place their "Automatic Review Loop" after artifact creation; keeps the existing per-task self-review intact.

**Covers**: REQ-001, REQ-007, REQ-010, NFR-002

**Decision Level**: Plan-level; does not change confirmed behavior.

### Decision 3: Determining the review target (resolves spec A-1)

**Context**: "This implementation's diff vs the feature-branch base" must be computed deterministically.

**Decision**: Compute analyzable code files changed by this run as:

```
git diff --name-only $(git merge-base HEAD <main>)..HEAD
∪  git diff --name-only            # uncommitted tracked
∪  git ls-files --others --exclude-standard   # untracked
```

then filter to `review-code`'s analyzable extensions (`.py .ts .tsx .js .jsx .go .rs .java .kt .kts .rb .sh .bash .zsh .c .h .cpp .hpp .cc .cxx .cs .swift .php`), excluding the `.codexspec/specs/` spec directory and generated/vendored paths. `<main>` is resolved from config `git.main_branches` (default `main`/`master`/`develop`).

- If the filtered set is empty → report "no code to review", skip the loop, complete normally (REQ-002).
- Fallback (no git, or not on a feature branch): review the project's primary source directory as `review-code` would by default, and **explicitly note** the degraded fidelity (may include pre-existing code). This is implementation support, not a scope change.

Pass the resulting paths to `/codexspec:review-code <paths>`.

**Rationale**: `implement-tasks` already assumes git (it commits); merge-base with the configured main branch is the most robust "feature-branch base". Spec A-1 deferred this to the plan.

**Covers**: REQ-001, REQ-002, NFR-002

**Decision Level**: Plan-level; does not change confirmed behavior.

### Decision 4: Auto-fix scope and tool split (resolves OPEN-001)

**Context**: `review-code` is review-only and its `allowed-tools` allowlist excludes `Edit`/`Write`; auto-fix must edit code and run tests.

**Decision**:

- **Tool split**: invoke `/codexspec:review-code` for read-only analysis (its allowlist already covers the linters/type-checkers it runs); `implement-tasks` applies every fix **itself**, under its own full tool scope (`Edit`/`Write` + `Bash` to run the test suite). Because the orchestrator (`implement-tasks`) holds the broad scope and performs the edits, the nested-invocation tool-permission question (OPEN-001) is non-blocking — fixes never depend on `review-code`'s restricted scope.
- **Severity**: auto-fix CRITICAL + HIGH + MEDIUM only; MEDIUM only when grounded in `.codexspec/memory/constitution.md` + the confirmed requirements/spec and focused on maintainability/readability/testability; LOW is report-only.
- **Test-safety**:
  - Functional defect (logic/correctness/security): TDD — add a failing reproducer (red) → fix (green) → refactor (green).
  - Non-functional refactor: run the suite before and after; if a change turns it red, it is incorrect → revert → confirm green restored → re-attempt; never ship red, never silently skip.
  - A fix that cannot be made green → treat as unresolved → stop and report.
- Commit auto-fix changes before reporting completion.

**Rationale**: Separates the read-only analysis concern (review-code) from the mutation concern (implement-tasks), which is exactly how the two commands' tool scopes are already designed. The test-safety procedure is the confirmed DEC-002.

**Alternatives considered**: Delegate edits to `review-code` — rejected: its `allowed-tools` forbids `Edit`/`Write` by design.

**Covers**: REQ-003, REQ-004, REQ-005, REQ-006, REQ-008, NFR-003; resolves OPEN-001.

**Decision Level**: Plan-level; does not change confirmed behavior.

### Decision 5: Loop bounds, stop conditions, terminal status

**Decision**: Max two fix-and-review rounds; stop on a repeating defect, an unresolved defect, or a user/architecture decision; never auto-fix advisories/design-opportunities; never introduce a new product decision. Residual CRITICAL/HIGH after the round limit → report "needs work" (per `review-code`'s status vocabulary) and do not claim success; otherwise report scores + items fixed + items deferred + final test status.

**Rationale**: Consistency with the existing review loops (NFR-001) and confirmed DEC-003/DEC-006.

**Covers**: REQ-007, REQ-009, NFR-001, NFR-003

**Decision Level**: Plan-level; does not change confirmed behavior.

## Architecture

The loop runs entirely as prose-guided behavior inside the `implement-tasks` command. `review-code` is invoked for analysis only; all mutation happens in `implement-tasks`' scope.

```
implement-tasks (full tool scope)
  │
  1. all tasks done → run full suite → confirm GREEN baseline
  │
  2. compute review target = analyzable code in this run's diff (Decision 3)
  │     └─ empty? → report "no code to review" → complete normally
  │
  3. REPEAT ≤ 2 rounds:
  │     invoke /codexspec:review-code <paths>   (read-only: Read/Grep/Glob + linters)
  │            │
  │            └─ findings: CRITICAL / HIGH / MEDIUM / LOW (+ scores)
  │     filter: keep CRITICAL+HIGH+MEDIUM (MEDIUM only if grounded — Decision 4)
  │     for each finding, apply test-safe fix IN implement-tasks scope:
  │        • functional → TDD red→green→refactor
  │        • refactor   → run tests before+after; red ⇒ revert, restore green, retry
  │        • cannot make green ⇒ mark unresolved
  │     re-run suite; commit green fixes (Decision 4)
  │     stop early if: repeat / unresolved / decision-needed
  │
  4. status: residual CRITICAL/HIGH ⇒ "needs work" (no false success); else report outcome
  │
  5. final commit (if any) + completion report
```

**Covers**: REQ-001, REQ-007, NFR-001, NFR-002, NFR-003

## Risks / Trade-offs

| Risk | Impact | Mitigation |
|------|--------|------------|
| `review-code` on a large diff is slow/costly | Medium | Strict diff scoping (CON-002/NFR-002); max 2 rounds |
| MEDIUM refactors cause churn | Medium | Grounding rule (REQ-004): only constitution/requirements-grounded, maintainability-focused; test-safety revert+retry; never ship red |
| Nested-invocation tool scoping uncertainty (OPEN-001) | Medium | Decision 4 tool split — fixes never rely on review-code's restricted scope |
| Diff-base mis-detection (wrong merge-base) over/under-includes files | Low | Use configured `git.main_branches`; degrade gracefully with an explicit fidelity note |

## Verification Strategy

- **Structural (pytest)**: extend `tests/test_sdd_workflow_templates.py` with assertions that `templates/commands/implement-tasks.md` contains the new loop and its key rules (invokes `review-code`; CRITICAL+HIGH+MEDIUM; MEDIUM grounding; test-safe revert/retry; max two rounds; "needs work" on residual high-severity; commit before reporting). Mirror the style of the existing review-loop tests.
- **REQ-010 preservation**: assert "Review & Refactor" (section 3.4) is still present, and that `test_adjacent_commands_preserve_requirements_authority` still passes (Feature-Resolution phrases untouched).
- **Self-bootstrap sync**: re-run `codexspec init` (or reinstall) and verify the `.claude/commands/codexspec/implement-tasks.md` **body** matches the updated template (frontmatter is expected to differ by interaction-language rendering).
- **Regression**: `uv run pytest` green; `uv run ruff check src/` clean.

## Implementation Notes

- No code, schema, or config changes — only `templates/commands/implement-tasks.md` (and the derived `.claude/commands/codexspec/implement-tasks.md` via init) plus test assertions.
- Phrasing of the new section should mirror the existing "Automatic Review Loop" sections for consistency (NFR-001), adapted for code paths and test-safety.

## Implementation Phases

### Phase 1: Template edit

- [ ] Restructure "### 6. Completion" into baseline-green → loop → commit/report.
- [ ] Add "### 7. Final Code Review Loop" with review-target computation (Decision 3), invocation of `/codexspec:review-code`, auto-fix scope + test-safety (Decision 4), bounds/stop/status (Decision 5).
- [ ] Leave "### 3. TDD Workflow → Review & Refactor" unchanged.

Covers: REQ-001…REQ-010, NFR-001…NFR-003

### Phase 2: Tests

- [ ] Add structural assertions for the new loop in `tests/test_sdd_workflow_templates.py`.
- [ ] Add a REQ-010 preservation assertion ("Review & Refactor" present).

Covers: verification of REQ-001…REQ-010, NFR-001…NFR-003

### Phase 3: Self-bootstrap sync + full verification

- [ ] Run `uv run codexspec init . --force` to regenerate `.claude/commands/codexspec/implement-tasks.md` (overwrites the existing derived file; a bare `init` enters update mode and prompts, defaulting to Yes).
- [ ] Verify derived body matches template; confirm frontmatter localization only.
- [ ] `uv run pytest` green; `uv run ruff check src/` clean.

Covers: Decision 1 (propagation); regression safety.

## Requirements Coverage

| Spec Requirement | Plan Coverage | Reference |
|------------------|---------------|-----------|
| REQ-001 | Full | Decision 1 / Decision 2 / Decision 3 / Phase 1 |
| REQ-002 | Full | Decision 3 / Phase 1 |
| REQ-003 | Full | Decision 4 / Phase 1 |
| REQ-004 | Full | Decision 4 / Phase 1 |
| REQ-005 | Full | Decision 4 / Phase 1 |
| REQ-006 | Full | Decision 4 / Phase 1 |
| REQ-007 | Full | Decision 2 / Decision 5 / Phase 1 |
| REQ-008 | Full | Decision 4 / Phase 1 |
| REQ-009 | Full | Decision 5 / Phase 1 |
| REQ-010 | Full | Decision 2 / Phase 1 (Phase 2 preservation test) |
| NFR-001 | Full | Decision 5 / Architecture / Phase 1 |
| NFR-002 | Full | Decision 2 / Decision 3 / Phase 1 |
| NFR-003 | Full | Decision 4 / Decision 5 / Phase 1 |
| OPEN-001 | Resolved (plan) | Decision 4 (tool split) |
