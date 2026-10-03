### P-2026-1003-204985-6: Test launchers must align Python and CLI paths

- claim: Selecting a Python interpreter for tests must also select its installed CLI directory for subprocess PATH lookup.
- type: pitfall
- scope/when: running pytest from plain Git hooks or launchers that select a project virtual environment
- root-cause: A launcher can run the correct Python while preserving the caller's PATH, so Bash or subprocess tests execute a globally installed older CLI. Running the same tests through uv run conceals the mismatch because uv activates the environment's PATH.
- workaround: Ask the selected interpreter for sysconfig.get_path('scripts') and prepend that directory to the child environment's PATH. Do not infer it only from the executable's parent: regular Windows Python installations use a separate Scripts directory. Verify with a nested pytest probe outside repository conftest scope after removing the correct CLI directory from the caller's PATH.
- lesson: Interpreter selection and command lookup are separate environment boundaries; both must agree before local checks represent the branch under test.
- evidence.facts: A plain git commit hook selected the worktree Python but Bash invoked an older global codexspec and failed with No such command '_worktree-helper'. The nested probe failed before PATH alignment, passed afterward, and the full plain-commit hook suite then passed. Python's Windows installation scheme places scripts at {base}/Scripts.
- evidence.state: Reproduced during feature 2026-1003-204985 CI investigation; covered by test_pytest_hook_uses_cli_from_selected_python_environment.
- provenance: distill during PR CI investigation, 2026-10-04; derivation: inferred; confidence: high
- status: candidate
