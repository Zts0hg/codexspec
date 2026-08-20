# Review Record: reverse-spec

**Feature**: `2026-0818-2053p5-reverse-spec`

This file is the defect history and the lessons drawn from it. It records what was
found and repaired, **not** outstanding work: nothing below is a pending action
except the single product question in the last section, which is flagged for the
maintainer and is not a defect.

It deliberately does **not** track the feature's gate status. A status document
living inside the diff cannot describe the review of the diff that contains it —
that self-reference is exactly what produced the round-5 finding below. The
authoritative terminal verdict is the `implement-tasks` §7.6 gate result, which
lives in the session and the branch history, not here.

---

## Review history

Rounds of **isolated** `review-code` ran against the complete-feature target. Each
round's admitted findings were repaired before the next round started, and each
round ran in a genuinely fresh context that inherited no prior conclusions.

| Round | Verdict | Findings | Outcome |
|---|---|---|---|
| 1 | FAIL | P2×1, P3×1 | repaired (one required a user decision → CON-007) |
| 2 | FAIL | P2×3, P3×8 | repaired |
| 3 | FAIL | P2×1, P3×2 | repaired |
| 4 | FAIL | P2×1, P3×5 | repaired (see "The convergence signal" below) |
| 5 | FAIL | P3×1 | repaired — a stale copy of this file, falsified by the commit that had just fixed round 4 |

Governance passed in every round: self-bootstrap (both derived artifacts verified
as faithful regenerations, never hand-edited), the two-constitutions separation,
the packaging boundary, and every command-count / enumeration lockstep site.

## The convergence signal — why rounds 3–5 are worth remembering

**The worst finding in each of rounds 3 and 4 was introduced by the previous
round's repair, both times in the same area: mode resolution and write
boundaries.**

- Round 2's repair made generation write incrementally (REQ-016 / NFR-004
  resumability). → Round 3 found that an interrupted run now left a `Status: open`
  workspace which step 8 refused outright, making resumability unreachable.
- Round 3's repair added "resume generate into the existing workspace". → Round 4
  found that this silently overwrote a draft the maintainer had already
  hand-corrected, and created a second exception to a boundary clause that
  declared its exception set closed.

Round 4's three worst findings were then diagnosed as **one defect with three
faces**, and fixed together rather than individually:

> The command inferred a workspace's identity and state from **artifacts that are
> themselves written incrementally during the run**. Any artifact used as a state
> marker is also a work product being streamed, so mid-run the marker set is
> partial and a partial state is indistinguishable from a different state.
> Provenance is likewise unknowable: the command cannot tell its own interrupted
> output from the maintainer's corrections.

