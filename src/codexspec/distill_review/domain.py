"""Carrier-independent distill-review state machine."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Mapping

from .models import ACTIONS, SCHEMA_VERSION, ReviewDraft
from .records import (
    RecordDocument,
    RecordError,
    discover_all_records,
    discover_records,
    editable_fields_for,
    outcome_state_is_verified,
    validate_record_content,
)


class ReviewError(ValueError):
    """A requested review transition is invalid."""


def render_consolidation(
    markdown: str,
    field_changes: Mapping[str, Any],
    status: str,
    verification: str,
) -> str:
    """Derive final consolidation Markdown from its immutable proposal snapshot."""
    replacements = {key: str(value).strip() for key, value in field_changes.items()}
    replacements["status"] = status
    if verification.strip():
        current = ""
        for line in markdown.splitlines():
            if line.startswith("- evidence.state:"):
                current = line.split(":", 1)[1].strip()
                break
        attestation = verification.strip()
        replacements["evidence.state"] = f"{current}; review verification: {attestation}" if current else attestation
    found: set[str] = set()
    lines = markdown.splitlines(keepends=True)
    for index, line in enumerate(lines):
        heading = re.match(r"^(#{2,3}\s+[A-Za-z]+-\d{4}-\d{4}-\d{4}[a-z0-9]{2}-\d+:).*$", line)
        if heading and "title" in replacements:
            title = replacements["title"]
            if not title or "\n" in title or "\r" in title:
                raise ReviewError("invalid_title")
            ending = "\r\n" if line.endswith("\r\n") else "\n"
            lines[index] = f"{heading.group(1)} {title}{ending}"
            found.add("title")
            continue
        if not line.startswith("- ") or ":" not in line:
            continue
        key = line[2:].split(":", 1)[0]
        if key not in replacements:
            continue
        value = replacements[key]
        if "\n" in value or "\r" in value:
            raise ReviewError(f"multiline_field: {key}")
        ending = "\r\n" if line.endswith("\r\n") else "\n"
        lines[index] = f"- {key}: {value}{ending}"
        found.add(key)
    missing = set(replacements) - found
    if missing:
        raise ReviewError(f"missing_consolidation_field: {sorted(missing)[0]}")
    return "".join(lines)


class ReviewService:
    def __init__(
        self,
        project_root: Path,
        records: Mapping[str, RecordDocument],
        clusters: Mapping[str, list[str]],
        *,
        proposals: Mapping[str, dict[str, Any]] | None = None,
        consolidations: list[dict[str, Any]] | None = None,
        draft: ReviewDraft | None = None,
        interaction_language: str = "en",
    ) -> None:
        self.project_root = project_root.resolve()
        self.records = dict(records)
        self.clusters = {key: list(value) for key, value in clusters.items()}
        self.proposals = dict(proposals or {})
        self.consolidations = list(consolidations or [])
        self.draft = draft or ReviewDraft()
        self.interaction_language = interaction_language
        if draft is not None:
            self._validate_loaded_draft_semantics()

    def _validate_loaded_draft_semantics(self) -> None:
        """Re-derive cached output when its source snapshot is still current.

        Draft files are recoverable user state, not an authority for bytes that
        may be written to the profile.  Stale or missing targets remain loaded
        so the UI can report and refresh them, but a decision whose base hash is
        current must exactly match the deterministic domain rendering.
        """
        stale: list[str] = []
        for key, decision in list(self.draft.decisions.items()):
            action = decision["action"]
            if action in {"vet", "replace", "remove"}:
                document = self.records.get(key)
                if document is None or decision["base_hash"] != document.sha256:
                    continue
                request = {
                    "fields": decision.get("fields", {}),
                    "status": decision.get("status", "candidate"),
                    "verification": decision.get("verification", ""),
                }
                derived = self._decision_for_record(action, key, request)
            elif action == "merge":
                members = decision["members"]
                current = all(
                    member in self.records and decision["member_hashes"].get(member) == self.records[member].sha256
                    for member in members
                )
                if current and sorted(members) != sorted(self.clusters.get(decision["cluster"], [])):
                    # A record joined or left the cluster between sessions. The staged merge
                    # can no longer describe it, so drop that one decision and its
                    # reconstructed proposal; the cluster returns as undecided and asks for a
                    # fresh proposal, while every other staged decision stays resumable.
                    stale.append(key)
                    continue
                if not current:
                    continue
                request = {
                    "action": "merge",
                    "cluster": decision["cluster"],
                    "field_changes": decision["field_changes"],
                    "status": decision["status"],
                    "verification": decision["verification"],
                }
                proposal = {
                    "cluster": decision["cluster"],
                    "members": decision["members"],
                    "member_hashes": decision["member_hashes"],
                    "category": decision["category"],
                    "record_id": decision["record_id"],
                    "filename": decision["filename"],
                    "markdown": decision["proposal_markdown"],
                    "fields": decision["editable_fields"],
                }
                derived = self._merge_decision_from_proposal(request, proposal)
            else:  # Defensive: ReviewDraft already validates this branch.
                raise ReviewError(f"invalid_draft_semantics: {key}")
            if decision != derived:
                raise ReviewError(f"invalid_draft_semantics: {key}; rerun with --discard-draft to remove it")
        for key in stale:
            dropped = self.draft.decisions.pop(key, None)
            if dropped is not None:
                # Only the proposal reconstructed from this draft shares its bytes.
                # A fresh manifest proposal for the same cluster describes the
                # current membership and must survive so the cluster stays mergeable.
                reconstruction = {
                    "cluster": dropped["cluster"],
                    "members": dropped["members"],
                    "member_hashes": dropped["member_hashes"],
                    "category": dropped["category"],
                    "record_id": dropped["record_id"],
                    "filename": dropped["filename"],
                    "markdown": dropped["proposal_markdown"],
                    "fields": dropped["editable_fields"],
                    "outcome_verified": outcome_state_is_verified(dropped["editable_fields"].get("evidence.state", "")),
                }
                self.consolidations = [item for item in self.consolidations if item != reconstruction]

    @classmethod
    def from_project(
        cls,
        project_root: Path,
        *,
        manifest_path: Path | None = None,
        draft: ReviewDraft | None = None,
        interaction_language: str = "en",
    ) -> ReviewService:
        try:
            all_records = discover_all_records(project_root)
        except RecordError as exc:
            raise ReviewError(f"invalid_profile: {exc}") from exc
        records = {
            record_id: document
            for record_id, document in all_records.items()
            if document.status == "candidate" or document.cluster
        }
        clusters: dict[str, list[str]] = {}
        for record_id, document in records.items():
            if document.cluster:
                clusters.setdefault(document.cluster, []).append(record_id)
        proposals: dict[str, dict[str, Any]] = {}
        consolidations: list[dict[str, Any]] = []
        if manifest_path is not None:
            try:
                manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError, UnicodeDecodeError) as exc:
                raise ReviewError("invalid_manifest") from exc
            if not isinstance(manifest, dict) or manifest.get("schema_version") != SCHEMA_VERSION:
                raise ReviewError("unsupported_manifest_schema")
            raw_proposals = manifest.get("proposals", {})
            raw_consolidations = manifest.get("consolidations", [])
            if not isinstance(raw_proposals, dict) or not isinstance(raw_consolidations, list):
                raise ReviewError("invalid_manifest_shape")
            for record_id, proposal in raw_proposals.items():
                if record_id not in records or not isinstance(proposal, dict):
                    raise ReviewError(f"unknown_proposal_target: {record_id}")
                if proposal.get("base_hash") != records[record_id].sha256:
                    raise ReviewError(f"stale_proposal: {record_id}")
                fields = proposal.get("fields", {})
                if not isinstance(fields, dict) or not all(isinstance(value, str) for value in fields.values()):
                    raise ReviewError(f"invalid_proposal_fields: {record_id}")
                try:
                    records[record_id].render(fields)
                except RecordError as exc:
                    raise ReviewError(f"invalid_proposal: {record_id}: {exc}") from exc
                proposals[record_id] = proposal
            reserved_record_ids = set(all_records)
            seen_consolidation_clusters: set[str] = set()
            for item in raw_consolidations:
                if not isinstance(item, dict):
                    raise ReviewError("invalid_consolidation")
                members = item.get("members")
                if not isinstance(members, list) or not members or any(member not in records for member in members):
                    raise ReviewError("invalid_consolidation_members")
                cluster = item.get("cluster")
                if not isinstance(cluster, str) or sorted(clusters.get(cluster, [])) != sorted(members):
                    raise ReviewError("invalid_consolidation_cluster")
                if cluster in seen_consolidation_clusters:
                    raise ReviewError(f"duplicate_consolidation_cluster: {cluster}")
                seen_consolidation_clusters.add(cluster)
                member_hashes = item.get("member_hashes")
                if not isinstance(member_hashes, dict) or set(member_hashes) != set(members):
                    raise ReviewError("invalid_consolidation_hashes")
                stale_members = [member for member in members if member_hashes.get(member) != records[member].sha256]
                if stale_members:
                    raise ReviewError(f"stale_consolidation: {','.join(sorted(stale_members))}")
                editable = item.get("fields", {})
                if not isinstance(editable, dict) or not all(isinstance(value, str) for value in editable.values()):
                    raise ReviewError("invalid_consolidation_fields")
                category = item.get("category")
                output_record_id = item.get("record_id")
                filename = item.get("filename", f"{output_record_id}.md")
                markdown = item.get("markdown")
                if (
                    not isinstance(category, str)
                    or not category
                    or not isinstance(output_record_id, str)
                    or not output_record_id
                    or not isinstance(filename, str)
                    or not filename
                    or not isinstance(markdown, str)
                    or not markdown
                ):
                    raise ReviewError("invalid_consolidation_output")
                if output_record_id in reserved_record_ids:
                    raise ReviewError(f"duplicate_record_id: {output_record_id}")
                reserved_record_ids.add(output_record_id)
                try:
                    output_fields = validate_record_content(
                        markdown.encode("utf-8"),
                        category=category,
                        record_id=output_record_id,
                        filename=filename,
                    )
                except (RecordError, UnicodeEncodeError) as exc:
                    raise ReviewError(f"invalid_consolidation_output: {exc}") from exc
                editable = item.get("fields", {})
                allowed = set(editable_fields_for(category, output_fields))
                protected = set(editable) - allowed
                if protected:
                    raise ReviewError(f"protected_field: {sorted(protected)[0]}")
                normalized = dict(item)
                normalized["fields"] = {
                    key: editable.get(key, output_fields[key]) for key in editable_fields_for(category, output_fields)
                }
                # The page cannot evaluate outcome evidence by itself; report whether the
                # rendered evidence.state already satisfies the vetting gate, the same flag
                # the record surface reads from the backend.
                normalized["outcome_verified"] = outcome_state_is_verified(
                    normalized["fields"].get("evidence.state", output_fields.get("evidence.state", ""))
                )
                consolidations.append(normalized)
        if clusters:
            supplied_clusters = {item.get("cluster") for item in consolidations}
            for cluster in sorted(clusters):
                if cluster in supplied_clusters:
                    continue
                saved = draft.decisions.get(f"cluster:{cluster}") if draft is not None else None
                if isinstance(saved, dict) and saved.get("action") == "merge":
                    consolidations.append(
                        {
                            "cluster": saved["cluster"],
                            "members": saved["members"],
                            "member_hashes": saved["member_hashes"],
                            "category": saved["category"],
                            "record_id": saved["record_id"],
                            "filename": saved["filename"],
                            "markdown": saved["proposal_markdown"],
                            "fields": saved["editable_fields"],
                            "outcome_verified": outcome_state_is_verified(
                                saved["editable_fields"].get("evidence.state", "")
                            ),
                        }
                    )
                    continue
                raise ReviewError(f"missing_merge_proposal: {cluster}")
        return cls(
            project_root,
            records,
            clusters,
            proposals=proposals,
            consolidations=consolidations,
            draft=draft,
            interaction_language=interaction_language,
        )

    def snapshot(self) -> dict[str, Any]:
        return {
            "schema_version": SCHEMA_VERSION,
            "project_name": self.project_root.name,
            "records": [self.records[key].to_public_dict() for key in sorted(self.records)],
            "clusters": self.clusters,
            "proposals": self.proposals,
            "consolidations": self.consolidations,
            "draft": self.draft.to_dict(),
            "summary": self.summary(),
            "interaction_language": self.interaction_language,
        }

    def stage(self, request: Mapping[str, Any], *, expected_revision: int | None = None) -> dict[str, Any]:
        if expected_revision is not None and expected_revision != self.draft.revision:
            raise ReviewError("stale_draft_revision")
        action = request.get("action")
        record_id = request.get("record_id")
        if action not in ACTIONS:
            raise ReviewError("invalid_action")
        if action == "merge":
            decision = self._merge_decision(request)
            for member in decision["members"]:
                self.draft.decisions.pop(member, None)
                self.draft.deferred = [item for item in self.draft.deferred if item != member]
            self.draft.decisions[f"cluster:{decision['cluster']}"] = decision
        elif action == "keep_separate":
            cluster = request.get("cluster")
            if not isinstance(cluster, str) or cluster not in self.clusters:
                raise ReviewError("unknown_cluster")
            self.draft.decisions.pop(f"cluster:{cluster}", None)
            for member in self.clusters[cluster]:
                if member not in self.draft.decisions and member not in self.draft.deferred:
                    self.draft.deferred.append(member)
        else:
            if not isinstance(record_id, str) or record_id not in self.records:
                raise ReviewError("unknown_record")
            if self.records[record_id].status != "candidate":
                raise ReviewError("record_not_candidate")
            # Validate before touching the draft: a request rejected here must leave the
            # staged work exactly as it was, including any merge this record belongs to.
            decision = None if action == "defer" else self._decision_for_record(action, record_id, request)
            for key, staged in list(self.draft.decisions.items()):
                if staged.get("action") == "merge" and record_id in staged.get("members", []):
                    self.draft.decisions.pop(key)
            if action == "defer":
                self.draft.decisions.pop(record_id, None)
                if record_id not in self.draft.deferred:
                    self.draft.deferred.append(record_id)
            else:
                self.draft.deferred = [item for item in self.draft.deferred if item != record_id]
                self.draft.decisions[record_id] = decision
        self.draft.revision += 1
        return self.draft.to_dict()

    def _decision_for_record(self, action: str, record_id: str, request: Mapping[str, Any]) -> dict[str, Any]:
        document = self.records[record_id]
        fields = request.get("fields", {})
        # Values persist into the draft verbatim and the draft codec requires strings;
        # anything else would stage successfully and make the saved draft unopenable.
        if not isinstance(fields, dict) or not all(isinstance(value, str) for value in fields.values()):
            raise ReviewError("invalid_fields")
        verification = request.get("verification")
        if verification is not None and not isinstance(verification, str):
            raise ReviewError("invalid_verification")
        if action == "remove":
            if fields or verification:
                raise ReviewError("remove_has_payload")
            return {"action": "remove", "base_hash": document.sha256}
        desired_status = request.get("status", "candidate" if action == "replace" else "vetted")
        if desired_status not in {"candidate", "vetted"}:
            raise ReviewError("invalid_desired_status")
        if action == "vet":
            desired_status = "vetted"
        try:
            rendered = document.render(
                fields,
                status=desired_status,
                verification=verification if verification and verification.strip() else None,
            )
        except RecordError as exc:
            raise ReviewError(str(exc)) from exc
        # Gate on the bytes that will be written, exactly as the apply-time gate does.
        # `render` rebuilds `evidence.state` from the stored value whenever an attestation
        # is supplied, so the request's own field value is not what gets written, and a
        # gate reading the request would accept a decision that application then refuses.
        final_evidence_state = next(
            (
                line.split(":", 1)[1].strip()
                for line in rendered.decode("utf-8").splitlines()
                if line.startswith("- evidence.state:")
            ),
            "",
        )
        if desired_status == "vetted" and not (
            outcome_state_is_verified(final_evidence_state)
            or (isinstance(verification, str) and outcome_state_is_verified(verification))
        ):
            raise ReviewError("verification_required")
        return {
            "action": "vet" if action == "vet" and not fields else "replace",
            "base_hash": document.sha256,
            "fields": dict(fields),
            "status": desired_status,
            # Store the value exactly as it was rendered: whitespace-only normalizes to
            # absent above, and apply-time re-render reads this field back verbatim.
            "verification": (verification or "").strip(),
            "rendered": rendered.decode("utf-8"),
        }

    def _merge_decision(self, request: Mapping[str, Any]) -> dict[str, Any]:
        cluster = request.get("cluster")
        if not isinstance(cluster, str) or cluster not in self.clusters:
            raise ReviewError("unknown_cluster")
        if "proposal" in request:
            raise ReviewError("inline_merge_proposal_not_allowed")
        proposal = next((item for item in self.consolidations if item.get("cluster") == cluster), None)
        if not isinstance(proposal, dict):
            raise ReviewError("missing_merge_proposal")
        return self._merge_decision_from_proposal(request, proposal)

    def _merge_decision_from_proposal(
        self,
        request: Mapping[str, Any],
        proposal: Mapping[str, Any],
    ) -> dict[str, Any]:
        cluster = request.get("cluster")
        if not isinstance(cluster, str) or cluster not in self.clusters:
            raise ReviewError("unknown_cluster")
        members = self.clusters[cluster]
        if sorted(proposal.get("members", [])) != sorted(members):
            raise ReviewError("invalid_consolidation_members")
        category = proposal.get("category")
        record_id = proposal.get("record_id")
        markdown = proposal.get("markdown")
        if (
            not isinstance(category, str)
            or not category
            or not isinstance(record_id, str)
            or not record_id
            or not isinstance(markdown, str)
            or not markdown
        ):
            raise ReviewError("invalid_consolidation_output")
        verification = request.get("verification")
        status = request.get("status", "candidate")
        if status not in {"candidate", "vetted"}:
            raise ReviewError("invalid_desired_status")
        if verification is not None and not isinstance(verification, str):
            raise ReviewError("invalid_verification")
        field_changes = request.get("field_changes", {})
        if not isinstance(field_changes, dict) or not all(isinstance(value, str) for value in field_changes.values()):
            raise ReviewError("invalid_fields")
        allowed_fields = set(proposal.get("fields", {}))
        if set(field_changes) - allowed_fields:
            raise ReviewError("protected_field")
        rendered = render_consolidation(markdown, field_changes, status, verification or "")
        final_evidence_state = next(
            (line.split(":", 1)[1].strip() for line in rendered.splitlines() if line.startswith("- evidence.state:")),
            "",
        )
        if status == "vetted" and not (
            outcome_state_is_verified(final_evidence_state)
            or (isinstance(verification, str) and outcome_state_is_verified(verification))
        ):
            raise ReviewError("verification_required")
        filename = proposal.get("filename", f"{record_id}.md")
        if not isinstance(filename, str):
            raise ReviewError("invalid_consolidation_output")
        try:
            validate_record_content(rendered.encode("utf-8"), category=category, record_id=record_id, filename=filename)
        except (RecordError, UnicodeEncodeError) as exc:
            raise ReviewError(f"invalid_consolidation_output: {exc}") from exc
        return {
            "action": "merge",
            "cluster": cluster,
            "members": members,
            "member_hashes": dict(proposal["member_hashes"]),
            "category": category,
            "record_id": record_id,
            "filename": filename,
            "markdown": rendered,
            "field_changes": dict(field_changes),
            "status": status,
            # Same convention as record decisions: store the value as it was rendered,
            # so an apply-time re-render can never read different bytes than staging did.
            "verification": (verification or "").strip(),
            "proposal_markdown": markdown,
            "editable_fields": dict(proposal.get("fields", {})),
        }

    def preview(self, record_id: str) -> dict[str, Any]:
        if record_id not in self.records:
            raise ReviewError("unknown_record")
        decision = self.draft.decisions.get(record_id)
        markdown = self.records[record_id].source.decode("utf-8")
        if decision and decision.get("action") in {"vet", "replace"}:
            markdown = decision["rendered"]
        return {"record_id": record_id, "markdown": markdown, "decision": decision}

    def preview_operation(self, request: Mapping[str, Any]) -> dict[str, Any]:
        action = request.get("action")
        if action == "merge":
            decision = self._merge_decision(request)
            return {"cluster": decision["cluster"], "markdown": decision["markdown"], "decision": decision}
        record_id = request.get("record_id")
        if action not in {"vet", "replace"} or not isinstance(record_id, str) or record_id not in self.records:
            raise ReviewError("preview_requires_edit")
        decision = self._decision_for_record(action, record_id, request)
        return {"record_id": record_id, "markdown": decision["rendered"], "decision": decision}

    def refresh(self, record_ids: list[str], *, expected_revision: int) -> dict[str, Any]:
        if expected_revision != self.draft.revision:
            raise ReviewError("stale_draft_revision")
        if not record_ids or any(not isinstance(record_id, str) for record_id in record_ids):
            raise ReviewError("invalid_refresh_targets")
        try:
            current_records, current_clusters = discover_records(self.project_root)
        except RecordError as exc:
            raise ReviewError(f"invalid_profile: {exc}") from exc
        for record_id in record_ids:
            if record_id in current_records:
                self.records[record_id] = current_records[record_id]
            else:
                self.records.pop(record_id, None)
            self.draft.decisions.pop(record_id, None)
            self.draft.deferred = [item for item in self.draft.deferred if item != record_id]
        for key, decision in list(self.draft.decisions.items()):
            if decision.get("action") == "merge" and set(decision.get("members", [])) & set(record_ids):
                self.draft.decisions.pop(key)
        self.clusters = current_clusters
        self.draft.revision += 1
        return self.snapshot()

    def summary(self) -> dict[str, list[str]]:
        result = {
            "added": [],
            "replaced": [],
            "promoted": [],
            "removed": [],
            "merged": [],
            "deferred": sorted(self.draft.deferred),
            "undecided": [],
        }
        decided_records: set[str] = set()
        for key, decision in self.draft.decisions.items():
            action = decision["action"]
            if action == "remove":
                result["removed"].append(key)
                decided_records.add(key)
            elif action == "merge":
                result["merged"].append(decision["cluster"])
                result["added"].append(decision["record_id"])
                result["removed"].extend(decision["members"])
                decided_records.update(decision["members"])
            elif decision.get("status") == "vetted":
                result["promoted"].append(key)
                decided_records.add(key)
                if action == "replace":
                    result["replaced"].append(key)
            else:
                result["replaced"].append(key)
                decided_records.add(key)
        result["undecided"] = sorted(set(self.records) - decided_records - set(self.draft.deferred))
        for value in result.values():
            value.sort()
        return result
