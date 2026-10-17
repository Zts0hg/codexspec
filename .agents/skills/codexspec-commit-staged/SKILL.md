---
name: codexspec:commit-staged
description: "仅根据暂存改动生成提交信息并执行已授权的提交；-p 只预览，不执行提交。"
---

## Constitution Compliance (MANDATORY)

**Before generating commit messages:**

1. **Check for Constitution File**: Look for `.codexspec/memory/constitution.md`
2. **If Constitution Exists**:
   - Load and read relevant principles (especially coding standards, commit conventions)
   - Ensure commit message style aligns with constitutional guidelines
   - Verify that the changes being committed don't violate any principles
3. **If No Constitution Exists**: Proceed with default Conventional Commits format

## Configuration Check

**IMPORTANT**: Before proceeding, check if the project configuration exists.

### Execution Steps

1. **Check Configuration File**
   - Check if `.codexspec/config.yml` exists
   - This is a simple file existence check, no parsing needed at this stage

2. **If Configuration Does NOT Exist**
   - Display a one-time prompt:

     ```
     💡 Project language is not configured. Run `$codexspec:config` to create a configuration file.
     ```

   - Use default values for current session:
     - `language.output`: "en"
     - `language.commit`: "en"
     - `language.templates`: "en"
   - Continue with command execution normally

3. **If Configuration Exists**
   - Proceed to `## Language Preference` section
   - Read configuration and apply language settings as before

4. **Session State** (Implicit)
   - The prompt is shown only once per conversation session
   - Claude's conversation context naturally maintains this state
   - No additional mechanism needed

## Language Preference

**IMPORTANT**: Before generating commit messages, read the project's language configuration from `.codexspec/config.yml`.

**Commit message language priority**:

1. If `language.commit` is set, use that language for the commit message description
2. Otherwise, use `language.output` as fallback
3. If neither is configured, default to English

**Note**:

- The commit type (feat, fix, docs, etc.) and scope should always remain in English
- Only the description part should use the configured language
- Technical terms (e.g., API, JWT, OAuth) may remain in English when appropriate

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
not success. Resolve and stage conflicts only in the returned worktree. Leave a pending
merge uncommitted. Run the project's required checks against the prepared files, then take a
`codexspec _commit-staged-helper snapshot` in that worktree with its original index (no inherited
GIT_INDEX_FILE). For a contentful merge, invoke `$codexspec:commit-staged -p` on that exact
snapshot and retain its complete message. Describe changes as integrated changes; do not attribute
all incoming code to conflict resolution. If the snapshot contains `default_message`, the merge
only connects history: keep its message unchanged by supplying `message: null`.

Call `codexspec _worktree-helper finish --feature <full-feature-name> --verification <json-file>`
(use `worktree-for-codexspec-maintenance` for maintenance preparation). The JSON contains the
verified `head`, staged `tree`, `checks` entries with `command` and integer `exit_code`, and,
for a pending merge, the complete `analysis` snapshot and `message`. The finish helper rechecks
and commits the same index. Never commit the pending merge directly or bypass a rejected snapshot.
If recovery finds the commit already created, verify its current HEAD/tree and submit head/tree/checks
without a new message. Never claim checks ran when they did not. If conflicts or checks cannot
be resolved, stop and retain the same identity; do not create a second feature to bypass preparation.
Fetch warnings indicate potentially stale remote information, not permission to bypass checks.

Initial fixed auto-dev/blueprint workspace creation follows the same pending handoff. If acquisition
or blueprint setup exits 3 with `merge_requires_resolution` or `merge_requires_verification`, use
its returned `workspace`, resolve/stage/check/analyze as above, and call
`codexspec _worktree-helper finish-initial --verification <json-file>`. Retry the original setup
only after `ready`. The helper excludes active auto-dev owners and retains interrupted preparation.

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

## Parameter Check and Input Identity

If `the text after the $codexspec:commit-staged skill mention` contains `-p`, analyze and return the message without committing.
Otherwise analyze and execute the authorized commit through the guarded helper.

By default the input is the invoking checkout's original staging area. Never
route analysis to another checkout or substitute an index to make a commit work.
A helper caller may explicitly supply its prepared `workspace`, `index_file`,
`head`, `tree`, and `required_scope`; this is a preview-only invocation. Use the
returned workspace and set `GIT_INDEX_FILE` to that exact prepared index for every
Git read in this invocation. Scope constrains formatting, not message intent.
Do not execute a helper-owned preparation here: return its message to its caller.

## Staging Boundary

The caller chooses and stages the intended changes before invoking this command.
This command must never run `git add`, `git reset`, `git checkout`, `git restore`,
`git stash`, or `git rm`, including after a hook failure. It must not select files,
repair staging, or include unstaged changes. Report unexpected or empty staging.

## Commit Runtime

