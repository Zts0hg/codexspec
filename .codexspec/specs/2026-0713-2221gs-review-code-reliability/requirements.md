# Confirmed Requirements: review-code-reliability

<!--
Language: Maintain this document in the language specified in .codexspec/config.yml.
This file is the authoritative, persistent record of user-confirmed intent.
Do not copy the full conversation. Keep only confirmed decisions and short evidence
quotes needed to resolve later interpretation disputes.
-->

**Feature ID**: `2026-0713-2221gs`
**Status**: Confirmed
**Last Confirmed**: 2026-07-14 20:58 CST

## Authority Rules

- Only entries with `Status: confirmed` are binding downstream inputs.
- `open` entries MUST NOT be converted into confirmed product requirements.
- Replaced entries remain in this file with `Status: superseded` and a link to the replacement.
- AI inferences must be labeled as assumptions and require user confirmation before becoming binding.

## Needs

### NEED-001: Reliable review-code defect detection

- **Status**: confirmed
- **Statement**: Improve the `review-code` command so it is materially less likely to miss actionable defects in implemented changes.
- **Rationale**: The existing broad quality-review design produced a complete-looking report while missing defects that were subsequently found during repeated change reviews.
- **User Evidence**: The user requested that CodexSpec's `review-code` design be checked and optimized based on the prior FoxHarness review-code miss analysis.
- **Confirmed At**: 2026-07-13 22:44 CST

### NEED-002: Requirements-aware defect review

- **Status**: confirmed
- **Statement**: When a review can identify the relevant CodexSpec feature artifacts, it must use them to assess implementation conformance and, when the complete feature delta is selected, requirements completeness.
- **Rationale**: Code can be internally correct while omitting or contradicting confirmed behavior, so code-only inspection cannot establish feature readiness.
- **User Evidence**: The user confirmed the mode-target-context model in which `--feature` supplies requirements context independently of the selected Git target.
- **Confirmed At**: 2026-07-13 23:20 CST

## Constraints

### CON-001: Product requirements remain source-independent

- **Status**: confirmed
- **Statement**: Persist required CodexSpec behavior and boundaries, but do not persist external implementation-research details as product requirements.
- **User Evidence**: The user confirmed that requirements and downstream artifacts describe only CodexSpec behavior and do not retain external source paths, symbols, or replication constraints.

### CON-002: Review quality takes priority over speed

- **Status**: confirmed
- **Statement**: Defect-gate design and completion decisions prioritize review quality and evidence completeness over latency or token cost. Necessary review stages, verification, inventory, and specialist coverage cannot be skipped to produce a faster PASS.
- **User Evidence**: The user explicitly stated that review quality takes priority over review speed.

## Decisions

### DEC-001: Default review-code positioning

- **Status**: confirmed
- **Decision**: The default `review-code` behavior is a change-scoped pre-merge defect gate. Its primary output is actionable findings and a patch-correctness verdict. Whole-path quality scoring remains available only through an explicit audit capability and is not the default merge gate.
- **Alternatives Rejected**: Keeping the existing whole-path, multi-dimension quality scorecard as the default review and merge gate; combining defect gating and quality scoring unconditionally in every review.
- **Reason**: Diff-focused defect detection keeps reviewer attention on regressions introduced by the current change, while broad scoring can conceal blocking defects behind an aggregate passing score.
- **User Evidence**: The user explicitly confirmed: "default change-scoped defect gate, existing path-level quality scoring retained only as an explicit audit capability."

### DEC-002: Default change-review scope

- **Status**: confirmed
- **Decision**: On a feature branch, the default defect-gate target is the complete feature delta relative to the merge base with its base branch. The target includes changes committed on the feature branch, staged changes, unstaged changes, and untracked files. On the base branch, the default target is all uncommitted changes. Callers can explicitly select all uncommitted changes or one commit instead.
- **Alternatives Rejected**: Reviewing only staged changes by default; reviewing only the current working-tree Changes area by default; reviewing only committed branch changes by default.
- **Reason**: A pre-merge gate must cover everything that can be delivered with the feature and must not omit already committed or not-yet-staged implementation work.
- **User Evidence**: The user confirmed that the default checks the complete branch difference, including committed, staged, and current changes, with alternatives to review only uncommitted changes or one commit.

### DEC-003: Explicit committed-only review target

- **Status**: confirmed
- **Decision**: `review-code --committed` reviews only the changes committed on the current feature branch relative to the merge base with its base branch, excluding staged, unstaged, and untracked changes. `--base <branch>` overrides the base branch for the default complete-feature target or the committed-only target. The primary target selectors `--committed`, `--uncommitted`, and `--commit <sha>` are mutually exclusive; `--base` is a modifier rather than a separate target.
- **Alternatives Rejected**: Treating committed-only review as indistinguishable from the default complete-feature review; overloading `--commit` to represent the accumulated current-branch delta.
- **Reason**: Reviewing one commit and reviewing all commits accumulated on a feature branch are distinct operations and need unambiguous selectors.
- **User Evidence**: The user explicitly confirmed the proposed `--committed` and `--base` behavior.

### DEC-004: Git-first base-branch resolution

- **Status**: confirmed
- **Decision**: When `--base` is omitted, `review-code` resolves the repository's default branch from Git metadata. It first uses the selected remote's local symbolic `HEAD`, may then perform a read-only remote `HEAD` query, and finally checks conventional remote and local refs in the order `origin/main`, `origin/master`, `main`, and `master`. If no unique base can be determined, the review fails with an actionable request for `--base`. The review reports the selected base ref and merge-base SHA.
- **Alternatives Rejected**: Adding a persistent `review.base_branch` setting; silently falling back to uncommitted-only review; automatically fetching or mutating Git refs.
- **Reason**: The default should follow repository Git metadata without introducing configuration burden or hidden repository-state changes, while an uncertain base must never produce a misleading clean result.
- **User Evidence**: The user confirmed Git-first default-branch detection, no new base-branch configuration, and no implicit fetch.

