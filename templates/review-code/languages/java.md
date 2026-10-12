# Java

## Purpose and Applicability

Java types, exceptions, synchronization or resource lifetimes are implicated. Confirm the supported language/version and relevant APIs from actual code and dependency configuration.

## Non-Applicability and False Positives

Do not load this detail for an unrelated extension or package declaration. Existing type, validation, ownership, control flow or framework guarantees may satisfy checks. Do not impose another language's representation or mechanisms.

## Necessary Evidence and Completion

Trace actual values, call/state paths and guarantees into affected consumers. Establish a violated contract and reachable impact for defects, or a current structural benefit and compatibility for maintenance. Record checked paths/evidence and stop when applicable work is complete.

## Checkpoints

### JAVA-SEMANTICS

Evaluate nullability, collections, checked/unchecked exceptions, initialization, synchronization and resource ownership using actual Java/version and framework guarantees. Kotlin-specific operators or coroutine rules do not apply merely because this file is loaded.

## Conditional Scoring Examples

Use these retained advisory deductions only after substantiating applicability, impact or present maintenance benefit under common.md. Numeric size/count cues prompt inspection; they never independently justify findings, deductions, refactors or defense. Equivalent valid mechanisms are accepted. These examples never assign defect-gate priorities.

**Axis 1 — Idiomatic Clarity & Simplicity**:

- (Java) Verbose stream chain when a simple loop is clearer: **-3**
- (Java) Not using `var` (Java 10+) for obvious local types: **-3**
- Unnecessary wrapper class / design pattern ceremony: **-5**

**Axis 2 — Correctness & Explicit Contracts**:

- (Java) Catching `Exception` or `Throwable` broadly: **-8**
- (Java) Returning `null` from a method that should return `Optional`: **-5**
- Missing `@Nullable` / `@NonNull` annotations (Java): **-3**
- Ignoring checked exception without logging: **-8**

**Axis 3 — Runtime Robustness & Resource Discipline**:

- Owned resource left unclosed instead of try-with-resources or equivalent correct cleanup: **-8**
- Thread created without a managed executor or equivalent lifecycle ownership: **-8**
- Missing structured concurrency or equivalent lifetime control (orphan threads): **-8**
- `System.out.println` instead of logger: **-3**

**Axis 4 — Architecture & Design Integrity**:

- God class (>500 lines): **-5**
- Circular package dependency: **-10**
- Service depending directly on implementation instead of interface: **-5**
- Missing dependency injection (hard-coded `new`): **-5**
