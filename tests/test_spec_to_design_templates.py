"""Contract tests for the spec-to-design stage and its downstream pipeline edits.

Scenario numbers refer to the Test Scenarios in
.codexspec/specs/2026-0812-2114vj-spec-to-design/tasks.md.
"""

from pathlib import Path

from typer.testing import CliRunner

from codexspec import app

ROOT = Path(__file__).parent.parent
COMMANDS = ROOT / "templates" / "commands"
DOCS = ROOT / "templates" / "docs"


def read_command(name: str) -> str:
    return (COMMANDS / f"{name}.md").read_text(encoding="utf-8")


def read_doc(name: str) -> str:
    return (DOCS / f"{name}.md").read_text(encoding="utf-8")


def section(content: str, heading: str) -> str:
    """Return the body of a `## heading` section up to the next `## `."""
    assert heading in content, f"missing section: {heading}"
    return content.split(heading, 1)[1].split("\n## ", 1)[0]


# --- T1.1: design-template.md ---


def test_design_template_fixed_core_headings() -> None:
    """S1.1.1: the fixed core is always present."""
    content = read_doc("design-template")
    for heading in ("## Architecture & Components", "## Key Design Decisions", "## Requirements Coverage"):
        assert heading in content


def test_design_template_optional_sections_marked_include_if() -> None:
    """S1.1.2: optional sections exist but are marked include-when-relevant."""
    content = read_doc("design-template")
    for optional in ("Data Models", "API / Interface Contracts", "Sequence & Data Flow", "Cross-Cutting Design"):
        assert optional in content
    assert "*(include if" in content


def test_design_template_has_covers_and_coverage_table() -> None:
    """S1.1.3: Covers usage and a Requirements Coverage table."""
    content = read_doc("design-template")
    assert "Covers" in content and "REQ-xxx" in content
    assert "| Spec Requirement | Design Coverage |" in content


# --- T1.2: spec-to-design.md ---


def test_spec_to_design_language_preference() -> None:
    """S1.2.1."""
    assert "## Language Preference" in read_command("spec-to-design")


def test_spec_to_design_invokes_review_design() -> None:
    """S1.2.2."""
    assert "/codexspec:review-design" in read_command("spec-to-design")


def test_spec_to_design_auto_next_invokes_spec_to_plan() -> None:
    """S1.2.3."""
    content = read_command("spec-to-design")
    auto_next = section(content, "## Auto-Next Chain Advance")
    assert "/codexspec:spec-to-plan" in auto_next


def test_spec_to_design_authority_ranks_requirements_spec_above_design_decisions() -> None:
    """S1.2.4: design-level decisions rank below requirements and spec."""
    body = section(read_command("spec-to-design"), "## Authority and Stop Conditions")
    req_i = body.index("Confirmed `requirements.md`")
    spec_i = body.index("`spec.md`")
    design_dec_i = body.index("Design-level technical decisions")
    assert req_i < design_dec_i and spec_i < design_dec_i


def test_spec_to_design_stops_on_product_intent_change() -> None:
    """S1.2.5."""
    content = read_command("spec-to-design")
    assert "change confirmed scope, behavior, constraints, or trade-offs" in content


def test_spec_to_design_has_no_branch_safety_check() -> None:
    """S1.2.6."""
    assert "Git Branch Safety Check" not in read_command("spec-to-design")


# --- T1.3: review-design.md ---


def test_review_design_language_preference() -> None:
    """S1.3.1."""
    assert "## Language Preference" in read_command("review-design")


def test_review_design_saves_review_design_report() -> None:
    """S1.3.2."""
    assert "review-design.md" in read_command("review-design")


def test_review_design_score_formula_is_verbatim() -> None:
    """S1.3.3: the Compatibility Score formula is identical to review-plan's."""
    review_design = read_command("review-design")
    for line in (
        "- No defects: `100`",
        "- Minor only: `max(80, 100 - 3 × Minor)`",
        "- Warning present: `max(50, 79 - 8 × (Warning - 1) - 3 × Minor)`",
        "- Critical present: `max(0, 49 - 15 × (Critical - 1) - 8 × Warning - 3 × Minor)`",
    ):
        assert line in review_design
        assert line in read_command("review-plan")


def test_review_design_authority_ranks_requirements_spec_above_design_decisions() -> None:
    """S1.3.4."""
    body = section(read_command("review-design"), "## Review Authority")
    req_i = body.index("Confirmed requirements")
    spec_i = body.index("Specification")
    design_dec_i = body.index("Design-level technical decisions")
    assert req_i < design_dec_i and spec_i < design_dec_i


# --- T2.1: generate-spec auto_next retarget ---


