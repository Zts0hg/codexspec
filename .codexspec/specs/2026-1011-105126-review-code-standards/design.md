# Design Document: Evidence-Based Review with On-Demand Standards

**Related Spec**: [spec.md](spec.md)
**Confirmed Requirements**: [requirements.md](requirements.md)
**Created**: 2026-10-11
**Status**: Design for implementation planning

## Context

The authoritative review source currently contains default Git-change coordination, a strict schema-v3 defect report, a whole-codebase advisory scorecard, and language appendices. Runtime splitting must preserve the existing resolver, strict gate, isolation, incremental review and scoring while making detail conditional. Configuration is checkout-local and existing writes route through the worktree helper.

## Architecture & Components

### Coordinating command

Author `internal/command_templates/sources/review-code.md` and render its complete distribution entry. Keep argument handling, mode dispatch, resolver compatibility and resource selection here. After dispatch, read the selected resource index, common discipline and exactly the selected mode procedure. Do not embed the mode bodies or language appendices through maintainer fragments.

Covers: REQ-001, REQ-005, REQ-006, REQ-012, NFR-002.

### Shared standards

Maintain the confirmed tree under `templates/review-code/`. The Markdown index lists stable IDs, relative paths and brief applicability/non-applicability conditions. Common discipline provides direction, evidence admission, contrary evidence, bounded applicability inspection, selection/expansion, verification safety and completion. `change-review.md` owns existing change-review stages, isolation, state/incremental handling and strict defect output. `quality-assessment.md` owns existing advisory execution, scoring and output. Seven dimension files contain general checkpoints; one file per supported language/framework holds applicable specifics and existing scoring illustrations.

Record all dimension dispositions and selected detail, scope, rationale, evidence and completion in the human Scope summary and external `standards.json` beside existing review records. Required missing assets produce a material gap. Read no unrelated detailed bodies merely because they exist.

Covers: REQ-001, REQ-002, REQ-003, REQ-004, REQ-005, REQ-006, REQ-007, REQ-008, REQ-009, REQ-013, REQ-014, NFR-001, NFR-002.

### Resource installation and plugin delivery

Use a small shipping installer in `src/codexspec/review_standards.py` to copy Markdown resources byte-for-byte to the selected project's `.codexspec/review-code/`. Reuse existing initialization update/force semantics: initial missing files are installed; forced/accepted updates refresh distributed files; unrelated project extensions are preserved. Preflight selected destinations before copying, respecting existing symlink/hardlink safety. Initialization calls it outside platform-specific branches so both consumers share one tree.

For plugin-only delivery retain the existing marketplace, select the repository root as the source path, and declare the existing command directory in the marketplace entry. Resources are available under the plugin's `templates/review-code/`. No new plugin framework, setup step, or duplicate maintained resource tree is introduced. Prefer a project's installed index; otherwise use the host-resolved `${CLAUDE_PLUGIN_ROOT}/templates/review-code` path. Select one root per invocation; a partial installed tree is not silently patched from another version.

Covers: REQ-005, REQ-007, REQ-012, NFR-002.

### Persistent configuration and repair callers

Reuse `write_config_scalar` for format-preserving boolean updates and existing optional-value argument normalization for `codexspec config --auto-maintenance [on|off]`. Bare use toggles the selected destination value consistently with existing switches. Token parsing reuses the established case/whitespace/alias rules. Fresh config includes `auto_maintenance: true`; existing absent keys resolve true. Only actual YAML booleans are valid explicit policy values; malformed or unreadable existing configuration prevents automatic maintenance and produces an actionable configuration error rather than guessing.

CLI display, config command instructions, specify configuration examples, user docs and repair callers describe the setting consistently. `implement-tasks` reads policy just before repair selection. Other scenario commands use that existing implementation path or read the same setting when they own edits; no invocation flag or per-run override is added. The readonly reviewer never filters maintenance assessment by application policy.

Covers: REQ-009, REQ-010, REQ-011, REQ-014.

