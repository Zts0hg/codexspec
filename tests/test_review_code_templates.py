"""Contract tests for the distributed review-code command."""

from __future__ import annotations

import re
from pathlib import Path

import yaml

ROOT = Path(__file__).parent.parent
TEMPLATE = ROOT / "templates" / "commands" / "review-code.md"


def read_template() -> str:
    return TEMPLATE.read_text(encoding="utf-8")


def split_template() -> tuple[dict[str, object], str]:
    content = read_template()
    _, raw_frontmatter, body = content.split("---", 2)
    return yaml.safe_load(raw_frontmatter), body


def section(body: str, start: str, end: str | None = None) -> str:
    selected = body.split(start, 1)[1]
    if end is not None:
        selected = selected.split(end, 1)[0]
    return selected


def test_frontmatter_declares_change_gate_and_platform_resolver() -> None:
    frontmatter, _ = split_template()

    assert frontmatter["description"] == (
        "Review a selected change as a strict defect gate, or audit paths with --audit"
    )
    hint = str(frontmatter["argument-hint"])
    assert "\n" in hint  # multi-line block scalar: explains mode semantics, not just flag names
    for syntax in [
        "[defect-gate selectors | --audit [paths...]]",
        "two mutually exclusive modes",
        "No arguments",
        "--committed",
        "--uncommitted",
        "--commit <sha>",
        "--parent <n>",
        "--base <branch>",
        "--feature <feature-dir>",
        "--focus <instructions>",
        "merge-base",
        "no gate verdict, no envelope",
        "--audit src/",
        "Examples:",
        "/codexspec:review-code --audit src/api",
    ]:
        assert syntax in hint

    assert frontmatter["scripts"] == {
        "sh": ".codexspec/scripts/review-context.sh",
        "ps": ".codexspec/scripts/review-context.ps1",
    }


def test_mode_dispatch_is_early_explicit_and_fail_closed() -> None:
    _, body = split_template()
    dispatch = section(body, "## Mode Dispatch", "## Audit Mode")

    assert "before reading target files" in dispatch
    assert "--audit" in dispatch
    assert "defect-gate mode" in dispatch
    assert "mutually exclusive" in dispatch
    assert "Bare paths" in dispatch
    assert "review-code --audit <path>" in dispatch
    assert "INCONCLUSIVE" in dispatch

    for bypass in [
        "--ignore-finding",
        "--waive",
        "--suppress-severity",
        "--fast",
        "--skip-risk",
        "--skip-tests",
    ]:
        assert bypass in dispatch


def test_usage_hints_give_concrete_invocations() -> None:
    _, body = split_template()
    hints = section(body, "## Usage Hints", "## Role and Non-Negotiable Boundary")

    for invocation in [
        "(no arguments)",
        "--committed",
        "--uncommitted",
        "--commit <sha>",
        "--base <branch>",
        "--parent <n>",
        "--feature <feature-dir>",
        "--focus <instructions>",
        "--audit <path> [...]",
    ]:
        assert invocation in hints

    assert "merge-base" in hints
    assert "valid only with (no arguments) or --committed" in hints
    assert "never changes Git scope" in hints
    assert "no gate verdict, no envelope" in hints
    assert "--audit src/" in hints


def test_argument_errors_echo_usage_hints() -> None:
    _, body = split_template()
    dispatch = section(body, "## Mode Dispatch", "## Audit Mode")

    assert "argument error" in dispatch
    assert "## Usage Hints" in dispatch


