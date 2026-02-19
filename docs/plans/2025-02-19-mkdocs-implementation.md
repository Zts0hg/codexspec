# MkDocs Documentation Site Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Implement a MkDocs + Material documentation site with GitHub Pages auto-deployment for CodexSpec.

**Architecture:** Use MkDocs with Material theme for documentation. Content organized in `docs/` directory with subsections for Getting Started, User Guide, Reference, and Development. GitHub Actions workflow triggers on docs changes to build and deploy to GitHub Pages.

**Tech Stack:** Python 3.11+, MkDocs 1.5+, MkDocs Material 9.5+, mkdocstrings, GitHub Pages

---

## Task 1: Update pyproject.toml with Docs Dependencies

**Files:**
- Modify: `pyproject.toml:37-42`

**Step 1: Add docs optional dependencies**

Add the `[project.optional-dependencies]` section with docs dependencies:

```toml
[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "pytest-cov>=4.0",
    "ruff>=0.1.0",
]
docs = [
    "mkdocs>=1.5.0",
    "mkdocs-material>=9.5.0",
    "mkdocstrings[python]>=0.24.0",
]
```

**Step 2: Sync dependencies**

Run: `uv sync --extra docs`
Expected: Dependencies installed successfully

**Step 3: Commit**

```bash
git add pyproject.toml uv.lock
git commit -m "chore: add MkDocs documentation dependencies"
```

---

## Task 2: Create mkdocs.yml Configuration

**Files:**
- Create: `mkdocs.yml`

**Step 1: Create mkdocs.yml**

Create the file with complete configuration:

```yaml
site_name: CodexSpec
site_description: A Spec-Driven Development (SDD) toolkit for Claude Code
site_url: https://zts0hg.github.io/codexspec/
repo_url: https://github.com/Zts0hg/codexspec
repo_name: Zts0hg/codexspec
edit_uri: edit/main/docs/

theme:
  name: material
  logo: assets/images/logo.png
  favicon: assets/images/favicon.png
  palette:
    - media: "(prefers-color-scheme: light)"
      scheme: default
      primary: indigo
      accent: indigo
      toggle:
        icon: material/brightness-7
        name: Switch to dark mode
    - media: "(prefers-color-scheme: dark)"
      scheme: slate
      primary: indigo
      accent: indigo
      toggle:
        icon: material/brightness-4
        name: Switch to light mode
  features:
    - navigation.instant
    - navigation.tracking
    - navigation.tabs
    - navigation.sections
    - navigation.expand
    - navigation.top
    - search.suggest
    - search.highlight
    - content.code.copy
    - content.action.edit
  icon:
    repo: fontawesome/brands/github

nav:
  - Home: index.md
  - Getting Started:
    - Installation: getting-started/installation.md
    - Quick Start: getting-started/quick-start.md
  - User Guide:
    - Workflow: user-guide/workflow.md
    - Commands: user-guide/commands.md
    - Internationalization: user-guide/i18n.md
  - Reference:
    - CLI: reference/cli.md
    - Configuration: reference/configuration.md
  - Development:
    - Contributing: development/contributing.md

markdown_extensions:
  - pymdownx.highlight:
      anchor_linenums: true
      line_spans: __span
  - pymdownx.inlinehilite
  - pymdownx.snippets
  - pymdownx.superfences
  - pymdownx.tabbed:
      alternate_style: true
  - pymdownx.tasklist:
      custom_checkbox: true
  - admonition
  - pymdownx.details
  - attr_list
  - md_in_html
  - toc:
      permalink: true

plugins:
  - search
  - mkdocstrings:
      handlers:
        python:
          paths: [src]
          options:
            show_source: true
            show_root_heading: true

extra:
  social:
    - icon: fontawesome/brands/github
      link: https://github.com/Zts0hg/codexspec

extra_css:
  - assets/stylesheets/extra.css
```

**Step 2: Commit**

```bash
git add mkdocs.yml
git commit -m "docs: add MkDocs configuration"
```

---

## Task 3: Create Docs Directory Structure

**Files:**
- Create: `docs/index.md`
- Create: `docs/getting-started/installation.md`
- Create: `docs/getting-started/quick-start.md`
- Create: `docs/user-guide/workflow.md`
- Create: `docs/user-guide/commands.md`
- Create: `docs/user-guide/i18n.md`
- Create: `docs/reference/cli.md`
- Create: `docs/reference/configuration.md`
- Create: `docs/development/contributing.md`
- Create: `docs/assets/stylesheets/extra.css`
- Create: `docs/assets/images/.gitkeep`

