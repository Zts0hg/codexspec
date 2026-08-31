## P-2026-0829-2159yg-2: `git diff --check` conflates conflict markers with whitespace errors, and an empty `core.whitespace` disables nothing

- claim: a `git diff --check` gate rejects whitespace-legitimate content unless the whitespace classes are explicitly negated; `-c core.whitespace=` (empty) does NOT disable them.
- type: pitfall
- scope/when: gating staged or unstaged content on `git diff --check` (e.g. conflict-marker-only validation in tooling)
- root-cause: `--check` reports both leftover conflict markers and `core.whitespace` violations (trailing whitespace, space-before-tab, ...) and exits non-zero for either; setting `core.whitespace` to the empty string resets to defaults rather than "none".
- workaround: disable the whitespace classes by negation while keeping marker detection: `git -c core.whitespace=-trailing-space,-space-before-tab,-tab-in-indent,-indent-with-non-tab diff --check`. Empirically verify all three states: markers present → exit 2; whitespace-only → exit 0; clean → exit 0.
- lesson: tool gates built on composite git checks must pin each failure class separately — a single-test gate hides which class the exit code came from.
- evidence.facts: the auto-dev sync resolution gate raised `merge_resolution_check_failed` for a resolution containing only a Markdown hard line break (two trailing spaces); with the negated `core.whitespace` list the same resolution passes while marker-bearing content still fails.
- evidence.state: confirmed at feature 2026-0829-2159yg-blueprint-auto-dev; commit f96d87a (src/codexspec/automation.py `_MARKER_CHECK_WHITESPACE`). Still valid for git 2.x.
- provenance: distill @pr (auto), 2026-08-31, derivation: inferred, confidence: high
- status: candidate
