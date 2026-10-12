# Common Review Discipline

## Purpose and Applicability

Read this file for every review, together with the selected mode procedure. It governs review direction, evidence, applicability, false-positive avoidance and completion. The source checklist supplies investigation questions; only confirmed requirements, recognized project constraints, actual semantics and compatibility contracts establish obligations.

## Establish Direction

Account for every selected change. Identify affected behavior, entry points, expected outcomes, contracts, producers, consumers, state changes and external boundaries before detailed checking. Prioritize concrete impact and risk. Reading all files does not establish behavior coverage.

Trace normal paths and evidenced failure, denial, cancellation, recovery and compatibility paths. Read relevant unchanged callers/dependencies. For a verified repeatable cause, inspect justified equivalent and symmetric occurrences within a bounded affected scope.

## Select Standards

1. Read only the lightweight index, this file and the selected mode initially.
2. Build the affected behavior/contract map from confirmed requirements, project constraints and selected evidence.
3. Briefly assess **every dimension**: applicable with trigger/scope, not applicable with reason, or uncertain with a bounded inspection needed.
4. Load detailed dimension and language/framework sections only where actual semantics, versions, input sources, calls/data flows or dependencies justify them. Extensions and keywords identify candidates, not applicability.
5. For uncertain applicability inspect directly relevant callers, inputs, runtime guarantees and dependency configuration. Report a gap only when necessary evidence for a concrete obligation or material risk remains unavailable.
6. Expand selection when tracing reveals relevant unchanged or cross-language boundaries. Missing required implementation still activates its standard; code-presence detection cannot excuse omitted requirements.
7. Record selected standard IDs/sections, rationale, relevant scope, evidence and completion, plus reasons for dimension exclusions and exact selected-resource digests for safe incremental reuse. The change-review records store keeps this in `standards.json`; summarize it in Scope.

Assessing all dimensions does not mean reading every detailed body. Do not label inapplicable questions as unverified defects. A selected required standard that cannot be read is a visible material gap, not silently skipped work.

## Admit Evidence, Check Guarantees

For a defect establish actual operating context, triggering-condition origin, a reachable path, violated contract/behavior, concrete impact and attribution to the selected change. Reproduce it or provide a deterministic code argument. Rare credible failure and malicious external input remain relevant.

Before reporting, check contrary evidence: upstream validation, types, state/order guarantees, framework/library behavior, resource ownership and recovery. Verify the guarantee covers the relevant path. Require an actual reachable bypass before adding defense. Never turn inability to prove absolute safety into a defect or mandatory verification campaign.

Separate evidenced defects, material missing verification and unsupported speculation. Only missing necessary evidence for an applicable obligation or material risk blocks completion. Reject unsupported assumptions; do not repeatedly convert them into repairs.

## Maintenance Assessment

Always assess and report substantiated readability, maintainability and extensibility improvements in default change review, regardless of automatic-application configuration. Limit them to selected changes and directly affected structure.

A pure maintenance suggestion states the present problem, concrete improvement, current benefit and compatibility evidence; it need not claim a functional failure. Preserve actual requirements and conventions. A style preference, size/count threshold, imagined future extension or generic “more defensive” suggestion is insufficient.

The reviewer remains read-only. A repair caller reads `workflow.auto_maintenance` and owns edits. Disabling application never suppresses suggestions, defects or necessary verification. Do not promote maintenance to P0–P3 merely to force application.

## False-Positive Avoidance

- **FP-01 — Framework conventions**: verify actual library guarantees before treating unusual patterns as failures.
- **FP-02 — Test simplification**: ignored errors are acceptable only when they do not invalidate preparation, execution or assertions; test filenames are not blanket exemptions.
- **FP-03 — Commented code**: report only lost required behavior or substantiated current maintenance cost, not comments themselves.
- **FP-04 — Style differences**: multiple valid implementations are permitted; a defect depends on behavior/obligations, and maintenance depends on current benefit.
- **FP-05 — Absent-value claims**: require an actual null/absence source and reachable propagation; “might be empty” without evidence is speculation.

Nullability, missing keys, ordering, numeric limits, ignored results and recovery are evaluated against actual language semantics and contracts. Do not impose one language's representation or mechanism on another. Authentication, transactions, uploads and similar themes are technical topics, not language identities.

## Verification Safety

Use project/feature instructions, existing CI/check entry points, then relevant standard tools. Inspect command definitions and flags before execution. Checks are read-only: no dependency installation/update, lock rewriting, formatting in write mode, migrations, publication, Git mutation or repair commands.

Redirect caches/reports outside the repository. If writes cannot be excluded, use a disposable exact-state mirror with independent Git metadata and copied dependencies; imports/executables must resolve inside it. Otherwise report the necessary check unavailable. Do not infer change attribution from an unrelated environment failure.

## Completion

Complete applicable behavior/contracts, relevant risks, deterministic verification and justified related-occurrence work. Record completion and key evidence. Stop once applicable obligations are complete; expand only for new evidenced dependencies, risks or relevant present maintenance needs.

Repair callers complete substantiated incremental maintenance when enabled, preserve intended behavior and public compatibility, and verify edits. Disabled suggestions remain visible without mandatory application. Neither defect fixes nor maintenance justify unsupported product requirements, unnecessary defensive layers/abstractions or unrelated repository-wide cleanup.

Scoring examples and size/count cues never independently establish findings or deductions. Apply common evidence/benefit rules before the selected mode's severity/scoring rules.
