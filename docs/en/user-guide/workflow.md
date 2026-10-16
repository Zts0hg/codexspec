# Workflow

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

<a id="shared-blueprint-and-autonomous-development"></a>

## Shared Blueprint and Autonomous Development

Use `blueprint` when you want to prepare several confirmed requirements before
development, and `auto-dev` to develop that queue:

```text
/codexspec:blueprint Add a confirmed requirement for task reminders
/codexspec:auto-dev
```

Blueprint discovery resolves user-owned direction, choices, and constraints
before a requirement enters the queue. The shared `.codexspec/blueprint.md`
uses `pending`, `in_progress`, and `completed` states. You can append,
replace, delete, or reorder pending requirements; active and completed entries
are read-only to blueprint maintenance.

Auto-dev follows document order, resumes an in-progress feature before starting
another, and re-reads the queue after each completion so newly appended pending
work can join the run. It performs the SDD stages, implementation, verification,
review, and repair within the confirmed requirements. Calling `auto-dev` enables
its automation independently of `workflow.auto_next` and does not change that setting.

Both commands share `worktree-for-codexspec-auto-dev` on branch
`codexspec/auto-dev`. They can operate concurrently under the shared ownership
and write protections; requirements are developed sequentially in that workspace.
Product decisions that cannot be resolved from confirmed requirements stop the run
with evidence rather than prompting during normal autonomous execution.

Inspect the current shared blueprint without changing it:

```bash
codexspec show-blueprint
```

<a id="worktree-development"></a>

## Worktree Development

A Git worktree is another working directory for the same repository, with its own
checked-out branch. CodexSpec uses one per ordinary feature by default, creating
it before the first requirement write and keeping that feature's documents,
implementation, tests, and repairs together.

```text
projects/
├── my-project/
└── my-project-codexspec-worktrees/
    ├── <feature-id>-task-reminders/
    ├── <feature-id>-search/
    ├── worktree-for-codexspec-maintenance/
    └── worktree-for-codexspec-auto-dev/
```

Continuing a feature reuses its workspace. Standalone configuration, constitution,
and profile changes use the maintenance worktree; changes made in an active feature
stay there. Configuration is **checkout-local**: a setting changed in a routed
worktree takes effect there first, and reaches other checkouts through Git
integration. Run CLI commands and checks in the returned workspace.

New feature baselines compare committed local and fetched remote main-branch
history by Git ancestry. Divergent histories merge inside the new worktree and
require verification. A failed fetch warns and permits locally available refs;
creation failures do not fall back to writing in the main checkout.

`workflow.worktrees` defaults to **true**; only literal YAML `false` disables
ordinary feature and maintenance isolation. Blueprint/auto-dev keep their fixed
shared worktree either way. Initialization and installation updates operate on
the checkout you explicitly select. Completed worktrees are retained; completion
does not automatically merge or delete them.