**Step 1: Create directory structure**

```bash
mkdir -p docs/getting-started
mkdir -p docs/user-guide
mkdir -p docs/reference
mkdir -p docs/development
mkdir -p docs/assets/stylesheets
mkdir -p docs/assets/images
```

**Step 2: Create docs/index.md (Homepage)**

```markdown
# Welcome to CodexSpec

[![PyPI version](https://img.shields.io/pypi/v/codexspec.svg)](https://pypi.org/project/codexspec/)
[![Python](https://img.shields.io/pypi/pyversions/codexspec.svg)](https://pypi.org/project/codexspec/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**A Spec-Driven Development (SDD) toolkit for Claude Code**

CodexSpec is a toolkit that helps you build high-quality software using a structured, specification-driven approach. It flips the script on traditional development by making specifications executable artifacts that directly guide implementation.

## Why CodexSpec?

### Human-AI Collaboration

CodexSpec is built on the belief that **effective AI-assisted development requires active human participation at every stage**.

| Problem | Solution |
|---------|----------|
| Unclear requirements | Interactive Q&A to clarify before building |
| Incomplete specifications | Dedicated review commands with scoring |
| Misaligned technical plans | Constitution-based validation |
| Vague task breakdowns | TDD-enforced task generation |

### Key Features

- **:material-cog: Constitution-Based** - Establish project principles that guide all decisions
- **:material-chat: Interactive Clarification** - Q&A-based requirement refinement
- **:material-check-circle: Review Commands** - Validate artifacts at each stage
- **:material-test-tube: TDD-Ready** - Test-first methodology built into tasks
- **:material-translate: i18n Support** - 13+ languages via LLM translation

## Quick Start

```bash
# Install
uv tool install codexspec

# Create a new project
codexspec init my-project

# Or initialize in existing project
codexspec init . --ai claude
```

[:material-arrow-right: Full Installation Guide](getting-started/installation.md)

## Workflow Overview

```
Idea → Clarify → Review → Plan → Review → Tasks → Review → Implement
            ↑              ↑              ↑
         Human checks    Human checks    Human checks
```

Every artifact has a corresponding review command to validate AI output before proceeding.

[:material-arrow-right: Learn the Workflow](user-guide/workflow.md)

## License

MIT License - see [LICENSE](https://github.com/Zts0hg/codexspec/blob/main/LICENSE) for details.
```

**Step 3: Create docs/getting-started/installation.md**

```markdown
# Installation

## Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) (recommended) or pip

## Option 1: Install with uv (Recommended)

The easiest way to install CodexSpec is using uv:

```bash
uv tool install codexspec
```

## Option 2: Install with pip

Alternatively, you can use pip:

```bash
pip install codexspec
```

## Option 3: One-time Usage

Run directly without installing:

```bash
# Create a new project
uvx codexspec init my-project

# Initialize in an existing project
cd your-existing-project
uvx codexspec init . --ai claude
```

## Option 4: Install from GitHub

For the latest development version:

```bash
# Using uv
uv tool install git+https://github.com/Zts0hg/codexspec.git

# Using pip
pip install git+https://github.com/Zts0hg/codexspec.git

# Specific branch or tag
uv tool install git+https://github.com/Zts0hg/codexspec.git@main
uv tool install git+https://github.com/Zts0hg/codexspec.git@v0.2.0
```

## Verify Installation

```bash
codexspec --help
codexspec version
```

## Upgrading

```bash
# Using uv
uv tool install codexspec --upgrade

# Using pip
pip install --upgrade codexspec
```

## Next Steps

[:material-arrow-right: Quick Start](quick-start.md)
```

**Step 4: Create docs/getting-started/quick-start.md**

```markdown
# Quick Start

## 1. Initialize a Project

After installation, create or initialize your project:

```bash
# Create new project
codexspec init my-awesome-project

# Or initialize in current directory
codexspec init . --ai claude

