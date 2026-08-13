<!-- markdownlint-disable MD041 -->
@.codexspec/memory/constitution.md
@docs/internal/repository-layout.md

# CLAUDE.md - CodexSpec Development Guide

This document provides comprehensive context and guidelines for Claude Code when working on the CodexSpec project itself.

## Project Overview

**CodexSpec** is a Requirements-First SDD toolkit for Claude Code. It is a Python CLI tool that can be installed via `uv tool install` and provides structured slash commands for AI-assisted software development.

### Purpose

CodexSpec helps developers:

- Establish project principles through a constitution
- Create detailed specifications focused on "what" and "why"
- Generate technical implementation plans
- Break down plans into actionable tasks
- Execute implementations systematically
- Validate quality through checklists and analysis

### Technology Stack

- **Language**: Python 3.11+
- **CLI Framework**: Typer (with Rich for formatting)
- **Package Manager**: uv
- **Build System**: Hatchling
- **Testing**: pytest
- **Linting**: ruff

## Architecture

### CLI Architecture

The CLI is built using Typer and follows a modular structure:

```python
# Main entry point
app = typer.Typer(
    name="codexspec",
    help="CodexSpec - A Requirements-First SDD toolkit for Claude Code",
)

# Commands
@app.command()
def init(...): ...

@app.command()
def check(...): ...

@app.command()
def version(...): ...

@app.command()
def config(...): ...  # NEW: Configuration management
```

### Internationalization (i18n) Architecture

CodexSpec uses **LLM-based dynamic translation** for internationalization instead of maintaining multiple template translations.

**Core Concept**: Keep templates in English, let Claude translate at runtime based on user's language preference.

**Implementation**:

1. `src/codexspec/i18n.py` - Language utilities (normalization, validation)
2. `.codexspec/config.yml` - Per-project language configuration
3. Template `## Language Preference` section - Instructs Claude to check config

**Language Configuration**:

```yaml
# .codexspec/config.yml
version: "1.0"
language:
  output: "zh-CN"  # Output language
  commit: "zh-CN"  # Commit message language (defaults to output)
  templates: "en"  # Always "en"
project:
  ai: "claude"
  created: "2025-02-15"
```

**Template Pattern**:

```markdown
## Language Preference

**IMPORTANT**: Before proceeding, read the project's language configuration from `.codexspec/config.yml`.
- If `language.output` is set to a language other than "en", respond and generate all content in that language
- If not configured or set to "en", use English as default
- Technical terms (e.g., API, JWT, OAuth) may remain in English when appropriate
```

**Benefits**:

- Zero translation maintenance overhead
- Template updates benefit all languages immediately
- Context-aware translations via Claude
- Supports any language Claude understands

### Constitution Language

The `constitution.md` file is generated in the language specified by `language.output` configuration. This is an intentional design decision:

- Claude can understand constitution files in any major language (English, Chinese, Japanese, Korean, etc.)
- A single file avoids synchronization issues between multiple language versions
- Teams should use a consistent working language for collaboration

**Design Rationale**:

1. Prevents content inconsistency across multiple file versions
2. Claude and other major AI models have sufficient multilingual understanding capabilities
3. Reduces maintenance overhead by eliminating the need to manage multiple translations

If an English reference version is needed for international teams, a manual translation copy can be created.

### Slash Command System

Slash commands are Markdown files with YAML frontmatter:

```yaml
---
description: Command description
handoffs:
  - agent: claude
    step: Description of what the agent should do
---

# Command Title

## User Input
$ARGUMENTS

## Instructions
...
```

### Spec Directory Naming Scheme

Spec directories use a **timestamp + random suffix** naming scheme to ensure uniqueness across parallel development branches:

**Format**: `{YYYY-MMDD-HHMM}{random}-{feature-name}`

| Component | Description | Example |
|-----------|-------------|---------|
| `YYYY` | 4-digit year | 2025 |
| `MM` | 2-digit month | 03 |
| `DD` | 2-digit day | 21 |
| `HH` | 2-digit hour (00-23) | 14 |
| `MM` | 2-digit minute (00-59) | 30 |
| `{random}` | 2 random chars [a-z0-9] | k7 |

**Example**: `2025-0321-1430k7-user-authentication`

```
2025-0321-1430k7-user-authentication
│    │     │   ││
│    │     │   │└── Random suffix (2 chars)
│    │     │   └─── Minute (30)
│    │     └─────── Hour (14)
│    └───────────── Month-Day (0321)
└────────────────── Year (2025)
```

**Benefits**:

- **Uniqueness**: Timestamp + random suffix eliminates conflicts in parallel development
- **Sortability**: Directories sort chronologically by name
- **Readability**: Human-readable timestamp with hyphen separators
- **Compatibility**: Old sequential format (001-xxx) coexists with new format

**Generation Command**:

```bash
TIMESTAMP=$(date +"%Y-%m%d-%H%M")
RANDOM_SUFFIX=$(head /dev/urandom | LC_ALL=C tr -dc 'a-z0-9' | head -c 2)
PREFIX="${TIMESTAMP}${RANDOM_SUFFIX}"
```

**Regex Validation**: `^\d{4}-\d{4}-\d{4}[a-z0-9]{2}-[a-z0-9-]+$`

### Template Processing

When `codexspec init` is run:

1. Creates `.codexspec/` directory structure
2. Creates `.claude/commands/` directory
3. Copies slash command templates
4. Creates default constitution
5. Creates project CLAUDE.md
6. Copies helper scripts (bash and powershell)
7. Initializes git (optional)

### Git Branch Safety Check

**Feature**: Automatic branch detection and creation prompt for new feature development.

**Purpose**: Prevent accidental development on main/master branches by prompting users to create a feature branch.

**Affected Commands**:

- `/codexspec:specify` - Requirement clarification
- `/codexspec:generate-spec` - Spec generation

**Behavior**:

1. When executing these commands on a main branch (`main` or `master`), the system prompts:
   - "创建新功能分支（推荐）" - Create and switch to a new feature branch
   - "在当前分支继续工作" - Continue on current branch
   - "取消操作" - Cancel operation

2. If user chooses to create a branch:
   - Prompts for feature name
   - Generates branch name: `{YYYY-MMDD-HHMM}{random}-{feature-name}`
   - Creates and switches to the new branch

3. Gracefully handles:
   - Non-git environments (skips check)
   - Feature branches (no prompt)
   - Custom main branch names via configuration

**Configuration** (`.codexspec/config.yml`):

```yaml
git:
  main_branches:
    - "main"
    - "master"
    - "develop"  # Add custom main branches
  branch_check_enabled: true  # Set to false to disable
```

**Implementation**: The check is implemented as a `## Git Branch Safety Check` section in the command templates, executed before `## Instructions`.

### Auto-Next Chain Advance

**Feature**: When `workflow.auto_next` is enabled, the SDD pipeline advances to the next command automatically once the current stage passes, instead of requiring manual triggering between stages.

**Affected Commands**: `/codexspec:specify`, `/codexspec:generate-spec`, `/codexspec:spec-to-design`, `/codexspec:spec-to-plan`, `/codexspec:plan-to-tasks` each gain an `## Auto-Next Chain Advance` section. `/codexspec:implement-tasks` is the terminal stage (nothing auto-fires after it).

**Chain**: `specify → generate-spec → spec-to-design → spec-to-plan → plan-to-tasks → implement-tasks`.

**Pass gate**:

- `generate-spec` / `spec-to-design` / `spec-to-plan` / `plan-to-tasks`: the command's built-in review loop Overall Status is `PASS` or `PASS_WITH_WARNINGS`. (`NEEDS_REVISION` / `BLOCKED` stops the chain and returns control to the user.)
- `specify`: has no review loop; the gate is the user's explicit confirmation that requirements discovery is complete (the **final** stage summary, not each intermediate one).

Before each advance the agent emits one notice line (e.g. `auto_next: review passed → invoking /codexspec:spec-to-plan`). For `plan-to-tasks`, the existing `analyze` auto-invoke runs first: it auto-remediates deterministic inconsistencies (conforming spec/plan/tasks to `requirements.md`, which it never modifies) and remains non-blocking (does not block `implement-tasks`); the jump into `implement-tasks` proceeds with no confirmation prompt.

**Configuration** (`.codexspec/config.yml`):

```yaml
workflow:
  auto_next: true   # Default false (opt-in). Only literal `true` enables.
```

**Implementation**: A conditional `## Auto-Next Chain Advance` section in the command templates, mirroring the `## Automatic Cross-Artifact Analysis` pattern in `plan-to-tasks`. Edit `templates/commands/`; the `.claude/commands/codexspec/` and `.agents/skills/codexspec-*/` forms are regenerated from templates (do not hand-edit the derived copies).

### First-Class Design Stage: spec-to-design

**Feature**: A dedicated **design** stage inserted between `spec` and `plan`, so the authoritative chain is `requirements → spec → design → plan → tasks`. It closes the "front-half design layer" gap where `spec-to-plan` used to conflate *what the system is* (architecture, components, interfaces, design decisions) with *how to build it* (phases, ordering, verification).

