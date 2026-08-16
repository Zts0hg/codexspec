---
description: Compile vetted project-profile knowledge into a reusable command/skill and contribute it upstream via a reviewed PR
argument-hint: "[what to evolve, or a profile area]"
---

# Evolve

## Language Preference

Read `.codexspec/config.yml`. Two independent language controls apply (each falls back to `language.output`, then English):

- **Interaction language** (`language.interaction`): language for all conversation with the user — questions, explanations, status messages, and `codexspec` CLI terminal output.
- **Document language** (`language.document`): language for generated artifact files.

Converse in the interaction language. **The compiled command/skill draft is a distributed template and MUST be authored in English** (project i18n convention), regardless of `language.document`. PR title/body follow `language.commit`.

## User Input

`$ARGUMENTS`

## Operating Model

`evolve` turns **vetted** sediment in `.codexspec/profile/` into a reusable capability and contributes it back to CodexSpec through a **human-reviewed PR**. It **never merges unattended** and **never** edits install artifacts.

## Selecting what to promote

Promote only records that are **both**:

1. `status: vetted` (never `candidate` or `conflict`), and
2. **general enough for the toolkit** — the generality extension of distill's boundary test: *"Is this useful to every CodexSpec user, or only to this project?"*

Project-specific knowledge **stays** in the profile. Only generally-useful capability is promoted upstream. When nothing qualifies, stop and report — do not force a promotion.

This selection spans **all six** profile categories. `strategies/` (metacognitive `trigger → action` rules) and `runbooks/` (ordered multi-step procedures) are often the **most** promotable material — a vetted, general strategy or runbook compiles cleanly into a reusable skill/command — but they clear the **same** `vetted` gate as every other category; the gate is unchanged.

## Compiling the draft

Compile the selected sediment into a SKILL.md / command-template draft that conforms to both:

- **Anthropic Agent Skills** (SKILL.md + progressive disclosure), and
- **existing CodexSpec command-template conventions** (YAML frontmatter + sections + `## Language Preference`, English).

Apply these compile rules:

- **Priority order** — core needs first, **negative constraints immediately after (highest weight)**, then the rest.
- **Logic-clean** — `replace`/`remove` any superseded rule first; the output MUST carry **no** contradictory rules.
- **Imperative wording** — use **必须 / 始终 / 严禁 / 仅允许** in place of 可以考虑 / 尽量 / 最好不要 / 或许. Match the project's explicit **Prefer / Avoid** rule style; do not use decorative markers.

## Where output goes (self-bootstrap)

Write **only** under `templates/` — a new `templates/commands/*.md` or a standalone skill package. **NEVER** edit `.claude/commands/codexspec/`: it is a regenerated install artifact, and any edit there is silently overwritten on the next reinstall and never reaches users. Changes reach users via `publish` → `init`.

## Contribution mechanics

**Before any `git push` or PR creation, present the compiled draft file(s) and the value statement to the user and obtain explicit approval. Proceed only on approval; NEVER push or open a PR unattended.** (Writing a local draft under `templates/` is git-reversible; the outward action is what is gated.)

On approval, open a PR for human review. **Auto-detect** the git path — this is a mechanics difference only, never a permission tier:

- Upstream **write access** → push a branch in-repo and open the PR.
- **No write access** → fork, push to the fork, open a cross-repo PR.

Both take the **identical** review path.

## Value gate and PR summary

Produce a one-sentence **value statement** as the PR summary:

> Resolves `<pain>`, by `<added/revised constraint>`, achieving `<quality/efficiency gain>`.

If no crisp value statement can be written, **open NO PR** — the batch is not worth promoting (this is the lightweight substitute for a metric/eval gate).

For review, keep each promoted `claim` paired with its `evidence` so a reviewer can check **claim ⇐ evidence**. A promoted change that later proves worse MUST be rolled back via `remove`/`replace` (git-traceable), not a manual file edit.

## Output

Report in the interaction language: what was selected, the draft file(s) written under `templates/`, and the PR (branch or fork) with its value statement — or **"nothing promoted"** with the reason (value gate / nothing vetted / nothing general enough).
