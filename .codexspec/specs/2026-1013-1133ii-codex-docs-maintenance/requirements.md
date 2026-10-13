# Confirmed Requirements: Codex Documentation Maintenance and README Translation

**Feature ID**: `2026-1013-1133ii`
**Status**: Confirmed
**Last Confirmed**: 2026-10-13

## Authority and Context

Only confirmed entries bind downstream work. Latest explicit user decisions
supersede earlier decisions about the same matter. This is separate work from
the completed English README audit.

The two maintainer commands currently live in `.claude/commands/codexspec/`.
They translate/check site documentation using `docs/en/`, seven localized
`docs/<lang>/` directories, and `docs/i18n/glossary.yml`. They have no native
Codex entrypoints or root README mapping. The English README in commit
`bdab1f3705daf5df6d5b11efdf17651f2b9efc94` is the translation baseline.

## Needs

### NEED-001: Native Codex entrypoints with Claude compatibility

- **Status**: confirmed
- **Statement**: Provide `$codexspec:translate-docs` and
  `$codexspec:check-i18n-semantics` as usable Codex skills, retaining existing
  Claude commands and consistent maintained rules across both hosts.
- **User Evidence**: "将这两个命令扩展到codex可以使用的命令。" The final confirmed
  summary names both Codex entries and Claude compatibility.
- **Confirmed At**: 2026-10-13

### NEED-002: Root README translation and semantic-check support

- **Status**: confirmed
- **Statement**: Extend both commands with root README source/target mapping and
  correct translated navigation and heading anchors. Retain site documentation
  support.
- **User Evidence**: The user confirmed NEED-002: README mapping and link/anchor
  handling while retaining existing site support.
- **Confirmed At**: 2026-10-13

### NEED-003: Complete translations of the latest English README

- **Status**: confirmed
- **Statement**: Completely translate the latest English README.md into the seven
  existing Chinese, Japanese, Korean, Spanish, French, German, and Brazilian
  Portuguese READMEs. Preserve English as the verified source.
- **User Evidence**: "然后使用这两个命令将我们最新更新的README翻译到其他语种的内容。"
  The final confirmed summary explicitly lists the seven existing languages.
- **Confirmed At**: 2026-10-13

### NEED-004: Execute translation and semantic verification

- **Status**: confirmed
- **Statement**: Actually invoke the new Codex entries to translate and check all
  seven READMEs. Repair omissions, semantic drift, inconsistent terminology,
  Markdown/link problems, and retain actual verification evidence.
- **User Evidence**: The final confirmed NEED-004 requires actual translation,
  semantic review, and repair rather than creating instructions alone.
- **Confirmed At**: 2026-10-13

## Constraints

### CON-001: Continue the maintainer-only installation boundary

- **Status**: confirmed
- **Statement**: Both commands remain repository-internal maintainer tools and
  are not distributed by `codexspec init`. Extend the maintainer conventions to
  native Codex entries without turning them into public user-project commands.
- **User Evidence**: The user confirmed the boundary proposal: "继续作为仓库内部
  维护工具，不通过 init 分发".
- **Confirmed At**: 2026-10-13

## Exclusions

### OUT-001: Preserve the source and avoid unrelated translation scope

- **Status**: confirmed
- **Statement**: Do not rewrite English README.md, add languages, retranslate the
  entire documentation site, or modify historical feature records. Maintainer
  guidance changes needed for the two entrypoints are within this feature.
- **User Evidence**: The confirmed summary preserves English, selects the seven
  existing README languages, and excludes site-wide retranslation.
- **Confirmed At**: 2026-10-13

## Decisions and Open Questions

No additional user-owned technical choice or blocking question. Shared-rule
maintenance, entry implementation, deterministic checks, execution sequencing,
and report layout are design choices within this scope.

## Applicable Background

- `.codexspec/specs/2026-1012-2306uu-readme-feature-audit/requirements.md` CON-001
  reserves other README languages for separate work. This feature performs that
  work without changing the completed English audit.
- `.codexspec/specs/2026-0620-15087m-separate-interaction-doc-language/requirements.md`
  OUT-001 identifies site translation as independent from language configuration.
- `.codexspec/specs/2026-0304-14502a-github-pages-i18n/spec.md` is legacy evidence
  of the site translation goal; absent requirements do not prove original user
  confirmation. Current command sources establish implemented behavior.
- `.codexspec/memory/constitution.md` currently describes Claude-only maintainer
  entries. NEED-001/CON-001 explicitly extend that entry scope to Codex while
  preserving the non-distribution boundary.
- `.codexspec/profile/constraints/C-2026-0902-054178-1-maintainer-validation-before-user-install.md`
  requires maintainer mechanisms to be verified before user installation paths.

## Confirmation Log

### 2026-10-13 — Final discovery confirmation

- **Summary Presented**: NEED-001 Codex entries with Claude compatibility;
  NEED-002 README mapping/navigation with site support; NEED-003 full seven-
  language README sync; NEED-004 actual translation/check/repair; maintainer-only
  tools, preserved English, and no site-wide retranslation.
- **User Confirmation**: "确认".
- **Entries Confirmed**: NEED-001, NEED-002, NEED-003, NEED-004, CON-001, OUT-001.
- **Open IDs**: None. Discovery is complete.
