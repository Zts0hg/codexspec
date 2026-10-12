# Rust

## Purpose and Applicability

Rust ownership, borrowing, Result handling, unsafe operations or task/resource lifetimes affect behavior. Confirm the supported language/version and relevant APIs from actual code and dependency configuration.

## Non-Applicability and False Positives

Do not load this detail for an unrelated extension or package declaration. Existing type, validation, ownership, control flow or framework guarantees may satisfy checks. Do not impose another language's representation or mechanisms.

## Necessary Evidence and Completion

Trace actual values, call/state paths and guarantees into affected consumers. Establish a violated contract and reachable impact for defects, or a current structural benefit and compatibility for maintenance. Record checked paths/evidence and stop when applicable work is complete.

## Checkpoints

### RS-OWNERSHIP

Use compiler ownership/borrowing guarantees as contrary evidence. Check unsafe invariants, shared ownership and actual resource/task lifecycle; valid Result discards or unwraps need an evidenced impact before reporting.

## Conditional Scoring Examples

Use these retained advisory deductions only after substantiating applicability, impact or present maintenance benefit under common.md. Numeric size/count cues prompt inspection; they never independently justify findings, deductions, refactors or defense. Equivalent valid mechanisms are accepted. These examples never assign defect-gate priorities.

**Axis 1 — Idiomatic Clarity & Simplicity**:

- Manual loop when iterator chain suffices: **-5**
- Unnecessary `.clone()` when borrowing works: **-8**
- Using `unwrap()` / `expect()` in library code: **-8**
- Not using `?` operator for error propagation: **-5**
- Verbose match when `if let` suffices: **-3**

**Axis 2 — Correctness & Explicit Contracts**:

- Missing error context (no `.context()` / `.map_err()`): **-5**
- Silencing a `Result` with `let _ =`: **-8**
- Public function missing doc comment: **-3**
- `cargo check` error: **-5**
- `cargo clippy` warning: **-3**

**Axis 3 — Runtime Robustness & Resource Discipline (+ Ownership & Borrowing)**:

- Unnecessary `unsafe` block without justification comment: **-10**
- Holding a lock across an `await` point: **-10**
- Leaking `Arc` references (never-decreasing ref count): **-8**
- Missing `Drop` implementation for resource wrapper: **-5**
- Spawning a task without a cancellation mechanism: **-8**

**Axis 4 — Architecture & Design Integrity**:

- God module (>1000 lines): **-5**
- Leaky abstraction exposing internal types in public API: **-8**
- Circular module dependency: **-10**
- Trait with >10 methods (likely needs decomposition): **-5**
