# README workflow diagrams

These are repository-maintainer assets, not installed CodexSpec commands.

## Maintainer entrypoints

- Codex: `$codexspec:update-workflow-diagrams <requested change>`
- Claude Code: `/codexspec:update-workflow-diagrams <requested change>`

Both entries load this handbook. Examples: update a workflow stage and synchronize
all languages; improve the German review-card wording; add a confirmed connection
and check every theme. State the intended content/layout change in ordinary prose.
The entries do not publish or commit by themselves. This handbook also supports
manual maintenance without either assistant.

Author the Claude command in
`.claude/commands/codexspec/update-workflow-diagrams.md`; derive its Codex entry with
`python -m internal.maintainer_doc_skills --write`, verify with `--check` and the
repository's `--check-distribution` gate. Do not hand-edit the derived skill.

## Sources and outputs

- `template.drawio`: approved light/dark graph pages; no handwriting photo or private reference page.
- `catalog.json`: stable cell ID → English reference, protected tokens and seven translations. Every translation stores its reviewed English `source` and its `text`. `literal` labels (commands/paths) are shared without translation.
- `layout.json`: named shared geometry profiles and locale-specific scale, cell geometry and edge-waypoint overrides, shared by both themes. Retain the existing overall composition; decide on broader changes only after observing actual renders.
- `generated/<locale>.drawio`: eight generated editable files with native light and dark pages. Edit sources, not these outputs.
- `assets/workflow/` (from the repository root): 16 generated PNGs and an input/output freshness manifest.

The original Chinese diagram wording and rich formatting are preserved when the Chinese catalog matches its template text. Changed Chinese catalog text uses the same escaped plain-text renderer as other locales. Newlines control deliberate breaks; HTML in catalog text is escaped. German compound labels use explicit hyphenation where necessary. Commands, paths, PASS, P0–P3, candidate and vetted remain literal.

## Choose the source for the change

The catalog is the wording authority; the template supplies graph structure and
base appearance; layout profiles supply adaptations. The generator substitutes
reviewed text and renders files. It does **not** translate text automatically.

| Requested update | Edit | Synchronization needed |
|---|---|---|
| Change a concept or shared description | The affected catalog entry's `en`, protected tokens if needed, and all seven `translations` | Review each translation against the new English meaning before updating its `source` |
| Improve wording in one language without changing meaning | That locale's `text` under the existing cell ID | Preserve the current English baseline and other approved translations; review the changed wording and its layout |
| Add/remove a stage, label or connector | Both theme pages in `template.drawio`; catalog entries for labels; affected layout overrides/waypoints | Preserve existing IDs; add unique IDs for new concepts; remove obsolete catalog/override entries and dangling references |
| Change common appearance or base placement | Both template pages and the relevant shared layout profile | Preserve theme-specific colors and identical geometry within each locale |
| Adjust one language's wrapping or spacing | Its catalog newlines and `layout.json` locale overrides | Keep meaning and font readability; inspect both themes and neighboring connectors |
| Change image paths or README presentation | The corresponding README picture blocks and generator path rules together | Verify all eight READMEs, fallback images and full-size links |

For example, changing the meaning of `wf-title.en` requires reviewing
`wf-title.translations` for all seven locales. A German phrasing correction changes
only `wf-title.translations.de.text`; it does not require rewriting the other
languages. Regenerate all outputs in either case: unchanged outputs should remain
unchanged, and the shared freshness manifest must describe the complete set.

Geometry is applied in this order: scale the template, then apply the resolved
shared-profile and locale-specific overrides. A profile or locale override can
therefore hide a base-template geometry edit. Inspect the effective configuration
before moving a shape repeatedly. Shared-profile edits affect every locale using
that profile; an override is for a genuine local difference.

### Editing in the draw.io application

Open `internal/workflow_diagrams/template.drawio` when changing the shared graph.
Retain exactly the `light` and `dark` native diagram pages, with matching IDs,
connections and geometry. Save **uncompressed XML** with nested `mxGraphModel`
elements; if the application saves compressed page text, export uncompressed XML
back to the template before generating. Keep private reference/photo pages out.

