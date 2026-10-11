# Feature Specification: Specs Context Recall

## Context

Feature artifacts under `.codexspec/specs/` retain user-confirmed requirements,
design rationale, and implementation history. Existing project context actively
directs profile consumption, while historical feature recall is uneven: blueprint
explicitly consults related implemented features, and other workflows primarily
resolve the currently selected feature. Profile distillation intentionally leaves
feature-specific rationale in those artifacts. The missing behavior is consistent,
task-relevant use of that history before decisions and questions.

## Goals

Prepare relevant decision history before questioning the user; reuse applicable
knowledge; distinguish continued, supplemented, and changed requirements; and keep
the user's latest explicit decision in control of the current work.

## User Scenarios

- A maintainer discussing a change receives a focused question about a specific
  unresolved difference, instead of having to reconstruct earlier decisions.
- An agent designing, implementing, debugging, or reviewing a feature can explain
  its relevant decision history without treating an old plan as proof of current
  implementation or as a reason to overrule a new user decision.
- An agent continuing an unchanged task reuses sufficient prepared background
  instead of repeating the same search and questions at each workflow stage.

## ADDED Requirements

### REQ-001: Trigger relevant historical recall

**Sources: NEED-001, NEED-003, OUT-001**

Before substantive requirements, behavior, design, debugging, implementation, or
review judgments, the agent must consult relevant history under
`.codexspec/specs/`. This applies in ordinary conversation and SDD workflows,
consistently through Codex and Claude. Sufficient previously prepared background
may be reused under REQ-008. Purely mechanical edits involving none of those
judgments may omit recall.

**Acceptance criteria:**

- A relevant ordinary-development request triggers recall without requiring the
  user to name a specs directory or invoke a dedicated history command.
- A requirements-stage invocation, including specify, quick, or blueprint,
  prepares relevant background before asking questions.
- Formatting or spelling correction alone does not mandate historical retrieval.

### REQ-002: Select related features and reconstruct their timeline

**Sources: NEED-001, NEED-005, DEC-001, DEC-002**

Identify features relevant to the current task, then examine earlier and later
decisions concerning the same matters. Use feature-directory timestamps to
understand the chronology of long-term iteration. Do not stop at the first
matching document when related requirements may have been supplemented or changed.
Read the artifacts needed for that task rather than every historical document.

**Acceptance criteria:**

- Given multiple related features with successive additions and changes, the
  prepared background identifies that evolution and the applicable requirements.
- An unrelated later feature does not replace an earlier requirement on a
  different matter merely because its directory is newer.
- An older unchanged requirement remains part of the applicable background.

### REQ-003: Preserve authority while interpreting decision evolution

**Sources: DEC-001, DEC-002, CON-001**

Confirmed requirements in every historical feature remain authoritative records
of user decisions. Classify related later decisions as continuations, additions,
or explicit changes. Combine additions with earlier requirements; apply a later
explicit change to the same matter while retaining the earlier rationale as
background. Do not weaken authority merely because a requirement is old, or infer
expiration when the relationship is unclear. Open proposals are not confirmed
user decisions.

**Acceptance criteria:**

- A later explicit change updates the requirement on that matter without erasing
  unrelated earlier requirements or the explanation of the earlier choice.
- An unresolved conflict is presented as a specific ambiguity, rather than
  silently selecting one document or assuming the old requirement expired.
- An unconfirmed suggestion does not become an authoritative replacement.

### REQ-004: Honor the current user's explicit decision

**Sources: CON-001, DEC-002**

Historical specs must never overrule or replace the user's latest explicit
decision in the current interaction. Use historical material to explain the
change and identify implications. Do not repeatedly ask the user to decide the
same matter merely because the new decision differs from historical requirements.

**Acceptance criteria:**

- When the user explicitly changes a historical choice, the agent proceeds on the
  new decision and explains relevant consequences without asking for the same
  decision again solely because of the historical difference.

### REQ-005: Turn background into fewer, more precise questions

**Sources: NEED-001, NEED-002, CON-001, CON-002**

Prepare known background, applicable requirements, and differences requiring
confirmation before questioning. Reuse information that history already establishes
and that applies to the task. When applicability or the relationship between
decisions remains materially unclear, explain the known background and ask a
concise question about the specific difference. Do not silently invent a decision
or ask the user to reconstruct available history.

