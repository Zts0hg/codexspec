"""Canonical blueprint documents and their strict mutation protocol."""

from __future__ import annotations

import hashlib
import json
import re
import secrets
from dataclasses import dataclass, replace
from datetime import datetime
from typing import Any, Callable, Mapping

PROTOCOL_VERSION = "1"
PENDING = "pending"
IN_PROGRESS = "in_progress"
COMPLETED = "completed"
STATUSES = frozenset({PENDING, IN_PROGRESS, COMPLETED})

_FEATURE_ID_RE = re.compile(r"^\d{4}-\d{4}-\d{4}[a-z0-9]{2}$")
_FEATURE_NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
_EMBEDDED_ID_RE = re.compile(r"^\*\*Feature ID\*\*:\s*`([^`]+)`\s*$", re.MULTILINE)
_MANAGED_INPUT_RE = re.compile(
    r"^(?:Feature ID|Development Status|Feature Directory):|^\*\*Feature ID\*\*:", re.MULTILINE
)


class BlueprintError(ValueError):
    """Raised when stored blueprint content violates its canonical contract."""


@dataclass(frozen=True)
class BlueprintBlock:
    """One validated requirements block in document order."""

    feature_id: str
    development_status: str
    feature_directory: str
    requirements_markdown: str

    def serialize(self) -> str:
        body = self.requirements_markdown.rstrip("\n") + "\n"
        return (
            f"Feature ID: {self.feature_id}\n"
            f"Development Status: {self.development_status}\n"
            f"Feature Directory: {self.feature_directory}\n"
            f"{body}"
        )


@dataclass(frozen=True)
class BlueprintDocument:
    """An ordered, validated blueprint document."""

    blocks: tuple[BlueprintBlock, ...] = ()

    @classmethod
    def parse(cls, source: bytes) -> BlueprintDocument:
        try:
            text = source.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise BlueprintError("blueprint must be UTF-8") from exc
        if "\r" in text.replace("\r\n", ""):
            raise BlueprintError("blueprint contains an unsupported line ending")
        text = text.replace("\r\n", "\n")
        if not text.strip():
            return cls()

        chunks = re.split(r"(?m)^---$", text)
        blocks: list[BlueprintBlock] = []
        seen: set[str] = set()
        for chunk in chunks:
            stripped = chunk.strip()
            if not stripped:
                raise BlueprintError("blueprint contains an empty requirements block")
            lines = stripped.split("\n")
            if len(lines) < 4:
                raise BlueprintError("blueprint block is missing its managed prefix or requirements content")
            feature_id = _field(lines[0], "Feature ID")
            status = _field(lines[1], "Development Status")
            directory = _field(lines[2], "Feature Directory")
            _validate_feature_id(feature_id)
            if feature_id in seen:
                raise BlueprintError(f"duplicate Feature ID: {feature_id}")
            seen.add(feature_id)
            if status not in STATUSES:
                raise BlueprintError(f"unsupported Development Status: {status}")

            requirements_markdown = "\n".join(lines[3:]).strip() + "\n"
            embedded = _EMBEDDED_ID_RE.findall(requirements_markdown)
            if embedded != [feature_id]:
                raise BlueprintError("requirements content must contain exactly one matching Feature ID")
            _validate_directory(feature_id, status, directory)
            blocks.append(BlueprintBlock(feature_id, status, directory, requirements_markdown))
        return cls(tuple(blocks))

    def serialize(self) -> bytes:
        if not self.blocks:
            return b""
        return "\n---\n".join(block.serialize().rstrip("\n") for block in self.blocks).encode() + b"\n"

    def find(self, feature_id: str) -> tuple[int, BlueprintBlock] | None:
        for index, block in enumerate(self.blocks):
            if block.feature_id == feature_id:
                return index, block
        return None


@dataclass(frozen=True)
class OperationOutcome:
    """A domain response and the replacement bytes when it applied."""

    response: dict[str, Any]
    content: bytes


@dataclass(frozen=True)
class OperationRequest:
    operation: str
    expected_blueprint_hash: str
    payload: Mapping[str, Any]
    feature_id: str | None = None


