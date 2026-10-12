# Logic and data flow

## Purpose

Review logic and data flow using current affected behavior and contracts.

## Applicability

Affected control flow, value propagation, parsing, time, ordering or shared data contracts.

## Non-Applicability and False Positives

Do not activate detail for hypothetical inputs or absent future requirements. Existing type, validation, state/order, ownership and framework guarantees may satisfy a checkpoint. A candidate cue alone is not a defect or maintenance benefit. Use common.md for admission and contrary-evidence rules.

## Necessary Evidence

For applicable checkpoints identify the input/state source, affected path, actual contract or present maintenance benefit, and existing guarantees. Defects require reachability, impact and change attribution; maintenance requires current benefit and compatibility.

## Completion

Record checked paths and key evidence, resolve material necessary gaps, and stop when applicable questions are answered. New traced boundaries may expand selection within the affected scope.

## Checkpoints

### LOG-01

Check branch coverage against reachable inputs and required states; impossible combinations do not require branches.

### LOG-02

Check loop start, stop and progress against actual input size and termination obligations.

### LOG-03

Check required return/results on reachable paths under the language and function contract.

### LOG-04

Inspect unreachable statements only for lost required behavior or substantiated local maintenance benefit.

### LOG-05

Check Boolean composition, precedence and negation against the intended predicate.

### LOG-06

Check comparison direction and inclusive/exclusive boundaries against the relevant rule.

### LOG-07

Trace similarly named fields and variables from their producers to the actual consumer; detect wrong identities.

### LOG-08

Check argument order and meaning, including same-typed parameters that can be swapped.

### LOG-09

Check that the returned value is the intended result rather than another related variable.

### LOG-10

Compare equivalent copied implementations and symmetric paths when a concrete common cause justifies it.

### LOG-11

Check time zones, timestamp units and calendar calculations only for supported temporal behavior.

### LOG-12

Trace cache/database reads and writes; check required invalidation, key identity and read/write symmetry.

### LOG-13

Check interface implementations against their declared result and behavioral contracts.

### LOG-14

Check equality against required value/reference identity, normalization and case semantics.

### LOG-15

Verify documented preconditions and postconditions against actual enforcement; documentation is evidence, not new product authority.

### LOG-16

Investigate unused accepted parameters when they imply lost behavior or present confusion; interface placeholders can be intentional.

### LOG-17

Check mutually exclusive fields against reachable writes and the actual state invariant.

### LOG-18

Check error/early-exit flow prevents unintended success effects when the failure contract requires it.

### LOG-19

Check concatenation, slicing, trimming and parsing preserve required string meaning and character boundaries.

### LOG-20

Check stable collection ordering only when an API, consumer, reproducibility or confirmed requirement depends on it.

### LOG-21

Check diagnostics name the actual failed condition and relevant field so users can act on them.
