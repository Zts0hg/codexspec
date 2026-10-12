"""Distribution contracts for the unified analysis handoff."""

from pathlib import Path

ROOT = Path(__file__).parents[1] / "templates/commands"


def test_all_commit_workflows_invoke_common_analysis():
    for name in ("implement-tasks", "auto-dev", "blueprint"):
        content = (ROOT / f"{name}.md").read_text()
        assert "/codexspec:commit-staged" in content
    for name in ("auto-dev", "blueprint"):
        content = (ROOT / f"{name}.md").read_text()
        assert "preparation_id" in content
        assert "analyzed_tree" in content
        assert "index_file" in content


def test_commit_analysis_owns_no_staging_and_requires_reanalysis():
    content = (ROOT / "commit-staged.md").read_text()
    assert "selected runtime with `snapshot`" in content
    assert "selected runtime with `commit`" in content
    assert "${CLAUDE_PLUGIN_ROOT}/.claude/commands/codexspec/commit-staged-helper.py" in content
    assert ".codexspec/scripts/commit-staged-helper.py" in content
    assert "codexspec _commit-staged-helper" in content
    assert "caller" in content
    assert "body" in content
    assert "analyze again" in content
    assert "Retry the commit with the same message" not in content
    assert "re-stage ONLY" not in content
