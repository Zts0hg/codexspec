"""Machine handoff and recovery tests for merge analysis."""

import json
from pathlib import Path

import pytest
from typer.testing import CliRunner

import codexspec
from codexspec.automation import AutoDevOwnership, AutomationError, ensure_dedicated_workspace, locate_repository
from codexspec.commit_runtime import snapshot
from tests.automation_test_support import git
from tests.test_auto_dev_git import services
from tests.test_merge_commit_analysis import diverge
from tests.test_worktrees import diverged, evidence


@pytest.mark.parametrize("entry", ["auto-dev", "blueprint"])
def test_initial_merge_cli_retains_workspace_and_releases_owner(tmp_path, monkeypatch, entry):
    repo, local, remote = diverged(tmp_path)
    monkeypatch.chdir(repo)
    runner = CliRunner()
    args = ["_auto-dev-helper", "acquire"] if entry == "auto-dev" else ["_blueprint-helper", "inspect", "--ensure"]
    pending = runner.invoke(codexspec.app, args, input="{}")
    assert pending.exit_code == 3, pending.output
    payload = json.loads(pending.output)
    work = Path(payload["workspace"])
    context = locate_repository(repo)
    assert payload["status"] == "merge_requires_verification"
    assert git(work, "rev-parse", "HEAD").stdout.strip() == local
    assert not AutoDevOwnership(context).record_path.exists()
    repeat = runner.invoke(codexspec.app, args, input="{}")
    assert repeat.exit_code == 3 and json.loads(repeat.output)["workspace"] == str(work)
    proof = tmp_path / "verification.json"
    data = evidence(work)
    proof.write_text(json.dumps(data))
    finish = runner.invoke(codexspec.app, ["_worktree-helper", "finish-initial", "--verification", str(proof)])
    assert finish.exit_code == 0, finish.output
    assert git(work, "show", "-s", "--format=%P", "HEAD").stdout.split() == [local, remote]
    assert not (context.coordination_dir / "initial-merge.json").exists()
    resumed = runner.invoke(codexspec.app, args, input="{}")
    assert resumed.exit_code == 0, resumed.output
    if entry == "auto-dev":
        token = json.loads(resumed.output)["token"]
        assert (
            runner.invoke(codexspec.app, ["_auto-dev-helper", "release"], input=json.dumps({"token": token})).exit_code
            == 0
        )


def test_sync_cli_requires_analysis_and_preserves_pending_on_refusal(tmp_path, monkeypatch):
    repo, _, service, token = services(tmp_path)
    work = service.workspace.path
    before = diverge(repo, work)
    monkeypatch.chdir(work)
    runner = CliRunner()

    def invoke(action, body):
        return runner.invoke(codexspec.app, ["_auto-dev-helper", action], input=json.dumps(body))

    assert json.loads(invoke("sync-default", {"token": token}).output)["state"] == "needs_verification"
    old = invoke("continue-sync", {"token": token, "checks_passed": True})
    assert old.exit_code == 1 and "analysis_required" in old.output
    analyzed = snapshot(work)
    message = "chore: integrate main\n\nInclude main.txt from main.\n"
    done = invoke("continue-sync", {"token": token, "checks_passed": True, "analysis": analyzed, "message": message})
    assert done.exit_code == 0, done.output
    assert git(work, "rev-parse", "HEAD").stdout.strip() != before
    assert git(work, "show", "-s", "--format=%B", "HEAD").stdout.rstrip() == message.rstrip()


def test_initial_merge_failure_retains_journal_and_can_retry(tmp_path):
    from codexspec.automation import finish_initial_workspace

    repo, local, _ = diverged(tmp_path)
    context = locate_repository(repo)
    with pytest.raises(AutomationError, match="initial_merge_requires"):
        ensure_dedicated_workspace(context)
    work = context.worktree_path
    proof = evidence(work)
    bad = {**proof, "checks": [{"command": "fixture", "exit_code": 1}]}
    with pytest.raises(AutomationError, match="verification_failed"):
        finish_initial_workspace(context, bad)
    assert (context.coordination_dir / "initial-merge.json").exists()
    assert git(work, "rev-parse", "HEAD").stdout.strip() == local
    owner = AutoDevOwnership(context)
    token = owner.acquire()
    with pytest.raises(AutomationError, match="already_running"):
        finish_initial_workspace(context, proof)
    owner.release(token)
    assert finish_initial_workspace(context, proof)["status"] == "ready"
