# Implementation Plan: Two CodexSpec Example Applications

**Related Spec**: [spec.md](spec.md)
**Related Design**: [design.md](design.md)
**Confirmed Requirements**: [requirements.md](requirements.md)
**Created**: 2026-10-17
**Status**: Draft

## Context

This plan executes the two-repository, external-lead design in [design.md](design.md). The CodexSpec repository records the cross-project commitment and eventually links to two public applications. Each application repository owns its real product requirements, code, tests, and development history. The external lead has delegated authority to determine and accept all feature-level product decisions; repository-local coding agents implement them through CodexSpec.

## Goals and Scope

- Deliver a mature Todo List and a mature personal bookkeeping application, each in its own public open-source GitHub repository, with English and Simplified Chinese CodexSpec settings respectively.
- Make every independently scoped feature, bug fix, and refactor a real, separately confirmed CodexSpec change in its own repository.
- Provide a verified chronological guide for each application and working entry links in the CodexSpec repository.

The detailed product roadmaps and technology stacks are decisions for the external lead to record in the two application repositories. This cross-project plan does not substitute one umbrella requirements record for those individual changes. A third application and changes to CodexSpec's general `specify` confirmation rule are outside the confirmed scope.

## Existing Repository Constraints

- CodexSpec is developed in an isolated feature worktree. Its feature artifacts and later README edits remain in the selected CodexSpec feature workspace; the two application repositories are separately selected projects with their own CodexSpec roots and worktrees.
- The CodexSpec root READMEs are eight language variants. New user-facing links in the English README must be synchronized across the seven translations using the repository documentation workflow.
- The CodexSpec project constitution requires local quality gates and a green remote CI result for the exact commit before a push is considered complete. The application repositories receive their own project constitutions and verification criteria.
- The existing CodexSpec workflow retains feature worktrees rather than merging them automatically. Accepted changes in either application must be integrated deliberately before a guide points to the final public history.

## Plan-Level Decisions

### P1: Validate the operating loop with Todo List before using it for bookkeeping

- **Context**: Both projects need the same lead-to-agent confirmation and traceability process; bookkeeping adds more data-integrity complexity.
- **Options Considered**: Begin both at once; establish one complete change cycle in Todo List first.
- **Decision**: Establish and verify the first real `specify` → implementation → review → integrated revision → guide entry cycle in Todo List, then use the proven process for the remaining Todo List work and the bookkeeping repository. This does not limit either product's final scope.
- **Rationale**: A concrete end-to-end cycle exposes session, worktree, and Git-history errors while the first product change is small.
- **Trade-off**: Bookkeeping begins later, but both products retain the required complete outcome.
- **Covers**: REQ-002, REQ-004, REQ-005, REQ-006; Design: Two isolated application repositories and coding-agent sessions; Per-change CodexSpec record and accepted revision.

### P2: Treat each accepted change as the guide's unit of progress

- **Context**: Readers need actual revisions, not retrospective descriptions or moving branch links.
- **Options Considered**: Write one guide at the end; update each application's guide after every accepted, integrated change.
- **Decision**: After each independently scoped change passes review and is integrated into that application's main history, record its immutable accepted revision and update the chronological guide. Verify its links and stage instructions at that revision.
- **Rationale**: The guide remains synchronized with genuine development and makes broken provenance visible early.
- **Trade-off**: Documentation is part of every change's acceptance, increasing per-change work.
- **Covers**: REQ-004, REQ-006, REQ-009; NFR-001, NFR-002; Design: Per-change CodexSpec record and accepted revision; Reader guides and CodexSpec entry links.

### P3: Publish the main CodexSpec links after both application URLs are verified

- **Context**: The CodexSpec repository must not contain links to absent or inaccessible applications.
- **Options Considered**: Add placeholder links before publication; add final links after both public repositories are reachable.
- **Decision**: Publish and verify each application repository first, then add the two links to the CodexSpec README variants and verify the rendered documentation and CI.
- **Rationale**: The main repository presents only working entry points.
- **Trade-off**: The CodexSpec README update is the final cross-project integration step.
- **Covers**: REQ-008, REQ-010; NFR-001; Design: Reader guides and CodexSpec entry links.

### P4: Keep repository bootstrap separate from the first product capability

- **Context**: Project initialization, governance, and empty test/CI scaffolding can precede a product requirement, but a working application and its run instructions are part of a product change that readers must trace.
- **Options Considered**: Build a runnable baseline during repository bootstrap; build each first runnable application through its first recorded CodexSpec feature cycle.
- **Decision**: Bootstrap only non-product repository infrastructure before the first `specify` cycle. Implement and verify each application's first runnable user workflow and its fresh-clone run instructions within that application's first independently recorded feature.
- **Rationale**: The chronological guide can identify the actual first working revision without hiding product code in an unrecorded setup step.
- **Trade-off**: Initial setup does not yield a running application until the first feature is accepted.
- **Covers**: REQ-004, REQ-006, REQ-009; NFR-001, NFR-002; Design: Per-change CodexSpec record and accepted revision; Reader guides and CodexSpec entry links.

