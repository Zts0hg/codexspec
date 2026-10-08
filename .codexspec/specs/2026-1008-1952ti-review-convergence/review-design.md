# Design Review Report

## Summary

- **Overall Status**: PASS
- **Compatibility Score**: 100/100
- **Authority Mode**: Requirements-first
- **Readiness**: Ready for Planning
- **Review Rounds**: 3 reviews, 2 automatic fix rounds
  - Round 1: NEEDS_REVISION (3 Warning, 5 Minor root causes; score 50); all remediations deterministic and applied.
  - Round 2: two Round 1 remediations were incompletely applied (stale "affected contract" wording in the merge rule; a stale `results/<fingerprint>/` path in C8), plus one new Minor (scenario-decision gaps vs `implement-tasks` §7.5 `INCONCLUSIVE` handling); all fixed.
  - Round 3: no defects.

## Requirement Coverage

| Requirement | Design Reference | Result |
|---|---|---|
| REQ-001 | C2, C6, Decision 2 | Covered |
| REQ-002 | C1, C2, Decisions 2, 3, 5 | Covered |
| REQ-003 | C2, C6, Decision 1 | Covered |
| REQ-004 | C6 rules 4–5 | Covered |
| REQ-005 | C3, Decision 1 | Covered |
| REQ-006 | C3, C4, Decision 1 | Covered |
| REQ-007 | C4, C5, Decision 1 | Covered |
| REQ-008 | C4, C5, Decision 4 | Covered |
| REQ-009 | C3, API contracts | Covered |
| REQ-010 | C10 | Covered |
| REQ-011 | C1, C6 | Covered |
| REQ-012 | C6, C7 | Covered |
| REQ-013 | C8 mirror contract | Covered |
| REQ-014 | C1, C2 output, C8 output, Decision 5 | Covered |
| REQ-015 | C8 topology | Covered |
| REQ-016 | C9, Decision 2 | Covered |
| NFR-001 | C2, C4, C6 | Covered |
| NFR-002 | C3, Decision 1 | Covered |
| NFR-003 | C6 | Covered |
| NFR-004 | All components; Decision 1 trade-offs | Covered |

Every component and decision carries `Covers:`. No design decision changes confirmed behavior; the one labeled assumption from the spec (meaning of "feature artifacts") is resolved by Decision 4 without expanding scope.

## Verified Defects

### Critical

None.

### Warnings

None remaining. Resolved in Round 1 → 2:

- **W1 — New modifiers would be rejected by the resolver.**
  - Evidence: `scripts/bash/review-context.sh:115-117` rejects any unrecognized `--*` argument with `unknown_argument`. `review-code` passes its arguments to the resolver.
  - Location: C2, C3, API contracts.
  - Mismatch: `--incremental-from` and `--decided-by` were defined as `review-code` arguments without saying how they get past the resolver.
  - Impact: every incremental or overridden invocation would end in `INCONCLUSIVE`.
  - Remediation applied: the coordinator validates both modifiers and strips them before invoking the resolver. The resolver scripts and manifest schema stay unchanged, which is also safe when a newer template runs against an older installed resolver.
- **W2 — The mirror contract would lose dependencies and was pinned to `HEAD`.**
  - Evidence: Verification Safety forbids installing dependencies. The existing rule asks for a "mirror of the selected state". In linked worktrees, `.git` is a file pointing at the shared Git directory.
  - Location: C8.
  - Mismatch: a fresh `git clone` lacks the ignored, installed dependency directories, so test suites cannot run. "Checked out at HEAD" is wrong for `--commit` targets.
  - Impact: mirrors would still void rounds (REQ-013), just for a different reason.
  - Remediation applied: the mirror is now specified by what it must contain:
    - the selected state, at the manifest `HEAD` or the selected commit;
    - the ignored files that checks need, copied rather than linked;
    - its own Git metadata from a local clone, never sharing the original's Git directory.
- **W3 — Affected-contract computation relied on free-text fields.**
  - Evidence: contract `producers`, `propagation`, `consumers` and `entry_surfaces` are free text in the schema `2` example (for example `"policy resolver"`).
  - Location: C2, Decision 2.
  - Mismatch: delta entries (paths) cannot be mechanically matched to free text.
  - Impact: scope would depend on judgment by the same context that made the repairs, so it could under-scope.
  - Remediation applied: each `inventory.json` entry records its `partition_ids`. Affected partitions are those containing a delta entry, and their `contract_ids` are the affected contracts.
  - Completion: two stale references were finished in Round 2.

### Minor

None remaining. Resolved:

- **M1 — Fingerprint used as a directory name.** `sha256:<hex>` contains `:`, which is invalid in Windows paths (cross-platform requirement in CLAUDE.md). The directory name is now `sha256-<hex>`; the stale C8 reference was completed in Round 2.
- **M2 — No fallback when the prior record is missing.** Decision 5 claimed "a missing record only forces a complete review", but C6 had no such rule. C6 rule 5 now adds the fallback and requires naming the last valid result.
- **M3 — Question-tool availability on Codex.** "Plain text when neither exists" did not cover Codex, where `request_user_input` exists but is unavailable outside the root thread or Plan mode (default mode needs a flag). C5 now falls back to plain text, ends the turn, and resumes from the ledger.
- **M4 — Base-mismatch criterion was ambiguous.** It said "base" without saying whether that meant `base_ref` or `merge_base_sha`, and a moved merge-base changes every entry's selected evidence. C2 now requires both to match.
- **M5 — Incremental envelope semantics were undefined.** Whether `review_coverage` lists carried records, and how the hard rule "complete feature target requires complete requirements coverage" holds in an incremental result, were not specified. C2 now states that the envelope lists only this round's coverage, that accounting runs over the merged records, and that the existing rules are unchanged.
- **M6 (Round 2) — Scenario-decision gaps vs §7.5 `INCONCLUSIVE` handling.** A pending decision could have been retried as a transient failure or treated as a terminal stop. C5 now takes precedence for `scenario decision <id>` gaps.

## Risk Advisories

- **Cloning from linked worktrees and special repositories (C8)**: local clones from a linked worktree path, shallow clones, partial clones, or repositories with alternates can behave differently. Planning should verify the mirror recipe on a linked worktree (this repository's own layout) and define the `INCONCLUSIVE` reason when cloning is impossible.
- **Hosts that run `implement-tasks` inside a subagent (C8 topology)**: with depth-1 topology, the coordinator must be able to spawn. Claude Code subagents cannot spawn subagents, so such a setup yields `INCONCLUSIVE` for isolated reviews. This is today's behavior, and auto-dev currently runs stages in its own context, so it does not apply now.
- **Direct `ask`-mode runs without feature context (C5)**: decisions are not persisted, so the same items reappear on every direct run. The user can switch to `--decided-by reviewer` or run with `--feature`.

## Design Opportunities

- `root_cause_class` normalization (C6) could reuse the ten risk-profile names as a coarse prefix (for example `filesystem/path handling: symlink ancestor escape`), which makes recurrence matching more stable without changing the review-code schema.

## Score Derivation

- Final round: Critical 0, Warning 0, Minor 0 → no defects → 100
- Round 1 (for the record): Warning 3, Minor 5 → max(50, 79 − 8×2 − 3×5) = max(50, 48) = 50
