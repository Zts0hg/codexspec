---
description: Review and validate the task breakdown for completeness and correct ordering
handoffs:
  - agent: claude
    step: Review tasks against plan and dependencies
---

# Tasks Reviewer

## User Input

$ARGUMENTS

## Instructions

Review the task breakdown for completeness, correct ordering, and proper dependency management. This ensures the tasks are ready for implementation.

### Steps

1. **Load Tasks**: Read the tasks from `.codexspec/specs/{feature-id}/tasks.md`.

2. **Load Plan**: Read the plan from `.codexspec/specs/{feature-id}/plan.md`.

3. **Coverage Check**: Verify all plan items are covered:
   - [ ] All implementation phases have corresponding tasks
   - [ ] All components have creation tasks
   - [ ] All APIs have implementation tasks
   - [ ] Testing tasks are included

4. **Dependency Validation**: Check task dependencies:
   - [ ] Dependencies are correctly identified
   - [ ] No circular dependencies
   - [ ] Dependencies are minimal but sufficient

5. **Ordering Check**: Verify task execution order:
   - [ ] Setup tasks come first
   - [ ] Dependencies execute before dependents
   - [ ] Testing tasks come after implementation

6. **Parallelization Review**: Check parallel execution markers:
   - [ ] Truly independent tasks are marked parallelizable
   - [ ] Dependent tasks are not marked parallel

7. **File Path Validation**: Check file specifications:
   - [ ] All tasks have file paths specified
   - [ ] File paths follow project structure
   - [ ] File paths are consistent with plan

8. **Generate Report**: Create a review report.

### Report Template

```markdown
# Tasks Review Report

## Summary
- **Tasks File**: {feature-id}/tasks.md
- **Status**: ✅ Pass / ⚠️ Needs Work / ❌ Fail
- **Overall Score**: X/100

## Coverage Analysis

| Plan Item | Task Coverage | Notes |
|-----------|---------------|-------|
| Phase 1: Foundation | ✅ | Tasks 1.1, 1.2 |
| Phase 2: Core | ✅ | Tasks 2.1-2.4 |
| Phase 3: Testing | ⚠️ | Missing integration tests |
| Data Models | ✅ | Task 2.1 |
| API Endpoints | ✅ | Tasks 2.3, 2.4 |

## Dependency Validation

| Task | Dependencies | Status | Notes |
|------|--------------|--------|-------|
| 1.1 | None | ✅ | Root task |
| 1.2 | 1.1 | ✅ | Correct |
| 2.1 | 1.1 | ✅ | Can run with 1.2 |
| 2.2 | 2.1 | ✅ | Correct |
| 2.3 | 2.2 | ⚠️ | Missing 2.1 dependency |

## Ordering Analysis

```
✅ Correct Order:
1.1 → 1.2 → 2.1 → 2.2 → 2.3 → 3.1

⚠️ Suggested Parallel Execution:
1.1 → [1.2 || 2.1] → 2.2 → 2.3 → 3.1
```

## Parallelization Review

| Task | Marked Parallel | Actually Parallel | Correct? |
|------|-----------------|-------------------|----------|
| 1.1 | No | No | ✅ |
| 2.1 | Yes | Yes | ✅ |
| 2.2 | Yes | No | ⚠️ Should not be parallel |

## Issues Found

### Critical
- [ ] Task 2.3 missing dependency on Task 2.1

### Warning
- [ ] Task 2.2 marked parallel but depends on 2.1
- [ ] Missing integration test tasks

### Suggestion
- [ ] Consider breaking Task 2.4 into smaller tasks
- [ ] Add checkpoint after Phase 2

## Recommendations

1. Add Task 2.1 as dependency for Task 2.3
2. Remove parallel marker from Task 2.2
3. Add integration test tasks in Phase 3
```

### Quality Criteria

- [ ] All plan items have task coverage
- [ ] Dependencies are validated
- [ ] Ordering is verified
- [ ] Parallelization is correct
- [ ] Issues are prioritized

> [!NOTE]
> This is a placeholder command. The full implementation will be added in future versions.
