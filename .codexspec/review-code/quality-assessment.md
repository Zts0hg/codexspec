# Whole-Codebase Quality Assessment

Read index.md and common.md before this procedure. Use the same applicability, evidence and maintenance rules; this mode retains its advisory scoring.

## Audit Mode

Only enter this branch when the first parsed argument is `--audit`. It is a self-contained advisory quality scorecard over complete current file contents. It MUST NOT invoke the resolver. It MUST NOT emit a result envelope. It MUST NOT be consumed by `implement-tasks`. Stop after the audit report.

Audit paths are every argument after `--audit`. With no paths, review the main source directory (default: `src/`). Reject any defect selector/modifier mixed into the audit invocation.

You are the **Chief Architect** for this audit. Conduct a broad review for idiomatic clarity, correctness, robustness, architecture, and constitution alignment. Static tools are optional and their absence degrades coverage visibly.

### Audit File Resolution

- **With audit paths**: Treat only the arguments after `--audit` as paths to review (supports space-separated multiple paths)
- **Without audit paths**: Review the main source directory (default: `src/`)

### Execution Steps

#### 1. Initialize Review Context

- [ ] Parse target paths from user input
- [ ] Verify paths exist and contain source files
- [ ] Load `.codexspec/memory/constitution.md` for project quality standards (if exists)

#### 2. Language Detection

Identify candidate languages from extensions, then verify actual language/version semantics and dependencies before selecting standards:

| Extension(s) | Language | Framework Detection |
|---|---|---|
| `.py` | Python | — |
| `.ts`, `.tsx` | TypeScript | React if `package.json` declares `react` AND `.tsx`/`.jsx` files exist |
| `.js`, `.jsx` | JavaScript | React if `package.json` declares `react` AND `.tsx`/`.jsx` files exist |
| `.go` | Go | — |
| `.rs` | Rust | — |
| `.java` | Java | — |
| `.kt`, `.kts` | Kotlin | — |
| `.rb` | Ruby | — |
| `.sh`, `.bash`, `.zsh` | Shell | — |
| `.c`, `.h` | C | — |
| `.cpp`, `.hpp`, `.cc`, `.cxx` | C++ | — |
| `.cs` | C# | — |
| `.swift` | Swift | — |
| `.php` | PHP | — |

For unlisted extensions, infer the language from file content (shebangs, syntax patterns). Report detected language(s) in the review output.

**Mixed-language projects**: If multiple languages are detected, run a per-language review pass for each. Produce per-language sub-scores and report an **unweighted mean** as the top-line advisory score.

#### 3. Run Static Analysis (Tool Auto-Detection)

Probe for available tools by checking config files. Run matching tools; skip gracefully if tool or config is absent. **Report degraded coverage explicitly** in the Static Analysis table when a tool is unavailable.

| Language | Config Probe | Tools to Run |
|---|---|---|
| Python | `pyproject.toml` or `setup.py` or `setup.cfg` | `ruff check {paths}`, `mypy {paths}` |
| TypeScript/JavaScript | `package.json` + `tsconfig.json` | `npx --no-install eslint {paths}` (if eslint config exists), `npx --no-install tsc --noEmit` (if tsconfig exists) |
| Go | `go.mod` | `go vet ./...`, `gofmt -l {paths}` |
| Rust | `Cargo.toml` | `cargo check`, `cargo clippy` |
| Shell | any `.sh` file | `shellcheck {paths}` |
| Other | — | Skip static analysis; note "No automated tools available — manual review only" |

Capture and categorize all tool outputs.

#### 4. Load and Analyze Code

- [ ] Read all source files in target paths
- [ ] Identify module structure and dependencies
- [ ] Map code patterns against the 4 review dimensions below

#### 5. Review Dimension 1: Idiomatic Clarity & Simplicity (25%)

Assess whether the code leverages the language's native idioms, standard library, and ecosystem conventions.

- [ ] Detect over-engineering (unnecessary abstractions when simpler constructs suffice)
- [ ] Verify preference for standard library and ecosystem-canonical solutions
- [ ] Check adherence to the language's simplicity philosophy (e.g., Python's "Simple is better than complex", Go's "Clear is better than clever")
- [ ] Validate documentation patterns (module/function docs vs. inline noise)

