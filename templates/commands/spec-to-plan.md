---
description: Convert a feature specification into a technical implementation plan
argument-hint: ".codexspec/specs/{feature-id}/spec.md"
handoffs:
  - agent: claude
    step: Generate technical plan from specification
---

# Specification to Plan Converter

## Role Definition

You are now the **Chief Architect** of this project. Your responsibility is to transform business requirements into a solid, implementable technical plan that respects all architectural principles defined in the project's constitution.

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
   - Read `.codexspec/memory/constitution.md` for architectural guidelines
   - Scan the existing codebase to understand current patterns and conventions

2. **Define Tech Stack**
   Based on constitution, existing codebase, and user input, explicitly define:
   - Programming languages with version constraints
   - Frameworks and libraries
   - Database systems
   - Infrastructure requirements
   - Any existing tech stack constraints that must be followed

3. **Constitutionality Review** (MANDATORY)
   - Go through EACH principle in `constitution.md` one by one
   - Explicitly verify that the technical plan complies with each principle
   - Document any principles that influenced design decisions
   - If a principle conflicts with requirements, flag it for discussion

4. **Design Architecture**
   Create the system architecture including:
   - High-level component diagram (use ASCII or Mermaid)
   - Module/file structure with clear responsibilities
   - **Module dependency graph** - show which modules depend on which
   - API contracts
   - Data models
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
   Write to `.codexspec/specs/{feature-id}/plan.md` (same directory as spec.md)

### Module Structure Requirements

For each module/component in your plan, specify:
- **Responsibility**: What this module owns and does
- **Dependencies**: Which other modules it depends on
- **Interfaces**: What it exposes to other modules
- **Files**: Specific files to create or modify

### Reference Templates

Use the following templates as reference:

- **Detailed**: `.codexspec/templates/docs/plan-template-detailed.md` - Full format with tech stack, architecture, data models, API contracts, phases, and decisions
- **Simple**: `.codexspec/templates/docs/plan-template-simple.md` - Lightweight format for smaller features

Choose based on project complexity.

### Output Template Structure

```markdown
# Implementation Plan: [Feature Name]

## 1. Tech Stack

| Category | Technology | Version | Notes |
|----------|------------|---------|-------|
| Language | Python | ≥3.11 | |
| Framework | FastAPI | ^0.100 | |
| Database | PostgreSQL | 15 | |
| Frontend | React | 18 | TypeScript for new files |

## 2. Constitutionality Review

| Principle | Compliance | Notes |
|-----------|------------|-------|
| Package Cohesion | ✅ | Services grouped by domain |
| Error Handling | ✅ | Using custom exception classes |
| TDD | ✅ | Tests planned for each phase |
| ... | ... | ... |

## 3. Architecture Overview

[High-level description and diagram]

## 4. Component Structure

```
project/
├── src/
│   ├── api/           # REST endpoints
│   ├── models/        # Data models
│   ├── services/      # Business logic
│   └── repositories/  # Data access
└── tests/
```

## 5. Module Dependency Graph

```
┌─────────────┐
│    API      │
└──────┬──────┘
       │ depends on
       ▼
┌─────────────┐     ┌─────────────┐
│  Services   │────▶│ Repositories│
└─────────────┘     └──────┬──────┘
                           │
                           ▼
                    ┌─────────────┐
                    │   Models    │
                    └─────────────┘
```

## 6. Module Specifications

### Module: [Name]
- **Responsibility**: [What it does]
- **Dependencies**: [Other modules it uses]
- **Interface**: [What it exposes]
- **Files**: [Specific files]

## 7. Data Models

### [Model 1]
| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| id | UUID | Primary key | auto-generated |
| ... | ... | ... | ... |

## 8. API Contracts

### POST /api/endpoint
- **Request**: `{ field: type }`
- **Response**: `{ field: type }`
- **Errors**: 400, 401, 500

## 9. Implementation Phases

### Phase 1: Foundation
- [ ] Setup project structure
- [ ] Configure dependencies
- [ ] Create base models

### Phase 2: Core
- [ ] Implement repository layer
- [ ] Implement service layer
- [ ] Implement API endpoints

### Phase 3: Testing
- [ ] Unit tests for services
- [ ] Integration tests for API
- [ ] E2E tests

## 10. Technical Decisions

### Decision 1: [Title]
- **Choice**: [What was decided]
- **Rationale**: [Why this approach]
- **Alternatives**: [What else was considered]
- **Trade-offs**: [What we gave up]
```

### Quality Criteria

Before saving, verify:
- [ ] Tech stack is clearly defined with version constraints
- [ ] Constitutionality review is complete (all principles checked)
- [ ] Architecture has clear diagrams
- [ ] Module responsibilities are explicit
- [ ] Module dependencies are mapped
- [ ] Data models are complete with constraints
- [ ] API contracts specify request/response/error
- [ ] Implementation phases are logical and sequential
- [ ] Technical decisions have rationale

### Important Notes

> [!WARNING]
> Do NOT skip the Constitutionality Review. This ensures the plan aligns with established architectural principles and prevents technical debt accumulation.

> [!TIP]
> If the specification path is not provided, look for `spec.md` files in `.codexspec/specs/` and ask the user which one to use.
