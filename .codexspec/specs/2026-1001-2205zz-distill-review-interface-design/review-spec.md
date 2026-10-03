# Specification Review Report

## Summary

- **Overall Status**: PASS
- **Compatibility Score**: 100/100
- **Authority Mode**: Requirements-first
- **Readiness**: Ready for Planning
- **Rounds**: 2 (round 1 found four defects; round 2 found one further defect; all five were remediated within the automatic fix budget)

The specification compiles every confirmed need, constraint, decision, and exclusion from `requirements.md`. All seven review safety invariants are carried intact, every functional and non-functional requirement cites a confirmed source, every cited source exists as a confirmed entry, and no resolved question is presented as an open product choice. Both matters this review raised for the user have since been decided by the user and folded into the confirmed record; see **Raised For Decision, Now Settled** below. No open question remains.

## Traceability

| Confirmed Entry | Spec Reference | Result |
|---|---|---|
| NEED-001 | REQ-001, REQ-002, REQ-003, REQ-023 | Full |
| NEED-002 | REQ-004 | Full |
| NEED-003 | REQ-005 | Full |
| NEED-004 | REQ-006 through REQ-009, REQ-023 | Full |
| NEED-005 | REQ-001, REQ-003, REQ-010, REQ-011, REQ-023 | Full |
| NEED-006 | REQ-012, REQ-013, REQ-023 | Full |
| NEED-007 | REQ-014, REQ-015 | Full |
| NEED-008 | REQ-016, REQ-017 | Full |
| NEED-009 | REQ-018, REQ-019 | Full |
| NEED-010 | NFR-001, NFR-002 | Full |
| NEED-011 | NFR-003, NFR-004 | Full |
| NEED-012 | REQ-017, REQ-021, REQ-022 | Full |
| NEED-013 | REQ-020 | Full |
| NEED-014 | REQ-013, REQ-023 | Full — confirmed after this review raised it; see Raised For Decision, Now Settled |
| CON-001 | NFR-005 | Full |
| CON-002 | NFR-006 | Full |
| CON-003 | NFR-007, REQ-007, REQ-008, REQ-015, REQ-020 | Full |
| CON-004 | NFR-008 | Full |
| CON-005 | NFR-009 | Full |
| CON-006 | NFR-010, REQ-022 | Full |
| DEC-001 | REQ-001; Confirmed Constraints and Decisions | Full |
| DEC-002 | NFR-001, REQ-012; Confirmed Constraints and Decisions | Full |
| DEC-003 | NFR-001, REQ-006; Confirmed Constraints and Decisions | Full |
| DEC-004 | NFR-008; Confirmed Constraints and Decisions | Full |
| DEC-005 | Confirmed Constraints and Decisions; Requirements Traceability | Full — process decision, correctly produces no requirement |
| OUT-001 | Out of Scope; NFR-007 | Full |
| OUT-002 | Out of Scope; REQ-016 | Full |
| OUT-003 | Out of Scope; NFR-005 | Full |
| OUT-004 | Out of Scope; NFR-005 | Full |
| OPEN-001 | REQ-018 | Resolved before compilation; carried as a requirement, not promoted as an open item |
| OPEN-002 | REQ-020 | Resolved before compilation; carried as a requirement, not promoted as an open item |
| OPEN-003 | NFR-002 | Resolved before compilation; carried as a requirement, not promoted as an open item |

## Verified Defects

### Critical

None.

### Warnings

None outstanding.

### Minor

None outstanding.

## Remediated During Review

Each entry records a defect that was verified, its remediation, and the confirmed evidence that determined the remediation. No remediation introduced a product decision.

### Round 1

