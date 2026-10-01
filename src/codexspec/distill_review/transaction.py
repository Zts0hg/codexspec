"""Recoverable, hash-guarded profile mutation transactions."""

from __future__ import annotations

import base64
import hashlib
import json
import os
import secrets
import tempfile
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Callable, Iterator, Mapping

from codexspec.profile import PROFILE_CATEGORIES

from .domain import ReviewError, render_consolidation
from .models import ReviewDraft
from .records import (
    RecordDocument,
    RecordError,
    discover_all_records,
    outcome_state_is_verified,
    parse_record,
    validate_record_content,
)
from .session import AtomicWriteConflictError, SessionError, SessionStore


class TransactionError(RuntimeError):
    """A profile batch cannot be applied without violating its preconditions."""

    def __init__(
        self,
        message: str,
        *,
        records: list[str] | None = None,
        failures: list[str] | None = None,
    ) -> None:
        super().__init__(message)
        self.records = records or []
        self.failures = failures or [message]


def _encoded(content: bytes | None) -> str | None:
    return None if content is None else base64.b64encode(content).decode("ascii")


def _decoded(content: str | None) -> bytes | None:
    return None if content is None else base64.b64decode(content.encode("ascii"), validate=True)


def _valid_hash(value: object) -> bool:
    return isinstance(value, str) and len(value) == 64 and all(character in "0123456789abcdef" for character in value)


