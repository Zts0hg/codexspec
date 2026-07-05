# Commands

This is the reference for CodexSpec's slash commands. These commands are invoked in Claude Code's chat interface.

For workflow patterns and when to use each command, see [Workflow](workflow.md). For CLI commands, see [CLI](../reference/cli.md).

## Quick Reference

Grouped by category, mirroring the README catalog. Within each group, commands appear in workflow order.

### Core Workflow Commands

| Command | Purpose |
|---------|---------|
| `/codexspec:constitution` | Create or update project constitution with cross-artifact validation |
| `/codexspec:specify` | Clarify, confirm, and persist requirements in `requirements.md` |
| `/codexspec:generate-spec` | Generate `spec.md` document from clarified requirements (★ Auto-review) |
| `/codexspec:spec-to-plan` | Convert specification to technical implementation plan (★ Auto-review) |
| `/codexspec:plan-to-tasks` | Break down plan into traceable, verifiable tasks (★ Auto-review) |
| `/codexspec:implement-tasks` | Execute tasks with conditional TDD workflow |

### Review Commands (Quality Gates)

| Command | Purpose |
|---------|---------|
| `/codexspec:review-spec` | Validate specification for completeness and quality |
| `/codexspec:review-plan` | Review technical plan for feasibility and alignment |
| `/codexspec:review-tasks` | Validate task coverage, ordering, and feasibility |

### Enhancement Commands

| Command | Purpose |
|---------|---------|
| `/codexspec:config` | Manage project configuration interactively (create/view/modify/reset) |
| `/codexspec:clarify` | Scan existing spec for ambiguities (4 categories, max 5 questions) |
| `/codexspec:analyze` | Cross-artifact consistency analysis (read-only, severity-based) |
| `/codexspec:checklist` | Generate requirements quality checklists |
| `/codexspec:tasks-to-issues` | Convert tasks to GitHub Issues |

### Git Workflow Commands

| Command | Purpose |
|---------|---------|
| `/codexspec:commit-staged` | Generate commit message from staged changes (session-context aware) |
| `/codexspec:pr` | Generate PR/MR description from git diff (auto-detects platform) |

### Code Review Commands

| Command | Purpose |
|---------|---------|
| `/codexspec:review-code` | Review code in any language (idiomatic clarity, correctness, robustness, architecture) |
| `/codexspec:review-python-code` | Review Python code (PEP 8, type safety, robustness, constitution consistency) |
| `/codexspec:review-react-code` | Review React/TypeScript code (component architecture, Hooks rules, state, performance) |

### Fast Track

| Command | Purpose |
|---------|---------|
| `/codexspec:quick` | Run a streamlined Requirements-First SDD flow for small changes |

---

## Command Categories

### Core Workflow Commands

Commands for the primary Requirements-First SDD workflow: Constitution → Confirmed Requirements → Specification → Plan → Tasks → Implementation. Confirmed requirements are the highest-priority authority here — nothing in the chain is binding until you explicitly confirm it at the Confirmation Gate.

### Review Commands (Quality Gates)

Commands that validate artifacts at each workflow stage under an **evidence-based review** contract: every defect must include concrete `Evidence`, `Location`, `Mismatch`, `Impact`, and `Remediation`. Advisory design suggestions are reported separately and never change status or trigger automatic changes. Verified defects may be fixed and re-reviewed for at most two rounds; advisories remain optional throughout.

### Enhancement Commands

Commands for iterative refinement, cross-artifact validation, configuration, and project management integration.

### Git Workflow Commands

Commands that turn finished work into shareable artifacts: commit messages from the staged diff and structured PR/MR descriptions from the branch diff.

### Code Review Commands

Commands that review source code (any language, Python-specific, React/TypeScript-specific) for idiomatic clarity, correctness, robustness, architecture, and constitution alignment. Findings use the same severity discipline as the artifact reviews: CRITICAL/HIGH issues must cite concrete evidence; LOW suggestions are advisory only.

### Fast Track

A streamlined command that runs the Requirements-First SDD flow end-to-end for small, well-bounded changes.

---

## Command Reference

### `/codexspec:constitution`

Create or update the project constitution. The constitution defines architectural principles, technology stack, code standards, and governance rules that guide all subsequent development decisions.

**Syntax:**

