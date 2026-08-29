---
name: codexspec:implement-tasks
description: "执行实现任务，支持条件 TDD 工作流（代码使用 TDD，文档/配置直接实现）"
---

# Task Implementer

## Language Preference

Read `.codexspec/config.yml`. Two independent language controls apply (each falls back to `language.output`, then English):

- **Interaction language** (`language.interaction`): language for all conversation with the user — questions, explanations, status messages, and `codexspec` CLI terminal output.
- **Document language** (`language.document`): language for generated artifact files (requirements/spec/plan/tasks).

Converse in the interaction language and author artifacts in the document language. Apply the project's translation standard to both: translate by meaning (not word-for-word), keep English for terms with no good native equivalent, and write as if originally in that language.

## Feature Resolution

Resolve the feature in this order:

1. Use an explicit path from `the text after the $codexspec:implement-tasks skill mention` when it identifies a `tasks.md` file
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
- `design.md`
- `plan.md`
- `tasks.md`
- `.codexspec/memory/constitution.md` when present

Authority order:

1. Confirmed entries in `requirements.md`
2. `spec.md`
3. Constitution and verified repository facts
4. `design.md`
5. Approved `plan.md`
6. `tasks.md`

A legacy feature may have no `design.md`; when it is absent, proceed with `plan.md` as the design-and-plan authority.

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
   - If a test stays red across several green attempts, a fix reddens a previously-passing test, or you catch yourself guessing: stop patching and follow **Systematic Debugging Escalation** (below)

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
$codexspec:review-code --feature <feature-dir>
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
  `requirements_coverage`, `verification`, `findings`, `finding_counts`,
  `review_coverage`, `follow_up`, `coverage_gaps`, `coverage_gap_count`,
  `review_context`, and `reviewers` exist with known types and enum values;
- schema version `2` and `mode: defect` are exact; reject schema version `1`
  explicitly as unsupported instead of migrating or inferring missing coverage;
- target and feature context match this repository, invocation, and resolved
  feature directory; the default selector represents the complete feature, and
  the target fingerprint is a non-empty deterministic identifier for the exact
  reviewed target evidence;
- all target members (`selector`, `fingerprint`, `complete_feature`, `empty`,
  refs/SHAs, and `inventory_count`) exist with known types, and target emptiness
  agrees with the inventory count; `default` and `committed` require base and
  merge-base identity, `uncommitted` carries no base or commit identity, and
  `commit` carries commit and parent identity but no base identity;
  `uncommitted` and `commit` are not complete features, complete or partial
  requirements coverage requires a feature, and complete requirements coverage
  additionally requires a complete-feature target;
- `review_context: isolated`, the primary reviewer is `complete`, and every
  required specialist is present and `complete`;
- finding, contract, partition, root-cause, follow-up, and coverage-gap IDs are
  unique within their entity types; every current-result cross-reference and
  outgoing follow-up source resolves in the current result; every incoming
  follow-up source resolves in the retained originating schema-v2 result
  identified by its fingerprint; and every completed coverage record has
  evidence;
- the top-level object and every nested record contain no undeclared fields;
  every `specialist:<profile>` partition owner resolves to one uniquely declared
  specialist reviewer with that exact profile, and a specialist marked
  `not_required` owns no partition;
- finding counts match the `findings` array, coverage-gap count matches the
  `coverage_gaps` array, incomplete/not-applicable searches include reasons,
  follow-up states are valid for their received or required direction, a null
  fingerprint has a blocking gap whose scope is exactly `target identity`, and
  `INCONCLUSIVE` contains no admitted finding;
- human findings, counts, coverage gaps, verification commands, and envelope
  values agree.

Treat audit output, multiple or missing envelopes, malformed JSON, unsupported
fields or enums, target mismatch, shared context, incomplete reviewer topology,
or contradictory data as `INCONCLUSIVE`. Never infer success from an empty
finding list or favorable prose.

A successful envelope additionally requires `verdict: PASS`,
`requirements_coverage.status: complete`, `verification.status: complete`, all
P0-P3 counts are zero, mandatory contract coverage and all review partitions are
complete, every required root-cause variant search is complete, every received
follow-up obligation is verified or validly superseded with evidence, there is
no open or unresolved follow-up obligation, and no blocking coverage gap. Any
other state enters the repair, retry, or blocked path below.

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

#### 7.3b Retain Neutral Cross-Round Obligations

For every valid non-PASS schema-v2 result, retain the union of neutral
obligations from `follow_up.required` that remain applicable after repair and
incoming records from `follow_up.received` whose `status: unresolved` remains
applicable. Do not retain incoming records marked `verified` or `superseded`.
The obligations may have been derived from findings, contracts, partitions, or
incomplete searches, but do not transmit the completed coverage records or
variant-search records themselves. Preserve each obligation's stable ID,
source IDs, objective statement, and originating target fingerprint in the
caller's execution context. Reject conflicting records with the same ID rather
than choosing one. Do not create repository-local review-state files.

