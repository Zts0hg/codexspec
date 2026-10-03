### P-2026-1003-204985-2: Routed writes must propagate their destination to secondary file updates

- claim: Redirecting the primary output path does not redirect helper functions that still derive their output from the process working directory.
- type: pitfall
- scope/when: routing configuration or artifact writes into another checkout, especially when the operation regenerates commands, indexes, caches, or other secondary files
- root-cause: The config command selected a maintenance config path, but its command-description updater independently used Path.cwd(), splitting one operation's writes across two checkouts.
- workaround: Derive secondary destinations from the same explicit project root as the primary output, and validate every destination before the first write. Assert both the destination's expected changes and the source checkout's unchanged bytes in integration tests.
- lesson: Trace all side effects downstream of a routed entry point; a correct primary filename alone does not establish isolation.
- evidence.facts: tests/test_worktrees_cli.py::test_language_routing_includes_command_frontmatter reproduces the issue for both language setters and verifies source preservation after routing the helper through config_file.parent.parent.
- evidence.state: Both setter regressions and the 71-test worktree/CLI suite pass; this record does not claim completion of the final feature review.
- provenance: distill during feature-worktrees implementation, 2026-10-03; independently reproduced in temporary repositories
- status: candidate
