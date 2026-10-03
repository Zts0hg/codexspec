---
description: 把已定稿（vetted）的项目知识整理成可复用的命令/技能，经人工评审的 PR 贡献回上游
argument-hint: "[要演化的内容或 profile 领域]"
---

# Evolve

## Language Preference

Read `.codexspec/config.yml`. Two independent language controls apply (each falls back to `language.output`, then English):

- **Interaction language** (`language.interaction`): language for all conversation with the user — questions, explanations, status messages, and `codexspec` CLI terminal output.
- **Document language** (`language.document`): language for generated artifact files.

Converse in the interaction language. **The compiled command/skill draft is a distributed template and MUST be authored in English** (project i18n convention), regardless of `language.document`. PR title/body follow `language.commit`.

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

`evolve` turns **vetted** sediment in `.codexspec/profile/` into a reusable capability and contributes it back to CodexSpec through a **human-reviewed PR**. It **never merges unattended** and **never** edits install artifacts.

## Selecting what to promote

Promote only records that are **both**:

1. `status: vetted` (never `candidate` or `conflict`), and
2. **general enough for the toolkit** — the generality extension of distill's boundary test: *"Is this useful to every CodexSpec user, or only to this project?"*

Project-specific knowledge **stays** in the profile. Only generally-useful capability is promoted upstream. When nothing qualifies, stop and report — do not force a promotion.

This selection spans **all six** profile categories. `strategies/` (metacognitive `trigger → action` rules) and `runbooks/` (ordered multi-step procedures) are often the **most** promotable material — a vetted, general strategy or runbook compiles cleanly into a reusable skill/command — but they clear the **same** `vetted` gate as every other category; the gate is unchanged.

## Compiling the draft

Compile the selected sediment into a SKILL.md / command-template draft that conforms to both:

- **Anthropic Agent Skills** (SKILL.md + progressive disclosure), and
- **existing CodexSpec command-template conventions** (YAML frontmatter + sections + `## Language Preference`, English).

Apply these compile rules:

- **Priority order** — core needs first, **negative constraints immediately after (highest weight)**, then the rest.
- **Logic-clean** — `replace`/`remove` any superseded rule first; the output MUST carry **no** contradictory rules.
- **Imperative wording** — use **必须 / 始终 / 严禁 / 仅允许** in place of 可以考虑 / 尽量 / 最好不要 / 或许. Match the project's explicit **Prefer / Avoid** rule style; do not use decorative markers.

## Where output goes (self-bootstrap)

Write **only** under `templates/` — a new `templates/commands/*.md` or a standalone skill package. **NEVER** edit `.claude/commands/codexspec/`: it is a regenerated install artifact, and any edit there is silently overwritten on the next reinstall and never reaches users. Changes reach users via `publish` → `init`.

## Contribution mechanics

**Before any `git push` or PR creation, present the compiled draft file(s) and the value statement to the user and obtain explicit approval. Proceed only on approval; NEVER push or open a PR unattended.** (Writing a local draft under `templates/` is git-reversible; the outward action is what is gated.)

On approval, open a PR for human review. **Auto-detect** the git path — this is a mechanics difference only, never a permission tier:

- Upstream **write access** → push a branch in-repo and open the PR.
- **No write access** → fork, push to the fork, open a cross-repo PR.

Both take the **identical** review path.

## Value gate and PR summary

Produce a one-sentence **value statement** as the PR summary:

> Resolves `<pain>`, by `<added/revised constraint>`, achieving `<quality/efficiency gain>`.

If no crisp value statement can be written, **open NO PR** — the batch is not worth promoting (this is the lightweight substitute for a metric/eval gate).

For review, keep each promoted `claim` paired with its `evidence` so a reviewer can check **claim ⇐ evidence**. A promoted change that later proves worse MUST be rolled back via `remove`/`replace` (git-traceable), not a manual file edit.

## Output

Report in the interaction language: what was selected, the draft file(s) written under `templates/`, and the PR (branch or fork) with its value statement — or **"nothing promoted"** with the reason (value gate / nothing vetted / nothing general enough).
