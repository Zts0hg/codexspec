## S-2026-0814-1548g5-1: When a review surfaces one instance of a class-defect, sweep for all siblings that same round

- claim: On a review finding that is one member of an obvious class (a stale enumeration, a missed lockstep site, an untranslated string), stop and grep for every sibling of that class before fixing — do not fix only the named instance.
- type: strategy
- scope/when: reacting to a `review-code` (or reviewer) finding during `implement-tasks`, especially "stale/duplicated statement" or "missed site" defects
- trigger: a review round reports a defect that is clearly one occurrence of a repeatable pattern ("X still says four", "site Y wasn't updated") rather than a one-off.
- action: derive the search pattern from the finding and grep the whole repo for all occurrences in the same round; fix them together and re-grep to confirm zero remain. Only then re-run the gate. Treat "the reviewer named one site" as a lower bound, never the complete list.
- evidence.facts: "three successive rounds each surfaced a distinct stale \"four category\" enumeration site that the plan had missed ... A single upfront grep sweep would have caught all sites at once instead of one-per-review-round"
- evidence.state: observed at feature 2026-0814-1548g5-distill-effectiveness, base commit 04cb62d8. The review gate took three FAIL rounds (onboard.md:33 → onboard.md:48 → CLAUDE.md prose) because each fix addressed only the reviewer-named site; a whole-repo grep after round 2 found the remaining four CLAUDE.md sites at once and round 3 passed.
- provenance: distill @implement-tasks, 2026-08-16, derivation: inferred, confidence: high
- scope: self
- status: candidate
