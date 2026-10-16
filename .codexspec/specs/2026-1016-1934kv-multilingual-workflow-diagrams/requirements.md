# Confirmed Requirements: Multilingual Workflow Diagrams

- **Feature ID**: `2026-1016-1934kv`
- **Status**: Confirmed
- **Last Confirmed**: 2026-10-17

## Authority

Only confirmed entries are binding. Current explicit user decisions take precedence over historical requirements. Document and code paths below are relative to the selected feature workspace unless stated otherwise.

## Needs

### NEED-001: Eight language versions

- **Status**: confirmed
- **Statement**: Provide the existing workflow diagram in English, Simplified Chinese, Japanese, Korean, German, French, Spanish, and Brazilian Portuguese.
- **Rationale**: Readers of every root README should see the standardized requirements-first SDD workflow and experience iteration loop in their language.
- **User Evidence**: “是否可以将drawio的内容也做成八种语言以便放入各个语言的REAME中”; final summary confirmed with “确认”.

### NEED-002: Repeatable generation

- **Status**: confirmed
- **Statement**: Maintain a diagram template, an English-to-locale text catalog and a generation script. Produce editable draw.io diagrams and images for README display.
- **User Evidence**: “drawio 的代码 + 英文对照到各个语种的对照表 + 替换脚本”; final summary confirmed.

### NEED-003: Integrate every README and both themes

- **Status**: confirmed
- **Statement**: Produce eight languages in light and dark themes (16 display variants) and integrate the matching variants into all eight root READMEs with theme-aware selection.
- **User Evidence**: Selected A: complete generation, checking and README integration in this feature; final summary confirmed.

### NEED-004: Repeatable maintenance for frequent updates

- **Status**: confirmed
- **Statement**: Provide a maintained update handbook and matching Codex/Claude Code maintenance entries, so future and frequent draw.io changes can be synchronized conveniently across the language variants while retaining their layout/readability checks.
- **User Evidence**: “drawio后续还会更新，甚至是频繁更新。所以需要考虑使用需要总结一个更新drawio的步骤文档或者skill来确保之后的更新能够保持方便同步改动到各个语言版本的特点？”
- **Relationship**: Extends NEED-002 and CON-003 with an operational handoff; retains repository-only tooling and the accepted visual output.

## Decisions

### DEC-001: Controlled locale-specific layout

- **Status**: confirmed
- **Decision**: Preserve workflow relationships, visual hierarchy, all seven review dimensions and their dashed arrows. Allow language-specific wrapping, box dimensions, spacing and local arrangement. Light and dark variants of the same language must use the same layout.
- **Alternatives Rejected**: One identical layout for all languages sized for the longest translation.
- **Reason**: Long translations and the existing narrow, character-stacked Chinese review pillars require language-appropriate layout for readability.
- **User Evidence**: Selected A for controlled locale adaptation; final summary confirmed.

### DEC-003: Visual balance takes precedence over fixed text direction

- **Status**: confirmed
- **Decision**: Choose text direction, card proportions, spacing and local arrangement for a balanced, attractive and readable result. Vertical writing is not mandatory. Avoid retaining tall containers when horizontal labels leave excessive empty space. Preserve seven distinct review dimensions and their clear relationship to code review; both themes share the adapted layout.
- **User Evidence**: “我并不是要求不能改变文字方向，而是希望美观”; “调整给我看看效果”.
- **Relationship**: Clarifies DEC-001 and the visual acceptance criteria in CON-002. DEC-002 still governs the overall workflow composition.
- **Confirmation**: Direct correction followed by an explicit request to render the adjustment for inspection; no additional confirmation is needed for this local revision.

## Constraints

### CON-001: Faithful, natural language

- **Status**: confirmed
- **Statement**: Preserve the approved diagram's content and workflow scope. Retain approved Chinese wording and establish an accurate English baseline. Use idiomatic target-language phrasing; preserve command names and paths. Do not omit meaning to fit the layout.
- **User Evidence**: Final summary confirmed. Earlier diagram instructions explicitly exclude auto-dev, auto-next arguments/configuration and the clarify command while emphasizing standardized SDD and the experience iteration loop.

### CON-002: Rendered readability acceptance

- **Status**: confirmed
- **Statement**: Check translation completeness, text overflow, overlapping content and connector obstruction. Render and visually inspect all 16 variants, including readability at README display size. Successful script execution or continually reducing font size is insufficient evidence of acceptance.
- **User Evidence**: “是否可能出现超出图形边界甚至与其他内容叠合导致难以浏览阅读”; final summary confirmed.

### CON-003: Maintainable synchronization