### DEC-005: Explicit quality-audit mode

- **Status**: confirmed
- **Decision**: `review-code`, `review-code --committed`, `review-code --uncommitted`, and `review-code --commit <sha>` are change-scoped defect-gate invocations. Only `review-code --audit [paths...]` invokes the whole-path quality audit and scoring behavior. Audit mode examines complete current file contents, can report pre-existing quality and architecture concerns, and is advisory rather than a patch-correctness gate. `--audit` is mutually exclusive with `--committed`, `--uncommitted`, `--commit`, and `--base`. If audit paths are omitted, the existing default source-directory resolution is retained. `implement-tasks` uses defect-gate mode and does not invoke audit mode as its completion gate.
- **Alternatives Rejected**: A separate audit command; implicit quality-audit behavior whenever paths are supplied; combining quality scoring with every defect-gate review.
- **Reason**: An explicit mode preserves the existing audit capability while keeping merge-blocking defect detection focused and semantically unambiguous.
- **User Evidence**: The user confirmed that only `--audit [path]` runs the original whole-path quality audit and that all other listed selectors review a Git change scope.

### DEC-006: Supplemental defect-review focus

- **Status**: confirmed
- **Decision**: Defect-gate mode supports repeatable `--focus <instructions>` arguments. Each focus adds a risk-specific review obligation without replacing the general defect rubric, narrowing the selected Git change target, or allowing other evident defects to be ignored. Defect-gate mode does not accept path filters; path arguments remain exclusive to `--audit` mode.
- **Alternatives Rejected**: Replacing the core review instructions with arbitrary custom text; treating focus as a scope restriction; allowing path-limited defect reviews to emit a whole-change clean verdict.
- **Reason**: Specialized checks improve coverage for high-risk domains, while retaining the complete change target prevents a partial review from being mistaken for a merge-ready result.
- **User Evidence**: The user confirmed the repeatable supplemental `--focus` design.

### DEC-007: Mode, target, and context parameter model

- **Status**: confirmed
- **Decision**: `review-code` arguments are separated into three layers: review mode, Git target, and review context. Defect-gate mode accepts one Git target plus compatible `--base`, `--feature`, and repeatable `--focus` context modifiers. Audit mode accepts only `--audit [paths...]` and is mutually exclusive with all defect-gate target and context arguments. `--feature` supplies requirements context and never changes the Git target.
- **Alternatives Rejected**: Treating feature artifacts as a Git scope; running requirements traceability during whole-path quality audit; allowing audit and defect-gate arguments to produce a combined ambiguous report.
- **Reason**: Orthogonal parameters keep change selection, requirements evidence, and quality auditing independently understandable and prevent partial reviews from claiming whole-feature readiness.
- **User Evidence**: The user confirmed the proposed mode-target-context model.

### DEC-008: Requirements traceability depth follows target completeness

- **Status**: confirmed
- **Decision**: A default complete-feature review with resolved feature artifacts checks both full requirements coverage and implementation conformance. `--uncommitted` and `--commit` check only conformance of affected requirements and explicitly do not assess whole-feature completeness. `--committed` checks full completeness only when no excluded uncommitted changes exist; otherwise it performs affected-requirement conformance only. Direct review auto-matches a unique feature from the current branch, while `--feature <feature-dir>` explicitly selects or overrides it. If feature context cannot be resolved, code-defect review continues with a visible `Requirements coverage: not evaluated` degradation. `implement-tasks` explicitly supplies its current feature directory and uses the complete-feature target.
- **Alternatives Rejected**: Treating every partial Git target as proof of whole-feature completeness; failing all code reviews when no CodexSpec feature exists; silently omitting requirements-coverage status.
- **Reason**: Requirements conclusions must not exceed the completeness of the reviewed Git target, while ordinary repositories and ad hoc changes must remain reviewable.
- **User Evidence**: The user confirmed the target-dependent traceability rules and standard `implement-tasks` invocation.

### DEC-009: Mandatory four-stage defect review

- **Status**: confirmed
- **Decision**: Every defect-gate invocation executes four stages: (1) Scope Pass resolves and inventories the exact Git target and available project/feature context; (2) Behavior Pass traces changed behavior through entry points, call chains, data flows, failure paths, compatibility, concurrency, and resource handling; (3) Risk Pass selects change-appropriate specialist checks and re-inspects relevant evidence independently of the Behavior Pass summary; and (4) Verification Pass runs applicable deterministic checks, validates concrete trigger and impact evidence for each finding, removes speculative or duplicate findings, and produces the verdict plus coverage degradations. `--focus` adds Risk Pass obligations but cannot remove automatically selected risks. Risk and verification depth adapts to the changed surface, while all four stages remain mandatory.
- **Alternatives Rejected**: A single broad quality-reading pass; relying on one initial summary for all later risk analysis; making specialist checks entirely manual or `--focus`-only.
- **Reason**: Explicitly revisiting the change through behavioral, adversarial, and verification lenses reduces attention anchoring and the pattern of discovering boundary defects only across repeated external review rounds.
- **User Evidence**: The user confirmed the mandatory four-stage review model.

### DEC-010: Three-state defect-gate verdict

- **Status**: confirmed
- **Decision**: Defect-gate mode emits exactly one terminal verdict: `PASS` (`patch is correct`), `FAIL` (`patch is incorrect`), or `INCONCLUSIVE` (`correctness not established`). PASS requires successful completion of all four review stages, no unresolved qualifying findings, and completion of all mandatory verification; an empty findings list alone is insufficient. FAIL requires a validated defect or a deterministic verification failure attributable to the selected change. INCONCLUSIVE covers unresolved or incomplete Git scope, inaccessible required evidence, blocked mandatory verification, timeout or environment failure, invalid reviewer output, or interrupted review. `implement-tasks` treats only PASS as completion.
- **Alternatives Rejected**: Inferring success from an empty findings list; collapsing operational review failures into either PASS or FAIL; allowing `implement-tasks` to complete on degraded or malformed review output.
- **Reason**: A reliable merge gate must distinguish observed defects from an inability to establish correctness and must fail closed when required evidence is unavailable.
- **User Evidence**: The user adopted the proposed three-state verdict semantics.