Generated locale files are editable inspection copies, but generation overwrites
them. If a proposed change was made there, compare it with the generated baseline
and transfer its meaning, graph or geometry changes to the catalog, template or
locale overrides above. Do not replace the canonical template with one localized
output: that would bake its language and scaled geometry into every locale.

Chinese template rich text is retained only while its plain text matches the
Chinese catalog. When approved Chinese wording changes, update both theme labels
if their rich formatting should be preserved; otherwise the generator uses the
catalog's escaped text and explicit line breaks.

## Repeatable update procedure

1. Work in the selected feature/maintenance checkout under the repository's
   workspace rules. Inspect its current diff and run the baseline `--check` before
   edits. A pre-existing failure must be understood; do not regenerate over someone
   else's unfinished work merely to obtain a green check.
2. Identify the affected concepts and edit the sources listed above. For workflow
   or capability changes, verify current implementation and confirmed requirements
   before changing the diagram's meaning.
3. Review only the affected text semantically, then read each changed translation
   on its own for idiomatic expression. Apply the shared translation rules in
   `internal/references/doc-translation.md` and terminology in
   `docs/i18n/glossary.yml`. The Markdown translation commands do not accept this
   JSON catalog as a document selection; apply their language principles to the
   catalog directly. Do not change reviewed `source` values without reviewing text.
4. Finish source formatting first, then generate all eight editable files. Inspect
   the diff for unintended changes to labels, graph relationships and locale
   overrides. A routine wording update should not rewrite unrelated content.
5. Export all sixteen images, run the deterministic checks and targeted tests,
   then perform the rendered inspection below. Fix overflow in source geometry or
   natural wrapping and repeat generation/export; do not patch individual PNGs.
6. Check all README image references and theme selection. Existing paths normally
   need no README edits: replacing the generated images updates their display.
   Show changed areas and full-size paths for any requested visual confirmation.
7. Finish applicable repository checks before freezing the result for final review.
   If a formatter changes any input bound by the manifest, regenerate/re-export and
   recheck it before review. A source hash change alone is not evidence of an image
   change; compare actual output bytes or pixels and record what was observed.
8. Hand off the source edits and their generated files/assets together, with actual
   checks, per-language visual outcomes and any limitations. Commit/merge/push only
   within the session's existing authorization; this procedure grants none itself.

## Generate and verify

From the repository root:

```bash
uv run python -m internal.workflow_diagrams --write
uv run python -m internal.workflow_diagrams --render --drawio /path/to/drawio
uv run python -m internal.workflow_diagrams --check
uv run --extra dev python -m pytest tests/test_workflow_diagrams.py
```

On macOS the renderer defaults to `/Applications/draw.io.app/Contents/MacOS/draw.io`.
Export uses the draw.io desktop CLI, with explicit page selection, scale 1 and a
24-pixel border. `--render` requires current generated draw.io files and publishes
its manifest only after every export succeeds. A failed export, missing PNG or
changed inputs is an error. A stale manifest is not evidence of visual acceptance.

To change a label, update its English `en` and review every nonliteral locale.
Only then update each translation's `source` to that English text. Do not simply
refresh all source fields to suppress a stale-translation diagnostic. Preserve
approved Chinese phrasing unless the underlying content changes. Review both
semantic fidelity and natural target-language expression.

Every provided `parent`, `source` or `target` reference must identify an existing
cell; invalid references stop generation and name the element and attribute. Free
connectors may omit endpoints.

When changing the graph, update both theme pages consistently. Preserve cell IDs
for unchanged concepts; synchronize the catalog when adding/removing labels.
Each `locales` entry selects a named `profiles` baseline with `profile`. Optional
`scale` replaces that baseline scale; `cells` merges coordinates for each stable
cell ID; `points` replaces the complete waypoint list for each edge ID. Profile
changes affect every locale that uses it, while locale overrides remain isolated.
Review locale overrides and protected literal lists. Regenerate and re-render
all variants after source, layout or generator changes.

