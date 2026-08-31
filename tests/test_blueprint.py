"""Tests for blueprint document parsing and operation protocol."""

import json

import pytest

from codexspec.blueprint import (
    BlueprintDocument,
    BlueprintError,
    apply_operation,
    blueprint_hash,
)

FEATURE_ID = "2026-0830-1030ab"
OTHER_ID = "2026-0830-1045cd"


def requirements(feature_id: str = FEATURE_ID, title: str = "User authentication") -> str:
    return (
        f"# Confirmed Requirements: {title}\n\n"
        f"**Feature ID**: `{feature_id}`\n"
        "**Status**: Confirmed\n\n"
        "## Requirements\n\n"
        "### NEED-001: Authenticate users\n\n"
        "Users can authenticate securely.\n"
    )


def unmanaged_requirements(title: str = "User authentication") -> str:
    return requirements(FEATURE_ID, title).replace(f"**Feature ID**: `{FEATURE_ID}`\n", "")


def block(
    feature_id: str = FEATURE_ID,
    *,
    status: str = "pending",
    directory: str = "not-created",
    title: str = "User authentication",
) -> str:
    return (
        f"Feature ID: {feature_id}\n"
        f"Development Status: {status}\n"
        f"Feature Directory: {directory}\n"
        f"{requirements(feature_id, title)}"
    )


def request(operation: str, expected_hash: str, payload: dict[str, object], **extra: object) -> bytes:
    body = {
        "protocol_version": "1",
        "operation": operation,
        "expected_blueprint_hash": expected_hash,
        "payload": payload,
        **extra,
    }
    return json.dumps(body).encode()


def test_document_round_trip_lf_and_preserves_requirements_body() -> None:
    source = block().encode()
    document = BlueprintDocument.parse(source)
    assert document.blocks[0].requirements_markdown == requirements()
    assert document.serialize() == source


def test_document_boundary_does_not_depend_on_requirements_headings() -> None:
    body = f"Arbitrary requirements content\n\n**Feature ID**: `{FEATURE_ID}`\n\nNo fixed heading is required.\n"
    source = (f"Feature ID: {FEATURE_ID}\nDevelopment Status: pending\nFeature Directory: not-created\n{body}").encode()
    document = BlueprintDocument.parse(source)
    assert document.blocks[0].requirements_markdown == body
    assert document.serialize() == source


def test_document_normalizes_crlf_and_multiple_blocks() -> None:
    source = f"{block()}\n---\n{block(OTHER_ID, title='Release notes')}".replace("\n", "\r\n").encode()
    document = BlueprintDocument.parse(source)
    assert len(document.blocks) == 2
    assert b"\r" not in document.serialize()
    assert document.serialize().endswith(b"\n")


@pytest.mark.parametrize(
    "source",
    [
        "Development Status: pending\nFeature Directory: not-created\n" + requirements(),
        "Feature ID: broken\nDevelopment Status: pending\nFeature Directory: not-created\n" + requirements("broken"),
        block().replace("Development Status: pending", "Development Status: blocked"),
        block().replace("Feature Directory: not-created", "Feature Directory: .codexspec/specs/wrong"),
        block().replace(f"`{FEATURE_ID}`", f"`{OTHER_ID}`"),
        f"{block()}\n---\nfree prose\n---\n{block(OTHER_ID)}",
        block().replace("## Requirements", "---\n## Requirements"),
        f"{block()}\n--- \n{block(OTHER_ID)}",
        f"{block()}\n---\n{block()}",
    ],
)
def test_document_rejects_invalid_structure(source: str) -> None:
    with pytest.raises(BlueprintError):
        BlueprintDocument.parse(source.encode())


def test_document_hashes_exact_bytes() -> None:
    lf = block().encode()
    crlf = block().replace("\n", "\r\n").encode()
    assert blueprint_hash(lf) != blueprint_hash(crlf)
    assert blueprint_hash(lf).startswith("sha256:")


