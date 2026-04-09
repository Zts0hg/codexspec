---
description: Review React/TypeScript code for component architecture, hooks compliance, state management, performance, and constitution alignment
argument-hint: |
  Path to React/TypeScript file or directory to review

  Examples:
  - `src/components/` - Review entire components directory
  - `src/components/Button.tsx` - Review single file
  - `src/hooks/ src/components/` - Review multiple paths
allowed-tools: Read, Grep, Glob, Bash(npm run lint:*), Bash(npx eslint:*), Bash(npx tsc --noEmit:*)
---

# React Code Reviewer

## Language Preference

**IMPORTANT**: Before proceeding, read the project's language configuration from `.codexspec/config.yml`.

- If `language.output` is set to a language other than "en", respond and generate all content in that language
- If not configured or set to "en", use English as default
- Technical terms (e.g., JSX, Hooks, Props, State) may remain in English when appropriate
- All user-facing messages, questions, and generated documents should use the configured language

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Role

You are the **Frontend Chief Architect** for this React/TypeScript project. Your responsibility is to conduct rigorous code reviews that identify component architecture issues, hooks violations, state management problems, performance bottlenecks, and violations of React best practices.

## Instructions

Perform a comprehensive code review of React/TypeScript files at the specified path. This command combines static analysis tools with architectural review to provide actionable feedback.

### File Resolution

- **With argument**: Treat `$ARGUMENTS` as the path(s) to review (supports space-separated multiple paths)
- **Without argument**: Review the main source directory (default: `src/`)

### Execution Steps

1. **Initialize Review Context**
   - [ ] Parse target paths from user input
   - [ ] Verify paths exist and contain React/TypeScript files (`.tsx`, `.ts`, `.jsx`, `.js`)
   - [ ] Load `.codexspec/memory/constitution.md` for project quality standards (if exists)

2. **Run Static Analysis**
   - [ ] Execute `npx eslint {paths}` for linting results (if eslint config exists)
   - [ ] Execute `npx tsc --noEmit` for TypeScript type checking results (if tsconfig exists)
   - [ ] Capture and categorize all tool outputs

3. **Load and Analyze Code**
   - [ ] Read all React/TypeScript files in target paths
   - [ ] Identify component structure and dependencies
   - [ ] Map code patterns against review dimensions

4. **Review Dimension 1: Component Atomicity & Single Responsibility (SRP)**
   - [ ] Check if each file contains only one primary component
   - [ ] Identify components exceeding 200 lines (potential refactoring candidates)
   - [ ] Verify complex business logic is extracted into custom Hooks
   - [ ] Validate separation between UI presentation and business logic

5. **Review Dimension 2: Hooks Compliance & Side Effects Management**
   - [ ] Verify `useEffect` has explicit and complete dependency arrays
   - [ ] Detect "over-synchronized state" misuse (derived state that should be computed)
   - [ ] Identify unnecessary `useEffect` usage (when `useMemo` or direct computation suffices)
   - [ ] Assess stale closure risks in event handlers and async operations

6. **Review Dimension 3: State Management & Data Flow**
   - [ ] Validate state is "as local as possible" (avoid unnecessary global state)
   - [ ] Check for excessive prop drilling (consider context or composition)
   - [ ] Verify props destructuring and default value handling
   - [ ] Assess async request handling (loading states, error handling, race condition protection)

7. **Review Dimension 4: Performance & Robustness**
   - [ ] Identify potential unnecessary re-render issues
   - [ ] Check if functions/objects in render are properly memoized (`useCallback`, `useMemo`)
   - [ ] Verify null/undefined safety (optional chaining, nullish coalescing)
   - [ ] Assess usage of `React.memo`, `useMemo`, `useCallback` for optimization

8. **Constitution Alignment** (if constitution exists)
   - [ ] Cross-reference findings against constitution MUST principles
   - [ ] Identify violations of project-specific quality standards
   - [ ] Flag deviations from established coding conventions

9. **Assign Severity Levels**
   - [ ] **CRITICAL**: Constitution MUST violations, logic bugs, security vulnerabilities, memory leaks
   - [ ] **HIGH**: Hooks violations, ESLint/TypeScript errors, performance hazards
   - [ ] **MEDIUM**: Design pattern improvements, refactoring large components, state management improvements
   - [ ] **LOW**: Readability improvements, code style enhancements

10. **Generate Report**
    - [ ] Compile all findings into structured report
    - [ ] Include specific code locations and refactoring suggestions
    - [ ] Calculate quality scores per dimension

### Scoring Rubrics

Before scoring, apply these rubrics to ensure consistent, transparent evaluation.

#### Component Atomicity & SRP (25%)

| Score Range | Criteria |
|-------------|----------|
| 90-100 | Each file has one primary component; all under 200 lines; business logic extracted to custom Hooks; clear UI/logic separation |
| 70-89 | Most components atomic; 1-2 slightly large components; minor mixing of concerns |
| 50-69 | Several components exceed 200 lines; business logic mixed into UI components |
| Below 50 | Components are monolithic; no separation of concerns; pervasive SRP violations |

