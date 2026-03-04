# Quick Start

## 1. Initialize a Project

After installation, create or initialize your project:

```bash
# Create new project
codexspec init my-awesome-project

# Or initialize in current directory
codexspec init . --ai claude

# With Chinese output
codexspec init my-project --lang zh-CN
```

## 2. Establish Project Principles

Launch Claude Code in the project directory:

```bash
cd my-awesome-project
claude
```

Use the constitution command:

```
/codexspec.constitution Create principles focused on code quality and testing
```

## 3. Clarify Requirements

Use `/codexspec.specify` to explore requirements:

```
/codexspec.specify I want to build a task management application
```

## 4. Generate Specification

Once clarified, generate the spec document:

```
/codexspec.generate-spec
```

## 5. Review and Validate

**Recommended:** Validate before proceeding:

```
/codexspec.review-spec
```

## 6. Create Technical Plan

```
/codexspec.spec-to-plan Use Python FastAPI for backend
```

## 7. Generate Tasks

```
/codexspec.plan-to-tasks
```

## 8. Implement

```
/codexspec.implement-tasks
```

## Project Structure

After initialization:

```
my-project/
+-- .codexspec/
|   +-- memory/
|   |   +-- constitution.md
|   +-- specs/
|   |   +-- {feature-id}/
|   |       +-- spec.md
|   |       +-- plan.md
|   |       +-- tasks.md
|   +-- scripts/
+-- .claude/
|   +-- commands/
+-- CLAUDE.md
```

## Next Steps

[Full Workflow Guide](../user-guide/workflow.md)
