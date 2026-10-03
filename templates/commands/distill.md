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

## Expression Standard

**IMPORTANT**: Everything this command produces — documents, reviews, reports, commit messages, diagnostics, and replies — is written for a reader who cannot see your working context. Apply the rules below to every artifact and message you output:

- **Write for the reader at hand-off.** Every reference must resolve without access to this session: no session-only identifiers or section numbers, no narration of what changed during the conversation, no arguments with absent reviewers. State current reality and cite committed, reachable sources.
- **Preserve every proposition.** Before summarizing or trimming, list the facts a passage carries: actors, conditions, ordering, modalities (must, never), negative guarantees, and consequences. Remove only reasoning transcripts, repetition, and decoration. Shorter is not clearer if any fact is lost.
- **State what the surface requires.** Diagnostics name what failed, which rule was violated, and the correction. Problem reports carry the defect, its location, its impact, and the evidence. Decisions record the alternatives they beat. Rejections give the reason in one line. Shipped work is described in the present tense; plans and open questions are labeled as such.
- **Define terms before relying on them.** Prefer the concrete rule, field, or behavior over a coined label; give a project-specific term a plain-language definition at first use, then use it consistently.
- **Be honest, not agreeable.** Verify claims before accepting them; fix or rebut on technical grounds. One substantiated blocker is worth more than a list of nitpicks. When a decision is needed, present only viable options, recommend one, and state the real difference between them.
- **Declare what is binding.** Say explicitly which instructions are hard requirements and where judgment is required. Keep one explanation in one place and link to it, but keep at the point of use the contract a reader needs there.

## Workspace Routing Before Writes

This section governs the location of every later file, index, branch, and commit mutation.
Record `SOURCE_ROOT` as the explicitly selected checkout (otherwise the invoking checkout) before
changing working directories. Read its `.codexspec/config.yml`: `workflow.worktrees` defaults to
on; only the literal boolean `false` disables it. Configuration remains checkout-local. Read-only
inspection keeps its original source target and does not create a worktree merely to read files.

- With `CODEXSPEC_AUTO_DEV_DELEGATION`, use the dedicated worktree supplied by auto-dev as
  `OUTPUT_ROOT` throughout. `blueprint` and `auto-dev` themselves retain their existing fixed branch
  `codexspec/auto-dev` and worktree `worktree-for-codexspec-auto-dev`; they always use the new shared
  `<repository-name>-codexspec-worktrees` parent, irrespective of the ordinary isolation switch.
- With ordinary isolation disabled, `OUTPUT_ROOT` is `SOURCE_ROOT` and existing in-place behavior
  applies. `codexspec init`, both first-time setup and installation updates, is explicitly exempt:
  it operates on its selected checkout regardless of this switch.
- For a new ordinary feature (`specify`, `quick`, or another feature-creation entry), invoke the
  installed platform create-new-feature script or `codexspec _worktree-helper create --name
  <short-name>` before the first artifact write. Parse returned JSON rather than evaluating shell
  output. `workspace`, `feature_dir`, and `requirements_file` are absolute paths; `branch` is the
  full `<feature-id>-<feature-name>`. Set `OUTPUT_ROOT` to that workspace.
- For an existing ordinary feature, resolve its explicit feature path/name first, otherwise its
  current feature branch, using `codexspec _worktree-helper resolve --feature <full-feature-name>`.
  Reuse that returned worktree. Do not silently pick another feature or create a replacement
  from main. If an explicit feature path names another checkout, use that checkout's configuration
  and preserve the identity of its documents and code.
- For standalone project-level writes without a selected ordinary feature, use
  `codexspec _worktree-helper route` from `SOURCE_ROOT`. An active feature workspace is reused;
  otherwise the helper uses `worktree-for-codexspec-maintenance`. Use the returned absolute
  workspace as `OUTPUT_ROOT`. Revalidate both source and destination rather than interpreting an
  arbitrary existing directory as a managed workspace.

When creation is interrupted, retain the returned `branch` and `workspace` even in an error
response. Resume the same identity with `codexspec _worktree-helper create --feature
<full-feature-name>`; a `creating` response from resolve requires this recovery step before
merge verification. A new `--name` request never adopts an existing identity after a random
name collision; report that collision and retry a new identity only for a genuinely new feature.

