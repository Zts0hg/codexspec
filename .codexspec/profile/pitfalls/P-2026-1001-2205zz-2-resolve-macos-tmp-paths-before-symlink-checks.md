### P-2026-1001-2205zz-2: macOS /var symlink trips path-ancestry safety checks on temp fixtures

- claim: Pass tempfile.mkdtemp results through Path.resolve() before handing them to code that rejects symlinked path ancestors.
- type: pitfall
- scope/when: writing pytest fixtures or probe scripts that build profile or project trees under macOS temp directories
- root-cause: tempfile.mkdtemp returns /var/folders/... and /var is a symlink to /private/var, so a loader that rejects records under symlinked ancestors fails with symlink_not_allowed on an otherwise valid fixture.
- workaround: root = Path(tempfile.mkdtemp(prefix=...)).resolve() at creation, and pass the resolved root as the project root everywhere afterwards.
- lesson: OS-level symlinked temp prefixes interact with application path-safety checks; resolve fixture roots once, at creation.
- evidence.facts: parse_record raised symlink_not_allowed for a fixture record under /var/folders until the base path was resolved; the same failure recurred across three separate probe scripts before the cause was pinned.
- evidence.state: confirmed at feature 2026-1001-2205zz; still valid.
- provenance: distill @implement-tasks, 2026-10-03, derivation: inferred, confidence: high
- status: candidate
