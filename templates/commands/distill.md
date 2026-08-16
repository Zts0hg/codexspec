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
- **Near-moment (ambient)**: driven by the profile block's "capture knowledge as you go" rule, distill may be invoked **near the moment** reusable cross-feature knowledge is produced — in **any session**, including plain chat or a **non-SDD fix** that never reaches a wrap-up command. This is the primary way knowledge from ad-hoc work is captured at all.
- **Long-run**: in a long-running `implement-tasks`, distill **along the way** near each knowledge-producing event rather than only at the very end, so mid-task evidence is not lost to context compaction; the end-of-task `auto_distill` still runs as a **backstop**.
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

Six **category directories**, each holding **one record per file** (`<id>.md`) with **only current-effective** knowledge — dense, with no "retired" section (git history is the ledger). One-file-per-record is deliberate: parallel feature branches each add differently-named files, so distilled knowledge merges without conflict. Create the directory and record file on first write.

- `constraints/` — negative constraints (`严禁 / 仅允许`). These carry the **highest** weight and MUST be honored first.
- `conventions/` — positive cross-feature conventions / steering.
- `pitfalls/` — cross-feature traps and their workarounds.
- `decisions/` — cross-feature / architectural decisions only (ADR-lite). **Never** single-feature requirement rationale.
- `strategies/` — metacognitive `trigger → action` rules: when you recognize signal X, switch to approach Y. A **self-model** (knowledge about the agent's own recurring slips in this project) lives here too, marked `scope: self`. A strategy is the layer **above** a pitfall — the transferable "what to do when" generalized across many specific traps.
- `runbooks/` — ordered multi-step procedures with failure recovery: how to carry out a known multi-step task (e.g. a release), step by step, including what to do when a step fails.

There is **no** `facts/` category — a bare fact with no "therefore do X" is either feature-scoped (leave it in `requirements.md`) or belongs as a `convention`/`constraint` with an evidence anchor.

### Record format — `claim` and `evidence` physically separated

Every record MUST separate the distilled claim from the evidence it rests on:

- `id` — **type letter + full source-feature id + local sequence**, e.g. `P-2026-0812-14054p-1` or `Con-2026-0812-14054p-1`. It is **both** the record's `### <id>: <title>` heading **and its filename** (`pitfalls/P-2026-0812-14054p-1.md`). The **source-feature id** is the distilling feature's full spec-dir id `{YYYY-MMDD-HHMM}{rr}` (e.g. `2026-0812-14054p`); it is globally unique by the timestamp+random scheme spec directories use, so records distilled on parallel feature branches never collide on id **or filename** (they merge with no conflict). Keep the **full** id (not a short tail) so the record is self-describing: the date supports recency/staleness reading, and the feature id ties the record to its originating change for decision context and scope. When distilling with no feature context, generate a fresh `{YYYY-MMDD-HHMM}{rr}` id now (same convention as create-new-feature). **Never** use a bare sequential id such as `P-001` — those collide across parallel branches.
- `claim` — one-sentence reusable **summary** (a title line, not the actionable body — for a `pitfall` the usable content lives in the three body parts below, not in this sentence).
- `type` — `convention` | `constraint` | `pitfall` | `decision` | `strategy` | `runbook` (`constraint` = highest priority).
- `scope/when` — natural-language applicability condition (e.g. "when editing Python code"); omit for global. **No formal syntax.**
- `evidence.facts` — the concrete observations behind it; **quote the user's original words, do not paraphrase**.
- `evidence.state` — the context/validity when true (feature / commit / config; still valid?).
- `provenance` — source feature/session, trigger, timestamp, `derivation = explicit | inferred`, `confidence = high | medium | low`. `derivation` records only **how the claim was first obtained** (the user's own words vs inferred); it is **not** a gate on `status` (see below).
- `status` — `candidate` | `vetted` | `conflict/needs-adjudication`. A record is `vetted` **only** when BOTH (a) it was **verified by an outcome** (a test passed, a workaround worked) AND (b) a **human endorsed it** — either it came from the user's own words (`derivation: explicit`) **or** the user approved it in `/distill review`. `derivation` is **not** itself a gate: an `inferred` record that is outcome-verified and human-approved becomes `vetted` and is eligible for `evolve`. Un-verified speculation MUST NOT be `vetted`. `conflict/needs-adjudication` marks a deferred conflict (see Conflict adjudication) and is not `evolve`-eligible. Only `vetted` records are eligible for `evolve`.

**Pitfall records carry more than a claim.** A `pitfall` (or any trap-type record) MUST, beyond `claim` and `evidence`, spell out three body parts — a bare "here is the trap" record is a defect (the next person just re-hits it):

- `root-cause` — *why* the trap happens (the underlying mechanism), not merely what it is.
- `workaround` — the concrete way around it, with the code / paths / commands to apply.
- `lesson` — the transferable takeaway that generalizes beyond this one instance.

If you cannot state all three, the pitfall is not yet understood well enough to record. `convention` / `constraint` / `decision` records usually need only `claim` + `evidence`; this three-part body is required specifically for traps.

**Strategy records carry a `trigger → action` body.** A `strategy` MUST, beyond `claim` and `evidence`, spell out two parts:

- `trigger` — the **signature** by which you recognize you are in this situation (e.g. "a substring contract test fails", "a fix is not converging after several attempts"). This is what lets the strategy be recalled by the situation, not by remembering the one incident that produced it.
- `action` — what to do when the trigger fires.

A **self-model** — a strategy about your *own* recurring slip (e.g. "I keep forgetting to regenerate derived forms") — is a strategy marked `scope: self`; its `trigger` is self-referential but the body is identical.

**Runbook records carry an ordered body.** A `runbook` MUST, beyond `claim` and `evidence`, spell out:

- `steps` — the ordered steps to carry out the task.
- `failure-recovery` — for the steps that can fail, what to do to recover (the branch that a flat one-line record loses).

If you cannot state these parts, the strategy or runbook is not yet worth recording — the same anti-hollow bar as pitfalls.

> **onboard variant**: `/codexspec:onboard` writes to this same store and format, with one difference — its records are inferred from code, so `evidence.facts` holds a verbatim **code observation** (path + snippet) instead of a user quote, `provenance` marks the onboard scan, and `derivation` is always `inferred`. onboard therefore writes `status: candidate` **at write time** (it never writes `vetted` itself); such a record can still be promoted to `vetted` later once it is outcome-verified and approved in `/distill review` — its `inferred` origin is not a barrier (per the `status` rule above).

This separation is what makes a later error locatable as **misread** (facts wrong) vs **overreach** (claim over-generalized) vs **stale** (state no longer holds).

Example — a `convention` (claim + evidence is enough), file `conventions/Con-2026-0809-2219gg-1.md`:

```markdown
### Con-2026-0809-2219gg-1: Prefer absolute imports
- claim: Always use absolute imports in `src/`.
- type: convention
- scope/when: Python modules under `src/`
- evidence.facts: "Use absolute imports; relative ones broke the packaged wheel last time."
- evidence.state: confirmed at feature 2026-0809-2219gg; commit a1b2c3d
- provenance: distill @implement-tasks, 2026-08-09, derivation: explicit, confidence: high
- status: vetted
```

Example — a `pitfall` (note the required `root-cause` / `workaround` / `lesson` body), file `pitfalls/P-2026-0810-1330ab-1.md`:

```markdown
### P-2026-0810-1330ab-1: `re.sub` with a string replacement corrupts blocks containing backslashes
- claim: Inject a rendered block with a function replacement in `re.sub`, never a string.
- type: pitfall
- scope/when: upserting a rendered block into a file via `re.sub` in `src/`
- root-cause: a string replacement passed to `re.sub` interprets `\g<...>` and backslash escapes, so any such sequence inside the block silently corrupts the output.
- workaround: pass a callable replacement — `pattern.sub(lambda _m: block, text)` — so the block is inserted verbatim.
- lesson: whenever the replacement is data (not a pattern), use the callable form; the same trap applies in any language whose replace interprets `$1` / `\1`.
- evidence.facts: the injected block contained `\g<0>` and rendered as garbage until switched to the lambda form.
- evidence.state: confirmed at feature 2026-0810-1330ab; commit c0ffee1. Still valid.
- provenance: distill @implement-tasks, 2026-08-10, derivation: inferred, confidence: high
- status: candidate
```

Example — a `strategy` (note the `trigger` / `action` body), file `strategies/S-2026-0813-1606fz-1.md`:

```markdown
### S-2026-0813-1606fz-1: When a substring contract test fails, suspect markdown emphasis first
- claim: A failing substring assertion over a prose template is usually a wrong assertion, not a wrong template.
- type: strategy
- scope/when: writing or debugging substring contract tests over `templates/commands/*.md`
- trigger: a `test_*_template.py` substring assertion fails on a phrase you believe the template contains.
- action: check whether the template wrote inline `**`/`*`/backticks inside the asserted span before touching the template; re-target the assertion at an emphasis-free span.
- evidence.facts: "断言 span 里含 `**not**` 导致子串匹配失败"
- evidence.state: confirmed at feature 2026-0813-1606fz; still valid.
- provenance: distill @implement-tasks, 2026-08-13, derivation: inferred, confidence: high
- status: candidate
```

Example — a `runbook` (note the ordered `steps` + `failure-recovery` body), file `runbooks/R-2026-0813-1143el-1.md`:

```markdown
### R-2026-0813-1143el-1: Release a new CodexSpec version
- claim: The end-to-end steps (and failure recovery) to cut a release.
- type: runbook
- scope/when: publishing a new version of this repo
- steps: 1) bump the version manually in `pyproject.toml`, `__version__`, and `uv.lock`; 2) run `publish.sh`; 3) push the tag; 4) commit the marketplace update.
- failure-recovery: if the `pip-audit` pre-commit hook aborts on a transient SSL error, reset the half-applied bump and re-run with `SKIP=pip-audit`.
- evidence.facts: "publish.sh 不自动 bump __version__；pip-audit 偶发 SSL 失败中止发布"
- evidence.state: confirmed at feature 2026-0813-1143el; still valid.
- provenance: distill @implement-tasks, 2026-08-13, derivation: inferred, confidence: high
- status: candidate
```

## Extraction

Read the interaction segment and extract, per the dimensions above, only **verified** knowledge — prefer facts confirmed by outcomes over speculation; speculation MUST NOT become `vetted`.

Before writing, **read the current profile** (the record files under each category directory) and skip anything already covered; update anything changed via `replace`. **This is how deduplication is done — by judgment, not an algorithm.**

## Debounce across the trigger surface

distill can now fire from several points close together — the near-moment ambient rule, the long-run along-the-way calls, and the wrap-up hooks (`implement-tasks` → `commit-staged` → `pr`) — often over largely the **same** work. To avoid re-distilling and near-duplicate records, apply a lightweight debounce:

- **Session-local boundary.** Keep a **session-local already-distilled boundary** — your own memory, in this conversation's context, of what you have already distilled this session and up to which point of the interaction. This is held **in conversation context**; introduce **no persistent runtime state** (no marker file, no counter on disk).
- **Delta-only.** On a later trigger, distill only the **substantive new delta** since that boundary. If nothing substantive was produced since, **early-exit** (report "nothing to distill") without deep-reading the whole profile.
- **Cross-session fallback.** When the boundary is unavailable — a new session, or context was compacted — there is no session memory to lean on, so distill **falls back to reading the profile and skipping covered records** (the judgment dedup above). Worst case is one extra early-exiting scan, never a duplicate.

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

## Consolidation (compress narrow records into general rules)

Growth is not just accumulation: many narrow records on one theme should compress into **one general rule plus its exceptions** (the way experience compacts into judgment). distill performs the **detect-and-mark** half automatically; a human performs the **merge** half in `/distill review`.

- **Mark, don't merge.** When you notice a cluster of narrow records sharing a generalization (e.g. several derived-artifact pitfalls, or several lockstep conventions), **mark** them as **consolidation candidates** by writing a **per-record field** into each member's own file — `consolidation: candidate; cluster: <short-theme-key>` — using the same shared `<short-theme-key>` on every member. This is judgment, not an algorithm. It is **non-destructive**: marking **does not auto-rewrite or delete** any record.
- **No central index.** The cluster lives only as that shared key across the members' own files — there is **no central index** or manifest file (which would be a merge-conflict magnet and break the conflict-free store). `/distill review` discovers a cluster by scanning for records that share a `cluster:` key.
- **Cross-category promotion.** A consolidation may cross categories — e.g. **promoting several** `pitfalls` **into one** `strategy` (the transferable "what to do when" above the individual traps). The general record is written in whichever category fits the generalized claim.

The merge itself is confirmed by a human in `/distill review` (below); distill never merges unattended.

## Vetting candidates (manual, interactive)

Auto-distill writes `candidate` records non-interactively and **never prompts**. Promote them through the **manual review mode** — `/distill review` (or `/distill` with no new segment to distill): list every pending `candidate` compactly (claim + evidence + provenance) and let the user approve inline — "vet all", "vet 1,3", "edit 2", "drop 4". Apply the choices by editing each record's `status` (a `replace`). **The user never hand-edits the profile files.**

The user's approval here **is** the human endorsement half of the `vetted` gate: an approved `candidate` that is already outcome-verified becomes `vetted` **regardless of its original `derivation`** (an `inferred` record is not blocked from vetting). If a candidate has not yet been outcome-verified, approval keeps it `candidate` (or the user may attest the outcome to complete the gate). This is the path by which `inferred` knowledge — including everything `/codexspec:onboard` writes — reaches `vetted` and becomes `evolve`-eligible.

**Consolidation review.** In the same review mode, also surface any **consolidation candidate** clusters (records sharing a `cluster:` key, from the Consolidation section above): show the cluster's members compactly and let the user confirm the merge inline — "merge 1", "merge all", "keep separate". On confirmation, write the single general record (a **general rule plus its exceptions**), `remove` the superseded members, and clear the `cluster:`/`consolidation:` marker from anything that survives so no stale flag lingers. If the user declines, leave every member untouched. distill only ever **marked** the cluster; the merge happens **only** here, on explicit confirmation.

## Self-check before finishing

A lightweight judgment pass (not an engineered lint) over what you just wrote:

- **Not hollow** — every `pitfall` states `root-cause` + `workaround` + `lesson`, not just a `claim`. If it collapses to one line, either flesh it out or drop it.
- **Links resolve** — any `[[id]]` cross-link points to an existing record file under `.codexspec/profile/`, or is an intentional forward reference to one you are also writing now. Don't leave a link to a record that will never exist.

## Output

Report concisely in the interaction language: which records were added / replaced / removed and in which file, any `conflict` records deferred, or "nothing to distill" on early-exit. distill **never** gates the caller.
