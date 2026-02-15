---
description: Create or update the project constitution - the governing principles that guide all development decisions
handoffs:
  - agent: claude
    step: Analyze project context and generate constitution
---

# Project Constitution Generator

## User Input

$ARGUMENTS

## Instructions

You are tasked with creating or updating the project constitution. The constitution serves as the foundational document that guides all technical decisions and implementation choices throughout the project lifecycle.

### Steps

1. **Analyze the Request**: Understand the user's requirements for project principles, coding standards, and governance rules.

2. **Review Existing Context**: Check `.codexspec/memory/constitution.md` if it exists for current principles.

3. **Generate Constitution**: Create a comprehensive constitution document that includes:
   - Core development principles
   - Code quality standards
   - Testing requirements
   - Documentation guidelines
   - Architecture decisions
   - Performance requirements
   - Security considerations

4. **Save the Constitution**: Write the constitution to `.codexspec/memory/constitution.md`

### Output Format

The constitution should be structured as a markdown document with clear sections and actionable guidelines.

### Template Structure

```markdown
# Project Constitution

## Core Principles

### 1. [Principle Name]
- [Guideline 1]
- [Guideline 2]

### 2. [Principle Name]
...

## Development Workflow

1. [Step 1]
2. [Step 2]
...

## Decision Guidelines

When making technical decisions, prioritize:
1. [Priority 1]
2. [Priority 2]
...
```

### Quality Criteria

- [ ] All principles are clear and actionable
- [ ] Guidelines are specific and measurable
- [ ] Workflow steps are well-defined
- [ ] Decision priorities are established
- [ ] Constitution aligns with project goals

> [!NOTE]
> This is a placeholder command. The full implementation will be added in future versions.
