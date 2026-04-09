---
description: Review Python code for PEP 8 compliance, type safety, engineering robustness, and constitution alignment
argument-hint: |
  Path to Python file or directory to review

  Examples:
  - `src/codexspec/` - Review entire package
  - `src/codexspec/__init__.py` - Review single file
  - `src/ tests/` - Review multiple paths
allowed-tools: Read, Grep, Glob, Bash(ruff check:*), Bash(mypy:*), Bash(python -m py_compile:*)
---

# Python Code Reviewer

## Language Preference

**IMPORTANT**: Before proceeding, read the project's language configuration from `.codexspec/config.yml`.

- If `language.output` is set to a language other than "en", respond and generate all content in that language
- If not configured or set to "en", use English as default
- Technical terms (e.g., API, Type Hints, PEP 8) may remain in English when appropriate
- All user-facing messages, questions, and generated documents should use the configured language

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Role

You are the **Chief Architect** for this Python project. Your responsibility is to conduct rigorous code reviews that identify logic defects, performance bottlenecks, type safety issues, and violations of engineering best practices.

## Instructions

Perform a comprehensive code review of Python files at the specified path. This command combines static analysis tools with architectural review to provide actionable feedback.

### File Resolution

- **With argument**: Treat `$ARGUMENTS` as the path(s) to review (supports space-separated multiple paths)
- **Without argument**: Review the main source directory (default: `src/`)

### Execution Steps

1. **Initialize Review Context**
   - [ ] Parse target paths from user input
   - [ ] Verify paths exist and contain Python files
   - [ ] Load `.codexspec/memory/constitution.md` for project quality standards (if exists)

2. **Run Static Analysis**
   - [ ] Execute `ruff check {paths}` for linting results
   - [ ] Execute `mypy {paths}` for type checking results
   - [ ] Capture and categorize all tool outputs

3. **Load and Analyze Code**
   - [ ] Read all Python files in target paths
   - [ ] Identify module structure and dependencies
   - [ ] Map code patterns against review dimensions

4. **Review Dimension 1: Pythonic & KISS Principle**
   - [ ] Detect over-engineering (unnecessary classes when functions suffice)
   - [ ] Verify preference for built-in functions and standard library (`pathlib`, `itertools`, `collections`)
   - [ ] Check adherence to "Simple is better than complex"
   - [ ] Validate docstring usage (module/function docstrings vs. inline comments)

5. **Review Dimension 2: Type Safety & Explicitness**
   - [ ] Check type annotation completeness (function parameters, return types)
   - [ ] Identify overly broad exception handling (`except Exception:`)
   - [ ] Verify exception context preservation (`raise ... from err`)
   - [ ] Assess dependency injection patterns for testability

6. **Review Dimension 3: Engineering Robustness**
   - [ ] Verify resource management (`with` context managers for files/connections)
   - [ ] Check async/await usage patterns (blocking event loop risks)
   - [ ] Validate logging practices (`logging` module vs. `print` statements)
   - [ ] Review log level appropriateness

7. **Constitution Alignment** (if constitution exists)
   - [ ] Cross-reference findings against constitution MUST principles
   - [ ] Identify violations of project-specific quality standards
   - [ ] Flag deviations from established coding conventions

8. **Assign Severity Levels**
   - [ ] **CRITICAL**: Constitution MUST violations, logic bugs, security vulnerabilities
   - [ ] **HIGH**: Type safety gaps, ruff/mypy errors, resource leaks
   - [ ] **MEDIUM**: Design pattern improvements, refactoring long functions, missing type annotations
   - [ ] **LOW**: Readability improvements, Pythonic syntax sugar

9. **Generate Report**
   - [ ] Compile all findings into structured report
   - [ ] Include specific code locations and refactoring suggestions
   - [ ] Calculate quality scores per dimension

### Scoring Rubrics

Before scoring, apply these rubrics to ensure consistent, transparent evaluation.

#### Pythonic & KISS (30%)

| Score Range | Criteria |
|-------------|----------|
| 90-100 | Code follows Python idioms; uses built-in/stdlib effectively; no over-engineering; functions are focused |
| 70-89 | Mostly Pythonic; minor instances of unnecessary complexity or missed stdlib usage |
| 50-69 | Several non-idiomatic patterns; unnecessary classes or abstractions; missed standard library opportunities |
| Below 50 | Pervasive over-engineering; code fights against Python idioms; significant complexity issues |

**Typical Deductions**:

- Unnecessary class when function suffices: -8 each
- Missed standard library opportunity (e.g., manual iteration vs. itertools): -5 each
- Function exceeding single responsibility: -5 each
- Overly complex logic when simpler alternative exists: -5 each

#### Type Safety & Explicitness (30%)

| Score Range | Criteria |
|-------------|----------|
| 90-100 | Complete type annotations; specific exception handling; exception context preserved; good DI patterns |
| 70-89 | Most functions annotated; minor type safety gaps; 1-2 broad exception catches |
| 50-69 | Incomplete type annotations; several broad exception handlers; missing `raise from` |
| Below 50 | No type annotations; pervasive `except Exception:`; no exception context preservation |