def blueprint_hash(source: bytes) -> str:
    """Return the protocol hash for exact bytes."""
    return f"sha256:{hashlib.sha256(source).hexdigest()}"


def generate_feature_id(now: datetime | None = None) -> str:
    """Generate a timestamp-based permanent Feature ID."""
    current = now or datetime.now()
    alphabet = "abcdefghijklmnopqrstuvwxyz0123456789"
    suffix = "".join(secrets.choice(alphabet) for _ in range(2))
    return current.strftime("%Y-%m%d-%H%M") + suffix


def apply_operation(
    request_bytes: bytes,
    current_bytes: bytes,
    *,
    feature_id_factory: Callable[[], str] = generate_feature_id,
) -> OperationOutcome:
    """Validate and apply one protocol operation to exact current bytes."""
    try:
        operation = _decode_request(request_bytes)
    except (ValueError, TypeError, json.JSONDecodeError) as exc:
        return OperationOutcome(_invalid_request(str(exc)), current_bytes)

    current_hash = blueprint_hash(current_bytes)
    if operation.expected_blueprint_hash != current_hash:
        return OperationOutcome(
            _error_response("conflict", operation, current_hash, "stale_blueprint", "Blueprint has changed."),
            current_bytes,
        )

    document = BlueprintDocument.parse(current_bytes)
    try:
        replacement, feature_id, data = _apply(document, operation, feature_id_factory)
    except _ConflictError as exc:
        return OperationOutcome(_error_response("conflict", operation, current_hash, exc.code, str(exc)), current_bytes)
    except _RejectedError as exc:
        return OperationOutcome(_error_response("rejected", operation, current_hash, exc.code, str(exc)), current_bytes)

    new_content = replacement.serialize()
    return OperationOutcome(
        {
            "protocol_version": PROTOCOL_VERSION,
            "result": "applied",
            "operation": operation.operation,
            "feature_id": feature_id,
            "previous_blueprint_hash": current_hash,
            "blueprint_hash": blueprint_hash(new_content),
            "data": data,
        },
        new_content,
    )


def _field(line: str, name: str) -> str:
    prefix = f"{name}: "
    if not line.startswith(prefix) or line == prefix:
        raise BlueprintError(f"expected '{name}' as a non-empty managed field")
    return line[len(prefix) :]


def _validate_feature_id(feature_id: str) -> None:
    if not _FEATURE_ID_RE.fullmatch(feature_id):
        raise BlueprintError(f"invalid Feature ID: {feature_id}")


def _validate_directory(feature_id: str, status: str, directory: str) -> None:
    if status == PENDING:
        if directory != "not-created":
            raise BlueprintError("pending requirements must use Feature Directory: not-created")
        return
    prefix = f".codexspec/specs/{feature_id}-"
    if not directory.startswith(prefix) or not directory.endswith("/"):
        raise BlueprintError(f"feature directory must match {prefix}<feature-name>/")
    feature_name = directory[len(prefix) : -1]
    if not _FEATURE_NAME_RE.fullmatch(feature_name):
        raise BlueprintError("feature directory must contain a normalized feature name")


def _decode_request(source: bytes) -> OperationRequest:
    value = json.loads(source)
    if not isinstance(value, dict):
        raise ValueError("request must be a JSON object")
    operation = value.get("operation")
    existing = operation in {
        "replace_pending_requirement",
        "delete_pending_requirement",
        "move_pending_requirement",
        "update_status",
    }
    allowed = {"protocol_version", "operation", "expected_blueprint_hash", "payload"}
    if existing:
        allowed.add("feature_id")
    if set(value) != allowed:
        raise ValueError("request has missing or unexpected fields")
    if value["protocol_version"] != PROTOCOL_VERSION:
        raise ValueError("unsupported protocol_version")
    if not isinstance(operation, str) or operation not in {
        "append_requirement",
        "replace_pending_requirement",
        "delete_pending_requirement",
        "move_pending_requirement",
        "update_status",
    }:
        raise ValueError("unsupported operation")
    expected_hash = value["expected_blueprint_hash"]
    if not isinstance(expected_hash, str) or not re.fullmatch(r"sha256:[0-9a-f]{64}", expected_hash):
        raise ValueError("expected_blueprint_hash must be an exact sha256 value")
    payload = value["payload"]
    if not isinstance(payload, dict):
        raise ValueError("payload must be an object")
    feature_id = value.get("feature_id")
    if existing:
        if not isinstance(feature_id, str):
            raise ValueError("feature_id must be a string")
        _validate_feature_id(feature_id)
    _validate_payload(operation, payload)
    return OperationRequest(operation, expected_hash, payload, feature_id)


