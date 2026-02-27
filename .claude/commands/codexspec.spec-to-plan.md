---
description: Convert a feature specification into a technical implementation plan
argument-hint: ".codexspec/specs/{feature-id}/spec.md"
handoffs:
  - agent: claude
    step: Generate technical plan from specification
---

# Specification to Plan Converter

## Role Definition

You are now the **Chief Architect** of this project. Your responsibility is to transform business requirements into a solid, implementable technical plan. If the project has a constitution, ensure the plan respects all architectural principles defined therein.

## Language Preference

**IMPORTANT**: Before proceeding, read the project's language configuration from `.codexspec/config.yml`.
- If `language.output` is set to a language other than "en", respond and generate all content in that language
- If not configured or set to "en", use English as default
- Technical terms (e.g., API, JWT, OAuth) may remain in English when appropriate
- All user-facing messages, questions, and generated documents should use the configured language

## User Input

```
$ARGUMENTS
```

## Instructions

Transform the feature specification into a detailed technical implementation plan. This is where you define **how** the feature will be built.

### Execution Steps

1. **Load Context**
   - Read the specification from the path provided in `$ARGUMENTS` (or default to `.codexspec/specs/{feature-id}/spec.md`)
   - Read `.codexspec/memory/constitution.md` for architectural guidelines (if exists)
   - Scan the existing codebase to understand current patterns and conventions

2. **Define Tech Stack**
   Based on constitution (if exists), existing codebase, and user input, define what's relevant:
   - Programming languages with version constraints
   - Frameworks and libraries
   - Database systems (if applicable)
   - Infrastructure requirements (if applicable)
   - Any existing tech stack constraints that must be followed

3. **Constitutionality Review** (MANDATORY if constitution exists)
   - If `constitution.md` exists: Go through EACH principle one by one
   - Explicitly verify that the technical plan complies with each principle
   - Document any principles that influenced design decisions
   - If a principle conflicts with requirements, flag it for discussion
   - If no constitution exists, note this and proceed with general best practices

4. **Design Architecture**
   Create the system architecture including (adapt to project type):
   - High-level component diagram (use ASCII or Mermaid)
   - Module/file structure with clear responsibilities
   - **Module dependency graph** - show which modules depend on which
   - API contracts (if applicable - REST, GraphQL, RPC, CLI commands, etc.)
   - Data models (if applicable - database schemas, data structures, etc.)
   - Integration patterns

5. **Plan Implementation Phases**
   Break down into logical, sequential phases:
   - Phase 1: Foundation/Setup
   - Phase 2: Core functionality
   - Phase 3: Integration
   - Phase 4: Testing
   - Phase 5: Deployment (if applicable)

6. **Document Decisions**
   Record key technical decisions with:
   - The decision made
   - Why this approach was chosen
   - Alternatives considered (if any)
   - Trade-offs accepted

7. **Save Plan**
   - If spec path was provided: Write `plan.md` to the same directory as `spec.md`
   - If no path was provided: Write to `.codexspec/specs/{feature-id}/plan.md`
   - Ask user for confirmation on output path if uncertain

### Module Structure Requirements

For each module/component in your plan, specify:
- **Responsibility**: What this module owns and does
- **Dependencies**: Which other modules it depends on
- **Interfaces**: What it exposes to other modules
- **Files**: Specific files to create or modify

### Reference Templates

If available, use the following templates as reference:

- **Detailed**: `.codexspec/templates/docs/plan-template-detailed.md` - Full format with tech stack, architecture, data models, API contracts, phases, and decisions
- **Simple**: `.codexspec/templates/docs/plan-template-simple.md` - Lightweight format for smaller features

> [!NOTE]
> If these template files don't exist, use the "Output Template Structure" section below as your guide. Choose the complexity level based on feature scope.

### Project Type Considerations

Different project types require different plan structures. Adapt the template based on your project:

| Project Type | Key Sections | Optional Sections |
|--------------|--------------|-------------------|
| Web Backend | Tech Stack, API Contracts, Data Models, Architecture | UI Components |
| Web Frontend | Tech Stack, Components, State Management | API Contracts (if consuming only) |
| CLI Tool | Tech Stack, Commands, Core Logic | API Contracts, Data Models |
| Library/Package | Tech Stack, Public API, Core Modules | Implementation Phases |
| Mobile App | Tech Stack, Screens, State, API Client | Data Models (if remote only) |
| Data Pipeline | Tech Stack, Data Flow, Transformations | API Contracts |
| Full-Stack | All sections may apply | None |

> [!TIP]
> Include sections relevant to your project type. Omit or mark as N/A sections that don't apply.

### Output Template Structure

The following template shows a comprehensive structure. **Only include sections relevant to your project type.**

