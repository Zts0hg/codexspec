### S-2026-0902-054178-6: When deferring an embedded auto-distill obligation, re-anchor it to the next stable boundary, never to "the end of the flow"

- claim: An embedded wrap-up obligation (auto-distill, summary, announcement) that is deferred must be re-anchored to a concrete upcoming boundary and executed there; deferring it to "the end of the flow" lets it evaporate when the flow extends.
- type: strategy
- scope: self
- scope/when: long multi-gate flows (review loops, stacked PR chains, releases) that carry an embedded wrap-up obligation from an invoked command
- trigger: you catch yourself deferring an embedded wrap-up obligation (e.g. the pr command's Automatic Distillation) because the flow is mid-flight and a distill now would capture a half-state.
- action: either run it immediately at the next stable boundary (a gate passing, a merge landing — mid-flow distill writing `candidate` records is acceptable; the vetting rules already keep unverified speculation out of `vetted`), or write the obligation into the task list as an explicit entry with that boundary named. Never leave it as an unanchored "at the end".
- evidence.facts: the pr command's Automatic Distillation activated at both PR-body generations; the deferral to "end of the flow" was overtaken by the CI-error detour, the two Windows fixes, and the release, and the records were only written when the user manually invoked `/codexspec:distill`.
- evidence.state: confirmed at feature 2026-0902-054178 rollout (2026-09-07). Still valid.
- provenance: distill @plain chat, 2026-09-07, derivation: inferred, confidence: high
- status: candidate
