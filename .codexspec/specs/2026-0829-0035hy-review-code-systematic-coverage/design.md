# Design Document: Systematic Review Coverage

**Related Spec**: `.codexspec/specs/2026-0829-0035hy-review-code-systematic-coverage/spec.md`
**Confirmed Requirements**: `.codexspec/specs/2026-0829-0035hy-review-code-systematic-coverage/requirements.md`
**Created**: 2026-08-29
**Status**: Draft

## Context

`review-code` is distributed as one command template and rendered for Claude Code and Codex. Its
defect-gate branch currently coordinates four mandatory passes and emits a schema-v1 result. The
Git review-context resolver independently provides deterministic target selection. The
`implement-tasks` template consumes the result and owns all repair mutations.

The new design keeps those ownership boundaries. It adds one explicit system-contract pass,
requires each validated defect to trigger a bounded search for related occurrences, and replaces
the result envelope with schema v2 so coverage and repair follow-up can be validated by callers.
No persistent review state or project-specific behavior is introduced.

## Architecture & Components

### Distributed Review Command

- **Responsibility**: Define defect-gate mode, coordinate the five mandatory passes, preserve audit
  mode, and emit the human report plus exactly one schema-v2 result envelope.
- **Interface**: `templates/commands/review-code.md`; existing selectors and modifiers remain
  unchanged. The command receives the validated resolver manifest, selected raw evidence, project
  authority, optional neutral prior obligations from its caller, and read-only reviewer tools.
- **Covers**: REQ-001 through REQ-021; NFR-001 through NFR-005

### System Contract Mapper

- **Responsibility**: Derive only the system-wide consistency rules and cross-module contracts
  implicated by the selected change, then map their sources, producers, propagation boundaries,
  consumers, entry surfaces, and relevant scenarios.
- **Interface**: A mandatory System Contract Pass between Scope and Behavior. It consumes confirmed
  requirements when available, project instructions, public compatibility boundaries, semantic
  change evidence, dependencies, and verified repository facts. It produces `contracts` records in
  schema v2.
- **Covers**: REQ-002 through REQ-006; NFR-002, NFR-003, NFR-005

### Review Partition Coordinator

- **Responsibility**: Partition large or disjoint review work by behavior or contract rather than
  file extension, assign each partition to the primary reviewer or a required specialist, and
  ensure every partition reaches a terminal state even after a finding is admitted.
- **Interface**: Produces `partitions` records with stable review-local IDs, scope, owner, contract
  references, and completion state. A file inventory remains a separate completeness control and
  cannot satisfy a behavior partition by itself.
- **Covers**: REQ-005 through REQ-007, REQ-017, REQ-018

### Root-Cause Variant Analyzer

- **Responsibility**: For each validated finding with a potentially repeatable cause, identify the
  cause, derive a bounded semantic search scope, inspect equivalent occurrences, and return all
  qualifying findings before the review result is finalized.
- **Interface**: Runs inside the Verification Pass after a candidate finding is validated. Each
  completed search produces a `variant_searches` record. Newly discovered candidates return to
  finding validation; the loop ends only when no new qualifying occurrence remains in the bounded
  scope.
- **Covers**: REQ-007 through REQ-010; NFR-003, NFR-005

### Schema-v2 Result and Handoff

- **Responsibility**: Make findings, target identity, contract coverage, partition completion,
  related-defect searches, and repair follow-up machine-validatable without writing repository
  state.
- **Interface**: One `<review-code-result>` JSON object with `schema_version: "2"`. Existing result
  data remains, while new required `findings`, `review_coverage`, and `follow_up` structures carry
  the additional evidence. The target includes a deterministic fingerprint of the exact selected
  raw evidence.
- **Covers**: REQ-011 through REQ-18; NFR-001, NFR-004, NFR-005

### Repair-Loop Consumer

- **Responsibility**: Validate schema v2, independently reproduce findings, retain only neutral
  coverage and follow-up obligations, perform safe repairs, and supply applicable obligations to a
  fresh complete review of the updated target.
