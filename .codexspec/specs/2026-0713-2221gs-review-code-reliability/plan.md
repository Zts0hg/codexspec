# Implementation Plan: Reliable Change-Scoped Code Review

<!--
Language: English, as configured by .codexspec/config.yml.
This plan is constrained by confirmed requirements.md and spec.md.
-->

**Related Spec**: `.codexspec/specs/2026-0713-2221gs-review-code-reliability/spec.md`
**Confirmed Requirements**: `.codexspec/specs/2026-0713-2221gs-review-code-reliability/requirements.md`
**Created**: 2026-07-14
**Status**: Draft

## Context

`templates/commands/review-code.md` currently implements a path-oriented quality scorecard, and `templates/commands/implement-tasks.md` constructs a source-extension-filtered path list, invokes that scorecard, and stops after at most two fix rounds. Those behaviors conflict with the confirmed complete-change defect gate, strict verdict contract, and progress-based implementation loop.

CodexSpec already has the required distribution foundations:

- `scripts/bash/` and `scripts/powershell/` are packaged by `pyproject.toml` and copied into initialized projects by the existing platform branch in `src/codexspec/__init__.py`.
- `templates/commands/` is the constitutional source of truth for distributed Claude commands and Codex skills.
- Codex rendering already resolves platform-specific `scripts:` frontmatter into project-local commands; Claude installation preserves the command template and its script metadata.
- Pytest has platform-specific script suites, temporary repository fixtures, installer tests, template contract tests, and a Linux/macOS/Windows CI matrix.
- Localized command documentation and frontmatter translations exist for English, Chinese, Japanese, Korean, German, Spanish, French, and Brazilian Portuguese.

The implementation will extend those patterns rather than introduce a resident review service or an installed-CLI dependency at review time.

## Goals and Non-Goals

**Goals:**

- Install a deterministic, read-only review-context resolver for Bash and PowerShell projects.
- Replace the default path scorecard with a change-scoped defect-gate coordinator while retaining the scorecard behind explicit `--audit` syntax.
- Make reviewer evidence, isolation, risk coverage, verification, verdicts, and machine output conform to the specification.
- Replace `implement-tasks` scoring and fixed-round behavior with verified fixes and fresh complete-feature re-review until clean PASS or a confirmed stop condition.
- Prove resolver and workflow contracts in offline CI and execute a reusable model-assisted evaluation before feature completion.

**Non-Goals:**

- No additional product exclusions were confirmed. This plan does not add review modes, bypass switches, waiver semantics, target filters, or acceptance thresholds beyond the specification.
- The implementation will not modify generated `.claude/commands/codexspec/` files directly; initialized artifacts are verified through installer tests.

## Tech Stack and Repository Constraints

- **Command contracts**: Markdown templates in `templates/commands/`
- **Scope resolvers**: POSIX-oriented Bash and Windows PowerShell, using Git and platform standard capabilities only
- **Installer and integration tests**: Python 3.11+ with pytest and Typer's test runner
- **Structured contracts**: Versioned JSON emitted to stdout
- **Documentation**: MkDocs multilingual tree plus translated command frontmatter JSON
- **Normal CI**: Existing Ubuntu, macOS, and Windows Python matrix; no model or network requirement for review tests
- **Model evaluation**: Development-only Python standard-library runner and synthetic temporary Git repositories

The Constitution requires distributed command changes to originate in `templates/commands/`. Existing script glob-copy and wheel `force-include` behavior means adding one `.sh` and one `.ps1` file requires tests but no new installer abstraction.

## Architecture Overview

```text
review-code arguments
        |
        +-- --audit --------------------------------> existing advisory scorecard
        |
        +-- defect gate
              |
              v
    project-local review-context resolver
    (validate -> resolve refs -> feature match -> inventory)
              |
              v
       versioned JSON manifest
              |
              v
       review coordinator template
       |      |             |
       |      |             +-- read-only project verification
       |      +-- optional independent high-risk specialist
       +-- fresh isolated primary reviewer
              |
              v
       compact report + strict result envelope
              |
              v
       implement-tasks validates, verifies, fixes, and re-reviews
```