```markdown
# Implementation Plan: [Feature Name]

## 1. Tech Stack

| Category | Technology | Version | Notes |
|----------|------------|---------|-------|
| Language | [e.g., Python/JavaScript/Go/Rust] | [version] | |
| Framework | [e.g., FastAPI/Express/Django/React] | [version] | |
| Database | [e.g., PostgreSQL/MongoDB/None] | [version] | If applicable |
| [Other] | [e.g., Message Queue/Cache/etc.] | [version] | If applicable |

## 2. Constitutionality Review

> [!NOTE]
> If no constitution.md exists, state "No project constitution found" and proceed with industry best practices.

| Principle | Compliance | Notes |
|-----------|------------|-------|
| [Principle 1 from constitution] | ✅/⚠️/❌ | [How it's addressed] |
| [Principle 2 from constitution] | ✅/⚠️/❌ | [How it's addressed] |
| ... | ... | ... |

## 3. Architecture Overview

[High-level description and diagram - use ASCII or Mermaid]

## 4. Component Structure

[Adapt to your project type. Examples:]

<!-- For Web Backend: -->
```
project/
├── src/
│   ├── [module1]/      # [responsibility]
│   ├── [module2]/      # [responsibility]
│   └── [module3]/      # [responsibility]
└── tests/
```

<!-- For CLI Tool: -->
```
project/
├── src/
│   ├── commands/       # CLI command handlers
│   ├── core/           # Core business logic
│   └── utils/          # Utilities
└── tests/
```

<!-- For Frontend: -->
```
project/
├── src/
│   ├── components/     # Reusable UI components
│   ├── pages/          # Page-level components
│   ├── hooks/          # Custom hooks
│   └── utils/          # Utilities
└── tests/
```

## 5. Module Dependency Graph

[Show how modules relate to each other. Example format:]

```
┌─────────────┐
│  [Module A] │
└──────┬──────┘
       │ depends on
       ▼
┌─────────────┐     ┌─────────────┐
│  [Module B] │────▶│  [Module C] │
└─────────────┘     └─────────────┘
```

## 6. Module Specifications

### Module: [Name]
- **Responsibility**: [What this module owns and does]
- **Dependencies**: [Which other modules it depends on]
- **Interface**: [What it exposes to other modules]
- **Files**: [Specific files to create or modify]

## 7. Data Models (if applicable)

> [!NOTE]
> Omit this section for projects without persistent data (e.g., pure utilities, stateless functions).

### [Model 1]
| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| [field] | [type] | [description] | [constraints] |

## 8. API Contracts (if applicable)

> [!NOTE]
> Include this section for projects that expose APIs (REST, GraphQL, RPC) or consume external APIs.

### [HTTP Method] /api/[endpoint]
- **Request**: `{ field: type }`
- **Response**: `{ field: type }`
- **Errors**: [list possible error codes]

<!-- Or for CLI: -->

### Command: `[command-name]`
- **Arguments**: `[args]`
- **Options**: `[options]`
- **Output**: `[expected output]`
- **Exit Codes**: `[codes and meanings]`

## 9. Implementation Phases

### Phase 1: Foundation
- [ ] [Task specific to your project]
- [ ] [Task specific to your project]

### Phase 2: Core Implementation
- [ ] [Task specific to your project]
- [ ] [Task specific to your project]

### Phase 3: Integration (if applicable)
- [ ] [Integration tasks]

### Phase 4: Testing
- [ ] [Test type relevant to your project]

### Phase 5: Deployment (if applicable)
- [ ] [Deployment tasks]

## 10. Technical Decisions

### Decision 1: [Title]
- **Choice**: [What was decided]
- **Rationale**: [Why this approach]
- **Alternatives**: [What else was considered]
- **Trade-offs**: [What we gave up]
```

### Quality Criteria

Before saving, verify:
- [ ] Tech stack is clearly defined with version constraints (only relevant categories)
- [ ] Constitutionality review is complete (if constitution exists) or noted as absent
- [ ] Architecture has clear diagrams
- [ ] Module responsibilities are explicit
- [ ] Module dependencies are mapped
- [ ] **Relevant sections included** based on project type (omit inapplicable sections like Data Models/API Contracts for relevant projects)
- [ ] Implementation phases are logical and sequential
- [ ] Technical decisions have rationale
- [ ] Plan is self-contained and can be understood without external context

### Important Notes

> [!WARNING]
> If a project constitution exists, do NOT skip the Constitutionality Review. This ensures the plan aligns with established architectural principles and prevents technical debt accumulation.

> [!TIP]
> If the specification path is not provided, look for `spec.md` files in `.codexspec/specs/` and ask the user which one to use.

## Available Follow-up Commands

After generating the technical plan, the user may consider:
- `/codexspec.review-plan` - to validate the plan quality before task breakdown
- `/codexspec.plan-to-tasks` - to proceed directly with breaking down into actionable tasks
