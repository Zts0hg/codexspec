"""Lossless field-aware codec for profile Markdown records."""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Mapping

from codexspec.profile import PROFILE_CATEGORIES

_HEADING = re.compile(r"^(#{2,3})\s+([A-Za-z]+-\d{4}-\d{4}-\d{4}[a-z0-9]{2}-\d+):\s*(.+?)\r?\n?$")
_FIELD = re.compile(r"^- ([A-Za-z0-9_./-]+(?:\.[A-Za-z0-9_./-]+)*):(?:\s?(.*?))\r?\n?$")
_CLUSTER = re.compile(r"(?:^|;)\s*cluster:\s*([a-z0-9]+(?:-[a-z0-9]+)*)\s*(?:;|$)")
_PROTECTED = frozenset({"id", "category", "path", "type", "provenance", "status"})
_CATEGORY_TYPES = {
    "constraints": "constraint",
    "conventions": "convention",
    "pitfalls": "pitfall",
    "decisions": "decision",
    "strategies": "strategy",
    "runbooks": "runbook",
}
_CATEGORY_ID_PREFIXES = {
    "constraints": "C",
    "conventions": "Con",
    "pitfalls": "P",
    "decisions": "D",
    "strategies": "S",
    "runbooks": "R",
}
_RECORD_ID = re.compile(r"^(?P<prefix>[A-Za-z]+)-\d{4}-\d{4}-\d{4}[a-z0-9]{2}-\d+$")
_SLUG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
_TYPE_FIELDS = {
    "pitfall": ("root-cause", "workaround", "lesson"),
    "strategy": ("trigger", "action"),
    "runbook": ("steps", "failure-recovery"),
}
_COMMON_EDITABLE = ("claim", "scope", "scope/when")
_EVIDENCE_EDITABLE = ("evidence.facts", "evidence.state")


