---
description: 为小型变更运行精简的 Requirements-First SDD 流程
argument-hint: "描述一个小需求"
---

# Quick Implementation

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

## Scope Check

Quick is intended for a small, well-bounded change. Assess likely files, module span, new dependencies, and unresolved product decisions.

If the change is broad or has multiple independent outcomes, explain why the standard flow is safer and ask whether to continue with Quick.

## Compact Requirement Confirmation

Even in Quick mode, do not rely on session-only context.

1. Resolve only ambiguities that materially change implementation.
2. Create a feature workspace and `requirements.md` using the same timestamp feature convention as `/codexspec:specify`.
3. Present a concise confirmed requirement summary containing:
   - `NEED-*`
   - relevant `CON-*` and `DEC-*`
   - `OUT-*`
   - unresolved `OPEN-*`
4. Ask the user to confirm the summary.
5. Persist only confirmed entries, with short User Evidence and a Confirmation Log.

Do not start generation before confirmation. If a critical question remains open, stop.

## Automated Flow

Use the created feature directory explicitly for every command:

1. `/codexspec:generate-spec <feature-dir>/requirements.md`
2. `/codexspec:spec-to-plan <feature-dir>/spec.md`
3. `/codexspec:plan-to-tasks <feature-dir>/plan.md`
4. `/codexspec:implement-tasks <feature-dir>/tasks.md`

The generation commands own their automatic review loops. Do not duplicate review logic here.

If a review requires a new product or architecture decision, pause Quick and ask the user. Do not infer a decision merely to preserve automation.

## Completion

Report the feature directory, requirements/spec/plan/tasks paths, review outcomes, implementation verification, and unresolved advisories separately.