### DEC-011: Requirements coverage and terminal verdict interaction

- **Status**: confirmed
- **Decision**: When `implement-tasks` explicitly supplies feature artifacts for a complete-feature review, missing or unreadable required artifacts make the review INCONCLUSIVE. A direct review with no uniquely resolvable feature may still PASS at the code-defect level, but must report `Requirements coverage: not evaluated` and must not claim whole-feature readiness. Audit mode retains its separate advisory score statuses and does not use defect-gate verdicts.
- **Alternatives Rejected**: Treating absent feature context as an unconditional failure for all repositories; silently implying requirements completeness from a code-only PASS.
- **Reason**: Code-level review remains useful outside an SDD feature while workflow completion requires the stronger evidence it claims to verify.
- **User Evidence**: The user adopted the proposed distinction between workflow-required and direct-review requirements coverage.

### DEC-012: Project-first risk-adaptive verification

- **Status**: confirmed
- **Decision**: Verification commands are selected in this order: explicit project and feature instructions, existing CI/project-script entry points, build-manifest standard commands, then optional language-default analyzers. Applicable project-mandated checks and targeted checks for changed components are mandatory. A standard full test suite becomes mandatory when project instructions require it or the changed surface crosses shared boundaries that cannot be validated locally; it is not unconditional. Pure documentation changes need only applicable declared documentation checks. The reviewer records every executed command and outcome.
- **Alternatives Rejected**: Always running every repository test regardless of scope; using a fixed language-tool list ahead of project conventions; silently skipping unavailable mandatory checks.
- **Reason**: Existing project commands provide the most relevant evidence, while risk-based breadth preserves reliability without making unrelated suites an unconditional cost.
- **User Evidence**: The user adopted the proposed verification selection policy.

### DEC-013: Verification safety and failure classification

- **Status**: confirmed
- **Decision**: Review verification must not modify project files, install or update dependencies, rewrite lockfiles, publish, deploy, run migrations, or use formatter write modes. A mandatory command that cannot run makes the verdict INCONCLUSIVE. Missing optional tooling creates an explicit coverage degradation but does not independently block PASS. A failed check produces FAIL only when the failure is attributable to the selected change; unresolved attribution produces INCONCLUSIVE.
- **Alternatives Rejected**: Treating every tool failure as a patch defect; treating unavailable mandatory validation as a clean result; allowing review verification to mutate the implementation under review.
- **Reason**: Verification must fail closed without confusing environment failures with code defects or altering the evidence being assessed.
- **User Evidence**: The user adopted the proposed command safety and failure-handling rules.

### DEC-014: Defect finding admission and priority

- **Status**: confirmed
- **Decision**: A defect-gate finding must describe a discrete, actionable issue with material correctness, security, performance, reliability, compatibility, or confirmed-requirement impact; be introduced, worsened, or made reachable by the selected change; identify concrete trigger conditions and an evidence-backed impact path; be consistent with confirmed intent; and be something the author should fix before merge. Findings use priorities P0 through P3, where P3 remains a reproducible low-impact defect rather than a style suggestion. Every admitted P0-P3 finding makes the verdict FAIL. Style preferences, general refactoring opportunities, praise, and non-defect recommendations are excluded from defect-gate mode and remain audit concerns.
- **Alternatives Rejected**: Allowing aggregate scores to offset defects; admitting speculative risks as findings; allowing low-priority real defects to coexist with a clean PASS.
- **Reason**: Strict admission keeps the report focused while a zero-defect PASS remains semantically unambiguous.
- **User Evidence**: The user adopted the proposed finding criteria and all-priorities-block policy.

### DEC-015: Finding evidence locations and compact report

- **Status**: confirmed
- **Decision**: Findings prefer the shortest useful location in the reviewed diff. Missing-requirement findings may instead reference the authoritative requirement/spec entry plus the nearest implementation boundary, and verification findings reference both the failing command and relevant code. Material concerns that cannot be verified are recorded as evidence gaps and may make the verdict INCONCLUSIVE; they are not emitted as speculative findings. Defect-gate reports contain only Verdict, Scope, Findings, Requirements Coverage, Verification Summary, and Coverage Gaps, with no strengths section, recommendation catalog, or quality score.
- **Alternatives Rejected**: Requiring a fabricated changed-line location for omitted behavior; hiding evidence gaps; retaining the existing scorecard report structure in defect-gate mode.
- **Reason**: Findings need honest, actionable evidence while a concise report preserves reviewer attention for correctness.
- **User Evidence**: The user adopted the proposed evidence-location and output rules.

### DEC-016: Built-in risk profiles

- **Status**: confirmed
- **Decision**: Risk Pass includes built-in cross-language profiles for authorization/trust, command/process execution, filesystem/path handling, parsing/configuration, persistence/state, network/provider behavior, concurrency/lifecycle, public API/CLI compatibility, secrets/injection, and build/dependency behavior. Each activated profile applies its relevant normal, denial/failure, boundary, bypass, and legacy-compatibility scenarios. Behavior Pass still performs general correctness review when no profile matches.
- **Alternatives Rejected**: Relying entirely on reviewer improvisation; requiring users to supply all specialist concerns through `--focus`; replacing general behavior review with profile matching.
- **Reason**: Stable risk lenses make recurring boundary classes explicit and reduce omission caused by attention or wording differences between runs.
- **User Evidence**: The user adopted the proposed built-in risk profile set.

### DEC-017: Risk-profile activation and evidence

