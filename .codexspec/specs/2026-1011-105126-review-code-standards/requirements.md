# Confirmed Requirements: Evidence-Based Review with On-Demand Standards

**Feature ID**: `2026-1011-105126`
**Feature Branch**: `2026-1011-105126-review-code-standards`
**Status**: Confirmed — user review complete; auto-next continuation authorized
**Last Confirmed**: 2026-10-11 (Asia/Shanghai)

## Authority Rules

- Only entries with `Status: confirmed` are binding downstream inputs.
- Open questions and proposed scope choices MUST NOT become binding requirements without confirmation.
- Replaced entries remain with `Status: superseded` and a link to their replacements.
- Source checklists provide review prompts, not authority to invent product requirements or bypass finding admission.
- Final stage confirmation is distinct from a topic confirmation. `workflow.auto_next: true` advances from discovery only after explicit confirmation of the final stage summary.
- **User review hold (2026-10-11)**: The user requested the requirements document for inspection and explicitly instructed not to advance. This hold was released by the user on 2026-10-11 with “确认，按照auto-next自主推进流程”. The final requirements are confirmed and auto-next continuation is authorized.
- The Needs, Constraints, Decisions, and Out of Scope sections contain current requirements. Superseded Entries and the Confirmation Log retain history and do not reactivate withdrawn interfaces or proposals.

## Context and Evidence

The goal is to make `review-code` systematic and thorough while preventing fabricated scenarios from causing excessive fixes or defensive code. The command must determine applicable review work from actual changes, confirmed obligations, and affected behavior.

The existing command already defines scope, system-contract, behavior, risk, and verification passes. Its distribution template also includes audit scoring and language appendices. Splitting maintainer sources through build-time fragments alone does not reduce execution-time context because those fragments are expanded into complete command files.

Repository evidence is available in `internal/command_templates/sources/review-code.md`, `internal/command_template_fragments.py`, `src/codexspec/integrations/codex.py`, `src/codexspec/commands/installer.py`, and `docs/internal/repository-layout.md` in this checkout. These are existing facts, not a prescription for new runtime paths. The existing `review-code` role is read-only; implementation callers own edits and must consume the expanded review output safely.

The user supplied a checklist with seven dimensions and 87 bullet items, including five false-positive avoidance items:

- [Original checklist snapshot](references/review-dimensions.original.txt), preserved byte for byte.
- [Checklist assessment](references/checklist-assessment.md), identifying language-specific descriptions and context-dependent rules.

A pure maintenance suggestion identifies a substantiated improvement to readability, maintainability, or extensibility without claiming a functional defect. The user requires these suggestions in normal change review and automatic incremental implementation by default. The snapshot is provenance evidence. The assessment is analysis; its individual rewrites remain proposed until the final stage summary is confirmed. Future standards must be available from the project and distribution rather than depend on the external source path.

## Needs

### NEED-001: Establish review direction from affected behavior

- **Status**: confirmed
- **Statement**: Establish which behaviors changed, their entry points, the rules they must preserve, and affected callers and dependencies before detailed review. Organize review work around those behaviors and contracts, and assign depth according to concrete impact and risk. Account for all selected changes; file-reading completion alone does not establish behavior coverage.
- **User Evidence**: The user requested clearer, more organized review that avoids superficial inspection and missed problems, and agreed with the proposed behavior-oriented approach.
- **Confirmed At**: 2026-10-10

### NEED-002: Trace complete behavior and bounded related occurrences

- **Status**: confirmed
- **Statement**: Trace affected call chains and data flows through relevant producers, consumers, state transitions, and external boundaries. Inspect normal paths and evidenced failure, denial, cancellation, recovery, and compatibility paths. Read related unchanged code when needed to establish impact. For a verified repeatable cause, inspect equivalent implementations and symmetric paths within a justified affected scope.
- **User Evidence**: The user agreed with complete behavior-chain review and checking related occurrences in the same review.
- **Confirmed At**: 2026-10-10

### NEED-003: Require evidence that a defect is reachable and consequential

- **Status**: confirmed
- **Statement**: Before admitting a defect finding, establish its operating context, the origin of its triggering conditions, a reachable execution path, the violated contract or behavior, concrete impact, and attribution to the selected change. Reproduction or a clear deterministic code argument may establish the evidence. A rare but credible failure or malicious external input is not excluded merely because it is uncommon.
- **User Evidence**: The user explicitly rejected fabricated boundaries that do not occur in real scenarios and accepted evidence-based defect admission.
- **Confirmed At**: 2026-10-10

### NEED-004: Check contrary evidence before reporting a candidate

- **Status**: confirmed
- **Statement**: Check whether upstream validation, type guarantees, state transitions, call ordering, framework behavior, or recovery mechanisms already prevent or correctly handle the suspected failure. Verify that the guarantee covers the relevant paths. Require a real path around that guarantee before asking for additional defensive handling.
- **User Evidence**: The user agreed with checking existing guarantees before reporting a problem and requesting more defenses.
- **Confirmed At**: 2026-10-10