The settlement is recorded as **`design.md` Decision 7**, two rules applied
together: *identity is written before content* (creating a workspace is one
indivisible act — directory plus its identifying artifact, before any scanning),
and *resume completes; it never rewrites* (content present when a run begins is
treated as the maintainer's). The Boundaries clause became a stated rule instead
of a closed exception set, which was the shape that produced the contradiction
twice.

**Lesson**: when consecutive review rounds keep finding defects in one area and
each round's fix creates the next round's defect, the remaining problem is not one
more patch away. Stop patching symptoms and find the shared cause first.

## What each round's repairs touched

- **I-1 / I-2 / I-3** (round 4, the one defect above) —
  `templates/commands/reverse-spec.md`: mode resolution steps 4 and 8,
  `## Slice and Workspace`, `## Generate Mode`, `## Overview Mode`,
  `## Boundaries`.
- **I-4** — `design.md`: the sequence diagram's `one, still open` branch and C10
  contradicted C2 and the template; C2/C3/C5/C10 and the coverage table now match,
  and Decision 7 records the rationale.
- **I-5** — `tasks.md`: the T1.1 `## Scan Discipline` row named only the `[path]`
  override, so implementing it literally would have re-imported `onboard`'s
  forbidden profile write. It now names both overrides.
- **I-6** — `tests/test_reverse_spec_template.py`:
  `test_three_drift_kinds_are_named` asserted only that the three kind literals
  appeared somewhere in the file; they also appear in the report block and in mode
  resolution, so the assertion stayed green with the entire REQ-009 classification
  instruction deleted. It now asserts the classification sentence and each kind's
  defining clause.
- **Round 5's P3** — this file.

## Coverage closed in the final rounds

A section-deletion sweep in a disposable mirror now fails for every guarded rule.
Previously-hollow areas that were closed:

- `## Overview Mode` had **zero** contract coverage (REQ-015 / OUT-005 and User
  Story 4's acceptance scenarios). Deleting the whole section left the suite green.
- The `Slice:` header (REQ-004) — the entire baseline-lookup mechanism — had no
  assertion; nothing failed if it disappeared.
- `## User Input` / `$ARGUMENTS` had no coverage, though the command cannot
  receive `[path]` without it.
- The cross-command reference to `/codexspec:onboard` had no guard; the scan
  section could be renamed and the two overrides would silently describe text that
  no longer exists. (Guard shape follows `tests/test_distill_template.py`.)
- Assertions spanning markdown emphasis or backticks (brittle, against plan
  Decision 3 / pitfall `P-2026-0813-1606fz-1`) were removed: every assertion now
  runs against emphasis-stripped prose via the `prose()` helper.

## Declared, accepted coverage gaps

Not defects — recorded trade-offs, carried forward knowingly:

- **REQ-003, REQ-006, REQ-014 have no contract test.** `tasks.md` maps them to
  T1.1's manual deterministic check — a declared trade-off. (REQ-004, previously
  the sharpest instance, is now covered.)
- **Prose deliverable, no runtime assertions** — accepted in `design.md`
  Decision 1; the contract tests are the strongest available guard.
- **`allowed-tools` is wider than the Boundaries** (`Bash(git:*)`, `Edit`,
  `Write`), and the Codex render strips `allowed-tools` entirely from every skill.
  Byte-identical to the shipped `onboard.md` and pre-existing for all 26 commands;
  recorded and accepted as residual risk in `design.md` C10.
- **Partial confirmation is unmodeled** (`spec.md` confirmed, `design.md` open) —
  explicitly assumed away in `design.md` A-2.
- **A path whose final segment is empty** (`.`, `/`, a trailing slash) yields a
  workspace directory named `<id>-`. Writes remain provably confined to
  `.codexspec/specs/`, and baseline lookup uses the in-artifact `Slice:` header
  rather than the directory name, so the effect is cosmetic.
- **Absolute or out-of-repo paths**: the `Slice:` header is specified as a
  repo-relative path with no stated rule when no relative form exists. Affects
  diagnosability of lookup only; writes do not escape.
- **`plan.md:5`** still reads `design.md (C1–C11, Decisions 1–6)`; Decision 7 was
  added afterwards. Verified to introduce no substantive conflict with `plan.md`'s
  body — a stale count in a header line, below the finding threshold.
- **`docs/*/user-guide/commands.md` omits `reverse-spec`** — it also omits
  `onboard`, `debug`, `distill`, `evolve`, and `release-notes`. Pre-existing drift,
  not attributable to this change and not among REQ-020's lockstep sites.

## Open product question for the maintainer

**Not a defect, and it does not block the gate** — the round-5 reviewer and its
independent specialist both raised it and both declined to admit it, because
confirmed intent genuinely supports two readings. It needs a product decision, not
an implementation choice.

**`reverse-spec .` — an explicit path that happens to be the repository root —
enters generate mode and would draft one whole-repository detailed `spec.md`.**
Step 1 short-circuits only the *bare* run, and step 4 skips the overview
workspace, so an explicit root path finds zero matches and falls through to
generate.

- Reading A (current behavior is correct): DEC-011, OUT-005, and REQ-015 all
  anchor the monolithic-spec prohibition specifically to the **bare run / no
  `[path]`** case, and REQ-014 defines a slice as "a directory, module, or package
  path" — the repository root is one.
- Reading B (current behavior is a gap): NFR-005's second sentence is
  unconditional — "No output aggregates the whole repository into a single
  detailed specification."

If Reading B is intended, the fix is small — treat a slice that resolves to the
repository root as the bare run, or refuse it and point at the bare run — but it
changes confirmed scope and so was not applied.

## Environment notes

- `pre-commit` hangs for minutes building the `shellcheck_py` environment (its
  build downloads a binary and there is no network in the sandbox), and
  `pip-audit` needs network too. This change adds no shell code, so
  `SKIP=shellcheck,pip-audit git commit …` is safe; check the hook output shows
  the rest ran.
- `ruff-format` may reformat a staged Python file and abort the commit. Re-stage
  only the file the hook modified and retry — that is the single permitted
  `git add` during a commit.
- Regenerate derived artifacts with `uv run codexspec init . --force --ai both`.
  The `--ai both` flag is mandatory, or `project.ai` is rewritten to `claude`.
- Reviews must run in a genuinely isolated context. An inline self-review shares
  context and cannot produce a clean PASS (profile pitfall
  `P-2026-0811-1418yq-1`).
