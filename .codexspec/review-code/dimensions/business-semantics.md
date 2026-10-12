# Business rules and state semantics

## Purpose

Review business rules and state semantics using current affected behavior and contracts.

## Applicability

Confirmed domain preconditions, status transitions, identity, limits or result contracts are affected.

## Non-Applicability and False Positives

Do not activate detail for hypothetical inputs or absent future requirements. Existing type, validation, state/order, ownership and framework guarantees may satisfy a checkpoint. A candidate cue alone is not a defect or maintenance benefit. Use common.md for admission and contrary-evidence rules.

## Necessary Evidence

For applicable checkpoints identify the input/state source, affected path, actual contract or present maintenance benefit, and existing guarantees. Defects require reachability, impact and change attribution; maintenance requires current benefit and compatibility.

## Completion

Record checked paths and key evidence, resolve material necessary gaps, and stop when applicable questions are answered. New traced boundaries may expand selection within the affected scope.

## Checkpoints

### BUS-01

Trace required preconditions to their enforceable boundary, including required behavior that is absent.

### BUS-02

Check required rejection and failure behavior alongside the happy path; activate checks from obligations, not just existing code.

### BUS-03

Preserve required distinctions between success, failure and partial success.

### BUS-04

Inspect reachable paths that execute successfully but violate an actual domain rule.

### BUS-05

Check response/results, error/status codes and persisted outcomes describe the same operation.

### BUS-06

Check when old/new values, states, credentials and resources are compared relative to mutation.

### BUS-07

Check applicable uniqueness, ownership/policy, state transition, irreversibility and quota invariants.

### BUS-08

Check business error/status results actually govern subsequent execution rather than being recorded and ignored.
