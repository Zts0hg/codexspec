# Quick Start

<a id="30-second-quick-start"></a>

## 30-Second Quick Start

Install CodexSpec and initialize for the assistant you use:

```bash
uv tool install codexspec

# Create a new project for Claude Code
codexspec init my-project --ai claude

# Or initialize an existing project for Codex
cd your-existing-project
codexspec init . --ai codex

# Use --ai both when you want both integrations
```

Start your installed assistant in the initialized project. The same workflow
uses these two invocation forms:

| Assistant | Start requirements discovery |
|-----------|------------------------------|
| Claude Code (`claude`) | `/codexspec:specify I want to build a todo application` |
| Codex (`codex`) | `$codexspec:specify I want to build a todo application` |

Customize project principles with `constitution` when needed. Confirm the final
requirements summary, then continue using the returned feature directory and
workspace. See [Core Workflow](../user-guide/workflow.md#core-workflow) for the remaining commands.

Using the Codex desktop app? [Ask Codex to install and initialize your project](installation.md#install-with-the-codex-desktop-app).

<a id="core-workflow"></a>

## Core Workflow

The standard feature workflow preserves a source-linked chain:

```text
/specify          → requirements.md
/generate-spec    → spec.md       → review-spec
/spec-to-design   → design.md     → review-design
/design-to-plan   → plan.md       → review-plan
/plan-to-tasks    → tasks.md      → review-tasks → analyze
/implement-tasks  → implementation and complete-feature code review
```

Examples below use Claude's `/codexspec:` prefix. In Codex, use
`$codexspec:` with the same command name and arguments.

| Step | Command | Purpose and output |
|------|---------|--------------------|
| Project principles | `/codexspec:constitution` | Create/update `constitution.md` and validate affected artifacts |
| Requirements | `/codexspec:specify <idea>` | Discuss intent, confirm a final summary, and persist `requirements.md` |
| Specification | `/codexspec:generate-spec <feature-dir>` | Compile confirmed requirements into `spec.md` with source references |
| System design | `/codexspec:spec-to-design <feature-dir>` | Produce `design.md`: components, interfaces, and key design decisions |
| Implementation plan | `/codexspec:design-to-plan <feature-dir>` | Produce `plan.md`: phases, ordering, and verification |
| Tasks | `/codexspec:plan-to-tasks <feature-dir>` | Produce traceable, verifiable `tasks.md`; run cross-artifact analysis |
| Implementation | `/codexspec:implement-tasks <feature-dir>` | Execute tasks, verify outcomes, and repair independently verified review findings |

Replace `<feature-dir>` with the feature directory returned during discovery.
Continue in its worktree or pass its explicit path; this retains the same feature
identity across commands and sessions.

<a id="specify-clarify-and-analyze"></a>

### specify, clarify, and analyze

- **specify** starts or revisits requirement discovery. Only explicit confirmation
  makes the requirement summary binding.
- **clarify** resolves ambiguity in existing requirements/specification: up to five
  questions per run across four categories. It updates `requirements.md` first,
  then synchronizes `spec.md`.
- **analyze** checks the complete requirements → spec → design → plan → tasks
  chain. It automatically applies deterministic fixes to downstream artifacts
  when their correction follows from upstream authority; it never edits
  `requirements.md`. Unresolved findings are reported. It runs automatically after
  a passing task review and is informational rather than an implementation gate.

```text
/codexspec:clarify <feature-dir>
/codexspec:analyze <feature-dir>
```

<a id="small-changes-with-quick"></a>

### Small Changes with Quick

Use `quick` for a small, well-bounded change such as a localized fix:

```text
/codexspec:quick Fix the empty-state message on the task list
```

Quick confirms and persists a compact requirement summary, then orchestrates
specification, planning, tasks, and implementation with the generation commands'
reviews. Broad changes or unresolved product/design choices call for the standard
workflow; Quick pauses when it needs a new decision.

<a id="workflow-automation"></a>

### Workflow Automation

`workflow.auto_next` defaults to **false**. When it is `true` in the active
workspace's configuration, final requirement confirmation advances to
specification. Each generation stage advances after `PASS` or
`PASS_WITH_WARNINGS`; `NEEDS_REVISION` or `BLOCKED` stops the chain.
`implement-tasks` is terminal.

Automatic artifact repair is limited to verified defects whose correction
follows from upstream evidence, with at most two fix-and-review rounds.
Advisories remain separate. The implementation review/repair loop has its own
completion rules described below.

See the [workflow guide](../user-guide/workflow.md) for detailed contracts.

<a id="project-structure"></a>

## Project Structure

Initialization installs common resources plus the selected assistant integration:

```text
my-project/
├── .codexspec/
│   ├── config.yml
│   ├── memory/
│   │   └── constitution.md
│   ├── profile/
│   │   ├── constraints/
│   │   ├── conventions/
│   │   ├── pitfalls/
│   │   ├── decisions/
│   │   ├── strategies/
│   │   └── runbooks/
│   ├── review-code/              # Shared review standards
│   ├── specs/
│   │   └── <feature-id>-<name>/   # Added by feature workflows
│   │       ├── requirements.md
│   │       ├── spec.md
│   │       ├── design.md
│   │       ├── plan.md
│   │       ├── tasks.md
│   │       ├── review-*.md
│   │       └── checklists/       # When requested
│   ├── templates/docs/
│   └── scripts/                 # Platform helpers and commit runtime
├── .claude/commands/codexspec/   # --ai claude or both
├── .agents/skills/              # --ai codex or both
├── CLAUDE.md                    # Claude project context
└── AGENTS.md                    # Codex project context
```

The shared blueprint lives in the dedicated auto-dev worktree, rather than a
separate editable copy in each ordinary checkout. Manual knowledge-review drafts
are excluded from Git.