def test_defect_selectors_and_modifiers_have_exact_boundaries() -> None:
    _, body = split_template()
    contract = section(body, "### Defect-Gate Argument Contract", "## Resolver Compatibility Gate")

    for selector in ["default", "--committed", "--uncommitted", "--commit <sha>"]:
        assert selector in contract
    for modifier in ["--base <branch>", "--parent <n>", "--feature <feature-dir>", "--focus <instructions>"]:
        assert modifier in contract

    assert "Primary selectors are mutually exclusive" in contract
    assert "`--base` is valid only with default or `--committed`" in contract
    assert "`--parent` is valid only with `--commit`" in contract
    assert "requirements context without changing Git scope" in contract
    assert "adds Risk Pass obligations" in contract
    assert "does not narrow" in contract
    assert "Defect-gate mode accepts no path filters" in contract


def test_resolver_is_mandatory_and_schema_validated() -> None:
    _, body = split_template()
    resolver = section(body, "## Resolver Compatibility Gate", "## Defect-Gate Review Protocol")

    assert "Bash: `.codexspec/scripts/review-context.sh $ARGUMENTS`" in resolver
    assert "PowerShell: `& .codexspec/scripts/review-context.ps1 $ARGUMENTS`" in resolver
    assert "{SCRIPT}" not in resolver
    assert '"schema_version": "1"' in resolver
    assert '"status": "ok"' in resolver
    assert "MUST NOT reconstruct or guess Git scope" in resolver
    for failure in [
        "missing resolver",
        "non-zero exit",
        "invalid JSON",
        "unsupported schema",
        "incomplete manifest",
    ]:
        assert failure in resolver
    assert "update or re-run `codexspec init`" in resolver


def test_five_stages_and_complete_inventory_are_required() -> None:
    _, body = split_template()
    protocol = section(body, "## Defect-Gate Review Protocol", "### Requirements Coverage")

    stages = re.findall(
        r"^### Stage \d: (Scope|System Contract|Behavior|Risk|Verification) Pass$",
        protocol,
        re.MULTILINE,
    )
    assert stages == ["Scope", "System Contract", "Behavior", "Risk", "Verification"]

    for artifact in [
        "code",
        "tests",
        "configuration",
        "schema",
        "migration",
        "scripts",
        "CI and release files",
        "manifests",
        "lockfiles",
        "documentation",
        "templates",
        "assets",
        "CodexSpec artifacts",
        "renames",
        "deletions",
        "symlinks",
        "binaries",
        "submodules",
        "generated output",
        "vendored content",
    ]:
        assert artifact in protocol

    for disposition in [
        "reviewed",
        "verified by tool/generator",
        "excluded with explicit justification",
        "uninspectable",
    ]:
        assert disposition in protocol

    assert "without source-extension filtering" in protocol
    assert "one complete inventory" in protocol
    assert "Unclassified" in protocol and "prevent `PASS`" in protocol


def test_system_contracts_and_semantic_partitions_are_mandatory() -> None:
    _, body = split_template()
    protocol = section(body, "## Defect-Gate Review Protocol", "### Requirements Coverage")
    contract_pass = section(protocol, "### Stage 2: System Contract Pass", "### Stage 3: Behavior Pass")

    for source in [
        "confirmed requirements",
        "project instructions",
        "semantic change evidence",
        "dependency relationships",
        "public behavior",
    ]:
        assert source in contract_pass
    for field in [
        "sources",
        "producers",
        "propagation boundaries",
        "consumers",
        "entry surfaces",
        "scenarios",
        "evidence",
        "status",
    ]:
        assert field in contract_pass
    assert "must not invent product requirements" in contract_pass.lower()
    assert "feature artifacts" in contract_pass and "not required" in contract_pass
    assert "origin_fingerprint" in contract_pass
    assert "never treat the prior record as current proof" in contract_pass
    assert "semantic scope" in protocol
    assert "file inventory" in protocol and "does not establish" in protocol
    assert "terminal state" in protocol