- **Status**: confirmed
- **Decision**: Profiles are activated from diff semantics, changed call chains, dependencies, and feature artifacts rather than filename or keyword matching alone; multiple profiles may apply. `--focus` only adds profiles or checks. Scope reports each activated profile and its trigger evidence. If a high-risk profile is activated but critical evidence cannot be inspected or verified, the verdict is INCONCLUSIVE rather than PASS.
- **Alternatives Rejected**: Opaque risk selection; keyword-only classification; allowing missing high-risk evidence to disappear into a clean result.
- **Reason**: Review conclusions must show why specialist coverage was selected and fail closed when that coverage cannot actually be performed.
- **User Evidence**: The user adopted the proposed activation and fail-closed evidence rules.

### DEC-018: Stable defect-gate result envelope

- **Status**: confirmed
- **Decision**: Every defect-gate report ends with a machine-stable `<review-code-result>` envelope containing one valid JSON object with `schema_version`, `mode`, `verdict`, `target`, `requirements_coverage`, `verification`, per-priority finding counts, and coverage-gap count. Field names and enum values remain fixed in English regardless of interaction language. Counts and statuses must agree with the human-readable report and PASS invariants. Missing, malformed, contradictory, unsupported, or unknown envelope data is interpreted as INCONCLUSIVE; callers must never infer success from surrounding prose. Audit reports remain human-readable scorecards and are not consumed by `implement-tasks`.
- **Alternatives Rejected**: Parsing localized prose and score thresholds; accepting malformed structured output as an empty-finding result; requiring audit reports to share defect-gate semantics.
- **Reason**: Workflow orchestration needs a deterministic fail-closed contract that cannot confuse output failure with review success.
- **User Evidence**: The user adopted the stable result envelope protocol.

### DEC-019: Evidence-verified fix and full re-review loop

- **Status**: confirmed
- **Decision**: `implement-tasks` establishes a green baseline, invokes defect-gate mode with the current feature directory, independently verifies every reported finding before editing, applies only verified fixes, and re-runs targeted plus mandatory verification. Functional defects use TDD with a reproducing regression test; documentation and non-code configuration defects use their applicable checks. Every subsequent review re-evaluates the complete feature delta. Only a valid final PASS envelope permits successful completion, and no P0-P3 finding may be deferred while claiming success.
- **Alternatives Rejected**: Automatically editing for every unverified model finding; re-reviewing only fixed files; completing when only lower-priority defects remain; using audit score thresholds as implementation completion.
- **Reason**: Finding verification controls false positives, while full-target re-review detects interactions and regressions introduced by fixes.
- **User Evidence**: The user adopted the proposed evidence-verified fix and full re-review workflow.

### DEC-020: Progress-based loop termination

- **Status**: confirmed
- **Decision**: Remove the fixed two-round review limit and continue while verified findings are being resolved or new actionable defects are discovered. Stop without success when the same defect survives two verified fix attempts, two consecutive rounds make no substantive progress, a finding requires a new product or architecture decision, or the same independently refuted false positive recurs. Transient INCONCLUSIVE causes may be retried up to two times; persistent INCONCLUSIVE remains blocking. Stopped loops report FAIL or INCONCLUSIVE evidence and do not translate the outcome into a score-based `needs work` success path.
- **Alternatives Rejected**: A fixed low round cap; unbounded repetition without progress detection; treating repeated output or environment failure as PASS.
- **Reason**: Reliability depends on reaching a clean review, while progress and repetition guards prevent unproductive infinite loops.
- **User Evidence**: The user adopted the proposed continue-to-clean-PASS and progress-based stop rules.

### DEC-021: Complete change inventory

- **Status**: confirmed
- **Decision**: Scope Pass inventories every entry in the selected Git target without source-extension filtering, including implementation, tests, configuration, schemas, migrations, scripts, CI/release files, manifests, lockfiles, documentation, templates, user-visible assets, CodexSpec artifacts, renames, deletions, symlinks, binaries, submodules, generated outputs, and vendored content. Documentation- or configuration-only changes cannot skip defect-gate review. CodexSpec artifacts are checked as requirements evidence and for unauthorized intent drift rather than excluded from scope.
- **Alternatives Rejected**: Reviewing only recognized source extensions; excluding feature artifacts categorically; reporting `no code to review` for behavior-affecting non-code changes.
- **Reason**: Behavior and security defects frequently originate in configuration, scripts, metadata, generated state, and documentation contracts rather than conventional source files.
- **User Evidence**: The user adopted the complete change inventory rule.

### DEC-022: Non-text, derived, and large-change coverage

- **Status**: confirmed
- **Decision**: Generated outputs are validated against their source and generator; lockfiles against manifests and unexpected dependency changes; vendored content against source/version/checksum and stated intent; and binary/submodule changes against available metadata and referenced content. Critical inaccessible content makes the verdict INCONCLUSIVE. Large diffs are partitioned while preserving one complete inventory and may not be silently truncated. Every changed entry ends as `reviewed`, `verified by tool/generator`, `excluded with explicit justification`, or `uninspectable`; unclassified entries or critical uninspectable evidence prohibit PASS.
- **Alternatives Rejected**: Unexplained generated/vendor exclusion; silent context-window truncation; assuming opaque binary or submodule changes are correct.
- **Reason**: Scope completeness must be demonstrable even when line-oriented source review is not the appropriate verification method.
- **User Evidence**: The user adopted the proposed handling and inventory states for all changed entries.

### DEC-023: Fresh isolated reviewer context

- **Status**: confirmed
- **Decision**: Defect-gate mode runs by default in a fresh isolated reviewer context that receives only the review contract, selected Git target, cwd/environment facts, project instructions and Constitution, applicable feature artifacts, and necessary tool access. It does not inherit implementation reasoning, prior conclusions, or previous review findings. Each post-fix full review uses another fresh context. The outer workflow validates the result envelope, independently verifies findings, and performs fixes; the reviewer remains review-only. The result envelope records `review_context` as `isolated` or `shared`.
- **Alternatives Rejected**: Treating same-context self-review as equivalent evidence; carrying prior findings into the next reviewer; allowing the review worker to apply fixes.
- **Reason**: Fresh evidence-oriented context reduces confirmation bias and anchoring to implementation intent or previous review output.
- **User Evidence**: The user adopted the default isolated-reviewer strategy.