def test_protocol_append_applied_with_generated_id() -> None:
    current = b""
    req = request(
        "append_requirement",
        blueprint_hash(current),
        {"feature_name": "user-authentication", "requirements_markdown": unmanaged_requirements()},
    )
    outcome = apply_operation(req, current, feature_id_factory=lambda: FEATURE_ID)
    assert outcome.response["result"] == "applied"
    assert outcome.response["feature_id"] == FEATURE_ID
    assert outcome.response["previous_blueprint_hash"] == blueprint_hash(current)
    assert outcome.response["blueprint_hash"] == blueprint_hash(outcome.content)
    assert BlueprintDocument.parse(outcome.content).blocks[0].feature_id == FEATURE_ID


def test_protocol_append_normalizes_crlf_requirements() -> None:
    current = b""
    req = request(
        "append_requirement",
        blueprint_hash(current),
        {
            "feature_name": "user-authentication",
            "requirements_markdown": unmanaged_requirements().replace("\n", "\r\n"),
        },
    )
    outcome = apply_operation(req, current, feature_id_factory=lambda: FEATURE_ID)
    assert outcome.response["result"] == "applied"
    assert b"\r" not in outcome.content


def test_protocol_replace_delete_and_move_pending() -> None:
    current = f"{block()}\n---\n{block(OTHER_ID, title='Release notes')}".encode()
    replace = request(
        "replace_pending_requirement",
        blueprint_hash(current),
        {"feature_name": "renamed-feature", "requirements_markdown": unmanaged_requirements("Renamed feature")},
        feature_id=FEATURE_ID,
    )
    replaced = apply_operation(replace, current)
    assert replaced.response["result"] == "applied"
    assert b"Renamed feature" in replaced.content

    move = request(
        "move_pending_requirement",
        blueprint_hash(replaced.content),
        {"position": "after", "reference_feature_id": OTHER_ID},
        feature_id=FEATURE_ID,
    )
    moved = apply_operation(move, replaced.content)
    assert [item.feature_id for item in BlueprintDocument.parse(moved.content).blocks] == [OTHER_ID, FEATURE_ID]

    delete = request(
        "delete_pending_requirement",
        blueprint_hash(moved.content),
        {},
        feature_id=FEATURE_ID,
    )
    deleted = apply_operation(delete, moved.content)
    assert deleted.response["data"] == {}
    assert [item.feature_id for item in BlueprintDocument.parse(deleted.content).blocks] == [OTHER_ID]


@pytest.mark.parametrize(
    ("payload", "expected"),
    [
        ({"position": "first_pending"}, [OTHER_ID, FEATURE_ID]),
        ({"position": "last_pending"}, [FEATURE_ID, OTHER_ID]),
        ({"position": "before", "reference_feature_id": FEATURE_ID}, [OTHER_ID, FEATURE_ID]),
        ({"position": "after", "reference_feature_id": FEATURE_ID}, [FEATURE_ID, OTHER_ID]),
    ],
)
def test_protocol_supports_every_pending_move_position(payload: dict[str, str], expected: list[str]) -> None:
    current = f"{block()}\n---\n{block(OTHER_ID, title='Release notes')}".encode()
    raw = request(
        "move_pending_requirement",
        blueprint_hash(current),
        payload,
        feature_id=OTHER_ID,
    )
    outcome = apply_operation(raw, current)
    assert outcome.response["result"] == "applied"
    assert [item.feature_id for item in BlueprintDocument.parse(outcome.content).blocks] == expected


def test_protocol_status_transitions_preserve_directory() -> None:
    current = block().encode()
    directory = f".codexspec/specs/{FEATURE_ID}-user-authentication/"
    start = request(
        "update_status",
        blueprint_hash(current),
        {"expected_status": "pending", "new_status": "in_progress", "feature_directory": directory},
        feature_id=FEATURE_ID,
    )
    started = apply_operation(start, current)
    assert BlueprintDocument.parse(started.content).blocks[0].feature_directory == directory

    finish = request(
        "update_status",
        blueprint_hash(started.content),
        {"expected_status": "in_progress", "new_status": "completed"},
        feature_id=FEATURE_ID,
    )
    finished = apply_operation(finish, started.content)
    completed = BlueprintDocument.parse(finished.content).blocks[0]
    assert completed.development_status == "completed"
    assert completed.feature_directory == directory


