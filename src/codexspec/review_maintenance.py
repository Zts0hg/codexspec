"""Persistent maintenance policy and target-bound review suggestion validation."""

from __future__ import annotations

import json
import re
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Any

import yaml

from .automation import AutomationError
from .worktrees import write_config_scalar


def read_auto_maintenance(config: Path) -> bool:
    """Read the boolean policy; absence defaults on, invalid explicit state refuses edits."""
    try:
        # Inspect the entry itself so an unreadable link is not treated as absent.
        config.lstat()
    except FileNotFoundError:
        return True
    except OSError as exc:
        raise AutomationError("invalid_maintenance_config", str(config)) from exc
    try:
        # Use the existing writer's dry-run validation for duplicate keys, YAML
        # layouts and aliases; read and write must agree on the managed field.
        write_config_scalar(
            config,
            "workflow",
            "auto_maintenance",
            "true",
            True,
            error_prefix="maintenance",
            dry_run=True,
        )
        data = yaml.safe_load(config.read_bytes().decode("utf-8")) or {}
    except (OSError, UnicodeDecodeError, yaml.YAMLError) as exc:
        raise AutomationError("invalid_maintenance_config", str(config)) from exc
    if "workflow" not in data:
        return True
    workflow = data["workflow"]
    if not isinstance(workflow, dict):
        raise AutomationError("invalid_workflow_section", str(config))
    if "auto_maintenance" not in workflow:
        return True
    value = workflow["auto_maintenance"]
    if type(value) is not bool:
        raise AutomationError("invalid_auto_maintenance", "Use an unquoted YAML boolean true or false.")
    return value


def write_auto_maintenance(config: Path, value: bool) -> None:
    """Persist only this policy, preserving unrelated YAML and formatting."""
    if type(value) is not bool:
        raise ValueError("auto_maintenance requires a boolean")
    write_config_scalar(
        config,
        "workflow",
        "auto_maintenance",
        str(value).lower(),
        value,
        error_prefix="maintenance",
    )


def _nonempty(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _strings(value: object) -> bool:
    return isinstance(value, list) and bool(value) and all(_nonempty(item) for item in value)


def _safe_path(value: str) -> bool:
    windows = PureWindowsPath(value)
    path = PurePosixPath(value.replace("\\", "/"))
    return (
        bool(path.parts)
        and not windows.drive
        and not path.is_absolute()
        and ".." not in path.parts
        and "\x00" not in value
    )


def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Duplicate maintenance field: {key}")
        result[key] = value
    return result


def parse_maintenance_result(output: str, fingerprint: str | None) -> dict[str, Any]:
    """Validate exactly one companion against the defect report's target identity.

    This validates shape and relationships. Repair callers still independently
    establish present benefit, change attribution and behavioral compatibility.
    """
    start, end = "<review-code-maintenance>", "</review-code-maintenance>"
    if output.count(start) != 1 or output.count(end) != 1:
        raise ValueError("Expected exactly one review-code-maintenance block")
    match = re.search(re.escape(start) + r"\s*(.*?)\s*" + re.escape(end), output, re.DOTALL)
    if match is None:
        raise ValueError("Malformed maintenance block")
    try:
        result = json.loads(match.group(1), object_pairs_hook=_unique_object)
    except (json.JSONDecodeError, RecursionError) as exc:
        raise ValueError("Invalid maintenance JSON") from exc
    if not isinstance(result, dict) or set(result) != {"schema_version", "target_fingerprint", "suggestions"}:
        raise ValueError("Invalid maintenance object fields")
    if result["schema_version"] != "1":
        raise ValueError("Unsupported maintenance schema")
    target = result["target_fingerprint"]
    if target != fingerprint or (target is not None and not _nonempty(target)):
        raise ValueError("Maintenance target fingerprint mismatch")
    suggestions = result["suggestions"]
    if not isinstance(suggestions, list) or (target is None and suggestions):
        raise ValueError("Suggestions require a resolved target")
    keys = {
        "id",
        "location",
        "summary",
        "problem",
        "improvement",
        "benefit",
        "evidence",
        "affected_paths",
        "compatibility",
    }
    identities = set()
    for item in suggestions:
        if not isinstance(item, dict) or set(item) != keys:
            raise ValueError("Invalid maintenance suggestion fields")
        if any(not _nonempty(item[key]) for key in keys - {"evidence", "affected_paths"}):
            raise ValueError("Maintenance text fields must be nonempty")
        identity = item["id"]
        if not re.fullmatch(r"M-[A-Za-z0-9-]+", identity) or identity in identities:
            raise ValueError("Invalid or duplicate maintenance identity")
        identities.add(identity)
        if not _strings(item["evidence"]) or not _strings(item["affected_paths"]):
            raise ValueError("Maintenance requires benefit evidence and affected paths")
        if any(not _safe_path(path) for path in item["affected_paths"]):
            raise ValueError("Maintenance paths must be project-relative")
        location = re.fullmatch(r"(.+):([1-9][0-9]*)", item["location"])
        if location is None or location.group(1) not in item["affected_paths"]:
            raise ValueError("Maintenance location must identify an affected path and line")
    return result
