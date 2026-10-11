"""Tests for blueprint helper and public display CLI commands."""

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Iterator

import pytest
from typer.testing import CliRunner

from codexspec import app
from codexspec.automation import ensure_dedicated_workspace, locate_repository
from tests.automation_test_support import git, make_repo
from tests.test_blueprint import block, unmanaged_requirements


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


@pytest.fixture
def project(tmp_path: Path) -> Iterator[tuple[Path, Path]]:
    repo = make_repo(tmp_path / "project")
    workspace = ensure_dedicated_workspace(locate_repository(repo))
    workspace.blueprint_path.parent.mkdir(parents=True)
    workspace.blueprint_path.write_bytes(block().encode())
    git(workspace.path, "add", ".codexspec/blueprint.md")
    git(workspace.path, "commit", "-m", "docs(blueprint): initialize")
    original = Path.cwd()
    os.chdir(repo)
    try:
        yield repo, workspace.path
    finally:
        os.chdir(original)


def test_show_blueprint_writes_exact_raw_content(project: tuple[Path, Path], runner: CliRunner) -> None:
    _, workspace = project
    expected = (workspace / ".codexspec/blueprint.md").read_bytes()
    result = runner.invoke(app, ["show-blueprint"])
    assert result.exit_code == 0
    assert result.stdout_bytes == expected
    assert result.stderr_bytes == b""


def test_show_blueprint_reports_missing_branch_without_mutation(tmp_path: Path, runner: CliRunner) -> None:
    repo = make_repo(tmp_path / "project")
    original = Path.cwd()
    os.chdir(repo)
    try:
        before = git(repo, "status", "--porcelain").stdout
        result = runner.invoke(app, ["show-blueprint"])
        after = git(repo, "status", "--porcelain").stdout
    finally:
        os.chdir(original)
    assert result.exit_code != 0
    assert result.stdout_bytes == b""
    assert "codexspec/auto-dev branch" in result.stderr.lower()
    assert before == after


def test_show_blueprint_reports_not_repository(tmp_path: Path, runner: CliRunner) -> None:
    original = Path.cwd()
    os.chdir(tmp_path)
    try:
        result = runner.invoke(app, ["show-blueprint"])
    finally:
        os.chdir(original)
    assert result.exit_code != 0
    assert result.stdout_bytes == b""
    assert "git repository" in result.stderr.lower()


def test_show_blueprint_reports_missing_worktree(tmp_path: Path, runner: CliRunner) -> None:
    repo = make_repo(tmp_path / "project")
    git(repo, "branch", "codexspec/auto-dev", "main")
    original = Path.cwd()
    os.chdir(repo)
    try:
        result = runner.invoke(app, ["show-blueprint"])
    finally:
        os.chdir(original)
    assert result.exit_code != 0
    assert result.stdout_bytes == b""
    assert "worktree" in result.stderr.lower()


def test_show_blueprint_reports_missing_file(tmp_path: Path, runner: CliRunner) -> None:
    repo = make_repo(tmp_path / "project")
    ensure_dedicated_workspace(locate_repository(repo))
    original = Path.cwd()
    os.chdir(repo)
    try:
        result = runner.invoke(app, ["show-blueprint"])
    finally:
        os.chdir(original)
    assert result.exit_code != 0
    assert result.stdout_bytes == b""
    assert ".codexspec/blueprint.md" in result.stderr


def test_hidden_inspect_and_apply_use_machine_json(project: tuple[Path, Path], runner: CliRunner) -> None:
    _, workspace = project
    inspected = runner.invoke(app, ["_blueprint-helper", "inspect"])
    assert inspected.exit_code == 0
    state = json.loads(inspected.stdout)
    assert state["worktree_path"] == str(workspace)
    assert state["blueprint_exists"] is True
    request = {
        "protocol_version": "1",
        "operation": "append_requirement",
        "expected_blueprint_hash": state["blueprint_hash"],
        "payload": {
            "feature_name": "release-notes",
            "requirements_markdown": unmanaged_requirements("Release notes"),
        },
    }
    preparation = runner.invoke(app, ["_blueprint-helper", "prepare"], input=json.dumps(request))
    assert preparation.exit_code == 0, preparation.output
    prepared = json.loads(preparation.stdout)
    applied = runner.invoke(
        app,
        ["_blueprint-helper", "apply"],
        input=json.dumps(
            {
                "preparation_id": prepared["preparation_id"],
                "analyzed_tree": prepared["tree"],
                "message": "docs(blueprint): add release note requirements",
            }
        ),
    )
    assert applied.exit_code == 0
    assert json.loads(applied.stdout)["result"] == "applied"


