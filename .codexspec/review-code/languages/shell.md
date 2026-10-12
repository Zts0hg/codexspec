# Shell

## Purpose and Applicability

Affected Bash, Zsh or POSIX shell syntax interprets data or controls processes/resources. Confirm the supported language/version and relevant APIs from actual code and dependency configuration.

## Non-Applicability and False Positives

Do not load this detail for an unrelated extension or package declaration. Existing type, validation, ownership, control flow or framework guarantees may satisfy checks. Do not impose another language's representation or mechanisms.

## Necessary Evidence and Completion

Trace actual values, call/state paths and guarantees into affected consumers. Establish a violated contract and reachable impact for defects, or a current structural benefit and compatibility for maintenance. Record checked paths/evidence and stop when applicable work is complete.

## Checkpoints

### SH-EXEC

Trace expansion, quoting, option parsing, pipelines, exit status and cleanup under the actual shell/version. set -euo pipefail is not a universal requirement or guarantee; equivalent explicit handling can be correct.

## Conditional Scoring Examples

Use these retained advisory deductions only after substantiating applicability, impact or present maintenance benefit under common.md. Numeric size/count cues prompt inspection; they never independently justify findings, deductions, refactors or defense. Equivalent valid mechanisms are accepted. These examples never assign defect-gate priorities.

**Axis 1 — Idiomatic Clarity & Simplicity**:

- Using `expr` or backticks when `$((...))` / `$()` works: **-3**
- Parsing `ls` output instead of using globs: **-8**
- Using `cat file | cmd` when `cmd < file` suffices (useless use of cat): **-3**
- Not using `local` for function variables: **-5**
- Hardcoded paths instead of variables/parameters: **-3**

**Axis 2 — Correctness & Explicit Contracts**:

- Unquoted variable expansion (`$var` instead of `"$var"`): **-8**
- Missing `shellcheck` directive acknowledgment for intentional behavior: **-3**
- No input validation for script arguments: **-5**
- Using `test` / `[` when `[[` provides safer semantics: **-3**
- `shellcheck` finding: **-5**

**Axis 3 — Runtime Robustness & Resource Discipline (+ Execution Safety)**:

- Missing `set -euo pipefail` (or equivalent): **-10**
- No `trap` for cleanup on exit/error: **-8**
- Temporary files without `mktemp` and cleanup: **-8**
- Command injection risk via unvalidated input in eval/command substitution: **-10**
- Using `kill -9` without trying graceful shutdown first: **-3**

**Axis 4 — Architecture & Design Integrity**:

- Script exceeding 300 lines without function decomposition: **-5**
- No usage/help message for scripts accepting arguments: **-3**
- Mixed concerns (deployment + configuration + monitoring in one script): **-8**
- Missing exit codes documentation: **-3**
