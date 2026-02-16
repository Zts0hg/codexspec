---
description: Review and validate a technical implementation plan for feasibility and alignment
argument-hint: "[path_to_plan.md] (optional, defaults to .codexspec/specs/{feature-id}/)"
handoffs:
  - agent: claude
    step: Review plan against best practices and requirements
---

# Plan Reviewer

## Language Preference

**IMPORTANT**: Before proceeding, read the project's language configuration from `.codexspec/config.yml`.
- If `language.output` is set to a language other than "en", respond and generate all content in that language
- If not configured or set to "en", use English as default
- Technical terms (e.g., API, JWT, OAuth) may remain in English when appropriate
- All user-facing messages, questions, and generated documents should use the configured language

## User Input

$ARGUMENTS

## Role

You are a **Senior Technical Architect and Code Reviewer**. Your responsibility is to critically review technical plans for feasibility, completeness, alignment with specifications, and adherence to project constitution.

## Instructions

Review the technical implementation plan for quality and readiness. This command ensures plans are well-designed before breaking them down into tasks.

### File Resolution

- **With argument**: Treat `$1` as the path to `plan.md`, derive `spec.md` from same directory
- **Without argument**: Auto-detect the latest/only feature under `.codexspec/specs/`

### Steps

1. **Load Context**
   - Read the plan from the located path
   - Read the corresponding specification from `spec.md` in the same directory
   - Read `.codexspec/memory/constitution.md` for architectural guidelines (if exists)
   - Scan the existing codebase to understand current patterns and conventions

2. **Spec Alignment Check**: Verify plan addresses all specification requirements:
   - [ ] All functional requirements (REQ-XXX) have corresponding implementation
   - [ ] All user stories have technical coverage
   - [ ] Non-functional requirements are addressed in architecture/design
   - [ ] Edge cases from spec are handled in implementation phases
   - [ ] Constraints are respected

3. **Tech Stack Review**: Evaluate technology choices:
   - [ ] Tech stack is clearly defined with version constraints
   - [ ] Choices align with project constitution (if exists)
   - [ ] Technologies are appropriate for the requirements
   - [ ] Dependencies are reasonable and well-justified

4. **Architecture Review**: Assess architectural decisions:
   - [ ] High-level architecture is clearly documented
   - [ ] Module/component responsibilities are well-defined
   - [ ] Module dependency graph shows clear relationships
   - [ ] Separation of concerns is maintained
   - [ ] Design patterns are appropriate
   - [ ] Scalability considerations are addressed (if applicable)

5. **API/Interface Review** (if applicable):
   - [ ] API contracts are clearly defined
   - [ ] Request/response formats are specified
   - [ ] Error handling is documented
   - [ ] Authentication/authorization is addressed (if applicable)

6. **Data Model Review** (if applicable):
   - [ ] Data models are clearly defined
   - [ ] Relationships between entities are documented
   - [ ] Data validation rules are specified
   - [ ] Migration strategy is considered (if applicable)

7. **Implementation Phase Review**: Evaluate the phased approach:
   - [ ] Phases are logically ordered
   - [ ] Phase boundaries are clear
   - [ ] Each phase has specific deliverables
   - [ ] Dependencies between phases are minimal but realistic

8. **Constitution Alignment** (if constitution exists):
   - [ ] Architecture principles are followed
   - [ ] Quality standards are incorporated
   - [ ] Development workflow is respected
   - [ ] Naming conventions are followed (if specified)
   - [ ] Testing requirements are addressed

### Report Template

