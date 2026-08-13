## P-2026-0813-1606fz-1: Markdown emphasis inside an asserted phrase breaks template-contract substring tests

- claim: A template-contract substring assertion must target a span that carries no inline markdown emphasis, or it fails against text the template wrapped in `**`/`*`/backticks.
- type: pitfall
- scope/when: writing substring-based contract tests over the `templates/commands/*.md` command templates in the codexspec repo (`test_onboard_template.py`, `test_debug_template.py`, `test_release_notes_template.py`, `test_distill_template.py`, …)
- root-cause: the raw template text carries markdown emphasis markers inside phrases, so a literal like `"Do not block until"` does not exist as a substring when the source wrote `Do **not** block until` — the `**` sits between the words in the raw string the test reads.
- workaround: assert an emphasis-free span (e.g. `"block until the whole scan finishes"`) rather than a phrase spanning an emphasized word; prefer fixing the assertion over editing the template just to satisfy a test.
- lesson: substring assertions over prose-with-markup must land on spans with no inline formatting. When such a contract test fails, first check whether the template behavior is actually correct and only the asserted string is wrong.
- evidence.facts: `test_onboard_scan_is_streaming_and_resumable` asserted `"Do not block until" in content` and failed because `onboard.md` wrote "Do **not** block until the whole scan finishes"; re-asserting the emphasis-free span "block until the whole scan finishes" turned it green with the template unchanged.
- evidence.state: observed at feature 2026-0813-1606fz-onboard, base commit 1a0a49e; verified by outcome (17/17 onboard contract tests green after the assertion fix, full suite 1165 passed). Same substring-contract-test pattern as [[P-2026-0811-1418yq-1]]'s sibling test files.
- provenance: distill @implement-tasks, 2026-08-13, derivation: inferred, confidence: high
- status: candidate
