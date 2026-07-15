---
description: 执行实现任务，支持条件 TDD 工作流（代码使用 TDD，文档/配置直接实现）
argument-hint: "[tasks 路径] | [spec 路径 plan 路径 tasks 路径]"
handoffs:
  - agent: claude
    step: Execute implementation tasks from the task breakdown
---

# Task Implementer

## Language Preference

Read `.codexspec/config.yml`. Two independent language controls apply (each falls back to `language.output`, then English):

- **Interaction language** (`language.interaction`): language for all conversation with the user — questions, explanations, status messages, and `codexspec` CLI terminal output.
- **Document language** (`language.document`): language for generated artifact files (requirements/spec/plan/tasks).

Converse in the interaction language and author artifacts in the document language. Apply the project's translation standard to both: translate by meaning (not word-for-word), keep English for terms with no good native equivalent, and write as if originally in that language.

## Feature Resolution

Resolve the feature in this order:

1. Use an explicit path from `$ARGUMENTS` when it identifies a `tasks.md` file
   or feature directory.
2. Otherwise match the current branch, which must use the timestamp format, to
   `.codexspec/specs/<branch>/`.
3. If no unique feature can be resolved, ask the user to select one. Never
   silently select the latest workspace.

Derive all artifact paths from the selected feature directory. All
implementation-side output belongs to that workspace.

## Input Documents and Authority

Read:

- `requirements.md`
- `spec.md`
- `plan.md`
- `tasks.md`
- `.codexspec/memory/constitution.md` when present

Authority order:

1. Confirmed entries in `requirements.md`
2. `spec.md`
3. Constitution and verified repository facts
4. Approved `plan.md`
5. `tasks.md`

When `requirements.md` is absent, use legacy spec-only mode. Treat `spec.md` as
the temporary highest feature authority and state that fidelity to the original
discussion cannot be verified.

## Role

You are an **autonomous implementation agent**. Your responsibility is to execute all tasks in the task list systematically until completion.

## Instructions

### 1. Prerequisites

Before starting, verify that `spec.md`, `plan.md`, and `tasks.md` exist in the
resolved workspace. Stop if tasks conflict with higher-authority artifacts
instead of silently implementing the conflict.

### 2. Tech Stack Detection

Identify the project's technology stack:

1. Check `plan.md` for defined tech stack
2. Verify with project files: `package.json`, `pyproject.toml`, `go.mod`, `Cargo.toml`, etc.
3. Determine conventions: source directory, test directory, test command, package manager

### 3. TDD Workflow (Per Task)

For **each task**, determine the workflow based on task type:

#### Implementation Tasks (code that needs testing)

1. **Red - Write Test First**
   - Write unit tests that define expected behavior
   - Tests should fail initially (no implementation exists yet)

2. **Green - Implement to Pass**
   - Write the minimum code necessary to make tests pass
   - Follow the technical plan and constitution guidelines

3. **Verify - Run Tests**
   - Execute all relevant tests
   - Ensure new tests pass and no existing tests break

4. **Review & Refactor**
   - Check for bugs, edge cases, security issues
   - Improve code readability and maintainability
   - Keep tests green while refactoring

5. **Mark Complete**
   - Update `tasks.md`: change `[ ]` to `[x]`
   - Record any important notes or decisions
   - Continue to next task (respect dependencies)

#### Non-Testable Tasks (docs, config, assets)

Implement directly and verify correctness. Task types that typically don't need tests:

- Documentation (README, API docs, user guides)
- Configuration files (JSON, YAML, TOML)
- Static assets (images, styles, fonts)
- Infrastructure files (Dockerfile, CI/CD configs)

### 4. Autonomous Execution

**Work continuously** until all tasks are completed:

- Do not wait for user approval between tasks
- When encountering blockers:
  - Record the issue in `issues.md` (task ID, error, attempted solutions, status)
  - Continue to the next independent task
- Commit code after completing significant tasks or phases
- Update progress in `tasks.md` as tasks are completed

### 5. Issue Recording

When encountering problems, create/update `issues.md` in the same directory as `tasks.md`:

```markdown
## Issue: [Brief Description]
- **Task**: Task X.X
- **Error**: [Error message or description]
- **Attempted**: [Solutions you tried]
- **Status**: Blocked / Workaround Found / Needs Discussion
```

### 6. Pre-Review Baseline

After all tasks are implemented:

- Run targeted checks, every project-mandated check, and the full suite when
  project instructions require it or shared-boundary impact demands it.
- Run applicable deterministic checks for documentation and configuration.
- Establish a green full-suite baseline before the Final Code Review Loop. No
  repair may regress it. If required verification is red, incomplete, or unsafe
  to execute, resolve that state before review or record the implementation as
  blocked; do not ask the reviewer to turn an invalid baseline into success.

### 7. Final Code Review Loop

After the baseline is green, use the strict defect gate to review and repair the
complete implementation. Review output is untrusted until its machine envelope
and evidence have been validated. The reviewer is review-only; this implementer
owns verification and edits.

#### 7.1 Invoke the Complete Feature Gate

Invoke exactly:

```text
/codexspec:review-code --feature <feature-dir>
```

