# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.7.26] - 2026-10-18

### Changed

- Clarified descriptions for all 28 workflow commands so users can identify each
  command's purpose and result from compact, informative text in command pickers.
  Descriptions reflect current behavior and distinguish neighboring workflow stages.
- Synchronized descriptions in English, Simplified Chinese, Japanese, Korean,
  German, French, Spanish and Brazilian Portuguese across Claude commands, Codex
  skills and command listings.

### For contributors

- Recorded the approved wording and supporting requirements, design and
  verification evidence; updated description assertions in integration and
  packaging tests, including YAML parsing that accepts quoted descriptions.
- Updated marketplace metadata for the preceding v0.7.25 release.

## [0.7.25] - 2026-10-17

### Added

- Discover project installations with `codexspec scan <path>`. Offline, read-only
  scanning includes hidden and nested projects and worktrees, reports recorded
  versions and actual content consistency, and identifies incomplete scans.
- Upgrade discovered projects with `--upgrade`, choosing each project or all
  remaining projects; use `--upgrade --yes` for automatic selection. One latest
  stable release is prepared in an isolated environment without replacing the
  global CLI. Affected local modifications or uncertain preservation skip the
  whole project with an explicit reason, including in automatic mode.
- Successful verified installations record the version, managed-file list and
  checksums. Legacy projects can upgrade without manual metadata migration;
  same-version content mismatches remain repairable. Configuration and
  project-owned content are preserved, and newer versions are not downgraded.

### Changed

- Refreshed English and seven translated READMEs and documentation sites with
  current capabilities, Codex desktop installation, stage review behavior,
  historical decision reuse and native-language explanations.
- Added eight-language light/dark workflow diagrams shared by READMEs and the
  documentation site.

### For contributors

- Added repository-only Codex documentation translation and semantic-review
  skills, shared maintenance rules, and workflow-diagram generation and checks.
  These maintenance tools remain outside user-project installation and packages.
- Added installation discovery, migration, preservation and cross-platform CLI
  tests, plus requirements, design and review records. Strengthened checks for
  documentation paths, generated resources and package boundaries.
- Updated marketplace metadata for the preceding v0.7.24 release and documented
  guarded release commits and recovery procedures.

## [0.7.24] - 2026-10-12

### Added

- Review standards now live in shared resources with a compact index, common rules,
  seven review dimensions, and language/framework checklists loaded when relevant.
  Reviews can expand coverage as actual behavior reveals unchanged dependencies or
  cross-language boundaries.
- Added default-on `workflow.auto_maintenance` and
  `codexspec config --auto-maintenance on|off`. The setting controls automatic
  implementation of substantiated maintenance suggestions independently of
  `auto_next`; suggestions remain visible when automatic implementation is off.

### Changed

- Selected-change reviews follow five passes through scope, contracts, behavior,
  risks and verification. Defect admission requires reachable triggers, attributable
  changes and concrete impact, and checks upstream guarantees and contrary evidence
  to avoid speculative defensive fixes.
- Repair workflows independently verify maintenance benefit and behavioral
  compatibility, retain unfinished work, and require a fresh complete review.
  Strict defect gates and whole-code quality assessment scoring are preserved.
- Codex and Claude share `.codexspec/review-code/`. Installation preserves project
  edits and extensions unless replacement is requested, validates the destination
  group before copying, and ships complete byte-identical resources.

### For contributors

- Mapped all 87 source-checklist items to general or conditional language checks;
  added configuration, report, installation, package and six offline evidence cases.
  The offline cases do not measure live-model review reliability.
- Updated eight-language user references, synchronized command installations and
  documented plugin root/component paths and the tag-first marketplace transition.
- Made Windows plugin fixtures explicitly read UTF-8 and compare symbolic-link
  targets using their observed before/after state.
- Updated marketplace metadata for the preceding v0.7.23 release.

## [0.7.23] - 2026-10-11

### Added

- Codex and Claude now receive guidance to recall relevant `.codexspec/specs/`
  history before substantive decisions and questions, in ordinary conversation
  and SDD workflows. Claude plugin startup provides the same guidance without
  requiring project initialization or a persistent CodexSpec CLI.
- Historical recall distinguishes unchanged requirements, later additions, and
  explicit changes while always honoring the user's latest explicit decision.
  Reading depth follows the task; sufficient background is reused to reduce
  repeated questions and unnecessary searches.

### For contributors

- Added context installation, policy, plugin, and package coverage, plus the
  feature's requirements, design, planning, and verification records. Validation
  distinguishes instruction delivery from measured autonomous-agent effectiveness.
- Replaced machine-specific usernames and paths in documentation examples with
  generic placeholders.
- Updated marketplace metadata for the preceding v0.7.22 release.

