---
name: codexspec:implement-tasks
description: "执行实现任务，支持条件 TDD 工作流（代码使用 TDD，文档/配置直接实现）"
---

# Task Implementer

## Language Preference

Read `.codexspec/config.yml`. Two independent language controls apply (each falls back to `language.output`, then English):

- **Interaction language** (`language.interaction`): language for all conversation with the user — questions, explanations, status messages, and `codexspec` CLI terminal output.
- **Document language** (`language.document`): language for generated artifact files (requirements/spec/plan/tasks).

Converse in the interaction language and author artifacts in the document language. Apply the project's translation standard to both: translate by meaning (not word-for-word), keep English for terms with no good native equivalent, and write as if originally in that language.

## Feature Resolution

Resolve the feature in this order:

1. Use an explicit path from `the text after the $codexspec:implement-tasks skill mention` when it identifies a `tasks.md` file
   or feature directory.
2. Otherwise match the current branch, which must use the timestamp format, to
   `.codexspec/specs/<branch>/`.
3. If no unique feature can be resolved, ask the user to select one. Never
   silently select the latest workspace.

Derive all artifact paths from the selected feature directory. All
implementation-side output belongs to that workspace.

## Input Documents and Authority

Read:

- `requirements.md`
- `spec.md`
- `plan.md`
- `tasks.md`
- `.codexspec/memory/constitution.md` when present

Authority order:

1. Confirmed entries in `requirements.md`
2. `spec.md`
3. Constitution and verified repository facts
4. Approved `plan.md`
5. `tasks.md`

When `requirements.md` is absent, use legacy spec-only mode. Treat `spec.md` as
the temporary highest feature authority and state that fidelity to the original
discussion cannot be verified.

## Role

You are an **autonomous implementation agent**. Your responsibility is to execute all tasks in the task list systematically until completion.

## Instructions

### 1. Prerequisites

Before starting, verify that `spec.md`, `plan.md`, and `tasks.md` exist in the
resolved workspace. Stop if tasks conflict with higher-authority artifacts
instead of silently implementing the conflict.

### 2. Tech Stack Detection

Identify the project's technology stack:

1. Check `plan.md` for defined tech stack
2. Verify with project files: `package.json`, `pyproject.toml`, `go.mod`, `Cargo.toml`, etc.
3. Determine conventions: source directory, test directory, test command, package manager

### 3. TDD Workflow (Per Task)

For **each task**, determine the workflow based on task type:

#### Implementation Tasks (code that needs testing)

1. **Red - Write Test First**
   - Write unit tests that define expected behavior
   - Tests should fail initially (no implementation exists yet)

2. **Green - Implement to Pass**
   - Write the minimum code necessary to make tests pass
   - Follow the technical plan and constitution guidelines

3. **Verify - Run Tests**
   - Execute all relevant tests
   - Ensure new tests pass and no existing tests break

4. **Review & Refactor**
   - Check for bugs, edge cases, security issues
   - Improve code readability and maintainability
   - Keep tests green while refactoring

5. **Mark Complete**
   - Update `tasks.md`: change `[ ]` to `[x]`
   - Record any important notes or decisions
   - Continue to next task (respect dependencies)

#### Non-Testable Tasks (docs, config, assets)

Implement directly and verify correctness. Task types that typically don't need tests:

- Documentation (README, API docs, user guides)
- Configuration files (JSON, YAML, TOML)
- Static assets (images, styles, fonts)
- Infrastructure files (Dockerfile, CI/CD configs)

### 4. Autonomous Execution

**Work continuously** until all tasks are completed:

- Do not wait for user approval between tasks
- When encountering blockers:
  - Record the issue in `issues.md` (task ID, error, attempted solutions, status)
  - Continue to the next independent task
- Commit code after completing significant tasks or phases
- Update progress in `tasks.md` as tasks are completed

### 5. Issue Recording

When encountering problems, create/update `issues.md` in the same directory as `tasks.md`:

```markdown
## Issue: [Brief Description]
- **Task**: Task X.X
- **Error**: [Error message or description]
- **Attempted**: [Solutions you tried]
- **Status**: Blocked / Workaround Found / Needs Discussion
```

