# Confirmed Requirements: implement-tasks-code-review

<!--
Language: Maintain this document in the language specified in .codexspec/config.yml.
This file is the authoritative, persistent record of user-confirmed intent.
Do not copy the full conversation. Keep only confirmed decisions and short evidence
quotes needed to resolve later interpretation disputes.
-->

**Feature ID**: `2026-0623-1658cw`
**Status**: Confirmed (core) — OPEN-001 is non-blocking
**Last Confirmed**: 2026-06-23

## Authority Rules

- Only entries with `Status: confirmed` are binding downstream inputs.
- `open` entries MUST NOT be converted into confirmed product requirements.
- Replaced entries remain in this file with `Status: superseded` and a link to the replacement.
- AI inferences must be labeled as assumptions and require user confirmation before becoming binding.

## Needs

### NEED-001: Chain implement-tasks to review-code for final code quality

- **Status**: confirmed
- **Statement**: After `/codexspec:implement-tasks` finishes implementing all tasks, it must automatically invoke `/codexspec:review-code` on the implemented code and run an auto-fix loop, mirroring how `generate-spec`, `spec-to-plan`, and `plan-to-tasks` chain to their `review-*` commands. The goal is to guarantee the quality of the final code implementation.
- **Rationale**: The three generation commands already self-review their output; the implementation step is the last quality gate and currently has no equivalent, so defects in the generated code reach the user unchecked.
- **User Evidence**: "将 /codexspec:implement-tasks 命令也衔接上 /codexspec:review-code 进行代码的auto review和auto fix，来确保最终代码实现的质量"
- **Confirmed At**: 2026-06-23

## Constraints

### CON-001: Review runs once, at the end of the run

- **Status**: confirmed
- **Statement**: `review-code` runs exactly once, after ALL tasks have been implemented — not per task. This matches the existing review-after-generation pattern and bounds review cost.
- **User Evidence**: Selected "全部完成后运行一次".

### CON-002: Scope is this implementation's diff, including test code

- **Status**: confirmed
- **Statement**: `review-code` reviews only the source files changed by this implementation (the diff versus the feature-branch base), including test code. Pre-existing or otherwise unchanged code is not reviewed.
- **User Evidence**: Selected "本次实现的改动".

### CON-003: Non-code changes are skipped

- **Status**: confirmed
- **Statement**: Only analyzable source files (e.g. `.py`, `.ts`, `.go`, `.rs`, …) are passed to `review-code`. Pure documentation, configuration, and asset changes are skipped. If the diff contains no analyzable code, the loop reports "no code to review" and skips gracefully.
- **User Evidence**: Selected "仅审代码，跳过非代码".

### CON-004: Auto-fix severity gate

