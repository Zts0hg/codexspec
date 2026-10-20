# Design Document: Two CodexSpec Example Applications

**Related Spec**: [spec.md](spec.md)
**Confirmed Requirements**: [requirements.md](requirements.md)
**Created**: 2026-10-17
**Status**: Draft

## Context

The CodexSpec repository needs two independent, usable example applications whose real development history teaches readers how separate requirements become successive product changes. The Todo List and personal bookkeeping applications are independent products. This design defines their shared development and publication structure. Each application receives its own product architecture and detailed feature requirements through its own CodexSpec workflow; this document does not prewrite those histories.

The external project lead owns product decisions and acceptance. A separate coding agent operates inside each application repository. The original user has delegated feature-level decisions and repository-local `specify` summary confirmations to the external lead.

## Architecture & Components

### External project lead

- **Responsibility**: Research each product domain, define a coherent final product scope and completion criteria, choose independently scoped changes, supply requirements to the relevant coding agent, explicitly confirm `specify` summaries, inspect code and verification, and accept or send back work. The lead owns publication decisions and resolves product ambiguities without transferring feature choices to the original user.
- **Interface**: A change brief and acceptance decision sent to the repository-local agent; a reviewed stage summary, implementation report, test evidence, and published revision received from it.
- **Covers**: REQ-003, REQ-005, REQ-007, REQ-011; NFR-003.

### Two isolated application repositories and coding-agent sessions

- **Responsibility**: One public Git repository holds the Todo List; another holds the personal bookkeeping tool. Each has its own CodexSpec initialization, constitution, source, tests, README, license, Git history, and repository-local coding-agent session. Todo List initializes with `language.output: en`; bookkeeping initializes with `language.output: zh-CN`. In both repositories, interaction, document, and commit languages follow that base through the existing fallback; command templates remain English. The agent uses CodexSpec skills within its selected repository and follows any returned feature worktree for that change.
- **Interface**: The lead provides one independent change brief at a time. The agent reports the feature directory and stage summary, waits for the lead's explicit confirmation, then produces artifacts and implementation evidence. Repository and worktree paths are explicit in subsequent instructions.
- **Covers**: REQ-001, REQ-002, REQ-003, REQ-004, REQ-005, REQ-008, REQ-011, REQ-012.

### Per-change CodexSpec record and accepted revision

- **Responsibility**: Every independently scoped feature, bug fix, or refactor owns a complete-name `.codexspec/specs/<feature-id>-<feature-name>/` directory and a traceable Git revision. The directory retains the genuine requirements, specification, design, plans, tasks, reviews, and verification artifacts that the chosen CodexSpec path actually produced. The revision identifies the accepted code state for that change; later changes have their own records and revisions.
- **Interface**: Stable project-relative feature path plus a commit SHA or immutable tag that the guide can link to. The repository-local agent's confirmation and acceptance evidence remains in the authentic record or its associated review history.
- **Covers**: REQ-004, REQ-005, REQ-006, REQ-009; NFR-001.

### Application completion rubric and executable checks

- **Responsibility**: Each repository records its lead-approved product scope and acceptance criteria. These cover primary workflows, error behavior, persistence and data integrity where relevant, tests, and fresh-clone setup. The lead checks the running product and test evidence before declaring it complete.
- **Interface**: Product roadmap or blueprint, per-change acceptance criteria, automated checks, and a final release verification record maintained within the application repository.
- **Covers**: REQ-003, REQ-007, REQ-008; NFR-002, NFR-003.

### Reader guides and CodexSpec entry links

- **Responsibility**: Each application repository has a chronological guide whose entries link an independent change to its feature directory, accepted revision, and runnable verification instructions. The CodexSpec repository's user-facing README entry links to both public repositories after their URLs and guides work. The documentation site may also link to them, but README entry links satisfy the confirmed main-repository requirement.
- **Interface**: Public GitHub URLs for each repository, stable relative paths and commit links within each guide, and run instructions checked against the linked revisions.
- **Covers**: REQ-008, REQ-009, REQ-010; NFR-001, NFR-002.

## Key Design Decisions

### D1: Keep product leadership outside each repository-local agent

- **Context**: The user delegated all feature decisions and summary confirmations to the lead while requiring real coding-agent use in each independent repository.
- **Decision**: Run a separate Codex CLI agent session rooted in each repository. The lead communicates as the external product owner and engineer, sending normal requirements and review feedback. A persistent tmux session is the preferred local transport because it supports the explicit back-and-forth needed by `codexspec:specify`; the transport is replaceable if another session mechanism preserves the same role and worktree boundaries. The agent is neither asked to determine nor told to rely on the lead's human identity.
- **Alternatives**: Having the external lead directly write all product code would not produce the requested repository-local coding-agent workflow. A one-shot, noninteractive process per change is possible but makes stage-summary confirmation and correction less direct.
- **Trade-offs**: Persistent sessions require monitoring and explicit tracking of which repository and feature worktree each agent is using.
- **Covers**: REQ-002, REQ-003, REQ-005, REQ-011.

