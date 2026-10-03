### P-2026-1003-204985-1: Conda readline import can crash pytest before collection

- claim: If pytest exits with signal 11 before collection on this Mac, reproduce `import readline` under the selected interpreter before changing project code.
- type: pitfall
- scope/when: preparing or debugging the CodexSpec test environment on a Mac where uv selects `/opt/anaconda3/bin/python3.12`
- root-cause: Pytest's capture initialization imports readline; the selected Conda Python 3.12.7 native readline module crashed during import even in a one-line process, before any repository test ran. The deeper native-library fault was not diagnosed.
- workaround: Run `uv run python -X faulthandler -c 'import readline'`; if it reproduces, compare an already installed supported interpreter. Python 3.11.13 managed by uv passed the same import; `uv sync --extra dev --python 3.11` rebuilt the disposable feature environment and allowed pytest to collect normally.
- lesson: A test-runner startup crash may belong to the selected interpreter, so isolate its failing standard-library import before changing tests or application code.
- evidence.facts: Conda Python 3.12.7 exited 139 both for pytest startup at `_pytest/capture.py` `_readline_workaround` and for `import readline`; uv-managed Python 3.11.13 imported readline successfully. After environment replacement pytest reported the expected missing `codexspec.worktrees` module rather than crashing.
- evidence.state: Outcome verified on 2026-10-03 during feature 2026-1003-204985. Applicability is limited to the observed interpreter installation; this does not claim all Conda installations are defective.
- provenance: distill @implement-tasks, 2026-10-03, derivation: inferred, confidence: high
- status: candidate