### 6. Pre-Review Baseline

After all tasks are implemented:

- Run the full test suite.
- Confirm the suite is green. This green state is the baseline for the Final
  Code Review Loop; no auto-fix may regress it. If the suite is already red at
  this point, stop and fix the implementation before reviewing.

### 7. Final Code Review Loop

After the baseline is green, review the implemented code and auto-fix verified
defects. This mirrors the `review-spec` / `review-plan` / `review-tasks` loops
the sibling generation commands run.

#### 7.1 Determine the Review Target

Review only the analyzable code changed by this implementation, not the whole
repository and not per task. Compute the candidate file set:

```
git diff --name-only $(git merge-base HEAD <main>)..HEAD
git diff --name-only                       # uncommitted tracked changes
git ls-files --others --exclude-standard   # untracked files
```

`<main>` is the project's default branch, resolved from `git.main_branches` in
`.codexspec/config.yml` (default: `main`, `master`, `develop`).

Then filter the candidate set:

- Keep only analyzable source extensions: `.py .ts .tsx .js .jsx .go .rs .java
  .kt .kts .rb .sh .bash .zsh .c .h .cpp .hpp .cc .cxx .cs .swift .php`.
- Exclude `.codexspec/specs/` and generated/vendored paths (e.g. `dist/`,
  lockfiles, `.venv/`).

If the filtered set is empty (e.g. the implementation produced only docs,
config, or assets), report "no code to review", skip this loop, and proceed to
step 8.

Fallback: if git is unavailable or the current branch is not a feature branch
(so the diff base cannot be determined), review the project's primary source
directory as `$codexspec:review-code` would by default, and explicitly note the
degraded fidelity (the review may include pre-existing code).

#### 7.2 Invoke the Review

Invoke `$codexspec:review-code <filtered-paths>`.

`$codexspec:review-code` is **review-only**; it produces findings and scores but
does not edit code. Apply every fix **yourself**, under this command's tool
scope (which includes `Edit`/`Write` and running the test suite via `Bash`).

#### 7.3 Auto-Fix Scope

- Auto-fix **CRITICAL, HIGH, and MEDIUM** findings only.
- **LOW** (suggestion) findings are report-only; never auto-fix them.
- A **MEDIUM** finding is auto-fixed only when it is grounded in
  `.codexspec/memory/constitution.md` and the confirmed requirements/spec, and
  it concerns **maintainability, readability, or testability**. Ungrounded or
  purely stylistic MEDIUM findings are report-only.
- Do not auto-fix advisories or design opportunities, and do not introduce any
  new product decision.

#### 7.4 Test-Safe Fixes (never ship red)

Every fix must be test-safe. A fix that breaks tests is, by definition, an
incorrect change — it is never shipped and never silently skipped.

- **Functional defects** (logic, correctness, security): follow TDD — add a
  failing test that reproduces the defect (red), apply the fix until that test
  passes (green), then refactor while tests stay green.
- **Non-functional fixes** (refactors for maintainability, readability,
  testability): run the suite before and after the change. If the change turns
  any test red, revert it, confirm the suite is green again, and re-attempt the
  refactor.
- If a fix cannot be made green after retry, treat it as **unresolved** and stop
  (see 7.5).

#### 7.5 Loop Bounds and Stop Conditions

- Run at most **two** fix-and-review rounds. (The per-fix TDD retry in 7.4
  happens within a round; the two-round limit bounds overall effort.)
- Stop when a defect repeats, remains unresolved, or requires a user or
  architecture decision.
- After each green round, commit the fixes (see step 8).

#### 7.6 Terminal Status

- If CRITICAL or HIGH defects remain unresolved after the maximum rounds, the
  status is **"needs work"** — do not claim success.
- Otherwise report the review outcome: scores, items fixed, items deferred, and
  the final test status.

### 8. Final Report and Commit

- Commit any review-driven changes from step 7 that are not already committed.
- Report the completion summary: files modified, review status (scores, items
  fixed, items deferred, final test status), and the overall status (success or
  "needs work").
