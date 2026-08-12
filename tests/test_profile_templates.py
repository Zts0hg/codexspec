"""Template-invariant tests for profile consumption (T-005).

Scenario numbers refer to T-005 in
.codexspec/specs/2026-0812-14054p-profile-consumption/tasks.md.
"""

from pathlib import Path

from codexspec.profile import render_profile_block

ROOT = Path(__file__).parent.parent
COMMANDS = ROOT / "templates" / "commands"


def _cmd(name: str) -> str:
    return (COMMANDS / f"{name}.md").read_text(encoding="utf-8")


def test_specify_consults_profile() -> None:
    """Scenario 1 (REQ-005 / SC-004a)."""
    content = _cmd("specify")
    assert "## Consult Project Profile" in content
    assert ".codexspec/profile" in content


def test_no_other_stage_consults_profile() -> None:
    """Scenario 2 (CON-003 / SC-004b).

    The pure downstream SDD stages must not reference the profile at all, and no
    template other than specify may carry a profile-consumption section. (The
    distill-write mention inside implement-tasks/commit-staged/pr is not a read.)
    """
    pure_stages = [
        "generate-spec",
        "spec-to-plan",
        "plan-to-tasks",
        "review-spec",
        "review-plan",
        "review-tasks",
        "review-code",
    ]
    for name in pure_stages:
        assert ".codexspec/profile" not in _cmd(name), f"{name} unexpectedly references the profile"

    consumers = [p.stem for p in COMMANDS.glob("*.md") if "## Consult Project Profile" in _cmd(p.stem)]
    assert consumers == ["specify"], f"only specify may consult the profile, got: {consumers}"


def test_evolve_still_reads_vetted_profile() -> None:
    """Scenario 3 (NFR-003 / SC-005): evolve's vetted-profile consumption is intact."""
    content = _cmd("evolve")
    assert "profile" in content
    assert "vetted" in content


def test_no_staleness_surface_codex_uses_pointer() -> None:
    """Scenario 4 (SC-006): the Codex constraints delivery inlines nothing (no @import)."""
    codex_block = render_profile_block("codex")
    assert "@import" not in codex_block
    assert "@.codexspec" not in codex_block
    # Claude, by contrast, delivers constraints via @import (guaranteed + auto-fresh)
    assert "@.codexspec/profile/constraints.md" in render_profile_block("claude")