### NEED-005: Split review content to reduce irrelevant execution context

- **Status**: confirmed
- **Statement**: Separate the coordinating command, common review discipline, mode-specific procedures, general checkpoints, and language, framework, or technical-topic subchecklists. Follow the initial organization in DEC-006 and the granularity constraint in CON-007; technical-topic detail may remain as sections inside the relevant checklist rather than requiring a separate file. Read applicable standards during execution so unrelated mode rules and detailed subchecklists need not be loaded in every invocation. Authoring-only splitting followed by complete expansion does not satisfy this need.
- **User Evidence**: The user requested splitting review directions, dimensions, and checklists to reduce command size and unrelated injected requirements while enabling on-demand use and continued expansion.
- **Confirmed At**: 2026-10-11

### NEED-006: Select standards from semantic evidence and expand during tracing

- **Status**: confirmed
- **Statement**: Read a lightweight standard index, construct the affected behavior map, and assess the applicability of every review dimension before choosing detailed checkpoints. Use confirmed requirements, project constraints, actual language semantics and versions, call relationships, data flows, and dependencies. File extensions and keywords can identify candidates but cannot alone establish applicability. Load additional standards when tracing discovers new relevant boundaries, including unchanged dependencies and implementations in other languages. A binding obligation can activate a standard even when its expected implementation is absent.
- **User Evidence**: The user asked when general and specialized checklists apply and how to choose them, then explicitly replied “同意” to the proposed selection and expansion procedure.
- **Confirmed At**: 2026-10-11

### NEED-007: Make standards extensible and coverage inspectable

- **Status**: confirmed
- **Statement**: Give standards clear purposes, applicability and non-applicability conditions, concrete checkpoints, necessary evidence, common false-positive conditions, and completion criteria. The lightweight index identifies standards and their locations without embedding full checklists. Record which standards apply, why they were selected, their relevant scope, completion, and key evidence. Adding standards must preserve defect admission, substantiated maintenance assessment, and the applicable completion rules.
- **User Evidence**: The user requested standards that can continually expand and accepted indexed selection, applicability assessment, and completion accounting.
- **Confirmed At**: 2026-10-11

### NEED-008: Integrate the supplied checklist without language leakage or lost intent

- **Status**: confirmed
- **Statement**: Inspect and integrate the supplied checklist's review intent. Generalize descriptions that express language-independent behavior; retain language-specific semantics and APIs in applicable subchecklists. Treat technical topics such as HTTP, database behavior, file upload, and browser rendering separately from language identity. Account for every source item with its retained, generalized, split, rewritten, or excluded destination and rationale, including false-positive avoidance guidance.
- **User Evidence**: The user supplied `review-dimensions.md` and explicitly required checking language bindings, generalizing them, or splitting them into language-specific on-demand subchecklists.
- **Confirmed At**: 2026-10-11

### NEED-009: Automatically implement incremental maintenance suggestions by default

- **Status**: confirmed
- **Statement**: The normal implementation workflow that uses `review-code`, including `implement-tasks`, must automatically implement substantiated pure maintenance suggestions by default. Provide the persistent boolean setting `workflow.auto_maintenance` in `.codexspec/config.yml`, managed through `codexspec config --auto-maintenance on|off` as specified by DEC-009; it defaults to enabled. Implementation callers read this configuration when choosing their automatic repair scope and do not accept a new maintenance invocation argument or per-run override. The policy applies independently of `workflow.auto_next` and does not require parameter support or forwarding in the preceding non-implementation SDD stages. When disabled, continue reviewing and reporting relevant maintenance suggestions while leaving their implementation to the user; actual defect repair remains mandatory. Readability, maintainability, and extensibility are explicit review concerns in the default workflow rather than being reserved for whole-codebase quality assessment.
- **User Evidence**: “增加一个参数来控制是否自动实施纯维护性建议，默认是开启。” The user explained that deferral risks forgotten maintenance, accumulated complexity, and harder concentrated cleanup.
- **Confirmed At**: 2026-10-11

### NEED-010: Keep maintenance timely and grounded in the current increment

- **Status**: confirmed
- **Statement**: Assess maintenance opportunities in the selected change and the structure directly affected by it. Explain the present structural or comprehension problem, the concrete improvement, and the expected readability, maintenance, or extension benefit. Apply incremental improvements during the current workflow rather than defer them until complexity accumulates. A pure maintenance suggestion need not demonstrate a functional defect, but it must have a substantiated benefit and remain consistent with actual requirements, compatibility, and project conventions.
- **User Evidence**: The user described readability, maintainability, and extensibility as the basis of steady long-term iteration and requested immediate incremental maintenance.
- **Confirmed At**: 2026-10-11

## Constraints

### CON-001: Uncertainty alone does not establish a defect or blocking gap