- **Interface**: `templates/commands/implement-tasks.md`. It rejects schema v1 and malformed schema
  v2, preserves the current progress guards, and never supplies implementation reasoning or prior
  correctness conclusions to the next reviewer.
- **Covers**: REQ-013 through REQ-18; NFR-001, NFR-004

### Contract and Behavioral Evaluation

- **Responsibility**: Lock the distributed prompt contract, result parser, repair-loop behavior,
  and source-independent review outcomes.
- **Interface**: Existing template tests, workflow-template tests, and review-code evaluation
  runner, extended with schema-v2 fixtures and cases for multi-surface contracts, multiple related
  defects, continued review after an early finding, incomplete coverage, neutral repair handoff,
  schema-v1 rejection, and clean PASS behavior.
- **Covers**: REQ-022; NFR-002, NFR-004

## Key Design Decisions

### Decision 1: Add a System Contract Pass without replacing existing safety passes

- **Context**: Contract discovery must occur before behavior inspection, while existing Scope,
  Behavior, Risk, and Verification protections remain required.
- **Decision**: Defect-gate mode uses five ordered passes: Scope, System Contract, Behavior, Risk,
  and Verification. Verification includes finding validation, bounded root-cause variant searches,
  validation of newly discovered candidates, and final completion checks.
- **Alternatives**: Hide contract mapping inside Scope; add separate Variant and Completion passes;
  replace the existing risk model.
- **Trade-offs**: One new explicit pass changes existing template contracts but makes the missing
  responsibility visible without duplicating candidate validation or weakening established passes.
- **Covers**: REQ-002, REQ-007 through REQ-010, REQ-015, REQ-021

### Decision 2: Track behavior coverage separately from file inventory

- **Context**: Inventory disposition proves that evidence was accounted for but cannot prove an
  end-to-end behavior was traced.
- **Decision**: Keep the current inventory and add contract and behavior partitions as separate,
  linked coverage records. PASS requires both forms of coverage to be complete.
- **Alternatives**: Add more meanings to the existing `reviewed` disposition; replace inventory
  with behavior partitions.
- **Trade-offs**: The result grows, but file completeness and behavior completeness remain
  independently understandable and machine-validatable.
- **Covers**: REQ-003, REQ-005, REQ-006, REQ-017, REQ-018

### Decision 3: Use a bounded iterative search for related defects

- **Context**: A validated finding may reveal equivalent defects, but an unrestricted repository
  search would turn change review into a whole-codebase audit.
- **Decision**: Derive the sibling scope from the validated cause and selected change: equivalent
  constructors, callers, implementations, adapters, entry surfaces, and symmetric paths that can
  violate the same contract. Record the search method and checked scope. Validate newly found
  candidates and repeat only within that bounded scope.
- **Alternatives**: Report only the first occurrence; always grep the whole repository; defer
  related searching to the repairer.
- **Trade-offs**: The reviewer performs more work after the first finding, but the work is bounded
  by semantic equivalence and reduces repeated review rounds.
- **Covers**: REQ-008 through REQ-010; NFR-003

### Decision 4: Make schema v2 strict and self-contained

- **Context**: Optional schema-v1 additions could be ignored by existing callers and would not
  enforce review completion.
- **Decision**: Schema v2 requires all new structures and standardized finding IDs. Unknown,
  missing, malformed, or contradictory fields are `INCONCLUSIVE`. The Git resolver manifest keeps
  its independent schema.
- **Alternatives**: Optional v1 fields; human-report-only coverage; automatic migration of v1
  results.
- **Trade-offs**: Callers must migrate atomically, but incompatible results fail explicitly rather
  than silently losing coverage evidence.
- **Covers**: REQ-011, REQ-012, REQ-016, REQ-018, REQ-019; NFR-004

### Decision 5: Keep repair handoff caller-owned and neutral

- **Context**: Review state must survive repair rounds without mutating the reviewed repository or
  biasing the next reviewer.
