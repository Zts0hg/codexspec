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

3. **Parallel Marking**: Mark tasks that can be executed in parallel with other tasks at the same level using `[P]`. Note: tasks with `[P]` may still have dependencies on earlier phases.

4. **Phase Organization**: Organize tasks into these standard phases (adjust names as appropriate for the project):
   - **Phase 1: Foundation** - Project structure, configuration, base modules
   - **Phase 2: Core Implementation** - Primary business logic (TDD)
   - **Phase 3: Integration** - External services, APIs, connectors
   - **Phase 4: Interface Layer** - User-facing interfaces (CLI, Web API, UI, etc.)
   - **Phase 5: Testing & Documentation** - End-to-end tests, documentation

5. **Technology Stack Adaptation**: Adapt file paths, directory structure, naming conventions, and testing frameworks to match the project's technology stack as specified in the constitution or plan (e.g., Python uses `src/`, `tests/`; JavaScript uses `src/`, `__tests__/`; Go uses internal packages, etc.).

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

**Note**: The example below uses generic placeholders. You MUST adapt file paths, module names, and directory structure to match the project's technology stack (e.g., Python: `src/`, `tests/`, `pyproject.toml`; JavaScript: `src/`, `__tests__/`, `package.json`; Go: internal packages, `go.mod`; etc.).

```markdown
# Task Breakdown: [Feature Name]

## Overview
Total tasks: [N]
Parallelizable tasks: [M]
Estimated phases: [K]

## Phase 1: Foundation

### Task 1.1: Setup Project Structure
- **Type**: Setup
- **Files**: `[source-dir]/[main-entry]`
- **Description**: Create the main project structure with entry point
- **Dependencies**: None
- **Est. Complexity**: Low

### Task 1.2: Create Core Module [P]
- **Type**: Setup
- **Files**: `[source-dir]/core/[module-init]`
- **Description**: Create core module with basic structure
- **Dependencies**: Task 1.1
- **Est. Complexity**: Low

### Task 1.3: Create Data Module [P]
- **Type**: Setup
- **Files**: `[source-dir]/data/[module-init]`
- **Description**: Create data layer module
- **Dependencies**: Task 1.1
- **Est. Complexity**: Low

### Task 1.4: Configure Dependencies
- **Type**: Setup
- **Files**: `[config-file]`
- **Description**: Add all required dependencies to the project
- **Dependencies**: Task 1.1
- **Est. Complexity**: Low

## Phase 2: Core Implementation (TDD)

### Task 2.1: Write Tests for Entity A [P]
- **Type**: Testing
- **Files**: `[test-dir]/[entity-a-test]`
- **Description**: Write unit tests for Entity A (before implementation)
- **Dependencies**: Task 1.3
- **Est. Complexity**: Low

### Task 2.2: Implement Entity A
- **Type**: Implementation
- **Files**: `[source-dir]/data/[entity-a-file]`
- **Description**: Implement Entity A to pass tests in Task 2.1
- **Dependencies**: Task 2.1
- **Est. Complexity**: Low

### Task 2.3: Write Tests for Service A [P]
- **Type**: Testing
- **Files**: `[test-dir]/[service-a-test]`
- **Description**: Write unit tests for Service A (before implementation)
- **Dependencies**: Task 2.2
- **Est. Complexity**: Medium

### Task 2.4: Implement Service A
- **Type**: Implementation
- **Files**: `[source-dir]/services/[service-a-file]`
- **Description**: Implement Service A to pass tests in Task 2.3
- **Dependencies**: Task 2.3
- **Est. Complexity**: Medium

### Task 2.5: Write Tests for Entity B [P]
- **Type**: Testing
- **Files**: `[test-dir]/[entity-b-test]`
- **Description**: Write unit tests for Entity B (before implementation)
- **Dependencies**: Task 1.3
- **Est. Complexity**: Low

### Task 2.6: Implement Entity B
- **Type**: Implementation
- **Files**: `[source-dir]/data/[entity-b-file]`
- **Description**: Implement Entity B to pass tests in Task 2.5
- **Dependencies**: Task 2.5
- **Est. Complexity**: Low

## Phase 3: Integration

### Task 3.1: Write Tests for External Client [P]
- **Type**: Testing
- **Files**: `[test-dir]/[client-test]`
- **Description**: Write integration tests for external service client
- **Dependencies**: Task 2.4
- **Est. Complexity**: Medium

### Task 3.2: Implement External Client
- **Type**: Implementation
- **Files**: `[source-dir]/clients/[client-file]`
- **Description**: Implement external client to pass tests in Task 3.1
- **Dependencies**: Task 3.1
- **Est. Complexity**: High

## Phase 4: Interface Layer

### Task 4.1: Write Tests for Interface Handlers
- **Type**: Testing
- **Files**: `[test-dir]/[interface-test]`
- **Description**: Write tests for interface handlers (CLI/Web API/UI)
- **Dependencies**: Task 3.2
- **Est. Complexity**: Medium

### Task 4.2: Implement Interface Entry Point
- **Type**: Implementation
- **Files**: `[source-dir]/[interface-entry]`
- **Description**: Implement interface handlers to pass tests in Task 4.1
- **Dependencies**: Task 4.1
- **Est. Complexity**: Medium

## Phase 5: Testing & Documentation

### Task 5.1: Write End-to-End Tests
- **Type**: Testing
- **Files**: `[test-dir]/[e2e-test]`
- **Description**: Write end-to-end tests covering complete user workflows
- **Dependencies**: Task 4.2
- **Est. Complexity**: High

### Task 5.2: Write API Documentation [P]
- **Type**: Documentation
- **Files**: `[docs-dir]/api.md`
- **Description**: Document all public APIs and their usage
- **Dependencies**: Task 4.2
- **Est. Complexity**: Low

### Task 5.3: Write User Guide [P]
- **Type**: Documentation
- **Files**: `[docs-dir]/user-guide.md`
- **Description**: Write user-facing documentation and usage examples
- **Dependencies**: Task 4.2
- **Est. Complexity**: Medium

## Execution Order

```
Phase 1: Task 1.1 ──► ┌─► Task 1.2 [P]
                       │
                       └─► Task 1.3 [P] ──► Task 1.4
                                                │
Phase 2: ┌───────────────────────────────────────┴───────────────┐
         │                                                       │
    Task 2.1 [P]                                            Task 2.5 [P]
         │                                                       │
    Task 2.2 ──► Task 2.3 [P]                              Task 2.6
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
                         │
Phase 5: ┌───────────────┴───────────────┐
         │                               │
    Task 5.1                        Task 5.2 [P]
                                         │
                                    Task 5.3 [P]
```

## Checkpoints

- [ ] **Checkpoint 1**: After Phase 1 - Verify project structure and module setup
- [ ] **Checkpoint 2**: After Phase 2 - Verify all core tests pass
- [ ] **Checkpoint 3**: After Phase 3 - Verify integration tests pass
- [ ] **Checkpoint 4**: After Phase 4 - Verify interface layer functionality
- [ ] **Checkpoint 5**: After Phase 5 - Verify end-to-end tests and documentation
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

## Available Follow-up Commands

After generating the task breakdown, the user may consider:
- `/codexspec.review-tasks` - to validate the task breakdown quality before implementation
- `/codexspec.implement-tasks` - to proceed directly with implementing the tasks
