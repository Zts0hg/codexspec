import json
from pathlib import Path

import pytest

from codexspec.distill_review.domain import ReviewError, ReviewService, render_consolidation
from codexspec.distill_review.models import ReviewDraft
from codexspec.distill_review.records import (
    RecordError,
    discover_records,
    outcome_state_is_verified,
    parse_record,
    validate_record_content,
)
from codexspec.distill_review.session import SessionStore


def record_text(record_id: str = "P-2026-0927-2310d6-1", *, verified: bool = False) -> str:
    state = "test passed; still valid" if verified else "observed but not yet verified"
    return (
        f"### {record_id}: Preserve unknown content\n"
        "\n"
        "- claim: Original claim\n"
        "- type: pitfall\n"
        "- scope/when: editing profile records\n"
        "- root-cause: A parser can discard unfamiliar Markdown.\n"
        "- workaround: Preserve source spans.\n"
        "- lesson: Render only fields the user changed.\n"
        '- evidence.facts: "observed fact"\n'
        f"- evidence.state: {state}\n"
        "- custom.future: keep me byte-for-byte\n"
        "- provenance: distill @implement-tasks, 2026-09-28, derivation: inferred\n"
        "- status: candidate\n"
    )


def make_profile(tmp_path: Path, *, verified: bool = False) -> Path:
    root = tmp_path / "project"
    target = root / ".codexspec/profile/pitfalls/P-2026-0927-2310d6-1-preserve-unknown.md"
    target.parent.mkdir(parents=True)
    target.write_text(record_text(verified=verified), encoding="utf-8")
    return root


