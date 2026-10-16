# Design: Multilingual Workflow Diagrams

**Status**: Ready for review. **Authority**: requirements.md and spec.md in this feature.

## Architecture & Components

### D-01: Template and catalogs

**Covers: REQ-001, REQ-002, REQ-005, NFR-001, NFR-002**

`internal/workflow_diagrams/template.drawio` stores only the approved light/dark graph pages; omit the reference photo page. `catalog.json` maps existing stable cell IDs to English text, protected literal tokens and seven locale translations with their reviewed English source. Rich text is generated from escaped plain lines; explicitly approved Chinese HTML can be retained from the template. Catalog text is never interpreted as executable markup. The source uses stable IDs, not English wording as identity. The footer retains the version basis and workflow summary but omits the private-photo reference.

### D-02: Locale layout

**Covers: REQ-001, REQ-003, REQ-006, NFR-002**

`layout.json` defines per-locale geometry overrides, preserving the existing overall regions, horizontal workflow and lower knowledge loop. Widen/heighten affected local boxes and move related waypoints together where rendered text requires it. Chinese character-stacked review labels remain; other locales use compact horizontal cards with language-specific heights, preserving all seven dashed arrows and top-aligned text. Card height follows actual rendered label height. Tighten the implementation panel and the gap before the lower knowledge section together so that shorter cards do not merely transfer excess whitespace to their surroundings. Themes share every geometry override. Never shrink fonts automatically to fit. Do not globally recompose based on a hypothetical README width; inspect actual renderings first (DEC-002).

### D-03: Maintainer generator and checks

**Covers: REQ-001, REQ-002, REQ-003, REQ-005, REQ-006, NFR-001**

`internal/workflow_diagrams.py` uses Python standard-library XML/JSON operations. `--write` generates `internal/workflow_diagrams/generated/<locale>.drawio` (two native editable pages per locale). `--check` compares expected bytes with generated files and validates catalogs, graph identity, geometry parity, README references and an export manifest. Missing/extra keys, stale reviewed source or changed protected tokens fail with locale/ID diagnostics.

`--render --drawio PATH` invokes the local draw.io CLI with explicit theme/page and PNG exports into `assets/workflow/`. PNG avoids SVG foreignObject/font rendering differences in GitHub images; editable source is supplied separately. SVG exports may be used as temporary inspection evidence. Export timeouts or failed commands are errors, never validated output. Hash-based manifest binds display assets to their input bytes and output bytes so stale images are detectable without invoking a graphical renderer in ordinary checks.

A maintainer-only browser inspection helper measures HTML text using the same installed fonts and captures actual renderer outputs. Geometry checks flag crossing/overlapping independent shapes while allowing intentional containment. Connector obstruction is inspected on the actual exports; automation must not claim complete route/collision proof. A visual report identifies all 16 variants and actual display sizes inspected.

### D-04: README integration and maintenance guide

**Covers: REQ-004, NFR-001, NFR-002**

Insert one theme-aware picture block after each README's SDD stage illustration, using its locale PNG, localized alt text and an explicit full-size link. `<source media="(prefers-color-scheme: dark)">` selects dark, with light fallback. `internal/workflow_diagrams/README.md` documents editing, source freshness, generation, required renderer/fonts and validation limitations. Classify `assets/workflow/` as repository documentation images outside packaging/init, and internal sources as maintainer-only in the repository layout guide. The 16 explicitly named native-resolution PNGs use a dedicated 2500 KiB pre-commit limit; other added files keep the existing 500 KiB limit. This accommodates the inspected 1.4–2.1 MiB exports without reducing legibility. No public templates, commands, installation code or dependency allowlists change.

### D-05: Shared maintenance procedure and host entrypoints

**Covers: REQ-007, REQ-002, REQ-005, NFR-001**

Keep the complete procedure in `internal/workflow_diagrams/README.md`. A short
repository-only `update-workflow-diagrams` Claude command loads it; the existing
`internal.maintainer_doc_skills` renderer derives its native Codex skill. Extend
the exact internal-entry inventory and distribution consistency check without
adding a public template or changing package/init behavior. The two host entry
bodies share one authored source and do not duplicate the update procedure.

The guide separates shared wording, locale-only wording, graph changes and local
layout changes. It documents uncompressed XML, stable IDs, override precedence,
manual translation review, all-variant regeneration, format-before-export ordering,
rendered acceptance and failure recovery. Generated copies are not source inputs.

## Key Design Decisions

### ADR-001: Explicit reviewed source, not silent fallback

**Covers: REQ-002, REQ-005**
Each translation records the English text it was reviewed against. A changed reference makes stale translations visible even when IDs remain stable. Exact matching is simple and reviewable; maintainers explicitly re-review translated meaning rather than blindly updating hashes.

### ADR-002: Native draw.io plus PNG

**Covers: REQ-001, REQ-004, REQ-006**
Use the installed draw.io CLI (verified version 30.2.6, supports export/page-index/PNG/SVG). Keep editable source separate from display images. PNG increases asset size but preserves fonts, line breaks and appearance in README consumers. Use readable native resolution and click-through access; record scaled-display observations without inventing a fixed README width.

### ADR-003: Local geometry overrides and actual inspection

**Covers: REQ-003, REQ-006, NFR-002**
Retain the existing global composition. Geometry overrides are data shared by both themes, not duplicated theme-specific edits. Browser measurements are a diagnostic aid; actual draw.io exports and human visual inspection remain the acceptance evidence.

## Requirements Coverage

| Requirement | Design |
|---|---|
| REQ-001 | D-01, D-02, D-03, ADR-002 |
| REQ-002 | D-01, D-03, ADR-001 |
| REQ-003 | D-02, D-03, ADR-003 |
| REQ-004 | D-04, ADR-002 |
| REQ-005 | D-01, D-03, ADR-001 |
| REQ-006 | D-02, D-03, ADR-002, ADR-003 |
| REQ-007 | D-05 |
| NFR-001 | D-01, D-03, D-04 |
| NFR-002 | D-01, D-02, D-04, ADR-003 |

## Risks and Limits

Different installed fonts can change text metrics. Pin the font families used for acceptance in the visual report, check availability before rendering, and repeat visual review on a new environment. No generic no-overlap claim can substitute for observing all exported variants. Overall restructuring is deferred pending real evidence, not silently authorized by this design.
