"""Tests for atomic blueprint mutation commits."""

import base64
import json
import os
from pathlib import Path

import pytest

from codexspec.automation import (
    AutoDevOwnership,
    AutomationError,
    BlueprintStore,
    ensure_dedicated_workspace,
    locate_repository,
)
from codexspec.blueprint import BlueprintDocument, blueprint_hash
from tests.automation_test_support import git, make_repo
from tests.test_blueprint import FEATURE_ID, block, request, unmanaged_requirements


def append_request(expected_hash: str) -> bytes:
    return json.dumps(
        {
            "protocol_version": "1",
            "operation": "append_requirement",
            "expected_blueprint_hash": expected_hash,
            "payload": {
                "feature_name": "user-authentication",
                "requirements_markdown": unmanaged_requirements(),
            },
        }
    ).encode()


def _apply_with_analysis(store, request_bytes, **kwargs):
    prepared = store.prepare(request_bytes, **kwargs)
    if prepared.get("state") != "prepared":
        return prepared
    return store.apply_and_commit(
        prepared["preparation_id"],
        prepared["tree"],
        "docs(blueprint): update confirmed requirements\n\nRecord the staged blueprint changes.\n",
        owner_token=kwargs.get("owner_token"),
    )


def test_store_commits_only_blueprint_and_preserves_unrelated_index(tmp_path: Path) -> None:
    repo = make_repo(tmp_path / "project")
    workspace = ensure_dedicated_workspace(locate_repository(repo))
    (workspace.path / "staged.txt").write_text("staged\n")
    git(workspace.path, "add", "staged.txt")
    store = BlueprintStore(workspace)
    response = _apply_with_analysis(store, append_request(blueprint_hash(b"")), feature_id_factory=lambda: FEATURE_ID)
    assert response["result"] == "applied"
    changed = git(workspace.path, "show", "--name-only", "--pretty=format:", "HEAD").stdout.splitlines()
    assert changed == [".codexspec/blueprint.md"]
    assert git(workspace.path, "diff", "--cached", "--name-only").stdout.strip() == "staged.txt"


def test_store_returns_conflict_for_stale_request_without_commit(tmp_path: Path) -> None:
    repo = make_repo(tmp_path / "project")
    workspace = ensure_dedicated_workspace(locate_repository(repo))
    store = BlueprintStore(workspace)
    first = _apply_with_analysis(store, append_request(blueprint_hash(b"")), feature_id_factory=lambda: FEATURE_ID)
    head = git(workspace.path, "rev-parse", "HEAD").stdout.strip()
    second = _apply_with_analysis(store, append_request(blueprint_hash(b"")))
    assert first["result"] == "applied"
    assert second["result"] == "conflict"
    assert git(workspace.path, "rev-parse", "HEAD").stdout.strip() == head


def test_store_recovers_replacement_interrupted_before_commit(tmp_path: Path) -> None:
    repo = make_repo(tmp_path / "project")
    workspace = ensure_dedicated_workspace(locate_repository(repo))
    store = BlueprintStore(workspace)
    old = b""
    replacement = block().encode()
    pre_head = git(workspace.path, "rev-parse", "HEAD").stdout.strip()
    workspace.blueprint_path.parent.mkdir(parents=True)
    workspace.blueprint_path.write_bytes(replacement)
    store.recovery_path.parent.mkdir(parents=True, exist_ok=True)
    store.recovery_path.write_text(
        json.dumps(
            {
                "old_content": base64.b64encode(old).decode(),
                "old_hash": blueprint_hash(old),
                "new_hash": blueprint_hash(replacement),
                "pre_head": pre_head,
                "operation": "append_requirement",
                "feature_id": FEATURE_ID,
            }
        )
    )
    _apply_with_analysis(store, append_request(blueprint_hash(old)), feature_id_factory=lambda: FEATURE_ID)
    assert not store.recovery_path.exists()
    assert workspace.blueprint_path.exists()


