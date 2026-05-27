---
description: 审查和验证任务分解的完整性、排序和 TDD 合规性
argument-hint: "[tasks.md 路径] (可选，默认为 .codexspec/specs/{feature-id}/)"
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

9. **Constitution Alignment Check**: Verify task breakdown respects project principles:
   - [ ] TDD enforcement aligns with constitution testing standards
   - [ ] Quality gates and checkpoints reflect constitution principles
   - [ ] Naming conventions are followed (per constitution)
   - [ ] Workflow guidelines from constitution are considered

### Scoring Rubrics

Before scoring, apply these rubrics to ensure consistent, transparent evaluation.

#### Plan Coverage (25%)

| Score Range | Criteria |
|-------------|----------|
| 90-100 | All plan phases, modules, APIs, and data models have corresponding tasks; no gaps |
| 70-89 | Most plan items covered; 1-2 minor components missing task coverage |
| 50-69 | Several plan items lack task coverage; missing tasks for key modules |
| Below 50 | Major plan phases or components have no corresponding tasks |

**Typical Deductions**:

- Plan phase with no tasks: -15 each
- Module/component without implementation task: -10 each
- API endpoint without task: -8 each
- Missing testing tasks for plan items: -5 each

#### TDD Compliance (25%)

| Score Range | Criteria |
|-------------|----------|
| 90-100 | All code components have test tasks before implementation tasks; test tasks are not optional |
| 70-89 | Most components follow TDD; 1-2 minor ordering issues |
| 50-69 | Several components lack test-first ordering; some test tasks missing |
| Below 50 | No TDD enforcement; tests are absent or consistently after implementation |

**Typical Deductions**:

- Component without test task: -12 each
- Test task ordered after implementation task: -8 each
- Test task marked as optional: -5 each

#### Dependency & Ordering (20%)

| Score Range | Criteria |
|-------------|----------|
| 90-100 | All dependencies correctly identified; no circular dependencies; foundation tasks first; logical ordering |
| 70-89 | Dependencies mostly correct; 1-2 minor ordering issues |
| 50-69 | Several missing or incorrect dependencies; some ordering problems |
| Below 50 | Circular dependencies present; major ordering errors; dependencies largely incorrect |

**Typical Deductions**:

- Circular dependency: -15 each
- Missing dependency declaration: -5 each
- Incorrect task ordering: -8 each
- Foundation task not placed first: -10

#### Task Granularity (10%)

| Score Range | Criteria |
|-------------|----------|
| 90-100 | Each task involves one primary file; clear single deliverable; appropriate scope |
| 70-89 | Most tasks are atomic; 1-2 tasks slightly broad but manageable |
| 50-69 | Several tasks involve multiple files or unclear scope |
| Below 50 | Tasks are overly broad or too narrow; no atomic focus |

**Typical Deductions**:

- Task involving multiple primary files: -8 each
- Task scope too broad (should be split): -5 each
- Task scope too narrow (should be combined): -3 each

#### Parallelization & Files (10%)

| Score Range | Criteria |
|-------------|----------|
| 90-100 | Independent tasks correctly marked [P]; file paths specified and follow conventions; no false parallel markers |
| 70-89 | Mostly correct parallel markers; minor file path issues |
| 50-69 | Several incorrect parallel markers; missing file paths |
| Below 50 | Parallel markers largely incorrect; file paths missing or wrong |

**Typical Deductions**:

- Dependent task incorrectly marked [P]: -8 each
- Independent task missing [P] marker: -3 each
- Task without file path specification: -5 each
- File path not following project convention: -3 each

#### Constitution Alignment (10%)

| Score Range | Criteria |
|-------------|----------|
| 90-100 | Fully aligned with all constitution principles; TDD/quality standards addressed; workflow guidelines followed |
| 70-89 | Mostly aligned; minor gaps in addressing specific principles |
| 50-69 | Partial alignment; several principles not addressed |
| Below 50 | Significant violations or disregard of constitution |

