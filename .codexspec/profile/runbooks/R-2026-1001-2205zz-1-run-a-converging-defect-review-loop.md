### R-2026-1001-2205zz-1: Run a converging defect-review loop to a clean merge gate

- claim: The round structure that takes a reviewed worktree from admitted findings to several clean reviewers on one fingerprint.
- type: runbook
- scope/when: multi-round pre-merge defect review of a feature branch in this repository
- steps: 1) compute the target fingerprint from the review manifest (.codexspec/scripts/review-context.sh --feature <dir>, sha256 over the manifest plus per-record git hash-object); 2) launch an isolated fresh primary reviewer with staged scope/contract/behavior/risk/verification instructions and incoming obligations stated as neutral behaviors to verify, never as repairs; 3) reproduce every admitted finding independently before editing; 4) fix test-first (failing test first, then the fix) and verify behavioral fixes in a live browser or runtime; 5) record each round's repairs in the feature tasks.md; 6) recompute the fingerprint, grow the obligations by the round's findings restated as behaviors, and start a fresh isolated round; 7) on a round with zero findings, run the security and filesystem specialists on that same fingerprint and close the loop only when all reviewers report zero findings with all obligations verified.
- failure-recovery: if a reviewer dies on a usage limit (API 429), relaunch it as a fresh isolated round once the limit resets — a transient inconclusive is retryable, not a verdict; if a reviewer admits a finding, do not argue it down without reproducing it — a reproduced finding is repaired, an unreproducible one is answered with reproduction evidence and referred to the next fresh round.
- evidence.facts: eight review rounds took this branch from twelve admitted findings (two P1-class) to three reviewers at zero findings on fingerprint sha256:628aa7a4a41893d0f41e1454293ed8b17f430c9f11fe3d5851982cbf988c38f4; every round's repairs were pinned by regression tests.
- evidence.state: confirmed at feature 2026-1001-2205zz; still valid.
- provenance: distill @implement-tasks, 2026-10-03, derivation: inferred, confidence: high
- status: candidate
