---
description: 自主开发共享蓝图中的每个待定需求
argument-hint: ""
---

# Continuous Blueprint Development

## Language Preference

Read `.codexspec/config.yml`. Converse in `language.interaction` and author SDD artifacts in
`language.document`, each falling back to `language.output`, then English.

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
