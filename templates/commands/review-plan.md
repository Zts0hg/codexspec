---
description: Review and validate a technical implementation plan
handoffs:
  - agent: claude
    step: Review plan against best practices and requirements
---

# Plan Reviewer

## User Input

$ARGUMENTS

## Instructions

Review the technical implementation plan for completeness, feasibility, and alignment with the specification and constitution.

### Steps

1. **Load Plan**: Read the plan from `.codexspec/specs/{feature-id}/plan.md`.

2. **Load Specification**: Read the spec from `.codexspec/specs/{feature-id}/spec.md`.

3. **Load Constitution**: Read `.codexspec/memory/constitution.md` for architectural guidelines.

4. **Alignment Check**: Verify plan aligns with specification:
   - [ ] All functional requirements are addressed
   - [ ] All user stories have corresponding implementation
   - [ ] Non-functional requirements are considered
   - [ ] Constraints are respected

5. **Feasibility Check**: Assess technical feasibility:
   - [ ] Tech stack choices are appropriate
   - [ ] Architecture is sound
   - [ ] Timeline estimates are realistic
   - [ ] Resources are adequate

6. **Architecture Review**: Check architectural decisions:
   - [ ] Follows separation of concerns
   - [ ] Scalability considered
   - [ ] Maintainability addressed
   - [ ] Security considered

7. **Constitution Alignment**: Check alignment with project principles:
   - [ ] Tech choices align with constitution
   - [ ] Quality standards addressed
   - [ ] Development workflow followed

8. **Generate Report**: Create a review report.

### Report Template

```markdown
# Plan Review Report

## Summary
- **Plan**: {feature-id}
- **Status**: ✅ Pass / ⚠️ Needs Work / ❌ Fail
- **Overall Score**: X/100

## Alignment with Specification

| Requirement | Covered | Implementation |
|-------------|---------|----------------|
| REQ-001 | ✅ | API endpoint POST /users |
| REQ-002 | ✅ | UserService.create() |
| REQ-003 | ⚠️ | Partially covered |
| REQ-004 | ❌ | Not addressed |

## Technical Feasibility

| Aspect | Assessment | Notes |
|--------|------------|-------|
| Tech Stack | ✅ | Well-suited for requirements |
| Architecture | ✅ | Clean separation of concerns |
| Data Models | ⚠️ | Missing audit fields |
| API Design | ✅ | RESTful and well-documented |

## Architecture Review

### Strengths
- Clear module separation
- Well-defined API contracts
- Proper error handling strategy

### Concerns
- No caching strategy defined
- Authentication approach unclear

## Issues Found

### Critical
- [ ] REQ-004 is not addressed in the plan

### Warning
- [ ] Data models missing audit fields (created_at, updated_at)
- [ ] No caching strategy for frequently accessed data

### Suggestion
- [ ] Consider adding API rate limiting
- [ ] Document database indexing strategy

## Recommendations

1. Add implementation for REQ-004
2. Include audit fields in all data models
3. Define caching strategy for performance
```

### Quality Criteria

- [ ] All requirements are checked for coverage
- [ ] Technical feasibility is assessed
- [ ] Architecture is reviewed
- [ ] Issues are prioritized
- [ ] Recommendations are actionable

> [!NOTE]
> This is a placeholder command. The full implementation will be added in future versions.