Load only the applicable language/framework standards listed in index.md; their scoring examples are conditional calibration references.

#### 6. Review Dimension 2: Correctness & Explicit Contracts (25%)

Assess whether failure modes, inputs, and invariants are made explicit at boundaries.

- [ ] Check type annotation/declaration completeness (where the language supports it)
- [ ] Identify overly broad or silenced error handling
- [ ] Verify error context preservation (e.g., Python `raise from`, Go `fmt.Errorf("%w")`, Rust `?` with context)
- [ ] Assess boundary validation and null/empty discipline

Load only the applicable language/framework standards listed in index.md; their scoring examples are conditional calibration references.

#### 7. Review Dimension 3: Runtime Robustness & Resource Discipline (25%)

Assess lifecycle management, concurrency correctness, side-effect containment, and observability.

- [ ] Verify resource management (context managers, RAII, `defer`, `try-with-resources`, cleanup functions)
- [ ] Check concurrency/async patterns for correctness (blocking event loops, goroutine leaks, data races)
- [ ] Validate logging and observability practices (structured logging vs. print statements)
- [ ] Assess side-effect discipline and error propagation

**Mandatory Subsection Injection**: When affected behavior activates one of the following language/framework topics, include a dedicated findings subsection under this dimension with the specified checks:

| Language/Framework | Mandatory Subsection | Checks |
|---|---|---|
| **React** | Hooks Compliance | Rules of Hooks, `useEffect` exhaustive-deps, stale closures, effect cleanup, derived-state-as-state misuse, unnecessary `useEffect` |
| **Rust** | Ownership & Borrowing | Borrow checker compliance, unnecessary clones, lifetime annotations, unsafe usage justification |
| **Go** | Goroutine & Context Discipline | Goroutine leaks, context cancellation propagation, `defer` correctness, channel close semantics |
| **C/C++** | Memory & Lifetime Safety | malloc/free pairing, buffer overflows, dangling pointers, use-after-free, RAII in C++ |
| **Shell** | Execution Safety | `set -euo pipefail`, variable quoting, word splitting, glob expansion, command injection risks |

Load only the applicable language/framework standards listed in index.md; their scoring examples are conditional calibration references.

#### 8. Review Dimension 4: Architecture & Design Integrity (15%)

Assess structural soundness, cohesion, and testability.

- [ ] Check Single Responsibility Principle adherence (functions, classes, modules)
- [ ] Assess module cohesion and dependency direction
- [ ] Verify testability (dependency injection, mockable boundaries, pure functions)
- [ ] Identify inappropriate coupling or circular dependencies

Load only the applicable language/framework standards listed in index.md; their scoring examples are conditional calibration references.

#### 9. Constitution Alignment (10%)

If `.codexspec/memory/constitution.md` exists:

- [ ] Cross-reference findings against constitution MUST principles
- [ ] Identify violations of project-specific quality standards
- [ ] Flag deviations from established coding conventions

If the constitution's principles are language-specific (e.g., Python-focused) and the file under review uses a different language, score this axis on **meta-principles only** (testability, documentation, simplicity) and note the degradation.

> **Note**: If no constitution exists, this category defaults to 100 (full marks) and its weight is redistributed proportionally to other categories.

#### 10. Assign Severity Levels

- [ ] **CRITICAL**: Constitution MUST violations, logic bugs, security vulnerabilities, memory leaks
- [ ] **HIGH**: Tool errors (linter/type checker), resource leaks, concurrency hazards
- [ ] **MEDIUM**: Design pattern improvements, refactoring opportunities, missing type annotations
- [ ] **LOW**: Readability improvements, style enhancements, idiomatic sugar

#### 11. Generate Report

- [ ] Compile all findings into structured report (see Report Template below)
- [ ] Include specific code locations and refactoring suggestions
- [ ] Calculate quality scores per dimension

### Scoring Rubrics

Before scoring, apply these rubrics to ensure consistent, transparent evaluation.

#### Idiomatic Clarity & Simplicity (25%)

