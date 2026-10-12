# Swift

## Purpose and Applicability

Affected behavior depends on Swift values, optionals, resources or asynchronous ownership. Confirm the supported language/version and relevant APIs from actual code and dependency configuration.

## Non-Applicability and False Positives

Do not load this detail for an unrelated extension or package declaration. Existing type, validation, ownership, control flow or framework guarantees may satisfy checks. Do not impose another language's representation or mechanisms.

## Necessary Evidence and Completion

Trace actual values, call/state paths and guarantees into affected consumers. Establish a violated contract and reachable impact for defects, or a current structural benefit and compatibility for maintenance. Record checked paths/evidence and stop when applicable work is complete.

## Checkpoints

### SW-SEMANTICS

Check actual optional/value sources, error handling and resource/task ownership. Existing type and lifecycle guarantees can satisfy checks; unsupported runtime assumptions require bounded inspection.
