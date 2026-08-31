# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
