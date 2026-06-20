---
description: 将已批准的计划展开为可追溯、可执行的任务
argument-hint: "[tasks 功能目录、plan.md 或 spec.md]"
handoffs:
  - agent: claude
    step: Generate tasks from the approved plan
---

# Plan to Tasks Converter

## Language Preference

Read `.codexspec/config.yml`. Use `language.output`; default to English.

## User Input

`$ARGUMENTS`

## Role

Act as a **plan expander**. Produce implementation tasks that execute the approved plan without redesigning it.

## Feature Resolution and Inputs

Use an explicit path first, then the current branch. Ask the user if the feature cannot be resolved uniquely; never select the latest directory silently.

Read:

- `requirements.md`
- `spec.md`
- `plan.md`
- Constitution and relevant repository conventions

Legacy compatibility: when `requirements.md` is absent, use `spec.md` as the temporary highest authority and state the limitation.

## Stop Conditions

Before task generation, verify that the plan covers the specification and does not contradict confirmed requirements.

Stop instead of guessing when:

- A plan component is undefined or internally contradictory.
- A task would require a new architecture or product decision.
- Required file paths or dependencies cannot be determined safely.
- A critical upstream item remains open.

## Task Rules

- Every task must include `Covers: REQ-xxx; Plan: <component/phase>`.
- A task must have one clear, verifiable outcome.
- Do not equate atomicity with exactly one file. Multiple tightly related files may belong to one task when splitting them would make validation artificial or incomplete.
- Use exact paths when they are known from the plan or repository; do not invent paths to satisfy a template.
- Preserve the plan's organization. Group by user story, component, or technical phase according to the approved plan.
- Declare only dependencies that are needed to execute or validate the task.
- Mark `[P]` only when tasks can actually run concurrently after their declared dependencies. Missing `[P]` is not inherently a defect.
- Require test-first ordering only when mandated by the constitution, specification, plan, or established repository workflow.
- Otherwise include the appropriate verification task without imposing TDD as a universal method.
- Do not add polish, monitoring, abstraction, documentation, or hardening tasks unless they are required by the approved plan, repository policy, or a verified implementation need.

## Required Output

Save `<feature-dir>/tasks.md`.

Include:

- Task groups derived from the plan
- Task IDs, outcomes, paths, dependencies, and traceability
- Verification steps and checkpoints appropriate to the change
- A coverage table mapping plan components and requirements to tasks
- Unmapped tasks, if any, with explicit justification

## Pre-Save Validation

1. Every plan deliverable has task coverage.
2. Every task maps to upstream authority or necessary implementation support.
3. Dependencies are acyclic and ordered before dependents.
4. Verification is sufficient for the actual risk and project policy.
5. No task expands product scope or silently changes the plan.

## Automatic Review Loop

Invoke `/codexspec:review-tasks <feature-dir>/tasks.md`.

- Automatically fix only verified defects with deterministic corrections.
- Do not auto-apply Risk Advisories or Design Opportunities.
- Do not split or add tasks solely to improve a score.
- Run a maximum of two automatic fix-and-review rounds.
- Stop if defects repeat, remain unresolved, or require a user or architecture decision.

## Output Summary

Report the tasks path, plan/requirement coverage, dependency summary, unresolved items, and auto-review status.
