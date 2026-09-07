### S-2026-0907-1623rh-1: When a defect-gate envelope has schema-only violations, have the same reviewer re-emit it instead of re-reviewing

- claim: A review-code result envelope whose substance is complete but whose shape violates the schema-2 rules is repaired by sending the same isolated reviewer one correction request to re-emit the envelope with identical content — never by the coordinator editing the machine data, and never by discarding a finished review for a full re-run.
- type: strategy
- scope: self
- scope/when: coordinating `/codexspec:review-code` (or any schema-2 envelope gate) as the outer caller
- trigger: envelope validation fails on shape, not substance — e.g. selector-identity fields wrong (`default`/`committed` require non-null base_ref + merge_base_sha with NULL commit_sha/parent_sha; `commit` requires the reverse), undeclared or missing entity fields (with zero admitted findings `variant_searches` must be `[]`; contracts/partitions have fixed field sets), or array/counts disagreements.
- action: enumerate the exact violations in one message to the same reviewer; ask for a corrected envelope with identical verdict, findings, contracts, partitions, gaps, and verification content and zero new review work; revalidate the returned envelope from scratch before accepting. Only shape may change — any substantive difference voids the review.
- evidence.facts: the implement-tasks final gate returned a PASS review (7 complete contracts, 1 non-blocking gap, 9 green verification commands) whose envelope carried non-null commit_sha/parent_sha under selector `default` and two variant_searches records using undeclared fields; one correction message produced a valid envelope that revalidated as PASS with no second review cycle.
- evidence.state: confirmed at feature 2026-0907-1623rh implement-tasks (2026-09-07); corrected envelope validated and accepted. Still valid.
- provenance: distill @implement-tasks, 2026-09-07, derivation: inferred, confidence: high
- status: candidate
