# Assessment of the Supplied Review Checklist

**Assessment Date**: 2026-10-11
**Source**: [Original byte-preserving snapshot](review-dimensions.original.txt)
**Authority**: Analysis supporting NEED-008. The source and this assessment do not independently establish product requirements.

## Inventory

The source contains seven dimensions: logic, business semantics, security, concurrency, robustness, performance, and code quality. It contains 87 bullet items, including five false-positive avoidance items under code quality. Original line references below refer to the snapshot and remain stable while its bytes remain unchanged.

## Language Bindings and Proposed Placement

| Original lines | Language-bound wording | Language-independent intent | Proposed specialized detail |
| --- | --- | --- | --- |
| 45 | `exec.Command`, `os/exec` | Untrusted input must not produce unauthorized process execution or alter dangerous command semantics. | Go process APIs, shell interpretation, argument handling, and executable selection. |
| 68, 71, 74 | goroutine and concurrent `map/slice` access | Concurrent access and task lifetimes must preserve the applicable guarantees. | Go goroutine scheduling, map/slice access, and task termination. |
| 70, 75 | mutex, atomic, channel | Synchronization and communication must avoid races and unintended blocking. | Runtime-specific lock, atomic, and channel semantics when actually used. |
| 81, 89, 121 | nil pointers and panic from nested fields | An invalid or absent value must not reach a use that violates the contract. | Go nil-pointer and interface-value behavior; corresponding nullability semantics in other languages. |
| 82, 83 | slice bounds and map-key presence | Collection access must correctly handle the applicable index or missing-entry behavior. | Per-language collection defaults, failure behavior, and static guarantees. |
| 84, 92, 118 | returned `error`, `_ = err`, empty catch | Required failure information must be consumed or propagated; intentional ignored results need context. | Go returned errors, exception handling, and equivalent result mechanisms. |
| 94 | `panic/recover` | Exceptional failure and recovery must preserve the intended guarantees. | Go panic/recover behavior and equivalent runtime mechanisms where relevant. |
| 97 | type assertion and comma-ok | Runtime conversion or assertion must be safe for reachable inputs and expected semantics. | Go assertion forms and relevant type-conversion rules in other languages. |
| 8, 19, 24, 25, 85 | return paths, equality, string boundaries, map order, integer overflow | Results must satisfy return, equality, text, ordering, and numeric contracts. | Language/runtime semantics only where the affected behavior depends on them. |

Replacing language-specific words without preserving their meaning is insufficient. For example, map missing-key behavior, reference equality, and integer limits differ across languages; their general questions need language-specific interpretation.

## Technical Topics That Are Not Language Identities

| Original lines | Topic | Applicability evidence |
| --- | --- | --- |
| 17, 44, 91, 102 | Database queries, transactions, and caches | Affected read/write paths, transaction boundaries, invalidation, or query execution. |
| 48, 53–63, 95 | HTTP/RPC, authentication, and authorization | Affected request/response behavior, protected actions, identity propagation, and permission decisions. |
| 46, 64, 90 | Filesystem access and uploads | Input-derived paths, file operations, content interpretation, and ownership of resource cleanup. |
| 51, 52 | HTML rendering and server-side outbound requests | Untrusted values reach the relevant rendering or request boundary. |
| 67–76, 96 | Concurrency and background execution | Reachable shared-state access, communication, cancellation, or background result handling. |

These standards may apply in multiple languages. File extensions alone neither activate nor exclude them. Confirmed obligations can activate a check even if its implementation is absent.

## Context-Dependent Rules Requiring Rewording

