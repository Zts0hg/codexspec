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
    for syntax in [
        "[--committed | --uncommitted | --commit <sha>]",
        "[--base <branch>]",
        "[--parent <n>]",
        "[--feature <feature-dir>]",
        "[--focus <instructions>]...",
        "--audit [paths...]",
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


def test_four_stages_and_complete_inventory_are_required() -> None:
    _, body = split_template()
    protocol = section(body, "## Defect-Gate Review Protocol", "### Requirements Coverage")

    stages = re.findall(r"^### Stage \d: (Scope|Behavior|Risk|Verification) Pass$", protocol, re.MULTILINE)
    assert stages == ["Scope", "Behavior", "Risk", "Verification"]

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
        '"finding_counts"',
        '"coverage_gap_count"',
        '"review_context"',
        '"reviewers"',
        '"primary"',
        '"specialists"',
    ]:
        assert field in rendered
    for priority in ["P0", "P1", "P2", "P3"]:
        assert f'"{priority}"' in rendered

    assert "PASS | FAIL | INCONCLUSIVE" in output
    assert "complete | partial | not_evaluated" in output
    assert "isolated | shared" in output
    assert "Missing, malformed, contradictory, unsupported, or unknown" in output
    assert "empty finding list alone" in output
    assert "all four finding counts are zero" in output

    for forbidden in ["Quality Score", "Strengths", "Recommendations"]:
        assert forbidden not in rendered


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
