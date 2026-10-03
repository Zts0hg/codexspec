---
name: codexspec:blueprint
description: "讨论并维护共享产品蓝图中的已确认需求"
---

# Blueprint Requirements Discovery

## Language Preference

Read `.codexspec/config.yml`. Two independent language controls apply (each falls back to
`language.output`, then English):

- **Interaction language** (`language.interaction`): language for all conversation with the user.
- **Document language** (`language.document`): language for requirements Markdown sent to the helper.

Converse in the interaction language and author requirement content in the document language. Use
clear, standard software-development terminology; do not invent abbreviations to summarize concepts.

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

`the text after the $codexspec:blueprint skill mention`

## Goal

Discuss and confirm one new requirement, or maintain one existing pending requirement, in the single
shared `.codexspec/blueprint.md`. This command never creates a feature directory, changes a
development status, or starts SDD development.

## Shared Workspace

1. Run `codexspec _blueprint-helper inspect --ensure` from the invoking repository.
2. Use only the returned worktree and blueprint. Never read or edit a blueprint copy in the caller
   checkout, and never write `.codexspec/blueprint.md` directly.
3. Retain the returned `blueprint_hash` for one helper mutation request.
4. Read `.codexspec/memory/constitution.md`, all constraints and relevant records under
   `.codexspec/profile/`, relevant implemented features under `.codexspec/specs/`, and every current
   blueprint block before discussing or changing a requirement.

## Allowed Work

- Append one newly confirmed requirement as the last pending block.
- Replace the complete agent-authored Markdown of one pending block while preserving its Feature ID.
- Delete one pending block after explicit confirmation.
- Move one pending block to the first/last pending position or before/after another pending block.
- View `in_progress` and `completed` blocks as context. Never modify, delete, or move them.

Blueprint order is implementation order. Resolve prerequisites and requested reordering here; do not
add priorities, dependency metadata, or scheduling behavior.

## Requirements Discussion

For an append or replacement, follow the same discipline as `specify`:

- Ask one material question at a time.
- Explore goals, workflows, constraints, error behavior, compatibility, scope, and material trade-offs.
- Resolve every user-owned direction, option, and product detail before confirmation.
- Distinguish user statements from agent inferences. Do not mark an inference confirmed.
- Maintain `NEED-*`, `CON-*`, `DEC-*`, `OUT-*`, and `OPEN-*` entries in specify's requirements
  organization. No blocking or user-owned `OPEN-*` item may remain when appending/replacing.
- Present a concise final stage summary and require explicit user confirmation. Silence is not
  confirmation.
- Preserve superseded decisions when they are useful history and append a confirmation-log entry.

The resulting `requirements_markdown` must be a complete specify-style requirements document except
that it omits all helper-managed `Feature ID`, `Development Status`, and `Feature Directory` fields.
It must not contain a standalone `---` line. The helper treats the complete Markdown after the three
managed lines as the requirements body; it must not depend on a particular heading to find that body.

Delete and move operations do not require a new requirements discussion, but they require an
unambiguous permanent Feature ID and explicit confirmation of the exact deletion or destination.

## Exact Helper Requests

Send exactly one JSON object to `codexspec _blueprint-helper apply` on stdin. Use protocol version
`1`, the inspected hash, and no unlisted keys.

Append omits top-level `feature_id`:

```json
{"protocol_version":"1","operation":"append_requirement","expected_blueprint_hash":"sha256:<hex>","payload":{"feature_name":"release-notes","requirements_markdown":"<confirmed Markdown without managed fields>"}}
```

Replace includes the target Feature ID and the same exact payload fields:

```json
{"protocol_version":"1","operation":"replace_pending_requirement","feature_id":"2026-0830-1030ab","expected_blueprint_hash":"sha256:<hex>","payload":{"feature_name":"release-notes","requirements_markdown":"<confirmed Markdown without managed fields>"}}
```

Delete uses an empty payload:

```json
{"protocol_version":"1","operation":"delete_pending_requirement","feature_id":"2026-0830-1030ab","expected_blueprint_hash":"sha256:<hex>","payload":{}}
```

Move uses exactly one of these payload forms:

```json
{"position":"first_pending"}
{"position":"last_pending"}
{"position":"before","reference_feature_id":"2026-0830-1045cd"}
{"position":"after","reference_feature_id":"2026-0830-1045cd"}
```

Use these payloads only with the `move_pending_requirement` operation and the target's top-level
`feature_id`.

`blueprint` must never send `update_status`.

## Result Handling

- `applied`: report the operation, affected/generated Feature ID, and new blueprint hash.
- `conflict`: inspect again, re-evaluate the already confirmed intent against current blocks, and
  construct one fresh request. Do not reuse the stale hash or overwrite concurrent work.
- `rejected`: report the helper's concrete blueprint rule and leave the document unchanged.
- `invalid_request`: correct the request shape from the contract; never weaken validation or edit the
  file directly.
- Non-zero transport/internal failure: report stderr, inspect current state before any retry, and do
  not claim that a mutation applied.
- `merge_in_progress` transport failure: another short Git operation owns the dedicated worktree.
  Wait without holding a lock, inspect again, and retry the same confirmed intent with the current
  hash until the merge finishes. If the merge changed the blueprint, re-evaluate the intent against
  the new blocks exactly as for `conflict`; do not ask the user to reconfirm an unchanged intent.

## Completion

Report the applied operation, permanent Feature ID, current document position, development status,
and dedicated blueprint path. End without invoking `generate-spec`, `auto-dev`, or any implementation
stage.
