---
description: Break down a technical implementation plan into actionable tasks
handoffs:
  - agent: claude
    step: Generate task breakdown from plan
---

# Plan to Tasks Converter

## Language Preference

**IMPORTANT**: Before proceeding, read the project's language configuration from `.codexspec/config.yml`.
- If `language.output` is set to a language other than "en", respond and generate all content in that language
- If not configured or set to "en", use English as default
- Technical terms (e.g., API, JWT, OAuth) may remain in English when appropriate
- All user-facing messages, questions, and generated documents should use the configured language

## User Input

$ARGUMENTS

## Instructions

Break down the technical implementation plan into specific, actionable tasks that can be executed in order.

### Steps

1. **Read Plan**: Load the plan from `.codexspec/specs/{feature-id}/plan.md`.

2. **Read Constitution**: Review `.codexspec/memory/constitution.md` for workflow guidelines.

3. **Identify Tasks**: Parse the plan and identify all implementation tasks:
   - Setup tasks
   - Model creation tasks
   - Service implementation tasks
   - API endpoint tasks
   - Testing tasks
   - Documentation tasks

4. **Analyze Dependencies**: Determine task dependencies:
   - Which tasks must complete before others can start
   - Which tasks can run in parallel

5. **Order Tasks**: Organize tasks in the correct dependency order.

6. **Mark Parallelizable**: Identify tasks that can be executed in parallel with `[P]` marker.

7. **Add File Paths**: Specify the exact files that need to be created or modified.

8. **Save Tasks**: Write to `.codexspec/specs/{feature-id}/tasks.md`

### Reference Templates

Use the following templates as reference for generating the task breakdown:

- **Detailed**: `.codexspec/templates/docs/tasks-template-detailed.md` - Full format with phases, user story mapping, parallel markers, dependency graphs, and execution strategies
- **Simple**: `.codexspec/templates/docs/tasks-template-simple.md` - Simple grouped task list format

Choose the appropriate template based on project complexity.

### Template Structure

```markdown
# Task Breakdown: [Feature Name]

## Overview
Total tasks: [N]
Parallelizable tasks: [M]

## Phase 1: Foundation

### Task 1.1: Setup Project Structure
- **Type**: Setup
- **Files**: `src/__init__.py`, `src/api/__init__.py`, `src/models/__init__.py`
- **Description**: Create the basic project directory structure
- **Dependencies**: None
- **Est. Complexity**: Low

### Task 1.2: Configure Dependencies
- **Type**: Setup
- **Files**: `pyproject.toml`, `requirements.txt`
- **Description**: Add all required dependencies to the project
- **Dependencies**: Task 1.1
- **Est. Complexity**: Low

## Phase 2: Core Implementation

### Task 2.1: Create Data Models [P]
- **Type**: Implementation
- **Files**: `src/models/user.py`, `src/models/task.py`
- **Description**: Implement all data models as defined in the plan
- **Dependencies**: Task 1.1
- **Est. Complexity**: Medium

### Task 2.2: Create Service Layer [P]
- **Type**: Implementation
- **Files**: `src/services/user_service.py`, `src/services/task_service.py`
- **Description**: Implement business logic services
- **Dependencies**: Task 2.1
- **Est. Complexity**: High

## Phase 3: Testing

### Task 3.1: Write Unit Tests
- **Type**: Testing
- **Files**: `tests/test_models.py`, `tests/test_services.py`
- **Description**: Write comprehensive unit tests
- **Dependencies**: Task 2.2
- **Est. Complexity**: Medium

## Execution Order

```
Task 1.1 ──► Task 1.2 ──► Task 2.1 ──┬──► Task 2.2 ──► Task 3.1
                                    │
                                    └──► Task 2.3 (parallel)
```

## Checkpoints

- [ ] **Checkpoint 1**: After Phase 1 - Verify project structure
- [ ] **Checkpoint 2**: After Phase 2 - Verify core functionality
- [ ] **Checkpoint 3**: After Phase 3 - Verify test coverage
```

### Quality Criteria

- [ ] All plan items are covered by tasks
- [ ] Dependencies are correctly identified
- [ ] Parallelizable tasks are marked
- [ ] File paths are specific
- [ ] Complexity estimates are reasonable
- [ ] Checkpoints are defined

> [!NOTE]
> This is a placeholder command. The full implementation will be added in future versions.
