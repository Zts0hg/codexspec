---
name: codexspec:review-spec
description: "审查规格的忠实度、内部质量与计划就绪度"
---

# Specification Reviewer

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

`the text after the $codexspec:review-spec skill mention`

## Review Authority

Resolve the feature by explicit path, then current branch. Never silently select the latest feature.

Read `requirements.md`, `spec.md`, and the constitution. If `requirements.md` is absent, enter legacy compatibility mode: use `spec.md` as temporary authority and state that fidelity to the original discussion cannot be verified.

Authority order:

1. Confirmed requirements and decisions
2. The specification being reviewed
3. Constitution and verified repository facts
4. Applicable best practices

## Review Passes

### 1. Fidelity

- Map every confirmed `NEED`, `CON`, `DEC`, and `OUT` entry to the specification.
- Detect omissions, semantic changes, scope expansion, promoted open questions, and ignored superseding decisions.
- Verify every `REQ`/`NFR` has valid `Sources:`.

### 2. Intrinsic Quality

Report only defects that can affect the user goal or technical planning:

- Contradictions
- Multiple materially different interpretations
- Untestable required behavior
- Missing expected behavior for relevant failure or boundary cases
- Impossible or unverifiable requirements

Do not require a section, metric, persona format, or example merely because a template contains it.

### 3. Advisories

Applicable best practices may be offered under **Risk Advisories** or **Design Opportunities** only. State the applicability condition, concrete risk or benefit, and relationship to the confirmed goal.

Advisories do not affect status, do not affect the score, and must not be auto-fixed.

## Finding Validation

Before reporting a defect, provide:

- **Evidence**: confirmed requirement, upstream statement, constitution rule, or verified fact
- **Location**: exact section or requirement
- **Mismatch**: difference between evidence and current content
- **Impact**: concrete effect on the goal or next stage
- **Remediation**: minimum correction that introduces no new decision

Merge findings with the same root cause. Never deduct or report the same defect again under another category.

Reject a candidate finding when it is only a preferred method, cannot describe a concrete impact, or would overwrite a confirmed user trade-off.

It is valid and preferred to report zero defects when none are substantiated.

## Severity and Status

- **Critical**: core requirement is wrong, impossible, unsafe, or materially contradicts confirmed intent; blocks planning.
- **Warning**: likely to cause incorrect planning or major rework; should be fixed first.
- **Minor**: localized, verified defect with limited impact; does not block planning.
- **Advisory**: optional risk note or opportunity; not a defect.

Status:

- Any Critical: `BLOCKED`
- No Critical and at least one Warning: `NEEDS_REVISION`
- Only Minor defects: `PASS_WITH_WARNINGS`
- No defects: `PASS`

## Compatibility Score

Calculate only after validating and deduplicating defects:

- No defects: `100`
- Minor only: `max(80, 100 - 3 × Minor)`
- Warning present: `max(50, 79 - 8 × (Warning - 1) - 3 × Minor)`
- Critical present: `max(0, 49 - 15 × (Critical - 1) - 8 × Warning - 3 × Minor)`

Advisory does not affect the score. Fixed template omissions and optional formatting never create automatic deductions.

## Report

Save `<feature-dir>/review-spec.md`:

```markdown
# Specification Review Report

## Summary
- **Overall Status**: PASS / PASS_WITH_WARNINGS / NEEDS_REVISION / BLOCKED
- **Compatibility Score**: X/100
- **Authority Mode**: Requirements-first / Legacy spec-only
- **Readiness**: Ready for Planning / Revision Required

## Traceability
| Confirmed Entry | Spec Reference | Result |

## Verified Defects
### Critical
### Warnings
### Minor

## Risk Advisories

## Design Opportunities

## Score Derivation
- Critical root causes: X
- Warning root causes: X
- Minor root causes: X
- Formula: ...
```
