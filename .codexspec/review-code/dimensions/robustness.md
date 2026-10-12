# Robustness and resource ownership

## Purpose

Review robustness and resource ownership using current affected behavior and contracts.

## Applicability

Input boundaries, fallible operations, conversions, resources or failure/recovery behavior are affected.

## Non-Applicability and False Positives

Do not activate detail for hypothetical inputs or absent future requirements. Existing type, validation, state/order, ownership and framework guarantees may satisfy a checkpoint. A candidate cue alone is not a defect or maintenance benefit. Use common.md for admission and contrary-evidence rules.

## Necessary Evidence

For applicable checkpoints identify the input/state source, affected path, actual contract or present maintenance benefit, and existing guarantees. Defects require reachability, impact and change attribution; maintenance requires current benefit and compatibility.

## Completion

Record checked paths and key evidence, resolve material necessary gaps, and stop when applicable questions are answered. New traced boundaries may expand selection within the affected scope.

## Checkpoints

### ROB-01

Trace an actual absent-value source to a dereference and check existing guarantees before requesting a null guard.

### ROB-02

Check reachable index/slice bounds against producers and invariants; use actual language indexing behavior.

### ROB-03

Check missing-key semantics against whether absence is valid, distinguishable or a failure under the contract.

### ROB-04

Identify fallible results that matter to required behavior; verify meaningful handling rather than demanding every result be checked identically.

### ROB-05

Check numeric range, overflow and precision against actual types, operations and supported input scale.

### ROB-06

Check field limits and common abuse paths against applicable business/resource constraints at an enforceable boundary.

### ROB-07

Check required restricted-value validation before downstream effects, accepting equivalent type/schema guarantees.

### ROB-08

Check pagination/batch size against actual supported limits and resource exposure; no universal numeric bounds are invented.

### ROB-09

Trace nested absent values through validation into consumers and verify the guarantee covers reachable paths.

### ROB-10

Identify who owns release of files/connections/locks; verify that owner's required success and failure paths.

### ROB-11

Trace connection and transaction ownership; verify applicable commit/rollback/release paths, accepting framework-managed lifetimes.

### ROB-12

Check whether discarded errors mask required failure handling, corrupt preparation or falsify tests; intentional safe discards are not defects.

### ROB-13

Check error context supports required diagnosis without conflicting with confidentiality or public error policy.

### ROB-14

Check recovery boundaries against actual failure semantics and ownership; do not require local recovery everywhere.

### ROB-15

Check HTTP/RPC error mapping against declared protocol, compatibility and information policy; internal categories need not always map to distinct public codes.

### ROB-16

Check detached/async result handling by its actual owner; intentionally detached work is valid when required completion/failure/lifecycle obligations are met.

### ROB-17

Check conversions/assertions against reachable values and language guarantees, including precision and type mismatch where applicable.