Resolve one runtime for this invocation, without changing the input workspace:

- When loaded from a Claude plugin, use its bundled
  `${CLAUDE_PLUGIN_ROOT}/.claude/commands/codexspec/commit-staged-helper.py`.
- After project initialization (including one-time `uvx` initialization), use
  `<original workspace>/.codexspec/scripts/commit-staged-helper.py` when present.
- Otherwise, an installed `codexspec _commit-staged-helper` is the same protocol.

Run a bundled helper with an available Python 3.11+ interpreter, for example
`python3 -I -S "<absolute helper path>" snapshot` (Windows: `py -3.11`, or a
verified newer Python). Quote the helper path. Keep that same runtime for commit.
The standalone file uses only the Python standard library and Git; it requires
neither a persistent CodexSpec CLI nor an LLM client. The agent generates the
message; the runtime only snapshots, validates, and executes Git.

If no runtime is available, report the missing installation asset or Python/Git
prerequisite; do not install packages automatically or bypass validation.
Existing workspace-routing requirements still apply to execution. Preview never
requires creating or resolving another worktree. This runtime does not replace
the CLI used by blueprint, auto-dev, or worktree routing.

## Analysis

1. For the original index, invoke the selected runtime with `snapshot` and retain
   its exact JSON object (`workspace`, `index_file`, nullable `head`, `tree`, plus
   `merge_heads` and optional `default_message` during a merge).
   For a helper-owned preview, verify `git rev-parse HEAD` and `git write-tree`
   against the supplied `head` and `tree`, with its explicit index selected.
   For a pending merge whose snapshot contains `default_message`, its staged tree
   equals HEAD: skip semantic generation in steps 2–3 and retain that message unchanged. Preview
   returns that default text; execution sends `message: null` with the exact snapshot.
   Non-merge empty staging remains an error.
2. Run `git diff --staged --name-status` and `git diff --staged` against that same
   index. The staged diff is the only authoritative input for semantic claims.
   Do not infer intent from earlier conversation or describe unstaged changes.
   For a merge, these are changes integrated relative to the current HEAD. Do not
   imply that all incoming changes were authored as conflict resolutions.
   If the diff is insufficient, stop and report what cannot be established.
3. Generate a Conventional Commits subject, `type(scope): description`, respecting
   the project's conventions, required helper scope, and configured commit
   language. Type and scope remain in English. Use a concise subject and a body
   when needed to cover all material staged changes: relevant behavior, affected
   components, removals, compatibility changes, and tests actually present in
   the diff. Do not claim tests passed based on conversation or test-file presence.
   Include `BREAKING CHANGE:` when the staged change supports it. Never add AI
   attribution or `Co-Authored-By` lines.
4. Verify the complete snapshot again, including merge parents/default message when present. If it changed, discard the stale message
   and analyze again after the caller has prepared the intended content. Do not
   keep the old message merely because file names are unchanged.
5. In preview mode, return the full message only, retaining the validated input
   identity for the calling workflow. Do not create a commit or invoke distill.
6. In execute mode, invoke the selected runtime with `commit`, sending exactly
   this JSON on stdin in the same workspace:

```json
{"analysis":{"workspace":"<original workspace>","index_file":"<original index>","head":"<HEAD or null>","tree":"<analyzed tree>"},"message":"<full subject and optional body>"}
```

For merges, include every field from the exact snapshot in `analysis`; use null
for `message` only when `default_message` is present.

Use structured input or a UTF-8 temporary file; never interpolate the message into
shell code. The helper preserves hooks and checks the actual commit index before
creation. Report success only after its `committed` response.

## Failure and Retry

- Empty, unexpected, or insufficient staged input: report the condition; do not
  stage or guess a message.
- `stale_analysis`: return to caller preparation and analyze again. A prepared
  helper index must be refreshed by that helper, not repaired here.
- Hook-modified files: the caller may stage only the authorized fixes, then must
  invoke this command again to analyze the new staged content before retrying.
  This command never restages or retries with a message from different content.
- Other failures: report the exact error and preserve existing state. Never
  bypass hooks, switch indexes, or fall back to raw `git commit`.

## Automatic Distillation

Read `workflow.auto_distill` from `.codexspec/config.yml` (**default `true`** — enabled unless explicitly set to the literal `false`; absent or any non-`false` value means enabled).

When `workflow.auto_distill` is enabled (not the literal `false`) AND a commit was created successfully, invoke `$codexspec:distill` exactly once on this session's interaction, then end.

- distill is non-blocking and non-interactive: it never prompts and never alters the commit or its message; it early-exits when there is nothing reusable to capture.
- distill only writes records to `.codexspec/profile/`; it never touches tracked project files or the git state.
- Do not invoke distill when `auto_distill` is disabled or when no commit was created (for example, an ABORT above).