def write_consolidation_manifest(root: Path, manifest_path: Path, *, cluster: str = "parser-loss") -> Path:
    member_id = "P-2026-0927-2310d6-1"
    member = next((root / ".codexspec/profile/pitfalls").glob("*.md"))
    output_id = "P-2026-0927-2310d6-9"
    manifest_path.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "proposals": {},
                "consolidations": [
                    {
                        "cluster": cluster,
                        "members": [member_id],
                        "member_hashes": {member_id: parse_record(member, root).sha256},
                        "category": "pitfalls",
                        "record_id": output_id,
                        "filename": f"{output_id}-generalized.md",
                        "markdown": record_text(output_id),
                        "fields": {"claim": "Generalized"},
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    return manifest_path


def test_record_round_trips_and_preserves_unknown_fields(tmp_path: Path) -> None:
    root = make_profile(tmp_path)
    path = next((root / ".codexspec/profile/pitfalls").glob("*.md"))
    document = parse_record(path, root)
    assert document.render({}) == path.read_bytes()
    revised = document.render({"claim": "Revised claim"})
    assert b"- claim: Revised claim\n" in revised
    assert b"- custom.future: keep me byte-for-byte\n" in revised


def test_record_rejects_protected_field_and_symlink(tmp_path: Path) -> None:
    root = make_profile(tmp_path)
    path = next((root / ".codexspec/profile/pitfalls").glob("*.md"))
    document = parse_record(path, root)
    with pytest.raises(RecordError, match="protected_field"):
        document.render({"provenance": "changed"})
    with pytest.raises(RecordError, match="protected_field"):
        document.render({"custom.future": "changed"})
    link = path.with_name("P-2026-0927-2310d6-2.md")
    link.symlink_to(path)
    with pytest.raises(RecordError, match="symlink"):
        parse_record(link, root)


def test_record_rejects_multiple_headings_and_duplicate_ids_across_statuses(tmp_path: Path) -> None:
    root = make_profile(tmp_path)
    first = next((root / ".codexspec/profile/pitfalls").glob("*.md"))
    first.write_text(first.read_text() + "\n### P-2026-0927-2310d6-9: second record\n")
    with pytest.raises(RecordError, match="duplicate_record_heading"):
        discover_records(root)

    first.write_text(record_text().replace("- status: candidate", "- status: vetted"))
    duplicate = root / ".codexspec/profile/pitfalls/P-2026-0927-2310d6-1-duplicate.md"
    duplicate.write_text(record_text())
    with pytest.raises(RecordError, match="duplicate_record_id"):
        discover_records(root)


def test_discovery_returns_candidates_and_clusters(tmp_path: Path) -> None:
    root = make_profile(tmp_path)
    second = root / ".codexspec/profile/pitfalls/P-2026-0927-2310d6-2.md"
    second.write_text(
        record_text("P-2026-0927-2310d6-2").replace(
            "- status: candidate", "- consolidation: candidate; cluster: parser-loss\n- status: candidate"
        ),
        encoding="utf-8",
    )
    records, clusters = discover_records(root)
    assert set(records) == {"P-2026-0927-2310d6-1", "P-2026-0927-2310d6-2"}
    assert clusters == {"parser-loss": ["P-2026-0927-2310d6-2"]}


def test_domain_requires_verification_then_stages_vet(tmp_path: Path) -> None:
    service = ReviewService.from_project(make_profile(tmp_path))
    record_id = "P-2026-0927-2310d6-1"
    with pytest.raises(ReviewError, match="verification_required"):
        service.stage({"action": "vet", "record_id": record_id})
    draft = service.stage({"action": "vet", "record_id": record_id, "verification": "Regression test passed on Linux."})
    assert draft["decisions"][record_id]["action"] == "vet"
    markdown = service.preview(record_id)["markdown"]
    assert markdown.endswith("- status: vetted\n")
    assert "observed but not yet verified; review verification: Regression test passed on Linux." in markdown


def test_domain_accepts_localized_outcome_verification(tmp_path: Path) -> None:
    service = ReviewService.from_project(make_profile(tmp_path), interaction_language="zh-CN")
    draft = service.stage(
        {
            "action": "vet",
            "record_id": "P-2026-0927-2310d6-1",
            "verification": "完整测试套件已通过。",
        }
    )
    assert draft["decisions"]["P-2026-0927-2310d6-1"]["status"] == "vetted"


def test_loaded_draft_rejects_forged_cached_rendering(tmp_path: Path) -> None:
    root = make_profile(tmp_path, verified=True)
    service = ReviewService.from_project(root)
    record_id = "P-2026-0927-2310d6-1"
    service.stage({"action": "vet", "record_id": record_id})
    decision = service.draft.decisions[record_id]
    decision["rendered"] = decision["rendered"].replace("- provenance: distill", "- provenance: forged")
    with pytest.raises(ReviewError, match="invalid_draft_semantics"):
        ReviewService.from_project(root, draft=service.draft)


@pytest.mark.parametrize(
    "verification",
    [
        "x",
        "not yet verified; no test result exists",
        "The report says tests passed, but the result was never verified.",
        "Tests passed in the hypothetical example; actual outcome is pending.",
        "Tests passed? Unknown; no outcome was recorded.",
        "Tests passed, but this is only an assumption/guess.",
        "Maybe tests passed.",
        "Tests probably passed.",
        "Tests seem to have passed.",
    ],
)
def test_domain_rejects_non_outcome_verification_attestation(tmp_path: Path, verification: str) -> None:
    service = ReviewService.from_project(make_profile(tmp_path))
    with pytest.raises(ReviewError, match="verification_required"):
        service.stage(
            {
                "action": "vet",
                "record_id": "P-2026-0927-2310d6-1",
                "verification": verification,
            }
        )


def test_domain_revision_can_remain_candidate_and_summary_includes_defer(tmp_path: Path) -> None:
    service = ReviewService.from_project(make_profile(tmp_path))
    record_id = "P-2026-0927-2310d6-1"
    service.stage({"action": "replace", "record_id": record_id, "fields": {"claim": "Better claim"}})
    service.stage({"action": "defer", "record_id": record_id})
    summary = service.summary()
    assert summary["deferred"] == [record_id]
    assert not summary["replaced"]
    assert not summary["undecided"]


def test_consolidation_rejects_multiline_title_change() -> None:
    markdown = record_text("P-2026-0927-2310d6-9")
    with pytest.raises(ReviewError, match="invalid_title"):
        render_consolidation(markdown, {"title": "Safe title\nInjected Markdown"}, "candidate", "")


def test_vetting_gate_uses_final_edited_evidence_state(tmp_path: Path) -> None:
    service = ReviewService.from_project(make_profile(tmp_path, verified=True))
    record_id = "P-2026-0927-2310d6-1"
    with pytest.raises(ReviewError, match="verification_required"):
        service.stage(
            {
                "action": "vet",
                "record_id": record_id,
                "fields": {"evidence.state": "outcome not yet verified"},
            }
        )


def test_domain_preview_does_not_stage_the_revision(tmp_path: Path) -> None:
    service = ReviewService.from_project(make_profile(tmp_path))
    record_id = "P-2026-0927-2310d6-1"
    preview = service.preview_operation(
        {"action": "replace", "record_id": record_id, "fields": {"claim": "Preview only"}}
    )
    assert "- claim: Preview only" in preview["markdown"]
    assert service.draft.revision == 0
    assert not service.draft.decisions


def test_domain_manifest_rejects_stale_proposal(tmp_path: Path) -> None:
    root = make_profile(tmp_path)
    manifest = {
        "schema_version": 1,
        "proposals": {
            "P-2026-0927-2310d6-1": {
                "base_hash": "0" * 64,
                "fields": {"claim": "stale"},
            }
        },
        "consolidations": [],
    }
    manifest_path = tmp_path / "manifest.json"
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    with pytest.raises(ReviewError, match="stale_proposal"):
        ReviewService.from_project(root, manifest_path=manifest_path)


def test_snapshot_declares_only_structured_editable_fields(tmp_path: Path) -> None:
    service = ReviewService.from_project(make_profile(tmp_path))
    record = service.snapshot()["records"][0]
    assert record["editable_fields"] == [
        "title",
        "claim",
        "scope/when",
        "root-cause",
        "workaround",
        "lesson",
        "evidence.facts",
        "evidence.state",
    ]
    assert "custom.future" not in record["editable_fields"]


def test_manifest_rejects_protected_consolidation_editor_field(tmp_path: Path) -> None:
    root = make_profile(tmp_path)
    first = next((root / ".codexspec/profile/pitfalls").glob("*.md"))
    first.write_text(
        first.read_text().replace(
            "- status: candidate", "- consolidation: candidate; cluster: parser-loss\n- status: candidate"
        )
    )
    manifest = {
        "schema_version": 1,
        "proposals": {},
        "consolidations": [
            {
                "cluster": "parser-loss",
                "members": ["P-2026-0927-2310d6-1"],
                "member_hashes": {"P-2026-0927-2310d6-1": parse_record(first, root).sha256},
                "category": "pitfalls",
                "record_id": "P-2026-0927-2310d6-3",
                "filename": "P-2026-0927-2310d6-3.md",
                "markdown": record_text("P-2026-0927-2310d6-3"),
                "fields": {"provenance": "must remain protected"},
            }
        ],
    }
    manifest_path = tmp_path / "protected-manifest.json"
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    with pytest.raises(ReviewError, match="protected_field"):
        ReviewService.from_project(root, manifest_path=manifest_path)


def test_domain_stages_structured_consolidation_proposal(tmp_path: Path) -> None:
    root = make_profile(tmp_path)
    first = next((root / ".codexspec/profile/pitfalls").glob("*.md"))
    first.write_text(
        first.read_text().replace(
            "- status: candidate", "- consolidation: candidate; cluster: parser-loss\n- status: candidate"
        )
    )
    proposal_id = "S-2026-0927-2310d6-1"
    proposal = (
        record_text(proposal_id, verified=True)
        .replace("- type: pitfall", "- type: strategy")
        .replace(
            "- root-cause: A parser can discard unfamiliar Markdown.\n"
            "- workaround: Preserve source spans.\n"
            "- lesson: Render only fields the user changed.\n",
            "- trigger: editing a structured record\n- action: preserve opaque spans\n",
        )
    )
    manifest = {
        "schema_version": 1,
        "proposals": {},
        "consolidations": [
            {
                "cluster": "parser-loss",
                "members": ["P-2026-0927-2310d6-1"],
                "member_hashes": {"P-2026-0927-2310d6-1": parse_record(first, root).sha256},
                "category": "strategies",
                "record_id": proposal_id,
                "filename": f"{proposal_id}-preserve-unknown.md",
                "markdown": proposal,
                "fields": {"claim": "Original claim", "scope/when": "editing profile records"},
            }
        ],
    }
    manifest_path = tmp_path / "manifest.json"
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    service = ReviewService.from_project(root, manifest_path=manifest_path)
    service.stage(
        {
            "action": "merge",
            "cluster": "parser-loss",
            "field_changes": {"claim": "Generalized claim"},
            "status": "vetted",
        }
    )
    decision = service.draft.decisions["cluster:parser-loss"]
    assert "- claim: Generalized claim" in decision["markdown"]
    assert "- status: vetted" in decision["markdown"]
    assert decision["members"] == ["P-2026-0927-2310d6-1"]


def test_consolidation_rejects_non_outcome_verification_attestation(tmp_path: Path) -> None:
    root = make_profile(tmp_path)
    first = next((root / ".codexspec/profile/pitfalls").glob("*.md"))
    first.write_text(
        first.read_text().replace(
            "- status: candidate", "- consolidation: candidate; cluster: parser-loss\n- status: candidate"
        )
    )
    output_id = "P-2026-0927-2310d6-5"
    manifest = {
        "schema_version": 1,
        "proposals": {},
        "consolidations": [
            {
                "cluster": "parser-loss",
                "members": ["P-2026-0927-2310d6-1"],
                "member_hashes": {"P-2026-0927-2310d6-1": parse_record(first, root).sha256},
                "category": "pitfalls",
                "record_id": output_id,
                "filename": f"{output_id}.md",
                "markdown": record_text(output_id),
                "fields": {},
            }
        ],
    }
    manifest_path = tmp_path / "negative-verification.json"
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    service = ReviewService.from_project(root, manifest_path=manifest_path)
    with pytest.raises(ReviewError, match="verification_required"):
        service.stage(
            {
                "action": "merge",
                "cluster": "parser-loss",
                "status": "vetted",
                "verification": "not yet verified",
            }
        )


def test_domain_rejects_schema_invalid_consolidation_output(tmp_path: Path) -> None:
    root = make_profile(tmp_path)
    first = next((root / ".codexspec/profile/pitfalls").glob("*.md"))
    first.write_text(
        first.read_text().replace(
            "- status: candidate", "- consolidation: candidate; cluster: parser-loss\n- status: candidate"
        )
    )
    manifest = {
        "schema_version": 1,
        "proposals": {},
        "consolidations": [
            {
                "cluster": "parser-loss",
                "members": ["P-2026-0927-2310d6-1"],
                "member_hashes": {"P-2026-0927-2310d6-1": parse_record(first, root).sha256},
                "category": "strategies",
                "record_id": "S-2026-0927-2310d6-2",
                "filename": "S-2026-0927-2310d6-2.md",
                "markdown": record_text("S-2026-0927-2310d6-2"),
                "fields": {},
            }
        ],
    }
    manifest_path = tmp_path / "invalid-manifest.json"
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    with pytest.raises(ReviewError, match="invalid_consolidation_output"):
        ReviewService.from_project(root, manifest_path=manifest_path)


def test_domain_rejects_non_markdown_consolidation_output(tmp_path: Path) -> None:
    root = make_profile(tmp_path)
    first = next((root / ".codexspec/profile/pitfalls").glob("*.md"))
    first.write_text(
        first.read_text().replace(
            "- status: candidate", "- consolidation: candidate; cluster: parser-loss\n- status: candidate"
        )
    )
    record_id = "P-2026-0927-2310d6-6"
    manifest = {
        "schema_version": 1,
        "proposals": {},
        "consolidations": [
            {
                "cluster": "parser-loss",
                "members": ["P-2026-0927-2310d6-1"],
                "member_hashes": {"P-2026-0927-2310d6-1": parse_record(first, root).sha256},
                "category": "pitfalls",
                "record_id": record_id,
                "filename": f"{record_id}-hidden.json",
                "markdown": record_text(record_id),
                "fields": {},
            }
        ],
    }
    manifest_path = tmp_path / "non-markdown.json"
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    with pytest.raises(ReviewError, match="invalid_consolidation_output"):
        ReviewService.from_project(root, manifest_path=manifest_path)


def test_domain_rejects_duplicate_consolidation_output_ids(tmp_path: Path) -> None:
    root = make_profile(tmp_path)
    directory = root / ".codexspec/profile/pitfalls"
    first = next(directory.glob("*.md"))
    first.write_text(
        first.read_text().replace(
            "- status: candidate", "- consolidation: candidate; cluster: parser-loss\n- status: candidate"
        )
    )
    second_id = "P-2026-0927-2310d6-2"
    second = directory / f"{second_id}.md"
    second.write_text(
        record_text(second_id).replace(
            "- status: candidate", "- consolidation: candidate; cluster: evidence-loss\n- status: candidate"
        )
    )
    output_id = "P-2026-0927-2310d6-9"
    manifest = {
        "schema_version": 1,
        "proposals": {},
        "consolidations": [
            {
                "cluster": cluster,
                "members": [member_id],
                "member_hashes": {member_id: parse_record(path, root).sha256},
                "category": "pitfalls",
                "record_id": output_id,
                "filename": f"{output_id}-{cluster}.md",
                "markdown": record_text(output_id),
                "fields": {},
            }
            for cluster, member_id, path in (
                ("parser-loss", "P-2026-0927-2310d6-1", first),
                ("evidence-loss", second_id, second),
            )
        ],
    }
    manifest_path = tmp_path / "duplicate-output-id.json"
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    with pytest.raises(ReviewError, match="duplicate_record_id"):
        ReviewService.from_project(root, manifest_path=manifest_path)


def test_consolidation_manifest_rejects_stale_member_hash(tmp_path: Path) -> None:
    root = make_profile(tmp_path)
    first = next((root / ".codexspec/profile/pitfalls").glob("*.md"))
    first.write_text(
        first.read_text().replace(
            "- status: candidate", "- consolidation: candidate; cluster: parser-loss\n- status: candidate"
        )
    )
    proposal_id = "P-2026-0927-2310d6-8"
    manifest = {
        "schema_version": 1,
        "proposals": {},
        "consolidations": [
            {
                "cluster": "parser-loss",
                "members": ["P-2026-0927-2310d6-1"],
                "member_hashes": {"P-2026-0927-2310d6-1": "0" * 64},
                "category": "pitfalls",
                "record_id": proposal_id,
                "filename": f"{proposal_id}.md",
                "markdown": record_text(proposal_id),
                "fields": {"claim": "Generalized"},
            }
        ],
    }
    manifest_path = tmp_path / "stale-consolidation.json"
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    with pytest.raises(ReviewError, match="stale_consolidation"):
        ReviewService.from_project(root, manifest_path=manifest_path)


def test_member_and_merge_decisions_replace_each_other(tmp_path: Path) -> None:
    root = make_profile(tmp_path)
    first = next((root / ".codexspec/profile/pitfalls").glob("*.md"))
    first.write_text(
        first.read_text().replace(
            "- status: candidate", "- consolidation: candidate; cluster: parser-loss\n- status: candidate"
        )
    )
    proposal_id = "P-2026-0927-2310d6-7"
    member_hash = parse_record(first, root).sha256
    manifest = {
        "schema_version": 1,
        "proposals": {},
        "consolidations": [
            {
                "cluster": "parser-loss",
                "members": ["P-2026-0927-2310d6-1"],
                "member_hashes": {"P-2026-0927-2310d6-1": member_hash},
                "category": "pitfalls",
                "record_id": proposal_id,
                "filename": f"{proposal_id}.md",
                "markdown": record_text(proposal_id),
                "fields": {"claim": "Generalized"},
            }
        ],
    }
    manifest_path = tmp_path / "merge.json"
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    service = ReviewService.from_project(root, manifest_path=manifest_path)
    member = "P-2026-0927-2310d6-1"
    service.stage({"action": "replace", "record_id": member, "fields": {"claim": "member edit"}})
    service.stage({"action": "merge", "cluster": "parser-loss", "field_changes": {}})
    assert member not in service.draft.decisions
    service.stage({"action": "defer", "record_id": member})
    assert "cluster:parser-loss" not in service.draft.decisions
    assert service.summary()["deferred"] == [member]


def test_keep_separate_preserves_staged_member_decisions(tmp_path: Path) -> None:
    root = make_profile(tmp_path, verified=True)
    first = next((root / ".codexspec/profile/pitfalls").glob("*.md"))
    first.write_text(
        first.read_text().replace(
            "- status: candidate", "- consolidation: candidate; cluster: parser-loss\n- status: candidate"
        )
    )
    manifest = write_consolidation_manifest(root, tmp_path / "keep-separate.json")
    service = ReviewService.from_project(root, manifest_path=manifest)
    member = "P-2026-0927-2310d6-1"
    service.stage({"action": "vet", "record_id": member})
    service.stage({"action": "keep_separate", "cluster": "parser-loss"})
    assert service.draft.decisions[member]["action"] == "vet"
    assert member not in service.draft.deferred
    assert service.summary()["promoted"] == [member]


def test_cluster_requires_generalized_proposal_when_no_merge_draft_exists(tmp_path: Path) -> None:
    root = make_profile(tmp_path)
    target = next((root / ".codexspec/profile/pitfalls").glob("*.md"))
    target.write_text(
        target.read_text().replace(
            "- status: candidate", "- consolidation: candidate; cluster: parser-loss\n- status: candidate"
        )
    )
    with pytest.raises(ReviewError, match="missing_merge_proposal: parser-loss"):
        ReviewService.from_project(root)


def test_cluster_rejects_duplicate_generalized_proposals(tmp_path: Path) -> None:
    root = make_profile(tmp_path)
    target = next((root / ".codexspec/profile/pitfalls").glob("*.md"))
    target.write_text(
        target.read_text().replace(
            "- status: candidate", "- consolidation: candidate; cluster: parser-loss\n- status: candidate"
        )
    )
    manifest_path = write_consolidation_manifest(root, tmp_path / "duplicate-cluster.json")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["consolidations"].append(dict(manifest["consolidations"][0]))
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    with pytest.raises(ReviewError, match="duplicate_consolidation_cluster: parser-loss"):
        ReviewService.from_project(root, manifest_path=manifest_path)


def test_saved_merge_draft_resumes_without_temporary_manifest(tmp_path: Path) -> None:
    root = make_profile(tmp_path)
    first = next((root / ".codexspec/profile/pitfalls").glob("*.md"))
    first.write_text(
        first.read_text().replace(
            "- status: candidate", "- consolidation: candidate; cluster: parser-loss\n- status: candidate"
        )
    )
    output_id = "P-2026-0927-2310d6-9"
    manifest = {
        "schema_version": 1,
        "proposals": {},
        "consolidations": [
            {
                "cluster": "parser-loss",
                "members": ["P-2026-0927-2310d6-1"],
                "member_hashes": {"P-2026-0927-2310d6-1": parse_record(first, root).sha256},
                "category": "pitfalls",
                "record_id": output_id,
                "filename": f"{output_id}-generalized.md",
                "markdown": record_text(output_id),
                "fields": {"claim": "Generalized"},
            }
        ],
    }
    manifest_path = tmp_path / "merge-resume.json"
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    service = ReviewService.from_project(root, manifest_path=manifest_path)
    service.stage(
        {
            "action": "merge",
            "cluster": "parser-loss",
            "field_changes": {"claim": "Resumable merge"},
        }
    )

    resumed = ReviewService.from_project(root, draft=service.draft)

    assert "Resumable merge" in resumed.draft.decisions["cluster:parser-loss"]["markdown"]


@pytest.mark.parametrize(
    ("category", "record_id", "filename"),
    [
        ("constraints", "Wrong-2026-0927-2310d6-1", "Wrong-2026-0927-2310d6-1.md"),
        ("pitfalls", "P-2026-0927-2310d6-1", "P-2026-0927-2310d6-1-bad\\slug.md"),
        ("pitfalls", "P-2026-0927-2310d6-1", "P-2026-0927-2310d6-1-UPPER.md"),
        ("pitfalls", "P-2026-0927-2310d6-1", "P-2026-0927-2310d6-1-bad%slug.md"),
        ("pitfalls", "P-2026-0927-2310d6-1", f"P-2026-0927-2310d6-1-{'a' * 51}.md"),
    ],
)
def test_record_identity_rejects_wrong_prefix_and_nonportable_slug(
    category: str, record_id: str, filename: str
) -> None:
    source = record_text(record_id)
    if category == "constraints":
        source = source.replace("- type: pitfall", "- type: constraint").replace(
            "- root-cause: A parser can discard unfamiliar Markdown.\n"
            "- workaround: Preserve source spans.\n"
            "- lesson: Render only fields the user changed.\n",
            "",
        )
    with pytest.raises(RecordError):
        validate_record_content(source.encode(), category=category, record_id=record_id, filename=filename)


@pytest.mark.parametrize(
    "state",
    [
        "requirement confirmed; implementation pending",
        "decision confirmed, outcome not exercised",
        "decided and implemented; no test result recorded",
        "test not passed",
        "checks have not green",
    ],
)
def test_outcome_gate_rejects_non_outcome_keywords(state: str) -> None:
    assert not outcome_state_is_verified(state)


@pytest.mark.parametrize(
    "state",
    [
        "full test suite passed",
        "workaround worked in production",
        "CI checks are green",
        "完整测试套件已通过。",
        "完整測試套件已通過。",
        "テストスイートが成功しました。",
        "테스트 스위트가 통과했습니다.",
    ],
)
def test_outcome_gate_accepts_concrete_results(state: str) -> None:
    assert outcome_state_is_verified(state)


def test_vetting_gate_matches_the_bytes_that_will_be_written(tmp_path: Path) -> None:
    """The gate must read the rendered record, not the request.

    `render()` rebuilds `evidence.state` from the stored value whenever a verification
    attestation is supplied, discarding an edit to that field. A gate that reads the
    request therefore accepts a decision whose written bytes do not establish
    verification, and the apply-time gate then refuses the whole batch.
    """
    root = make_profile(tmp_path)
    service = ReviewService.from_project(root)
    operation = {
        "action": "vet",
        "record_id": "P-2026-0927-2310d6-1",
        "fields": {"evidence.state": "full suite passed; still valid"},
        "verification": "see CI run 123",
    }
    with pytest.raises(ReviewError, match="verification_required"):
        service.preview_operation(operation)
    with pytest.raises(ReviewError, match="verification_required"):
        service.stage(operation)
    assert not service.draft.decisions


def test_vetting_gate_still_accepts_an_attestation_that_establishes_the_outcome(tmp_path: Path) -> None:
    root = make_profile(tmp_path)
    service = ReviewService.from_project(root)
    operation = {
        "action": "vet",
        "record_id": "P-2026-0927-2310d6-1",
        "verification": "full suite passed; still valid",
    }
    rendered = service.preview_operation(operation)["markdown"]
    assert "- status: vetted" in rendered
    assert "review verification: full suite passed" in rendered


def test_rejected_staging_request_leaves_the_draft_untouched(tmp_path: Path) -> None:
    """`stage()` must not mutate the draft before its last validation runs."""
    root = make_profile(tmp_path)
    target = next((root / ".codexspec/profile/pitfalls").glob("*.md"))
    target.write_text(
        target.read_text().replace(
            "- status: candidate",
            "- consolidation: candidate; cluster: parser-loss\n- status: candidate",
        ),
        encoding="utf-8",
    )
    manifest = write_consolidation_manifest(root, tmp_path / "reject.json")
    service = ReviewService.from_project(root, manifest_path=manifest)
    service.stage({"action": "merge", "cluster": "parser-loss", "field_changes": {"claim": "Generalized"}})
    before = json.dumps(service.draft.to_dict(), sort_keys=True)
    with pytest.raises(ReviewError, match="remove_has_payload"):
        service.stage(
            {
                "action": "remove",
                "record_id": "P-2026-0927-2310d6-1",
                "fields": {"claim": "x"},
            }
        )
    assert json.dumps(service.draft.to_dict(), sort_keys=True) == before


def test_saved_merge_draft_survives_a_new_member_joining_its_cluster(tmp_path: Path) -> None:
    """A membership change makes a staged merge stale, not the whole session unopenable."""
    root = make_profile(tmp_path)
    first = next((root / ".codexspec/profile/pitfalls").glob("*.md"))
    first.write_text(
        first.read_text().replace(
            "- status: candidate",
            "- consolidation: candidate; cluster: parser-loss\n- status: candidate",
        ),
        encoding="utf-8",
    )
    manifest = write_consolidation_manifest(root, tmp_path / "join.json")
    service = ReviewService.from_project(root, manifest_path=manifest)
    service.stage({"action": "merge", "cluster": "parser-loss", "field_changes": {"claim": "Generalized"}})
    saved = ReviewDraft.from_dict(service.draft.to_dict())
    joined = first.with_name("P-2026-0927-2310d6-2-joined.md")
    joined.write_text(
        record_text("P-2026-0927-2310d6-2").replace(
            "- status: candidate",
            "- consolidation: candidate; cluster: parser-loss\n- status: candidate",
        ),
        encoding="utf-8",
    )
    # Reopened without a manifest: the saved draft supplies the merge proposal, so the
    # membership change is seen by the loaded-draft re-derivation rather than by manifest
    # validation. A stale merge must drop out of the draft, not refuse the whole session.
    reopened = ReviewService.from_project(root, draft=saved)
    assert "cluster:parser-loss" not in reopened.draft.decisions
    assert sorted(reopened.clusters["parser-loss"]) == ["P-2026-0927-2310d6-1", "P-2026-0927-2310d6-2"]
    assert "P-2026-0927-2310d6-2" in reopened.records


def test_stale_draft_prune_keeps_a_fresh_manifest_consolidation(tmp_path: Path) -> None:
    """Dropping a stale staged merge must remove only the proposal reconstructed from
    that draft. A fresh manifest proposal for the same cluster describes the current
    membership and must survive so the cluster stays mergeable this session. (S001.14)"""
    root = tmp_path / "project"
    pit = root / ".codexspec/profile/pitfalls"
    pit.mkdir(parents=True)
    members = ["P-2026-1002-2205zz-1", "P-2026-1002-2205zz-2"]
    for member in members:
        (pit / f"{member}.md").write_text(
            record_text(member).replace(
                "- status: candidate",
                "- consolidation: cluster: dup\n- status: candidate",
            ),
            encoding="utf-8",
        )
    late_joiner = "P-2026-1002-2205zz-3"
    (pit / f"{late_joiner}.md").write_text(record_text(late_joiner), encoding="utf-8")

    def manifest(cluster_members: list[str], output_id: str) -> Path:
        hashes = {member: parse_record(pit / f"{member}.md", root).sha256 for member in cluster_members}
        manifest_path = root / "manifest.json"
        manifest_path.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "proposals": {},
                    "consolidations": [
                        {
                            "cluster": "dup",
                            "members": cluster_members,
                            "member_hashes": hashes,
                            "category": "pitfalls",
                            "record_id": output_id,
                            "filename": f"{output_id}-generalized.md",
                            "markdown": record_text(output_id, verified=True),
                            "fields": {"claim": "Generalized"},
                        }
                    ],
                }
            ),
            encoding="utf-8",
        )
        return manifest_path

    stale_service = ReviewService.from_project(root, manifest_path=manifest(members, "P-2026-1002-2205zz-9"))
    stale_service.stage({"action": "merge", "cluster": "dup", "status": "candidate", "field_changes": {}})
    store = SessionStore(root)
    store.prepare()
    store.save(ReviewDraft.from_dict(stale_service.draft.to_dict()))

    # A third record joins the cluster and the agent regenerates the manifest for it.
    (pit / f"{late_joiner}.md").write_text(
        record_text(late_joiner).replace(
            "- status: candidate",
            "- consolidation: cluster: dup\n- status: candidate",
        ),
        encoding="utf-8",
    )
    fresh = manifest([*members, late_joiner], "P-2026-1002-2205zz-8")

    service = ReviewService.from_project(root, manifest_path=fresh, draft=store.load())
    assert any(item.get("cluster") == "dup" for item in service.consolidations), (
        "the fresh manifest proposal must survive the stale-draft prune"
    )
    assert "cluster:dup" not in service.draft.decisions, "the stale staged merge is gone"
    service.stage({"action": "merge", "cluster": "dup", "status": "candidate", "field_changes": {}})