- **Status**: confirmed
- **Statement**: Distinguish evidenced defects, material missing verification, and unsupported assumptions. A blocking gap requires a concrete applicable obligation or risk and missing necessary evidence. Maintenance suggestions require demonstrated structural benefit rather than a claim of functional failure. The inability to prove absolute safety is insufficient. Reject unsupported speculation rather than repeatedly turning it into mandatory repair or verification work.
- **User Evidence**: The user requested avoiding unrealistic boundaries, excessive review, excessive fixes, and excessive defensive programming, and agreed with distinguishing evidence from speculation.

### CON-003: Conditional loading cannot weaken review completeness

- **Status**: confirmed
- **Statement**: Common review discipline and the selected mode's obligations remain mandatory. Conditional loading selects applicable detailed work without narrowing the selected change or suppressing general correctness, relevant risks, required verification, or finding admission. Missing required standards cannot be silently skipped. Assessing every dimension does not require reading every detailed checklist or treating inapplicable items as unverified defects.
- **User Evidence**: The user accepted always-used review discipline, a short applicability assessment across dimensions, on-demand details, and completion checks.

### CON-004: Respect actual language semantics and behavioral contracts

- **Status**: confirmed
- **Statement**: Language-independent checkpoints must not impose a language-specific representation or mechanism on other languages. Language-specific details apply only to affected behavior that depends on them. Nullability, missing keys, ordering, numeric limits, ignored results, and recovery behavior must be evaluated against actual semantics and contracts; universal wording must not create automatic requirements for repetitive defensive checks.
- **User Evidence**: The user explicitly required generalization or language-specific splitting and agreed with applicability based on language semantics and behavior.

### CON-005: The maintenance switch controls optional edits, not defect obligations

- **Status**: confirmed
- **Statement**: Treat automatic maintenance implementation as a configured execution policy read by the command that performs repairs, independently of whether SDD stages advance automatically. Turning it off must not suppress maintenance assessment or reporting, weaken defect admission, skip necessary verification, or waive an actual defect or binding violation. Keep pure maintenance suggestions distinguishable from admitted defects so a maintenance suggestion is not misrepresented as a correctness or security failure.
- **User Evidence**: The user requested a parameter controlling whether suggestions are automatically implemented, while retaining the requirement for thorough, evidence-based defect review.

### CON-006: Complete evidenced review and enabled incremental maintenance with bounded changes

- **Status**: confirmed
- **Statement**: Complete applicable behavior, contract, risk, deterministic verification, and bounded related-occurrence work. Also complete substantiated incremental maintenance when automatic implementation is enabled; when it is disabled, keep the suggestions visible without requiring their automatic application. Require concrete current benefit for maintenance changes, preserve intended behavior and public compatibility, and verify changed code before accepting completion. End review once applicable obligations are complete; expand work only for new evidenced dependencies, risks, or relevant maintenance needs. Neither maintenance benefits nor defect repairs justify invented future requirements, unnecessary defensive layers, or unrelated repository-wide cleanup.
- **Replaces**: CON-002.
- **User Evidence**: The initial request rejected excessive review and excessive fixes; the later instruction explicitly added immediate automatic incremental maintenance by default.

### CON-007: Avoid premature checklist fragmentation

- **Status**: confirmed
- **Statement**: Use independently useful loading units for the initial standard library: one index, one common-rules file, one file per review mode, one file per general dimension, and initially one file per supported language or framework. Keep technical topics such as authentication, authorization, transactions, caches, uploads, and language-specific error or collection handling as sections in their corresponding files. Split a topic into a separate file only when it has grown into a substantial independent review theme and its current organization repeatedly loads unrelated content. Do not pre-create a separate file for each checkpoint or topic, and do not impose an arbitrary line-count threshold for further splitting.
- **User Evidence**: The user raised concern that the original fine-grained tree was over-split and explicitly approved the simpler layout with “很好，就按照这个方案”.
- **Confirmed At**: 2026-10-11

## Decisions

### DEC-001: Combine mandatory discipline with conditionally loaded detail

- **Status**: confirmed
- **Decision**: Every review uses common discipline and its selected mode's procedure. General checkpoints are chosen for affected behavior. Language, framework, and technical-topic subchecklists supply relevant implementation-specific detail.
- **Alternatives Rejected**: Load every language and technical checklist in every invocation; use maintainer-only fragment expansion as the sole solution to execution-context size.
- **Reason**: Preserve systematic review while reducing unrelated context and enabling standards to grow independently.
- **User Evidence**: The user explicitly agreed with this loading distinction and procedure.

### DEC-002: Determine review direction per change and reuse dimensions and checkpoints

- **Status**: confirmed
- **Decision**: Generate review direction from the current change's behavior and contracts. Reuse dimensions as perspectives and checkpoints as concrete questions. Use a lightweight index to find applicable standards; allow requirement obligations to activate checks even when code is missing.
- **Reason**: A fixed universal checklist cannot alone identify the specific behavior that matters in each change, and implementation-only detection would miss omitted required behavior.
- **User Evidence**: The user agreed with the behavior map, dimension applicability assessment, semantic selection, and missing-implementation example.

### DEC-003: Resolve uncertain applicability through bounded inspection

