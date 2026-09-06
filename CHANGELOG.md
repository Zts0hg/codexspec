# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
