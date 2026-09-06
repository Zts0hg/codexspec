---
description: 解决需求歧义，并将 requirements.md 与 spec.md 同步
argument-hint: "[spec.md、requirements.md 或 功能目录]"
---

# Requirements Clarifier

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

`$ARGUMENTS`

## Feature Resolution

Use an explicit path first, then the current branch. Ask the user when resolution is ambiguous; never silently select the latest feature.

Read:

- `requirements.md`
- `spec.md`
- `review-spec.md` when present
- Constitution

Legacy compatibility: when only `spec.md` exists, extract candidate requirement records with `Status: open`. Do not assume the extracted wording reflects the original discussion until the user confirms it.

## Clarification Priorities

Prioritize:

1. Confirmed requirement and spec mismatches
2. Critical or Warning defects from `review-spec.md`
3. Open items that block planning
4. Material ambiguity, contradiction, missing behavior, or unverifiable requirements

Do not ask questions solely to fill a template section or add generic best practices.

## Question Loop

- Ask exactly one material question at a time.
- Explain the affected requirement IDs and implementation consequence.
- Offer 2-4 meaningful options when possible.
- Limit a session to five questions unless the user explicitly asks to continue.

After each answer, keep it as a candidate. At a coherent stage boundary, present a stage summary and request explicit confirmation.

## Persistence Order

Update `requirements.md` first.

Only after the user confirms the stage summary:

1. Add or modify the relevant `NEED`, `CON`, `DEC`, `OUT`, or `OPEN` entries.
2. Mark replaced entries `superseded` rather than deleting them.
3. Add short User Evidence and a Confirmation Log entry.
4. Update `spec.md` to reflect the confirmed entries.
5. Update `Sources:` and the requirements traceability table.

Never update `spec.md` with an unconfirmed answer. Never leave confirmed requirements and spec content knowingly inconsistent.

## Completion

Report:

- Questions asked and confirmed
- Requirements entries added, changed, superseded, or left open
- Spec requirements updated
- Remaining blockers
- Whether `/codexspec:review-spec` should run again
