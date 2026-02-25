---
description: Review and validate a feature specification for completeness, clarity, and quality
argument-hint: "[path_to_spec.md] (optional, defaults to .codexspec/specs/{feature-id}/)"
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

| Category | Weight | Score | Weighted |
|----------|--------|-------|----------|
| Completeness | 25% | X/100 | X |
| Clarity | 25% | X/100 | X |
| Consistency | 20% | X/100 | X |
| Testability | 20% | X/100 | X |
| Constitution Alignment | 10% | X/100 | X |
| **Total** | **100%** | | **X/100** |

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
- **Re-run Review**: `/codexspec.review-spec` - to verify changes after fixing issues
- **Proceed Anyway**: If you decide the warnings/suggestions are not critical or out of scope for the current iteration, you can proceed directly to `/codexspec.spec-to-plan`

### Next Steps Based on Review Result
- **Pass**: `/codexspec.spec-to-plan` - to proceed with technical implementation planning
- **Needs Work**: Fix the identified issues first, then re-run `/codexspec.review-spec` to verify, or proceed anyway if issues are acceptable
- **Fail**: `/codexspec.clarify` - to systematically identify and fix specification issues
```

### Quality Criteria

Before completing the review, verify:
- [ ] All sections of the spec have been examined
- [ ] Issues are categorized by severity (Critical/Warning/Suggestion)
- [ ] Each issue has a clear, actionable suggestion
- [ ] Score reflects actual quality accurately
- [ ] Recommendations are prioritized
- [ ] Next steps are clear and appropriate

### Output

Save the review report to: `.codexspec/specs/{feature-id}/review-spec.md`
