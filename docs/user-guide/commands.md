# Commands

This is the reference for CodexSpec's slash commands. These commands are invoked in Claude Code's chat interface.

For workflow patterns and when to use each command, see [Workflow](workflow.md). For CLI commands, see [CLI](../reference/cli.md).

## Quick Reference

| Command | Purpose |
|---------|---------|
| `/codexspec.constitution` | Create or update project constitution with cross-artifact validation |
| `/codexspec.specify` | Clarify requirements through interactive Q&A |
| `/codexspec.generate-spec` | Generate spec.md document from clarified requirements |
| `/codexspec.clarify` | Scan existing spec for ambiguities (iterative refinement) |
| `/codexspec.spec-to-plan` | Convert specification to technical implementation plan |
| `/codexspec.plan-to-tasks` | Break down plan into atomic, TDD-enforced tasks |
| `/codexspec.implement-tasks` | Execute tasks with conditional TDD workflow |
| `/codexspec.review-spec` | Validate specification for completeness and quality |
| `/codexspec.review-plan` | Review technical plan for feasibility and alignment |
| `/codexspec.review-tasks` | Validate task breakdown for TDD compliance |
| `/codexspec.analyze` | Cross-artifact consistency analysis (read-only) |
| `/codexspec.checklist` | Generate requirements quality checklists |
| `/codexspec.tasks-to-issues` | Convert tasks to GitHub issues |
| `/codexspec.commit` | Generate Conventional Commits messages with session context |
| `/codexspec.commit-staged` | Generate commit message from staged changes |

---

## Command Categories

### Core Workflow Commands

Commands for the primary SDD workflow: Constitution → Specification → Plan → Tasks → Implementation.

### Review Commands (Quality Gates)

Commands that validate artifacts at each workflow stage. **Recommended before proceeding to the next stage.**

### Advanced Commands

Commands for iterative refinement, cross-artifact validation, and project management integration.

---

## Command Reference

### `/codexspec.constitution`

Create or update the project constitution. The constitution defines architectural principles, technology stack, code standards, and governance rules that guide all subsequent development decisions.

**Syntax:**
```
/codexspec.constitution [principles description]
```

**Arguments:**
| Argument | Required | Description |
|----------|----------|-------------|
| `principles description` | No | Description of principles to include (will be prompted if not provided) |

**What it does:**
- Creates `.codexspec/memory/constitution.md` if not exists
- Updates existing constitution with new principles
- Validates cross-artifact consistency with templates
- Generates Sync Impact Report showing changes and affected files
- Includes constitutionality review for dependent templates

**What it creates:**
```
.codexspec/
└── memory/
    └── constitution.md    # Project governance document
```

**Example:**
```text
You: /codexspec.constitution Focus on code quality, testing standards, and clean architecture

AI:  Creating constitution...

     ✓ Created .codexspec/memory/constitution.md
     Version: 1.0.0

     Sync Impact Report:
     - plan-template-*.md: ✅ aligned
     - spec-template-*.md: ✅ aligned
     - tasks-template-*.md: ✅ aligned

     Core Principles:
     1. Code Quality First
     2. Test-Driven Development
     3. Clean Architecture

     Suggested commit: docs: create constitution v1.0.0
```

**Tips:**
- Define principles early in the project for consistent decision-making
- Include both technical and process principles
- Review constitution before major feature development
- Constitution changes trigger cross-artifact validation

---

### `/codexspec.specify`

Clarify requirements through interactive Q&A. This command explores your initial idea without creating any files—you maintain full control.

**Syntax:**
```
/codexspec.specify [your idea or requirement]
```

**Arguments:**
| Argument | Required | Description |
|----------|----------|-------------|
| `your idea or requirement` | No | Initial description of what you want to build (will be prompted if not provided) |

**What it does:**
- Asks clarifying questions to understand your idea
- Explores edge cases you might not have considered
- Co-creates high-quality requirements through dialogue
- Focuses on "what" and "why", not technical implementation
- **Does NOT generate files** - you decide when to create documentation

**What it does NOT create:**
- No files are created during this command
- Requirements stay in conversation until you approve

