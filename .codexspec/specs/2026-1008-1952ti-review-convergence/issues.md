# Issues

## Issue: Behavioral acceptance on real hosts is pending (T024, T025)

- **Task**: T024 (manual acceptance), T025 (optional live eval)
- **Error**: Not a failure. These tasks need real LLM review loops on Codex and Claude Code. The change targets Codex's behavior in particular, so the run belongs with the user rather than being self-certified by the implementer. String-contract tests prove the rules are present; they cannot prove a host follows them.
- **Attempted**: All automated verification passed: the full suite (1890 passed, 54 skipped), ruff, `--check-distribution`, `mkdocs build --strict`, markdownlint, a rendering check of both host forms in a scratch project, and an end-to-end run of `codexspec config --decided-by`.
- **How to run T024** (after `uv tool install --force .` from this branch, or `codexspec init --ai both` in a scratch repository):
  1. Seed a small feature with one real defect and run `implement-tasks`. Confirm that a complete `FAIL` is followed, after the repair, by an incremental round whose Scope reports `incremental since <fingerprint>` and covers only the changed and affected partitions, and that a complete `PASS` closes the loop (TS-24.1, TS-24.2).
  2. Set `review.decided_by: ask` and seed an out-of-context trigger (for example, Unicode case-folding collisions in an ASCII-only tool). Confirm the scenario prompt, choose accept, check the new `OUT-xxx` in `requirements.md`, and confirm the next round does not raise it again (TS-24.3). Re-run with `--decided-by reviewer` (TS-24.4).
  3. Seed two instances of one root cause so that they surface in different rounds. Confirm the trip (c) escalation into `debug` (TS-24.5).
  4. Use a check that needs Git metadata and installed dependencies. Confirm it runs in the mirror and that the original repository's Git state is unchanged (TS-24.6).
  5. With default configuration, confirm there are no scenario items and that admission behavior is unchanged (TS-24.7).

  Record which host ran each scenario. Re-running the original non-converging `games-dev-roguelite` loop is the most realistic check of NEED-001.
- **Status**: Needs Discussion. It awaits the user's decision to run it, or permission for the implementer to run it.