- **Decision**: The result carries outgoing objective obligations. The caller retains only those
  neutral obligation records and supplies them as incoming obligations to the next review; it does
  not transmit completed prior coverage or variant-search records. The fresh reviewer sees the
  behavior or evidence to re-establish, original target fingerprint, and source IDs, but not
  implementation reasoning, prior evidence/status fields, root-cause conclusions, or a prior
  correctness conclusion.
- **Alternatives**: Repository-local review files; no handoff; sending the entire prior report and
  repair narrative to the next reviewer.
- **Trade-offs**: Cross-session persistence remains the caller's responsibility, but review-code
  stays read-only and isolation remains meaningful.
- **Covers**: REQ-013 through REQ-016; NFR-001

### Decision 6: Keep the human report at six sections

- **Context**: Existing consumers and users recognize the six-section defect report, while the
  additional evidence primarily needs machine-readable structure.
- **Decision**: Retain Verdict, Scope, Findings, Requirements Coverage, Verification Summary, and
  Coverage Gaps. Scope summarizes contract and partition coverage; Findings reports finding IDs and
  related-defect search results; the envelope carries the complete structures.
- **Alternatives**: Add separate Contract Coverage and Repair Handoff sections; report only JSON.
- **Trade-offs**: The prose stays compact, while readers needing full detail use the envelope.
- **Covers**: REQ-011, REQ-012, NFR-005

## Data Models / Key Entities

### Schema-v2 Result Envelope

The exact JSON member order is not significant. Every listed member is required unless explicitly
marked nullable. Empty arrays are valid only when the corresponding work is not applicable.

| Entity | Field | Type | Constraints | Covers |
|---|---|---|---|---|
| Result | `schema_version` | string | Exact value `"2"` | REQ-011 |
| Result | `mode` | string | Exact value `"defect"` | REQ-011 |
| Result | `verdict` | enum | `PASS`, `FAIL`, `INCONCLUSIVE` | REQ-017, REQ-018 |
| Target | `fingerprint` | string | Non-empty deterministic digest of exact selected raw evidence | REQ-012, REQ-014 |
| Finding | `id` | string | Unique and stable within the direct repair handoff | REQ-012, REQ-013 |
| Finding | `priority` | enum | `P0`, `P1`, `P2`, `P3` | REQ-012 |
| Finding | `location` | string | Shortest useful selected-change location | REQ-012 |
| Finding | `summary` | string | Concrete defect title | REQ-012, NFR-005 |
| Finding | `trigger` | string | Reproducible condition that reaches the defect | REQ-012 |
| Finding | `impact` | string | Concrete correctness, security, reliability, performance, or compatibility effect | REQ-012 |
| Finding | `root_cause_id` | string or null | Links repeatable findings to one variant search | REQ-008, REQ-012 |
| Contract | `id` | string | Unique within result and handoff | REQ-003 |
| Contract | `statement` | string | Plain-language consistency rule | REQ-003, NFR-005 |
| Contract | `sources` | array[string] | Authority or evidence references; non-empty | REQ-003, REQ-004 |
| Contract | `producers` | array[string] | Applicable source boundaries | REQ-003 |
| Contract | `propagation` | array[string] | Applicable transfer boundaries | REQ-003 |
| Contract | `consumers` | array[string] | Applicable final-use boundaries | REQ-003 |
| Contract | `entry_surfaces` | array[string] | Applicable public or runtime entries | REQ-003 |
| Contract | `scenarios` | array[string] | Relevant normal, failure, denial, boundary, cancellation, or compatibility scenarios | REQ-003 |
| Contract | `evidence` | array[string] | Concrete trace or deterministic-check references supporting the status | REQ-003, REQ-017 |
| Contract | `status` | enum | `complete`, `incomplete`, `not_applicable` | REQ-003, REQ-018 |
| Partition | `id` | string | Unique within result | REQ-005 |
| Partition | `scope` | string | Behavior or contract scope, not an extension filter | REQ-005 |
| Partition | `owner` | string | `primary` or `specialist:<activated-profile>` | REQ-005 |
| Partition | `contract_ids` | array[string] | Existing contract references | REQ-005 |
| Partition | `evidence` | array[string] | Reviewed call chains, scenarios, or check references | REQ-005, REQ-017 |
| Partition | `status` | enum | `complete`, `incomplete`, `failed`, `uninspectable` | REQ-005, REQ-018 |
| VariantSearch | `root_cause_id` | string | Unique within result | REQ-008 |
| VariantSearch | `finding_ids` | array[string] | Existing finding references | REQ-008 |
| VariantSearch | `cause` | string | Concrete validated root cause | REQ-008, NFR-005 |
| VariantSearch | `scope` | array[string] | Bounded equivalent surfaces checked | REQ-008, REQ-009 |
| VariantSearch | `methods` | array[string] | Search or trace methods used | REQ-008 |
| VariantSearch | `checked_locations` | array[string] | Locations inspected inside the bounded scope | REQ-008, REQ-009 |
| VariantSearch | `evidence` | array[string] | Search outputs or call-chain references supporting completion | REQ-008, REQ-010 |
| VariantSearch | `reason` | string or null | Required when status is `not_applicable` or `incomplete` | REQ-009, REQ-010 |
| VariantSearch | `status` | enum | `complete`, `incomplete`, `not_applicable` | REQ-008 through REQ-010 |
| FollowUp | `id` | string | Stable within the direct repair handoff | REQ-013 |
| FollowUp | `origin_fingerprint` | string | Fingerprint of the result that created it | REQ-013, REQ-014 |
| FollowUp | `source_ids` | array[string] | Finding or contract IDs | REQ-013 |
| FollowUp | `statement` | string | Objective behavior or evidence to re-establish | REQ-013, NFR-005 |
| FollowUp | `status` | enum | Incoming: `verified`, `unresolved`, `superseded`; outgoing: `open` | REQ-013 through REQ-016 |
| FollowUp | `evidence` | array[string] | Required for `verified` or `superseded` | REQ-013, REQ-014 |
| CoverageGap | `id` | string | Unique within result | REQ-018 |
| CoverageGap | `scope` | string | Missing contract, partition, search, reviewer, or verification evidence | REQ-018 |
| CoverageGap | `impact` | string | Effect on review confidence or completion | REQ-018, NFR-005 |
| CoverageGap | `blocking` | boolean | Must agree with verdict and completion rules | REQ-017, REQ-018 |

