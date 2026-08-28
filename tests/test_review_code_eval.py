"""Contract tests for the development-only review-code evaluation runner."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any

import pytest

from tests.evals.review_code import run_eval

EXPECTED_CASES = {
    "authorization-bypass": "authorization/trust",
    "command-quoting": "command/process execution",
    "filesystem-traversal": "filesystem/path handling",
    "parsing-invalid-default": "parsing/configuration",
    "persistence-roundtrip": "persistence/state",
    "network-retry": "network/provider behavior",
    "concurrency-cancellation": "concurrency/lifecycle",
    "api-compatibility": "public API/CLI compatibility",
    "secrets-redaction": "secrets/injection",
    "build-manifest-drift": "build/dependency behavior",
    "verification-mutation": "build/dependency behavior",
    "clean-refactor": "public API/CLI compatibility",
    "clean-indirect-test": "parsing/configuration",
    "contract-multi-surface": "parsing/configuration",
    "related-propagation-defects": "parsing/configuration",
    "early-finding-complete-coverage": "public API/CLI compatibility",
    "incomplete-contract-coverage": "public API/CLI compatibility",
    "clean-contract-propagation": "parsing/configuration",
}


def _envelope(
    *,
    verdict: str = "FAIL",
    profiles: list[str] | None = None,
    findings: list[dict[str, Any]] | None = None,
) -> str:
    normalized_findings: list[dict[str, Any]] = []
    for index, finding in enumerate(findings or [], start=1):
        normalized = {
            "id": f"F-{index:03d}",
            "priority": finding["priority"],
            "location": finding.get("location", f"src/tool.py:{index}"),
            "summary": finding["summary"],
            "trigger": finding.get("trigger", "exercise the changed behavior"),
            "impact": finding.get("impact", "the selected behavior is incorrect"),
            "root_cause_id": finding.get("root_cause_id", f"RC-{index:03d}"),
        }
        normalized_findings.append(normalized)

    variant_searches = []
    for root_cause_id in dict.fromkeys(
        finding["root_cause_id"] for finding in normalized_findings if finding["root_cause_id"] is not None
    ):
        variant_searches.append(
            {
                "root_cause_id": root_cause_id,
                "finding_ids": [
                    finding["id"] for finding in normalized_findings if finding["root_cause_id"] == root_cause_id
                ],
                "cause": "the changed boundary violates one shared contract",
                "scope": ["all equivalent changed boundaries"],
                "methods": ["call-site search", "entry-to-consumer trace"],
                "checked_locations": [finding["location"] for finding in normalized_findings],
                "evidence": ["all equivalent changed boundaries were checked"],
                "reason": None,
                "status": "complete",
            }
        )

    result = {
        "schema_version": "2",
        "mode": "defect",
        "verdict": verdict,
        "target": {
            "selector": "default",
            "fingerprint": "sha256:fixture-target",
            "complete_feature": True,
            "empty": False,
            "base_ref": "main",
            "merge_base_sha": "0123456789abcdef",
            "commit_sha": None,
            "parent_sha": None,
            "inventory_count": 1,
        },
        "requirements_coverage": {"status": "complete", "feature": ".codexspec/specs/example"},
        "verification": {"status": "complete", "commands": []},
        "findings": normalized_findings,
        "finding_counts": {"P0": 0, "P1": 0, "P2": 0, "P3": 0},
        "review_coverage": {
            "contracts": [
                {
                    "id": "C-001",
                    "statement": "Every changed entry preserves the resolved value",
                    "sources": ["selected public behavior"],
                    "producers": ["value resolver"],
                    "propagation": ["changed adapter"],
                    "consumers": ["runtime consumer"],
                    "entry_surfaces": ["public entry"],
                    "scenarios": ["normal", "invalid input"],
                    "evidence": ["entry-to-consumer trace"],
                    "status": "complete",
                }
            ],
            "partitions": [
                {
                    "id": "P-001",
                    "scope": "resolved value propagation",
                    "owner": "primary",
                    "contract_ids": ["C-001"],
                    "evidence": ["all changed entry call chains inspected"],
                    "status": "complete",
                }
            ],
            "variant_searches": variant_searches,
        },
        "follow_up": {
            "received": [],
            "required": [
                {
                    "id": f"FU-{index:03d}",
                    "origin_fingerprint": "sha256:fixture-target",
                    "source_ids": [finding["id"], "C-001"],
                    "statement": f"Re-establish: {finding['summary']}",
                    "status": "open",
                    "evidence": [],
                }
                for index, finding in enumerate(normalized_findings, start=1)
            ],
        },
        "coverage_gaps": [],
        "coverage_gap_count": 0,
        "review_context": "isolated",
        "reviewers": {"primary": "complete", "specialists": []},
        "activated_profiles": profiles or [],
    }
    for finding in result["findings"]:
        result["finding_counts"][finding["priority"]] += 1
    return "Human report\n<review-code-result>\n" + json.dumps(result) + "\n</review-code-result>\n"


def _write_case(tmp_path: Path, *, case_id: str = "command-quoting") -> Path:
    case_dir = tmp_path / case_id
    case_dir.mkdir()
    (case_dir / "case.json").write_text(
        json.dumps(
            {
                "schema_version": "1",
                "id": case_id,
                "description": "Synthetic command quoting defect",
                "risk_profiles": ["command/process execution"],
                "setup": {
                    "files": {
                        "pyproject.toml": "[project]\nname = 'fixture'\nversion = '0.1.0'\n",
                        "src/tool.py": "import os\n\ndef run(name):\n    return os.system('echo ' + name)\n",
                    },
                    "feature_artifacts": {
                        "requirements.md": "# Requirements\n",
                        "spec.md": "# Spec\n",
                        "plan.md": "# Plan\n",
                        "tasks.md": "# Tasks\n",
                    },
                },
                "expect": {
                    "verdict": "FAIL",
                    "acceptable_verdicts": ["FAIL", "INCONCLUSIVE"],
                    "minimum_findings": [
                        {
                            "priority": "P1",
                            "contains": "command injection",
                            "aliases": ["shell concatenation"],
                        }
                    ],
                    "forbidden_findings": ["missing tests"],
                    "profile_aliases": {"command/process execution": ["shell command"]},
                },
            }
        ),
        encoding="utf-8",
    )
    return case_dir


def _stub_codexspec_init(repo: Path) -> None:
    repo.mkdir(parents=True, exist_ok=True)


def test_parse_review_result_requires_exactly_one_valid_envelope() -> None:
    parsed = run_eval.parse_review_result(
        _envelope(
            profiles=["command/process execution"],
            findings=[{"priority": "P1", "summary": "command injection through shell concatenation"}],
        )
    )

    assert parsed["verdict"] == "FAIL"
    assert parsed["finding_counts"]["P1"] == 1

    with pytest.raises(run_eval.ResultParseError, match="exactly one"):
        run_eval.parse_review_result("no envelope")
    with pytest.raises(run_eval.ResultParseError, match="exactly one"):
        run_eval.parse_review_result(_envelope() + _envelope())
    with pytest.raises(run_eval.ResultParseError, match="invalid JSON"):
        run_eval.parse_review_result("<review-code-result>\n{\n</review-code-result>")
    with pytest.raises(run_eval.ResultParseError, match="must be an object"):
        run_eval.parse_review_result("<review-code-result>\n[]\n</review-code-result>")


def test_parse_review_result_rejects_schema_v1_and_cross_field_contradictions() -> None:
    valid = json.loads(
        run_eval.RESULT_RE.search(
            _envelope(
                findings=[{"priority": "P2", "summary": "adapter drops resolved value"}],
            )
        ).group(1)
    )

    invalid_results: list[tuple[str, dict[str, Any]]] = []
    schema_v1 = json.loads(json.dumps(valid))
    schema_v1["schema_version"] = "1"
    invalid_results.append(("unsupported result schema", schema_v1))

    missing_fingerprint = json.loads(json.dumps(valid))
    del missing_fingerprint["target"]["fingerprint"]
    invalid_results.append(("fingerprint", missing_fingerprint))

    missing_complete_feature = json.loads(json.dumps(valid))
    del missing_complete_feature["target"]["complete_feature"]
    invalid_results.append(("complete_feature", missing_complete_feature))

    unknown_field = json.loads(json.dumps(valid))
    unknown_field["legacy_success"] = True
    invalid_results.append(("unknown keys", unknown_field))

    bad_count = json.loads(json.dumps(valid))
    bad_count["finding_counts"]["P2"] = 0
    invalid_results.append(("finding counts", bad_count))

    dangling_reference = json.loads(json.dumps(valid))
    dangling_reference["review_coverage"]["partitions"][0]["contract_ids"] = ["C-999"]
    invalid_results.append(("contract", dangling_reference))

    duplicate_ids = json.loads(json.dumps(valid))
    duplicate_ids["findings"].append(dict(duplicate_ids["findings"][0]))
    duplicate_ids["finding_counts"]["P2"] = 2
    invalid_results.append(("unique", duplicate_ids))

    missing_evidence = json.loads(json.dumps(valid))
    missing_evidence["review_coverage"]["contracts"][0]["evidence"] = []
    invalid_results.append(("evidence", missing_evidence))

    bad_pass = json.loads(json.dumps(valid))
    bad_pass["verdict"] = "PASS"
    invalid_results.append(("PASS", bad_pass))

    unsupported_fail = json.loads(json.dumps(valid))
    unsupported_fail["findings"] = []
    unsupported_fail["finding_counts"]["P2"] = 0
    unsupported_fail["review_coverage"]["variant_searches"] = []
    unsupported_fail["follow_up"]["required"] = []
    invalid_results.append(("FAIL", unsupported_fail))

    unsupported_inconclusive = json.loads(json.dumps(unsupported_fail))
    unsupported_inconclusive["verdict"] = "INCONCLUSIVE"
    invalid_results.append(("INCONCLUSIVE", unsupported_inconclusive))

    mismatched_follow_up_fingerprint = json.loads(json.dumps(valid))
    mismatched_follow_up_fingerprint["follow_up"]["required"][0]["origin_fingerprint"] = "sha256:different-target"
    invalid_results.append(("origin_fingerprint", mismatched_follow_up_fingerprint))

    mismatched_root_cause = json.loads(json.dumps(valid))
    mismatched_root_cause["findings"].append(
        {
            "id": "F-002",
            "priority": "P2",
            "location": "src/tool.py:2",
            "summary": "second occurrence",
            "trigger": "exercise the second path",
            "impact": "the second path is incorrect",
            "root_cause_id": "RC-001",
        }
    )
    mismatched_root_cause["finding_counts"]["P2"] = 2
    invalid_results.append(("root-cause", mismatched_root_cause))

    for message, result in invalid_results:
        output = "<review-code-result>\n" + json.dumps(result) + "\n</review-code-result>"
        with pytest.raises(run_eval.ResultParseError, match=message):
            run_eval.parse_review_result(output)


def test_parse_review_result_allows_null_fingerprint_only_for_blocked_non_pass() -> None:
    result = json.loads(run_eval.RESULT_RE.search(_envelope(verdict="PASS")).group(1))
    result["verdict"] = "INCONCLUSIVE"
    result["target"]["fingerprint"] = None
    result["coverage_gaps"] = [
        {
            "id": "G-001",
            "scope": "target identity",
            "impact": "the exact reviewed evidence cannot be identified",
            "blocking": True,
        }
    ]
    result["coverage_gap_count"] = 1
    output = "<review-code-result>\n" + json.dumps(result) + "\n</review-code-result>"

    assert run_eval.parse_review_result(output)["verdict"] == "INCONCLUSIVE"


def test_case_expectations_match_profiles_findings_and_forbidden_text(tmp_path: Path) -> None:
    case = run_eval.load_case(_write_case(tmp_path))
    result = run_eval.parse_review_result(
        _envelope(
            profiles=["command/process execution"],
            findings=[{"priority": "P1", "summary": "command injection through shell concatenation"}],
        )
    )

    evaluation = run_eval.evaluate_result(case, result)

    assert evaluation.passed is True
    assert evaluation.failures == []

    wrong_verdict = run_eval.parse_review_result(_envelope(verdict="PASS", profiles=[]))
    failed_verdict = run_eval.evaluate_result(case, wrong_verdict)
    assert failed_verdict.passed is False
    assert any("expected verdict FAIL" in failure for failure in failed_verdict.failures)
    assert any("missing risk profile" in failure for failure in failed_verdict.failures)

    forbidden = run_eval.parse_review_result(
        _envelope(findings=[{"priority": "P3", "summary": "missing tests for trivial helper"}])
    )
    failed_finding = run_eval.evaluate_result(case, forbidden)
    assert failed_finding.passed is False
    assert any("forbidden finding text" in failure for failure in failed_finding.failures)


def test_canned_adapter_runs_case_and_records_credential_free_result(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    case_dir = _write_case(tmp_path)
    output = _envelope(
        profiles=["command/process execution"],
        findings=[{"priority": "P1", "summary": "command injection through shell concatenation"}],
    )
    monkeypatch.setattr(run_eval, "_codexspec_init", _stub_codexspec_init)

    record = run_eval.run_case(case_dir, host="canned", canned_output=output, work_root=tmp_path / "work")

    assert record["case"] == "command-quoting"
    assert record["host"] == "canned"
    assert record["passed"] is True
    assert record["expectation_failures"] == []
    assert record["verdict"] == "FAIL"
    serialized = json.dumps(record)
    assert "prompt" not in serialized.lower()
    assert "credential" not in serialized.lower()


def test_run_case_records_parse_failure_without_aborting(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    case_dir = _write_case(tmp_path)
    monkeypatch.setattr(run_eval, "_codexspec_init", _stub_codexspec_init)

    record = run_eval.run_case(
        case_dir,
        host="canned",
        canned_output="not a valid review result",
        work_root=tmp_path / "work",
    )

    assert record["passed"] is False
    assert record["verdict"] == "INCONCLUSIVE"
    assert record["coverage_gap_count"] == 1
    assert record["attempts"] == 3
    assert any("ResultParseError" in failure for failure in record["expectation_failures"])


def test_live_host_adapters_use_subprocess_argument_arrays(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    calls: list[dict[str, Any]] = []

    def fake_run(args: list[str], **kwargs: Any) -> subprocess.CompletedProcess[str]:
        calls.append({"args": args, **kwargs})
        return subprocess.CompletedProcess(args, 0, stdout=_envelope(verdict="PASS"), stderr="")

    monkeypatch.setattr(run_eval.subprocess, "run", fake_run)
    repo = tmp_path / "repo"
    repo.mkdir()

    run_eval.CodexHost().run(repo, Path(".codexspec/specs/example"))
    run_eval.ClaudeHost().run(repo, Path(".codexspec/specs/example"))

    assert calls
    assert all(isinstance(call["args"], list) for call in calls)
    assert all(call.get("shell") is not True for call in calls)
    assert calls[0]["args"][:2] == ["codex", "exec"]
    assert calls[1]["args"][:2] == ["claude", "-p"]


def test_systematic_coverage_fixtures_encode_their_review_premises(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.setattr(run_eval, "_codexspec_init", _stub_codexspec_init)
    cases_root = Path("tests/evals/review_code/cases")

    early = run_eval.load_case(cases_root / "early-finding-complete-coverage")
    early_repo, _ = run_eval.prepare_repository(early, tmp_path / "early")
    baseline_api = run_eval._git(early_repo, "show", "main:src/api.py").stdout
    assert "return 'stable'" in baseline_api
    assert "return 'renamed'" in (early_repo / "src/api.py").read_text(encoding="utf-8")

    incomplete = run_eval.load_case(cases_root / "incomplete-contract-coverage")
    incomplete_repo, _ = run_eval.prepare_repository(incomplete, tmp_path / "incomplete")
    numstat = run_eval._git(incomplete_repo, "diff", "--numstat", "main...HEAD", "--", "generated/client.bin").stdout
    assert numstat.startswith("-\t-\tgenerated/client.bin")
    assert not (incomplete_repo / "src/generator.py").exists()


def test_prepare_repository_does_not_inherit_callers_git_index(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    outer_repo = tmp_path / "outer"
    outer_repo.mkdir()
    run_eval._git(outer_repo, "init", "-b", "main")
    (outer_repo / "sentinel.txt").write_text("outer index\n", encoding="utf-8")
    run_eval._git(outer_repo, "add", "sentinel.txt")
    outer_index = outer_repo / ".git" / "index"
    original_index = outer_index.read_bytes()

    monkeypatch.setenv("GIT_INDEX_FILE", str(outer_index))
    monkeypatch.setattr(run_eval, "_codexspec_init", _stub_codexspec_init)
    case = run_eval.load_case(Path("tests/evals/review_code/cases/early-finding-complete-coverage"))

    prepared_repo, _ = run_eval.prepare_repository(case, tmp_path / "prepared")

    assert outer_index.read_bytes() == original_index
    assert (prepared_repo / ".git" / "index").is_file()


def test_review_code_eval_corpus_declares_required_cases_and_expectations() -> None:
    cases_root = Path("tests/evals/review_code/cases")
    case_dirs = run_eval.iter_cases(cases_root)

    assert {path.name for path in case_dirs} == set(EXPECTED_CASES)
    for case_dir in case_dirs:
        case = run_eval.load_case(case_dir)
        expected_profile = EXPECTED_CASES[case.case_id]
        assert expected_profile in case.data["risk_profiles"]
        assert case.data["setup"]["files"]
        assert case.data["expect"]["verdict"] in {"PASS", "FAIL", "INCONCLUSIVE"}
        assert case.data["expect"]["forbidden_findings"]
        if case.case_id.startswith("clean-"):
            assert case.data["expect"]["verdict"] == "PASS"
            assert case.data["expect"]["minimum_findings"] == []
        elif case.case_id == "incomplete-contract-coverage":
            assert case.data["expect"]["verdict"] == "INCONCLUSIVE"
            assert case.data["expect"]["minimum_findings"] == []
            assert case.data["expect"]["blocking_coverage_gap"] is True
        else:
            assert case.data["expect"]["minimum_findings"]
        assert case.data["expect"].get("acceptable_verdicts", [case.data["expect"]["verdict"]])

        if case.case_id == "verification-mutation":
            assert case.data["expect"]["verification_safety"] == "mirror_or_reject_no_mutation"

        if case.case_id == "related-propagation-defects":
            assert len(case.data["expect"]["minimum_findings"]) >= 2
            assert case.data["expect"]["root_cause_group"]
        if case.case_id == "early-finding-complete-coverage":
            assert case.data["expect"]["all_partitions_terminal"] is True
            assert "return 'stable'" in case.data["setup"]["baseline_files"]["src/api.py"]
        if case.case_id in {"contract-multi-surface", "clean-contract-propagation"}:
            assert case.data["expect"]["minimum_contract_surfaces"] >= 2