- **Status**: confirmed
- **Statement**: Shared content or template changes must support regeneration of all variants. Report missing translations and translations requiring updates explicitly, rather than silently mixing languages.
- **User Evidence**: Final summary confirmed.

## Out of Scope

### OUT-001: Repository documentation maintenance boundary

- **Status**: confirmed
- **Statement**: Maintain the workflow diagram and README integration only. Do not expand represented product functionality or translate site documentation. Original handwriting photographs and proofreading records are excluded from public display diagrams. Generation tools are repository-maintainer tools and must not enter installed user-project content.
- **User Evidence**: Final summary confirmed.

## Source and Historical Context

- Existing editable source at discovery: `/Users/xiaoming/Downloads/IMG_3933-drawio/codexspec-workflow-themes.drawio`; its light and dark workflow pages are the visual/content baseline. The photo/reference page is excluded from public display.
- `.codexspec/specs/2026-1013-1133ii-codex-docs-maintenance/requirements.md`: repository-only maintenance, seven root README translations, authored Claude and derived Codex entries.
- `.codexspec/specs/2026-1014-193481-readme-native-expression/requirements.md`: natural target-language expression and fidelity are separate checks; preserve approved Chinese wording.
- `.codexspec/profile/constraints/C-2026-0902-054178-1-maintainer-validation-before-user-install.md`: maintenance mechanisms must not become installation-time dependencies or failures.

## Open Questions

None blocking. OPEN-001 (README display density) is resolved by DEC-002. File organization, export format and local layout algorithms remain design decisions.

### DEC-002: Render the existing overall composition first

- **Status**: confirmed
- **Decision**: Retain the current overall structure for the initial implementation. Decide whether further overall layout adjustments are needed only after rendering and observing actual results. There is no fixed 900-pixel README width requirement.
- **Reason**: Hypothetical display-width calculations alone are insufficient grounds to redesign the diagram.
- **User Evidence**: “先沿用现在的整体结构，具体渲染之后是否需要调整需要实际渲染并观测后决定”.

## Confirmation Log

### 2026-10-16 — Layout policy

- **Summary Presented**: Permit controlled locale-specific adjustments while preserving workflow relationships, review dimensions and theme layout parity.
- **User Confirmation**: “A”.
- **Entries Confirmed**: DEC-001 (included again in final summary).

### 2026-10-16 — Delivery scope

- **Summary Presented**: Generate and check diagrams, then integrate light/dark variants into all eight READMEs in this feature.
- **User Confirmation**: “A”.
- **Entries Confirmed**: NEED-003 (included again in final summary).

### 2026-10-16 — Final discovery summary

- **Summary Presented**: Eight languages; template, catalog and script; editable diagrams and 16 themed display variants; controlled layout; README integration; faithful natural translations; rendered readability checks; missing/stale translation reporting; repository-only tooling and public-image exclusions.
- **User Confirmation**: “确认”.
- **Entries Confirmed**: NEED-001, NEED-002, NEED-003, DEC-001, CON-001, CON-002, CON-003, OUT-001.

### 2026-10-16 — Resolve display-density question

- **Summary Presented**: Keep the existing overall structure, perform locale adaptation and actual render inspection before deciding on overall changes.
- **User Confirmation**: “先沿用现在的整体结构，具体渲染之后是否需要调整需要实际渲染并观测后决定”.
- **Entries Confirmed**: DEC-002; OPEN-001 resolved. No requirement limits README width to 900 pixels.

### 2026-10-16 — Review-card visual balance

- **User Confirmation**: “我并不是要求不能改变文字方向，而是希望美观”; “调整给我看看效果”.
- **Entries Confirmed**: DEC-003 clarifies the local adaptation criteria. The rendered layout is provided for visual inspection.

### 2026-10-16 — Final visual acceptance and integration

- **User Confirmation**: “很好。效果不错。我已经确认效果”; requested README integration, local merge into main and remote push.
- **Entries Confirmed**: DEC-003 compact review-card layout is accepted. All eight README picture blocks already reference the corresponding accepted light/dark assets.
- **Integration Scope**: Commit the complete feature, merge locally into main and push after the required final review and validation. No product release or version change is included.

### 2026-10-17 — Future maintenance procedure

- **User Request**: Capture an update document or skill for frequent multilingual diagram updates.
- **User Selection**: “更新手册 + Codex／Claude Code 两套维护入口（推荐）”.
- **Entries Confirmed**: NEED-004. The implementation may reuse the repository's authored Claude/derived Codex maintenance-entry pattern and a single shared procedure; no additional product installation surface is requested.