**Example:**
```text
You: /codexspec.specify I want to build a task management app

AI:  Great! Let me help you clarify the requirements.

     First, who are the target users for this app?
     - Individual professionals
     - Small teams
     - Enterprise organizations
     - All of the above

You: Small teams, mainly software development teams

AI:  Got it. For small dev teams:
     - Do you need real-time collaboration features?
     - Should tasks support sub-tasks or just flat lists?
     - Any integration requirements (GitHub, Slack, etc.)?

You: Real-time is important. Sub-tasks yes. GitHub integration would be nice.

AI:  [Continues exploring requirements...]

     Summary of clarified requirements:
     - Target: Small dev teams (5-20 people)
     - Core: Tasks with sub-tasks, real-time updates
     - Integration: GitHub (optional)
     - Priority: Real-time collaboration > Sub-tasks > GitHub

     Ready to generate the spec document?
     Use /codexspec.generate-spec to create spec.md
```

**Tips:**
- Use for initial requirement exploration
- Don't worry about being complete—refinement is iterative
- Ask questions if the AI makes assumptions
- Review the summary before generating spec

---

### `/codexspec.generate-spec`

Generate the `spec.md` document from clarified requirements. This command acts as a "requirement compiler" that transforms your clarified requirements into a structured specification.

**Syntax:**
```
/codexspec.generate-spec
```

**Arguments:**
| Argument | Required | Description |
|----------|----------|-------------|
| None | - | Uses context from previous `/codexspec.specify` session |

**What it does:**
- Creates `.codexspec/specs/{NNN}-{feature-name}/` directory
- Generates comprehensive `spec.md` with:
  - Feature overview and goals
  - User stories with acceptance criteria
  - Functional requirements (REQ-XXX format)
  - Non-functional requirements (NFR-XXX format)
  - Edge cases and handling approaches
  - Out of scope items

**What it creates:**
```
.codexspec/
└── specs/
    └── 001-task-management/
        └── spec.md
```

**Example:**
```text
You: /codexspec.generate-spec

AI:  Generating specification...

     ✓ Created .codexspec/specs/001-task-management/spec.md

     Sections included:
     - Overview: Task management for small dev teams
     - 4 User Stories with acceptance criteria
     - 12 Functional Requirements (REQ-001 to REQ-012)
     - 3 Non-Functional Requirements (NFR-001 to NFR-003)
     - 5 Edge Cases documented
     - Out of Scope: Mobile apps, Enterprise SSO

     Next steps:
     - Review the spec with /codexspec.review-spec
     - Or proceed to /codexspec.spec-to-plan
```

**Tips:**
- Run after `/codexspec.specify` has clarified requirements
- Review the generated spec before proceeding
- Use `/codexspec.review-spec` for quality validation
- Edit spec.md directly if minor adjustments needed

---

### `/codexspec.clarify`

Scan an existing specification for ambiguities and gaps. Use this for iterative refinement after initial spec creation.

**Syntax:**
```
/codexspec.clarify [path_to_spec.md]
```

**Arguments:**
| Argument | Required | Description |
|----------|----------|-------------|
| `path_to_spec.md` | No | Path to spec file (auto-detected if not provided) |

**What it does:**
- Scans spec using 4 focused ambiguity categories
- Asks targeted clarification questions (max 5)
- Updates spec.md with clarification answers
- Integrates with review-spec findings if available

**Ambiguity Categories:**

| Category | What it Detects |
|----------|-----------------|
| **Completeness Gaps** | Missing sections, empty content, absent acceptance criteria |
| **Specificity Issues** | Vague terms ("fast", "scalable"), undefined constraints |
| **Behavioral Clarity** | Error handling gaps, undefined state transitions |
| **Measurability Problems** | Non-functional requirements without metrics |

**Example:**
```text
You: /codexspec.clarify

AI:  Scanning spec.md for ambiguities...

     Found issues in 3 categories.

     ## Question 1/5: Specificity

     **Context**: NFR-001 states "System should respond quickly"

     **Question**: What is the target response time?

     | Option | Description | Impact |
     |--------|-------------|--------|
     | A | < 100ms for all operations | High performance requirement |
     | B | < 500ms for reads, < 1s for writes | Balanced approach |
     | Custom | Provide a different answer | - |

     **Recommendation**: Option B - balanced for typical web app

You: B

AI:  ✓ Updated NFR-001: Response time < 500ms reads, < 1s writes
     Added to Clarifications section in spec.md
```

**Tips:**
- Use when spec.md exists but needs refinement
- Integrates with `/codexspec.review-spec` findings
- Maximum 5 questions per session
- Run multiple times for complex specifications

