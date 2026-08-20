# Design Review Report

## Summary

- **Overall Status**: PASS
- **Compatibility Score**: 100/100
- **Authority Mode**: Requirements-first
- **Readiness**: Ready for Planning

## Review Rounds

| Round | Status | Score | Outcome |
|---|---|---|---|
| 1 | PASS_WITH_WARNINGS | 94/100 | Two Minor defects, both traceability/coverage faults with deterministic remediation. Fixed automatically. |
| 2 | PASS | 100/100 | Both resolved; no residual defects. |

### Round 1 defect 1 — coverage attribution errors (Minor, resolved)

- **Evidence**: the design rule that every component and decision carries an
  accurate `Covers:`, and `spec.md` REQ-012 ("report only; never repair") /
  REQ-021 ("language regime").
- **Location**: `design.md` → C6 `Covers:` line, and the Requirements Coverage
  rows for REQ-012 and REQ-021.
- **Mismatch**: C6 governs inference marking and the confirmation contract and
  says nothing about refraining from repair, yet claimed to cover REQ-012. The
  REQ-021 row pointed at "NFR-001 coverage below" — another requirement's row
  rather than a design element.
- **Impact**: an implementer tracing REQ-012 would land on a component that does
  not constrain repair behavior, and REQ-021 had no directly resolvable design
  anchor — both weaken exactly the traceability the stage exists to provide.
- **Remediation applied**: removed REQ-012 from C6; re-pointed REQ-012 at C7, C8,
  and C10 (the components that actually withhold repair) and REQ-021 at C1 and C11.

### Round 1 defect 2 — NFR-003 had no genuine design coverage (Minor, resolved)

- **Evidence**: `spec.md` NFR-003 states that this feature does not modify
  `_get_default_constitution()` and does not propagate project-governance rules
  into the shipped default constitution; the constitution's own SCOPE callout
  separates the two constitutions.
- **Location**: `design.md` → C10 `Covers:` line and the NFR-003 coverage row.
- **Mismatch**: NFR-003 was attributed to C10, but C10 is a **runtime** safety
  boundary ("the command must not modify the constitution while running"). NFR-003
  is a **development-time** constraint on the feature's own change set. The two
  are different claims, so the requirement was in fact uncovered.
- **Impact**: the one requirement that guards the repository's most easily
  confused invariant — two constitutions that must never be synced — had no design
  element actually bounding the change set.
- **Remediation applied**: C11 now enumerates the bounded change set (template,
  installer entry and count sites, contract test, 8 README rows, regenerated
  derived artifacts) and states explicitly that neither constitution is touched;
  NFR-003 is re-pointed at C11 and removed from C10.

## Requirement Coverage

| Requirement | Design Reference | Result |
|---|---|---|
| REQ-001 standalone command surface | C1, Decision 1, Interface Contract | Covered |
| REQ-002 mode auto-detection | C2, C3, Decisions 2–3, Sequence | Covered |
| REQ-003 generate output boundary | C4, Sequence | Covered |
| REQ-004 workspace records its slice | C3, Decision 2, Key Entities | Covered |
| REQ-005 derived content marked inferred/open | C6, Key Entities | Covered |
| REQ-006 confirmation reuses existing convention | C6, Key Entities | Covered |
| REQ-007 baseline is confirmed spec/design only | C7, Sequence | Covered |
| REQ-008 unconfirmed baseline blocks reconcile | C2, Sequence | Covered |
| REQ-009 three drift kinds | C7, Decision 5 | Covered |
| REQ-010 persistent report plus briefing | C8, Key Entities, Sequence | Covered |
| REQ-011 severity by impact; gates nothing | C7, C8, Decision 6 | Covered |
| REQ-012 report only, never repair | C7, C8, C10 | Covered (round 1 fix) |
| REQ-013 direction appeals to requirements | C7, Decision 5 | Covered |
| REQ-014 slice unit and workspace creation | C3 | Covered |
| REQ-015 bare run yields a map | C2, C5, Decision 3, Sequence | Covered |
| REQ-016 scan discipline reused | C9, Decision 4 | Covered |
| REQ-017 read-only, workspace-confined writes | C10 | Covered |
| REQ-018 no pipeline coupling | C1, Decision 6 | Covered |
| REQ-019 path-based slice input only | Interface Contract | Covered |
| REQ-020 registration and lockstep | C11 | Covered |
| REQ-021 language regime | C1, C11 | Covered (round 1 fix) |
| NFR-001 English template with Language Preference | C1 | Covered |
| NFR-002 self-bootstrap discipline | C1, Decision 1 | Covered |
| NFR-003 two constitutions separate | C11 (bounded change set) | Covered (round 1 fix) |
| NFR-004 scales without blocking | C9 | Covered |
| NFR-005 independently readable output | C3, C5 | Covered |
| NFR-006 no fabricated intent | C4, Decision 5 | Covered |

Coverage: 27 of 27 (`REQ-001..021`, `NFR-001..006`). Every component (C1–C11) and
every Key Design Decision (1–6) carries a `Covers:` line. No design decision
alters confirmed behavior; Decision 5 is explicitly justified as a refinement of
REQ-010's already-mandatory `evidence` field rather than a narrowing of REQ-009.

### Repository facts verified

- `installer.py` currently declares `core (11) -> enhanced (8) -> git (3) ->
  review (1) -> utility (2)`, `Total: 25 commands`, and an inline
  `# Enhanced Commands (8)` comment — matching C11's stated deltas to 9 and 26.
- `tests/commands/test_installer.py` asserts `len(result) == 25` and
  `len(enhanced_commands) == 8`; `tests/test_cli.py` asserts `"25" in
  result.stdout` — the three independent count sites C11 names.
- `onboard.md` frontmatter and its `## Codebase Scan` section exist as C1 and C9
  describe, so the referenced discipline resolves to real text.
- `scripts/bash/create-new-feature.sh` generates `{YYYY-MMDD-HHMM}{rr}` ids and
  normalizes the feature name to ASCII kebab-case, consistent with C3's use of the
  slice's final path segment as the feature name.

## Verified Defects

### Critical

None.

### Warnings

None.

### Minor

None remaining. Both round 1 Minor defects are documented above and resolved.

## Risk Advisories

- **Slice-to-workspace binding depends on a user-maintained field.** Applicability:
  Decision 2 stores the slice path inside the artifacts, so moving or renaming a
  directory silently breaks the binding and the next run falls back to generate
  mode — quietly producing a second workspace for the same code instead of
  reconciling. The design already asks the user to choose when several workspaces
  match, so the failure is recoverable rather than destructive, but it is silent.
  Consider having the plan stage decide whether generate mode should say which
  slice value it recorded, so a later mismatch is diagnosable.

- **The `Slice:` header is a new artifact convention.** Applicability: `spec.md`
  and `design.md` produced by the forward pipeline carry no such field, so only
  reverse-spec-produced artifacts participate in baseline lookup. That is
  internally consistent, but a user who hand-writes a spec for a module will not
  get reconciliation until they add the field. Worth one sentence in the command's
  output or documentation; not a defect against any confirmed requirement.

## Design Opportunities

- **`slices.md` could record the survey's sampling depth per slice.** C9's
  discipline already distinguishes deep-read from sampled areas; carrying that
  distinction into the slice list would tell the user which candidate slices rest
  on thin evidence. Optional and outside the confirmed requirement.

## Score Derivation

- Critical root causes: 0
- Warning root causes: 0
- Minor root causes: 0 (2 found in round 1, both resolved before this final review)
- Formula: no defects → `100`
- Advisories (2) and Design Opportunities (1) do not affect status or score.
