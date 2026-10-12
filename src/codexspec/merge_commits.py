"""Verify a prepared merge and finalize its analyzed index without staging."""

from pathlib import Path
from typing import Any, Sequence

from .commit_runtime import AutomationError, GitRunner, commit_snapshot, snapshot


def finish_verified_merge(
    repository: Path, verification: dict[str, Any], baselines: Sequence[str], *, merge_hook: bool = False
) -> None:
    git = GitRunner()
    checks = verification.get("checks") if isinstance(verification, dict) else None
    if (
        not isinstance(checks, list)
        or not checks
        or any(
            not isinstance(check, dict)
            or not isinstance(check.get("command"), str)
            or not check["command"].strip()
            or type(check.get("exit_code")) is not int
            or check["exit_code"] != 0
            for check in checks
        )
    ):
        raise AutomationError("baseline_verification_failed")
    head = git.run(repository, "rev-parse", "HEAD").stdout.strip()
    merging = git.run(repository, "rev-parse", "--verify", "MERGE_HEAD", check=False).returncode == 0
    tree = git.run(
        repository, "write-tree" if merging else "rev-parse", *(() if merging else ("HEAD^{tree}",))
    ).stdout.strip()
    clean = git.run(repository, "diff", "--quiet", check=False).returncode == 0
    if verification.get("head") != head or verification.get("tree") != tree or not clean:
        raise AutomationError("baseline_verification_stale_or_unresolved")
    if merging:
        analyzed = verification.get("analysis")
        if not isinstance(analyzed, dict) or "message" not in verification:
            raise AutomationError("analysis_required")
        current = snapshot(repository, use_caller_index=False)
        if current != analyzed or [head, *current.get("merge_heads", [])] != list(baselines):
            raise AutomationError("stale_analysis")
        commit_snapshot(repository, analyzed, verification["message"], use_caller_index=False, merge_hook=merge_hook)
        head = git.run(repository, "rev-parse", "HEAD").stdout.strip()
    if git.run(repository, "status", "--porcelain", "--untracked-files=no").stdout:
        raise AutomationError("baseline_verification_stale_or_unresolved")
    for baseline in baselines:
        if git.run(repository, "merge-base", "--is-ancestor", baseline, head, check=False).returncode:
            raise AutomationError("baseline_history_not_integrated", baseline)
