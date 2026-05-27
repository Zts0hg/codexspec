# AGENTS.md - codexspec Guidelines

> **IMPORTANT**: Before making any decisions, read the project constitution at
> `.codexspec/memory/constitution.md`. All code changes and decisions must comply
> with the principles defined there.

## Project Overview

This project uses the **CodexSpec** methodology - a Spec-Driven Development (SDD)
approach that emphasizes specifications as executable artifacts that directly guide
implementation.

CodexSpec skills are installed in `.codex/skills/`. Use `/skills` to inspect
available skills, or ask Codex to use `codexspec-specify`, `codexspec-quick`,
and the other installed CodexSpec skills.

## Available SDD Workflow

The following workflow steps are available in this project. Each step produces
artifacts in the `.codexspec/specs/` directory:

### Core Workflow

1. **Establish Principles**: Edit `.codexspec/memory/constitution.md` to define project guidelines
2. **Clarify Requirements**: Explore what you want to build through interactive Q&A
3. **Generate Specification**: Write detailed requirements in `.codexspec/specs/{feature}/spec.md`
4. **Create Technical Plan**: Write implementation plan in `.codexspec/specs/{feature}/plan.md`
5. **Break Down Tasks**: Create task breakdown in `.codexspec/specs/{feature}/tasks.md`
6. **Implement**: Execute tasks according to the breakdown
7. **Review**: Validate code against spec and constitution

### Review & Quality

- **Review Spec**: Check specification for completeness and quality
- **Review Plan**: Check technical plan for feasibility
- **Review Tasks**: Check task breakdown for completeness
- **Analyze**: Cross-artifact consistency and quality analysis
- **Checklist**: Generate quality checklists for requirements validation

## Recommended Workflow

1. Start by reading the constitution at `.codexspec/memory/constitution.md`
2. Create a feature directory: `.codexspec/specs/{timestamp}-{feature-name}/`
3. Write `spec.md` — focus on **what** and **why**
4. Write `plan.md` — focus on **how** (technical design)
5. Write `tasks.md` — break down into atomic, ordered tasks
6. Implement tasks in order, writing tests first

## Directory Structure

```
.codex/
└── skills/
    ├── codexspec-specify/ # CodexSpec reusable skills
    └── codexspec-quick/

.codexspec/
├── memory/
│   └── constitution.md    # Project governing principles
├── specs/
│   └── {feature-id}/
│       ├── spec.md        # Feature specification
│       ├── plan.md        # Technical implementation plan
│       ├── tasks.md       # Task breakdown
│       └── checklists/    # Quality checklists
├── templates/             # Custom templates
├── scripts/               # Helper scripts
└── config.yml             # Project configuration
```

## Important Notes

- Always read the constitution before making decisions
- Specifications focus on **what** and **why**, not **how**
- Plans focus on **how** and technical choices
- Tasks should be specific, ordered, and actionable

## Guidelines

1. **Constitution First**: Read `.codexspec/memory/constitution.md` before ANY action
2. **Respect the Constitution**: All decisions MUST align with the project constitution
3. **Follow the Workflow**: Use the SDD workflow in the recommended order
4. **Be Explicit**: When specifications are unclear, ask for clarification
5. **Validate**: Always review artifacts before implementation
6. **Document**: Keep all artifacts up-to-date

---

*This file is maintained by CodexSpec. Manual edits should be made with care.*