- **Status**: confirmed
- **Decision**: When applicability is uncertain, inspect directly relevant input sources, callers, dependency configuration, or runtime semantics before deciding. Report a gap only when a material required verification cannot be completed. Continue loading when tracing reveals additional evidence.
- **Reason**: Avoid both premature exclusion of relevant work and indiscriminate activation of hypothetical risks.
- **User Evidence**: The user agreed with bounded applicability inspection and gap reporting tied to necessary evidence.

### DEC-004: Include maintenance suggestions in default review and automate them during implementation

- **Status**: confirmed
- **Decision**: Default change review includes pure maintenance suggestions, and the implementation workflow applies substantiated incremental suggestions by default according to the persistent project setting defined by DEC-009. Review remains an assessment step; the implementation caller owns edits. The maintenance policy does not change which actual defects must be repaired.
- **Alternatives Rejected**: Reserve pure maintenance advice for a separate whole-codebase quality assessment or require users to remember to perform all maintenance later.
- **Reason**: Continuous small improvements preserve readability, maintainability, and extensibility and avoid accumulated complexity and difficult concentrated cleanup.
- **User Evidence**: Explicit instruction that automatic implementation defaults to enabled because delayed suggestions can be forgotten.
- **Confirmed At**: 2026-10-11

### DEC-006: Use a compact shared runtime resource directory with explicit source and install paths

- **Status**: confirmed
- **Decision**: Maintain the review resources in `templates/review-code/` and install the same resource tree into the selected user project's `.codexspec/review-code/` through `codexspec init`. Claude commands and Codex skills share that installed resource tree. Installing the CLI tool alone must not create these project files; project initialization or installation update performs the copy.
- **Initial Resource Layout**:

```text
templates/review-code/
├── index.md
├── common.md
├── change-review.md
├── quality-assessment.md
├── dimensions/
│   ├── logic.md
│   ├── business-semantics.md
│   ├── security.md
│   ├── concurrency.md
│   ├── robustness.md
│   ├── performance.md
│   └── maintainability.md
├── languages/
│   ├── go.md
│   ├── python.md
│   └── ... (files for the actually supported languages)
└── frameworks/
    └── react.md
```

- **File Responsibilities**: `index.md` is the lightweight applicability and location index; `common.md` contains mandatory review discipline; `change-review.md` contains the default selected-change review procedure and output obligations; `quality-assessment.md` contains the separate whole-codebase quality assessment procedure, scoring rules, and output obligations. Dimension files provide language-independent checkpoints. Language and framework files provide their specific semantics. Technical-topic sections follow CON-007 rather than requiring initial `topics/`, per-language subdirectories, or a separate scoring file.
- **Source and Derived Paths**: Keep the main command's authoritative source at `internal/command_templates/sources/review-code.md`, render its complete distribution entry to `templates/commands/review-code.md`, and maintain the separate resource files directly under `templates/review-code/`. In initialized projects, the platform entries are `.claude/commands/codexspec/review-code.md` and/or `.agents/skills/codexspec-review-code/SKILL.md`, according to the enabled platform. The CodexSpec repository's own `.codexspec/review-code/` and platform entries are derived self-bootstrap installation copies, just as in user projects; they are not additional maintenance sources.
- **Reason**: Make the maintainer-to-user mapping explicit, share runtime standards across supported platforms, enable dimension and language selection, and limit file and reference overhead in the initial library.
- **User Evidence**: After seeing the compact tree for both the CodexSpec repository and an initialized user project, the user explicitly approved it with “很好，就按照这个方案”.
- **Confirmed At**: 2026-10-11

### DEC-009: Manage persistent maintenance configuration through config and read it at repair time

- **Status**: confirmed
- **Decision**: Add the independent boolean `workflow.auto_maintenance` to `.codexspec/config.yml`. It defaults to `true`, including when absent from an existing project's configuration. Manage it persistently through `codexspec config --auto-maintenance on|off`, following the existing configuration-management model of `auto-next`. Use `on/off` as canonical parameter values in help, documentation, and examples. Retain the accepted aliases `on/true/1/yes` and `off/false/0/no`, with consistent case and surrounding-whitespace handling; store the value as an unquoted YAML boolean and use boolean internal state.
- **Execution Scope**: `implement-tasks` and other commands that invoke `review-code` and automatically repair findings read the selected project's maintenance configuration when deciding whether substantiated pure maintenance suggestions join the automatic repair scope. When enabled, include these suggestions; when disabled, continue reporting them without automatically applying them. Actual defect repair and necessary verification remain mandatory.
- **Interface Boundary**: Do not add an `--auto-maintenance` invocation argument to `implement-tasks` or the other implementation scenario commands. They consume configuration rather than receive the configuration setter parameter. No per-run override or "invocation parameter > configuration > default" hierarchy is part of this feature. Non-implementation SDD stages do not parse or forward the setting, and read-only `review-code` continues assessing and reporting maintenance suggestions without performing edits.
- **Independence**: `workflow.auto_next` controls only automatic advancement between SDD stages. `workflow.auto_maintenance` controls only the inclusion of pure maintenance suggestions in automatic repair. The latter behaves identically whether an implementation command is invoked manually or reached automatically.
- **Replaces**: DEC-008 and OPEN-003.
- **Reason**: Reuse the project's familiar persistent configuration entry point and keep implementation commands responsible for applying the configured repair policy.
- **User Evidence**: “对，跟 auto-next 一样可以使用 codexspec config 来设置参数。但是不需要implement-tasks来接收参数，在implement-tasks这些会调用review-code的场景命令中增加要求按照 auto-maintenance 来决定是否将维护性建议纳入自动修复范围即可”. The earlier confirmations of the switch name, values, aliases, and default remain effective.
- **Confirmed At**: 2026-10-11

