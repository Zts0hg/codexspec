# Design Review Report

## Summary

- **Overall Status**: PASS
- **Compatibility Score**: 100/100
- **Authority Mode**: Requirements-first
- **Readiness**: Ready for Planning
- **Rounds**: 2 (round 1 found one Critical, one Warning, and one Minor; round 2 found one further Minor; all four were remediated within the automatic fix budget)

Every specification requirement has design coverage, every component and decision carries a `Covers` line, the three design assumptions stay labeled as assumptions, and no decision overrides a confirmed trade-off. The two backend additions stay additive and read-only, and the design states why nothing is added to the persisted draft. The defects found concerned the design's own central mechanism and three concrete derivations from the existing backend's data shapes; each remediation was determined by a verified repository fact, and none required a product decision.

## Requirement Coverage

| Requirement | Design Reference | Result |
|---|---|---|
| REQ-001 | Page shell; Layout and responsive grid | Covered |
| REQ-002 | Queue renderer; Decision 4; `queue.*` keys | Covered |
| REQ-003 | Decision 6 | Covered |
| REQ-004 | Ledger and progress; Decision 2; Decision 5 | Covered |
| REQ-005 | Final-content panel; Working surface renderer | Covered |
| REQ-006 | Final-content panel and gate indicator; Decision 1 | Covered |
| REQ-007 | Preview gate authority; Decision 1; Sequence & Data Flow | Covered |
| REQ-008 | Final-content panel and gate indicator; `verification.*` keys | Covered |
| REQ-009 | Status and feedback channel | Covered |
| REQ-010 | Ledger and progress; Decision 5 | Covered |
| REQ-011 | Ledger and progress (identifier-to-target resolution) | Covered |
| REQ-012 | Decision action bar | Covered |
| REQ-013 | Decision action bar; Decision 3; `confirm*` keys | Covered |
| REQ-014 | Adaptive field control; Decision 2 | Covered |
| REQ-015 | Adaptive field control | Covered |
| REQ-016 | Keyboard controller; Decision 7 | Covered |
| REQ-017 | Keyboard controller; Decision 7 | Covered |
| REQ-018 | Decision 6; Page shell; `autoAdvance` key | Covered |
| REQ-019 | Status and feedback channel; `allDecided` key | Covered |
| REQ-020 | Session snapshot extension; Page shell | Covered |
| REQ-021 | Queue renderer; Decision 4; Accessibility | Covered |
| REQ-022 | Page shell; Adaptive field control; Status channel; Accessibility | Covered |
| REQ-023 | Working surface renderer; Decision action bar; `members` key | Covered |
| NFR-001 | Design token layer; token table; Decision 4 | Covered |
| NFR-002 | Design token layer | Covered |
| NFR-003 | Layout and responsive grid | Covered |
| NFR-004 | Layout and responsive grid; Internationalization and direction | Covered |
| NFR-005 | Security and delivery | Covered |
| NFR-006 | Decision 2; Decision 4; Security and delivery | Covered |
| NFR-007 | Decision 1; Decision 8; the two additive projections | Covered |
| NFR-008 | Localization layer; catalog key table | Covered |
| NFR-009 | Localization layer; Status and feedback channel | Covered |
| NFR-010 | Verification | Covered |

## Verified Defects

### Critical

None outstanding.

### Warnings

None outstanding.

### Minor

None outstanding.

## Remediated During Review

Each entry records a verified defect, the repository fact that determined its remediation, and what changed. No remediation introduced a product decision.

### Round 1