def outcome_state_is_verified(state: str) -> bool:
    """Recognize concrete outcome evidence across supported interaction languages."""
    if "?" in state or "？" in state:
        return False
    if re.search(
        r"\b(?:not\s+(?:yet\s+)?verified|unverified|failed|failing|did\s+not\s+work|not\s+implemented)\b"
        r"|\b(?:never\s+verified|hypothetical|pending|unknown|uncertain|unconfirmed|not\s+recorded|no\s+outcome)\b"
        r"|\b(?:maybe|probably|perhaps|seems?|appears?|assum(?:e|ed|ing|ption)|guess(?:ed|ing)?)\b"
        r"|\b(?:tests?|checks?|build|workflow)\b[^.;]*\b(?:not|never|did\s+not|has(?:n't|\s+not)|have(?:n't|\s+not))\s+(?:passed|green)\b",
        state,
        re.IGNORECASE,
    ):
        return False
    normalized = state.casefold()
    negative_phrases = (
        "尚未验证",
        "尚未驗證",
        "未验证",
        "未驗證",
        "未通过",
        "未通過",
        "検証されていません",
        "失敗",
        "검증되지",
        "실패",
        "غير متحقق",
        "فشل",
        "nicht verifiziert",
        "fehlgeschlagen",
        "no verificado",
        "falló",
        "non vérifié",
        "échoué",
        "सत्यापित नहीं",
        "विफल",
        "non verificato",
        "fallito",
        "não verificado",
        "falhou",
        "не проверено",
        "не пройден",
        "未知",
        "待验证",
        "待驗證",
        "待确认",
        "待確認",
        "假设",
        "假設",
        "不确定",
        "不確定",
        "未记录",
        "未記錄",
        "保留中",
        "未確定",
        "미확인",
        "가정",
        "معلق",
        "غير مؤكد",
        "hypothetisch",
        "ausstehend",
        "desconocido",
        "pendiente",
        "hypothétique",
        "en attente",
        "काल्पनिक",
        "लंबित",
        "ipotetico",
        "in sospeso",
        "hipotético",
        "pendente",
        "гипотетич",
        "ожидает",
    )
    if any(phrase in normalized for phrase in negative_phrases):
        return False
    outcome_patterns = (
        r"\b(?:tests?|test suite|full suite|checks?|ci checks?|build|workflow|windows legs?)\b[^.;]*"
        r"\b(?:passed|green)\b",
        r"\bworkaround\b[^.;]*\bworked\b",
        r"\bverified\s+(?:by|through|via)\b",
        r"\boutcome\s*(?::|was|is)\s*verified\b",
        r"(?:测试|測試|检查|檢查|构建|構建|工作流|验证|驗證).{0,40}(?:通过|通過|成功|完成|已验证|已驗證)",
        r"(?:テスト|チェック|ビルド|ワークフロー|検証).{0,40}(?:合格|通過|成功|完了|確認済み)",
        r"(?:테스트|검사|빌드|워크플로|검증).{0,40}(?:통과|성공|완료|확인)",
        r"(?:اختبار|فحص|بناء|سير العمل|تحقق).{0,40}(?:نجح|اجتاز|مكتمل|تم التحقق)",
        r"\b(?:tests?|prüfungen?|build|workflow)\b.{0,60}\b(?:bestanden|erfolgreich|grün)\b",
        r"\b(?:pruebas?|comprobaciones?|compilación|flujo)\b.{0,60}\b(?:pasaron|aprobadas?|exitosa?|verde)\b",
        r"\b(?:tests?|vérifications?|compilation|workflow)\b.{0,60}\b(?:réussis?|passés?|verte?)\b",
        r"(?:परीक्षण|जाँच|बिल्ड|वर्कफ़्लो|सत्यापन).{0,40}(?:सफल|पास|पूर्ण|सत्यापित)",
        r"\b(?:tests?|controlli|build|flusso)\b.{0,60}\b(?:superati|riusciti|verde)\b",
        r"\b(?:testes?|verificações|compilação|fluxo)\b.{0,60}\b(?:passaram|aprovados?|bem-sucedida|verde)\b",
        r"(?:тесты?|проверки|сборка|процесс|проверено).{0,60}(?:прошли|успешн|завершен|подтвержден)",
    )
    return any(re.search(pattern, state, re.IGNORECASE) for pattern in outcome_patterns)


def editable_fields_for(category: str, fields: Mapping[str, str]) -> tuple[str, ...]:
    """Return the ordered structured fields users may edit for one record."""
    expected_type = _CATEGORY_TYPES.get(category)
    if expected_type is None:
        raise RecordError("invalid_category")
    ordered = (*_COMMON_EDITABLE, *_TYPE_FIELDS.get(expected_type, ()), *_EVIDENCE_EDITABLE)
    return ("title", *(key for key in ordered if key in fields))


class RecordError(ValueError):
    """A profile record cannot be represented or changed safely."""


