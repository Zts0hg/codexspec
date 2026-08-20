# Tasks Review Report

## Summary

- **Overall Status**: PASS
- **Compatibility Score**: 100/100
- **Authority Mode**: Requirements-first
- **Readiness**: Ready for Implementation

## Review Rounds

| Round | Status | Score | Outcome |
|---|---|---|---|
| 1 | PASS_WITH_WARNINGS | 94/100 | Two Minor defects, both deterministic corrections. Fixed automatically. |
| 2 | PASS | 100/100 | Both resolved; no residual defects. |

### Round 1 defect 1 — T4.2 carried a non-specific `Covers:` (Minor, resolved)

- **Evidence**: the task rule that every task includes `Covers: REQ-xxx; Plan: <component/phase>`.
- **Location**: `tasks.md` → T4.2.
- **Mismatch**: the line read "all REQ/NFR by verification", naming no identifiers.
- **Impact**: the final checkpoint could not be traced to specific requirements,
  weakening the coverage table it feeds.
- **Remediation applied**: `Covers:` now names `REQ-001..021` and `NFR-001..006`
  and states that the task is a whole-feature regression checkpoint rather than an
  individual gate.

### Round 1 defect 2 — dependency diagram contradicted T4.2's declared dependencies (Minor, resolved)

- **Evidence**: T4.2 declares `Dependencies: T1.1, T2.1, T3.2, T3.3, T4.1`.
- **Location**: `tasks.md` → Dependency Summary diagram.
- **Mismatch**: the diagram routed T4.1 and the T3.x chain into T4.2 but left T2.1
  as a dangling leaf off T1.1, so the picture disagreed with the declaration.
- **Impact**: an implementer reading the diagram could run the final verification
  before the contract tests exist, producing a green baseline that proves nothing
  about the template discipline.
- **Remediation applied**: the diagram now routes T2.1 into T4.2 alongside T4.1 and
  the T3.x chain.

## Coverage

| Requirement / Plan Item | Task References | Result |
|---|---|---|
| Plan Phase 1 — command template (C1–C10) | T1.1 | Covered |
| Plan Phase 2 — contract tests | T2.1 | Covered |
| Plan Phase 3 — registration and count sites (C11) | T3.1, T3.2, T3.3 | Covered |
| Plan Phase 4 — regeneration and verification | T4.1, T4.2 | Covered |
| Plan Decision 1 — template before tests | T1.1 → T2.1 ordering | Covered |
| Plan Decision 2 — up-front grep sweep | T3.1 step 1, T3.2 step 6 | Covered |
| Plan Decision 3 — emphasis-free assertions | T2.1 constraint | Covered |
| Plan Decision 4 — regenerate last with `--ai both` | T4.1 | Covered |
| Plan Decision 5 — README Enhanced table | T3.3 | Covered |
| REQ-001 standalone command surface | T1.1, T2.1 (S1) | Covered |
| REQ-002 mode auto-detection | T1.1, T2.1 (S3, S4, S5) | Covered |
| REQ-003 generate output boundary | T1.1 | Covered |
| REQ-004 workspace records its slice | T1.1 | Covered |
| REQ-005 derived content marked inferred/open | T1.1, T2.1 (S16) | Covered |
| REQ-006 confirmation reuses existing convention | T1.1 | Covered |
| REQ-007 baseline is confirmed spec/design only | T1.1, T2.1 (S7, S8) | Covered |
| REQ-008 unconfirmed baseline blocks reconcile | T1.1, T2.1 (S6) | Covered |
| REQ-009 three drift kinds | T1.1, T2.1 (S9, S12) | Covered |
| REQ-010 persistent report plus briefing | T1.1, T2.1 (S12, S15) | Covered |
| REQ-011 severity by impact; gates nothing | T1.1, T2.1 (S10, S11) | Covered |
| REQ-012 report only, never repair | T1.1, T2.1 (S14) | Covered |
| REQ-013 direction appeals to requirements | T1.1, T2.1 (S13) | Covered |
| REQ-014 slice unit and workspace creation | T1.1 | Covered |
| REQ-015 bare run yields a map | T1.1, T2.1 (S3) | Covered |
| REQ-016 scan discipline reused | T1.1, T2.1 (S18) | Covered |
| REQ-017 read-only, workspace-confined writes | T1.1, T2.1 (S17) | Covered |
| REQ-018 no pipeline coupling | T1.1, T2.1 (S11, S20) | Covered |
| REQ-019 path-based slice input only | T1.1, T2.1 (S1, S19) | Covered |
| REQ-020 registration and lockstep | T3.1 (S1–S4), T3.2, T3.3 | Covered |
| REQ-021 language regime | T1.1, T2.1 (S2), T3.2, T4.2 | Covered |
| NFR-001 English template with Language Preference | T1.1, T2.1 (S2) | Covered |
| NFR-002 self-bootstrap discipline | T4.1 | Covered |
| NFR-003 two constitutions separate | T3.2 step 5 | Covered |
| NFR-004 scales without blocking | T1.1 | Covered |
| NFR-005 independently readable output | T1.1 | Covered |
| NFR-006 no fabricated intent | T1.1 | Covered |

