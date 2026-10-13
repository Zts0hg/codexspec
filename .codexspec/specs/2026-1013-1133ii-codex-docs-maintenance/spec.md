# Feature Specification: Codex Documentation Maintenance

**Feature Branch**: `2026-1013-1133ii-codex-docs-maintenance`
**Status**: Ready for Design
**Authority**: [requirements.md](requirements.md)

## Goal and Scenarios

Codex and Claude maintainers use the same repository-only translation and
semantic-check rules for site documentation and root READMEs. A maintainer can
translate all seven README variants from the verified English source, inspect
semantic fidelity, repair findings, and verify navigation without changing the
English source or distributing maintainer tooling to user projects.

## Requirements

### REQ-001: Usable Codex entrypoints and retained Claude entries

Provide native `codexspec:translate-docs` and `codexspec:check-i18n-semantics`
Codex skills with the existing command names. Retain Claude entrypoints and
consistent workflow rules, terminology guidance, arguments and interpretation
across hosts. Interaction follows project language preferences; translation
content follows its selected target language.

Sources: NEED-001.

### REQ-002: Explicit source/target mapping for both documentation surfaces

Both workflows support root README.md and its seven existing localized root
README files, as well as existing site documentation sources and localized
`docs/<lang>/` targets. Selection must be explicit enough to avoid routing
READMEs into the documentation site or translating unrelated files. Invalid
languages or unavailable source inputs produce actionable errors.

Sources: NEED-002, CON-001, OUT-001.

### REQ-003: Preserve technical meaning and navigable translations

Translate meaning naturally while preserving the source's conditions, ordering,
defaults, exclusions, command/code examples and file references. Apply the repo
terminology guidance. Preserve branding, language navigation and source-linked
references; update translated TOC and section anchors so local links resolve.
Check omitted or added content, drift, terminology, formatting and links.

Sources: NEED-002, NEED-003, NEED-004.

### REQ-004: Execute complete seven-language README synchronization

Invoke the new Codex translator for Chinese, Japanese, Korean, Spanish, French,
German and Brazilian Portuguese READMEs, using the latest verified English
README at the selected feature baseline. Translate all source sections and
capabilities, including the preserved installation guide. Then invoke the
semantic-check entrypoint, repair substantiated problems and retain per-language
check outcomes and source correspondence.

Sources: NEED-003, NEED-004.

### REQ-005: Maintain and verify the repository-internal boundary

Keep both tools outside public command distribution, package installation and
`codexspec init` behavior. Extend the existing maintainer conventions to Codex
entrypoints. Detect stale or unusable maintained entrypoints with repository
checks. Preserve English README.md, historical feature records, existing
languages and the non-targeted site content.

Sources: CON-001, OUT-001, NEED-001.

### NFR-001: Maintainable instructions and evidence

Use maintained shared rules rather than drifting host-specific copies. Keep
entrypoint discovery concise and matching the repository naming conventions.
Use meaningful deterministic checks for technical preservation and navigation,
plus semantic assessment for meaning. Record executed checks honestly; an
instruction file or mechanical check alone does not prove translation fidelity.

Sources: NEED-001, NEED-004, CON-001.

## Acceptance and Error Behavior

- Both native Codex skill files are usable and semantically equivalent to the
  retained Claude entries; maintained sources and derived files agree.
- README selection maps only README.md to the seven root README variants.
  Existing site selection retains its source/target layout and language aliases.
- Each translated README covers all source sections, commands, options and
  defaults; executable examples and technical tokens retain source semantics.
- Local links, translated anchors, language navigation, Markdown and structure
  checks pass for every target. The semantic report assesses each language and
  identifies no unresolved substantive fidelity issue.
- English README content equals the baseline exactly. No new language or
  unrelated site-wide translation is introduced.
- Public commands remain the existing distributed set; installation/package
  behavior does not acquire the two maintainer tools.
- Selection errors fail before translation writes; missing/stale host files are
  reported by checks. Semantic failures are reported and repaired rather than
  silently counted as success.

## Scope and Authority

No product ambiguity remains. The confirmed Codex entrypoint extension updates
the older Claude-only maintainer description; it preserves the installation
boundary. The completed English-only audit remains historically unchanged.

Out of scope: rewriting English README, adding languages, site-wide
retranslation, modifying historical requirements, and public user-project
translation-command distribution.

## Traceability

| Confirmed Entry | Coverage |
|-----------------|----------|
| NEED-001 | REQ-001, REQ-005, NFR-001 |
| NEED-002 | REQ-002, REQ-003 |
| NEED-003 | REQ-003, REQ-004 |
| NEED-004 | REQ-003, REQ-004, NFR-001 |
| CON-001 | REQ-002, REQ-005, NFR-001 |
| OUT-001 | REQ-002, REQ-005, Scope |
