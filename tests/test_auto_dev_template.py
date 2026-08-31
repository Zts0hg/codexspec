"""Contract tests for the auto-dev command and run-local delegation."""

from pathlib import Path

ROOT = Path(__file__).parents[1]
TEMPLATE = (ROOT / "templates/commands/auto-dev.md").read_text(encoding="utf-8")
STAGES = (
    "generate-spec.md",
    "spec-to-design.md",
    "spec-to-plan.md",
    "plan-to-tasks.md",
    "implement-tasks.md",
)


def test_auto_dev_owns_run_and_resumes_in_progress_first() -> None:
    for phrase in (
        "_auto-dev-helper acquire",
        "another live run",
        "returned `merge_recovery`",
        "`needs_verification`",
        "interrupted synchronization merge",
        "`prepare-sync-verification`",
        "If any block is `in_progress`, resume it",
        "never change it back to pending",
        "create the already recorded directory",
        "reconstruct its `requirements.md`",
        "sync-default",
        "first current pending block",
        "release ownership",
        "returned `heartbeat_interval_seconds`",
        "returned `worktree_path` as the working directory",
        "never to the checkout that invoked `auto-dev`",
    ):
        assert phrase in TEMPLATE
    assert "Never run `git add`" in TEMPLATE


def test_auto_dev_extracts_exact_requirements_and_runs_all_stages() -> None:
    assert "after exactly the three blueprint-managed" in TEMPLATE
    assert "directly to its `requirements.md`" in TEMPLATE
    for stage in ("generate-spec", "spec-to-design", "spec-to-plan", "plan-to-tasks", "implement-tasks"):
        assert f"/codexspec:{stage}" in TEMPLATE
    assert "CODEXSPEC_AUTO_DEV_DELEGATION" in TEMPLATE
    assert "must not read, write, toggle, or rely on `workflow.auto_next`" in TEMPLATE


def test_auto_dev_has_completion_fresh_read_and_stop_preservation() -> None:
    assert '"new_status":"completed"' in TEMPLATE
    assert "re-inspect the complete blueprint" in TEMPLATE
    assert "Requirements appended during this run join the same run" in TEMPLATE
    assert "preserve the `in_progress` status" in TEMPLATE
    assert "Never ask the user" in TEMPLATE


def test_every_stage_has_uniform_delegation_and_direct_compatibility() -> None:
    for filename in STAGES:
        content = (ROOT / "templates/commands" / filename).read_text(encoding="utf-8")
        assert "CODEXSPEC_AUTO_DEV_DELEGATION" in content
        assert "Direct invocations are unchanged" in content
        assert "workflow.auto_next" in content
