# Open Issues: reverse-spec

**Feature**: `2026-0818-2053p5-reverse-spec`
**Branch**: `2026-0818-2053p5-reverse-spec` · **Commit**: `bf0129b` (only commit ahead of `origin/main` = `ea61c31`)
**Working tree**: clean · **Baseline**: 1231 passed / 50 skipped · `ruff check src/ tests/` clean
**implement-tasks §7.6 terminal status**: **NOT SUCCESS** — the last complete-feature review returned `FAIL`; its findings are unrepaired.

---

## Where things stand

All seven tasks in `tasks.md` are implemented and committed. Four rounds of
isolated `review-code` have run. Rounds 1–3 produced 16 verified defects, all
repaired. Round 4 produced 6 more, listed below, **none of which is repaired**.

| Round | Verdict | Findings | Status |
|---|---|---|---|
| 1 | FAIL | P2×1, P3×1 | repaired (one required a user decision → CON-007) |
| 2 | FAIL | P2×3, P3×8 | repaired |
| 3 | FAIL | P2×1, P3×2 | repaired |
| 4 | FAIL | P2×1, P3×5 | **open — this document** |

Governance passed in every round: self-bootstrap (derived artifacts verified as
faithful regenerations, never hand-edited), the two-constitutions separation, the
packaging boundary, and every command-count / enumeration site.

## The convergence signal — read this before fixing anything

**The worst finding in each of rounds 3 and 4 was introduced by the previous
round's repair, both times in the same area: mode resolution and write
boundaries.**

- Round 2's repair made generation write incrementally (to satisfy REQ-016 /
  NFR-004 resumability). → Round 3 found that an interrupted run now leaves a
  `Status: open` workspace which step 8 refused outright, making resumability
  unreachable.
- Round 3's repair added "resume generate into the existing workspace". → Round 4
  found that this silently overwrites a draft the maintainer has already
  hand-corrected, and creates a second exception to a boundary clause that
  declares its exception set closed.

Under §7.5 the progress guards have **not** tripped — each round's defects were
new, none survived two fixes, and no refuted finding recurred, so the loop is
formally allowed to continue. But the pattern says the remaining problem is not
"one more patch away". **I-1, I-2 and I-3 below are three faces of one unsettled
design question — how a partially-written or partially-corrected workspace is
recognized and resumed. Settle that question once, then apply all three.** Fixing
them independently is what produced this pattern twice.

---

## Open findings

### I-1 [P2] `resume generate` can silently overwrite a hand-corrected draft

- **Location**: `templates/commands/reverse-spec.md` — Mode Resolution step 8
  (resume clause) vs. the `## Boundaries` clause beginning "Never edits an
  artifact it did not produce".
- **Defect (two parts)**:
  1. The Boundaries clause states that regenerating its own `reconcile.md` is
     **the one exception**. Step 8's resume is a second exception, so the two
     instructions cannot both be followed: an agent honoring Boundaries refuses to
     write and strands the workspace; an agent honoring step 8 breaches a boundary
     the template just declared exhaustive.
  2. Unlike the `reconcile.md` path — which requires "Say so before overwriting" —
     resume has **no pre-overwrite notice and no consent**.
- **User harm**: `spec.md` User Story 1 confirms the flow "the maintainer reviews
  the draft, **corrects what the code got wrong**, and confirms it". A maintainer
  who has corrected the draft but not yet flipped `Status` to `confirmed` and then
  re-runs the command lands in step 8; the agent re-derives from code and
  overwrites those corrections without asking. This contradicts confirmed CON-004
  / REQ-017 ("MUST NOT automatically modify code or any pre-existing artifact").
