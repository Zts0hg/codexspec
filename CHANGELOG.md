# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.7.18] - 2026-10-04

### Added

- Ordinary features now use one Git worktree per feature by default, under the sibling
  `<repository-name>-codexspec-worktrees/<full-feature-name>` directory. Existing feature
  workspaces are reused and retained after completion.
- Added checkout-local `workflow.worktrees` configuration and `codexspec config --worktrees`
  controls. Only literal YAML `false` disables ordinary worktree isolation.
- Added isolated maintenance workspaces for standalone project edits, shared workspace
  routing across all 28 commands, and recoverable feature preparation. Creation compares
  local and fetched remote main by ancestry; divergent histories merge in the new worktree
  and require verification before development continues.

### Changed

- **Breaking:** Ordinary workflow writes now leave the main checkout untouched by default.
  Blueprint and auto-dev retain their fixed shared worktree model, but use the same new
  sibling parent directory. Earlier directory layouts have no migration layer.
- Configuration changes take effect in their destination checkout and propagate to other
  checkouts through Git integration. First-time initialization and installation updates
  continue to operate on the explicitly selected checkout.

### Fixed

- Worktree configuration edits preserve UTF-8 content, comments, and LF/CRLF line endings,
  including exact-byte round trips when toggling an existing setting.

### For contributors

- Git test fixtures now require explicit commit identity, and test launchers align CLI
  lookup with the selected Python environment. Cleanup and file-mutation regressions cover
  disappearing temporary locks, timestamp granularity, and Windows text handling.
- CI collects all six OS/Python test results independently of lint; package builds require
  both lint and the full matrix to pass.
- Updated plugin marketplace metadata for the preceding v0.7.17 release.

## [0.7.17] - 2026-10-03

### Added

- Added a manual distill review workspace: `/codexspec:distill review` (and a bare
  `/codexspec:distill`) opens a packaged, fully offline HTML page — a three-column
  layout (review queue / working surface / staged-change ledger) in the project design
  system, with state-grouped queues, byte-identical final-Markdown previews gated per
  control, destructive-action second confirmations, a keyboard map with no
  terminal-operation key, adaptive single-line fields, and 13 display-language
  catalogs. The workspace ships as three static assets plus catalogs: no CDN, no
  network calls, strict CSP.
- Added the deterministic review runtime (`src/codexspec/distill_review/`): a
  field-aware, lossless record codec; a review domain with preview-before-stage and
  byte-symmetric vetting gates; a token-protected loopback HTTP carrier; a recoverable,
  Git-excluded draft store with a single-writer lease; and a journaled, hash-guarded,
  all-or-nothing batch application with crash recovery.
- Added the hidden `_distill-review-helper` CLI (HTML and text modes, `--manifest`
  proposals, `--discard-draft` escape) that the distill command drives; auto-distill
  never invokes either interactive carrier.
- Added six project profile records distilled from the review loop, including one
  marked consolidation cluster awaiting human review in `/distill review`.

### Changed

- Documentation command tables now list `distill`, `evolve`, and `onboard` with the
  distill guide in all eight languages.
- The pre-commit pytest hook reruns the suite in the project's own environment
  (repository `.venv`, the current interpreter when pytest is importable, or
  `uv run`) instead of requiring `uv`, and CI now runs the distill-review suites
  on every platform, including Windows.

## [0.7.16] - 2026-09-07

### Added

- Profile records in `.codexspec/profile/` are now stored as `<id>-<slug>.md`: the
  unchanged record id stays the sole uniqueness carrier (conflict-free parallel-branch
  merges preserved), and a semantic slug derived from the record title (lowercase ASCII
  kebab, at most 50 characters, English rendering for non-ASCII titles, bare-`<id>.md`
  fallback) makes each record's topic readable from a directory listing. The id, the
  `### <id>: <title>` heading, and `[[id]]` cross-links are unchanged; existing records
  are not migrated.

## [0.7.15] - 2026-09-07

### Added

- Added a maintainer-only shared command fragment mechanism
  (`internal/command_template_fragments.py`): per-command sources opt in, standalone
  `<!-- CODEXSPEC:INCLUDE name.md -->` lines pull literal bytes from shared fragments,
  `--write` atomically syncs `templates/commands/`, and the read-only `--check` /
  `--check-distribution` modes gate CI and the release script.
- Added an Expression Standard section to every command template, rendered from one
  shared fragment: hand-off reader perspective, proposition preservation, per-surface
  required content, term definitions before use, honesty over agreeableness, and
  declared binding-ness.
- Added packaging archive tests enforcing the distribution boundary: maintainer
  authoring files never ship, packaged commands carry no unresolved directives, and
  duplicate archive members are rejected.
- Added `.gitattributes` (`* text=auto eol=lf`) so byte-level distribution checks
  materialize identically on every platform.

### Fixed

- Fixed Windows CI failures: `codexspec init` now copies helper scripts in binary mode
  (no CRLF divergence from the LF-pinned worktree), and fragment file-stability checks
  compare Windows-safe stat fields while still detecting real mid-read mutations.

### For contributors

- To opt a command into shared fragments: create
  `internal/command_templates/sources/<command>.md` with `CODEXSPEC:INCLUDE` lines,
  then run `uv run --locked python internal/command_template_fragments.py --write`;
  CI and the release script reject stale output.
- Updated plugin marketplace metadata for v0.7.15.

## [0.7.13] - 2026-08-29

### Added

- Added systematic cross-module contract coverage and explicit review-partition tracking to
  `review-code` defect-gate mode.
- Added bounded root-cause variant searches so equivalent callers, implementations, adapters,
  entry surfaces, and symmetric paths are checked in the same review round.
- Added neutral post-repair verification obligations and target fingerprints for independently
  closing review findings across repair rounds.

### Changed

- **Breaking:** Upgraded the `review-code` defect-gate result envelope to schema v2; schema-v1
  results are now rejected by the `implement-tasks` repair gate.
- Updated `implement-tasks` to preserve objective coverage and follow-up obligations while still
  requiring every fresh reviewer to repeat the complete review.

### For contributors

- Added source-independent review evaluations for multi-surface contracts, related defects,
  continued coverage after an early finding, incomplete coverage, and clean changes.
- Updated plugin marketplace metadata for v0.7.12.
