# Python

## Purpose and Applicability

Python objects, exceptions, collections, context managers or asynchronous tasks participate in affected behavior. Confirm the supported language/version and relevant APIs from actual code and dependency configuration.

## Non-Applicability and False Positives

Do not load this detail for an unrelated extension or package declaration. Existing type, validation, ownership, control flow or framework guarantees may satisfy checks. Do not impose another language's representation or mechanisms.

## Necessary Evidence and Completion

Trace actual values, call/state paths and guarantees into affected consumers. Establish a violated contract and reachable impact for defects, or a current structural benefit and compatibility for maintenance. Record checked paths/evidence and stop when applicable work is complete.

## Checkpoints

### PY-VALUES

Check absent values, dictionary-key behavior and mutable defaults using actual producer/type/entry guarantees. Missing keys can be intentional; comprehension/style alternatives are maintenance only with current benefit.

### PY-ERRORS

Trace exceptions, return values, preparation and cleanup. Broad catches can be intentional boundaries; require evidence of masked failure or lost context. Context managers are one valid ownership mechanism.

### PY-ASYNC

Check blocking work, task ownership, cancellation and cleanup only on affected async paths; standard-library or framework guarantees can satisfy the obligation.

## Conditional Scoring Examples

Use these retained advisory deductions only after substantiating applicability, impact or present maintenance benefit under common.md. Numeric size/count cues prompt inspection; they never independently justify findings, deductions, refactors or defense. Equivalent valid mechanisms are accepted. These examples never assign defect-gate priorities.

**Axis 1 — Idiomatic Clarity & Simplicity**:

- Unnecessary class when a function suffices: **-8**
- Missed `pathlib` / `itertools` / `collections` opportunity: **-5**
- Manual iteration instead of comprehension or generator expression: **-3**
- Mutable default argument (`def f(x=[])`): **-8**
- `dict[key]` without guard when `dict.get()` is appropriate: **-3**

**Axis 2 — Correctness & Explicit Contracts**:

- Public function missing type annotations: **-5**
- Bare `except:` or `except Exception:` without re-raise: **-8**
- Missing `raise ... from err` context: **-3**
- `mypy` error: **-5**
- Overly broad `Optional` when a more specific Union applies: **-3**

**Axis 3 — Runtime Robustness & Resource Discipline**:

- File/connection opened without `with` context manager: **-8**
- `print()` instead of `logging`: **-3**
- Blocking call in async context: **-10**
- Incorrect log level usage: **-3**
- `ruff` violation: **-3**

**Axis 4 — Architecture & Design Integrity**:

- God function (>50 lines of logic without clear structure): **-5**
- Circular import: **-10**
- Hard-coded dependency that should be injected: **-5**
- Module mixing I/O and pure computation: **-5**