```
/codexspec:constitution [principles description]
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
You: /codexspec:constitution Focus on code quality, testing standards, and clean architecture

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

### `/codexspec:specify`

Clarify requirements through interactive Q&A, confirm the resulting summary, and persist it for later sessions.

**Syntax:**

```
/codexspec:specify [your idea or requirement]
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
- Assigns stable IDs to confirmed needs, constraints, decisions, exclusions, and open questions
- Records user evidence and a confirmation log
- Creates the feature workspace and `requirements.md`

**What it creates:**

```text
.codexspec/specs/{feature-id}-{feature-name}/requirements.md
```

Only confirmed items become authoritative requirements. Open questions remain explicitly open. This is the Confirmation Gate for requirements: nothing is binding until you explicitly confirm the final summary.

**Example:**

```text
You: /codexspec:specify I want to build a task management app

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
     Use /codexspec:generate-spec to create spec.md
```

**Tips:**

- Use for initial requirement exploration
- Don't worry about being complete—refinement is iterative
- Ask questions if the AI makes assumptions
- Review the summary before generating spec

---

### `/codexspec:generate-spec`

Generate the `spec.md` document from clarified requirements. This command acts as a "requirement compiler" that transforms your clarified requirements into a structured specification.

**Syntax:**

```
/codexspec:generate-spec
```

**Arguments:**

| Argument | Required | Description |
|----------|----------|-------------|
| Feature path | No | Explicit feature directory, `requirements.md`, or target `spec.md`; required when resolution is ambiguous |

**What it does:**

- Reads confirmed requirements from the selected feature workspace
- Supports legacy workspaces containing only `spec.md`, with an explicit traceability warning
- Generates comprehensive `spec.md` with:
  - Feature overview and goals
  - User stories with acceptance criteria
  - Functional requirements (REQ-XXX format)
  - Non-functional requirements (NFR-XXX format)
  - Edge cases and handling approaches
  - Out of scope items
- Adds `Sources` references back to requirement IDs
- Stops for user confirmation instead of resolving authority conflicts by assumption
- Automatically reviews and may repair evidence-backed defects for at most two rounds

**What it creates:**

```
.codexspec/
└── specs/
    └── 2026-0613-1200ab-task-management/
        └── spec.md
```

**Example:**

```text
You: /codexspec:generate-spec

AI:  Generating specification...

     ✓ Created .codexspec/specs/2026-0613-1200ab-task-management/spec.md

     Sections included:
     - Overview: Task management for small dev teams
     - 4 User Stories with acceptance criteria
     - 12 Functional Requirements (REQ-001 to REQ-012)
     - 3 Non-Functional Requirements (NFR-001 to NFR-003)
     - 5 Edge Cases documented
     - Out of Scope: Mobile apps, Enterprise SSO

     Next steps:
     - Review the spec with /codexspec:review-spec
     - Or proceed to /codexspec:spec-to-plan
```

**Tips:**

- Run after `/codexspec:specify` has clarified requirements
- Review the generated spec before proceeding
- Use `/codexspec:review-spec` for quality validation
- Edit spec.md directly if minor adjustments needed

---

### `/codexspec:clarify`

Scan an existing specification for ambiguities and gaps. Use this for iterative refinement after initial spec creation.

**Syntax:**

```
/codexspec:clarify [path_to_spec.md]
```

**Arguments:**

| Argument | Required | Description |
|----------|----------|-------------|
| `path_to_spec.md` | No | Path to spec file (auto-detected if not provided) |

**What it does:**

- Scans requirements and spec using focused ambiguity categories
- Asks targeted clarification questions (max 5)
- Updates `requirements.md` first after user confirmation, then synchronizes `spec.md`
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
You: /codexspec:clarify

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
- Integrates with `/codexspec:review-spec` findings
- Maximum 5 questions per session
- Run multiple times for complex specifications

---

### `/codexspec:spec-to-plan`

Convert the feature specification into a technical implementation plan. This is where you define **how** the feature will be built.

**Syntax:**

```
/codexspec:spec-to-plan [path_to_spec.md]
```

**Arguments:**

| Argument | Required | Description |
|----------|----------|-------------|
| `path_to_spec.md` | No | Path to spec file (auto-detected from `.codexspec/specs/` if not provided) |

**What it does:**

