---
name: codexspec-quick
description: "一站式快速实现小型需求：读取宪法和配置，完成轻量澄清，然后自动推进 spec、plan、tasks 和代码实现。适用于范围小、模块少、无需新增依赖的需求。"
---

# CodexSpec Quick

Use this skill when the user wants to complete a small, self-contained requirement in one flow.

## Preconditions

1. Read `.codexspec/memory/constitution.md` before making decisions.
2. Check whether `.codexspec/config.yml` exists.
3. If configuration exists, follow `language.output` for user-facing responses.
4. If configuration does not exist, continue with English defaults for the current session and suggest using `codexspec-config` later.

## Scope Check

Treat this skill as appropriate only when most of these are true:

- The change is likely to touch no more than 3 files
- The work stays within a single module or narrow feature slice
- No new external dependency is needed

If the requirement looks medium or large, say so clearly and recommend switching to the standard CodexSpec flow with skills such as `codexspec-specify`, `codexspec-generate-spec`, `codexspec-spec-to-plan`, `codexspec-plan-to-tasks`, and `codexspec-implement-tasks`.

## Workflow

1. Summarize the requirement and identify only the ambiguities that materially affect implementation.
2. Ask concise clarification questions only when necessary.
3. Create or update the relevant artifact set under `.codexspec/specs/<feature-id>/`:
   - `spec.md`
   - `plan.md`
   - `tasks.md`
4. Implement the required code changes.
5. Run the most relevant verification available.
6. Report what was created, what changed, and any remaining risks.

## Artifact Guidance

- `spec.md` focuses on what and why.
- `plan.md` focuses on how.
- `tasks.md` should be ordered, specific, and actionable.

## Output Style

- Keep progress visible.
- Be explicit when complexity exceeds the quick path.
- Prefer completing the full flow over stopping after documentation unless the user asks to pause.
