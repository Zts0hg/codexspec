---
description: 审查 design.md 的需求覆盖与技术可行性，判断是否可制定实现计划。
argument-hint: "[design.md 或 功能目录]"
handoffs:
  - agent: claude
    step: Review design against confirmed requirements, spec, and repository facts
---

# Design Reviewer

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
not success. Resolve and stage conflicts only in the returned worktree. Leave a pending
merge uncommitted. Run the project's required checks against the prepared files, then take a
`codexspec _commit-staged-helper snapshot` in that worktree with its original index (no inherited
GIT_INDEX_FILE). For a contentful merge, invoke `/codexspec:commit-staged -p` on that exact
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

`$ARGUMENTS`

## Review Authority

Resolve by explicit path, then current branch; never silently select the latest feature.

Read `requirements.md`, `spec.md`, `design.md`, the constitution, and only the repository files necessary to verify design claims.

If `requirements.md` is absent, use legacy spec-only mode and disclose that original-discussion fidelity cannot be verified.

Authority order:

1. Confirmed requirements
2. Specification
3. Constitution and verified repository facts
4. Design-level technical decisions
5. Applicable best practices

## Review Passes

### 1. Fidelity and Coverage

- Verify every `REQ`/`NFR` has design coverage.
- Verify each component, interface, data change, and design decision has `Covers:`.
- Detect omitted behavior, semantic changes, scope expansion, and design decisions that override confirmed trade-offs.
- Verify design-level assumptions remain labeled and do not become product requirements.

### 2. Feasibility and Internal Quality

Report evidence-backed defects such as:

- Referencing nonexistent modules, APIs, paths, or capabilities
- Contradictory component responsibilities or interfaces
- Missing design decisions that genuinely block planning
- Invalid data, compatibility, security, or interface assumptions
- Complexity that creates concrete risk without serving a confirmed requirement

Data models, API contracts, sequence diagrams, cross-cutting design sections, and explicit interfaces are required only when the feature or repository context makes them necessary.

### 3. Advisories

Put optional best practices in **Risk Advisories** or **Design Opportunities**. Include applicability, actual risk or benefit, and relationship to the user goal.

Advisories do not affect status, do not affect the score, and must not be auto-fixed.

## Finding Validation

Every defect must include:

- **Evidence**
- **Location**
- **Mismatch**
- **Impact**
- **Remediation**

Merge findings with the same root cause. Do not deduct the same root cause under alignment, architecture, and decision-record planning separately.

Reject findings that are only stylistic preference, generic best practice without applicability, or a demand to replace a confirmed trade-off.

Zero verified defects is a valid result.

## Severity, Status, and Compatibility Score

- Critical: blocks a correct or feasible implementation
- Warning: likely incorrect implementation or major rework
- Minor: localized verified defect
- Advisory: optional and non-scoring

Status:

- Critical present: `BLOCKED`
- Warning present without Critical: `NEEDS_REVISION`
- Minor only: `PASS_WITH_WARNINGS`
- No defects: `PASS`

Compatibility Score:

- No defects: `100`
- Minor only: `max(80, 100 - 3 × Minor)`
- Warning present: `max(50, 79 - 8 × (Warning - 1) - 3 × Minor)`
- Critical present: `max(0, 49 - 15 × (Critical - 1) - 8 × Warning - 3 × Minor)`

Advisory does not affect the score. There are no fixed deductions for omitted template sections.

## Report

Save `<feature-dir>/review-design.md`:

```markdown
# Design Review Report

## Summary
- **Overall Status**: PASS / PASS_WITH_WARNINGS / NEEDS_REVISION / BLOCKED
- **Compatibility Score**: X/100
- **Authority Mode**: Requirements-first / Legacy spec-only
- **Readiness**: Ready for Planning / Revision Required

## Requirement Coverage
| Requirement | Design Reference | Result |

## Verified Defects
### Critical
### Warnings
### Minor

## Risk Advisories

## Design Opportunities

## Score Derivation
```