**Typical Deductions**:

- Component exceeding 200 lines: -5 each
- Business logic not extracted to custom Hook: -8 each
- Multiple primary components in one file: -8 each
- No separation between UI and logic: -10 each

#### Hooks Compliance (25%)

| Score Range | Criteria |
|-------------|----------|
| 90-100 | All useEffect have complete dependency arrays; no derived-state-as-state; no unnecessary useEffect; no stale closure risks |
| 70-89 | Minor Hooks issues; 1-2 incomplete dependency arrays or unnecessary useEffect |
| 50-69 | Several Hooks violations; derived state stored in state; missing dependencies |
| Below 50 | Pervasive Hooks rule violations; stale closures; incorrect dependency management |

**Typical Deductions**:

- useEffect with incomplete dependency array: -8 each
- Derived state stored as separate state (should be computed): -8 each
- Unnecessary useEffect (useMemo or direct computation suffices): -5 each
- Stale closure risk in async/event handler: -8 each

#### State Management (25%)

| Score Range | Criteria |
|-------------|----------|
| 90-100 | State as local as possible; no excessive prop drilling; proper async handling with loading/error states |
| 70-89 | Mostly good state management; minor prop drilling; 1-2 missing loading states |
| 50-69 | Unnecessary global state; significant prop drilling; missing error handling |
| Below 50 | Poor state architecture; pervasive prop drilling; no async error handling |

**Typical Deductions**:

- Unnecessary global/lifted state: -8 each
- Prop drilling more than 3 levels: -5 each
- Missing loading state for async operation: -5 each
- Missing error handling for async operation: -8 each
- Race condition in async operation: -10 each

#### Performance & Robustness (20%)

| Score Range | Criteria |
|-------------|----------|
| 90-100 | No unnecessary re-renders; proper memoization; null/undefined safety; appropriate React.memo usage |
| 70-89 | Minor performance issues; 1-2 missing memoizations; mostly null-safe |
| 50-69 | Several re-render issues; missing memoization for expensive computations; null safety gaps |
| Below 50 | Pervasive performance issues; no memoization; frequent null/undefined crashes |

**Typical Deductions**:

- Unmemoized expensive computation in render: -8 each
- Object/function created in render without useCallback/useMemo: -5 each
- Missing optional chaining for nullable access: -3 each
- Missing React.memo for frequently re-rendered component: -5 each

#### Constitution Alignment (5%)

| Score Range | Criteria |
|-------------|----------|
| 90-100 | Fully aligned with all constitution MUST principles; project conventions followed |
| 70-89 | Mostly aligned; minor gaps in addressing specific principles |
| 50-69 | Partial alignment; several principles not addressed |
| Below 50 | Significant violations or disregard of constitution |

> **Note**: If no constitution exists, this category defaults to 100 (full marks) and its weight is redistributed proportionally to other categories.

**Typical Deductions**:

- Constitution MUST violation: -15 each
- Constitution SHOULD violation: -8 each
- Naming convention violation: -3 each

#### Suggestion Score Cap Rule

**IMPORTANT**: Suggestions (LOW) items may deduct a **maximum of 5 points** from the total score. After resolving all CRITICAL and HIGH issues, the score should be **≥ 95**.

- CRITICAL Issues: -10 to -20 points each
- HIGH Issues: -5 to -10 points each
- MEDIUM Issues: -3 to -5 points each
- LOW Suggestions: -1 to -2 points each, **capped at 5 points total**

### Report Template

````markdown
# React Code Review Report

## Meta Information
- **Target**: {paths}
- **Review Date**: {date}
- **Reviewer Role**: Frontend Chief Architect

## Summary
- **Overall Status**: ✅ Pass / ⚠️ Needs Work / ❌ Fail
- **Quality Score**: X/100
- **One-line Assessment**: {concise quality summary}

## Static Analysis Results

| Tool | Status | Issues | Details |
|------|--------|--------|---------|
| ESLint | ✅/⚠️/❌ | {count} | {summary or "No issues found"} |
| TypeScript | ✅/⚠️/❌ | {count} | {summary or "No issues found"} |

## Dimension Analysis

| Dimension | Score | Status | Key Findings |
|-----------|-------|--------|--------------|
| Component Atomicity & SRP | X/100 | ✅/⚠️/❌ | {summary} |
| Hooks Compliance | X/100 | ✅/⚠️/❌ | {summary} |
| State Management | X/100 | ✅/⚠️/❌ | {summary} |
| Performance & Robustness | X/100 | ✅/⚠️/❌ | {summary} |

## Constitution Alignment

> [!NOTE]
> If no constitution exists, state "No project constitution found - using general React best practices."

| Principle | Status | Notes |
|-----------|--------|-------|
| {principle name} | ✅/⚠️/❌ | {alignment assessment} |

## Detailed Findings

### Critical Issues (CRITICAL)
*Must fix before merge - Constitution violations, logic bugs, memory leaks, security vulnerabilities*

