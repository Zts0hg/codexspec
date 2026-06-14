---
description: 在技术规划前通过定向澄清问题识别功能规格中的不明确区域
argument-hint: "[spec.md 路径] (可选，默认为 .codexspec/specs/{feature-id}/)"
---

# Requirements Clarifier

## Language Preference

Read `.codexspec/config.yml`. Use `language.output`; default to English.

## User Input

`$ARGUMENTS`

## Feature Resolution

Use an explicit path first, then the current branch. Ask the user when resolution is ambiguous; never silently select the latest feature.

Read:

- `requirements.md`
- `spec.md`
- `review-spec.md` when present
- Constitution

Legacy compatibility: when only `spec.md` exists, extract candidate requirement records with `Status: open`. Do not assume the extracted wording reflects the original discussion until the user confirms it.

## Clarification Priorities

Prioritize:

1. Confirmed requirement and spec mismatches
2. Critical or Warning defects from `review-spec.md`
3. Open items that block planning
4. Material ambiguity, contradiction, missing behavior, or unverifiable requirements

Do not ask questions solely to fill a template section or add generic best practices.

## Question Loop

- Ask exactly one material question at a time.
- Explain the affected requirement IDs and implementation consequence.
- Offer 2-4 meaningful options when possible.
- Limit a session to five questions unless the user explicitly asks to continue.

After each answer, keep it as a candidate. At a coherent stage boundary, present a stage summary and request explicit confirmation.

## Persistence Order

Update `requirements.md` first.

Only after the user confirms the stage summary:

1. Add or modify the relevant `NEED`, `CON`, `DEC`, `OUT`, or `OPEN` entries.
2. Mark replaced entries `superseded` rather than deleting them.
3. Add short User Evidence and a Confirmation Log entry.
4. Update `spec.md` to reflect the confirmed entries.
5. Update `Sources:` and the requirements traceability table.

Never update `spec.md` with an unconfirmed answer. Never leave confirmed requirements and spec content knowingly inconsistent.

## Completion

Report:

- Questions asked and confirmed
- Requirements entries added, changed, superseded, or left open
- Spec requirements updated
- Remaining blockers
- Whether `/codexspec:review-spec` should run again
