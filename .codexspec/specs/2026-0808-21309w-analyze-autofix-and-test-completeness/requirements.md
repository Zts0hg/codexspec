# Confirmed Requirements: analyze-autofix-and-test-completeness

<!--
Language: Maintain this document in the language specified in .codexspec/config.yml.
This file is the authoritative, persistent record of user-confirmed intent.
Do not copy the full conversation. Keep only confirmed decisions and short evidence
quotes needed to resolve later interpretation disputes.
-->

**Feature ID**: `2026-0808-21309w`
**Status**: Confirmed
**Last Confirmed**: 2026-08-08

## Overview

Two related enhancements to the CodexSpec SDD pipeline, driven by two observed
gaps:

1. **`analyze` reports but never repairs.** Today `analyze` is read-only: it
   detects cross-artifact inconsistencies and describes a remediation, but leaves
   every fix to the user, which makes it low-value.
2. **Test detail is lost between `tasks.md` and the delivered code.** After
   `implement-tasks`, the implemented tests miss scenarios (especially edge and
   error cases) that `tasks.md` implied, and nothing in the pipeline catches it.

Both are addressed by enhancing three existing distributed command templates
only — `templates/commands/analyze.md`, `plan-to-tasks.md`, and
`implement-tasks.md`. No new command is introduced, and `review-code.md` is not
modified.

## Authority Rules

- Only entries with `Status: confirmed` are binding downstream inputs.
- `open` entries MUST NOT be converted into confirmed product requirements.
- Replaced entries remain in this file with `Status: superseded` and a link to the replacement.
- AI inferences must be labeled as assumptions and require user confirmation before becoming binding.

## Needs

### NEED-001: `analyze` must resolve inconsistencies, not merely report them

- **Status**: confirmed
- **Statement**: When `analyze` detects an inconsistency, it must repair the
  affected downstream artifact(s) to restore consistency, rather than only
  emitting a remediation description for the user to apply by hand.
- **Rationale**: A pure reporter forces the user to apply every fix manually; the
  whole point of detecting an inconsistency is to eliminate it. This is the
  user's primary complaint about the current `analyze`.
- **User Evidence**: "The current `analyze` reports inconsistencies but has no
  repair action; make it actually useful." / "If there were no `analyze` command
  and you had to design one from scratch, should it be read-only or auto-fix?"
- **Confirmed At**: 2026-08-08

### NEED-002: `plan-to-tasks` must enumerate explicit, verifiable test scenarios

- **Status**: confirmed
- **Statement**: For every **testable** task, `tasks.md` must carry an explicit,
  individually identifiable list of test scenarios covering the happy path plus
  the boundary/error conditions the behavior implies, so the implementation can
  be checked against them one-to-one.
- **Rationale**: `tasks.md` today only asks for "appropriate verification"; it
  does not enumerate concrete scenarios, so `implement-tasks` can silently omit
  edge/error tests and the final gate has nothing precise to check against.
- **User Evidence**: "After `implement-tasks`, comparing `tasks.md` against the
  code I find gaps in the implementation, mainly missing test details." Chosen
  direction: front-load by enriching `plan-to-tasks` so every testable task
  enumerates scenarios, including boundary/error.
- **Confirmed At**: 2026-08-08

### NEED-003: `implement-tasks` must self-verify scenario coverage before reporting success

- **Status**: confirmed
- **Statement**: Before `implement-tasks` reports success, its existing review
  loop must self-verify that every test scenario enumerated in `tasks.md` maps to
  at least one implemented test that genuinely exercises and asserts it (not a
  hollow test). A missing or hollow scenario is blocking.
- **Rationale**: Closes the `tasks.md`-intent → delivered-tests gap at the point
  where code exists, complementing the front-load enumeration (NEED-002).
- **User Evidence**: Chosen direction is "front + back, double insurance"; the
  back-end check is folded into `implement-tasks`' review loop.
- **Confirmed At**: 2026-08-08

## Constraints

### CON-001: `requirements.md` is the single source of truth; `analyze` never modifies it

- **Status**: confirmed
- **Statement**: `spec.md`, `plan.md`, and `tasks.md` are all derived from
  `requirements.md`, which is the user-confirmed authority. `analyze` therefore
  never edits `requirements.md`; all remediation conforms the downstream
  artifacts to `requirements.md`. The fix direction is dictated by the authority
  hierarchy (requirements > spec > plan > tasks) and is always deterministic.
- **User Evidence**: "`requirements` is the user-authoritative confirmed source
  the others are generated from; so there is no case where requirements needs to
  change — cases needing changes to the other documents can be auto-corrected
  based on requirements."

### CON-002: "No upstream authority" is not itself a defect; `analyze` acts only on conflicts