- Reads specification and constitution
- Includes only technical detail needed by confirmed requirements and repository constraints
- Checks applicable constitution rules without treating optional conventions as feature requirements
- Adds `Covers` links to specification requirements
- Documents technical decisions with rationale
- Stops when a decision would change confirmed intent

**What it creates:**

```
.codexspec/
└── specs/
    └── 2026-0613-1200ab-task-management/
        └── plan.md    # Technical implementation plan
```

**Example:**

```text
You: /codexspec:spec-to-plan Use Python FastAPI for backend, React for frontend, PostgreSQL for database

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
- Applicable constitution rules are mandatory; irrelevant template conventions are not
- Include relevant sections based on project type
- Review plan before proceeding to tasks

---

### `/codexspec:plan-to-tasks`

Break down the technical plan into actionable tasks with explicit coverage and verifiable outcomes.

**Syntax:**

```
/codexspec:plan-to-tasks [path_to_spec.md path_to_plan.md]
```

**Arguments:**

| Argument | Required | Description |
|----------|----------|-------------|
| `paths` | No | Paths to spec and plan (auto-detected if not provided) |

**What it does:**

- Creates tasks with one verifiable outcome; a task may touch multiple related files
- Uses test-first ordering only when required by the plan, constitution, confirmed needs, or risk
- Marks tasks `[P]` only when they are genuinely independent
- Specifies exact file paths for each task
- Adds `Covers` links to plan and requirement IDs

**What it creates:**

```
.codexspec/
└── specs/
    └── 2026-0613-1200ab-task-management/
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
You: /codexspec:plan-to-tasks

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

- Each task should produce one verifiable outcome and may touch tightly related files
- Test tasks precede implementation only when test-first is required
- `[P]` marks truly independent parallelizable tasks
- Review dependencies before implementation

---

### `/codexspec:implement-tasks`

Execute implementation tasks with conditional TDD workflow. Works through the task list systematically.

**Syntax:**

```
/codexspec:implement-tasks [tasks_path]
/codexspec:implement-tasks [spec_path plan_path tasks_path]
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
You: /codexspec:implement-tasks

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
- Run `/codexspec:review-tasks` first for validation

---

### `/codexspec:review-spec`

Validate the specification against confirmed requirements and its own internal quality.

**Syntax:**

```
/codexspec:review-spec [path_to_spec.md]
```

**Arguments:**

| Argument | Required | Description |
|----------|----------|-------------|
| `path_to_spec.md` | No | Path to spec file (auto-detected if not provided) |

**What it does:**

- Checks fidelity to confirmed `requirements.md` entries
- Checks internal consistency, clarity, and verifiability
- Treats a missing template section as a defect only when authoritative content requires it
- Requires each defect to include `Evidence`, `Location`, `Mismatch`, `Impact`, and `Remediation`
- Separates `Risk Advisories / Design Opportunities` from defects
- Generates status plus a compatibility score derived from classified findings

**Shared review contract:**

| Category | Meaning |
|----------|---------|
| Fidelity defect | Conflicts with or omits an authoritative source |
| Intrinsic defect | Internally contradictory, infeasible, or unverifiable |
| Advisory | Optional improvement without evidence of a current defect |

Status is `PASS`, `PASS_WITH_WARNINGS`, `NEEDS_REVISION`, or `BLOCKED`. Advisories never change status or score.

**Example:**

```text
You: /codexspec:review-spec

AI:  Overall Status: NEEDS_REVISION
     Compatibility Score: 79/100

     Warning SPEC-001
     Evidence: CON-002 requires a measurable response-time limit.
     Location: spec.md, REQ-006
     Mismatch: "Respond quickly" has no measurable threshold.
     Impact: Acceptance cannot be verified.
     Remediation: Ask the user to confirm a threshold, update requirements.md,
                  then synchronize REQ-006.

     Risk Advisories / Design Opportunities:
     - None
```

**Tips:**

- Run before `/codexspec:spec-to-plan`
- Treat `BLOCKED` and `NEEDS_REVISION` as not ready to proceed
- Do not promote advisories into requirements
- Re-run after making fixes

---

### `/codexspec:review-plan`

Review the technical implementation plan for fidelity, feasibility, and justified technical decisions.

**Syntax:**

```
/codexspec:review-plan [path_to_plan.md]
```

**Arguments:**

| Argument | Required | Description |
|----------|----------|-------------|
| `path_to_plan.md` | No | Path to plan file (auto-detected if not provided) |

**What it does:**

- Verifies `Covers` links and required spec coverage
- Checks applicable constitution rules and repository facts
- Flags unjustified complexity only when it creates a concrete cost or conflict
- Requires evidence fields for every defect and merges findings with the same root cause
- Reports optional architecture improvements as advisories
- Uses the shared status and compatibility-score contract

**Example:**

```text
You: /codexspec:review-plan

