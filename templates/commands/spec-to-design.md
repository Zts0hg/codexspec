---
description: Convert a confirmed specification into a traceable design document
argument-hint: "[spec.md or feature directory]"
handoffs:
  - agent: claude
    step: Produce a design document constrained by confirmed requirements and spec
---

# Specification to Design Converter

## Language Preference

Read `.codexspec/config.yml`. Two independent language controls apply (each falls back to `language.output`, then English):

- **Interaction language** (`language.interaction`): language for all conversation with the user — questions, explanations, status messages, and `codexspec` CLI terminal output.
- **Document language** (`language.document`): language for generated artifact files (requirements/spec/plan/tasks).

Converse in the interaction language and author artifacts in the document language. Apply the project's translation standard to both: translate by meaning (not word-for-word), keep English for terms with no good native equivalent, and write as if originally in that language.

## User Input

`$ARGUMENTS`

## Role

Act as a **constrained system designer**. Define *what the system is* — architecture, components, interfaces, and key design decisions — that realizes the specification, while preserving confirmed user intent. Do not plan *how to build it* in phases; that belongs to the downstream `plan` stage.

## Feature Resolution

Use an explicit path first, then the current branch. If neither uniquely identifies a feature, ask the user to select one. Never silently select the latest feature.

Read:

- `requirements.md`
- `spec.md`
- `.codexspec/memory/constitution.md` when present
- Relevant repository files needed to verify existing patterns and constraints

Legacy compatibility: if `requirements.md` is absent, treat `spec.md` as the temporary highest authority and disclose that original-discussion fidelity cannot be checked.

## Authority and Stop Conditions

Authority order:

1. Confirmed `requirements.md`
2. `spec.md`
3. Constitution and verified repository facts
4. Design-level technical decisions
5. General best practices

Before designing, verify that `spec.md` covers the confirmed requirements. Stop if it omits, contradicts, or silently expands them.

Stop and request a user decision when:

- The design would change confirmed scope, behavior, constraints, or trade-offs.
- Two reasonable designs produce materially different user outcomes.
- A critical `OPEN-*` item blocks a safe design.
- The specification conflicts with the constitution or verified repository facts.

## Design Rules

- Every component, interface, data change, and design decision must include `Covers: REQ-xxx`.
- Record material design choices as **Key Design Decisions** (ADR-lite) with context, the decision, alternatives considered when material, and accepted trade-offs.
- Design-level decisions may refine implementation design but cannot redefine product intent.
- **Scale to complexity.** The design template's fixed core (Architecture & Components, Key Design Decisions, Requirements Coverage) is always present; its optional sections (Data Models, API / Interface Contracts, Sequence & Data Flow, Cross-Cutting Design, Risks & Trade-offs) appear ONLY when the feature warrants them. A trivial feature may be a thin page whose Key Design Decisions section records "no significant design decisions". Do not add a section merely because the template contains it.
- Reuse repository patterns before introducing new abstractions or dependencies.
- Explicitly identify assumptions. Do not convert assumptions into requirements.
- Prefer the smallest design that satisfies the confirmed requirements.

## Required Output

Save `<feature-dir>/design.md` using `.codexspec/templates/docs/design-template.md`.

Include:

- Context inherited from the specification
- Architecture & Components, each with `Covers:`
- Key Design Decisions (ADR-lite), each with `Covers:`
- Optional sections (data models, API/interface contracts, sequence/data flow, cross-cutting design, risks) only when they materially help implement or verify this feature
- A Requirements Coverage table mapping every `REQ`/`NFR` to design coverage

Do not force optional sections when they are irrelevant.

## Pre-Save Validation

1. Every binding spec requirement has design coverage.
2. Every component or decision maps to a requirement or is identified as necessary design support.
3. No design decision changes confirmed behavior.
4. File paths and repository assumptions are verified where practical.
5. Unresolved conflicts cause the command to stop rather than guess.

## Automatic Review Loop

Invoke `/codexspec:review-design <feature-dir>/design.md`.

- Automatically fix only verified defects with a deterministic remediation supported by upstream evidence or repository facts.
- Do not auto-fix advisories or choose among materially different designs.
- Run a maximum of two automatic fix-and-review rounds.
- Stop if a defect repeats, remains unresolved, or requires a user decision.

## Auto-Next Chain Advance

Read `workflow.auto_next` from `.codexspec/config.yml` (default `false`; only the literal value `true` enables it — absent, `false`, or any other value means disabled).

When `workflow.auto_next` is `true` AND the Automatic Review Loop above concluded in a passing state — the final Overall Status is `PASS` or `PASS_WITH_WARNINGS` — advance the chain automatically:

1. Emit exactly one notice line, in the interaction language, e.g. `auto_next: review passed → invoking /codexspec:spec-to-plan <feature-dir>`.
2. Invoke `/codexspec:spec-to-plan <feature-dir>` exactly once, then end this command.

Do not auto-advance when `workflow.auto_next` is disabled, or the review loop stopped at `NEEDS_REVISION` or `BLOCKED`, or stopped early per the conditions above; in those cases hand control back to the user exactly as the review loop already does. This advances the chain and does not modify the Output Summary.

## Output Summary

Report the design path, requirement coverage, key design decisions, unresolved items, and auto-review status.