class ProfileTransaction:
    def __init__(
        self,
        project_root: Path,
        records: Mapping[str, RecordDocument],
        draft: ReviewDraft,
        store: SessionStore,
    ) -> None:
        self.project_root = project_root.resolve()
        self.records = dict(records)
        self.draft = draft
        self.store = store

    def _confined_path(self, relative: str) -> Path:
        path = (self.project_root / relative).absolute()
        codexspec = (self.project_root / ".codexspec").absolute()
        profile = (self.project_root / ".codexspec" / "profile").absolute()
        try:
            parts = path.relative_to(profile).parts
        except ValueError as exc:
            raise TransactionError(f"path_outside_profile: {relative}") from exc
        if len(parts) != 2 or parts[0] not in PROFILE_CATEGORIES:
            raise TransactionError(f"invalid_target_path: {relative}")
        category_path = profile / parts[0]
        if any(component.is_symlink() for component in (codexspec, profile, category_path, path)):
            raise TransactionError(f"symlink_target: {relative}")
        try:
            if codexspec.resolve() != codexspec or profile.resolve() != profile:
                raise ValueError
            path.resolve().relative_to(profile)
        except ValueError as exc:
            raise TransactionError(f"path_outside_profile: {relative}") from exc
        return path

    def _changes(self) -> list[dict[str, Any]]:
        changes: list[dict[str, Any]] = []
        targets: set[str] = set()
        transaction_token = secrets.token_hex(8)
        merge_record_ids: set[str] = set()
        conflicts = self._hash_conflicts()
        failures = [f"hash_conflict: {record_id}" for record_id in conflicts]
        failed_records = set(conflicts)

        def append(path: Path, *, expected_hash: str | None, new: bytes | None, record_id: str) -> None:
            relative = path.relative_to(self.project_root).as_posix()
            if relative in targets:
                raise TransactionError(f"duplicate_target: {relative}", records=[record_id])
            targets.add(relative)
            target = self._confined_path(relative)
            old = target.read_bytes() if target.exists() else None
            if expected_hash is None:
                if old is not None:
                    raise TransactionError(f"unexpected_existing_target: {relative}", records=[record_id])
            else:
                if old is None:
                    raise TransactionError(f"missing_target: {relative}", records=[record_id])
                actual = hashlib.sha256(old).hexdigest()
                if actual != expected_hash:
                    raise TransactionError(f"hash_conflict: {record_id}", records=[record_id])
            changes.append(
                {
                    "record_id": record_id,
                    "path": relative,
                    "backup": (
                        target.with_name(f".{target.name}.distill-review-{transaction_token}-{len(changes)}.bak")
                        .relative_to(self.project_root)
                        .as_posix()
                    ),
                    "old": _encoded(old),
                    "new": _encoded(new),
                    "phase": "pending",
                }
            )

        for key, decision in self.draft.decisions.items():
            try:
                if decision.get("action") == "merge":
                    output_id = decision.get("record_id")
                    if isinstance(output_id, str) and output_id in merge_record_ids:
                        raise TransactionError(f"duplicate_record_id: {output_id}", records=[output_id])
                    if isinstance(output_id, str):
                        merge_record_ids.add(output_id)
                self._append_decision_changes(key, decision, append)
            except (TransactionError, KeyError, TypeError, UnicodeEncodeError) as exc:
                failure = str(exc) if isinstance(exc, TransactionError) else f"invalid_draft_decision: {key}: {exc}"
                if failure not in failures:
                    failures.append(failure)
                if isinstance(exc, TransactionError) and exc.records:
                    failed_records.update(exc.records)
                else:
                    failed_records.add(key)
        if failures:
            raise TransactionError(
                "validation_failed: " + "; ".join(failures),
                records=sorted(failed_records),
                failures=failures,
            )
        return changes

    def _append_decision_changes(
        self,
        key: str,
        decision: Mapping[str, Any],
        append: Callable[..., None],
    ) -> None:
        action = decision.get("action")
        if action in {"vet", "replace"}:
            document = self.records.get(key)
            if document is None:
                raise TransactionError(f"unknown_draft_target: {key}", records=[key])
            base_hash = decision.get("base_hash")
            if not _valid_hash(base_hash):
                raise TransactionError(f"invalid_base_hash: {key}", records=[key])
            cached_rendered = decision.get("rendered")
            if not isinstance(cached_rendered, str):
                raise TransactionError(f"invalid_rendered_record: {key}: missing_content", records=[key])
            try:
                current = parse_record(document.path, self.project_root)
                if current.sha256 != base_hash:
                    raise TransactionError(f"hash_conflict: {key}", records=[key])
                rendered = current.render(
                    decision.get("fields", {}),
                    status=decision.get("status"),
                    verification=decision.get("verification") or None,
                )
                validated = validate_record_content(
                    rendered,
                    category=current.category,
                    record_id=current.record_id,
                    filename=current.path.name,
                )
            except (RecordError, TypeError) as exc:
                raise TransactionError(f"invalid_rendered_record: {key}: {exc}", records=[key]) from exc
            if rendered.decode("utf-8") != cached_rendered:
                raise TransactionError(f"invalid_draft_semantics: {key}", records=[key])
            if action == "vet" and decision.get("status") != "vetted":
                raise TransactionError(f"invalid_draft_semantics: {key}", records=[key])
            if decision.get("status") == "vetted" and not (
                outcome_state_is_verified(validated["evidence.state"])
                or outcome_state_is_verified(str(decision.get("verification", "")))
            ):
                raise TransactionError(f"verification_required: {key}", records=[key])
            append(current.path, expected_hash=base_hash, new=rendered, record_id=key)
        elif action == "remove":
            document = self.records.get(key)
            if document is None:
                raise TransactionError(f"unknown_draft_target: {key}", records=[key])
            base_hash = decision.get("base_hash")
            if not _valid_hash(base_hash):
                raise TransactionError(f"invalid_base_hash: {key}", records=[key])
            append(document.path, expected_hash=base_hash, new=None, record_id=key)
        elif action == "merge":
            self._append_merge_changes(decision, append)
        else:
            raise TransactionError(f"invalid_action: {action}", records=[key])

    def _append_merge_changes(self, decision: Mapping[str, Any], append: Callable[..., None]) -> None:
        category = decision.get("category")
        filename = decision.get("filename")
        record_id = decision.get("record_id")
        if (
            not isinstance(category, str)
            or category not in PROFILE_CATEGORIES
            or not isinstance(record_id, str)
            or not isinstance(filename, str)
            or Path(filename).name != filename
        ):
            raise TransactionError("invalid_merge_target")
        if Path(filename).suffix != ".md" or not (
            filename == f"{record_id}.md" or filename.startswith(f"{record_id}-")
        ):
            raise TransactionError("invalid_merge_filename", records=[record_id])
        try:
            if record_id in discover_all_records(self.project_root):
                raise TransactionError(f"duplicate_record_id: {record_id}", records=[record_id])
        except RecordError as exc:
            raise TransactionError(f"invalid_profile_record: {exc}", records=[record_id]) from exc
        cached_rendered = decision.get("markdown")
        proposal_markdown = decision.get("proposal_markdown")
        if not isinstance(cached_rendered, str) or not isinstance(proposal_markdown, str):
            raise TransactionError("invalid_merge_markdown", records=[record_id])
        try:
            rendered_value = render_consolidation(
                proposal_markdown,
                decision.get("field_changes", {}),
                decision.get("status", "candidate"),
                decision.get("verification", ""),
            )
        except (ReviewError, TypeError) as exc:
            raise TransactionError(f"invalid_merge_markdown: {exc}", records=[record_id]) from exc
        if rendered_value != cached_rendered:
            raise TransactionError(f"invalid_draft_semantics: {record_id}", records=[record_id])
        rendered = rendered_value.encode("utf-8")
        try:
            validated = validate_record_content(rendered, category=category, record_id=record_id, filename=filename)
        except RecordError as exc:
            raise TransactionError(f"invalid_rendered_record: {record_id}: {exc}", records=[record_id]) from exc
        if decision.get("status") == "vetted" and not (
            outcome_state_is_verified(validated["evidence.state"])
            or outcome_state_is_verified(str(decision.get("verification", "")))
        ):
            raise TransactionError(f"verification_required: {record_id}", records=[record_id])
        add_path = self.project_root / ".codexspec" / "profile" / category / filename
        append(add_path, expected_hash=None, new=rendered, record_id=record_id)
        members = decision.get("members")
        member_hashes = decision.get("member_hashes")
        if not isinstance(members, list) or not isinstance(member_hashes, dict):
            raise TransactionError("invalid_merge_members", records=[record_id])
        for member in members:
            if not isinstance(member, str) or not _valid_hash(member_hashes.get(member)):
                raise TransactionError("invalid_merge_members", records=[record_id])
            document = self.records.get(member)
            if document is None:
                raise TransactionError(f"unknown_draft_target: {member}", records=[member])
            append(document.path, expected_hash=member_hashes[member], new=None, record_id=member)

    def _hash_conflicts(self) -> list[str]:
        conflicts: set[str] = set()
        for key, decision in self.draft.decisions.items():
            action = decision.get("action")
            if action in {"vet", "replace", "remove"}:
                document = self.records.get(key)
                if document is None or not document.path.is_file() or document.path.is_symlink():
                    conflicts.add(key)
                elif hashlib.sha256(document.path.read_bytes()).hexdigest() != decision.get("base_hash"):
                    conflicts.add(key)
            elif action == "merge":
                for member in decision.get("members", []):
                    document = self.records.get(member)
                    if document is None:
                        conflicts.add(member)
                        continue
                    expected = decision.get("member_hashes", {}).get(member)
                    if not document.path.is_file() or document.path.is_symlink():
                        conflicts.add(member)
                    elif hashlib.sha256(document.path.read_bytes()).hexdigest() != expected:
                        conflicts.add(member)
        return sorted(conflicts)

    def prepare(self) -> dict[str, Any]:
        self.store.prepare()
        changes = self._changes()
        journal = {"schema_version": 2, "state": "prepared", "changes": changes}
        self.store.save_transaction(journal)
        return journal

    @staticmethod
    def _sync_directory(path: Path) -> None:
        """Durably order directory entries where the platform permits it."""
        try:
            descriptor = os.open(path, os.O_RDONLY)
        except OSError:
            return
        try:
            os.fsync(descriptor)
        except OSError:
            if os.name != "nt":
                raise
        finally:
            os.close(descriptor)

    def _revalidate_mutation_paths(self, path: Path, backup: Path | None = None) -> tuple[Path, Path | None]:
        """Re-establish confinement immediately before a filesystem mutation."""
        try:
            relative = path.absolute().relative_to(self.project_root).as_posix()
        except ValueError as exc:
            raise TransactionError(f"path_outside_profile: {path}") from exc
        target = self._confined_path(relative)
        if backup is None:
            return target, None
        try:
            backup_relative = backup.absolute().relative_to(self.project_root).as_posix()
        except ValueError as exc:
            raise TransactionError(f"invalid_backup_path: {backup}") from exc
        return target, self._backup_path(backup_relative, target)

    def _install_exclusive(self, path: Path, content: bytes) -> None:
        path, _ = self._revalidate_mutation_paths(path)
        descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
        temporary = Path(temporary_name)
        try:
            with os.fdopen(descriptor, "wb") as stream:
                if hasattr(os, "fchmod"):
                    os.fchmod(stream.fileno(), 0o644)
                stream.write(content)
                stream.flush()
                os.fsync(stream.fileno())
            try:
                path, _ = self._revalidate_mutation_paths(path)
                if temporary.parent != path.parent or temporary.is_symlink():
                    raise TransactionError(f"symlink_target: {path}")
                os.link(temporary, path)
            except FileExistsError as exc:
                raise AtomicWriteConflictError(f"concurrent_write: {path}") from exc
            ProfileTransaction._sync_directory(path.parent)
        finally:
            try:
                checked_path, _ = self._revalidate_mutation_paths(path)
                if temporary.parent == checked_path.parent and not temporary.is_symlink():
                    temporary.unlink(missing_ok=True)
            except TransactionError:
                # The temporary remains inside the directory that was trusted
                # when it was created; never follow a replaced ancestor merely
                # to clean it up.
                pass

    @contextmanager
    def _mutation_directory(self, path: Path, backup: Path) -> Iterator[tuple[int, str, str] | None]:
        """Pin a trusted category directory on POSIX so ancestor swaps cannot redirect I/O."""
        path, checked_backup = self._revalidate_mutation_paths(path, backup)
        if checked_backup is None:
            raise TransactionError(f"invalid_backup_path: {backup}")
        if os.name == "nt" or not hasattr(os, "O_DIRECTORY") or not hasattr(os, "O_NOFOLLOW"):
            yield None
            return
        try:
            relative_parts = path.relative_to(self.project_root).parts
        except ValueError as exc:
            raise TransactionError(f"path_outside_profile: {path}") from exc
        if (
            len(relative_parts) != 4
            or relative_parts[:2] != (".codexspec", "profile")
            or relative_parts[2] not in PROFILE_CATEGORIES
        ):
            raise TransactionError(f"invalid_target_path: {path}")
        flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
        descriptors: list[int] = []
        try:
            descriptor = os.open(self.project_root, flags)
            descriptors.append(descriptor)
            for component in relative_parts[:3]:
                descriptor = os.open(component, flags, dir_fd=descriptor)
                descriptors.append(descriptor)
        except OSError as exc:
            for descriptor in reversed(descriptors):
                os.close(descriptor)
            raise TransactionError(f"symlink_target: {path}") from exc
        try:
            yield descriptors[-1], path.name, checked_backup.name
        finally:
            for descriptor in reversed(descriptors):
                os.close(descriptor)

    @staticmethod
    def _exists_at(directory: int, name: str) -> bool:
        try:
            os.stat(name, dir_fd=directory, follow_symlinks=False)
        except FileNotFoundError:
            return False
        return True

    @staticmethod
    def _read_at(directory: int, name: str) -> bytes:
        flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
        descriptor = os.open(name, flags, dir_fd=directory)
        try:
            with os.fdopen(descriptor, "rb", closefd=False) as stream:
                return stream.read()
        finally:
            os.close(descriptor)

    @classmethod
    def _read_optional_at(cls, directory: int, name: str) -> bytes | None:
        return cls._read_at(directory, name) if cls._exists_at(directory, name) else None

    @staticmethod
    def _rename_at(directory: int, source: str, destination: str) -> None:
        os.rename(source, destination, src_dir_fd=directory, dst_dir_fd=directory)
        os.fsync(directory)

    @staticmethod
    def _unlink_at(directory: int, name: str, *, missing_ok: bool = True) -> None:
        try:
            os.unlink(name, dir_fd=directory)
            os.fsync(directory)
        except FileNotFoundError:
            if not missing_ok:
                raise

    @staticmethod
    def _install_exclusive_at(directory: int, name: str, content: bytes) -> None:
        temporary_name = f".{name}.{secrets.token_hex(8)}.tmp"
        flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0)
        descriptor = os.open(temporary_name, flags, 0o644, dir_fd=directory)
        try:
            with os.fdopen(descriptor, "wb", closefd=False) as stream:
                if hasattr(os, "fchmod"):
                    os.fchmod(descriptor, 0o644)
                stream.write(content)
                stream.flush()
                os.fsync(descriptor)
            try:
                os.link(
                    temporary_name,
                    name,
                    src_dir_fd=directory,
                    dst_dir_fd=directory,
                    follow_symlinks=False,
                )
            except FileExistsError as exc:
                raise AtomicWriteConflictError(f"concurrent_write: {name}") from exc
            os.fsync(directory)
        finally:
            try:
                os.unlink(temporary_name, dir_fd=directory)
            except FileNotFoundError:
                pass

    def _write_target(
        self,
        path: Path,
        content: bytes | None,
        *,
        expected: bytes | None,
        backup: Path,
    ) -> None:
        path, checked_backup = self._revalidate_mutation_paths(path, backup)
        if checked_backup is None:
            raise TransactionError(f"invalid_backup_path: {backup}")
        backup = checked_backup
        with self._mutation_directory(path, backup) as pinned:
            if pinned is not None:
                directory, target_name, backup_name = pinned
                if self._exists_at(directory, backup_name):
                    raise AtomicWriteConflictError(f"backup_exists: {backup}")
                if expected is None:
                    if self._exists_at(directory, target_name):
                        raise AtomicWriteConflictError(f"concurrent_write: {path}")
                else:
                    try:
                        os.rename(
                            target_name,
                            backup_name,
                            src_dir_fd=directory,
                            dst_dir_fd=directory,
                        )
                    except FileNotFoundError as exc:
                        raise AtomicWriteConflictError(f"concurrent_write: {path}") from exc
                    os.fsync(directory)
                    if self._read_at(directory, backup_name) != expected:
                        if not self._exists_at(directory, target_name):
                            os.rename(
                                backup_name,
                                target_name,
                                src_dir_fd=directory,
                                dst_dir_fd=directory,
                            )
                            os.fsync(directory)
                        raise AtomicWriteConflictError(f"concurrent_write: {path}")
                if content is not None:
                    self._install_exclusive_at(directory, target_name, content)
                return
        if backup.exists() or backup.is_symlink():
            raise AtomicWriteConflictError(f"backup_exists: {backup}")
        if expected is None:
            if path.exists() or path.is_symlink():
                raise AtomicWriteConflictError(f"concurrent_write: {path}")
        else:
            try:
                path, checked_backup = self._revalidate_mutation_paths(path, backup)
                if checked_backup is None:
                    raise TransactionError(f"invalid_backup_path: {backup}")
                backup = checked_backup
                os.replace(path, backup)
            except FileNotFoundError as exc:
                raise AtomicWriteConflictError(f"concurrent_write: {path}") from exc
            self._sync_directory(path.parent)
            if backup.read_bytes() != expected:
                if not path.exists() and not path.is_symlink():
                    path, checked_backup = self._revalidate_mutation_paths(path, backup)
                    if checked_backup is None:
                        raise TransactionError(f"invalid_backup_path: {backup}")
                    backup = checked_backup
                    os.replace(backup, path)
                    self._sync_directory(path.parent)
                raise AtomicWriteConflictError(f"concurrent_write: {path}")
        if content is not None:
            self._install_exclusive(path, content)

    def _backup_path(self, relative: str, target: Path) -> Path:
        backup = (self.project_root / relative).absolute()
        prefix = f".{target.name}.distill-review-"
        if (
            backup.parent != target.parent
            or not backup.name.startswith(prefix)
            or not backup.name.endswith(".bak")
            or backup.is_symlink()
        ):
            raise TransactionError(f"invalid_backup_path: {relative}")
        token = backup.name[len(prefix) : -4]
        parts = token.rsplit("-", 1)
        if len(parts) != 2 or len(parts[0]) != 16 or not all(c in "0123456789abcdef" for c in parts[0]):
            raise TransactionError(f"invalid_backup_path: {relative}")
        if not parts[1].isdigit():
            raise TransactionError(f"invalid_backup_path: {relative}")
        return backup

    @staticmethod
    def _rollback_path(backup: Path) -> Path:
        return backup.with_name(f"{backup.name}.rollback")

    def apply(self) -> dict[str, Any]:
        journal = self.prepare()
        journal["state"] = "applying"
        active_record_id: str | None = None
        try:
            self.store.save_transaction(journal)
            for change in journal["changes"]:
                active_record_id = change["record_id"]
                self._write_target(
                    self.project_root / change["path"],
                    _decoded(change["new"]),
                    expected=_decoded(change["old"]),
                    backup=self.project_root / change["backup"],
                )
                change["phase"] = "installed"
                self.store.save_transaction(journal)
            self._verify_installed(journal)
            journal["state"] = "committed"
            self.store.save_transaction(journal)
        except AtomicWriteConflictError as exc:
            try:
                self._restore(journal)
                self.store.discard_transaction()
            except (TransactionError, SessionError) as rollback_exc:
                raise TransactionError(
                    f"rollback_failed: {rollback_exc}",
                    records=getattr(rollback_exc, "records", []),
                    failures=getattr(rollback_exc, "failures", [str(rollback_exc)]),
                ) from exc
            record_id = active_record_id or "unknown"
            raise TransactionError(f"hash_conflict: {record_id}", records=[record_id]) from exc
        except Exception as exc:
            try:
                self._restore(journal)
                self.store.discard_transaction()
            except (TransactionError, SessionError) as rollback_exc:
                raise TransactionError(
                    f"rollback_failed: {rollback_exc}",
                    records=getattr(rollback_exc, "records", []),
                    failures=getattr(rollback_exc, "failures", [str(rollback_exc)]),
                ) from exc
            raise TransactionError(f"apply_failed: {exc}") from exc
        try:
            self._cleanup_backups(journal)
            self.store.discard()
            self.store.discard_transaction()
        except (OSError, SessionError, TransactionError):
            # The committed profile is authoritative. Keep the committed
            # journal so startup recovery can retry idempotent cleanup.
            return {"status": "applied", "cleanup_pending": True}
        return {"status": "applied"}

    def _verify_installed(self, journal: Mapping[str, Any]) -> None:
        conflicts: list[str] = []
        for change in journal["changes"]:
            path = self._confined_path(change["path"])
            backup = self._backup_path(change["backup"], path)
            old = _decoded(change["old"])
            new = _decoded(change["new"])
            current = path.read_bytes() if path.exists() else None
            saved = backup.read_bytes() if backup.exists() else None
            if current != new or (old is not None and saved != old) or (old is None and backup.exists()):
                conflicts.append(change["record_id"])
        if conflicts:
            raise AtomicWriteConflictError("concurrent_write: " + ",".join(sorted(set(conflicts))))

    def _cleanup_backups(self, journal: Mapping[str, Any]) -> None:
        for change in journal["changes"]:
            path = self._confined_path(change["path"])
            backup = self._backup_path(change["backup"], path)
            with self._mutation_directory(path, backup) as pinned:
                if pinned is not None:
                    directory, _, backup_name = pinned
                    self._unlink_at(directory, backup_name)
                    self._unlink_at(directory, f"{backup_name}.rollback")
                    continue
            backup.unlink(missing_ok=True)
            self._rollback_path(backup).unlink(missing_ok=True)
            self._sync_directory(path.parent)

    def _restore_at(
        self,
        directory: int,
        target_name: str,
        backup_name: str,
        *,
        old: bytes | None,
        new: bytes | None,
        phase: str,
    ) -> bool:
        """Restore one change through a pinned directory; return whether it conflicts."""
        current = self._read_optional_at(directory, target_name)
        saved = self._read_optional_at(directory, backup_name)
        rollback_name = f"{backup_name}.rollback"
        rolled_back = self._read_optional_at(directory, rollback_name)
        if rolled_back is not None:
            if rolled_back != new:
                return True
            if old is not None and saved == old and current is None:
                self._rename_at(directory, backup_name, target_name)
                self._unlink_at(directory, rollback_name)
                return False
            if old is not None and saved is None and current == old:
                self._unlink_at(directory, rollback_name)
                return False
            if old is None and current is None:
                self._unlink_at(directory, rollback_name)
                return False
            return True
        if old is not None and saved is not None:
            if saved != old:
                return True
            if current is None:
                self._rename_at(directory, backup_name, target_name)
            elif current == new:
                self._rename_at(directory, target_name, rollback_name)
                if self._read_at(directory, rollback_name) != new:
                    if not self._exists_at(directory, target_name):
                        self._rename_at(directory, rollback_name, target_name)
                    return True
                self._rename_at(directory, backup_name, target_name)
                self._unlink_at(directory, rollback_name)
            elif current == old:
                self._unlink_at(directory, backup_name)
            else:
                return True
        elif old is None:
            if saved is not None:
                return True
            if current == new:
                self._rename_at(directory, target_name, rollback_name)
                if self._read_at(directory, rollback_name) == new:
                    self._unlink_at(directory, rollback_name, missing_ok=False)
                else:
                    if not self._exists_at(directory, target_name):
                        self._rename_at(directory, rollback_name, target_name)
                    return True
            elif current is not None:
                return True
        elif phase != "pending" and current != old:
            return True
        return False

    def _restore(self, journal: Mapping[str, Any]) -> None:
        conflicts: list[str] = []
        for change in reversed(journal["changes"]):
            path = self._confined_path(change["path"])
            backup = self._backup_path(change["backup"], path)
            old = _decoded(change["old"])
            new = _decoded(change["new"])
            with self._mutation_directory(path, backup) as pinned:
                if pinned is not None:
                    directory, target_name, backup_name = pinned
                    if self._restore_at(
                        directory,
                        target_name,
                        backup_name,
                        old=old,
                        new=new,
                        phase=change.get("phase", "pending"),
                    ):
                        conflicts.append(change["record_id"])
                        continue
                    change["phase"] = "pending"
                    if self.store.transaction_exists():
                        self.store.save_transaction(journal)
                    continue
            current = path.read_bytes() if path.exists() else None
            saved = backup.read_bytes() if backup.exists() else None
            rollback = self._rollback_path(backup)
            if rollback.is_symlink():
                conflicts.append(change["record_id"])
                continue
            if rollback.exists():
                rolled_back = rollback.read_bytes()
                if rolled_back != new:
                    conflicts.append(change["record_id"])
                    continue
                if old is not None and saved == old and current is None:
                    os.replace(backup, path)
                    rollback.unlink(missing_ok=True)
                    self._sync_directory(path.parent)
                    change["phase"] = "pending"
                    continue
                if old is not None and not backup.exists() and current == old:
                    rollback.unlink(missing_ok=True)
                    self._sync_directory(path.parent)
                    change["phase"] = "pending"
                    continue
                if old is None and current is None:
                    rollback.unlink(missing_ok=True)
                    self._sync_directory(path.parent)
                    change["phase"] = "pending"
                    continue
                conflicts.append(change["record_id"])
                continue
            if old is not None and backup.exists():
                if saved != old:
                    conflicts.append(change["record_id"])
                    continue
                if current is None:
                    os.replace(backup, path)
                    self._sync_directory(path.parent)
                elif current == new:
                    os.replace(path, rollback)
                    self._sync_directory(path.parent)
                    if rollback.read_bytes() != new:
                        if not path.exists() and not path.is_symlink():
                            os.replace(rollback, path)
                            self._sync_directory(path.parent)
                        conflicts.append(change["record_id"])
                        continue
                    os.replace(backup, path)
                    rollback.unlink(missing_ok=True)
                    self._sync_directory(path.parent)
                elif current == old:
                    backup.unlink(missing_ok=True)
                else:
                    conflicts.append(change["record_id"])
                    continue
            elif old is None:
                if backup.exists():
                    conflicts.append(change["record_id"])
                    continue
                if current == new:
                    os.replace(path, rollback)
                    self._sync_directory(path.parent)
                    if rollback.read_bytes() == new:
                        rollback.unlink(missing_ok=False)
                        self._sync_directory(path.parent)
                    else:
                        if not path.exists() and not path.is_symlink():
                            os.replace(rollback, path)
                            self._sync_directory(path.parent)
                        conflicts.append(change["record_id"])
                        continue
                elif current is not None:
                    conflicts.append(change["record_id"])
                    continue
            elif change.get("phase") == "pending":
                # No backup means the old target was never moved. A concurrent
                # edit discovered at that boundary belongs to the other writer.
                continue
            elif current != old:
                conflicts.append(change["record_id"])
                continue
            change["phase"] = "pending"
            if self.store.transaction_exists():
                self.store.save_transaction(journal)
        if conflicts:
            raise TransactionError(
                "recovery_conflict: " + ",".join(sorted(set(conflicts))),
                records=sorted(set(conflicts)),
            )

    @classmethod
    def recover(cls, project_root: Path, store: SessionStore) -> None:
        try:
            source = store.load_transaction_bytes()
        except SessionError as exc:
            raise TransactionError(f"invalid_transaction_journal: {exc}") from exc
        if source is None:
            return
        try:
            journal = json.loads(source)
        except (OSError, json.JSONDecodeError) as exc:
            raise TransactionError(f"invalid_transaction_journal: {store.transaction_path}") from exc
        if not isinstance(journal, dict) or journal.get("schema_version") != 2:
            raise TransactionError("unsupported_transaction_journal")
        transaction = cls(project_root, {}, ReviewDraft(), store)
        try:
            transaction._validate_journal(journal)
        except (TransactionError, KeyError, TypeError, ValueError, UnicodeError) as exc:
            raise TransactionError(f"invalid_transaction_journal: {exc}") from exc
        if journal.get("state") == "committed":
            transaction._cleanup_backups(journal)
            store.discard()
            store.discard_transaction()
            return
        if journal.get("state") == "prepared":
            store.discard_transaction()
            return
        try:
            transaction._restore(journal)
        except TransactionError as exc:
            raise TransactionError(
                f"recovery_failed: {exc}",
                records=exc.records,
                failures=exc.failures,
            ) from exc
        except Exception as exc:
            raise TransactionError(f"recovery_failed: {exc}") from exc
        store.discard_transaction()

    def _validate_journal(self, journal: Mapping[str, Any]) -> None:
        if set(journal) != {"schema_version", "state", "changes"}:
            raise TransactionError("invalid_journal_shape")
        if journal.get("state") not in {"prepared", "applying", "committed"}:
            raise TransactionError("invalid_journal_state")
        changes = journal.get("changes")
        if not isinstance(changes, list):
            raise TransactionError("invalid_journal_changes")
        targets: set[str] = set()
        for change in changes:
            if not isinstance(change, dict) or set(change) != {
                "record_id",
                "path",
                "backup",
                "old",
                "new",
                "phase",
            }:
                raise TransactionError("invalid_journal_change")
            record_id = change.get("record_id")
            relative = change.get("path")
            if not isinstance(record_id, str) or not record_id or not isinstance(relative, str):
                raise TransactionError("invalid_journal_change")
            if relative in targets:
                raise TransactionError(f"duplicate_target: {relative}")
            targets.add(relative)
            target = self._confined_path(relative)
            backup = change.get("backup")
            if not isinstance(backup, str):
                raise TransactionError("invalid_journal_change")
            self._backup_path(backup, target)
            old = change.get("old")
            new = change.get("new")
            if change.get("phase") not in {"pending", "installed"}:
                raise TransactionError("invalid_journal_change")
            if old is not None and not isinstance(old, str):
                raise TransactionError("invalid_journal_content")
            if new is not None and not isinstance(new, str):
                raise TransactionError("invalid_journal_content")
            if old is None and new is None:
                raise TransactionError("invalid_journal_content")
            _decoded(old)
            _decoded(new)
