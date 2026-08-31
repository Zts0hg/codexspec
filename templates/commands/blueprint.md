---
description: Discuss and maintain confirmed requirements in the shared product blueprint
argument-hint: "Describe a new requirement, or identify a pending requirement to replace, delete, or move"
---

# Blueprint Requirements Discovery

## Language Preference

Read `.codexspec/config.yml`. Two independent language controls apply (each falls back to
`language.output`, then English):

- **Interaction language** (`language.interaction`): language for all conversation with the user.
- **Document language** (`language.document`): language for requirements Markdown sent to the helper.

Converse in the interaction language and author requirement content in the document language. Use
clear, standard software-development terminology; do not invent abbreviations to summarize concepts.

## User Input

`$ARGUMENTS`

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