- **Suggested direction** (not applied — see the convergence note): do not add a
  third exception. Reopen the Boundaries clause from a closed set to a stated rule
  ("it rewrites only artifacts it produced in this workspace, and never without
  notice"), and give resume the same pre-overwrite notice the `reconcile.md` path
  already has. Decide alongside I-2 and I-3.

### I-2 [P3] The overview positive marker fails for an interrupted overview run

- **Location**: `templates/commands/reverse-spec.md` — Mode Resolution step 4
  (`slices.md` as the positive marker) vs. `## Overview Mode` (writes
  incrementally).
- **Defect**: an overview run interrupted after `design.md` but before
  `slices.md` has no marker. A later `reverse-spec .` therefore treats that
  overview workspace as a slice workspace: if open → step 8 resumes generate and
  writes a `spec.md` into it, violating REQ-015 / OUT-005 ("the bare run produces
  no `spec.md`"); if confirmed → step 7 reconciles against a design-only baseline,
  the exact state `design.md` Decision 3 calls undefined.
- **Note**: the interruption hole closed for slice workspaces was left open on the
  overview side. Same root question as I-1 and I-3.

### I-3 [P3] "Never create a second workspace for a slice" is unreachable in one window

- **Location**: `templates/commands/reverse-spec.md` — step 8's prohibition vs.
  `## Slice and Workspace` ("the `Slice:` header is the whole baseline-lookup
  mechanism; there is no index file") vs. `## Generate Mode` ("create the
  workspace as soon as the slice is confirmed to have analyzable code").
- **Defect**: between directory creation and writing the `Slice:` header, the
  workspace is invisible to the step-4 lookup. An interruption inside that window
  makes the next run create a second workspace and orphan the first — directly
  against the confirmed boundary row in `spec.md` ("Continue the existing
  workspace rather than creating a second one for the same slice").
- **Suggested direction**: write the `Slice:` header as the first act of creating
  the workspace, so the lookup key exists before any interruption is possible.

### I-4 [P3] `design.md` sequence diagram contradicts its own C2

- **Location**: `.codexspec/specs/2026-0818-2053p5-reverse-spec/design.md` —
  `## Sequence & Data Flow`, the `one, still open` branch still reads
  `REFUSE / write nothing`; C10 likewise still says "never edits a pre-existing
  artifact" with no mention of resume or report regeneration.
- **Defect**: C2 item 8 in the same document says resume, and the template
  implements resume. `design.md` is the direct upstream authority for plan and
  tasks, so someone implementing or reviewing from it reaches the behavior this
  work deliberately removed.
- **Fix**: mechanical propagation — update the diagram branch and C10 to match C2.

### I-5 [P3] `tasks.md` T1.1 would reinstate a forbidden write

- **Location**: `.codexspec/specs/2026-0818-2053p5-reverse-spec/tasks.md` — the
  T1.1 content table row for `## Scan Discipline` still reads "restating only the
  `[path]` difference".
- **Defect**: the template now carries **two** overrides on the delegated
  `onboard` scan text; the first is "this command writes nothing to
  `.codexspec/profile/`". `onboard.md` instructs "Stream findings to the store as
  you go — write each convention as soon as it is confirmed", so implementing
  T1.1 literally re-imports that write and violates OUT-002 / CON-004.
- **Fix**: mechanical — the row must name both overrides. (`plan.md` is already
  neutral and needs no change.)

### I-6 [P3] `test_three_drift_kinds_are_named` is a hollow assertion

- **Location**: `tests/test_reverse_spec_template.py`.
- **Defect**: it asserts only that the three kind literals appear somewhere in the
  file. They also appear in the `## Reconcile Report` code block and in Mode
  Resolution step 5, independently of the classification instruction.
- **Proof**: in a disposable mirror, deleting the entire REQ-009 classification
  instruction from the template left all 30 tests green.
- **Fix**: assert the classification sentence itself, e.g. the span beginning
  "Re-read the slice's current code and classify each finding as exactly one of".
  The file already documents this discipline in two other comments; this
  assertion is the one that violates it.

---

## Declared coverage gaps (not defects — decide whether to close any)

Measured by section-deletion sweeps in a disposable mirror:

- **`## Overview Mode` has zero contract coverage.** Deleting the whole section
  leaves all 30 tests green. REQ-015 / OUT-005 and User Story 4's three acceptance
  scenarios have no automated evidence. This is the largest gap and the cheapest
  to close.
- **REQ-003, REQ-004, REQ-006, REQ-014 have no contract test.** `tasks.md` maps
  them to T1.1's manual deterministic check only — a declared trade-off, not an
  omission. The sharpest instance is REQ-004: the `Slice:` header is the entire
  baseline-lookup mechanism and nothing fails if it disappears. I-3 makes this
  more pressing.
- **`## User Input` / `$ARGUMENTS` has no coverage**; deleting it leaves 30 tests
  green even though the command could not receive `[path]` without it.
- **Some assertions span markdown emphasis or backticks**, against plan Decision 3
  / T2.1's own rule (pitfall `P-2026-0813-1606fz-1`). Currently green; brittle.
- **The cross-command reference to `/codexspec:onboard` has no test.** Nothing
  asserts that `onboard.md` still has a `## Codebase Scan` section or that its
  overridden directives are still where the override expects them. The repository
  has precedent for such a guard in `tests/test_distill_template.py`.
- **Prose deliverable, no runtime assertions** — accepted in `design.md`
  Decision 1.
- **`allowed-tools` is far wider than the Boundaries** (`Bash(git:*)`, `Edit`,
  `Write`), and the Codex render strips `allowed-tools` entirely. Recorded and
  accepted as residual risk in `design.md` C10; not a defect introduced here.
- **Partial confirmation is unmodeled** (`spec.md` confirmed, `design.md` open) —
  explicitly assumed away in `design.md` A-2.
- **`docs/*/user-guide/commands.md` omits `reverse-spec`** — it also omits
  `onboard`, `debug`, `distill`, `evolve`, `release-notes`; pre-existing drift, not
  attributable to this change.

---

## Definition of done

`implement-tasks` §7.6 requires a final valid `PASS` envelope from a **fresh
isolated** complete-feature review, with complete requirements coverage, complete
verification, zero P0–P3 findings, no blocking coverage gap, no uncovered
enumerated test scenario from `tasks.md`, and a still-green baseline.

Concretely, before that review can be run:

1. Settle the resume/recognition question once, then apply I-1, I-2, I-3 together.
2. Apply I-4, I-5, I-6 (mechanical).
3. Optionally close the `## Overview Mode` coverage gap and add a `Slice:` header
   assertion.
4. Re-run: `uv run ruff check src/ tests/`; `uv run pytest -q` (must stay ≥ 1231
   passed / 50 skipped, no regression).
5. Regenerate derived artifacts with `uv run codexspec init . --force --ai both`
   — the `--ai both` flag is mandatory or `project.ai` is rewritten — and confirm
   `git status` shows no `.codexspec/config.yml` change.
6. Commit (Conventional Commits, English, **no AI attribution of any kind**), then
   run a fresh isolated review round.

## Environment notes for whoever picks this up

- `pre-commit` will hang for minutes building the `shellcheck_py` environment
  (its build downloads a binary and there is no network in the sandbox), and
  `pip-audit` needs network too. This change adds no shell code, so
  `SKIP=shellcheck,pip-audit git commit …` is safe; check the hook output shows
  the rest ran.
- `ruff-format` may reformat a staged Python file and abort the commit. Re-stage
  only the file the hook modified and retry — that is the single permitted
  `git add` during a commit.
- Reviews must run in a genuinely isolated context. An inline self-review shares
  context and cannot produce a clean PASS (profile pitfall
  `P-2026-0811-1418yq-1`).
