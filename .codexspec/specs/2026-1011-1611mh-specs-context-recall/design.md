# Design: Specs Context Recall

**Related Spec**: [spec.md](spec.md)
**Confirmed Requirements**: [requirements.md](requirements.md)
**Created**: 2026-10-11
**Status**: Designed

## Context

The consumer of feature history is the agent. Existing installation already
delivers bounded profile and commit instructions in CLAUDE.md and AGENTS.md, and
emits commit guidance from the Claude plugin SessionStart hook. This design extends
those delivery mechanisms with task-dependent historical recall instructions.
It does not turn a date sorter into a decision interpreter: the agent reads user
decisions and their relationships in the original feature artifacts.

## Architecture & Components

### C1: Shared historical-recall guidance

- **Responsibility**: `src/codexspec/specs_context.py` owns the channel-neutral
  `render_specs_context()` block and `inject_specs_context(path)` installation
  function. Dedicated `CODEXSPEC SPECS START/END` markers bound its content.
- **Interface**: The rendered text defines substantive-work triggers, selecting
  related features, requirements chronology, authority, scenario depth, targeted
  questioning, stopping, and background reuse. The injector replaces its own
  block idempotently while preserving project-authored surrounding text.
- **Covers**: REQ-001 through REQ-008; NFR-001.

### C2: Installed context and plugin delivery

- **Responsibility**: Claude initialization in `src/codexspec/__init__.py` and
  Codex context setup in `src/codexspec/integrations/codex.py` call C1 alongside
  the existing managed blocks. The existing plugin hook installer in
  `src/codexspec/commit_guidance.py` emits both unchanged commit guidance and C1
  guidance using one composed output.
- **Interface**: Preserve `render_commit_guidance()` output and the existing
  hook installation entry point. Add a composition renderer for the combined
  plugin context. Retain the current exec-form Git/printf delivery, quoting and
  linked-destination checks; no CodexSpec CLI is needed when the hook executes.
- **Covers**: REQ-001, REQ-002, REQ-003, REQ-004, REQ-005, REQ-006, REQ-007,
  REQ-008; NFR-001.

### C3: Workflow-stage reminders

- **Responsibility**: A short literal fragment
  `internal/command_templates/fragments/specs-recall.md` reminds substantive
  commands to use the shared historical-recall rules in the selected repository.
  It distinguishes background from the current feature's confirmed authority and
  preserves the command's existing target and write boundaries.
- **Interface**: Include the fragment after workspace routing in specify, quick,
  blueprint, generate-spec, spec-to-design, design-to-plan, plan-to-tasks,
  implement-tasks, debug, review-spec, review-design, review-plan, review-tasks,
  review-code, and analyze sources. The detailed policy stays in C1. Other
  substantive work receives the ambient C1 trigger without changing unrelated
  commands' input contracts, such as optional PR spec integration.
- **Covers**: REQ-001, REQ-004, REQ-005, REQ-006, REQ-008; NFR-001.

### C4: Distribution and verification

- **Responsibility**: Existing maintainer rendering and `codexspec init` produce
  complete templates, installed skills/commands, context blocks and plugin hooks.
  Runtime delivery never interprets internal fragment directives.
- **Interface**: Tests exercise fresh and repeated installation, preservation of
  authored content, channel equivalence, plugin execution without a CLI, and
  packaged delivery. Semantic scenario fixtures describe expected judgments and
  forbidden interpretations independently of renderer string equality.
- **Covers**: REQ-001 through REQ-008; NFR-001.

## Key Design Decisions

### D1: Deliver an active pointer and instructions, not an eager history dump

- **Context**: Relevance, sufficiency, and meaning of a later user decision depend
  on the current task. The agent already has file-search and read capabilities.
- **Decision**: Ship a fixed guidance block directing the agent to inspect
  `.codexspec/specs/` as needed. No new retrieval CLI, persisted central index,
  automatic document rewrite, or semantic-ranking service is necessary.
- **Alternatives**: Embedding all specs in startup context would violate bounded
  retrieval; a new retrieval service would add infrastructure without resolving
  the agent's required interpretation of user intent.
- **Trade-offs**: Tests can establish delivery and policy coverage, but cannot
  promise that every LLM execution follows the instructions. Behavioral observations
  must be distinguished from static contract tests.
