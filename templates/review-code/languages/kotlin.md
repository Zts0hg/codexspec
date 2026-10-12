# Kotlin

## Purpose and Applicability

Kotlin types, Java interop, coroutines or resource lifetimes are implicated. Confirm the supported language/version and relevant APIs from actual code and dependency configuration.

## Non-Applicability and False Positives

Do not load this detail for an unrelated extension or package declaration. Existing type, validation, ownership, control flow or framework guarantees may satisfy checks. Do not impose another language's representation or mechanisms.

## Necessary Evidence and Completion

Trace actual values, call/state paths and guarantees into affected consumers. Establish a violated contract and reachable impact for defects, or a current structural benefit and compatibility for maintenance. Record checked paths/evidence and stop when applicable work is complete.

## Checkpoints

### KT-SEMANTICS

Check nullable/platform types, assertions, coroutine ownership/cancellation and cleanup under the actual Kotlin/interop/framework contracts. Java-only idiom preferences are not mandatory Kotlin behavior.

## Conditional Scoring Examples

Use these retained advisory deductions only after substantiating applicability, impact or present maintenance benefit under common.md. Numeric size/count cues prompt inspection; they never independently justify findings, deductions, refactors or defense. Equivalent valid mechanisms are accepted. These examples never assign defect-gate priorities.

**Axis 1 — Idiomatic Clarity & Simplicity**:

- (Kotlin) Using Java-style null checks instead of `?.` / `?:`: **-5**
- (Kotlin) Using `!!` (non-null assertion) without justification: **-8**
- Unnecessary wrapper class / design pattern ceremony: **-5**

**Axis 2 — Correctness & Explicit Contracts**:

- (Kotlin) Exposed mutable collection (`MutableList` in public API): **-5**
- Java interop only: missing required nullability information on a Java API consumed by Kotlin (`@Nullable` / `@NonNull` or equivalent): **-3**
- Java interop only: ignoring a declared Java exception when the established error contract requires handling or reporting: **-8**

**Axis 3 — Runtime Robustness & Resource Discipline**:

- Owned resource left unclosed instead of `.use {}` or equivalent correct cleanup: **-8**
- Thread created without executor service / coroutine: **-8**
- (Kotlin) Blocking call inside coroutine without `withContext(Dispatchers.IO)`: **-10**
- Missing structured concurrency (orphan threads/coroutines): **-8**
- `System.out.println` instead of logger: **-3**

**Axis 4 — Architecture & Design Integrity**:

- God class (>500 lines): **-5**
- Circular package dependency: **-10**
- Service depending directly on implementation instead of interface: **-5**
- Missing dependency injection (hard-coded constructor calls): **-5**
