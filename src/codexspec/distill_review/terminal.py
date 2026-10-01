"""Explicit terminal fallback backed by the shared review domain."""

from __future__ import annotations

import json
import re
import unicodedata
from collections.abc import Callable
from functools import lru_cache
from pathlib import Path
from typing import Any

from .domain import ReviewError, ReviewService
from .session import SessionStore
from .transaction import ProfileTransaction, TransactionError

_CATALOG_DIR = Path(__file__).parent / "assets" / "i18n"


@lru_cache(maxsize=None)
def catalog_for(language: str) -> dict[str, Any]:
    if not re.fullmatch(r"[A-Za-z-]+", language):
        language = "en"
    path = _CATALOG_DIR / f"{language}.json"
    if not path.is_file() and language.startswith("pt-"):
        path = _CATALOG_DIR / "pt.json"
    if not path.is_file():
        path = _CATALOG_DIR / "en.json"
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return value if isinstance(value, dict) else {}


def _message(service: ReviewService, key: str, english: str) -> str:
    value = catalog_for(service.interaction_language).get(f"terminal.{key}", english)
    return value if isinstance(value, str) else english


def localized_error(
    language: str,
    error: Exception | str,
    *,
    records: list[str] | None = None,
    failures: list[str] | None = None,
) -> str:
    message = str(error)
    key, separator, detail = message.partition(":")
    catalog = catalog_for(language)
    localized = catalog.get(f"error.{key}")
    if not isinstance(localized, str):
        localized = catalog.get("error.validation", "Review validation failed.")
    lines = [str(localized), f"{catalog.get('error.code', 'Rule')}: {key}"]
    if separator and detail.strip():
        lines.append(f"{catalog.get('error.detail', 'Detail')}: {detail.strip()}")
    error_records = records if records is not None else getattr(error, "records", None)
    error_failures = failures if failures is not None else getattr(error, "failures", None)
    if error_records:
        lines.append(f"{catalog.get('error.records', 'Records')}: {', '.join(error_records)}")
    if error_failures and error_failures != [message]:
        lines.append(f"{catalog.get('error.failures', 'Failures')}: {'; '.join(error_failures)}")
    return "\n".join(lines)


def localized_result(language: str, status: str) -> str:
    value = catalog_for(language).get(f"result.{status}", status)
    return value if isinstance(value, str) else status


def _localized_error(service: ReviewService, error: Exception) -> str:
    return localized_error(service.interaction_language, error)


def _localized_result(service: ReviewService, status: str) -> str:
    return localized_result(service.interaction_language, status)


def safe_terminal(value: object) -> str:
    """Render untrusted profile content without terminal control sequences."""
    result: list[str] = []
    for character in str(value):
        codepoint = ord(character)
        if character in {"\n", "\t"}:
            result.append(character)
        elif codepoint < 32 or codepoint == 127 or 0x80 <= codepoint <= 0x9F:
            result.append(f"\\x{codepoint:02x}")
        elif unicodedata.category(character) == "Cf":
            result.append(f"\\u{codepoint:04x}")
        else:
            result.append(character)
    return "".join(result)


def _emit(output_fn: Callable[[str], None], value: object) -> None:
    output_fn(safe_terminal(value))


def _display_summary(service: ReviewService) -> str:
    summary = service.summary()
    catalog = catalog_for(service.interaction_language)
    localized = {catalog.get(f"summary.{key}", key): value for key, value in summary.items()}
    return json.dumps(localized, ensure_ascii=False, indent=2)


def _confirm_preview(
    service: ReviewService,
    operation: dict[str, Any],
    *,
    input_fn: Callable[[str], str],
    output_fn: Callable[[str], None],
) -> bool:
    _emit(output_fn, service.preview_operation(operation)["markdown"])
    confirmation = input_fn(_message(service, "confirm_preview", "Stage this exact preview? [y/N]: ")).strip().lower()
    return confirmation in {"y", "yes"}


