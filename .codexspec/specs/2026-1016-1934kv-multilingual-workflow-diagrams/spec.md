# Feature Specification: Multilingual Workflow Diagrams

## Context and Goals

The approved workflow diagram currently has Chinese light/dark pages outside the repository. Its stable cell IDs support a shared template and translations, but fixed Chinese character-stacked labels cannot safely carry longer Latin-language wording. Every root README needs a faithful, readable diagram in its language and active theme. The feature adds maintainer tooling and documentation assets, not installed product functionality.

## User Scenarios

1. A README reader sees the full requirements-first SDD workflow, reviews and experience loop in their README language, with a matching light or dark theme.
2. A maintainer changes a source label, sees which translations require review, updates them and regenerates all variants without manually duplicating diagrams.
3. A maintainer catches a long translation that overflows a box or obscures an arrow before publishing the image.

## Functional Requirements

### REQ-001: Complete language and theme coverage

**Sources: NEED-001, NEED-002, NEED-003**

Generate editable draw.io diagrams and README display images for `en`, `zh-CN`, `ja`, `ko`, `de`, `fr`, `es`, and `pt-BR`, each with light and dark themes. A complete build has all 16 display variants. Diagram workflow content is equivalent across variants.

**Acceptance**: Every locale/theme combination opens or renders successfully; generated editable diagrams retain native editable nodes and edges.

### REQ-002: Shared authoring and translation model

**Sources: NEED-002, CON-001, CON-003**

Maintain a reusable diagram template, English reference labels, locale translations and a script to regenerate outputs. Preserve approved Chinese wording and establish faithful English meanings. Use stable associations between graph elements and translated labels; preserve command names and paths.

**Acceptance**: A maintainer can identify a diagram label and its English/locale equivalents, update approved text, and regenerate affected outputs without manually editing each generated file. Translations use natural target-language expression without dropping propositions to fit.

### REQ-003: Controlled layout adaptation

**Sources: DEC-001, DEC-002, DEC-003, CON-002**

Retain the existing overall composition initially. Base any later overall adjustment on actual rendered observation, not a hypothetical fixed README width. Allow locale-specific wrapping, box sizing, spacing and local arrangements. Preserve workflow relationships, visual hierarchy, the seven review dimensions and their dashed arrows. Both themes of a locale share layout. Choose text direction and container proportions together; avoid excessive empty card space and judge visual balance on actual renders.

**Acceptance**: A long translation fits without clipping or colliding with neighboring content; the corresponding light/dark variants have equivalent geometry and connections. Seven review dimensions remain separate, readable elements connected to code review.

### REQ-004: Theme-aware README integration

**Sources: NEED-003**

Each root README references its own locale's light and dark display assets, selects them according to reader theme, and includes an accessible fallback.

**Acceptance**: All eight READMEs resolve their image links, use the correct locale, and select appropriate light/dark assets. Assets can be viewed at full size for detailed reading.

### REQ-005: Completeness and freshness diagnostics

**Sources: CON-003, CON-002**

Before accepting regenerated output, report missing translations and translations requiring review after source changes. Do not silently substitute another language for missing text. Shared template/content changes can regenerate all variants.

**Acceptance**: Removing a required translation or changing its English reference without reviewing the corresponding translation produces a concrete diagnostic identifying the label and locale. Stale generated outputs are detectable.

### REQ-006: Layout and rendered validation

**Sources: CON-002, DEC-001, DEC-003**

Provide checks for text overflow, content overlap and connector obstruction, and render every variant for visual inspection. Evaluate images at their README display size as well as full size; script success alone does not satisfy acceptance.

**Acceptance**: Known overflow or collision examples are detected by the applicable automated or visual check. The final report identifies automated coverage and limitations, all 16 rendered variants inspected, any adjustments made and the final readability result. Excessive shrinking or omitting meaning is not an acceptable fix.

### REQ-007: Reusable update procedure

**Sources: NEED-004, NEED-002, CON-003, OUT-001**

Provide one maintained procedure explaining source ownership, text/graph/layout
changes, translation review, regeneration, rendering, visual checks and recovery.
Distinguish canonical sources from editable generated inspection copies. Future
updates must not require manually maintaining eight independent diagrams.

**Acceptance**: A maintainer can follow a shared-wording change, single-language
wording correction, graph edit or local layout edit through to synchronized,
verified README assets. Both Codex and Claude Code entries load the same procedure; maintenance
entries remain outside public templates and installation.

## Non-functional Requirements

### NFR-001: Repository-only maintenance

**Sources: OUT-001**

Keep generation code, source catalogs and maintenance dependencies outside public CLI/template registration and installed project content. README images do not require a runtime translation service. No user installation behavior changes.

### NFR-002: Consistent content and presentation

**Sources: CON-001, CON-002, DEC-001**

Preserve the approved workflow and experience loop, semantic colors and hierarchy. Keep translations idiomatic and theme contrast readable. Layout adjustments must not alter workflow meaning or hide content.

## Expected Failure Behavior

- Missing/stale translation: identify locale and stable label, require correction/review, do not claim a complete build.
- Invalid template or disconnected label association: identify the relevant element and stop generation of accepted output.
- Missing renderer or fonts: explain the dependency and distinguish unrendered output from validated output.
- Overflow, overlap or obstruction: identify the affected variant and elements; adjust wrapping/geometry and repeat applicable checks before accepting.
- Stale output or broken README link: report the path and required regeneration/correction.

## Confirmed Constraints and Decisions

Controlled locale-specific layouts are intentional; global identical geometry is not required. Light and dark geometry within a locale is identical. Commands and paths retain their literal spellings. Reviewed Chinese wording is preserved while an English baseline supports maintenance. Manual visual checking complements automated measurements and does not become an unsubstantiated claim of perfect automatic layout detection.

## Out of Scope

No added product functions, site-document translation, auto-dev content, auto-next parameter/configuration content or clarify command content. Original handwritten photographs and proofreading records are not public display diagrams. No public installation mechanism or new installed command is introduced.

## Open Questions and Assumptions

No blocking open questions. Storage paths, export format and layout algorithms are design choices, not new product requirements. Availability of a renderer is to be verified during design.

## Requirements Traceability

| Confirmed entry | Specification coverage |
|---|---|
| NEED-001 | REQ-001 |
| NEED-002 | REQ-001, REQ-002 |
| NEED-003 | REQ-001, REQ-004 |
| NEED-004 | REQ-007 |
| DEC-002 | REQ-003 |
| DEC-003 | REQ-003, REQ-006 |
| DEC-001 | REQ-003, REQ-006, NFR-002 |
| CON-001 | REQ-002, NFR-002, Out of Scope |
| CON-002 | REQ-003, REQ-005, REQ-006, NFR-002 |
| CON-003 | REQ-002, REQ-005 |
| OUT-001 | NFR-001, Out of Scope |
