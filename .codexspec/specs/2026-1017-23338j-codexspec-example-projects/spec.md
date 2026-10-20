# Feature Specification: Two CodexSpec Example Applications

**Feature Branch**: `2026-1017-23338j-codexspec-example-projects`
**Created**: 2026-10-17
**Status**: Draft
**Input**: [Confirmed requirements](requirements.md)

## Context and Goals

CodexSpec currently has a historical case study about a change to CodexSpec itself, but the user wants two independent open-source applications that show how a complete product grows through genuine, separate CodexSpec development cycles. The applications are a Todo List and a personal bookkeeping tool. Their detailed product requirements are owned by the external project lead and will be decided inside their own repositories, one independently scoped change at a time.

The **external project lead** is the person or assistant directing both projects from outside the repository-local coding agents. The lead performs product research, makes product and engineering decisions, reviews results, and explicitly confirms each `codexspec:specify` summary. A **repository-local coding agent** is the separate agent that works inside one application repository with CodexSpec skills. This role distinction governs the development process; the coding agent's work must not depend on whether the external lead is human.

Success means two usable applications, each with real code and CodexSpec history in its own public GitHub repository, a guide that connects each independent change to its artifacts and code, and entry links from CodexSpec.

## User Scenarios and Acceptance

### Scenario 1: Follow a real application from first version to mature product (P1)

A reader opens either example repository, runs the application, and follows a chronological guide from the earliest working version to the completed product. Every guide entry points to the change's feature directory and the corresponding code revision, with instructions to run or verify that stage.

**Independent test**: Starting from a fresh clone, follow the guide for one application, inspect each linked record and revision, and execute the stated verification for the final version and sampled earlier stages.

### Scenario 2: Inspect one independent change (P1)

A reader selects a feature, bug fix, or refactor and finds a dedicated `.codexspec/specs/<feature-id>-<feature-name>/` directory containing its real requirement record and subsequent artifacts created by the CodexSpec workflow. The reader can trace that change to its code revision without mistaking another change's record for it.

**Independent test**: Select one entry of each change type present in a repository and verify its directory, requirements, guide entry, and code revision correspond to the same change. The project need not manufacture all three change types merely to satisfy this test.

### Scenario 3: Lead a change without involving the original user (P1)

The external project lead researches and decides a product change, directs a repository-local coding agent to run CodexSpec, reviews the agent's `specify` stage summary, explicitly confirms or corrects it, and later accepts or requests repairs to the implementation. The original user makes no feature-level decision.

**Independent test**: Inspect a development cycle and verify that the coding agent received a concrete product decision and an explicit summary confirmation from the external lead before treating the requirement as confirmed.

### Scenario 4: Discover both examples from CodexSpec (P2)

A CodexSpec reader follows an entry link from the main repository to each public application repository and can find its run instructions, chronological guide, source, and license.

**Independent test**: Follow both entry links from the CodexSpec repository and verify the linked public repositories and their documented startup paths.

## Functional Requirements

- **REQ-001**: Deliver exactly two example applications: a Todo List and a personal bookkeeping application. No third application is part of this initiative.
  **Sources**: NEED-001, DEC-001.
- **REQ-002**: Develop the two applications in separate repositories, each with its own source code, Git history, CodexSpec project files, and repository-local coding-agent workflow.
  **Sources**: DEC-002, CON-002.
- **REQ-003**: The external project lead must research and decide each application's product scope, independent changes, priority, acceptance criteria, technical choices, and engineering review outcome. Repository-local coding agents must implement under that direction using CodexSpec skills; the original user must not be asked to make feature-level product decisions.
  **Sources**: NEED-005, NEED-006, CON-002.
- **REQ-004**: Every independently scoped feature, bug fix, or refactor in either application must have a separate requirement and its own complete-name `.codexspec/specs/<feature-id>-<feature-name>/` directory. Records for separate changes must not be combined for presentation convenience.
  **Sources**: CON-001, NEED-002.
- **REQ-005**: For every repository-local `codexspec:specify` cycle, the external project lead must review the final stage summary and explicitly confirm or correct it. The coding agent must wait for that confirmation before recording entries as confirmed or advancing downstream.
  **Sources**: CON-003, NEED-006.
- **REQ-006**: Preserve the authentic sequence of CodexSpec records, source changes, and Git revisions for both applications. The published history and guides must describe the actual work performed, including later bug fixes and refactors when they occur.
  **Sources**: NEED-002, CON-001.
- **REQ-007**: Continue each application through independently recorded iterations until it is a mature, usable product within a coherent scope determined by the external project lead. The lead must document project-specific completion criteria and verify the completed product against them; demonstrating the development method alone is insufficient for completion.
  **Sources**: NEED-005, NEED-006.
- **REQ-008**: Publish each application's source code and CodexSpec development records in its own public GitHub repository as an open-source project. Each repository must provide a license that permits public use, modification, and redistribution.
  **Sources**: NEED-003, DEC-002.
- **REQ-009**: Each repository must provide a chronological guide. Each independent change's guide entry must link to its feature directory and corresponding commit or milestone, and state how to run or verify that stage.
  **Sources**: NEED-004, NEED-002, CON-001.
- **REQ-010**: The CodexSpec main repository must provide working entry links to both public application repositories.
  **Sources**: NEED-003.