## [0.7.22] - 2026-10-11

### Fixed

- Invalid auto-dev helper requests no longer create the shared branch or worktree.
  Request validation now runs before ownership or workspace mutations.
- Auto-dev follow-up operations require the existing workspace instead of silently
  recreating it. Ownership renewal, assertion and release work without initializing
  a workspace; acquisition still creates one when needed.

### For contributors

- Added 24 regression cases covering invalid requests, ownership operations,
  missing workspaces and successful acquisition.
- Updated marketplace metadata for the preceding v0.7.21 release and documented
  the release procedure using guarded commits.

## [0.7.21] - 2026-10-11

### Added

- Codex and Claude project context, plus Claude plugin startup, now explicitly
  route authorized commits through `commit-staged` for complete messages based
  on the exact staging area.
- A shared commit guard ships with initialized projects and the Claude plugin.
  Direct commits require Git and Python 3.11+, without a persistent CodexSpec CLI.

### Changed

- Auto-dev feature commits and blueprint updates prepare their own indexes before
  staged analysis and pass complete messages to finalization. Existing ownership,
  path, locking and recovery protections remain in force.
- Contentful automatic merges wait for staged analysis and verification.
  History-only merges retain Git's default message while validating content and
  parents; fast-forwards create no commit. Hooks, signing and signoff are preserved.
- **Breaking for custom helper clients:** hidden commit and merge protocols now
  require analyzed snapshots or preparation IDs and complete messages. Refresh
  command installations together with the runtime. Changed staged content requires
  fresh preparation and analysis, including after hook modifications.

### Fixed

- Git stdin preserves exact UTF-8 bytes on Windows, preventing newline translation
  from changing prepared blueprint content or commit messages.

### For contributors

- Added regression coverage for staging isolation, stale analysis, native hook and
  signing behavior, merge options, recovery, CLI-free installation and UTF-8 transport.
- Synchronized command installations and documentation, and recorded the confirmed
  requirements and verification evidence.
- Updated plugin marketplace metadata for the preceding v0.7.20 release.

## [0.7.20] - 2026-10-10

### Changed

- **Breaking:** Renamed `spec-to-plan` to `design-to-plan` to match the confirmed
  design-to-plan stage. The old command is removed without an alias or forwarding
  entry. Update explicit invocations and custom automation to the new name.
- Workflow handoffs, command discovery, translations, and current documentation
  use the new name. Planner inputs, legacy-artifact handling, `plan.md` output,
  review behavior, and the existing Quick sequence are unchanged.
- Claude and Codex installation updates retire the selected integrations' old
  runnable entries after the replacement is available, preserve unrelated files,
  and report replacement or cleanup failures explicitly.

### For contributors

- Removed orphaned nested helper-script copies from the repository while retaining
  the active installed helper locations.
- Added installation-retirement and failure-path regressions; synchronized generated
  command artifacts and eight-language documentation.
- Recorded guidance for keeping repository-sensitive test fixtures outside Git checkouts.
- Updated plugin marketplace metadata for the preceding v0.7.19 release.

## [0.7.19] - 2026-10-09

### Added

- Review repair loops now reuse coverage for unchanged, unaffected evidence through
  `review-code --incremental-from`, while final acceptance still requires a fresh
  complete-feature review with a PASS verdict.
- Added `review.decided_by` and `codexspec config --decided-by reviewer|ask`.
  The default `reviewer` mode keeps existing defect admission; `ask` lets users
  resolve out-of-context scenarios once through confirmed OUT/CON requirements.
- Implementation loops retain neutral follow-up obligations and root-cause classes
  outside the repository, escalating recurring classes into systematic debugging.

### Changed

- **Breaking:** Review-result envelopes now use schema 3. Schema-1/2 results are
  rejected; update command installations and result consumers together. The
  resolver manifest schema remains unchanged.
- Verification mirrors require independent Git metadata, copied dependencies and
  imports resolved inside the mirror. Reviewers use fresh contexts as direct
  children of the coordinator on both supported hosts.

### Fixed

- Decision-mode configuration writes preserve unrelated YAML values and line endings
  across supported block, flow, quoted, null, alias and explicit-key layouts.
  Configuration display uses the writer's validation rules.
- An unusable incremental baseline falls back to a complete review. Incremental
  obligations are permitted by the reviewer isolation rules without exposing prior
  findings or conclusions.

### For contributors

- Live eval adapters parse successful host stdout separately from diagnostic stderr
  and reject nonzero host exits. Schema-3 parser, workflow, configuration and
  localization tests cover the updated contracts.
- Updated eight-language documentation, generated command forms and acceptance
  evidence; recorded checks for relocated Python environments.
- Updated plugin marketplace metadata for the preceding v0.7.18 release.

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
