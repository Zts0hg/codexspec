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

## Operating Constraints

This command is read-only. Do not modify artifacts.

Resolve the feature by explicit path, then current branch. Ask the user if it is ambiguous; never select the latest feature silently.

## Inputs

Load:

- `requirements.md`
- `spec.md`
- `plan.md`
- `tasks.md`
- Constitution

Legacy compatibility: if `requirements.md` is missing, state that the analysis starts at `spec.md` and cannot validate fidelity to the original discussion.

## End-to-End Traceability

Build the chain:

```text
confirmed NEED/CON/DEC/OUT
  -> REQ/NFR Sources
  -> plan Covers
  -> task Covers + Plan reference
```

Detect:

- Confirmed requirements with no spec coverage
- Spec requirements with missing or invalid sources
- Spec requirements with no plan coverage
- Plan deliverables with no task coverage
- Tasks with no upstream authority or implementation-support justification
- Semantic drift, scope expansion, contradictions, and use of superseded/open entries
- Dependency or ordering conflicts that prevent execution

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
- Verified defects by severity
- Unmapped or unauthorized items
- Risk Advisories
- Design Opportunities
- Coverage counts for each link in the chain

It is valid to report zero defects.
