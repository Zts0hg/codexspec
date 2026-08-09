---
description: Distill reusable, cross-feature knowledge from an interaction into the project profile
argument-hint: "[interaction segment or context to distill]"
---

# Distill

## Language Preference

Read `.codexspec/config.yml`. Two independent language controls apply (each falls back to `language.output`, then English):

- **Interaction language** (`language.interaction`): language for all conversation with the user — questions, explanations, status messages, and `codexspec` CLI terminal output.
- **Document language** (`language.document`): language for generated artifact files (the profile records).

Converse in the interaction language and author artifacts in the document language. Apply the project's translation standard to both: translate by meaning (not word-for-word), keep English for terms with no good native equivalent, and write as if originally in that language. **Exception**: `evidence.facts` quotes the user's original words verbatim and MUST NOT be translated.

## User Input

`$ARGUMENTS`

## Operating Model

`distill` extracts the reusable, cross-feature knowledge produced during work and persists it to the project-level store `.codexspec/profile/`. It runs two ways:

- **Auto (primary)**: embedded in wrap-up commands (`implement-tasks` on completion, `commit-staged`, `pr`), gated by `workflow.auto_distill` in `.codexspec/config.yml` (**default enabled**; disabled only when explicitly set to the literal `false`).
- **Manual (fallback)**: invoked directly on the supplied or most-recent interaction segment.

distill is **non-blocking and non-interactive**: it never prompts, never gates another command, and **early-exits without writing** when the delta contains nothing reusable.

**Input contract**: distill operates on "a segment of interaction to distill." It MUST NOT assume it is live in the conversation, so the same routine works whether embedded (fed live context) or invoked manually on a supplied segment.

## What distill captures — and what it must NOT

Capture **only** knowledge that is reusable **across features** and that the per-feature SDD artifacts structurally cannot accumulate.

Apply this boundary test to every candidate: **"Would a single feature's `requirements.md` / `spec.md` / `plan.md` record this?"**

- **Yes** → it is feature-scoped; leave it in that artifact. **Do NOT** copy it into the profile. (Requirement rationale already lives in `requirements.md`; approach rationale in plan/design.)
- **No / it spans features** → it may enter the profile.

**Never** create a feature-local store. The profile is project-level only; a feature's memory is its existing spec directory.

## The profile store: `.codexspec/profile/`

Four markdown files, each holding **only current-effective** knowledge — dense, with no "retired" section (git history is the ledger). Create the directory and file on first write.

- `constraints.md` — negative constraints (`严禁 / 仅允许`). These carry the **highest** weight and MUST be honored first.
- `conventions.md` — positive cross-feature conventions / steering.
- `pitfalls.md` — cross-feature traps and their workarounds.
- `decisions.md` — cross-feature / architectural decisions only (ADR-lite). **Never** single-feature requirement rationale.

### Record format — `claim` and `evidence` physically separated

Every record MUST separate the distilled claim from the evidence it rests on:

- `claim` — one-sentence reusable statement.
- `type` — `convention` | `constraint` | `pitfall` | `decision` (`constraint` = highest priority).
- `scope/when` — natural-language applicability condition (e.g. "when editing Python code"); omit for global. **No formal syntax.**
- `evidence.facts` — the concrete observations behind it; **quote the user's original words, do not paraphrase**.
- `evidence.state` — the context/validity when true (feature / commit / config; still valid?).
- `provenance` — source feature/session, trigger, timestamp, `derivation = explicit | inferred`.
- `status` — `vetted` **only** when `derivation = explicit` (the user's own words) AND the item was verified by an outcome (a test passed, a workaround worked); every `inferred` item stays `candidate`. Only `vetted` records are eligible for `evolve`.

This separation is what makes a later error locatable as **misread** (facts wrong) vs **overreach** (claim over-generalized) vs **stale** (state no longer holds).

Example entry:

```markdown
### C-003: Prefer absolute imports
- claim: Always use absolute imports in `src/`.
- type: convention
- scope/when: Python modules under `src/`
- evidence.facts: "Use absolute imports; relative ones broke the packaged wheel last time."
- evidence.state: confirmed at feature 2026-0809-2219gg; commit a1b2c3d
- provenance: distill @implement-tasks, 2026-08-09, derivation: explicit
- status: vetted
```

## Extraction

Read the interaction segment and extract, per the dimensions above, only **verified** knowledge — prefer facts confirmed by outcomes over speculation; speculation MUST NOT become `vetted`.

Before writing, **read the current profile** and skip anything already covered; update anything changed via `replace`. **This is how deduplication is done — by judgment, not an algorithm.**

## Conflict adjudication

When a new item conflicts with an existing rule, resolve in this order:

1. **Recency** — newer corrections win (usually a `replace`).
2. **Specificity** — a specific instruction overrides the general one **only within its scope**.
3. **Scenario-decoupling** — if neither wins, keep **both** under a `scope/when` condition rather than forcing a winner.
4. **Defer, don't guess** — if genuinely unresolvable, write the record with `status: conflict/needs-adjudication` and surface it at the next interactive point or at evolve time. **Never block, never guess.**

## Mutation discipline

Change the profile **only** through three conceptual operations (you edit the markdown directly — these are a discipline, **not** a tool API or matching algorithm):

- `add` — append a new verified item.
- `replace` — supersede an outdated/wrong item in place (keeps files dense).
- `remove` — delete an item invalidated by a changed environment.

git history is the audit ledger. Do **NOT** keep a retired section inside the files.

## Vetting candidates (manual, interactive)

Auto-distill writes `candidate` records non-interactively and **never prompts**. Promote them through the **manual review mode** — `/distill review` (or `/distill` with no new segment to distill): list every pending `candidate` compactly (claim + evidence + provenance) and let the user approve inline — "vet all", "vet 1,3", "edit 2", "drop 4". Apply the choices by editing each record's `status` (a `replace`). **The user never hand-edits the profile files.**

## Output

Report concisely in the interaction language: which records were added / replaced / removed and in which file, any `conflict` records deferred, or "nothing to distill" on early-exit. distill **never** gates the caller.