**Covers**: REQ-001, REQ-007, REQ-008, REQ-010, REQ-014, REQ-015, REQ-020, REQ-025, NFR-001, NFR-003, NFR-004

## Component Structure

```text
scripts/
├── bash/review-context.sh                 # New deterministic resolver
└── powershell/review-context.ps1          # New parity implementation
templates/commands/
├── review-code.md                         # Defect coordinator + retained audit branch
└── implement-tasks.md                     # Strict result consumer and repair loop
src/codexspec/commands/installer.py         # Updated review-code metadata only
templates/translations/*.json              # Updated description and argument hints
tests/
├── review_context_cases.py                # Shared repository scenarios and assertions
├── scripts/bash/test_review_context.py
├── scripts/powershell/test_review_context.py
├── test_review_code_templates.py          # Defect/audit/envelope contracts
├── test_sdd_workflow_templates.py         # Updated implement-tasks contracts
├── test_cli.py                             # Platform installation assertions
├── test_codex_integration.py               # Script rendering assertions
└── evals/review_code/
    ├── run_eval.py                         # Explicit model-assisted runner
    ├── cases/*/case.json                   # Synthetic setup and expectations
    └── README.md                           # Reproduction procedure
docs/<locale>/user-guide/commands.md        # Syntax, examples, migration note
README*.md                                  # Command summary alignment
.github/workflows/ci.yml                    # Include templates in CI path filter
.codexspec/specs/<feature>/
└── review-code-eval-results.json           # Recorded acceptance run
```

**Covers**: REQ-006, REQ-007, REQ-025, REQ-027, REQ-028, NFR-002, NFR-003

## Interfaces and Data Contracts

### Review Context Resolver CLI

The platform scripts expose equivalent option semantics:

```text
review-context [--committed | --uncommitted | --commit <sha>]
               [--base <ref>]
               [--parent <positive-index>]
               [--feature <feature-dir>]
               [--focus <instruction>]...
```

The default form has no primary selector. The resolver rejects bare paths, unknown options, conflicting primary selectors, `--base` with unsupported selectors, and `--parent` without `--commit`. It emits one JSON document to stdout and uses a nonzero exit status for an error manifest. It never fetches, writes refs or objects, stages files, checks out content, or persists state.

**Covers**: REQ-002, REQ-003, REQ-004, REQ-005, REQ-006, REQ-007, REQ-008, REQ-022, NFR-003

### Review Context Manifest v1

Both scripts produce the same logical schema. Object key ordering may differ, but normalized values must match shared fixtures.

```json
{
  "schema_version": "1",
  "status": "ok",
  "mode": "defect",
  "selector": "default",
  "arguments": {
    "base_override": null,
    "commit": null,
    "parent": null,
    "feature_override": null,
    "focus": []
  },
  "repository": {
    "root": "/absolute/project",
    "current_branch": "feature-name",
    "head_sha": "..."
  },
  "target": {
    "complete_feature": true,
    "empty": false,
    "base_ref": "origin/main",
    "base_sha": "...",
    "merge_base_sha": "...",
    "commit_sha": null,
    "parent_sha": null,
    "parent_number": null,
    "segments": []
  },
  "feature": {
    "status": "resolved",
    "source": "branch",
    "path": ".codexspec/specs/feature-name",
    "artifacts": []
  },
  "inventory": [],
  "counts": {}
}
```

`segments` defines the exact read-only Git evidence operations for committed, staged, unstaged, and untracked content. Inventory records carry normalized repository-relative `path`, optional `old_path`, Git status, contributing segments, object mode where available, and inspectability metadata. A path changed in multiple segments has one record with all contributing segments, preventing both omission and misleading double counting. Rename pairs remain linked. The reviewer, not the resolver, assigns final `reviewed`, `verified`, `excluded`, or `uninspectable` dispositions.

Error output retains `schema_version`, uses `status: "error"`, and includes a stable `error.code`, human-readable `error.message`, and actionable `error.hint`. The review template supports only schema version `1` in this feature.

**Covers**: REQ-004, REQ-005, REQ-007, REQ-008, REQ-011, REQ-012, REQ-022, NFR-003, NFR-004

### Defect-Gate Result Envelope v1