### DEC-024: Isolation degradation boundary

- **Status**: confirmed
- **Decision**: When the host cannot create an isolated reviewer, an ordinary direct invocation may fall back to the current context only with a visible `review_context: shared` coverage gap. An `implement-tasks` final gate or any review with an activated high-risk profile requires isolation; inability to provide it makes the verdict INCONCLUSIVE. Audit mode does not require isolated execution.
- **Alternatives Rejected**: Making CodexSpec unusable for every direct review on hosts without delegation; accepting shared self-review as a clean high-risk or workflow-completion gate.
- **Reason**: Capability fallback preserves broad usability without weakening the evidence standard for claims of feature readiness or high-risk correctness.
- **User Evidence**: The user adopted the proposed mandatory-versus-degraded isolation boundary.

### DEC-025: Risk-adaptive independent specialist review

- **Status**: confirmed
- **Decision**: Ordinary defect reviews use one isolated primary reviewer. When semantic risk assessment identifies high-impact trust, authorization, command execution, injection, secrets, destructive filesystem, data migration, or comparable boundaries, the workflow also starts at least one fresh independent specialist reviewer. The specialist receives raw target evidence, relevant call chains and feature artifacts, and activated risk obligations, but not primary findings. Related profiles may share one specialist; materially disjoint domains may be partitioned. The coordinator unions and deduplicates outputs without discarding a specialist finding merely because the primary missed it, then applies the standard evidence-admission rules. Missing, failed, malformed, or incomplete required specialist review makes the verdict INCONCLUSIVE.
- **Alternatives Rejected**: Using multiple reviewers for every low-risk change; giving the specialist the primary answer to critique; treating specialist execution as optional after a high-risk trigger.
- **Reason**: Independent adversarial attention improves high-risk recall with targeted cost and reduces reliance on many repeated general reviews.
- **User Evidence**: The user adopted the risk-adaptive dual-reviewer strategy.

### DEC-026: Reviewer execution disclosure

- **Status**: confirmed
- **Decision**: The result envelope records primary and specialist reviewer execution states so callers can verify that required independent review actually occurred. High-risk PASS requires successful primary and required specialist completion.
- **Alternatives Rejected**: Reporting only a merged finding list with no evidence that required reviewers ran.
- **Reason**: A machine-consumed gate must expose whether its required review topology was satisfied.
- **User Evidence**: The user adopted the proposed reviewer status fields.

### DEC-027: Git target failure and empty-target behavior

- **Status**: confirmed
- **Decision**: An unresolved base, merge base, or requested commit produces INCONCLUSIVE and never falls back to path audit. Default and uncommitted targets include untracked but not ignored files. A direct code-only review with an empty target returns PASS with `target: empty` and an explicit no-changes statement. An `implement-tasks` feature review still performs requirements traceability for an empty target and fails when confirmed implementation obligations are absent. Scope always discloses exact refs, resolved SHAs, and inventory counts.
- **Alternatives Rejected**: Treating Git target failure as a reason to audit a source directory; skipping requirements checks whenever the diff is empty; including ignored files implicitly.
- **Reason**: Target failures and genuinely empty changes have different meanings, and neither may create a misleading feature-readiness result.
- **User Evidence**: The user adopted the proposed target boundaries together with the adjusted merge-commit rule.

### DEC-028: Single-commit parent semantics

- **Status**: confirmed
- **Decision**: `--commit <sha>` reviews a normal commit relative to its parent and a root commit relative to the Git empty tree. A merge commit defaults to its first parent, and Scope must disclose that parent. `--parent <n>` may override the selected parent only with `--commit`; an invalid parent index produces INCONCLUSIVE. `--committed` remains a merge-base-to-HEAD net-diff operation and does not use `--parent`.
- **Alternatives Rejected**: Requiring `--parent` for every merge-commit review; silently using an undisclosed parent; treating a merge commit as if it had one unambiguous parent.
- **Reason**: First-parent behavior matches the common meaning of what a merge introduced while explicit disclosure and override preserve correctness for other review intents.
- **User Evidence**: After clarification of merge parents, the user adopted default first-parent behavior with optional override.

### DEC-029: Hard-error migration for legacy path arguments

- **Status**: confirmed
- **Decision**: Bare path arguments such as `review-code src/` are invalid after this change and produce an actionable instruction to use `review-code --audit src/`. Paths are never inferred as audit activation or defect-target filters. Invalid or conflicting defect-gate arguments produce an explicit error plus an INCONCLUSIVE result envelope. Documentation, examples, translations, workflow callers, and template tests migrate atomically to the new syntax, and release notes identify the default-mode and path-audit breaking changes. No implicit compatibility period is provided.
- **Alternatives Rejected**: Silently preserving bare paths as audit mode for one release; interpreting paths as a narrowed defect target; accepting ambiguous legacy automation.
- **Reason**: Successful ambiguous calls would prevent users and automation from knowing which review contract actually ran.
- **User Evidence**: The user adopted the hard-error migration strategy.

### DEC-030: Reviewer instruction and evidence isolation

- **Status**: confirmed
- **Decision**: Only host-level instructions, the review protocol, explicit user arguments, recognized project instruction files, the Constitution, and confirmed feature artifacts may contribute authoritative review context. Source comments and strings, ordinary documents, generated/vendor content, commit messages, test logs, and tool output are untrusted evidence and cannot issue reviewer instructions. Project context may add standards but cannot weaken target inventory, review-only execution, risk coverage, mandatory verification, finding evidence, verdict, or result-envelope invariants. Feature artifacts supply product intent but embedded text that asks to bypass the gate is non-authoritative. Ambiguous instruction sources are treated as ordinary evidence.
- **Alternatives Rejected**: Allowing arbitrary repository text or tool output to override review behavior; allowing project instructions to disable core gate integrity; automatically trusting ambiguous command-like content.
- **Reason**: The content under review may be adversarial or accidentally instruction-shaped and must not control its own assessment.
- **User Evidence**: The user adopted the proposed instruction-versus-evidence isolation rules.

