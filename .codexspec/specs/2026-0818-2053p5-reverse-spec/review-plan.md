# Plan Review Report

## Summary

- **Overall Status**: PASS
- **Compatibility Score**: 100/100
- **Authority Mode**: Requirements-first
- **Readiness**: Ready for Tasks

## Review Rounds

| Round | Status | Score | Outcome |
|---|---|---|---|
| 1 | PASS_WITH_WARNINGS | 94/100 | Two Minor defects, both with deterministic remediation from upstream evidence. Fixed automatically. |
| 2 | PASS | 100/100 | Both resolved; no residual defects. |

### Round 1 defect 1 — half of design Decision 5 left unlocked by tests (Minor, resolved)

- **Evidence**: `design.md` Decision 5 has two halves: a `semantic-mismatch` item
  must quote both sides as evidence, and a disagreement whose resolution is not
  derivable must still be reported with direction `needs-your-judgment`
  (REQ-013). Both exist to prevent fabricated output.
- **Location**: `plan.md` → Phase 2 test enumeration and its `Covers:` line.
- **Mismatch**: Phase 2 enumerated an assertion for the both-side-evidence half
  but none for the direction-reasoning half, and omitted REQ-013 from its
  `Covers:`. REQ-013 was therefore planned into the template (Phase 1) with no
  contract test locking it, while its sibling clause from the same decision was
  locked.
- **Impact**: the `needs-your-judgment` safeguard could be dropped or weakened
  during authoring or a later edit with no test failing — precisely the
  anti-fabrication guarantee the design leans on for the feature's core value.
- **Remediation applied**: added the direction-reasoning assertion (including the
  `needs-your-judgment` fallback) to Phase 2's enumeration, added REQ-013 to its
  `Covers:`, noted that Decision 5's two halves are both asserted, and updated the
  coverage row to `Phase 1, Phase 2`.

### Round 1 defect 2 — NFR-003 coverage pointed at a phase that does not state it (Minor, resolved)

- **Evidence**: `spec.md` NFR-003 (neither constitution is modified);
  `plan.md` Non-Goals states "No edit to either constitution (NFR-003)".
- **Location**: `plan.md` → Requirements Coverage row for NFR-003.
- **Mismatch**: the row cited only "Phase 3 (bounded change set)", but Phase 3's
  text describes the installer entry, count sites, and README rows without
  mentioning either constitution. The constraint is actually carried by Non-Goals.
- **Impact**: an implementer tracing NFR-003 lands on a phase whose text does not
  contain the constraint, weakening traceability for the invariant the repository
  most easily confuses.
- **Remediation applied**: the row now cites Non-Goals (explicit exclusion) and
  Phase 3 (bounded change set).

### Rejected candidate finding

- **Claim considered**: Phase 4 (derived regeneration) states a dependency only on
  Phase 1, but regeneration would also require Phase 3's registry entry, making the
  stated dependency incomplete.
- **Verification**: `src/codexspec/commands/installer.py` installs command
  templates with `for template_file in templates_dir.glob("*.md")` — the copy is
  driven by the templates directory, not by `get_commands_metadata()`, which feeds
  `list-commands` output and the init summary only.
- **Outcome**: **rejected**. A new template installs regardless of registration, so
  Phase 4's dependency on Phase 1 alone is accurate and complete. No defect.

## Requirement Coverage