AI:  Overall Status: PASS
     Compatibility Score: 100/100
     Verified defects: none

     Risk Advisories / Design Opportunities:
     - A caching layer may become useful if production measurements exceed
       the confirmed latency target. It is not required by the current plan.
```

**Tips:**

- Run before `/codexspec:plan-to-tasks`
- Resolve evidence-backed defects before task generation
- Keep speculative architecture ideas in the advisory section
- Verify tech stack aligns with team skills

---

### `/codexspec:review-tasks`

Validate the task breakdown for coverage, verifiable outcomes, correct ordering, and feasible dependencies.

**Syntax:**

```
/codexspec:review-tasks [path_to_tasks.md]
```

**Arguments:**

| Argument | Required | Description |
|----------|----------|-------------|
| `path_to_tasks.md` | No | Path to tasks file (auto-detected if not provided) |

**What it does:**

- Checks all required plan items and requirements have task coverage
- Validates test-first ordering only where an authoritative source requires it
- Verifies each task has one outcome that can be checked
- Validates dependencies (no cycles, correct ordering)
- Reviews parallelization markers
- Validates file paths
- Requires evidence fields for every defect
- Reports optional process refinements as advisories
- Uses the shared status and compatibility-score contract

**Example:**

```text
You: /codexspec:review-tasks

AI:  Overall Status: NEEDS_REVISION
     Compatibility Score: 79/100

     Warning TASK-001
     Evidence: Task 2.5 declares a dependency on Task 2.4.
     Location: tasks.md, Task 2.5
     Mismatch: Task 2.5 is also marked [P].
     Impact: Parallel execution can start before its prerequisite completes.
     Remediation: Remove [P] or remove the dependency if the plan proves independence.
```

**Tips:**

- Run before `/codexspec:implement-tasks`
- Test-order findings are defects only when testing is required by an authoritative source
- Check parallelization markers are accurate
- Verify file paths match project structure

---

### `/codexspec:analyze`

Perform a non-destructive consistency analysis across requirements.md, spec.md, plan.md, and tasks.md. Identifies authority conflicts, traceability gaps, duplication, and missing coverage.

**Syntax:**

```
/codexspec:analyze
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
You: /codexspec:analyze

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

     Resolve CRITICAL issues before /codexspec:implement-tasks
```

**Tips:**

- Run after `/codexspec:plan-to-tasks`, before implementation
- CRITICAL issues should block implementation
- Read-only analysis—no files are modified
- Use findings to improve artifact quality

---

### `/codexspec:checklist`

Generate quality checklists for validating requirements completeness, clarity, and consistency. These are "unit tests for requirements writing."

**Syntax:**

```
/codexspec:checklist [focus_area]
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
You: /codexspec:checklist security

AI:  Generating security checklist...

     ✓ Created .codexspec/specs/2026-0613-1200ab-task-management/checklists/security.md

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

### `/codexspec:tasks-to-issues`

Convert tasks from `tasks.md` into GitHub issues for project tracking and collaboration.

**Syntax:**

```
/codexspec:tasks-to-issues
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
You: /codexspec:tasks-to-issues

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

### `/codexspec:commit-staged`

Generate a Conventional Commits compliant commit message based on staged git changes with session context awareness. This command understands your development session to generate meaningful commit messages.

**Syntax:**

```
/codexspec:commit-staged [-p]
```

**Arguments:**

| Argument | Required | Description |
|----------|----------|-------------|
| `-p` | No | Preview mode - display message without committing |

**What it does:**

- Executes `git diff --staged` to retrieve staged changes
- Analyzes changes and session context for intent understanding
- Follows Conventional Commits specification
- In execute mode (default): commits directly after generating message
- In preview mode (`-p`): displays message without committing
- Reports error if no staged changes exist

**Example:**

```text
You: /codexspec:commit-staged

