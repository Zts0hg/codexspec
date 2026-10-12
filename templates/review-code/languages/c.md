# C

## Purpose and Applicability

C pointers, buffers, lifetime, conversion, memory or concurrency behavior is affected. Confirm the supported language/version and relevant APIs from actual code and dependency configuration.

## Non-Applicability and False Positives

Do not load this detail for an unrelated extension or package declaration. Existing type, validation, ownership, control flow or framework guarantees may satisfy checks. Do not impose another language's representation or mechanisms.

## Necessary Evidence and Completion

Trace actual values, call/state paths and guarantees into affected consumers. Establish a violated contract and reachable impact for defects, or a current structural benefit and compatibility for maintenance. Record checked paths/evidence and stop when applicable work is complete.

## Checkpoints

### C-MEMORY

Trace actual pointer/buffer origins, lengths, allocation failures, ownership and release. Check reachable overflow, dangling/use-after-free and races; absent redundant checks are not defects when proven invariants cover the path.

## Conditional Scoring Examples

Use these retained advisory deductions only after substantiating applicability, impact or present maintenance benefit under common.md. Numeric size/count cues prompt inspection; they never independently justify findings, deductions, refactors or defense. Equivalent valid mechanisms are accepted. These examples never assign defect-gate priorities.

**Axis 1 — Idiomatic Clarity & Simplicity**:

- (C) Magic numbers without named constants: **-3**
- Overly complex macro when `inline` function or `constexpr` works: **-5**

**Axis 2 — Correctness & Explicit Contracts**:

- Missing `const` correctness on parameters/methods: **-5**
- Unchecked return value from system call / allocation: **-8**
- Missing bounds checking on array/buffer access: **-8**
- Implicit conversion that may lose data: **-5**

**Axis 3 — Runtime Robustness & Resource Discipline (+ Memory & Lifetime Safety)**:

- `malloc` without corresponding `free`: **-10**
- Buffer overflow risk (e.g., `strcpy` instead of `strncpy` or `snprintf`): **-10**
- Use-after-free or dangling pointer: **-10**
- Missing null check after allocation: **-5**
- Data race (shared mutable state without synchronization): **-10**

**Axis 4 — Architecture & Design Integrity**:

- Header file exposing implementation details: **-5**
- Circular `#include` dependency: **-10**
- (C) Module with >50 public functions: **-5**