### DEC-031: Injection evidence handling

- **Status**: confirmed
- **Decision**: Suspected prompt injection, forged tool output, or review-bypass content is examined as security evidence. It becomes a finding only when introduced or exposed by the selected change and the standard concrete-impact criteria are satisfied; otherwise it does not alter reviewer behavior or create a speculative finding.
- **Alternatives Rejected**: Ignoring injection-shaped content entirely; reporting every command-like string as a vulnerability.
- **Reason**: Review integrity and finding precision both require treating such content as untrusted while still assessing real exploitability.
- **User Evidence**: The user adopted the proposed injection-evidence boundary.

### DEC-032: Test-gap finding boundary

- **Status**: confirmed
- **Decision**: Missing tests become defect findings only when binding project/feature evidence requires them, a changed observable behavior or failure branch has no existing test or equivalent deterministic verification, a real defect fix lacks regression protection, or a high-risk denial/bypass/failure path lacks evidence. Each finding names the exact unverified behavior and scenario; generic coverage-improvement advice is excluded. Existing indirect tests count when they demonstrably cover the contract, and behavior-preserving refactors do not require redundant tests. A binding missing test is FAIL; an existing mandatory test that cannot run is INCONCLUSIVE. Projects with no binding test requirement record a coverage gap, which blocks PASS only when change risk leaves no adequate substitute evidence.
- **Alternatives Rejected**: Flagging every uncovered line; ignoring explicit test obligations; treating an unavailable required test as either a code defect or a clean pass.
- **Reason**: Test findings should represent a concrete correctness-evidence gap rather than an arbitrary coverage preference.
- **User Evidence**: The user adopted the concrete-behavior-first test-gap rules.

### DEC-033: No built-in finding waiver

- **Status**: confirmed
- **Decision**: `review-code` provides no `--ignore`, `--waive`, or severity-suppression mechanism. A valid finding leaves the gate FAIL until it is fixed and cleanly re-reviewed, disproved by verifiable evidence and absent from a fresh review, or made consistent with intent through a formally confirmed requirement/constraint/out-of-scope change followed by re-review. User acceptance of a still-valid defect without an authoritative intent change does not produce PASS, and `implement-tasks` cannot complete on that basis; users retain the ability to act outside the gate without CodexSpec claiming success.
- **Alternatives Rejected**: Inline reviewer suppressions; user acknowledgements that convert known defects into PASS; priority-based automatic deferral.
- **Reason**: A built-in waiver would undermine the zero-defect meaning of PASS and become an ambiguous bypass path.
- **User Evidence**: The user adopted the no-waiver policy.

### DEC-034: No fast-path gate degradation

- **Status**: confirmed
- **Decision**: Defect-gate mode provides no `--fast`, `--skip-risk`, `--skip-tests`, or equivalent switches. Four-stage review, applicable mandatory verification, complete inventory, and required specialist review cannot be disabled. Callers may select a smaller explicit Git target, but its verdict applies only to that target and cannot establish whole-feature readiness. Large changes are partitioned rather than truncated, and host resource exhaustion that prevents required work produces INCONCLUSIVE. `--focus` only adds coverage, and audit mode cannot substitute for the gate.
- **Alternatives Rejected**: A fast mode that retains the PASS label; silent diff truncation; treating partial-target or audit results as complete feature evidence.
- **Reason**: Faster shallow review would reintroduce the misleading clean-result failure mode this feature is intended to remove.
- **User Evidence**: The user adopted the no-fast-path strategy and explicitly prioritized review quality over speed.

### DEC-035: Project-local deterministic review-context resolver

- **Status**: confirmed
- **Decision**: Git target argument validation, base/merge-base/parent resolution, feature matching, and complete change inventory are implemented by project-local read-only helper scripts distributed through the existing CodexSpec initialization mechanism, not by an installed CodexSpec CLI runtime or ad hoc model commands. CodexSpec ships Bash and PowerShell implementations under its platform script sources; initialization copies the applicable implementation into `.codexspec/scripts/` in the user's project, and the review template invokes that local helper. The resolver emits a versioned JSON manifest to stdout and does not persist files or mutate Git state. Bash and PowerShell must implement equivalent semantics and pass shared behavioral fixtures.
- **Alternatives Rejected**: Requiring the CodexSpec CLI to remain installed at review time; leaving deterministic scope computation entirely to the model; writing resolver state into the project.
- **Reason**: Project-local scripts match CodexSpec's self-contained distribution model while making scope construction deterministic and testable in the repository actually being reviewed.
- **User Evidence**: The user confirmed the corrected project-local resolver design.

### DEC-036: Resolver compatibility failure is inconclusive

- **Status**: confirmed
- **Decision**: The review template accepts only supported resolver manifest schema versions. A missing helper, unsupported version, invalid JSON, or resolver failure produces INCONCLUSIVE with actionable project-update guidance; the reviewer must not fall back to model-computed Git scope.
- **Alternatives Rejected**: Silent compatibility fallback; accepting partially parsed manifests; making resolver availability depend on an external service.
- **Reason**: Falling back after deterministic scope construction fails would recreate the scope-omission risk the helper exists to prevent.
- **User Evidence**: The user confirmed the project-local resolver behavior including fail-closed compatibility handling.

### DEC-037: Deterministic resolver and workflow contract tests

