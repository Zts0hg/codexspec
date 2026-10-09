# Implementation Plan: Remove orphaned nested script copies

## Context, Goals, and Non-Goals

Deliver design.md C1/C2 on the current main baseline using the existing Python/pytest,
uv, Bash and package build tooling. Scope remains the six deletions plus feature evidence.

## Plan-Level Decisions

- Use a dedicated feature checkout created by the worktree helper; preserve caller stash.
- Perform the reference audit before integrating `7fdfe17`; reuse existing behavioral
  tests and executable smoke probes because no new runtime behavior is implemented.
- Build fresh wheel/sdist and enable archive tests with `CODEXSPEC_DIST_DIR`.
- Freeze evidence before the independent complete-feature review. Merge and synchronize
  only after the gate passes. CI workflow path filters may omit a deletion/docs-only
  change; record that result rather than inventing a green platform-matrix run.

## Implementation Phases

1. P1 Audit consumers: exact/normalized path searches and inspection of dynamic source
   selection, sibling imports, callers, and packaging. Classify historical references.
   Covers: REQ-001; Design: C1, D1.
2. P2 Remove copies: merge the old cleanup commit into the feature checkout; inspect the
   resulting delta and ensure supported source/flat files and packaging are unchanged.
   Covers: REQ-002; Design: C1, D1.
3. P3 Verify: run existing installer, Bash/helper, packaging tests and installed-script
   smoke probes; build/inspect archives; run full pytest, distribution checks, and
   applicable lint/document/security hooks. Record commands, outcomes, and skips.
   Covers: REQ-001, REQ-002, REQ-003; Design: C1, C2.
4. P4 Integrate: complete independent review, commit evidence, fast-forward main where
   possible, push without force, and check remote SHA and applicable CI results.
   Covers: REQ-003; Design: C2, D2.

## Risks and Recovery

- Active caller discovered: stop deletion; do not broaden scope into a migration.
- Check failure: diagnose before integration; preserve original branch and stash.
- Native Windows unavailable locally: record skips and simulated installation coverage;
  unchanged PowerShell sources and package-byte checks supplement but do not replace
  a native platform run.
- Remote main advances: fetch and integrate safely, then revalidate affected evidence.

## Requirements Coverage

| Requirement | Design component | Plan phase |
| --- | --- | --- |
| REQ-001 | C1, D1 | P1, P3 |
| REQ-002 | C1, D1 | P2, P3 |
| REQ-003 | C2, D2 | P3, P4 |
