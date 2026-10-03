---
name: codexspec:generate-spec
description: "将已确认的需求编写为可追溯的 spec.md"
---

# Specification Generator

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

`the text after the $codexspec:generate-spec skill mention`

## Role

Act as a **requirements compiler**. Convert the persistent, user-confirmed decision record into `spec.md` without changing product intent.

## Authority Order

1. Confirmed entries in `requirements.md`
2. Existing `spec.md` when operating in legacy compatibility mode
3. Project constitution and verified repository facts
4. Explicit assumptions, which are never equivalent to confirmed requirements
5. General best practices

## Feature Resolution

1. If `the text after the $codexspec:generate-spec skill mention` identifies a `requirements.md` file or feature directory, use it.
2. Otherwise match the current git branch to `.codexspec/specs/<branch>/`.
3. If there is no unique match, ask the user to select a feature. Never silently select the latest directory.
4. If `requirements.md` is absent but an existing `spec.md` is present, use legacy compatibility mode:
   - Treat `spec.md` as the temporary highest authority.
   - State that fidelity to the original discussion cannot be verified.
   - Do not regenerate it from guessed requirements.
5. If neither artifact exists, stop and direct the user to `$codexspec:specify`.

## Compilation Rules

- Read all `NEED-*`, `CON-*`, `DEC-*`, `OUT-*`, and `OPEN-*` entries.
- Only entries with `Status: confirmed` may become binding requirements.
- Preserve `open` entries as unresolved questions. Do not turn them into requirements.
- Ignore `superseded` entries except for historical context.
- Use `REQ-xxx` consistently for functional requirements and `NFR-xxx` for non-functional requirements.
- Every requirement must include `Sources: NEED-xxx, CON-xxx, DEC-xxx`.
- Preserve confirmed exclusions in Out of Scope.
- Add an assumption only when required to make the document understandable. Label it clearly and do not use it to expand scope.
- If confirmed entries conflict, or a critical open item prevents a single faithful specification, stop and report the conflict instead of choosing an interpretation.

## Required Output

Use the appropriate simple or detailed template from `.codexspec/templates/docs/`.

The specification must include:

- Context and goals
- User stories or user-visible scenarios where applicable
- `REQ-*` and `NFR-*` items with `Sources:`
- Acceptance criteria and expected error behavior
- Confirmed constraints and decisions
- Open questions that block later work
- Out of Scope
- A traceability table mapping every confirmed requirements entry to spec coverage

Do not add sections merely to satisfy a template when they are irrelevant.

Save to `<feature-dir>/spec.md`.

## Pre-Save Validation

Before saving:

1. Verify every confirmed `NEED`, `CON`, `DEC`, and `OUT` entry is represented or explicitly marked not applicable with a reason.
2. Verify every `REQ`/`NFR` has at least one valid source.
3. Verify no `OPEN` or AI inference was presented as confirmed.
4. Verify terminology and scope remain consistent with `requirements.md`.
5. Stop if any discrepancy would require a new user decision.

## Automatic Review Loop

Invoke `$codexspec:review-spec <feature-dir>/spec.md` after saving.

- Automatically fix only verified defects whose remediation is directly determined by confirmed upstream evidence.
- Never auto-fix Risk Advisories or Design Opportunities.
- Never introduce a new product decision during auto-fix.
- Run a maximum of two automatic fix-and-review rounds.
- If defects remain, the same defect repeats, or remediation requires a user decision, stop and report the evidence.

## Auto-Dev Delegation

When the invocation context explicitly contains `CODEXSPEC_AUTO_DEV_DELEGATION`, execute this
command and its review gate normally, return the resulting pass or stop state to `auto-dev`, and
skip the entire **Auto-Next Chain Advance** section below. Do not read `workflow.auto_next` in that
delegated invocation. Direct invocations are unchanged.

## Auto-Next Chain Advance

Read `workflow.auto_next` from `.codexspec/config.yml` (default `false`; only the literal value `true` enables it — absent, `false`, or any other value means disabled).

When `workflow.auto_next` is `true` AND the Automatic Review Loop above concluded in a passing state — the final Overall Status is `PASS` or `PASS_WITH_WARNINGS` — advance the chain automatically:

1. Emit exactly one notice line, in the interaction language, e.g. `auto_next: review passed → invoking $codexspec:spec-to-design <feature-dir>`.
2. Invoke `$codexspec:spec-to-design <feature-dir>` exactly once, then end this command.

Do not auto-advance when `workflow.auto_next` is disabled, or the review loop stopped at `NEEDS_REVISION` or `BLOCKED`, or stopped early per the conditions above; in those cases hand control back to the user exactly as the review loop already does. This advances the chain and does not modify the Output Summary.

## Output Summary

Report:

- Spec path
- Confirmed requirement coverage
- Open items
- Auto-review status and number of rounds