Replace `<feature-dir>` with the resolved workspace path. Do not pass `--audit`:
an advisory scorecard is never a completion gate. Do not pass a narrowed
selector (`--committed`, `--uncommitted`, or `--commit`) or paths. The default
resolver target must be the complete feature target, including committed,
staged, unstaged, and untracked non-ignored changes.

Do not filter by extension or artifact class. Source, tests, documentation and
configuration, schemas, scripts, workflows, dependency files, generated
artifacts, renames, deletions, binaries, and CodexSpec artifacts all remain in
scope. An empty Git target does not skip confirmed-obligation assessment.

#### 7.2 Validate the Result Before Acting

Locate exactly one `<review-code-result>` block and parse its body as one JSON
object. Prose cannot override, repair, or supply missing machine data. Validate:

- required fields `schema_version`, `mode`, `verdict`, `target`,
  `requirements_coverage`, `verification`, `finding_counts`,
  `coverage_gap_count`, `review_context`, and `reviewers` exist with known types
  and enum values;
- schema version `1` and `mode: defect` are exact;
- target and feature context match this repository, invocation, and resolved
  feature directory; the default selector represents the complete feature;
- `review_context: isolated`, the primary reviewer is `complete`, and every
  required specialist is present and `complete`;
- human findings, counts, coverage gaps, verification commands, and envelope
  values agree.

Treat audit output, multiple or missing envelopes, malformed JSON, unsupported
fields or enums, target mismatch, shared context, incomplete reviewer topology,
or contradictory data as `INCONCLUSIVE`. Never infer success from an empty
finding list or favorable prose.

A successful envelope additionally requires `verdict: PASS`,
`requirements_coverage.status: complete`, `verification.status: complete`, all
P0-P3 counts are zero, and no blocking coverage gap. Any other state enters the
repair, retry, or blocked path below.

#### 7.3 Independently Verify Findings

For every reported P0-P3 finding, independently verify its trigger,
selected-change attribution, impact, and binding obligation against raw code,
artifacts, and deterministic evidence. Do not edit for an unverified finding,
and do not accept or reject a finding because of reviewer confidence alone.

If evidence refutes a finding, record the finding identity and refutation. Do
not edit. A fresh complete review may clear it; the current review remains
non-PASS and cannot be declared successful by the implementer.

If verification requires a new product or architecture decision, stop and
request that decision. Do not invent intent or weaken the requirement.

#### 7.4 Apply Test-Safe Repairs

Apply only verified repairs:

- For a functional defect, first add a reproducing regression test and observe
  the expected failure. Then use red-green-refactor until the defect is fixed
  while existing behavior remains green.
- For documentation and non-code configuration defects, use the applicable
  deterministic checks before and after the repair. Do not manufacture a code
  test when the binding contract is non-code.
- After each repair set, run the relevant targeted checks and all
  project-mandated checks. Re-establish the green full-suite baseline before
  another review.
- If a repair regresses a check, undo only that repair, confirm the prior green
  state, and retry from verified evidence. Never ship, hide, or defer a red
  result.

#### 7.5 Fresh Re-Review and Progress Guards

After every green repair set, invoke the exact complete-feature command from
7.1 with a fresh isolated reviewer. Do not provide previous findings,
implementation reasoning, or repair conclusions to that reviewer. Revalidate
the entire envelope and topology from scratch.

Continue while substantive progress occurs: verified defects are repaired or a
fresh review identifies new actionable defects that can be verified. Maintain
stable finding identities and per-round records so these exact guards can be
enforced:

- stop without success when the same defect survives two verified fixes;
- stop without success when two consecutive rounds make no substantive progress;
- stop without success when a finding requires a new product or architecture decision;
- stop without success when the same independently refuted false positive recurs.

A transient `INCONCLUSIVE` cause such as a reviewer timeout or temporary tool
failure may be retried without edits. Retry it up to two times. Reset the
transient retry count only after a valid review result or a materially different
cause. If the cause persists, is deterministic, or reflects missing evidence,
remain `INCONCLUSIVE`; do not turn it into a finding or success.

There is no fixed round count while substantive progress continues, but every
guard above is mandatory. No finding may be deferred, waived, severity-filtered,
or cleared by an audit score.

#### 7.6 Terminal Status

Success requires a final valid `PASS` envelope from a fresh complete-feature
review, with complete requirements and verification, isolated required reviewer
topology, zero P0-P3 counts, no blocking coverage gaps, and a still-green
baseline.

Any `FAIL`, persistent `INCONCLUSIVE`, unresolved verified defect, repeated
refuted finding, decision requirement, or no-progress guard is blocking. Preserve
the report, envelope, reproduction/refutation evidence, attempted repairs, and
test state. It must not be converted to success by prose, score, elapsed effort,
or a commit.

### 8. Final Report and Commit

- Report completed tasks, files changed, verification commands and outcomes,
  review rounds, verified repairs, refuted findings, unresolved evidence, and
  the final envelope verdict.
- Report success only under 7.6. Otherwise report `FAIL` or `INCONCLUSIVE` and
  the exact blocking evidence.
- Commits remain outside verdict logic. If the surrounding workflow calls for
  a commit, create it only after the applicable checks are green; a commit must
  never alter, replace, or imply the review verdict.
