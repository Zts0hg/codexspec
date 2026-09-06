---
description: Review design fidelity, feasibility, and planning readiness
argument-hint: "[design.md or feature directory]"
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
