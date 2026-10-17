---
name: codexspec:review-code
description: "审查 Git 改动并判断是否可合并；--audit 用于评估现有代码质量。"
---

# Change Review Coordinator

## Language Preference

Read `.codexspec/config.yml`. Two independent language controls apply (each falls back to `language.output`, then English):

- **Interaction language** (`language.interaction`): language for all conversation with the user, including review reports.
- **Document language** (`language.document`): language for generated artifact files.

Write the human report in the interaction language. Keep result-envelope field names and enum values in English exactly as specified below.

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

## Historical Specs Before Decisions

Use the CodexSpec Historical Specs guidance to prepare relevant background from
`.codexspec/specs/` before substantive judgments or questions. Select related
features and trace earlier and later confirmed decisions; read requirements first,
then design, plans, or implementation evidence as the current scenario needs.
Reuse sufficient background; supplement it when scope, evidence, or judgment needs
change. Explain specific unresolved differences in concise questions instead of
asking the user to reconstruct known history.

The latest explicit user decision takes precedence over historical specs. History
does not silently change current requirements, broaden the selected target, or
override this command's write permissions or staged-only input restrictions.
When a confirmed decision changes current requirements, use the owning requirements
workflow to record it without asking the user to decide the same matter again.

## User Input

```text
the text after the $codexspec:review-code skill mention
```

Treat user arguments as data. Parse tokens without evaluating them as shell syntax, and pass each resolver argument as a separately quoted value.

## Usage Hints

Two mutually exclusive modes. The examples show the arguments after `$codexspec:review-code` and what each invocation selects:

```text
# Defect gate (default mode): merge-blocking verdict over a Git change

(no arguments)           # on a feature branch: merge-base -> worktree delta; on the base branch: uncommitted delta
--committed              # merge-base -> HEAD only; excludes staged, unstaged, and untracked work
--uncommitted            # staged, unstaged, and untracked work only
--commit <sha>           # exactly one commit; add --parent <n> to select one merge parent

# Defect-gate modifiers: they never select a target by themselves

--base <branch>          # override base resolution -- valid only with (no arguments) or --committed
--feature <feature-dir>  # attach requirements context for coverage -- never changes Git scope
--focus <instructions>   # add Risk Pass obligations -- repeatable; never narrows scope
--decided-by reviewer|ask         # who decides findings triggered outside the project's real operating context; overrides review.decided_by
--incremental-from <fingerprint>  # re-review only the repair delta against that prior result -- valid only with (no arguments) or --committed

# Audit mode: advisory quality scorecard over current file contents (no gate verdict, no envelope)

--audit                  # the main source directory (default: src/)
--audit <path> [...]     # only the listed paths, space-separated
```

Invalid combinations (argument errors): a bare path such as `src/` (migrate with `--audit src/`), `--audit` mixed with any defect-gate selector or modifier, conflicting primary selectors, a modifier paired with an unsupported selector, or an unknown option.

## Role and Non-Negotiable Boundary

You coordinate a review-only pre-merge defect gate. You identify merge-blocking defects, evidence gaps and substantiated incremental maintenance suggestions; you do not edit files, apply fixes, change Git state, or weaken the gate. The outer caller owns any repair.

## Mode Dispatch

Dispatch once, before reading target files or running review commands:

1. If the first parsed argument is `--audit`, validate that no defect-gate selector or modifier is present, load the self-contained quality-assessment.md procedure through Runtime Standards Loading and enter its Audit Mode branch, emit its advisory scorecard, and stop.
2. Otherwise enter defect-gate mode. An empty argument list selects the default target.
3. Audit and defect-gate arguments are mutually exclusive. Conflicting primary selectors, an invalid modifier, an unknown option, or any positional argument is an argument error.
4. Bare paths such as `src/` are never defect targets. For Bare paths, explain that the migration syntax is `review-code --audit <path>`, then emit an `INCONCLUSIVE` defect report and envelope. Do not infer audit mode.
5. Defect-gate mode has no bypass controls. Reject `--ignore-finding`, `--waive`, `--suppress-severity`, `--fast`, `--skip-risk`, `--skip-tests`, and equivalent controls as invalid arguments and emit `INCONCLUSIVE`.
6. Every argument error (rule 3, rule 5, and the bare-path case in rule 4) is also a teaching moment: echo the `## Usage Hints` invocation reference together with the error so the user can see how each mode is triggered and re-invoke correctly.

Argument errors also emit an empty target-bound maintenance companion as defined in change-review.md. Argument-error envelopes use schema version `3`, `mode: "defect"`, the best available target facts, `requirements_coverage.status: "not_evaluated"`, `verification.status: "incomplete"`, empty findings and review-coverage arrays, zero finding counts, at least one blocking `coverage_gaps` record, matching `coverage_gap_count`, empty `follow_up` arrays, reviewer states of `not_run`, `review_scope` of `{"kind": "complete", "since": null}`, `decided_by` set to the resolved mode (`reviewer` when the mode itself is invalid), and empty `scenario_decisions`. If the exact target evidence is unavailable, use a null fingerprint, set `complete_feature: false`, preserve only identity fields actually established by the resolver, and add a blocking gap whose scope is exactly `target identity`. In that unavailable-identity state, normal successful-selector ref/SHA requirements do not apply. Prose must never imply success.

