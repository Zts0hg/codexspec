import base64
import json
import os
import shutil
import subprocess
from contextlib import contextmanager
from pathlib import Path

import pytest

from codexspec.distill_review.domain import ReviewService
from codexspec.distill_review.lease import ActiveSessionError, ReviewLease
from codexspec.distill_review.models import ReviewDraft
from codexspec.distill_review.records import parse_record
from codexspec.distill_review.session import SessionError, SessionStore, atomic_bytes, ensure_runtime_ignored
from codexspec.distill_review.transaction import ProfileTransaction, TransactionError
from tests.automation_test_support import sanitized_git_env
from tests.test_distill_review_core import make_profile, record_text


def git(root: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(root), *args],
        check=True,
        capture_output=True,
        text=True,
        env=sanitized_git_env(),
    )
    return result.stdout.strip()


def test_session_round_trip_discard_and_corrupt_draft(tmp_path: Path) -> None:
    root = make_profile(tmp_path)
    store = SessionStore(root)
    draft = ReviewDraft(
        revision=2,
        decisions={"P-2026-0927-2310d6-1": {"action": "remove", "base_hash": "0" * 64}},
    )
    store.save(draft)
    assert store.load() == draft
    store.discard()
    assert store.load() is None
    store.draft_path.parent.mkdir(parents=True, exist_ok=True)
    store.draft_path.write_text("not-json", encoding="utf-8")
    with pytest.raises(SessionError, match="invalid_draft"):
        store.load()
    assert store.draft_path.read_text() == "not-json"