def test_consolidation_snapshot_reports_whether_its_evidence_satisfies_vetting(tmp_path: Path) -> None:
    """REQ-007/REQ-023: the page cannot evaluate outcome evidence by itself, so a
    consolidation must report whether its rendered evidence.state already satisfies the
    vetting gate — the same flag the record surface reads from the backend. (S001.18)"""
    root = tmp_path / "project"
    pit = root / ".codexspec/profile/pitfalls"
    pit.mkdir(parents=True)
    member = "P-2026-1003-2205zz-1"
    (pit / f"{member}.md").write_text(
        record_text(member).replace(
            "- status: candidate",
            "- consolidation: cluster: dup\n- status: candidate",
        ),
        encoding="utf-8",
    )
    member_hash = parse_record(pit / f"{member}.md", root).sha256

    def manifest_with(markdown: str, output_id: str) -> Path:
        manifest_path = root / f"manifest-{output_id}.json"
        manifest_path.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "proposals": {},
                    "consolidations": [
                        {
                            "cluster": "dup",
                            "members": [member],
                            "member_hashes": {member: member_hash},
                            "category": "pitfalls",
                            "record_id": output_id,
                            "filename": f"{output_id}-generalized.md",
                            "markdown": markdown,
                            "fields": {},
                        }
                    ],
                }
            ),
            encoding="utf-8",
        )
        return manifest_path

    verified = ReviewService.from_project(
        root, manifest_path=manifest_with(record_text("P-2026-1003-2205zz-9", verified=True), "P-2026-1003-2205zz-9")
    )
    unverified = ReviewService.from_project(
        root, manifest_path=manifest_with(record_text("P-2026-1003-2205zz-8"), "P-2026-1003-2205zz-8")
    )
    assert verified.consolidations[0]["outcome_verified"] is True
    assert unverified.consolidations[0]["outcome_verified"] is False
    # The backend half of the disagreement: vetting such a merge needs no attestation.
    decision = verified.stage({"action": "merge", "cluster": "dup", "status": "vetted", "field_changes": {}})
    assert decision["decisions"]["cluster:dup"]["status"] == "vetted"


