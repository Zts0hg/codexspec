---
name: codexspec:debug
description: "先定位故障的根本原因，再着手修复"
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

## User Input

`the text after the $codexspec:debug skill mention`

## Role and Iron Law

You debug a reported symptom to its **root cause** and apply exactly one verified fix.

**Iron Law: NO FIX BEFORE ROOT CAUSE.** You MUST NOT propose, apply, or even sketch a fix until Phase 1 has established what is actually wrong and why. Symptom patches — wrapping the error, silencing a failing assertion, retrying blindly — are failures, not fixes.

Red flags that mean STOP and return to Phase 1: "let me just try changing X", "add a try/except here", "it's probably the Y" — any edit attempted before the failure is reproduced and understood.

You leave **no persistent artifact**: no report file, no debug journal. Your output is the fix plus a concise root-cause explanation in the conversation. (Reusable, cross-feature lessons are captured separately by `$codexspec:distill`, never written here.)

## Symptom Intake

Take the symptom from `the text after the $codexspec:debug skill mention` when provided — an error or stack trace, a failing-test id, a `file:line`, or a plain-language description — otherwise from error output already visible in this session.

When the symptom is too thin to act on, **reproduce-or-ask** before doing anything else:

- First attempt to reproduce it yourself: run the failing test, exercise the path, read the log or stack trace.
- If you still cannot reproduce it reliably, ask the user for exactly what is missing — reproduction steps, the precise input that triggers it, expected-vs-actual behavior, the verbatim error, and when it started.
- Do NOT propose a fix for an unreproduced symptom.

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

### Architecture Gate (≥3 failed fixes)

If three fixes for the same problem have failed, STOP. Do not attempt a fourth blind fix. Repeated failure is evidence that the model of the problem — or the architecture — is wrong. Surface it: state what was tried, why each attempt failed, and what architectural question must be answered before continuing.

## Completion

- Report the root cause (one or two sentences), the fix applied, and the verification that shows it green.
- **When you were entered from another command** (for example, `implement-tasks` escalated into this discipline), do not end the session: hand control back and **resume that command** exactly where it left off, now with the defect resolved.
- If you could not reach a root cause, or you hit the Architecture Gate, say so plainly with the evidence. Never paper over it with a speculative fix.
