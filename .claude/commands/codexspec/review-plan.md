---
description: 审查计划的忠实度、可行性与实现就绪度
argument-hint: "[plan.md 或 功能目录]"
handoffs:
  - agent: claude
    step: Review plan against confirmed requirements, spec, and repository facts
---

# Plan Reviewer

## Language Preference

Read `.codexspec/config.yml`. Two independent language controls apply (each falls back to `language.output`, then English):

- **Interaction language** (`language.interaction`): language for all conversation with the user — questions, explanations, status messages, and `codexspec` CLI terminal output.
- **Document language** (`language.document`): language for generated artifact files (requirements/spec/plan/tasks).

Converse in the interaction language and author artifacts in the document language. Apply the project's translation standard to both: translate by meaning (not word-for-word), keep English for terms with no good native equivalent, and write as if originally in that language.

## User Input

`$ARGUMENTS`

## Review Authority

Resolve by explicit path, then current branch; never silently select the latest feature.

Read `requirements.md`, `spec.md`, `plan.md`, the constitution, and only the repository files necessary to verify plan claims.

If `requirements.md` is absent, use legacy spec-only mode and disclose that original-discussion fidelity cannot be verified.

Authority order:

1. Confirmed requirements
2. Specification
3. Constitution and verified repository facts
4. Plan-level technical decisions
5. Applicable best practices

## Review Passes

### 1. Fidelity and Coverage

- Verify every `REQ`/`NFR` has plan coverage.
- Verify each component or phase has `Covers:`.
- Detect omitted behavior, semantic changes, scope expansion, and plan decisions that override confirmed trade-offs.
- Verify plan-level assumptions remain labeled and do not become product requirements.

### 2. Feasibility and Internal Quality

Report evidence-backed defects such as:

- Referencing nonexistent modules, APIs, paths, or capabilities
- Contradictory component responsibilities or dependencies
- Missing implementation decisions that genuinely block task generation
- Invalid ordering, migration, compatibility, security, or data assumptions
- Complexity that creates concrete risk without serving a confirmed requirement

Architecture diagrams, dependency graphs, explicit versions, design patterns, scalability sections, deployment plans, and observability are required only when the feature or repository context makes them necessary.

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

Merge findings with the same root cause. Do not deduct the same root cause under alignment, architecture, and phase planning separately.

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

Save `<feature-dir>/review-plan.md`:

```markdown
# Plan Review Report

## Summary
- **Overall Status**: PASS / PASS_WITH_WARNINGS / NEEDS_REVISION / BLOCKED
- **Compatibility Score**: X/100
- **Authority Mode**: Requirements-first / Legacy spec-only
- **Readiness**: Ready for Tasks / Revision Required

## Requirement Coverage
| Requirement | Plan Reference | Result |

## Verified Defects
### Critical
### Warnings
### Minor

## Risk Advisories

## Design Opportunities

## Score Derivation
```