The top-level schema keeps the existing `target`, `requirements_coverage`, `verification`,
`finding_counts`, `coverage_gap_count`, `review_context`, and `reviewers` members. It adds required
`findings`, `review_coverage`, `follow_up`, and `coverage_gaps` members:

```json
{
  "schema_version": "2",
  "mode": "defect",
  "verdict": "FAIL",
  "target": {
    "selector": "default",
    "fingerprint": "git-object-digest",
    "inventory_count": 3
  },
  "requirements_coverage": {"status": "complete", "feature": "..."},
  "verification": {"status": "complete", "commands": []},
  "findings": [
    {
      "id": "F-001",
      "priority": "P2",
      "location": "src/adapter.py:42",
      "summary": "One adapter drops the resolved policy",
      "trigger": "Resolve a policy through the secondary adapter",
      "impact": "The consumer runs with a different policy than the selected configuration",
      "root_cause_id": "RC-001"
    }
  ],
  "finding_counts": {"P0": 0, "P1": 0, "P2": 1, "P3": 0},
  "review_coverage": {
    "contracts": [
      {
        "id": "C-001",
        "statement": "Every adapter preserves the resolved policy",
        "sources": ["public configuration contract"],
        "producers": ["policy resolver"],
        "propagation": ["adapter constructors"],
        "consumers": ["runtime consumer"],
        "entry_surfaces": ["primary entry", "secondary entry"],
        "scenarios": ["normal", "invalid policy"],
        "evidence": ["constructor and consumer call-chain trace"],
        "status": "complete"
      }
    ],
    "partitions": [
      {
        "id": "P-001",
        "scope": "policy resolution and propagation",
        "owner": "primary",
        "contract_ids": ["C-001"],
        "evidence": ["both entry call chains inspected"],
        "status": "complete"
      }
    ],
    "variant_searches": [
      {
        "root_cause_id": "RC-001",
        "finding_ids": ["F-001"],
        "cause": "one adapter reconstructs rather than propagates the resolved value",
        "scope": ["all selected-change adapter constructors"],
        "methods": ["constructor call-site search", "entry-to-consumer trace"],
        "checked_locations": ["src/adapter.py:20", "src/adapter.py:42"],
        "evidence": ["all adapter constructor call sites accounted for"],
        "reason": null,
        "status": "complete"
      }
    ]
  },
  "follow_up": {
    "received": [],
    "required": [
      {
        "id": "FU-001",
        "origin_fingerprint": "git-object-digest",
        "source_ids": ["F-001", "C-001"],
        "statement": "Verify every adapter preserves the resolved policy",
        "status": "open",
        "evidence": []
      }
    ]
  },
  "coverage_gaps": [],
  "coverage_gap_count": 0,
  "review_context": "isolated",
  "reviewers": {"primary": "complete", "specialists": []}
}
```