- **W-001 (Warning) — the confirmed focus-indicator obligation was missing.** NEED-012 requires that every control carry a focus indicator visible in both colour schemes; the first compiled draft carried only NEED-012's queue-selection half, so design and planning would have had no reason to define focus treatment per scheme and the interface could have shipped with an invisible focus indicator in one of them. Remediated by adding the obligation to REQ-022, which already carries NEED-012, with an acceptance scenario under User Story 5 and coverage in SC-006. Wording taken from NEED-012.
- **W-002 (Warning) — the consolidation-cluster surface was open to two materially different readings.** Clusters are in scope in REQ-002, REQ-006, REQ-011 and in the Edge Cases, and the cluster surface carries its own decision set (merge as candidate, merge as vetted, keep separate), none of which appeared in REQ-012's routine or separated group. The literal reading left the cluster surface with the undifferentiated control row this feature exists to remove. Remediated by adding REQ-023, which applies the already-confirmed working-surface rules — REQ-005, REQ-006 through REQ-009, and REQ-012's separation of routine from file-removing decisions — to the cluster surface, defers the arrangement of its three decisions to design, and states explicitly that the merge-confirmation question is not settled here.
- **M-001 (Minor) — NFR-006's justification for excluding vector graphics was technically false.** An `<svg>` element written inline in an HTML document is placed in the SVG namespace by the parser and needs no namespace attribute, so the original reason ("a vector root element declares a namespace URL") could be refuted. Remediated by restating the accurate obstacle: the page builds its content from script, where creating an SVG node requires the namespace URL, and a stylesheet `data:` URI reference requires the namespace declaration; either route would put an absolute URL scheme into assets that `tests/test_distill_review_interfaces.py::test_frontend_is_offline_and_uses_fragment_bearer` asserts contain none. The confirmed exclusion in CON-002 is unchanged.
- **M-002 (Minor) — the missing-catalog edge case cited rules that do not contain it.** The English-catalog fallback is existing carrier behavior preserved by NFR-007 and OUT-001, not an obligation of NFR-008 or NFR-009. Remediated by re-attributing the bullet and scoping the NFR-008 reference to the key-parity obligation it actually states.

### Round 2

- **M-003 (Minor) — "one colour per decision state" admitted a seven-colour reading that contradicts the confirmed palette.** NFR-001 required one colour per decision state while Key Entities defined decision state through the backend's seven accounting groups, so a designer could have read NFR-001 as demanding seven state colours, contradicting DEC-002, which confirms one colour each for vetted, discarded, and deferred plus a single accent. Remediated from DEC-002's own enumeration: NFR-001 now names the state colours, and Key Entities separates the queue-level decision state that the colours cover from the ledger group that counts the staged batch, noting that several ledger groups can describe one record's single decision.

## Raised For Decision, Now Settled

Both advisories this review raised were put to the user, who decided both. The resulting changes are recorded in `requirements.md` and carried into `spec.md`; the specification was re-verified against the amended record afterwards, and every confirmed need, including the new one, is traced above.

- **Merging removes files but was not covered by the confirmed second-confirmation rule.** A confirmed merge creates the generalized record and removes every superseded member record when the batch is applied, so merging removes files exactly as discarding does, while NEED-006 and therefore REQ-013 named only discarding a record and discarding the draft. Extending the rule was a new product requirement that this review could not apply on its own. **Decision**: the user extended it — "把二次确认扩到合并。" Recorded as NEED-014 (confirmed 2026-10-01 22:42:17 +0800), with an "Extended By" pointer added to NEED-006, whose confirmed statement is unchanged. REQ-013 now covers all three file-removing or decision-dropping actions, REQ-023 classifies merging as file-removing and keeping records separate as routine, SC-004 measures all three, and User Story 3 carries an acceptance scenario for the merge case.
- **Progress counting across a merged cluster was derivable but not stated.** If the design counted queue entries instead of the backend's accounting, a cluster of three members staged as one merge would be counted differently from the ledger and the progress figure would disagree with it. **Decision**: the user directed that the advisories be implemented as recommended — "风险提示按照你建议的实施。" Because this refines NEED-002 and NEED-005 rather than adding product intent, it is recorded in the specification rather than as a new confirmed entry: REQ-004 now requires the figure to be derived from the same accounting the ledger uses and states the cluster case explicitly, and cites both NEED-002 and NEED-005.

## Risk Advisories

None outstanding.

## Design Opportunities

Both were put to the user with the advisories above and both are adopted in `design.md`.

- **REQ-007 can be satisfied with one additive read-only field.** The backend already holds the authoritative set of previewed operations, keyed by the draft revision, and discards an entry once its operation is staged. Reporting that state — a per-item gate flag, or the previewed-operation key — in the session and draft responses would let the page display the gate rather than infer it. That is precisely the additive, test-covered backend extension CON-003 permits, and it removes the page-side inference REQ-007 exists to eliminate.
- **The keyboard map and the text mode can be defined from one table.** REQ-016 requires reusing the text review mode's letters where they exist and OUT-002 forbids changing that mode. Defining the shared letters in one place both carriers read would make REQ-016 directly testable and keep the two maps from drifting.

## Score Derivation

- Critical root causes: 0
- Warning root causes: 0
- Minor root causes: 0
- Formula: No outstanding defects = **100**. Round 1 scored 65 (two Warnings, two Minor: max(50, 79 − 8 × 1 − 3 × 2)); all four were remediated, round 2 found and remediated one further Minor, and the final document carries no verified defect. Advisories and the recorded open matter do not affect the score.
