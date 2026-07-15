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
}


def _envelope(
    *,
    verdict: str = "FAIL",
    profiles: list[str] | None = None,
    findings: list[dict[str, str]] | None = None,
) -> str:
    result = {
        "schema_version": "1",
        "mode": "defect",
        "verdict": verdict,
        "target": {"selector": "default", "complete_feature": True, "empty": False, "inventory_count": 1},
        "requirements_coverage": {"status": "complete", "feature": ".codexspec/specs/example"},
        "verification": {"status": "complete", "commands": []},
        "finding_counts": {"P0": 0, "P1": 0, "P2": 0, "P3": 0},
        "coverage_gap_count": 0,
        "review_context": "isolated",
        "reviewers": {"primary": "complete", "specialists": []},
        "activated_profiles": profiles or [],
        "findings": findings or [],
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

    bad = run_eval.parse_review_result(
        _envelope(
            verdict="PASS",
            profiles=[],
            findings=[{"priority": "P3", "summary": "missing tests for trivial helper"}],
        )
    )
    failed = run_eval.evaluate_result(case, bad)
    assert failed.passed is False
    assert any("expected verdict FAIL" in failure for failure in failed.failures)
    assert any("missing risk profile" in failure for failure in failed.failures)
    assert any("forbidden finding text" in failure for failure in failed.failures)


def test_canned_adapter_runs_case_and_records_credential_free_result(tmp_path: Path) -> None:
    case_dir = _write_case(tmp_path)
    output = _envelope(
        profiles=["command/process execution"],
        findings=[{"priority": "P1", "summary": "command injection through shell concatenation"}],
    )

    record = run_eval.run_case(case_dir, host="canned", canned_output=output, work_root=tmp_path / "work")

    assert record["case"] == "command-quoting"
    assert record["host"] == "canned"
    assert record["passed"] is True
    assert record["expectation_failures"] == []
    assert record["verdict"] == "FAIL"
    serialized = json.dumps(record)
    assert "prompt" not in serialized.lower()
    assert "credential" not in serialized.lower()


def test_run_case_records_parse_failure_without_aborting(tmp_path: Path) -> None:
    case_dir = _write_case(tmp_path)

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
        else:
            assert case.data["expect"]["minimum_findings"]
        assert case.data["expect"].get("acceptable_verdicts", [case.data["expect"]["verdict"]])

        if case.case_id == "verification-mutation":
            assert case.data["expect"]["verification_safety"] == "mirror_or_reject_no_mutation"