Schema validation requires unique IDs within each entity type and valid cross-references. Outgoing
`follow_up.required.source_ids` resolve in the current result; incoming
`follow_up.received.source_ids` resolve in the retained originating schema-v2 result identified by
`origin_fingerprint`, because a repaired finding is not repeated in the current `findings` array.
The caller performs that originating-result validation before passing only the neutral obligation
to a fresh reviewer. Root-cause searches reference exactly the findings linked to that cause;
outgoing obligations cover every current finding and use the current target fingerprint. Target
members retain their schema-v1 types plus the v2 fingerprint, target emptiness agrees with inventory
count, and a non-empty target has contract and partition coverage. Finding counts equal the
`findings` array, `coverage_gap_count` equals the `coverage_gaps` array,
evidence for every completed coverage record, a reason for every incomplete or not-applicable
variant search, and verdict consistency with all completion rules. `PASS` permits no open or
unresolved follow-up obligation and no blocking coverage gap. `FAIL` requires at least one admitted
finding; an attributable deterministic check failure is represented as a finding. `INCONCLUSIVE`
requires a blocking coverage gap. A null target fingerprint is valid only for a non-PASS result
with a blocking target-identity gap.

### Target Fingerprint

The coordinator computes the fingerprint from the exact validated resolver manifest and exact raw
selected evidence supplied to the reviewer, using Git object hashing or an equivalent deterministic
byte-preserving digest available without modifying the repository. The same evidence must produce
the same fingerprint; any committed, staged, unstaged, untracked, rename, deletion, binary,
submodule, or symlink evidence change must change it. Failure to compute or reproduce the digest is
a coverage gap and prevents PASS.

- **Covers**: REQ-012, REQ-014, REQ-018, REQ-019; NFR-001, NFR-004

## Sequence & Data Flow

### Initial Review

1. The coordinator resolves and validates the Git target with the existing resolver.
2. It collects the exact raw selected evidence and computes the target fingerprint.
3. Scope creates the complete file inventory and preliminary behavior partitions.
4. System Contract derives and maps applicable cross-module contracts without inventing intent.
5. Behavior traces normal and failure flows against the contracts and partitions.
6. Risk activates semantic profiles and independent specialists as required.
7. Verification validates candidates. Each validated repeatable cause triggers bounded variant
   analysis; newly found candidates return to validation.
8. The coordinator confirms every mandatory inventory record, contract, partition, specialist,
   variant search, and deterministic check has a legal terminal state.
9. It emits the six-section report and exactly one schema-v2 envelope.

### Repair and Re-Review

1. The caller validates schema v2 and independently reproduces each admitted finding.
2. It retains only objective outgoing `follow_up.required` records—not completed coverage or
   variant-search records—and performs only verified repairs.
3. After restoring a green baseline, it resolves the updated complete target.
4. It starts a fresh isolated review and supplies the prior objective obligations as incoming work,
   excluding repair reasoning and prior correctness conclusions.
