# CodexSpec

[![PyPI version](https://img.shields.io/pypi/v/codexspec.svg)](https://pypi.org/project/codexspec/)
[![Python](https://img.shields.io/pypi/pyversions/codexspec.svg)](https://pypi.org/project/codexspec/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**A Spec-Driven Development (SDD) toolkit for Claude Code**

CodexSpec is a toolkit that helps you build high-quality software using a structured, specification-driven approach. It flips the script on traditional development by making specifications executable artifacts that directly guide implementation.

## Features

- **Structured Workflow**: Clear commands for each phase of development
- **Claude Code Integration**: Native slash commands for Claude Code
- **Constitution-Based**: Project principles guide all decisions
- **Specification-First**: Define what and why before how
- **Plan-Driven**: Technical choices come after requirements
- **Task-Oriented**: Break down implementation into actionable tasks
- **Quality Assurance**: Built-in review, analysis, and checklist commands
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
uv tool install git+https://github.com/Zts0hg/codexspec.git@v0.1.0
```

## Quick Start

After installation, you can use the CLI:

```bash
# Create new project
codexspec init my-project

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

### 3. Create a Specification

Use `/codexspec.specify` to define what you want to build:

```
/codexspec.specify Build a task management application with the following features: create tasks, assign to users, set due dates, and track progress
```

### 4. Clarify Requirements (Optional but Recommended)

Use `/codexspec.clarify` to resolve ambiguities before planning:

```
/codexspec.clarify
```

### 5. Create a Technical Plan

Use `/codexspec.spec-to-plan` to define how to implement it:

```
/codexspec.spec-to-plan Use Python with FastAPI for the backend, PostgreSQL for the database, and React for the frontend
```

### 6. Generate Tasks

Use `/codexspec.plan-to-tasks` to break down the plan:

```
/codexspec.plan-to-tasks
```

### 7. Analyze (Optional but Recommended)

Use `/codexspec.analyze` for cross-artifact consistency check:

```
/codexspec.analyze
```

### 8. Implement

Use `/codexspec.implement-tasks` to execute the implementation:

```
/codexspec.implement-tasks
```

## Available Commands

### CLI Commands

| Command | Description |
|---------|-------------|
| `codexspec init` | Initialize a new CodexSpec project |
| `codexspec check` | Check for installed tools |
| `codexspec version` | Display version information |

### `codexspec init` Options

| Option | Description |
|--------|-------------|
| `PROJECT_NAME` | Name for your new project directory |
| `--here`, `-h` | Initialize in current directory |
| `--ai`, `-a` | AI assistant to use (default: claude) |
| `--force`, `-f` | Force overwrite existing files |
| `--no-git` | Skip git initialization |
| `--debug`, `-d` | Enable debug output |

### Slash Commands

After initialization, these slash commands are available in Claude Code:

#### Core Commands

| Command | Description |
|---------|-------------|
| `/codexspec.constitution` | Create or update project governing principles |
| `/codexspec.specify` | Define what you want to build (requirements) |
| `/codexspec.generate-spec` | Generate detailed specification from requirements |
| `/codexspec.spec-to-plan` | Convert specification to technical plan |
| `/codexspec.plan-to-tasks` | Break down plan into actionable tasks |
| `/codexspec.implement-tasks` | Execute tasks according to breakdown |

#### Review Commands

| Command | Description |
|---------|-------------|
| `/codexspec.review-spec` | Review specification for completeness |
| `/codexspec.review-plan` | Review technical plan for feasibility |
| `/codexspec.review-tasks` | Review task breakdown for completeness |

#### Enhanced Commands

| Command | Description |
|---------|-------------|
| `/codexspec.clarify` | Clarify underspecified areas before planning |
| `/codexspec.analyze` | Cross-artifact consistency analysis |
| `/codexspec.checklist` | Generate quality checklists for requirements |
| `/codexspec.tasks-to-issues` | Convert tasks to GitHub issues |

## Workflow Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    CodexSpec Workflow                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. Constitution  ──►  Define project principles             │
│         │                                                    │
│         ▼                                                    │
│  2. Specify  ───────►  Create feature specification          │
│         │                                                    │
│         ▼                                                    │
│  3. Clarify  ───────►  Resolve ambiguities (optional)        │
│         │                                                    │
│         ▼                                                    │
│  4. Review Spec  ───►  Validate specification                │
│         │                                                    │
│         ▼                                                    │
│  5. Spec to Plan  ──►  Create technical plan                 │
│         │                                                    │
│         ▼                                                    │
│  6. Review Plan  ───►  Validate technical plan               │
│         │                                                    │
│         ▼                                                    │
│  7. Plan to Tasks  ─►  Generate task breakdown               │
│         │                                                    │
│         ▼                                                    │
│  8. Analyze  ───────►  Cross-artifact consistency (optional) │
│         │                                                    │
│         ▼                                                    │
│  9. Review Tasks  ──►  Validate task breakdown               │
│         │                                                    │
│         ▼                                                    │
│  10. Implement  ─────►  Execute implementation               │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

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
| Core Philosophy | Spec-driven development | Spec-driven development |
| CLI Name | `specify` | `codexspec` |
| Primary AI | Multi-agent support | Claude Code focused |
| Command Prefix | `/speckit.*` | `/codexspec.*` |
| Workflow | specify → plan → tasks → implement | constitution → specify → clarify → plan → tasks → analyze → implement |
| Review Steps | Optional | Built-in review commands |
| Clarify Command | Yes | Yes |
| Analyze Command | Yes | Yes |
| Checklist Command | Yes | Yes |
| Extension System | Yes | Yes |
| PowerShell Scripts | Yes | Yes |

## Philosophy

CodexSpec follows these core principles:

1. **Intent-driven development**: Specifications define the "what" before the "how"
2. **Rich specification creation**: Use guardrails and organizational principles
3. **Multi-step refinement**: Rather than one-shot code generation
4. **Heavy reliance on AI**: Leverage AI for specification interpretation
5. **Review-oriented**: Validate each artifact before moving forward
6. **Quality-first**: Built-in checklists and analysis for requirements quality

## Contributing

Contributions are welcome! Please read our contributing guidelines before submitting a pull request.

## License

MIT License - see [LICENSE](LICENSE) for details.

## Acknowledgements

- Inspired by [GitHub spec-kit](https://github.com/github/spec-kit)
- Built for [Claude Code](https://claude.ai/code)
