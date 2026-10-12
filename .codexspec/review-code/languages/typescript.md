# TypeScript

## Purpose and Applicability

TypeScript type narrowing, runtime values, async work or module behavior affects the change. Confirm the supported language/version and relevant APIs from actual code and dependency configuration.

## Non-Applicability and False Positives

Do not load this detail for an unrelated extension or package declaration. Existing type, validation, ownership, control flow or framework guarantees may satisfy checks. Do not impose another language's representation or mechanisms.

## Necessary Evidence and Completion

Trace actual values, call/state paths and guarantees into affected consumers. Establish a violated contract and reachable impact for defects, or a current structural benefit and compatibility for maintenance. Record checked paths/evidence and stop when applicable work is complete.

## Checkpoints

### TS-VALUES

Check runtime origins despite static types, narrowing/assertions and required discriminated-union cases. Compile-time constraints that cover a path can exclude imagined values.

### TS-ASYNC

Trace Promise rejection, cancellation, event/timer ownership and actual cleanup requirements. Do not mandate AbortController or local catch for every operation.

## Conditional Scoring Examples

Use these retained advisory deductions only after substantiating applicability, impact or present maintenance benefit under common.md. Numeric size/count cues prompt inspection; they never independently justify findings, deductions, refactors or defense. Equivalent valid mechanisms are accepted. These examples never assign defect-gate priorities.

**Axis 1 — Idiomatic Clarity & Simplicity**:

- Using `any` instead of a proper type: **-8**
- Unnecessary type assertion (`as`) when narrowing suffices: **-5**
- Verbose `if/else` when nullish coalescing (`??`) or optional chaining (`?.`) applies: **-3**
- Not using `const` for immutable bindings: **-3**
- Redundant type annotation where inference is sufficient: **-3**

**Axis 2 — Correctness & Explicit Contracts**:

- Missing return type annotation on exported function: **-5**
- `tsc` error (strict mode): **-5**
- Unchecked `.data` access on API response without validation: **-8**
- Empty catch block swallowing errors: **-8**
- Missing discriminated union exhaustiveness check: **-5**

**Axis 3 — Runtime Robustness & Resource Discipline**:

- Unhandled Promise rejection (missing `.catch()` or `try/catch`): **-8**
- Event listener added without cleanup/removal: **-8**
- ESLint violation: **-3**
- `setTimeout`/`setInterval` without cleanup: **-5**
- Missing `AbortController` for cancellable fetch: **-5**

**Axis 4 — Architecture & Design Integrity**:

- Barrel file re-exporting everything (tree-shaking killer): **-5**
- Circular dependency between modules: **-10**
- Business logic in UI layer: **-8**
- God file (>500 lines): **-5**
