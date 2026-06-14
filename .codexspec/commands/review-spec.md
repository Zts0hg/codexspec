---
description: 审查和验证功能规格的完整性、清晰度和质量
argument-hint: "[spec.md 路径] (可选，默认为 .codexspec/specs/{feature-id}/)"
handoffs:
  - agent: claude
    step: Review specification against quality criteria
---

# Specification Reviewer

## Language Preference

**IMPORTANT**: Before proceeding, read the project's language configuration from `.codexspec/config.yml`.

- If `language.output` is set to a language other than "en", respond and generate all content in that language
- If not configured or set to "en", use English as default
- Technical terms (e.g., API, JWT, OAuth) may remain in English when appropriate
- All user-facing messages, questions, and generated documents should use the configured language

## User Input

$ARGUMENTS

## Role

You are a **Senior Product Manager and Business Analyst**. Your responsibility is to critically review specifications for completeness, clarity, consistency, and readiness for technical planning.

## Instructions

Review the feature specification for quality and readiness. This command ensures specifications are well-defined before investing time in technical planning.

### File Resolution

- **With argument**: Treat `$1` as the path to `spec.md`
- **Without argument**: Auto-detect the latest/only feature under `.codexspec/specs/`

### Steps

1. **Load Context**
   - Read the specification from the located path
   - Read `.codexspec/memory/constitution.md` for project quality standards (if exists)
   - Check for existing specs in `.codexspec/specs/` to identify potential overlaps or conflicts

2. **Completeness Check**: Verify all required sections are present and substantive:
   - [ ] **Feature Overview**: Clear description of what is being built
   - [ ] **Goals**: Measurable objectives (at least 2-3)
   - [ ] **User Stories**: Complete with "As a/I want/So that" format
   - [ ] **Acceptance Criteria**: Each user story has specific, testable criteria
   - [ ] **Functional Requirements**: Numbered and specific (REQ-XXX format)
   - [ ] **Non-Functional Requirements**: Measurable (e.g., "< 200ms response time")
   - [ ] **Edge Cases**: Identified with handling approaches
   - [ ] **Out of Scope**: Clear boundaries defined

3. **Clarity Check**: Ensure requirements are unambiguous:
   - [ ] No vague language ("fast", "good", "user-friendly", "scalable" without metrics)
   - [ ] Each requirement has a single, clear interpretation
   - [ ] Technical terms are defined or linked to documentation
   - [ ] User roles and personas are clearly defined
   - [ ] Input/output formats are specified where applicable

4. **Consistency Check**: Verify no internal contradictions:
   - [ ] Requirements don't conflict with each other
   - [ ] User stories align with stated goals
   - [ ] Non-functional requirements don't contradict functional requirements
   - [ ] Scope boundaries are consistent with goals

5. **Testability Check**: Verify requirements can be verified:
   - [ ] Each functional requirement can be tested
   - [ ] Acceptance criteria are concrete and executable
   - [ ] Edge cases have expected behaviors defined
   - [ ] Error conditions have specified responses

6. **Constitution Alignment** (if constitution exists):
   - [ ] Requirements support constitution's project goals
   - [ ] Quality standards are addressed
   - [ ] Naming conventions are followed (if specified)
   - [ ] Workflow guidelines are considered

### Scoring Rubrics

Before scoring, apply these rubrics to ensure consistent, transparent evaluation.

#### Completeness (25%)

| Score Range | Criteria |
|-------------|----------|
| 90-100 | All 8 required sections present with substantive content; each section has concrete, specific details |
| 70-89 | 6-7 sections present and substantive; 1-2 sections thin but present |
| 50-69 | 4-5 sections present; several sections missing or placeholder-only |
| Below 50 | Fewer than 4 sections; major gaps in coverage |

**Typical Deductions**:

- Missing required section entirely: -15 per section
- Section present but placeholder/stub only: -8 per section
- Section present but lacks specificity: -5 per section

