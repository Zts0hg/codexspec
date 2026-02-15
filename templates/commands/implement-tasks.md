---
description: Execute the implementation tasks according to the task breakdown
handoffs:
  - agent: claude
    step: Implement tasks following the defined order and dependencies
---

# Task Implementer

## User Input

$ARGUMENTS

## Instructions

Execute the implementation tasks in the correct order, following the task breakdown. This command drives the actual code generation and implementation.

### Steps

1. **Validate Prerequisites**: Before starting, verify:
   - [ ] Constitution exists at `.codexspec/memory/constitution.md`
   - [ ] Specification exists at `.codexspec/specs/{feature-id}/spec.md`
   - [ ] Plan exists at `.codexspec/specs/{feature-id}/plan.md`
   - [ ] Tasks exist at `.codexspec/specs/{feature-id}/tasks.md`

2. **Load Context**: Read and understand:
   - Project constitution (principles and guidelines)
   - Feature specification (requirements)
   - Implementation plan (architecture and tech stack)
   - Task breakdown (execution order)

3. **Parse Tasks**: Load and parse the task breakdown:
   - Identify task order
   - Note dependencies
   - Identify parallelizable tasks

4. **Execute Tasks**: Implement each task:
   - Follow task descriptions precisely
   - Create/modify specified files
   - Respect task dependencies
   - Follow constitution guidelines
   - Implement according to plan

5. **Validate Progress**: After each task or phase:
   - Verify implementation matches plan
   - Check code quality against constitution
   - Ensure requirements are met

6. **Report Progress**: Provide clear updates:
   - Current task being executed
   - Files created/modified
   - Any issues encountered
   - Next steps

### Execution Pattern

```
For each task in order:
    1. Check if dependencies are complete
    2. Read task requirements
    3. Implement in specified files
    4. Verify implementation
    5. Report completion
    6. Move to next task
```

### Progress Report Template

```markdown
# Implementation Progress

## Current Status
- **Phase**: [Current Phase]
- **Task**: [Current Task]
- **Progress**: X/Y tasks complete

## Completed Tasks
- [x] Task 1.1: Setup project structure
- [x] Task 1.2: Configure dependencies
- [x] Task 2.1: Create data models

## In Progress
- [ ] Task 2.2: Create service layer
  - Files: src/services/*.py
  - Status: Implementing UserService

## Pending Tasks
- [ ] Task 2.3: API endpoints
- [ ] Task 3.1: Unit tests

## Files Modified
| File | Action | Lines |
|------|--------|-------|
| src/models/user.py | Created | 45 |
| src/models/task.py | Created | 38 |
| src/services/user_service.py | Created | 67 |

## Issues Encountered
- None so far

## Next Steps
1. Complete Task 2.2
2. Start Task 2.3 (API endpoints)
```

### Implementation Guidelines

1. **Follow the Plan**: Stick to the technical plan unless there's a good reason to deviate
2. **Constitution Compliance**: Ensure code follows project principles
3. **Quality First**: Write clean, tested, maintainable code
4. **Incremental Progress**: Complete one task before moving to the next
5. **Error Handling**: Handle errors gracefully and report issues

### Error Handling

If implementation fails:
1. Stop and report the error
2. Explain what went wrong
3. Suggest potential fixes
4. Wait for user guidance before continuing

> [!NOTE]
> This is a placeholder command. The full implementation will be added in future versions.