AI:  Analyzing staged changes...

     Files staged:
     - src/auth/service.py
     - tests/test_auth.py

     Generated commit message:
     feat(auth): implement token refresh logic

     - Add refresh token generation
     - Include token expiration handling
     - Add tests for refresh flow

     Executing commit...

     ✓ Committed: def5678
```

**Preview Mode Example:**

```text
You: /codexspec:commit-staged -p

AI:  Preview mode - no commit will be executed

     Suggested commit message:
     feat(auth): implement token refresh logic

     - Add refresh token generation
     - Include token expiration handling
     - Add tests for refresh flow
```

**Tips:**

- Stage changes first with `git add`
- Only analyzes staged content - respects Git's two-stage commit workflow
- Considers session context for meaningful commit messages
- Use `-p` flag to preview before committing
- Follows Conventional Commits specification by default

---

### `/codexspec:review-code`

Review code in any language for idiomatic clarity, correctness, robustness, architecture, and constitution alignment.

**Syntax:**

```
/codexspec:review-code [path...]
```

**Arguments:**

| Argument | Required | Description |
|----------|----------|-------------|
| `path...` | No | One or more source files or directories to review (space-separated). Defaults to `src/` if omitted |

**What it does:**

- Detects the primary language(s) from file extensions and runs a per-language pass for mixed-language targets
- Runs static analysis tools when their config is present (`ruff`/`mypy`, `eslint`/`tsc`, `go vet`/`gofmt`, `cargo check`/`cargo clippy`, `shellcheck`); skips gracefully and reports degraded coverage otherwise
- Scores four dimensions: Idiomatic Clarity & Simplicity, Correctness & Explicit Contracts, Runtime Robustness & Resource Discipline, and Architecture & Design Integrity
- Injects mandatory subsections for detected frameworks (e.g., Hooks Compliance for React, Ownership & Borrowing for Rust, Goroutine & Context Discipline for Go, Memory & Lifetime Safety for C/C++, Execution Safety for Shell)
- Cross-references findings against `.codexspec/memory/constitution.md` when present; if absent, the constitution axis is dropped and its weight is redistributed
- Classifies findings by severity: CRITICAL, HIGH, MEDIUM, LOW (LOW suggestions are capped at a 5-point total deduction)

**Example:**

```text
You: /codexspec:review-code src/

AI:  # Code Review Report

     ## Summary
     - Overall Status: Needs Work
     - Quality Score: 78/100
     - Detected Language: Python

     ## Static Analysis Results
     | Tool   | Status | Issues | Details                |
     |--------|--------|--------|------------------------|
     | ruff   | Warn   | 3      | Unused imports, line length |
     | mypy   | Pass   | 0      | No type errors         |

     ## Detailed Findings
     ### Critical Issues (CRITICAL)
     - [ ] [CODE-001] src/auth/service.py:42 - bare `except Exception:` swallows the original cause
       Impact: Original error context is lost during debugging.
       Suggestion: narrow the exception and re-raise with `raise ... from err`.

     ### Suggestions (LOW)
     - [ ] [CODE-004] src/auth/service.py:120 - manual loop where a comprehension suffices

     ## Recommendations
     1. Priority 1: Fix CODE-001 before merge.
     2. Priority 2: Apply LOW suggestions opportunistically.
```

**Tips:**

- Pass multiple paths to review a focused slice, e.g., `src/ tests/`
- The score is advisory; CRITICAL/HIGH findings are the actionable signal
- For Python-only or React-only projects, prefer the dedicated `/codexspec:review-python-code` or `/codexspec:review-react-code` for deeper, language-specific checks
- Re-run after fixes to confirm the score recovers (≥ 95 expected once CRITICAL/HIGH issues are resolved)

---

### `/codexspec:review-python-code`

Review Python code for PEP 8 compliance, type safety, engineering robustness, and constitution consistency.

**Syntax:**

```
/codexspec:review-python-code [path...]
```

**Arguments:**

| Argument | Required | Description |
|----------|----------|-------------|
| `path...` | No | One or more Python files or directories to review (space-separated). Defaults to `src/` if omitted |

**What it does:**

- Runs `ruff check` for PEP 8 / linting results and `mypy` for type-checking results
- Reviews four Python-specific dimensions: Pythonic & KISS Principle, Type Safety & Explicitness, Engineering Robustness, and Constitution Alignment
- Checks type-annotation completeness, broad-exception handling, and `raise ... from err` context preservation
- Validates resource management (`with` context managers), async/await correctness, and structured `logging` discipline
- Cross-references findings against `.codexspec/memory/constitution.md` MUST/SHOULD principles when present
- Classifies findings by severity: CRITICAL (constitution MUST violations, logic bugs, security vulnerabilities), HIGH (type-safety gaps, ruff/mypy errors, resource leaks), MEDIUM (design/refactor opportunities, missing annotations), LOW (readability, Pythonic sugar)

**Example:**

```text
You: /codexspec:review-python-code src/codexspec/