## Out of Scope

### OUT-002: Unsupported defect claims and unnecessary changes

- **Status**: confirmed
- **Statement**: Do not admit defects based only on invented unreachable states or unsupported operating environments, or introduce unsupported product requirements, defensive layers, abstractions, or unrelated broad cleanup. Maintenance improvements are permitted without a functional defect when their current benefit is substantiated under NEED-009 and NEED-010.
- **Replaces**: OUT-001.
- **Reason**: Preserve the original restraint against overreview while allowing the user's requested continuous incremental maintenance.
- **User Evidence**: The user first prohibited fabricated scenarios and excessive fixes, then explicitly requested automatic incremental maintenance.

## Applicable Project Governance

These are inherited project rules, not new user decisions:

- `.codexspec/memory/constitution.md` and `docs/internal/repository-layout.md` govern authoring and distribution boundaries. Edit authoritative command sources, not installed command or skill copies.
- Vetted profile constraint `C-2026-0902-054178-1` requires maintainer validation before user installation or execution can expose authoring/distribution mechanism errors. User-facing standards must ship as complete usable resources; internal fragment sources and maintainer tools do not become runtime dependencies.
- Candidate pitfall `P-2026-0829-0035hy-3` recommends validating the semantic premise of review evaluation cases rather than accepting generic counts or empty structural records. Use it cautiously as supporting validation guidance.
- Candidate pitfall `P-2026-1003-204985-2` warns that artifact, installer, index, and other secondary destinations must use the same selected workspace as primary writes.

## Open Questions

### OPEN-002: Choose implementation details for standard organization

- **Status**: open
- **Question**: Which index representation, installation/update implementation across supported delivery channels, runtime maintenance-policy handling, and report representation best satisfy conditional loading and default automatic incremental maintenance?
- **Why It Matters**: These are implementation design choices. DEC-009 resolves the persistent maintenance setting, its config setter, and its consumption by repair callers. DEC-006 and CON-007 resolve the maintained and installed paths, initial file organization, and splitting policy. Design must choose the index format, resource installation and resolution details (including plugin-only delivery), runtime configuration reading, and safe consumption of maintenance suggestions, including any versioned report changes. It must not add implementation invocation arguments or per-run overrides, reintroduce whole-chain parameter propagation, reopen the confirmed names or organization, or expand product scope. No numeric size target or new plugin mechanism has been confirmed.
- **Blocks Specification Generation**: No; choose and justify them during design without expanding product scope.
- **Owner**: Design

## Superseded Entries

### DEC-008: Keep confirmed maintenance semantics separate from its unconfirmed setting interface

- **Status**: superseded
- **Decision**: Retain the agreed switch name `--auto-maintenance`, canonical values `on/off`, and default-enabled maintenance behavior. Retain the accepted aliases `on/true/1/yes` and `off/false/0/no`, with the existing switches' case and whitespace handling; any YAML or internal policy representation uses booleans. The user-facing entry point for changing this setting is addressed separately by OPEN-003 and must not be inferred from the word "parameter".
- **Execution Scope**: The implementation caller uses the resolved maintenance policy when deciding whether substantiated pure maintenance suggestions join automatic repair. This applies to `implement-tasks` and other direct repair callers, regardless of whether they are invoked manually or reached automatically. `workflow.auto_next` controls only SDD stage advancement. Read-only `review-code` continues assessing and reporting relevant maintenance suggestions, and switching maintenance off does not waive actual defect repair or necessary verification.
- **Stage Boundary**: The non-implementation SDD stages do not need to parse or forward the maintenance setting. Applying a policy during implementation does not imply that the implementation command accepts a new invocation flag, nor does it establish a per-run override mechanism.
- **Replaces**: DEC-007.
- **Reason**: Preserve the user's confirmed intent while preventing an inferred control interface or override scenario from becoming downstream authority.
- **User Evidence**: The user confirmed the maintenance name, values, and default; distinguished repair policy from `auto-next`; then questioned the source of the proposed per-run input: “是怎么传入，从哪里传入，我怎么没有印象这种用法？还是说是你推理出的这个场景？”
- **Confirmed At**: 2026-10-11
- **Replaced By**: DEC-009. The maintenance semantics are retained; the setting entry point is now explicitly resolved as persistent project configuration.

