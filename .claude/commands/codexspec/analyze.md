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