#### Clarity (25%)

| Score Range | Criteria |
|-------------|----------|
| 90-100 | No vague language; all requirements have single clear interpretation; technical terms defined |
| 70-89 | Minor ambiguities (1-2 vague terms); mostly precise language |
| 50-69 | Multiple ambiguities; several terms undefined; some requirements open to interpretation |
| Below 50 | Pervasive vagueness; most requirements unclear or multi-interpretable |

**Typical Deductions**:

- Vague term without metrics (e.g., "fast", "user-friendly"): -5 each
- Requirement with multiple interpretations: -8 each
- Undefined technical term or acronym: -3 each

#### Consistency (20%)

| Score Range | Criteria |
|-------------|----------|
| 90-100 | No internal contradictions; all sections align perfectly; scope boundaries match goals |
| 70-89 | Minor inconsistencies (1-2); easily resolved without major impact |
| 50-69 | Several inconsistencies between sections; conflicting requirements present |
| Below 50 | Major contradictions; requirements fundamentally conflict with goals or each other |

**Typical Deductions**:

- Direct contradiction between requirements: -15 each
- Scope boundary inconsistent with goals: -10
- Minor misalignment between sections: -5 each

#### Testability (20%)

| Score Range | Criteria |
|-------------|----------|
| 90-100 | All requirements testable; acceptance criteria concrete and executable; edge cases have expected behaviors |
| 70-89 | Most requirements testable; 1-2 criteria need more specificity |
| 50-69 | Several requirements lack testable criteria; edge cases missing expected behaviors |
| Below 50 | Most requirements not verifiable; no concrete acceptance criteria |

**Typical Deductions**:

- Requirement without testable acceptance criteria: -8 each
- Edge case without expected behavior: -5 each
- Non-measurable NFR (e.g., "should be scalable" without metrics): -8 each

#### Constitution Alignment (10%)

| Score Range | Criteria |
|-------------|----------|
| 90-100 | Fully aligned with all constitution principles; quality standards addressed |
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
# Specification Review Report

## Meta Information
- **Specification**: {feature-id}/spec.md
- **Review Date**: {date}
- **Reviewer Role**: Senior Product Manager / Business Analyst

## Summary
- **Overall Status**: ✅ Pass / ⚠️ Needs Work / ❌ Fail
- **Quality Score**: X/100
- **Readiness**: Ready for Planning / Needs Revision / Major Rework Required

## Section Analysis

| Section | Status | Completeness | Quality | Notes |
|---------|--------|--------------|---------|-------|
| Overview | ✅/⚠️/❌ | 100% | High/Medium/Low | [Specific feedback] |
| Goals | ✅/⚠️/❌ | 100% | High/Medium/Low | [Specific feedback] |
| User Stories | ✅/⚠️/❌ | 80% | Medium | [Specific feedback] |
| Acceptance Criteria | ✅/⚠️/❌ | 60% | Low | [Specific feedback] |
| Functional Requirements | ✅/⚠️/❌ | 100% | High | [Specific feedback] |
| Non-Functional Requirements | ✅/⚠️/❌ | 50% | Medium | [Specific feedback] |
| Edge Cases | ✅/⚠️/❌ | 0% | N/A | [Section missing] |
| Out of Scope | ✅/⚠️/❌ | 100% | High | [Specific feedback] |

## Detailed Findings

### Critical Issues (Must Fix)
- [ ] **[SPEC-001]**: [Issue description with specific location]
  - **Impact**: [Why this matters]
  - **Suggestion**: [How to fix it]

### Warnings (Should Fix)
- [ ] **[SPEC-002]**: [Issue description]
  - **Impact**: [Potential risk]
  - **Suggestion**: [Recommended fix]

### Suggestions (Nice to Have)
- [ ] **[SPEC-003]**: [Enhancement description]
  - **Benefit**: [Value of making this change]

## Clarity Assessment