The retained handoff states only the behavior or evidence to re-establish. It
must exclude implementation reasoning, prior correctness conclusions, previous
finding prose beyond stable source identities, and assertions that a repair
succeeded. If a required obligation cannot be associated with its originating
target or represented without such a conclusion, keep it unresolved and treat
the next result as `INCONCLUSIVE`.

#### 7.3a Scenario Coverage Self-Check

Independently of the reviewer — do not extend or rely on `review-code` for this —
verify that every test scenario enumerated in `tasks.md` maps to at least one
implemented test that genuinely exercises and asserts it. A scenario with no
covering test, or covered only by a hollow or non-asserting test (the test must
assert the scenario's expected outcome), is a blocking scenario-coverage gap.

Treat each gap as a verified obligation and repair it via 7.4 (red-green: add the
covering test, observe it fail for the missing behavior, then make it pass), then
re-verify and re-review per 7.5. This check is owned by this implementer; it adds
no command and does not modify `review-code`.

#### 7.4 Apply Test-Safe Repairs

Apply only verified repairs:

- For a functional defect, first add a reproducing regression test and observe
  the expected failure. Then use red-green-refactor until the defect is fixed
  while existing behavior remains green. When such a repair is non-trivial — the
  cause is not a mechanical local edit but must be traced across call chains,
  state, or data flow — follow **Systematic Debugging Escalation** (below).
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
7.1 with a fresh isolated reviewer. Supply only the retained neutral follow-up
obligations from 7.3b as incoming work, including each originating target
fingerprint, source IDs, and objective statement. Do not provide completed
prior coverage or variant-search records, previous finding prose,
implementation reasoning, prior correctness conclusions, or assertions that a
repair succeeded.

The fresh isolated reviewer must associate incoming obligations with the
originating target, verify each obligation independently against the updated
target and its new fingerprint, and still execute all five general passes:
Scope, System Contract, Behavior, Risk, and Verification. Incoming obligations
supplement rather than replace this complete review. Revalidate the entire
schema-v2 envelope and reviewer topology from scratch; any unresolved,
unvalidated, or unassociated required obligation is `INCONCLUSIVE`.

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
review, with complete requirements, contract and partition coverage, variant
searches, received follow-up verification, and deterministic verification;
isolated required reviewer topology; zero P0-P3 counts; no open or unresolved
follow-up; no blocking coverage gaps; no uncovered enumerated test scenario
from `tasks.md` (per 7.3a); and a still-green baseline.

Any `FAIL`, persistent `INCONCLUSIVE`, unresolved verified defect, repeated
refuted finding, decision requirement, or no-progress guard is blocking. Preserve
the report, envelope, reproduction/refutation evidence, attempted repairs, and
test state. It must not be converted to success by prose, score, elapsed effort,
or a commit.

### 8. Final Report and Commit

- Report completed tasks, files changed, verification commands and outcomes,
  review rounds, verified repairs, refuted findings, retained and resolved
  follow-up obligations, unresolved evidence, and the final envelope verdict.
- Report success only under 7.6. Otherwise report `FAIL` or `INCONCLUSIVE` and
  the exact blocking evidence.
- Commits remain outside verdict logic. If the surrounding workflow calls for
  a commit, create it only after the applicable checks are green; a commit must
  never alter, replace, or imply the review verdict.

## Systematic Debugging Escalation

When a fix is not converging, escalate into the systematic root-cause discipline instead of continuing to patch. This is a reference, not a duplicate: the discipline lives once in `$codexspec:debug`.

**Trip conditions** (either one):

- **(a) During the TDD Verify/green loop (§3)**: the same test stays red after several green attempts, a fix reddens a previously-passing test, or you notice guess-and-check behavior.
- **(b) During a test-safe repair (§7.4)**: you are fixing a **functional/correctness (or robustness) defect** whose fix is **non-trivial** — it requires tracing across call chains, state, or data flow, not a mechanical local edit. This trip does NOT apply to idiomatic-clarity, architecture, constitution-alignment, style, or trivial mechanical fixes.

**Escalation**:

```text
Invoke $codexspec:debug
```

Apply its root-cause discipline to the failing test (trip a) or the defect under repair (trip b). The escalation is **non-gating and low-ceremony**: it produces no PASS/FAIL, emits no mandatory notice line, and does not interrupt the user.

**Resume**: once `debug` has reached the root cause and applied a verified fix, **return here and continue** the task or repair exactly where you left off — re-establish the green baseline and proceed. There is no runtime stack; resuming is your responsibility, not the engine's.

## Automatic Distillation

Read `workflow.auto_distill` from `.codexspec/config.yml` (**default `true`** — enabled unless explicitly set to the literal `false`; absent or any non-`false` value means enabled).

When `workflow.auto_distill` is enabled (not the literal `false`) AND this command reported success (§7.6), invoke `$codexspec:distill` exactly once on this session's interaction, then end.

- distill is non-blocking and non-interactive: it never prompts, never changes this command's verdict or report, and early-exits when there is nothing reusable to capture.
- distill only writes `candidate`/`vetted` records to `.codexspec/profile/`; it MUST NOT modify `requirements.md`, `spec.md`, `plan.md`, or `tasks.md`.
- Do not invoke distill when `auto_distill` is disabled or when this command did not report success.
