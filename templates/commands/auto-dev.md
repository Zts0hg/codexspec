---
description: Autonomously develop every pending requirement in the shared blueprint
argument-hint: ""
---

# Continuous Blueprint Development

## Language Preference

Read `.codexspec/config.yml`. Converse in `language.interaction` and author SDD artifacts in
`language.document`, each falling back to `language.output`, then English.

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

## Goal

Continuously run the complete Requirements-First SDD flow for the shared blueprint in document
order. Requirements in the blueprint are already confirmed. Do not ask the user to reconfirm them,
perform new requirements discovery, or depend on `workflow.auto_next`.

## Run Ownership and Finalization

1. Run `codexspec _auto-dev-helper acquire` with `{}` on stdin. If another live run owns the
   repository, report it and exit immediately without waiting.
2. Keep the returned opaque `token`. Run `renew` before and after each stage and tool operation. If
   an operation can run longer than the returned `heartbeat_interval_seconds`, keep calling `renew`
   at that interval until it finishes. Run `assert-owner` immediately before every repository
   mutation. Never reuse a token after an ownership failure.
3. Inspect the returned `merge_recovery`. When it reports `needs_resolution`, this run has fenced an
   interrupted synchronization merge to its new token; edit every conflicted file and call
   `prepare-sync-verification` with the token and the exact complete `resolved_paths` list before
   running checks. When it reports `needs_verification`, use the
   existing merge result as the verification candidate. Run the project's required baseline checks
   and call `continue-sync`, or call `abort-sync` if conflict preparation or a passing baseline
   cannot be completed. Then repeat `sync-default` until it returns `clean`, and run the baseline
   checks once more before selecting any requirement.
4. On every normal success or controlled stop, call `release` in finalization. An unexpected
   termination is recovered by stale-owner reclamation on the next invocation.
5. `blueprint` remains allowed while this run is active; do not hold a blueprint or Git lock while
   interpreting documents or implementing code.

Use the returned `worktree_path` as the working directory for every direct file read or write, SDD
stage invocation, project check, test, review, and conflict edit in this run. Relative paths in this
command are relative to that dedicated worktree, never to the checkout that invoked `auto-dev`.

All hidden auto-dev helper actions receive exact JSON on stdin. Except `acquire`, each includes the
returned `token`.

## Select Work

Call `codexspec _blueprint-helper inspect` and validate the complete document.

1. If any block is `in_progress`, resume it before considering pending work. Use its recorded
   `Feature Directory`; never change it back to pending and never create a second directory.
2. Otherwise, if no block is pending, inspect once more, release ownership, and end successfully.
3. Otherwise, before selecting work, call `_auto-dev-helper sync-default`. A fetch warning is
   non-blocking and must not suppress a fresh sync/fetch attempt before the next pending requirement.
4. If synchronization returns `needs_resolution`, edit conflicts autonomously and call
   `prepare-sync-verification` with exactly
   `{"token":"<token>","resolved_paths":["<every conflict path>"]}`. This helper rejects an
   incomplete or expanded path list and remaining conflict markers, stages only those literal paths
   under the shared Git lock, and must return `needs_verification`. If synchronization already returns `needs_verification`, use
   that completed merge as the check candidate. Run the project's required baseline checks and call
   `continue-sync` with `checks_passed: true` only after restoring a passing baseline. If conflict
   preparation or checks cannot pass, call `abort-sync`, release ownership, and stop while the next
   block remains pending. Never run `git add` or commit the synchronization merge directly.
5. After every successful `continue-sync`, repeat `sync-default` so all locally available local and
   remote-tracking default refs are merged and verified. When `sync-default` returns `clean`, run the
   required baseline checks even when no merge was needed. Stop before changing pending status if
   that baseline does not pass.
6. Re-inspect after synchronization and select the first current pending block. Document order is
   the only implementation order.

## Start a Pending Requirement

For the selected block:

