# Documentation site refresh validation

## Scope and provenance

Baseline: `05c773f2839a1d4a8777b2cff96e9c07962ca41f`.
The accepted root README and its seven translations supply the current product narrative.
Current command templates, CLI implementation and relevant confirmed historical requirements
supply detailed behavior. Root READMEs and workflow image bytes remain unchanged.

Updated 12 pages in each of eight locales (96 pages), locale navigation, build-time workflow
asset registration and its tests. The repository layout and diagram maintenance handbook
explain shared asset ownership. Historical case-study decisions are preserved as history.
There is no runtime feature, version change, commit or publication in this task.

## Content review

| Page (relative to `docs/en/`) | Assessed sections and propositions |
|---|---|
| `index.md` | Dual-host positioning, confirmed requirements, stage reviews, automation boundaries, quick start and theme images. |
| `getting-started/installation.md` | CLI/desktop/plugin installation, prerequisites, refresh and managed context preservation. |
| `getting-started/quick-start.md` | Host invocation syntax, separate design phase, review sequence, feature workspace and project layout. |
| `user-guide/workflow.md` | Requirements authority and traceability, review gates, automation, worktrees, blueprint, existing code, knowledge lifecycle and historical-decision example. |
| `user-guide/commands.md` | All 28 public commands, inputs and options, review contracts, scope selection, helper prerequisites, bounded remediation and output behavior. |
| `user-guide/i18n.md` | 13 runtime languages versus eight documentation locales, both maintenance hosts, terminology, mechanical versus semantic review and diagram reuse. |
| `reference/cli.md` | Six public CLI commands, init/config options, defaults, refresh preservation and read-only blueprint diagnostics. |
| `reference/configuration.md` | Language fallback, workflow switches, reviewer decision mode, defaults and checkout-local configuration. |
| `development/contributing.md` | Prerequisites, development/docs extras, test/build commands and authoritative authoring sources. |
| `development/scripts-architecture.md` | Host adapters, platform scripts, commit helper, feature IDs, managed context blocks, repository/package boundary and extension limitations. |
| `case-studies/case-study-pr-description-generator.md` | Historical context, original decisions and their reversal, examples, current-workflow navigation; old sequence and score remain historical. |
| `WINDOWS-TROUBLESHOOTING.md` | CLI version/check commands, uv shell/path diagnosis, restart requirements and evidence-based permission troubleshooting. |

The retained Python/React reviewer names are described only as plugin compatibility artifacts,
not members of the 28-command installation catalog. The quick workflow intentionally retains
its abbreviated stages; it is not presented as the full standard workflow.

## Translation review

Scope: `docs/en/<page>` → `docs/<locale>/<page>` for every page above and each locale below.
The final source hash table pins the reviewed English revisions. The corresponding target
uses the identical relative page path. This identifies all 84 source/target pairs.

The same agent performed a separate semantic-review pass following `check-i18n-semantics`
and returned concrete corrections to the translation workflow. This is an agent assessment,
not an independent human or native-speaker review. Reviewed README wording is reused where
applicable; retained detailed site sections were compared with the updated English source.
Fidelity and natural expression were assessed separately. Passing token/structure checks
are supporting evidence only, not proof of meaning or fluency.

| Locale / target root | Fidelity after repair | Natural expression after repair | Concrete findings repaired | Mechanical result |
|---|---|---|---|---|
| zh / `docs/zh/` | No unresolved drift found | No unresolved defect found | Restored current stage sequencing, staged-only commit behavior and clearer review prose; retained accepted README introduction | 12 pairs, 0 errors |
| ja / `docs/ja/` | No unresolved drift found | No unresolved defect found | Corrected next design step and the historical default/workflow causal relationship; localized labels and removed mixed Chinese text `変更场景` | 12 pairs, 0 errors |
| ko / `docs/ko/` | No unresolved drift found | No unresolved defect found | Corrected stage order and the historical causal relationship; repaired `다듓`, untranslated labels and unnatural expressions such as `빈틀` | 12 pairs, 0 errors |
| de / `docs/de/` | No unresolved drift found | No unresolved defect found | A skipped unavailable check had been described as termination; corrected authority terminology, `Was er passiert`, `Knapp Beschreibung` and unclear causal pronouns | 12 pairs, 0 errors |
| fr / `docs/fr/` | No unresolved drift found | No unresolved defect found | Replaced `authentique` with authority terminology where required; translated an English prose quotation and restored explicit missing-blueprint prerequisites | 12 pairs, 0 errors |
| es / `docs/es/` | No unresolved drift found | No unresolved defect found | Clarified commits versus confirmations, missing-blueprint prerequisites and the historical causal relationship; removed `Conflicta` and avoidable calques | 12 pairs, 0 errors |
| pt-BR / `docs/pt-BR/` | No unresolved drift found | No unresolved defect found | Restored explicit blueprint prerequisites and causal meaning; replaced literal `graciosamente` and awkward directory/URL phrases | 12 pairs, 0 errors |

