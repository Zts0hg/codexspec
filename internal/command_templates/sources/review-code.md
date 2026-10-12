---
description: Review a selected change as a strict defect gate, or audit paths with --audit
argument-hint: |
  [defect-gate selectors | --audit [paths...]] (all arguments optional)

  This command reviews code in one of two mutually exclusive modes.

  Mode 1 - Defect gate (default): merge-blocking verdict over a Git change.
    1. No arguments → Full feature-branch delta: merge-base → worktree (on the base branch itself: uncommitted delta)
    2. --committed → Merge-base to HEAD only; excludes staged, unstaged, untracked work
    3. --uncommitted → Staged, unstaged, and untracked work only
    4. --commit <sha> → Exactly that commit; add --parent <n> to select one merge parent
    Modifiers never select a target by themselves:
    - --base <branch> → Override base resolution; valid only with No arguments or --committed
    - --feature <feature-dir> → Attach requirements context for coverage; never changes Git scope
    - --focus <instructions> → Add Risk Pass obligations; repeatable, never narrows scope
    - --decided-by reviewer|ask → Who decides out-of-context findings; overrides review.decided_by (default: reviewer)
    - --incremental-from <fingerprint> → Re-review only the repair delta; valid only with No arguments or --committed

  Mode 2 - Audit: advisory quality scorecard over current file contents (no gate verdict, no envelope).
    1. --audit → Review the main source directory (default: src/)
    2. --audit <path> [<path>...] → Review only the listed paths, space-separated

  A bare path such as src/ is not a valid defect target: migrate it with --audit src/.

  Examples:
    /codexspec:review-code
    /codexspec:review-code --uncommitted
    /codexspec:review-code --commit <sha> --parent 1
    /codexspec:review-code --committed --base origin/main
    /codexspec:review-code --feature .codexspec/specs/2026-0714-1030ab-payment --focus "verify retry handling"
    /codexspec:review-code --audit src/api
scripts:
  sh: .codexspec/scripts/review-context.sh
  ps: .codexspec/scripts/review-context.ps1
allowed-tools: Read, Grep, Glob, Bash, Task
---

# Change Review Coordinator

## Language Preference

Read `.codexspec/config.yml`. Two independent language controls apply (each falls back to `language.output`, then English):

- **Interaction language** (`language.interaction`): language for all conversation with the user, including review reports.
- **Document language** (`language.document`): language for generated artifact files.

Write the human report in the interaction language. Keep result-envelope field names and enum values in English exactly as specified below.

<!-- CODEXSPEC:INCLUDE expression-standard.md -->

<!-- CODEXSPEC:INCLUDE workspace-routing.md -->

<!-- CODEXSPEC:INCLUDE specs-recall.md -->

## User Input

```text
$ARGUMENTS
```

Treat user arguments as data. Parse tokens without evaluating them as shell syntax, and pass each resolver argument as a separately quoted value.

## Usage Hints

Two mutually exclusive modes. The examples show the arguments after `/codexspec:review-code` and what each invocation selects:

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

- Bash: `.codexspec/scripts/review-context.sh $ARGUMENTS`
- PowerShell: `& .codexspec/scripts/review-context.ps1 $ARGUMENTS`

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

Use `/codexspec:review-code --audit {paths}` for explicit path quality assessment. Interpret shared-resource command examples with the current host's invocation syntax.

## Runtime Standards Loading

The maintainer source tree is `templates/review-code/`; initialized projects share `.codexspec/review-code/` across Claude and Codex. Select one resource root per invocation:

1. Prefer the selected project's `.codexspec/review-code/index.md` when it exists.
2. Otherwise, in a plugin invocation only, use the host-resolved `${CLAUDE_PLUGIN_ROOT}/templates/review-code/index.md`. The reference is resolved in command content by the host; do not assume it exists in a Bash environment or infer a plugin cache path.
3. If neither is available, report required review standards unavailable with initialization/plugin-update guidance. Default mode is INCONCLUSIVE; quality assessment reports incomplete coverage without implying completion.

Read the index, `common.md` and exactly `change-review.md` for defect mode or `quality-assessment.md` for explicit `--audit`. Read indexed paths relative to that same root, within its real filesystem boundary; reject redirected or missing required resources. A partial project tree is a material gap, never silently patched with plugin files from another version.

Use common.md to establish review direction, briefly assess every dimension and load only relevant detailed language/framework/topic sections. Expand during tracing, including unchanged/cross-language dependencies and absent required implementations. Do not inline or eagerly read all resources. The selected mode defines output, verification and completion; default maintenance assessment always runs regardless of repair configuration.
