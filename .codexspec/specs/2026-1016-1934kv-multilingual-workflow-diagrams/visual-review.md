# Render and Translation Review

## Scope and environment

Eight locale draw.io files, each with light/dark pages, generate all 16 PNGs in
`assets/workflow/`. Source: approved workflow pages, without the reference photo.
Renderer: draw.io desktop 30.2.6 on macOS; Latin Arial, Chinese PingFang SC,
Japanese Hiragino Sans, Korean Apple SD Gothic Neo. Native PNG sizes: 3213 × 2330
for Chinese; 5294 × 2701 for the other locales. Fonts were observed rendering
complete CJK glyphs in the exports; no replacement boxes were observed.

## Observed repairs

- Initial English output overflowed the narrow review labels and several fixed-height descriptions. Locale geometry now provides space without reducing font sizes or changing the overall composition.
- Chinese keeps the approved rich-text formatting; flattening it had increased several labels' height. The analyze/traceability row now has matching 60-unit heights.
- The history-retention connector originally crossed longer translated section titles. It now follows the right-side whitespace and enters the history box below the context title.
- Korean keeps complete words together. German compounds use explicit line-end hyphenation in the review pillars.

## Actual rendered text bounds

`internal.measure_workflow_svg` measured actual draw.io SVG inspection exports
for both themes. Each exported page exposes 72 labels. Total: **1152 labels**;
**zero overflow findings** with the documented 3-pixel rounding tolerance.
The SVG copies are inspection intermediates; PNGs are the public assets.

| Locale | Labels measured (light / dark) | Overflow (light / dark) | PNG inspection |
| --- | --- | --- | --- |
| en | 72 / 72 | 0 / 0 | Both inspected |
| zh-CN | 72 / 72 | 0 / 0 | Both inspected |
| ja | 72 / 72 | 0 / 0 | Both inspected |
| ko | 72 / 72 | 0 / 0 | Both inspected |
| de | 72 / 72 | 0 / 0 | Both inspected |
| fr | 72 / 72 | 0 / 0 | Both inspected |
| es | 72 / 72 | 0 / 0 | Both inspected |
| pt-BR | 72 / 72 | 0 / 0 | Both inspected |

The initial 16 PNGs were viewed for overall flow, text clipping, overlapping content,
connector obstruction and theme contrast. The dense review area was also inspected
at native resolution, including the final Korean word-wrap change. Seven separate
top-aligned rectangles and their dashed arrows remain in every variant. Light and
dark geometry equality is covered by generation validation and tests.

## README-style browser preview

The actual picture blocks from all eight READMEs were loaded in local browser
previews. At a 1440 × 1000 viewport, the preview article used a 1012-pixel maximum
content width. All 16 language/theme selections resolved to the expected PNG and
loaded successfully. English and Chinese screenshots were observed in light and
dark themes; a 768-pixel viewport provided a narrower English example.

The wide diagram remains useful as an overview when scaled, but its fine print is
not comfortably readable at these reduced sizes. Full-resolution images preserve
readable details and each README provides full-size light/dark links. This is a
recorded presentation limitation, not a claim that all details are readable at any
viewport. There is no fixed 900-pixel README rule. Per DEC-002, preserve the current
overall composition; broader restructuring remains a decision based on these real
observations, not an automatic change in this feature.

## Fidelity and natural expression

All 61 translated labels were compared to their English reference and the approved
Chinese source; 11 literal command/path labels are shared. All seven translations
have matching reviewed-source records and preserve their protected tokens. The
phrasing follows the target language rather than copying English sentence order.
The original Chinese wording is retained, except the explicitly excluded reference
to the original handwritten photo. README alt text and full-size captions are
localized. The README verification helper reports no errors for any of seven pairs.

## Limits

Text-bound checks are not a proof of all possible connector intersections, glyph
substitution or human readability. Independent-box checks allow intentional panel
containment. Visual observation complements these checks. A font, template, label
or generator change requires fresh exports and inspection; the asset manifest
catches stale source/output bytes, not unperformed human review.

## Accepted compact review-card layout (DEC-003)

The user clarified that visual balance, not a fixed writing direction, is the goal.
Non-Chinese review cards retain their 180-unit width and existing font sizes but
use heights based on the measured text: 108 for English/German/French, 84 for
Japanese/Korean, and 132 for Spanish/Brazilian Portuguese, instead of 300.
All seven cards within a language share a height. Their top alignment, text and
seven dashed connections remain unchanged. The implementation panel is 200 units
shorter, and the entire lower knowledge section moves upward by 200 units with its
waypoints. This avoids transferring the removed card whitespace to a large gap
below it. Chinese output is pixel-identical to the previously inspected versions.

All 16 variants were exported again. Fresh actual-SVG measurements cover 1152
labels with zero overflow. Independent-box intersection checks pass in all eight
languages. The seven updated light-theme detail crops and all seven dark-theme
detail regions were inspected, and the English full diagram was observed for
composition and connectors. Local preview crops are in `previews/`; they provide
visible comparison with the original tall English cards. The 19 existing targeted
tests and source/output freshness checks pass. The user explicitly accepted this
rendered result: “很好。效果不错。我已经确认效果”. The earlier complete-feature
review fingerprint does not cover these revised files; the final gate records
belong to the exact revised target and are stored outside the repository.

## Final generator validation

The generator rejects provided parent/source/target references to absent cells,
while retaining free connectors without endpoints. All 22 targeted tests pass.
After this validation change, all 16 PNGs were exported again and are byte-identical
to the visually accepted assets. The refreshed manifest binds them to the current
generator; the accepted visual result is unchanged.
