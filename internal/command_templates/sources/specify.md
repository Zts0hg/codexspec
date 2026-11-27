---
description: Clarify a feature’s goals, scope and constraints, then save confirmed requirements to requirements.md.
argument-hint: "Describe the initial idea, or provide an existing feature directory"
scripts:
  sh: .codexspec/scripts/create-new-feature.sh
  ps: .codexspec/scripts/create-new-feature.ps1
---

# Requirement Discovery

## Language Preference

Read `.codexspec/config.yml`. Two independent language controls apply (each falls back to `language.output`, then English):

- **Interaction language** (`language.interaction`): language for all conversation with the user — questions, explanations, status messages, and `codexspec` CLI terminal output.
- **Document language** (`language.document`): language for generated artifact files (requirements/spec/plan/tasks).

Converse in the interaction language and author artifacts in the document language. Apply the project's translation standard to both: translate by meaning (not word-for-word), keep English for terms with no good native equivalent, and write as if originally in that language.

<!-- CODEXSPEC:INCLUDE expression-standard.md -->

<!-- CODEXSPEC:INCLUDE workspace-routing.md -->

<!-- CODEXSPEC:INCLUDE specs-recall.md -->

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
4. With worktree isolation enabled, require a `ready` result and carry its absolute workspace and
   artifact paths throughout discovery. Follow Workspace Routing Before Writes for pending baseline
   verification or failure; never continue by writing in the invoking checkout. Only explicit
   disabled mode retains the existing unavailable-branch fallback.

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

## Prepare Discovery

Before substantive discovery or questioning, prepare the setting and evidence below. Reuse sufficient background from historical specs and the project profile instead of repeating its retrieval.

1. Read `workflow.auto_next` from the applicable workspace's `.codexspec/config.yml`. Default to disabled; only the literal boolean `true` enables it. An absent setting, `false`, or any other value is disabled. Use this setting to select the discovery depth below.
2. Inspect the relevant current implementation: actual behavior, callers, callees, and dependencies needed to establish the question's premise. Before deciding whether a question or option is applicable, verify the premises that determine its applicability. Do not infer the existence, implementation status, relationships, or impact of functionality solely from surface descriptions in requests, interfaces, names, or documentation. Treat unverified premises as unknown. Classify content or behavior as placeholder, unused, or functional only after inspection establishes that classification. Use verified facts to answer factual matters already established and formulate applicable questions. Do not ask questions premised on functionality or relationships that inspection establishes do not exist. If a real dependency creates a material scope or outcome choice, explain the relationship and ask the user rather than assuming retention or removal.
3. Independently obtain accessible factual information before requesting it from the user. Determine whether relevant code, documentation, configuration, history, logs, tests, and other available tools and sources can supply or establish it. Within the task's scope and existing authorization, collect and investigate it first. Do not ask users to locate information or perform checks the agent can perform itself.

Distinguish verified implementation facts, confirmed user intent, and unverified inferences. An unsuccessful search does not prove absence. If relevant code does not yet exist or cannot be inspected, state the available evidence and uncertainty. If necessary information remains inaccessible, contradictory, or inconclusive after targeted investigation, briefly state what is known and the specific evidence gap, then ask only for the missing information necessary to proceed. Collected facts do not substitute for user decisions. Existing behavior does not automatically become a requirement to preserve it.

Inspect only sources and execution paths needed for the current judgment. Do not require a repository-wide audit or exhaustive diagnosis. Stop when evidence is sufficient and reuse prepared evidence. Supplement it only when scope changes, new evidence appears, or existing evidence is insufficient. Do not repeatedly perform the same failed checks or indefinitely expand retrieval instead of identifying the remaining gap. This preparation does not require a fixed sequence of tool calls before every question.

## Select Questions for the Automation Mode

Current-state verification and autonomous fact-gathering apply in both modes. The user decides choices affecting behavior, scope, compatibility, or important cost or maintenance trade-offs. Independently select equivalent technical implementations that satisfy the same confirmed requirements. Judge architecture and dependency choices by their actual consequences. Do not require separate confirmation for every purely technical choice. Do not infer user goals or preferences from collected facts.

- **When enabled**: Examine foreseeable specification, design, planning, and implementation consequences. Resolve the user decisions those stages would otherwise require before final confirmation. Explain verified facts and offer viable choices. An item is not non-blocking merely because specification generation can proceed; if a later automatic stage still needs a user decision, resolve it during discovery.
- **When disabled**: retain normal staged clarification without moving every later technical choice into specify.

Do not produce complete design or implementation plans during specify. If a previously unforeseeable material decision appears downstream, stop and ask the user under the existing downstream rules rather than guessing; early clarification does not authorize new product decisions.

## Discussion Rules

- Base substantive questions on the prepared evidence; investigate necessary factual gaps before asking the user.
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
- When `workflow.auto_next` is enabled, all foreseeable downstream user decisions identified above are resolved; they cannot remain open or be deferred as non-blocking.

Report:

- Feature directory
- Requirements record path
- Confirmed IDs
- Open IDs and whether they block specification generation
- Next command: `/codexspec:generate-spec <feature-dir>`

## Auto-Next Chain Advance

Read `workflow.auto_next` from `.codexspec/config.yml` (default `false`; only the literal value `true` enables it).

When `workflow.auto_next` is `true` AND discovery is complete — the Completion criteria above are met and the user has explicitly confirmed the final stage summary (not each intermediate topic confirmation) — advance the chain automatically:

1. Emit exactly one notice line, in the interaction language, e.g. `auto_next: requirements confirmed → invoking /codexspec:generate-spec <feature-dir>`.
2. Invoke `/codexspec:generate-spec <feature-dir>` exactly once, then end this command.

Do not auto-advance on intermediate topic confirmations, or when `workflow.auto_next` is disabled (absent, `false`, or non-`true`); in those cases report normally and hand off to the next command manually. This advances the chain and does not modify the Completion report.
