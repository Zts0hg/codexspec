---
description: Execute the implementation tasks following TDD workflow
argument-hint: "[spec_path] [plan_path] [tasks_path]"
arguments:
  - name: spec_path
    description: Path to specification file (spec.md). Optional - defaults to .codexspec/specs/{latest}/spec.md
  - name: plan_path
    description: Path to technical plan file (plan.md). Optional - defaults to .codexspec/specs/{latest}/plan.md
  - name: tasks_path
    description: Path to tasks file (tasks.md). Optional - defaults to .codexspec/specs/{latest}/tasks.md
---

# Task Implementer

## Language Preference

**IMPORTANT**: Before proceeding, read the project's language configuration from `.codexspec/config.yml`.
- If `language.output` is set to a language other than "en", respond and generate all content in that language
- If not configured or set to "en", use English as default
- Technical terms (e.g., API, JWT, OAuth) may remain in English when appropriate
- All user-facing messages, questions, and generated documents should use the configured language

## Input Documents

- **Specification** (`spec.md`): $1
- **Technical Plan** (`plan.md`): $2
- **Task List** (`tasks.md`): $3

If any argument is not provided, use default paths under `.codexspec/specs/` directory.

## Instructions

As an autonomous development agent, implement all tasks in the task list following strict TDD (Test-Driven Development) principles. Work continuously until all tasks are completed.

### Prerequisites Check

Before starting, verify these files exist:
- [ ] Specification file
- [ ] Technical plan file
- [ ] Tasks file

Load and understand:
- Project constitution (from `.codexspec/memory/constitution.md` if exists)
- Feature requirements from specification
- Architecture and tech stack from plan
- Task breakdown and dependencies

### TDD Workflow (Per Task)

For **each task** in the task list, follow this cycle:

1. **🔴 Red - Write Test First**
   - Write unit tests that define expected behavior
   - Tests should fail initially (no implementation exists yet)
   - Focus on test coverage for the task requirements

2. **🟢 Green - Implement to Pass**
   - Write the minimum code necessary to make tests pass
   - Follow the technical plan and constitution guidelines
   - Create/modify files as specified in the task

3. **✅ Verify - Run Tests**
   - Execute all relevant tests
   - Ensure new tests pass and no existing tests break
   - Fix any test failures before proceeding

4. **🔍 Review - Check for Issues**
   - Look for potential bugs, edge cases, security issues
   - Verify implementation matches the plan
   - Check code quality against constitution principles

5. **🧹 Refactor - Improve Code Quality**
   - Improve code readability, maintainability
   - Remove duplication while keeping tests green
   - Ensure good testability and extensibility

6. **📝 Mark Complete**
   - Update `tasks.md`: change `[ ]` to `[x]` for completed task
   - Record any important notes or decisions made

7. **➡️ Continue to Next Task**
   - Move to the next task in order
   - Respect task dependencies

### Autonomous Mode

**Work continuously** until all tasks are completed:
- Do not wait for user approval between tasks
- When encountering blockers:
  - Record the issue in `.codexspec/specs/{feature-id}/issues.md`
  - Include: task ID, error description, attempted solutions
  - Continue to the next independent task
- Periodically commit code (after completing significant tasks or phases)
- Update progress in `tasks.md` as tasks are completed

### Issue Recording

When encountering problems, create/update `issues.md`:

```markdown
# Implementation Issues

## Issue 1: [Brief Description]
- **Task**: Task X.X
- **Date**: YYYY-MM-DD HH:MM
- **Error**: [Error message or description]
- **Context**: [What you were trying to do]
- **Attempted**: [Solutions you tried]
- **Status**: Blocked / Workaround Found / Needs Discussion
- **Impact**: [What this blocks or affects]
```

### Progress Reporting

After completing each phase or significant task group, provide a brief update:

```markdown
# Implementation Progress

**Status**: X/Y tasks completed

## Completed
- [x] Task 1.1: [description]
- [x] Task 1.2: [description]

## In Progress
- [ ] Task 2.1: [description] - [current status]

## Files Modified
| File | Action | Description |
|------|--------|-------------|
| src/module.py | Created | Brief description |

## Issues
- None / See issues.md
```

### Execution Pattern

```
For each task in tasks.md:
    1. Check if dependencies are complete
    2. If blocked → record in issues.md, continue to next
    3. Write tests (Red)
    4. Implement code (Green)
    5. Run tests and verify
    6. Review and refactor
    7. Mark task complete in tasks.md
    8. If milestone reached → commit changes
    9. Continue to next task

After all tasks:
    - Run full test suite
    - Final commit if needed
    - Report completion summary
```

### Quality Guidelines

1. **TDD First**: Never write implementation before tests
2. **Constitution Compliance**: Follow project principles from constitution.md
3. **Plan Adherence**: Stick to technical plan unless blocked
4. **Clean Code**: Prioritize readability and maintainability
5. **Test Coverage**: Aim for meaningful test coverage, not just numbers
6. **Incremental Commits**: Commit after logical units of work
