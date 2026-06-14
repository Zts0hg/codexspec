---
description: 一站式快速实现小型需求 — 自动完成 spec、plan、tasks 和代码实现
argument-hint: "描述你的需求"
---

# Quick Implementation

## Language Preference

Read `.codexspec/config.yml`. Use `language.output`; default to English.

## User Input

`$ARGUMENTS`

## Scope Check

Quick is intended for a small, well-bounded change. Assess likely files, module span, new dependencies, and unresolved product decisions.

If the change is broad or has multiple independent outcomes, explain why the standard flow is safer and ask whether to continue with Quick.

## Compact Requirement Confirmation

Even in Quick mode, do not rely on session-only context.

1. Resolve only ambiguities that materially change implementation.
2. Create a feature workspace and `requirements.md` using the same timestamp feature convention as `/codexspec:specify`.
3. Present a concise confirmed requirement summary containing:
   - `NEED-*`
   - relevant `CON-*` and `DEC-*`
   - `OUT-*`
   - unresolved `OPEN-*`
4. Ask the user to confirm the summary.
5. Persist only confirmed entries, with short User Evidence and a Confirmation Log.

Do not start generation before confirmation. If a critical question remains open, stop.

## Automated Flow

Use the created feature directory explicitly for every command:

1. `/codexspec:generate-spec <feature-dir>/requirements.md`
2. `/codexspec:spec-to-plan <feature-dir>/spec.md`
3. `/codexspec:plan-to-tasks <feature-dir>/plan.md`
4. `/codexspec:implement-tasks <feature-dir>/tasks.md`

The generation commands own their automatic review loops. Do not duplicate review logic here.

If a review requires a new product or architecture decision, pause Quick and ask the user. Do not infer a decision merely to preserve automation.

## Completion

Report the feature directory, requirements/spec/plan/tasks paths, review outcomes, implementation verification, and unresolved advisories separately.