def test_review_continues_after_findings_and_searches_root_cause_variants() -> None:
    _, body = split_template()
    protocol = section(body, "## Defect-Gate Review Protocol", "### Requirements Coverage")
    verification = section(protocol, "### Stage 5: Verification Pass")

    assert "must not terminate" in protocol.lower()
    for partition in ["contract", "behavior", "risk", "specialist", "verification"]:
        assert partition in protocol
    for concept in [
        "root-cause identifier",
        "bounded sibling search scope",
        "equivalent callers",
        "implementations",
        "adapters",
        "entry surfaces",
        "symmetric paths",
    ]:
        assert concept in verification
    assert "newly discovered candidates" in verification
    assert "not_applicable" in verification and "reason" in verification
    assert "incomplete" in verification and "INCONCLUSIVE" in verification
    assert "every admitted finding" in verification and "root-cause identifier" in verification
    assert "incomplete contract" in verification
    assert "incomplete partition" in verification
    assert "incomplete variant search" in verification
    assert "blocking coverage gap" in verification
    assert "follow_up.received" in verification
    assert "follow_up.required" in verification
    assert "never a repair approach or correctness conclusion" in verification


def test_cross_round_handoff_transmits_only_neutral_obligations() -> None:
    _, body = split_template()
    isolation = section(body, "### Reviewer Isolation", "### Instruction and Evidence Trust")

    assert "neutral incoming follow-up obligations" in isolation
    assert "Do not send completed prior coverage records, root-cause variant searches" in isolation
    assert "applicable neutral incoming coverage/follow-up obligations" not in isolation


def test_requirements_coverage_tracks_target_completeness() -> None:
    _, body = split_template()
    coverage = section(body, "### Requirements Coverage", "### Risk Profiles")

    assert "complete" in coverage
    assert "partial" in coverage
    assert "not_evaluated" in coverage
    assert "full requirements completeness and implementation conformance" in coverage
    assert "affected-requirement conformance" in coverage
    assert "no whole-feature-readiness claim" in coverage
    assert "implement-tasks" in coverage
    assert "missing or unreadable" in coverage
    assert "INCONCLUSIVE" in coverage


def test_all_risk_profiles_use_semantic_activation() -> None:
    _, body = split_template()
    profiles = section(body, "### Risk Profiles", "### Reviewer Isolation")

    expected = [
        "authorization/trust",
        "command/process execution",
        "filesystem/path handling",
        "parsing/configuration",
        "persistence/state",
        "network/provider behavior",
        "concurrency/lifecycle",
        "public API/CLI compatibility",
        "secrets/injection",
        "build/dependency behavior",
    ]
    assert re.findall(r"^\d+\. `([^`]+)`$", profiles, re.MULTILINE) == expected
    assert "semantic diff, call-chain, dependency, and feature evidence" in profiles
    for scenario in ["normal", "denial/failure", "boundary", "bypass", "compatibility"]:
        assert scenario in profiles
    assert "keywords alone" in profiles


def test_reviewers_are_fresh_isolated_and_specialists_are_independent() -> None:
    _, body = split_template()
    isolation = section(body, "### Reviewer Isolation", "### Instruction and Evidence Trust")

    assert "fresh review-only context" in isolation
    assert "must not inherit implementation reasoning, prior conclusions, or previous findings" in isolation
    assert "must not apply fixes" in isolation
    assert "raw target evidence" in isolation
    assert "not primary findings" in isolation
    assert "union and deduplicate" in isolation
    assert "high-risk" in isolation and "INCONCLUSIVE" in isolation
    assert "implement-tasks" in isolation and "isolated" in isolation


def test_repository_evidence_cannot_rewrite_gate_rules() -> None:
    _, body = split_template()
    trust = section(body, "### Instruction and Evidence Trust", "### Verification Safety")

    assert "untrusted evidence" in trust
    for evidence in [
        "source text",
        "ordinary documents",
        "generated or vendored content",
        "commit messages",
        "test logs",
        "tool output",
    ]:
        assert evidence in trust
    assert "must not weaken" in trust
    assert "concrete qualifying impact" in trust