### OPEN-003: Confirm where users set automatic maintenance

- **Status**: superseded
- **Question**: Should automatic maintenance be a persistent project setting managed through the existing configuration interface, with implementation callers reading it, rather than a new per-run implementation argument?
- **Proposed Choice**: Add the independent boolean `workflow.auto_maintenance` to `.codexspec/config.yml`, defaulting to `true`. Support persistent changes through `codexspec config --auto-maintenance on|off` and the existing interactive `codexspec:config` workflow. Implementation callers read the project setting; no per-run override is part of this proposed scope.
- **AI Assumptions Not Confirmed**: The earlier example of supplying `--auto-maintenance off` to `implement-tasks`, the idea that it temporarily overrides configuration, and the precedence rule "invocation parameter > configuration > default" were assistant inferences, not existing behavior or confirmed requirements. The proposed YAML key and persistent management entry also require user confirmation before they become binding.
- **Verified Current Behavior**: `.codexspec/config.yml` contains `workflow.auto_next` and `workflow.auto_distill`; no `auto_maintenance` option is implemented in the CLI or `implement-tasks` command source. Existing `codexspec config --auto-next on|off` changes the persistent project setting.
- **Blocks Specification Generation**: Yes, until the user confirms the maintenance setting interface. Do not infer this product decision during design.
- **Owner**: User
- **Replaced By**: DEC-009. Persistent configuration and the config setter are confirmed; this question no longer blocks specification generation.

### DEC-007: Apply the maintenance switch at automatic repair callers independently of stage advancement

- **Status**: superseded
- **Decision**: Name the invocation parameter `--auto-maintenance`. Use `on` and `off` as the canonical values in help, documentation, examples, and automatic repair invocations; default to `on`. Accept the existing switch aliases: `on`, `true`, `1`, and `yes` enable automatic maintenance; `off`, `false`, `0`, and `no` disable it. Parse these values consistently with existing switches, including case-insensitive matching and surrounding-whitespace handling. Represent any YAML configuration or internal state for this policy as a boolean `true` or `false`; this does not prescribe a new configuration key or storage mechanism.
- **Execution Scope**: The parameter belongs to `implement-tasks` and any other command that directly invokes `review-code` and performs automatic repairs. The implementation caller consults it when deciding whether substantiated pure maintenance suggestions join the automatic repair scope. Its semantics and default apply identically whether that caller is invoked manually or reached automatically. `workflow.auto_next` controls only advancement between SDD stages and does not enable, disable, or otherwise change this repair policy.
- **Stage Boundary**: Do not require `specify`, `generate-spec`, `spec-to-design`, `design-to-plan`, or `plan-to-tasks` to parse or forward this parameter through the SDD chain. Read-only `review-code` does not own this execution switch and continues assessing and reporting relevant maintenance suggestions regardless of whether the implementation caller applies them. Turning the switch off does not waive actual defect repair or necessary verification under CON-005.
- **Replaces**: DEC-005.
- **Reason**: Keep the repair policy with the command that edits code, retain the existing switch-value convention, and keep stage advancement independent of repair scope.
- **User Evidence**: “不应该只是在implement-tasks这种会触发review-code并且自动修复的环节中根据这个参数来考虑是否要将维护性建议纳入自动修复范围吗？”; “auto-next只是用来控制各个sdd环节是否自动推进的”. The earlier confirmations of the name, canonical values, aliases, and default remain effective.
- **Confirmed At**: 2026-10-11
- **Replaced By**: DEC-008 and OPEN-003. The repair policy and switch-value convention are retained; a direct `implement-tasks` invocation flag and per-run configuration override are not confirmed interfaces.

### DEC-005: Use the existing switch-value convention for automatic maintenance

- **Status**: superseded
- **Decision**: Name the invocation parameter `--auto-maintenance`. Use `on` and `off` as the canonical values in help, documentation, examples, and automated stage handoffs; default to `on`. Accept the existing switch aliases: `on`, `true`, `1`, and `yes` enable automatic maintenance; `off`, `false`, `0`, and `no` disable it. Parse these values consistently with existing switches, including case-insensitive matching and surrounding-whitespace handling. Represent any YAML configuration or internal state for this policy as a boolean `true` or `false`; this does not prescribe a new configuration key or storage mechanism.
- **Flow Requirement**: A value selected at the workflow entry must be preserved throughout `auto-next` until the implementation caller applies it. Forward the normalized `on` or `off` value; subsequent stages must not silently replace an explicit `off` with the default `on`. Parameter naming and user-facing value semantics are resolved during requirements discovery rather than left for design-stage clarification. Review remains read-only, and CON-005 governs the distinction between automatic edits, maintenance reporting, and mandatory defect repair.
- **Reason**: Match the documented `on/off` convention and accepted aliases of `--auto-next`, `--auto-distill`, and `--worktrees` so users can reuse one switch-value convention.
- **User Evidence**: The user requested deciding the name before design because the flow uses `auto-next`, then requested consistent values for switches and explicitly replied “同意” to the proposed `on/off` convention, existing aliases, boolean state representation, and normalized `auto-next` forwarding.
- **Confirmed At**: 2026-10-11
- **Replaced By**: DEC-007. The switch name, values, aliases, and default are retained; the requirement to carry it through all `auto-next` stages is withdrawn.