Coverage: 27 of 27 requirements, 4 of 4 plan phases, 5 of 5 plan-level decisions.
Every task carries `Covers:` plus a plan reference. Dependencies are acyclic and
each dependent is ordered after its predecessors. No task expands product scope or
alters the approved plan.

### Executability checks performed

- **Paths verified**: `templates/commands/reverse-spec.md` (new, correct source
  directory per the self-bootstrap rule), `tests/test_reverse_spec_template.py`
  (new, matching the `test_onboard_template.py` naming precedent),
  `src/codexspec/commands/installer.py`, `tests/commands/test_installer.py`,
  `tests/test_cli.py`, and all 8 `README*.md` files — all exist as referenced.
- **Count deltas verified against the live registry**: total 25 → 26, enhanced
  8 → 9, matching `get_commands_metadata()` and the two independent assertion
  sites.
- **T3.1/T3.2 red-green ordering is real**: S3 (registry entry shape) cannot pass
  before T3.2 adds the entry, so the red state is genuine rather than nominal.
- **`[P]` marking is safe**: T1.1 and T3.1 touch disjoint files (a new template
  versus two test files) and neither consumes the other's output.
- **Scenario traceability is one-to-one**: 20 scenarios on T2.1 and 4 on T3.1, each
  individually identified and each derived from a specification acceptance
  criterion or requirement behavior. None is invented.

## Verified Defects

### Critical

None.

### Warnings

None.

### Minor

None remaining. Both round 1 Minor defects are documented above and resolved.

## Risk Advisories

- **Seven requirements are verified only by T1.1's deterministic read.** REQ-003,
  REQ-004, REQ-006, REQ-014, NFR-004, NFR-005, and NFR-006 have no contract-test
  scenario. This follows the approved plan (Decision 1 makes Phase 1 a
  deterministic-review deliverable) and is therefore not a tasks-level defect. The
  sharpest instance remains REQ-004: the `Slice:` header convention is the entire
  basis of baseline lookup, and nothing fails if the template omits it. The
  implementer's own §7.3a scenario self-check will not catch this either, since no
  scenario is enumerated for it — the deterministic checklist in T1.1 is the only
  control.

- **T1.1 is a single large task covering 24 requirements.** Splitting a single
  prose file would create artificial validation boundaries, so keeping it whole is
  correct per the task rules. The consequence is that partial completion is not
  independently verifiable; the section-by-component table inside T1.1 is what
  makes progress checkable.

## Design Opportunities

- **T3.1's sweep command could be recorded with its output.** Plan Decision 2 exists
  because the count sites were previously discovered one review round at a time.
  Pasting the sweep's result into the task record would make it evident at review
  time that the sweep actually ran. Optional; not required for correctness.

## Score Derivation

- Critical root causes: 0
- Warning root causes: 0
- Minor root causes: 0 (2 found in round 1, both resolved before this final review)
- Formula: no defects → `100`
- Advisories (2) and Design Opportunities (1) do not affect status or score.
