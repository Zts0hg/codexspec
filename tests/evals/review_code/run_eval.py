"""Development-only runner for synthetic review-code evaluations."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass
from functools import lru_cache
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
    "findings",
    "finding_counts",
    "review_coverage",
    "follow_up",
    "coverage_gaps",
    "coverage_gap_count",
    "review_context",
    "reviewers",
}
VALID_VERDICTS = {"PASS", "FAIL", "INCONCLUSIVE"}
VALID_PRIORITIES = {"P0", "P1", "P2", "P3"}
VALID_SELECTORS = {"default", "committed", "uncommitted", "commit"}
VALID_REQUIREMENTS_STATUSES = {"complete", "partial", "not_evaluated"}
VALID_VERIFICATION_STATUSES = {"complete", "incomplete"}
VALID_CONTRACT_STATUSES = {"complete", "incomplete", "not_applicable"}
VALID_PARTITION_STATUSES = {"complete", "incomplete", "failed", "uninspectable"}
VALID_VARIANT_STATUSES = {"complete", "incomplete", "not_applicable"}
VALID_REVIEWER_STATES = {"complete", "incomplete", "failed", "not_required", "not_run"}


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


@lru_cache(maxsize=1)
def _git_local_env_vars() -> tuple[str, ...]:
    """Return environment variables that Git scopes to one repository."""

    completed = subprocess.run(
        ["git", "rev-parse", "--local-env-vars"],
        text=True,
        capture_output=True,
        check=True,
    )
    return tuple(completed.stdout.splitlines())


def _foreign_repo_environment() -> dict[str, str]:
    """Return an environment detached from the caller's Git repository."""

    environment = os.environ.copy()
    for name in _git_local_env_vars():
        environment.pop(name, None)
    return environment


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
        env=_foreign_repo_environment(),
        text=True,
        capture_output=True,
        check=True,
    )


