"""Historical recall policy and installation contracts, not LLM recall measurements."""

from pathlib import Path

import pytest
from typer.testing import CliRunner

from codexspec import app

ROOT = Path(__file__).resolve().parents[1]
START = "<!-- CODEXSPEC SPECS START -->"
END = "<!-- CODEXSPEC SPECS END -->"
COMMANDS = (
    "specify",
    "quick",
    "blueprint",
    "generate-spec",
    "spec-to-design",
    "design-to-plan",
    "plan-to-tasks",
    "implement-tasks",
    "debug",
    "review-spec",
    "review-design",
    "review-plan",
    "review-tasks",
    "review-code",
    "analyze",
)


@pytest.mark.parametrize("ai", ["claude", "codex", "both"])
def test_t001_s1_s2_init_installs_once_and_preserves_project_content(tmp_path, ai):
    runner = CliRunner()
    for name in ("CLAUDE.md", "AGENTS.md"):
        (tmp_path / name).write_text("# Project\n\nKeep my rules and C:\\project.\n", encoding="utf-8")
    history = tmp_path / ".codexspec/specs/2026-0101-1200ab-old/requirements.md"
    history.parent.mkdir(parents=True)
    history.write_text("PRIVATE HISTORY MUST NOT BE INLINED\n", encoding="utf-8")
    args = ["init", str(tmp_path), "--ai", ai, "--no-git", "--force", "--lang", "en"]
    first = runner.invoke(app, args)
    assert first.exit_code == 0, first.stdout
    before = {name: (tmp_path / name).read_bytes() for name in ("CLAUDE.md", "AGENTS.md")}
    again = runner.invoke(app, args)
    assert again.exit_code == 0, again.stdout
    blocks = []
    for name, integration in (("CLAUDE.md", "claude"), ("AGENTS.md", "codex")):
        content = (tmp_path / name).read_text(encoding="utf-8")
        assert (tmp_path / name).read_bytes() == before[name]
        assert "Keep my rules and C:\\project." in content
        assert "PRIVATE HISTORY MUST NOT BE INLINED" not in content
        if ai in (integration, "both"):
            assert content.count(START) == content.count(END) == 1
            assert "<!-- CODEXSPEC PROFILE START -->" in content
            assert "<!-- CODEXSPEC COMMITS START -->" in content
            blocks.append(content.split(START)[1].split(END)[0])
        else:
            assert START not in content
    if ai == "both":
        assert blocks[0] == blocks[1]
    assert history.read_text(encoding="utf-8") == "PRIVATE HISTORY MUST NOT BE INLINED\n"
    assert START not in (tmp_path / ".codexspec/memory/constitution.md").read_text(encoding="utf-8")


def test_t001_s3_replace_only_own_block_and_preserve_backslashes(tmp_path):
    from codexspec.specs_context import inject_specs_context, render_specs_context

    path = tmp_path / "AGENTS.md"
    prefix = b"# User rules\r\nLiteral \\g<0> and C:\\work\r\n"
    suffix = b"\r\n<!-- OTHER BLOCK -->\r\nKeep this.\r\n"
    path.write_bytes(prefix + f"{START}\nold rule\n{END}".encode() + suffix)
    inject_specs_context(path)
    expected = prefix + render_specs_context().encode() + suffix
    assert path.read_bytes() == expected
    inject_specs_context(path)
    assert path.read_bytes() == expected


def test_t001_s4_fresh_context_is_bounded_and_complete(tmp_path):
    from codexspec.specs_context import inject_specs_context, render_specs_context

    path = tmp_path / "CLAUDE.md"
    inject_specs_context(path)
    block = render_specs_context()
    assert path.read_text(encoding="utf-8") == block + "\n"
    assert block.startswith(START) and block.endswith(END)
    for scenario in ("ordinary conversation", "requirements", "design", "debugging", "review"):
        assert scenario in block
    assert ".codexspec/specs/" in block
    assert "first matching document" in block
    assert "related features" in block


@pytest.mark.parametrize(
    ("case", "clauses"),
    [
        ("T-004-S2", ("Older unchanged requirements remain applicable", "unrelated later feature")),
        ("T-004-S3", ("Combine later additions", "earlier requirements")),
        ("T-004-S4", ("later explicit change", "same matter", "earlier rationale")),
        ("T-004-S5", ("latest explicit decision", "never override", "Do not ask again")),
        ("T-004-S6", ("relationship is unclear", "specific difference", "expired")),
        ("T-004-S7", ("code and tests", "plans alone do not prove implementation")),
        ("T-004-S8", ("Reuse prepared background", "scope changes", "new evidence", "insufficient")),
        ("T-004-S9", ("mechanical edits", "missing or incomplete", "invent")),
    ],
    ids=lambda value: value if isinstance(value, str) else None,
)
def test_history_scenario_policy_contract(case, clauses):
    """Assert necessary decision rules for each case; does not execute an LLM."""
    from codexspec.specs_context import render_specs_context

    policy = " ".join(render_specs_context().split())
    for clause in clauses:
        assert clause in policy, f"{case}: missing policy clause {clause!r}"


@pytest.mark.parametrize("command", COMMANDS)
def test_workflow_reminder_preserves_current_authority_and_scope(command):
    content = (ROOT / f"templates/commands/{command}.md").read_text(encoding="utf-8")
    assert "## Historical Specs Before Decisions" in content
    section = content.split("## Historical Specs Before Decisions", 1)[1].split("\n## ", 1)[0]
    for rule in (
        ".codexspec/specs/",
        "Reuse sufficient background",
        "latest explicit user decision",
        "selected target",
        "staged-only",
        "current requirements",
    ):
        assert rule in section
