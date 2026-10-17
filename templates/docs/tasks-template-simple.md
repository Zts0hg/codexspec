# Tasks: [FEATURE NAME]

<!--
Language: Generate this document in the language specified in .codexspec/config.yml
If not configured, use English.
-->

Group work according to the approved plan. Repeat the task structure only for actual
deliverables; a small change may need one group and one task.

## 1. [Task Group from the Approved Plan]

- [ ] 1.1 [Task outcome] — Covers: REQ-xxx; Plan: [component/phase]
  - **Paths**: [Known paths from the plan or repository]
  - **Dependencies**: [Predecessor and required result, or none]
  - **Verification**: [Check and expected observable result]
  - **Test Scenarios** (testable tasks only):
    - **1.1-S1**: [Normal input/action and expected result, derived from acceptance criteria]
    - **1.1-S2**: [Applicable boundary/error condition and expected result]

For documentation, configuration, assets, or infrastructure tasks, omit Test Scenarios
and retain the appropriate deterministic Verification. Do not invent scenarios or extra
tasks to fill the template.

## Dependencies

- [Dependent task → prerequisite task and the result it needs; omit when there are none]
- Use `[P]` only when the approved interfaces and prerequisites permit concurrent work
  without conflicting writes or shared-state dependencies. Different files alone do not
  establish independence.

## Coverage

| Requirement | Plan Component / Phase | Task | Scenario / Verification |
|-------------|------------------------|------|-------------------------|
| REQ-xxx / NFR-xxx | [plan reference] | 1.1 | 1.1-S1, 1.1-S2 / [deterministic check] |

## Notes

- Each task should have a single verifiable outcome; do not split work solely to enforce one file per task.
- Test-first ordering applies only when required by the constitution, specification, plan, or established repository workflow.
- Planned checks and unchecked tasks do not prove completion; implementation reports the actual results and scenario-to-test mapping.
