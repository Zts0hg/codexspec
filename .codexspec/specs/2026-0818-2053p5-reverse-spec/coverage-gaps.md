# Coverage Gaps: reverse-spec

**Describes commit**: `888fece` (the state a fresh isolated `review-code` passed).
**Recorded**: 2026-08-21.

**Resolution update**: 2026-08-24. G-3, G-4, and G-5 remain below as the
historical findings against `888fece`, but are resolved by the follow-up change
that also adds direct regression contracts. Re-run each entry's command before
relying on either the original or resolution claim.

## What this file is

A register of what the review gates **could not verify**, plus one product question
the confirmed requirements do not settle. It exists so these can be discussed later
without re-deriving them.

In the `review-code` protocol a **finding** must show a concrete trigger → impact
chain, and any admitted P0–P3 makes the verdict FAIL. A **coverage gap** is
different: it is an evidence or confidence limit, and the protocol explicitly
requires that an unverified material concern be recorded as a gap rather than
written up as a speculative finding. **Nothing in this file is a known defect.**

## What this file is not

It is **not** a gate status and **not** a TODO list. It makes no claim about
whether the feature is finished — that is the `implement-tasks` §7.6 gate result,
which lives in the session and the branch history.

This distinction is deliberate. A predecessor file (`issues.md`) was removed after
being flagged in two consecutive review rounds: it stated present-tense claims
about behavior, the commits that changed that behavior did not update it, and it
went on directing readers to redo finished work. A status document living inside
the diff that changes the state it describes cannot stay true.

The defence here is that **every entry carries the command that re-checks it**. If
the template moves on, a stale entry can be detected in seconds instead of being
believed. Re-verify before relying on any entry, and treat "describes commit"
above as the scope of every claim below.

## Disposition legend

| Disposition | Meaning |
|---|---|
| **Accepted** | A recorded trade-off. Closing it would reverse a confirmed decision or change the delivery form. |
| **Needs a decision** | Confirmed intent genuinely does not settle it. Requires a product call, not an implementation choice. |
| **Candidate** | Real, small, and closable without new intent. Not closed because any edit invalidates the PASS envelope pinned to `888fece`. |
| **Intentional** | Working as designed; listed so it is not mistaken for an oversight. |
| **Resolved** | The gap existed at `888fece` and has since been closed with direct verification. |

---

## G-1 — Behavior is verifiable only as written discipline

**Disposition**: Accepted (`design.md` Decision 1)

`reverse-spec` is a pure agent-driven command template, like `onboard`, `debug`,
and `distill`. Its behavior *is* its prose. The 54 contract tests in
`tests/test_reverse_spec_template.py` assert **what the template says**, not what
an agent does with it.

**Why this matters concretely**: the tests catch a rule being *deleted*. They do
not catch a rule being *wrong*. Every defect found in review rounds 6, 7, and 8 was
a semantically incorrect instruction, and the suite was fully green each time.

**What this bounds**: the PASS at `888fece` means the discipline *reads* correct
against the confirmed artifacts. It does not mean any mode was executed
end-to-end — no review round ran the command.

**Why not closed**: the alternative is a Python analysis module. `design.md`
Decision 1 rejected it — drift detection here is semantic, not syntactic, so a
module would either wrap the same judgment or narrow findings to what a parser can
see, which is narrower than the confirmed requirement.

**Re-verify**: `uv run pytest tests/test_reverse_spec_template.py -q`

---

## G-2 — `allowed-tools` is far wider than the stated Boundaries

**Disposition**: Accepted with additional written mitigation (`design.md` C10)

The final frontmatter grants general `Bash`, `Edit`, and `Write`, while
`## Boundaries` forbids modifying git state and confines writes to the feature
workspace. General Bash became necessary in T5.9 because Linux, macOS, and Windows
expose atomic no-replace directory publication through different native
primitives; the earlier onboard-identical grant could not execute the requirement.
More completely: `src/codexspec/integrations/codex.py` strips `allowed-tools`
entirely when rendering the Codex skill form, so **0 of 26 `SKILL.md` files carry
any tool restriction at all**. REQ-017's boundary remains written discipline, not
a mechanical sandbox common to both channels.

**Mitigation**: T5.9 makes the argument one separately quoted literal path, forbids
executing repository-provided commands, and permits native publication only as a
single named state transition with stop-on-unavailable behavior. T5.11 also makes
`/codexspec:onboard` a provenance reference rather than a runtime include, so a
repository-local sibling prompt cannot bypass the evidence-only rule. These rules
close the concrete input/publication/instruction-source failures without
pretending the tool grant itself is a sandbox.

**Why not closed**: a mechanically narrow cross-platform publication capability
does not exist in the current command-tool model, and Codex rendering removes the
field regardless. Closing the architectural gap requires a purpose-built helper or
tool-policy redesign across integrations, outside this feature's accepted written-
discipline delivery model.

**Re-verify**:

```bash
grep '^allowed-tools:' templates/commands/reverse-spec.md      # expect: general Bash
grep -l 'allowed-tools' .agents/skills/*/SKILL.md | wc -l      # expect: 0
```

---

## G-3 — Mode-resolution step 1 does not restate symlink resolution

**Disposition**: Resolved

**Resolution**: mode-resolution step 1 now instructs the agent to resolve symbolic
links before the repository-root comparison and explicitly routes a symlink whose
real path is the root to overview mode. A dedicated contract test guards both
clauses.

Steps 4 and 5 both state explicitly that the path is judged **after** symbolic
links are resolved. Step 1 says only "a path that resolves to the repository root",
without repeating it.

