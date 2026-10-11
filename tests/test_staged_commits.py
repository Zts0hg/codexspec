"""Prepared staging must describe exactly the prospective commit."""

from pathlib import Path

import pytest

from codexspec.automation import AutomationError, GitRunner, ensure_dedicated_workspace, locate_repository
from codexspec.staged_commits import PreparedCommits
from tests.automation_test_support import git, make_repo


def setup_store(tmp_path):
    repo = make_repo(tmp_path / "repo")
    workspace = ensure_dedicated_workspace(locate_repository(repo))
    return workspace, PreparedCommits(workspace)


def test_preparation_preserves_unrelated_staging(tmp_path):
    workspace, store = setup_store(tmp_path)
    (workspace.path / "selected.txt").write_text("selected\n")
    (workspace.path / "other.txt").write_text("other\n")
    git(workspace.path, "add", "other.txt")
    before = git(workspace.path, "write-tree").stdout.strip()
    prepared = store.prepare(["selected.txt"], kind="feature", scope="2026-1010-21225w", token="owner")
    assert git(workspace.path, "write-tree").stdout.strip() == before
    staged = GitRunner().run(workspace.path, "diff", "--cached", "--name-only", index_file=Path(prepared["index_file"]))
    assert staged.stdout.splitlines() == ["selected.txt"]
    assert store.load(prepared["preparation_id"], kind="feature", token="owner")["tree"] == prepared["tree"]


def test_blueprint_preparation_does_not_publish(tmp_path):
    workspace, store = setup_store(tmp_path)
    prepared = store.prepare([".codexspec/blueprint.md"], kind="blueprint", scope="blueprint", content="proposal\n")
    assert not workspace.blueprint_path.exists()
    blob = GitRunner().run(workspace.path, "show", ":.codexspec/blueprint.md", index_file=Path(prepared["index_file"]))
    assert blob.stdout == "proposal\n"


def test_preparation_rejects_changed_tree_head_and_owner(tmp_path):
    workspace, store = setup_store(tmp_path)
    (workspace.path / "selected.txt").write_text("selected\n")
    prepared = store.prepare(["selected.txt"], kind="feature", scope="2026-1010-21225w", token="owner")
    with pytest.raises(AutomationError, match="preparation_owner"):
        store.load(prepared["preparation_id"], kind="feature", token="other")
    GitRunner().run(workspace.path, "read-tree", "HEAD", index_file=Path(prepared["index_file"]))
    with pytest.raises(AutomationError, match="stale_analysis"):
        store.load(prepared["preparation_id"], kind="feature", token="owner")
    fresh = store.prepare(["selected.txt"], kind="feature", scope="2026-1010-21225w", token="owner")
    git(workspace.path, "commit", "--allow-empty", "-m", "chore: advance")
    with pytest.raises(AutomationError, match="stale_analysis"):
        store.load(fresh["preparation_id"], kind="feature", token="owner")


def test_empty_and_foreign_preparations_are_rejected(tmp_path):
    workspace, store = setup_store(tmp_path)
    with pytest.raises(AutomationError, match="empty_staged_changes"):
        store.prepare(["README.md"], kind="feature", scope="2026-1010-21225w")
    for identifier in ("../foreign", "bad", "0" * 32):
        with pytest.raises(AutomationError, match="invalid_preparation"):
            store.load(identifier, kind="feature")


def test_preparation_captures_deletion_and_rename(tmp_path):
    workspace, store = setup_store(tmp_path)
    (workspace.path / "README.md").rename(workspace.path / "renamed.md")
    prepared = store.prepare(["README.md", "renamed.md"], kind="feature", scope="2026-1010-21225w")
    names = git(workspace.path, "ls-tree", "--name-only", prepared["tree"]).stdout.splitlines()
    assert "renamed.md" in names
    assert "README.md" not in names


def test_direct_commit_preserves_partial_staging_and_body(tmp_path):
    from codexspec.staged_commits import commit_snapshot, snapshot

    repo = make_repo(tmp_path / "repo")
    (repo / "README.md").write_text("staged\n")
    git(repo, "add", "README.md")
    (repo / "README.md").write_text("unstaged\n")
    prepared = snapshot(repo)
    result = commit_snapshot(repo, prepared, "fix: correct staged text\n\nExplain the staged change.\n")
    assert result["state"] == "committed"
    assert git(repo, "show", "HEAD:README.md").stdout == "staged\n"
    assert (repo / "README.md").read_text() == "unstaged\n"
    assert "Explain the staged change." in git(repo, "log", "-1", "--format=%B").stdout
    assert git(repo, "rev-parse", "HEAD^{tree}").stdout.strip() == prepared["tree"]