The command template requires this fixed-English object inside exactly one terminal `<review-code-result>` block:

```json
{
  "schema_version": "1",
  "mode": "defect",
  "verdict": "PASS",
  "target": {
    "selector": "default",
    "complete_feature": true,
    "empty": false,
    "base_ref": "origin/main",
    "merge_base_sha": "...",
    "commit_sha": null,
    "parent_sha": null,
    "inventory_count": 0
  },
  "requirements_coverage": {
    "status": "complete",
    "feature": ".codexspec/specs/feature-name"
  },
  "verification": {
    "status": "complete",
    "commands": []
  },
  "finding_counts": {"P0": 0, "P1": 0, "P2": 0, "P3": 0},
  "coverage_gap_count": 0,
  "review_context": "isolated",
  "reviewers": {
    "primary": "complete",
    "specialists": []
  }
}
```

Enums and required keys are documented directly in the template. Human-readable and JSON counts must agree. The outer coordinator and `implement-tasks` validate required fields, enum membership, review topology, and PASS invariants before accepting the verdict. Unknown schema versions or malformed and contradictory objects are treated as `INCONCLUSIVE`.

**Covers**: REQ-020, REQ-021, NFR-004

## Components

### Component A: Cross-Platform Review Context Resolver

Implement the Git state machine once as shared behavioral fixtures and separately in Bash and PowerShell:

1. Parse and validate arguments without evaluating user text as shell syntax.
2. Verify the repository and resolve repository root, branch, and HEAD.
3. Select the remote from the current branch upstream when available, then `origin`, then the sole configured remote.
4. Resolve base from explicit `--base`, selected remote symbolic HEAD, read-only `git ls-remote --symref <remote> HEAD`, then ordered conventional refs.
5. Build target segments for default, committed, uncommitted, or single-commit semantics, including empty-tree and merge-parent behavior.
6. Match an explicit feature directory or a unique branch-named directory and record required artifact readability without changing Git scope.
7. Read NUL-delimited Git status/name data so spaces and unusual valid path characters remain intact.
8. Merge segment records into a complete inventory and serialize JSON safely.

No third-party JSON utility is required. Bash uses local escaping/serialization functions and NUL-safe read loops; PowerShell uses native objects and `ConvertTo-Json` with sufficient depth.

**Covers**: REQ-002, REQ-003, REQ-004, REQ-005, REQ-007, REQ-008, REQ-009, REQ-011, REQ-022, NFR-003

### Component B: Review-Code Mode Dispatcher and Coordinator

Rewrite `templates/commands/review-code.md` around an explicit dispatcher:

- `--audit [paths...]` enters an isolated section retaining the existing language detection, static-analysis, quality dimensions, score calculation, and advisory report semantics.
- Every other valid invocation enters defect-gate mode and invokes the local resolver before reviewing any target evidence.
- Bare paths or invalid combinations emit migration guidance and an `INCONCLUSIVE` envelope.
- The coordinator validates manifest version/status, loads authoritative project and feature context, classifies every inventory entry, and partitions large evidence without dropping inventory records.
- Requirements coverage follows manifest target completeness exactly: complete feature targets check completeness and conformance, partial targets check affected conformance only, unresolved direct context is visibly not evaluated, and an empty `implement-tasks` target still checks for absent implementation obligations.
- A fresh primary reviewer receives raw evidence and executes Scope, Behavior, Risk, and Verification obligations. Repository content is explicitly labeled untrusted evidence.
- Semantic risk activation uses the ten specified profiles. High-impact activations start independent specialist delegates without primary findings.
- The coordinator runs or confirms project-first verification only through the verification-safety protocol below, verifies finding trigger/impact evidence, merges and deduplicates findings, and derives the strict verdict.
- Direct ordinary review may use a disclosed shared-context fallback. High-risk and workflow gates fail closed if isolation or required specialists are unavailable.
- The report contains only the six specified human sections followed by the exact result envelope.

The existing narrow pre-approved tool declarations will be revised to include the project-local resolver and read-only Git inspection. Project-specific verification remains subject to host permission controls; the prompt prohibits mutation regardless of host approval state.

