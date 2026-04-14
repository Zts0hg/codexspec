---
description: Review code in any language for idiomatic clarity, correctness, robustness, architecture, and constitution alignment
argument-hint: |
  Path to source file or directory to review (any language)

  Examples:
  - `src/` - Review entire source tree
  - `src/components/Button.tsx` - Review single file
  - `src/ tests/` - Review multiple paths
allowed-tools: Read, Grep, Glob, Bash(ruff check:*), Bash(mypy:*), Bash(python -m py_compile:*), Bash(npx eslint:*), Bash(npx tsc:*), Bash(npm run lint:*), Bash(go vet:*), Bash(gofmt:*), Bash(golangci-lint:*), Bash(cargo check:*), Bash(cargo clippy:*), Bash(shellcheck:*)
---

# Code Reviewer

## Language Preference

**IMPORTANT**: Before proceeding, read the project's language configuration from `.codexspec/config.yml`.

- If `language.output` is set to a language other than "en", respond and generate all content in that language
- If not configured or set to "en", use English as default
- Technical terms (e.g., API, Type Hints, PEP 8, Hooks, RAII) may remain in English when appropriate
- All user-facing messages, questions, and generated documents should use the configured language

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Role

You are the **Chief Architect** for this project. Your responsibility is to conduct rigorous code reviews that identify logic defects, performance bottlenecks, type safety issues, architectural problems, and violations of engineering best practices — regardless of the programming language used.

## Instructions

Perform a comprehensive code review of source files at the specified path. This command combines static analysis tools (when available) with architectural review to provide actionable feedback.

### File Resolution

- **With argument**: Treat `$ARGUMENTS` as the path(s) to review (supports space-separated multiple paths)
- **Without argument**: Review the main source directory (default: `src/`)

### Execution Steps

#### 1. Initialize Review Context

- [ ] Parse target paths from user input
- [ ] Verify paths exist and contain source files
- [ ] Load `.codexspec/memory/constitution.md` for project quality standards (if exists)

#### 2. Language Detection

Scan target paths and determine the primary language(s) from file extensions:

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
| TypeScript/JavaScript | `package.json` + `tsconfig.json` | `npx eslint {paths}` (if eslint config exists), `npx tsc --noEmit` (if tsconfig exists) |
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

See **Language Appendix** below for language-specific checkpoints.

#### 6. Review Dimension 2: Correctness & Explicit Contracts (25%)

Assess whether failure modes, inputs, and invariants are made explicit at boundaries.

- [ ] Check type annotation/declaration completeness (where the language supports it)
- [ ] Identify overly broad or silenced error handling
- [ ] Verify error context preservation (e.g., Python `raise from`, Go `fmt.Errorf("%w")`, Rust `?` with context)
- [ ] Assess boundary validation and null/empty discipline

See **Language Appendix** below for language-specific checkpoints.

#### 7. Review Dimension 3: Runtime Robustness & Resource Discipline (25%)

Assess lifecycle management, concurrency correctness, side-effect containment, and observability.

- [ ] Verify resource management (context managers, RAII, `defer`, `try-with-resources`, cleanup functions)
- [ ] Check concurrency/async patterns for correctness (blocking event loops, goroutine leaks, data races)
- [ ] Validate logging and observability practices (structured logging vs. print statements)
- [ ] Assess side-effect discipline and error propagation

**Mandatory Subsection Injection**: When one of the following languages/frameworks is detected, you MUST include a dedicated findings subsection under this dimension with the specified checks:

| Language/Framework | Mandatory Subsection | Checks |
|---|---|---|
| **React** | Hooks Compliance | Rules of Hooks, `useEffect` exhaustive-deps, stale closures, effect cleanup, derived-state-as-state misuse, unnecessary `useEffect` |
| **Rust** | Ownership & Borrowing | Borrow checker compliance, unnecessary clones, lifetime annotations, unsafe usage justification |
| **Go** | Goroutine & Context Discipline | Goroutine leaks, context cancellation propagation, `defer` correctness, channel close semantics |
| **C/C++** | Memory & Lifetime Safety | malloc/free pairing, buffer overflows, dangling pointers, use-after-free, RAII in C++ |
| **Shell** | Execution Safety | `set -euo pipefail`, variable quoting, word splitting, glob expansion, command injection risks |

See **Language Appendix** below for language-specific checkpoints.

#### 8. Review Dimension 4: Architecture & Design Integrity (15%)