| Score Range | Criteria |
|-------------|----------|
| 90-100 | Code follows language idioms; uses stdlib/ecosystem effectively; no over-engineering; functions are focused |
| 70-89 | Mostly idiomatic; minor instances of unnecessary complexity or missed stdlib usage |
| 50-69 | Several non-idiomatic patterns; unnecessary abstractions; missed standard library opportunities |
| Below 50 | Pervasive over-engineering; code fights against language conventions; significant complexity issues |

**Typical Deductions**:

- Unnecessary abstraction when simpler construct suffices: -8 each
- Missed standard library / ecosystem opportunity: -5 each
- Function exceeding single responsibility: -5 each
- Overly complex logic when simpler alternative exists: -5 each

#### Correctness & Explicit Contracts (25%)

| Score Range | Criteria |
|-------------|----------|
| 90-100 | Complete type annotations (where applicable); specific error handling; error context preserved; explicit contracts |
| 70-89 | Most boundaries annotated; minor gaps; 1-2 broad error catches |
| 50-69 | Incomplete type annotations; several broad error handlers; missing error context |
| Below 50 | No type discipline; pervasive silenced errors; no boundary contracts |

**Typical Deductions**:

- Public function missing type annotations (typed languages): -5 each
- Overly broad error catch without re-raise/context: -8 each
- Missing error context preservation: -3 each
- Type checker error (mypy/tsc/etc.): -5 each

#### Runtime Robustness & Resource Discipline (25%)

| Score Range | Criteria |
|-------------|----------|
| 90-100 | Proper resource lifecycle management; correct concurrency patterns; proper observability; no side-effect leaks |
| 70-89 | Mostly robust; minor resource management gaps; 1-2 logging issues |
| 50-69 | Several resource leaks; print statements instead of logging; concurrency pattern issues |
| Below 50 | No resource lifecycle management; pervasive print debugging; dangerous concurrency patterns |

**Typical Deductions**:

- Resource without proper lifecycle management (no context manager/RAII/defer/cleanup): -8 each
- Print statement instead of structured logging: -3 each
- Blocking call in async context / goroutine leak / data race: -10 each
- Linter violation: -3 each
- Mandatory-subsection violation (Hooks/ownership/goroutine/memory/shell safety): -8 each

#### Architecture & Design Integrity (15%)

| Score Range | Criteria |
|-------------|----------|
| 90-100 | Clear SRP adherence; strong module cohesion; testable design; clean dependency direction |
| 70-89 | Mostly well-structured; minor cohesion gaps; 1-2 testability issues |
| 50-69 | Several SRP violations; unclear module boundaries; hard to test |
| Below 50 | Monolithic design; circular dependencies; untestable architecture |

**Typical Deductions**:

- SRP violation (component/class/module doing too much): -8 each
- Circular dependency: -10 each
- Untestable design (hard-coded dependencies, no injection points): -5 each
- Excessive coupling between modules: -5 each

#### Constitution Alignment (10%)

| Score Range | Criteria |
|-------------|----------|
| 90-100 | Fully aligned with all constitution MUST principles; project conventions followed |
| 70-89 | Mostly aligned; minor gaps in addressing specific principles |
| 50-69 | Partial alignment; several principles not addressed |
| Below 50 | Significant violations or disregard of constitution |

**Typical Deductions**:

- Constitution MUST violation: -15 each
- Constitution SHOULD violation: -8 each
- Naming convention violation: -3 each

#### Suggestion Score Cap Rule

**IMPORTANT**: Suggestions (LOW) items may deduct a **maximum of 5 points** from the total score. After resolving all CRITICAL and HIGH issues, the score should be **>= 95**.

- CRITICAL Issues: -10 to -20 points each
- HIGH Issues: -5 to -10 points each
- MEDIUM Issues: -3 to -5 points each
- LOW Suggestions: -1 to -2 points each, **capped at 5 points total**

### Report Template

````markdown
# Code Review Report

## Meta Information
- **Target**: {paths}
- **Detected Language(s)**: {language(s)}
- **Review Date**: {date}
- **Reviewer Role**: Chief Architect

## Summary
- **Overall Status**: Pass / Needs Work / Fail
- **Quality Score**: X/100
- **One-line Assessment**: {concise quality summary}

## Static Analysis Results