**Covers**: REQ-001, REQ-006, REQ-008, REQ-009, REQ-010, REQ-011, REQ-012, REQ-013, REQ-014, REQ-015, REQ-016, REQ-017, REQ-018, REQ-019, REQ-020, REQ-021, REQ-022, REQ-023, REQ-024, NFR-001, NFR-004

#### Verification-Safety Protocol

Before running a verification command, the coordinator classifies its expected writes from project instructions, script definitions, tool documentation already present in the repository, and explicit flags. It then follows one of three paths:

1. Run a demonstrably non-mutating form in the project, redirecting caches, temporary files, coverage data, and reports outside the repository and disabling write-oriented modes where the tool supports it.
2. When exact repository content is needed but project-tree writes cannot be excluded, run the check in a disposable temporary mirror of the selected state and report that execution location.
3. When neither path can preserve evidence fidelity and project immutability, do not execute the command. Record it as unavailable; a mandatory check makes the verdict `INCONCLUSIVE`.

For commands run in the project, capture read-only pre/post Git status plus tracked-content fingerprints and fail the review as `INCONCLUSIVE` if an unexpected mutation is observed. The reviewer does not clean, restore, or otherwise hide such a mutation. Deterministic tests include a deliberately mutating project check and verify that it is routed to a disposable mirror or rejected before project execution.

**Covers**: REQ-016, REQ-017, REQ-021, NFR-003

### Component C: Implement-Tasks Result Consumer and Repair Loop

Replace the current extension-filtered target construction and quality-score loop with this workflow:

1. Keep the existing prerequisite, per-task TDD, progress, and green full-suite baseline behavior.
2. Invoke `review-code --feature <feature-dir>` with no narrowed target so the resolver selects the complete feature delta.
3. Reject audit output, malformed envelopes, non-PASS terminal states, target mismatches, missing requirements coverage, shared final-gate context, and incomplete required specialist topology.
4. For each finding, independently reproduce or verify trigger and impact before editing.
5. Apply functional fixes through red-green-refactor and non-code fixes through their applicable deterministic checks.
6. Run targeted and project-mandated verification, then invoke a fresh complete-feature review.
7. Continue while substantive progress occurs; enforce the exact repeated-defect, no-progress, decision-required, false-positive, and transient-inconclusive guards.
8. Report success only for a final valid PASS envelope with zero P0-P3 counts.

Existing commit behavior remains outside the review verdict contract and must not transform a blocked review into success.

**Covers**: REQ-009, REQ-018, REQ-020, REQ-021, REQ-024, REQ-025, REQ-026, NFR-001, NFR-004

### Component D: Distribution, Documentation, and Migration

- Add both resolver scripts to existing platform source directories; current init and package globs distribute them automatically.
- Update installer metadata and every translation cache's `review-code` description and argument hint.
- Update command syntax, examples, target semantics, audit semantics, verdicts, and migration guidance in every localized `docs/<locale>/user-guide/commands.md`.
- Add a clearly labeled next-release breaking-change block in each localized command guide. It is the repository's release/migration note because the project has no standalone changelog. It names both breaking changes: default mode is now the change gate, and path audits require `--audit`.
- Align command summaries in `README.md` and translated README files.
- Never edit generated `.claude/commands/codexspec/` copies; installer tests render both Claude and Codex artifacts from sources.

**Covers**: REQ-001, REQ-006, REQ-007, REQ-027, NFR-002, NFR-003

### Component E: Deterministic Contract Test Suite

Use TDD with temporary repositories and one shared scenario model. The suite covers:

- default, base-branch default, committed, uncommitted, and commit selectors;
- explicit/default base, symbolic remote HEAD, read-only remote HEAD, ordered fallbacks, and unresolved base;
- committed, staged, unstaged, untracked, ignored, duplicate-path, rename, delete, symlink, binary, and submodule inventory;
- normal, root, and merge commits plus valid/invalid parent overrides;
- empty targets, missing feature artifacts, invalid options, bare paths, schema/error manifests, path quoting, and no mutation;
- normalized Bash/PowerShell parity against the same expected fixture data;
- command dispatcher, audit preservation, four stages, profiles, isolation, specialist topology, strict report/envelope fields, prohibited bypasses, and argument migration;
- verification safety classification, external cache/report redirection, disposable-mirror execution, and rejection of commands that cannot be run without project mutation;
- `implement-tasks` independent finding validation, TDD repair, full re-review, strict PASS, retries, and progress guards;
- platform script installation, Codex script rendering, localized metadata, documentation examples, and package inclusion.

