# CodexSpec

[中文](README.zh-CN.md) | [日本語](README.ja.md) | [Español](README.es.md) | [Português](README.pt-BR.md) | [한국어](README.ko.md) | [Deutsch](README.de.md) | [Français](README.fr.md)

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

#### Core Commands

| Command | Description |
|---------|-------------|
| `/codexspec.constitution` | Create or update project governing principles |
| `/codexspec.specify` | **Clarify** requirements through interactive Q&A (no file generation) |
| `/codexspec.generate-spec` | **Generate** `spec.md` document after requirements are clarified |
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
| `/codexspec.clarify` | Scan existing spec.md for ambiguities and update with clarifications |
| `/codexspec.analyze` | Cross-artifact consistency analysis |
| `/codexspec.checklist` | Generate quality checklists for requirements |
| `/codexspec.tasks-to-issues` | Convert tasks to GitHub issues |

## Workflow Overview

```
┌──────────────────────────────────────────────────────────────┐
│                    CodexSpec Workflow                        │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  1. Constitution  ──►  Define project principles             │
│         │                                                    │
│         ▼                                                    │
│  2. Specify  ───────►  Interactive Q&A to clarify            │
│         │             requirements (no file created)         │
│         │                                                    │
│         ▼                                                    │
│  3. Generate Spec  ─►  Create spec.md document               │
│         │             (user calls explicitly)                │
│         │                                                    │
│         ▼                                                    │
│  4. Review Spec  ───►  Validate specification                │
│         │                                                    │
│         ▼                                                    │
│  5. Clarify  ───────►  Resolve ambiguities (optional)        │
│         │                                                    │
│         ▼                                                    │
│  6. Spec to Plan  ──►  Create technical plan                 │
│         │                                                    │
│         ▼                                                    │
│  7. Review Plan  ───►  Validate technical plan               │
│         │                                                    │
│         ▼                                                    │
│  8. Plan to Tasks  ─►  Generate task breakdown               │
│         │                                                    │
│         ▼                                                    │
│  9. Analyze  ───────►  Cross-artifact consistency (optional) │
│         │                                                    │
│         ▼                                                    │
│  10. Review Tasks  ─►  Validate task breakdown               │
│         │                                                    │
│         ▼                                                    │
│  11. Implement  ─────►  Execute implementation               │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

### Key Concept: Requirement Clarification Workflow

CodexSpec provides **two distinct clarification commands** for different stages of the workflow:

#### specify vs clarify: When to Use Which?

| Aspect | `/codexspec.specify` | `/codexspec.clarify` |
|--------|----------------------|----------------------|
| **Purpose** | Initial requirement exploration | Iterative refinement of existing spec |
| **When to Use** | Starting with a new idea, no spec.md exists | spec.md exists, need to fill gaps |
| **Input** | Your initial idea or requirement | Existing spec.md file |
| **Output** | None (dialogue only) | Updates spec.md with clarifications |
| **Method** | Open-ended Q&A | Structured ambiguity scan (6 categories) |
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
                └── Scans for ambiguities in 6 categories:
                    • Functional Scope & Behavior
                    • Domain & Data Model
                    • Interaction & UX Flow
                    • Non-Functional Quality Attributes
                    • Edge Cases & Failure Handling
                    • Conflict Resolution
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
| Core Philosophy | Spec-driven development | Spec-driven development |
| CLI Name | `specify` | `codexspec` |
| Primary AI | Multi-agent support | Claude Code focused |
| Command Prefix | `/speckit.*` | `/codexspec.*` |
| Workflow | specify → plan → tasks → implement | constitution → specify → generate-spec → plan → tasks → analyze → implement |
| Two-Phase Spec | No | Yes (clarify + generate) |
| Review Steps | Optional | Built-in review commands |
| Clarify Command | Yes | Yes |
| Analyze Command | Yes | Yes |
| Checklist Command | Yes | Yes |
| Extension System | Yes | Yes |
| PowerShell Scripts | Yes | Yes |
| i18n Support | No | Yes (13+ languages via LLM translation) |

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