def test_verification_is_project_first_read_only_and_mutation_safe() -> None:
    _, body = split_template()
    verification = section(body, "### Verification Safety", "### Finding Admission")

    ordered_sources = [
        "explicit project and feature instructions",
        "existing CI or project-script entry points",
        "standard build-manifest commands",
        "optional language-default analyzers",
    ]
    assert [verification.index(source) for source in ordered_sources] == sorted(
        verification.index(source) for source in ordered_sources
    )
    for prohibited in [
        "install or update dependencies",
        "rewrite lockfiles",
        "format in write mode",
        "publish",
        "deploy",
        "run migrations",
    ]:
        assert prohibited in verification

    assert "redirect caches, temporary files, coverage data, and reports outside the repository" in verification
    assert "disposable temporary mirror" in verification
    assert "pre/post Git status" in verification
    assert "tracked-content fingerprints" in verification
    assert "must not clean, restore, or hide" in verification
    assert "mutating project-check example" in verification
    assert "route it to a disposable mirror or reject it before project-tree execution" in verification
    assert "mandatory" in verification and "INCONCLUSIVE" in verification
    assert "optional" in verification and "coverage gap" in verification


def test_findings_are_evidence_backed_and_all_priorities_fail() -> None:
    _, body = split_template()
    admission = section(body, "### Finding Admission", "## Defect-Gate Output Contract")

    for criterion in [
        "introduced, worsened, or made reachable by the selected change",
        "concrete trigger and impact evidence",
        "correctness, security, performance, reliability, compatibility, or confirmed intent",
        "warrant repair before merge",
    ]:
        assert criterion in admission
    for priority in ["P0", "P1", "P2", "P3"]:
        assert priority in admission
    assert "Every admitted priority makes the verdict `FAIL`" in admission
    assert "binding obligation" in admission
    assert "equivalent deterministic evidence" in admission
    assert "behavior-preserving refactors" in admission
    assert "coverage gap" in admission
    assert "style preferences" in admission
    assert "generic coverage advice" in admission
    assert "praise" in admission
    assert "general refactoring opportunities" in admission


def test_defect_report_has_exactly_six_human_sections_and_one_envelope() -> None:
    _, body = split_template()
    output = section(body, "## Defect-Gate Output Contract", "## Audit Mode")
    report = re.search(r"````markdown\n(.*?)\n````", output, re.DOTALL)
    assert report is not None
    rendered = report.group(1)

    assert re.findall(r"^## (.+)$", rendered, re.MULTILINE) == [
        "Verdict",
        "Scope",
        "Findings",
        "Requirements Coverage",
        "Verification Summary",
        "Coverage Gaps",
    ]
    assert rendered.count("<review-code-result>") == 1
    assert rendered.count("</review-code-result>") == 1

    for field in [
        '"schema_version"',
        '"mode"',
        '"verdict"',
        '"target"',
        '"requirements_coverage"',
        '"verification"',
        '"findings"',
        '"finding_counts"',
        '"review_coverage"',
        '"contracts"',
        '"partitions"',
        '"variant_searches"',
        '"follow_up"',
        '"received"',
        '"required"',
        '"coverage_gaps"',
        '"coverage_gap_count"',
        '"review_context"',
        '"reviewers"',
        '"primary"',
        '"specialists"',
    ]:
        assert field in rendered
    assert '"schema_version": "3"' in rendered
    assert '"fingerprint"' in rendered
    for priority in ["P0", "P1", "P2", "P3"]:
        assert f'"{priority}"' in rendered

    assert "PASS | FAIL | INCONCLUSIVE" in output
    assert "complete | partial | not_evaluated" in output
    assert "isolated | shared" in output
    assert "Missing, malformed, contradictory, unsupported, or unknown" in output
    assert "empty finding list alone" in output
    assert "all four finding counts are zero" in output
    assert "all five stages complete" in output
    assert "unique" in output and "cross-reference" in output
    assert "originating schema-v3 result" in output
    assert "finding counts match" in output.lower()
    assert "coverage gap count matches" in output.lower()
    assert "completed coverage record" in output and "evidence" in output
    assert "open or unresolved follow-up" in output
    assert "blocking coverage gap" in output
    assert "permits no additional members" in output
    assert "do not add an `activated_profiles`" in output
    assert "scope` is exactly `target identity`" in output
    assert "specialist profiles are unique" in output
    assert "INCONCLUSIVE` contains no admitted finding" in output
    assert "uncommitted` and `commit` cannot claim `complete_feature`" in output
    assert "Every admitted finding has a non-null `root_cause_id`" in output
    assert "complete feature target requires complete requirements coverage" in output
    assert "code-level `PASS`" in output
    assert "contract, partition, variant-search, or coverage-gap" in output

    for forbidden in ["Quality Score", "Strengths", "Recommendations"]:
        assert forbidden not in rendered