def test_hidden_auto_dev_owner_actions_are_fenced(project: tuple[Path, Path], runner: CliRunner) -> None:
    acquired = runner.invoke(app, ["_auto-dev-helper", "acquire"], input="{}")
    assert acquired.exit_code == 0
    acquired_body = json.loads(acquired.stdout)
    assert acquired_body["heartbeat_interval_seconds"] > 0
    token = acquired_body["token"]
    asserted = runner.invoke(app, ["_auto-dev-helper", "assert-owner"], input=json.dumps({"token": token}))
    assert asserted.exit_code == 0
    prepared = runner.invoke(
        app,
        ["_auto-dev-helper", "prepare-sync-verification"],
        input=json.dumps({"token": token, "resolved_paths": ["README.md"]}),
    )
    assert prepared.exit_code != 0
    assert "no_merge_in_progress" in prepared.stderr
    wrong = runner.invoke(app, ["_auto-dev-helper", "renew"], input=json.dumps({"token": "wrong"}))
    assert wrong.exit_code != 0
    released = runner.invoke(app, ["_auto-dev-helper", "release"], input=json.dumps({"token": token}))
    assert released.exit_code == 0


def _start_cli(cwd: Path, *args: str, input_text: str) -> subprocess.Popen[str]:
    command = [
        sys.executable,
        "-c",
        "import sys; from codexspec import main; main()",
        *args,
    ]
    process = subprocess.Popen(
        command,
        cwd=cwd,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    assert process.stdin is not None
    process.stdin.write(input_text)
    process.stdin.close()
    return process


def _finish_cli(process: subprocess.Popen[str]) -> tuple[int, str, str]:
    return_code = process.wait(timeout=20)
    assert process.stdout is not None
    assert process.stderr is not None
    return return_code, process.stdout.read(), process.stderr.read()


def test_concurrent_blueprint_helpers_apply_once_and_conflict_once(
    project: tuple[Path, Path], runner: CliRunner
) -> None:
    repo, _ = project
    inspected = json.loads(runner.invoke(app, ["_blueprint-helper", "inspect"]).stdout)
    request = json.dumps(
        {
            "protocol_version": "1",
            "operation": "append_requirement",
            "expected_blueprint_hash": inspected["blueprint_hash"],
            "payload": {
                "feature_name": "release-notes",
                "requirements_markdown": unmanaged_requirements("Release notes"),
            },
        }
    )
    processes = [
        _start_cli(repo, "_blueprint-helper", "prepare", input_text=request),
        _start_cli(repo, "_blueprint-helper", "prepare", input_text=request),
    ]
    prepared_results = [_finish_cli(process) for process in processes]
    assert [code for code, _, _ in prepared_results] == [0, 0]
    preparations = [json.loads(stdout) for _, stdout, _ in prepared_results]
    processes = [
        _start_cli(
            repo,
            "_blueprint-helper",
            "apply",
            input_text=json.dumps(
                {
                    "preparation_id": item["preparation_id"],
                    "analyzed_tree": item["tree"],
                    "message": "docs(blueprint): add release notes requirements",
                }
            ),
        )
        for item in preparations
    ]
    results = [_finish_cli(process) for process in processes]
    assert sorted(code for code, _, _ in results) == [0, 1]
    assert next(json.loads(stdout)["result"] for code, stdout, _ in results if code == 0) == "applied"
    assert "stale_analysis" in next(stderr for code, _, stderr in results if code != 0)


def test_concurrent_auto_dev_acquire_has_exactly_one_owner(project: tuple[Path, Path]) -> None:
    repo, _ = project
    processes = [
        _start_cli(repo, "_auto-dev-helper", "acquire", input_text="{}"),
        _start_cli(repo, "_auto-dev-helper", "acquire", input_text="{}"),
    ]
    results = [_finish_cli(process) for process in processes]
    assert sorted(code for code, _, _ in results) == [0, 1]
    winner = next(json.loads(stdout) for code, stdout, _ in results if code == 0)
    released = _start_cli(
        repo,
        "_auto-dev-helper",
        "release",
        input_text=json.dumps({"token": winner["token"]}),
    )
    assert _finish_cli(released)[0] == 0


@pytest.mark.parametrize(
    ("action", "body", "error"),
    [
        ("unknown", {}, "unsupported_auto_dev_helper_action"),
        ("unknown", {"token": "invalid"}, "unsupported_auto_dev_helper_action"),
        ("acquire", {"extra": True}, "unexpected_fields"),
        ("release", {}, "missing_token"),
        ("renew", {"token": None}, "missing_token"),
        ("assert-owner", {"token": "invalid", "extra": True}, "unexpected_fields"),
        ("sync-default", {"token": "invalid", "extra": True}, "unexpected_fields"),
        ("abort-sync", {"token": "invalid", "extra": True}, "unexpected_fields"),
        ("prepare-sync-verification", {"token": "invalid", "resolved_paths": []}, "invalid_prepare_sync_request"),
        ("continue-sync", {"token": "invalid", "checks_passed": "yes"}, "invalid_continue_sync_request"),
        ("prepare-feature", {"token": "invalid", "feature_id": "x", "paths": "x"}, "invalid_prepare_feature_request"),
        ("commit-feature", {"token": "invalid"}, "analysis_required"),
        ("discard-feature", {"token": "invalid"}, "invalid_preparation"),
    ],
)
def test_invalid_auto_dev_request_has_no_workspace_side_effects(tmp_path, monkeypatch, runner, action, body, error):
    repo = make_repo(tmp_path / "project")
    monkeypatch.chdir(repo)
    context = locate_repository(repo)
    before = git(repo, "worktree", "list", "--porcelain").stdout
    result = runner.invoke(app, ["_auto-dev-helper", action], input=json.dumps(body))
    assert result.exit_code == 1
    assert error in result.stderr
    assert git(repo, "worktree", "list", "--porcelain").stdout == before
    assert not context.worktree_path.parent.exists()
    assert not context.coordination_dir.exists()
    assert git(repo, "show-ref", "--verify", "refs/heads/codexspec/auto-dev", check=False).returncode != 0


@pytest.mark.parametrize("action", ["renew", "assert-owner", "release"])
def test_auto_dev_owner_actions_do_not_require_a_workspace(tmp_path, monkeypatch, runner, action):
    from codexspec.automation import AutoDevOwnership

    repo = make_repo(tmp_path / "project")
    monkeypatch.chdir(repo)
    context = locate_repository(repo)
    ownership = AutoDevOwnership(context)
    token = ownership.acquire()
    try:
        result = runner.invoke(app, ["_auto-dev-helper", action], input=json.dumps({"token": token}))
        assert result.exit_code == 0, result.output
        assert not context.worktree_path.parent.exists()
        assert git(repo, "show-ref", "--verify", "refs/heads/codexspec/auto-dev", check=False).returncode != 0
    finally:
        if ownership.record_path.exists():
            ownership.release(token)


@pytest.mark.parametrize(
    ("action", "body"),
    [
        ("sync-default", {}),
        ("abort-sync", {}),
        ("prepare-sync-verification", {"resolved_paths": ["README.md"]}),
        ("continue-sync", {"checks_passed": True}),
        ("prepare-feature", {"feature_id": "2026-1011-1234ab", "paths": ["README.md"]}),
        ("commit-feature", {"preparation_id": "missing", "analyzed_tree": "missing", "message": "feat: test"}),
        ("discard-feature", {"preparation_id": "missing"}),
    ],
)
def test_auto_dev_followup_does_not_recreate_missing_workspace(tmp_path, monkeypatch, runner, action, body):
    from codexspec.automation import AutoDevOwnership

    repo = make_repo(tmp_path / "project")
    monkeypatch.chdir(repo)
    context = locate_repository(repo)
    workspace = ensure_dedicated_workspace(context)
    git(repo, "worktree", "remove", str(workspace.path))
    ownership = AutoDevOwnership(context)
    token = ownership.acquire()
    try:
        result = runner.invoke(app, ["_auto-dev-helper", action], input=json.dumps({"token": token, **body}))
        assert result.exit_code == 1
        assert "missing_fixed_worktree" in result.stderr
        assert not workspace.path.exists()
        assert str(workspace.path) not in git(repo, "worktree", "list", "--porcelain").stdout
    finally:
        ownership.release(token)


def test_auto_dev_acquire_still_creates_missing_workspace(tmp_path, monkeypatch, runner):
    repo = make_repo(tmp_path / "project")
    monkeypatch.chdir(repo)
    acquired = runner.invoke(app, ["_auto-dev-helper", "acquire"], input="{}")
    assert acquired.exit_code == 0, acquired.output
    body = json.loads(acquired.stdout)
    assert Path(body["worktree_path"]).is_dir()
    released = runner.invoke(app, ["_auto-dev-helper", "release"], input=json.dumps({"token": body["token"]}))
    assert released.exit_code == 0, released.output
