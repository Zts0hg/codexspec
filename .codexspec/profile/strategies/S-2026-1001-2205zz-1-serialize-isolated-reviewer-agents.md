### S-2026-1001-2205zz-1: Serialize isolated reviewer agents instead of launching them concurrently

- claim: Launch multiple isolated review agents one at a time (at most two), never three or more in parallel.
- type: strategy
- scope/when: spawning isolated reviewer or specialist subagents for a review gate in one session
- trigger: a review round needs several isolated reviewers (a primary plus specialists) and they are about to be launched in one parallel batch.
- action: launch the heaviest reviewer first and start the others only after it returns; when a reviewer dies on an API 429 usage limit, retry it alone once the limit resets before concluding anything about the target.
- evidence.facts: a three-reviewer parallel launch lost its primary reviewer to an API 429 session limit mid-verification; every subsequent serial launch of the same size completed.
- evidence.state: confirmed at feature 2026-1001-2205zz across review rounds 2 through 8; still valid.
- provenance: distill @implement-tasks, 2026-10-03, derivation: inferred, confidence: high
- status: candidate