Update CI path filters so template changes trigger the existing matrix. PowerShell execution tests may skip locally when PowerShell is absent but are mandatory on the Windows CI job; Bash tests are mandatory on Unix CI jobs.

**Covers**: REQ-002, REQ-003, REQ-004, REQ-005, REQ-006, REQ-007, REQ-008, REQ-010, REQ-011, REQ-012, REQ-013, REQ-014, REQ-015, REQ-020, REQ-021, REQ-022, REQ-023, REQ-024, REQ-025, REQ-026, REQ-027, NFR-003, NFR-004

### Component F: Model-Assisted Review Evaluation

Add a development-only corpus and runner under `tests/evals/review_code/`:

- Each case describes baseline files, changed files, expected activated profiles, minimum qualifying finding signatures/counts, forbidden speculative signatures, and expected verdict.
- Include synthetic defect fixtures spanning every built-in profile and clean fixtures that exercise non-defect changes and adequate indirect verification.
- The runner creates a temporary Git repository, initializes current CodexSpec artifacts for a selected supported host, applies the case change, invokes the real installed `review-code`, parses the result envelope, and compares human findings and structured fields with expectations.
- Host adapters use the product's supported Claude or Codex entrypoint and require existing local authentication; no credentials are stored.
- Normal CI validates corpus schema, fixture setup, result parsing, and expectation matching with canned outputs, but never invokes a model or network.
- Before implementation completion, run the complete corpus on at least one supported host and save a timestamped, host-identified, per-case result record in the feature directory.

**Covers**: REQ-013, REQ-014, REQ-018, REQ-020, REQ-021, REQ-023, REQ-028, NFR-001, NFR-002

## Plan-Level Decisions

### PLD-001: Version 1 Uses Two Explicit JSON Contracts

**Evidence**: The resolver and workflow require deterministic fail-closed interoperability, but one contract describes repository evidence and the other describes the final review result.

**Decision**: Use separate version `1` review-context and result-envelope schemas. Keep required keys fixed and test normalized semantic equality across platforms.

**Rationale**: Combining scope construction and model verdict output would couple deterministic Git behavior to reviewer execution and make failures harder to classify.

**Alternatives Considered**: One combined schema; localized prose parsing; model-computed Git scope.

**Trade-off**: Two validators are documented in prompts/tests, but each contract has one responsibility.

**Covers**: REQ-007, REQ-008, REQ-020, NFR-003, NFR-004

### PLD-002: One Command Template with Strictly Separated Branches

**Evidence**: `review-code` is one installed command, and audit behavior must remain reachable only through `--audit`.

**Decision**: Retain audit rubric content inside `templates/commands/review-code.md`, but place it behind an early mutually exclusive dispatcher before the new defect-gate coordinator.

**Rationale**: This preserves command discoverability and existing audit scoring without creating another installed command or an extra runtime include mechanism.

**Alternatives Considered**: New audit command; external audit rubric file; mixed score and defect report.

**Trade-off**: The template remains large, so contract tests must guard branch isolation and prevent audit language from leaking into defect output.

**Covers**: REQ-001, REQ-006, REQ-019, REQ-020

### PLD-003: Resolver Inventory Records Merge Path Contributions

**Evidence**: A file may have committed, staged, and unstaged contributions, while the specification requires a complete inventory without misleading omission or double counting.

**Decision**: Represent each current repository-relative path once and attach all contributing target segments; retain `old_path` for renames and segment-specific evidence commands.

**Rationale**: Reviewers can inspect every layer while final inventory and counts remain stable.

**Alternatives Considered**: One row per Git segment; flattening to final file contents only.

**Trade-off**: Resolver merging is more involved, but shared fixtures make it deterministic.

**Covers**: REQ-002, REQ-011, REQ-012, REQ-022

### PLD-004: Prompt-Level Coordinator with Capability-Aware Delegation