- **C-001 (Critical) — the gate projection did not exclude keys from earlier draft revisions, so the false-ready state survived.** Verified in `src/codexspec/distill_review/server.py`: a previewed-operation key is built as `f"{draft.revision}:{encoded}"`, `/api/preview` adds it, `/api/draft` discarded only the key it consumed, `/api/refresh` clears the set, and no path removed keys whose embedded revision had been superseded. The first draft projected "every key currently held", and its data-flow claimed the page's recorded digest would be absent after an unrelated mutation. That was false: the key remained present though unreachable, so the page would read its own digest as valid and show a gate the backend refuses — on the very path the design cites as its motivating example. Remediated by establishing the invariant that the set only ever holds keys for the current draft revision: the set is cleared whenever the revision advances, in place of discarding the single consumed key. This is exact rather than conservative, because a key stored under an earlier revision can never again satisfy a lookup composed from the current one, and it is strictly stricter than the previous single-key discard, so it weakens no invariant. The alternatives — projecting without clearing, and filtering the projection by revision while leaving stale keys in the set — are now recorded with their reasons, and the data-flow states the actual mechanism.
- **W-001 (Warning) — two parts of the design disagreed about the source of the queue's per-entry state.** Verified in `src/codexspec/distill_review/domain.py`: `ReviewService.summary()` places a discarded record and the member records a merge replaces in the same `removed` group, so that object cannot distinguish them, while `ReviewDraft.decisions` can, because each decision carries its `action`. The queue component said it read the draft; the single-accounting decision said the queue derived state from the summary. Remediated by stating the split: per-entry decision state comes from `draft.decisions` and `draft.deferred`; counts, group totals, and the progress figure come from `summary`. Both arrive in the same response and are projections of the same draft, which is what the single-accounting decision exists to guarantee, and the rejected alternative is recorded with the shape of `summary()` as its reason.
- **M-001 (Minor) — the order of a destructive confirmation relative to the gate check was unspecified.** The backend refuses an ungated merge with `preview_required`, so a reviewer could confirm the deletion of member records and then be refused, having been told a consequence that did not occur. Remediated by fixing the order: the gate is evaluated before the confirmation, no destructive confirmation is raised for an action the backend would refuse, and while the gate is unsatisfied the control routes to previewing as the gate indicator already advertises. Discarding the draft is not preview-gated and goes straight to its confirmation.

### Round 2

- **M-002 (Minor) — one ledger group listed identifiers that cannot be selected.** Verified in `src/codexspec/distill_review/domain.py`: `summary()["added"]` holds the `record_id` a staged merge will create, and `ReviewService.from_project` requires that identifier not to be an existing record. Selecting such an entry under the requirement that every listed identifier opens its record or cluster would therefore have resolved to nothing, leaving a dead control on the panel built for navigation. Remediated by stating the resolution for each group: identifiers in `replaced`, `promoted`, `removed`, `deferred`, and `undecided` are records and select themselves; a `merged` entry is a cluster name and selects that cluster; an `added` identifier resolves to the cluster whose staged merge declares it, matched through the `record_id` of the `cluster:`-keyed decisions.

## Risk Advisories

- **`CSS.supports` is called without a guard in the stated assumption.** Applicability: the adaptive field control's capability check. The design's assumption says that if `CSS.supports` were absent the fallback path runs, but an unguarded call on a missing `CSS` object throws instead of falling back. This is a one-line implementation concern, not a design change, and the fallback it guards is already the safe default.
- **Clearing the previewed-operation set on every revision advance makes a second preview necessary more often.** Applicability: a reviewer who previews one item, decides a different item, and returns. The backend already behaves this way — the stored key was unreachable regardless — so nothing becomes stricter in practice; what changes is that the interface now reports it in advance instead of letting the reviewer discover it through a refusal. Worth watching in use: if reviewers find the repeated preview tedious, the remedy is a workflow decision for the user, not a relaxation of the gate.

## Design Opportunities

- **The gate projection could report per-item state instead of a token set.** Returning, for each in-scope item, whether the backend currently holds a previewed operation for it would remove the page's digest bookkeeping and make the three gate states a direct read. It is a slightly larger response and server change than the token list, and the token list is correct once the revision invariant holds, so this is an alternative shape rather than a correction.
- **Pruning rather than clearing would generalize if previews ever became revision-independent.** The current design clears because no stored key can survive a revision advance. If a future change ever stored keys that outlive a revision, the clear would become lossy where a revision-scoped filter would not. Nothing in this feature requires it; it is noted so a later change does not inherit the clear without re-checking why it was safe.

## Score Derivation

- Critical root causes: 0
- Warning root causes: 0
- Minor root causes: 0
- Formula: No outstanding defects = **100**. Round 1 scored 38 (one Critical, one Warning, one Minor: max(0, 49 − 0 − 8 − 3)); all three were remediated, round 2 found and remediated one further Minor, and the final document carries no verified defect. Advisories do not affect the score.
