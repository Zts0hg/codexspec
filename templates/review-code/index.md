# Review Standards Index

Read this lightweight index, common.md and the selected mode procedure first. Detailed files are read only when actual behavior or binding obligations activate them. Use common.md for selection, bounded uncertain inspection, late expansion, evidence and completion rules. Paths are relative to the selected resource root; never mix roots or versions.

## Mandatory Discipline and Selected Mode

| ID | Path | Load condition |
|----|------|----------------|
| COMMON | common.md | Every review |
| CHANGE | change-review.md | Default selected Git-change review |
| QUALITY | quality-assessment.md | Explicit --audit quality assessment only |

## Dimensions

Briefly assess every row; do not read every detailed body merely to make that assessment. An absent required implementation can activate a dimension. Mark inapplicable dimensions with reasons; uncertainty prompts bounded inspection, not automatic defects.

| ID | Path | Applicable when | Do not activate merely because |
|----|------|-----------------|-------------------------------|
| LOG | dimensions/logic.md | Affected control flow, value propagation, parsing, time, ordering or shared data contracts. | A keyword, hypothetical input or generic style cue exists |
| BUS | dimensions/business-semantics.md | Confirmed domain preconditions, status transitions, identity, limits or result contracts are affected. | A keyword, hypothetical input or generic style cue exists |
| SEC | dimensions/security.md | Protected operations, untrusted inputs, credentials, sensitive data or external side effects are affected. | A keyword, hypothetical input or generic style cue exists |
| CON | dimensions/concurrency.md | Mutable state, initialization, asynchronous work, synchronization or check/use operations can overlap. | A keyword, hypothetical input or generic style cue exists |
| ROB | dimensions/robustness.md | Input boundaries, fallible operations, conversions, resources or failure/recovery behavior are affected. | A keyword, hypothetical input or generic style cue exists |
| PER | dimensions/performance.md | Actual operation frequency, data volume, latency or resource budgets make selected behavior consequential. | A keyword, hypothetical input or generic style cue exists |
| MAI | dimensions/maintainability.md | Selected changes or directly affected structure have a substantiated current readability, maintenance or extension problem. | A keyword, hypothetical input or generic style cue exists |

## Language and Framework Detail

Select actual semantics and versions from affected traces. Dependencies discovered in unchanged or cross-language implementations may activate additional detail; extensions/packages alone do not establish applicability.

| ID | Path | Load condition |
|----|------|----------------|
| LANG-PYTHON | languages/python.md | Python objects, exceptions, collections, context managers or asynchronous tasks participate in affected behavior. |
| LANG-TYPESCRIPT | languages/typescript.md | TypeScript type narrowing, runtime values, async work or module behavior affects the change. |
| LANG-JAVASCRIPT | languages/javascript.md | JavaScript runtime values, coercion, collections, async work or module behavior affects the change. |
| LANG-GO | languages/go.md | Affected behavior depends on Go values, process execution, errors, goroutines, channels or context semantics. |
| LANG-RUST | languages/rust.md | Rust ownership, borrowing, Result handling, unsafe operations or task/resource lifetimes affect behavior. |
| LANG-SHELL | languages/shell.md | Affected Bash, Zsh or POSIX shell syntax interprets data or controls processes/resources. |
| LANG-JAVA | languages/java.md | Java types, exceptions, synchronization or resource lifetimes are implicated. |
| LANG-KOTLIN | languages/kotlin.md | Kotlin types, Java interop, coroutines or resource lifetimes are implicated. |
| LANG-RUBY | languages/ruby.md | Ruby values, exception boundaries, Enumerable behavior or thread/resource ownership affects behavior. |
| LANG-C | languages/c.md | C pointers, buffers, lifetime, conversion, memory or concurrency behavior is affected. |
| LANG-CPP | languages/cpp.md | C++ ownership, object lifetime, buffers, conversion or concurrency behavior is affected. |
| LANG-CSHARP | languages/csharp.md | Affected behavior depends on C# values, exceptions, resources or asynchronous ownership. |
| LANG-SWIFT | languages/swift.md | Affected behavior depends on Swift values, optionals, resources or asynchronous ownership. |
| LANG-PHP | languages/php.md | Affected behavior depends on PHP values, conversions, requests or resource/error handling. |
| FRAMEWORK-REACT | frameworks/react.md | React components/hooks/effects/rendering or lifecycle participates in affected behavior |

## Extension and Splitting Policy

New standards supply purpose, applicability/non-applicability, concrete checkpoints, evidence, common false positives and completion. Add a short index row, not its body. Preserve defect admission, maintenance assessment and completion rules. Keep technical topics as sections initially; split only a substantial independent theme that repeatedly causes unrelated content loading. Do not use arbitrary line counts or create per-checkpoint files.
