---
name: codexspec:review-tasks
description: "审查任务的忠实度、可执行性、依赖关系与验证"
---

# Tasks Reviewer

## Language Preference

Read `.codexspec/config.yml`. Two independent language controls apply (each falls back to `language.output`, then English):

- **Interaction language** (`language.interaction`): language for all conversation with the user — questions, explanations, status messages, and `codexspec` CLI terminal output.
- **Document language** (`language.document`): language for generated artifact files (requirements/spec/plan/tasks).

Converse in the interaction language and author artifacts in the document language. Apply the project's translation standard to both: translate by meaning (not word-for-word), keep English for terms with no good native equivalent, and write as if originally in that language.

## User Input

`the text after the $codexspec:review-tasks skill mention`

## Review Authority

Resolve by explicit path, then current branch; never silently select the latest feature.

Read `requirements.md`, `spec.md`, `plan.md`, `tasks.md`, the constitution, and relevant repository paths.

If `requirements.md` is absent, use legacy spec-only mode and disclose that original-discussion fidelity cannot be verified.

Authority order:

1. Confirmed requirements
2. Specification
3. Constitution and verified repository facts
4. Approved plan
5. Task list
6. Applicable best practices

## Review Passes

### 1. Fidelity and Coverage

- Map plan deliverables and `REQ`/`NFR` items to tasks.
- Verify every task includes `Covers:` and a plan reference, or is explicitly justified implementation support.
- Detect omitted deliverables, unauthorized scope, redesign hidden inside tasks, and tasks based on superseded or open requirements.

### 2. Executability and Internal Quality

Report only evidence-backed defects:

- A task lacks a verifiable outcome
- Required paths or dependencies are wrong or impossible
- A dependency is circular or a dependent is ordered first
- Verification is insufficient for an actual requirement or repository quality gate
- Task boundaries make the result impossible to implement or validate
- A parallel marker is unsafe because declared work overlaps or depends on unfinished output

Do not treat one-file tasks, maximum parallelism, a fixed phase layout, or universal TDD as inherent quality requirements.

Test-first ordering is a defect only when required by the constitution, specification, plan, or established repository workflow.

### 3. Advisories

Optional sequencing, parallelism, task splitting, documentation, or testing improvements belong in **Risk Advisories** or **Design Opportunities** when they are not required for correctness.

Advisories do not affect status, do not affect the score, and must not be auto-fixed.

## Finding Validation

Every defect must include:

- **Evidence**
- **Location**
- **Mismatch**
- **Impact**
- **Remediation**

Merge findings with the same root cause. One missing upstream deliverable must not be deducted again as coverage, ordering, granularity, and file-path defects.

Reject findings that only optimize style or methodology without a concrete implementation risk.

Zero verified defects is a valid result.

## Severity, Status, and Compatibility Score

- Critical: tasks cannot produce a correct implementation or violate confirmed intent
- Warning: likely implementation failure or major rework
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

Advisory does not affect the score. There are no fixed deductions for file count, test placement, phase names, or `[P]` coverage.

## Report

Save `<feature-dir>/review-tasks.md`:

```markdown
# Tasks Review Report

## Summary
- **Overall Status**: PASS / PASS_WITH_WARNINGS / NEEDS_REVISION / BLOCKED
- **Compatibility Score**: X/100
- **Authority Mode**: Requirements-first / Legacy spec-only
- **Readiness**: Ready for Implementation / Revision Required

## Coverage
| Requirement / Plan Item | Task References | Result |

## Verified Defects
### Critical
### Warnings
### Minor

## Risk Advisories

## Design Opportunities

## Score Derivation
```