- **Status**: confirmed
- **Statement**: `analyze` separates two dimensions.
  - **Completeness**: every upstream authority (ultimately `requirements`) must
    be covered downstream; missing coverage is auto-added downstream. A
    downstream entry that merely adds derived/elaborated detail beyond upstream
    authority does **not** harm completeness and is preserved untouched.
  - **Consistency**: `analyze` acts **only on conflicts** (a downstream entry
    contradicting `requirements`/upstream truth or another entry). On conflict it
    auto-resolves by conforming the unauthorized/lower-authority side with the
    **minimal change** needed to remove the conflict. No conflict → no action.
    No human escalation path is required.
- **User Evidence**: "An extra downstream entry does not harm completeness, so
  from the completeness view it should not be deleted. From the consistency view,
  check whether it conflicts with other content; if it does, adjudicate by the
  upstream/`requirements` source; if it does not conflict, do nothing."

### CON-003: Scenario enumeration applies to testable tasks only

- **Status**: confirmed
- **Statement**: The test-scenario requirement (NEED-002) applies only to
  testable tasks, mirroring `implement-tasks`' existing code-vs-docs/config split.
  Non-testable tasks (docs, config, assets, infra) keep their deterministic
  verification and are not forced to carry test scenarios.
- **User Evidence**: Consistent with the existing conditional-TDD distinction in
  `implement-tasks`.

### CON-004: Front and back are coupled — scenarios must be individually traceable

- **Status**: confirmed
- **Statement**: The scenarios enumerated by `plan-to-tasks` (NEED-002) must be
  individually identifiable and traceable so the `implement-tasks` self-check
  (NEED-003) can map "scenario → test" one-to-one. The two ends are designed
  together: the more checkable the enumeration, the more precisely the back-end
  can verify it.
- **User Evidence**: "The two ends bite together: the more checkable the
  front-end lists them, the more the back-end can verify each one."

### CON-005: Edit source templates only, never the self-bootstrap install artifact

- **Status**: confirmed
- **Statement**: All changes are made in the source templates under
  `templates/commands/` (`analyze.md`, `plan-to-tasks.md`, `implement-tasks.md`).
  The derived copies under `.claude/commands/codexspec/` are install artifacts
  and must never be hand-edited (self-bootstrap rule).
- **User Evidence**: Project governance (constitution / repository-layout).

## Decisions

### DEC-001: `analyze` fully auto-fixes by default, with no escalation path

- **Status**: confirmed
- **Decision**: `analyze` applies deterministic, authority-directed fixes
  automatically by default — both in manual runs and inside the `auto_next` chain
  run — with no confirmation prompt. Given CON-002, there is no class of finding
  that requires human escalation.
- **Alternatives Rejected**:
  - Keep `analyze` purely read-only (rejected: too low-value, the core complaint).
  - Propose-then-confirm as the default, or an escalation carve-out for
    "no upstream authority" findings (rejected after CON-002 reframed such
    findings as non-defects unless they conflict).
- **Reason**: Because `requirements` is the single source of truth, the fix
  direction is always deterministic, so unattended auto-fix is safe in direction.
- **User Evidence**: "Auto-fix everything, because ... there is no case that
  needs to change requirements, and changes to the other documents can be
  auto-corrected and repaired based on requirements."

### DEC-002: The back-end completeness check lives inside `implement-tasks`' review loop

- **Status**: confirmed
- **Decision**: NEED-003 is implemented as a self-check within `implement-tasks`'
  existing Final Code Review Loop (§7), reusing its repair path (7.4–7.6): a
  scenario gap is treated as a blocking defect and repaired (red-green add the
  missing test, re-verify, re-review) before success can be reported.
- **Alternatives Rejected**:
  - Extend `review-code`'s `--feature` machine gate to add scenario coverage as a
    first-class blocking coverage dimension (rejected: would pull in a 4th
    template and widen scope).
  - Add a new dedicated post-implement command (rejected: no new commands).
  - Extend `analyze` to cover `tasks → code` (rejected: see DEC-003 / OUT-003).
- **Reason**: Keeps scope to exactly three templates and reuses the existing
  blocking gate and repair machinery.
- **User Evidence**: "Fold it into `implement-tasks`' review loop."

### DEC-003: `analyze` stays artifact↔artifact; it is not extended to `tasks → code`

- **Status**: confirmed
- **Decision**: `analyze` continues to verify only cross-artifact consistency and
  completeness among `requirements`/`spec`/`plan`/`tasks`. Code-level
  verification is not added to `analyze`.
- **Alternatives Rejected**: Extending `analyze`'s traceability chain to add the
  `tasks → code` link (rejected).
- **Reason**: Timing — see OUT-003. `analyze` runs before code exists, so it
  structurally cannot verify code.
- **User Evidence**: Chosen back-end home is `implement-tasks`, not `analyze`.

### DEC-004: Front-load rigor — every testable task MUST enumerate scenarios (incl. boundary/error)

