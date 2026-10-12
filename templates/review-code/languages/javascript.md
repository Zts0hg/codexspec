# JavaScript

## Purpose and Applicability

JavaScript runtime values, coercion, collections, async work or module behavior affects the change. Confirm the supported language/version and relevant APIs from actual code and dependency configuration.

## Non-Applicability and False Positives

Do not load this detail for an unrelated extension or package declaration. Existing type, validation, ownership, control flow or framework guarantees may satisfy checks. Do not impose another language's representation or mechanisms.

## Necessary Evidence and Completion

Trace actual values, call/state paths and guarantees into affected consumers. Establish a violated contract and reachable impact for defects, or a current structural benefit and compatibility for maintenance. Record checked paths/evidence and stop when applicable work is complete.

## Checkpoints

### JS-VALUES

Check null/undefined, coercion, equality, property access and ordering against actual producers and contracts. Do not infer TypeScript guarantees for untyped runtime inputs.

### JS-ASYNC

Trace required Promise rejection handling and lifecycle ownership of events, timers and background work. Existing owners can provide cleanup; local handling is not universal.