Assess structural soundness, cohesion, and testability.

- [ ] Check Single Responsibility Principle adherence (functions, classes, modules)
- [ ] Assess module cohesion and dependency direction
- [ ] Verify testability (dependency injection, mockable boundaries, pure functions)
- [ ] Identify inappropriate coupling or circular dependencies

See **Language Appendix** below for language-specific checkpoints.

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
- **Re-run Review**: `/codexspec:review-code {paths}` - verify fixes after changes
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

## Language Appendix: Per-Language Deduction Exemplars

This appendix provides concrete, point-valued deduction examples for common languages. Use these as calibration references when scoring — they ensure depth parity across languages. For languages not listed here, apply the generic 4-axis framework using first principles and the language's official style guide.

### Python

**Axis 1 — Idiomatic Clarity & Simplicity**:

- Unnecessary class when a function suffices: **-8**
- Missed `pathlib` / `itertools` / `collections` opportunity: **-5**
- Manual iteration instead of comprehension or generator expression: **-3**
- Mutable default argument (`def f(x=[])`): **-8**
- `dict[key]` without guard when `dict.get()` is appropriate: **-3**

**Axis 2 — Correctness & Explicit Contracts**:

- Public function missing type annotations: **-5**
- Bare `except:` or `except Exception:` without re-raise: **-8**
- Missing `raise ... from err` context: **-3**
- `mypy` error: **-5**
- Overly broad `Optional` when a more specific Union applies: **-3**

**Axis 3 — Runtime Robustness & Resource Discipline**:

- File/connection opened without `with` context manager: **-8**
- `print()` instead of `logging`: **-3**
- Blocking call in async context: **-10**
- Incorrect log level usage: **-3**
- `ruff` violation: **-3**

**Axis 4 — Architecture & Design Integrity**:

- God function (>50 lines of logic without clear structure): **-5**
- Circular import: **-10**
- Hard-coded dependency that should be injected: **-5**
- Module mixing I/O and pure computation: **-5**

### TypeScript

**Axis 1 — Idiomatic Clarity & Simplicity**:

- Using `any` instead of a proper type: **-8**
- Unnecessary type assertion (`as`) when narrowing suffices: **-5**
- Verbose `if/else` when nullish coalescing (`??`) or optional chaining (`?.`) applies: **-3**
- Not using `const` for immutable bindings: **-3**
- Redundant type annotation where inference is sufficient: **-3**

**Axis 2 — Correctness & Explicit Contracts**:

- Missing return type annotation on exported function: **-5**
- `tsc` error (strict mode): **-5**
- Unchecked `.data` access on API response without validation: **-8**
- Empty catch block swallowing errors: **-8**
- Missing discriminated union exhaustiveness check: **-5**

**Axis 3 — Runtime Robustness & Resource Discipline**:

- Unhandled Promise rejection (missing `.catch()` or `try/catch`): **-8**
- Event listener added without cleanup/removal: **-8**
- ESLint violation: **-3**
- `setTimeout`/`setInterval` without cleanup: **-5**
- Missing `AbortController` for cancellable fetch: **-5**

**Axis 4 — Architecture & Design Integrity**:

- Barrel file re-exporting everything (tree-shaking killer): **-5**
- Circular dependency between modules: **-10**
- Business logic in UI layer: **-8**
- God file (>500 lines): **-5**

### React (TypeScript/JavaScript + React framework)

> Apply these **in addition to** the base TypeScript/JavaScript exemplars above.

**Axis 3 — Mandatory Subsection: Hooks Compliance**:

- `useEffect` with incomplete dependency array: **-8**
- Derived state stored as separate `useState` (should be computed): **-8**
- Unnecessary `useEffect` when `useMemo` or direct computation suffices: **-5**
- Stale closure risk in async/event handler: **-8**
- Missing `useEffect` cleanup for subscriptions/timers: **-8**

**Axis 4 — Architecture (React-specific)**:

- Component exceeding 200 lines: **-5**
- Business logic not extracted to custom Hook: **-8**
- Multiple primary components in one file: **-8**
- Missing loading/error state for async operation: **-5**
- Prop drilling more than 3 levels deep: **-5**
- Unnecessary global/lifted state: **-8**
- Unmemoized expensive computation in render: **-8**
- Object/function created in render without `useCallback`/`useMemo`: **-5**
- Missing `React.memo` for frequently re-rendered component: **-5**
- Race condition in async operation: **-10**