**Typical Deductions**:

- Public function missing type annotations: -5 each
- Bare `except:` or `except Exception:` without re-raise: -8 each
- Missing `raise ... from err` context: -3 each
- mypy error: -5 each

#### Engineering Robustness (30%)

| Score Range | Criteria |
|-------------|----------|
| 90-100 | Proper resource management (context managers); correct async patterns; proper logging; no print statements |
| 70-89 | Mostly robust; minor resource management gaps; 1-2 logging issues |
| 50-69 | Several resource leaks; print statements instead of logging; async pattern issues |
| Below 50 | No context managers for resources; pervasive print debugging; blocking async operations |

**Typical Deductions**:

- File/connection without context manager: -8 each
- `print()` instead of `logging`: -3 each
- Blocking call in async context: -10 each
- Incorrect log level usage: -3 each
- ruff violation: -3 each

#### Constitution Alignment (10%)

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
# Python Code Review Report

## Meta Information
- **Target**: {paths}
- **Review Date**: {date}
- **Reviewer Role**: Chief Architect

## Summary
- **Overall Status**: ✅ Pass / ⚠️ Needs Work / ❌ Fail
- **Quality Score**: X/100
- **One-line Assessment**: {concise quality summary}

## Static Analysis Results

| Tool | Status | Issues | Details |
|------|--------|--------|---------|
| ruff | ✅/⚠️/❌ | {count} | {summary or "No issues found"} |
| mypy | ✅/⚠️/❌ | {count} | {summary or "No issues found"} |

## Dimension Analysis

| Dimension | Score | Status | Key Findings |
|-----------|-------|--------|--------------|
| Pythonic & KISS | X/100 | ✅/⚠️/❌ | {summary} |
| Type Safety & Explicitness | X/100 | ✅/⚠️/❌ | {summary} |
| Engineering Robustness | X/100 | ✅/⚠️/❌ | {summary} |

## Constitution Alignment

> [!NOTE]
> If no constitution exists, state "No project constitution found - using general Python best practices."

| Principle | Status | Notes |
|-----------|--------|-------|
| {principle name} | ✅/⚠️/❌ | {alignment assessment} |

## Detailed Findings

### Critical Issues (CRITICAL)
*Must fix before merge - Constitution violations, logic bugs, security vulnerabilities*

- [ ] **[CODE-001]**: `{filename}:{line_number}` - {issue description}
  - **Impact**: {why this matters}
  - **Suggestion**:
    ```python
    {refactored code snippet}
    ```

### Warnings (HIGH)
*Should fix - Type safety, tool errors, resource management*

- [ ] **[CODE-002]**: `{filename}:{line_number}` - {issue description}
  - **Impact**: {potential risk}
  - **Suggestion**:
    ```python
    {refactored code snippet}
    ```

### Warnings (MEDIUM)
*Consider fixing - Design improvements, refactoring opportunities*

- [ ] **[CODE-003]**: `{filename}:{line_number}` - {issue description}
  - **Suggestion**: {improvement recommendation}

### Suggestions (LOW)
*Nice to have - Readability, Pythonic enhancements*

- [ ] **[CODE-004]**: `{filename}:{line_number}` - {enhancement description}
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
| Pythonic & KISS | 30% | X/100 | [Which rubric range applies] | [List specific deductions, e.g., "Unnecessary class in utils.py: -8"] | X |
| Type Safety | 30% | X/100 | [Which rubric range applies] | [e.g., "2 functions missing annotations: -10"] | X |
| Engineering Robustness | 30% | X/100 | [Which rubric range applies] | [e.g., "File opened without context manager: -8"] | X |
| Constitution Alignment | 10% | X/100 | [Which rubric range applies] | [e.g., "All principles followed"] | X |
| **Total** | **100%** | | | | **X/100** |

> **Suggestion Cap**: LOW suggestions deducted X/5 points (cap: 5 points max)

## Available Follow-up Commands

Based on the review result, consider:

### If Issues Found
- **Direct Fix**: Describe the changes you want (e.g., "Fix CODE-001 and CODE-002") and I will apply the fixes
- **Re-run Review**: `/codexspec:review-python-code {paths}` - verify fixes after changes
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

- [ ] Static analysis tools (ruff, mypy) have been executed
- [ ] All three review dimensions have been assessed
- [ ] Constitution alignment has been checked (if constitution exists)
- [ ] Issues are categorized by severity (CRITICAL/HIGH/MEDIUM/LOW)
- [ ] Each CRITICAL/HIGH issue has specific code refactoring suggestions
- [ ] Score reflects actual code quality accurately (validated via Score Validation Checklist)
- [ ] Strengths section highlights positive aspects
- [ ] Recommendations are prioritized and actionable

### Output

Display the review report in the conversation. Optionally save to `.codexspec/reviews/python-code-review-{timestamp}.md` if requested.