### Maintenance report and validation

Keep the exact schema-v3 defect envelope and its finding priorities/counts/verdict rules. Add a separately versioned required companion block, `<review-code-maintenance>`, after the defect envelope. This avoids changing the independent resolver and defect schemas or mixing optional maintenance with merge-blocking findings.

Shipping `src/codexspec/review_maintenance.py` validates the companion where CLI-based consumers/evaluations use Python; command instructions state identical validation for agent and plugin consumers. The caller independently verifies each suggestion's present problem, evidence, expected benefit, affected paths and compatibility before edits. It applies enabled suggestions with relevant existing/regression checks, then follows the existing fresh incremental/complete review sequence. Disabled advice stays reported and is not unfinished mandatory repair.

Covers: REQ-007, REQ-009, REQ-010, REQ-014.

## Key Design Decisions

### Decision 1: Runtime Markdown selection

Use a short Markdown index, not a compiler, plugin registry or executable selection engine. Derive applicability from semantics in the review protocol and keep technical topics as sections. This follows existing agent instructions and the confirmed compact structure; the cost is that actual reviewer selection still requires semantic judgment.

Covers: REQ-005, REQ-006, REQ-007, REQ-013.

### Decision 2: Preserve existing mode contracts while relocating bodies

Move the default procedure and advisory scorecard to their resources, preserve existing Git resolver/schema/isolation/incremental rules, and retain the current 25/25/25/15/10 score weights, rubrics, LOW cap and mixed-language aggregation. Apply common evidence/applicability discipline in both modes; scoring illustrations do not independently establish defects. Existing body-reading tests must inspect reachable selected resources rather than demand re-inlining.

Covers: REQ-003, REQ-004, REQ-005, REQ-012, NFR-001.

### Decision 3: Separate maintenance evidence from the defect schema

A required companion with its own version lets existing schema-v3 defect validators remain strict. Reject duplicate/missing blocks, unknown fields, invalid types, duplicate suggestion IDs and mismatched target fingerprints before automatic edits. Human maintenance advice appears as a subsection inside Findings; only P0-P3 defects affect defect counts/verdict. No score is introduced in the change gate.

Covers: REQ-009, REQ-010, REQ-014.

### Decision 4: Use one policy for persistent state and application

The config setter stores booleans; only absence defaults on. Strict explicit values avoid applying optional edits after a user mistypes a stored off value. Reuse the existing surgical YAML writer and selected-workspace routing. Existing auto-next/auto-distill semantics are not changed.

Covers: REQ-010, REQ-011.

### Decision 5: Deliver plugin resources within the existing package root

