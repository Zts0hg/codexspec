---
name: codexspec:plan-to-tasks
description: "将已批准的计划展开为可追溯、可执行的任务"
---

# Plan to Tasks Converter

## Language Preference

Read `.codexspec/config.yml`. Two independent language controls apply (each falls back to `language.output`, then English):

- **Interaction language** (`language.interaction`): language for all conversation with the user — questions, explanations, status messages, and `codexspec` CLI terminal output.
- **Document language** (`language.document`): language for generated artifact files (requirements/spec/plan/tasks).

Converse in the interaction language and author artifacts in the document language. Apply the project's translation standard to both: translate by meaning (not word-for-word), keep English for terms with no good native equivalent, and write as if originally in that language.

## Expression Standard

**IMPORTANT**: Everything this command produces — documents, reviews, reports, commit messages, diagnostics, and replies — is written for a reader who cannot see your working context. Apply the rules below to every artifact and message you output:

- **Write for the reader at hand-off.** Every reference must resolve without access to this session: no session-only identifiers or section numbers, no narration of what changed during the conversation, no arguments with absent reviewers. State current reality and cite committed, reachable sources.
- **Preserve every proposition.** Before summarizing or trimming, list the facts a passage carries: actors, conditions, ordering, modalities (must, never), negative guarantees, and consequences. Remove only reasoning transcripts, repetition, and decoration. Shorter is not clearer if any fact is lost.
- **State what the surface requires.** Diagnostics name what failed, which rule was violated, and the correction. Problem reports carry the defect, its location, its impact, and the evidence. Decisions record the alternatives they beat. Rejections give the reason in one line. Shipped work is described in the present tense; plans and open questions are labeled as such.
- **Define terms before relying on them.** Prefer the concrete rule, field, or behavior over a coined label; give a project-specific term a plain-language definition at first use, then use it consistently.
- **Be honest, not agreeable.** Verify claims before accepting them; fix or rebut on technical grounds. One substantiated blocker is worth more than a list of nitpicks. When a decision is needed, present only viable options, recommend one, and state the real difference between them.
- **Declare what is binding.** Say explicitly which instructions are hard requirements and where judgment is required. Keep one explanation in one place and link to it, but keep at the point of use the contract a reader needs there.

## Workspace Routing Before Writes

This section governs the location of every later file, index, branch, and commit mutation.
Record `SOURCE_ROOT` as the explicitly selected checkout (otherwise the invoking checkout) before
changing working directories. Read its `.codexspec/config.yml`: `workflow.worktrees` defaults to
on; only the literal boolean `false` disables it. Configuration remains checkout-local. Read-only
inspection keeps its original source target and does not create a worktree merely to read files.

- With `CODEXSPEC_AUTO_DEV_DELEGATION`, use the dedicated worktree supplied by auto-dev as
  `OUTPUT_ROOT` throughout. `blueprint` and `auto-dev` themselves retain their existing fixed branch
  `codexspec/auto-dev` and worktree `worktree-for-codexspec-auto-dev`; they always use the new shared
  `<repository-name>-codexspec-worktrees` parent, irrespective of the ordinary isolation switch.
- With ordinary isolation disabled, `OUTPUT_ROOT` is `SOURCE_ROOT` and existing in-place behavior
  applies. `codexspec init`, both first-time setup and installation updates, is explicitly exempt:
  it operates on its selected checkout regardless of this switch.
- For a new ordinary feature (`specify`, `quick`, or another feature-creation entry), invoke the
  installed platform create-new-feature script or `codexspec _worktree-helper create --name
  <short-name>` before the first artifact write. Parse returned JSON rather than evaluating shell
  output. `workspace`, `feature_dir`, and `requirements_file` are absolute paths; `branch` is the
  full `<feature-id>-<feature-name>`. Set `OUTPUT_ROOT` to that workspace.
- For an existing ordinary feature, resolve its explicit feature path/name first, otherwise its
  current feature branch, using `codexspec _worktree-helper resolve --feature <full-feature-name>`.
  Reuse that returned worktree. Do not silently pick another feature or create a replacement
  from main. If an explicit feature path names another checkout, use that checkout's configuration
  and preserve the identity of its documents and code.
- For standalone project-level writes without a selected ordinary feature, use
  `codexspec _worktree-helper route` from `SOURCE_ROOT`. An active feature workspace is reused;
  otherwise the helper uses `worktree-for-codexspec-maintenance`. Use the returned absolute
  workspace as `OUTPUT_ROOT`. Revalidate both source and destination rather than interpreting an
  arbitrary existing directory as a managed workspace.