---

### `/codexspec.spec-to-plan`

Convert the feature specification into a technical implementation plan. This is where you define **how** the feature will be built.

**Syntax:**
```
/codexspec.spec-to-plan [path_to_spec.md]
```

**Arguments:**
| Argument | Required | Description |
|----------|----------|-------------|
| `path_to_spec.md` | No | Path to spec file (auto-detected from `.codexspec/specs/` if not provided) |

**What it does:**
- Reads specification and constitution
- Defines tech stack with version constraints
- Performs constitutionality review (mandatory if constitution exists)
- Creates architecture with module dependency graph
- Documents technical decisions with rationale
- Plans implementation phases

**What it creates:**
```
.codexspec/
└── specs/
    └── 001-task-management/
        └── plan.md    # Technical implementation plan
```

**Example:**
```text
You: /codexspec.spec-to-plan Use Python FastAPI for backend, React for frontend, PostgreSQL for database

AI:  Generating technical plan...

     Constitutionality Review:
     ✓ Clean Architecture: Modular design with clear boundaries
     ✓ TDD: Test-first approach enforced in phases
     ✓ Code Quality: Linting and type hints required

     Architecture:
     - Backend: FastAPI with layered architecture
     - Frontend: React with component structure
     - Database: PostgreSQL with migration strategy

     Module Dependency Graph:
     ┌─────────────┐
     │    API      │
     └──────┬──────┘
            │
     ┌──────▼──────┐
     │  Services   │
     └──────┬──────┘
            │
     ┌──────▼──────┐
     │    Data     │
     └─────────────┘

     ✓ Created plan.md
     5 Implementation Phases defined
```

**Tips:**
- Run after spec is reviewed and stable
- Constitutionality review is mandatory if constitution exists
- Include relevant sections based on project type
- Review plan before proceeding to tasks

---

### `/codexspec.plan-to-tasks`

Break down the technical plan into atomic, actionable tasks with TDD enforcement.

**Syntax:**
```
/codexspec.plan-to-tasks [path_to_spec.md path_to_plan.md]
```

**Arguments:**
| Argument | Required | Description |
|----------|----------|-------------|
| `paths` | No | Paths to spec and plan (auto-detected if not provided) |

**What it does:**
- Creates atomic tasks (one primary file per task)
- Enforces TDD: test tasks precede implementation tasks
- Marks parallelizable tasks with `[P]`
- Specifies exact file paths for each task
- Defines phase checkpoints

**What it creates:**
```
.codexspec/
└── specs/
    └── 001-task-management/
        └── tasks.md    # Task breakdown
```

**Task Structure:**
```markdown
### Task 2.1: Write Tests for Entity A [P]
- **Type**: Testing
- **Files**: `tests/test_entity_a.py`
- **Description**: Write unit tests for Entity A
- **Dependencies**: Task 1.3
- **Est. Complexity**: Low
```

**Example:**
```text
You: /codexspec.plan-to-tasks

AI:  Breaking down plan into tasks...

     ✓ Created tasks.md
     Total: 24 tasks
     Parallelizable: 8 tasks (33%)

     Phase 1: Foundation (4 tasks)
     Phase 2: Core Implementation - TDD (10 tasks)
     Phase 3: Integration (4 tasks)
     Phase 4: Interface Layer (3 tasks)
     Phase 5: Testing & Documentation (3 tasks)

     Execution Order:
     Phase 1 → [Phase 2 tasks in parallel groups] → Phase 3 → Phase 4 → Phase 5

     Checkpoints defined at each phase boundary.
```

**Tips:**
- Each task should involve only ONE primary file
- Test tasks always precede implementation tasks
- `[P]` marks truly independent parallelizable tasks
- Review dependencies before implementation

---

### `/codexspec.implement-tasks`

Execute implementation tasks with conditional TDD workflow. Works through the task list systematically.

**Syntax:**
```
/codexspec.implement-tasks [tasks_path]
/codexspec.implement-tasks [spec_path plan_path tasks_path]
```

**Arguments:**
| Argument | Required | Description |
|----------|----------|-------------|
| `tasks_path` | No | Path to tasks.md (auto-detected if not provided) |
| `spec_path plan_path tasks_path` | No | Explicit paths to all three documents |