See [Worktree Development](workflow.md#worktree-development)
and [configuration](../reference/configuration.md#workflow-and-review-settings).

<a id="work-with-existing-code"></a>

## Work with Existing Code

Two entry points serve different goals:

| Command | Use it to | Output/boundary |
|---------|-----------|-----------------|
| `onboard [path]` | Seed reusable project knowledge from an existing codebase | Candidate conventions and narrowly evidenced constraints in the profile; code remains read-only |
| `reverse-spec [path]` | Understand existing architecture or compare code with confirmed intent | Draft artifacts or a drift report; code remains read-only |

```text
/codexspec:onboard src/
/codexspec:reverse-spec
/codexspec:reverse-spec src/auth
```

Onboard infers conventions from observable code and proposes constraints only
from explicit prohibitions. Convention candidates take local effect immediately;
constraint candidates require an in-session persist/edit/drop decision.
It preserves existing knowledge and does not invent past decision rationale or
experiential pitfalls from a cold scan.

Reverse-spec has three modes:

- **Overview**: no path, or repository root, produces a thin architecture
  `design.md` and `slices.md` for choosing modules to inspect.
- **Generate**: a module path without a confirmed baseline produces draft
  `spec.md`, `design.md`, and open/inferred requirements.
- **Reconcile**: a module with a confirmed baseline produces `reconcile.md`,
  reporting undocumented behavior, unimplemented specifications, and semantic
  mismatches against confirmed spec/design, with requirements governing intent.

Inferred drafts require human confirmation before becoming a baseline.
Reconciliation reports the proposed direction—fix code, update documents, or
decide intent—and does not automatically apply it.

<a id="review-and-debugging"></a>

## Review and Debugging

Four artifact reviewers check fidelity, coverage, feasibility, and internal
quality: `review-spec`, `review-design`, `review-plan`, and `review-tasks`.
They run automatically after generation and can also be invoked manually.
Reports distinguish verified defects from non-gating risk advisories and design
opportunities, with a compatibility score.

`review-code` provides a separate change-scoped defect gate and an explicit
whole-code quality assessment:

```text
/codexspec:review-code --feature <feature-dir>
/codexspec:review-code --uncommitted
/codexspec:review-code --audit src/
```

Default review covers the complete feature-branch delta, including committed,
staged, unstaged, and untracked non-ignored changes. You can explicitly select
committed, uncommitted, or one-commit evidence. `--feature` attaches requirements
context without narrowing Git scope. `--audit` assesses the named paths and
produces an advisory scorecard rather than a completion verdict.

Reviews load shared standards from `.codexspec/review-code/`, selecting relevant
behavior dimensions and language/framework checks. Findings require concrete
evidence, reachable triggers, selected-change attribution, and impact.
The reviewer reports defects and substantiated maintenance suggestions without
editing files; the repair caller independently verifies them.

Implementation uses test-first for code tasks and direct implementation with
appropriate checks for documentation/configuration. After repairs, incremental
re-review can reuse unaffected coverage; final acceptance requires a fresh
complete-feature `PASS`, completed coverage and verification, and zero admitted
P0–P3 defects. Substantiated maintenance suggestions are reported separately.

`workflow.auto_maintenance` defaults to **true** and controls whether repair
callers also apply verified, compatible maintenance improvements. Turning it off
still reports those suggestions and does not waive defects or required checks.
It is separate from stage advancement and is not an `implement-tasks` argument.

For root-cause-first debugging:

```text
/codexspec:debug Investigate intermittent failures when saving a task
```

Debug follows investigation → pattern analysis → single-hypothesis verification
→ failing-test-first fix. Implementation escalates when repairs are stuck,
a non-trivial correctness defect needs tracing, or the same root-cause class
recurs across review rounds. Three failed fixes trigger architectural reassessment.

Use `checklist` to assess requirement clarity, completeness, and consistency:

```text
/codexspec:checklist Check the authentication requirements for completeness
```

See the [command reference](commands.md) for review selectors,
arguments, and detailed procedures.

<a id="project-knowledge"></a>

## Project Knowledge

The project profile stores reusable knowledge under `.codexspec/profile/`:

| Category | Contents |
|----------|----------|
| `constraints/` | Explicit prohibitions and hard boundaries, read first |
| `conventions/` | Patterns, naming, and cross-feature guidance |
| `pitfalls/` | Experienced traps, causes, workarounds, and lessons |
| `decisions/` | Reusable architectural and cross-feature decisions |
| `strategies/` | Signals that call for a different working approach |
| `runbooks/` | Ordered procedures and failure recovery |

`distill` captures reusable knowledge from work; feature-specific intent remains
in that feature's requirements/design/plan. Init installs guidance in CLAUDE.md
and/or AGENTS.md to read all constraints and relevant knowledge before substantive
work. Knowledge added later can take effect without re-initialization.
Candidate records are used cautiously; vetted records require outcome
verification and human endorsement.

```text
/codexspec:distill Capture the reusable lessons from this work
/codexspec:distill review
/codexspec:evolve
```

Manual `distill review`, or a direct `distill` with no new material to capture,
opens a local, offline browser workspace. You can revise, vet, discard, defer,
and consolidate records, preview final Markdown, then select **Apply all**.
Decisions remain in a recoverable draft until application; conflict checks
prevent partial application or silent overwrite. An explicit text fallback is
available for environments without a browser.

`workflow.auto_distill` defaults to **true** and controls three wrap-up hooks:
successful `implement-tasks`, executed commits through `commit-staged`, and `pr`
generation. Commit preview does not trigger capture.

Installed project guidance also asks agents to capture reusable knowledge as it
arises in ordinary conversations, fixes outside SDD, and during long
`implement-tasks` runs. That guidance applies independently of the wrap-up
setting; end-of-task capture provides a final backstop.

Within a session, repeated triggers process only new material. Across sessions,
`distill` reads the profile and skips knowledge already covered. Capture exits
without writing when nothing reusable remains. Automatic capture never opens
manual review, waits for a human, or blocks the calling workflow.

`evolve` selects only vetted knowledge useful beyond the project, compiles a
command/skill draft, and obtains explicit approval before pushing or opening
a contribution PR for human review.

See [Project Knowledge](commands.md#codexspecdistill)
for detailed guidance.

<a id="reusing-historical-decisions"></a>

### Reusing Historical Decisions

Before asking you about a change, the agent consults related feature histories
under `.codexspec/specs/`. It reads confirmed decisions in `requirements.md`,
follows later additions and explicit replacements, and consults design rationale
or implementation evidence when needed. This preparation also applies before
substantive design, implementation, debugging, or review judgments, in ordinary
conversation as well as SDD workflows.

Feature-directory timestamps help reconstruct the sequence of iterations;
a newer document does not automatically invalidate an older decision. Older
unchanged requirements remain applicable, and open proposals are not treated
as confirmed intent. Retrieval stays focused on the current task and stops once
the background is sufficient; that background is reused for later stages.

For example, when changing an interface, an agent without historical context
might ask:

> “How should this feature handle backward compatibility?”

After checking the relevant decisions and current implementation, it can instead
ask a focused question:

> “You previously confirmed that the old interface should be retained, and the
> current implementation still supports it. I suggest keeping that behavior for
> this change. Should we?”

Established information that clearly still applies can be reused without asking
again. If you have already said “Remove the old interface in this change,” the
agent follows that decision and explains the migration impact. **Your latest
explicit decision always takes precedence**; history helps prepare better
questions and avoid repeated ones.

Refresh existing project installations to receive this guidance.

<a id="git-workflow"></a>

## Git Workflow

```text
/codexspec:commit-staged -p
/codexspec:pr --spec <feature-dir>/spec.md
/codexspec:release-notes --from <ref> --to HEAD
/codexspec:tasks-to-issues <feature-dir>
```

- **commit-staged** analyzes the exact staging area and generates a Conventional
  Commits message; `-p` previews without committing. The calling workflow chooses
  and stages files. Authorized execution uses the guarded runtime, rechecking that
  committed content matches the analysis. Agent commit guidance applies in ordinary
  conversation, SDD, blueprint, and auto-dev workflows; command availability alone
  does not invoke it or authorize a commit.
- **pr** generates a structured GitHub PR or GitLab MR description from the diff.
  `--spec` optionally adds feature context from a `spec.md` file path, or a
  feature directory name or prefix resolved to that file. Default output is text
  for use in the hosting platform.
- **release-notes** derives a Keep a Changelog entry and release body from Git
  history. The default section is `[Unreleased]`; `--version` uses a supplied
  label. It does not stage, commit, bump versions, tag, publish, or create a release.
- **tasks-to-issues** creates GitHub issues from existing tasks, including
  dependencies and acceptance criteria. It requires an authenticated GitHub CLI
  and verifies that the issue repository matches the configured remote.

Direct commit preview and authorized in-place commits require Python 3.11+ and
Git; the runtime is installed with CLI projects and bundled with the Claude plugin.
Contentful agent-created merges also use staged analysis. History-only merges
retain Git's default message while validating the tree and parents; fast-forwards
create no commit.

## Traceability and continuation

Confirmed `requirements.md` governs feature intent; the downstream chain is `spec.md` → `design.md` → `plan.md` → `tasks.md`, interpreted alongside applicable project principles and verified repository facts. Requirements use stable IDs, specification entries cite `Sources`, and downstream work cites `Covers`. A downstream artifact cannot silently redefine an upstream decision. Conflicting authority or a new product decision requires user resolution. Legacy features without requirements disclose the lack of original confirmation; missing legacy design artifacts use the documented fallback.

Pass an explicit feature path when selection is ambiguous; commands do not silently choose the newest directory. The worktree parent is derived from the primary repository, including when invoked from a nested directory or another linked worktree. For bare repositories it is a sibling named `<bare-repository-name>-codexspec-worktrees`. Standalone maintenance uses branch `codexspec/maintenance`.

A failed worktree preparation retains its identity for continuation. Divergent-baseline merges must pass project checks before feature requirements are published or development starts. Read-only inspection keeps its source; reports use the resolved output checkout. Staged commit execution keeps the selected index and never transfers main’s staged changes into another worktree. If a new worktree lacks required installed resources, initialize that destination before continuing.

## Review Model

Reviews separate three kinds of output:

- **Fidelity defects**: conflict with an authoritative source or omit required coverage.
- **Intrinsic defects**: the artifact is internally contradictory, unverifiable, or infeasible.
- **Risk advisories / design opportunities**: optional improvements without evidence of a current defect.

Every defect must identify its evidence, location, mismatch, impact, and minimal remediation. Findings with the same root cause are merged. Advisories do not affect status, score, or automatic fixes.

Review status is:

- `PASS`: no critical, warning, or minor defects.
- `PASS_WITH_WARNINGS`: only minor defects remain.
- `NEEDS_REVISION`: one or more warnings remain.
- `BLOCKED`: a critical conflict prevents reliable continuation.

The compatibility score is derived from the same classified findings rather than fixed template-section deductions. Status is authoritative; the score exists for integrations that still expect a number.

## Bounded Auto Review

Generation commands run the matching review automatically. This is the **evidence-based review** discipline in action: they may repair only evidence-backed defects and re-review for at most two rounds. They stop earlier on `PASS`, and stop for user input when:

- an authoritative source conflicts with another source;
- a fix would change confirmed intent;
- the remaining item is advisory rather than defective;
- two repair rounds have been used.

Manual `/codexspec:review-*` commands can be run at any time for a fresh report.