- **Status**: confirmed
- **Statement**: Auto-fix covers **CRITICAL + HIGH + MEDIUM** only. **LOW** suggestions (capped at 5 points in `review-code`'s rubric) are report-only and are never auto-fixed.
- **User Evidence**: Selected "CRITICAL+HIGH+MEDIUM".

## Decisions

### DEC-001: MEDIUM findings must be grounded in constitution and requirements

- **Status**: confirmed
- **Decision**: To avoid subjectivity, a MEDIUM finding is auto-fixed ONLY when it is grounded in `.codexspec/memory/constitution.md` and the confirmed requirements/spec, AND it focuses on **maintainability, readability, or testability**. Ungrounded or purely stylistic MEDIUM items are reported, not auto-fixed.
- **Alternatives Rejected**: (a) Auto-fixing all MEDIUM indiscriminately — too subjective and noisy. (b) Auto-fixing only CRITICAL+HIGH — too conservative; discards valuable maintainability refactors.
- **Reason**: The user explicitly required constitution/requirements grounding for MEDIUM and a focus on the three meta-qualities.
- **User Evidence**: "为了避免MEDIUM偏主观，需要结合 constitution、requirements 进行判断，同时侧重系统代码实现的可维护性、可读性、可测试性"

### DEC-002: Auto-fix is test-safe by construction (TDD-aligned)

- **Status**: confirmed
- **Decision**: Auto-fix must be test-safe, following two tracks:
  - **Functional defects** (logic / correctness / security): fix via TDD — add a failing test that reproduces the defect (red) → apply the fix (green) → refactor (still green).
  - **Non-functional fixes** (refactors for maintainability / readability / testability): must preserve behavior; tests run before AND after. If a change breaks tests, it is by definition an incorrect change → revert → confirm tests are green again → re-attempt. A fix is never shipped with failing tests and is never silently skipped.
  A fix that cannot be made green after retry is treated as **unresolved** → stop and report.
- **Alternatives Rejected**: "skip the breaking fix and continue", "revert the whole round and stop", "first-red-stops" — all treat a broken fix as something to abandon, rather than as a signal that the fix itself was wrong and must be redone correctly.
- **Reason**: The user challenged the premise that auto-fix should break tests at all; a correct fix is inherently test-safe, and a test breakage means the change itself is wrong.
- **User Evidence**: "正确的fix应该是按照tdd的方式…测试的破坏意味着代码改动错误，需要恢复代码改动后并确认测试重新全绿后再次重新进行重构"

### DEC-003: Loop bounds and stop conditions mirror existing review loops

- **Status**: confirmed
- **Decision**: Mirror the existing review loops — run a maximum of **two** automatic fix-and-review rounds; stop if a defect repeats, remains unresolved, or requires a user/architecture decision; never auto-fix advisories or design opportunities; never introduce a new product decision during auto-fix. The TDD retry of a single fix (DEC-002) happens within a round; the two-round limit bounds overall effort.
- **Reason**: Consistency with `generate-spec` / `spec-to-plan` / `plan-to-tasks` review loops.
- **User Evidence**: Confirmed in the stage summary (no objection).

### DEC-004: The end-of-run review loop is additive, not a replacement

- **Status**: confirmed
- **Decision**: The end-of-run `review-code` loop is added on top of `implement-tasks`' existing per-task "Review & Refactor" step (TDD workflow step 4). It does NOT replace that step.
- **Reason**: The per-task step is lightweight and immediate; the new loop is the rigorous final gate. Both coexist.
- **User Evidence**: Confirmed as AI assumption A1 in the stage summary.

### DEC-005: Auto-fix changes are committed before reporting completion

- **Status**: confirmed
- **Decision**: Changes produced by the auto-fix loop are committed before the command reports completion — either as part of the final commit or as a dedicated review-fixes commit — consistent with `implement-tasks`' existing incremental-commit behavior.
- **User Evidence**: Confirmed as AI assumption A2 in the stage summary.

### DEC-006: Residual CRITICAL/HIGH defects yield a "needs work" status, never false success

- **Status**: confirmed
- **Decision**: If CRITICAL or HIGH defects remain after the maximum number of rounds, the command reports "needs work" (per `review-code`'s status vocabulary) and does NOT claim success.
- **User Evidence**: Confirmed as AI assumption A3 in the stage summary.

## Out of Scope

### OUT-001: Per-task incremental review-code

- **Status**: confirmed
- **Statement**: `review-code` is NOT invoked per task; it runs once at end of run.
- **Reason**: User selected "全部完成后运行一次" (CON-001).
- **User Evidence**: Stage-summary confirmation.

### OUT-002: Reviewing pre-existing or unchanged code

- **Status**: confirmed
- **Statement**: `review-code` does not review code that predates or is untouched by this implementation.
- **Reason**: Only this implementation's diff is in scope (CON-002).
- **User Evidence**: Stage-summary confirmation.

### OUT-003: review-code on pure documentation / configuration / assets

- **Status**: confirmed
- **Statement**: Pure documentation, configuration, and asset changes are not reviewed by `review-code`.
- **Reason**: `review-code`'s value is code static analysis; non-code is skipped (CON-003).
- **User Evidence**: Stage-summary confirmation.

### OUT-004: Auto-fixing LOW suggestions

- **Status**: confirmed
- **Statement**: LOW (suggestion) findings are report-only and are never auto-fixed.
- **Reason**: Severity gate CON-004.
- **User Evidence**: Stage-summary confirmation.

## Open Questions

### OPEN-001: Tool-permission mechanics of the nested review-code invocation

- **Status**: open
- **Why It Matters**: `review-code`'s frontmatter restricts `allowed-tools` to `Read, Grep, Glob` plus a specific set of linters/type-checkers. When `implement-tasks` invokes `/codexspec:review-code` mid-run, whether the nested command inherits `implement-tasks`' broader tool access (so it can run the project's lint / type-check / test tooling during review) or is scoped to `review-code`'s restricted list affects the feasibility of running real static analysis inside the loop. This is an implementation detail to resolve at plan/implementation time and does not change the requirement's intent.
- **Owner**: Implementation / Plan

## Superseded Entries

<!-- No entries have been superseded yet. Keep replaced entries here with Status: superseded and a Replaced By link as they arise. -->

## Confirmation Log

### Session 2026-06-23

- **Summary Presented**: Stage summary covering NEED-001; constraints CON-001 (timing: once at end) / CON-002 (scope: this implementation's diff, incl. tests) / CON-003 (skip non-code) / CON-004 (severity gate CRITICAL+HIGH+MEDIUM); decisions DEC-001 (MEDIUM grounded in constitution+requirements, focus on maintainability/readability/testability) / DEC-002 (test-safe TDD-aligned auto-fix) / DEC-003 (max 2 rounds, existing stop conditions); out-of-scope OUT-001..004; open question OPEN-001 (nested-command tool permissions, non-blocking); AI assumptions A1 (additive) / A2 (commit fixes) / A3 (needs-work on residual defects).
- **User Confirmation**: "确认，写入 requirements.md" (explicit confirmation of the full stage summary).
- **Entries Confirmed**: NEED-001, CON-001, CON-002, CON-003, CON-004, DEC-001, DEC-002, DEC-003, DEC-004, DEC-005, DEC-006, OUT-001, OUT-002, OUT-003, OUT-004.
- **Entries Left Open**: OPEN-001 (non-blocking — implementation mechanic).