**File Resolution:**
- **No arguments**: Auto-detect from `.codexspec/specs/`
- **One argument**: Treat as `tasks.md` path, derive others from same directory
- **Three arguments**: Explicit paths to spec.md, plan.md, and tasks.md

**What it does:**
- Reads tasks.md and identifies incomplete tasks
- Applies TDD workflow for code tasks:
  - **Red**: Write failing tests first
  - **Green**: Implement to pass tests
  - **Verify**: Run all tests
  - **Refactor**: Improve while keeping tests green
- Direct implementation for non-testable tasks (docs, config)
- Updates task checkboxes as work progresses
- Records blockers in issues.md if encountered

**TDD Workflow for Code Tasks:**
```
Red → Green → Verify → Refactor → Mark Complete
```

**Direct Implementation for Non-Testable:**
- Documentation files
- Configuration files
- Static assets
- Infrastructure files

**Example:**
```text
You: /codexspec.implement-tasks

AI:  Starting implementation...

     Loading context:
     - spec.md ✓
     - plan.md ✓
     - tasks.md ✓
     - constitution.md ✓

     Tech Stack: Python 3.11+ / FastAPI / PostgreSQL / pytest

     Working on Task 1.1: Setup Project Structure
     ✓ Created src/taskman/__init__.py
     ✓ Created pyproject.toml
     [x] Task 1.1 Complete

     Working on Task 2.1: Write Tests for Task Entity [P]
     ✓ Created tests/test_task.py
     Running tests... 5 passed (all expected failures)
     [x] Task 2.1 Complete

     Working on Task 2.2: Implement Task Entity
     ✓ Created src/taskman/models/task.py
     Running tests... 5 passed
     [x] Task 2.2 Complete

     ...
```

**Tips:**
- Can resume where left off if interrupted
- Blockers are recorded in issues.md
- Commits are made after significant tasks/phases
- Run `/codexspec.review-tasks` first for validation

---

### `/codexspec.review-spec`

Validate the specification for completeness, clarity, consistency, and readiness for technical planning.

**Syntax:**
```
/codexspec.review-spec [path_to_spec.md]
```

**Arguments:**
| Argument | Required | Description |
|----------|----------|-------------|
| `path_to_spec.md` | No | Path to spec file (auto-detected if not provided) |

**What it does:**
- Checks completeness of all required sections
- Evaluates clarity and specificity
- Verifies internal consistency
- Assesses testability of requirements
- Checks constitution alignment
- Generates scored review report

**Review Dimensions:**

| Dimension | Weight | What it Validates |
|-----------|--------|-------------------|
| Completeness | 25% | All sections present and substantive |
| Clarity | 25% | No vague language, single interpretations |
| Consistency | 20% | No internal contradictions |
| Testability | 20% | Requirements can be verified |
| Constitution Alignment | 10% | Aligns with project principles |

**Example:**
```text
You: /codexspec.review-spec

AI:  Reviewing specification...

     # Specification Review Report

     ## Summary
     - **Overall Status**: ⚠️ Needs Work
     - **Quality Score**: 72/100
     - **Readiness**: Needs Revision

     ## Section Analysis
     | Section | Status | Completeness | Quality |
     |---------|--------|--------------|---------|
     | Overview | ✅ | 100% | High |
     | Goals | ✅ | 100% | High |
     | User Stories | ⚠️ | 80% | Medium |
     | Functional Requirements | ✅ | 100% | High |
     | Non-Functional Requirements | ⚠️ | 50% | Medium |
     | Edge Cases | ❌ | 0% | N/A |

     ## Critical Issues (Must Fix)
     - [SPEC-001]: Edge Cases section is empty
       - Impact: May miss important failure scenarios
       - Suggestion: Document at least 3-5 edge cases

     ## Warnings (Should Fix)
     - [SPEC-002]: NFR-001 uses vague term "fast"
       - Impact: Cannot verify without metrics
       - Suggestion: Specify concrete response time

     ## Recommendations
     1. Add Edge Cases section with handling approaches
     2. Quantify non-functional requirements
     3. Add acceptance criteria to User Story 3

     Available follow-up:
     - /codexspec.clarify - to address ambiguities
     - /codexspec.spec-to-plan - if issues resolved
```

**Tips:**
- Run before `/codexspec.spec-to-plan`
- Address Critical issues before proceeding
- Warnings don't block but indicate risk
- Re-run after making fixes