def test_non_string_field_values_are_refused_before_entering_the_draft(tmp_path: Path) -> None:
    """Field values persist into the draft verbatim and the draft codec requires strings,
    so a non-string value staged from the text carrier or a raw client made the saved
    draft unopenable until every staged decision was discarded. (S001.20)"""
    root = make_profile(tmp_path)
    record_id = "P-2026-0927-2310d6-1"
    service = ReviewService.from_project(root)
    with pytest.raises(ReviewError):
        service.stage({"action": "replace", "record_id": record_id, "fields": {"claim": 42}})
    assert record_id not in service.draft.decisions, "a refused request leaves the draft untouched"

    target = next((root / ".codexspec/profile/pitfalls").glob("*.md"))
    target.write_text(
        target.read_text(encoding="utf-8").replace(
            "- status: candidate",
            "- consolidation: cluster: parser-loss\n- status: candidate",
        ),
        encoding="utf-8",
    )
    manifest = write_consolidation_manifest(root, root / "manifest.json")
    merged = ReviewService.from_project(root, manifest_path=manifest)
    with pytest.raises(ReviewError):
        merged.stage(
            {"action": "merge", "cluster": "parser-loss", "status": "candidate", "field_changes": {"claim": 42}}
        )
    assert "cluster:parser-loss" not in merged.draft.decisions