def test_target_fingerprint_is_deterministic_complete_and_read_only() -> None:
    _, body = split_template()
    protocol = section(body, "## Defect-Gate Review Protocol", "## Audit Mode")

    assert "exact validated resolver manifest" in protocol
    assert "exact raw selected evidence" in protocol
    assert "deterministic" in protocol and "byte-preserving" in protocol
    for evidence in [
        "committed",
        "staged",
        "unstaged",
        "untracked",
        "rename",
        "deletion",
        "binary",
        "submodule",
        "symlink",
    ]:
        assert evidence in protocol
    assert "must change the fingerprint" in protocol
    assert "without modifying the repository" in protocol
    assert "cannot be computed or reproduced" in protocol
    assert "INCONCLUSIVE" in protocol


def test_audit_is_a_self_contained_advisory_scorecard_without_envelope() -> None:
    _, body = split_template()
    audit = section(body, "## Audit Mode", "## Language Appendix")

    assert "Only enter this branch when the first parsed argument is `--audit`" in audit
    assert "complete current file contents" in audit
    assert "default: `src/`" in audit
    for dimension in [
        "Idiomatic Clarity & Simplicity",
        "Correctness & Explicit Contracts",
        "Runtime Robustness & Resource Discipline",
        "Architecture & Design Integrity",
        "Constitution Alignment",
    ]:
        assert dimension in audit
    for status in ["Pass", "Needs Work", "Fail"]:
        assert status in audit
    assert "Quality Score" in audit
    assert "advisory" in audit.lower()
    assert "MUST NOT invoke the resolver" in audit
    assert "MUST NOT emit a result envelope" in audit
    assert "MUST NOT be consumed by `implement-tasks`" in audit
    assert "<review-code-result>" not in audit


# --- Review convergence (feature 2026-1008-1952ti) ---


def test_decision_and_incremental_modifiers_are_documented() -> None:
    """TS-5.1"""
    frontmatter, body = split_template()
    hint = str(frontmatter["argument-hint"])
    hints = section(body, "## Usage Hints", "## Role and Non-Negotiable Boundary")
    for text in (hint, hints):
        assert "--decided-by reviewer|ask" in text
        assert "--incremental-from <fingerprint>" in text
        assert "review.decided_by" in text


def test_decision_and_incremental_modifier_boundaries() -> None:
    """TS-5.2 / TS-5.3 / TS-5.4"""
    _, body = split_template()
    contract = " ".join(section(body, "### Defect-Gate Argument Contract", "## Resolver Compatibility Gate").split())

    assert "`--incremental-from` is valid only with default or `--committed`" in contract
    assert "with `--uncommitted` or `--commit` it is an argument error" in contract
    assert "`--decided-by` is valid with every defect-gate selector" in contract
    assert "any value other than `reviewer` or `ask` is an argument error" in contract
    assert "combining either with `--audit` is an argument error" in contract
    assert "Each of `--decided-by` and `--incremental-from` may appear at most once" in contract