**Evidence**: CodexSpec distributes command instructions across supported hosts and does not maintain a resident review runtime. Isolation is mandatory only for high-risk and workflow completion gates; ordinary direct review has a confirmed degraded fallback.

**Decision**: Define coordinator, primary, and specialist roles in the command template. Use the host's fresh-agent/delegation capability when available, disclose execution state in the envelope, permit shared fallback only at the confirmed boundary, and otherwise return `INCONCLUSIVE`.

**Rationale**: This enforces the product contract within the existing distribution architecture without an external service.

**Alternatives Considered**: Treat same-context self-review as isolated; launch an installed CodexSpec daemon; always fail direct reviews without delegation.

**Trade-off**: Host capability affects whether strong gates can complete, but degradation is explicit and fail closed.

**Covers**: REQ-014, REQ-015, REQ-020, REQ-021, NFR-004

### PLD-005: Shared Fixtures Define Cross-Platform Semantics

**Evidence**: The CI matrix runs each native shell on its supported platform, so direct side-by-side execution is not always available in one job.

**Decision**: Store platform-neutral repository scenarios and expected normalized manifests in Python test support. Bash and PowerShell suites independently compare against the same expectations; installer tests verify native script selection.

**Rationale**: Shared expectations prove semantic parity without adding a shell runtime dependency to every CI host.

**Alternatives Considered**: Duplicate platform tests; install PowerShell everywhere; compare only script text.

**Trade-off**: CI as a whole establishes parity rather than one process executing both scripts.

**Covers**: REQ-007, REQ-027, NFR-003

### PLD-006: Development-Only Model Evaluation Runner

**Evidence**: Actual model behavior must be measured, but normal CI must remain deterministic and offline.

**Decision**: Keep model cases and an explicit host-adapter runner under `tests/evals/`; normal tests validate the harness with canned outputs, while feature acceptance performs and records one authenticated complete run.

**Rationale**: The same corpus can detect later prompt regressions without making every PR depend on model availability or nondeterministic output.

**Alternatives Considered**: Static phrase assertions only; model calls in CI; one-off manual notes without a reusable harness.

**Trade-off**: Maintainers must deliberately run the live evaluation when the review protocol changes.

**Covers**: REQ-028, NFR-001, NFR-002

### PLD-007: Localized Command Guide as Migration Release Note

**Evidence**: The repository has no standalone changelog, while every supported locale already documents command syntax in one user guide.

**Decision**: Add a clearly titled next-release breaking-change and migration block to each localized command guide, and align README summaries and translation metadata in the same change.

**Rationale**: Users encounter migration guidance where they look up the changed command, without introducing an otherwise unused release-document system.

**Alternatives Considered**: Add a new changelog solely for this feature; document only in PR text; update English only.

**Trade-off**: Release publishers must carry the same migration wording into external release descriptions, while the repository retains the canonical text.

**Covers**: REQ-006, NFR-002

## Implementation Phases

### Phase 1: Resolver Contract and TDD Fixtures

1. Define shared scenario builders, normalized manifest assertions, and failing selector/base/inventory/parent/no-mutation tests.
2. Implement `scripts/bash/review-context.sh` until Unix tests pass.
3. Implement `scripts/powershell/review-context.ps1` against the same expectations and verify Windows CI parity.
4. Extend init, package, and Codex rendering assertions for both script names.

**Covers**: REQ-002, REQ-003, REQ-004, REQ-005, REQ-006, REQ-007, REQ-008, REQ-009, REQ-011, REQ-022, REQ-027, NFR-003

### Phase 2: Defect-Gate Command Contract

1. Add failing template tests for mode exclusivity, resolver use, four stages, inventory dispositions, requirements coverage, risk profiles, isolation, specialists, verification safety, finding admission, report sections, envelope fields, and prohibited bypasses.
2. Restructure `review-code.md` into explicit defect and audit branches while preserving audit rubric behavior.
3. Add resolver and read-only Git tool declarations and strict instruction/evidence trust boundaries.
4. Verify rendered Claude and Codex commands retain the intended platform-local invocation.