def test_generate_spec_auto_next_targets_spec_to_design() -> None:
    """S2.1.1 / S2.1.2."""
    auto_next = section(read_command("generate-spec"), "## Auto-Next Chain Advance")
    assert "/codexspec:spec-to-design" in auto_next
    assert "/codexspec:spec-to-plan" not in auto_next


# --- T2.2: spec-to-plan narrowed ---


def test_spec_to_plan_reads_design() -> None:
    """S2.2.1."""
    assert "`design.md`" in read_command("spec-to-plan")


def test_spec_to_plan_authority_design_below_spec_above_plan_decisions() -> None:
    """S2.2.2."""
    body = section(read_command("spec-to-plan"), "## Authority and Stop Conditions")
    spec_i = body.index("`spec.md`")
    design_i = body.index("`design.md`")
    plan_dec_i = body.index("Plan-level technical decisions")
    assert spec_i < design_i < plan_dec_i


def test_spec_to_plan_uses_design_covers_notation() -> None:
    """S2.2.3."""
    assert "Covers: REQ-xxx; Design:" in read_command("spec-to-plan")


def test_spec_to_plan_role_is_implementation_planner() -> None:
    """S2.2.4."""
    content = read_command("spec-to-plan")
    assert "implementation planner" in content
    assert "constrained technical designer" not in content


# --- T2.3: plan templates slimmed ---


def test_plan_detailed_removes_design_only_sections() -> None:
    """S2.3.1."""
    content = read_doc("plan-template-detailed")
    for design_only in ("## Architecture Overview", "## Component Structure", "## Data Models", "## API Contracts"):
        assert design_only not in content


def test_plan_detailed_retains_plan_sections() -> None:
    """S2.3.2."""
    content = read_doc("plan-template-detailed")
    assert "## Implementation Phases" in content
    assert "## Requirements Coverage" in content


def test_plan_simple_removes_architecture_and_retitled() -> None:
    """S2.3.3."""
    content = read_doc("plan-template-simple")
    assert "## Architecture" not in content
    assert "# Implementation Plan" in content


# --- T2.4: plan-to-tasks reads design ---


def test_plan_to_tasks_reads_design_between_spec_and_plan() -> None:
    """S2.4.1 / S2.4.2."""
    body = section(read_command("plan-to-tasks"), "## Feature Resolution and Inputs")
    spec_i = body.index("`spec.md`")
    design_i = body.index("`design.md`")
    plan_i = body.index("`plan.md`")
    assert spec_i < design_i < plan_i


# --- T2.5: analyze chain deepened ---


def test_analyze_chain_includes_design_between_req_and_plan() -> None:
    """S2.5.1."""
    content = read_command("analyze")
    req_i = content.index("-> REQ/NFR Sources")
    design_i = content.index("-> design Covers")
    plan_i = content.index("-> plan Covers")
    assert req_i < design_i < plan_i


def test_analyze_loads_design_and_never_edits_requirements() -> None:
    """S2.5.2 / S2.5.3."""
    content = read_command("analyze")
    assert "- `design.md`" in content
    assert "never modifies `requirements.md`" in content


# --- T2.6: implement-tasks authority ---


def test_implement_tasks_reads_design_authority_below_spec_above_plan() -> None:
    """S2.6.1 / S2.6.2."""
    body = section(read_command("implement-tasks"), "## Input Documents and Authority")
    spec_i = body.index("`spec.md`")
    design_i = body.index("`design.md`")
    plan_i = body.index("Approved `plan.md`")
    assert spec_i < design_i < plan_i


# --- T2.7: review-plan / review-tasks authority ---


def test_review_plan_authority_and_design_aware_fidelity() -> None:
    """S2.7.1 / S2.7.2."""
    content = read_command("review-plan")
    order = content.split("Authority order:", 1)[1].split("\n## ", 1)[0]
    assert order.index("Specification") < order.index("`design.md`")
    assert "covers the confirmed `design.md` components" in content


def test_review_tasks_authority_design_below_spec() -> None:
    """S2.7.3."""
    order = read_command("review-tasks").split("Authority order:", 1)[1].split("\n## ", 1)[0]
    assert order.index("Specification") < order.index("`design.md`")


# --- T3.3: init copies the design template ---


def test_init_copies_design_template(tmp_path: Path) -> None:
    """S3.3.1: `codexspec init --force` copies design-template.md into the project docs."""
    runner = CliRunner()
    result = runner.invoke(app, ["init", str(tmp_path), "--force", "--no-git", "--lang", "en"])
    assert result.exit_code == 0, result.stdout
    assert (tmp_path / ".codexspec" / "templates" / "docs" / "design-template.md").exists()
