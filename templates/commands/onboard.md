---
description: Cold-start the project profile by scanning an existing codebase for conventions and constraints
argument-hint: "[path]"
allowed-tools: Read, Grep, Glob, Bash(git:*), Bash(ls/cat/find:*), Edit, Write
---

# Codebase Onboarding

## Language Preference

Read `.codexspec/config.yml`. Two independent language controls apply (each falls back to `language.output`, then English):

- **Interaction language** (`language.interaction`): language for all conversation with the user — questions, explanations, status messages, and `codexspec` CLI terminal output.
- **Document language** (`language.document`): language for generated artifact files (the profile records).

Converse in the interaction language and author artifacts in the document language. Apply the project's translation standard to both: translate by meaning (not word-for-word), keep English for terms with no good native equivalent, and write as if originally in that language. **Exception**: `evidence.facts` records a verbatim code observation (path + snippet) and MUST NOT be translated.

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

## Role and Operating Model

`onboard` is the **cold-start / bulk counterpart to `distill`**. Where `distill` writes the project profile incrementally from interaction, `onboard` scans an **existing codebase** once and batch-writes the reusable knowledge that is **implicit in the code and not already recorded accessibly** into the shared store `.codexspec/profile/`. It exists to bootstrap a brownfield project's profile so accumulated project knowledge is grounded immediately, instead of only after enough work has flowed through `distill`.

`onboard` is **read-only on the codebase** and **write-only to `.codexspec/profile/`**: it never modifies source, tests, git state, or the constitution. It is a **standalone, user-invoked command** — not an SDD pipeline stage: it has **no auto-next successor** and **no automatic hook**, and it leaves no persistent document beyond the profile records (no map, no walkthrough — those, if ever wanted, belong to a separate `explain`).

## Prerequisite & Scaffold

Before scanning:

- If `.codexspec/` is **absent**, the project is not codexspec-initialized. **Stop** and direct the user to run `codexspec init`. Do not scaffold a whole project.
- If `.codexspec/` is present but the profile store is missing, **ensure the canonical scaffold** — the six category directories `.codexspec/profile/{constraints,conventions,pitfalls,decisions,strategies,runbooks}/` (matching what `codexspec init` produces) — before writing.
- git is **not required**. onboard runs on a plain directory.

## Codebase Scan

Scan strategy is **high-signal-first over the whole repository in a single pass**:

- Respect `.gitignore`. When there is **no git / no `.gitignore`**, fall back to sensible defaults that skip vendored, build, and dependency directories (e.g. `node_modules`, `dist`, `build`, `.venv`, `target`), and say so in the summary.
- **Deep-read high-value sources**: directory structure; build / dependency / lint / formatter / type-checker config; entry points; existing docs (README, CONTRIBUTING, ADRs); test layout; and the frequently-imported core modules. **Shallow-sample** the bulk of business code rather than reading every file.
- **Stream findings to the store as you go** — write each convention as soon as it is confirmed — so the scan is **interruptible and resumable**. Do **not** block until the whole scan finishes before writing or interacting; a run interrupted mid-scan keeps what it already wrote and can be re-run to continue.
- An optional `[path]` argument (from `$ARGUMENTS`) **narrows** the scan to a single subdirectory or module.
- Never claim full coverage when you sampled — the summary distinguishes deep-read from sampled areas.

## What onboard Extracts — and What It Must NOT

Extraction uses your **flexible judgment over what the code actually shows** — not a fixed checklist of filenames or markers. onboard actively extracts **only two** of the six profile categories:

- **`conventions`** (the primary yield) — the code's observable regularities: directory/module structure, naming schemes, import style, the tech stack and toolchain (read from manifests), lint/format/type configuration, test framework and layout, and patterns repeated across the codebase. **Observable architecture / tech-stack facts** are captured here as fact-plus-steering, not as ADR-style decisions.
- **`constraints`** (narrow, high-risk) — **only** config-level **explicit hard prohibitions**: lint/type rules set to *error* that ban imports or APIs, `do not edit` / generated-file / managed-block markers, and CODEOWNERS / protected-path conventions. Every constraint candidate carries a **precise evidence anchor** (`file:line` or a config snippet). **Absent an explicit prohibition signal, propose no constraint** — silence, never a guess.

