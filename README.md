# CodexSpec

**English** | [中文](README.zh-CN.md) | [日本語](README.ja.md) | [Español](README.es.md) | [Português](README.pt-BR.md) | [한국어](README.ko.md) | [Deutsch](README.de.md) | [Français](README.fr.md)

[![PyPI version](https://img.shields.io/pypi/v/codexspec.svg)](https://pypi.org/project/codexspec/)
[![Python](https://img.shields.io/pypi/pyversions/codexspec.svg)](https://pypi.org/project/codexspec/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**A Spec-Driven Development (SDD) toolkit for Claude Code**

CodexSpec is a toolkit that helps you build high-quality software using a structured, specification-driven approach. It flips the script on traditional development by making specifications executable artifacts that directly guide implementation.

## Design Philosophy: Human-AI Collaboration

CodexSpec is built on the belief that **effective AI-assisted development requires active human participation at every stage**. The toolkit is designed around a core principle:

> **Review and validate each artifact before moving forward.**

### Why Human Oversight Matters

In AI-assisted development, skipping review stages leads to:

| Problem | Consequence |
|---------|-------------|
| Unclear requirements | AI makes assumptions that diverge from your intent |
| Incomplete specifications | Features get built without critical edge cases |
| Misaligned technical plans | Architecture doesn't match business needs |
| Vague task breakdowns | Implementation goes off-track, requiring expensive rework |

### The CodexSpec Approach

CodexSpec structures development into **reviewable checkpoints**:

```
Idea → Clarify → Review → Plan → Review → Tasks → Review → Analyze → Implement
              ↑              ↑              ↑
           Human checks    Human checks    Human checks
```

**Every artifact has a corresponding review command:**
- `spec.md` → `/codexspec.review-spec`
- `plan.md` → `/codexspec.review-plan`
- `tasks.md` → `/codexspec.review-tasks`
- All artifacts → `/codexspec.analyze`

This systematic review process ensures:
- **Early error detection**: Catch misunderstandings before code is written
- **Alignment verification**: Confirm AI's interpretation matches your intent
- **Quality gates**: Validate completeness, clarity, and feasibility at each stage
- **Reduced rework**: Invest minutes in review to save hours of reimplementation

## Features

### Core SDD Workflow
- **Constitution-Based**: Establish project principles that guide all subsequent decisions
- **Two-Phase Specification**: Interactive clarification (`/specify`) followed by document generation (`/generate-spec`)
- **Plan-Driven Development**: Technical choices come after requirements are validated
- **TDD-Ready Tasks**: Task breakdowns enforce test-first methodology

### Human-AI Collaboration
- **Review Commands**: Dedicated review commands for spec, plan, and tasks to validate AI output
- **Interactive Clarification**: Q&A-based requirement refinement with immediate feedback
- **Cross-Artifact Analysis**: Detect inconsistencies between spec, plan, and tasks before implementation
- **Quality Checklists**: Automated quality assessment for requirements

### Developer Experience
- **Claude Code Integration**: Native slash commands for Claude Code
- **Internationalization (i18n)**: Multi-language support via LLM dynamic translation
- **Cross-Platform**: Support for both Bash and PowerShell scripts
- **Extensible**: Plugin architecture for custom commands

## Installation

### Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) (recommended) or pip

### Option 1: Install with uv (Recommended)

The easiest way to install CodexSpec is using uv:

```bash
uv tool install codexspec
```

### Option 2: Install with pip

Alternatively, you can use pip:

```bash
pip install codexspec
```

### Option 3: One-time Usage

Run directly without installing:

```bash
# Create a new project
uvx codexspec init my-project

# Initialize in an existing project
cd your-existing-project
uvx codexspec init . --ai claude
```

### Option 4: Install from GitHub (Development Version)

For the latest development version or a specific branch:

```bash
# Using uv
uv tool install git+https://github.com/Zts0hg/codexspec.git

# Using pip
pip install git+https://github.com/Zts0hg/codexspec.git

# Specific branch or tag
uv tool install git+https://github.com/Zts0hg/codexspec.git@main
uv tool install git+https://github.com/Zts0hg/codexspec.git@v0.2.0
```

## Quick Start

After installation, you can use the CLI:

```bash
# Create new project
codexspec init my-project

# Create project with Chinese output
codexspec init my-project --lang zh-CN

# Initialize in existing project
codexspec init . --ai claude
# or
codexspec init --here --ai claude

# Check installed tools
codexspec check

# View version
codexspec version
```

To upgrade to the latest version:

```bash
# Using uv
uv tool install codexspec --upgrade

# Using pip
pip install --upgrade codexspec
```

## Usage

### 1. Initialize a Project

After [installation](#installation), create or initialize your project:

```bash
codexspec init my-awesome-project
# or in current directory
codexspec init . --ai claude
```

### 2. Establish Project Principles

Launch Claude Code in the project directory:

```bash
cd my-awesome-project
claude
```

Use the `/codexspec.constitution` command to create your project's governing principles:

```
/codexspec.constitution Create principles focused on code quality, testing standards, and clean architecture
```

### 3. Clarify Requirements

Use `/codexspec.specify` to **explore and clarify** your requirements through interactive Q&A:

```
/codexspec.specify I want to build a task management application
```

This command will:
- Ask clarifying questions to understand your idea
- Explore edge cases you might not have considered
- Co-create high-quality requirements through dialogue
- **NOT** generate files automatically - you stay in control

### 4. Generate Specification Document

Once requirements are clarified, use `/codexspec.generate-spec` to create the `spec.md` document:

```
/codexspec.generate-spec
```

This command acts as a "requirement compiler" that transforms your clarified requirements into a structured specification document.

### 5. Review Specification (Recommended)

**Before proceeding to planning, validate your specification:**

```
/codexspec.review-spec
```

This command generates a detailed review report with:
- Section completeness analysis
- Clarity and testability assessment
- Constitution alignment check
- Prioritized recommendations

### 6. Create a Technical Plan

Use `/codexspec.spec-to-plan` to define how to implement it:

```
/codexspec.spec-to-plan Use Python with FastAPI for the backend, PostgreSQL for the database, and React for the frontend
```

The command includes **constitutionality review** - verifying your plan aligns with project principles.

### 7. Review Plan (Recommended)

**Before breaking down into tasks, validate your technical plan:**

```
/codexspec.review-plan
```

This verifies:
- Specification alignment
- Architecture soundness
- Tech stack appropriateness
- Constitution compliance

### 8. Generate Tasks

Use `/codexspec.plan-to-tasks` to break down the plan:

```
/codexspec.plan-to-tasks
```

Tasks are organized into standard phases with:
- **TDD enforcement**: Test tasks precede implementation tasks
- **Parallel markers `[P]`**: Identify independent tasks
- **File path specifications**: Clear deliverables per task

### 9. Review Tasks (Recommended)

**Before implementation, validate task breakdown:**

```
/codexspec.review-tasks
```

This checks:
- Plan coverage
- TDD compliance
- Dependency correctness
- Task granularity

### 10. Analyze (Optional but Recommended)

Use `/codexspec.analyze` for cross-artifact consistency check:

```
/codexspec.analyze
```

This detects issues across spec, plan, and tasks:
- Coverage gaps (requirements without tasks)
- Duplication and inconsistencies
- Constitution violations
- Underspecified items

### 11. Implement

Use `/codexspec.implement-tasks` to execute the implementation:

```
/codexspec.implement-tasks
```

The implementation follows **conditional TDD workflow**:
- Code tasks: Test-first (Red → Green → Verify → Refactor)
- Non-testable tasks (docs, config): Direct implementation

## Available Commands

### CLI Commands

| Command | Description |
|---------|-------------|
| `codexspec init` | Initialize a new CodexSpec project |
| `codexspec check` | Check for installed tools |
| `codexspec version` | Display version information |
| `codexspec config` | View or modify project configuration |

### `codexspec init` Options

| Option | Description |
|--------|-------------|
| `PROJECT_NAME` | Name for your new project directory |
| `--here`, `-h` | Initialize in current directory |
| `--ai`, `-a` | AI assistant to use (default: claude) |
| `--lang`, `-l` | Output language (e.g., en, zh-CN, ja) |
| `--force`, `-f` | Force overwrite existing files |
| `--no-git` | Skip git initialization |
| `--debug`, `-d` | Enable debug output |

### `codexspec config` Options

| Option | Description |
|--------|-------------|
| `--set-lang`, `-l` | Set the output language |
| `--list-langs` | List all supported languages |

### Slash Commands

After initialization, these slash commands are available in Claude Code:

#### Core Workflow Commands

| Command | Description |
|---------|-------------|
| `/codexspec.constitution` | Create or update project constitution with cross-artifact validation and sync impact reporting |
| `/codexspec.specify` | **Clarify** requirements through interactive Q&A (no file generation) |
| `/codexspec.generate-spec` | **Generate** `spec.md` document after requirements are clarified |
| `/codexspec.spec-to-plan` | Convert specification to technical plan with constitutionality review and module dependency graph |
| `/codexspec.plan-to-tasks` | Break down plan into atomic, TDD-enforced tasks with parallel markers `[P]` |
| `/codexspec.implement-tasks` | Execute tasks with conditional TDD workflow (TDD for code, direct for docs/config) |

#### Review Commands (Quality Gates)

| Command | Description |
|---------|-------------|
| `/codexspec.review-spec` | Validate specification for completeness, clarity, consistency, and testability with scoring |
| `/codexspec.review-plan` | Review technical plan for feasibility, architecture quality, and constitution alignment |
| `/codexspec.review-tasks` | Validate task breakdown for plan coverage, TDD compliance, dependencies, and granularity |

#### Enhancement Commands

| Command | Description |
|---------|-------------|
| `/codexspec.clarify` | Scan existing spec.md for ambiguities using 4 focused categories, integrate with review findings |
| `/codexspec.analyze` | Non-destructive cross-artifact analysis (spec, plan, tasks) with severity-based issue detection |
| `/codexspec.checklist` | Generate quality checklists for requirements validation |
| `/codexspec.tasks-to-issues` | Convert tasks to GitHub issues for project management integration |

## Workflow Overview

```
┌──────────────────────────────────────────────────────────────────────────┐
│                    CodexSpec Human-AI Collaboration Workflow             │
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
│         │               4 focused categories, max 5 questions            │
│         ▼                                                                │
│  5. Spec to Plan  ──►  Create technical plan with:                       │
│         │               • Constitutionality review (MANDATORY)           │
│         │               • Module dependency graph                        │
│         ▼                                                                │
│  ╔═══════════════════════════════════════════════════════════════════╗   │
│  ║  ★ REVIEW GATE 2: /codexspec.review-plan ★                        ║   │
│  ║  Validate: Spec Alignment, Architecture, Tech Stack, Phases       ║   │
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
│  ║  Validate: Coverage, TDD Compliance, Dependencies, Granularity    ║   │
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

**Key Insight**: Each review gate (★) is a **human checkpoint** where you validate AI output before investing more time. Skipping these gates often leads to costly rework.

### Key Concept: Requirement Clarification Workflow

CodexSpec provides **two distinct clarification commands** for different stages of the workflow:

#### specify vs clarify: When to Use Which?

| Aspect | `/codexspec.specify` | `/codexspec.clarify` |
|--------|----------------------|----------------------|
| **Purpose** | Initial requirement exploration | Iterative refinement of existing spec |
| **When to Use** | Starting with a new idea, no spec.md exists | spec.md exists, need to fill gaps |
| **Input** | Your initial idea or requirement | Existing spec.md file |
| **Output** | None (dialogue only) | Updates spec.md with clarifications |
| **Method** | Open-ended Q&A | Structured ambiguity scan (4 categories) |
| **Question Limit** | Unlimited | Maximum 5 questions |
| **Typical Use** | "I want to build a todo app" | "The spec is missing error handling details" |

#### Two-Phase Specification

Before generating any documentation:

| Phase | Command | Purpose | Output |
|-------|---------|---------|--------|
| **Explore** | `/codexspec.specify` | Interactive Q&A to explore and refine requirements | None (dialogue only) |
| **Generate** | `/codexspec.generate-spec` | Compile clarified requirements into structured document | `spec.md` |

#### Iterative Clarification

After spec.md is created:

```
spec.md ──► /codexspec.clarify ──► Updated spec.md (with Clarifications section)
                │
                └── Scans for ambiguities in 4 focused categories:
                    • Completeness Gaps - Missing sections, empty content
                    • Specificity Issues - Vague terms, undefined constraints
                    • Behavioral Clarity - Error handling, state transitions
                    • Measurability Problems - Non-functional requirements without metrics
```

#### Benefits of This Design

- **Human-AI collaboration**: You actively participate in requirement discovery
- **Explicit control**: Files are only created when you decide
- **Quality focus**: Requirements are thoroughly explored before documentation
- **Iterative refinement**: Specs can be improved incrementally as understanding deepens

## Project Structure

After initialization, your project will have this structure:

```
my-project/
├── .codexspec/
│   ├── memory/
│   │   └── constitution.md    # Project governing principles
│   ├── specs/
│   │   └── {feature-id}/
│   │       ├── spec.md        # Feature specification
│   │       ├── plan.md        # Technical plan
│   │       ├── tasks.md       # Task breakdown
│   │       └── checklists/    # Quality checklists
│   ├── templates/             # Custom templates
│   ├── scripts/               # Helper scripts
│   │   ├── bash/              # Bash scripts
│   │   └── powershell/        # PowerShell scripts
│   └── extensions/            # Custom extensions
├── .claude/
│   └── commands/              # Slash commands for Claude Code
└── CLAUDE.md                  # Context for Claude Code
```

## Internationalization (i18n)

CodexSpec supports multiple languages through **LLM dynamic translation**. Instead of maintaining translated templates, we let Claude translate content at runtime based on your language configuration.

### Setting Language

**During initialization:**
```bash
# Create a project with Chinese output
codexspec init my-project --lang zh-CN

# Create a project with Japanese output
codexspec init my-project --lang ja
```

**After initialization:**
```bash
# View current configuration
codexspec config

# Change language setting
codexspec config --set-lang zh-CN

# List supported languages
codexspec config --list-langs
```

### Configuration File

The `.codexspec/config.yml` file stores language settings:

```yaml
version: "1.0"

language:
  # Output language for Claude interactions and generated documents
  output: "zh-CN"

  # Template language - keep as "en" for compatibility
  templates: "en"

project:
  ai: "claude"
  created: "2026-02-15"
```

### Supported Languages

| Code | Language |
|------|----------|
| `en` | English (default) |
| `zh-CN` | Chinese (Simplified) |
| `zh-TW` | Chinese (Traditional) |
| `ja` | Japanese |
| `ko` | Korean |
| `es` | Spanish |
| `fr` | French |
| `de` | German |
| `pt` | Portuguese |
| `ru` | Russian |
| `it` | Italian |
| `ar` | Arabic |
| `hi` | Hindi |

### How It Works

1. **Single English Templates**: All command templates remain in English
2. **Language Configuration**: Project specifies preferred output language
3. **Dynamic Translation**: Claude reads English instructions, outputs in target language
4. **Context-Aware**: Technical terms (JWT, OAuth, etc.) remain in English when appropriate

### Benefits

- **Zero Translation Maintenance**: No need to maintain multiple template versions
- **Always Up-to-Date**: Template updates automatically benefit all languages
- **Context-Aware Translation**: Claude provides natural, context-appropriate translations
- **Unlimited Languages**: Any language supported by Claude works immediately

## Extension System

CodexSpec supports a plugin architecture for adding custom commands:

### Extension Structure

```
my-extension/
├── extension.yml          # Extension manifest
├── commands/              # Custom slash commands
│   └── command.md
└── README.md
```

### Creating Extensions

1. Copy the template from `extensions/template/`
2. Modify `extension.yml` with your extension details
3. Add your custom commands in `commands/`
4. Test locally and publish

See `extensions/EXTENSION-DEVELOPMENT-GUIDE.md` for details.

## Development

### Prerequisites

- Python 3.11+
- uv package manager
- Git

### Local Development

```bash
# Clone the repository
git clone https://github.com/Zts0hg/codexspec.git
cd codexspec

# Install development dependencies
uv sync --dev

# Run locally
uv run codexspec --help

# Run tests
uv run pytest

# Lint code
uv run ruff check src/
```

### Building

```bash
# Build the package
uv build
```

## Comparison with spec-kit

CodexSpec is inspired by GitHub's spec-kit but with some key differences:

| Feature | spec-kit | CodexSpec |
|---------|----------|-----------|
| Core Philosophy | Spec-driven development | Spec-driven development + human-AI collaboration |
| CLI Name | `specify` | `codexspec` |
| Primary AI | Multi-agent support | Claude Code focused |
| Command Prefix | `/speckit.*` | `/codexspec.*` |
| Constitution System | Basic | Full constitution with cross-artifact validation |
| Two-Phase Spec | No | Yes (clarify + generate) |
| Review Commands | Optional | 3 dedicated review commands with scoring |
| Clarify Command | Yes | 4 focused categories, review integration |
| Analyze Command | Yes | Read-only, severity-based, constitution-aware |
| TDD in Tasks | Optional | Enforced (tests precede implementation) |
| Implementation | Standard | Conditional TDD (code vs docs/config) |
| Extension System | Yes | Yes |
| PowerShell Scripts | Yes | Yes |
| i18n Support | No | Yes (13+ languages via LLM translation) |

### Key Differentiators

1. **Review-First Culture**: Every major artifact has a dedicated review command
2. **Constitution Governance**: Principles are validated, not just documented
3. **TDD by Default**: Test-first methodology enforced in task generation
4. **Human Checkpoints**: Workflow designed around validation gates

## Philosophy

CodexSpec follows these core principles:

### SDD Fundamentals

1. **Intent-driven development**: Specifications define the "what" before the "how"
2. **Rich specification creation**: Use guardrails and organizational principles
3. **Multi-step refinement**: Rather than one-shot code generation
4. **Constitution governance**: Project principles guide all decisions

### Human-AI Collaboration

5. **Human-in-the-loop**: AI generates artifacts, humans validate them
6. **Review-oriented**: Validate each artifact before moving forward
7. **Progressive disclosure**: Complex information revealed incrementally
8. **Explicit over implicit**: Requirements should be clear, not assumed

### Quality Assurance

9. **Test-driven by default**: TDD workflow built into task generation
10. **Cross-artifact consistency**: Analyze spec, plan, and tasks together
11. **Constitution alignment**: All artifacts respect project principles

### Why Review Matters

| Without Review | With Review |
|---------------|-------------|
| AI makes incorrect assumptions | Human catches misinterpretations early |
| Incomplete requirements propagate | Gaps identified before implementation |
| Architecture drifts from intent | Alignment verified at each stage |
| Tasks miss critical functionality | Coverage validated systematically |
| **Result: Rework, wasted effort** | **Result: Right first time** |

## Contributing

Contributions are welcome! Please read our contributing guidelines before submitting a pull request.

## License

MIT License - see [LICENSE](LICENSE) for details.

## Acknowledgements

- Inspired by [GitHub spec-kit](https://github.com/github/spec-kit)
- Built for [Claude Code](https://claude.ai/code)