def test_store_recognizes_commit_interrupted_before_record_cleanup(tmp_path: Path) -> None:
    repo = make_repo(tmp_path / "project")
    workspace = ensure_dedicated_workspace(locate_repository(repo))
    store = BlueprintStore(workspace)
    old = b""
    replacement = block().encode()
    pre_head = git(workspace.path, "rev-parse", "HEAD").stdout.strip()
    workspace.blueprint_path.parent.mkdir(parents=True)
    workspace.blueprint_path.write_bytes(replacement)
    git(workspace.path, "add", ".codexspec/blueprint.md")
    git(workspace.path, "commit", "-m", "docs(blueprint): append requirement")
    store.recovery_path.parent.mkdir(parents=True, exist_ok=True)
    store.recovery_path.write_text(
        json.dumps(
            {
                "old_content": base64.b64encode(old).decode(),
                "old_hash": blueprint_hash(old),
                "new_hash": blueprint_hash(replacement),
                "pre_head": pre_head,
                "operation": "append_requirement",
                "feature_id": FEATURE_ID,
            }
        )
    )
    stale = _apply_with_analysis(store, append_request(blueprint_hash(old)))
    assert stale["result"] == "conflict"
    assert workspace.blueprint_path.read_bytes() == replacement
    assert not store.recovery_path.exists()


def test_store_fails_closed_for_unknown_recovery_state(tmp_path: Path) -> None:
    repo = make_repo(tmp_path / "project")
    workspace = ensure_dedicated_workspace(locate_repository(repo))
    store = BlueprintStore(workspace)
    pre_head = git(workspace.path, "rev-parse", "HEAD").stdout.strip()
    workspace.blueprint_path.parent.mkdir(parents=True)
    workspace.blueprint_path.write_text("unrelated\n")
    store.recovery_path.parent.mkdir(parents=True, exist_ok=True)
    store.recovery_path.write_text(
        json.dumps(
            {
                "old_content": base64.b64encode(b"").decode(),
                "old_hash": blueprint_hash(b""),
                "new_hash": blueprint_hash(block().encode()),
                "pre_head": pre_head,
                "operation": "append_requirement",
                "feature_id": FEATURE_ID,
            }
        )
    )
    with pytest.raises(AutomationError, match="unknown_blueprint_transaction"):
        _apply_with_analysis(store, append_request(blueprint_hash(b"")))
    assert workspace.blueprint_path.read_text() == "unrelated\n"


def test_store_rejects_write_while_sync_merge_is_owned(tmp_path: Path) -> None:
    repo = make_repo(tmp_path / "project")
    workspace = ensure_dedicated_workspace(locate_repository(repo))
    store = BlueprintStore(workspace)
    merge_record = workspace.repository.coordination_dir / "merge-owner.json"
    merge_record.parent.mkdir(parents=True, exist_ok=True)
    merge_record.write_text('{"token":"active"}\n')
    with pytest.raises(AutomationError, match="merge_in_progress"):
        _apply_with_analysis(store, append_request(blueprint_hash(b"")))
    assert not workspace.blueprint_path.exists()


def test_status_update_requires_current_auto_dev_token(tmp_path: Path) -> None:
    repo = make_repo(tmp_path / "project")
    context = locate_repository(repo)
    workspace = ensure_dedicated_workspace(context)
    workspace.blueprint_path.parent.mkdir(parents=True)
    current = block().encode()
    workspace.blueprint_path.write_bytes(current)
    git(workspace.path, "add", ".codexspec/blueprint.md")
    git(workspace.path, "commit", "-m", "docs(blueprint): initialize")
    store = BlueprintStore(workspace)
    directory = f".codexspec/specs/{FEATURE_ID}-user-authentication/"
    status_request = request(
        "update_status",
        blueprint_hash(current),
        {"expected_status": "pending", "new_status": "in_progress", "feature_directory": directory},
        feature_id=FEATURE_ID,
    )

    with pytest.raises(AutomationError, match="auto_dev_token_required"):
        _apply_with_analysis(store, status_request)
    owner = AutoDevOwnership(context)
    token = owner.acquire()
    with pytest.raises(Exception, match="lost_ownership"):
        _apply_with_analysis(store, status_request, owner_token="wrong")
    assert _apply_with_analysis(store, status_request, owner_token=token)["result"] == "applied"
    owner.release(token)


