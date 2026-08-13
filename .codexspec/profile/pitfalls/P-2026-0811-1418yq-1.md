## P-2026-0811-1418yq-1: The implement-tasks review gate needs an isolated reviewer subagent

- claim: The `review-code` defect gate invoked by `implement-tasks` requires an `isolated` reviewer topology; run inline in the implementer's own context it can only reach `shared`.
- type: pitfall
- scope/when: running `/codexspec:implement-tasks` (or `/codexspec:review-code --feature ...`) inline without delegating the review to a subagent
- root-cause: `review-code` derives its `review_context` from whether it runs in its own agent context. Run inline (same context that did the implementation) it can only self-report `review_context: "shared"`, because it cannot certify independence from the implementer's reasoning. §7.6 success requires `isolated`, so an inline review is never a clean success — and `auto_distill` only fires on a clean §7.6 success.
- workaround: spawn a dedicated review subagent (general-purpose), fed **only** the evidence (feature dir + changed files), NOT the implementer's reasoning; have it invoke `/codexspec:review-code --feature <dir>` and return the envelope. Its separate context yields `review_context: isolated` and a clean PASS, after which `auto_distill` fires.
- lesson: any gate that certifies "independent review" cannot be satisfied by the same agent that did the work — self-review is structurally `shared`. Delegate such gates to a subagent.
- evidence.facts: "auto_distill 默认开，那为什么没有自动跑？"; "spawn 一个独立复审子 agent(补上 isolated,拿到 clean PASS,distill 自动跑)"
- evidence.state: observed at feature 2026-0811-1418yq-debug-command, base commit 8e69f51. Confirmed by outcome — the inline review returned shared/INCONCLUSIVE and auto_distill did not fire; after spawning an isolated review subagent the envelope was a clean isolated PASS and auto_distill fired. Re-confirmed at feature 2026-0813-1606fz-onboard.
- provenance: distill @implement-tasks, 2026-08-11, derivation: inferred, confidence: high
- status: candidate
