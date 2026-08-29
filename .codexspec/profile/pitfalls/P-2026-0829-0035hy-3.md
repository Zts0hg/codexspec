## P-2026-0829-0035hy-3: Behavioral fixtures must assert their semantic premise, not a proxy count

- claim: An evaluation fixture must machine-check the concrete semantic evidence it declares instead of accepting generic counts or unrelated terminal states.
- type: pitfall
- scope/when: designing model, agent, compiler, or workflow evaluations whose outputs contain structured evidence
- root-cause: weak proxies such as entry-surface count, any terminal partition, any multi-finding search, or any blocking gap can be satisfied by evidence unrelated to the fixture's intended behavior. The test remains green while no longer measuring the contract named by the case.
- workaround: bind each case to field-specific terms or identities for the required producer-to-consumer trace, distinct semantic partitions, the exact findings grouped by one cause together with a completed, evidenced bounded search whose scope, methods, and checked locations include defective and clean sibling paths, or the blocking gap tied to the uninspectable surface. Include both a hollow counterexample that must fail and a semantically complete example that must pass.
- lesson: evaluation assertions should follow the meaning-bearing links in the claimed behavior; structural presence and cardinality are supporting checks, never substitutes for semantic correspondence.
- evidence.facts: A clean multi-surface case evaluated as passed with empty producer, propagation, consumer, and scenario arrays as long as two entry-surface strings were present. The early-finding and incomplete-coverage cases likewise accepted one arbitrary terminal partition or an unrelated blocking gap, and the related-defect case later passed first with empty search details and then with an incomplete, evidence-free search that omitted a clean sibling. Field-specific trace terms, distinct scope matching, grouped finding identities plus completed search evidence covering defective and clean siblings, and premise-specific gap terms rejected the hollow results and accepted complete examples.
- evidence.state: observed and outcome-verified across repeated reviews of feature 2026-0829-0035hy-review-code-systematic-coverage; applicable to future evaluation corpus changes.
- provenance: distill @commit-staged, 2026-08-29, derivation: inferred, confidence: high
- status: candidate