## Rendering environment and visual inspection

The accepted renderer is draw.io desktop 30.2.6 on macOS. Font families are Arial
for Latin languages, PingFang SC for Simplified Chinese, Hiragino Sans for Japanese,
and Apple SD Gothic Neo for Korean. Verify these fonts are installed before export.
Another environment may substitute fonts and must repeat layout and visual review.
PNG keeps the reviewed appearance independent of the README reader's installed fonts.
The 16 named workflow PNGs retain native resolution and have a dedicated 2500 KiB
pre-commit size limit, enforced on updates as well as additions. Other repository
files retain the existing 500 KiB added-file limit.

Export optional SVG inspection copies with draw.io's `--format svg`,
`--page-index 1` (or 2), `--svg-theme light` and `--embed-svg-fonts false`.
The diagnostic helper uses Playwright and an installed Chromium browser:

```bash
uv run --with playwright python -m internal.measure_workflow_svg /tmp/workflow/*.svg \
  --browser /path/to/chromium
```

The helper measures the actual exported HTML label bounds against their exported
shape bounds with a 3-pixel rounding tolerance. It fails when a label overflows or
no labels can be measured. It does not prove absence of all connector crossings,
font substitution or readability problems. The ordinary `--check` detects stale
sources/assets, missing translations, protected-token changes, independent box
intersections and missing README references; intentional container nesting is allowed.

Inspect **all 16 PNGs**, including dense areas and connectors, at native resolution
and in an actual README-style preview at representative window widths. Record the
sizes and limitations observed; there is no fixed 900-pixel README width rule.
Choose card proportions together with text direction. Horizontal review labels
use compact locale-specific heights; Chinese retains its approved vertical labels.
Inspect surrounding panel spacing as well as card interiors.
If a local label fails, adjust its language-appropriate breaks or geometry without
removing meaning or automatically shrinking fonts. Keep theme geometry identical.
Any proposal to restructure the whole diagram must be supported by rendered evidence.

Each README uses its own light/dark PNG in a `picture` block plus full-size links.
The source graphic can be read in full detail through those links. Check both theme
selection and the light fallback. Do not broaden package/init allowlists for these
sources, scripts, fonts or images.

The documentation site reuses these same PNG files through
`hooks/workflow_assets.py`; do not copy another source set into `docs/`.
After updating assets, run `uv run mkdocs build --strict` and preview all eight
home pages in both themes. The site uses Material theme-specific image links,
so test its manual theme toggle as well as initial theme selection.

## Troubleshooting and completion

| Check or observation | Recovery |
|---|---|
| Missing/stale translation or protected-token error | Use the named cell and locale to review the real text; repair the translation, then update its reviewed English `source` |
| Unknown catalog/layout cell or graph reference | Reconcile both template pages, catalog IDs and layout/waypoint overrides; preserve valid free connectors |
| Stale generated diagram | Regenerate from the reviewed source files, then inspect the diff |
| Stale source/output manifest | Re-export after finishing source formatting; never hand-edit hashes to hide drift |
| Renderer failure, timeout or missing font | Correct the renderer path/environment, then repeat the complete export and inspect outputs; retained old images are not fresh acceptance evidence |
| Overflow, obstructed connectors or excessive whitespace | Adjust natural line breaks, card proportions and nearby spacing; inspect all affected locales and both themes again |
| Unexpected diff in an untouched language | Check shared-profile inheritance, template scaling and accidental catalog edits before accepting it |

A completed update has eight editable files, sixteen current images and a matching
manifest; faithful natural translations; no unreviewed overflow/overlap; and eight
working README picture blocks. Record exact commands and results, render environment,
changed cell IDs/locales, observed readability and any outstanding decision. Keep
rejected renders and temporary SVG/browser previews outside the published assets.
The source manifest proves freshness, not that semantic or visual review occurred.
