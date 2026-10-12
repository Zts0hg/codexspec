# Material performance

## Purpose

Review material performance using current affected behavior and contracts.

## Applicability

Actual operation frequency, data volume, latency or resource budgets make selected behavior consequential.

## Non-Applicability and False Positives

Do not activate detail for hypothetical inputs or absent future requirements. Existing type, validation, state/order, ownership and framework guarantees may satisfy a checkpoint. A candidate cue alone is not a defect or maintenance benefit. Use common.md for admission and contrary-evidence rules.

## Necessary Evidence

For applicable checkpoints identify the input/state source, affected path, actual contract or present maintenance benefit, and existing guarantees. Defects require reachability, impact and change attribution; maintenance requires current benefit and compatibility.

## Completion

Record checked paths and key evidence, resolve material necessary gaps, and stop when applicable questions are answered. New traced boundaries may expand selection within the affected scope.

## Checkpoints

### PER-01

Check repeated database calls for actual N+1 cost at relevant scale and available batching/caching guarantees.

### PER-02

Check repeated large allocation/copy against actual object size and execution frequency.

### PER-03

Check repeated or avoidable loop work for meaningful cost; alternatives must preserve the required operation.

### PER-04

Check I/O granularity and buffering against relevant workload and existing library buffering.

### PER-05

Check repeated serialization/deserialization for material cost and whether conversions serve required boundaries.
