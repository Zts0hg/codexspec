---
description: Review and validate task breakdown for completeness, ordering, and TDD compliance
argument-hint: "[path_to_tasks.md] (optional, defaults to .codexspec/specs/{feature-id}/)"
handoffs:
  - agent: claude
    step: Review tasks against plan and dependencies
---

# Tasks Reviewer

## Language Preference

**IMPORTANT**: Before proceeding, read the project's language configuration from `.codexspec/config.yml`.
- If `language.output` is set to a language other than "en", respond and generate all content in that language
- If not configured or set to "en", use English as default
- Technical terms (e.g., API, JWT, OAuth) may remain in English when appropriate
- All user-facing messages, questions, and generated documents should use the configured language

## User Input

$ARGUMENTS

## Role

You are a **Technical Lead and Project Manager**. Your responsibility is to critically review task breakdowns for completeness, correct ordering, proper dependency management, and TDD compliance.

## Instructions

Review the task breakdown for quality and implementation readiness. This command ensures tasks are well-defined and properly ordered before execution.

### File Resolution

- **With argument**: Treat `$1` as the path to `tasks.md`, derive `plan.md` and `spec.md` from same directory
- **Without argument**: Auto-detect the latest/only feature under `.codexspec/specs/`

### Steps

1. **Load Context**
   - Read the tasks from the located path
   - Read the corresponding plan from `plan.md` in the same directory
   - Read the corresponding spec from `spec.md` in the same directory
   - Read `.codexspec/memory/constitution.md` for workflow requirements (if exists)

2. **Plan Coverage Check**: Verify all plan items have task coverage:
   - [ ] All implementation phases have corresponding tasks
   - [ ] All modules/components have creation tasks
   - [ ] All API endpoints have implementation tasks
   - [ ] All data models have implementation tasks
   - [ ] Testing tasks are included (per constitution TDD requirements)

3. **TDD Compliance Check**: Verify test-first workflow is enforced:
   - [ ] Test tasks precede implementation tasks for each component
   - [ ] Each code module has corresponding test file task
   - [ ] Test tasks are not skipped or optional
   - [ ] Integration tests are included where appropriate

4. **Task Granularity Check**: Verify tasks are atomic:
   - [ ] Each task involves only ONE primary file (atomic focus)
   - [ ] Task scope is appropriate (not too broad, not too narrow)
   - [ ] Tasks have clear, single deliverable
   - [ ] Complexity estimates are reasonable

5. **Dependency Validation**: Check task dependencies are correct:
   - [ ] Dependencies are correctly identified
   - [ ] No circular dependencies exist
   - [ ] Dependencies are minimal but sufficient
   - [ ] Dependency chain is verifiable (can trace from first to last task)

6. **Ordering Verification**: Check task execution order:
   - [ ] Setup/foundation tasks come first
   - [ ] Dependencies execute before dependents
   - [ ] Documentation tasks come after implementation
   - [ ] Checkpoints are defined at phase boundaries

7. **Parallelization Review**: Check parallel execution markers:
   - [ ] Truly independent tasks are marked parallelizable with `[P]`
   - [ ] Dependent tasks are NOT marked parallel
   - [ ] Parallel markers are consistent with dependencies
   - [ ] Parallel execution opportunities are identified

8. **File Path Validation**: Check file specifications:
   - [ ] All tasks have file paths specified
   - [ ] File paths follow project structure
   - [ ] File paths are consistent with plan
   - [ ] File naming conventions are followed (per constitution)

### Report Template

