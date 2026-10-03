### Con-2026-1001-2205zz-1: uv sync uses --extra dev, not --dev

- claim: Set up this repository's development environment with uv sync --extra dev (add --extra docs for docs builds); uv sync --dev is a silent no-op here.
- type: convention
- scope/when: preparing a local dev, test, or docs environment in this repository
- evidence.facts: dev dependencies live in [project.optional-dependencies]; uv sync --extra docs alone removed pytest and produced ModuleNotFoundError; only uv sync --extra dev --extra docs yields a working test and docs environment. CLAUDE.md's Quick Reference still documents uv sync --dev, which is stale.
- evidence.state: confirmed at feature 2026-1001-2205zz; still valid until the dependency groups move.
- provenance: distill @implement-tasks, 2026-10-03, derivation: inferred, confidence: high
- status: candidate