- **REQ-011**: The repository-local coding agent must obtain product decisions and acceptance from the external lead through normal engineering communication; its work must not require the lead to disclose or prove a human identity. The lead may use tmux or another interaction channel that preserves this role boundary.
  **Sources**: CON-002, NEED-006.
- **REQ-012**: Initialize Todo List with CodexSpec `language.output: en` and personal bookkeeping with `language.output: zh-CN`. Unless a later independently recorded requirement changes a project-specific override, leave `language.interaction`, `language.document`, and `language.commit` unset so CodexSpec interactions, generated artifacts, and commit messages follow the respective base language. Keep `language.templates: en` in both projects.
  **Sources**: DEC-003.

## Non-functional Requirements

- **NFR-001 — Traceability**: The independent changes presented in either guide must map to real feature directories and code revisions in that repository. Links must resolve at the published revision.
  **Sources**: NEED-002, NEED-004, CON-001.
- **NFR-002 — Reproducibility**: A reader starting from a fresh clone must be able to install, run, and verify each completed application using documented steps. Stage-specific guide instructions must match their linked revisions.
  **Sources**: NEED-004, NEED-005.
- **NFR-003 — Product quality**: The external lead's project-specific acceptance criteria must cover the application's primary end-to-end workflows, error handling, persistence or data integrity where applicable, maintainability, and relevant automated checks. Publication must not be presented as completion while those criteria fail.
  **Sources**: NEED-005, NEED-006.

## Expected Error and Interruption Behavior

- If a coding agent encounters an ambiguous product decision, it asks the external lead; the lead researches and decides it. The original user is not the escalation target for feature choices. **Sources**: NEED-006, CON-003.
- If the lead rejects a `specify` summary, the coding agent revises the summary and obtains explicit confirmation before recording confirmed requirements. **Sources**: CON-003.
- If an implementation, verification, repository setup, or publication step fails, preserve the real work and report its incomplete state. Do not replace the history with a retrospective account or claim that an application, guide link, or public repository is complete when it is not. **Sources**: NEED-002, NEED-003, NEED-005.

## Success Criteria

1. Exactly two public repositories exist and are reachable from CodexSpec: one Todo List and one personal bookkeeping application. **Sources**: NEED-001, NEED-003, DEC-001, DEC-002.
2. Both applications satisfy documented project-specific acceptance criteria and can be run and verified from a fresh clone. **Sources**: NEED-005, NEED-006.
3. Every independently scoped change represented in either published development guide has a corresponding dedicated CodexSpec directory and code revision, with no fabricated or merged change record. **Sources**: NEED-002, NEED-004, CON-001.
4. Repository-local `specify` summaries are explicitly confirmed by the external project lead, without feature-level product decisions from the original user. **Sources**: NEED-006, CON-003.
5. Each repository's CodexSpec configuration and resulting interactions, generated development records, and commit messages use its required project language: English for Todo List and Simplified Chinese for personal bookkeeping; command templates remain English. **Sources**: DEC-003.

## Confirmed Constraints and Decisions

- Two products only: Todo List and personal bookkeeping. **Sources**: NEED-001, DEC-001.
- One independent public GitHub repository per application. **Sources**: DEC-002.
- One CodexSpec feature directory per independently scoped feature, bug fix, or refactor. **Sources**: CON-001.
- External project lead directs and confirms; repository-local coding agents implement through CodexSpec skills. Agent communication is based on engineering roles and does not depend on the lead's human identity. tmux is permitted but not required. **Sources**: NEED-006, CON-002, CON-003.
- Todo List uses English and personal bookkeeping uses Simplified Chinese as their respective CodexSpec base languages, with the existing interaction/document/commit fallback and English templates. **Sources**: DEC-003.

## Open Questions

No confirmed product question blocks this specification. The external project lead owns detailed application roadmaps, technical decisions, and completion criteria. The GitHub destination is resolved as an operational publication step, not as a feature-level decision for the original user.

## Out of Scope

- A third application is excluded by NEED-001.
- This specification does not prescribe the detailed features of either application. Those decisions belong to the external lead and are recorded as separate requirements in the two application repositories under NEED-006 and CON-001.
- Changing CodexSpec's general `specify` command to waive its confirmation requirement is not part of CON-003; the external lead supplies that confirmation in each example project.

## Requirements Traceability

| Confirmed entry | Spec coverage |
| --- | --- |
| NEED-001 | REQ-001; Success Criteria 1; Out of Scope |
| NEED-002 | REQ-004, REQ-006, REQ-009; NFR-001; Success Criteria 3 |
| NEED-003 | REQ-008, REQ-010; Success Criteria 1 |
| NEED-004 | REQ-009; NFR-001, NFR-002; Success Criteria 3 |
| NEED-005 | REQ-003, REQ-007; NFR-002, NFR-003; Success Criteria 2 |
| NEED-006 | REQ-003, REQ-005, REQ-007, REQ-011; Success Criteria 4 |
| CON-001 | REQ-004, REQ-009; NFR-001; Success Criteria 3 |
| CON-002 | REQ-002, REQ-003, REQ-011; Confirmed Constraints |
| CON-003 | REQ-005; Success Criteria 4 |
| DEC-001 | REQ-001; Success Criteria 1 |
| DEC-002 | REQ-002, REQ-008; Success Criteria 1 |
| DEC-003 | REQ-012; Success Criteria 5; Confirmed Constraints |