```markdown
# Tasks Review Report

## Meta Information
- **Tasks File**: {feature-id}/tasks.md
- **Plan File**: {feature-id}/plan.md
- **Spec File**: {feature-id}/spec.md
- **Review Date**: {date}
- **Reviewer Role**: Technical Lead / Project Manager

## Summary
- **Overall Status**: ✅ Pass / ⚠️ Needs Work / ❌ Fail
- **Quality Score**: X/100
- **Readiness**: Ready for Implementation / Needs Revision / Major Rework Required
- **Total Tasks**: X
- **Parallelizable Tasks**: Y (Z%)

## Plan Coverage Analysis

| Plan Phase | Tasks Created | Coverage | Notes |
|------------|--------------|----------|-------|
| Phase 1: Foundation | Tasks 1.1-1.4 | ✅ 100% | All items covered |
| Phase 2: Core | Tasks 2.1-2.6 | ⚠️ 85% | Missing validation |
| Phase 3: Integration | Tasks 3.1-3.2 | ✅ 100% | Complete |
| Phase 4: Interface | Tasks 4.1-4.2 | ✅ 100% | Complete |
| Phase 5: Testing | Tasks 5.1-5.3 | ⚠️ 70% | Missing E2E tests |

| Plan Component | Task Coverage | Status | Task Reference |
|----------------|--------------|--------|----------------|
| Module A | ✅ Full | ✅ | Tasks 2.1, 2.2 |
| Module B | ✅ Full | ✅ | Tasks 2.3, 2.4 |
| API Endpoint X | ⚠️ Partial | ⚠️ | Missing error handling |
| Data Model Y | ❌ Missing | ❌ | No task found |

**Coverage Summary**: X/Y plan items have task coverage

## TDD Compliance Check

| Component | Test Task Exists? | Test Before Impl? | Status |
|-----------|------------------|-------------------|--------|
| Module A | ✅ Task 2.1 | ✅ | ✅ |
| Module B | ✅ Task 2.3 | ✅ | ✅ |
| Module C | ❌ Missing | N/A | ❌ |
| Service X | ✅ Task 3.1 | ❌ Wrong order | ⚠️ |

**TDD Compliance Rate**: X% (Y/Z components follow TDD)

### TDD Violations
- [ ] **[TDD-001]**: Task 3.2 (Implement Service X) should have test task 3.1 before it
- [ ] **[TDD-002]**: Module C missing test task entirely

## Task Granularity Analysis

| Task | Single File? | Scope Appropriate? | Status |
|------|--------------|-------------------|--------|
| 1.1 Setup | ✅ | ✅ | ✅ |
| 2.1 Test Module A | ✅ | ✅ | ✅ |
| 2.2 Implement Module A | ✅ | ✅ | ✅ |
| 2.5 Implement All Models | ❌ Multiple files | ⚠️ | ⚠️ |

### Overly Broad Tasks
- [ ] **[GRAN-001]**: Task 2.5 involves 3 files - should be split

### Overly Narrow Tasks
- [ ] **[GRAN-002]**: Task 3.1 could be combined with 3.2

## Dependency Validation

### Dependency Graph Analysis

```
Valid Dependency Chain:
1.1 ──► 1.2 ──► 2.1 ──► 2.2 ──► 3.1 ──► 3.2
                │
                └──► 2.3 ──► 2.4 ──► 3.2