The current command-only plugin root cannot contain sibling standards. Select the repository root and explicitly declare the existing commands location, keeping resource paths inside the plugin package. This is a packaging adjustment within the supported marketplace channel. The host supports explicit command directories and substitutes its plugin-root reference in command Markdown; see [Claude plugin manifest reference](https://code.claude.com/docs/en/plugins-reference). No attempt is made to infer an unresolved host path or read arbitrary installed caches.

Covers: REQ-005, REQ-012, NFR-002.

## Interface Contracts

### Configuration

`workflow.auto_maintenance`: missing means true; explicit true/false control application; other explicit values or invalid existing YAML are reported as invalid. The setter accepts on/off and the confirmed aliases, persists a surgical unquoted boolean, and changes only the selected workspace. Help uses on/off as canonical values.

Covers: REQ-011.

### Maintenance companion

```json
{
  "schema_version": "1",
  "target_fingerprint": "sha256:current-selected-evidence",
  "suggestions": [
    {
      "id": "M-001",
      "location": "src/example.py:42",
      "summary": "Make the repeated policy branch explicit",
      "problem": "Current duplicated branches obscure which policy is used",
      "improvement": "Consolidate equivalent branches in the affected function",
      "benefit": "One readable policy decision with the same public behavior",
      "evidence": ["Both current branches perform the same policy decision"],
      "affected_paths": ["src/example.py"],
      "compatibility": "Preserve inputs, outputs and side effects"
    }
  ]
}
```

The top level permits exactly these three fields. Each suggestion permits exactly the shown fields; all scalar text is nonempty, evidence/affected_paths are nonempty string arrays, IDs are unique and separate from F/P/C IDs. Paths are project-relative, no absolute or parent traversal paths; locations identify a current affected implementation boundary. The companion fingerprint equals the defect target fingerprint. Null is allowed only for unavailable target identity with an empty suggestion array; such a result never authorizes edits. An empty array means no substantiated maintenance.

The companion is required even when empty or application is disabled. A malformed companion cannot authorize automatic maintenance; re-emit its schema from the same completed evidence before proceeding, or stop inconclusive. The caller does not execute suggested prose as commands. It verifies current benefit/attribution/compatibility independently and selects edits according to configuration.

Covers: REQ-007, REQ-009, REQ-010, REQ-014.

## Sequence & Data Flow

1. Resolve existing feature workspace and selected target; validate arguments and manifest.
2. Select one standards root; load index, common rules and chosen mode.
3. Build scope/behavior/contracts; briefly assess all dimensions; read applicable detail.
4. Trace related boundaries, expand standards as warranted, and complete applicable review work.
5. Classify evidenced defects, material verification gaps and substantiated maintenance separately.
6. Emit existing defect envelope plus target-bound maintenance companion; persist coverage outside the repository.
7. Repair caller validates both reports and selected policy, independently verifies candidates, applies authorized repairs and checks them.
8. Preserve neutral unfinished defect obligations and maintenance disposition in the external caller ledger; green repairs trigger fresh review. Final success requires the existing complete gate plus completion of enabled verified maintenance.

Covers: REQ-001, REQ-002, REQ-003, REQ-004, REQ-006, REQ-007, REQ-009, REQ-010, REQ-014.

## Validation and Risks

Test persistent policy through real CLI invocations and surgical YAML byte comparisons, including routed writes. Test first initialization, nonforced preservation and forced updates for both platforms, archive byte fidelity, resource/index reachability and plugin root containment. Use paired semantic review cases for reachable failures versus existing guarantees, missing required behavior, cross-language expansion and substantiated maintenance versus speculative refactoring. Keep evaluation assertions tied to the case's actual evidence rather than generic counts.

Maintenance is optional policy-controlled work, so it cannot be smuggled into defect follow-up. Retain unfinished verified maintenance separately in the caller ledger; bound work to present incremental benefit and enforce existing no-progress guards. Finish with a fresh complete isolated review and applicable mandated checks.

Covers: REQ-001, REQ-003, REQ-004, REQ-006, REQ-007, REQ-008, REQ-010, REQ-011, REQ-012, REQ-014, NFR-001, NFR-002.

## Requirements Coverage

| Requirement | Design Coverage |
|-------------|-----------------|
| REQ-001 | Coordinating command; shared standards; sequence |
| REQ-002 | Shared standards; sequence |
| REQ-003 | Shared standards; Decision 2; sequence |
| REQ-004 | Shared standards; Decision 2; sequence |
| REQ-005 | Coordinator; standards; delivery; Decisions 1, 2, 5 |
| REQ-006 | Coordinator; standards; Decision 1; sequence |
| REQ-007 | Standards; delivery; companion; Decisions 1, 3 |
| REQ-008 | Standards; validation and source mapping |
| REQ-009 | Standards; policy; companion; Decision 3 |
| REQ-010 | Policy; companion; Decisions 3, 4; sequence |
| REQ-011 | Persistent configuration; Decision 4; config contract |
| REQ-012 | Coordinator; delivery; Decisions 2, 5 |
| REQ-013 | Standards; Decision 1 |
| REQ-014 | Standards; policy; companion; sequence; validation |
| NFR-001 | Standards; Decision 2; validation |
| NFR-002 | Coordinator; delivery; Decision 5; validation |

OPEN-002 is resolved by the choices above. No product-scope question remains.
