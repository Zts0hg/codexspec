---
description: 通过交互式问答澄清需求，探索和完善初始想法
argument-hint: "描述你的初始想法或需求"
scripts:
  sh: .codexspec/scripts/create-new-feature.sh
  ps: .codexspec/scripts/create-new-feature.ps1
---

# Requirement Discovery

## Language Preference

Read `.codexspec/config.yml`. Use `language.output`; default to English.

## User Input

`$ARGUMENTS`

## Goal

Turn the user discussion into a persistent, traceable `requirements.md`. The discussion is the richest source of intent, but only the user's confirmed stage summary becomes binding downstream authority.

Do not generate `spec.md` in this command.

## Feature Workspace

### New Feature

When `$ARGUMENTS` is a new requirement:

1. Derive a short kebab-case feature name.
2. Run the platform create-new-feature script:
   - Bash: `{SCRIPT} --name "<feature-name>"`
   - PowerShell: `{SCRIPT} -ShortName "<feature-name>" "<description>"`
3. Parse the created feature directory and `requirements.md` path.
4. If branch creation is unavailable, continue in the workspace and report the limitation.

### Existing Feature

When the argument identifies an existing feature:

1. Use the explicit directory first.
2. Otherwise match the current branch.
3. If multiple features are possible, ask the user to select one. Never silently select the latest.
4. Load the existing `requirements.md`.
5. Legacy feature: if only `spec.md` exists, extract candidate entries from it, mark them `open`, and require user confirmation before they become authoritative.

## Discussion Rules

- Ask one material question at a time.
- Use structured choices when there are 2-4 meaningful options.
- Explore user goals, workflows, constraints, error behavior, compatibility, scope boundaries, and important trade-offs.
- Prefer the user's actual objective over generic methods or idealized architecture.
- Distinguish the user's statement from AI inference.
- Do not mark an inference as `confirmed`.
- Record rejected alternatives only when they clarify a confirmed decision.
- Do not preserve the entire chat transcript.

## Candidate Entries

Maintain candidate entries using:

- `NEED-xxx`: goals and required behavior
- `CON-xxx`: constraints and boundaries
- `DEC-xxx`: confirmed trade-offs or choices
- `OUT-xxx`: exclusions
- `OPEN-xxx`: unresolved questions

Each candidate includes a concise statement and, when useful, short **User Evidence**.

## Stage Summary Confirmation

After a coherent topic or at the end of discovery:

1. Present a concise stage summary grouped by candidate IDs.
2. Clearly separate:
   - Proposed confirmed entries
   - Open questions
   - AI assumptions that still need confirmation
3. Ask the user to confirm or correct the stage summary.
4. Only after explicit confirmation:
   - Write the entries to `requirements.md`.
   - Set their status to `confirmed`.
   - Append a Confirmation Log entry.
5. If a decision changes, keep the old entry with `Status: superseded` and link it to the replacement.

Do not treat silence or lack of objection as confirmation.

## Completion

Discovery is complete when:

- The primary goal and required behaviors are confirmed.
- Material constraints and exclusions are confirmed.
- Important trade-offs are recorded.
- Remaining open questions are either non-blocking or explicitly deferred.

Report:

- Feature directory
- Requirements record path
- Confirmed IDs
- Open IDs and whether they block specification generation
- Next command: `/codexspec:generate-spec <feature-dir>`
