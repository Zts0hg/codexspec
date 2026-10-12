"""Strict maintenance evidence must match the selected defect report."""

import copy
import json

import pytest

from codexspec.review_maintenance import parse_maintenance_result

FINGERPRINT = "sha256:current-target"


def companion(suggestions=None, fingerprint=FINGERPRINT):
    return {"schema_version": "1", "target_fingerprint": fingerprint, "suggestions": suggestions or []}


def suggestion():
    return {
        "id": "M-001",
        "location": "src/policy.py:12",
        "summary": "Consolidate current duplicated policy selection",
        "problem": "Two identical branches obscure the selected policy",
        "improvement": "Consolidate the equivalent branches in this function",
        "benefit": "Read one policy decision without changing behavior",
        "evidence": ["Both branches return the same selected policy"],
        "affected_paths": ["src/policy.py"],
        "compatibility": "Preserve inputs, outputs and side effects",
    }


def output(value):
    return "<review-code-maintenance>\n" + json.dumps(value) + "\n</review-code-maintenance>"


@pytest.mark.parametrize("items", [[], [suggestion()]])
def test_m01_valid_report(items):
    report = companion(items)
    assert parse_maintenance_result(output(report), FINGERPRINT) == report


def test_m01_unavailable_identity_carries_no_edits():
    report = companion(fingerprint=None)
    assert parse_maintenance_result(output(report), None) == report


@pytest.mark.parametrize(
    "text",
    [
        "",
        "<review-code-maintenance>bad JSON</review-code-maintenance>",
        output(companion()) + output(companion()),
        output({**companion(), "extra": True}),
        output({**companion(), "schema_version": "2"}),
        output({"schema_version": "1", "suggestions": []}),
    ],
)
def test_m02_invalid_container(text):
    with pytest.raises(ValueError):
        parse_maintenance_result(text, FINGERPRINT)


@pytest.mark.parametrize(
    "change",
    [
        {"benefit": ""},
        {"evidence": []},
        {"evidence": [""]},
        {"affected_paths": ["../policy.py"]},
        {"affected_paths": ["/tmp/policy.py"]},
        {"affected_paths": ["C:\\policy.py"]},
        {"extra": "unknown"},
        {"id": "F-001"},
    ],
)
def test_m03_invalid_suggestion(change):
    item = suggestion()
    item.update(change)
    with pytest.raises(ValueError):
        parse_maintenance_result(output(companion([item])), FINGERPRINT)


def test_m03_mismatched_target_and_duplicate_ids():
    with pytest.raises(ValueError):
        parse_maintenance_result(output(companion(fingerprint="sha256:old-target")), FINGERPRINT)
    item = suggestion()
    with pytest.raises(ValueError):
        parse_maintenance_result(output(companion([item, copy.deepcopy(item)])), FINGERPRINT)
    with pytest.raises(ValueError):
        parse_maintenance_result(output(companion([item], fingerprint=None)), None)
