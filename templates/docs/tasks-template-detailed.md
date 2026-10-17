# Tasks: [FEATURE NAME]

<!--
Language: Generate this document in the language specified in .codexspec/config.yml
If not configured, use English.
-->

**Input**: Design documents from `.codexspec/specs/{feature-id}/`
**Prerequisites**: Approved plan.md and spec.md; requirements.md and design.md when available. Follow the command's legacy-compatibility rules when either is absent.

**Tests**: Tests are required when the constitution, specification, plan, or established repository workflow requires them. Use test-first ordering only when that policy applies; otherwise include the verification work appropriate to the change.

**Organization**: Preserve the approved plan's grouping by user story, component, or technical phase. Add setup, foundation, documentation, monitoring, or hardening tasks only when the approved plan, repository policy, or a verified implementation need requires them. These headings and examples do not authorize extra scope.

## Format: `[ID] [P?] [Story] Description`

- **[ID]**: Unique task ID, such as T001.
- **[P]**: Parallel-safe after the declared prerequisites, with settled interfaces and no conflicting writes or shared-state dependencies. Different files alone do not establish independence.
- **[Story]**: User story label when the plan groups work by story; omit it for component or phase groups.
- Include exact file paths when known from the plan or repository; do not invent paths.
- Each task must produce a single verifiable outcome. A task may touch multiple tightly related files when splitting them would make the result unverifiable or create artificial coordination.
- Add `Covers: REQ-xxx; Plan: <component/phase>` to preserve traceability.

## [Group from the Approved Plan]

**Goal**: [Observable result delivered by this group]
**Upstream**: [Plan component/phase and its covered requirement or acceptance criteria]
**Prerequisites**: [Necessary predecessor results, or none]

### T001: [Verifiable Task Outcome]

- [ ] T001 [Story if applicable] [Outcome] — Covers: REQ-xxx; Plan: [component/phase]
  - **Paths**: [Known implementation and verification paths]
  - **Dependencies**: [Task IDs and the results they supply, or none]
  - **Verification**: [Test/check and expected observable result]

#### Test Scenarios for T001

For testable tasks, enumerate individually identifiable cases derived from the upstream
acceptance criteria and behavior. Include the happy path and applicable boundary/error
conditions. Repeat only for cases the behavior implies; stop for underspecified upstream
behavior rather than inventing an expected result.

| Scenario | Upstream Behavior | Input / Action | Expected Result |
|----------|-------------------|----------------|-----------------|
| T001-S1 | REQ-xxx / [acceptance criterion] | [Normal input/action] | [Observable result to assert] |
| T001-S2 | REQ-xxx / [boundary/error behavior] | [Applicable boundary/error input] | [Observable result to assert] |

Documentation, configuration, assets, and infrastructure tasks omit this scenario section
and retain their deterministic Verification. Do not manufacture code tests for non-code work.

Repeat this task structure for the actual deliverables. Verification may belong to the
same task as implementation; create a separate task only when it has its own verifiable
outcome and useful dependency boundary.

## Dependencies & Execution Order

| Task | Prerequisite | Required Result |
|------|--------------|-----------------|
| [Dependent task ID] | [Predecessor task ID] | [Contract, artifact, or verified outcome needed before starting] |

Keep dependencies acyclic and list predecessors before dependents. Do not make every
story depend on a generic foundation phase unless the approved plan actually requires it.

### Parallel Opportunities

- [Task IDs that may run concurrently, their satisfied prerequisites, and why their writes and shared-state use are independent]
- Leave tasks sequential when an interface or dependency is unresolved. A `[P]` label is not permission to ignore a prerequisite.

## Coverage

| Requirement | Plan Component / Phase | Task | Scenario / Verification |
|-------------|------------------------|------|-------------------------|
| REQ-xxx / NFR-xxx | [plan reference] | T001 | T001-S1, T001-S2 / [deterministic check] |

Every plan deliverable needs task coverage. Explain any task that is necessary
implementation support rather than direct requirement coverage; do not use that category
to introduce unrelated work.

## Execution Notes

- Execute the approved plan's order and delivery strategy; do not impose a fixed MVP or deployment sequence.
- When test-first is required, verify the expected failure before implementation. Otherwise run the appropriate verification without imposing TDD.
- Keep planned checks separate from actual results. During implementation, map each enumerated scenario to a test that asserts its expected outcome and report executed commands, results, and tested revision.
- Mark a task complete only after its outcome and required verification are established. Missing scenario coverage remains subject to the existing implement-tasks self-check.
- Git staging, commits, deployment, and other external actions follow existing workflow authorization; a task checkbox does not grant permission.
