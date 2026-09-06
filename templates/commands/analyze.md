---
description: Analyze end-to-end traceability and consistency across SDD artifacts
argument-hint: "[feature directory]"
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
