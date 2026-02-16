---
description: Break down a technical implementation plan into actionable tasks
argument-hint: "[path_to_spec.md path_to_plan.md] (optional, defaults to .codexspec/specs/{feature-id}/)"
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

## Role

You are acting as a **Technical Lead**. Your responsibility is to transform technical implementation plans into an **exhaustive, atomic, dependency-ordered, AI-executable task list**.

## Instructions

Analyze the provided spec and plan documents, then break down the technical implementation plan into specific, actionable tasks.

### Critical Requirements

1. **Task Granularity**: Each task should involve modifying or creating **only one primary file**. Avoid broad tasks like "implement all features".

2. **TDD Enforcement**: Per the project constitution's "Test-First Principle", **testing tasks MUST precede implementation tasks** for each component.

3. **Parallel Marking**: Mark tasks with no dependencies using `[P]` to indicate they can run in parallel.

4. **Phase Organization**: Even if the plan contains rough phase divisions, organize tasks into these standard phases (adjust names as appropriate for the project):
   - **Phase 1: Foundation** - Project structure, configuration, data models
   - **Phase 2: Core Implementation** - Primary business logic (TDD)
   - **Phase 3: Integration** - External APIs, services, connectors
   - **Phase 4: Interface** - CLI, API endpoints, UI components
   - **Phase 5: Testing & Documentation** - Integration tests, docs

### Steps

1. **Locate Documents**:
   - **If arguments provided**: Use the specified paths to `spec.md` and `plan.md`
   - **If no arguments**: Search `.codexspec/specs/` directory for the latest or active feature folder, then read `spec.md` and `plan.md` from `.codexspec/specs/{feature-id}/`

2. **Read Documents**: Load and analyze the spec and plan from the located paths.

3. **Read Constitution**: Review `.codexspec/memory/constitution.md` for project-specific workflow guidelines.

4. **Identify Tasks**: Parse the plan and identify all implementation tasks with single-file focus.

5. **Analyze Dependencies**: Determine task dependencies:
   - Which tasks must complete before others can start
   - Which tasks can run in parallel

6. **Order Tasks**: Organize tasks in correct dependency order, ensuring tests come before implementations.

7. **Mark Parallelizable**: Identify tasks that can be executed in parallel with `[P]` marker.

8. **Add File Paths**: Specify the exact files that need to be created or modified for each task.

9. **Save Tasks**: Write to `.codexspec/specs/{feature-id}/tasks.md`

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
Estimated phases: [K]

## Phase 1: Foundation

### Task 1.1: Setup Project Structure
- **Type**: Setup
- **Files**: `src/__init__.py`, `src/api/__init__.py`, `src/models/__init__.py`
- **Description**: Create the basic project directory structure
- **Dependencies**: None
- **Est. Complexity**: Low

### Task 1.2: Configure Dependencies
- **Type**: Setup
- **Files**: `pyproject.toml`
- **Description**: Add all required dependencies to the project
- **Dependencies**: Task 1.1
- **Est. Complexity**: Low

## Phase 2: Core Implementation (TDD)

### Task 2.1: Write Tests for User Model [P]
- **Type**: Testing
- **Files**: `tests/test_user_model.py`
- **Description**: Write unit tests for User model (before implementation)
- **Dependencies**: Task 1.1
- **Est. Complexity**: Low

### Task 2.2: Implement User Model
- **Type**: Implementation
- **Files**: `src/models/user.py`
- **Description**: Implement User model to pass tests in Task 2.1
- **Dependencies**: Task 2.1
- **Est. Complexity**: Low

### Task 2.3: Write Tests for User Service [P]
- **Type**: Testing
- **Files**: `tests/test_user_service.py`
- **Description**: Write unit tests for UserService (before implementation)
- **Dependencies**: Task 2.2
- **Est. Complexity**: Medium

### Task 2.4: Implement User Service
- **Type**: Implementation
- **Files**: `src/services/user_service.py`
- **Description**: Implement UserService to pass tests in Task 2.3
- **Dependencies**: Task 2.3
- **Est. Complexity**: Medium

### Task 2.5: Write Tests for Task Model [P]
- **Type**: Testing
- **Files**: `tests/test_task_model.py`
- **Description**: Write unit tests for Task model (before implementation)
- **Dependencies**: Task 1.1
- **Est. Complexity**: Low

### Task 2.6: Implement Task Model
- **Type**: Implementation
- **Files**: `src/models/task.py`
- **Description**: Implement Task model to pass tests in Task 2.5
- **Dependencies**: Task 2.5
- **Est. Complexity**: Low

## Phase 3: Integration

### Task 3.1: Write Tests for API Client [P]
- **Type**: Testing
- **Files**: `tests/test_api_client.py`
- **Description**: Write integration tests for external API client
- **Dependencies**: Task 2.4
- **Est. Complexity**: Medium

### Task 3.2: Implement API Client
- **Type**: Implementation
- **Files**: `src/clients/api_client.py`
- **Description**: Implement API client to pass tests in Task 3.1
- **Dependencies**: Task 3.1
- **Est. Complexity**: High

## Phase 4: Interface

### Task 4.1: Write Tests for CLI Commands
- **Type**: Testing
- **Files**: `tests/test_cli.py`
- **Description**: Write tests for CLI command handlers
- **Dependencies**: Task 3.2
- **Est. Complexity**: Medium

### Task 4.2: Implement CLI Entry Point
- **Type**: Implementation
- **Files**: `src/cli.py`
- **Description**: Implement CLI commands to pass tests in Task 4.1
- **Dependencies**: Task 4.1
- **Est. Complexity**: Medium

## Execution Order

```
Phase 1: Task 1.1 ──► Task 1.2
                         │
Phase 2: ┌───────────────┴───────────────┐
         │                               │
    Task 2.1 [P]                    Task 2.5 [P]
         │                               │
    Task 2.2 ──► Task 2.3 [P]       Task 2.6
                     │
                Task 2.4
                     │
Phase 3: ┌───────────┴───────────┐
         │                       │
    Task 3.1 [P]            (other parallel tasks)
         │
    Task 3.2
         │
Phase 4: Task 4.1 ──► Task 4.2
```

## Checkpoints

- [ ] **Checkpoint 1**: After Phase 1 - Verify project structure and dependencies
- [ ] **Checkpoint 2**: After Phase 2 - Verify all core tests pass
- [ ] **Checkpoint 3**: After Phase 3 - Verify integration tests pass
- [ ] **Checkpoint 4**: After Phase 4 - Verify end-to-end functionality
```

### Quality Criteria

- [ ] All plan items are covered by tasks
- [ ] Each task involves only ONE primary file (atomic granularity)
- [ ] TDD is enforced: test tasks precede implementation tasks for each component
- [ ] Dependencies are correctly identified
- [ ] Parallelizable tasks are marked with `[P]`
- [ ] File paths are specific and accurate
- [ ] Complexity estimates are reasonable
- [ ] Checkpoints are defined at phase boundaries