def test_auto_dev_recovers_blueprint_file_written_before_commit(tmp_path: Path) -> None:
    repo = make_repo(tmp_path / "project")
    context = locate_repository(repo)
    workspace = ensure_dedicated_workspace(context)
    store = BlueprintStore(workspace)
    pre_head = git(workspace.path, "rev-parse", "HEAD").stdout.strip()
    replacement = block().encode()
    workspace.blueprint_path.parent.mkdir(parents=True)
    workspace.blueprint_path.write_bytes(replacement)
    store.recovery_path.parent.mkdir(parents=True, exist_ok=True)
    store.recovery_path.write_text(
        json.dumps(
            {
                "old_content": base64.b64encode(b"").decode(),
                "old_hash": blueprint_hash(b""),
                "new_hash": blueprint_hash(replacement),
                "pre_head": pre_head,
                "operation": "append_requirement",
                "feature_id": FEATURE_ID,
            }
        )
    )
    owner = AutoDevOwnership(context)
    token = owner.acquire()

    store.recover_pending_transaction(owner_token=token)

    assert not workspace.blueprint_path.exists()
    assert not store.recovery_path.exists()
    owner.release(token)


@pytest.mark.skipif(os.name == "nt", reason="Windows synthesizes POSIX permission bits (0o666/0o444 only)")
def test_atomic_replacement_preserves_and_chooses_sane_file_modes(tmp_path: Path) -> None:
    repo = make_repo(tmp_path / "project")
    context = locate_repository(repo)
    workspace = ensure_dedicated_workspace(context)
    store = BlueprintStore(workspace)

    first = _apply_with_analysis(store, append_request(blueprint_hash(b"")))
    assert first["result"] == "applied"
    blueprint = workspace.blueprint_path
    assert (blueprint.stat().st_mode & 0o777) == 0o644

    blueprint.chmod(0o640)
    document = BlueprintDocument.parse(blueprint.read_bytes())
    moved_id = document.blocks[0].feature_id
    replace = json.dumps(
        {
            "protocol_version": "1",
            "operation": "replace_pending_requirement",
            "feature_id": moved_id,
            "expected_blueprint_hash": blueprint_hash(blueprint.read_bytes()),
            "payload": {
                "feature_name": "renamed-feature",
                "requirements_markdown": unmanaged_requirements("Renamed feature"),
            },
        }
    ).encode()
    assert _apply_with_analysis(store, replace)["result"] == "applied"
    assert (blueprint.stat().st_mode & 0o777) == 0o640


def test_noop_operation_applies_without_creating_a_commit(tmp_path: Path) -> None:
    repo = make_repo(tmp_path / "project")
    context = locate_repository(repo)
    workspace = ensure_dedicated_workspace(context)
    store = BlueprintStore(workspace)

    assert _apply_with_analysis(store, append_request(blueprint_hash(b"")))["result"] == "applied"
    blueprint = workspace.blueprint_path
    current_hash = blueprint_hash(blueprint.read_bytes())
    head_before = git(workspace.path, "rev-parse", "HEAD").stdout.strip()
    feature_id = BlueprintDocument.parse(blueprint.read_bytes()).blocks[0].feature_id

    noop = json.dumps(
        {
            "protocol_version": "1",
            "operation": "move_pending_requirement",
            "feature_id": feature_id,
            "expected_blueprint_hash": current_hash,
            "payload": {"position": "first_pending"},
        }
    ).encode()
    outcome = _apply_with_analysis(store, noop)
    assert outcome["result"] == "applied"
    assert outcome["blueprint_hash"] == current_hash
    assert git(workspace.path, "rev-parse", "HEAD").stdout.strip() == head_before
    assert not store.recovery_path.exists()


def test_blueprint_analysis_precedes_publication_and_preserves_message(tmp_path):
    repo = make_repo(tmp_path / "project")
    workspace = ensure_dedicated_workspace(locate_repository(repo))
    store = BlueprintStore(workspace)
    prepared = store.prepare(append_request(blueprint_hash(b"")), feature_id_factory=lambda: FEATURE_ID)
    assert prepared["state"] == "prepared"
    assert not workspace.blueprint_path.exists()
    message = "docs(blueprint): add authentication requirements\n\nRecord the confirmed login behavior.\n"
    result = store.apply_and_commit(prepared["preparation_id"], prepared["tree"], message)
    assert result["result"] == "applied"
    assert result["feature_id"] == FEATURE_ID
    assert git(workspace.path, "rev-parse", "HEAD^{tree}").stdout.strip() == prepared["tree"]
    assert "Record the confirmed login behavior." in git(workspace.path, "log", "-1", "--format=%B").stdout