- **Covers**: REQ-001, REQ-002, REQ-007, REQ-008; NFR-001.

### D2: Retain original decision evidence and reconstruct relationships

- **Context**: Requirements are authoritative user records along a long-term
  timeline. A later document can supplement, change, or concern a different matter.
- **Decision**: Select by task concepts and affected areas; inspect related
  requirements and their confirmation/replacement information in directory time
  order. Follow relevant earlier and later references, without stopping at the
  first match. Explicit recorded revisions within an older directory also count
  as decisions; do not discard them merely because the directory was created
  earlier. If a material relationship cannot be established, ask about it.
- **Alternatives**: Filename-only newest-wins and oldest-wins both lose confirmed
  relationships; treating current implementation as proof of a user decision
  confuses actual behavior with confirmed intent.
- **Trade-offs**: Some conflicts require a targeted user question. Historical
  plans can explain intended implementation but cannot prove implementation.
- **Covers**: REQ-002, REQ-003, REQ-005, REQ-006.

### D3: Preserve workflow authority while using background

- **Context**: Generators, implementers, and reviewers already have selected
  feature authority and target boundaries. Recall must not silently redefine them.
- **Decision**: The latest explicit user decision overrides historical specs.
  Explain implications without repeatedly seeking the same decision. Reflect a
  changed requirement through the owning requirements workflow before downstream
  artifacts rely on it. Historical background does not silently edit the current
  baseline, broaden a review target, or override a command's staged-input contract.
  Reviewer conclusions must concern the selected change and current requirements.
- **Alternatives**: Treating every historical constraint as a new downstream gate
  would invalidate the user's confirmed changes and multiply questions.
- **Trade-offs**: Background is reused, but scope changes or new evidence can
  require further reading. A workflow may need its existing upstream-update
  handoff; this does not authorize re-questioning an explicit decision.
- **Covers**: REQ-004, REQ-005, REQ-006, REQ-008.

### D4: Reuse bounded managed blocks and the existing plugin hook

- **Context**: The repository has established non-destructive context injection,
  plugin startup delivery, and complete-template distribution mechanisms.
- **Decision**: Use a separate specs block for init; compose the same text into
  the existing startup hook alongside commit guidance. Keep all source changes in
  the maintained source paths and regenerate derived files through normal tools.
- **Trade-offs**: Context and plugin guidance can both be present; the policy must
  explicitly reuse prepared background instead of causing duplicate searches.
- **Covers**: REQ-001, REQ-008; NFR-001.

## Verification Scenarios

Delivery tests and scenario reasoning answer different questions. Verify emitted
instructions at all entry points, and separately inspect these representative
decision cases against the installed policy:

1. An older confirmed requirement remains unchanged while a later unrelated
   feature exists: retain it without a redundant question.
2. A later related feature adds a constraint: combine both requirements.
3. A later explicit decision changes one behavior: apply that change and retain
   earlier unrelated requirements and rationale.
4. A current user explicitly reverses the historical choice: obey the new
   decision without asking it again.
5. Two records have an unclear relationship: ask one question describing the
   exact difference; do not infer expiration.
6. A debugging task finds a plan contradicted by code: distinguish intent and
   implementation before concluding whether a defect or requirement change exists.
7. Sufficient background survives a stage transition: reuse it; new scope or
   contradictory evidence prompts additional retrieval.
8. Mechanical edit, empty history, or incomplete historical artifacts: do not
   fabricate authority or perform unrelated exhaustive reading.

These scenarios cover REQ-001 through REQ-008 and NFR-001. Record precisely whether
validation was structural, direct scenario reasoning, or an actual agent execution.

## Requirements Coverage

| Spec Requirement | Design Coverage |
|---|---|
| REQ-001 | C1, C2, C3, C4; D1, D4 |
| REQ-002 | C1, C2, C4; D1, D2 |
| REQ-003 | C1, C2, C4; D2 |
| REQ-004 | C1, C2, C3, C4; D3 |
| REQ-005 | C1, C2, C3, C4; D2, D3 |
| REQ-006 | C1, C2, C3, C4; D2, D3 |
| REQ-007 | C1, C2, C4; D1 |
| REQ-008 | C1, C2, C3, C4; D1, D3, D4 |
| NFR-001 | C1, C2, C3, C4; D1, D4 |