def _codexspec_init(repo: Path) -> None:
    command = shutil.which("codexspec") or "codexspec"
    completed = subprocess.run(
        [command, "init", str(repo), "--ai", "both", "--no-git", "--lang", "en"],
        env=_foreign_repo_environment(),
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


def _retry_remove_writable(function: Any, path: str, _exc: Any) -> None:
    os.chmod(path, stat.S_IREAD | stat.S_IWRITE)
    function(path)


def _remove_tree(path: Path) -> None:
    if sys.version_info >= (3, 12):
        shutil.rmtree(path, onexc=_retry_remove_writable)
    else:
        shutil.rmtree(path, onerror=_retry_remove_writable)


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
    if "baseline_files" in setup and not isinstance(setup["baseline_files"], dict):
        raise ValueError(f"{source}: setup.baseline_files must be an object when present")
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
    minimum_surfaces = expect.get("minimum_contract_surfaces")
    if minimum_surfaces is not None and (
        isinstance(minimum_surfaces, bool) or not isinstance(minimum_surfaces, int) or minimum_surfaces < 1
    ):
        raise ValueError(f"{source}: expect.minimum_contract_surfaces must be a positive integer")
    if "all_partitions_terminal" in expect and not isinstance(expect["all_partitions_terminal"], bool):
        raise ValueError(f"{source}: expect.all_partitions_terminal must be a boolean")
    if "blocking_coverage_gap" in expect and not isinstance(expect["blocking_coverage_gap"], bool):
        raise ValueError(f"{source}: expect.blocking_coverage_gap must be a boolean")
    contract_trace = expect.get("required_contract_trace")
    if contract_trace is not None:
        allowed_fields = {"producers", "propagation", "consumers", "entry_surfaces", "scenarios"}
        if (
            not isinstance(contract_trace, dict)
            or not contract_trace
            or not set(contract_trace).issubset(allowed_fields)
        ):
            raise ValueError(f"{source}: expect.required_contract_trace has invalid fields")
        for field, groups in contract_trace.items():
            _validate_term_groups(groups, f"{source}: expect.required_contract_trace.{field}")
    minimum_partitions = expect.get("minimum_partitions")
    if minimum_partitions is not None and (
        isinstance(minimum_partitions, bool) or not isinstance(minimum_partitions, int) or minimum_partitions < 1
    ):
        raise ValueError(f"{source}: expect.minimum_partitions must be a positive integer")
    if "required_partition_scopes" in expect:
        _validate_term_groups(expect["required_partition_scopes"], f"{source}: expect.required_partition_scopes")
    if "required_blocking_gap_terms" in expect:
        _validate_term_groups(expect["required_blocking_gap_terms"], f"{source}: expect.required_blocking_gap_terms")
    variant_trace = expect.get("required_variant_search_trace")
    if variant_trace is not None:
        allowed_fields = {"scope", "methods", "checked_locations"}
        if not isinstance(variant_trace, dict) or set(variant_trace) != allowed_fields:
            raise ValueError(f"{source}: expect.required_variant_search_trace must define {sorted(allowed_fields)}")
        for field, groups in variant_trace.items():
            _validate_term_groups(groups, f"{source}: expect.required_variant_search_trace.{field}")


def _validate_term_groups(value: Any, name: str) -> None:
    if (
        not isinstance(value, list)
        or not value
        or any(
            not isinstance(group, list)
            or not group
            or any(not isinstance(term, str) or not term.strip() for term in group)
            for group in value
        )
    ):
        raise ValueError(f"{name} must be a non-empty array of non-empty term arrays")


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


def _object(value: Any, name: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ResultParseError(f"{name} must be an object")
    return value


def _array(value: Any, name: str) -> list[Any]:
    if not isinstance(value, list):
        raise ResultParseError(f"{name} must be an array")
    return value


def _string(value: Any, name: str, *, nullable: bool = False) -> str | None:
    if nullable and value is None:
        return None
    if not isinstance(value, str) or not value.strip():
        raise ResultParseError(f"{name} must be a non-empty string")
    return value


def _strings(value: Any, name: str, *, non_empty: bool = False) -> list[str]:
    items = _array(value, name)
    if any(not isinstance(item, str) or not item.strip() for item in items):
        raise ResultParseError(f"{name} must contain only non-empty strings")
    if non_empty and not items:
        raise ResultParseError(f"{name} must not be empty")
    return items


def _non_negative_integer(value: Any, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ResultParseError(f"{name} must be a non-negative integer")
    return value


def _required_fields(record: dict[str, Any], required: set[str], name: str) -> None:
    missing = sorted(required - set(record))
    if missing:
        raise ResultParseError(f"{name} missing required keys: {', '.join(missing)}")


def _known_fields(record: dict[str, Any], allowed: set[str], name: str) -> None:
    unknown = sorted(set(record) - allowed)
    if unknown:
        raise ResultParseError(f"{name} contains unknown keys: {', '.join(unknown)}")


def _unique_ids(records: list[dict[str, Any]], name: str, *, field: str = "id") -> set[str]:
    identifiers = [_string(record.get(field), f"{name}.{field}") for record in records]
    if len(identifiers) != len(set(identifiers)):
        raise ResultParseError(f"{name} {field} values must be unique")
    return {identifier for identifier in identifiers if identifier is not None}


def _validate_coverage(result: dict[str, Any]) -> None:
    coverage = _object(result["review_coverage"], "review_coverage")
    _required_fields(coverage, {"contracts", "partitions", "variant_searches"}, "review_coverage")
    _known_fields(coverage, {"contracts", "partitions", "variant_searches"}, "review_coverage")

    contracts = [_object(item, "contract") for item in _array(coverage["contracts"], "contracts")]
    contract_ids = _unique_ids(contracts, "contract")
    for contract in contracts:
        _required_fields(
            contract,
            {
                "id",
                "statement",
                "sources",
                "producers",
                "propagation",
                "consumers",
                "entry_surfaces",
                "scenarios",
                "evidence",
                "status",
            },
            "contract",
        )
        _known_fields(
            contract,
            {
                "id",
                "statement",
                "sources",
                "producers",
                "propagation",
                "consumers",
                "entry_surfaces",
                "scenarios",
                "evidence",
                "status",
            },
            "contract",
        )
        _string(contract["statement"], "contract.statement")
        _strings(contract["sources"], "contract.sources", non_empty=True)
        for field in ["producers", "propagation", "consumers", "entry_surfaces", "scenarios"]:
            _strings(contract[field], f"contract.{field}")
        evidence = _strings(contract["evidence"], "contract.evidence")
        if contract["status"] not in VALID_CONTRACT_STATUSES:
            raise ResultParseError(f"unsupported contract status {contract['status']!r}")
        if contract["status"] == "complete" and not evidence:
            raise ResultParseError("completed contract must include evidence")

    partitions = [_object(item, "partition") for item in _array(coverage["partitions"], "partitions")]
    _unique_ids(partitions, "partition")
    for partition in partitions:
        _required_fields(partition, {"id", "scope", "owner", "contract_ids", "evidence", "status"}, "partition")
        _known_fields(partition, {"id", "scope", "owner", "contract_ids", "evidence", "status"}, "partition")
        _string(partition["scope"], "partition.scope")
        owner = _string(partition["owner"], "partition.owner")
        if owner != "primary" and (not owner.startswith("specialist:") or not owner.removeprefix("specialist:")):
            raise ResultParseError(f"unsupported partition owner {owner!r}")
        references = _strings(partition["contract_ids"], "partition.contract_ids")
        if not set(references).issubset(contract_ids):
            raise ResultParseError("partition contains an unknown contract reference")
        evidence = _strings(partition["evidence"], "partition.evidence")
        if partition["status"] not in VALID_PARTITION_STATUSES:
            raise ResultParseError(f"unsupported partition status {partition['status']!r}")
        if partition["status"] == "complete" and not evidence:
            raise ResultParseError("completed partition must include evidence")

    findings = [_object(item, "finding") for item in _array(result["findings"], "findings")]
    finding_ids = _unique_ids(findings, "finding")
    for finding in findings:
        _required_fields(
            finding,
            {"id", "priority", "location", "summary", "trigger", "impact", "root_cause_id"},
            "finding",
        )
        _known_fields(
            finding,
            {"id", "priority", "location", "summary", "trigger", "impact", "root_cause_id"},
            "finding",
        )
        if finding["priority"] not in VALID_PRIORITIES:
            raise ResultParseError(f"unsupported finding priority {finding['priority']!r}")
        for field in ["location", "summary", "trigger", "impact"]:
            _string(finding[field], f"finding.{field}")
        _string(finding["root_cause_id"], "finding.root_cause_id", nullable=True)

    searches = [_object(item, "variant search") for item in _array(coverage["variant_searches"], "variant_searches")]
    root_cause_ids = _unique_ids(searches, "variant search", field="root_cause_id")
    for search in searches:
        _required_fields(
            search,
            {
                "root_cause_id",
                "finding_ids",
                "cause",
                "scope",
                "methods",
                "checked_locations",
                "evidence",
                "reason",
                "status",
            },
            "variant search",
        )
        _known_fields(
            search,
            {
                "root_cause_id",
                "finding_ids",
                "cause",
                "scope",
                "methods",
                "checked_locations",
                "evidence",
                "reason",
                "status",
            },
            "variant search",
        )
        _string(search["cause"], "variant_search.cause")
        references = _strings(search["finding_ids"], "variant_search.finding_ids", non_empty=True)
        if not set(references).issubset(finding_ids):
            raise ResultParseError("variant search contains an unknown finding reference")
        search_details = {
            field: _strings(search[field], f"variant_search.{field}")
            for field in ["scope", "methods", "checked_locations"]
        }
        evidence = _strings(search["evidence"], "variant_search.evidence")
        status = search["status"]
        if status not in VALID_VARIANT_STATUSES:
            raise ResultParseError(f"unsupported variant search status {status!r}")
        reason = _string(search["reason"], "variant_search.reason", nullable=True)
        if status == "complete" and not evidence:
            raise ResultParseError("completed variant search must include evidence")
        if status == "complete" and any(not values for values in search_details.values()):
            raise ResultParseError("completed variant search requires scope, methods, and checked_locations")
        if status == "complete" and reason is not None:
            raise ResultParseError("completed variant search reason must be null")
        if status in {"incomplete", "not_applicable"} and reason is None:
            raise ResultParseError(f"{status} variant search must include a reason")

    for finding in findings:
        root_cause_id = finding["root_cause_id"]
        if root_cause_id is not None and root_cause_id not in root_cause_ids:
            raise ResultParseError("finding contains an unknown root-cause reference")
    for search in searches:
        expected_findings = {
            finding["id"] for finding in findings if finding["root_cause_id"] == search["root_cause_id"]
        }
        if set(search["finding_ids"]) != expected_findings:
            raise ResultParseError("root-cause search must reference exactly its linked findings")


def _validate_follow_up(result: dict[str, Any]) -> None:
    follow_up = _object(result["follow_up"], "follow_up")
    _required_fields(follow_up, {"received", "required"}, "follow_up")
    _known_fields(follow_up, {"received", "required"}, "follow_up")
    received = [_object(item, "received follow-up") for item in _array(follow_up["received"], "follow_up.received")]
    required = [_object(item, "required follow-up") for item in _array(follow_up["required"], "follow_up.required")]
    all_records = [*received, *required]
    _unique_ids(all_records, "follow-up")
    source_ids = {
        item["id"] for collection in (result["findings"], result["review_coverage"]["contracts"]) for item in collection
    }
    for direction, records, statuses in [
        ("received", received, {"verified", "unresolved", "superseded"}),
        ("required", required, {"open"}),
    ]:
        for record in records:
            _required_fields(
                record,
                {"id", "origin_fingerprint", "source_ids", "statement", "status", "evidence"},
                f"{direction} follow-up",
            )
            _known_fields(
                record,
                {"id", "origin_fingerprint", "source_ids", "statement", "status", "evidence"},
                f"{direction} follow-up",
            )
            origin_fingerprint = _string(
                record["origin_fingerprint"],
                f"{direction} follow-up.origin_fingerprint",
                nullable=direction == "required" and result["target"]["fingerprint"] is None,
            )
            references = _strings(record["source_ids"], f"{direction} follow-up.source_ids", non_empty=True)
            if direction == "required" and not set(references).issubset(source_ids):
                raise ResultParseError("required follow-up contains an unknown source reference")
            _string(record["statement"], f"{direction} follow-up.statement")
            if record["status"] not in statuses:
                raise ResultParseError(f"unsupported {direction} follow-up status {record['status']!r}")
            evidence = _strings(record["evidence"], f"{direction} follow-up.evidence")
            if direction == "received" and record["status"] in {"verified", "superseded"} and not evidence:
                raise ResultParseError(f"{record['status']} follow-up must include evidence")
            if direction == "required" and origin_fingerprint != result["target"]["fingerprint"]:
                raise ResultParseError("required follow-up origin_fingerprint must match the current target")

    required_source_ids = {source_id for record in required for source_id in record["source_ids"]}
    finding_ids = {finding["id"] for finding in result["findings"]}
    if not finding_ids.issubset(required_source_ids):
        raise ResultParseError("every finding must have a required follow-up obligation")


def _validate_gaps_and_reviewers(result: dict[str, Any]) -> None:
    gaps = [_object(item, "coverage gap") for item in _array(result["coverage_gaps"], "coverage_gaps")]
    _unique_ids(gaps, "coverage gap")
    for gap in gaps:
        _required_fields(gap, {"id", "scope", "impact", "blocking"}, "coverage gap")
        _known_fields(gap, {"id", "scope", "impact", "blocking"}, "coverage gap")
        _string(gap["scope"], "coverage_gap.scope")
        _string(gap["impact"], "coverage_gap.impact")
        if not isinstance(gap["blocking"], bool):
            raise ResultParseError("coverage_gap.blocking must be a boolean")
    if _non_negative_integer(result["coverage_gap_count"], "coverage_gap_count") != len(gaps):
        raise ResultParseError("coverage gap count matches neither coverage_gaps nor the human report")

    reviewers = _object(result["reviewers"], "reviewers")
    _required_fields(reviewers, {"primary", "specialists"}, "reviewers")
    _known_fields(reviewers, {"primary", "specialists"}, "reviewers")
    if reviewers["primary"] not in VALID_REVIEWER_STATES:
        raise ResultParseError(f"unsupported primary reviewer state {reviewers['primary']!r}")
    specialists = [_object(item, "specialist") for item in _array(reviewers["specialists"], "reviewers.specialists")]
    specialist_profiles: set[str] = set()
    specialist_states: dict[str, str] = {}
    for record in specialists:
        _required_fields(record, {"profile", "state"}, "specialist")
        _known_fields(record, {"profile", "state", "reason"}, "specialist")
        profile = _string(record["profile"], "specialist.profile")
        if profile in specialist_profiles:
            raise ResultParseError("specialist profiles must be unique")
        specialist_profiles.add(profile)
        if record["state"] not in VALID_REVIEWER_STATES:
            raise ResultParseError(f"unsupported specialist state {record['state']!r}")
        specialist_states[profile] = record["state"]
        if "reason" in record:
            _string(record["reason"], "specialist.reason")

    for partition in result["review_coverage"]["partitions"]:
        owner = partition["owner"]
        if owner == "primary":
            owner_state = reviewers["primary"]
            if owner_state == "not_required":
                raise ResultParseError("primary partition owner cannot be not_required")
        else:
            profile = owner.removeprefix("specialist:")
            if profile not in specialist_profiles:
                raise ResultParseError("specialist partition owner must reference a declared specialist reviewer")
            owner_state = specialist_states[profile]
            if owner_state == "not_required":
                raise ResultParseError("owned specialist reviewer cannot be not_required")
        if partition["status"] == "complete" and owner_state != "complete":
            raise ResultParseError("completed partition requires a complete owner")

    if result["review_context"] == "shared" and not any(gap["scope"] == "reviewer isolation" for gap in gaps):
        raise ResultParseError("shared review context requires a reviewer isolation coverage gap")


def _validate_verdict_consistency(result: dict[str, Any]) -> None:
    verdict = result["verdict"]
    blocking_gaps = [gap for gap in result["coverage_gaps"] if gap["blocking"]]
    if verdict == "FAIL":
        if not result["findings"]:
            raise ResultParseError("FAIL requires at least one admitted finding")
        return
    if verdict == "INCONCLUSIVE":
        if not blocking_gaps:
            raise ResultParseError("INCONCLUSIVE requires a blocking coverage gap")
        if result["findings"]:
            raise ResultParseError("INCONCLUSIVE cannot contain admitted findings; use FAIL")
        return
    if result["verification"]["status"] != "complete":
        raise ResultParseError("PASS requires complete verification")
    if result["requirements_coverage"]["status"] != "complete":
        raise ResultParseError("PASS requires complete requirements coverage")
    if any(result["finding_counts"].values()):
        raise ResultParseError("PASS requires zero findings")
    coverage = result["review_coverage"]
    if any(record["status"] != "complete" for record in coverage["contracts"]):
        raise ResultParseError("PASS requires complete contract coverage")
    if any(record["status"] != "complete" for record in coverage["partitions"]):
        raise ResultParseError("PASS requires complete partition coverage")
    if any(record["status"] != "complete" for record in coverage["variant_searches"]):
        raise ResultParseError("PASS requires complete variant searches")
    if any(record["status"] not in {"verified", "superseded"} for record in result["follow_up"]["received"]):
        raise ResultParseError("PASS cannot contain unresolved follow-up obligations")
    if result["follow_up"]["required"]:
        raise ResultParseError("PASS cannot contain open follow-up obligations")
    if blocking_gaps:
        raise ResultParseError("PASS cannot contain a blocking coverage gap")
    if result["reviewers"]["primary"] != "complete" or any(
        specialist["state"] not in {"complete", "not_required"} for specialist in result["reviewers"]["specialists"]
    ):
        raise ResultParseError("PASS requires complete reviewer topology")


def parse_review_result(output: str) -> dict[str, Any]:
    """Parse the strict review-code result envelope."""

    matches = RESULT_RE.findall(output)
    if len(matches) != 1:
        raise ResultParseError(f"expected exactly one review-code-result envelope, found {len(matches)}")
    try:
        result = json.loads(matches[0])
    except json.JSONDecodeError as exc:
        raise ResultParseError(f"invalid JSON in review-code-result envelope: {exc}") from exc

    result = _object(result, "result envelope")
    missing = sorted(REQUIRED_RESULT_KEYS - set(result))
    if missing:
        raise ResultParseError(f"result envelope missing required keys: {', '.join(missing)}")
    _known_fields(result, REQUIRED_RESULT_KEYS, "result envelope")
    if result["schema_version"] != "2":
        raise ResultParseError(f"unsupported result schema {result['schema_version']!r}")
    if result["mode"] != "defect":
        raise ResultParseError(f"unsupported mode {result['mode']!r}")
    if result["verdict"] not in VALID_VERDICTS:
        raise ResultParseError(f"unsupported verdict {result['verdict']!r}")
    target = _object(result["target"], "target")
    _required_fields(
        target,
        {
            "selector",
            "fingerprint",
            "complete_feature",
            "empty",
            "base_ref",
            "merge_base_sha",
            "commit_sha",
            "parent_sha",
            "inventory_count",
        },
        "target",
    )
    _known_fields(
        target,
        {
            "selector",
            "fingerprint",
            "complete_feature",
            "empty",
            "base_ref",
            "merge_base_sha",
            "commit_sha",
            "parent_sha",
            "inventory_count",
        },
        "target",
    )
    if target["selector"] not in VALID_SELECTORS:
        raise ResultParseError(f"unsupported target selector {target['selector']!r}")
    fingerprint = _string(target["fingerprint"], "target fingerprint", nullable=True)
    if not isinstance(target["complete_feature"], bool):
        raise ResultParseError("target.complete_feature must be a boolean")
    if not isinstance(target["empty"], bool):
        raise ResultParseError("target.empty must be a boolean")
    for field in ["base_ref", "merge_base_sha", "commit_sha", "parent_sha"]:
        _string(target[field], f"target.{field}", nullable=True)
    inventory_count = _non_negative_integer(target["inventory_count"], "target.inventory_count")
    if target["empty"] != (inventory_count == 0):
        raise ResultParseError("target.empty must agree with target.inventory_count")
    selector = target["selector"]
    if fingerprint is None:
        if result["verdict"] == "PASS":
            raise ResultParseError("PASS requires a target fingerprint")
        gaps = _array(result["coverage_gaps"], "coverage_gaps")
        if not any(
            isinstance(gap, dict) and gap.get("blocking") is True and gap.get("scope") == "target identity"
            for gap in gaps
        ):
            raise ResultParseError("a missing target fingerprint requires a blocking target identity coverage gap")
        if target["complete_feature"]:
            raise ResultParseError("a target with unavailable identity cannot be a complete feature")
        if selector in {"default", "committed"}:
            if target["commit_sha"] is not None or target["parent_sha"] is not None:
                raise ResultParseError("unavailable default or committed identity cannot include commit-only SHAs")
        elif selector == "uncommitted":
            if any(target[field] is not None for field in ["base_ref", "merge_base_sha", "commit_sha", "parent_sha"]):
                raise ResultParseError("uncommitted selector cannot include base or commit identity")
        elif target["base_ref"] is not None or target["merge_base_sha"] is not None:
            raise ResultParseError("unavailable commit identity cannot include base_ref or merge_base_sha")
    else:
        if selector in {"uncommitted", "commit"} and target["complete_feature"]:
            raise ResultParseError(f"{selector} target cannot be a complete feature")
        if selector in {"default", "committed"}:
            if target["base_ref"] is None or target["merge_base_sha"] is None:
                raise ResultParseError(f"{selector} selector requires base_ref and merge_base_sha")
            if target["commit_sha"] is not None or target["parent_sha"] is not None:
                raise ResultParseError("commit_sha and parent_sha are only valid with the commit selector")
        elif selector == "uncommitted":
            if any(target[field] is not None for field in ["base_ref", "merge_base_sha", "commit_sha", "parent_sha"]):
                raise ResultParseError("uncommitted selector cannot include base or commit identity")
        else:
            if target["base_ref"] is not None or target["merge_base_sha"] is not None:
                raise ResultParseError("commit selector cannot include base_ref or merge_base_sha")
            if target["commit_sha"] is None:
                raise ResultParseError("commit selector requires commit_sha")
            if target["parent_sha"] is None:
                raise ResultParseError("commit selector requires parent_sha")

    requirements = _object(result["requirements_coverage"], "requirements_coverage")
    _required_fields(requirements, {"status", "feature"}, "requirements_coverage")
    _known_fields(requirements, {"status", "feature"}, "requirements_coverage")
    if requirements["status"] not in VALID_REQUIREMENTS_STATUSES:
        raise ResultParseError(f"unsupported requirements status {requirements['status']!r}")
    feature = _string(requirements["feature"], "requirements_coverage.feature", nullable=True)
    if requirements["status"] == "complete" and not target["complete_feature"]:
        raise ResultParseError("complete requirements coverage requires a complete feature target")
    if requirements["status"] in {"complete", "partial"} and feature is None:
        raise ResultParseError(f"{requirements['status']} requirements coverage requires a feature")

    verification = _object(result["verification"], "verification")
    _required_fields(verification, {"status", "commands"}, "verification")
    _known_fields(verification, {"status", "commands"}, "verification")
    if verification["status"] not in VALID_VERIFICATION_STATUSES:
        raise ResultParseError(f"unsupported verification status {verification['status']!r}")
    _strings(verification["commands"], "verification.commands")

    counts = _object(result["finding_counts"], "finding_counts")
    if set(counts) != VALID_PRIORITIES or not all(
        not isinstance(counts[key], bool) and isinstance(counts[key], int) and counts[key] >= 0
        for key in VALID_PRIORITIES
    ):
        raise ResultParseError("finding_counts must contain integer P0, P1, P2, and P3 fields")
    findings = _array(result["findings"], "findings")
    actual_counts = {priority: 0 for priority in VALID_PRIORITIES}
    for finding in findings:
        record = _object(finding, "finding")
        if record.get("priority") in actual_counts:
            actual_counts[record["priority"]] += 1
    if counts != actual_counts:
        raise ResultParseError("finding counts match neither findings nor the human report")

    if result["review_context"] not in {"isolated", "shared"}:
        raise ResultParseError(f"unsupported review context {result['review_context']!r}")
    _validate_coverage(result)
    if not target["empty"]:
        if not result["review_coverage"]["contracts"]:
            raise ResultParseError("a non-empty target requires contract coverage")
        if not result["review_coverage"]["partitions"]:
            raise ResultParseError("a non-empty target requires review partitions")
    _validate_follow_up(result)
    _validate_gaps_and_reviewers(result)
    _validate_verdict_consistency(result)
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


def _matches_term_groups(text: str, groups: list[list[str]]) -> bool:
    normalized = text.lower()
    return all(any(term.lower() in normalized for term in group) for group in groups)


def _has_distinct_candidates(candidate_sets: list[set[str]], allowed: set[str] | None = None) -> bool:
    def assign(index: int, used: set[str]) -> bool:
        if index == len(candidate_sets):
            return True
        candidates = candidate_sets[index] if allowed is None else candidate_sets[index] & allowed
        return any(assign(index + 1, used | {candidate}) for candidate in candidates - used)

    return assign(0, set())


def _finding_matches_expectation(finding: dict[str, Any], expected: dict[str, Any]) -> bool:
    priorities = set(expected.get("priorities") or [expected["priority"]])
    terms = [expected["contains"], *expected.get("aliases", [])]
    text = json.dumps(finding, sort_keys=True).lower()
    return finding.get("priority") in priorities and any(term.lower() in text for term in terms)


def _observed_profiles(case: Case, result: dict[str, Any]) -> list[str]:
    output_text = str(result.get("_output_text", "")).lower()
    observed: list[str] = []
    for profile in case.data["risk_profiles"]:
        aliases = case.data["expect"].get("profile_aliases", {}).get(profile, [])
        if any(term.lower() in output_text for term in [profile, *aliases]):
            observed.append(profile)
    return observed


def evaluate_result(case: Case, result: dict[str, Any]) -> Evaluation:
    """Compare one parsed result with case expectations."""

    failures: list[str] = []
    expected = case.data["expect"]
    acceptable_verdicts = expected.get("acceptable_verdicts", [expected["verdict"]])
    if result["verdict"] not in acceptable_verdicts:
        failures.append(f"expected verdict {' or '.join(acceptable_verdicts)}, got {result['verdict']}")

    activated = set(_observed_profiles(case, result))
    require_profiles = expected.get("require_profiles", True)
    for profile in case.data["risk_profiles"] if require_profiles else []:
        if profile not in activated:
            failures.append(f"missing risk profile: {profile}")

    structured_findings = [finding for finding in result["findings"] if isinstance(finding, dict)]
    expected_findings = expected.get("minimum_findings", [])
    finding_candidate_sets: list[set[str]] = []
    for expected_finding in expected_findings:
        candidates = {
            finding["id"] for finding in structured_findings if _finding_matches_expectation(finding, expected_finding)
        }
        finding_candidate_sets.append(candidates)
        if not candidates:
            priorities = expected_finding.get("priorities", [expected_finding["priority"]])
            needles = [expected_finding["contains"], *expected_finding.get("aliases", [])]
            failures.append(f"missing minimum finding: {priorities!r} containing one of {needles!r}")
    if finding_candidate_sets and not _has_distinct_candidates(finding_candidate_sets):
        failures.append("minimum finding expectations must match distinct structured findings")

    finding_texts = _finding_texts(result)
    for forbidden in expected.get("forbidden_findings", []):
        needle = str(forbidden).lower()
        if any(needle in text for text in finding_texts):
            failures.append(f"forbidden finding text present: {needle!r}")

    coverage = result["review_coverage"]
    minimum_surfaces = expected.get("minimum_contract_surfaces")
    if minimum_surfaces is not None:
        surfaces = {surface for contract in coverage["contracts"] for surface in contract["entry_surfaces"]}
        if len(surfaces) < minimum_surfaces:
            failures.append(f"expected at least {minimum_surfaces} contract entry surfaces, got {len(surfaces)}")

    required_contract_trace = expected.get("required_contract_trace")
    if required_contract_trace and not any(
        all(
            _matches_term_groups("\n".join(contract[field]), groups)
            for field, groups in required_contract_trace.items()
        )
        for contract in coverage["contracts"]
    ):
        failures.append("expected one contract trace with all required producer-to-consumer roles and scenarios")

    grouped_searches = [
        search
        for search in coverage["variant_searches"]
        if _has_distinct_candidates(finding_candidate_sets, set(search["finding_ids"]))
    ]
    if expected.get("root_cause_group") and not grouped_searches:
        failures.append("expected at least two findings in one root-cause variant search")

    required_variant_trace = expected.get("required_variant_search_trace")
    if required_variant_trace and not any(
        all(_matches_term_groups("\n".join(search[field]), groups) for field, groups in required_variant_trace.items())
        for search in grouped_searches
    ):
        failures.append("expected grouped findings with the required bounded variant search trace")

    minimum_partitions = expected.get("minimum_partitions")
    if minimum_partitions is not None and len(coverage["partitions"]) < minimum_partitions:
        failures.append(f"expected at least {minimum_partitions} review partitions")

    required_partition_scopes = expected.get("required_partition_scopes")
    if required_partition_scopes:
        partition_candidates = [
            {
                partition["id"]
                for partition in coverage["partitions"]
                if _matches_term_groups(partition["scope"], [terms])
            }
            for terms in required_partition_scopes
        ]
        if not _has_distinct_candidates(partition_candidates):
            failures.append("expected distinct review partitions for every required semantic scope")

    if expected.get("all_partitions_terminal"):
        partitions = coverage["partitions"]
        terminal = VALID_PARTITION_STATUSES
        if not partitions or any(partition["status"] not in terminal for partition in partitions):
            failures.append("expected every review partition to have a terminal state")

    if expected.get("blocking_coverage_gap") and not any(gap["blocking"] for gap in result["coverage_gaps"]):
        failures.append("expected a blocking coverage gap")

    required_gap_terms = expected.get("required_blocking_gap_terms")
    if required_gap_terms and not any(
        gap["blocking"] and _matches_term_groups(f"{gap['scope']}\n{gap['impact']}", required_gap_terms)
        for gap in result["coverage_gaps"]
    ):
        failures.append("expected a blocking coverage gap tied to the declared fixture premise")

    return Evaluation(passed=not failures, failures=failures)


def prepare_repository(case: Case, work_root: Path) -> tuple[Path, Path]:
    """Create a temporary initialized repository for a case."""

    repo = work_root / case.case_id
    if repo.exists():
        _remove_tree(repo)
    work_root.mkdir(parents=True, exist_ok=True)
    _codexspec_init(repo)
    _git(repo, "init", "-b", "main")
    _write_files(repo, {"README.md": "# Eval fixture\n", **case.data["setup"].get("baseline_files", {})})
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
            env=_foreign_repo_environment(),
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
            env=_foreign_repo_environment(),
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
                "activated_profiles": _observed_profiles(case, result),
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
