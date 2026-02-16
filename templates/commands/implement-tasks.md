---
description: Execute implementation tasks with conditional TDD workflow (TDD for code, direct implementation for docs/config)
argument-hint: "[tasks_path] | [spec_path plan_path tasks_path]"
arguments:
  - name: tasks_path_or_spec
    description: If only one argument provided, treated as tasks.md path. If three arguments, this is spec.md path. Optional - auto-detect if omitted.
  - name: plan_path
    description: Path to technical plan file (plan.md). Only used when three arguments are provided.
  - name: tasks_path
    description: Path to tasks file (tasks.md). Only used when three arguments are provided.
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

### File Resolution Logic

**Case 1: No arguments (`$1` is empty)**
- Auto-detect under `.codexspec/specs/` directory:
  1. List all subdirectories under `.codexspec/specs/`
  2. If only one feature directory exists, use it
  3. If multiple exist, select the most recently modified one (based on `tasks.md` mtime)
  4. Read `spec.md`, `plan.md`, `tasks.md` from that directory

**Case 2: One argument (`$1` provided, `$2` is empty)**
- Treat `$1` as `tasks.md` path
- Derive `spec.md` and `plan.md` from the same directory

**Case 3: Three arguments (`$1`, `$2`, `$3` all provided)**
- `$1` = spec.md path
- `$2` = plan.md path
- `$3` = tasks.md path

**Output Location**
All output files (`issues.md`, progress reports) will be placed in the same directory as `tasks.md`.

## Instructions

As an autonomous development agent, implement all tasks in the task list. Use TDD (Test-Driven Development) for implementation tasks, and direct implementation for non-testable tasks (docs, config, assets). Work continuously until all tasks are completed.

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

### Tech Stack Detection

Before implementing, identify the project's technology stack:

1. **Check `plan.md`** for defined tech stack
2. **Check project files** to confirm and detect details:
   - `package.json` → JavaScript/TypeScript (Node.js)
   - `pyproject.toml` / `setup.py` → Python
   - `go.mod` → Go
   - `Cargo.toml` → Rust
   - `pom.xml` / `build.gradle` → Java
   - `*.csproj` → C#/.NET
3. **Determine project conventions**:
   - Source directory: `src/`, `lib/`, `app/`, etc.
   - Test directory: `tests/`, `__tests__/`, `test/`, `*_test.go` files, etc.
   - Test command: `npm test`, `pytest`, `go test ./...`, `cargo test`, etc.
   - Package manager: `npm`, `yarn`, `pnpm`, `pip`, `uv`, `cargo`, etc.

### TDD Workflow (Per Task)

For **each task** in the task list, determine the workflow based on task type:

#### For Implementation Tasks (code that needs testing):

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

6. **📝 Mark Complete & Continue**
   - Update `tasks.md`: change `[ ]` to `[x]` for completed task
   - Record any important notes or decisions made
   - Move to the next task (respect dependencies)

#### For Non-Testable Tasks (docs, config, assets):

1. **Implement Directly**
   - Create or modify the required files
   - Follow project conventions and guidelines

2. **Verify Correctness**
   - Check syntax, formatting, and content accuracy
   - Ensure alignment with specification and plan

3. **Mark Complete**
   - Update `tasks.md` and continue

**Task types that typically don't need tests:**
- Documentation (README, API docs, user guides, changelogs)
- Configuration files (JSON, YAML, TOML, .env templates)
- Static assets (images, styles, fonts)
- Infrastructure files (Dockerfile, docker-compose, CI/CD configs)
- Database migrations (schema changes, seed data)

### Project Type Adaptation

Adapt implementation approach based on project type:

| Project Type | Source Dir | Test Dir/Pattern | Test Command | Notes |
|--------------|------------|------------------|--------------|-------|
| Python | `src/` | `tests/` | `pytest` or `uv run pytest` | Use `python -m pytest` if no uv |
| JavaScript | `src/` | `__tests__/` or `tests/` | `npm test` | Check `package.json` scripts |
| TypeScript | `src/` | `__tests__/` or `tests/` | `npm test` | May need `npm run test:unit` |
| Go | `.` (pkg root) | `*_test.go` alongside source | `go test ./...` | Tests in same package |
| Rust | `src/` | `tests/` + `#[test]` in src | `cargo test` | Unit tests in src, integration in tests/ |
| Java | `src/main/java/` | `src/test/java/` | `mvn test` or `./gradlew test` | Mirror package structure |
| C#/.NET | `src/` | `tests/` | `dotnet test` | Solution structure varies |

**Important**: Always adapt paths and commands to the actual project structure detected

### Autonomous Mode

**Work continuously** until all tasks are completed:
- Do not wait for user approval between tasks
- When encountering blockers:
  - Record the issue in `issues.md` (same directory as `tasks.md`)
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
    3. Determine task type (implementation vs non-testable)
    4. If implementation task:
       a. Write tests (Red)
       b. Implement code (Green)
       c. Run tests and verify
       d. Review and refactor
    5. If non-testable task:
       a. Implement directly
       b. Verify correctness
    6. Mark task complete in tasks.md
    7. If milestone reached → commit changes
    8. Continue to next task

After all tasks:
    - Run full test suite (if applicable)
    - Final commit if needed
    - Report completion summary
```

### Quality Guidelines

1. **TDD for Code**: Use TDD for implementation tasks that need tests
2. **Direct Implementation**: For non-testable tasks (docs, config), implement directly
3. **Constitution Compliance**: Follow project principles from constitution.md
4. **Plan Adherence**: Stick to technical plan unless blocked
5. **Clean Code**: Prioritize readability and maintainability
6. **Test Coverage**: Aim for meaningful test coverage on testable code
7. **Incremental Commits**: Commit after logical units of work