@dataclass(frozen=True)
class RecordDocument:
    project_root: Path
    path: Path
    category: str
    record_id: str
    title: str
    source: bytes
    lines: tuple[str, ...]
    heading_index: int
    field_indexes: Mapping[str, int]
    fields: Mapping[str, str]

    @property
    def sha256(self) -> str:
        return hashlib.sha256(self.source).hexdigest()

    @property
    def status(self) -> str:
        return self.fields.get("status", "")

    @property
    def cluster(self) -> str | None:
        value = self.fields.get("consolidation", "")
        match = _CLUSTER.search(value)
        return match.group(1) if match else None

    @property
    def outcome_verified(self) -> bool:
        return outcome_state_is_verified(self.fields.get("evidence.state", ""))

    @property
    def editable_fields(self) -> tuple[str, ...]:
        return editable_fields_for(self.category, self.fields)

    def render(
        self,
        changes: Mapping[str, str],
        *,
        status: str | None = None,
        verification: str | None = None,
    ) -> bytes:
        unknown = set(changes) - set(self.field_indexes) - {"title"}
        if unknown:
            raise RecordError(f"unknown_field: {sorted(unknown)[0]}")
        protected = set(changes) - set(self.editable_fields)
        if protected:
            raise RecordError(f"protected_field: {sorted(protected)[0]}")
        lines = list(self.lines)
        if "title" in changes:
            title = str(changes["title"]).strip()
            if not title or "\n" in title or "\r" in title:
                raise RecordError("invalid_title")
            hashes = _HEADING.match(lines[self.heading_index]).group(1)  # type: ignore[union-attr]
            ending = "\r\n" if lines[self.heading_index].endswith("\r\n") else "\n"
            lines[self.heading_index] = f"{hashes} {self.record_id}: {title}{ending}"
        replacements = dict(changes)
        if verification is not None:
            if "evidence.state" not in self.field_indexes:
                raise RecordError("missing_evidence_state")
            attestation = verification.strip()
            if not attestation:
                raise RecordError("empty_verification")
            current = self.fields["evidence.state"].strip()
            replacements["evidence.state"] = (
                f"{current}; review verification: {attestation}" if current else attestation
            )
        if status is not None:
            if status not in {"candidate", "vetted", "conflict/needs-adjudication"}:
                raise RecordError("invalid_status")
            replacements["status"] = status
        for key, raw_value in replacements.items():
            if key == "title":
                continue
            value = str(raw_value).strip()
            if "\n" in value or "\r" in value:
                raise RecordError(f"multiline_field: {key}")
            index = self.field_indexes[key]
            ending = "\r\n" if lines[index].endswith("\r\n") else "\n"
            lines[index] = f"- {key}: {value}{ending}"
        rendered = "".join(lines).encode("utf-8")
        validate_record_content(
            rendered,
            category=self.category,
            record_id=self.record_id,
            filename=self.path.name,
        )
        return rendered

    def to_public_dict(self) -> dict[str, object]:
        return {
            "id": self.record_id,
            "title": self.title,
            "category": self.category,
            "path": self.path.relative_to(self.project_root).as_posix(),
            "sha256": self.sha256,
            "status": self.status,
            "cluster": self.cluster,
            "outcome_verified": self.outcome_verified,
            "fields": dict(self.fields),
            "editable_fields": list(self.editable_fields),
            "protected_fields": sorted(_PROTECTED),
            "markdown": self.source.decode("utf-8"),
        }


def parse_record(path: Path, project_root: Path) -> RecordDocument:
    root = project_root.resolve()
    profile_root = (root / ".codexspec" / "profile").resolve()
    candidate = path.absolute()
    if path.is_symlink():
        raise RecordError("symlink_not_allowed")
    resolved = path.resolve()
    try:
        relative = resolved.relative_to(profile_root)
    except ValueError as exc:
        raise RecordError("path_outside_profile") from exc
    if len(relative.parts) != 2 or relative.parts[0] not in PROFILE_CATEGORIES:
        raise RecordError("invalid_record_path")
    if candidate != resolved:
        raise RecordError("symlink_not_allowed")
    if not resolved.is_file() or resolved.suffix != ".md" or resolved.name == ".gitkeep":
        raise RecordError("invalid_record_file")
    source = resolved.read_bytes()
    try:
        text = source.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise RecordError("record_not_utf8") from exc
    lines, heading_index, record_id, title, fields, indexes = _inspect_record_text(text)
    validate_record_content(source, category=relative.parts[0], record_id=record_id, filename=resolved.name)

    return RecordDocument(
        project_root=root,
        path=resolved,
        category=relative.parts[0],
        record_id=record_id,
        title=title,
        source=source,
        lines=lines,
        heading_index=heading_index,
        field_indexes=indexes,
        fields=fields,
    )


