# Go

## Purpose and Applicability

Affected behavior depends on Go values, process execution, errors, goroutines, channels or context semantics. Confirm the supported language/version and relevant APIs from actual code and dependency configuration.

## Non-Applicability and False Positives

Do not load this detail for an unrelated extension or package declaration. Existing type, validation, ownership, control flow or framework guarantees may satisfy checks. Do not impose another language's representation or mechanisms.

## Necessary Evidence and Completion

Trace actual values, call/state paths and guarantees into affected consumers. Establish a violated contract and reachable impact for defects, or a current structural benefit and compatibility for maintenance. Record checked paths/evidence and stop when applicable work is complete.

## Checkpoints

### GO-EXEC

os/exec normally passes arguments without a shell. Establish actual shell interpretation or dangerous option semantics and reachable external input before admitting injection; API presence or argument concatenation alone is insufficient.

### GO-CONC

Trace actual goroutine overlap, map/slice ownership, synchronization and initialization guarantees. Check channel blocking/close progress and required context cancellation/exit; immutable or confined state needs no invented locks.

### GO-ERROR

Trace meaningful returned errors and early exits; discarded errors require a concrete failure impact. An underscore discard in a test is not safe if setup failed or the assertion becomes false evidence.

### GO-NIL

Trace actual nil sources, nested pointers, interface dynamic types, collection keys and indexes. Use comma-ok assertions only where an unchecked mismatch is reachable and violates the contract; proven types need no redundant branch.

### GO-RECOVERY

Review panic/recover at the actual failure boundary and owner. Do not demand recovery in every function or treat an impossible panic as reachable.

### GO-NUM

Check integer width, architecture, conversion and overflow using actual values and supported limits, not a hypothetical unbounded environment.

## Conditional Scoring Examples

Use these retained advisory deductions only after substantiating applicability, impact or present maintenance benefit under common.md. Numeric size/count cues prompt inspection; they never independently justify findings, deductions, refactors or defense. Equivalent valid mechanisms are accepted. These examples never assign defect-gate priorities.

**Axis 1 — Idiomatic Clarity & Simplicity**:

- Unnecessary getter/setter on exported struct field: **-5**
- Using `interface{}` / `any` when a concrete type suffices: **-5**
- Not using `errors.New` / `fmt.Errorf` for simple errors: **-3**
- Overly abstract interface with only one implementation: **-5**
- Using `init()` for non-trivial logic: **-8**

**Axis 2 — Correctness & Explicit Contracts**:

- Ignoring returned `error` (assigned to `_`): **-8**
- Missing `fmt.Errorf("...: %w", err)` for error wrapping: **-5**
- Exported function missing doc comment: **-3**
- Naked return in a non-trivial function: **-5**
- `go vet` finding: **-5**

**Axis 3 — Runtime Robustness & Resource Discipline (+ Goroutine & Context Discipline)**:

- Goroutine leak (no exit condition, no context cancellation): **-10**
- Missing `defer` for resource cleanup: **-8**
- Not propagating `context.Context` through call chain: **-8**
- Channel not closed by producer: **-5**
- `sync.Mutex` held across I/O call: **-8**
- Using `fmt.Println` instead of structured logger: **-3**

**Axis 4 — Architecture & Design Integrity**:

- Package with >20 exported symbols (god package): **-5**
- Interface placement that demonstrably couples a consumer to provider-specific implementation details: **-5** (small consumer-side interfaces are idiomatic; location alone does not justify a deduction)
- Circular package dependency: **-10**
- Test depending on external service without build tag: **-5**