### Go

**Axis 1 — Idiomatic Clarity & Simplicity**:

- Unnecessary getter/setter on exported struct field: **-5**
- Using `interface{}` / `any` when a concrete type suffices: **-5**
- Not using `errors.New` / `fmt.Errorf` for simple errors: **-3**
- Overly abstract interface with only one implementation: **-5**
- Using `init()` for non-trivial logic: **-8**

**Axis 2 — Correctness & Explicit Contracts**:

- Ignoring returned `error` (assigned to `_`): **-8**
- Missing `fmt.Errorf("...: %w", err)` for error wrapping: **-5**
- Exported function missing doc comment: **-3**
- Naked return in a non-trivial function: **-5**
- `go vet` finding: **-5**

**Axis 3 — Runtime Robustness & Resource Discipline (+ Goroutine & Context Discipline)**:

- Goroutine leak (no exit condition, no context cancellation): **-10**
- Missing `defer` for resource cleanup: **-8**
- Not propagating `context.Context` through call chain: **-8**
- Channel not closed by producer: **-5**
- `sync.Mutex` held across I/O call: **-8**
- Using `fmt.Println` instead of structured logger: **-3**

**Axis 4 — Architecture & Design Integrity**:

- Package with >20 exported symbols (god package): **-5**
- Interface defined in consumer package rather than provider: **-5** (note: in Go, consumer-side interfaces are idiomatic for small interfaces)
- Circular package dependency: **-10**
- Test depending on external service without build tag: **-5**

### Rust

**Axis 1 — Idiomatic Clarity & Simplicity**:

- Manual loop when iterator chain suffices: **-5**
- Unnecessary `.clone()` when borrowing works: **-8**
- Using `unwrap()` / `expect()` in library code: **-8**
- Not using `?` operator for error propagation: **-5**
- Verbose match when `if let` suffices: **-3**

**Axis 2 — Correctness & Explicit Contracts**:

- Missing error context (no `.context()` / `.map_err()`): **-5**
- Silencing a `Result` with `let _ =`: **-8**
- Public function missing doc comment: **-3**
- `cargo check` error: **-5**
- `cargo clippy` warning: **-3**

**Axis 3 — Runtime Robustness & Resource Discipline (+ Ownership & Borrowing)**:

- Unnecessary `unsafe` block without justification comment: **-10**
- Holding a lock across an `await` point: **-10**
- Leaking `Arc` references (never-decreasing ref count): **-8**
- Missing `Drop` implementation for resource wrapper: **-5**
- Spawning a task without a cancellation mechanism: **-8**

**Axis 4 — Architecture & Design Integrity**:

- God module (>1000 lines): **-5**
- Leaky abstraction exposing internal types in public API: **-8**
- Circular module dependency: **-10**
- Trait with >10 methods (likely needs decomposition): **-5**

### Shell (Bash/Zsh/POSIX sh)

**Axis 1 — Idiomatic Clarity & Simplicity**:

- Using `expr` or backticks when `$((...))` / `$()` works: **-3**
- Parsing `ls` output instead of using globs: **-8**
- Using `cat file | cmd` when `cmd < file` suffices (useless use of cat): **-3**
- Not using `local` for function variables: **-5**
- Hardcoded paths instead of variables/parameters: **-3**

**Axis 2 — Correctness & Explicit Contracts**:

- Unquoted variable expansion (`$var` instead of `"$var"`): **-8**
- Missing `shellcheck` directive acknowledgment for intentional behavior: **-3**
- No input validation for script arguments: **-5**
- Using `test` / `[` when `[[` provides safer semantics: **-3**
- `shellcheck` finding: **-5**

**Axis 3 — Runtime Robustness & Resource Discipline (+ Execution Safety)**:

- Missing `set -euo pipefail` (or equivalent): **-10**
- No `trap` for cleanup on exit/error: **-8**
- Temporary files without `mktemp` and cleanup: **-8**
- Command injection risk via unvalidated input in eval/command substitution: **-10**
- Using `kill -9` without trying graceful shutdown first: **-3**

**Axis 4 — Architecture & Design Integrity**:

- Script exceeding 300 lines without function decomposition: **-5**
- No usage/help message for scripts accepting arguments: **-3**
- Mixed concerns (deployment + configuration + monitoring in one script): **-8**
- Missing exit codes documentation: **-3**

