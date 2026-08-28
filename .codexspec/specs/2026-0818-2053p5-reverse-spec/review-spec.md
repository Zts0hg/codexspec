# Specification Review Report

## Summary

- **Overall Status**: PASS
- **Compatibility Score**: 100/100
- **Authority Mode**: Requirements-first
- **Readiness**: Ready for Planning

## Review Rounds

| Round | Status | Score | Outcome |
|---|---|---|---|
| 1 | NEEDS_REVISION | 79/100 | One Warning: contradictory mode selection for a bare whole-repository run. Remediation was uniquely determined by upstream evidence and applied automatically. |
| 2 | PASS | 100/100 | Contradiction resolved; no residual defects. |

### Round 1 defect (resolved)

- **Evidence**: DEC-011 states unconditionally that "The bare run produces **no
  `spec.md` and no `reconcile.md`**", while DEC-005 defines mode selection by
  baseline presence.
- **Location**: `spec.md` → REQ-002 versus REQ-015.
- **Mismatch**: REQ-002 selected reconcile mode whenever a confirmed baseline
  existed, with no exception for the bare run. After a user confirms the overview
  workspace's `design.md`, a repeated bare run therefore satisfied REQ-002's
  reconcile condition while REQ-015 forbade producing a `reconcile.md`. The two
  requirements prescribed different behavior for the same input, and the spec
  admitted two materially different readings of whether a bare run can reconcile.
- **Impact**: an implementer could have built reconciliation-on-bare-run,
  contradicting confirmed DEC-011 and requiring rework of the mode-selection
  logic.
- **Remediation applied**: scoped baseline-driven mode detection to runs that
  supply a `[path]`, and stated that a bare run always performs the REQ-015
  architectural survey and never reconciles. DEC-011 is both unconditional and
  more specific to this case, so the fix direction was determined by upstream
  evidence and introduced no new product decision. A matching boundary-behavior
  row and a traceability update were added so the behavior is testable and
  traceable.

## Traceability

| Confirmed Entry | Spec Reference | Result |
|---|---|---|
| NEED-001 brownfield entry | REQ-003, REQ-016, User Story 1 | Covered |
| NEED-002 detect drift | REQ-009, REQ-010, REQ-012, User Story 2 | Covered |
| NEED-003 one command, two modes | REQ-002, User Stories 1–3 | Covered |
| NEED-004 slice-sized output | REQ-014, REQ-015, NFR-004, NFR-005 | Covered |
| NEED-005 standalone, read-only | REQ-001, REQ-017 | Covered |
| DEC-001 output boundary | REQ-003, NFR-006 | Covered |
| DEC-002 inferred/open until confirmed | REQ-005, REQ-006 | Covered |
| DEC-003 report only, human direction | REQ-012 | Covered |
| DEC-004 baseline is spec/design, not requirements | REQ-007, REQ-013 | Covered |
| DEC-005 mode detection and degradation | REQ-002, REQ-004, REQ-008, User Story 3 | Covered |
| DEC-006 slice unit, own workspace | REQ-002, REQ-004, REQ-014 | Covered |
| DEC-007 reuse onboard scanning discipline | REQ-016, NFR-004 | Covered |
| DEC-008 persistent report plus briefing; naming | REQ-010 | Covered |
| DEC-009 standalone, no chaining | REQ-001, REQ-018 | Covered |
| DEC-010 report structure and severity | REQ-009, REQ-010, REQ-011 | Covered |
| DEC-011 slice definition, whole-repo map | REQ-002, REQ-014, REQ-015, User Story 4 | Covered (round 1 fix) |
| DEC-012 confirmed baseline mechanism | REQ-005, REQ-006 | Covered |
| CON-001 template governance | REQ-001, NFR-002 | Covered |
| CON-002 distribution lockstep, language family | REQ-020, REQ-021 | Covered |
| CON-003 English template, Language Preference | REQ-001, REQ-021, NFR-001 | Covered |
| CON-004 read-only, workspace-confined writes | REQ-017 | Covered |
| CON-005 two constitutions separate | NFR-003 | Covered |
| CON-006 authoritative script and ID convention | REQ-014 | Covered |
| OUT-001 no auto code change / drift resolution | REQ-012, Out of Scope | Covered |
| OUT-002 no profile writes | REQ-017, Out of Scope | Covered |
| OUT-003 no fabricated intent | REQ-003, REQ-005, NFR-006 | Covered |
| OUT-004 no code-vs-requirements comparison | REQ-007, Out of Scope | Covered |
| OUT-005 no monolithic repo spec | REQ-015, NFR-005 | Covered |
| OUT-006 no auto_next / auto_distill | REQ-018 | Covered |
| OUT-007 no diff/PR slice source | REQ-019 | Covered |