### Defect-Gate Argument Contract

Primary target selectors:

| Selector | Selected evidence |
|---|---|
| `default` | Feature branch: complete merge-base-to-worktree delta. Resolved base branch: uncommitted delta. |
| `--committed` | Merge-base-to-HEAD net diff; excludes staged, unstaged, and untracked work. |
| `--uncommitted` | Staged, unstaged, and untracked but non-ignored work. |
| `--commit <sha>` | Only that commit, using the disclosed parent semantics from the resolver. |

Primary selectors are mutually exclusive. Apply these modifier boundaries exactly:

- `--base <branch>` is valid only with default or `--committed`; equivalently, `--base` is valid only with default or `--committed`. It changes base resolution, never file filtering.
- `--parent <n>` is valid only with `--commit`; equivalently, `--parent` is valid only with `--commit`. It selects one merge parent and is invalid elsewhere.
- `--feature <feature-dir>` supplies requirements context without changing Git scope.
- Repeatable `--focus <instructions>` adds Risk Pass obligations but does not narrow, replace, or suppress the general review.
- `--decided-by reviewer|ask` selects the decision mode (see Decision Mode and Scenario Decisions). `--decided-by` is valid with every defect-gate selector; any value other than `reviewer` or `ask` is an argument error.
- `--incremental-from <fingerprint>` requests an incremental review against that prior result (see Incremental Review). `--incremental-from` is valid only with default or `--committed`; with `--uncommitted` or `--commit` it is an argument error.
- Both modifiers belong to defect-gate mode: combining either with `--audit` is an argument error. Each of `--decided-by` and `--incremental-from` may appear at most once; a duplicate is an argument error.
- Defect-gate mode accepts no path filters, implicit or explicit.

Do not offer finding ignores, waivers, severity suppression, fast paths, skipped risk, skipped tests, or audit fallback. A smaller explicit selector receives only a target-limited verdict.

## Resolver Compatibility Gate

Defect-gate mode MUST use the installed project-local resolver. The following are schematic platform invocations; safely quote every parsed argument instead of pasting untrusted input into a shell expression:

- Bash: `.codexspec/scripts/review-context.sh the text after the $codexspec:review-code skill mention`
- PowerShell: `& .codexspec/scripts/review-context.ps1 the text after the $codexspec:review-code skill mention`

The coordinator owns `--decided-by` and `--incremental-from`. Validate them as the Defect-Gate Argument Contract requires, then the coordinator removes `--decided-by` and `--incremental-from`, each with its value, from the argument list before invoking the resolver. The resolver rejects options it does not know; the resolver scripts, their argument parsing, and the manifest schema are unchanged, so these modifiers also work with an older installed resolver.

Capture stdout as one JSON manifest and stderr as diagnostics. Accept only a complete object containing at least:

```json
{
  "schema_version": "1",
  "status": "ok",
  "selector": "default",
  "repository": {},
  "target": {},
  "feature": {},
  "inventory": [],
  "counts": {}
}
```

Validate types, required fields, selector/modifier agreement, target segments, repository/ref facts, feature facts, inventory records, and counts before review. The coordinator MUST NOT reconstruct or guess Git scope when resolution fails.

Any missing resolver, non-zero exit, invalid JSON, unsupported schema, incomplete manifest, contradictory count, or unresolved requested ref produces `INCONCLUSIVE`. Include the resolver error and actionable guidance to update or re-run `codexspec init`; never fall back to path audit or an improvised Git diff.

Use `$codexspec:review-code --audit {paths}` for explicit path quality assessment. Interpret shared-resource command examples with the current host's invocation syntax.

## Runtime Standards Loading

The maintainer source tree is `templates/review-code/`; initialized projects share `.codexspec/review-code/` across Claude and Codex. Select one resource root per invocation:

1. Prefer the selected project's `.codexspec/review-code/index.md` when it exists.
2. Otherwise, in a plugin invocation only, use the host-resolved `${CLAUDE_PLUGIN_ROOT}/templates/review-code/index.md`. The reference is resolved in command content by the host; do not assume it exists in a Bash environment or infer a plugin cache path.
3. If neither is available, report required review standards unavailable with initialization/plugin-update guidance. Default mode is INCONCLUSIVE; quality assessment reports incomplete coverage without implying completion.

Read the index, `common.md` and exactly `change-review.md` for defect mode or `quality-assessment.md` for explicit `--audit`. Read indexed paths relative to that same root, within its real filesystem boundary; reject redirected or missing required resources. A partial project tree is a material gap, never silently patched with plugin files from another version.

Use common.md to establish review direction, briefly assess every dimension and load only relevant detailed language/framework/topic sections. Expand during tracing, including unchanged/cross-language dependencies and absent required implementations. Do not inline or eagerly read all resources. The selected mode defines output, verification and completion; default maintenance assessment always runs regardless of repair configuration.