1. Derive a concise normalized `feature-name` from the requirements content and the exact directory
   `.codexspec/specs/<feature-id>-<feature-name>/`. Do not require or rewrite a particular Markdown
   heading to derive the name.
2. Send `_blueprint-helper apply --auto-dev-token <token>` an `update_status` request with the
   current hash and exactly:

```json
{"protocol_version":"1","operation":"update_status","feature_id":"<feature-id>","expected_blueprint_hash":"sha256:<hex>","payload":{"expected_status":"pending","new_status":"in_progress","feature_directory":".codexspec/specs/<feature-id>-<feature-name>/"}}
```

3. On conflict, re-inspect and restart selection. On rejected/invalid/transport failure, stop with
   evidence; do not create the directory first.
4. Create the recorded directory. Copy the block content after exactly the three blueprint-managed
   prefix lines directly to its `requirements.md`. This copied content includes the embedded Feature
   ID but excludes blueprint-only Development Status and Feature Directory fields. Perform both
   operations inside the returned dedicated worktree.

## Resume and Stage Resolution

For an in-progress block, inspect `requirements.md`, `spec.md`, `design.md`, `plan.md`, `tasks.md`,
their review reports, implementation, tests, and code-review evidence. Select the earliest missing,
stale, incomplete, or no-longer-passing stage. Do not repeat a previously passing stage unless
current upstream content or verification evidence invalidates it. If interruption occurred after
the status commit but before directory creation, create the already recorded directory (not a new
or renamed directory) and reconstruct its `requirements.md` from that same block before resolving
the earliest unfinished stage.

Invoke every SDD command with this explicit run-local statement in its invocation context:

```text
CODEXSPEC_AUTO_DEV_DELEGATION: return the stage result to auto-dev and skip the stage's global auto_next section.
```

Then execute in order as needed:

1. `/codexspec:generate-spec <feature-dir>`
2. `/codexspec:spec-to-design <feature-dir>`
3. `/codexspec:spec-to-plan <feature-dir>`
4. `/codexspec:plan-to-tasks <feature-dir>`
5. `/codexspec:implement-tasks <feature-dir>`

Auto-dev owns advancement. It must not read, write, toggle, or rely on `workflow.auto_next`.

## Autonomous Decisions, Repair, and Commits

- Trace uncertainty from task to plan, design, specification, and confirmed requirements. When no
  user-owned choice is present, apply an established software-engineering practice and continue.
- Never ask the user for a direction, option, or routine implementation detail during this command.
- Let every stage run its existing review, repair, retry, and no-progress rules. Repair verified
  findings autonomously. A stage stop guard ends this run; preserve the `in_progress` status,
  directory, artifacts, code, and exact evidence, release ownership, and do not start later work.
- Before each implementation commit, assert ownership and call `_auto-dev-helper commit-feature`
  with exact keys `token`, `feature_id`, `commit_type`, `description`, and explicit `paths`.
  The helper constructs `<type>(<feature-id>): <description>`, rejects the blueprint path, and
  preserves multiple commits in Git order. Do not squash and do not maintain a hash list.

## Complete and Continue

Only after all reused pass conditions, project checks, tests, final code review, and required repairs
pass, send `_blueprint-helper apply --auto-dev-token <token>` this exact status operation using a
fresh blueprint hash:

```json
{"protocol_version":"1","operation":"update_status","feature_id":"<feature-id>","expected_blueprint_hash":"sha256:<hex>","payload":{"expected_status":"in_progress","new_status":"completed"}}
```

On `applied`, re-inspect the complete blueprint and return to **Select Work**. Requirements appended during this run join the same run at their current document positions. Stop successfully only after a fresh inspection finds neither an in-progress block nor a pending block.

## Final Report

Report completed Feature IDs and directories, resumed work, synchronization warnings/merges,
verification evidence, controlled stops, and the final fresh-read result. Never translate stage
failure verdicts into new blueprint statuses.