def test_coordinator_strips_its_own_modifiers_before_the_resolver() -> None:
    """TS-5.5"""
    _, body = split_template()
    resolver = " ".join(section(body, "## Resolver Compatibility Gate", "## Defect-Gate Review Protocol").split())

    assert "removes `--decided-by` and `--incremental-from`" in resolver
    assert "before invoking the resolver" in resolver
    assert "the resolver scripts, their argument parsing, and the manifest schema are unchanged" in resolver


def _compact(text: str) -> str:
    return " ".join(text.split())


def test_decision_mode_resolution_and_scenario_items() -> None:
    """TS-6.1 - TS-6.6, TS-6.8"""
    _, body = split_template()
    decision = _compact(section(body, "### Decision Mode and Scenario Decisions", "## Defect-Gate Output Contract"))

    assert "`--decided-by` → `review.decided_by` in `.codexspec/config.yml` → `reviewer`" in decision
    assert "is an argument error" in decision and "never treated as `ask`" in decision
    assert "In `reviewer` mode there is no scenario classification" in decision
    assert "Finding Admission applies exactly as written" in decision
    assert "outside the project's real operating context" in decision
    assert "confirmed requirements, the Constitution, and recognized project instructions" in decision
    assert "`context_basis`" in decision
    assert "blocking coverage gap whose scope is exactly `scenario decision <id>`" in decision
    assert "never `PASS` while any scenario decision is pending" in decision
    assert "`FAIL` when any admitted finding exists, otherwise `INCONCLUSIVE`" in decision
    assert "accepted scenario" in decision and "is not reported again" in decision
    assert "confirmed `CON` entry" in decision and "ordinary admitted finding" in decision

    output = _compact(section(body, "## Defect-Gate Output Contract", "## Audit Mode"))
    assert "resolved decision mode" in output


def test_schema_v3_envelope_members_and_rules() -> None:
    """TS-7.1 - TS-7.4"""
    _, body = split_template()
    output = section(body, "## Defect-Gate Output Contract", "## Audit Mode")
    rendered = re.search(r"````markdown\n(.*?)\n````", output, re.DOTALL)
    assert rendered is not None
    for member in [
        '"review_scope"',
        '"kind": "complete"',
        '"since": null',
        '"decided_by": "reviewer"',
        '"scenario_decisions": []',
    ]:
        assert member in rendered.group(1)

    rules = _compact(output)
    assert "`schema_version = 3`" in rules
    assert "`review_scope.kind = complete | incremental`" in rules
    assert "`decided_by = reviewer | ask`" in rules
    assert "`since` is a fingerprint string exactly when `kind` is `incremental`" in rules
    assert "and null when it is `complete`" in rules
    assert "`scenario_decisions` is empty when `decided_by` is `reviewer`" in rules
    assert "`context_basis`" in rules and "`status: pending`" in rules
    assert "its blocking coverage gap is an outgoing follow-up source" in rules
    assert "A result with a pending scenario decision is never `PASS`" in rules
    assert "no pending scenario decision" in rules

    dispatch = _compact(section(body, "## Mode Dispatch", "### Defect-Gate Argument Contract"))
    assert "Argument-error envelopes use schema version `3`" in dispatch
    assert "empty `scenario_decisions`" in dispatch


