---
description: 将已确认的需求编写为可追溯的 spec.md
argument-hint: "[requirements.md 或 功能目录]"
handoffs:
  - agent: claude
    step: Generate a specification from confirmed requirements
---

# Specification Generator

## Language Preference

Read `.codexspec/config.yml`. Two independent language controls apply (each falls back to `language.output`, then English):

- **Interaction language** (`language.interaction`): language for all conversation with the user — questions, explanations, status messages, and `codexspec` CLI terminal output.
- **Document language** (`language.document`): language for generated artifact files (requirements/spec/plan/tasks).

Converse in the interaction language and author artifacts in the document language. Apply the project's translation standard to both: translate by meaning (not word-for-word), keep English for terms with no good native equivalent, and write as if originally in that language.

## User Input

`$ARGUMENTS`

## Role

Act as a **requirements compiler**. Convert the persistent, user-confirmed decision record into `spec.md` without changing product intent.

## Authority Order

1. Confirmed entries in `requirements.md`
2. Existing `spec.md` when operating in legacy compatibility mode
3. Project constitution and verified repository facts
4. Explicit assumptions, which are never equivalent to confirmed requirements
5. General best practices

## Feature Resolution

1. If `$ARGUMENTS` identifies a `requirements.md` file or feature directory, use it.
2. Otherwise match the current git branch to `.codexspec/specs/<branch>/`.
3. If there is no unique match, ask the user to select a feature. Never silently select the latest directory.
4. If `requirements.md` is absent but an existing `spec.md` is present, use legacy compatibility mode:
   - Treat `spec.md` as the temporary highest authority.
   - State that fidelity to the original discussion cannot be verified.
   - Do not regenerate it from guessed requirements.
5. If neither artifact exists, stop and direct the user to `/codexspec:specify`.

## Compilation Rules

- Read all `NEED-*`, `CON-*`, `DEC-*`, `OUT-*`, and `OPEN-*` entries.
- Only entries with `Status: confirmed` may become binding requirements.
- Preserve `open` entries as unresolved questions. Do not turn them into requirements.
- Ignore `superseded` entries except for historical context.
- Use `REQ-xxx` consistently for functional requirements and `NFR-xxx` for non-functional requirements.
- Every requirement must include `Sources: NEED-xxx, CON-xxx, DEC-xxx`.
- Preserve confirmed exclusions in Out of Scope.
- Add an assumption only when required to make the document understandable. Label it clearly and do not use it to expand scope.
- If confirmed entries conflict, or a critical open item prevents a single faithful specification, stop and report the conflict instead of choosing an interpretation.

## Required Output

Use the appropriate simple or detailed template from `.codexspec/templates/docs/`.

The specification must include:

- Context and goals
- User stories or user-visible scenarios where applicable
- `REQ-*` and `NFR-*` items with `Sources:`
- Acceptance criteria and expected error behavior
- Confirmed constraints and decisions
- Open questions that block later work
- Out of Scope
- A traceability table mapping every confirmed requirements entry to spec coverage

Do not add sections merely to satisfy a template when they are irrelevant.

Save to `<feature-dir>/spec.md`.

## Pre-Save Validation

Before saving:

1. Verify every confirmed `NEED`, `CON`, `DEC`, and `OUT` entry is represented or explicitly marked not applicable with a reason.
2. Verify every `REQ`/`NFR` has at least one valid source.
3. Verify no `OPEN` or AI inference was presented as confirmed.
4. Verify terminology and scope remain consistent with `requirements.md`.
5. Stop if any discrepancy would require a new user decision.

## Automatic Review Loop

Invoke `/codexspec:review-spec <feature-dir>/spec.md` after saving.

- Automatically fix only verified defects whose remediation is directly determined by confirmed upstream evidence.
- Never auto-fix Risk Advisories or Design Opportunities.
- Never introduce a new product decision during auto-fix.
- Run a maximum of two automatic fix-and-review rounds.
- If defects remain, the same defect repeats, or remediation requires a user decision, stop and report the evidence.

## Output Summary

Report:

- Spec path
- Confirmed requirement coverage
- Open items
- Auto-review status and number of rounds
