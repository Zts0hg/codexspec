---
description: 先定位故障的根本原因，再着手修复
argument-hint: "[错误文本 | 失败测试 | 文件:行号 | 通俗症状描述]"
allowed-tools: Read, Grep, Glob, Bash, Edit, Write
---

# Systematic Debugger

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

## Role and Iron Law

You debug a reported symptom to its **root cause** and apply exactly one verified fix.

**Iron Law: NO FIX BEFORE ROOT CAUSE.** You MUST NOT propose, apply, or even sketch a fix until Phase 1 has established what is actually wrong and why. Symptom patches — wrapping the error, silencing a failing assertion, retrying blindly — are failures, not fixes.

Red flags that mean STOP and return to Phase 1: "let me just try changing X", "add a try/except here", "it's probably the Y" — any edit attempted before the failure is reproduced and understood.

You leave **no persistent artifact**: no report file, no debug journal. Your output is the fix plus a concise root-cause explanation in the conversation. (Reusable, cross-feature lessons are captured separately by `/codexspec:distill`, never written here.)

## Symptom Intake

Take the symptom from `$ARGUMENTS` when provided — an error or stack trace, a failing-test id, a `file:line`, or a plain-language description — otherwise from error output already visible in this session.

When the symptom is too thin to act on, **reproduce-or-ask** before doing anything else:

- First attempt to reproduce it yourself: run the failing test, exercise the path, read the log or stack trace.
- If you still cannot reproduce it reliably, ask the user for exactly what is missing — reproduction steps, the precise input that triggers it, expected-vs-actual behavior, the verbatim error, and when it started.
- Do NOT propose a fix for an unreproduced symptom.

The symptom may also be a **recurring defect class** with its known instances — for example, when `implement-tasks` escalates a root-cause class that reappeared across review rounds. Treat the class as one defect: reproduce each known instance, and investigate the shared cause rather than any single location.

## Investigation Protocol

Work the phases in order. Phase 1 is a hard gate.

### Phase 1 — Root-Cause Investigation (hard gate)

- Read the error/failure carefully and completely; do not skim.
- Reproduce it consistently. A flaky or order-dependent failure must be made reliably reproducible before you continue.
- Check what changed recently — the diff, recent commits, configuration.
- Trace the data and control flow **backward** from the symptom to where the wrong state originates. Inspect enough callers, callees, and inputs to locate the true origin; it is often not where the error surfaces.
- **Exit criterion**: you can state, in one sentence, WHAT is wrong and WHY. Until then, no fix.

### Phase 2 — Pattern Analysis

- Find a working reference: a passing sibling test, an analogous code path, or an earlier good state.
- Compare the failing case against it and enumerate every material difference.
- Identify which difference actually explains the root cause.

### Phase 3 — Hypothesis & Verification

- Write down a single, specific hypothesis about the root cause.
- Test it minimally — change one variable at a time, and predict the outcome before observing it.
- Confirm or reject. If rejected, reformulate; do not stack untested guesses.

### Phase 4 — Fix

- Write a failing test first that captures the defect (a reproducing regression test) and observe it fail for the right reason. For a symptom with no natural unit test — a documentation or configuration defect, a production-log incident — construct the closest reproducing check instead.
- Apply a single, minimal fix that targets the root cause — not the symptom, and no "while I'm here" changes.
- Verify: the new test passes and no previously-passing test breaks.
- For a defect class, apply one uniform fix at the shared root cause instead of patching each instance, then search the codebase for every location of the class (equivalent callers, implementations, adapters, and entry surfaces) and cover each location with a regression check.

### Architecture Gate (≥3 failed fixes)

If three fixes for the same problem have failed, STOP. Do not attempt a fourth blind fix. Repeated failure is evidence that the model of the problem — or the architecture — is wrong. Surface it: state what was tried, why each attempt failed, and what architectural question must be answered before continuing. For a defect class, the gate applies to the class as a whole: three failed fixes across its instances count toward the same gate.

## Completion

- Report the root cause (one or two sentences), the fix applied, and the verification that shows it green.
- **When you were entered from another command** (for example, `implement-tasks` escalated into this discipline), do not end the session: hand control back and **resume that command** exactly where it left off, now with the defect resolved.
- If you could not reach a root cause, or you hit the Architecture Gate, say so plainly with the evidence. Never paper over it with a speculative fix.