- **`/codexspec:spec-to-design`** (new) reads `requirements.md` + `spec.md`, produces `design.md` as a first-class traceable artifact (every component/interface/data change/decision carries `Covers: REQ-xxx`), and embeds its own review loop (`review-design`) + `auto_next` (→ `spec-to-plan`). It acts as a **constrained system designer** and stops rather than change confirmed product intent.
- **`/codexspec:review-design`** (new) is symmetric with `review-spec`/`review-plan`/`review-tasks` (same Severity/Status/**Compatibility Score** formula), saving `review-design.md`.
- **`design.md`** uses a single `templates/docs/design-template.md` — a fixed core (Architecture & Components, ADR-lite Key Design Decisions, Requirements Coverage) plus **on-demand** optional sections (data models, API/interface contracts, sequence/data flow, cross-cutting design, risks). Output scales with complexity; no simple/detailed two-tier split.
- **`spec-to-plan` narrowed** to an implementation planner that consumes `design.md`; plan components carry `Covers: REQ-xxx; Design: <design component>` (ultimate REQ anchor + immediate upstream pointer, extending the existing `tasks` notation). The plan templates were slimmed — the design-only sections (Architecture / Component Structure / Data Models / API Contracts / ADR-style Decisions) moved to `design.md`.
- **Authority order** across the affected commands is `requirements > spec > design > plan > tasks` (design ranked below the constitution/verified-facts authority, above the plan). `generate-spec` auto_next now targets `spec-to-design`; `plan-to-tasks` / `implement-tasks` read `design.md`; `analyze` deepened its chain to `confirmed → REQ → design → plan → task`; `review-plan` / `review-tasks` gained `design` in their authority order. `review-code` and both constitutions are untouched.

**Implementation**: Edit `templates/commands/spec-to-design.md` / `review-design.md`, `templates/docs/design-template.md`, and the design-aware edits to `generate-spec` / `spec-to-plan` / `plan-to-tasks` / `analyze` / `implement-tasks` / `review-plan` / `review-tasks` and the slimmed `plan-template-{simple,detailed}.md`; register both commands in `installer.py` (core). The `.claude/commands/codexspec/` and `.agents/skills/codexspec-*/` forms are regenerated from templates (do not hand-edit the derived copies).

### Self-Evolution: Distill & Evolve

**Feature**: Capture reusable knowledge produced during work and (optionally) contribute it back to CodexSpec itself. Two distributed commands plus a project-level store:

- `/codexspec:distill` — extract reusable, **cross-feature** knowledge (constraints, conventions, pitfalls, cross-feature/architectural decisions) from an interaction into `.codexspec/profile/` (four markdown files: `constraints.md` / `conventions.md` / `pitfalls.md` / `decisions.md`). Each record separates the `claim` from its `evidence`, and files are mutated only via add/replace/remove with git history as the audit ledger. Bounded by the requirements-as-truth test ("would a single feature's `requirements`/`spec`/`plan` record it?" → yes = leave it there); there is no feature-local tier.
- `/codexspec:evolve` — compile **vetted** profile sediment into a SKILL.md / command-template draft and contribute it upstream via a **human-reviewed PR** (confirms before any push; edits only `templates/`, never the install artifact).

**Auto-Distill** (`workflow.auto_distill`): when enabled, `distill` runs automatically at the end of the wrap-up commands (`implement-tasks`, `commit-staged`, `pr`) via an embedded `## Automatic Distillation` section — non-blocking, never mutates SDD artifacts, and early-exits when there is nothing to capture. **Unlike `auto_next`, `auto_distill` defaults to ON (opt-out)** — only the literal `false` disables it.

**Configuration** (`.codexspec/config.yml`):

```yaml
workflow:
  auto_distill: true   # Default ON (opt-out). Only literal `false` disables.
```

Also togglable via `/codexspec:config` or `codexspec config --auto-distill on|off` (bare `--auto-distill` toggles).

**Implementation**: Edit `templates/commands/distill.md` / `evolve.md` and the embedded `## Automatic Distillation` sections in the wrap-up templates; the `.claude/commands/codexspec/` and `.agents/skills/codexspec-*/` forms are regenerated from templates (do not hand-edit the derived copies).

### Systematic Debugging: debug

**Feature**: A root-cause-first debugging discipline, delivered from one definition two ways — as a standalone `/codexspec:debug` command and as a low-ceremony escalation that `implement-tasks` enters when a fix is not converging.

- **One discipline, two reach paths (DRY)**: the four-phase discipline (root-cause investigation hard gate → pattern analysis → single-hypothesis verification → failing-test-first fix; **≥3 failed fixes → stop and question the architecture**) lives once in `debug.md`. The standalone command *is* that file; the `implement-tasks` hook references it via `Invoke /codexspec:debug` and never duplicates the text.
- **Single hook, two trip conditions**: `implement-tasks` carries one `## Systematic Debugging Escalation` section that trips on (a) a stuck TDD green loop, or (b) repairing a **non-trivial** functional/correctness defect surfaced by its `review-code` call. The escalation is conditional, non-gating, low-ceremony, and ends by explicitly resuming the task. `review-code` stays review-only and is **not** modified.
- **No config key, no artifact**: there is no `workflow.auto_debug` (systematic debugging when stuck is strictly-better default behavior, like conditional TDD); `debug` produces no persistent artifact — reusable root causes flow through the existing `distill` → `.codexspec/profile/pitfalls/` channel.

**Implementation**: Edit `templates/commands/debug.md` and the `## Systematic Debugging Escalation` section in `implement-tasks.md`; the `.claude/commands/codexspec/` and `.agents/skills/codexspec-*/` forms are regenerated from templates (do not hand-edit the derived copies).

### Codebase Onboarding: onboard

**Feature**: The **cold-start / bulk counterpart to `distill`** — a standalone `/codexspec:onboard [path]` command that scans an existing codebase once and batch-writes reusable knowledge into the shared `.codexspec/profile/` store, so a brownfield project's profile is grounded immediately instead of only after enough work has flowed through `distill`.

- **Reuses distill's store/format (DRY)**: onboard writes the same one-file-per-record, namespaced-id store; `distill.md` remains the canonical record-format doc (onboard adds only a cross-note there). onboard's deltas: `derivation` is always `inferred` → `status` is always `candidate` (never `vetted`), and `evidence.facts` holds a code observation (path + snippet) instead of a user quote.
- **Extracts only `conventions` + narrow `constraints`**; **never `decisions`/`pitfalls`** — a documented one is redundant to copy, an undocumented one is unreliable to infer (pitfalls are experiential; decision rationale would be fabricated); those two stay `distill`'s channels. Extraction is flexible agent judgment over what the code shows, not a fixed marker/file checklist; constraints come only from config-level explicit prohibitions with a precise evidence anchor (no signal → no constraint).
- **Tiered safety gate**: `conventions` are written immediately as `candidate` (take local effect, async-reviewable via `/distill review`); `constraints` (the one honored-first, highest-weight category) are held for a quick **persist / don't-persist** in-session review before writing — this gate is not `/distill review` and never promotes to `vetted`. The scan is high-signal-first, whole-repo, streaming/resumable, `.gitignore`-respecting (sensible fallback when no git), with optional `[path]` narrowing.
- **Standalone, additive, read-only on code**: not an SDD pipeline stage (no auto-next, no auto-hook, no Automatic Distillation section); read-only on the codebase, write-only to the profile; never clobbers existing `vetted`/human/`distill` records (append new files), so re-runs are idempotent.

**Implementation**: Edit `templates/commands/onboard.md` and the one-line onboard cross-note in `templates/commands/distill.md`; register `onboard` in `installer.py` under the `enhanced` category (adjacent to distill/evolve). The `.claude/commands/codexspec/` and `.agents/skills/codexspec-*/` forms are regenerated from templates (do not hand-edit the derived copies).

### Profile Consumption

**Feature**: Make a project's distilled `.codexspec/profile/` **take effect locally** — the read side that complements `distill` (which writes) and `evolve` (which contributes upstream). Without it the profile was write-only-then-upstream; this closes the loop so accumulated knowledge stops repeated pitfalls and re-litigated decisions **within the user's own project**.

- **Two consumption layers**:
  - **Ambient (A)** — `codexspec init` injects a bounded, idempotent managed block (`<!-- CODEXSPEC PROFILE START/END -->`) into each configured integration's context file (**CLAUDE.md and/or AGENTS.md** per `project.ai`), so the profile is discoverable in every session including plain chat.
  - **Requirements-time (B)** — `specify` reads the profile during discovery (a `## Consult Project Profile` step), so `requirements.md` is a synthesis that already accounts for it. **Only `specify` reads the profile**; downstream stages keep `requirements.md` as authority (transitive), and `review-code`/`evolve`/the constitution are untouched.
- **Uniform pointer block (identical on both channels, no `@import`)**: CLAUDE.md and AGENTS.md get the **same** block — constraints as a strong mandatory pointer ("before non-trivial work you MUST read every record under `.codexspec/profile/constraints/`"), and `conventions`/`pitfalls`/`decisions` as a pointer index read on demand. No `@import` anywhere, so the block is channel-neutral, the always-loaded footprint is independent of profile size, and there is no inlined copy to go stale. Accepted trade-off: constraints are no longer guaranteed in-context (a strong pointer, not `@import`), in exchange for channel uniformity and a conflict-free store.
- **One-file-per-record store (conflict-free parallel merges)**: the store is `.codexspec/profile/{constraints,conventions,pitfalls,decisions}/`, **one record per file** (`<id>.md`, the id also being the filename). Parallel feature branches add differently-named files, so distilled knowledge merges with **zero conflict** — no manual merge is ever imposed on the user. distill's add/replace/remove become create/edit/delete of a single file.
- **Immediate effect, no re-init**: init **unconditionally** injects the block and **ensures the profile scaffold** (the four category directories, each kept by a `.gitkeep`), so knowledge distilled later is live at once with no dangling reference. No `status` filter for local use — `candidate` records take effect locally (weighted with caution); `vetted` remains only the `evolve` gate.

**Implementation**: `src/codexspec/profile.py` (`ensure_profile_scaffold` / `render_profile_block` / `inject_profile_block`), wired into `src/codexspec/__init__.py` (scaffold + CLAUDE.md injection, after the compliance import) and `src/codexspec/integrations/codex.py` (AGENTS.md injection); the store layout + B-layer read live in `templates/commands/distill.md` and `templates/commands/specify.md`. CodexSpec's own repo receives the ambient block by dogfooding `init` at release (not by hand-editing its CLAUDE.md/AGENTS.md); the `.claude/commands/` and `.agents/skills/` forms of `specify` regenerate from the template.

### Plugin Marketplace Support

**Feature**: CodexSpec is available as a Claude Code plugin via the plugin marketplace.

**Purpose**: Allow users to install CodexSpec slash commands directly without the CLI tool.

**Marketplace Configuration** (`.claude-plugin/marketplace.json`):

```json
{
  "$schema": "https://anthropic.com/claude-code/marketplace.schema.json",
  "name": "codexspec-market",
  "description": "Requirements-First SDD toolkit for Claude Code",
  "owner": {
    "name": "Zts0hg"
  },
  "plugins": [
    {
      "name": "codexspec",
      "description": "Complete Spec-Driven Development toolkit...",
      "source": {
        "source": "github",
        "repo": "Zts0hg/codexspec",
        "ref": "v0.5.11",
        "path": ".claude/commands/codexspec"
      },
      "version": "0.5.11",
      "strict": false
    }
  ]
}
```

**Key Design Decisions**:

1. **Single Plugin Package**: All CodexSpec commands bundled as one plugin (not separate plugins per command)
2. **`strict: false`**: Plugin doesn't require `plugin.json` - commands work directly from markdown templates
3. **Version Sync**: `ref` and `version` in `marketplace.json` are automatically updated by `publish.sh`
4. **Multi-language Support**: Reuses existing LLM dynamic translation via `.codexspec/config.yml`

**Installation Methods Comparison**:

| Method | Best For | Features |
|--------|----------|----------|
| CLI (`uv tool install`) | Full development workflow | `init`, `check`, `config` commands + slash commands |
| Plugin Marketplace | Quick start, existing projects | Slash commands only |

**Publish Integration** (`publish.sh`):

- `update_marketplace()`: Updates `ref` and `version` fields in `marketplace.json`
- `commit_marketplace_changes()`: Commits and pushes marketplace updates
- `--skip-marketplace`: Option to skip marketplace updates during publish

**User Installation**:

```bash
# Add marketplace
> /plugin marketplace add Zts0hg/codexspec

# Install plugin
> /plugin install codexspec@codexspec-market
```

## Available Slash Commands

### Core Commands (11)

| Command                      | Description                              |
| ---------------------------- | ---------------------------------------- |
| `/codexspec:constitution`    | Create/update project constitution       |
| `/codexspec:specify`         | Create feature specification             |
| `/codexspec:generate-spec`   | Generate detailed spec from requirements |
| `/codexspec:spec-to-design`  | Produce design.md (architecture/components/ADR-lite) from spec |
| `/codexspec:spec-to-plan`    | Convert design to implementation plan    |
| `/codexspec:plan-to-tasks`   | Break down plan into tasks               |
| `/codexspec:review-spec`     | Review specification                     |
| `/codexspec:review-design`   | Review design                            |
| `/codexspec:review-plan`     | Review technical plan                    |
| `/codexspec:review-tasks`    | Review task breakdown                    |
| `/codexspec:implement-tasks` | Execute implementation                   |

### Enhanced Commands (5) - NEW

| Command                      | Description                                 |
| ---------------------------- | ------------------------------------------- |
| `/codexspec:clarify`         | Ask clarification questions before planning |
| `/codexspec:analyze`         | Cross-artifact consistency analysis with auto-remediation |
| `/codexspec:checklist`       | Generate requirements quality checklists    |
| `/codexspec:tasks-to-issues` | Convert tasks to GitHub issues              |
| `/codexspec:debug`           | Systematic root-cause debugging (standalone + implement-tasks escalation) |

### Self-Evolution Commands (3) - NEW

| Command                | Description                                                              |
| ---------------------- | ------------------------------------------------------------------------ |
| `/codexspec:distill`   | Distill reusable cross-feature knowledge from an interaction into `.codexspec/profile/` |
| `/codexspec:evolve`    | Compile vetted profile knowledge into a command/skill draft and contribute it upstream via a reviewed PR |
| `/codexspec:onboard`   | Cold-start the project profile from an existing codebase (distill's bulk counterpart): scan → conventions + narrow constraints, never decisions/pitfalls |

### Internal Maintenance Commands (NOT distributed to users)

These commands exist **only** in `.claude/commands/codexspec/` and are intentionally absent from `templates/commands/`. They are tightly coupled to CodexSpec's own documentation site (MkDocs i18n, fixed `docs/{lang}/` structure, CodexSpec-specific glossary) and are used by CodexSpec maintainers and the `docs-i18n.yml` CI workflow. **They are not installed by `codexspec init` and are not user-facing features.**

| Command                           | Description                                                          |
| --------------------------------- | -------------------------------------------------------------------- |
| `/codexspec:translate-docs`       | Translate CodexSpec's own docs from `docs/en/` to 7 target languages |
| `/codexspec:check-i18n-semantics` | Verify semantic consistency of CodexSpec's own translated docs       |

Both commands read the project glossary at `docs/i18n/glossary.yml` (canonical, repo-only path). The path `.codexspec/i18n/glossary.yml` is **not** used and should not be referenced in any artifact.

### Git Workflow Commands

| Command                    | Description                                         |
| -------------------------- | --------------------------------------------------- |
| `/codexspec:commit-staged` | Generate commit from staged changes strictly from the staged diff |
| `/codexspec:pr`            | Generate PR/MR descriptions                         |

### Code Review Commands (1)

| Command                      | Description                                      |
| ---------------------------- | ------------------------------------------------ |
| `/codexspec:review-code` | Review code in any language for idiomatic clarity, correctness, robustness, architecture, and constitution alignment |

## Development Guidelines

### Code Style

- **Line Length**: 120 characters max
- **Formatting**: Follow PEP 8
- **Imports**: Use absolute imports
- **Type Hints**: Use type hints for public functions
- **Docstrings**: Use docstrings for public functions and classes

### Naming Conventions

- **CLI Commands**: lowercase with hyphens (e.g., `spec-to-plan`)
- **Python Functions**: snake_case (e.g., `get_templates_dir`)
- **Python Classes**: PascalCase (e.g., `Console`)
- **Constants**: UPPER_SNAKE_CASE (e.g., `__version__`)

### Error Handling

- Use Typer's `Exit` for CLI errors
- Provide clear, actionable error messages
- Use Rich for formatted output

### Testing

- Write tests for all public functions
- Use pytest fixtures for common setup
- Test edge cases and error conditions

### Script Testing

Scripts are tested via pytest subprocess calls:

- **Bash scripts**: `tests/scripts/bash/`
- **PowerShell scripts**: `tests/scripts/powershell/`

Run script tests:

```bash
# All script tests
uv run pytest tests/scripts/ -v

# Bash only
uv run pytest tests/scripts/bash/ -v

# PowerShell only (requires pwsh installed)
uv run pytest tests/scripts/powershell/ -v
```

**Prerequisites for PowerShell tests:**

- Install PowerShell: https://learn.microsoft.com/powershell/
- Tests are automatically skipped if pwsh is not available

## Commands Implementation Status

| Command                      | Status     | Notes                                                                         |
| ---------------------------- | ---------- | ----------------------------------------------------------------------------- |
| `init`                       | ✅ Complete | Initializes project structure, supports --lang, Constitution Compliance check |
| `check`                      | ✅ Complete | Checks for installed tools                                                    |
| `version`                    | ✅ Complete | Displays version info                                                         |
| `config`                     | ✅ Complete | View/modify project configuration                                             |
| `/codexspec:config`          | ✅ Template | Interactive configuration management for Plugin users                          |
| `/codexspec:constitution`    | ✅ Template | Template complete, CLAUDE.md Compliance check on first-time creation          |
| `/codexspec:specify`         | ✅ Template | Template complete, includes Configuration Check                               |
| `/codexspec:generate-spec`   | ✅ Template | Template complete                                                             |
| `/codexspec:spec-to-design`  | ✅ Template | Template complete — first-class design stage between spec and plan            |
| `/codexspec:spec-to-plan`    | ✅ Template | Template complete — narrowed to implementation planning, consumes design.md   |
| `/codexspec:plan-to-tasks`   | ✅ Template | Template complete                                                             |
| `/codexspec:review-spec`     | ✅ Template | Template complete                                                             |
| `/codexspec:review-design`   | ✅ Template | Template complete — reviews design.md, symmetric with the other review gates  |
| `/codexspec:review-plan`     | ✅ Template | Template complete                                                             |
| `/codexspec:review-tasks`    | ✅ Template | Template complete                                                             |
| `/codexspec:implement-tasks` | ✅ Template | Template complete                                                             |
| `/codexspec:clarify`         | ✅ Template | Template complete                                                             |
| `/codexspec:analyze`         | ✅ Template | Template complete                                                             |
| `/codexspec:checklist`       | ✅ Template | Template complete                                                             |
| `/codexspec:tasks-to-issues` | ✅ Template | Template complete                                                             |
| `/codexspec:distill`         | ✅ Template | Self-evolution: extract reusable cross-feature knowledge into `.codexspec/profile/` |
| `/codexspec:evolve`          | ✅ Template | Self-evolution: compile vetted profile knowledge into a command/skill draft + reviewed PR |
| `/codexspec:onboard`         | ✅ Template | Cold-start the profile from an existing codebase (distill's bulk counterpart): conventions + narrow constraints, tiered safety gate, never decisions/pitfalls |
| `/codexspec:debug`           | ✅ Template | Systematic root-cause debugging: one four-phase discipline; standalone command + implement-tasks reference-style escalation |
| `/codexspec:commit-staged`   | ✅ Template | Generate commit from staged changes strictly from the staged diff             |
| `/codexspec:pr`              | ✅ Template | Generate PR/MR descriptions                                                   |
| `/codexspec:review-code` | ✅ Template | Review code in any language for idiomatic clarity, correctness, robustness, architecture, and constitution alignment |
| `/codexspec:translate-docs`  | ✅ Internal | Maintainer-only — lives only in `.claude/commands/codexspec/`, not distributed via `init` |
| `/codexspec:check-i18n-semantics` | ✅ Internal | Maintainer-only — lives only in `.claude/commands/codexspec/`, not distributed via `init` |

### Constitution Compliance Feature

The `init` and `/codexspec:constitution` commands now include a **dual safeguard mechanism** to ensure CLAUDE.md contains the Constitution Compliance section:

- **init command**: Checks existing CLAUDE.md for compliance section; prompts user to add if missing
- **constitution command**: On first-time creation, checks CLAUDE.md and offers to prepend compliance section

**Helper Functions** (in `src/codexspec/__init__.py`):

- `has_compliance_section(Path) -> bool`: Check if CLAUDE.md has compliance section
- `prepend_compliance_section(Path) -> None`: Prepend compliance section to existing CLAUDE.md
- `confirm_add_compliance() -> bool`: User confirmation prompt
- `_get_compliance_section_content() -> str`: Get compliance section content

## Extension System

CodexSpec supports a plugin architecture for custom commands.

### Extension Structure

```
my-extension/
├── extension.yml          # Manifest
├── commands/              # Custom commands
└── README.md
```

### Extension Manifest

```yaml
schema_version: "1.0"

extension:
  id: "my-extension"
  name: "My Extension"
  version: "1.0.0"
  description: "What it does"

requires:
  codexspec_version: ">=0.1.0"

provides:
  commands:
    - name: "codexspec.my-extension.command"
      file: "commands/command.md"
      description: "Description"
```

See `extensions/EXTENSION-DEVELOPMENT-GUIDE.md` for details.

## Future Development Reference

### Multi-AI Agent Support (Not Yet Implemented)

Spec-kit supports 15+ AI agents. CodexSpec currently focuses on Claude Code but could be extended to support:

| Agent              | Notes                      |
| ------------------ | -------------------------- |
| Gemini CLI         | Google's AI assistant      |
| GitHub Copilot     | VS Code integration        |
| Cursor             | AI-powered IDE             |
| Windsurf           | Codeium's IDE              |
| Codex CLI          | OpenAI's CLI               |
| Amazon Q Developer | AWS AI assistant           |
| Others             | See spec-kit for full list |

**Implementation Considerations:**

1. Different command directory structures:
   - Claude: `.claude/commands/`
   - Gemini: `.gemini/commands/`
   - Copilot: `.github/agents/`
2. Different command formats:
   - Most use Markdown with YAML frontmatter
   - Some use TOML or other formats
3. Different argument handling
4. Agent-specific features and limitations

**Reference:** See `spec-kit/` directory for implementation details.

### Other Future Enhancements

1. **Interactive Mode**: Guided workflow with prompts
2. **Validation Framework**: Automated validation of artifacts
3. **Template Customization**: User-defined templates
4. **Extension CLI Commands**: `codexspec extension list/add/remove`
5. **Web UI**: Browser-based workflow management

## Key Implementation Details

### UV Tool Installation

The project is designed to work with `uv tool install`:

```bash
uv tool install codexspec --from git+https://github.com/Zts0hg/codexspec:git
```

This requires:

1. Proper `pyproject.toml` configuration
2. Entry point in `[project.scripts]`
3. Correct package structure

### Template Directory Resolution

Templates must be found both in development and when installed:

```python
def get_templates_dir() -> Path:
    # When installed via uv/pip
    package_dir = Path(__file__).parent.parent.parent / "templates"
    if package_dir.exists():
        return package_dir
    # Fallback
    return Path(__file__).parent.parent / "templates"
```

### Cross-Platform Compatibility

- Use `pathlib` for all path operations
- Handle Windows vs Unix command differences
- Support both Bash and PowerShell scripts

## When Working on This Project

### Self-Bootstrap: Never Edit `.claude/commands/codexspec/` Directly

**CRITICAL**: CodexSpec uses itself. The directory `.claude/commands/codexspec/` in this repository is an **install artifact** — it is the output of running `codexspec init` (or equivalent) on the CodexSpec project itself, not a source of truth.

**Rule**:

- ❌ **Never manually edit** files under `.claude/commands/codexspec/` for distributed commands. Any change there will be silently overwritten the next time CodexSpec is reinstalled, and will never reach end users.
- ✅ **Always edit** the source templates under `templates/commands/` instead. The correct propagation path is:
  1. Edit `templates/commands/<command>.md`
  2. Publish a new CodexSpec version (`publish.sh`)
  3. Re-run `codexspec init` (or `uv tool install --force .`) to sync `.claude/commands/codexspec/` from the updated templates

**The only exception** is the internal maintenance commands (`/codexspec:translate-docs`, `/codexspec:check-i18n-semantics`), which intentionally live *only* in `.claude/commands/codexspec/` and have no counterpart in `templates/commands/`. See `.codexspec/memory/constitution.md` → "Slash Command Template Modification Rules" for the full policy.

**When auditing or analyzing the project**: treat `.claude/commands/codexspec/<distributed-command>.md` as a derived file, the same way you would treat a compiled artifact or a lockfile — read it to observe the installed state, but make fixes upstream in `templates/commands/`.

### Two Constitutions, Two Different Purposes — Do Not Confuse Them

There are **two** constitution-related artifacts in this repo. They serve **completely different audiences** and must **never** be treated as copies of each other.

| Artifact | Audience | Purpose |
|---|---|---|
| `.codexspec/memory/constitution.md` (tracked) | **CodexSpec project developers** (you, future contributors) | Governance for this specific repository. Contains CodexSpec-project-specific rules like the Slash Command Template Modification Rules and the Self-bootstrap rule. |
| `_get_default_constitution()` in `src/codexspec/__init__.py` (hardcoded string, L1489-1556) | **End users of CodexSpec** | The **generic baseline** that `codexspec init` writes into a user's brand-new project. Users then customize it for their own project via `/codexspec:constitution`. |

**These are not mirrors of each other.** They are independent documents that happen to share a name ("constitution"):

- ❌ Do **not** "sync" edits between them. A CodexSpec-project-specific rule (e.g. Self-bootstrap, template modification workflow) has no meaning for end users and should stay out of `_get_default_constitution()`.
- ❌ Do **not** treat `.codexspec/memory/constitution.md` as a "reference" or "template" for the default. It is governance for the project you are working on right now, nothing more.
- ❌ Do **not** treat `_get_default_constitution()` as the source of truth for this project's principles. This project's principles live in the tracked `.codexspec/memory/constitution.md`.
- ✅ **Decision rule**: "Is this rule about how to develop CodexSpec itself, or is it a generic principle every CodexSpec end user would want?" Former → `.codexspec/memory/constitution.md`. Latter → `_get_default_constitution()`. Most rules belong in exactly one of the two, never both.

This distinction is also recorded at the top of `.codexspec/memory/constitution.md` as a "SCOPE" callout — if you ever find yourself tempted to "propagate" a change between the two, re-read that callout first.

### Before Making Changes

1. Read this CLAUDE.md file
2. Understand the current implementation status
3. Check existing code for patterns to follow
4. Ensure changes align with project goals

### When Adding Features

1. Update this CLAUDE.md if architecture changes
2. Add tests for new functionality
3. Update README.md for user-facing changes
4. Follow existing code patterns

### When Fixing Bugs

1. Write a test that reproduces the bug
2. Fix the bug
3. Ensure all tests pass
4. Update documentation if needed

## Quick Reference

### Common Commands

```bash
# Install for development
uv sync --dev

# Run CLI locally
uv run codexspec --help

# Run tests
uv run pytest

# Lint code
uv run ruff check src/

# Build package
uv build

# Install locally for testing
uv tool install --force .
```

### Important Files

| File                        | Purpose                                           |
| --------------------------- | ------------------------------------------------- |
| `pyproject.toml`            | Project configuration, dependencies, entry points |
| `src/codexspec/__init__.py` | Main CLI implementation                           |
| `src/codexspec/i18n.py`     | Internationalization utilities                    |
| `templates/commands/*.md`   | Slash command templates                           |
| `scripts/bash/*.sh`         | Bash helper scripts                               |
| `scripts/powershell/*.ps1`  | PowerShell helper scripts                         |
| `extensions/`               | Extension system                                  |
| `README.md`                 | User documentation                                |
| `CLAUDE.md`                 | This file - AI development context                |

---

*This file is the source of truth for AI assistants working on CodexSpec. Keep it updated as the project evolves.*

<!-- CODEXSPEC PROFILE START -->
## CodexSpec Project Profile

**Project constraints (highest priority — read these FIRST):** before any non-trivial work you MUST read every record under `.codexspec/profile/constraints/` — the project's hard prohibitions (严禁 / 仅允许). Honor them before anything else.

**Project profile — consult on demand when relevant to the task** (each directory holds one record per file):

- `.codexspec/profile/conventions/` — cross-feature conventions / steering; read before adopting a pattern, structure, or naming choice.
- `.codexspec/profile/pitfalls/` — known traps and their workarounds; read before implementing or debugging in an area that may have bitten before.
- `.codexspec/profile/decisions/` — past cross-feature / architectural decisions; read before deciding in the same area, to reuse prior rationale rather than re-litigate it.

Read the full record — each carries a `status` of `candidate` or `vetted`; weight `candidate` items with appropriate caution. A directory may be empty until `/codexspec:distill` has captured knowledge.
<!-- CODEXSPEC PROFILE END -->