Evidence locations: current command ordering and review behavior in
`docs/en/user-guide/commands.md` and its seven counterparts; explicit failure conditions in
`docs/en/reference/cli.md` under `codexspec show-blueprint`; the default that would disrupt a
real workflow in the historical case study's parameter-reversal explanation. Repairs preserve
command names, options, paths and examples. Fenced examples use the exact English source;
this is intentional under the repository translation rules, not an untranslated prose omission.

### Final English source hashes (SHA-256)

| Source | SHA-256 |
|---|---|
| `docs/en/WINDOWS-TROUBLESHOOTING.md` | `cf3626b8fe11bbf2f1f09682bebeca34758ef625dfed64b5101cf3d48c472cce` |
| `docs/en/case-studies/case-study-pr-description-generator.md` | `5d2cbefd2d283552ed185a32b296bf08e31f091e6381d5452716c5b0ba80935c` |
| `docs/en/development/contributing.md` | `5fc653e39c7c7dc7b24acb8e2d2e030fc6163c48870076dbca5391c5f860974e` |
| `docs/en/development/scripts-architecture.md` | `6733606c4e678ee5f1930c6d406c5900426ea669aeab5a36deaa502336868a1f` |
| `docs/en/getting-started/installation.md` | `04fc32a5b3203885e7f9f4e0d4d57153c4da62885f403f1b02fba4d5495bedf1` |
| `docs/en/getting-started/quick-start.md` | `1ff42325a9573de0718f4d074ccaaf62ff261ea470f081d3f68dd02818d2beef` |
| `docs/en/index.md` | `b0a81db2b73f59f412052cb52cdd0b1ca3e9ef4cee493dca025460481775f238` |
| `docs/en/reference/cli.md` | `bb6c8352c988b9ec78e58d0d27b876e406a9dbf130871cbaf85452b6cfbf2d29` |
| `docs/en/reference/configuration.md` | `882d025433e1d47828f2f2edf1362e758746f21c82a189be5335ef0674de0a75` |
| `docs/en/user-guide/commands.md` | `ec026ffa50f56d6157eb1e27ccb77bcefae3b28be51786dd9ceabd3f15c137a2` |
| `docs/en/user-guide/i18n.md` | `26105a460d3dec4951182076b088c4e857fc7e3ef56127bf5871a8a2f179dc8a` |
| `docs/en/user-guide/workflow.md` | `79c5beda485c1de5cdbe4b3f1105134340ce94a172fb1eba94cc53f1d5a5b7d2` |

## Executed validation

- `.venv/bin/python -B -m internal.doc_translation inventory --lang all`: 84 pairs selected.
- `.venv/bin/python -B -m internal.doc_translation verify --lang all`: exit 0; no mechanical errors.
- `.venv/bin/python -m mkdocs build --strict`: exit 0; all eight locales built, no build warnings.
- Targeted pytest modules: `test_docs_workflow_assets.py`, `test_review_code_docs.py`,
  `test_sdd_workflow_templates.py`, `test_maintainer_doc_tools.py`, `test_i18n_glossary.py`:
  **204 passed, 5 skipped**. Existing `PurePath.is_reserved()` deprecation warnings originate
  in `internal/command_template_fragments.py`; they do not fail the tests.
- Ruff check and format check for the new hook/test: passed.
- Markdownlint for changed documentation and `git diff --check`: passed.
- Built output contains exactly 16 workflow PNGs under the shared asset path.
  Hook tests verify byte-preserving copies, idempotent registration and missing-asset failure.
- Browser check: eight homepages × two widths (1440 and 390 pixels) × two manual theme
  settings = 32 combinations. Both image files load; only the matching theme is visible;
  no page-level horizontal overflow. Localized navigation and full-size image links are present.
- Additional mobile checks: Chinese configuration, French command reference and Japanese
  quick start; no page-level horizontal overflow. Chinese and French full-page screenshots
  inspected visually. Long code blocks/tables retain their internal scrolling behavior.

The diagrams keep the accepted README layout; readers can open the original full-size image
for small labels. Local browser diagnostics included unavailable per-locale sitemap requests
and GitHub metadata rate-limit responses; workflow assets loaded successfully. These existing
site integrations were not changed by the refresh. The site has been verified locally, not deployed.
