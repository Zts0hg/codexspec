---
description: Review and validate a feature specification for completeness and quality
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

## Instructions

Review the feature specification for completeness, clarity, and consistency. This command helps ensure specifications are ready for planning.

### Steps

1. **Load Specification**: Read the spec from `.codexspec/specs/{feature-id}/spec.md`.

2. **Load Constitution**: Read `.codexspec/memory/constitution.md` for quality standards.

3. **Completeness Check**: Verify all required sections are present:
   - [ ] Feature overview
   - [ ] Goals
   - [ ] User stories with acceptance criteria
   - [ ] Functional requirements
   - [ ] Non-functional requirements
   - [ ] Edge cases
   - [ ] Constraints

4. **Clarity Check**: Ensure requirements are clear and unambiguous:
   - [ ] No vague language ("fast", "good", "user-friendly")
   - [ ] Specific, measurable criteria
   - [ ] Clear boundaries and scope

5. **Consistency Check**: Verify no contradictions:
   - [ ] Requirements don't conflict with each other
   - [ ] User stories align with goals
   - [ ] Constraints are realistic

6. **Constitution Alignment**: Check alignment with project principles:
   - [ ] Requirements support constitution goals
   - [ ] Quality standards are addressed
   - [ ] Workflow guidelines are followed

7. **Generate Report**: Create a review report.

### Report Template

```markdown
# Specification Review Report

## Summary
- **Specification**: {feature-id}
- **Status**: ✅ Pass / ⚠️ Needs Work / ❌ Fail
- **Overall Score**: X/100

## Completeness

| Section | Status | Notes |
|---------|--------|-------|
| Overview | ✅ | Present and clear |
| Goals | ✅ | 3 goals defined |
| User Stories | ⚠️ | Missing acceptance criteria for Story 2 |
| Functional Reqs | ✅ | 5 requirements defined |
| Non-Functional Reqs | ⚠️ | Missing performance requirements |
| Edge Cases | ❌ | Section not present |
| Constraints | ✅ | 2 constraints defined |

## Issues Found

### Critical
- [ ] Edge cases section is missing

### Warning
- [ ] User Story 2 lacks acceptance criteria
- [ ] Performance requirements not specified

### Suggestion
- [ ] Consider adding error handling requirements

## Recommendations

1. Add edge cases section with at least 3 scenarios
2. Complete acceptance criteria for all user stories
3. Add specific performance metrics (e.g., "response time < 200ms")
```

### Quality Criteria

- [ ] Report covers all aspects
- [ ] Issues are prioritized (Critical/Warning/Suggestion)
- [ ] Recommendations are actionable
- [ ] Score reflects actual quality

> [!NOTE]
> This is a placeholder command. The full implementation will be added in future versions.