### CON-002: End review after applicable obligations are complete

- **Status**: superseded
- **Statement**: Complete applicable behavior, contract, risk, deterministic verification, and bounded related-occurrence work. Once that work is complete, end the review. Expand scope only for a new evidenced dependency or risk, not to keep finding hypothetical defects. Repair guidance describes the violated behavior or guarantee and does not require unsupported abstractions, redundant guards, or defensive layers.
- **User Evidence**: The user accepted completion criteria and repair guidance proportionate to demonstrated problems.
- **Replaced By**: CON-006.

### OUT-001: Fabricated scenarios and repairs without demonstrated need

- **Status**: superseded
- **Statement**: Do not admit defects based solely on invented unreachable states or unsupported operating environments, or demand fixes and defensive layers without a demonstrated violated obligation and impact.
- **Reason**: Such findings create excessive review and unnecessary changes.
- **User Evidence**: “避免捏造不会出现在真实场景的边界情况而过度review导致过度修复过度防御。”
- **Replaced By**: OUT-002.

### OPEN-001: Finalize the audit scope and treatment of maintenance advice

- **Status**: superseded
- **Question**: Does this feature primarily improve the default defect gate while separating audit content, preserving the existing audit scoring model, and placing purely advisory maintenance suggestions in audit?
- **Proposed Choice**: Yes. Share relevant evidence and applicability discipline, split audit procedures and scoring from default review, and retain audit's scoring model in this feature. Pure maintenance advice belongs in audit; a demonstrated behavior defect or violation of a binding obligation uses normal defect admission.
- **Why It Matters**: The user confirmed review goals and selection behavior but has not explicitly confirmed the final scope choice covering audit scoring and advice routing. This is a proposed decision, not a confirmed requirement.
- **Blocks Final Specification**: Yes, until the final scope summary is confirmed or corrected.
- **Owner**: User
- **Replaced By**: NEED-009, DEC-004.

## Confirmation Log

### Review discipline topic — 2026-10-10

- **Summary Presented**: Behavior-oriented direction, complete traces, reachable defect evidence, contrary-evidence checks, material uncertainty, and bounded completion.
- **User Confirmation**: “对，你说的有道理。” The user additionally requested splitting review standards for on-demand loading and expansion.
- **Entries Confirmed**: NEED-001, NEED-002, NEED-003, NEED-004, CON-001, CON-002, OUT-001.

### Checklist input — 2026-10-10 to 2026-10-11

- **Summary Presented**: Use the user-supplied checklist as input, inspecting and generalizing language bindings or extracting language-specific subchecklists.
- **User Confirmation**: Explicit instruction to integrate the supplied checklist and check language-specific descriptions.
- **Entries Confirmed**: NEED-008 and the language-generalization boundary in CON-004.

### Conditional loading topic — 2026-10-11

- **Summary Presented**: Always use common discipline and the selected mode; choose general checkpoints from affected behavior; use a lightweight index, a dimension applicability assessment, semantic language/topic selection, incremental expansion during tracing, missing-obligation activation, and bounded investigation of uncertain applicability.
- **User Confirmation**: “同意。”
- **Entries Confirmed**: NEED-005, NEED-006, NEED-007, CON-003, CON-004, DEC-001, DEC-002, DEC-003.
- **Final Stage Confirmation**: Pending. This topic confirmation does not trigger `auto_next`.

### Automatic incremental maintenance — 2026-10-11

- **Summary Presented**: Default implementation review evaluates maintenance alongside actual defects; a parameter controls automatic application of pure maintenance suggestions.
- **User Confirmation**: “增加一个参数来控制是否自动实施纯维护性建议，默认是开启。” The user explicitly required timely incremental improvements for readability, maintainability, and extensibility.
- **Entries Confirmed**: NEED-009, NEED-010, CON-005, CON-006, DEC-004, OUT-002.
- **Entries Superseded**: CON-002 and OUT-001 are replaced to allow substantiated maintenance without claiming a functional defect. The unconfirmed audit-only scope proposal OPEN-001 is replaced by NEED-009 and DEC-004.
- **Final Stage Confirmation**: Pending. This is a confirmed scope change, not confirmation of the final combined stage summary.

### Maintenance parameter and consistent switch values — 2026-10-11

- **Summary Presented**: Use `--auto-maintenance on|off`, default `on`; document and forward `on/off`, accept the existing switch aliases, and represent YAML/internal policy state as a boolean. Preserve the selected value along `auto-next` until implementation.
- **User Confirmation**: “同意” after the user requested consistent switch values and the proposed convention was checked against existing parameters.
- **Entries Confirmed**: DEC-005; NEED-009 now references the resolved parameter contract.
- **Open Question Updated**: OPEN-002 retains only implementation details and does not defer parameter naming or user-facing values.
- **Final Stage Confirmation**: Pending. This confirms parameter behavior, not the final combined discovery summary.