- **Status**: confirmed
- **Decision**: Required automated tests use temporary Git repositories to cover every target mode, committed/staged/unstaged/untracked/ignored sources, rename/delete/symlink/binary/submodule entries, default-base and merge-base resolution, normal/root/merge commits and parent override, empty/error cases, manifest schema, Bash/PowerShell parity, and no repository-state mutation. Template and integration tests cover argument contracts, mode exclusivity, four-stage review, verdict envelope, installer rendering for supported hosts, the `implement-tasks` clean-PASS loop, and removal of legacy bare-path semantics. These tests run without an LLM or network dependency in normal CI.
- **Alternatives Rejected**: Testing only for the presence of selected prompt phrases; leaving cross-platform target behavior untested; requiring model access in ordinary CI.
- **Reason**: Deterministic scope and orchestration behavior can and should be proven with reproducible TDD fixtures.
- **User Evidence**: The user confirmed the two-layer verification approach after clarification.

### DEC-038: Reusable model-assisted review quality evaluation

- **Status**: confirmed
- **Decision**: The CodexSpec development repository includes source-independent synthetic change fixtures with expected risk profiles, minimum qualifying findings, forbidden speculative findings, and verdicts, including both representative defect and clean-patch cases. These fixtures are not copied into initialized user projects and do not run in ordinary CI. Before this feature is considered implemented, the updated review command is exercised against the complete evaluation set on at least one supported host and the results are recorded; the corpus remains reusable for later review-prompt regressions.
- **Alternatives Rejected**: Claiming review-quality improvement solely from static template assertions; placing nondeterministic model calls in normal unit-test CI; embedding prior project-specific source cases in persistent artifacts.
- **Reason**: Actual model execution is the only direct evidence that the review protocol improves representative defect recall without unacceptable false positives.
- **User Evidence**: The user confirmed adoption of deterministic CI plus repeatable model-assisted evaluation.

## Open Questions

### OPEN-001: Audit capability interface

- **Status**: resolved
- **Resolution**: See DEC-005.
- **Owner**: User

### OPEN-002: Review target resolution

- **Status**: resolved
- **Resolution**: See DEC-002 through DEC-008 and DEC-027 through DEC-029.
- **Owner**: User

### OPEN-003: Defect-gate evidence and completion semantics

- **Status**: resolved
- **Resolution**: See DEC-009 through DEC-034.
- **Owner**: User

## Confirmation Log

### Session 2026-07-13 22:44 CST

- **Summary Presented**: Position `review-code` as a change-scoped defect gate by default and retain whole-path quality scoring only as an explicit audit capability.
- **User Confirmation**: "Confirmed."
- **Entries Confirmed**: NEED-001, DEC-001

### Session 2026-07-13 22:51 CST

- **Summary Presented**: Define the default review target as the complete feature-branch delta, while allowing explicit uncommitted-only and single-commit targets.
- **User Confirmation**: The user accepted the recommendation and asked how to select committed branch changes only.
- **Entries Confirmed**: DEC-002

### Session 2026-07-13 22:52 CST

- **Summary Presented**: Add a committed-only target selected by `--committed`, with `--base` acting as an optional base-branch override and primary review targets remaining mutually exclusive.
- **User Confirmation**: "Confirmed."
- **Entries Confirmed**: DEC-003

### Session 2026-07-13 23:00 CST

- **Summary Presented**: Resolve an omitted base from Git default-branch metadata with deterministic fallbacks, expose the selected ref and merge base, avoid implicit fetch, and fail rather than silently narrow an uncertain review scope.
- **User Confirmation**: "Confirmed."
- **Entries Confirmed**: DEC-004

### Session 2026-07-13 23:05 CST

- **Summary Presented**: Keep all Git-target selectors in defect-gate mode and expose the existing whole-path scorecard only through mutually exclusive `--audit [paths...]`; workflow completion uses only the defect gate.
- **User Confirmation**: "Confirmed."
- **Entries Confirmed**: DEC-005

### Session 2026-07-13 23:10 CST

- **Summary Presented**: Allow repeatable risk-specific focus instructions only as supplements to the complete defect review, and reserve path arguments for audit mode.
- **User Confirmation**: "Confirmed."
- **Entries Confirmed**: DEC-006

### Session 2026-07-13 23:20 CST

- **Summary Presented**: Separate review mode, Git target, and review context; enable full requirements completeness only for complete feature targets and clearly degrade partial or unresolved requirements coverage.
- **User Confirmation**: "Confirmed."
- **Entries Confirmed**: NEED-002, DEC-007, DEC-008

### Session 2026-07-14 11:06 CST

- **Summary Presented**: Require Scope, Behavior, risk-adaptive, and Verification passes for every defect-gate review, with independent evidence inspection and focus directives only adding coverage.
- **User Confirmation**: "Confirmed."
- **Entries Confirmed**: DEC-009

### Session 2026-07-14 11:08 CST

- **Summary Presented**: Use PASS, FAIL, and INCONCLUSIVE terminal states; require completed evidence rather than an empty findings list for PASS; and distinguish workflow-required requirements coverage from direct code-only review.
- **User Confirmation**: "Adopted."
- **Entries Confirmed**: DEC-010, DEC-011

### Session 2026-07-14 11:11 CST

- **Summary Presented**: Select mandatory checks from project conventions and changed risk, run the full suite only when required by policy or blast radius, forbid mutating verification, and distinguish attributable failures from inconclusive environment failures.
- **User Confirmation**: "Adopted."
- **Entries Confirmed**: DEC-012, DEC-013

### Session 2026-07-14 11:18 CST

- **Summary Presented**: Admit only evidence-backed defects introduced or exposed by the selected change, make every P0-P3 defect blocking, route non-defect advice to audit mode, and use a compact evidence-oriented report with honest coverage gaps.
- **User Confirmation**: "Adopted."
- **Entries Confirmed**: DEC-014, DEC-015

### Session 2026-07-14 11:22 CST

- **Summary Presented**: Add ten built-in cross-language risk profiles, activate them from semantic change evidence, allow focus directives only to add coverage, report activation reasons, and fail closed when high-risk evidence is unavailable.
- **User Confirmation**: "Adopted."
- **Entries Confirmed**: DEC-016, DEC-017

