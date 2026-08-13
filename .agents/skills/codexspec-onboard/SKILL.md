---
name: codexspec:onboard
description: Cold-start the project profile by scanning an existing codebase for conventions and constraints
---

# Codebase Onboarding

## Language Preference

Read `.codexspec/config.yml`. Two independent language controls apply (each falls back to `language.output`, then English):

- **Interaction language** (`language.interaction`): language for all conversation with the user — questions, explanations, status messages, and `codexspec` CLI terminal output.
- **Document language** (`language.document`): language for generated artifact files (the profile records).

Converse in the interaction language and author artifacts in the document language. Apply the project's translation standard to both: translate by meaning (not word-for-word), keep English for terms with no good native equivalent, and write as if originally in that language. **Exception**: `evidence.facts` records a verbatim code observation (path + snippet) and MUST NOT be translated.

## User Input

`the text after the $codexspec:onboard skill mention`

## Role and Operating Model

`onboard` is the **cold-start / bulk counterpart to `distill`**. Where `distill` writes the project profile incrementally from interaction, `onboard` scans an **existing codebase** once and batch-writes the reusable knowledge that is **implicit in the code and not already recorded accessibly** into the shared store `.codexspec/profile/`. It exists to bootstrap a brownfield project's profile so accumulated project knowledge is grounded immediately, instead of only after enough work has flowed through `distill`.

`onboard` is **read-only on the codebase** and **write-only to `.codexspec/profile/`**: it never modifies source, tests, git state, or the constitution. It is a **standalone, user-invoked command** — not an SDD pipeline stage: it has **no auto-next successor** and **no automatic hook**, and it leaves no persistent document beyond the profile records (no map, no walkthrough — those, if ever wanted, belong to a separate `explain`).

## Prerequisite & Scaffold

Before scanning:

- If `.codexspec/` is **absent**, the project is not codexspec-initialized. **Stop** and direct the user to run `codexspec init`. Do not scaffold a whole project.
- If `.codexspec/` is present but the profile store is missing, **ensure the canonical scaffold** — the four category directories `.codexspec/profile/{constraints,conventions,pitfalls,decisions}/` (matching what `codexspec init` produces) — before writing.
- git is **not required**. onboard runs on a plain directory.

## Codebase Scan

Scan strategy is **high-signal-first over the whole repository in a single pass**:

- Respect `.gitignore`. When there is **no git / no `.gitignore`**, fall back to sensible defaults that skip vendored, build, and dependency directories (e.g. `node_modules`, `dist`, `build`, `.venv`, `target`), and say so in the summary.
- **Deep-read high-value sources**: directory structure; build / dependency / lint / formatter / type-checker config; entry points; existing docs (README, CONTRIBUTING, ADRs); test layout; and the frequently-imported core modules. **Shallow-sample** the bulk of business code rather than reading every file.
- **Stream findings to the store as you go** — write each convention as soon as it is confirmed — so the scan is **interruptible and resumable**. Do **not** block until the whole scan finishes before writing or interacting; a run interrupted mid-scan keeps what it already wrote and can be re-run to continue.
- An optional `[path]` argument (from `the text after the $codexspec:onboard skill mention`) **narrows** the scan to a single subdirectory or module.
- Never claim full coverage when you sampled — the summary distinguishes deep-read from sampled areas.

## What onboard Extracts — and What It Must NOT

Extraction uses your **flexible judgment over what the code actually shows** — not a fixed checklist of filenames or markers. onboard actively extracts **only two** of the four profile categories:

- **`conventions`** (the primary yield) — the code's observable regularities: directory/module structure, naming schemes, import style, the tech stack and toolchain (read from manifests), lint/format/type configuration, test framework and layout, and patterns repeated across the codebase. **Observable architecture / tech-stack facts** are captured here as fact-plus-steering, not as ADR-style decisions.
- **`constraints`** (narrow, high-risk) — **only** config-level **explicit hard prohibitions**: lint/type rules set to *error* that ban imports or APIs, `do not edit` / generated-file / managed-block markers, and CODEOWNERS / protected-path conventions. Every constraint candidate carries a **precise evidence anchor** (`file:line` or a config snippet). **Absent an explicit prohibition signal, propose no constraint** — silence, never a guess.

