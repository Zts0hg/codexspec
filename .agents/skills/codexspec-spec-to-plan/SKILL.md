---
name: codexspec:spec-to-plan
description: "将已确认的设计转换为可追溯的实现计划"
---

# Specification to Plan Converter

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

`the text after the $codexspec:spec-to-plan skill mention`

## Role

Act as an **implementation planner**. Define how to build the confirmed design in phases while preserving confirmed user intent. The design (`design.md`) already defines *what* the system is — architecture, components, interfaces, and key design decisions. Do not redo that design here: consume it and plan *how* to implement it (phases, ordering, verification).

## Feature Resolution

Use an explicit path first, then the current branch. If neither uniquely identifies a feature, ask the user to select one. Never silently select the latest feature.

Read:

- `requirements.md`
- `spec.md`
- `design.md`
- `.codexspec/memory/constitution.md` when present
- Relevant repository files needed to verify existing patterns and constraints

Design-stage compatibility: if `design.md` is absent (a legacy feature created before the design stage), plan directly from `spec.md` and state that no separate design artifact was available.

Legacy compatibility: if `requirements.md` is absent, treat `spec.md` as the temporary highest authority and disclose that original-discussion fidelity cannot be checked.

## Authority and Stop Conditions

Authority order:

1. Confirmed `requirements.md`
2. `spec.md`
3. Constitution and verified repository facts
4. `design.md`
5. Plan-level technical decisions
6. General best practices

Before planning, verify that `spec.md` covers the confirmed requirements and that `design.md` covers the spec. Stop if either omits, contradicts, or silently expands them.

Stop and request a user decision when:

- The plan would change confirmed scope, behavior, constraints, or trade-offs.
- Two reasonable approaches produce materially different user outcomes.
- A critical `OPEN-*` item blocks a safe design.
- The specification conflicts with the constitution or verified repository facts.

## Planning Rules

- Consume `design.md`: the plan implements the confirmed design; it does not re-architect or introduce new components/interfaces beyond it. If the design is insufficient to plan against, stop and hand back to the design stage rather than designing here.
- Every implementation phase and plan component must include `Covers: REQ-xxx; Design: <design component>` — trace both to the ultimate requirement and to the design component it builds. (When planning a legacy feature with no `design.md`, fall back to `Covers: REQ-xxx`.)
- Record new implementation-level choices (build ordering, tooling, sequencing) as **Plan-Level Decisions** with evidence, rationale, alternatives considered when material, and accepted trade-offs. Architecture / interface / data-model decisions belong to `design.md`, not here.
- Plan-level decisions may refine implementation but cannot redefine product intent or the confirmed design.
- Reuse repository patterns before introducing new abstractions or dependencies.
- Explicitly identify assumptions. Do not convert assumptions into requirements.
- Prefer the smallest plan that delivers the confirmed design.

## Required Output

Save `<feature-dir>/plan.md` using the appropriate simple or detailed template.

Include:

- Context, goals, and non-goals inherited from the specification and design
- Relevant existing repository constraints
- Implementation approach and plan-level decisions (build ordering, tooling, sequencing)
- Implementation phases and units, each with `Covers: REQ-xxx; Design: <design component>`
- Verification strategy
- Risks and trade-offs that affect delivery
- Requirements coverage table mapping every `REQ`/`NFR` to plan references and the design component realized

Do not force a standard five-phase structure when the design calls for a different sequence. Do not restate the architecture/component design — reference `design.md`.

## Pre-Save Validation

1. Every binding spec requirement and every design component has plan coverage.
2. Every plan unit maps to a requirement/design component or is identified as necessary implementation support.
3. No plan decision changes confirmed behavior or the confirmed design.
4. File paths and repository assumptions are verified where practical.
5. Unresolved conflicts cause the command to stop rather than guess.

## Automatic Review Loop

Invoke `$codexspec:review-plan <feature-dir>/plan.md`.

- Automatically fix only verified defects with a deterministic remediation supported by upstream evidence or repository facts.
- Do not auto-fix advisories or choose among materially different designs.
- Run a maximum of two automatic fix-and-review rounds.
- Stop if a defect repeats, remains unresolved, or requires a user decision.

## Auto-Dev Delegation

When the invocation context explicitly contains `CODEXSPEC_AUTO_DEV_DELEGATION`, execute this
command and its review gate normally, return the resulting pass or stop state to `auto-dev`, and
skip the entire **Auto-Next Chain Advance** section below. Do not read `workflow.auto_next` in that
delegated invocation. Direct invocations are unchanged.

## Auto-Next Chain Advance

Read `workflow.auto_next` from `.codexspec/config.yml` (default `false`; only the literal value `true` enables it — absent, `false`, or any other value means disabled).

When `workflow.auto_next` is `true` AND the Automatic Review Loop above concluded in a passing state — the final Overall Status is `PASS` or `PASS_WITH_WARNINGS` — advance the chain automatically:

1. Emit exactly one notice line, in the interaction language, e.g. `auto_next: review passed → invoking $codexspec:plan-to-tasks <feature-dir>`.
2. Invoke `$codexspec:plan-to-tasks <feature-dir>` exactly once, then end this command.

Do not auto-advance when `workflow.auto_next` is disabled, or the review loop stopped at `NEEDS_REVISION` or `BLOCKED`, or stopped early per the conditions above; in those cases hand control back to the user exactly as the review loop already does. This advances the chain and does not modify the Output Summary.

## Output Summary

Report the plan path, requirement coverage, plan-level decisions, unresolved items, and auto-review status.
