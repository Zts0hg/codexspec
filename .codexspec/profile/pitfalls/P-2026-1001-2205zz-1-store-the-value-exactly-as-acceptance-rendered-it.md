### P-2026-1001-2205zz-1: Store the value exactly as acceptance rendered it

- claim: A gate that normalizes input at acceptance must persist the normalized value, or later revalidation reads different bytes and refuses what was already accepted.
- type: pitfall
- scope/when: any accept -> store -> revalidate pipeline (staging gates, saved drafts, journals)
- root-cause: acceptance renders with a normalized value (a whitespace-only attestation treated as absent) while storing the raw string; a later re-render or schema check reads the stored raw value and reaches a different verdict, so a batch is refused or a persisted draft becomes unloadable.
- workaround: normalize once at the storage boundary and store exactly the value the acceptance decision used — `"verification": (verification or "").strip()` — so every later consumer re-reads the same bytes.
- lesson: an accept/store asymmetry or a second normalizer is a latent accept-refuse contradiction; the stored value must be the one the decision was made on.
- evidence.facts: three admitted review findings in one feature: a vetting gate that read the request instead of the rendered bytes, a whitespace-only verification staged OK but refused the whole batch at apply with empty_verification, and a merge path storing the un-normalized attestation.
- evidence.state: confirmed at feature 2026-1001-2205zz; fixed and pinned by regression tests; still valid.
- provenance: distill @implement-tasks, 2026-10-03, derivation: inferred, confidence: high
- status: candidate
- consolidation: candidate; cluster: accept-store-value-parity