def run_text_review(
    service: ReviewService,
    store: SessionStore,
    *,
    input_fn: Callable[[str], str] = input,
    output_fn: Callable[[str], None] = print,
) -> dict[str, Any]:
    for record_id in sorted(service.records):
        record = service.records[record_id]
        if record.status != "candidate":
            continue
        _emit(output_fn, f"{record_id}: {record.fields.get('claim', record.title)}")
        _emit(output_fn, record.source.decode("utf-8"))
        while True:
            choice = (
                input_fn(_message(service, "candidate_prompt", "[v]et [e]dit [d]rop [s]kip [q]uit: ")).strip().lower()
            )
            try:
                if choice == "v":
                    verification = ""
                    if not record.outcome_verified:
                        verification = input_fn(
                            _message(service, "verification", "Verification result/evidence: ")
                        ).strip()
                    operation = {"action": "vet", "record_id": record_id, "verification": verification}
                    if not _confirm_preview(service, operation, input_fn=input_fn, output_fn=output_fn):
                        continue
                    service.stage(operation)
                elif choice == "e":
                    raw = input_fn(_message(service, "editable", "Editable fields as JSON object: ")).strip()
                    fields = json.loads(raw or "{}")
                    desired = (
                        input_fn(_message(service, "status", "Status [candidate/vetted]: ")).strip() or "candidate"
                    )
                    verification = ""
                    if desired == "vetted":
                        verification = input_fn(
                            _message(service, "verification", "Verification result/evidence: ")
                        ).strip()
                    operation = {
                        "action": "replace",
                        "record_id": record_id,
                        "fields": fields,
                        "status": desired,
                        "verification": verification,
                    }
                    if not _confirm_preview(service, operation, input_fn=input_fn, output_fn=output_fn):
                        continue
                    service.stage(operation)
                elif choice == "d":
                    service.stage({"action": "remove", "record_id": record_id})
                elif choice == "s":
                    service.stage({"action": "defer", "record_id": record_id})
                elif choice == "q":
                    if service.draft.decisions or service.draft.deferred:
                        store.save(service.draft)
                    _emit(output_fn, _localized_result(service, "cancelled"))
                    return {"status": "cancelled", "summary": service.summary()}
                else:
                    _emit(output_fn, _message(service, "unknown", "Unknown choice."))
                    continue
            except (ReviewError, json.JSONDecodeError) as exc:
                _emit(output_fn, f"{_message(service, 'error', 'Error')}: {_localized_error(service, exc)}")
                continue
            store.save(service.draft)
            break
    proposals = {item["cluster"]: item for item in service.consolidations}
    for cluster in sorted(service.clusters):
        proposal = proposals.get(cluster)
        _emit(
            output_fn,
            f"{_message(service, 'cluster', 'Cluster')} {cluster}: {', '.join(service.clusters[cluster])}",
        )
        for member in service.clusters[cluster]:
            _emit(output_fn, service.records[member].source.decode("utf-8"))
        while True:
            prompt = (
                _message(service, "cluster_prompt", "[m]erge [k]eep separate [q]uit: ")
                if proposal
                else _message(service, "keep_prompt", "[k]eep separate [q]uit: ")
            )
            choice = input_fn(prompt).strip().lower()
            try:
                if choice == "k":
                    service.stage({"action": "keep_separate", "cluster": cluster})
                elif choice == "m" and proposal is not None:
                    raw = input_fn(_message(service, "proposal", "Editable proposal fields as JSON object: ")).strip()
                    changes = json.loads(raw or "{}")
                    desired = (
                        input_fn(_message(service, "status", "Status [candidate/vetted]: ")).strip() or "candidate"
                    )
                    verification = ""
                    if desired == "vetted":
                        verification = input_fn(
                            _message(service, "verification", "Verification result/evidence: ")
                        ).strip()
                    operation = {
                        "action": "merge",
                        "cluster": cluster,
                        "field_changes": changes,
                        "status": desired,
                        "verification": verification,
                    }
                    if not _confirm_preview(service, operation, input_fn=input_fn, output_fn=output_fn):
                        continue
                    service.stage(operation)
                elif choice == "q":
                    if service.draft.decisions or service.draft.deferred:
                        store.save(service.draft)
                    _emit(output_fn, _localized_result(service, "cancelled"))
                    return {"status": "cancelled", "summary": service.summary()}
                else:
                    _emit(output_fn, _message(service, "unknown", "Unknown choice."))
                    continue
            except (ReviewError, json.JSONDecodeError) as exc:
                _emit(output_fn, f"{_message(service, 'error', 'Error')}: {_localized_error(service, exc)}")
                continue
            store.save(service.draft)
            break
    _emit(output_fn, _display_summary(service))
    final_choice = input_fn(_message(service, "apply", "[a]pply all / [c]ancel / [x]discard draft: ")).strip().lower()
    if final_choice == "x":
        store.discard()
        _emit(output_fn, _localized_result(service, "discarded"))
        return {"status": "discarded"}
    if final_choice != "a":
        _emit(output_fn, _localized_result(service, "cancelled"))
        return {"status": "cancelled", "summary": service.summary()}
    try:
        result = ProfileTransaction(service.project_root, service.records, service.draft, store).apply()
    except TransactionError as exc:
        _emit(output_fn, _localized_error(service, exc))
        return {
            "status": "conflict" if exc.records else "invalid_input",
            "error": str(exc),
            "records": exc.records,
            "failures": exc.failures,
            "summary": service.summary(),
        }
    result["summary"] = service.summary()
    _emit(output_fn, _localized_result(service, "applied"))
    return result