def _validate_payload(operation: str, payload: Mapping[str, Any]) -> None:
    if operation in {"append_requirement", "replace_pending_requirement"}:
        if set(payload) != {"feature_name", "requirements_markdown"}:
            raise ValueError(f"{operation} payload has missing or unexpected fields")
        feature_name = payload["feature_name"]
        markdown = payload["requirements_markdown"]
        if not isinstance(feature_name, str) or not _FEATURE_NAME_RE.fullmatch(feature_name):
            raise ValueError("feature_name must be normalized lowercase hyphen text")
        if not isinstance(markdown, str) or not markdown.strip():
            raise ValueError("requirements_markdown must be a non-empty string")
        normalized_markdown = markdown.replace("\r\n", "\n")
        if "\r" in normalized_markdown:
            raise ValueError("requirements_markdown contains an unsupported line ending")
        if re.search(r"(?m)^---$", normalized_markdown):
            raise ValueError("requirements_markdown contains the reserved separator")
        if _MANAGED_INPUT_RE.search(normalized_markdown):
            raise ValueError("requirements_markdown contains helper-managed metadata")
        return
    if operation == "delete_pending_requirement":
        if payload:
            raise ValueError("delete_pending_requirement payload must be empty")
        return
    if operation == "move_pending_requirement":
        position = payload.get("position")
        if position in {"first_pending", "last_pending"}:
            if set(payload) != {"position"}:
                raise ValueError("first/last move must omit reference_feature_id")
        elif position in {"before", "after"}:
            if set(payload) != {"position", "reference_feature_id"}:
                raise ValueError("before/after move requires reference_feature_id")
            reference = payload["reference_feature_id"]
            if not isinstance(reference, str):
                raise ValueError("reference_feature_id must be a string")
            _validate_feature_id(reference)
        else:
            raise ValueError("unsupported move position")
        return
    expected_keys = {"expected_status", "new_status"}
    old = payload.get("expected_status")
    new = payload.get("new_status")
    if old == PENDING and new == IN_PROGRESS:
        expected_keys.add("feature_directory")
        if not isinstance(payload.get("feature_directory"), str):
            raise ValueError("pending transition requires feature_directory")
    elif old == IN_PROGRESS and new == COMPLETED:
        pass
    else:
        if not isinstance(old, str) or not isinstance(new, str):
            raise ValueError("status fields must be strings")
    if set(payload) != expected_keys:
        raise ValueError("update_status payload has conditionally invalid fields")


