# Implementation Plan: Multilingual Workflow Diagrams

## Context and Boundaries

Implement design.md, preserving the approved overall composition and complete meaning. All sources and tools are repository-only. Do not modify public installation behavior, create a release or translate site pages.

## P-01: Sources and faithful catalogs

**Covers: REQ-001, REQ-002, REQ-003, REQ-005, NFR-001, NFR-002; Design: D-01, D-02**

Import the two approved pages without the photo/reference page. Establish stable-ID English reference text, preserve approved Chinese wording and author natural translations for six other locales. Define only the locale geometry overrides required by actual measurements/exports. Verify every original label and protected token is represented. Paths: `internal/workflow_diagrams/{template.drawio,catalog.json,layout.json}`.

## P-02: Generator and deterministic validation

**Covers: REQ-001, REQ-002, REQ-003, REQ-005, REQ-006, NFR-001; Design: D-03**

Use test-first implementation for `internal/workflow_diagrams.py` and `tests/test_workflow_diagrams.py`. Cover complete generation, catalog errors, geometry/theme parity, stale draw.io/assets and renderer failure. Add the maintainer browser measurement helper with tests for real overflow diagnostics where applicable. Generate eight editable two-page files. Render all 16 PNGs through draw.io, bind outputs to source/output hashes in a manifest and inspect each export. Refine local geometry and repeat affected renders.

## P-03: README integration and acceptance

**Covers: REQ-004, REQ-006, NFR-001, NFR-002; Design: D-03, D-04**

Add localized picture/full-size links to all eight root READMEs. Document workflow and font/render requirements in `internal/workflow_diagrams/README.md`; update `docs/internal/repository-layout.md` for repository-only assets. Run source/catalog/geometry/export/link checks, targeted tests, lint and the full project suite before final code review. Record actual render inspection, language fidelity and scaled-view limitations in this feature's `visual-review.md`. Further global layout decisions require rendered evidence.

## P-04: Frequent-update maintenance handoff

**Covers: REQ-007, NFR-001; Design: D-05**

Expand the existing update guide and add the authored Claude maintenance command
plus its generated Codex counterpart. Extend the existing internal entry inventory,
maintainer guidance and distribution consistency tests. Exercise generation/drift
checks for the new entry and verify it remains absent from public installations.
Walk through representative wording, graph and layout requests against the guide.
Complete all edits and deterministic checks before the final complete review.

## Plan-Level Decisions

Author translation sources before generator completion so tests use representative multilingual input. Implement code with failing tests first; static catalog/assets/docs use direct editing and deterministic checking. Draw.io rendering is local maintainer validation, not a new installed dependency or a mandatory graphical CI dependency. The manifest provides deterministic stale-output checking without pretending to replace visual review.

## Verification and Risks

Test missing/extra labels, stale source, protected token corruption, theme geometry identity, output drift, bad links and renderer failure. Inspect every language/theme at native resolution and representative actual preview widths; preserve observations rather than a blanket readability claim. Browser text metrics may differ from export; actual image evidence takes precedence. Run full suite before strict complete-feature review as required by implement-tasks.

## Coverage

| Requirement | Plan / Design |
|---|---|
| REQ-001 | P-01/02 / D-01/02/03 |
| REQ-002 | P-01/02 / D-01/03 |
| REQ-003 | P-01/02 / D-02/03 |
| REQ-004 | P-03 / D-04 |
| REQ-005 | P-01/02 / D-01/03 |
| REQ-006 | P-02/03 / D-03/04 |
| REQ-007 | P-04 / D-05 |
| NFR-001 | P-01/02/03 / D-01/03/04 |
| NFR-002 | P-01/03 / D-01/02/04 |

No blocking open items. P-01 precedes P-02; rendered outputs precede final acceptance in P-03.