### D2: Separate real product changes, then link accepted snapshots

- **Context**: Readers must be able to trace a real sequence of work; unrelated changes cannot share one requirement record for convenience.
- **Decision**: Treat each independently scoped feature, bug fix, or refactor as a separate CodexSpec feature directory. Keep its genuine artifacts and code revision in the same application's Git history. The guide uses immutable commit SHAs or tags for accepted snapshots rather than a moving branch head. Changes discovered during implementation that are part of the same accepted feature remain in that feature's review and repair cycle; a separately scoped product change gets a new directory.
- **Alternatives**: One umbrella requirements directory per application would hide the change-level decisions and violate the required granularity.
- **Trade-offs**: More directories and commits increase maintenance, but they are the evidence the examples are intended to show.
- **Covers**: REQ-004, REQ-006, REQ-009; NFR-001.

### D3: Define maturity in each application rather than in this orchestration feature

- **Context**: The products have different core workflows and risks, particularly around bookkeeping data. The user delegated their detailed feature choices to the lead.
- **Decision**: Before accepting either product as complete, the lead maintains a project-specific target capability set and verification rubric in that application repository, revises it through genuine independent requirements when needed, and validates the running application. This orchestration design sets the handoff and evidence contract, not a substitute feature list for either application.
- **Alternatives**: A shared generic checklist would be too weak to establish whether both distinct applications are usable; prescribing all detailed product behavior here would erase the intended repository-local requirements history.
- **Trade-offs**: Completion is evaluated separately per project, so both repositories need explicit, reviewable acceptance evidence.
- **Covers**: REQ-003, REQ-007; NFR-002, NFR-003.

### D4: Link public examples from existing CodexSpec documentation surfaces

- **Context**: Readers start at the CodexSpec repository, while the complete code and histories live in two other repositories.
- **Decision**: Put concise links and descriptions in CodexSpec's user-facing root README variants after both repositories are public and verified. Keep detailed chronological guides in the application repositories. No CodexSpec runtime or command-template change is required to make the examples discoverable.
- **Alternatives**: Copying each guide into the CodexSpec repository would create duplicate histories that could drift from the live application repositories.
- **Trade-offs**: The main repository depends on external URLs, which must be checked when published and maintained if repository names change.
- **Covers**: REQ-008, REQ-009, REQ-010; NFR-001.

## Interfaces and Traceability

The lead-to-agent contract is one change at a time: a concrete change brief enters the repository-local CodexSpec `specify` workflow; the agent returns a final summary and feature path; the lead explicitly confirms or corrects it; the agent then advances through the configured CodexSpec stages, implementation, checks, and review. A failed stage retains its actual state for correction. The lead's approval applies to the specific summary it reviewed, not to later unreviewed changes. **Covers**: REQ-003, REQ-004, REQ-005, REQ-006, REQ-011.

A guide entry identifies the change title and type, its feature directory, the accepted Git revision, and commands or user actions that verify that revision. Relative artifact links and immutable revision links must resolve in the published repository. **Covers**: REQ-006, REQ-009; NFR-001, NFR-002.

## Risks and Trade-offs

| Risk | Impact | Design response | Covers |
| --- | --- | --- | --- |
| A coding-agent session continues from the wrong repository or worktree | Artifacts and code split between checkouts | Keep one session per repository and require the returned absolute feature workspace in subsequent operations | REQ-002, REQ-004, REQ-005 |
| A guide is written after the fact with links to moving branches | Readers cannot reproduce the real development state | Generate entries from actual directories and accepted immutable revisions; verify links and stage instructions before publication | REQ-006, REQ-009; NFR-001, NFR-002 |
| A product is published when only the teaching workflow is demonstrated | The example is a partial application, contrary to the user's objective | Require project-specific primary-workflow and quality acceptance evidence before calling it complete | REQ-007; NFR-003 |

## Requirements Coverage

| Spec requirement | Design coverage |
| --- | --- |
| REQ-001 | Two isolated application repositories |
| REQ-002 | Two isolated repositories and agent sessions; D1 |
| REQ-003 | External project lead; completion rubric; D1, D3 |
| REQ-004 | Per-change record; D2; lead-to-agent interface |
| REQ-005 | External lead; agent sessions; lead-to-agent interface |
| REQ-006 | Per-change record; D2; guide interface |
| REQ-007 | Completion rubric; D3 |
| REQ-008 | Application repositories; reader guides and entry links; D4 |
| REQ-009 | Per-change record; reader guides; D2, D4 |
| REQ-010 | CodexSpec entry links; D4 |
| REQ-011 | External lead; agent sessions; D1 |
| REQ-012 | Two isolated repositories and agent sessions; project-specific CodexSpec initialization |
| NFR-001 | Per-change record; reader guides; D2, D4 |
| NFR-002 | Completion rubric; reader guides; D3 |
| NFR-003 | Completion rubric; D3 |