| Aspect | Rating | Notes |
|--------|--------|-------|
| Ambiguity Level | Low/Medium/High | [Examples of vague terms if any] |
| Technical Precision | High/Medium/Low | [Areas needing clarification] |
| Stakeholder Readability | High/Medium/Low | [Jargon that may need explanation] |

## Testability Assessment

| Requirement | Testable? | Notes |
|-------------|-----------|-------|
| REQ-001 | ✅ | Clear test case possible |
| REQ-002 | ⚠️ | Needs more specific acceptance criteria |
| REQ-003 | ❌ | Cannot verify without metrics |

## Constitution Alignment

> [!NOTE]
> If no constitution exists, state "No project constitution found - using general best practices."

| Principle | Alignment | Notes |
|-----------|-----------|-------|
| [Principle 1] | ✅/⚠️/❌ | [How spec aligns or conflicts] |
| [Principle 2] | ✅/⚠️/❌ | [How spec aligns or conflicts] |

## Scoring Breakdown

| Category | Weight | Score | Rubric Basis | Deduction Details | Weighted |
|----------|--------|-------|-------------|-------------------|----------|
| Completeness | 25% | X/100 | [Which rubric range applies] | [List specific deductions, e.g., "Missing Edge Cases section: -15"] | X |
| Clarity | 25% | X/100 | [Which rubric range applies] | [e.g., "2 vague terms: -10"] | X |
| Consistency | 20% | X/100 | [Which rubric range applies] | [e.g., "No contradictions found"] | X |
| Testability | 20% | X/100 | [Which rubric range applies] | [e.g., "REQ-003 not testable: -8"] | X |
| Constitution Alignment | 10% | X/100 | [Which rubric range applies] | [e.g., "All principles addressed"] | X |
| **Total** | **100%** | | | | **X/100** |

> **Suggestion Cap**: Suggestions deducted X/5 points (cap: 5 points max)

## Recommendations

### Priority 1: Before Planning
1. [Most critical action item]
2. [Second most critical]

### Priority 2: Quality Improvements
1. [Important improvement]
2. [Another improvement]

### Priority 3: Future Considerations
1. [Nice-to-have enhancement]

## Available Follow-up Commands

Based on the review result, the user may consider:

### If Issues Found (Warnings or Suggestions)
- **Direct Fix**: Simply describe the changes you want to make (e.g., "Fix SPEC-001 and update the acceptance criteria") and I will update the specification accordingly
- **Re-run Review**: `/codexspec:review-spec` - to verify changes after fixing issues
- **Proceed Anyway**: If you decide the warnings/suggestions are not critical or out of scope for the current iteration, you can proceed directly to `/codexspec:spec-to-plan`

### Next Steps Based on Review Result
- **Pass**: `/codexspec:spec-to-plan` - to proceed with technical implementation planning
- **Needs Work**: Fix the identified issues first, then re-run `/codexspec:review-spec` to verify, or proceed anyway if issues are acceptable
- **Fail**: `/codexspec:clarify` - to systematically identify and fix specification issues
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
   - Re-read the relevant section of the specification
   - Re-apply the rubric criteria objectively
   - If the original score was correct: explain the reasoning and maintain the score
   - If the original score was indeed incorrect: adjust with clear explanation of what changed and why

> **CRITICAL**: Never adjust scores simply because the user expresses dissatisfaction. Only adjust when re-evaluation reveals a genuine scoring error.

### Quality Criteria

Before completing the review, verify:

- [ ] All sections of the spec have been examined
- [ ] Issues are categorized by severity (Critical/Warning/Suggestion)
- [ ] Each issue has a clear, actionable suggestion
- [ ] Score reflects actual quality accurately (validated via Score Validation Checklist)
- [ ] Recommendations are prioritized
- [ ] Next steps are clear and appropriate

### Output

Save the review report to: `.codexspec/specs/{feature-id}/review-spec.md`