Coverage: 30 of 30 confirmed entries. Sources validity: all 21 `REQ` and 6 `NFR`
items cite at least one existing confirmed entry. No `OPEN` entry exists upstream,
so none could be promoted. The single labeled assumption (A-1, workspace records
its slice) is derived from DEC-005 plus DEC-006 and is stated as an assumption
rather than as confirmed intent.

## Verified Defects

### Critical

None.

### Warnings

None remaining. The round 1 Warning is documented above and was resolved.

### Minor

None.

## Risk Advisories

- **Semantic-mismatch detection depth is the feature's hardest technical risk.**
  Applicability: REQ-009's third kind requires judging that code and prose
  disagree in *meaning*, which is materially harder than detecting presence or
  absence. Risk: a shallow implementation degrades to near-zero recall on exactly
  the drift class the user cares most about ("确保代码实现没有偏离设计"), while a
  loose one produces false drift that erodes trust in the report. Relationship to
  the goal: this is the anti-drift core, not a peripheral case. Consider having
  the design stage state explicitly how much semantic comparison is attempted and
  what it declines to judge, and prefer `needs-your-judgment` (already available
  per REQ-013) over a confident wrong direction.

- **Confirmation is a manual, easily skipped step.** Applicability: REQ-006
  deliberately reuses the existing convention and adds no new command, so
  promotion to baseline depends on the user editing a status line. Risk: users may
  never confirm, leaving the feature permanently in generate mode and never
  delivering the anti-drift value. Relationship to the goal: the confirmed
  lifecycle (DEC-005) makes reconciliation contingent on this step. The generate
  mode's closing report is a natural place to state the exact confirmation action;
  this is a presentation choice, not a defect.

## Design Opportunities

- **`slices.md` could carry a suggested ordering.** REQ-015 requires path, a
  one-line description, and rough size or priority. Ordering the list so the
  highest-value slices appear first would make the deepening plan directly
  actionable on a large brownfield repository. Optional; the confirmed
  requirement does not demand it.

## Score Derivation

- Critical root causes: 0
- Warning root causes: 0 (1 found in round 1, resolved before this final review)
- Minor root causes: 0
- Formula: no defects → `100`
- Advisories (2) and Design Opportunities (1) do not affect status or score.

## Follow-up Review — 2026-08-24

- **Overall Status**: PASS
- **Compatibility Score**: 100/100
- **Scope**: G-3/G-4/G-5 closure
- **Traceability**: NEED-006 → REQ-002/007/008/015/022; DEC-015 →
  REQ-007/008/022; CON-008 → REQ-022; OUT-008 → Out of Scope.
- **Verified Defects**: none. The specification distinguishes a genuinely absent
  design from a present unconfirmed design and requires symlink resolution before
  the repository-root short-circuit. The complete-feature repair also makes
  trust, workspace/write-target containment, descendant symlinks, and conflicting
  identity markers explicit consequences of REQ-002/REQ-017.

## Follow-up Review — 2026-08-24 (final security repair)