def test_atomic_bytes_tolerates_platform_without_fchmod(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delattr(os, "fchmod")
    target = tmp_path / "result.txt"
    atomic_bytes(target, b"portable")
    assert target.read_bytes() == b"portable"


def test_session_rejects_runtime_symlink_outside_project(tmp_path: Path) -> None:
    root = make_profile(tmp_path)
    outside = tmp_path / "outside"
    outside.mkdir()
    runtime = root / ".codexspec/.runtime"
    runtime.symlink_to(outside, target_is_directory=True)
    store = SessionStore(root)
    with pytest.raises(SessionError, match="runtime_symlink"):
        store.save(ReviewDraft())
    assert not (outside / "distill-review/draft.json").exists()


def test_session_rejects_runtime_symlink_swap_without_external_write(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = make_profile(tmp_path)
    store = SessionStore(root)
    external = tmp_path / "external-runtime"
    external.mkdir()
    external_draft = external / "draft.json"
    external_draft.write_text("must survive", encoding="utf-8")
    real_prepare = store.prepare

    def prepare_then_swap() -> None:
        real_prepare()
        moved = store.runtime_dir.with_name("distill-review-original")
        if not store.runtime_dir.is_symlink():
            store.runtime_dir.rename(moved)
            try:
                store.runtime_dir.symlink_to(external, target_is_directory=True)
            except OSError:
                pytest.skip("directory symlink creation is unavailable")

    monkeypatch.setattr(store, "prepare", prepare_then_swap)
    with pytest.raises(SessionError, match="runtime_symlink"):
        store.save(ReviewDraft(revision=7))
    assert external_draft.read_text(encoding="utf-8") == "must survive"


def test_session_rejects_runtime_directory_identity_swap(tmp_path: Path) -> None:
    root = make_profile(tmp_path)
    store = SessionStore(root)
    store.prepare()
    moved = store.runtime_dir.with_name("distill-review-original")
    store.runtime_dir.rename(moved)
    store.runtime_dir.mkdir()

    with pytest.raises(SessionError, match="runtime_replaced"):
        store.save(ReviewDraft(revision=8))
    assert not (store.runtime_dir / "draft.json").exists()


def test_draft_rejects_incomplete_action_payload() -> None:
    with pytest.raises(ValueError, match="invalid_draft_decision"):
        ReviewDraft.from_dict(
            {
                "schema_version": 1,
                "revision": 1,
                "decisions": {"cluster:broken": {"action": "merge"}},
                "deferred": [],
            }
        )


def test_legacy_git_project_uses_local_exclude_without_dirtying_tree(tmp_path: Path) -> None:
    root = make_profile(tmp_path)
    git(root, "init")
    git(root, "config", "user.email", "test@example.com")
    git(root, "config", "user.name", "Test")
    git(root, "add", ".")
    git(root, "commit", "-m", "initial")
    before = git(root, "status", "--short")
    ensure_runtime_ignored(root, install_managed_file=False)
    SessionStore(root).save(ReviewDraft(revision=1))
    assert git(root, "status", "--short") == before
    exclude = Path(git(root, "rev-parse", "--git-path", "info/exclude"))
    if not exclude.is_absolute():
        exclude = root / exclude
    assert "/.codexspec/.runtime/" in exclude.read_text(encoding="utf-8")


def test_init_mode_creates_idempotent_codexspec_gitignore(tmp_path: Path) -> None:
    root = tmp_path / "project"
    ensure_runtime_ignored(root, install_managed_file=True)
    ensure_runtime_ignored(root, install_managed_file=True)
    content = (root / ".codexspec/.gitignore").read_text(encoding="utf-8")
    assert content.count(".runtime/") == 1


def test_review_lease_allows_one_writer_and_recovers_stale_metadata(tmp_path: Path) -> None:
    root = make_profile(tmp_path)
    first = ReviewLease(root)
    first.acquire({"port": 1234, "capability": "secret"})
    second = ReviewLease(root)
    with pytest.raises(ActiveSessionError) as error:
        second.acquire({"port": 5678, "capability": "other"})
    assert error.value.metadata["port"] == 1234
    first.release()
    second.acquire({"port": 5678, "capability": "other"})
    second.release()


def test_transaction_applies_mixed_batch_and_detects_hash_conflict(tmp_path: Path) -> None:
    root = make_profile(tmp_path)
    service = ReviewService.from_project(root)
    record_id = "P-2026-0927-2310d6-1"
    service.stage({"action": "replace", "record_id": record_id, "fields": {"claim": "Changed"}})
    store = SessionStore(root)
    store.save(service.draft)
    transaction = ProfileTransaction(root, service.records, service.draft, store)
    result = transaction.apply()
    assert result["status"] == "applied"
    assert "- claim: Changed" in next((root / ".codexspec/profile/pitfalls").glob("*.md")).read_text()
    assert store.load() is None

    service = ReviewService.from_project(root)
    service.stage({"action": "remove", "record_id": record_id})
    target = next((root / ".codexspec/profile/pitfalls").glob("*.md"))
    target.write_text(target.read_text() + "\nchanged concurrently\n")
    with pytest.raises(TransactionError, match="hash_conflict"):
        ProfileTransaction(root, service.records, service.draft, SessionStore(root)).apply()
    assert target.exists()


def test_transaction_rechecks_content_at_write_boundary(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    root = make_profile(tmp_path)
    service = ReviewService.from_project(root)
    record_id = "P-2026-0927-2310d6-1"
    service.stage({"action": "replace", "record_id": record_id, "fields": {"claim": "Review edit"}})
    target = service.records[record_id].path
    transaction = ProfileTransaction(root, service.records, service.draft, SessionStore(root))
    real_write = transaction._write_target

    def concurrent_write(path: Path, content: bytes | None, *args, **kwargs) -> None:
        path.write_text(record_text(record_id).replace("Original claim", "Concurrent claim"), encoding="utf-8")
        real_write(path, content, *args, **kwargs)

    from tests.test_distill_review_core import record_text

    monkeypatch.setattr(transaction, "_write_target", concurrent_write)
    with pytest.raises(TransactionError, match="conflict"):
        transaction.apply()
    assert "Concurrent claim" in target.read_text(encoding="utf-8")


def test_transaction_rejects_category_symlink_swap_without_external_write(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = make_profile(tmp_path)
    service = ReviewService.from_project(root)
    record_id = "P-2026-0927-2310d6-1"
    service.stage({"action": "replace", "record_id": record_id, "fields": {"claim": "Review edit"}})
    transaction = ProfileTransaction(root, service.records, service.draft, SessionStore(root))
    category = root / ".codexspec/profile/pitfalls"
    moved_category = category.with_name("pitfalls-original")
    external = tmp_path / "external"
    external.mkdir()
    external_target = external / service.records[record_id].path.name
    original = service.records[record_id].source
    external_target.write_bytes(original)
    real_prepare = transaction.prepare

    def prepare_then_swap() -> dict:
        journal = real_prepare()
        category.rename(moved_category)
        try:
            category.symlink_to(external, target_is_directory=True)
        except OSError:
            pytest.skip("directory symlink creation is unavailable")
        return journal

    monkeypatch.setattr(transaction, "prepare", prepare_then_swap)
    with pytest.raises(TransactionError, match="symlink_target|rollback_failed"):
        transaction.apply()
    assert external_target.read_bytes() == original


def test_transaction_rejects_codexspec_ancestor_symlink_swap_without_external_write(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = make_profile(tmp_path)
    service = ReviewService.from_project(root)
    record_id = "P-2026-0927-2310d6-1"
    service.stage({"action": "replace", "record_id": record_id, "fields": {"claim": "Review edit"}})
    transaction = ProfileTransaction(root, service.records, service.draft, SessionStore(root))
    codexspec = root / ".codexspec"
    moved_codexspec = root / ".codexspec-original"
    external = tmp_path / "external-codexspec"
    external_target = external / "profile/pitfalls" / service.records[record_id].path.name
    original = service.records[record_id].source
    external_target.parent.mkdir(parents=True)
    external_target.write_bytes(original)
    real_prepare = transaction.prepare

    def prepare_then_swap() -> dict:
        journal = real_prepare()
        codexspec.rename(moved_codexspec)
        try:
            codexspec.symlink_to(external, target_is_directory=True)
        except OSError:
            pytest.skip("directory symlink creation is unavailable")
        return journal

    monkeypatch.setattr(transaction, "prepare", prepare_then_swap)
    with pytest.raises(TransactionError, match="symlink_target|rollback_failed"):
        transaction.apply()
    assert external_target.read_bytes() == original


def test_transaction_rederives_stale_draft_before_apply(tmp_path: Path) -> None:
    root = make_profile(tmp_path, verified=True)
    service = ReviewService.from_project(root)
    record_id = "P-2026-0927-2310d6-1"
    service.stage({"action": "vet", "record_id": record_id})
    saved = ReviewDraft.from_dict(service.draft.to_dict())
    saved.decisions[record_id]["rendered"] = saved.decisions[record_id]["rendered"].replace(
        "- provenance: distill", "- provenance: FORGED PROVENANCE"
    )
    target = service.records[record_id].path
    original = target.read_bytes()
    target.write_bytes(original.replace(b"Original claim", b"Temporary claim"))
    resumed = ReviewService.from_project(root, draft=saved)
    target.write_bytes(original)

    with pytest.raises(TransactionError, match="invalid_draft_semantics"):
        ProfileTransaction(root, resumed.records, resumed.draft, SessionStore(root)).apply()
    assert b"FORGED PROVENANCE" not in target.read_bytes()


def test_transaction_preserves_edit_injected_at_atomic_move_boundary(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = make_profile(tmp_path)
    service = ReviewService.from_project(root)
    record_id = "P-2026-0927-2310d6-1"
    service.stage({"action": "replace", "record_id": record_id, "fields": {"claim": "Review edit"}})
    target = service.records[record_id].path
    concurrent = target.read_text().replace("Original claim", "Boundary edit").encode()
    injected = False

    real_move = os.replace if os.name == "nt" else os.rename

    def move_with_boundary_edit(source, destination, **kwargs) -> None:
        nonlocal injected
        if Path(source).name == target.name and ".distill-review-" in Path(destination).name and not injected:
            target.write_bytes(concurrent)
            injected = True
        real_move(source, destination, **kwargs)

    monkeypatch.setattr(os, "replace" if os.name == "nt" else "rename", move_with_boundary_edit)
    with pytest.raises(TransactionError, match="conflict"):
        ProfileTransaction(root, service.records, service.draft, SessionStore(root)).apply()
    assert target.read_bytes() == concurrent


def test_recovery_detects_third_party_edit_when_phase_marker_was_not_durable(tmp_path: Path) -> None:
    root = make_profile(tmp_path)
    service = ReviewService.from_project(root)
    record_id = "P-2026-0927-2310d6-1"
    service.stage({"action": "replace", "record_id": record_id, "fields": {"claim": "Review edit"}})
    store = SessionStore(root)
    transaction = ProfileTransaction(root, service.records, service.draft, store)
    journal = transaction.prepare()
    journal["state"] = "applying"
    store.transaction_path.write_text(json.dumps(journal), encoding="utf-8")
    change = journal["changes"][0]
    target = root / change["path"]
    transaction._write_target(
        target,
        base64.b64decode(change["new"]),
        expected=base64.b64decode(change["old"]),
        backup=root / change["backup"],
    )
    target.write_text(target.read_text().replace("Review edit", "Third-party edit"), encoding="utf-8")
    with pytest.raises(TransactionError, match="recovery_conflict"):
        ProfileTransaction.recover(root, store)
    assert "Third-party edit" in target.read_text(encoding="utf-8")
    assert store.transaction_path.exists()


@pytest.mark.parametrize("artifact", ["backup", "rollback"])
@pytest.mark.parametrize("path_fallback", [False, True])
def test_recovery_never_installs_mismatched_recovery_artifact(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    artifact: str,
    path_fallback: bool,
) -> None:
    root = make_profile(tmp_path)
    service = ReviewService.from_project(root)
    record_id = "P-2026-0927-2310d6-1"
    service.stage({"action": "replace", "record_id": record_id, "fields": {"claim": "Review edit"}})
    store = SessionStore(root)
    transaction = ProfileTransaction(root, service.records, service.draft, store)
    journal = transaction.prepare()
    journal["state"] = "applying"
    change = journal["changes"][0]
    target = root / change["path"]
    backup = root / change["backup"]
    new = base64.b64decode(change["new"])
    transaction._write_target(target, new, expected=base64.b64decode(change["old"]), backup=backup)
    change["phase"] = "installed"
    store.save_transaction(journal)
    corrupted = b"CORRUPTED RECOVERY ARTIFACT"
    if artifact == "backup":
        backup.write_bytes(corrupted)
    else:
        rollback = transaction._rollback_path(backup)
        target.rename(rollback)
        rollback.write_bytes(corrupted)

    if path_fallback:

        @contextmanager
        def unpinned(path: Path, backup_path: Path):
            yield None

        monkeypatch.setattr(transaction, "_mutation_directory", unpinned)

    with pytest.raises(TransactionError, match="recovery_conflict"):
        transaction._restore(journal)
    if artifact == "backup":
        assert target.read_bytes() == new
        assert backup.read_bytes() == corrupted
    else:
        assert not target.exists()
        assert transaction._rollback_path(backup).read_bytes() == corrupted


def test_prepared_recovery_preserves_later_external_edit(tmp_path: Path) -> None:
    root = make_profile(tmp_path)
    service = ReviewService.from_project(root)
    record_id = "P-2026-0927-2310d6-1"
    service.stage({"action": "remove", "record_id": record_id})
    store = SessionStore(root)
    ProfileTransaction(root, service.records, service.draft, store).prepare()
    target = service.records[record_id].path
    target.write_text(target.read_text().replace("Original claim", "Concurrent claim"), encoding="utf-8")
    ProfileTransaction.recover(root, store)
    assert "Concurrent claim" in target.read_text(encoding="utf-8")
    assert not store.transaction_path.exists()


def test_applying_recovery_reports_and_preserves_third_party_content(tmp_path: Path) -> None:
    root = make_profile(tmp_path)
    service = ReviewService.from_project(root)
    record_id = "P-2026-0927-2310d6-1"
    service.stage({"action": "replace", "record_id": record_id, "fields": {"claim": "Review edit"}})
    store = SessionStore(root)
    transaction = ProfileTransaction(root, service.records, service.draft, store)
    journal = transaction.prepare()
    journal["state"] = "applying"
    journal["changes"][0]["phase"] = "installed"
    store.transaction_path.write_text(json.dumps(journal), encoding="utf-8")
    target = service.records[record_id].path
    target.write_text(target.read_text().replace("Original claim", "Third-party claim"), encoding="utf-8")
    with pytest.raises(TransactionError, match="recovery_conflict") as error:
        ProfileTransaction.recover(root, store)
    assert error.value.records == [record_id]
    assert "Third-party claim" in target.read_text(encoding="utf-8")
    assert store.transaction_path.exists()


def test_transaction_reports_every_hash_conflict(tmp_path: Path) -> None:
    root = make_profile(tmp_path)
    original = next((root / ".codexspec/profile/pitfalls").glob("*.md"))
    second = original.with_name("P-2026-0927-2310d6-2.md")
    second.write_text(original.read_text().replace("P-2026-0927-2310d6-1", "P-2026-0927-2310d6-2"))
    service = ReviewService.from_project(root)
    for record_id in sorted(service.records):
        service.stage({"action": "remove", "record_id": record_id})
    original.write_text(original.read_text() + "\nfirst conflict\n")
    second.write_text(second.read_text() + "\nsecond conflict\n")
    with pytest.raises(TransactionError) as error:
        ProfileTransaction(root, service.records, service.draft, SessionStore(root)).apply()
    assert set(error.value.records) == {"P-2026-0927-2310d6-1", "P-2026-0927-2310d6-2"}
    assert original.exists() and second.exists()


def test_transaction_rolls_back_and_recovery_restores_old_bytes(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = make_profile(tmp_path)
    service = ReviewService.from_project(root)
    record_id = "P-2026-0927-2310d6-1"
    service.stage({"action": "replace", "record_id": record_id, "fields": {"claim": "Changed"}})
    store = SessionStore(root)
    store.save(service.draft)
    transaction = ProfileTransaction(root, service.records, service.draft, store)
    old = service.records[record_id].source
    real_write = transaction._write_target

    calls = 0

    def fail_after_write(path: Path, content: bytes | None, *args, **kwargs) -> None:
        nonlocal calls
        calls += 1
        real_write(path, content, *args, **kwargs)
        if calls == 1:
            raise OSError("injected")

    monkeypatch.setattr(transaction, "_write_target", fail_after_write)
    with pytest.raises(TransactionError, match="apply_failed"):
        transaction.apply()
    assert service.records[record_id].path.read_bytes() == old

    # Simulate a crash after a target changed but before normal rollback.
    transaction.prepare()
    journal = json.loads(store.transaction_path.read_text())
    journal["state"] = "applying"
    change = journal["changes"][0]
    target = root / change["path"]
    transaction._write_target(
        target,
        base64.b64decode(change["new"]),
        expected=base64.b64decode(change["old"]),
        backup=root / change["backup"],
    )
    store.transaction_path.write_text(json.dumps(journal), encoding="utf-8")
    ProfileTransaction.recover(root, store)
    assert target.read_bytes() == old
    assert not store.transaction_path.exists()


def test_committed_cleanup_failure_reports_success_and_is_retried(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = make_profile(tmp_path)
    service = ReviewService.from_project(root)
    record_id = "P-2026-0927-2310d6-1"
    service.stage({"action": "replace", "record_id": record_id, "fields": {"claim": "Committed"}})
    store = SessionStore(root)
    transaction = ProfileTransaction(root, service.records, service.draft, store)
    real_cleanup = transaction._cleanup_backups
    monkeypatch.setattr(transaction, "_cleanup_backups", lambda journal: (_ for _ in ()).throw(OSError("busy")))
    result = transaction.apply()
    assert result == {"status": "applied", "cleanup_pending": True}
    assert "Committed" in service.records[record_id].path.read_text(encoding="utf-8")
    assert json.loads(store.transaction_path.read_text())["state"] == "committed"
    monkeypatch.setattr(transaction, "_cleanup_backups", real_cleanup)
    ProfileTransaction.recover(root, store)
    assert not store.transaction_path.exists()


def test_recovery_rejects_journal_path_escape_without_touching_external_file(tmp_path: Path) -> None:
    root = make_profile(tmp_path)
    store = SessionStore(root)
    store.prepare()
    outside = tmp_path / "outside.txt"
    outside.write_text("must survive", encoding="utf-8")
    store.transaction_path.write_text(
        json.dumps(
            {
                "schema_version": 2,
                "state": "applying",
                "changes": [
                    {
                        "record_id": "evil",
                        "path": "../outside.txt",
                        "backup": "../outside.txt.distill-review-0000000000000000-0.bak",
                        "old": None,
                        "new": base64.b64encode(b"evil").decode(),
                        "phase": "pending",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    with pytest.raises(TransactionError, match="invalid_transaction_journal"):
        ProfileTransaction.recover(root, store)
    assert outside.read_text(encoding="utf-8") == "must survive"


def test_recovery_rejects_category_symlink_swap_without_external_write(tmp_path: Path) -> None:
    root = make_profile(tmp_path)
    service = ReviewService.from_project(root)
    record_id = "P-2026-0927-2310d6-1"
    service.stage({"action": "remove", "record_id": record_id})
    store = SessionStore(root)
    ProfileTransaction(root, service.records, service.draft, store).prepare()
    category = root / ".codexspec/profile/pitfalls"
    moved_category = category.with_name("pitfalls-original")
    external = tmp_path / "external-recovery"
    external.mkdir()
    external_target = external / service.records[record_id].path.name
    original = service.records[record_id].source
    external_target.write_bytes(original)
    category.rename(moved_category)
    try:
        category.symlink_to(external, target_is_directory=True)
    except OSError:
        pytest.skip("directory symlink creation is unavailable")

    with pytest.raises(TransactionError, match="invalid_transaction_journal.*(?:symlink_target|runtime_symlink)"):
        ProfileTransaction.recover(root, store)
    assert external_target.read_bytes() == original
    assert store.transaction_path.exists()


def test_recovery_rejects_codexspec_ancestor_symlink_without_external_write(tmp_path: Path) -> None:
    root = make_profile(tmp_path)
    service = ReviewService.from_project(root)
    record_id = "P-2026-0927-2310d6-1"
    service.stage({"action": "remove", "record_id": record_id})
    store = SessionStore(root)
    ProfileTransaction(root, service.records, service.draft, store).prepare()
    codexspec = root / ".codexspec"
    moved_codexspec = root / ".codexspec-original"
    external = tmp_path / "external-recovery-codexspec"
    shutil.copytree(codexspec, external)
    external_target = external / "profile/pitfalls" / service.records[record_id].path.name
    original = external_target.read_bytes()
    codexspec.rename(moved_codexspec)
    try:
        codexspec.symlink_to(external, target_is_directory=True)
    except OSError:
        pytest.skip("directory symlink creation is unavailable")

    with pytest.raises(TransactionError, match="invalid_transaction_journal.*(?:symlink_target|runtime_symlink)"):
        ProfileTransaction.recover(root, store)
    assert external_target.read_bytes() == original
    assert store.transaction_path.exists()


def test_transaction_aggregates_multiple_schema_failures(tmp_path: Path) -> None:
    root = make_profile(tmp_path)
    original = next((root / ".codexspec/profile/pitfalls").glob("*.md"))
    second = original.with_name("P-2026-0927-2310d6-2.md")
    second.write_text(original.read_text().replace("P-2026-0927-2310d6-1", "P-2026-0927-2310d6-2"))
    service = ReviewService.from_project(root)
    for record_id in sorted(service.records):
        service.stage({"action": "replace", "record_id": record_id, "fields": {"claim": "valid first"}})
        service.draft.decisions[record_id]["rendered"] = service.draft.decisions[record_id]["rendered"].replace(
            "- claim: valid first\n", ""
        )
    with pytest.raises(TransactionError) as error:
        ProfileTransaction(root, service.records, service.draft, SessionStore(root)).prepare()
    assert set(error.value.records) == set(service.records)
    assert len(error.value.failures) == 2


def _clustered_pitfall(record_id: str, cluster: str) -> str:
    return (
        f"### {record_id}: Preserve unknown content\n\n"
        "- claim: Original claim\n"
        "- type: pitfall\n"
        "- scope/when: editing profile records\n"
        "- root-cause: A parser can discard unfamiliar Markdown.\n"
        "- workaround: Preserve source spans.\n"
        "- lesson: Render only fields the user changed.\n"
        '- evidence.facts: "observed fact"\n'
        "- evidence.state: full suite passed; still valid\n"
        f"- consolidation: candidate; cluster: {cluster}\n"
        "- provenance: distill @implement-tasks, 2026-09-28, derivation: inferred\n"
        "- status: candidate\n"
    )


def _strategy(record_id: str) -> str:
    return (
        f"### {record_id}: Generalized strategy\n\n"
        "- claim: Promote the shared lesson into a strategy.\n"
        "- type: strategy\n"
        "- scope/when: reviewing profile records\n"
        "- trigger: the same pitfall recurs\n"
        "- action: apply the generalized rule\n"
        '- evidence.facts: "observed fact"\n'
        "- evidence.state: full suite passed; still valid\n"
        "- provenance: distill @implement-tasks, 2026-09-28, derivation: inferred\n"
        "- status: candidate\n"
    )


def _cross_category_merge(tmp_path: Path) -> tuple[Path, ReviewService, SessionStore]:
    """A profile with only `pitfalls/`, and a staged merge promoting them into a strategy."""
    root = (tmp_path.resolve()) / "project"
    pitfalls = root / ".codexspec/profile/pitfalls"
    pitfalls.mkdir(parents=True)
    members = ["P-2026-0927-2310d6-1", "P-2026-0927-2310d6-2"]
    for member in members:
        (pitfalls / f"{member}.md").write_text(_clustered_pitfall(member, "parser-loss"), encoding="utf-8")
    output = "S-2026-0927-2310d6-9"
    manifest = root / "consolidation.json"
    manifest.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "proposals": {},
                "consolidations": [
                    {
                        "cluster": "parser-loss",
                        "members": members,
                        "member_hashes": {
                            member: parse_record(pitfalls / f"{member}.md", root).sha256 for member in members
                        },
                        "category": "strategies",
                        "record_id": output,
                        "filename": f"{output}.md",
                        "markdown": _strategy(output),
                        "fields": {"claim": "Promote the shared lesson into a strategy."},
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    service = ReviewService.from_project(root, manifest_path=manifest)
    service.stage(
        {
            "action": "merge",
            "cluster": "parser-loss",
            "field_changes": {"claim": "Promote the shared lesson into a strategy."},
            "status": "candidate",
        }
    )
    store = SessionStore(root)
    store.save(service.draft)
    return root, service, store


def test_merge_creates_a_category_directory_that_does_not_exist_yet(tmp_path: Path) -> None:
    """The profile creates a category directory on first write, so a cross-category
    promotion must not require the directory to exist already."""
    root, service, store = _cross_category_merge(tmp_path)
    assert not (root / ".codexspec/profile/strategies").exists()
    result = ProfileTransaction(service.project_root, service.records, service.draft, store).apply()
    assert result["status"] == "applied"
    written = root / ".codexspec/profile/strategies/S-2026-0927-2310d6-9.md"
    assert written.is_file()
    assert not (root / ".codexspec/profile/pitfalls/P-2026-0927-2310d6-1.md").exists()
    assert not store.transaction_exists()


def test_a_missing_target_directory_never_leaves_an_unrecoverable_journal(tmp_path: Path) -> None:
    """A directory that disappears mid-flight must abort cleanly and clear the journal,
    not report a symlink attack and refuse every later session."""
    root, service, store = _cross_category_merge(tmp_path)
    transaction = ProfileTransaction(service.project_root, service.records, service.draft, store)
    original = ProfileTransaction._write_target

    def vanish(self, path, new, *, expected, backup):  # type: ignore[no-untyped-def]
        if path.parent.name == "strategies":
            shutil.rmtree(path.parent)
        return original(self, path, new, expected=expected, backup=backup)

    ProfileTransaction._write_target = vanish  # type: ignore[method-assign]
    try:
        with pytest.raises(TransactionError) as failure:
            transaction.apply()
    finally:
        ProfileTransaction._write_target = original  # type: ignore[method-assign]
    assert "symlink_target" not in str(failure.value)
    assert "rollback_failed" not in str(failure.value)
    assert not store.transaction_exists(), "a failed batch left a journal that blocks every later session"
    for member in ("P-2026-0927-2310d6-1", "P-2026-0927-2310d6-2"):
        assert (root / f".codexspec/profile/pitfalls/{member}.md").is_file()
    ProfileTransaction.recover(root, SessionStore(root))


def test_recovery_resolves_changes_in_a_vanished_directory(tmp_path: Path) -> None:
    """A category directory that disappeared while a batch was in flight holds no
    user bytes: for a created record there is nothing to put back, and for a
    replaced record its old bytes and the backup lived in that same directory.
    Recovery must resolve such a change instead of failing forever. (S001.15)"""
    root = make_profile(tmp_path)
    record_path = root / ".codexspec/profile/pitfalls/P-2026-0927-2310d6-1-preserve-unknown.md"
    old_b64 = base64.b64encode(record_path.read_bytes()).decode()
    new_b64 = base64.b64encode(record_path.read_bytes().replace(b"Original claim", b"New claim")).decode()
    store = SessionStore(root)
    store.prepare()
    store.save_transaction(
        {
            "schema_version": 2,
            "state": "applying",
            "changes": [
                {
                    "record_id": "P-2026-0927-2310d6-1",
                    "path": ".codexspec/profile/pitfalls/P-2026-0927-2310d6-1-preserve-unknown.md",
                    "backup": (
                        ".codexspec/profile/pitfalls/"
                        ".P-2026-0927-2310d6-1-preserve-unknown.md.distill-review-" + "0" * 16 + "-1.bak"
                    ),
                    "old": old_b64,
                    "new": new_b64,
                    "phase": "installed",
                }
            ],
        }
    )
    shutil.rmtree(record_path.parent)
    # Recovery resolves the change instead of failing forever on the absent directory.
    ProfileTransaction.recover(root, SessionStore(root))
    assert not SessionStore(root).transaction_exists()


def test_runtime_ignore_covers_a_nested_project_root(tmp_path: Path) -> None:
    """A project living inside a larger repository must still have its review runtime
    excluded: the info/exclude rule has to be anchored at the project, not the
    repository root. (S001.16)"""
    outer = tmp_path / "repo"
    outer.mkdir()
    subprocess.run(["git", "-C", str(outer), "init"], check=True, capture_output=True)
    root = outer / "deep" / "nested" / "project"
    profile = root / ".codexspec/profile/pitfalls"
    profile.mkdir(parents=True)
    (profile / "P-2026-1002-2205zz-1.md").write_text(record_text(), encoding="utf-8")
    ensure_runtime_ignored(root, install_managed_file=False)
    SessionStore(root).save(ReviewDraft(revision=1))
    probe = subprocess.run(
        ["git", "-C", str(root), "check-ignore", "-q", ".codexspec/.runtime/draft.json"],
        capture_output=True,
    )
    assert probe.returncode == 0, "runtime state must be git-excluded for a nested project"
    exclude = Path(git(root, "rev-parse", "--git-path", "info/exclude"))
    if not exclude.is_absolute():
        exclude = root / exclude
    assert "deep/nested/project/.codexspec/.runtime/" in exclude.read_text(encoding="utf-8")


def test_whitespace_only_verification_stages_and_applies_like_an_absent_one(tmp_path: Path) -> None:
    """Stage time normalizes a whitespace-only attestation to absent when rendering, so
    apply time must re-render from the same normalized value. Storing the raw string made
    the interface present a decision as accepted that the batch then refused. (S001.17)"""
    root = make_profile(tmp_path)
    record_id = "P-2026-0927-2310d6-1"
    service = ReviewService.from_project(root)
    service.stage({"action": "replace", "record_id": record_id, "verification": "   "})
    assert service.draft.decisions[record_id]["verification"] == "", (
        "the stored attestation must be the normalized value, not the raw whitespace"
    )
    store = SessionStore(root)
    store.prepare()
    result = ProfileTransaction(root, service.records, service.draft, store).apply()
    assert result["status"] == "applied"