onboard **never** extracts `decisions`, `pitfalls`, `strategies`, or `runbooks`. A documented decision or pitfall is already readable in the repo (redundant to copy); an undocumented one is unreliable to infer from a cold scan (pitfalls are experiential; decision rationale would be fabricated). `strategies` (metacognitive trigger→action rules) and `runbooks` (lived multi-step procedures) are likewise experiential — a cold scan cannot reliably infer either. All four remain `distill`'s channels, where the rationale and lived experience are available.

## Record Format

onboard **reuses `distill`'s profile store and record format verbatim** — one record per file under a category directory (`conventions/<id>-<slug>.md`, `constraints/<id>-<slug>.md`; bare `<id>.md` when no meaningful slug applies), ids namespaced by the source-feature id, and `claim` physically separated from `evidence`. See `distill.md` for the canonical format. onboard writes with these **deltas**:

- `provenance` marks the **onboard scan** as the source (distinct from `distill`), with `derivation: inferred` — always, because the knowledge is inferred from code, never quoted from the user.
- An onboard record's `status` is always **`candidate`** at write time — onboard **never** writes `vetted` itself. Its `inferred` origin is **not** a permanent barrier: such a record can later be promoted to `vetted` via `/distill review` once it is outcome-verified and the user approves it (the `evolve` gate remains `vetted`). See the `status` rule in `distill.md`.
- `evidence.facts` holds the **concrete code observation** — the file path plus the relevant snippet or config anchor — instead of a user quote.

## Integration with the Existing Profile

Before writing, **read the existing profile** and integrate:

- **De-duplicate** — skip anything already covered by an existing record (by judgment, not an algorithm).
- **Adjudicate conflicts** per `distill`'s order (recency → specificity → scenario-decoupling → defer); if genuinely unresolvable, write the record `status: conflict/needs-adjudication` and surface it — never block, never guess.
- **Never clobber.** onboard MUST NOT overwrite or delete any existing `vetted`, hand-authored, or `distill`-written record. It only **adds** new files (namespaced ids merge with zero conflict) or edits **its own** candidate file. This makes re-running onboard (whole repo, or a narrowed `[path]`) safe and **idempotent** — it augments without destroying.

## Safety Gate — quick review for high-risk, immediate effect for the rest

`candidate` records take local effect immediately (weighted with caution); vetting only gates `evolve`, not local effect. Because onboard is high-volume cold inference, it gates the one high-risk category and lets the bulk flow:

- **`conventions` → written immediately as `candidate`.** They take effect at once and are refined later, asynchronously and at your pace, via `/distill review`. No synchronous audit.
- **`constraints` → held for a quick in-session review at the end of the scan.** Because a wrong, top-weighted constraint would otherwise take honored-first effect unreviewed, onboard accumulates constraint candidates and, at the end, presents them for a fast review. This is a **persist / do-not-persist** decision for *this scan's* constraints — **not** a promotion to `vetted`, and **not** an invocation of `/distill review`. For each candidate you may **persist**, **edit then persist**, or **drop**; only persisted ones are written (as `candidate`). If the scan found **no** constraint candidates, there is no synchronous step.

The user reviews only the small high-risk set here; the ongoing, backlog-wide vetting of any `candidate` remains the separate asynchronous `/distill review` channel.

## Output Summary

Report concisely in the interaction language: the records added / updated per category and file, any `conflict` records deferred, and **which areas were deep-read versus sampled** (never imply full coverage when you sampled). On an empty or knowledge-free scan, write nothing and report "nothing to onboard".

## Boundaries (recap)

- Read-only on code; write-only to `.codexspec/profile/`; no source / test / git / constitution mutation.
- Standalone: no auto-next, no automatic hook, and **no Automatic Distillation step** (onboard is not a wrap-up command).
- Writes only `conventions` and `constraints`; never `decisions`, `pitfalls`, `strategies`, or `runbooks`.
- Produces no persistent document beyond profile records.
