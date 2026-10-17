# Implementation Plan: Project Installation Discovery and Upgrade

**Authority**: [requirements.md](requirements.md), [spec.md](spec.md), [design.md](design.md)
**Status**: Ready for Tasks

## Context and Goals

Implement design C1–C6 without changing its boundaries. Add offline scan and safe
interactive/automatic upgrades, including legacy installations and worktrees.
Do not add backup management, global CLI upgrades or Git mutations. The existing
init behavior remains the installation renderer, with verified metadata publication.

## Repository Constraints

Use src/codexspec for runtime code. Public templates and shipped script allowlists
remain unchanged unless a verified implementation need requires their source edits.
Do not edit installed .claude/.agents copies by hand. Preserve current language,
configuration and context behavior. Use the feature worktree for every edit and
check; fixtures and isolated rendering directories live outside Git checkouts.

## Plan-Level Decisions

- Build expected-content/metadata support first so discovery and upgrade share a
  single installation representation. Then implement discovery, safety/application,
  release worker, and CLI orchestration. This order makes pure behavior testable
  before network execution. Covers: REQ-002–014; Design: C1–C6.
- Use test-first changes for executable behavior and ordinary edits for docs.
  Existing pytest, Ruff, packaging and distribution checks are sufficient; no new
  testing framework. Mock network boundaries in unit tests, but exercise real Git,
  real temporary rendering and the private worker in integration tests.
  Covers: NFR-001, REQ-008–013; Design: C3–C5.
- No release/version bump, commit, merge or push is part of implementation unless
  separately authorized. Verify the proposed runtime with controlled artifacts;
  do not upgrade the user's unrelated repositories during development.
  Covers: NFR-001, NFR-002; Design: C3–C5.

## Implementation Phases

### P1: Metadata and rendering baseline

Add installations/metadata.py and render.py, plus package `__init__.py`. Reuse existing
installers in temporary output to generate expected complete artifacts and managed
projections. Add the init finalization hook only after its existing writes succeed;
verify output before metadata publication, including preserved nonforce files.
Tests: tests/test_installation_metadata.py and relevant existing init tests.

Covers: REQ-005–007, REQ-012, REQ-014, NFR-001; Design: C1, D1, D4.

### P2: Offline discovery

Add installations/discovery.py with bounded traversal, content inspection and Git
repository grouping. Cover legacy, checksum mismatch, worktrees, nested projects,
links and incomplete scans. Tests: tests/test_installation_discovery.py.
Depends on P1.

Covers: REQ-002–004, REQ-006–007; Design: C2.

### P3: Checked update plans and safe application

Add installations/upgrade.py for isolated input snapshots, target-result validation,
complete plan derivation, affected-path Git protection and metadata-last application.
Test with generated local plans before involving remote acquisition. Preserve
configuration and user content; report partial writes precisely.
Tests: tests/test_installation_upgrade.py with real temporary Git repositories.
Depends on P1.

Covers: REQ-009–014, NFR-001–002; Design: C4, C5, D2–D4.

### P4: Target release and private worker

Add installations/release.py and worker.py. Resolve one stable version, create
isolated runtime and validate target/protocol. Render only into temporary project
snapshots. Integration-test target worker output with actual source/package rendering
and network acquisition with controlled HTTP/process responses. Cover unsupported
protocol and environment/install failures before project writes.
Tests: tests/test_installation_release.py and worker tests.
Depends on P1 and P3.

Covers: REQ-008–009, REQ-012–013, NFR-002; Design: C3, C4, D2.

### P5: Public CLI integration

Add installations/cli.py and thin scan registration in `src/codexspec/__init__.py`.
Wire tables, prompts, deterministic project selection, exit semantics and summaries.
Add language strings using the existing translator fallback/catalog pattern.
Tests: tests/test_scan_cli.py with dependency injection at release boundary and real
scan/safety paths. Depends on P2–P4.

Covers: REQ-001, REQ-004, REQ-013–014, NFR-001–002; Design: C6.

### P6: Documentation and release-boundary validation

Update README.md, docs/en/reference/cli.md and CLAUDE.md with the three public
forms, independent version/consistency meaning, legacy behavior and skip reasons.
Verify generated/distribution boundaries and wheel inclusion of runtime modules.
Run relevant tests, full test suite, Ruff, distribution check and diff whitespace
check. Complete the mandatory independent final code-review gate and fix verified
defects through the repository debug workflow. Depends on P1–P5.

Covers: REQ-001–014, NFR-001–002; Design: C1–C6.

## Verification Strategy

- Assert read-only scans and every preflight skip with before/after file snapshots.
- Compare expected behavior, not just table strings or manifest existence.
- Exercise real Git staging/worktree states, missing Git, ignored/untracked files,
  deleted tracked files and hidden-index flags; use isolated author identities.
- Include same-version partial discard, legacy migration, language/integration
  preservation and protected custom context bodies.
- Test last-step metadata publication and per-project failure continuation.
- Real runtime worker integration validates renderer and protocol assumptions;
  remote tests are controlled and do not mutate user projects.
- Run each task's identified scenarios and record evidence in tasks.md.

## Risks and Trade-offs

Target Python/dependency incompatibility is a no-write acquisition error. Existing
untracked installations may be skipped because user content cannot be protected
reliably through Git. This follows confirmed safety priority, not a migration
failure to be bypassed. External concurrent writers prevent absolute multi-file
atomicity; detect stale preparation and report partial application without claiming
rollback. No user recovery feature is added.

## Requirements Coverage

| Requirement | Design | Plan |
| --- | --- | --- |
| REQ-001 | C6 | P5, P6 |
| REQ-002 | C2 | P2, P6 |
| REQ-003 | C2 | P2, P6 |
| REQ-004 | C2, C6 | P2, P5, P6 |
| REQ-005 | C1 | P1, P6 |
| REQ-006 | C1, C2 | P1, P2, P6 |
| REQ-007 | C1, C2 | P1, P2, P6 |
| REQ-008 | C3 | P4, P6 |
| REQ-009 | C3, C4 | P3, P4, P6 |
| REQ-010 | C4, C5 | P3, P6 |
| REQ-011 | C5 | P3, P6 |
| REQ-012 | C1, C4, C5 | P1, P3, P4, P6 |
| REQ-013 | C5, C6 | P3, P4, P5, P6 |
| REQ-014 | C1, C4, C6 | P1, P3, P5, P6 |
| NFR-001 | C4, C5 | P1, P3, P5, P6 |
| NFR-002 | C3, C5 | P3, P4, P5, P6 |