### Java / Kotlin

**Axis 1 — Idiomatic Clarity & Simplicity**:

- (Java) Verbose stream chain when a simple loop is clearer: **-3**
- (Java) Not using `var` (Java 10+) for obvious local types: **-3**
- (Kotlin) Using Java-style null checks instead of `?.` / `?:`: **-5**
- (Kotlin) Using `!!` (non-null assertion) without justification: **-8**
- Unnecessary wrapper class / design pattern ceremony: **-5**

**Axis 2 — Correctness & Explicit Contracts**:

- (Java) Catching `Exception` or `Throwable` broadly: **-8**
- (Java) Returning `null` from a method that should return `Optional`: **-5**
- (Kotlin) Exposed mutable collection (`MutableList` in public API): **-5**
- Missing `@Nullable` / `@NonNull` annotations (Java): **-3**
- Ignoring checked exception without logging: **-8**

**Axis 3 — Runtime Robustness & Resource Discipline**:

- Resource not using try-with-resources / `.use {}`: **-8**
- Thread created without executor service / coroutine: **-8**
- (Kotlin) Blocking call inside coroutine without `withContext(Dispatchers.IO)`: **-10**
- Missing structured concurrency (orphan threads/coroutines): **-8**
- `System.out.println` instead of logger: **-3**

**Axis 4 — Architecture & Design Integrity**:

- God class (>500 lines): **-5**
- Circular package dependency: **-10**
- Service depending directly on implementation instead of interface: **-5**
- Missing dependency injection (hard-coded `new`): **-5**

### Ruby

**Axis 1 — Idiomatic Clarity & Simplicity**:

- Verbose loop when `map` / `select` / `each_with_object` suffices: **-3**
- Not using Ruby's built-in `Enumerable` methods: **-5**
- Using `and` / `or` instead of `&&` / `||` for control flow: **-5**
- Monkey-patching core classes without compelling reason: **-8**
- Method exceeding 20 lines: **-5**

**Axis 2 — Correctness & Explicit Contracts**:

- Rescuing `Exception` instead of `StandardError`: **-8**
- Silencing exceptions with empty `rescue`: **-8**
- Missing `freeze` on string constants: **-3**
- No input validation in public methods: **-5**
- Missing Sorbet/RBS type signatures on public API (if project uses them): **-3**

**Axis 3 — Runtime Robustness & Resource Discipline**:

- File opened without block form (`File.open` without block): **-8**
- Using `Thread.new` without join/exception handling: **-8**
- `puts` / `p` instead of logger: **-3**
- Missing `ensure` block for cleanup: **-5**
- Global variable mutation: **-8**

**Axis 4 — Architecture & Design Integrity**:

- God class (>300 lines): **-5**
- Circular `require`: **-10**
- Service object without clear single responsibility: **-5**
- Missing dependency injection (hard-coded class references): **-5**

### C / C++

**Axis 1 — Idiomatic Clarity & Simplicity**:

- (C++) Using raw pointers when smart pointers (`unique_ptr`, `shared_ptr`) apply: **-8**
- (C++) Using C-style casts instead of `static_cast` / `dynamic_cast`: **-5**
- (C) Magic numbers without named constants: **-3**
- (C++) Not using range-based `for` when applicable: **-3**
- Overly complex macro when `inline` function or `constexpr` works: **-5**

**Axis 2 — Correctness & Explicit Contracts**:

- Missing `const` correctness on parameters/methods: **-5**
- Unchecked return value from system call / allocation: **-8**
- (C++) Missing `noexcept` on move operations: **-5**
- Missing bounds checking on array/buffer access: **-8**
- Implicit conversion that may lose data: **-5**

**Axis 3 — Runtime Robustness & Resource Discipline (+ Memory & Lifetime Safety)**:

- `malloc` without corresponding `free` (or mismatched `new`/`delete`): **-10**
- Buffer overflow risk (e.g., `strcpy` instead of `strncpy` or `snprintf`): **-10**
- Use-after-free or dangling pointer: **-10**
- (C++) Resource acquisition without RAII wrapper: **-8**
- Missing null check after allocation: **-5**
- Data race (shared mutable state without synchronization): **-10**

**Axis 4 — Architecture & Design Integrity**:

- Header file exposing implementation details: **-5**
- (C++) God class (>1000 lines): **-5**
- Circular `#include` dependency: **-10**
- (C) Module with >50 public functions: **-5**
