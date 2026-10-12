# Incremental maintainability

## Purpose

Review incremental maintainability using current affected behavior and contracts.

## Applicability

Selected changes or directly affected structure have a substantiated current readability, maintenance or extension problem.

## Non-Applicability and False Positives

Do not activate detail for hypothetical inputs or absent future requirements. Existing type, validation, state/order, ownership and framework guarantees may satisfy a checkpoint. A candidate cue alone is not a defect or maintenance benefit. Use common.md for admission and contrary-evidence rules.

## Necessary Evidence

For applicable checkpoints identify the input/state source, affected path, actual contract or present maintenance benefit, and existing guarantees. Defects require reachability, impact and change attribution; maintenance requires current benefit and compatibility.

## Completion

Record checked paths and key evidence, resolve material necessary gaps, and stop when applicable questions are answered. New traced boundaries may expand selection within the affected scope.

## Checkpoints

### MAI-01

Identify complex functions whose present control/data structure obstructs comprehension; line-count thresholds are inspection cues, never proof or mandatory splitting.

### MAI-02

Identify duplicated meaningful behavior whose current inconsistency or repeated editing creates maintenance cost; occurrence counts alone do not require abstraction.

### MAI-03

Identify unexplained literals whose shared meaning or current comprehension cost warrants a name; do not introduce constants mechanically.