- **Status**: confirmed
- **Decision**: `plan-to-tasks` mandates explicit scenario enumeration for every
  testable task, and must include boundary/error cases whenever the behavior
  implies them, each scenario individually traceable. Enforced by
  `plan-to-tasks`' Pre-Save Validation and the `review-tasks` loop. Anti-padding
  guard: enumerate only the scenarios the behavior actually implies — do not add
  filler to hit a count.
- **Alternatives Rejected**: Judgment-based enumeration "only where risk/behavior
  warrants" (rejected: risks reproducing the original "missing test detail" gap).
- **Reason**: Directly targets the observed gap of missing edge/error tests.
- **User Evidence**: "Every testable task must enumerate scenarios, including
  boundary/error."

### DEC-005: Test scenarios derive from spec/requirement behavior; `plan-to-tasks` expands, never invents

- **Status**: confirmed
- **Decision**: Scenarios originate from `spec.md` acceptance criteria and the
  covered requirement's behavior. `plan-to-tasks` expands them into concrete,
  per-task cases; it does not author new intent. When upstream behavior is too
  underspecified to enumerate meaningful scenarios, `plan-to-tasks` triggers its
  existing stop condition ("stop instead of guessing") rather than inventing.
- **Alternatives Rejected**: Inventing scenarios at the tasks stage without an
  upstream source (rejected: violates the "never invent intent" principle).
- **Reason**: Preserves the single-source-of-truth model (CON-001) end to end.
- **User Evidence**: Resolves OPEN-001 (where scenarios originate).

## Out of Scope

### OUT-001: `analyze` never modifies `requirements.md`

- **Status**: confirmed
- **Statement**: `requirements.md` is out of scope for `analyze`'s auto-fix.
- **Reason**: It is the user-confirmed source of truth (CON-001); only the user
  changes it, via `/codexspec:specify` or `/codexspec:clarify`.

### OUT-002: No new standalone commands

- **Status**: confirmed
- **Statement**: Neither enhancement introduces a new command; both are
  enhancements to existing commands.
- **Reason**: Avoid command sprawl; the needed behavior fits existing commands.

### OUT-003: `analyze` does not perform code-level (`tasks → code`) checks

- **Status**: confirmed
- **Statement**: `analyze` does not verify implemented code/tests against
  `tasks.md`.
- **Reason**: In the `auto_next` chain, `analyze` runs **after `plan-to-tasks`
  and before `implement-tasks`** — no code exists yet at that point, so a
  `tasks → code` check is structurally impossible there. Code-level verification
  therefore belongs to `implement-tasks` (which runs after code exists), which is
  exactly why NEED-003 / DEC-002 place the back-end check inside
  `implement-tasks`. This is a consequence of pipeline timing, not a preference.
- **User Evidence**: "This needs to be stated clearly: because `analyze` runs
  before `implement-tasks`, it is not the place to do a tasks→code check."

### OUT-004: `review-code.md` is not modified

- **Status**: confirmed
- **Statement**: The back-end check is not implemented by extending `review-code`.
- **Reason**: Keeps the change scoped to three templates (see DEC-002).

## Open Questions

### OPEN-001: Where do test scenarios originate (spec vs. plan-to-tasks)?

- **Status**: resolved
- **Resolved By**: DEC-005 — scenarios derive from `spec.md` acceptance criteria
  / covered requirement behavior; `plan-to-tasks` expands, never invents.
- **Why It Matters**: Determines whether `plan-to-tasks` may author scenarios or
  must trace them upstream. Non-blocking for spec generation.
- **Owner**: User

## Confirmation Log

### Session 2026-08-08

- **Summary Presented**: Two-feature scope on three templates —
  (1) `analyze` gains full auto-remediation bounded by the requirements-as-truth
  model (NEED-001, CON-001, CON-002, DEC-001), staying artifact-only for timing
  reasons (DEC-003, OUT-003); (2) test-scenario completeness front-loaded into
  `plan-to-tasks` (NEED-002, CON-003, DEC-004, DEC-005) and self-verified in
  `implement-tasks`' review loop (NEED-003, CON-004, DEC-002), touching no new
  command and not `review-code` (OUT-002, OUT-004).
- **User Confirmation**: "确认" (confirmed), after iteratively refining CON-002
  (conflict-only remediation), DEC-002 (back-end inside `implement-tasks`),
  DEC-004 (mandatory enumeration incl. boundary/error), and the timing rationale
  for OUT-003.
- **Entries Confirmed**: NEED-001, NEED-002, NEED-003, CON-001, CON-002, CON-003,
  CON-004, CON-005, DEC-001, DEC-002, DEC-003, DEC-004, DEC-005, OUT-001, OUT-002,
  OUT-003, OUT-004; OPEN-001 resolved by DEC-005.