# With Chinese output
codexspec init my-project --lang zh-CN
```

## 2. Establish Project Principles

Launch Claude Code in the project directory:

```bash
cd my-awesome-project
claude
```

Use the constitution command:

```
/codexspec.constitution Create principles focused on code quality and testing
```

## 3. Clarify Requirements

Use `/codexspec.specify` to explore requirements:

```
/codexspec.specify I want to build a task management application
```

## 4. Generate Specification

Once clarified, generate the spec document:

```
/codexspec.generate-spec
```

## 5. Review and Validate

**Recommended:** Validate before proceeding:

```
/codexspec.review-spec
```

## 6. Create Technical Plan

```
/codexspec.spec-to-plan Use Python FastAPI for backend
```

## 7. Generate Tasks

```
/codexspec.plan-to-tasks
```

## 8. Implement

```
/codexspec.implement-tasks
```

## Project Structure

After initialization:

```
my-project/
├── .codexspec/
│   ├── memory/
│   │   └── constitution.md
│   ├── specs/
│   │   └── {feature-id}/
│   │       ├── spec.md
│   │       ├── plan.md
│   │       └── tasks.md
│   └── scripts/
├── .claude/
│   └── commands/
└── CLAUDE.md
```

## Next Steps

[:material-arrow-right: Full Workflow Guide](../user-guide/workflow.md)
```

**Step 5: Commit progress**

```bash
git add docs/index.md docs/getting-started/
git commit -m "docs: add homepage and getting-started sections"
```

---

## Task 4: Create User Guide Documentation

**Files:**
- Create: `docs/user-guide/workflow.md`
- Create: `docs/user-guide/commands.md`
- Create: `docs/user-guide/i18n.md`

**Step 1: Create docs/user-guide/workflow.md**

```markdown
# Workflow

CodexSpec structures development into **reviewable checkpoints** with human validation at each stage.

## Workflow Overview

```
┌──────────────────────────────────────────────────────────────────────────┐
│                    CodexSpec Human-AI Collaboration Workflow             │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  1. Constitution  ──►  Define project principles                         │
│         │                                                                 │
│         ▼                                                                │
│  2. Specify  ───────►  Interactive Q&A to clarify requirements           │
│         │                                                                │
│         ▼                                                                │
│  3. Generate Spec  ─►  Create spec.md document                           │
│         │                                                                │
│         ▼                                                                │
│  ╔═══════════════════════════════════════════════════════════════════╗   │
│  ║  ★ REVIEW GATE 1: /codexspec.review-spec ★                        ║   │
│  ╚═══════════════════════════════════════════════════════════════════╝   │
│         │                                                                │
│         ▼                                                                │
│  4. Spec to Plan  ──►  Create technical plan                             │
│         │                                                                │
│         ▼                                                                │
│  ╔═══════════════════════════════════════════════════════════════════╗   │
│  ║  ★ REVIEW GATE 2: /codexspec.review-plan ★                        ║   │
│  ╚═══════════════════════════════════════════════════════════════════╝   │
│         │                                                                │
│         ▼                                                                │
│  5. Plan to Tasks  ─►  Generate atomic tasks                             │
│         │                                                                │
│         ▼                                                                │
│  ╔═══════════════════════════════════════════════════════════════════╗   │
│  ║  ★ REVIEW GATE 3: /codexspec.review-tasks ★                       ║   │
│  ╚═══════════════════════════════════════════════════════════════════╝   │
│         │                                                                │
│         ▼                                                                │
│  6. Implement  ─────►  Execute with conditional TDD workflow             │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
```

## Why Review Matters

| Without Review | With Review |
|---------------|-------------|
| AI makes incorrect assumptions | Human catches misinterpretations early |
| Incomplete requirements propagate | Gaps identified before implementation |
| Architecture drifts from intent | Alignment verified at each stage |
| **Result: Rework** | **Result: Right first time** |

## Core Commands

| Stage | Command | Purpose |
|-------|---------|---------|
| 1 | `/codexspec.constitution` | Define project principles |
| 2 | `/codexspec.specify` | Interactive Q&A for requirements |
| 3 | `/codexspec.generate-spec` | Create specification document |
| - | `/codexspec.review-spec` | ★ Validate specification |
| 4 | `/codexspec.spec-to-plan` | Create technical plan |
| - | `/codexspec.review-plan` | ★ Validate plan |
| 5 | `/codexspec.plan-to-tasks` | Break down into tasks |
| - | `/codexspec.review-tasks` | ★ Validate tasks |
| 6 | `/codexspec.implement-tasks` | Execute implementation |

## Two-Phase Specification

### specify vs clarify

| Aspect | `/codexspec.specify` | `/codexspec.clarify` |
|--------|----------------------|----------------------|
| **Purpose** | Initial exploration | Iterative refinement |
| **When** | No spec.md exists | spec.md exists, needs gaps filled |
| **Input** | Your initial idea | Existing spec.md |
| **Output** | None (dialogue only) | Updates spec.md |

## Conditional TDD

Implementation follows conditional TDD:

- **Code tasks**: Test-first (Red → Green → Verify → Refactor)
- **Non-testable tasks** (docs, config): Direct implementation
```