> **Note**: If no constitution exists, this category defaults to 100 (full marks) and its weight is redistributed proportionally to other categories.

**Typical Deductions**:

- Constitution principle not addressed: -10 per principle
- Direct violation of a constitution principle (e.g., test tasks omitted despite TDD requirement): -20 per violation

#### Suggestion Score Cap Rule

**IMPORTANT**: Suggestions (Nice to Have) items may deduct a **maximum of 5 points** from the total score. After resolving all Critical Issues and Warnings, the score should be **≥ 95**.

- Critical Issues: -10 to -20 points each
- Warnings: -5 to -10 points each
- Suggestions: -1 to -2 points each, **capped at 5 points total**

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

## Constitution Alignment

> [!NOTE]
> If no constitution exists, state "No project constitution found - using general best practices."

| Principle | Alignment | Notes |
|-----------|-----------|-------|
| [Principle 1] | ✅/⚠️/❌ | [How task breakdown aligns or conflicts] |
| [Principle 2] | ✅/⚠️/❌ | [How task breakdown aligns or conflicts] |

### Constitution Issues
- [ ] **[CONST-001]**: [Principle violation or gap, e.g., "TDD principle not enforced for Module C"]

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

| Category | Weight | Score | Rubric Basis | Deduction Details | Weighted |
|----------|--------|-------|-------------|-------------------|----------|
| Plan Coverage | 25% | X/100 | [Which rubric range applies] | [List specific deductions, e.g., "Module C missing task: -10"] | X |
| TDD Compliance | 25% | X/100 | [Which rubric range applies] | [e.g., "Service X test after impl: -8"] | X |
| Dependency & Ordering | 20% | X/100 | [Which rubric range applies] | [e.g., "Missing dependency Task 2.3→1.2: -5"] | X |
| Task Granularity | 10% | X/100 | [Which rubric range applies] | [e.g., "Task 2.5 involves 3 files: -8"] | X |
| Parallelization & Files | 10% | X/100 | [Which rubric range applies] | [e.g., "Task 2.1 false [P] marker: -8"] | X |
| Constitution Alignment | 10% | X/100 | [Which rubric range applies] | [e.g., "All principles addressed"] | X |
| **Total** | **100%** | | | | **X/100** |

> **Suggestion Cap**: Suggestions deducted X/5 points (cap: 5 points max)

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
- **Re-run Review**: `/codexspec:review-tasks` - to verify changes after fixing issues
- **Proceed Anyway**: If you decide the warnings/suggestions are not critical or out of scope for the current iteration, you can proceed directly to `/codexspec:implement-tasks`

### Next Steps Based on Review Result
- **Pass**: `/codexspec:implement-tasks` - to begin implementation
- **Needs Work**: Fix the identified issues first, then re-run `/codexspec:review-tasks` to verify, or proceed anyway if issues are acceptable
- **Fail**: `/codexspec:plan-to-tasks` - to regenerate the task breakdown
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
   - Re-read the relevant section of the tasks document
   - Re-apply the rubric criteria objectively
   - If the original score was correct: explain the reasoning and maintain the score
   - If the original score was indeed incorrect: adjust with clear explanation of what changed and why

> **CRITICAL**: Never adjust scores simply because the user expresses dissatisfaction. Only adjust when re-evaluation reveals a genuine scoring error.

### Quality Criteria

Before completing the review, verify:

- [ ] All plan items have been traced to tasks (Plan Coverage)
- [ ] TDD compliance has been verified for all code tasks (TDD Compliance)
- [ ] Dependency graph is validated with no cycles (Dependency & Ordering)
- [ ] Task granularity is appropriate (Task Granularity)
- [ ] Parallelization markers and file paths are correct (Parallelization & Files)
- [ ] Constitution principles are addressed (Constitution Alignment)
- [ ] Issues have clear, actionable suggestions
- [ ] Score reflects actual quality accurately (validated via Score Validation Checklist)

### Output

Save the review report to: `.codexspec/specs/{feature-id}/review-tasks.md`
