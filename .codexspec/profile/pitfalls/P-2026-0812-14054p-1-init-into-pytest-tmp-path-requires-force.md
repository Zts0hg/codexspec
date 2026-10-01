## P-2026-0812-14054p-1: `codexspec init` into a pytest `tmp_path` needs `--force`

- claim: A test that invokes `codexspec init <tmp_path>` must pass `--force`, or `init` aborts because the directory already exists.
- type: pitfall
- scope/when: writing pytest tests that run the `init` CLI command into `tmp_path`
- root-cause: `init` guards against clobbering a real project by aborting (exit 1) when the target directory already exists, unless `--force` is passed; pytest's `tmp_path` fixture pre-creates the directory, so the guard always trips.
- workaround: pass `--force` in the CLI invocation whenever a test runs `codexspec init <tmp_path>` (e.g. `init <tmp_path> --force`).
- lesson: a CLI that guards on "directory exists" will always trip against a test fixture that pre-creates its temp dir — pass the override flag in tests, or target a not-yet-existing subpath.
- evidence.facts: the init CLI aborts with `Error: Directory '...' already exists / Use --force to overwrite or choose a different name` (exit 1) when the target already exists; tests failed until the invocation was changed to include `--force`.
- evidence.state: observed at feature 2026-0812-14054p-profile-consumption, base commit 8e69f51; confirmed by outcome (test_init_profile went green after adding `--force`).
- provenance: distill @implement-tasks, 2026-08-12, derivation: inferred, confidence: high
- status: candidate