def _inspect_record_text(
    text: str,
) -> tuple[tuple[str, ...], int, str, str, dict[str, str], dict[str, int]]:
    lines = tuple(text.splitlines(keepends=True))
    heading_index = -1
    record_id = ""
    title = ""
    fields: dict[str, str] = {}
    indexes: dict[str, int] = {}
    for index, line in enumerate(lines):
        heading = _HEADING.match(line)
        if heading:
            if heading_index >= 0:
                raise RecordError("duplicate_record_heading")
            heading_index = index
            record_id = heading.group(2)
            title = heading.group(3)
            continue
        field = _FIELD.match(line)
        if not field:
            continue
        key, value = field.group(1), field.group(2)
        if key in fields:
            raise RecordError(f"duplicate_field: {key}")
        fields[key] = value
        indexes[key] = index
    if heading_index < 0:
        raise RecordError("missing_record_heading")
    return lines, heading_index, record_id, title, fields, indexes


def validate_record_content(source: bytes, *, category: str, record_id: str, filename: str) -> dict[str, str]:
    """Validate record schema and protected identity without touching the filesystem."""
    if category not in PROFILE_CATEGORIES:
        raise RecordError("invalid_category")
    try:
        text = source.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise RecordError("record_not_utf8") from exc
    _, _, heading_id, title, fields, _ = _inspect_record_text(text)
    if heading_id != record_id:
        raise RecordError("record_id_mismatch")
    identity = _RECORD_ID.fullmatch(record_id)
    if identity is None or identity.group("prefix") != _CATEGORY_ID_PREFIXES[category]:
        raise RecordError("category_id_mismatch")
    if "/" in filename or "\\" in filename or not filename.endswith(".md"):
        raise RecordError("heading_filename_mismatch")
    stem = filename[:-3]
    if stem == record_id:
        slug = None
    elif stem.startswith(f"{record_id}-"):
        slug = stem[len(record_id) + 1 :]
    else:
        raise RecordError("heading_filename_mismatch")
    if slug is not None and (len(slug) > 50 or _SLUG.fullmatch(slug) is None):
        raise RecordError("invalid_filename_slug")
    required = {"claim", "type", "evidence.facts", "evidence.state", "provenance", "status"}
    expected_type = _CATEGORY_TYPES[category]
    required.update(_TYPE_FIELDS.get(expected_type, set()))
    missing = sorted(required - set(fields))
    if missing:
        raise RecordError(f"missing_field: {missing[0]}")
    empty = sorted(key for key in required if not fields[key].strip())
    if empty:
        raise RecordError(f"empty_field: {empty[0]}")
    if fields["type"] != expected_type:
        raise RecordError("category_type_mismatch")
    if fields["status"] not in {"candidate", "vetted", "conflict/needs-adjudication"}:
        raise RecordError("invalid_status")
    return {"title": title, **fields}


def discover_all_records(project_root: Path) -> dict[str, RecordDocument]:
    """Discover every profile record and enforce repository-wide ID uniqueness."""
    root = project_root.resolve()
    profile = root / ".codexspec" / "profile"
    records: dict[str, RecordDocument] = {}
    if not profile.exists():
        return records
    for category in PROFILE_CATEGORIES:
        directory = profile / category
        if not directory.is_dir():
            continue
        for path in sorted(directory.glob("*.md")):
            if path.name == ".gitkeep":
                continue
            document = parse_record(path, root)
            if document.record_id in records:
                raise RecordError(f"duplicate_record_id: {document.record_id}")
            records[document.record_id] = document
    return records


def discover_records(project_root: Path) -> tuple[dict[str, RecordDocument], dict[str, list[str]]]:
    records: dict[str, RecordDocument] = {}
    clusters: dict[str, list[str]] = {}
    for document in discover_all_records(project_root).values():
        if document.status == "candidate" or document.cluster:
            records[document.record_id] = document
        if document.cluster:
            clusters.setdefault(document.cluster, []).append(document.record_id)
    return records, clusters