When creation is interrupted, retain the returned `branch` and `workspace` even in an error
response. Resume the same identity with `codexspec _worktree-helper create --feature
<full-feature-name>`; a `creating` response from resolve requires this recovery step before
merge verification. A new `--name` request never adopts an existing identity after a random
name collision; report that collision and retry a new identity only for a genuinely new feature.

A `ready` response is required before writing feature artifacts or continuing development. Exit
status 3 with `merge_requires_resolution` or `merge_requires_verification` is a preparation handoff,
not success. Resolve conflicts and complete the merge only in the returned worktree, run the
project's required checks, and call `codexspec _worktree-helper finish --feature <full-feature-name>
--verification <json-file>` (use `worktree-for-codexspec-maintenance` for maintenance preparation).
The temporary JSON contains the verified `head`, `tree`, and `checks` entries with `command` and
integer `exit_code`; never claim a check ran when it did not. If conflicts cannot be resolved or
verification fails, stop. Retain the returned feature identity for continuation; do not create a
second feature to bypass failed preparation. Fetch warnings mean remote information may be stale;
they do not authorize bypassing an invalid baseline or failed verification.

Every mutating tool call and later SDD invocation must explicitly use `OUTPUT_ROOT` or paths inside
it. Before each file write, verify real filesystem containment: refuse symbolic links in the
output path and existing destination files with multiple hard links. A lexical path beneath
`OUTPUT_ROOT` alone does not establish isolation; never write through a link into another checkout.
A `cd` in one shell subprocess does not change the agent's later tool working directories.
Carry the same absolute workspace across stage handoffs. If required installation assets are
absent in a new worktree, run normal installation explicitly against that destination, preserving
existing project-authored files; stop if the required runtime or setup is unavailable.

Preserve input provenance: artifact-only reviews/reverse specification can read `SOURCE_ROOT`
while writing reports to `OUTPUT_ROOT`; their artifact containment checks apply to `OUTPUT_ROOT`.
Source edits and executable checks use the selected feature workspace. `commit-staged` preview
reads the original index; execution must stop if routing would substitute a different index or
mutate the protected main checkout. Do not copy, stash, stage, reset, or discard caller-owned changes
to make routing appear successful. Report an incompatible input/workspace and the required target
instead. Existing command-specific prohibitions still apply.

For configuration edits, decide routing from `SOURCE_ROOT`'s setting, then read and modify the
configuration in `OUTPUT_ROOT`. A bare toggle uses the destination's value. Report the exact path
and explain that other checkouts receive the setting through Git integration; do not add a shared
override or imply immediate changes to main's effective value. Completion retains worktrees; it
does not automatically merge to main or delete them. Any occupied path, invalid identity, failed
creation, or unusable baseline is an explicit stop, never permission to fall back to main writes.

## User Input

`the text after the $codexspec:plan-to-tasks skill mention`

## Role

Act as a **plan expander**. Produce implementation tasks that execute the approved plan without redesigning it.

## Feature Resolution and Inputs

Use an explicit path first, then the current branch. Ask the user if the feature cannot be resolved uniquely; never select the latest directory silently.

Read:

- `requirements.md`
- `spec.md`
- `design.md`
- `plan.md`
- Constitution and relevant repository conventions

`design.md` (the confirmed design) sits between `spec.md` and `plan.md` in authority; read it as context so tasks trace to the design the plan implements. A legacy feature may have no `design.md`; proceed from `plan.md` in that case.

Legacy compatibility: when `requirements.md` is absent, use `spec.md` as the temporary highest authority and state the limitation.

## Stop Conditions

Before task generation, verify that the plan covers the specification and does not contradict confirmed requirements.

Stop instead of guessing when:

- A plan component is undefined or internally contradictory.
- A task would require a new architecture or product decision.
- Required file paths or dependencies cannot be determined safely.
- A critical upstream item remains open.

## Task Rules

- Every task must include `Covers: REQ-xxx; Plan: <component/phase>`.
- A task must have one clear, verifiable outcome.
- Do not equate atomicity with exactly one file. Multiple tightly related files may belong to one task when splitting them would make validation artificial or incomplete.
- Use exact paths when they are known from the plan or repository; do not invent paths to satisfy a template.
- Preserve the plan's organization. Group by user story, component, or technical phase according to the approved plan.
- Declare only dependencies that are needed to execute or validate the task.
- Mark `[P]` only when tasks can actually run concurrently after their declared dependencies. Missing `[P]` is not inherently a defect.
- Require test-first ordering only when mandated by the constitution, specification, plan, or established repository workflow.
- Otherwise include the appropriate verification task without imposing TDD as a universal method.
- For every **testable** task, enumerate an explicit, individually identifiable **Test Scenarios** list: the happy path plus the boundary and error conditions the behavior implies. Non-testable tasks (docs, config, assets, infrastructure) keep their deterministic verification and do not carry test scenarios.
- Derive test scenarios from the specification's acceptance criteria and the covered requirement's behavior, expanding them into concrete cases; never invent scenarios with no upstream basis. If upstream behavior is too underspecified to enumerate meaningful scenarios, stop per the Stop Conditions rather than guessing.
- Keep each scenario individually identifiable and traceable so implementation and the `implement-tasks` self-check can map each scenario to a test one-to-one. Do not pad: enumerate only scenarios the behavior actually implies.
- Do not add polish, monitoring, abstraction, documentation, or hardening tasks unless they are required by the approved plan, repository policy, or a verified implementation need.

## Required Output

Save `<feature-dir>/tasks.md`.

Include:

- Task groups derived from the plan
- Task IDs, outcomes, paths, dependencies, and traceability
- Verification steps and checkpoints appropriate to the change
- An explicit **Test Scenarios** list for every testable task (happy path plus behavior-implied boundary/error cases), each scenario individually identifiable
- A coverage table mapping plan components and requirements to tasks, including scenario-to-task mapping for testable tasks
- Unmapped tasks, if any, with explicit justification

## Pre-Save Validation

1. Every plan deliverable has task coverage.
2. Every task maps to upstream authority or necessary implementation support.
3. Dependencies are acyclic and ordered before dependents.
4. Verification is sufficient for the actual risk and project policy.
5. No task expands product scope or silently changes the plan.
6. Every testable task enumerates sufficient, individually traceable test scenarios (happy path plus behavior-implied boundary/error), all derived from upstream behavior with none invented.

## Automatic Review Loop

Invoke `$codexspec:review-tasks <feature-dir>/tasks.md`.

- Automatically fix only verified defects with deterministic corrections.
- Do not auto-apply Risk Advisories or Design Opportunities.
- Do not split or add tasks solely to improve a score.
- Run a maximum of two automatic fix-and-review rounds.
- Stop if defects repeat, remain unresolved, or require a user or architecture decision.

## Automatic Cross-Artifact Analysis

When the review loop above concludes in a passing state — the final `$codexspec:review-tasks` Overall Status is `PASS` or `PASS_WITH_WARNINGS` — invoke `$codexspec:analyze <feature-dir>` exactly once.

- Do not invoke analyze when the review loop stopped at `NEEDS_REVISION` or `BLOCKED`, or stopped early per the conditions above; in those cases end here, handing control back to the user as the review loop already does.
- analyze runs once. It auto-remediates deterministic, authority-directed inconsistencies (conforming `spec.md`/`plan.md`/`tasks.md` to `requirements.md`; it never edits `requirements.md`) and reports the result. Do not run a fix-and-reanalyze loop.
- If `requirements.md` is absent, analyze still runs in legacy mode, reports findings only (no auto-modification), and discloses its legacy limitation (it starts at `spec.md` and cannot verify fidelity to the original discussion) per its own behavior.
- analyze's deterministic conforming fixes need no re-review; its remediations and any residual findings do not add a gate before `$codexspec:implement-tasks`.
- Do not modify the Output Summary for analyze, and do not save an additional analyze report file; analyze's own output is the report.

## Auto-Dev Delegation

When the invocation context explicitly contains `CODEXSPEC_AUTO_DEV_DELEGATION`, execute this
command, its task review, and cross-artifact analysis normally; return the resulting pass or stop
state to `auto-dev`, and skip the entire **Auto-Next Chain Advance** section below. Do not read
`workflow.auto_next` in that delegated invocation. Direct invocations are unchanged.

## Auto-Next Chain Advance

Read `workflow.auto_next` from `.codexspec/config.yml` (default `false`; only the literal value `true` enables it).

When `workflow.auto_next` is `true` AND the review loop above concluded in a passing state (`PASS` or `PASS_WITH_WARNINGS`) — after the analyze step above has run — advance the chain automatically:

1. Emit exactly one notice line, in the interaction language, e.g. `auto_next: review passed → invoking $codexspec:implement-tasks <feature-dir>`.
2. Invoke `$codexspec:implement-tasks <feature-dir>` exactly once, with no confirmation prompt, then end this command.

analyze's deterministic auto-fixes and any residual findings do NOT block this advance (see the Automatic Cross-Artifact Analysis section above). Do not auto-advance when `workflow.auto_next` is disabled, or the review loop stopped at `NEEDS_REVISION` or `BLOCKED`, or stopped early; hand control back to the user as the review loop already does. This advances the chain and does not modify the Output Summary.

## Output Summary

Report the tasks path, plan/requirement coverage, dependency summary, unresolved items, and auto-review status.
