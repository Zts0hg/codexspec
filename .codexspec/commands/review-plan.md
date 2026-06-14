---
description: 审查和验证技术实现计划的可行性和一致性
argument-hint: "[plan.md 路径] (可选，默认为 .codexspec/specs/{feature-id}/)"
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

### Scoring Rubrics

Before scoring, apply these rubrics to ensure consistent, transparent evaluation.

#### Spec Alignment (30%)

| Score Range | Criteria |
|-------------|----------|
| 90-100 | All functional requirements, user stories, and NFRs have clear implementation coverage; edge cases addressed |
| 70-89 | Most requirements covered; 1-2 minor gaps in NFR or edge case coverage |
| 50-69 | Several requirements only partially covered; missing implementation for key user stories |
| Below 50 | Major requirements missing from plan; significant gaps between spec and plan |

**Typical Deductions**:

- Functional requirement with no implementation: -15 each
- User story without technical coverage: -10 each
- NFR not addressed in architecture: -8 each
- Edge case from spec not handled: -5 each

#### Tech Stack (15%)

| Score Range | Criteria |
|-------------|----------|
| 90-100 | All technologies clearly defined with versions; choices well-justified and appropriate for requirements |
| 70-89 | Tech stack defined; minor version gaps; mostly appropriate choices |
| 50-69 | Incomplete stack definition; some questionable technology choices |
| Below 50 | Vague or missing tech stack; inappropriate choices for requirements |

**Typical Deductions**:

- Technology without version constraint: -5 each
- Unjustified technology choice: -10 each
- Missing critical category (e.g., no testing framework): -10

#### Architecture Quality (25%)

| Score Range | Criteria |
|-------------|----------|
| 90-100 | Clear diagrams; well-defined module responsibilities; proper separation of concerns; dependency graph complete |
| 70-89 | Good architecture; minor gaps in documentation; mostly clear module boundaries |
| 50-69 | Architecture outlined but vague; unclear module responsibilities; missing dependency graph |
| Below 50 | No clear architecture; modules poorly defined; significant design issues |

**Typical Deductions**:

- Missing architecture diagram: -15
- Module without clear responsibility: -8 each
- Missing dependency graph: -10
- Tight coupling between modules: -8 each
- Missing separation of concerns: -10

#### Phase Planning (20%)

| Score Range | Criteria |
|-------------|----------|
| 90-100 | Phases logically ordered; clear deliverables per phase; realistic scope; minimal inter-phase dependencies |
| 70-89 | Good phasing; 1-2 phases with unclear deliverables or slightly large scope |
| 50-69 | Phase ordering has issues; several phases lack clear deliverables |
| Below 50 | No meaningful phase breakdown; deliverables unclear; unrealistic scope |

**Typical Deductions**:

- Phase without clear deliverables: -10 each
- Illogical phase ordering: -10
- Overly large phase scope: -5 each
- Missing phase dependencies: -5

#### Constitution Alignment (10%)

| Score Range | Criteria |
|-------------|----------|
| 90-100 | Fully aligned with all constitution principles; architecture principles followed; testing requirements addressed |
| 70-89 | Mostly aligned; minor gaps in addressing specific principles |
| 50-69 | Partial alignment; several principles not addressed |
| Below 50 | Significant violations or disregard of constitution |

> **Note**: If no constitution exists, this category defaults to 100 (full marks) and its weight is redistributed proportionally to other categories.

**Typical Deductions**:

- Constitution principle not addressed: -10 per principle
- Direct violation of a constitution principle: -20 per violation

#### Suggestion Score Cap Rule

**IMPORTANT**: Suggestions (Nice to Have) items may deduct a **maximum of 5 points** from the total score. After resolving all Critical Issues and Warnings, the score should be **≥ 95**.

- Critical Issues: -10 to -20 points each
- Warnings: -5 to -10 points each
- Suggestions: -1 to -2 points each, **capped at 5 points total**

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

| Category | Weight | Score | Rubric Basis | Deduction Details | Weighted |
|----------|--------|-------|-------------|-------------------|----------|
| Spec Alignment | 30% | X/100 | [Which rubric range applies] | [List specific deductions, e.g., "REQ-003 not addressed: -15"] | X |
| Tech Stack | 15% | X/100 | [Which rubric range applies] | [e.g., "No version for DB: -5"] | X |
| Architecture Quality | 25% | X/100 | [Which rubric range applies] | [e.g., "Missing dependency graph: -10"] | X |
| Phase Planning | 20% | X/100 | [Which rubric range applies] | [e.g., "Phase 2 scope too large: -5"] | X |
| Constitution Alignment | 10% | X/100 | [Which rubric range applies] | [e.g., "All principles addressed"] | X |
| **Total** | **100%** | | | | **X/100** |

> **Suggestion Cap**: Suggestions deducted X/5 points (cap: 5 points max)

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

### If Issues Found (Warnings or Suggestions)
- **Direct Fix**: Simply describe the changes you want to make (e.g., "Fix PLAN-001 and add the missing API endpoints") and I will update the plan accordingly
- **Re-run Review**: `/codexspec:review-plan` - to verify changes after fixing issues
- **Proceed Anyway**: If you decide the warnings/suggestions are not critical or out of scope for the current iteration, you can proceed directly to `/codexspec:plan-to-tasks`

### Next Steps Based on Review Result
- **Pass**: `/codexspec:plan-to-tasks` - to proceed with task breakdown
- **Needs Work**: Fix the identified issues first, then re-run `/codexspec:review-plan` to verify, or proceed anyway if issues are acceptable
- **Fail**: `/codexspec:spec-to-plan` - to regenerate the technical plan
```

### Score Validation Checklist

Before finalizing scores, the reviewer MUST verify:

- [ ] Every deduction in "Deduction Details" column has a corresponding issue in "Detailed Findings"
- [ ] The arithmetic is correct: each category score = 100 minus sum of deductions
- [ ] Weighted total = sum of (category score × weight) for all categories
- [ ] Suggestion deductions do not exceed 5-point cap
- [ ] No "phantom deductions" (deductions without matching issues)
- [ ] Score is consistent with Overall Status (Pass ≥ 80, Needs Work 50-79, Fail < 50)

### Score Challenge Response Protocol

When a user questions or challenges the score, follow this three-step process:

1. **Provide Evidence**: Present the complete scoring breakdown with all deduction details. Reference the specific rubric criteria and issue IDs that justify each deduction.

2. **Ask for Specifics**: Ask the user which specific scoring item(s) they believe are incorrect. Do NOT preemptively adjust any scores.

3. **Targeted Re-evaluation**: For each challenged item:
   - Re-read the relevant section of the plan
   - Re-apply the rubric criteria objectively
   - If the original score was correct: explain the reasoning and maintain the score
   - If the original score was indeed incorrect: adjust with clear explanation of what changed and why

> **CRITICAL**: Never adjust scores simply because the user expresses dissatisfaction. Only adjust when re-evaluation reveals a genuine scoring error.

### Quality Criteria

Before completing the review, verify:

- [ ] Every spec requirement is traced to plan elements
- [ ] Architecture is assessed for soundness
- [ ] Tech stack choices are evaluated
- [ ] Constitution alignment is checked
- [ ] Issues have clear, actionable suggestions
- [ ] Score reflects actual quality accurately (validated via Score Validation Checklist)
- [ ] Next steps are clear and appropriate

### Output

Save the review report to: `.codexspec/specs/{feature-id}/review-plan.md`