### Session 2026-07-14 13:49 CST

- **Summary Presented**: Append a fixed English JSON result envelope to defect-gate reports and treat any missing, malformed, or contradictory envelope as INCONCLUSIVE; keep audit output separate.
- **User Confirmation**: "Adopted."
- **Entries Confirmed**: DEC-018

### Session 2026-07-14 13:57 CST

- **Summary Presented**: Replace the two-round score-based loop with independently verified fixes, TDD where applicable, complete-feature re-review after every change, clean PASS as the only success state, and progress-based stop/retry guards.
- **User Confirmation**: "Adopted."
- **Entries Confirmed**: DEC-019, DEC-020

### Session 2026-07-14 14:13 CST

- **Summary Presented**: Inventory and account for every changed artifact, including non-code and opaque content; verify derived content appropriately; partition large diffs without silent omission; and prohibit PASS with unaccounted or critical inaccessible evidence.
- **User Confirmation**: "Adopted."
- **Entries Confirmed**: DEC-021, DEC-022

### Session 2026-07-14 14:31 CST

- **Summary Presented**: Use a fresh review-only context without implementation or prior-review history, require a new context after fixes, record isolation in the result, permit visible shared-context fallback only for ordinary direct reviews, and fail closed for workflow or high-risk gates.
- **User Confirmation**: "Adopted."
- **Entries Confirmed**: DEC-023, DEC-024

### Session 2026-07-14 14:34 CST

- **Summary Presented**: Add an independent adversarial specialist only for high-impact risk, keep its evidence and reasoning independent from the primary reviewer, merge findings without primary bias, fail closed when required specialist review is incomplete, and disclose reviewer execution states.
- **User Confirmation**: "Adopted."
- **Entries Confirmed**: DEC-025, DEC-026

### Session 2026-07-14 15:13 CST

- **Summary Presented**: Fail closed on unresolved Git targets, distinguish empty code-only changes from missing feature implementation, include untracked but not ignored files, review normal/root commits against the correct base, and use disclosed first-parent semantics with optional override for merge commits.
- **User Confirmation**: "Adopted."
- **Entries Confirmed**: DEC-027, DEC-028

### Session 2026-07-14 15:19 CST

- **Summary Presented**: Reject legacy bare-path calls with actionable migration guidance, never infer audit or path-limited defect semantics, emit INCONCLUSIVE for invalid defect invocations, and update all callers and release documentation atomically.
- **User Confirmation**: "Adopted."
- **Entries Confirmed**: DEC-029

### Session 2026-07-14 15:22 CST

- **Summary Presented**: Separate authoritative review context from untrusted repository and tool evidence, forbid project content from weakening gate invariants, and assess injection-shaped content only as evidence under the normal defect criteria.
- **User Confirmation**: "Adopted."
- **Entries Confirmed**: DEC-030, DEC-031

### Session 2026-07-14 15:29 CST

- **Summary Presented**: Keep requirements, specification, plan, and tasks source-independent by persisting only CodexSpec behavior and excluding external source paths, symbols, or replication constraints.
- **User Confirmation**: "Confirmed."
- **Entries Confirmed**: CON-001

### Session 2026-07-14 19:17 CST

- **Summary Presented**: Treat test absence as a defect only for binding requirements or concrete unverified changed behavior, accept demonstrably sufficient existing coverage, classify unavailable mandatory tests as INCONCLUSIVE, and avoid generic coverage advice.
- **User Confirmation**: "Adopted."
- **Entries Confirmed**: DEC-032

### Session 2026-07-14 19:18 CST

- **Summary Presented**: Provide no inline waiver or severity suppression; clear findings only through a verified fix, evidence-based invalidation, or formally confirmed intent change; never let accepted known defects become workflow PASS.
- **User Confirmation**: "Adopted."
- **Entries Confirmed**: DEC-033

### Session 2026-07-14 19:23 CST

- **Summary Presented**: Add no switches that skip defect-gate stages, use narrower explicit targets only with target-limited verdicts, partition rather than truncate large changes, and treat resource-limited incomplete review as INCONCLUSIVE.
- **User Confirmation**: "Adopted. Review quality takes priority over review speed."
- **Entries Confirmed**: CON-002, DEC-034

### Session 2026-07-14 19:30 CST

- **Summary Presented**: Remove irrelevant external-runtime and sandbox exclusions and avoid duplicating already confirmed behavior as a separate Out of Scope catalog.
- **User Confirmation**: "Confirmed."
- **Entries Confirmed**: The unused OUT-001 placeholder was removed; no new requirement entry was created.

### Session 2026-07-14 20:41 CST

- **Summary Presented**: Distribute a read-only Bash/PowerShell review-context resolver into each initialized project, emit a shared versioned JSON manifest without writes, test platform parity, and return INCONCLUSIVE rather than model-fallback when the helper or schema is unavailable.
- **User Confirmation**: "Confirmed."
- **Entries Confirmed**: DEC-035, DEC-036

### Session 2026-07-14 20:55 CST

- **Summary Presented**: Use normal offline CI to prove resolver and workflow contracts, and maintain a separate source-independent synthetic fixture corpus that is run explicitly on a supported host to verify real reviewer defect detection and false-positive behavior.
- **User Confirmation**: "Confirmed and adopted."
- **Entries Confirmed**: DEC-037, DEC-038

### Session 2026-07-14 20:58 CST

- **Summary Presented**: Final consistency review confirmed the complete change-scoped defect-gate interface, deterministic scope resolution, requirements traceability, risk-adaptive independent review, strict verdict and evidence rules, implementation re-review loop, and deterministic plus model-assisted validation strategy, with no unresolved requirement questions.
- **User Confirmation**: "Confirmed."
- **Entries Confirmed**: Final requirements record approved for specification generation.