@pytest.mark.parametrize("hook", ["pre-commit", "prepare-commit-msg", "commit-msg"])
def test_hooks_that_stage_changes_abort_before_commit(tmp_path, hook):
    from codexspec.staged_commits import commit_snapshot, snapshot

    repo = make_repo(tmp_path / "repo")
    hooks = repo / "custom-hooks"
    hooks.mkdir()
    script = hooks / hook
    script.write_text('#!/bin/sh\nprintf "changed by hook\\n" > README.md\ngit add README.md\n')
    script.chmod(0o755)
    git(repo, "config", "core.hooksPath", "custom-hooks")
    (repo / "README.md").write_text("staged\n")
    git(repo, "add", "README.md")
    prepared = snapshot(repo)
    with pytest.raises(AutomationError):
        commit_snapshot(repo, prepared, "fix: staged text")
    assert git(repo, "rev-parse", "HEAD").stdout.strip() == prepared["head"]
    with pytest.raises(AutomationError, match="stale_analysis"):
        commit_snapshot(repo, prepared, "fix: staged text")


def test_hooks_keep_arguments_failures_and_post_commit(tmp_path):
    from codexspec.staged_commits import commit_snapshot, snapshot

    repo = make_repo(tmp_path / "repo")
    hooks = repo / "custom hooks"
    hooks.mkdir()
    git(repo, "config", "core.hooksPath", str(hooks))
    script = hooks / "commit-msg"
    script.write_text('#!/bin/sh\ntest -f "$1" || exit 4\nexit 1\n')
    script.chmod(0o755)
    (repo / "README.md").write_text("staged\n")
    git(repo, "add", "README.md")
    prepared = snapshot(repo)
    with pytest.raises(AutomationError):
        commit_snapshot(repo, prepared, "fix: staged text")
    assert git(repo, "rev-parse", "HEAD").stdout.strip() == prepared["head"]
    script.write_text('#!/bin/sh\ntest -f "$1"\n')
    post = hooks / "post-commit"
    post.write_text('#!/bin/sh\nprintf "ran" > hook-ran\n')
    post.chmod(0o755)
    commit_snapshot(repo, snapshot(repo), "fix: staged text")
    assert (repo / "hook-ran").read_text() == "ran"


def test_guarded_path_commit_preserves_unrelated_index(tmp_path):
    from codexspec.staged_commits import guarded_commit

    workspace, store = setup_store(tmp_path)
    (workspace.path / "selected.txt").write_text("selected\n")
    (workspace.path / "other.txt").write_text("other\n")
    git(workspace.path, "add", "other.txt")
    prepared = store.prepare(["selected.txt"], kind="feature", scope="2026-1010-21225w")
    git(workspace.path, "add", "selected.txt")
    result = guarded_commit(
        workspace.path, prepared["head"], prepared["tree"], "feat: selected", paths=["selected.txt"]
    )
    assert git(workspace.path, "rev-parse", f"{result}^{{tree}}").stdout.strip() == prepared["tree"]
    assert git(workspace.path, "diff", "--cached", "--name-only").stdout.splitlines() == ["other.txt"]


def test_direct_initial_commit(tmp_path):
    from codexspec.staged_commits import commit_snapshot, snapshot

    repo = tmp_path / "initial"
    repo.mkdir()
    git(repo, "init", "-b", "feature")
    git(repo, "config", "user.name", "Tests")
    git(repo, "config", "user.email", "tests@codexspec.invalid")
    (repo / "new.txt").write_text("new\n")
    git(repo, "add", "new.txt")
    prepared = snapshot(repo)
    assert prepared["head"] is None
    commit_snapshot(repo, prepared, "feat: initial file")
    assert git(repo, "show", "HEAD:new.txt").stdout == "new\n"


def test_direct_commit_preserves_project_specific_message_conventions(tmp_path):
    from codexspec.staged_commits import commit_snapshot, snapshot

    repo = make_repo(tmp_path / "repo")
    (repo / "README.md").write_text("changed\n")
    git(repo, "add", "README.md")
    commit_snapshot(repo, snapshot(repo), "PROJECT-42 Correct staged content")
    assert git(repo, "log", "-1", "--format=%s").stdout.strip() == "PROJECT-42 Correct staged content"


def test_preparation_rejects_foreign_workspace_and_linked_record(tmp_path):
    import json

    workspace, store = setup_store(tmp_path)
    (workspace.path / "selected.txt").write_text("selected\n")
    prepared = store.prepare(["selected.txt"], kind="feature", scope="2026-1010-21225w")
    record_path = Path(prepared["index_file"]).parent / "record.json"
    record = json.loads(record_path.read_text())
    record["workspace"] = str(tmp_path / "foreign")
    record_path.write_text(json.dumps(record))
    with pytest.raises(AutomationError, match="invalid_preparation"):
        store.load(prepared["preparation_id"], kind="feature")
    record_path.unlink()
    original = tmp_path / "record.json"
    original.write_text(json.dumps(record))
    try:
        record_path.symlink_to(original)
    except OSError:
        pytest.skip("symlink creation unavailable")
    with pytest.raises(AutomationError, match="invalid_preparation"):
        store.discard(prepared["preparation_id"], kind="feature")
    assert original.exists()