The round-9 reviewer could not confirm a failure path and therefore recorded a gap.
An independent trace during the follow-up discussion suggests it is more reachable
than that, if an agent reads step 1 lexically:

```
repo contains  ln -s . self  ;  run  reverse-spec self
  step 1  "self" read literally != repo root  ->  no short-circuit   <- the ambiguity
  step 4  resolves to repo root, which is inside the repo  ->  not refused
  step 5  normalization resolves the symlink  ->  becomes the repo root
  step 7  no match  ->  generate  ->  whole-repository detailed spec.md
```

That last step is what NFR-005 forbids unconditionally and what DEC-014 was
confirmed to close.

**Backstop**: `## Slice and Workspace` carries an unconditional rule — "The
repository root is not a slice: a path that resolves to it is the bare run" — which
would very likely catch this in practice. The concern is the inconsistency itself:
one rule stated three ways across three steps is the shape that produced repeated
findings in rounds 3–8.

**Cost to close**: one clause in step 1, plus a contract assertion.

**Re-verify**:

```bash
uv run pytest \
  tests/test_reverse_spec_template.py::test_repository_root_comparison_resolves_symlinks_first -q
```

---

## G-4 — REQ-014's identifier convention has no contract assertion

**Disposition**: Resolved

**Resolution**: `test_workspace_identifier_convention_is_guarded` directly
asserts the timestamp-plus-random convention, the separate-generator prohibition,
and the sequential-numbering prohibition.

The template requires reusing the `{YYYY-MMDD-HHMM}{rr}` convention and forbids
both a separate identifier generator and sequential numbering. Deleting that clause
**leaves all 54 tests green** — measured, not assumed.

The other half of the same confirmed constraint is guarded: CON-007's
no-git-branch rule fails `test_workspace_creation_never_touches_git` when removed.
So one confirmed constraint currently has a net under one half and not the other.

**Substitute evidence**: `tasks.md` T1.1's deterministic documentation check, which
review rounds performed by reading the template against `design.md` C1–C10. Risk is
bounded, which is why it does not block PASS.

**Cost to close**: one assertion.

**Re-verify**:

```bash
uv run pytest \
  tests/test_reverse_spec_template.py::test_workspace_identifier_convention_is_guarded -q
```

---

## G-5 — Partial confirmation is unmodeled — **this one needs a product decision**

**Disposition**: Resolved

**Resolution**: the user selected the conservative policy: reconcile requires a
confirmed `spec.md` and every present `design.md` to be confirmed. A present open,
missing-status, or unreadable design keeps the workspace unconfirmed; only a
genuinely absent design uses the existing spec-only fallback. The decision is
recorded as DEC-015 and protected by a dedicated contract test.

Mode resolution step 10 reads "One exact match whose artifacts are confirmed" —
plural, and silent on which file adjudicates when they disagree. The unmodeled
state is `spec.md` **confirmed** while `design.md` is present but still **open**.

**This is not the case REQ-007 already handles.** REQ-007 covers a design that is
*absent* (legitimately scaled away, or predating the design stage) and reconciles
against the spec alone. Here the design *exists and is unconfirmed* — a different
state.

`design.md` A-2 assumes it away: "A slice's artifacts are the ones a user confirms
as a whole; the design does not model partially-confirmed artifacts." So it is a
declared exclusion, not an oversight.

**The decision, if it is ever taken**: when `spec.md` is confirmed and `design.md`
is open, should the command

- **(a)** reconcile against the confirmed spec alone, treating the open design as
  though absent (consistent with REQ-007's existing degradation); or
- **(b)** treat the workspace as not confirmed as a whole and resume the draft
  (consistent with DEC-012's file-level status and A-2's all-or-nothing reading)?

Both are defensible against confirmed intent, which is exactly why it was not
decided during implementation. **(b)** is the more conservative reading and matches
the current template's literal behavior via step 10's "Only a file-level
`Status: confirmed` counts."

**Re-verify**:

```bash
uv run pytest \
  tests/test_reverse_spec_template.py::test_every_present_baseline_artifact_must_be_confirmed -q
```

---

## G-6 — The test module asserts against sibling templates

**Disposition**: Intentional

`tests/test_reverse_spec_template.py` reads `onboard.md` and `distill.md`:

- `test_onboard_still_carries_the_delegated_scan_section` — `reverse-spec`
  delegates its scan discipline to `/codexspec:onboard` and declares three overrides
  on that text. If onboard's `## Codebase Scan` section is renamed or its
  overridden directives removed, the delegation dangles and those overrides describe
  text that no longer exists.
- `test_verbatim_evidence_is_exempt_from_translation` — the verbatim-evidence
  carve-out follows a convention established by those two templates; the assertion
  checks the precedent still exists.

Precedent for this shape: `tests/test_distill_template.py` guards `onboard.md` the
same way.

**Accepted cost**: editing a sibling template can fail *this* feature's test
module, which reads as confusing. That is the alarm working as intended — the
cross-command reference is live, not decorative.

**Re-verify** (naming the two tests, since one reads its sibling templates through
a loop variable rather than a literal):

```bash
grep -n 'def test_onboard_still_carries\|def test_verbatim_evidence' \
  tests/test_reverse_spec_template.py
```

---

## Closed follow-up

G-3, G-4, and G-5 were closed together on 2026-08-24. G-5 used the product
decision recorded in DEC-015; G-3 and G-4 required no new product intent.

Note that the PASS envelope is pinned to `888fece`. Any template or test edit means
that envelope no longer describes HEAD, so closing a gap needs a fresh isolated
`review-code` round to re-establish it. That is the cost to weigh against the size
of the fix — not the edit itself.