## Implementation Phases

### Phase 1: Prepare independent project environments

1. Select two new, unoccupied local repository paths and public GitHub repository names. Verify the authenticated GitHub destination and inspect the current CodexSpec installation. From each selected repository root, initialize Todo List with `codexspec init . --ai codex --lang en` and bookkeeping with `codexspec init . --ai codex --lang zh-CN`. Verify that each repository has Codex skills, the corresponding `language.output`, no unintended interaction/document/commit override, and `language.templates: en`. Keep secrets and private test data out of both repositories. **Covers**: REQ-001, REQ-002, REQ-008, REQ-012; Design: Two isolated application repositories and coding-agent sessions.
2. Establish each repository's project constitution, open-source license, empty source/test scaffolding, and basic CI without adding product behavior. The external lead documents a project-specific target scope and completion rubric before declaring any final product complete. Defer executable application code and fresh-clone run instructions to the first recorded product feature in each repository. **Covers**: REQ-003, REQ-004, REQ-006, REQ-007, REQ-008; NFR-001, NFR-003; Design: Application completion rubric and executable checks; Per-change CodexSpec record and accepted revision.
3. Start a separate repository-rooted coding-agent session for each project, using tmux where practical. Verify that the agent loads that repository's CodexSpec skills and can return its feature worktree path. Keep the external lead as the only product decision and summary-confirmation contact. **Covers**: REQ-002, REQ-003, REQ-005, REQ-011; Design: External project lead; Two isolated application repositories and coding-agent sessions.

### Phase 2: Prove the Todo List development cycle

1. The external lead researches and selects the first independently scoped Todo List capability, gives the repository-local agent a concrete change brief, and has it run `codexspec:specify`. Review and explicitly confirm or correct the final stage summary. **Covers**: REQ-003, REQ-004, REQ-005, REQ-011; Design: External project lead; Per-change CodexSpec record and accepted revision.
2. Let the agent follow CodexSpec's downstream stages in the returned feature workspace, implement and verify the first runnable Todo List workflow with fresh-clone run instructions, and report review evidence. The lead inspects behavior and artifacts, requests repairs if needed, and accepts only a passing result. **Covers**: REQ-004, REQ-006, REQ-007, REQ-009; NFR-002, NFR-003; Design: Two isolated application repositories and coding-agent sessions; Application completion rubric and executable checks; Per-change CodexSpec record and accepted revision.
3. Integrate the accepted change into the Todo List repository's Git history, capture its immutable revision, and add the first chronological guide entry with feature-directory and run/verification links. Check that those links and instructions work from the accepted revision. **Covers**: REQ-006, REQ-009; NFR-001, NFR-002; Design: Per-change CodexSpec record and accepted revision; Reader guides and CodexSpec entry links.

### Phase 3: Complete both applications through separate changes

1. For each remaining Todo List capability or independently scoped bug fix/refactor, repeat the Phase 2 lead/agent confirmation, implementation, review, integration, and guide cycle in a new feature directory. Expand the product-specific scope only through real, separately recorded decisions until its completion rubric passes. **Covers**: REQ-003, REQ-004, REQ-005, REQ-006, REQ-007, REQ-009, REQ-011; NFR-001, NFR-002, NFR-003; Design: External project lead; Per-change CodexSpec record and accepted revision; Application completion rubric and executable checks; Reader guides and CodexSpec entry links.
2. Research and define the bookkeeping product's domain-specific completion rubric, then run each independently scoped feature, bug fix, or refactor through the same repository-local CodexSpec cycle with explicit lead confirmation and acceptance. Its first feature must produce the first runnable bookkeeping workflow and fresh-clone run instructions; no product behavior is built in bootstrap. Include integrity checks suited to stored financial records and verify every accepted revision's guide entry. Continue until the complete product passes its rubric. **Covers**: REQ-003, REQ-004, REQ-005, REQ-006, REQ-007, REQ-009, REQ-011; NFR-001, NFR-002, NFR-003; Design: External project lead; Two isolated application repositories and coding-agent sessions; Per-change CodexSpec record and accepted revision; Application completion rubric and executable checks; Reader guides and CodexSpec entry links.

### Phase 4: Publish and connect the examples

