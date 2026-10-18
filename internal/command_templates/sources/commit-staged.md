---
description: Generate a message strictly from staged changes and execute the authorized commit; use -p to preview without committing.
argument-hint: "[-p] Use -p to only preview the message without committing"
allowed-tools: Bash(git diff:*), Bash(git status:*), Bash(git rev-parse:*), Bash(git write-tree:*), Bash(codexspec _commit-staged-helper:*), Bash(python3:*), Bash(python:*), Bash(py:*)
forbidden-tools: Bash(git add:*), Bash(git reset:*), Bash(git checkout:*), Bash(git restore:*), Bash(git stash:*), Bash(git rm:*)
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
     💡 Project language is not configured. Run `/codexspec:config` to create a configuration file.
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

<!-- CODEXSPEC:INCLUDE expression-standard.md -->

<!-- CODEXSPEC:INCLUDE workspace-routing.md -->

## Parameter Check and Input Identity

If `$ARGUMENTS` contains `-p`, analyze and return the message without committing.
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

When `workflow.auto_distill` is enabled (not the literal `false`) AND a commit was created successfully, invoke `/codexspec:distill` exactly once on this session's interaction, then end.

- distill is non-blocking and non-interactive: it never prompts and never alters the commit or its message; it early-exits when there is nothing reusable to capture.
- distill only writes records to `.codexspec/profile/`; it never touches tracked project files or the git state.
- Do not invoke distill when `auto_distill` is disabled or when no commit was created (for example, an ABORT above).