A `ready` response is required before writing feature artifacts or continuing development. Exit
status 3 with `merge_requires_resolution` or `merge_requires_verification` is a preparation handoff,
not success. Resolve conflicts and complete the merge only in the returned worktree, run the
project's required checks, and call `codexspec _worktree-helper finish --feature <full-feature-name>
--verification <json-file>` (use `worktree-for-codexspec-maintenance` for maintenance preparation).
The temporary JSON contains the verified `head`, `tree`, and `checks` entries with `command` and
integer `exit_code`; never claim a check ran when it did not. If conflicts cannot be resolved or
verification fails, stop. Retain the returned feature identity for continuation; do not create a
second feature to bypass failed preparation. Fetch warnings mean remote information may be stale;
they do not authorize bypassing an invalid baseline or failed verification.

Every mutating tool call and later SDD invocation must explicitly use `OUTPUT_ROOT` or paths inside
it. Before each file write, verify real filesystem containment: refuse symbolic links in the
output path and existing destination files with multiple hard links. A lexical path beneath
`OUTPUT_ROOT` alone does not establish isolation; never write through a link into another checkout.
A `cd` in one shell subprocess does not change the agent's later tool working directories.
Carry the same absolute workspace across stage handoffs. If required installation assets are
absent in a new worktree, run normal installation explicitly against that destination, preserving
existing project-authored files; stop if the required runtime or setup is unavailable.

Preserve input provenance: artifact-only reviews/reverse specification can read `SOURCE_ROOT`
while writing reports to `OUTPUT_ROOT`; their artifact containment checks apply to `OUTPUT_ROOT`.
Source edits and executable checks use the selected feature workspace. `commit-staged` preview
reads the original index; execution must stop if routing would substitute a different index or
mutate the protected main checkout. Do not copy, stash, stage, reset, or discard caller-owned changes
to make routing appear successful. Report an incompatible input/workspace and the required target
instead. Existing command-specific prohibitions still apply.

For configuration edits, decide routing from `SOURCE_ROOT`'s setting, then read and modify the
configuration in `OUTPUT_ROOT`. A bare toggle uses the destination's value. Report the exact path
and explain that other checkouts receive the setting through Git integration; do not add a shared
override or imply immediate changes to main's effective value. Completion retains worktrees; it
does not automatically merge to main or delete them. Any occupied path, invalid identity, failed
creation, or unusable baseline is an explicit stop, never permission to fall back to main writes.

## User Input

`$ARGUMENTS`

## Operating Model

`distill` extracts the reusable, cross-feature knowledge produced during work and persists it to the project-level store `.codexspec/profile/`. It runs two ways:

- **Auto (primary)**: embedded in wrap-up commands (`implement-tasks` on completion, `commit-staged`, `pr`), gated by `workflow.auto_distill` in `.codexspec/config.yml` (**default enabled**; disabled only when explicitly set to the literal `false`).
- **Near-moment (ambient)**: driven by the profile block's "capture knowledge as you go" rule, distill may be invoked **near the moment** reusable cross-feature knowledge is produced — in **any session**, including plain chat or a **non-SDD fix** that never reaches a wrap-up command. This is the primary way knowledge from ad-hoc work is captured at all.
- **Long-run**: in a long-running `implement-tasks`, distill **along the way** near each knowledge-producing event rather than only at the very end, so mid-task evidence is not lost to context compaction; the end-of-task `auto_distill` still runs as a **backstop**.
- **Manual (fallback)**: invoked directly on the supplied or most-recent interaction segment.

The extraction paths above are **non-blocking and non-interactive**: they never prompt, never gate another command, and **early-exit without writing** when the delta contains nothing reusable. Manual review is a separate, explicitly invoked mode described under **Vetting candidates**. Auto-distill MUST NOT invoke the review helper, never opens a browser, never waits for review, and is never gated by a saved manual-review draft.

**Input contract**: distill operates on "a segment of interaction to distill." It MUST NOT assume it is live in the conversation, so the same routine works whether embedded (fed live context) or invoked manually on a supplied segment.

## What distill captures — and what it must NOT

Capture **only** knowledge that is reusable **across features** and that the per-feature SDD artifacts structurally cannot accumulate.

Apply this boundary test to every candidate: **"Would a single feature's `requirements.md` / `spec.md` / `plan.md` record this?"**

- **Yes** → it is feature-scoped; leave it in that artifact. **Do NOT** copy it into the profile. (Requirement rationale already lives in `requirements.md`; approach rationale in plan/design.)
- **No / it spans features** → it may enter the profile.

**Never** create a feature-local store. The profile is project-level only; a feature's memory is its existing spec directory.

## The profile store: `.codexspec/profile/`

Six **category directories**, each holding **one record per file** (`<id>.md`, or `<id>-<slug>.md` — see the `id` rule below) with **only current-effective** knowledge — dense, with no "retired" section (git history is the ledger). One-file-per-record is deliberate: parallel feature branches each add differently-named files, so distilled knowledge merges without conflict. Create the directory and record file on first write.

- `constraints/` — negative constraints (`严禁 / 仅允许`). These carry the **highest** weight and MUST be honored first.
- `conventions/` — positive cross-feature conventions / steering.
- `pitfalls/` — cross-feature traps and their workarounds.
- `decisions/` — cross-feature / architectural decisions only (ADR-lite). **Never** single-feature requirement rationale.
- `strategies/` — metacognitive `trigger → action` rules: when you recognize signal X, switch to approach Y. A **self-model** (knowledge about the agent's own recurring slips in this project) lives here too, marked `scope: self`. A strategy is the layer **above** a pitfall — the transferable "what to do when" generalized across many specific traps.
- `runbooks/` — ordered multi-step procedures with failure recovery: how to carry out a known multi-step task (e.g. a release), step by step, including what to do when a step fails.

There is **no** `facts/` category — a bare fact with no "therefore do X" is either feature-scoped (leave it in `requirements.md`) or belongs as a `convention`/`constraint` with an evidence anchor.

### Record format — `claim` and `evidence` physically separated

Every record MUST separate the distilled claim from the evidence it rests on:

- `id` — **type letter + full source-feature id + local sequence**, e.g. `P-2026-0812-14054p-1` or `Con-2026-0812-14054p-1`. The `### <id>: <title>` heading keeps the bare id; the **filename** is `<id>-<slug>.md`, where the **slug** is a semantic suffix derived from the record title: lowercase ASCII letters and digits with hyphens as separators (`^[a-z0-9]+(-[a-z0-9]+)*$`, no leading/trailing hyphen), at most 50 characters, rendered in English when the title is not ASCII. When no meaningful slug can be derived, write the legacy bare form `<id>.md` — both forms are valid store members. The slug never enters the id, the heading, or `[[id]]` links, and never participates in uniqueness. Locating a record from its id stays mechanical: the record's file is exactly the one named `<id>.md` or the one named `<id>-<slug>.md`; because the slug admits only `[a-z0-9-]`, no other filename can begin with `<id>` followed by `-` or `.`, so a lookup by id is unambiguous even when one sequence number is a digit-prefix of another. The **source-feature id** is the distilling feature's full spec-dir id `{YYYY-MMDD-HHMM}{rr}` (e.g. `2026-0812-14054p`); it is globally unique by the timestamp+random scheme spec directories use, so records distilled on parallel feature branches never collide on id **or filename** (they merge with no conflict) — uniqueness is carried entirely by the id. Keep the **full** id (not a short tail) so the record is self-describing: the date supports recency/staleness reading, and the feature id ties the record to its originating change for decision context and scope. When distilling with no feature context, generate a fresh `{YYYY-MMDD-HHMM}{rr}` id now (same convention as create-new-feature). **Never** use a bare sequential id such as `P-001` — those collide across parallel branches.
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

