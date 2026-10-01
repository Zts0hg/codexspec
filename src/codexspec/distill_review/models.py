"""Versioned data models shared by every distill-review carrier."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import asdict, dataclass, field
from typing import Any

SCHEMA_VERSION = 1
ACTIONS = frozenset({"vet", "replace", "remove", "merge", "defer", "keep_separate"})


def _valid_hash(value: object) -> bool:
    return isinstance(value, str) and len(value) == 64 and all(character in "0123456789abcdef" for character in value)


def _string_mapping(value: object) -> bool:
    return isinstance(value, dict) and all(
        isinstance(key, str) and isinstance(item, str) for key, item in value.items()
    )


def _validate_decision(key: str, decision: dict[str, Any]) -> None:
    action = decision.get("action")
    if action in {"vet", "replace"}:
        required = {"action", "base_hash", "fields", "status", "verification", "rendered"}
        valid = (
            set(decision) == required
            and _valid_hash(decision.get("base_hash"))
            and _string_mapping(decision.get("fields"))
            and decision.get("status") in {"candidate", "vetted"}
            and (action != "vet" or decision.get("status") == "vetted")
            and isinstance(decision.get("verification"), str)
            and isinstance(decision.get("rendered"), str)
        )
    elif action == "remove":
        valid = set(decision) == {"action", "base_hash"} and _valid_hash(decision.get("base_hash"))
    elif action == "merge":
        required = {
            "action",
            "cluster",
            "members",
            "member_hashes",
            "category",
            "record_id",
            "filename",
            "markdown",
            "field_changes",
            "status",
            "verification",
            "proposal_markdown",
            "editable_fields",
        }
        members = decision.get("members")
        member_hashes = decision.get("member_hashes")
        valid = (
            set(decision) == required
            and isinstance(decision.get("cluster"), str)
            and key == f"cluster:{decision.get('cluster')}"
            and isinstance(members, list)
            and bool(members)
            and len(members) == len(set(members))
            and all(isinstance(member, str) and member for member in members)
            and isinstance(member_hashes, dict)
            and set(member_hashes) == set(members)
            and all(_valid_hash(value) for value in member_hashes.values())
            and all(
                isinstance(decision.get(field), str) and decision.get(field)
                for field in ("category", "record_id", "filename", "markdown")
            )
            and _string_mapping(decision.get("field_changes"))
            and isinstance(decision.get("proposal_markdown"), str)
            and bool(decision.get("proposal_markdown"))
            and _string_mapping(decision.get("editable_fields"))
            and decision.get("status") in {"candidate", "vetted"}
            and isinstance(decision.get("verification"), str)
        )
    else:
        valid = False
    if not valid:
        raise ValueError(f"invalid_draft_decision: {key}")


@dataclass(frozen=True)
class VerificationAttestation:
    outcome: str

    def validate(self) -> None:
        if not self.outcome.strip():
            raise ValueError("verification_required")


@dataclass
class ReviewDraft:
    schema_version: int = SCHEMA_VERSION
    revision: int = 0
    decisions: dict[str, dict[str, Any]] = field(default_factory=dict)
    deferred: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> ReviewDraft:
        if value.get("schema_version") != SCHEMA_VERSION:
            raise ValueError("unsupported_draft_schema")
        revision = value.get("revision")
        decisions = value.get("decisions")
        deferred = value.get("deferred")
        if not isinstance(revision, int) or revision < 0:
            raise ValueError("invalid_draft_revision")
        if not isinstance(decisions, dict) or not isinstance(deferred, list):
            raise ValueError("invalid_draft_shape")
        merge_members: set[str] = set()
        merge_record_ids: set[str] = set()
        record_decisions: set[str] = set()
        for record_id, decision in decisions.items():
            if not isinstance(record_id, str) or not isinstance(decision, dict):
                raise ValueError("invalid_draft_decision")
            _validate_decision(record_id, decision)
            if decision["action"] == "merge":
                output_id = decision["record_id"]
                if output_id in merge_record_ids:
                    raise ValueError("duplicate_draft_record_id")
                merge_record_ids.add(output_id)
                merge_members.update(decision["members"])
            else:
                record_decisions.add(record_id)
        if any(not isinstance(item, str) for item in deferred):
            raise ValueError("invalid_draft_deferred")
        if record_decisions & merge_members or set(deferred) & (record_decisions | merge_members):
            raise ValueError("conflicting_draft_decision")
        return cls(revision=revision, decisions=deepcopy(decisions), deferred=list(dict.fromkeys(deferred)))