def _apply(
    document: BlueprintDocument,
    operation: OperationRequest,
    feature_id_factory: Callable[[], str],
) -> tuple[BlueprintDocument, str, dict[str, Any]]:
    blocks = list(document.blocks)
    if operation.operation == "append_requirement":
        feature_id = feature_id_factory()
        _validate_feature_id(feature_id)
        if document.find(feature_id) is not None:
            raise _RejectedError("duplicate_feature_id", "Generated Feature ID already exists.")
        block = _new_pending_block(feature_id, operation.payload)
        blocks.append(block)
        return (
            BlueprintDocument(tuple(blocks)),
            feature_id,
            {
                "development_status": PENDING,
                "feature_directory": "not-created",
            },
        )

    assert operation.feature_id is not None  # nosec B101 - decode guarantees presence
    found = document.find(operation.feature_id)
    if found is None:
        raise _RejectedError("feature_not_found", "Target Feature ID does not exist.")
    index, target = found
    if operation.operation == "update_status":
        return _update_status(document, index, target, operation)
    if target.development_status != PENDING:
        raise _RejectedError("protected_status", "Only pending requirements can be changed by this operation.")

    if operation.operation == "replace_pending_requirement":
        blocks[index] = _new_pending_block(target.feature_id, operation.payload)
        return BlueprintDocument(tuple(blocks)), target.feature_id, {}
    if operation.operation == "delete_pending_requirement":
        del blocks[index]
        return BlueprintDocument(tuple(blocks)), target.feature_id, {}

    position = operation.payload["position"]
    if position in {"before", "after"} and operation.payload["reference_feature_id"] == target.feature_id:
        raise _RejectedError("self_reference", "A requirement cannot be moved relative to itself.")
    moving = blocks.pop(index)
    if position == "first_pending":
        destination = next((i for i, item in enumerate(blocks) if item.development_status == PENDING), len(blocks))
    elif position == "last_pending":
        pending_indexes = [i for i, item in enumerate(blocks) if item.development_status == PENDING]
        destination = pending_indexes[-1] + 1 if pending_indexes else len(blocks)
    else:
        reference_id = operation.payload["reference_feature_id"]
        reference = next(((i, item) for i, item in enumerate(blocks) if item.feature_id == reference_id), None)
        if reference is None:
            raise _RejectedError("reference_not_found", "Move reference Feature ID does not exist.")
        reference_index, reference_block = reference
        if reference_block.development_status != PENDING:
            raise _RejectedError("protected_reference", "Move reference must be pending.")
        destination = reference_index + (1 if position == "after" else 0)
    blocks.insert(destination, moving)
    return BlueprintDocument(tuple(blocks)), target.feature_id, {"position": position}


def _new_pending_block(feature_id: str, payload: Mapping[str, Any]) -> BlueprintBlock:
    markdown = _insert_feature_id(payload["requirements_markdown"], feature_id)
    return BlueprintBlock(feature_id, PENDING, "not-created", markdown)


def _insert_feature_id(markdown: str, feature_id: str) -> str:
    normalized = markdown.replace("\r\n", "\n").strip()
    # Split on "\n" only: str.splitlines() would also rewrite Unicode line
    # separators (U+2028, U+0085, ...) inside the confirmed requirements body.
    lines = normalized.split("\n")
    lines.insert(1, f"\n**Feature ID**: `{feature_id}`")
    return "\n".join(lines).strip() + "\n"


def _update_status(
    document: BlueprintDocument,
    index: int,
    target: BlueprintBlock,
    operation: OperationRequest,
) -> tuple[BlueprintDocument, str, dict[str, Any]]:
    expected = operation.payload["expected_status"]
    new_status = operation.payload["new_status"]
    if target.development_status != expected:
        raise _ConflictError("stale_status", "Development status has changed.")
    if expected == PENDING and new_status == IN_PROGRESS:
        directory = operation.payload["feature_directory"]
        try:
            _validate_directory(target.feature_id, IN_PROGRESS, directory)
        except BlueprintError as exc:
            raise _RejectedError("mismatched_feature_directory", str(exc)) from exc
        changed = replace(target, development_status=IN_PROGRESS, feature_directory=directory)
    elif expected == IN_PROGRESS and new_status == COMPLETED:
        changed = replace(target, development_status=COMPLETED)
    else:
        raise _RejectedError("unsupported_transition", "The requested development status transition is not allowed.")
    blocks = list(document.blocks)
    blocks[index] = changed
    return BlueprintDocument(tuple(blocks)), target.feature_id, {"development_status": new_status}


def _invalid_request(message: str) -> dict[str, Any]:
    return {
        "protocol_version": PROTOCOL_VERSION,
        "result": "invalid_request",
        "error": {"code": "invalid_request", "message": message, "details": {}},
    }


def _error_response(
    result: str,
    operation: OperationRequest,
    current_hash: str,
    code: str,
    message: str,
) -> dict[str, Any]:
    return {
        "protocol_version": PROTOCOL_VERSION,
        "result": result,
        "operation": operation.operation,
        "feature_id": operation.feature_id,
        "blueprint_hash": current_hash,
        "error": {"code": code, "message": message, "details": {}},
    }


class _RejectedError(Exception):
    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code


class _ConflictError(_RejectedError):
    pass