1. Verify both applications from fresh clones, including primary workflows, automated checks, guide links, license, and history-to-directory mapping. Resolve defects as separate scoped requirements when they are standalone fixes, and do not claim completion while a required check fails. **Covers**: REQ-004, REQ-006, REQ-007, REQ-008, REQ-009; NFR-001, NFR-002, NFR-003; Design: Per-change CodexSpec record and accepted revision; Application completion rubric and executable checks; Reader guides and CodexSpec entry links.
2. Create or update the two public GitHub repositories with the verified source, artifacts, immutable revisions, and guides. Check the public URLs, cloneability, and license visibility. **Covers**: REQ-001, REQ-008, REQ-009; NFR-001, NFR-002; Design: Two isolated application repositories and coding-agent sessions; Reader guides and CodexSpec entry links.
3. Add concise entry links and descriptions to the CodexSpec root README variants, synchronize their translations, and run the repository's relevant documentation and CI gates before pushing. Verify the public links after the exact pushed commit's required CI completes. **Covers**: REQ-010; NFR-001; Design: Reader guides and CodexSpec entry links.

## Verification Strategy

- At every `specify` stage, inspect the exact summary and feature directory before the external lead explicitly confirms it. Verify that no requirement record is marked confirmed by silence. **Covers**: REQ-005; Design: External project lead; Two isolated application repositories and coding-agent sessions.
- Verify each project's CodexSpec configuration and a representative interaction, generated artifact, and commit message against its required language. English command templates are not treated as a language failure. **Covers**: REQ-012; Design: Two isolated application repositories and coding-agent sessions.
- For each accepted change, inspect the actual Git diff, CodexSpec artifacts, checks, code review, and guide entry. Follow the link to the immutable revision and run the stated check there. **Covers**: REQ-004, REQ-006, REQ-009; NFR-001, NFR-002; Design: Per-change CodexSpec record and accepted revision; Reader guides and CodexSpec entry links.
- Before publication, run both applications and their primary user workflows from clean clones, inspect persistence and error behavior, and compare the results to the lead's recorded project-specific completion rubrics. **Covers**: REQ-007, REQ-008; NFR-002, NFR-003; Design: Application completion rubric and executable checks.
- For CodexSpec main-repository integration, verify all README variants and public URLs, local quality gates, and required remote CI for the exact pushed commit. **Covers**: REQ-010; NFR-001; Design: Reader guides and CodexSpec entry links.

## Risks and Recovery

| Risk | Impact | Recovery |
| --- | --- | --- |
| A repository-local agent writes into its source checkout after CodexSpec routed the feature to a worktree | Split or invalid development history | Stop the change, inspect returned paths and current Git state, move no caller-owned data implicitly, and resume the same feature identity in its selected worktree |
| A CodexSpec stage or application check fails | Unverified product change | Preserve its artifacts and code, have the lead request a repair and rerun the affected check; do not integrate or publish it as accepted |
| A guide points to an absent revision or a command that does not work at that revision | Readers cannot reproduce the sequence | Correct the guide against the actual immutable revision and verify it from a fresh clone before public linking |
| GitHub publication or CI is unavailable | Public completion cannot be established | Retain local repositories and exact verification evidence; report the incomplete publication and retry only after the external state permits it |

## Requirements Coverage

| Spec requirement | Design component | Plan coverage |
| --- | --- | --- |
| REQ-001 | Two isolated application repositories and coding-agent sessions | Phase 1.1; Phase 4.2 |
| REQ-002 | Two isolated application repositories and coding-agent sessions | Phase 1.1, 1.3; P1 |
| REQ-003 | External project lead; completion rubric | Phase 1.2; Phase 2.1; Phase 3; P1 |
| REQ-004 | Per-change CodexSpec record | Phase 1.2; Phase 2.1–2.2; Phase 3; Phase 4.1; P2, P4 |
| REQ-005 | External project lead; agent sessions | Phase 1.3; Phase 2.1; Phase 3; Verification Strategy |
| REQ-006 | Per-change CodexSpec record | Phase 1.2; Phase 2.2–2.3; Phase 3; Phase 4.1; P2, P4 |
| REQ-007 | Application completion rubric | Phase 1.2; Phase 3; Phase 4.1 |
| REQ-008 | Application repositories; reader guides | Phase 1.1–1.2; Phase 4.1–4.2; P3 |
| REQ-009 | Per-change record; reader guides | Phase 2.2–2.3; Phase 3; Phase 4.1–4.2; P2, P4 |
| REQ-010 | CodexSpec entry links | Phase 4.3; P3 |
| REQ-011 | External lead; agent sessions | Phase 1.3; Phase 2.1; Phase 3 |
| REQ-012 | Two isolated repositories and agent sessions | Phase 1.1; Verification Strategy |
| NFR-001 | Per-change record; reader guides | Phase 2.3; Phase 3; Phase 4; P2–P3 |
| NFR-002 | Completion rubric; reader guides | Phase 2.2–2.3; Phase 3–4; P4 |
| NFR-003 | Completion rubric | Phase 1.2; Phase 3; Phase 4.1 |
