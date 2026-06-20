---
description: 执行实现任务，支持条件 TDD 工作流（代码使用 TDD，文档/配置直接实现）
argument-hint: "[tasks 路径] | [spec 路径 plan 路径 tasks 路径]"
handoffs:
  - agent: claude
    step: Execute implementation tasks from the task breakdown
---

# Task Implementer

## Language Preference

Read `.codexspec/config.yml`. Two independent language controls apply (each falls back to `language.output`, then English):

- **Interaction language** (`language.interaction`): language for all conversation with the user — questions, explanations, status messages, and `codexspec` CLI terminal output.
- **Document language** (`language.document`): language for generated artifact files (requirements/spec/plan/tasks).

Converse in the interaction language and author artifacts in the document language. Apply the project's translation standard to both: translate by meaning (not word-for-word), keep English for terms with no good native equivalent, and write as if originally in that language.

## Feature Resolution

Resolve the feature in this order:

1. Use an explicit path from `$ARGUMENTS` when it identifies a `tasks.md` file
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

### 6. Completion

After all tasks:

- Run full test suite (if applicable)
- Final commit if needed
- Report completion summary with files modified