AI:  # Python Code Review Report

     ## Static Analysis
     | Tool  | Status | Issues |
     |-------|--------|--------|
     | ruff  | Pass   | 0      |
     | mypy  | Pass   | 0      |

     ## Findings
     ### Warnings (HIGH)
     - [ ] [CODE-002] src/codexspec/__init__.py:218 - public function missing return type annotation
       Suggestion: add the return type and verify with mypy.

     ### Suggestions (LOW)
     - [ ] [CODE-004] src/codexspec/cli.py:140 - use `pathlib.Path` instead of `os.path` string concatenation
```

**Tips:**

- Use instead of `/codexspec:review-code` when the target is Python-only and you want the PEP 8 / type-safety depth
- Both `ruff` and `mypy` must be installed and configured in the target project for full coverage; the command reports degraded coverage when they are absent
- Constitution MUST principles are scored; language-agnostic meta-principles (testability, simplicity) apply when no constitution exists

---

### `/codexspec:review-react-code`

Review React/TypeScript code for component architecture, Hooks rules, state management, performance, and constitution consistency.

**Syntax:**

```
/codexspec:review-react-code [path...]
```

**Arguments:**

| Argument | Required | Description |
|----------|----------|-------------|
| `path...` | No | One or more React/TypeScript files or directories to review (space-separated; expects `.tsx`, `.ts`, `.jsx`, `.js`). Defaults to `src/` if omitted |

**What it does:**

- Runs `npx eslint` (when an ESLint config exists) and `npx tsc --noEmit` (when a `tsconfig.json` exists)
- Reviews four React-specific dimensions: Component Atomicity & Single Responsibility, Hooks Compliance & Side-Effects Management, State Management & Data Flow, and Performance & Robustness
- Verifies `useEffect` dependency arrays are exhaustive, detects derived-state-as-state misuse, and flags unnecessary effects
- Checks for stale-closure risks, missing effect cleanup, prop drilling, unmemoized expensive renders, and missing loading/error states
- Cross-references findings against `.codexspec/memory/constitution.md` when present
- Classifies findings by severity: CRITICAL (Hooks-of violations, race conditions), HIGH (missing cleanup, unhandled promise rejections), MEDIUM (refactor candidates), LOW (readability)

**Example:**

```text
You: /codexspec:review-react-code src/components/

AI:  # React Code Review Report

     ## Static Analysis
     | Tool  | Status | Issues |
     |-------|--------|--------|
     | eslint| Warn   | 2      |
     | tsc   | Pass   | 0      |

     ## Findings
     ### Critical Issues (CRITICAL)
     - [ ] [CODE-001] src/components/UserProfile.tsx:38 - `useEffect` missing `userId` in dependency array
       Impact: stale closure fetches the wrong user after navigation.
       Suggestion: add `userId` to the dependency array or extract to a custom hook.

     ### Suggestions (LOW)
     - [ ] [CODE-004] src/components/Button.tsx:12 - extract derived value instead of `useState`
