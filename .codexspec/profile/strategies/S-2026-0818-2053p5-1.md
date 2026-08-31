### S-2026-0818-2053p5-1: Freeze implementation evidence before launching final review

- claim: Start the `implement-tasks` final review only after edits, derived regeneration, deterministic verification, scenario coverage, and a diff fingerprint are complete and stable.
- type: strategy
- scope/when: before invoking an isolated `$codexspec:review-code --feature ...` gate from `$codexspec:implement-tasks`
- trigger: a final review would need to be cancelled, restarted, or amended because implementation edits, derived artifacts, or verification evidence are still moving.
- action: finish all edits first; regenerate derived artifacts; run targeted, cross-cutting, full-suite, lint, format, markdown, type, security, diff, and scenario checks as applicable; compute and record a diff fingerprint; then launch a fresh isolated review and avoid edits until the review returns.
- evidence.facts: "这种错误时机启动复审又取消的行为很浪费我的token，你觉得该如何避免？"
- evidence.state: confirmed during feature `2026-0818-2053p5-reverse-spec`; the final PASS was reached only after keeping the worktree frozen at fingerprint `ea07373b1caa851d29b635f74f2248b8bc4b4bff1d125ceefacaaa277faa22f1` and supplying complete post-freeze verification evidence.
- provenance: distill @implement-tasks, 2026-08-29, derivation: inferred, confidence: high
- status: candidate