**Step 2: Move existing commands.md content**

Read the existing `docs/commands.md` and move it to `docs/user-guide/commands.md` with minor adjustments for MkDocs format.

**Step 3: Create docs/user-guide/i18n.md**

```markdown
# Internationalization

CodexSpec supports multiple languages through **LLM dynamic translation**.

## How It Works

1. **Single English Templates**: All command templates remain in English
2. **Language Configuration**: Project specifies preferred output language
3. **Dynamic Translation**: Claude translates content at runtime

## Setting Language

### During Initialization

```bash
# Chinese output
codexspec init my-project --lang zh-CN

# Japanese output
codexspec init my-project --lang ja
```

### After Initialization

```bash
# View current configuration
codexspec config

# Change language
codexspec config --set-lang zh-CN

# List supported languages
codexspec config --list-langs
```

## Configuration File

`.codexspec/config.yml`:

```yaml
version: "1.0"

language:
  output: "zh-CN"  # Output language
  templates: "en"  # Keep as "en"

project:
  ai: "claude"
  created: "2025-02-15"
```

## Supported Languages

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

## Benefits

- **Zero Translation Maintenance**: No need to maintain multiple template versions
- **Always Up-to-Date**: Template updates benefit all languages
- **Context-Aware**: Technical terms remain in English when appropriate
```

**Step 4: Commit**

```bash
git add docs/user-guide/
git commit -m "docs: add user-guide documentation"
```

---

## Task 5: Create Reference Documentation

**Files:**
- Create: `docs/reference/cli.md`
- Create: `docs/reference/configuration.md`

**Step 1: Create docs/reference/cli.md**

```markdown
# CLI Reference

## Commands

### `codexspec init`

Initialize a new CodexSpec project.

```bash
codexspec init [PROJECT_NAME] [OPTIONS]
```

**Arguments:**

| Argument | Description |
|----------|-------------|
| `PROJECT_NAME` | Name for your new project directory |

**Options:**

| Option | Short | Description |
|--------|-------|-------------|
| `--here` | `-h` | Initialize in current directory |
| `--ai` | `-a` | AI assistant to use (default: claude) |
| `--lang` | `-l` | Output language (e.g., en, zh-CN, ja) |
| `--force` | `-f` | Force overwrite existing files |
| `--no-git` | | Skip git initialization |
| `--debug` | `-d` | Enable debug output |

**Examples:**

```bash
# Create new project
codexspec init my-project

# Initialize in current directory
codexspec init . --ai claude

# With Chinese output
codexspec init my-project --lang zh-CN
```

---

### `codexspec check`

Check for installed tools.

```bash
codexspec check
```

---

### `codexspec version`

Display version information.

```bash
codexspec version
```

---

### `codexspec config`

View or modify project configuration.

```bash
codexspec config [OPTIONS]
```

**Options:**

| Option | Short | Description |
|--------|-------|-------------|
| `--set-lang` | `-l` | Set the output language |
| `--list-langs` | | List all supported languages |
```

**Step 2: Create docs/reference/configuration.md**

```markdown
# Configuration

## Config File Location

`.codexspec/config.yml`

## Configuration Schema

```yaml
version: "1.0"

language:
  output: "en"      # Output language for documents
  templates: "en"   # Template language (keep as "en")

project:
  ai: "claude"      # AI assistant
  created: "2025-02-15"
```

## Language Settings

### `language.output`

The language for Claude interactions and generated documents.

**Supported values:** See [Internationalization](../user-guide/i18n.md#supported-languages)

### `language.templates`

Template language. Should remain as `"en"` for compatibility.

## Project Settings

### `project.ai`

The AI assistant being used. Currently supports:

- `claude` (default)

### `project.created`

Date when the project was initialized.
```