```

**Tips:**

- Use instead of `/codexspec:review-code` when the target is React/TypeScript-only and you want Hooks/component-architecture depth
- Both ESLint and a `tsconfig.json` should be present for full coverage; the command reports degraded coverage when they are absent
- React findings layer on top of the base TypeScript checks, so type-safety issues are still surfaced

---

### `/codexspec:quick`

Run a streamlined Requirements-First SDD flow for small changes.

**Syntax:**

```
/codexspec:quick [describe a small requirement]
```

**Arguments:**

| Argument | Required | Description |
|----------|----------|-------------|
| `describe a small requirement` | No | Short description of the small, well-bounded change (you will be prompted if not provided) |

**What it does:**

- Assesses scope (files touched, module span, new dependencies, unresolved product decisions) and, if the change is broad or has multiple independent outcomes, recommends the standard flow
- Creates a feature workspace and `requirements.md` using the same timestamp convention as `/codexspec:specify`
- Resolves only ambiguities that materially change implementation; presents a concise confirmed summary (`NEED-*`, relevant `CON-*`/`DEC-*`, `OUT-*`, unresolved `OPEN-*`)
- Holds at the Confirmation Gate: nothing is generated until you confirm the summary
- Chains the generation commands against the new feature directory: `/codexspec:generate-spec`, `/codexspec:spec-to-plan`, `/codexspec:plan-to-tasks`, `/codexspec:implement-tasks`
- Defers to each generation command's own auto-review loop; pauses and asks the user if a review needs a new product or architecture decision
- Reports the feature directory, artifact paths, review outcomes, implementation verification, and unresolved advisories separately

**What it creates:**

```text
.codexspec/specs/{timestamp}-{feature-name}/
├── requirements.md
├── spec.md
├── plan.md
└── tasks.md
```

**Example:**

```text
You: /codexspec:quick Add a "remember me" checkbox to the login form

AI:  Scope check: 1 component, 1 form field, no new dependencies. Quick is appropriate.

     Confirmed requirements:
     - NEED-1: "Remember me" checkbox on the login form (default unchecked)
     - DEC-1: Persist a long-lived refresh token only when checked
     OUT-1: SSO / social login (unchanged)

     Confirm this summary to start the automated flow. [y/N]

You: y

AI:  Running generate-spec → spec-to-plan → plan-to-tasks → implement-tasks ...

     ✓ Feature dir: .codexspec/specs/2026-0713-0915ab-remember-me/
     ✓ All reviews PASS_WITH_WARNINGS or higher
     ✓ Implementation verified
     Open advisories: none
```

**Tips:**

- Reserve Quick for genuinely small, single-outcome changes; otherwise run `/codexspec:specify` and the standard flow
- Confirmation is still required — Quick never infers a product decision to keep automation moving
- If any generation review returns `NEEDS_REVISION`/`BLOCKED`, Quick stops and hands control back to you

---

### `/codexspec:pr`

Generate a structured GitHub Pull Request / GitLab Merge Request description from the git diff. Optionally integrates `spec.md` for SDD-traced context.

**Syntax:**

```
/codexspec:pr [--target-branch <branch>] [--sections <list>] [--spec <id-or-path>] [--output <file>]
```

**Arguments:**

| Argument | Required | Description |
|----------|----------|-------------|
| `--target-branch <branch>` | No | Branch to compare against (default: `origin/main`) |
| `--sections <list>` | No | Comma-separated subset of `summary, changes, testing, verify, checklist, notes` (default: `all`) |
| `--spec <id-or-path>` | No | Opt-in spec integration: a feature id (e.g., `2025-0321-1430k7-auth`) resolved under `.codexspec/specs/`, or an explicit `path/to/spec.md`. Omit to generate from git only |
| `--output <file>` | No | Save the description to a file instead of the terminal |

**What it does:**

- Collects git context (current branch, remote URL, commits ahead, file changes, full diff, commit messages) against the target branch
- Auto-detects the platform from the remote URL: GitHub → "Pull Request", GitLab → "Merge Request", other/none → defaults to GitHub terminology with a warning
- Loads `.codexspec/memory/constitution.md` when present and aligns the description with documentation/code-review standards
- Honors `language.commit` (then `language.output`, then English) for the description language; technical terms (API, JWT, PR, MR) stay in English where appropriate
- When `--spec` is provided, adds a Context section with user stories and requirements pulled from spec.md; otherwise generates purely from the diff
- Emits sections per `--sections` (Summary, Changes, Testing, Verification Steps, Pre-merge Checklist, Notes / Breaking Changes)

**Example:**

```text
You: /codexspec:pr --spec 2026-0613-1200ab-task-management

AI:  Generating Pull Request description...

     Platform: GitHub (github.com/example/taskman)
     Branch:   feature/task-management  →  origin/main
     Commits:  8 ahead

     ## Pull Request: Task management for small dev teams

     ### Context
     - User stories and REQ-* pulled from spec.md

     ### Summary
     - Adds task CRUD, sub-tasks, and real-time updates

     ### Changes
     - src/taskman/models/task.py (new)
     - src/taskman/api/tasks.py (new)
     - ...

     ### Verification Steps
     1. `uv run pytest`
     2. `uv run codexspec check`