**Covers**: REQ-001, REQ-006, REQ-008, REQ-009, REQ-010, REQ-011, REQ-012, REQ-013, REQ-014, REQ-015, REQ-016, REQ-017, REQ-018, REQ-019, REQ-020, REQ-021, REQ-022, REQ-023, REQ-024, NFR-001, NFR-004

### Phase 3: Implement-Tasks Strict Review Loop

1. Replace old path-filter, score, severity deferral, fallback audit, and two-round assertions with failing strict-envelope loop tests.
2. Rewrite the final loop to invoke complete-feature `review-code --feature`, verify findings, use TDD for functional fixes, and parse the final envelope fail closed.
3. Encode progress and retry guards exactly and preserve non-success evidence in completion reporting.

**Covers**: REQ-009, REQ-018, REQ-020, REQ-021, REQ-024, REQ-025, REQ-026, NFR-001, NFR-004

### Phase 4: Distribution and User Migration

1. Update command metadata and all frontmatter translation caches.
2. Update localized command guides, next-release breaking-change blocks, examples, and README command summaries.
3. Update CI path filters and documentation/template consistency tests.
4. Build wheel and source distributions and assert both resolver scripts and updated templates are present.

**Covers**: REQ-001, REQ-006, REQ-007, REQ-027, NFR-002, NFR-003

### Phase 5: Evaluation and Acceptance

1. Add synthetic defect and clean cases plus deterministic harness tests with canned reviewer outputs.
2. Run targeted resolver, template, installer, and evaluation-harness tests, followed by the full pytest suite and package build.
3. Initialize a temporary project from the implementation and execute the complete live model corpus on one supported host.
4. Record per-case results in the feature directory and fail feature completion if minimum findings, expected verdicts, or forbidden-finding constraints are not met.

**Covers**: REQ-013, REQ-014, REQ-018, REQ-020, REQ-021, REQ-027, REQ-028, NFR-001, NFR-002, NFR-003, NFR-004

## Verification Strategy

### Resolver Verification

- Run native script suites on their supported CI hosts.
- Compare normalized JSON against shared expected manifests.
- Snapshot branch, refs, index/worktree status, and tracked contents before and after each invocation.
- Exercise file names with spaces and shell metacharacters to verify safe argument and JSON handling.

**Covers**: REQ-002, REQ-003, REQ-004, REQ-005, REQ-007, REQ-008, REQ-011, REQ-022, REQ-027, NFR-003

### Template and Workflow Verification

- Assert defect and audit branches expose mutually exclusive syntax and outputs.
- Assert every mandatory pass, profile, result field, failure state, and no-bypass rule is present as a behavioral instruction rather than only a keyword list.
- Render commands through both integrations and inspect platform-local script references.
- Validate `implement-tasks` rejects malformed, partial, shared-context final-gate, specialist-incomplete, FAIL, and INCONCLUSIVE envelopes.

**Covers**: REQ-001, REQ-006, REQ-009, REQ-010, REQ-013, REQ-014, REQ-015, REQ-020, REQ-021, REQ-024, REQ-025, REQ-026, REQ-027, NFR-004

### Project-Level Verification

- `uv run ruff check .`
- `uv run pytest` across the existing CI matrix
- `uv build` followed by archive-content checks and `twine check`
- `uv run mkdocs build --strict` after localized documentation updates
- Complete live evaluation run and recorded result artifact

**Covers**: REQ-006, REQ-007, REQ-027, REQ-028, NFR-001, NFR-002, NFR-003

## Security Considerations

- User arguments and repository paths are data, not shell fragments. Resolver tests include metacharacter-bearing paths and focus text.
- Git and repository output remains untrusted evidence in the reviewer prompt and cannot override gate instructions.
- Resolver operations are read-only; no implicit fetch, dependency installation, formatter write, migration, publish, or deploy operation is allowed.
- High-impact trust and command surfaces require isolated specialist evidence; unavailable coverage fails closed.
- Evaluation runner inherits existing host authentication but never reads, records, or copies credentials into fixtures or result artifacts.

**Covers**: REQ-004, REQ-014, REQ-015, REQ-017, REQ-023, NFR-003

## Performance and Scale

