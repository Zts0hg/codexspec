"""Machine interfaces cannot bypass staged analysis metadata."""

import json

from typer.testing import CliRunner

from codexspec import app
from tests.automation_test_support import git, make_repo


def test_direct_snapshot_and_commit_cli(tmp_path, monkeypatch):
    repo = make_repo(tmp_path / "repo")
    monkeypatch.chdir(repo)
    (repo / "README.md").write_text("changed\n")
    git(repo, "add", "README.md")
    runner = CliRunner()
    result = runner.invoke(app, ["_commit-staged-helper", "snapshot"])
    assert result.exit_code == 0, result.output
    analyzed = json.loads(result.stdout)
    committed = runner.invoke(
        app,
        ["_commit-staged-helper", "commit"],
        input=json.dumps(
            {
                "analysis": analyzed,
                "message": "fix: update staged content\n\nExplain the change.\n",
            }
        ),
    )
    assert committed.exit_code == 0, committed.output
    assert json.loads(committed.stdout)["state"] == "committed"


def test_feature_machine_handoff_and_legacy_rejection(tmp_path, monkeypatch):
    repo = make_repo(tmp_path / "repo")
    monkeypatch.chdir(repo)
    runner = CliRunner()
    acquired = runner.invoke(app, ["_auto-dev-helper", "acquire"], input="{}")
    state = json.loads(acquired.stdout)
    from pathlib import Path

    workspace = Path(state["worktree_path"])
    (workspace / "change.txt").write_text("change\n")
    request = {"token": state["token"], "feature_id": "2026-1010-21225w", "paths": ["change.txt"]}
    result = runner.invoke(app, ["_auto-dev-helper", "prepare-feature"], input=json.dumps(request))
    assert result.exit_code == 0, result.output
    prepared = json.loads(result.stdout)
    old = runner.invoke(
        app,
        ["_auto-dev-helper", "commit-feature"],
        input=json.dumps(
            {
                **request,
                "commit_type": "feat",
                "description": "legacy",
            }
        ),
    )
    assert old.exit_code != 0
    result = runner.invoke(
        app,
        ["_auto-dev-helper", "commit-feature"],
        input=json.dumps(
            {
                "token": state["token"],
                "preparation_id": prepared["preparation_id"],
                "analyzed_tree": prepared["tree"],
                "message": "feat(2026-1010-21225w): add change",
            }
        ),
    )
    assert result.exit_code == 0, result.output
    assert json.loads(result.stdout)["state"] == "committed"


def test_blueprint_legacy_apply_is_rejected(tmp_path, monkeypatch):
    repo = make_repo(tmp_path / "repo")
    monkeypatch.chdir(repo)
    runner = CliRunner()
    result = runner.invoke(app, ["_blueprint-helper", "apply", "--ensure"], input='{"operation":"append_requirement"}')
    assert result.exit_code != 0
    assert "analysis" in result.stderr


def test_invalid_analysis_fields_and_discard_preserve_caller_state(tmp_path, monkeypatch):
    from pathlib import Path

    repo = make_repo(tmp_path / "repo")
    monkeypatch.chdir(repo)
    runner = CliRunner()
    acquired = json.loads(runner.invoke(app, ["_auto-dev-helper", "acquire"], input="{}").stdout)
    workspace = Path(acquired["worktree_path"])
    (workspace / "change.txt").write_text("change\n")
    prepared = json.loads(
        runner.invoke(
            app,
            ["_auto-dev-helper", "prepare-feature"],
            input=json.dumps(
                {
                    "token": acquired["token"],
                    "feature_id": "2026-1010-21225w",
                    "paths": ["change.txt"],
                }
            ),
        ).stdout
    )
    before = git(workspace, "status", "--porcelain").stdout
    base = {
        "token": acquired["token"],
        "preparation_id": prepared["preparation_id"],
        "analyzed_tree": prepared["tree"],
        "message": "feat(2026-1010-21225w): add change",
    }
    for bad in ({**base, "message": None}, {**base, "analyzed_tree": []}, {**base, "extra": True}):
        result = runner.invoke(app, ["_auto-dev-helper", "commit-feature"], input=json.dumps(bad))
        assert result.exit_code != 0
        assert "analysis_required" in result.stderr
    discarded = runner.invoke(
        app,
        ["_auto-dev-helper", "discard-feature"],
        input=json.dumps(
            {
                "token": acquired["token"],
                "preparation_id": prepared["preparation_id"],
            }
        ),
    )
    assert discarded.exit_code == 0, discarded.output
    assert not Path(prepared["index_file"]).exists()
    assert git(workspace, "status", "--porcelain").stdout == before
