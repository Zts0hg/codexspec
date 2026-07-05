# Quick Start

This page walks through the complete **Requirements-First SDD** flow in eight steps.
Confirmed requirements are the highest-priority authority, and nothing is binding until you explicitly confirm it — each stage ends at a **Confirmation Gate** you control.

For small, well-bounded changes you can skip the full walkthrough and run [`/codexspec:quick`](#small-changes-codexspecquick) instead.

## 1. Initialize a Project

After installation, create or initialize your project:

```bash
# Create new project
codexspec init my-awesome-project

# Or initialize in current directory
codexspec init . --ai claude

# With Chinese output (sets the output base)
codexspec init my-project --lang zh-CN

# Fully non-interactive (CI/scripts): zh-CN output base, English commit messages
codexspec init my-project --lang zh-CN --commit-lang en

# Set every language dimension explicitly (scriptable, no prompts)
codexspec init my-project \
  --interaction-lang zh-CN --document-lang en --commit-lang en
```

Then move into the project and launch Claude Code:

```bash
cd my-awesome-project
claude
```

## 2. Establish Project Principles

Use the constitution command to set the standards every later artifact will be checked against:

```
/codexspec:constitution Create principles focused on code quality and testing
```

## 3. Clarify Requirements

Use `/codexspec:specify` to explore requirements:

```
/codexspec:specify I want to build a task management application
```

This command asks clarifying questions, surfaces edge cases, and asks you to confirm a final requirement summary that is persisted to `requirements.md`.

> **Confirmation Gate**: `/codexspec:specify` only writes entries you explicitly confirm. The requirement summary it presents is **not** binding until you accept it — refuse, amend, or re-open any item before saying yes. Nothing downstream can override what you confirm here.

## 4. Generate Specification

Once the requirement summary is confirmed, generate the spec document:

```
/codexspec:generate-spec
```

`generate-spec` compiles the confirmed entries into a structured `spec.md` with source references for traceability, then runs an automatic review (defects need concrete evidence; advisory suggestions never trigger automatic changes; verified defects may be fixed and re-reviewed for at most two rounds).

## 5. Review and Validate

**Recommended:** validate the spec before proceeding:

```
/codexspec:review-spec
```

This is an **evidence-based review**: every reported defect cites concrete evidence, and design advisories stay separate from acceptance.

## 6. Create Technical Plan

```
/codexspec:spec-to-plan Use Python FastAPI for backend
```

The plan records `Covers` links back to specification requirements and verifies applicable constitution principles.

## 7. Generate Tasks

```
/codexspec:plan-to-tasks
```

Tasks are organized around verifiable outcomes with traceability links to the plan and requirements. Test-first ordering is applied **conditionally** — only where the plan, constitution, or task risk requires it. Non-testable tasks (docs, config) are implemented directly.

## 8. Implement

```
/codexspec:implement-tasks
```

Implementation follows **conditional TDD**: code tasks use the Red → Green → Verify → Refactor cycle when required; documentation and configuration tasks are implemented directly.

## Small Changes: `/codexspec:quick`

For a small, well-bounded change you do not need the full eight-step walkthrough. `/codexspec:quick` runs a compact Requirements-First SDD flow in a single command:

```
/codexspec:quick Add a "remember me" checkbox to the login form
```

Quick still respects the same guardrails as the full flow:

- It creates a feature workspace and `requirements.md` using the same timestamp convention as `/codexspec:specify`.
- It presents a concise confirmed requirement summary (`NEED-*`, relevant `CON-*`/`DEC-*`, `OUT-*`, unresolved `OPEN-*`) and waits for your explicit confirmation — the **Confirmation Gate** still applies.
- It then chains `/codexspec:generate-spec` → `/codexspec:spec-to-plan` → `/codexspec:plan-to-tasks` → `/codexspec:implement-tasks` against that feature directory, with each generation command owning its own automatic review loop.

If the change turns out to be broad or to have multiple independent outcomes, Quick pauses and recommends the standard flow instead.

## Project Structure

After initialization:

```
my-project/
├── .codexspec/
│   ├── memory/
│   │   └── constitution.md    # Project constitution
│   ├── specs/
│   │   └── {feature-id}/
│   │       ├── spec.md        # Feature specification
│   │       ├── plan.md        # Technical plan
│   │       ├── tasks.md       # Task breakdown
│   │       └── checklists/    # Quality checklists
│   ├── templates/             # Custom templates
│   ├── scripts/               # Helper scripts
│   └── extensions/            # Custom extensions
├── .claude/
│   └── commands/              # Claude Code slash commands
├── .agents/
│   └── skills/                # Codex skills (when initialized with --ai codex or both)
├── CLAUDE.md                  # Claude Code context
└── AGENTS.md                  # Codex context
```

## Next Steps

[Full Workflow Guide](../user-guide/workflow.md)