**Step 3: Commit**

```bash
git add docs/reference/
git commit -m "docs: add reference documentation"
```

---

## Task 6: Create Development Documentation

**Files:**
- Create: `docs/development/contributing.md`

**Step 1: Create docs/development/contributing.md**

```markdown
# Contributing

## Prerequisites

- Python 3.11+
- uv package manager
- Git

## Local Development

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

## Documentation

```bash
# Install docs dependencies
uv sync --extra docs

# Preview documentation locally
uv run mkdocs serve

# Build documentation
uv run mkdocs build
```

## Building

```bash
uv build
```

## Pull Request Process

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

## Code Style

- Line length: 120 characters max
- Follow PEP 8
- Use type hints for public functions
```

**Step 2: Commit**

```bash
git add docs/development/
git commit -m "docs: add contributing guide"
```

---

## Task 7: Create Assets and Styles

**Files:**
- Create: `docs/assets/stylesheets/extra.css`
- Create: `docs/assets/images/.gitkeep`

**Step 1: Create docs/assets/stylesheets/extra.css**

```css
/* Custom styles for CodexSpec docs */

/* Make code blocks more prominent */
.highlight {
  margin: 1em 0;
}

/* Admonition styling */
.admonition {
  margin: 1em 0;
}

/* Better table styling */
.md-typeset table:not([class]) {
  display: table;
  width: 100%;
}

/* Improve task list styling */
.md-typeset .task-list-item {
  margin: 0.5em 0;
}
```

**Step 2: Create .gitkeep for images**

```bash
touch docs/assets/images/.gitkeep
```

**Step 3: Commit**

```bash
git add docs/assets/
git commit -m "docs: add assets and custom styles"
```

---

## Task 8: Create GitHub Actions Workflow

**Files:**
- Create: `.github/workflows/docs.yml`

**Step 1: Create .github/workflows/docs.yml**

```yaml
name: Deploy Docs

on:
  push:
    branches: [main]
    paths:
      - 'docs/**'
      - 'mkdocs.yml'
      - 'src/**'
      - 'pyproject.toml'
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: pages
  cancel-in-progress: false

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          cache: 'pip'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -e ".[docs]"

      - name: Build MkDocs
        run: mkdocs build --strict

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: site

  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    needs: build
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

**Step 2: Commit**

```bash
git add .github/workflows/docs.yml
git commit -m "ci: add GitHub Actions workflow for docs deployment"
```

---

## Task 9: Update .gitignore

**Files:**
- Modify: `.gitignore`

**Step 1: Add MkDocs build output to .gitignore**

Add the following to `.gitignore`:

```
# MkDocs
site/
```

**Step 2: Commit**

```bash
git add .gitignore
git commit -m "chore: add MkDocs site to gitignore"
```

---

## Task 10: Update README with Docs Link

**Files:**
- Modify: `README.md`

**Step 1: Add documentation link to README**

Add a link to the documentation site in the README header section (after the badges):

```markdown
**[📖 Documentation](https://zts0hg.github.io/codexspec/)** |
```

**Step 2: Commit**

```bash
git add README.md
git commit -m "docs: add documentation site link to README"
```

---

## Task 11: Test Local Build

**Step 1: Sync dependencies**

Run: `uv sync --extra docs`
Expected: Dependencies installed successfully

**Step 2: Build documentation**

Run: `uv run mkdocs build --strict`
Expected: Build succeeds with no warnings

**Step 3: Preview locally (optional)**

Run: `uv run mkdocs serve`
Expected: Local server starts at http://127.0.0.1:8000

---

## Task 12: Final Commit and Push

**Step 1: Ensure all changes are committed**

Run: `git status`
Expected: No uncommitted changes

**Step 2: Push to remote**

Run: `git push origin main`
Expected: Changes pushed successfully

---

## Verification

After pushing:

1. Check GitHub Actions workflow runs successfully
2. Verify GitHub Pages is enabled in repository settings
3. Confirm documentation site is accessible at https://zts0hg.github.io/codexspec/

## Notes

- The old `docs/commands.md` can be removed after migration is verified
- Consider adding logo and favicon images to `docs/assets/images/`
- Enable GitHub Pages in repository Settings → Pages → Source: GitHub Actions