@pytest.mark.parametrize(
    "raw",
    [
        b"not json",
        b"[]",
        json.dumps({"protocol_version": "2"}).encode(),
        request("unknown", blueprint_hash(b""), {}),
        request("append_requirement", blueprint_hash(b""), {}, feature_id=FEATURE_ID),
        request("delete_pending_requirement", blueprint_hash(b""), {"extra": True}, feature_id=FEATURE_ID),
        request(
            "move_pending_requirement",
            blueprint_hash(b""),
            {"position": "first_pending", "reference_feature_id": OTHER_ID},
            feature_id=FEATURE_ID,
        ),
        request(
            "append_requirement",
            blueprint_hash(b""),
            {"feature_name": "../escape", "requirements_markdown": "# x\n"},
        ),
        request(
            "append_requirement",
            blueprint_hash(b""),
            {"feature_name": "User Auth", "requirements_markdown": "# x\n"},
        ),
    ],
)
def test_protocol_invalid_request_shape(raw: bytes) -> None:
    outcome = apply_operation(raw, b"")
    assert set(outcome.response) == {"protocol_version", "result", "error"}
    assert outcome.response["result"] == "invalid_request"
    assert outcome.response["error"]["details"] is not None


def test_protocol_conflict_precedes_business_rules() -> None:
    current = block(status="completed", directory=f".codexspec/specs/{FEATURE_ID}-user-authentication/").encode()
    raw = request("delete_pending_requirement", blueprint_hash(b"stale"), {}, feature_id=FEATURE_ID)
    outcome = apply_operation(raw, current)
    assert outcome.response["result"] == "conflict"


def test_protocol_rejects_protected_and_missing_targets() -> None:
    current = block(status="completed", directory=f".codexspec/specs/{FEATURE_ID}-user-authentication/").encode()
    raw = request("delete_pending_requirement", blueprint_hash(current), {}, feature_id=FEATURE_ID)
    outcome = apply_operation(raw, current)
    assert outcome.response["result"] == "rejected"
    assert outcome.response["blueprint_hash"] == blueprint_hash(current)
    assert outcome.content == current


def test_protocol_status_conflict_and_directory_rejection_are_distinct() -> None:
    current = block().encode()
    stale_status = request(
        "update_status",
        blueprint_hash(current),
        {"expected_status": "in_progress", "new_status": "completed"},
        feature_id=FEATURE_ID,
    )
    assert apply_operation(stale_status, current).response["result"] == "conflict"

    wrong_directory = request(
        "update_status",
        blueprint_hash(current),
        {
            "expected_status": "pending",
            "new_status": "in_progress",
            "feature_directory": f".codexspec/specs/{OTHER_ID}-wrong-name/",
        },
        feature_id=FEATURE_ID,
    )
    assert apply_operation(wrong_directory, current).response["result"] == "rejected"


def test_protocol_rejects_agent_supplied_managed_metadata() -> None:
    raw = request(
        "append_requirement",
        blueprint_hash(b""),
        {
            "feature_name": "user-authentication",
            "requirements_markdown": requirements(),
        },
    )
    outcome = apply_operation(raw, b"")
    assert outcome.response["result"] == "invalid_request"


def test_protocol_move_self_reference_is_rejected_as_self_reference() -> None:
    current = f"{block()}\n---\n{block(OTHER_ID, title='Release notes')}".encode()
    raw = request(
        "move_pending_requirement",
        blueprint_hash(current),
        {"position": "before", "reference_feature_id": FEATURE_ID},
        feature_id=FEATURE_ID,
    )
    outcome = apply_operation(raw, current)
    assert outcome.response["result"] == "rejected"
    assert outcome.response["error"]["code"] == "self_reference"
    assert outcome.content == current


def test_protocol_preserves_unicode_line_separators_in_requirements_body() -> None:
    separator = "\u2028"
    markdown = unmanaged_requirements().replace(
        "Users can authenticate securely.",
        f"First line{separator}nested second line",
    )
    assert separator in markdown
    req = request(
        "append_requirement",
        blueprint_hash(b""),
        {"feature_name": "user-authentication", "requirements_markdown": markdown},
    )
    outcome = apply_operation(req, b"", feature_id_factory=lambda: FEATURE_ID)
    assert outcome.response["result"] == "applied"
    parsed = BlueprintDocument.parse(outcome.content)
    assert separator in parsed.blocks[0].requirements_markdown
    assert parsed.serialize() == outcome.content
