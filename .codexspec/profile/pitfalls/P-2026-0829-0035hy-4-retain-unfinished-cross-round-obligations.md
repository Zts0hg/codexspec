## P-2026-0829-0035hy-4: Cross-round state must retain every unfinished obligation

- claim: A retry coordinator must carry forward every unresolved input and every incomplete mandatory item from the current round until an independent worker records a terminal disposition.
- type: pitfall
- scope/when: implementing caller-owned state handoff for retry, repair, approval, or verification loops
- root-cause: rebuilding the next-round handoff solely from selected outgoing records silently drops either an older unresolved input or current mandatory work that has no finding, such as incomplete coverage, verification, or reviewer output.
- workaround: require the producer to emit a neutral obligation for every current incomplete mandatory item, then construct retained state from all new outgoing obligations and all incoming obligations still marked unresolved; allow only the next independent worker to retire an input as verified or superseded with current evidence, preserve stable identity and provenance, and reject conflicting duplicate identities.
- lesson: state transition logic must account for persistent inputs, every source of newly unfinished work, and terminal inputs separately; “retain finding outputs” is not equivalent to “retain all unfinished work.”
- evidence.facts: A valid non-PASS review could place a prior obligation only in `follow_up.received` with `status: unresolved`, while `implement-tasks` rebuilt retained state only from `follow_up.required`, causing the prior obligation to disappear. After fixing that consumer path, a result could still contain incomplete contract, partition, search, verification, or reviewer work without emitting any corresponding outgoing obligation, so the work disappeared after the finding was repaired. Producer completeness plus unresolved-input retention closed both paths.
- evidence.state: observed and regression-tested at feature 2026-0829-0035hy-review-code-systematic-coverage; focused workflow tests pass after retaining the unresolved-input/outgoing union.
- provenance: distill near-moment, 2026-08-29, derivation: inferred, confidence: high
- status: candidate