| Requirement | Plan Reference | Design Component | Result |
|---|---|---|---|
| REQ-001 standalone command surface | Phase 1, Decision 1 | C1 | Covered |
| REQ-002 mode auto-detection | Phase 1, Phase 2 | C2, C3 | Covered |
| REQ-003 generate output boundary | Phase 1 | C4 | Covered |
| REQ-004 workspace records its slice | Phase 1 | C3 | Covered |
| REQ-005 derived content marked inferred/open | Phase 1, Phase 2 | C6 | Covered |
| REQ-006 confirmation reuses existing convention | Phase 1 | C6 | Covered |
| REQ-007 baseline is confirmed spec/design only | Phase 1, Phase 2 | C7 | Covered |
| REQ-008 unconfirmed baseline blocks reconcile | Phase 1, Phase 2 | C2 | Covered |
| REQ-009 three drift kinds | Phase 1, Phase 2 | C7 | Covered |
| REQ-010 persistent report plus briefing | Phase 1, Phase 2 | C8 | Covered |
| REQ-011 severity by impact; gates nothing | Phase 1, Phase 2 | C7, C8 | Covered |
| REQ-012 report only, never repair | Phase 1, Phase 2 | C7, C8, C10 | Covered |
| REQ-013 direction appeals to requirements | Phase 1, Phase 2 | C7 | Covered (round 1 fix) |
| REQ-014 slice unit and workspace creation | Phase 1 | C3 | Covered |
| REQ-015 bare run yields a map | Phase 1, Phase 2 | C2, C5 | Covered |
| REQ-016 scan discipline reused | Phase 1, Phase 2 | C9 | Covered |
| REQ-017 read-only, workspace-confined writes | Phase 1, Phase 2 | C10 | Covered |
| REQ-018 no pipeline coupling | Phase 1, Phase 2 | C1 | Covered |
| REQ-019 path-based slice input only | Phase 1, Phase 2 | C1 | Covered |
| REQ-020 registration and lockstep | Phase 3, Decisions 2 and 5 | C11 | Covered |
| REQ-021 language regime | Phases 1–3 | C1, C11 | Covered |
| NFR-001 English template with Language Preference | Phase 1, Phase 2, Decision 3 | C1 | Covered |
| NFR-002 self-bootstrap discipline | Phase 4, Decision 4 | C1 | Covered |
| NFR-003 two constitutions separate | Non-Goals, Phase 3 | C11 | Covered (round 1 fix) |
| NFR-004 scales without blocking | Phase 1 | C9 | Covered |
| NFR-005 independently readable output | Phase 1 | C3, C5 | Covered |
| NFR-006 no fabricated intent | Phase 1 | C4 | Covered |

Coverage: 27 of 27. Design component coverage: C1 (Phases 1, 4), C2–C10
(Phases 1, 2), C11 (Phase 3) — all eleven realized. Every phase and every
Plan-Level Decision carries `Covers: REQ-xxx; Design: <component>`. The plan
introduces no component, interface, or data model beyond `design.md`, and no
plan-level decision alters confirmed behavior.

### Repository facts verified during review

- `install_commands_to_subdir` copies via `templates_dir.glob("*.md")`, not via the
  registry — see the rejected finding above.
- All 8 `README*.md` files contain a `/codexspec:debug` row, confirming each has the
  Enhanced Commands table that Decision 5 targets; each also has a separate
  Self-Evolution table holding `onboard`, confirming that README grouping differs
  from the installer category as Decision 5 states.
- Installer categories are `core (11)`, `enhanced (8)` = `clarify, analyze,
  checklist, tasks-to-issues, distill, evolve, onboard, debug`, `git (3)`,
  `review (1)`, `utility (2)` — matching the Phase 3 deltas.
- Full-suite baseline measured on this branch: 1199 passed, 50 skipped, matching
  plan assumption A-1.

## Verified Defects

### Critical

None.

### Warnings

None.

### Minor

None remaining. Both round 1 Minor defects are documented above and resolved.

## Risk Advisories

- **Phase 1 has no automated gate of its own.** Applicability: Plan-Level Decision 1
  authors the template before its tests, so Phase 1 is verified by deterministic
  review against `design.md`. Risk: a component realized only partially in prose
  would not surface until Phase 2 happens to assert it, and Phase 2 asserts a
  chosen subset rather than every clause. The plan's deterministic doc check in the
  Verification Strategy is the intended control; the tasks stage is where scenario
  enumeration decides how much of C1–C10 is actually locked. Accepted trade-off,
  consistent with how every existing command template was built.

- **Nine of the template's clauses are Phase-1-only.** Applicability: REQ-003,
  REQ-004, REQ-006, REQ-014, NFR-004, NFR-005, NFR-006 are planned into the
  template without a named contract test. This is a legitimate scoping choice, not
  a defect — but it means the `Slice:` header convention (REQ-004), on which
  baseline lookup entirely depends, is unlocked. Worth considering at the tasks
  stage whether that one clause deserves an assertion.