---

### `/codexspec.review-plan`

Review the technical implementation plan for feasibility, architecture quality, and alignment with specification.

**Syntax:**
```
/codexspec.review-plan [path_to_plan.md]
```

**Arguments:**
| Argument | Required | Description |
|----------|----------|-------------|
| `path_to_plan.md` | No | Path to plan file (auto-detected if not provided) |

**What it does:**
- Verifies spec requirements have plan coverage
- Evaluates tech stack choices
- Assesses architecture decisions
- Validates implementation phases
- Checks constitution alignment
- Generates scored review report

**Review Dimensions:**

| Dimension | Weight | What it Validates |
|-----------|--------|-------------------|
| Spec Alignment | 30% | All requirements have implementation |
| Tech Stack | 15% | Appropriate technology choices |
| Architecture Quality | 25% | Sound design and patterns |
| Phase Planning | 15% | Logical and realistic phases |
| Constitution Alignment | 15% | Follows project principles |

**Example:**
```text
You: /codexspec.review-plan

AI:  Reviewing technical plan...

     # Plan Review Report

     ## Summary
     - **Overall Status**: ✅ Pass
     - **Quality Score**: 85/100
     - **Readiness**: Ready for Task Breakdown

     ## Spec Alignment
     | Requirement | Coverage | Status |
     |-------------|----------|--------|
     | REQ-001 to REQ-012 | ✅ Full | All covered |
     | US-001 to US-004 | ✅ Full | All covered |
     | NFR-001 to NFR-003 | ⚠️ Partial | Caching not detailed |

     ## Architecture Review
     Strengths:
     - Clean separation of concerns
     - Well-defined module boundaries
     - Appropriate design patterns

     Concerns:
     - Missing error handling strategy documentation

     ## Constitution Alignment
     | Principle | Compliance |
     |-----------|------------|
     | Clean Architecture | ✅ |
     | TDD | ✅ |
     | Code Quality | ✅ |

     Ready for /codexspec.plan-to-tasks
```

**Tips:**
- Run before `/codexspec.plan-to-tasks`
- Critical issues should be resolved
- Use to catch architecture problems early
- Verify tech stack aligns with team skills

---

### `/codexspec.review-tasks`

Validate the task breakdown for completeness, TDD compliance, correct ordering, and proper dependencies.

**Syntax:**
```
/codexspec.review-tasks [path_to_tasks.md]
```

**Arguments:**
| Argument | Required | Description |
|----------|----------|-------------|
| `path_to_tasks.md` | No | Path to tasks file (auto-detected if not provided) |

**What it does:**
- Checks all plan items have task coverage
- Validates TDD compliance (tests before implementation)
- Verifies task granularity (atomic, single-file focus)
- Validates dependencies (no cycles, correct ordering)
- Reviews parallelization markers
- Validates file paths

**Review Dimensions:**

| Dimension | Weight | What it Validates |
|-----------|--------|-------------------|
| Plan Coverage | 30% | All plan items have tasks |
| TDD Compliance | 25% | Test-first workflow enforced |
| Dependency & Ordering | 20% | Correct dependencies, no cycles |
| Task Granularity | 15% | Atomic, appropriate scope |
| Parallelization & Files | 10% | Correct markers and paths |

**Example:**
```text
You: /codexspec.review-tasks

AI:  Reviewing task breakdown...

     # Tasks Review Report

     ## Summary
     - **Overall Status**: ⚠️ Needs Work
     - **Quality Score**: 78/100
     - **Total Tasks**: 24
     - **Parallelizable**: 8 (33%)

     ## TDD Compliance
     | Component | Test Task | Test Before Impl | Status |
     |-----------|-----------|------------------|--------|
     | Task Entity | ✅ | ✅ | ✅ |
     | User Entity | ✅ | ✅ | ✅ |
     | TaskService | ❌ Missing | N/A | ❌ |

     ## TDD Violations
     - [TDD-001]: TaskService missing test task

     ## Dependency Issues
     - [DEP-001]: Task 2.5 marked [P] but depends on 2.4

     ## Recommendations
     1. Add test task for TaskService before implementation
     2. Fix parallelization marker on Task 2.5

     Fix issues before /codexspec.implement-tasks
```

**Tips:**
- Run before `/codexspec.implement-tasks`
- TDD violations are critical for code quality
- Check parallelization markers are accurate
- Verify file paths match project structure

