---
description: Convert a confirmed design into a traceable implementation plan
argument-hint: "[design.md, spec.md, or feature directory]"
handoffs:
  - agent: claude
    step: Generate an implementation plan constrained by the confirmed design and requirements
---

# Specification to Plan Converter

## Language Preference

Read `.codexspec/config.yml`. Two independent language controls apply (each falls back to `language.output`, then English):

- **Interaction language** (`language.interaction`): language for all conversation with the user — questions, explanations, status messages, and `codexspec` CLI terminal output.
- **Document language** (`language.document`): language for generated artifact files (requirements/spec/plan/tasks).

Converse in the interaction language and author artifacts in the document language. Apply the project's translation standard to both: translate by meaning (not word-for-word), keep English for terms with no good native equivalent, and write as if originally in that language.

## User Input

`$ARGUMENTS`

## Role

Act as an **implementation planner**. Define how to build the confirmed design in phases while preserving confirmed user intent. The design (`design.md`) already defines *what* the system is — architecture, components, interfaces, and key design decisions. Do not redo that design here: consume it and plan *how* to implement it (phases, ordering, verification).

## Feature Resolution

Use an explicit path first, then the current branch. If neither uniquely identifies a feature, ask the user to select one. Never silently select the latest feature.

Read:

- `requirements.md`
- `spec.md`
- `design.md`
- `.codexspec/memory/constitution.md` when present
- Relevant repository files needed to verify existing patterns and constraints

Design-stage compatibility: if `design.md` is absent (a legacy feature created before the design stage), plan directly from `spec.md` and state that no separate design artifact was available.

Legacy compatibility: if `requirements.md` is absent, treat `spec.md` as the temporary highest authority and disclose that original-discussion fidelity cannot be checked.

## Authority and Stop Conditions

Authority order:

1. Confirmed `requirements.md`
2. `spec.md`
3. Constitution and verified repository facts
4. `design.md`
5. Plan-level technical decisions
6. General best practices

Before planning, verify that `spec.md` covers the confirmed requirements and that `design.md` covers the spec. Stop if either omits, contradicts, or silently expands them.

Stop and request a user decision when:

- The plan would change confirmed scope, behavior, constraints, or trade-offs.
- Two reasonable approaches produce materially different user outcomes.
- A critical `OPEN-*` item blocks a safe design.
- The specification conflicts with the constitution or verified repository facts.

## Planning Rules

- Consume `design.md`: the plan implements the confirmed design; it does not re-architect or introduce new components/interfaces beyond it. If the design is insufficient to plan against, stop and hand back to the design stage rather than designing here.
- Every implementation phase and plan component must include `Covers: REQ-xxx; Design: <design component>` — trace both to the ultimate requirement and to the design component it builds. (When planning a legacy feature with no `design.md`, fall back to `Covers: REQ-xxx`.)
- Record new implementation-level choices (build ordering, tooling, sequencing) as **Plan-Level Decisions** with evidence, rationale, alternatives considered when material, and accepted trade-offs. Architecture / interface / data-model decisions belong to `design.md`, not here.
- Plan-level decisions may refine implementation but cannot redefine product intent or the confirmed design.
- Reuse repository patterns before introducing new abstractions or dependencies.
- Explicitly identify assumptions. Do not convert assumptions into requirements.
- Prefer the smallest plan that delivers the confirmed design.

## Required Output

Save `<feature-dir>/plan.md` using the appropriate simple or detailed template.

Include:

- Context, goals, and non-goals inherited from the specification and design
- Relevant existing repository constraints
- Implementation approach and plan-level decisions (build ordering, tooling, sequencing)
- Implementation phases and units, each with `Covers: REQ-xxx; Design: <design component>`
- Verification strategy
- Risks and trade-offs that affect delivery
- Requirements coverage table mapping every `REQ`/`NFR` to plan references and the design component realized

Do not force a standard five-phase structure when the design calls for a different sequence. Do not restate the architecture/component design — reference `design.md`.

## Pre-Save Validation

1. Every binding spec requirement and every design component has plan coverage.
2. Every plan unit maps to a requirement/design component or is identified as necessary implementation support.
3. No plan decision changes confirmed behavior or the confirmed design.
4. File paths and repository assumptions are verified where practical.
5. Unresolved conflicts cause the command to stop rather than guess.

## Automatic Review Loop

Invoke `/codexspec:review-plan <feature-dir>/plan.md`.

- Automatically fix only verified defects with a deterministic remediation supported by upstream evidence or repository facts.
- Do not auto-fix advisories or choose among materially different designs.
- Run a maximum of two automatic fix-and-review rounds.
- Stop if a defect repeats, remains unresolved, or requires a user decision.

## Auto-Next Chain Advance

Read `workflow.auto_next` from `.codexspec/config.yml` (default `false`; only the literal value `true` enables it — absent, `false`, or any other value means disabled).

When `workflow.auto_next` is `true` AND the Automatic Review Loop above concluded in a passing state — the final Overall Status is `PASS` or `PASS_WITH_WARNINGS` — advance the chain automatically:

1. Emit exactly one notice line, in the interaction language, e.g. `auto_next: review passed → invoking /codexspec:plan-to-tasks <feature-dir>`.
2. Invoke `/codexspec:plan-to-tasks <feature-dir>` exactly once, then end this command.

Do not auto-advance when `workflow.auto_next` is disabled, or the review loop stopped at `NEEDS_REVISION` or `BLOCKED`, or stopped early per the conditions above; in those cases hand control back to the user exactly as the review loop already does. This advances the chain and does not modify the Output Summary.

## Output Summary

Report the plan path, requirement coverage, plan-level decisions, unresolved items, and auto-review status.