onboard **never** extracts `decisions` or `pitfalls`. A documented decision or pitfall is already readable in the repo (redundant to copy); an undocumented one is unreliable to infer from a cold scan (pitfalls are experiential; decision rationale would be fabricated). Those two categories remain `distill`'s channels, where the rationale and lived experience are available.

## Record Format

onboard **reuses `distill`'s profile store and record format verbatim** — one record per file under a category directory (`conventions/<id>.md`, `constraints/<id>.md`), ids namespaced by the source-feature id, and `claim` physically separated from `evidence`. See `distill.md` for the canonical format. onboard writes with these **deltas**:

- `provenance` marks the **onboard scan** as the source (distinct from `distill`), with `derivation: inferred` — always, because the knowledge is inferred from code, never quoted from the user.
- Because `derivation` is always `inferred`, an onboard record's `status` is always **`candidate`** — onboard **never** writes `vetted`. (`vetted` requires an explicit source verified by an outcome, and remains the `evolve` gate; promotion still goes through the normal `/distill review` path.)
- `evidence.facts` holds the **concrete code observation** — the file path plus the relevant snippet or config anchor — instead of a user quote.

## Integration with the Existing Profile

Before writing, **read the existing profile** and integrate:

- **De-duplicate** — skip anything already covered by an existing record (by judgment, not an algorithm).
- **Adjudicate conflicts** per `distill`'s order (recency → specificity → scenario-decoupling → defer); if genuinely unresolvable, write the record `status: conflict/needs-adjudication` and surface it — never block, never guess.
- **Never clobber.** onboard MUST NOT overwrite or delete any existing `vetted`, hand-authored, or `distill`-written record. It only **adds** new files (namespaced ids merge with zero conflict) or edits **its own** candidate file. This makes re-running onboard (whole repo, or a narrowed `[path]`) safe and **idempotent** — it augments without destroying.

## Safety Gate — quick review for high-risk, immediate effect for the rest

`candidate` records take local effect immediately (weighted with caution); vetting only gates `evolve`, not local effect. Because onboard is high-volume cold inference, it gates the one high-risk category and lets the bulk flow:

- **`conventions` → written immediately as `candidate`.** They take effect at once and are refined later, asynchronously and at your pace, via `/distill review`. No synchronous audit.
- **`constraints` → held for a quick in-session review at the end of the scan.** Because a wrong, top-weighted constraint would otherwise take honored-first effect unreviewed, onboard accumulates constraint candidates and, at the end, presents them for a fast review. This is a **persist / do-not-persist** decision for *this scan's* constraints — **not** a promotion to `vetted`, and **not** an invocation of `/distill review`. For each candidate you may **persist**, **edit then persist**, or **drop**; only persisted ones are written (as `candidate`). If the scan found **no** constraint candidates, there is no synchronous step.

The user reviews only the small high-risk set here; the ongoing, backlog-wide vetting of any `candidate` remains the separate asynchronous `/distill review` channel.

## Output Summary

Report concisely in the interaction language: the records added / updated per category and file, any `conflict` records deferred, and **which areas were deep-read versus sampled** (never imply full coverage when you sampled). On an empty or knowledge-free scan, write nothing and report "nothing to onboard".

## Boundaries (recap)

- Read-only on code; write-only to `.codexspec/profile/`; no source / test / git / constitution mutation.
- Standalone: no auto-next, no automatic hook, and **no Automatic Distillation step** (onboard is not a wrap-up command).
- Writes only `conventions` and `constraints`; never `decisions` or `pitfalls`.
- Produces no persistent document beyond profile records.