| Original lines | Risk of an unconditional interpretation | Proposed review question |
| --- | --- | --- |
| 6, 8 | Require every conceivable branch or a return value from every function. | Do reachable paths satisfy the function's actual behavior and return contract? |
| 21 | Report every unused parameter. | Does ignoring the parameter violate an actual caller or interface expectation, accounting for callbacks and compatibility signatures? |
| 25 | Require deterministic ordering from every collection. | Does a caller or public contract require order, and does this implementation satisfy it? |
| 45 | Treat `exec.Command` use with user input as proof of shell injection. | Trace the execution target, arguments, interpreter use, and resulting unauthorized behavior. |
| 46 | Equate path containment with filtering `../`. | Can final path resolution and the file operation escape the authorized boundary? |
| 48 | Require one universal logging and response policy. | Does the actual response expose information that violates the audience's authorized access or the project contract? |
| 49 | Treat password hashing and encryption as interchangeable, or infer safety from function-name search. | Distinguish credential purpose and verify the actual protection across the storage path. |
| 62, 63 | Require personal ownership for every authorized resource operation. | Does the project's permission policy authorize the current subject, action, target, and related resources? |
| 64 | Require content sniffing for every binary upload regardless of use. | Can the accepted content or its later interpretation violate the upload boundary's actual constraints? |
| 70–76 | Require locks or cancellation without establishing concurrent behavior. | Is the relevant access concurrent or the task lifetime unbounded, and which existing mechanisms establish safety? |
| 81–85, 89, 97 | Require repeated null, key, error, overflow, or assertion checks at every use. | Can a violating input reach this use despite existing type, entry, state, and control-flow guarantees? |
| 86–88 | Invent universal range, allowlist, or pagination requirements. | Which valid-input, compatibility, resource, and abuse constraints apply, and where are they enforced? |
| 90, 91 | Assume the reviewed function owns every resource it touches. | Which component owns release or transaction completion, and does every required path fulfill that responsibility? |
| 95 | Require different public status codes for every internal error category. | Does error mapping preserve the declared protocol, compatibility, and information-exposure requirements? |
| 96 | Reject intentionally detached tasks merely because results are not awaited locally. | Does the task's actual owner handle required completion, failure, and lifecycle guarantees? |
| 102–106 | Report allocation, unbuffered I/O, or repeated work without meaningful impact. | Does the actual operation and relevant scale establish a material performance defect? |
| 111–113 | Convert size, duplication counts, or missing constants into automatic merge blockers. | Is there a demonstrated behavior defect or binding violation, or only a maintenance suggestion? |
| 118 | Exempt ignored errors solely because the file is a test. | Does ignoring the error mask failed preparation, invalidate the assertion, or falsely pass the test? |
| 120 | Require a uniquely correct implementation before reporting a defect. | Is behavior demonstrably wrong or a binding rule violated, independently of how many valid implementations exist? |

## Evidence Supporting the Corrections

- Go's process package intentionally does not invoke a shell by default; API presence alone cannot establish shell injection. See [Go `os/exec` documentation](https://pkg.go.dev/os/exec#pkg-overview).
- Authorization evaluates permissions for a subject and action under a policy; ownership is only one possible relationship. See [OWASP Authorization Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html).
- Password verification storage normally uses suitable password hashing rather than treating reversible encryption as an equivalent choice. See [OWASP Password Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html).

## Integration and Validation Guidance

Preserve the source item's review intent while making its applicability and finding evidence explicit. The complete original-to-standard mapping belongs to implementation preparation and must account for all 87 items. Combine duplicate review questions with links to their source items rather than silently losing intent.

Common false-positive avoidance belongs in shared review discipline. Language-specific illustrations belong in the appropriate subchecklists. Source prose, comments, API names, and numeric style thresholds are investigation evidence rather than authority to invent product contracts.

Use paired behavior cases to verify both discovery and restraint: a real input that bypasses an alleged guarantee must trigger the relevant check, while a guarantee proven to cover all affected paths must prevent a speculative finding. Other useful cases include missing required authorization, late discovery of an unchanged cross-language dependency, optional collection ordering, safe direct argument passing, and intentionally detached work with a valid owner.

Default change review now includes substantiated maintenance suggestions, and the implementation workflow automatically applies incremental improvements by default under NEED-009, NEED-010, and DEC-004 in [requirements.md](../requirements.md). They remain distinguishable from actual defects; the switch controls application rather than whether maintenance is assessed. DEC-009 confirms persistent configuration through `codexspec config --auto-maintenance on|off`. The separate version-1 maintenance companion is defined in [design.md](../design.md), resolving the non-blocking representation question OPEN-002. The former audit-only proposal OPEN-001 is superseded.