Example — a `convention` (claim + evidence is enough), file `conventions/Con-2026-0809-2219gg-1-prefer-absolute-imports.md`:

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

Example — a `pitfall` (note the required `root-cause` / `workaround` / `lesson` body), file `pitfalls/P-2026-0810-1330ab-1-re-sub-string-replacement-corruption.md`:

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

Example — a `strategy` (note the `trigger` / `action` body), file `strategies/S-2026-0813-1606fz-1-suspect-markdown-emphasis-first.md`:

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

Example — a `runbook` (note the ordered `steps` + `failure-recovery` body), file `runbooks/R-2026-0813-1143el-1-release-a-new-codexspec-version.md`:

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

- `add` — create a new record file `<category>/<id>-<slug>.md` (bare `<category>/<id>.md` when no meaningful slug applies) for a verified item.
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

Auto-distill writes `candidate` records non-interactively and **never prompts**. A direct `/distill review`, or a direct `/distill` with no new segment to distill, enters manual review. Manual review defaults to the local HTML carrier; use the explicit text fallback only when the user requests it or a browser is unsuitable. Auto-distill MUST NOT invoke the review helper.

### Prepare semantic proposals, then hand control to deterministic code

The Agent performs semantic work **before** the UI starts: read the pending candidates, identify their editable structured fields, and draft a generalized consolidation record for every discovered cluster. Put candidate suggestions and required consolidation proposals in a **versioned proposal manifest** in an operating-system temporary file outside the repository:

```json
{
  "schema_version": 1,
  "proposals": {
    "<record-id>": {
      "base_hash": "<sha256-of-current-record-bytes>",
      "fields": {"claim": "<suggested claim>"}
    }
  },
  "consolidations": [
    {
      "cluster": "<cluster-key>",
      "members": ["<record-id>"],
      "member_hashes": {"<record-id>": "<sha256-of-current-member-bytes>"},
      "category": "<target-category>",
      "record_id": "<new-record-id>",
      "filename": "<new-record-filename>.md",
      "markdown": "<complete proposed record>",
      "fields": {"claim": "<editable value>", "scope/when": "<editable value>"}
    }
  ]
}
```

Suggestions and consolidation proposals are untrusted inputs. The helper re-scans the profile, checks every proposal base hash, requires an exact current-byte hash for every consolidation member, checks protected identity, and rejects a stale or invalid manifest. Candidate suggestions are optional, but every discovered consolidation cluster MUST have exactly one generalized proposal so HTML and text review can offer the complete merge-or-keep-separate decision. Omit the manifest only when there are no consolidation clusters and no useful candidate suggestions; ordinary candidate-only review still works without it. Delete the temporary manifest after the helper finishes.

Invoke the packaged helper exactly through the installed CLI:

```text
codexspec _distill-review-helper --project-root . --manifest <temporary-manifest-path>
```

For the explicit fallback, add `--mode text`. The helper is hidden from the documented CLI surface; it exists so the slash command can cross into deterministic code without asking the user to edit files.

If the helper reports a structurally invalid saved draft, preserve that file and show the diagnostic. Only after the user explicitly chooses to discard the damaged session, rerun the helper with `--discard-draft`; never delete a damaged draft implicitly.

The helper starts a token-protected service bound only to `127.0.0.1`, opens the packaged offline HTML page, and prints the local URL if browser launch fails. The UI lists every candidate and consolidation cluster. For each candidate the user may vet, revise structured fields, discard, or defer. Revision cannot change the record ID, category, provenance, or file identity. After revision the user chooses candidate or vetted status. A candidate without recorded outcome verification cannot become `vetted` until the user supplies the verification result or evidence.

Every decision is staged in a recoverable, Git-excluded project draft. Nothing changes in `.codexspec/profile/` until the user reviews the complete summary and selects **Apply all**. The deterministic backend—not the Agent—validates typed `vet` / `replace` / `remove` / `merge` operations, rechecks source hashes, and applies the batch with recoverable all-or-nothing semantics. Any conflict stops the whole batch, preserves the draft, and identifies the affected records. Cancel never applies profile mutations; discard removes only the saved draft.

The user's approval in this UI **is** the human endorsement half of the `vetted` gate. An approved candidate that is already outcome-verified becomes `vetted` regardless of its original `derivation`. If a candidate has not yet been outcome-verified, the UI requires an attested outcome before promotion. This is the path by which inferred knowledge—including everything `/codexspec:onboard` writes—reaches `vetted` and becomes `evolve`-eligible.

**Consolidation review.** In the same HTML or text review, show every consolidation cluster and the Agent-proposed general rule plus its exceptions as structured editable fields with a final Markdown preview. The user may merge as candidate, merge as vetted when verification is complete, or keep the members separate. On confirmed merge, the deterministic backend creates the generalized record and removes every superseded member in the same batch. Keeping records separate leaves their profile files untouched. Distill only ever marks clusters; a merge still happens only on explicit human confirmation.

## Self-check before finishing

A lightweight judgment pass (not an engineered lint) over what you just wrote:

- **Not hollow** — every `pitfall` states `root-cause` + `workaround` + `lesson`, not just a `claim`. If it collapses to one line, either flesh it out or drop it.
- **Links resolve** — any `[[id]]` cross-link points to an existing record file under `.codexspec/profile/`, or is an intentional forward reference to one you are also writing now. Don't leave a link to a record that will never exist.

## Output

Report concisely in the interaction language: which records were added / replaced / removed and in which file, any `conflict` records deferred, or "nothing to distill" on early-exit. distill **never** gates the caller.