def test_blueprint_stale_analysis_never_publishes(tmp_path):
    repo = make_repo(tmp_path / "project")
    workspace = ensure_dedicated_workspace(locate_repository(repo))
    store = BlueprintStore(workspace)
    prepared = store.prepare(append_request(blueprint_hash(b"")))
    with pytest.raises(AutomationError, match="stale_analysis"):
        store.apply_and_commit(prepared["preparation_id"], "0" * 40, "docs(blueprint): add requirements")
    assert not workspace.blueprint_path.exists()
    git(workspace.path, "commit", "--allow-empty", "-m", "chore: advance")
    with pytest.raises(AutomationError, match="stale_analysis"):
        store.apply_and_commit(prepared["preparation_id"], prepared["tree"], "docs(blueprint): add requirements")
    assert not workspace.blueprint_path.exists()


@pytest.mark.skipif(os.name == "nt", reason="Git executable mode is platform dependent")
def test_blueprint_prepared_mode_matches_existing_executable_file(tmp_path):
    repo = make_repo(tmp_path / "project")
    workspace = ensure_dedicated_workspace(locate_repository(repo))
    store = BlueprintStore(workspace)
    _apply_with_analysis(store, append_request(blueprint_hash(b"")))
    workspace.blueprint_path.chmod(0o755)
    git(workspace.path, "add", ".codexspec/blueprint.md")
    git(workspace.path, "commit", "-m", "chore: preserve executable mode")
    result = _apply_with_analysis(store, append_request(blueprint_hash(workspace.blueprint_path.read_bytes())))
    assert result["result"] == "applied"
    assert git(workspace.path, "ls-tree", "HEAD", ".codexspec/blueprint.md").stdout.startswith("100755")


def test_blueprint_preparation_applies_path_clean_filter(tmp_path):
    repo = make_repo(tmp_path / "project")
    (repo / ".gitattributes").write_text(".codexspec/blueprint.md filter=canonical\n")
    git(repo, "config", "filter.canonical.clean", "sed s/securely/safely/g")
    git(repo, "add", ".gitattributes")
    git(repo, "commit", "-m", "chore: configure clean filter")
    workspace = ensure_dedicated_workspace(locate_repository(repo))
    store = BlueprintStore(workspace)
    prepared = store.prepare(append_request(blueprint_hash(b"")), feature_id_factory=lambda: FEATURE_ID)
    preview = git(workspace.path, "show", f"{prepared['tree']}:.codexspec/blueprint.md").stdout
    assert "safely" in preview
    assert "securely" not in preview
    assert not workspace.blueprint_path.exists()
    result = store.apply_and_commit(
        prepared["preparation_id"], prepared["tree"], "docs(blueprint): add authentication requirement"
    )
    assert result["result"] == "applied"
    assert git(workspace.path, "rev-parse", "HEAD^{tree}").stdout.strip() == prepared["tree"]
    assert git(workspace.path, "show", "HEAD:.codexspec/blueprint.md").stdout == preview


def test_blueprint_post_commit_failure_preserves_published_file_and_recovery(tmp_path):
    repo = make_repo(tmp_path / "project")
    workspace = ensure_dedicated_workspace(locate_repository(repo))
    store = BlueprintStore(workspace)
    hook = repo / ".git/hooks/post-commit"
    hook.write_text(
        "#!/bin/sh\n"
        'printf "updated\\n" > version.txt\n'
        "git add version.txt\n"
        "tree=$(git write-tree) || exit 1\n"
        "parent=$(git rev-parse HEAD) || exit 1\n"
        'commit=$(printf "chore: generated version\\n" | git commit-tree "$tree" -p "$parent") || exit 1\n'
        'git update-ref HEAD "$commit" "$parent"\n'
    )
    hook.chmod(0o755)
    prepared = store.prepare(append_request(blueprint_hash(b"")), feature_id_factory=lambda: FEATURE_ID)
    with pytest.raises(AutomationError, match="committed_tree_mismatch"):
        store.apply_and_commit(prepared["preparation_id"], prepared["tree"], "docs(blueprint): add requirement")
    committed = git(workspace.path, "show", "HEAD:.codexspec/blueprint.md").stdout
    assert workspace.blueprint_path.exists()
    assert workspace.blueprint_path.read_text() == committed
    assert store.recovery_path.exists()
    assert not git(workspace.path, "diff", "--name-only", "--", ".codexspec/blueprint.md").stdout
    with pytest.raises(AutomationError, match="unknown_blueprint_transaction"):
        store.prepare(append_request(blueprint_hash(workspace.blueprint_path.read_bytes())))
    assert store.recovery_path.exists()
    assert workspace.blueprint_path.read_text() == committed