- [ ] **[REACT-001]**: `{filename}:{line_number}` - {issue description}
  - **Impact**: {why this matters}
  - **Suggestion**:
    ```tsx
    {refactored code snippet}
    ```

### Warnings (HIGH)
*Should fix - Hooks violations, tool errors, performance issues*

- [ ] **[REACT-002]**: `{filename}:{line_number}` - {issue description}
  - **Impact**: {potential risk}
  - **Suggestion**:
    ```tsx
    {refactored code snippet}
    ```

### Warnings (MEDIUM)
*Consider fixing - Design improvements, refactoring opportunities*

- [ ] **[REACT-003]**: `{filename}:{line_number}` - {issue description}
  - **Suggestion**: {improvement recommendation}

### Suggestions (LOW)
*Nice to have - Readability, style enhancements*

- [ ] **[REACT-004]**: `{filename}:{line_number}` - {enhancement description}
  - **Benefit**: {value of this change}

## Strengths
- {highlight 1-2 positive findings in the codebase}

## Recommendations

### Priority 1: Must Fix (Before Merge)
1. {most critical action}
2. {second most critical}

### Priority 2: Should Fix (This Sprint)
1. {important improvement}
2. {another improvement}

### Priority 3: Nice to Have (Future)
1. {optional enhancement}

## Scoring Breakdown

| Category | Weight | Score | Rubric Basis | Deduction Details | Weighted |
|----------|--------|-------|-------------|-------------------|----------|
| Component Atomicity & SRP | 25% | X/100 | [Which rubric range applies] | [List specific deductions, e.g., "UserPanel.tsx 350 lines: -5"] | X |
| Hooks Compliance | 25% | X/100 | [Which rubric range applies] | [e.g., "useEffect missing dep in Form.tsx: -8"] | X |
| State Management | 25% | X/100 | [Which rubric range applies] | [e.g., "Missing error state in useFetch: -8"] | X |
| Performance & Robustness | 20% | X/100 | [Which rubric range applies] | [e.g., "Unmemoized filter in List.tsx: -8"] | X |
| Constitution Alignment | 5% | X/100 | [Which rubric range applies] | [e.g., "All principles followed"] | X |
| **Total** | **100%** | | | | **X/100** |

> **Suggestion Cap**: LOW suggestions deducted X/5 points (cap: 5 points max)

## Available Follow-up Commands

Based on the review result, consider:

### If Issues Found
- **Direct Fix**: Describe the changes you want (e.g., "Fix REACT-001 and REACT-002") and I will apply the fixes
- **Re-run Review**: `/codexspec:review-react-code {paths}` - verify fixes after changes
- **Proceed Anyway**: If issues are acceptable for current iteration

### Next Steps Based on Review Result
- **Pass**: Code is ready for commit/merge
- **Needs Work**: Fix HIGH/CRITICAL issues, then re-run review
- **Fail**: Significant rework required - consider `/codexspec:clarify` for design discussion
````

### Score Validation Checklist

Before finalizing scores, the reviewer MUST verify:

- [ ] Every deduction in "Deduction Details" column has a corresponding issue in "Detailed Findings"
- [ ] The arithmetic is correct: each category score = 100 minus sum of deductions
- [ ] Weighted total = sum of (category score × weight) for all categories
- [ ] LOW suggestion deductions do not exceed 5-point cap
- [ ] No "phantom deductions" (deductions without matching issues)
- [ ] Score is consistent with Overall Status (Pass ≥ 80, Needs Work 50-79, Fail < 50)

### Score Challenge Response Protocol

When a user questions or challenges the score, follow this three-step process:

1. **Provide Evidence**: Present the complete scoring breakdown with all deduction details. Reference the specific rubric criteria and issue IDs that justify each deduction.

2. **Ask for Specifics**: Ask the user which specific scoring item(s) they believe are incorrect. Do NOT preemptively adjust any scores.

3. **Targeted Re-evaluation**: For each challenged item:
   - Re-read the relevant code section
   - Re-apply the rubric criteria objectively
   - If the original score was correct: explain the reasoning and maintain the score
   - If the original score was indeed incorrect: adjust with clear explanation of what changed and why

> **CRITICAL**: Never adjust scores simply because the user expresses dissatisfaction. Only adjust when re-evaluation reveals a genuine scoring error.

### Quality Criteria

Before completing the review, verify:

- [ ] Static analysis tools (ESLint, TypeScript) have been executed (if config exists)
- [ ] All four review dimensions have been assessed
- [ ] Constitution alignment has been checked (if constitution exists)
- [ ] Issues are categorized by severity (CRITICAL/HIGH/MEDIUM/LOW)
- [ ] Each CRITICAL/HIGH issue has specific code refactoring suggestions
- [ ] Score reflects actual code quality accurately (validated via Score Validation Checklist)
- [ ] Strengths section highlights positive aspects
- [ ] Recommendations are prioritized and actionable

### Output

Display the review report in the conversation. Optionally save to `.codexspec/reviews/react-code-review-{timestamp}.md` if requested.
