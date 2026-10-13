# Confirmed Requirements: Comprehensive English README Audit

**Feature ID**: `2026-1012-2306uu`
**Status**: Confirmed
**Last Confirmed**: 2026-10-12

## Authority Rules

Only entries with Status: confirmed bind downstream artifacts. Open questions and
AI assumptions are not requirements. Preserve any replaced decision as superseded
and link it to its replacement.

## Context

The English README includes an installation guide added on 2026-10-12. That
addition does not establish that its description of project capabilities is
current or complete. This feature audits the entire README against the current
user-facing functionality, including functionality absent from the document.

## Needs

### NEED-001: Inventory all current user-facing capabilities

- **Status**: confirmed
- **Statement**: Start from the current implementation and establish a complete
  inventory of user-facing capabilities. Cover the six public CLI commands,
  28 distributed agent commands, and mechanisms shared across commands,
  including configuration, automation, worktrees, project knowledge, and
  historical requirements recall.
- **User Evidence**: The user requested a comprehensive comparison with the latest
  functionality and explicitly confirmed the final inventory-based summary.
- **Confirmed At**: 2026-10-12

### NEED-002: Check both accuracy and completeness

- **Status**: confirmed
- **Statement**: Compare every inventory item with the English README. Identify
  incorrect or outdated descriptions, entirely missing capabilities, and
  capabilities whose names appear without necessary explanations. Provide
  source evidence for each issue.
- **User Evidence**: “不仅是提及的功能描述落后于实际实现的情况，还包括对已有功能的描述缺失的情况也要一并检查和完善”.
- **Confirmed At**: 2026-10-12

### NEED-003: Correct and complete the README

- **Status**: confirmed
- **Statement**: Fix inaccurate descriptions and supply missing introductions so
  readers understand each capability's purpose, suitable use, invocation entry,
  and important default behavior. Existing detailed documentation may provide
  the full rules through links.
- **User Evidence**: The user explicitly requested checking and completing
  descriptions of existing functionality, then confirmed the final summary.
- **Confirmed At**: 2026-10-12

### NEED-004: Keep the entire README internally consistent

- **Status**: confirmed
- **Statement**: Update the introduction, advantages, quick start, workflows,
  command tables, configuration, generated project structure, and development
  examples together. Check links, duplicate content, and paragraph placement.
- **User Evidence**: Explicit confirmation of the final whole-document consistency
  summary.
- **Confirmed At**: 2026-10-12

## Constraints

### CON-001: English README only; preserve program behavior

- **Status**: confirmed
- **Statement**: Modify only the English README.md as the product change. Other
  README languages are separate future work. Do not change program behavior.
  Workflow requirements, specification, design, planning, review, and
  verification records belong to this feature's own directory.
- **User Evidence**: “只针对英文 README.md ，其他语言版本之后会单独开一个任务做。” The
  final summary also excludes changing program behavior and was confirmed.
- **Confirmed At**: 2026-10-12

## Decisions

No additional product choices were confirmed. README information placement and
concise explanations may be designed within NEED-003 and NEED-004.

## Out of Scope

Other README languages and program behavior changes are excluded by CON-001.
Detailed reference-document rewrites, command-template changes, and modifications
to historical requirement records are unnecessary for the confirmed README-only
product scope.

## Open Questions

None. The user's explicit request includes both checking and completing the
README; it is not limited to an audit report.

## Repository Evidence

- Baseline: `a0ab7fa52e1a3c68b5a7a3e66915a17b65a1039e`.
- `src/codexspec/__init__.py`: six public CLI commands and configuration options.
- `src/codexspec/commands/installer.py`: 28 distributed command registrations.
- `templates/commands/`, `templates/review-code/`, and `src/codexspec/`:
  current command behavior and shared runtime mechanisms.
- `CHANGELOG.md` and related confirmed records under `.codexspec/specs/`:
  decision evolution and release context. Historical plans alone do not establish
  implementation.
- Existing project profile convention Con-2026-1001-2205zz-1 identifies the
  development dependency extra; `pyproject.toml` verifies its current location.

## Confirmation Log

### 2026-10-12 — Final discovery confirmation

- **Summary Presented**: Inventory all current user capabilities; check stale,
  incorrect, absent, and insufficient descriptions with source evidence; correct
  and complete introductions and usage; synchronize the whole document; limit the
  product edit to English README.md without changing program behavior.
- **User Confirmation**: “确认”.
- **Entries Confirmed**: NEED-001, NEED-002, NEED-003, NEED-004, CON-001.
- **Open IDs**: None. Discovery is complete.