def test_manifest_rejects_non_string_editable_values(tmp_path: Path) -> None:
    """Manifest-supplied editable values reach the draft verbatim on resume, so they are
    validated at ingestion like every other structured input. (S001.21)"""
    root = tmp_path / "project"
    pit = root / ".codexspec/profile/pitfalls"
    pit.mkdir(parents=True)
    member = "P-2026-1003-2205zz-1"
    (pit / f"{member}.md").write_text(
        record_text(member).replace("- status: candidate", "- consolidation: cluster: dup\n- status: candidate"),
        encoding="utf-8",
    )
    member_hash = parse_record(pit / f"{member}.md", root).sha256

    def manifest(payload: dict) -> Path:
        path = root / "manifest.json"
        path.write_text(json.dumps({"schema_version": 1, **payload}), encoding="utf-8")
        return path

    with pytest.raises(ReviewError) as proposal_failure:
        ReviewService.from_project(
            root,
            manifest_path=manifest(
                {
                    "proposals": {member: {"base_hash": member_hash, "fields": {"claim": 42}}},
                    "consolidations": [],
                }
            ),
        )
    assert "invalid_proposal_fields" in str(proposal_failure.value)

    with pytest.raises(ReviewError) as consolidation_failure:
        ReviewService.from_project(
            root,
            manifest_path=manifest(
                {
                    "proposals": {},
                    "consolidations": [
                        {
                            "cluster": "dup",
                            "members": [member],
                            "member_hashes": {member: member_hash},
                            "category": "pitfalls",
                            "record_id": "P-2026-1003-2205zz-9",
                            "filename": "P-2026-1003-2205zz-9.md",
                            "markdown": record_text("P-2026-1003-2205zz-9"),
                            "fields": {"claim": 42},
                        }
                    ],
                }
            ),
        )
    assert "invalid_consolidation_fields" in str(consolidation_failure.value)
