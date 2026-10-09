# Design Document: Review Convergence

**Related Spec**: `.codexspec/specs/2026-1008-1952ti-review-convergence/spec.md`
**Confirmed Requirements**: `.codexspec/specs/2026-1008-1952ti-review-convergence/requirements.md`
**Created**: 2026-10-08
**Status**: Draft

## Context

`review-code` (defect-gate mode) is a coordinator: it runs the project-local resolver (`.codexspec/scripts/review-context.sh` / `.ps1`), computes a target fingerprint, delegates review to a fresh isolated primary reviewer plus required specialists, and emits a human report followed by one `<review-code-result>` envelope (schema `2`, closed object). `implement-tasks` §7 drives it in a final loop: invoke `review-code --feature <dir>`, validate the envelope, verify findings, repair, and re-review with a fresh reviewer until a valid complete-feature `PASS`. `auto-dev` delegates into `implement-tasks` and inherits that loop. `debug` provides the root-cause discipline that `implement-tasks` escalates into.

This design adds: incremental intermediate rounds with a complete final round (REQ-001..004), the `review.decided_by` decision mode (REQ-005..010), cross-round root-cause escalation (REQ-011..012), environment robustness (REQ-013..015), and host-explicit isolation (REQ-016), while keeping today's behavior under default configuration (NFR-001, NFR-002). All edits are to source templates, the config CLI, and the review-code eval/docs that already pin schema `2` (NFR-004).

## Architecture & Components

### C1. Review state store (outside the repository)