def test_direct_commit_uses_callers_explicit_index(tmp_path, monkeypatch):
    from codexspec.staged_commits import commit_snapshot, snapshot

    repo = make_repo(tmp_path / "repo")
    index = tmp_path / "caller-index"
    runner = GitRunner()
    runner.run(repo, "read-tree", "HEAD", index_file=index)
    (repo / "selected.txt").write_text("selected\n")
    runner.run(repo, "add", "selected.txt", index_file=index)
    (repo / "unrelated.txt").write_text("unrelated\n")
    git(repo, "add", "unrelated.txt")
    ordinary_index = Path(git(repo, "rev-parse", "--path-format=absolute", "--git-path", "index").stdout.strip())
    original_bytes = ordinary_index.read_bytes()
    monkeypatch.setenv("GIT_INDEX_FILE", str(index))
    prepared = snapshot(repo)
    assert prepared["index_file"] == str(index)
    commit_snapshot(repo, prepared, "feat: add selected content")
    assert runner.run(repo, "show", "HEAD:selected.txt").stdout == "selected\n"
    assert runner.run(repo, "ls-tree", "--name-only", "HEAD", "unrelated.txt").stdout == ""
    assert ordinary_index.read_bytes() == original_bytes


@pytest.mark.parametrize("workflow", ["direct", "feature", "blueprint"])
def test_reference_transaction_hook_preserves_stdin_and_denial(tmp_path, workflow):
    from codexspec.automation import AutoDevGit, AutoDevOwnership, BlueprintStore
    from codexspec.blueprint import blueprint_hash
    from codexspec.staged_commits import commit_snapshot, snapshot
    from tests.test_blueprint import FEATURE_ID
    from tests.test_blueprint_store import append_request

    workspace, _ = setup_store(tmp_path)
    repo = workspace.path
    hooks = tmp_path / "original hooks"
    hooks.mkdir()
    git(repo, "config", "core.hooksPath", str(hooks))
    hook = hooks / "reference-transaction"
    hook.write_text(
        "#!/bin/sh\n"
        "while read old new ref; do\n"
        '  printf "%s %s %s %s\\n" "$1" "$old" "$new" "$ref" >> hook-input\n'
        '  if test "$1" = prepared && test -f deny-commit; then exit 1; fi\n'
        "done\n"
    )
    hook.chmod(0o755)
    (repo / "deny-commit").touch()
    (repo / "selected.txt").write_text("selected\n")
    git(repo, "add", "selected.txt")
    head = git(repo, "rev-parse", "HEAD").stdout.strip()
    ordinary = git(repo, "commit", "-m", "ordinary", check=False)
    assert ordinary.returncode != 0
    assert git(repo, "rev-parse", "HEAD").stdout.strip() == head
    owner = AutoDevOwnership(workspace.repository)
    token = owner.acquire()
    service = AutoDevGit(workspace, owner)
    blueprint = BlueprintStore(workspace)

    def attempt():
        if workflow == "direct":
            prepared = snapshot(repo)
            commit_snapshot(repo, prepared, "feat: selected content")
        elif workflow == "feature":
            prepared = service.prepare_feature(token, FEATURE_ID, ["selected.txt"])
            service.commit_feature(
                token, prepared["preparation_id"], prepared["tree"], f"feat({FEATURE_ID}): selected content"
            )
        else:
            prepared = blueprint.prepare(append_request(blueprint_hash(b"")), owner_token=token)
            blueprint.apply_and_commit(
                prepared["preparation_id"], prepared["tree"], "docs(blueprint): record requirement", owner_token=token
            )
        return prepared

    try:
        with pytest.raises(AutomationError):
            attempt()
        assert git(repo, "rev-parse", "HEAD").stdout.strip() == head
        if workflow == "blueprint":
            assert not workspace.blueprint_path.exists()
        (repo / "deny-commit").unlink()
        (repo / "hook-input").write_text("")
        prepared = attempt()
        assert git(repo, "rev-parse", "HEAD^{tree}").stdout.strip() == prepared["tree"]
        records = (repo / "hook-input").read_text().splitlines()
        branch = git(repo, "symbolic-ref", "HEAD").stdout.strip()
        assert any(line.startswith("prepared ") and line.endswith(branch) for line in records)
        assert any(line.startswith("committed ") and line.endswith(branch) for line in records)
    finally:
        owner.release(token)