### Compact checklist organization and source-to-install mapping — 2026-10-11

- **Summary Presented**: Maintain independent review resources under `templates/review-code/`; initialize them into `.codexspec/review-code/` for shared Claude/Codex use. Use four top-level Markdown files, seven dimension files, and initially one file per language or framework. Keep technical topics as sections and split further only when justified by an independent theme and recurring unrelated loading. Show the main-command source, distribution entry, and derived self-bootstrap and user-project copies explicitly.
- **User Confirmation**: “很好，就按照这个方案”.
- **Entries Confirmed**: CON-007 and DEC-006; NEED-005 now references their granularity and layout rules.
- **Open Question Updated**: OPEN-002 retains implementation mechanics only; runtime paths and initial organization are no longer deferred.
- **Final Stage Confirmation**: Pending. This approves the directory-organization topic; the final combined discovery summary has not yet been explicitly confirmed.

### Maintenance repair policy is independent of automatic stage advancement — 2026-10-11

- **Summary Corrected**: `--auto-maintenance on|off` controls whether pure maintenance suggestions join the automatic repair scope of `implement-tasks` and other direct repair callers. `workflow.auto_next` controls only stage advancement. Manual and automatic invocation use the same maintenance semantics and default. Preceding non-implementation stages do not need to parse or forward the parameter, and read-only review continues reporting maintenance suggestions.
- **User Correction**: The user explicitly separated the implementation repair policy from SDD stage advancement: “auto-next只是用来控制各个sdd环节是否自动推进的”.
- **Entries Confirmed**: DEC-007; NEED-009 and CON-005 clarify the execution boundary.
- **Entry Superseded**: DEC-005. Its name, values, aliases, and default are retained by DEC-007; its whole-chain forwarding requirement is withdrawn.
- **Open Question Updated**: OPEN-002 no longer includes maintenance-policy handoff across SDD stages.
- **Final Stage Confirmation**: Pending. The final combined summary must reflect this correction.

### Setting interface and per-run override assumptions — 2026-10-11

- **Issue Raised**: The user asked where the proposed one-run `--auto-maintenance off` input comes from and whether the scenario was inferred.
- **Authority Correction**: Remove the inferred direct implementation flag and per-run override from binding requirements. Preserve confirmed behavior, name, values, default, and independence from `auto-next` in DEC-008; retain the earlier DEC-007 as superseded.
- **Question Added**: OPEN-003 proposes using persistent project configuration and existing configuration-management commands. Its configuration key, entry point, and absence of a per-run override await user confirmation.
- **Final Stage Confirmation**: Pending; OPEN-003 must be resolved before the final combined summary can authorize specification generation.

### Persistent configuration entry and implementation consumption — 2026-10-11

- **Summary Confirmed**: Manage `workflow.auto_maintenance` in `.codexspec/config.yml` through `codexspec config --auto-maintenance on|off`, default enabled. Commands that invoke review and perform automatic repairs read the setting to decide whether maintenance suggestions enter automatic repair. They do not accept a maintenance invocation argument, and no per-run override is introduced. Stage advancement remains independently controlled by `workflow.auto_next`.
- **User Confirmation**: “对，跟 auto-next 一样可以使用 codexspec config 来设置参数。但是不需要implement-tasks来接收参数，在implement-tasks这些会调用review-code的场景命令中增加要求按照 auto-maintenance 来决定是否将维护性建议纳入自动修复范围即可”.
- **Entry Confirmed**: DEC-009; NEED-009, CON-005, and DEC-004 reference or clarify the persistent configuration contract.
- **Entries Superseded**: DEC-008 and OPEN-003. The setting interface is resolved and no longer blocks specification generation.
- **Remaining Open Item**: OPEN-002 contains non-blocking implementation choices only.
- **Final Stage Confirmation**: Pending. The combined final summary must use this confirmed configuration contract.

### Requirements handoff for user review — 2026-10-11

- **User Instruction**: “写入requirements文档，先不要推进，我检查完毕之后会告诉你按照auto-next继续”.
- **Recorded State**: All confirmed review, checklist integration, compact layout, and persistent maintenance-configuration requirements are saved in this document. OPEN-002 contains non-blocking implementation choices only.
- **Advancement State**: Hold at the requirements stage for user inspection. Do not generate `spec.md` or invoke any downstream SDD stage during this handoff. Keep the existing `workflow.auto_next` configuration unchanged; wait for the user's post-review instruction to continue.
- **Final Stage Confirmation**: Pending user review and continuation instruction.

### Final Stage Confirmation (2026-10-11)

The user reviewed the effective requirements summary and confirmed: “确认，按照auto-next自主推进流程”. All current confirmed entries remain effective; OPEN-002 remains a non-blocking design choice. Continue the same feature workspace through the configured SDD chain.