---

### `/codexspec.analyze`

Perform a non-destructive cross-artifact consistency analysis across spec.md, plan.md, and tasks.md. Identifies inconsistencies, duplications, and coverage gaps.

**Syntax:**
```
/codexspec.analyze
```

**Arguments:**
| Argument | Required | Description |
|----------|----------|-------------|
| None | - | Analyzes the current feature's artifacts |

**What it does:**
- Detects duplications across artifacts
- Identifies ambiguities lacking measurable criteria
- Finds underspecified items
- Checks constitution alignment
- Maps requirement coverage to tasks
- Reports inconsistencies in terminology and ordering

**Severity Levels:**

| Level | Definition |
|-------|------------|
| **CRITICAL** | Constitution violation, missing core artifact, zero coverage |
| **HIGH** | Duplicate/conflicting requirement, ambiguous security attribute |
| **MEDIUM** | Terminology drift, missing non-functional coverage |
| **LOW** | Style/wording improvements |

**Example:**
```text
You: /codexspec.analyze

AI:  Analyzing artifacts...

     # Specification Analysis Report

     ## Coverage Summary
     | Requirement Key | Has Task? | Task IDs |
     |-----------------|-----------|----------|
     | REQ-001 | ✅ | 2.1, 2.2 |
     | REQ-002 | ✅ | 2.3, 2.4 |
     | REQ-003 | ❌ | None |

     ## Issues Found

     | ID | Category | Severity | Summary |
     |----|----------|----------|---------|
     | A1 | Coverage | CRITICAL | REQ-003 has no task coverage |
     | A2 | Duplication | HIGH | REQ-005 and REQ-008 overlap |
     | A3 | Ambiguity | MEDIUM | NFR-002 "secure" not defined |

     ## Metrics
     - Total Requirements: 12
     - Total Tasks: 24
     - Coverage: 92% (11/12 requirements)
     - Critical Issues: 1

     ## Next Actions
     1. Add tasks for REQ-003 (CRITICAL)
     2. Consider merging REQ-005 and REQ-008
     3. Define "secure" in NFR-002

     Resolve CRITICAL issues before /codexspec.implement-tasks
```

**Tips:**
- Run after `/codexspec.plan-to-tasks`, before implementation
- CRITICAL issues should block implementation
- Read-only analysis—no files are modified
- Use findings to improve artifact quality

---

### `/codexspec.checklist`

Generate quality checklists for validating requirements completeness, clarity, and consistency. These are "unit tests for requirements writing."

**Syntax:**
```
/codexspec.checklist [focus_area]
```

**Arguments:**
| Argument | Required | Description |
|----------|----------|-------------|
| `focus_area` | No | Domain focus (e.g., "ux", "api", "security", "performance") |

**What it does:**
- Generates checklists organized by quality dimensions
- Creates checklists in `FEATURE_DIR/checklists/` directory
- Items focus on requirement quality, not implementation testing

**Quality Dimensions:**
- **Requirement Completeness**: Are all necessary requirements present?
- **Requirement Clarity**: Are requirements specific and unambiguous?
- **Requirement Consistency**: Do requirements align without conflicts?
- **Acceptance Criteria Quality**: Are success criteria measurable?
- **Scenario Coverage**: Are all flows/cases addressed?
- **Edge Case Coverage**: Are boundary conditions defined?
- **Non-Functional Requirements**: Performance, Security, Accessibility specified?
- **Dependencies & Assumptions**: Are they documented?

**Example Checklist Types:**
- `ux.md` - Visual hierarchy, interaction states, accessibility
- `api.md` - Error formats, rate limiting, authentication
- `security.md` - Data protection, threat model, breach response
- `performance.md` - Metrics, load conditions, degradation

**Example:**
```text
You: /codexspec.checklist security

AI:  Generating security checklist...

     ✓ Created .codexspec/specs/001-task-management/checklists/security.md

     ## Security Requirements Quality Checklist

     ### Authentication Requirements
     - [ ] CHK001 - Are authentication requirements defined for all protected endpoints? [Completeness]
     - [ ] CHK002 - Is password complexity explicitly specified? [Clarity]
     - [ ] CHK003 - Are session timeout requirements quantified? [Measurability]

     ### Data Protection
     - [ ] CHK004 - Are data encryption requirements specified at rest? [Completeness]
     - [ ] CHK005 - Are data encryption requirements specified in transit? [Completeness]
     - [ ] CHK006 - Is PII handling explicitly documented? [Clarity]

     Total: 15 items across 4 categories
```

