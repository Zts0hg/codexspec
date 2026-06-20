---
description: 将已确认的规格转换为可追溯的技术计划
argument-hint: "[spec.md 或 功能目录]"
handoffs:
  - agent: claude
    step: Generate a technical plan constrained by confirmed requirements
---

# Specification to Plan Converter

## Language Preference

Read `.codexspec/config.yml`. Use `language.output`; default to English.

## User Input

`$ARGUMENTS`

## Role

Act as a **constrained technical designer**. Define how to implement the specification while preserving confirmed user intent.

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
4. Plan-level technical decisions
5. General best practices

Before designing, verify that `spec.md` covers the confirmed requirements. Stop if it omits, contradicts, or silently expands them.

Stop and request a user decision when:

- The plan would change confirmed scope, behavior, constraints, or trade-offs.
- Two reasonable approaches produce materially different user outcomes.
- A critical `OPEN-*` item blocks a safe design.
- The specification conflicts with the constitution or verified repository facts.

## Planning Rules

- Every component, interface, data change, and implementation phase must include `Covers: REQ-xxx`.
- Record new technical choices as **Plan-Level Decisions** with evidence, rationale, alternatives considered when material, and accepted trade-offs.
- Plan-level decisions may refine implementation but cannot redefine product intent.
- Reuse repository patterns before introducing new abstractions or dependencies.
- Include architecture diagrams, dependency graphs, API contracts, schemas, version constraints, security, performance, deployment, or observability only when they materially help implement or verify this feature.
- Explicitly identify assumptions. Do not convert assumptions into requirements.
- Prefer the smallest architecture that satisfies the confirmed requirements.

## Required Output

Save `<feature-dir>/plan.md` using the appropriate simple or detailed template.

Include:

- Context, goals, and non-goals inherited from the specification
- Relevant existing repository constraints
- Technical approach and plan-level decisions
- Components/interfaces with `Covers:`
- Implementation phases derived from the actual design
- Verification strategy
- Risks and trade-offs that affect delivery
- Requirements coverage table mapping every `REQ`/`NFR` to plan references

Do not force a standard five-phase structure when the design calls for a different sequence.

## Pre-Save Validation

1. Every binding spec requirement has plan coverage.
2. Every plan component maps to a requirement or is identified as necessary implementation support.
3. No plan decision changes confirmed behavior.
4. File paths and repository assumptions are verified where practical.
5. Unresolved conflicts cause the command to stop rather than guess.

## Automatic Review Loop

Invoke `/codexspec:review-plan <feature-dir>/plan.md`.

- Automatically fix only verified defects with a deterministic remediation supported by upstream evidence or repository facts.
- Do not auto-fix advisories or choose among materially different designs.
- Run a maximum of two automatic fix-and-review rounds.
- Stop if a defect repeats, remains unresolved, or requires a user decision.

## Output Summary

Report the plan path, requirement coverage, plan-level decisions, unresolved items, and auto-review status.
