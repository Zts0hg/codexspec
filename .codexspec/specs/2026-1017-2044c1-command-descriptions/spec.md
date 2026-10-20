# Specification: Command Descriptions

## Goal and User Scenarios

A first-time user browsing workflow commands can choose the right command,
understand the relevant input and anticipate its result without already knowing
the workflow's internal terminology. Experienced users see descriptions that
reflect the current command, including important effects and limitations.

## Requirements

### REQ-001: Cover the complete distributed command set

Sources: NEED-004.

Revise descriptions of all 28 registered distributed workflow commands. Lead with
the core purpose and principal result, distinguishing adjacent stages.
Acceptance: every registered command has a concrete, compact description; no
command is omitted. Use/input/result guide review, not a required prose checklist.

### REQ-002: Ground every description in current instructions

Sources: NEED-002.

Read the current command body and any referenced rules needed to establish its
behavior. Use supporting runtime and confirmed history for ambiguous claims.
Describe existing behavior accurately, including important modes, prerequisites
or effects when omission would mislead command selection.
Acceptance: retain a per-command evidence inventory linking the description
claims to current source sections. Unsupported claims are corrected or omitted;
unresolved material conflicts are reported rather than guessed.

### REQ-003: Keep every supported description surface aligned

Sources: NEED-003.

Update English source descriptions and every existing translation catalog,
Chinese command-list fallbacks, generated complete templates, installed Claude
commands and native Codex skills. Keep translations natural and faithful.
Acceptance: command keys and non-description fields remain unchanged; catalog
consistency, distribution generation and relevant integration checks pass.
Review actual text in each locale, since mechanical equality alone cannot prove meaning.

### NFR-001: Make descriptions readable and proportionate

Sources: CON-003, NEED-004.

Prefer one compact sentence with concrete familiar terms and distinguishing
information first. Preserve necessary meaning without a fixed character limit.
Keep detailed prerequisites, procedures and parameter references in command bodies
or hints. Acceptance: the leading text remains accurate and useful when truncated;
review for purpose, result and distinctions rather than exhaustive detail.

### REQ-004: Apply the approved bilingual wording

Sources: CON-002.

Before applying edits, present English and Chinese originals and proposals for
explicit user review. That review is complete: the user approved the full compact
wording set in description-proposals.md. Apply those 56 strings verbatim; translate
their meaning into the six other existing locales. Acceptance: source/en/zh-CN
values match the approved table, and no unapproved wording replaces them.

## Boundaries and Error Behavior

This is a content revision: preserve command bodies, arguments, command membership,
runtime behavior and version. Existing source/derived and packaging boundaries
apply. Invalid YAML, missing translations or stale generated files fail existing
maintainer checks and are fixed before delivery. No new runtime errors or modes
are introduced. README/site and repository-only maintenance descriptions are
outside this implementation's 28-command scope.

## Traceability

| Confirmed entry | Coverage |
| --- | --- |
| NEED-004 | REQ-001, NFR-001 |
| NEED-002 | REQ-002 |
| NEED-003 | REQ-003 |
| CON-003 | NFR-001 |
| CON-002 | REQ-004 |

## Open Questions

None.
