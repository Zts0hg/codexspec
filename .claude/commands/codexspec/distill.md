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

Four **category directories**, each holding **one record per file** (`<id>.md`) with **only current-effective** knowledge — dense, with no "retired" section (git history is the ledger). One-file-per-record is deliberate: parallel feature branches each add differently-named files, so distilled knowledge merges without conflict. Create the directory and record file on first write.

- `constraints/` — negative constraints (`严禁 / 仅允许`). These carry the **highest** weight and MUST be honored first.
- `conventions/` — positive cross-feature conventions / steering.
- `pitfalls/` — cross-feature traps and their workarounds.
- `decisions/` — cross-feature / architectural decisions only (ADR-lite). **Never** single-feature requirement rationale.

### Record format — `claim` and `evidence` physically separated

Every record MUST separate the distilled claim from the evidence it rests on:

- `id` — **type letter + full source-feature id + local sequence**, e.g. `P-2026-0812-14054p-1` or `Con-2026-0812-14054p-1`. It is **both** the record's `### <id>: <title>` heading **and its filename** (`pitfalls/P-2026-0812-14054p-1.md`). The **source-feature id** is the distilling feature's full spec-dir id `{YYYY-MMDD-HHMM}{rr}` (e.g. `2026-0812-14054p`); it is globally unique by the timestamp+random scheme spec directories use, so records distilled on parallel feature branches never collide on id **or filename** (they merge with no conflict). Keep the **full** id (not a short tail) so the record is self-describing: the date supports recency/staleness reading, and the feature id ties the record to its originating change for decision context and scope. When distilling with no feature context, generate a fresh `{YYYY-MMDD-HHMM}{rr}` id now (same convention as create-new-feature). **Never** use a bare sequential id such as `P-001` — those collide across parallel branches.
- `claim` — one-sentence reusable statement.
- `type` — `convention` | `constraint` | `pitfall` | `decision` (`constraint` = highest priority).
- `scope/when` — natural-language applicability condition (e.g. "when editing Python code"); omit for global. **No formal syntax.**
- `evidence.facts` — the concrete observations behind it; **quote the user's original words, do not paraphrase**.
- `evidence.state` — the context/validity when true (feature / commit / config; still valid?).
- `provenance` — source feature/session, trigger, timestamp, `derivation = explicit | inferred`.
- `status` — `vetted` **only** when `derivation = explicit` (the user's own words) AND the item was verified by an outcome (a test passed, a workaround worked); every `inferred` item stays `candidate`. Only `vetted` records are eligible for `evolve`.

> **onboard variant**: `/codexspec:onboard` writes to this same store and format, with one difference — its records are inferred from code, so `evidence.facts` holds a verbatim **code observation** (path + snippet) instead of a user quote, `provenance` marks the onboard scan, `derivation` is always `inferred`, and `status` is therefore always `candidate` (onboard never writes `vetted`).

This separation is what makes a later error locatable as **misread** (facts wrong) vs **overreach** (claim over-generalized) vs **stale** (state no longer holds).

Example entry — file `conventions/Con-2026-0809-2219gg-1.md`:

```markdown
### Con-2026-0809-2219gg-1: Prefer absolute imports
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

Before writing, **read the current profile** (the record files under each category directory) and skip anything already covered; update anything changed via `replace`. **This is how deduplication is done — by judgment, not an algorithm.**

## Conflict adjudication

When a new item conflicts with an existing rule, resolve in this order:

1. **Recency** — newer corrections win (usually a `replace`).
2. **Specificity** — a specific instruction overrides the general one **only within its scope**.
3. **Scenario-decoupling** — if neither wins, keep **both** under a `scope/when` condition rather than forcing a winner.
4. **Defer, don't guess** — if genuinely unresolvable, write the record with `status: conflict/needs-adjudication` and surface it at the next interactive point or at evolve time. **Never block, never guess.**

## Mutation discipline

Change the profile **only** through three conceptual operations (you edit the files directly — these are a discipline, **not** a tool API or matching algorithm):

- `add` — create a new record file `<category>/<id>.md` for a verified item.
- `replace` — supersede an outdated/wrong item **in its own file** (keeps records dense).
- `remove` — delete the record's file when a changed environment invalidates it.

git history is the audit ledger. Do **NOT** keep a retired file or a retired section.

## Vetting candidates (manual, interactive)

Auto-distill writes `candidate` records non-interactively and **never prompts**. Promote them through the **manual review mode** — `/distill review` (or `/distill` with no new segment to distill): list every pending `candidate` compactly (claim + evidence + provenance) and let the user approve inline — "vet all", "vet 1,3", "edit 2", "drop 4". Apply the choices by editing each record's `status` (a `replace`). **The user never hand-edits the profile files.**

## Output

Report concisely in the interaction language: which records were added / replaced / removed and in which file, any `conflict` records deferred, or "nothing to distill" on early-exit. distill **never** gates the caller.