- **Responsibility**: Persist per-review records that are too large for the conversation or must survive across rounds and context compaction, without writing into the repository.
- **Interface**: Root `${XDG_CACHE_HOME:-$HOME/.cache}/codexspec/review/<repo-id>/` (Windows: `%LOCALAPPDATA%\codexspec\review\<repo-id>\`), where `<repo-id>` is a digest of the repository's absolute common Git directory. Contents:
  - `results/<algorithm>-<hex>/` (the fingerprint `sha256:<hex>` with `:` replaced by `-`, so the name is valid on Windows) — `report.md`, `envelope.json`, `inventory.json` (every inventory entry with its disposition, per-entry evidence digest, and the `partition_ids` of the partitions that covered it), `coverage.json` (contracts, partitions, variant searches).
  - `loops/<feature-id>.json` — the `implement-tasks` loop ledger (C6).
- **Covers**: REQ-002, REQ-011, REQ-014; supports NFR-001 (no repository-local review state, matching the existing `implement-tasks` rule).

### C2. Incremental review mode in the `review-code` coordinator

- **Responsibility**: When invoked with `--incremental-from <fingerprint>`, review only the repair delta and what it affects, reusing prior coverage for unchanged evidence; otherwise run today's complete review unchanged.
- **Interface**:
  - Input: the prior result's records from C1. Missing, unreadable, or target-mismatched records (different repository, selector, feature, `base_ref`, or `merge_base_sha`) → the coordinator falls back to a complete review in the same invocation, reports `review_scope` as complete, and records a non-blocking gap whose scope is exactly `incremental baseline` (Revised during the implement-tasks review loop, round 2: an unusable baseline is never an argument error.) A changed merge-base changes the selected evidence of every entry, so it never permits reuse.
  - Scope computation (coordinator, before delegation): compare per-entry evidence digests of the current inventory with the prior `inventory.json`. Changed, added, removed, or renamed entries form the **delta**. Every prior partition listed in any delta entry's `partition_ids` is an **affected partition**; the `contract_ids` of affected partitions are the **affected contracts**; every entry of an affected partition joins the scope. (Contract fields such as `producers` and `entry_surfaces` are free text, so the path-addressable `partition_ids` link is the mapping; it makes scope computation mechanical rather than a judgment by the coordinator that just made the repairs.) Carried-over follow-up obligations join as today.
  - Delegation: the fresh reviewer receives the delta, the affected-contract statements and their entry/consumer lists as review obligations, the incoming follow-ups, and the full current evidence for tracing. It does not receive prior coverage evidence, statuses, or findings (isolation preserved). It may trace beyond the scope and must report any finding it discovers.
  - Merge: entries with unchanged digests that are not in an affected partition keep their prior disposition and coverage (marked `carried` in `inventory.json`); everything else takes the fresh result.
  - Output: envelope `review_scope.kind = "incremental"`, `review_scope.since = <prior fingerprint>`. The target block still describes the complete selected target (`complete_feature`, `inventory_count` = full inventory). `review_coverage` lists only this round's contracts, partitions, and variant searches (keeping the envelope small, REQ-014); carried coverage lives in C1 `inventory.json`/`coverage.json` marked `carried`. Inventory accounting and requirements coverage are evaluated over the merged carried-plus-fresh records, so the existing envelope rules (including "a complete feature target requires complete requirements coverage") hold unchanged. An incremental `PASS` is target-limited and never terminal.
- **Covers**: REQ-001, REQ-002, REQ-003

### C3. Decision mode resolution (`review.decided_by`)

- **Responsibility**: Resolve the decision mode for each `review-code` invocation.
- **Interface**: `--decided-by reviewer|ask` (defect-gate modifier, valid with every selector) overrides `.codexspec/config.yml` `review.decided_by`. Absent key → `reviewer`. An invalid value in either place → `INCONCLUSIVE` argument error with usage hints (never silently `ask`). The resolved mode is reported in Scope and the envelope (`decided_by`). `review-code` reads the config itself, so `implement-tasks`/`auto-dev` keep their fixed invocation.
- **Resolver boundary**: the resolver rejects any unrecognized `--*` argument (`unknown_argument`). The coordinator therefore validates its own modifiers (`--decided-by`, `--incremental-from`, including selector agreement and duplicates) and removes them from the argument list before invoking the resolver. The resolver scripts (Bash and PowerShell), their argument parsing, and the manifest schema are unchanged, which also keeps newer templates compatible with an older installed resolver.
- **Covers**: REQ-005, REQ-006, REQ-009

### C4. Scenario-decision items (`ask` mode only)

- **Responsibility**: Represent findings whose trigger depends on inputs or environments outside the project's real operating context as items awaiting a user decision, not as admitted findings.
- **Interface**:
  - Classification is made by the reviewer at Finding Admission, using the confirmed requirements, constitution, and project instructions as the definition of the real operating context. In `reviewer` mode this classification step does not exist (today's rules apply verbatim).
  - Each item: `id`, `location`, `summary`, `trigger`, `impact`, `context_basis` (why the trigger is outside the operating context), `status: pending`.
  - Effect on verdict: a pending item adds a blocking coverage gap with scope `scenario decision <id>`; the verdict is `FAIL` if any admitted finding exists, otherwise `INCONCLUSIVE`. It is never `PASS` while any item is pending.
  - Items already decided in `requirements.md` (C5) are authoritative context: an accepted scenario is out of scope and is not reported again; a "fix" decision is a binding constraint, so a violation is an ordinary admitted finding.
- **Covers**: REQ-007, REQ-008; preserves NFR-001

### C5. Scenario-decision recording (in `implement-tasks`)

- **Responsibility**: Ask the user once per pending item and record the answer as a confirmed requirements entry. A result whose blocking gaps include `scenario decision <id>` gaps is routed here first; §7.5's transient-retry and persistent-`INCONCLUSIVE` stop handling apply only to the remaining gaps, so a pending decision is never retried as a transient failure or treated as a terminal stop.
- **Interface**: Ask with the host's structured-question tool (Claude Code `AskUserQuestion`; Codex `request_user_input`, following that tool's own schema). When the tool is absent or not available in the current mode (Codex offers `request_user_input` only in the root thread, in Plan mode, or behind a feature flag in Default mode), ask in plain text and end the turn; on the user's reply, resume the loop from the C6 ledger. Record into the feature's `requirements.md`:
  - accept → a new `OUT-xxx` entry ("scenario X is not supported") with the user's answer as evidence;
  - fix → a new `CON-xxx` entry ("scenario X must be handled") with the user's answer as evidence;
  - plus a Confirmation Log line. Then continue the loop; a "fix" item is repaired as a verified finding.
  - Under `CODEXSPEC_AUTO_DEV_DELEGATION`, never prompt: return a stop state naming the pending items (auto-dev's existing stage stop guard handles it).
  - A direct `review-code` run without feature context reports the items only; nothing is persisted.
- **Covers**: REQ-008

### C6. Loop ledger and cross-round root-cause escalation (in `implement-tasks`)

- **Responsibility**: Drive the round sequence and detect recurring root-cause classes.
- **Interface**: `loops/<feature-id>.json` in C1 holds: round list (fingerprint, `review_scope.kind`, verdict), the last complete-review fingerprint, verified findings with an assigned `root_cause_class` (a short normalized cause statement written by `implement-tasks` from the reviewer's root-cause description and its own verification), retained follow-up obligations, and pending scenario items. Round policy:
  1. First review: complete.
  2. After a green repair set: incremental, `--incremental-from <last result fingerprint>`.
  3. After an incremental `PASS`: complete. Only a complete `PASS` satisfies §7.6.
  4. After a complete `FAIL`: back to rule 2.
  5. `--incremental-from` always names the last valid (schema-validated, non-argument-error) result. If an incremental invocation returns `review_scope.kind: complete` with a non-blocking `incremental baseline` gap, the prior records were unusable and `review-code` already reviewed completely: treat it as a valid complete round; this is not a transient retry and not a failed round.
  - Escalation: before repairing a verified finding whose class matches a class recorded in an earlier round, enter `debug` with the class (all known instances plus the reviewer's variant-search scope) as one defect.
- **Covers**: REQ-001, REQ-003, REQ-004, REQ-011, REQ-012

### C7. Class-level intake in `debug`

- **Responsibility**: Accept a root-cause class as the symptom so the four-phase discipline targets the shared cause.
- **Interface**: Symptom Intake accepts "a recurring defect class with its known instances". Phase 4 requires one uniform fix for the class and a codebase-wide search for every location of the class, each covered by a regression check. The existing Architecture Gate (≥3 failed fixes) applies to the class.
- **Covers**: REQ-012

### C8. Verification environment rules in `review-code`

- **Responsibility**: Prevent environment overhead from voiding rounds.
- **Interface**:
  - Disposable mirror contract (the command sequence is a planning detail): the mirror reproduces the selected state — the manifest's `HEAD` for default/`--committed`/`--uncommitted`, the selected commit for `--commit` — plus the selected staged, unstaged, and untracked content where the selector includes it; it contains the ignored files the checks need to run without installing anything (for example installed dependency directories), copied rather than linked so checks cannot write into the original; and it has its own Git metadata obtained from a local clone (for example `git clone --local --no-hardlinks --no-checkout`). It never shares the original's Git directory: copying a linked worktree's `.git` file would point the mirror at the original repository's Git state. The original's Git state is never touched (no `git worktree add`).
  - Output: the full inventory, coverage records, and verification logs go to the C1 results directory for the current fingerprint; the human report lists counts and the records path, and the conversation carries only the six-section report and the envelope.
  - Topology: the `review-code` coordinator runs in the caller's context and is the only spawner. The primary reviewer and every specialist are direct children of the coordinator; reviewers never spawn reviewers (maximum depth 1 below the coordinator). Related risk profiles share one specialist; the coordinator spawns at most one specialist per materially disjoint high-impact domain.
- **Covers**: REQ-013, REQ-014, REQ-015

### C9. Host-explicit isolation instructions

- **Responsibility**: State isolation as concrete per-host spawn rules.
- **Interface**: In Reviewer Isolation:
  - Codex: spawn with `spawn_agent` and `fork_turns: "none"`; `fork_turns: "all"` or any conversation fork is forbidden for reviewers and specialists.
  - Claude Code: delegate with the `Task`/`Agent` tool to a fresh non-fork subagent; never use a fork that inherits the conversation.
  - Both: the task message contains only the items Reviewer Isolation lists; it never includes prior finding prose, implementation reasoning, or repair-success claims.
- **Covers**: REQ-016

### C10. Configuration surface

- **Responsibility**: Let users view and set `review.decided_by`.
- **Interface**: `codexspec config --decided-by reviewer|ask` writes `review.decided_by` under a `review:` mapping (created if absent), following the existing `workflow.*` read/write helpers; bare `codexspec config` shows the effective value. `/codexspec:config` adds a menu entry with the same semantics. `codexspec init` does not need to write the key (absent = `reviewer`).
- **Covers**: REQ-010

## Key Design Decisions

### Decision 1: Envelope schema bump to `3`, additive

- **Context**: Incremental results and scenario items need machine-readable representation; schema `2` is a closed object that callers reject when extended.
- **Decision**: Schema `3` = schema `2` plus three required top-level members: `review_scope` (`{kind: "complete"|"incremental", since: fingerprint|null}`), `decided_by` (`"reviewer"|"ask"`), and `scenario_decisions` (array of C4 items; always empty in `reviewer` mode). All schema `2` rules otherwise unchanged. `implement-tasks` accepts only `3` and its §7.6 success additionally requires `review_scope.kind = "complete"` and no pending scenario item.
- **Alternatives**: Keep schema `2` and encode items as coverage gaps with a scope-string convention, and infer incremental scope from the invocation — rejected because the caller would parse prose/string conventions for decision details, which the existing "prose cannot supply machine data" rule forbids.
- **Trade-offs**: Updates the eval harness (`tests/evals/review_code/`), template tests, and command docs that pin `"2"`. With default config a schema `3` result carries `review_scope.kind = "complete"`, `decided_by = "reviewer"`, empty `scenario_decisions`, and is otherwise identical in content to today's (NFR-002).
- **Covers**: REQ-003, REQ-005, REQ-007, NFR-002

### Decision 2: The coordinator, not the reviewer, holds prior coverage

- **Context**: NEED-002 reuses prior coverage; Reviewer Isolation forbids passing prior coverage or conclusions to the fresh reviewer.
- **Decision**: Scope computation and the merge of carried coverage happen in the coordinator (C2). The fresh reviewer receives only scope obligations (delta entries, affected-contract statements and their surfaces), never prior evidence or statuses.
- **Alternatives**: Give the reviewer prior coverage to "skip" — rejected: breaks isolation and lets stale conclusions leak.
- **Trade-offs**: Impact analysis depends on how completely the prior round recorded each entry's `partition_ids`; the final complete review (REQ-003) is the backstop.
- **Covers**: REQ-001, REQ-002, REQ-016

### Decision 3: Per-entry evidence digests computed by the coordinator

- **Context**: The resolver manifest (schema `1`) has no per-entry content hashes; reuse needs them.
- **Decision**: The coordinator computes a per-entry digest (`git hash-object` of the selected content, or a deletion/rename/mode marker) when computing the target fingerprint, and stores it in `inventory.json`. The resolver schema is not changed.
- **Alternatives**: Extend the resolver manifest — rejected: the existing rule says not to change the resolver's independently versioned schema for review-result identity.
- **Covers**: REQ-002

### Decision 4: Scenario decisions persist in `requirements.md`

- **Context**: REQ-008 requires decisions recorded in feature artifacts and followed by later rounds.
- **Decision**: Accept → `OUT-xxx`; fix → `CON-xxx`; with a Confirmation Log entry. Reviewers already read confirmed requirements as authoritative, so later rounds follow them with no new mechanism.
- **Alternatives**: A separate decisions file — rejected: a new artifact reviewers would need to learn, and not part of the authority chain.
- **Trade-offs**: `spec.md`/`design.md` are not regenerated; `analyze` may report the new entries as untraced, which is expected and informational.
- **Covers**: REQ-008

### Decision 5: Out-of-repository state store under the user cache directory

- **Context**: Records must not enter the repository (existing `implement-tasks` rule), must survive long sessions and compaction (the observed session compacted 18 times), and must keep large output out of the conversation.
- **Decision**: C1 under `$XDG_CACHE_HOME`/`%LOCALAPPDATA%`, keyed by repository and fingerprint.
- **Alternatives**: System temp directory — rejected: may be cleaned mid-loop; conversation-only state — rejected: lost on compaction and the source of the oversized-output failures.
- **Trade-offs**: Stale entries accumulate; they are disposable cache and may be deleted at any time (a missing record only forces a complete review).
- **Covers**: REQ-002, REQ-011, REQ-014

## API / Interface Contracts

`review-code` defect-gate argument additions:

| Argument | Valid with | Effect | Errors |
|---|---|---|---|
| `--incremental-from <fingerprint>` | default, `--committed` | Incremental review against that prior result | Unknown/unreadable/mismatched prior result → complete review with a non-blocking `incremental baseline` gap (never an argument error); with `--audit` → argument error |
| `--decided-by reviewer\|ask` | every defect-gate selector | Overrides `review.decided_by` | Any other value → `INCONCLUSIVE` (argument error) |

Both modifiers are consumed by the `review-code` coordinator and stripped before the resolver call (C3, Resolver boundary); the resolver never sees them.

`implement-tasks` §7.1 keeps `$codexspec:review-code --feature <feature-dir>` for complete rounds and adds `--incremental-from <fingerprint>` only for incremental rounds (C6). Neither caller passes `--decided-by`.

Envelope schema `3` additions (Decision 1):

```json
"review_scope": {"kind": "incremental", "since": "sha256:..."},
"decided_by": "ask",
"scenario_decisions": [
  {"id": "S-001", "location": "path:line", "summary": "...", "trigger": "...",
   "impact": "...", "context_basis": "...", "status": "pending"}
]
```

Validation: `since` is non-null iff `kind = "incremental"`; `scenario_decisions` is empty when `decided_by = "reviewer"`; each pending item has a matching blocking gap `scenario decision <id>` that is also an outgoing follow-up source; a result with a pending item is never `PASS`.

## Sequence & Data Flow

```
implement-tasks loop (C6)
  round 1: review-code --feature F                      → complete result R1 (records in C1)
  FAIL → verify → [class seen before? → debug (C7)] → repair → green
  round 2: review-code --feature F --incremental-from R1 → coordinator diffs digests vs R1,
           computes delta + affected partitions/contracts, spawns fresh reviewer (C9), merges carried coverage
  incremental FAIL → repeat from verify;  pending scenario item → ask user (C5) → requirements.md
  incremental PASS → round n: review-code --feature F   → complete result
  complete PASS (no pending items) → §7.6 success;  complete FAIL → back to incremental
```

## Risks & Trade-offs

| Risk | Impact | Mitigation |
|---|---|---|
| Affected-partition mapping misses an indirect dependency (an unchanged entry whose behavior changes through a changed dependency outside its recorded partitions) | A defect in unchanged code is not seen during an intermediate round | The final complete review (REQ-003) re-covers everything; incremental `PASS` is never terminal |
| Reviewer misclassifies a realistic trigger as out-of-context in `ask` mode | A real defect could be accepted by the user | The user sees trigger, impact, and `context_basis` before accepting; default mode is unaffected |
| Inconsistent `root_cause_class` naming across rounds | A recurrence is missed and escalation does not fire | Classes are written by the same caller with its verification; the reviewer's variant-search scope is included; missing escalation never drops a finding |
| Schema bump breaks external consumers of schema `2` | Their validation rejects results | Only CodexSpec's own commands consume the envelope; `implement-tasks` and the eval harness are updated together |

## Requirements Coverage

| Spec Requirement | Design Coverage |
|---|---|
| REQ-001 | C2, C6, Decision 2 |
| REQ-002 | C1, C2, Decision 2, Decision 3, Decision 5 |
| REQ-003 | C2, C6, Decision 1 |
| REQ-004 | C6 (round policy rule 4) |
| REQ-005 | C3, Decision 1 |
| REQ-006 | C3, C4 (no classification in `reviewer` mode), Decision 1 |
| REQ-007 | C4, Decision 1 |
| REQ-008 | C4, C5, Decision 4 |
| REQ-009 | C3 (review-code reads config), API contracts |
| REQ-010 | C10 |
| REQ-011 | C6, C1 |
| REQ-012 | C6, C7 |
| REQ-013 | C8 (mirror) |
| REQ-014 | C1, C8 (output), Decision 5 |
| REQ-015 | C8 (topology) |
| REQ-016 | C9, Decision 2 |
| NFR-001 | C2 (incremental never terminal), C4 (pending never PASS), C6 |
| NFR-002 | C3 default, Decision 1 trade-offs |
| NFR-003 | C6 (no round cap; escalation instead) |
| NFR-004 | All components live in `templates/commands/{review-code,implement-tasks,debug,config}.md` and the `codexspec config` command; eval/tests/docs updated for schema `3` |