5. The fresh reviewer verifies each incoming obligation against the new target and independently
   executes all five general passes.
6. The new result records incoming obligation states and any new outgoing obligations. Only a full
   PASS with every required completion condition closes the loop.

## Cross-Cutting Design

### Read-Only Safety

The target fingerprint, contract mapping, variant search, and handoff are computed and emitted
without writing state. Existing verification mirror and mutation-detection rules remain mandatory.

### Source Independence

The prompt uses semantic roles such as producer, propagation boundary, consumer, adapter, entry
surface, and symmetric path. Evaluation fixtures use synthetic repositories and generic behaviors;
no source incident, repository name, fixed language, or framework is embedded.

### Reviewer Independence

The coordinator may compare prior and current schema-v2 envelopes. A fresh reviewer receives only
objective obligations, original target fingerprint, authoritative context, current raw evidence,
and the normal review protocol. It never receives the implementer's explanation, patch rationale,
or a claim that the obligation is already satisfied.

## Risks & Trade-offs

| Risk | Impact | Mitigation |
|---|---|---|
| Prompt and envelope become larger | More review context is consumed | Keep human output at six sections; use concise records; partition only when behavior is materially disjoint |
| Reviewer invents contracts | False findings or scope expansion | Require sources and limit inferred contracts to verified behavior and public boundaries |
| Variant search becomes unbounded | Review latency grows without better relevance | Require a cause-derived semantic scope and allow `not_applicable` with a concrete reason |
| Prior obligations bias the fresh reviewer | Repair may be accepted without independent proof | Supply neutral statements and source IDs, never prior conclusions or repair reasoning |
| Target fingerprint is computed inconsistently | Handoff may reference stale evidence | Define one exact evidence bundle per invocation and fail closed when its digest cannot be reproduced |
| Existing consumers still emit schema v1 | Updated workflow cannot complete | Explicitly reject v1 and migrate template, parser, tests, evaluation fixtures, and documentation together |

## Requirements Coverage

| Spec Requirement | Design Coverage |
|---|---|
| REQ-001 | Distributed Review Command; System Contract Mapper; Source Independence |
| REQ-002 | System Contract Mapper; Decision 1 |
| REQ-003 | System Contract Mapper; Contract entity |
| REQ-004 | System Contract Mapper; Source Independence |
| REQ-005 | Review Partition Coordinator; Partition entity |
| REQ-006 | Review Partition Coordinator; Decision 2 |
| REQ-007 | Review Partition Coordinator; Decisions 1 and 3 |
| REQ-008 | Root-Cause Variant Analyzer; VariantSearch entity; Decision 3 |
| REQ-009 | Root-Cause Variant Analyzer; Decision 3 |
| REQ-010 | Root-Cause Variant Analyzer; VariantSearch states |
| REQ-011 | Schema-v2 Result and Handoff; Result entity |
| REQ-012 | Schema-v2 Result and Handoff; data model; target fingerprint |
| REQ-013 | Schema-v2 Result and Handoff; FollowUp entity; Decision 5 |
| REQ-014 | Repair-Loop Consumer; target fingerprint; repair sequence |
| REQ-015 | Repair-Loop Consumer; initial and repair sequences |
| REQ-016 | Repair-Loop Consumer; Decision 4 |
| REQ-017 | Review Partition Coordinator; schema-v2 validation; completion sequence |
| REQ-018 | Schema-v2 validation; target fingerprint; completion sequence |
| REQ-019 | Distributed Review Command; target fingerprint; Decision 4 |
| REQ-020 | Distributed Review Command; Decision 6 |
| REQ-021 | Distributed Review Command; Decision 1 |
| REQ-022 | Contract and Behavioral Evaluation |
| NFR-001 | Schema-v2 Result and Handoff; Read-Only Safety |
| NFR-002 | System Contract Mapper; Source Independence; evaluation |
| NFR-003 | Root-Cause Variant Analyzer; Decision 3 |
| NFR-004 | Schema-v2 data model and validation |
| NFR-005 | System Contract Mapper; Variant Analyzer; human report |