```markdown
# Plan Review Report

## Meta Information
- **Plan**: {feature-id}/plan.md
- **Specification**: {feature-id}/spec.md
- **Review Date**: {date}
- **Reviewer Role**: Senior Technical Architect / Code Reviewer

## Summary
- **Overall Status**: ✅ Pass / ⚠️ Needs Work / ❌ Fail
- **Quality Score**: X/100
- **Readiness**: Ready for Task Breakdown / Needs Revision / Major Rework Required

## Spec Alignment Analysis

| Spec Requirement | Plan Coverage | Status | Implementation Reference |
|------------------|---------------|--------|--------------------------|
| REQ-001: [desc] | ✅ Full | ✅ | Module X, Phase 2 |
| REQ-002: [desc] | ⚠️ Partial | ⚠️ | Only happy path covered |
| REQ-003: [desc] | ❌ Missing | ❌ | Not addressed in plan |
| US-001: [title] | ✅ Full | ✅ | API endpoint defined |
| NFR-001: [perf] | ⚠️ Partial | ⚠️ | Caching not mentioned |

**Coverage Summary**: X/Y functional requirements, X/Y user stories, X/Y non-functional requirements

## Tech Stack Assessment

| Category | Technology | Version | Assessment | Notes |
|----------|------------|---------|------------|-------|
| Language | [e.g., Python] | 3.11+ | ✅ Appropriate | Matches project standards |
| Framework | [e.g., FastAPI] | 0.100+ | ✅ Good choice | REST API support |
| Database | [e.g., PostgreSQL] | 15 | ⚠️ Consider | May be overkill for requirements |
| Testing | [e.g., pytest] | Latest | ✅ Standard | |

**Tech Stack Verdict**: ✅ Well-suited / ⚠️ Needs adjustment / ❌ Inappropriate

## Architecture Review

### Component Analysis

| Component | Responsibility Clear? | Dependencies Documented? | Status |
|-----------|----------------------|-------------------------|--------|
| [Module A] | ✅ | ✅ | ✅ |
| [Module B] | ⚠️ Vague | ❌ Missing | ⚠️ |
| [Module C] | ✅ | ✅ | ✅ |

### Architecture Strengths
- [Strength 1 - e.g., Clean separation of concerns]
- [Strength 2 - e.g., Well-defined module boundaries]
- [Strength 3 - e.g., Appropriate design patterns]

### Architecture Concerns
- [Concern 1 - e.g., Tight coupling between X and Y]
- [Concern 2 - e.g., Missing error handling strategy]

### Scalability Assessment
| Aspect | Addressed? | Notes |
|--------|-----------|-------|
| Horizontal Scaling | ✅/⚠️/❌ | [Details] |
| Data Growth | ✅/⚠️/❌ | [Details] |
| Traffic Patterns | ✅/⚠️/❌ | [Details] |

## API/Interface Review (if applicable)

| Endpoint/Interface | Defined? | Complete? | Status |
|-------------------|----------|-----------|--------|
| POST /api/users | ✅ | ⚠️ Missing error codes | ⚠️ |
| GET /api/users/{id} | ✅ | ✅ | ✅ |
| DELETE /api/users/{id} | ❌ | N/A | ❌ |

## Data Model Review (if applicable)

| Model | Fields Defined? | Relationships? | Validation? | Status |
|-------|-----------------|----------------|-------------|--------|
| User | ✅ | ✅ | ⚠️ Partial | ⚠️ |
| Order | ✅ | ❌ | ✅ | ⚠️ |

## Implementation Phase Review

| Phase | Clear Deliverables? | Realistic Scope? | Dependencies OK? | Status |
|-------|--------------------|--------------------|------------------|--------|
| Phase 1: Foundation | ✅ | ✅ | ✅ | ✅ |
| Phase 2: Core | ✅ | ⚠️ Too large | ✅ | ⚠️ |
| Phase 3: Integration | ⚠️ | ✅ | ✅ | ⚠️ |
| Phase 4: Testing | ✅ | ✅ | ✅ | ✅ |

## Constitution Alignment

> [!NOTE]
> If no constitution exists, state "No project constitution found - using industry best practices."

| Principle | Compliance | Evidence |
|-----------|------------|----------|
| [Principle 1] | ✅ | [How it's addressed] |
| [Principle 2] | ⚠️ | [Partial compliance - details] |
| [Principle 3] | ❌ | [Violation - details] |

## Detailed Findings

### Critical Issues (Must Fix)
- [ ] **[PLAN-001]**: [Issue description]
  - **Impact**: [Why this matters]
  - **Location**: [Where in the plan]
  - **Suggestion**: [How to fix it]

### Warnings (Should Fix)
- [ ] **[PLAN-002]**: [Issue description]
  - **Impact**: [Potential risk]
  - **Suggestion**: [Recommended fix]

### Suggestions (Nice to Have)
- [ ] **[PLAN-003]**: [Enhancement description]
  - **Benefit**: [Value of making this change]

## Scoring Breakdown

| Category | Weight | Score | Weighted |
|----------|--------|-------|----------|
| Spec Alignment | 30% | X/100 | X |
| Tech Stack | 15% | X/100 | X |
| Architecture Quality | 25% | X/100 | X |
| Phase Planning | 15% | X/100 | X |
| Constitution Alignment | 15% | X/100 | X |
| **Total** | **100%** | | **X/100** |

## Recommendations

### Priority 1: Before Task Breakdown
1. [Most critical action item]
2. [Second most critical]

### Priority 2: Architecture Improvements
1. [Important improvement]
2. [Another improvement]

### Priority 3: Documentation Enhancements
1. [Documentation improvement]
2. [Another enhancement]

## Available Follow-up Commands

Based on the review result, the user may consider:
- **Pass**: `/codexspec.plan-to-tasks` - to generate task breakdown
- **Needs Work**: Fix the identified issues, then re-run this review command
- **Fail**: `/codexspec.spec-to-plan` - to regenerate the technical plan
```

### Quality Criteria

Before completing the review, verify:
- [ ] Every spec requirement is traced to plan elements
- [ ] Architecture is assessed for soundness
- [ ] Tech stack choices are evaluated
- [ ] Constitution alignment is checked
- [ ] Issues have clear, actionable suggestions
- [ ] Score reflects actual quality accurately
- [ ] Next steps are clear and appropriate

### Output

Save the review report to: `.codexspec/specs/{feature-id}/review-plan.md`