```

| Task | Declared Dependencies | Correct? | Circular? | Status |
|------|----------------------|----------|-----------|--------|
| 1.1 | None | ✅ | No | ✅ |
| 1.2 | 1.1 | ✅ | No | ✅ |
| 2.1 | 1.1 | ✅ | No | ✅ |
| 2.2 | 2.1 | ✅ | No | ✅ |
| 2.3 | 2.2, 1.2 | ⚠️ Missing 1.2 | No | ⚠️ |
| 3.1 | 2.4 | ✅ | No | ✅ |

### Dependency Issues
- [ ] **[DEP-001]**: Task 2.3 missing dependency on Task 1.2
- [ ] **[DEP-002]**: Potential circular: Task X → Task Y → Task X

## Ordering Verification

| Check | Status | Notes |
|-------|--------|-------|
| Foundation first | ✅ | Phase 1 before all others |
| Dependencies respected | ✅ | All deps execute first |
| Docs after impl | ✅ | Phase 5 is last |
| Checkpoints defined | ✅ | 5 checkpoints present |

### Ordering Issues
- [ ] **[ORD-001]**: Task 3.2 runs before test task 3.1

## Parallelization Review

| Task | Marked [P]? | Actually Independent? | Correct? |
|------|-------------|----------------------|----------|
| 1.1 | No | No (root) | ✅ |
| 1.2 | Yes | Yes | ✅ |
| 1.3 | Yes | Yes | ✅ |
| 2.1 | Yes | No (depends on 1.3) | ❌ Incorrect marker |
| 2.3 | No | Yes (independent of 2.2) | ⚠️ Should be [P] |

### Parallelization Issues
- [ ] **[PAR-001]**: Task 2.1 marked [P] but depends on 1.3
- [ ] **[PAR-002]**: Task 2.3 should be marked [P] - runs parallel with 2.4

## File Path Validation

| Task | File Path Specified? | Follows Convention? | Status |
|------|---------------------|--------------------| -------|
| 1.1 | ✅ | ✅ | ✅ |
| 2.1 | ✅ | ⚠️ Wrong naming | ⚠️ |
| 3.1 | ❌ Missing | N/A | ❌ |

### File Path Issues
- [ ] **[FILE-001]**: Task 2.1 file path doesn't match project naming convention
- [ ] **[FILE-002]**: Task 3.1 missing file path specification

## Detailed Findings

### Critical Issues (Must Fix)
- [ ] **[TASK-001]**: [Issue description]
  - **Impact**: [Why this matters]
  - **Location**: [Task X.X]
  - **Suggestion**: [How to fix it]

### Warnings (Should Fix)
- [ ] **[TASK-002]**: [Issue description]
  - **Impact**: [Potential risk]
  - **Suggestion**: [Recommended fix]

### Suggestions (Nice to Have)
- [ ] **[TASK-003]**: [Enhancement description]
  - **Benefit**: [Value of making this change]

## Scoring Breakdown

| Category | Weight | Score | Weighted |
|----------|--------|-------|----------|
| Plan Coverage | 30% | X/100 | X |
| TDD Compliance | 25% | X/100 | X |
| Dependency & Ordering | 20% | X/100 | X |
| Task Granularity | 15% | X/100 | X |
| Parallelization & Files | 10% | X/100 | X |
| **Total** | **100%** | | **X/100** |

## Execution Timeline Estimate

```
Phase 1: Task 1.1 ──► [1.2 || 1.3 || 1.4] (parallel)
                           │
Phase 2: ┌──────────────────┴──────────────────┐
         │                                      │
    Task 2.1 ──► 2.2                    Task 2.3 ──► 2.4
         │                                      │
    Task 2.5                                    Task 2.6
         │                                      │
         └──────────────────┬───────────────────┘
                            │
Phase 3: ┌──────────────────┼──────────────────┐
         │                  │                  │
    Task 3.1           Task 3.2 [P]      Task 3.3 [P]
         │
Phase 4: Task 4.1 ──► 4.2
         │
Phase 5: [5.1 || 5.2 || 5.3] (parallel)
```

## Recommendations

### Priority 1: Before Implementation
1. [Most critical action item]
2. [Second most critical]

### Priority 2: Quality Improvements
1. [Important improvement]
2. [Another improvement]

### Priority 3: Optimization
1. [Nice-to-have enhancement]
2. [Another optimization]

## Available Follow-up Commands

Based on the review result, the user may consider:

### If Issues Found (Warnings or Suggestions)
- **Direct Fix**: Simply describe the changes you want to make (e.g., "Fix TASK-001 and split Task 2.5 into smaller tasks") and I will update the tasks accordingly
- **Re-run Review**: `/codexspec.review-tasks` - to verify changes after fixing issues
- **Proceed Anyway**: If you decide the warnings/suggestions are not critical or out of scope for the current iteration, you can proceed directly to `/codexspec.implement-tasks`

### Next Steps Based on Review Result
- **Pass**: `/codexspec.implement-tasks` - to begin implementation
- **Needs Work**: Fix the identified issues first, then re-run `/codexspec.review-tasks` to verify, or proceed anyway if issues are acceptable
- **Fail**: `/codexspec.plan-to-tasks` - to regenerate the task breakdown
```

### Quality Criteria

Before completing the review, verify:
- [ ] All plan items have been traced to tasks (Plan Coverage)
- [ ] TDD compliance has been verified for all code tasks (TDD Compliance)
- [ ] Dependency graph is validated with no cycles (Dependency & Ordering)
- [ ] Task granularity is appropriate (Task Granularity)
- [ ] Parallelization markers and file paths are correct (Parallelization & Files)
- [ ] Issues have clear, actionable suggestions
- [ ] Score reflects actual quality accurately

### Output

Save the review report to: `.codexspec/specs/{feature-id}/review-tasks.md`