**Acceptance criteria:**

- An applicable established fact eliminates the corresponding redundant question.
- Uncertain continuation of an earlier product choice produces a targeted
  confirmation with background, instead of a broad question from scratch.
- Missing or insufficient historical evidence is not represented as a confirmed
  historical decision; an unresolved material choice is asked explicitly.

### REQ-006: Read to the depth required by the scenario

**Sources: NEED-004, NEED-005**

| Scenario | Required retrieval depth |
|---|---|
| Requirements discussion, specify, quick, blueprint | Related requirements and decision evolution; design rationale when necessary to explain a trade-off; known background, applicable requirements, and remaining differences. |
| Design and planning | Confirmed requirements plus relevant historical designs, alternatives, and trade-offs; implementation plans when implementation experience is relevant. |
| Implementation and debugging | Expected behavior and successive changes, then relevant design, code, and tests to assess actual behavior. Historical plans alone are not proof of implementation. |
| Code review | Requirements and design relevant to concrete changes and concerns, including current-requirement divergence, compatibility implications, and repeated existing problems. |

**Acceptance criteria:**

- Each scenario retrieves enough context for its particular judgment without
  requiring every artifact of every related feature.
- A debugging conclusion about actual behavior is checked against implementation
  evidence rather than derived solely from an intended implementation plan.

### REQ-007: Stop when the current judgment is supported

**Sources: CON-002, NEED-005**

Stop expanding retrieval once the relevant requirements, decision evolution, and
applicability are sufficiently understood to support the current judgment. Do not
extend into unrelated history. If a material ambiguity remains, present the
specific difference in a concise question instead of silently choosing an
interpretation or treating the background as complete.

**Acceptance criteria:**

- Sufficient background ends retrieval without an exhaustive historical scan.
- An unresolved material relationship between decisions produces a targeted
  clarification, not an unsupported claim of certainty.

### REQ-008: Reuse and supplement prepared background

**Sources: CON-003, CON-002**

Reuse already assembled background instead of rescanning at every workflow stage.
Supplement retrieval when task scope changes, new evidence appears, or existing
background is insufficient for the required judgment. Reuse must not disguise
incomplete context as sufficient knowledge.

**Acceptance criteria:**

- Transitioning to another stage without changed needs reuses sufficient history.
- A new requirement, contradictory evidence, or a previously unsupported judgment
  triggers appropriate additional retrieval.

## Quality Constraints

### NFR-001: Consistent coverage and bounded retrieval

**Sources: NEED-003, NEED-005, CON-002, CON-003, OUT-001**

Codex and Claude must receive equivalent recall behavior. Retrieval depth follows
the task and sufficiency rules, without requiring full-history loading or repeated
scans solely because a workflow stage changes. Mechanical-edit exemption must
not remove recall from substantive judgments.

## Expected Boundary Behavior

- No relevant history, missing artifacts, or unclear decision relationships cannot
  manufacture authority. Preserve what is known and ask only remaining material
  questions under REQ-005 and REQ-007.
- A historical plan disagreeing with current code is evidence to investigate,
  not proof that the plan was implemented or that the user changed a requirement.
- A latest explicit user decision is applied under REQ-004 even when the historical
  design favors a different choice.

## Out of Scope

**Sources: OUT-001**

Mandatory recall for purely mechanical changes that involve no substantive
requirement, behavior, design, debugging, implementation, or review judgment.

## Assumptions and Open Questions

No additional product assumptions are required. OPEN-001 and OPEN-002 in
`requirements.md` are resolved. No blocking product questions remain.

## Requirements Traceability

| Confirmed Entry | Spec Coverage |
|---|---|
| NEED-001 | REQ-001, REQ-002, REQ-005 |
| NEED-002 | REQ-005 |
| NEED-003 | REQ-001, NFR-001 |
| NEED-004 | REQ-006 |
| NEED-005 | REQ-002, REQ-006, REQ-007, NFR-001 |
| CON-001 | REQ-003, REQ-004, REQ-005 |
| CON-002 | REQ-005, REQ-007, REQ-008, NFR-001 |
| CON-003 | REQ-008, NFR-001 |
| DEC-001 | REQ-002, REQ-003 |
| DEC-002 | REQ-002, REQ-003, REQ-004 |
| OUT-001 | REQ-001, NFR-001, Out of Scope |