- **Overall Status**: PASS
- **Compatibility Score**: 100/100
- **Scope**: REQ-002/004/008/010/017/022 clarification after the isolated gate.
- **Traceability**: existing confirmed DEC-015 and CON-004 now explicitly cover a
  missing spec, coherent cross-artifact `Slice:` identity, every path-entry
  containment check, and sensitive-evidence redaction.
- **Verified Defects**: none. All four cases are deterministic consequences of the
  existing mode, never-guess, workspace confinement, and sensitive-data rules;
  no new product choice was introduced.

## Follow-up Review — 2026-08-27 (trust/parser/compatibility repair)

- **Overall Status**: PASS
- **Compatibility Score**: 100/100
- **Scope**: REQ-001/002/008/010/017/019/022 clarification.
- **Traceability**: confirmed DEC-012, CON-004, and OUT-007 now explicitly cover
  unique status metadata, hardlink-safe writes, global sensitive-value redaction,
  and existing-path precedence over changeset-shaped spelling.
- **Verified Defects**: none. The repair narrows no product behavior and introduces
  no new mechanism; it closes deterministic consequences of existing authority.

## Follow-up Review — 2026-08-27 (workspace identity/read repair)

- **Overall Status**: PASS
- **Compatibility Score**: 100/100
- **Scope**: REQ-002/004/014/017/022 clarification.
- **Traceability**: DEC-013, CON-004, and CON-007 now cover portable persisted
  identity, validated workspace reads, and exclusive random-collision retry.
- **Verified Defects**: none; the ASCII `slice` suffix remains a human fallback,
  while the portable in-artifact value remains authoritative identity.

## Follow-up Review — 2026-08-27 (Unicode identity/atomic publication repair)

- **Overall Status**: PASS
- **Compatibility Score**: 100/100
- **Scope**: REQ-002/004/014/016/017/022 and NFR-004 clarification.
- **Traceability**: DEC-013 preserves exact filesystem code points; CON-004's
  workspace boundary requires identity to validate before an official workspace
  becomes visible.
- **Verified Defects**: none. Separator portability no longer collapses distinct
  canonically equivalent directories, and interrupted creation exposes no
  unidentifiable official workspace.

## Follow-up Review — 2026-08-27 (input/publication/replacement repair)

- **Overall Status**: PASS
- **Compatibility Score**: 100/100
- **Scope**: REQ-001/002/004/010/014/016/017/019/022 and NFR-004.
- **Traceability**: DEC-008, DEC-013, CON-004, and CON-007 now pin literal argument
  data flow, control-safe identity/output, executable native publication, and
  explicit confirmation before report replacement.
- **Verified Defects**: none; each repair is a deterministic safety or persistence
  consequence of confirmed boundaries rather than new product intent.

## Follow-up Review — 2026-08-27 (identity/handle/resume/preflight repair)

- **Overall Status**: PASS
- **Compatibility Score**: 100/100
- **Scope**: REQ-002/004/008/014/016/017/022 and NFR-004.
- **Traceability**: DEC-015, CON-004, and CON-007 now refuse secret-bearing slice
  identity, bind workspace access to verified opened objects, require explicit
  confirmation before appending to pre-existing artifacts, and put the empty-code
  preflight before workspace preparation.
- **Verified Defects**: none. These changes resolve contradictions or race windows
  inside already-confirmed safety and persistence boundaries; they add no product
  mode or authority source.

## Follow-up Review — 2026-08-28 (sibling trust/control-source repair)

- **Overall Status**: PASS
- **Compatibility Score**: 100/100
- **Scope**: REQ-010/016/017/022 and NFR-004.
- **Traceability**: DEC-007 and CON-004 now distinguish behavioral reuse from
  runtime prompt inclusion and preserve the existing untrusted-input source
  qualifier for control escaping.
- **Verified Defects**: none. The scan behavior is unchanged; authority is closed
  over repository-local sibling prompts, and command-authored Markdown structure
  remains outside data escaping.