- Git commands use NUL-delimited streaming where path output is involved.
- Inventory records are deduplicated by path while retaining segment provenance.
- Large diffs are partitioned for reviewer context but preserve one manifest and final accounting table.
- No target-size threshold can silently drop evidence; resource exhaustion is reported as `INCONCLUSIVE`.

**Covers**: REQ-011, REQ-012, REQ-021, REQ-024, NFR-001

## Risks and Trade-offs

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Bash and PowerShell drift on Git edge cases | Medium | High | Shared expected manifests, native CI, schema contract, parity acceptance |
| Prompt size grows by retaining audit and adding the defect gate | High | Medium | Strict mode dispatch, concise defect report, template contract tests |
| Host lacks isolated delegation | Medium | High for workflow gates | Confirmed shared fallback only for ordinary direct review; otherwise `INCONCLUSIVE` |
| Project verification commands have side effects | Medium | High | Project-first selection plus explicit read-only prohibition and evidence-gap behavior |
| Model evaluation varies between runs | High | Medium | Minimum/forbidden expectations, clean cases, recorded host metadata, deterministic harness tests |
| Multilingual docs become inconsistent | Medium | Medium | Update all locales atomically and add syntax consistency tests |
| Very large or opaque changes exceed available evidence | Medium | High | Complete inventory, partitioning, explicit disposition, fail-closed verdict |

## Requirements Coverage

| Spec Requirement | Plan Coverage | Result |
|---|---|---|
| REQ-001 | Architecture; Component B; Component D; Phases 2 and 4 | Full |
| REQ-002 | Resolver CLI; Component A; Phase 1 | Full |
| REQ-003 | Resolver CLI; Component A; Phase 1 | Full |
| REQ-004 | Resolver CLI/manifest; Component A; Phase 1 | Full |
| REQ-005 | Resolver CLI/manifest; Component A; Phase 1 | Full |
| REQ-006 | Resolver CLI; Components B/D; Phases 1/2/4 | Full |
| REQ-007 | Resolver contract; Components A/D; Phases 1/4 | Full |
| REQ-008 | Manifest compatibility; Components A/B; Phases 1/2 | Full |
| REQ-009 | Manifest feature context; Components A/B/C; Phases 1/2/3 | Full |
| REQ-010 | Component B; Phase 2 | Full |
| REQ-011 | Manifest inventory; Components A/B/E; Phases 1/2 | Full |
| REQ-012 | Components B/E; Phase 2; Scale section | Full |
| REQ-013 | Components B/E/F; Phases 2/5 | Full |
| REQ-014 | Components B/E/F; Phases 2/5 | Full |
| REQ-015 | Component B; Phase 2; PLD-004 | Full |
| REQ-016 | Component B; Phase 2 | Full |
| REQ-017 | Component B; Phase 2; Security section | Full |
| REQ-018 | Components B/C/F; Phases 2/3/5 | Full |
| REQ-019 | Component B; Phase 2; PLD-002 | Full |
| REQ-020 | Result envelope; Components B/C/F; Phases 2/3/5 | Full |
| REQ-021 | Result envelope; Components B/C/F; Phases 2/3/5 | Full |
| REQ-022 | Manifest; Components A/B/E; Phases 1/2 | Full |
| REQ-023 | Components B/E/F; Phase 2; Security section | Full |
| REQ-024 | Components B/C/E; Phases 2/3 | Full |
| REQ-025 | Component C; Phase 3 | Full |
| REQ-026 | Component C; Phase 3 | Full |
| REQ-027 | Component E; all deterministic phases | Full |
| REQ-028 | Component F; Phase 5; PLD-006 | Full |
| NFR-001 | Architecture; Components B/C/F; Phases 2/3/5 | Full |
| NFR-002 | Components D/F; Phases 4/5 | Full |
| NFR-003 | Resolver contracts; Components A/E; Phases 1/4/5 | Full |
| NFR-004 | Result contracts; Components B/C/E; Phases 2/3 | Full |

## Assumptions and Unresolved Items

No product assumptions or unresolved requirement questions remain. The selected-remote precedence, version `1` schema shapes, merged-path inventory representation, localized migration-note placement, and evaluation-runner layout are plan-level technical choices that preserve confirmed behavior and can be revised during implementation only if repository evidence requires an equivalent implementation.
