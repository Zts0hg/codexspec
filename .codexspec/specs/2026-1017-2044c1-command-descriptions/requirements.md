# Confirmed Requirements: Command Descriptions

**Feature ID**: `2026-1017-2044c1`
**Status**: Confirmed
**Last Confirmed**: 2026-10-17

## Context

First-time users need command descriptions that help them choose an appropriate
command and understand what to provide and expect. Abstract summaries such as
"persist the authoritative requirements record" do not provide enough guidance.

## Needs

### NEED-001: Explain use, input, and outcome

- **Status**: superseded by NEED-004
- **Statement**: Rewrite descriptions of all 28 distributed workflow commands
  as brief guidance explaining when to use the command, the relevant input,
  and the useful result. Distinguish neighboring commands in the workflow.
- **User Evidence**: The user accepted the proposed specify, generate-spec and
  clarify examples and the proposed scope with "符合预期".

### NEED-002: Derive descriptions from current behavior

- **Status**: confirmed
- **Statement**: Read each command's current instructions and relevant supporting
  behavior before writing its description. Correct outdated claims; do not
  merely expand or translate old descriptions. Include important prerequisites,
  modes or boundaries when they affect command selection or expectations.
- **User Evidence**: "需要根据当前命令的实际内容考虑新的 description 内容，避免旧
  description 存在落后于命令最新内容导致 description不够准确的情况。"

### NEED-003: Synchronize description surfaces

- **Status**: confirmed
- **Statement**: Keep distributed command descriptions, all existing language
  catalogs, installed Claude commands and Codex skills, and command-list fallback
  descriptions aligned. Preserve the same meaning across languages and surfaces.
- **User Evidence**: The accepted proposal included multilingual versions and
  fallback descriptions in command listings.

## Constraints

### CON-001: Use concise, approachable language

- **Status**: superseded by CON-003
- **Statement**: Usually use one or two sentences, adapted to command complexity.
  Prefer concrete behavior and familiar language over abstract workflow jargon.
  Preserve necessary information instead of enforcing an arbitrary length limit.
  Full parameter lists belong in usage instructions rather than descriptions.
- **User Evidence**: "符合预期" accepted these writing rules and sample detail.

## Scope Interpretation

This is a description revision. Command bodies, arguments, runtime behavior,
public command membership, README/site content, repository-only maintenance
commands, and package versions need no product changes. These are implementation
boundaries inferred from the accepted 28-command description scope, not additional
user-confirmed exclusions. Existing source/derived and packaging rules apply.

## Prepared Background

- `../2026-1012-2306uu-readme-feature-audit/requirements.md`: purpose, appropriate
  use and actual capability coverage matter; that earlier change targeted README.
- `../2026-1014-193481-readme-native-expression/requirements.md`: natural target
  language expression with faithful meaning; its README-specific scope stays separate.
- `../2026-0902-054178-shared-command-sections/requirements.md`: maintainer-only
  authoring, complete generated distributions, checks before user installation.
- `../2026-1010-21225w-unified-staged-commit-analysis/requirements.md`: staged-only
  analysis; supersedes the obsolete conversation-aware fallback description.
- `../2026-0808-21309w-analyze-autofix-and-test-completeness/requirements.md`:
  analyze automatically repairs deterministic downstream inconsistencies.
- `../2026-1009-2352qc-design-to-plan/requirements.md`: planning consumes design;
  preserve the current name and responsibilities.

## Open Questions

Individual wording awaits user confirmation under CON-002. See the latest writing standard below.

## Confirmation Log

### 2026-10-17 — Description scope and writing rules

- **Summary Presented**: Rewrite the 28 distributed workflow descriptions around
  use, input and result, generally in one or two sentences; distinguish neighboring
  commands; include important boundaries; synchronize languages and fallback text.
- **User Confirmation**: "符合预期" plus the explicit requirement to derive each
  description from current command content instead of outdated descriptions.
- **Entries Confirmed**: NEED-001, NEED-002, NEED-003, CON-001.
- **Discovery**: Complete; no unresolved product decision blocks the next stage.

## 2026-10-17 — Review wording before applying changes

### CON-002: Present bilingual before/after proposals for user confirmation

- **Status**: confirmed
- **Statement**: Before applying description edits, present each command's original
  and proposed wording in both English and Simplified Chinese. Allow discussion
  and adjustment, and wait for explicit confirmation of the proposed wording.
- **User Evidence**: "记得不要直接修改，要列出原本的内容和建议修改的内容（列出英文版和中文版）给我确认是否还有需要讨论和调整的"
- **Effect**: This supersedes the earlier implementation assumption that agreement
  on writing style authorizes immediate application of the drafted descriptions.
  NEED-001 through NEED-003 and CON-001 remain applicable.
- **Confirmation Log**: Explicit user instruction received during drafting;
  description edits were withdrawn and a bilingual proposal retained.

### Current Workflow State

Awaiting user review of description-proposals.md. Earlier downstream artifacts and
review reports describe the plan before CON-002 and are historical preparation,
not authorization to apply wording. Refresh them against CON-002 after the user
confirms the proposed text. No command descriptions are currently changed.

## 2026-10-17 — Compact descriptions for command lists

### NEED-004: Help users choose commands at a glance

- **Status**: confirmed
- **Statement**: Revise all 28 distributed workflow descriptions to state the core
  purpose and principal result in a compact sentence, placing distinguishing
  information first. Use when/input/result as editorial checks, without requiring
  every description to explicitly enumerate all three. Distinguish adjacent stages.
- **Replaces**: NEED-001. Retains its scope and first-time-user objective.
- **User Evidence**: The user explained that long descriptions are truncated in
  the command picker and confirmed the proposed compact approach with "确认".

### CON-003: Prioritize useful leading text over exhaustive detail

- **Status**: confirmed
- **Statement**: Prefer one concise sentence with concrete, familiar language.
  Put the main purpose and result before introductory context, and include only
  modes or effects important to command selection. Leave complete prerequisites,
  procedures and boundaries in the command body or argument hints. A truncated
  leading portion must remain accurate and useful without a corrective ending.
  Do not impose an arbitrary fixed character limit or assume a fixed display width.
- **Replaces**: CON-001, refining brevity while retaining clarity and necessary meaning.
- **User Evidence**: "命令的description过长可以会被省略显示末尾部分";
  "这次不能只是单纯把description变得事无巨细的冗长"; "确认".

### Confirmation Log

- The user confirmed the compact writing standard and the shorter specify example.
- NEED-002 (current behavior), NEED-003 (surface synchronization), and CON-002
  (bilingual before/after review before application) remain binding.
- The full 28-command compact wording is a new proposal, not yet approved.
- Earlier downstream artifacts require revision before implementation resumes.

## 2026-10-17 — Approval to apply all compact descriptions

- **User Confirmation**: "确认，按照建议版本更新并同步到各个语言".
- **Approved Text**: All 28 English and Simplified Chinese proposed descriptions
  in description-proposals.md, as presented immediately before this confirmation.
- **Effect**: CON-002 is satisfied. Apply those exact English/Chinese values and
  synchronize faithful compact translations in all six other existing locales.
- **Current State**: Wording discussion is complete; implementation may resume.
  NEED-002, NEED-003, NEED-004, CON-002 and CON-003 remain binding. Historical
  awaiting-review statements above describe earlier points in this discussion.