**Tips:**
- Checklists validate requirement quality, not implementation correctness
- Use for requirements review and improvement
- Create domain-specific checklists for focused validation
- Run before proceeding to technical planning

---

### `/codexspec.tasks-to-issues`

Convert tasks from `tasks.md` into GitHub issues for project tracking and collaboration.

**Syntax:**
```
/codexspec.tasks-to-issues
```

**Arguments:**
| Argument | Required | Description |
|----------|----------|-------------|
| None | - | Converts all tasks from the current feature |

**What it does:**
- Parses task IDs, descriptions, dependencies, and file paths
- Creates GitHub issues with structured body
- Adds labels based on task type (setup, implementation, testing, documentation)
- Links dependencies between issues
- Reports created issues with URLs

**Prerequisites:**
- Git repository with GitHub remote
- GitHub CLI (`gh`) installed and authenticated
- `tasks.md` file exists

**Example:**
```text
You: /codexspec.tasks-to-issues

AI:  Converting tasks to GitHub issues...

     Repository: github.com/example/taskman

     Creating issues:
     ✓ #42: Task 1.1 - Setup Project Structure (setup)
     ✓ #43: Task 2.1 - Write Tests for Task Entity (testing)
     ✓ #44: Task 2.2 - Implement Task Entity (implementation)
     ...

     Summary:
     - Issues created: 24
     - Labels applied: setup(4), implementation(12), testing(5), documentation(3)
     - Dependencies linked: 18

     View issues: https://github.com/example/taskman/issues
```

**Tips:**
- Requires GitHub CLI authentication (`gh auth login`)
- Only works with GitHub repositories
- Creates issues in the repository's default configuration
- Check for duplicates before running

---

### `/codexspec.commit`

Generate a Conventional Commits compliant commit message based on git status and session context. This command is context-aware and handles different git states.

**Syntax:**
```
/codexspec.commit
```

**Arguments:**
| Argument | Required | Description |
|----------|----------|-------------|
| None | - | Analyzes current git state and session context |

**What it does:**
- Collects git context (branch, status, staged/unstaged changes)
- Analyzes session conversation history for intent understanding
- Follows priority logic based on git state:
  - **Staged changes exist**: Generate commit message from staged changes only
  - **No staged, but unstaged changes**: Suggest commit message with staging reminder
  - **No changes**: Report clean working directory
- Generates Conventional Commits compliant messages
- Confirms with user before executing commit

**Git State Handling:**

| State | Behavior |
|-------|----------|
| Staged changes | Generate message, confirm, commit |
| Unstaged only | Suggest message, remind to stage, ask if should stage all |
| Clean | Report "No changes detected" |

**Example:**
```text
You: /codexspec.commit

AI:  Analyzing git context...

     Branch: feature/add-auth
     Staged: 2 files
     Unstaged: 3 files

     Suggested commit message:
     feat(auth): add JWT authentication module

     - Implement token generation and validation
     - Add middleware for protected routes
     - Include unit tests for auth service

     Confirm commit? (y/n)

You: y

AI:  ✓ Committed: abc1234
```

**Tips:**
- More flexible than `/codexspec.commit-staged` - handles various git states
- Considers session context for meaningful commit messages
- Always confirms before committing
- For unstaged changes, provides clear reminder to stage first

---

### `/codexspec.commit-staged`

Generate a Conventional Commits compliant commit message based solely on staged git changes. This is a simpler, focused command for when you've already staged your changes.

**Syntax:**
```
/codexspec.commit-staged
```

**Arguments:**
| Argument | Required | Description |
|----------|----------|-------------|
| None | - | Analyzes staged changes only |

**What it does:**
- Executes `git diff --staged` to retrieve staged changes
- Analyzes changes and generates commit message
- Follows Conventional Commits specification
- Confirms with user before committing
- Reports error if no staged changes exist

**Example:**
```text
You: /codexspec.commit-staged

AI:  Analyzing staged changes...

     Files staged:
     - src/auth/service.py
     - tests/test_auth.py

     Suggested commit message:
     feat(auth): implement token refresh logic

     - Add refresh token generation
     - Include token expiration handling
     - Add tests for refresh flow

     Confirm commit? (y/n)

You: y

AI:  ✓ Committed: def5678
```