## Design Opportunities

- **The verification table could record the measured baseline at run time.**
  Assumption A-1 pins 1199/50 while correctly stating the requirement is
  no-regression rather than a fixed number. Having the implementer record the
  measured baseline before Phase 1 would make the comparison self-documenting.
  Optional.

## Score Derivation

- Critical root causes: 0
- Warning root causes: 0
- Minor root causes: 0 (2 found in round 1, both resolved before this final review)
- Formula: no defects → `100`
- Advisories (2) and Design Opportunities (1) do not affect status or score.

## Follow-up Review — 2026-08-24

- **Overall Status**: PASS
- **Compatibility Score**: 100/100
- **Scope**: Phase 5 coverage-gap closure
- **Coverage**: Phase 5 traces REQ-002/007/008/014/015/017/022 to
  C1/C2/C3/C9/C10 and Decision 9, with regression tests before each template
  repair and derived regeneration after it.
- **Verified Defects**: none.

## Follow-up Review — 2026-08-24 (final security repair)

- **Overall Status**: PASS
- **Compatibility Score**: 100/100
- **Scope**: Phase 5 final gate repairs.
- **Coverage**: Phase 5 now includes path-entry containment, coherent workspace
  identity, sensitive-evidence redaction, and the design-only interrupted state;
  each maps to C1/C2/C3/C7/C8/C10 and a focused red-before-green contract.
- **Verified Defects**: none.

## Follow-up Review — 2026-08-27 (trust/parser/compatibility repair)

- **Overall Status**: PASS
- **Compatibility Score**: 100/100
- **Scope**: Phase 5 final gate repairs.
- **Coverage**: the phase includes global output redaction, hardlink rejection,
  unique status parsing, existing-path precedence, authority metadata correction,
  and the required regenerate/targeted/cross/full/freeze checks.
- **Verified Defects**: none.

## Follow-up Review — 2026-08-27 (workspace identity/read repair)

- **Overall Status**: PASS
- **Compatibility Score**: 100/100
- **Scope**: Phase 5 final workspace-boundary repairs.
- **Coverage**: safe baseline reads, exclusive collision retry, portable identity,
  Unicode suffix fallback, regenerate, complete verification, and freeze checks.
- **Verified Defects**: none.

## Follow-up Review — 2026-08-27 (Unicode identity/atomic publication repair)

- **Overall Status**: PASS
- **Compatibility Score**: 100/100
- **Scope**: Phase 5 final publication repairs.
- **Coverage**: two red-before-green contracts preserve distinct Unicode path
  identities and require marker-before-publication ordering, followed by source/SDD
  synchronization, regeneration, complete verification, and a frozen review gate.
- **Verified Defects**: none.

## Follow-up Review — 2026-08-27 (input/publication/replacement repair)

- **Overall Status**: PASS
- **Compatibility Score**: 100/100
- **Scope**: Phase 5 final trust and persistence repairs.
- **Coverage**: four reviewer reproductions plus one sibling-sweep contract cover
  literal input, identity serialization, control-safe output, native publication,
  and confirmed report replacement, followed by regeneration, full validation,
  freeze, and fresh isolated review.
- **Verified Defects**: none.

## Follow-up Review — 2026-08-27 (identity/handle/resume/preflight repair)

- **Overall Status**: PASS
- **Compatibility Score**: 100/100
- **Scope**: Phase 5 final identity, access, persistence, and ordering repairs.
- **Coverage**: four red-before-green contracts cover secret-bearing identity,
  opened-handle workspace access, confirmation-gated resume, and empty-code
  preflight ordering, followed by SDD synchronization, regeneration, complete
  validation, freeze, and a fresh isolated review.
- **Verified Defects**: none.

## Follow-up Review — 2026-08-28 (sibling trust/control-source repair)

- **Overall Status**: PASS
- **Compatibility Score**: 100/100
- **Scope**: Phase 5 final authority and serialization repair.
- **Coverage**: two red-before-green contracts cover repository-local sibling
  prompt isolation and untrusted-data-only control escaping, followed by SDD
  synchronization, regeneration, complete validation, freeze, and a fresh
  isolated review.
- **Verified Defects**: none.
