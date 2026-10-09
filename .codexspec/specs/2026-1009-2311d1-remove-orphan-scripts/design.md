# Design: Remove orphaned nested script copies

## Context

Implement REQ-001–003 from spec.md without changing runtime architecture.

## Architecture & Components

### C1 — Supported script installation and execution

- Responsibility: `get_scripts_dir()` selects packaged scripts or repository `scripts/`;
  `init` copies platform sources by filename into flat `.codexspec/scripts/`.
  Shell helpers load their sibling `common` file relative to their own location.
- Change: remove only the six obsolete nested copies after checking consumers.
- Covers: REQ-001, REQ-002.

### C2 — Maintenance evidence and integration

- Responsibility: feature-local SDD records identify scope, historical cleanup commit,
  reference audit, executable verification, independent review, and integration conditions.
- Covers: REQ-003.

## Key Design Decisions

### D1 — Delete unused copies; preserve the supported sources

- Context: the installer reads `scripts/`, not this repository's `.codexspec/scripts/`.
- Decision: retain authoritative sources and flat copies unchanged. Historical prose may
  continue to name removed files; it is not an executable dependency.
- Alternatives: rewire callers or migrate installation paths only if the audit finds an
  active consumer; that would require revisiting the bounded deletion scope.
- Trade-off: no compatibility wrapper for an undocumented obsolete nested path.
- Covers: REQ-001, REQ-002.

### D2 — Reuse the historical deletion with current evidence

- Decision: integrate original commit `7fdfe17` on the prepared feature branch after the
  consumer audit, preserving its history; add current evidence and gate main integration.
- Trade-off: an old commit alone is not proof against the current baseline.
- Covers: REQ-003.

## Requirements Coverage

| Requirement | Design coverage |
| --- | --- |
| REQ-001 | C1, D1 |
| REQ-002 | C1, D1 |
| REQ-003 | C2, D2 |
