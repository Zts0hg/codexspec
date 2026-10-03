---
description: 分析 SDD 工件间的端到端可追溯性与一致性
argument-hint: "[功能目录]"
---

# Cross-Artifact Analyzer

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

`$ARGUMENTS`

## Operating Model

This command detects cross-artifact inconsistencies **and auto-remediates them**. It is not read-only.

- `requirements.md` is the single source of truth. analyze **never modifies `requirements.md`**. Every fix conforms the downstream artifacts (`spec.md`, `design.md`, `plan.md`, `tasks.md`) to `requirements.md`; the fix direction is uniquely determined by the authority hierarchy (requirements > spec > design > plan > tasks) and never requires inventing intent.
- Auto-apply deterministic, authority-directed fixes **by default** — both when invoked manually and when invoked inside the `auto_next` chain — with no confirmation prompt and no human-escalation path.

Resolve the feature by explicit path, then current branch. Ask the user if it is ambiguous; never select the latest feature silently.

## Inputs

Load:

- `requirements.md`
- `spec.md`
- `design.md`
- `plan.md`
- `tasks.md`
- Constitution

A legacy feature may have no `design.md`; when it is absent, analyze the chain without the design link and proceed.

Legacy compatibility: if `requirements.md` is missing, state that the analysis starts at `spec.md` and cannot validate fidelity to the original discussion. In legacy mode there is no source of truth to conform to, so do not auto-modify artifacts; report findings only.

## End-to-End Traceability

Build the chain:

```text
confirmed NEED/CON/DEC/OUT
  -> REQ/NFR Sources
  -> design Covers
  -> plan Covers (Covers: REQ; Design: <component>)
  -> task Covers + Plan reference
```

Detect:

- Confirmed requirements with no spec coverage
- Spec requirements with missing or invalid sources
- Spec requirements with no design coverage
- Design components with no plan coverage
- Plan deliverables with no task coverage
- Tasks with no upstream authority or implementation-support justification
- Semantic drift, scope expansion, contradictions, and use of superseded/open entries
- Dependency or ordering conflicts that prevent execution

## Remediation

Resolve findings along two dimensions. `requirements.md` is never edited.

- **Completeness** — every upstream authority (ultimately `requirements.md`) must be covered downstream. For an uncovered upstream item, auto-add the missing downstream coverage. A downstream entry that only adds derived or elaborated detail without upstream authority does **not** harm completeness and is preserved untouched — its mere existence is not a defect.
- **Consistency** — act **only on conflicts**: a downstream entry that contradicts `requirements.md`/upstream truth or another entry. Resolve a conflict by conforming the unauthorized or lower-authority side with the **minimal change** needed to remove it. When there is no conflict, take no action.
- **Determinism** — the fix direction is dictated by the authority hierarchy; never invent intent, and never rewrite `requirements.md`.
- **Conflict tie-break** — when two conflicting entries share no adjudicating upstream, trace both to their nearest common upstream authority and conform to it. If genuinely no common upstream exists, leave both entries unchanged and report the unresolved conflict; analyze still completes and does not gate or escalate.

Apply only deterministic, authority-directed remediations automatically. Keep optional Risk Advisories and Design Opportunities separate; never auto-apply those.

## Finding Rules

Use the same evidence requirements as the review commands:

- Evidence
- Location
- Mismatch
- Impact
- Remediation

Merge the same root cause. Separate optional Risk Advisories and Design Opportunities from verified defects.

## Output

Produce:

- Authority mode
- End-to-end coverage table
- Applied remediations: the exact downstream edits made to `spec.md`/`design.md`/`plan.md`/`tasks.md` and why, or "none"
- Verified defects by severity that were not auto-remediable (for example, a reported-only tie-break conflict)
- Unmapped or unauthorized items
- Risk Advisories
- Design Opportunities
- Coverage counts for each link in the chain

`requirements.md` is never among the changed files. It is valid to report zero findings and zero remediations.
