### P-2026-1001-2205zz-3: Validate structured input against the storage schema, not the lenient render path

- claim: A render path that silently stringifies values hides schema violations until the persisted state is reloaded, by which time the only escape is discarding user work.
- type: pitfall
- scope/when: APIs that accept structured values (JSON fields), persist them, and reload them under a stricter schema
- root-cause: the renderer coerces any value with str(), so a non-string field value stages successfully; the persisted-draft codec requires strings and rejects the whole decision at load, leaving the saved draft unopenable except by discarding every staged decision.
- workaround: type-check structured values against the strictest consumer's contract at the boundary where they enter state — all(isinstance(value, str) for value in fields.values()) — refusing the request before any mutation.
- lesson: validate at the boundary with the persistence schema, never the tolerance of a rendering helper; every producer feeding one store needs the same check.
- evidence.facts: a review finding staged a record with an integer field value end to end; the reload then refused the draft; fixed by value-type checks at all three producers (record fields, merge field changes, manifest editable values).
- evidence.state: confirmed at feature 2026-1001-2205zz; fixed and pinned by tests; still valid.
- provenance: distill @implement-tasks, 2026-10-03, derivation: inferred, confidence: high
- status: candidate
- consolidation: candidate; cluster: accept-store-value-parity