| Tool | Status | Issues | Details |
|------|--------|--------|---------|
| {tool name} | Pass/Warn/Fail | {count} | {summary or "No issues found"} |
| ... | ... | ... | ... |

> If no tools were available: "No automated static analysis tools detected for {language}. Review is based on manual analysis only. Consider installing {recommended tools} for future reviews."

## Dimension Analysis

| Dimension | Score | Status | Key Findings |
|-----------|-------|--------|--------------|
| Idiomatic Clarity & Simplicity | X/100 | Pass/Warn/Fail | {summary} |
| Correctness & Explicit Contracts | X/100 | Pass/Warn/Fail | {summary} |
| Runtime Robustness & Resource Discipline | X/100 | Pass/Warn/Fail | {summary} |
| Architecture & Design Integrity | X/100 | Pass/Warn/Fail | {summary} |

## Constitution Alignment

> [!NOTE]
> If no constitution exists, state "No project constitution found - using general best practices for {language}."

| Principle | Status | Notes |
|-----------|--------|-------|
| {principle name} | Pass/Warn/Fail | {alignment assessment} |

## Detailed Findings

### Critical Issues (CRITICAL)
*Must fix before merge - Constitution violations, logic bugs, security vulnerabilities, memory leaks*

- [ ] **[CODE-001]**: `{filename}:{line_number}` - {issue description}
  - **Impact**: {why this matters}
  - **Suggestion**:
    ```{language}
    {refactored code snippet}
    ```

### Warnings (HIGH)
*Should fix - Tool errors, resource leaks, concurrency hazards*

- [ ] **[CODE-002]**: `{filename}:{line_number}` - {issue description}
  - **Impact**: {potential risk}
  - **Suggestion**:
    ```{language}
    {refactored code snippet}
    ```

### Warnings (MEDIUM)
*Consider fixing - Design improvements, refactoring opportunities*

- [ ] **[CODE-003]**: `{filename}:{line_number}` - {issue description}
  - **Suggestion**: {improvement recommendation}

### Suggestions (LOW)
*Nice to have - Readability, idiomatic enhancements*

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
| Idiomatic Clarity & Simplicity | 25% | X/100 | [Which rubric range applies] | [List specific deductions] | X |
| Correctness & Explicit Contracts | 25% | X/100 | [Which rubric range applies] | [List specific deductions] | X |
| Runtime Robustness & Resource Discipline | 25% | X/100 | [Which rubric range applies] | [List specific deductions] | X |
| Architecture & Design Integrity | 15% | X/100 | [Which rubric range applies] | [List specific deductions] | X |
| Constitution Alignment | 10% | X/100 | [Which rubric range applies] | [List specific deductions] | X |
| **Total** | **100%** | | | | **X/100** |

> **Suggestion Cap**: LOW suggestions deducted X/5 points (cap: 5 points max)

## Available Follow-up Commands

Based on the review result, consider:

### If Issues Found
- **Direct Fix**: Describe the changes you want (e.g., "Fix CODE-001 and CODE-002") and I will apply the fixes
- **Re-run Audit**: `/codexspec:review-code --audit {paths}` - reassess quality after changes
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
- [ ] Weighted total = sum of (category score x weight) for all categories
- [ ] LOW suggestion deductions do not exceed 5-point cap
- [ ] No "phantom deductions" (deductions without matching issues)
- [ ] Score is consistent with Overall Status (Pass >= 80, Needs Work 50-79, Fail < 50)

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

- [ ] Static analysis tools have been executed (when available for detected language)
- [ ] All four review dimensions have been assessed
- [ ] Mandatory subsections have been included for detected language/framework (if applicable)
- [ ] Constitution alignment has been checked (if constitution exists)
- [ ] Issues are categorized by severity (CRITICAL/HIGH/MEDIUM/LOW)
- [ ] Each CRITICAL/HIGH issue has specific code refactoring suggestions
- [ ] Score reflects actual code quality accurately (validated via Score Validation Checklist)
- [ ] Strengths section highlights positive aspects
- [ ] Recommendations are prioritized and actionable

### Output

Display the review report in the conversation. Optionally save to `.codexspec/reviews/code-review-{timestamp}.md` if requested.

---