def test_incremental_review_reuses_only_unchanged_unaffected_coverage() -> None:
    """TS-8.1 - TS-8.9"""
    _, body = split_template()
    store = _compact(section(body, "### Review State Store", "### Incremental Review"))
    assert "`${XDG_CACHE_HOME:-$HOME/.cache}/codexspec/review/<repo-id>/`" in store
    assert "`%LOCALAPPDATA%\\codexspec\\review\\<repo-id>\\`" in store
    assert "never inside the repository" in store
    assert "`results/sha256-<hex>/`" in store
    assert "per-entry evidence digest" in store and "`partition_ids`" in store

    incremental = _compact(section(body, "### Incremental Review", "### Stage 1: Scope Pass"))
    assert "Without `--incremental-from`, run the complete review" in incremental
    assert "missing, unreadable, or mismatched records" in incremental.lower()
    for field in ["repository", "selector", "feature", "`base_ref`", "`merge_base_sha`"]:
        assert field in incremental
    assert "changed, added, removed, or renamed" in incremental
    assert "affected partition" in incremental and "`contract_ids`" in incremental
    assert "never prior coverage evidence, statuses, findings, or variant searches" in incremental
    assert "`carried`" in incremental
    assert "describes the complete selected target" in incremental
    assert "`review_coverage` lists only this round's" in incremental
    assert "never terminal" in incremental
    assert "may trace beyond" in incremental
    assert "carried coverage never suppresses an admitted finding" in incremental


def test_verification_mirror_output_and_topology_rules() -> None:
    """TS-9.1 - TS-9.5"""
    _, body = split_template()
    verification = _compact(section(body, "### Verification Safety", "### Finding Admission"))
    assert "the manifest `HEAD` for default, `--committed`, and `--uncommitted`" in verification
    assert "the selected commit for `--commit`" in verification
    assert "copied rather than linked" in verification
    assert "without installing anything" in verification
    assert "its own Git metadata from a local clone" in verification
    assert "never share the original's Git directory" in verification
    assert "never use `git worktree add`" in verification

    output = _compact(section(body, "## Defect-Gate Output Contract", "## Audit Mode"))
    assert "review state store" in output
    assert "only the six-section human report and the envelope" in output

    isolation = _compact(section(body, "### Reviewer Isolation", "### Instruction and Evidence Trust"))
    assert "is the only spawner" in isolation
    assert "direct children of the coordinator" in isolation
    assert "never spawn reviewers" in isolation


def test_isolation_is_explicit_for_each_host() -> None:
    """TS-10.1 - TS-10.3"""
    _, body = split_template()
    isolation = _compact(section(body, "### Reviewer Isolation", "### Instruction and Evidence Trust"))
    assert '`spawn_agent` with `fork_turns: "none"`' in isolation
    assert 'Never use `fork_turns: "all"`' in isolation
    assert "fresh non-fork subagent" in isolation and "`Task`/`Agent`" in isolation
    assert "never use a fork that inherits the conversation" in isolation
    assert "the task message contains only" in isolation
    assert "prior finding prose, implementation reasoning, or claims that a repair succeeded" in isolation


def test_mirror_checks_must_resolve_to_the_mirror() -> None:
    """Review round 1 F-001: copied environments with absolute paths are not isolated."""
    _, body = split_template()
    verification = _compact(section(body, "### Verification Safety", "### Finding Admission"))
    assert "embeds absolute paths to the original checkout" in verification
    assert "editable-install" in verification and "shebang" in verification
    assert "imported code resolves inside the mirror" in verification
    assert "never execute code from the original checkout" in verification


def test_incremental_baseline_error_is_machine_readable() -> None:
    """Review round 1 F-003."""
    _, body = split_template()
    incremental = _compact(section(body, "### Incremental Review", "### Stage 1: Scope Pass"))
    assert "falls back to a complete review in the same invocation" in incremental
    assert "non-blocking coverage gap whose scope is exactly `incremental baseline`" in incremental
    assert "never an argument error" in incremental


def test_isolation_allow_list_includes_incremental_scope_obligations() -> None:
    """Review round 4 F-001: incremental scope delivery must not contradict isolation."""
    _, body = split_template()
    isolation = _compact(section(body, "### Reviewer Isolation", "### Instruction and Evidence Trust"))
    protocol = _compact(section(body, "## Defect-Gate Review Protocol", "### Review State Store"))
    for text in (isolation, protocol):
        assert "incremental scope obligations" in text
    assert "never the prior evidence, statuses, findings, or variant searches" in isolation