```

**Tips:**

- Skip `--spec` for small bug fixes or changes with no formal specification
- Combine with `/codexspec:commit-staged` to produce both a commit message and a PR description from the same work
- See the [PR description generator case study](../case-studies/case-study-pr-description-generator.md) for a worked, end-to-end example of this command (including how spec.md context is wired in)

---

### `/codexspec:config`

Manage project configuration interactively (create/view/modify/reset). This is the slash-command counterpart to the `codexspec config` CLI, ideal for Plugin Marketplace installs.

**Syntax:**

```
/codexspec:config [--view]
```

**Arguments:**

| Argument | Required | Description |
|----------|----------|-------------|
| `--view` | No | Display the current configuration without modifying it. With no arguments, opens the interactive management menu |

**What it does:**

- Targets `.codexspec/config.yml` exclusively
- `--view` (or the "View current config" menu option) prints the file in a readable format; reports "Configuration Not Found" if absent
- Interactive mode, when a config exists, offers: View, Modify, Reset to defaults, Cancel
- If no config exists, runs the creation flow that writes a minimal, `output`-only config (interaction/document/commit resolve to `output`, then `en`, so an `output`-only file is fully functional)
- Lets you set each language dimension independently (output, interaction, document, commit) and toggle workflow options such as `auto_next`

**What it creates/edits:**

```
.codexspec/config.yml
```

**Example:**

```text
You: /codexspec:config

AI:  ## Configuration Manager

     Configuration file found at .codexspec/config.yml.
     What would you like to do?
     - View current config
     - Modify config
     - Reset to defaults
     - Cancel

You: Modify config

AI:  Select a dimension to change:
     - Output language (base)
     - Interaction language
     - Document language
     - Commit-message language
     - workflow.auto_next

You: Output language (base) → zh-CN

AI:  ✓ Updated language.output: "zh-CN"
     (interaction and document fall back to output, then en.)
```

**Tips:**

- Use `/codexspec:config --view` to inspect the current state before changing anything
- A fresh or reset config writes only `output`; set `interaction`/`document` only when they should differ from `output`
- For scripted changes in a terminal, prefer the `codexspec config` CLI (`--set-lang`, `--set-interaction-lang`, `--set-document-lang`, `--set-commit-lang`, `--auto-next`)

---

## Workflow Overview

```text
Idea → /specify → requirements.md → /generate-spec → spec.md → /spec-to-plan → plan.md → /plan-to-tasks → tasks.md → /implement
                                                   │                         │                            │
                                              Review spec               Review plan                  Review tasks
```

Each review is a human checkpoint. It validates fidelity and intrinsic quality using evidence-backed findings. Advisory design suggestions remain separate and never block progression. Verified defects may be fixed and re-reviewed for at most two rounds.

---

## Troubleshooting

### "Feature directory not found"

The command couldn't locate the feature directory.

**Solutions:**

- Run `codexspec init` first to initialize the project
- Check that `.codexspec/specs/` directory exists
- Verify you're in the correct project directory
- Pass an explicit feature directory or artifact path when multiple candidates exist

### "No spec.md found"

The specification file doesn't exist yet.

**Solutions:**

- Run `/codexspec:specify` to clarify requirements first
- Then run `/codexspec:generate-spec` to create spec.md

### "Constitution not found"

No project constitution exists.

**Solutions:**

- Run `/codexspec:constitution` to create one
- Constitution is optional but recommended for consistent decisions

### "Tasks file not found"

The tasks breakdown doesn't exist.

**Solutions:**

- Ensure you've run `/codexspec:spec-to-plan` first
- Then run `/codexspec:plan-to-tasks` to create tasks.md

### "GitHub CLI not authenticated"

The `/codexspec:tasks-to-issues` command requires GitHub authentication.

**Solutions:**

- Install GitHub CLI: `brew install gh` (macOS) or equivalent
- Authenticate: `gh auth login`
- Verify: `gh auth status`

---

## Next Steps

- [Workflow](workflow.md) - Common patterns and when to use each command
- [CLI](../reference/cli.md) - Terminal commands for project initialization
