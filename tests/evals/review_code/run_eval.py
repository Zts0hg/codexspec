"""Development-only runner for synthetic review-code evaluations."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

RESULT_RE = re.compile(r"<review-code-result>\s*(.*?)\s*</review-code-result>", re.DOTALL)
REQUIRED_RESULT_KEYS = {
    "schema_version",
    "mode",
    "verdict",
    "target",
    "requirements_coverage",
    "verification",
    "finding_counts",
    "coverage_gap_count",
    "review_context",
    "reviewers",
}
VALID_VERDICTS = {"PASS", "FAIL", "INCONCLUSIVE"}
VALID_PRIORITIES = {"P0", "P1", "P2", "P3"}


class ResultParseError(ValueError):
    """Raised when a review-code result envelope is missing or invalid."""


@dataclass(frozen=True)
class Evaluation:
    """Expectation-check outcome for one case."""

    passed: bool
    failures: list[str]


@dataclass(frozen=True)
class Case:
    """Loaded evaluation case."""

    path: Path
    data: dict[str, Any]

    @property
    def case_id(self) -> str:
        return str(self.data["id"])


def _git(repo: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            "git",
            "-c",
            "user.name=CodexSpec Eval",
            "-c",
            "user.email=eval@codexspec.invalid",
            *args,
        ],
        cwd=repo,
        text=True,
        capture_output=True,
        check=True,
    )


def _codexspec_init(repo: Path) -> None:
    command = shutil.which("codexspec") or "codexspec"
    completed = subprocess.run(
        [command, "init", str(repo), "--ai", "both", "--no-git", "--lang", "en"],
        text=True,
        capture_output=True,
    )
    if completed.returncode != 0:
        details = "\n".join(part for part in (completed.stdout.strip(), completed.stderr.strip()) if part)
        suffix = f":\n{details}" if details else "."
        raise RuntimeError(f"codexspec init failed with exit code {completed.returncode}{suffix}")


def _write_files(root: Path, files: dict[str, str]) -> None:
    for relative, content in files.items():
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")


def _validate_case(data: dict[str, Any], source: Path) -> None:
    required = {"schema_version", "id", "description", "risk_profiles", "setup", "expect"}
    missing = sorted(required - set(data))
    if missing:
        raise ValueError(f"{source}: missing required case keys: {', '.join(missing)}")
    if data["schema_version"] != "1":
        raise ValueError(f"{source}: unsupported case schema {data['schema_version']!r}")
    if not isinstance(data["risk_profiles"], list):
        raise ValueError(f"{source}: risk_profiles must be a list")
    setup = data["setup"]
    if not isinstance(setup, dict) or not isinstance(setup.get("files"), dict):
        raise ValueError(f"{source}: setup.files must be an object")
    expect = data["expect"]
    verdicts = expect.get("acceptable_verdicts", [expect.get("verdict")])
    if not isinstance(verdicts, list) or not verdicts or any(verdict not in VALID_VERDICTS for verdict in verdicts):
        raise ValueError(f"{source}: expected verdicts must be PASS, FAIL, or INCONCLUSIVE")
    for item in expect.get("minimum_findings", []):
        priorities = item.get("priorities", [item.get("priority")])
        if (
            not isinstance(priorities, list)
            or not priorities
            or any(priority not in VALID_PRIORITIES for priority in priorities)
            or not item.get("contains")
        ):
            raise ValueError(f"{source}: minimum_findings entries need priority and contains")
    aliases = expect.get("profile_aliases", {})
    if not isinstance(aliases, dict):
        raise ValueError(f"{source}: expect.profile_aliases must be an object when present")


def load_case(case_dir: Path) -> Case:
    """Load and validate one case directory."""

    source = case_dir / "case.json"
    data = json.loads(source.read_text(encoding="utf-8"))
    _validate_case(data, source)
    return Case(path=case_dir, data=data)


def iter_cases(cases_root: Path) -> list[Path]:
    """Return case directories in deterministic order."""

    if (cases_root / "case.json").is_file():
        return [cases_root]
    return sorted(path for path in cases_root.iterdir() if (path / "case.json").is_file())


def parse_review_result(output: str) -> dict[str, Any]:
    """Parse the strict review-code result envelope."""

    matches = RESULT_RE.findall(output)
    if len(matches) != 1:
        raise ResultParseError(f"expected exactly one review-code-result envelope, found {len(matches)}")
    try:
        result = json.loads(matches[0])
    except json.JSONDecodeError as exc:
        raise ResultParseError(f"invalid JSON in review-code-result envelope: {exc}") from exc

    missing = sorted(REQUIRED_RESULT_KEYS - set(result))
    if missing:
        raise ResultParseError(f"result envelope missing required keys: {', '.join(missing)}")
    if result["schema_version"] != "1":
        raise ResultParseError(f"unsupported result schema {result['schema_version']!r}")
    if result["mode"] != "defect":
        raise ResultParseError(f"unsupported mode {result['mode']!r}")
    if result["verdict"] not in VALID_VERDICTS:
        raise ResultParseError(f"unsupported verdict {result['verdict']!r}")
    counts = result["finding_counts"]
    if set(counts) != VALID_PRIORITIES or not all(isinstance(counts[key], int) for key in VALID_PRIORITIES):
        raise ResultParseError("finding_counts must contain integer P0, P1, P2, and P3 fields")
    result["_output_text"] = output
    return result


def _finding_texts(result: dict[str, Any]) -> list[str]:
    texts: list[str] = [str(result.get("_output_text", "")).lower()]
    for finding in result.get("findings", []):
        if isinstance(finding, dict):
            texts.append(json.dumps(finding, sort_keys=True).lower())
        else:
            texts.append(str(finding).lower())
    return texts


def evaluate_result(case: Case, result: dict[str, Any]) -> Evaluation:
    """Compare one parsed result with case expectations."""

    failures: list[str] = []
    expected = case.data["expect"]
    acceptable_verdicts = expected.get("acceptable_verdicts", [expected["verdict"]])
    if result["verdict"] not in acceptable_verdicts:
        failures.append(f"expected verdict {' or '.join(acceptable_verdicts)}, got {result['verdict']}")

    activated = set(result.get("activated_profiles", []))
    output_text = str(result.get("_output_text", "")).lower()
    require_profiles = expected.get("require_profiles", True)
    for profile in case.data["risk_profiles"] if require_profiles else []:
        aliases = case.data["expect"].get("profile_aliases", {}).get(profile, [])
        profile_terms = [profile, *aliases]
        if profile not in activated and not any(term.lower() in output_text for term in profile_terms):
            failures.append(f"missing risk profile: {profile}")

    finding_texts = _finding_texts(result)
    for expected_finding in expected.get("minimum_findings", []):
        expected_priorities = expected_finding.get("priorities", [expected_finding["priority"]])
        priorities = [priority.lower() for priority in expected_priorities]
        needles = [expected_finding["contains"], *expected_finding.get("aliases", [])]
        normalized_needles = [needle.lower() for needle in needles]
        if not any(
            any(priority in text for priority in priorities) and any(needle in text for needle in normalized_needles)
            for text in finding_texts
        ):
            failures.append(f"missing minimum finding: {priorities!r} containing one of {normalized_needles!r}")

    for forbidden in expected.get("forbidden_findings", []):
        needle = str(forbidden).lower()
        if any(needle in text for text in finding_texts):
            failures.append(f"forbidden finding text present: {needle!r}")

    return Evaluation(passed=not failures, failures=failures)


def prepare_repository(case: Case, work_root: Path) -> tuple[Path, Path]:
    """Create a temporary initialized repository for a case."""

    repo = work_root / case.case_id
    if repo.exists():
        shutil.rmtree(repo)
    work_root.mkdir(parents=True, exist_ok=True)
    _codexspec_init(repo)
    _git(repo, "init", "-b", "main")
    _write_files(repo, {"README.md": "# Eval fixture\n"})
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "baseline")
    _git(repo, "switch", "-c", case.case_id)

    setup = case.data["setup"]
    _write_files(repo, setup["files"])
    feature_dir = repo / ".codexspec" / "specs" / case.case_id
    feature_dir.mkdir(parents=True, exist_ok=True)
    artifacts = setup.get("feature_artifacts") or {
        "requirements.md": "# Requirements\n",
        "spec.md": "# Spec\n",
        "plan.md": "# Plan\n",
        "tasks.md": "# Tasks\n",
    }
    _write_files(feature_dir, artifacts)
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "case change")
    return repo, feature_dir


class HostAdapter:
    """Base class for review-code host adapters."""

    name = "host"

    def run(self, repo: Path, feature_dir: Path) -> str:
        raise NotImplementedError


class CannedHost(HostAdapter):
    """Adapter used by normal tests; no model or network access."""

    name = "canned"

    def __init__(self, output: str) -> None:
        self.output = output

    def run(self, repo: Path, feature_dir: Path) -> str:
        return self.output


class CodexHost(HostAdapter):
    """Invoke an authenticated Codex CLI in live mode."""

    name = "codex"

    def run(self, repo: Path, feature_dir: Path) -> str:
        feature_arg = feature_dir if not feature_dir.is_absolute() else feature_dir.relative_to(repo)
        prompt = f"$codexspec:review-code --feature {feature_arg}"
        completed = subprocess.run(
            ["codex", "exec", prompt],
            cwd=repo,
            text=True,
            capture_output=True,
            timeout=900,
        )
        return completed.stdout + completed.stderr


class ClaudeHost(HostAdapter):
    """Invoke an authenticated Claude CLI in live mode."""

    name = "claude"

    def run(self, repo: Path, feature_dir: Path) -> str:
        feature_arg = feature_dir if not feature_dir.is_absolute() else feature_dir.relative_to(repo)
        prompt = f"/codexspec:review-code --feature {feature_arg}"
        completed = subprocess.run(
            ["claude", "-p", prompt],
            cwd=repo,
            text=True,
            capture_output=True,
            timeout=900,
        )
        return completed.stdout + completed.stderr


def _adapter(host: str, canned_output: str | None) -> HostAdapter:
    if host == "canned":
        if canned_output is None:
            raise ValueError("canned host requires canned_output")
        return CannedHost(canned_output)
    if host == "codex":
        return CodexHost()
    if host == "claude":
        return ClaudeHost()
    raise ValueError(f"unsupported host: {host}")


def run_case(
    case_dir: Path,
    *,
    host: str,
    canned_output: str | None = None,
    work_root: Path | None = None,
    attempts: int = 3,
) -> dict[str, Any]:
    """Run one case and return a credential-free record."""

    case = load_case(case_dir)
    root = work_root or Path(tempfile.mkdtemp(prefix="codexspec-review-eval-"))
    started = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    last_error: Exception | None = None
    for attempt in range(1, max(attempts, 1) + 1):
        repo, feature_dir = prepare_repository(case, root)
        try:
            output = _adapter(host, canned_output).run(repo, feature_dir)
            result = parse_review_result(output)
            evaluation = evaluate_result(case, result)
            return {
                "schema_version": "1",
                "case": case.case_id,
                "host": host,
                "started_at": started,
                "attempts": attempt,
                "verdict": result["verdict"],
                "activated_profiles": result.get("activated_profiles", []),
                "finding_counts": result["finding_counts"],
                "coverage_gap_count": result["coverage_gap_count"],
                "passed": evaluation.passed,
                "expectation_failures": evaluation.failures,
            }
        except Exception as exc:
            last_error = exc

    if last_error is not None:
        verdict = "INCONCLUSIVE"
        profiles = []
        finding_counts = {"P0": 0, "P1": 0, "P2": 0, "P3": 0}
        coverage_gap_count = 1
        failures = [f"{type(last_error).__name__}: {last_error}"]
        passed = False

    return {
        "schema_version": "1",
        "case": case.case_id,
        "host": host,
        "started_at": started,
        "attempts": max(attempts, 1),
        "verdict": verdict,
        "activated_profiles": profiles,
        "finding_counts": finding_counts,
        "coverage_gap_count": coverage_gap_count,
        "passed": passed,
        "expectation_failures": failures,
    }


def run_cases(
    cases_root: Path,
    *,
    host: str,
    record_path: Path,
    canned_output: str | None = None,
    work_root: Path | None = None,
    attempts: int = 3,
) -> dict[str, Any]:
    """Run all cases under a root and write an aggregate record."""

    records = [
        run_case(case_dir, host=host, canned_output=canned_output, work_root=work_root, attempts=attempts)
        for case_dir in iter_cases(cases_root)
    ]
    aggregate = {
        "schema_version": "1",
        "host": host,
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "case_count": len(records),
        "passed": all(record["passed"] for record in records),
        "cases": records,
    }
    record_path.parent.mkdir(parents=True, exist_ok=True)
    record_path.write_text(json.dumps(aggregate, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return aggregate


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cases", type=Path, required=True)
    parser.add_argument("--host", choices=["canned", "codex", "claude"], required=True)
    parser.add_argument("--record", type=Path, required=True)
    parser.add_argument("--canned-output", type=Path)
    parser.add_argument("--work-root", type=Path)
    parser.add_argument("--attempts", type=int, default=3)
    args = parser.parse_args(argv)

    canned_output = args.canned_output.read_text(encoding="utf-8") if args.canned_output else None
    aggregate = run_cases(
        args.cases,
        host=args.host,
        record_path=args.record,
        canned_output=canned_output,
        work_root=args.work_root,
        attempts=args.attempts,
    )
    print(json.dumps({"passed": aggregate["passed"], "case_count": aggregate["case_count"]}, sort_keys=True))
    return 0 if aggregate["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
