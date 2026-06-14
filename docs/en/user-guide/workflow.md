# Workflow

CodexSpec structures development into reviewable checkpoints while preserving the user's confirmed intent across sessions.

## Workflow Overview

```text
Constitution
    |
Idea -> /specify -> requirements.md -> /generate-spec -> spec.md
                                                    -> /spec-to-plan -> plan.md
                                                                    -> /plan-to-tasks -> tasks.md
                                                                                       -> /implement-tasks
```

`requirements.md` persists the result of requirement discussions. It records confirmed needs, constraints, decisions, exclusions, open questions, user evidence, and a confirmation log.

## Authority And Traceability

When sources conflict, commands use this order:

1. Confirmed entries in `requirements.md`
2. `spec.md`
3. Applicable constitution rules and repository facts
4. `plan.md`
5. `tasks.md`
6. General best practices

Later artifacts cannot silently redefine earlier ones. Requirements use stable IDs, specification items cite `Sources`, plans and tasks cite `Covers`, and unresolved conflicts stop generation for user confirmation.

Legacy feature directories containing only `spec.md` remain supported. Commands explicitly report that traceability to the original discussion is unavailable.

## Core Commands

| Stage | Command | Output |
|-------|---------|--------|
| 1 | `/codexspec:constitution` | Project principles |
| 2 | `/codexspec:specify` | Confirmed `requirements.md` |
| - | `/codexspec:clarify` | Updated requirements, then synchronized spec |
| 3 | `/codexspec:generate-spec` | `spec.md` and `review-spec.md` |
| 4 | `/codexspec:spec-to-plan` | `plan.md` and `review-plan.md` |
| 5 | `/codexspec:plan-to-tasks` | `tasks.md` and `review-tasks.md` |
| 6 | `/codexspec:analyze` | Read-only end-to-end traceability analysis |
| 7 | `/codexspec:implement-tasks` | Implementation |

Pass an explicit feature directory or artifact path when more than one feature exists. Commands never choose the newest directory implicitly.

## Review Model

Reviews separate three kinds of output:

- **Fidelity defects**: conflict with an authoritative source or omit required coverage.
- **Intrinsic defects**: the artifact is internally contradictory, unverifiable, or infeasible.
- **Risk advisories / design opportunities**: optional improvements without evidence of a current defect.

Every defect must identify its evidence, location, mismatch, impact, and minimal remediation. Findings with the same root cause are merged. Advisories do not affect status, score, or automatic fixes.

Review status is:

- `PASS`: no critical, warning, or minor defects.
- `PASS_WITH_WARNINGS`: only minor defects remain.
- `NEEDS_REVISION`: one or more warnings remain.
- `BLOCKED`: a critical conflict prevents reliable continuation.

The compatibility score is derived from the same classified findings rather than fixed template-section deductions. Status is authoritative; the score exists for integrations that still expect a number.

## Bounded Auto Review

Generation commands run the matching review automatically. They may repair only evidence-backed defects and re-review for at most two rounds. They stop earlier on `PASS`, and stop for user input when:

- an authoritative source conflicts with another source;
- a fix would change confirmed intent;
- the remaining item is advisory rather than defective;
- two repair rounds have been used.

Manual `/codexspec:review-*` commands can be run at any time for a fresh report.

## specify vs clarify

| Aspect | `/codexspec:specify` | `/codexspec:clarify` |
|--------|----------------------|----------------------|
| Purpose | Establish and confirm initial intent | Resolve gaps or ambiguities |
| Primary artifact | `requirements.md` | `requirements.md` |
| Spec handling | Generated later | Synchronized after confirmed changes |
| Open questions | Recorded without promotion | Updated only after user confirmation |

## Conditional TDD

Tasks use test-first ordering when required by confirmed needs, project policy, the plan, or implementation risk. Documentation and configuration work may be implemented directly. Each task should produce one verifiable outcome; it is not required to touch only one file.
