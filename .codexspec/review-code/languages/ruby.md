# Ruby

## Purpose and Applicability

Ruby values, exception boundaries, Enumerable behavior or thread/resource ownership affects behavior. Confirm the supported language/version and relevant APIs from actual code and dependency configuration.

## Non-Applicability and False Positives

Do not load this detail for an unrelated extension or package declaration. Existing type, validation, ownership, control flow or framework guarantees may satisfy checks. Do not impose another language's representation or mechanisms.

## Necessary Evidence and Completion

Trace actual values, call/state paths and guarantees into affected consumers. Establish a violated contract and reachable impact for defects, or a current structural benefit and compatibility for maintenance. Record checked paths/evidence and stop when applicable work is complete.

## Checkpoints

### RB-SEMANTICS

Check actual truthiness, exception class boundaries, mutable shared objects and resource/thread owners. Library idioms and optional type tooling require project applicability, not universal adoption.

## Conditional Scoring Examples

Use these retained advisory deductions only after substantiating applicability, impact or present maintenance benefit under common.md. Numeric size/count cues prompt inspection; they never independently justify findings, deductions, refactors or defense. Equivalent valid mechanisms are accepted. These examples never assign defect-gate priorities.

**Axis 1 — Idiomatic Clarity & Simplicity**:

- Verbose loop when `map` / `select` / `each_with_object` suffices: **-3**
- Not using Ruby's built-in `Enumerable` methods: **-5**
- Using `and` / `or` instead of `&&` / `||` for control flow: **-5**
- Monkey-patching core classes without compelling reason: **-8**
- Method exceeding 20 lines: **-5**

**Axis 2 — Correctness & Explicit Contracts**:

- Rescuing `Exception` instead of `StandardError`: **-8**
- Silencing exceptions with empty `rescue`: **-8**
- Missing `freeze` on string constants: **-3**
- No input validation in public methods: **-5**
- Missing Sorbet/RBS type signatures on public API (if project uses them): **-3**

**Axis 3 — Runtime Robustness & Resource Discipline**:

- File opened without block form (`File.open` without block): **-8**
- Using `Thread.new` without join/exception handling: **-8**
- `puts` / `p` instead of logger: **-3**
- Missing `ensure` block for cleanup: **-5**
- Global variable mutation: **-8**

**Axis 4 — Architecture & Design Integrity**:

- God class (>300 lines): **-5**
- Circular `require`: **-10**
- Service object without clear single responsibility: **-5**
- Missing dependency injection (hard-coded class references): **-5**