**Tips:**
- Stage changes first with `git add`
- Only analyzes staged content - ignores unstaged
- Simpler than `/codexspec.commit` when you know what you want to commit
- Use `/codexspec.commit` for more context-aware messages

---

## Workflow Overview

```
┌──────────────────────────────────────────────────────────────────────────┐
│                    CodexSpec Human-AI Collaboration Workflow              │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  1. Constitution  ──►  Define project principles                         │
│         │                         with cross-artifact validation         │
│         ▼                                                                │
│  2. Specify  ───────►  Interactive Q&A to clarify requirements           │
│         │               (no file created - human control)                │
│         ▼                                                                │
│  3. Generate Spec  ─►  Create spec.md document                           │
│         │                                                                │
│         ▼                                                                │
│  ╔═══════════════════════════════════════════════════════════════════╗   │
│  ║  ★ REVIEW GATE 1: /codexspec.review-spec ★                        ║   │
│  ║  Validate: Completeness, Clarity, Testability, Constitution       ║   │
│  ╚═══════════════════════════════════════════════════════════════════╝   │
│         │                                                                │
│         ▼                                                                │
│  4. Clarify  ───────►  Resolve ambiguities (iterative)                   │
│         │               4 targeted categories, max 5 questions           │
│         ▼                                                                │
│  5. Spec to Plan  ──►  Create technical plan with:                       │
│         │               • Constitutionality review (MANDATORY)           │
│         │               • Module dependency graph                        │
│         ▼                                                                │
│  ╔═══════════════════════════════════════════════════════════════════╗   │
│  ║  ★ REVIEW GATE 2: /codexspec.review-plan ★                        ║   │
│  ║  Validate: Spec Alignment, Architecture, Tech Stack, Phases        ║   │
│  ╚═══════════════════════════════════════════════════════════════════╝   │
│         │                                                                │
│         ▼                                                                │
│  6. Plan to Tasks  ─►  Generate atomic tasks with:                       │
│         │               • TDD enforcement (tests before impl)            │
│         │               • Parallel markers [P]                           │
│         │               • File path specifications                       │
│         ▼                                                                │
│  ╔═══════════════════════════════════════════════════════════════════╗   │
│  ║  ★ REVIEW GATE 3: /codexspec.review-tasks ★                       ║   │
│  ║  Validate: Coverage, TDD Compliance, Dependencies, Granularity     ║   │
│  ╚═══════════════════════════════════════════════════════════════════╝   │
│         │                                                                │
│         ▼                                                                │
│  7. Analyze  ───────►  Cross-artifact consistency check                  │
│         │               Detect gaps, duplications, constitution issues   │
│         ▼                                                                │
│  8. Implement  ─────►  Execute with conditional TDD workflow             │
│                          Code: Test-first | Docs/Config: Direct          │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
```

**Key Point**: Each review gate (★) is a **human checkpoint** where you validate AI output before investing more time. Skipping these gates often leads to costly rework.

---

## Troubleshooting

### "Feature directory not found"

The command couldn't locate the feature directory.

**Solutions:**
- Run `codexspec init` first to initialize the project
- Check that `.codexspec/specs/` directory exists
- Verify you're in the correct project directory

### "No spec.md found"

The specification file doesn't exist yet.

**Solutions:**
- Run `/codexspec.specify` to clarify requirements first
- Then run `/codexspec.generate-spec` to create spec.md

### "Constitution not found"

No project constitution exists.

**Solutions:**
- Run `/codexspec.constitution` to create one
- Constitution is optional but recommended for consistent decisions

### "Tasks file not found"

The tasks breakdown doesn't exist.

**Solutions:**
- Ensure you've run `/codexspec.spec-to-plan` first
- Then run `/codexspec.plan-to-tasks` to create tasks.md

### "GitHub CLI not authenticated"

The `/codexspec.tasks-to-issues` command requires GitHub authentication.

**Solutions:**
- Install GitHub CLI: `brew install gh` (macOS) or equivalent
- Authenticate: `gh auth login`
- Verify: `gh auth status`

---

## Next Steps

- [Workflow](workflow.md) - Common patterns and when to use each command
- [CLI](../reference/cli.md) - Terminal commands for project initialization
