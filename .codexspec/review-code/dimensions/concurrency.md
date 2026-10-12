# Concurrency and lifecycle

## Purpose

Review concurrency and lifecycle using current affected behavior and contracts.

## Applicability

Mutable state, initialization, asynchronous work, synchronization or check/use operations can overlap.

## Non-Applicability and False Positives

Do not activate detail for hypothetical inputs or absent future requirements. Existing type, validation, state/order, ownership and framework guarantees may satisfy a checkpoint. A candidate cue alone is not a defect or maintenance benefit. Use common.md for admission and contrary-evidence rules.

## Necessary Evidence

For applicable checkpoints identify the input/state source, affected path, actual contract or present maintenance benefit, and existing guarantees. Defects require reachability, impact and change attribution; maintenance requires current benefit and compatibility.

## Completion

Record checked paths and key evidence, resolve material necessary gaps, and stop when applicable questions are answered. New traced boundaries may expand selection within the affected scope.

## Checkpoints

### CON-01

Identify actual shared mutable state and execution overlap; verify required isolation/atomicity using existing ownership, synchronization or transactional guarantees.

### CON-02

Check concurrent collection access under actual language/container guarantees and ownership; immutable or confined state needs no extra lock.

### CON-03

Check singleton/one-time initialization only where concurrent entry is possible and runtime initialization guarantees are insufficient.

### CON-04

Check lock scope against atomic invariants and demonstrated contention; neither finer nor coarser locking is universally better.

### CON-05

Identify the owner and completion/cancellation contract of background work; verify required exit and cleanup paths.

### CON-06

Check communication progress: producer/consumer lifetimes, blocking/buffering, close and cancellation behavior.

### CON-07

Check whether state may change between validation and use; verify the actual consistency mechanism across that window.
