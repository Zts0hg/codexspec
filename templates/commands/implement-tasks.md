---
description: Execute implementation tasks with conditional TDD workflow (TDD for code, direct implementation for docs/config)
argument-hint: "[tasks_path] | [spec_path plan_path tasks_path]"
handoffs:
  - agent: claude
    step: Execute implementation tasks from the task breakdown
---

# Task Implementer

## Language Preference

**IMPORTANT**: Before proceeding, read the project's language configuration from `.codexspec/config.yml`.
- If `language.output` is set to a language other than "en", respond and generate all content in that language
- If not configured or set to "en", use English as default
- Technical terms (e.g., API, JWT, OAuth) may remain in English when appropriate
- All user-facing messages, questions, and generated documents should use the configured language

## Input Documents

**Usage:**
- `/implement-tasks` → Auto-detect from `.codexspec/specs/`
- `/implement-tasks tasks.md` → `$1` as tasks path, derive others
- `/implement-tasks spec.md plan.md tasks.md` → All paths explicit

### File Resolution

- **No arguments**: Auto-detect the latest/only feature under `.codexspec/specs/`
- **One argument**: Treat `$1` as `tasks.md` path, derive `spec.md` and `plan.md` from same directory
- **Three arguments**: `$1` = spec.md, `$2` = plan.md, `$3` = tasks.md

**Output Location**: All output files go in the same directory as `tasks.md`.

## Role

You are an **autonomous implementation agent**. Your responsibility is to execute all tasks in the task list systematically until completion.

## Instructions

### 1. Prerequisites

Before starting, verify these files exist and load them:
- Specification file (spec.md)
- Technical plan file (plan.md)
- Tasks file (tasks.md)
- Project constitution (from `.codexspec/memory/constitution.md` if exists)

### 2. Tech Stack Detection

Identify the project's technology stack:
1. Check `plan.md` for defined tech stack
2. Verify with project files: `package.json`, `pyproject.toml`, `go.mod`, `Cargo.toml`, etc.
3. Determine conventions: source directory, test directory, test command, package manager

### 3. TDD Workflow (Per Task)

For **each task**, determine the workflow based on task type:

#### Implementation Tasks (code that needs testing):

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

#### Non-Testable Tasks (docs, config, assets):

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
