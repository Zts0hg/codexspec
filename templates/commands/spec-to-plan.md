---
description: Convert a feature specification into a technical implementation plan
handoffs:
  - agent: claude
    step: Generate technical plan from specification
---

# Specification to Plan Converter

## User Input

$ARGUMENTS

## Instructions

Convert the feature specification into a detailed technical implementation plan. This is where you define **how** the feature will be built.

### Steps

1. **Read Specification**: Load the specification from `.codexspec/specs/{feature-id}/spec.md`.

2. **Read Constitution**: Review `.codexspec/memory/constitution.md` for architectural guidelines.

3. **Define Tech Stack**: Based on user input and constitution, define:
   - Programming languages
   - Frameworks and libraries
   - Database systems
   - Infrastructure requirements

4. **Design Architecture**: Create the system architecture including:
   - High-level component diagram
   - Module/file structure
   - API contracts
   - Data models
   - Integration patterns

5. **Plan Implementation Phases**: Break down into logical phases:
   - Foundation/setup
   - Core functionality
   - Integration
   - Testing
   - Deployment

6. **Document Decisions**: Record key technical decisions and rationale.

7. **Save Plan**: Write to `.codexspec/specs/{feature-id}/plan.md`

### Reference Templates

Use the following templates as reference for generating the implementation plan:

- **Detailed**: `.codexspec/templates/docs/plan-template-detailed.md` - Full format with tech stack, architecture, data models, API contracts, phases, and decisions
- **Simple**: `.codexspec/templates/docs/plan-template-simple.md` - Lightweight format focused on design decisions and risk assessment

Choose the appropriate template based on project complexity.

### Template Structure

```markdown
# Implementation Plan: [Feature Name]

## Tech Stack
- **Language**: [e.g., Python 3.11]
- **Framework**: [e.g., FastAPI]
- **Database**: [e.g., PostgreSQL]
- **Frontend**: [e.g., React]

## Architecture Overview
[High-level architecture description]

## Component Structure
```
project/
├── src/
│   ├── api/
│   ├── models/
│   └── services/
└── tests/
```

## Data Models

### [Model 1]
| Field | Type | Description |
|-------|------|-------------|
| id | UUID | Primary key |
| ... | ... | ... |

## API Contracts

### POST /api/endpoint
- **Request**: [schema]
- **Response**: [schema]
- **Errors**: [list]

## Implementation Phases

### Phase 1: Foundation
- [ ] Setup project structure
- [ ] Configure dependencies
- [ ] Setup database

### Phase 2: Core
- [ ] Implement models
- [ ] Implement services
- [ ] Implement API endpoints

### Phase 3: Testing
- [ ] Unit tests
- [ ] Integration tests

## Technical Decisions
- **Decision 1**: [Description and rationale]
- **Decision 2**: [Description and rationale]
```

### Quality Criteria

- [ ] Tech stack is clearly defined
- [ ] Architecture is documented with diagrams
- [ ] Data models are complete
- [ ] API contracts are specified
- [ ] Implementation phases are logical
- [ ] Technical decisions have rationale

> [!NOTE]
> This is a placeholder command. The full implementation will be added in future versions.
