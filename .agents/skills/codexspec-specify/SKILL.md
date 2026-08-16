---
name: codexspec:specify
description: "讨论、确认并固化权威的需求记录"
---

# Requirement Discovery

## Language Preference

Read `.codexspec/config.yml`. Two independent language controls apply (each falls back to `language.output`, then English):

- **Interaction language** (`language.interaction`): language for all conversation with the user — questions, explanations, status messages, and `codexspec` CLI terminal output.
- **Document language** (`language.document`): language for generated artifact files (requirements/spec/plan/tasks).

Converse in the interaction language and author artifacts in the document language. Apply the project's translation standard to both: translate by meaning (not word-for-word), keep English for terms with no good native equivalent, and write as if originally in that language.

## User Input

`the text after the $codexspec:specify skill mention`

## Goal

Turn the user discussion into a persistent, traceable `requirements.md`. The discussion is the richest source of intent, but only the user's confirmed stage summary becomes binding downstream authority.

Do not generate `spec.md` in this command.

## Feature Workspace

### New Feature

When `the text after the $codexspec:specify skill mention` is a new requirement:

1. Derive a short kebab-case feature name.
2. Run the platform create-new-feature script:
   - Bash: `.codexspec/scripts/create-new-feature.sh --name "<feature-name>"`
   - PowerShell: `.codexspec/scripts/create-new-feature.ps1 -ShortName "<feature-name>" "<description>"`
3. Parse the created feature directory and `requirements.md` path.
4. If branch creation is unavailable, continue in the workspace and report the limitation.

### Existing Feature

When the argument identifies an existing feature:

1. Use the explicit directory first.
2. Otherwise match the current branch.
3. If multiple features are possible, ask the user to select one. Never silently select the latest.
4. Load the existing `requirements.md`.
5. Legacy feature: if only `spec.md` exists, extract candidate entries from it, mark them `open`, and require user confirmation before they become authoritative.

## Consult Project Profile

Before discussing and finalizing requirements, read the project profile under `.codexspec/profile/` when it exists so the confirmed `requirements.md` is a synthesis that already accounts for accumulated project knowledge. Each category is a directory holding one record per file:

- `constraints/` first — the project's hard prohibitions (highest weight); requirements MUST NOT contradict them.
- `pitfalls/`, `conventions/`, `decisions/`, `strategies/`, `runbooks/` — read the records relevant to this feature's area, to avoid re-hitting known traps, to follow established conventions, to reuse past cross-feature/architectural decisions rather than re-litigating them, and to apply proven strategies and procedures.

Each record carries a `status` (`candidate` or `vetted`); weight `candidate` entries with appropriate caution. Fold what is relevant into the discussion and the resulting entries; cite a profile record as evidence when it materially shapes a decision. This is the single point where the profile enters the SDD pipeline — downstream stages keep `requirements.md` as authority and do not re-read the profile. Degrade silently when the profile is absent or empty (nothing to apply); never block on it.

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
- Next command: `$codexspec:generate-spec <feature-dir>`

## Auto-Next Chain Advance

Read `workflow.auto_next` from `.codexspec/config.yml` (default `false`; only the literal value `true` enables it).

When `workflow.auto_next` is `true` AND discovery is complete — the Completion criteria above are met and the user has explicitly confirmed the final stage summary (not each intermediate topic confirmation) — advance the chain automatically:

1. Emit exactly one notice line, in the interaction language, e.g. `auto_next: requirements confirmed → invoking $codexspec:generate-spec <feature-dir>`.
2. Invoke `$codexspec:generate-spec <feature-dir>` exactly once, then end this command.

Do not auto-advance on intermediate topic confirmations, or when `workflow.auto_next` is disabled (absent, `false`, or non-`true`); in those cases report normally and hand off to the next command manually. This advances the chain and does not modify the Completion report.
