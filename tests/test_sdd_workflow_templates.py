"""Contract tests for the requirements-first SDD workflow."""

import json
from pathlib import Path

import pytest

from codexspec.translator import extract_frontmatter_fields

ROOT = Path(__file__).parent.parent
COMMANDS = ROOT / "templates" / "commands"
DOCS = ROOT / "templates" / "docs"
TRANSLATIONS = ROOT / "templates" / "translations"
SUPPORTED_LANGS = ["en", "zh-CN", "ja", "ko", "de", "es", "fr", "pt-BR"]


def read_command(name: str) -> str:
    return (COMMANDS / f"{name}.md").read_text(encoding="utf-8")


def _template_frontmatter(command: str) -> tuple[str | None, str | None]:
    fields = extract_frontmatter_fields(read_command(command))
    return fields.get("description"), fields.get("argument-hint")


def read_doc(name: str) -> str:
    return (DOCS / f"{name}.md").read_text(encoding="utf-8")


def test_requirements_template_defines_authoritative_decision_record():
    content = read_doc("requirements-template")

    for marker in [
        "NEED-",
        "CON-",
        "DEC-",
        "OUT-",
        "OPEN-",
        "confirmed",
        "superseded",
        "User Evidence",
    ]:
        assert marker in content

    for entry_id in ["NEED-001", "CON-001", "DEC-001", "OUT-001"]:
        entry = content.split(entry_id, 1)[1].split("\n## ", 1)[0]
        assert "**Status**: open" in entry


def test_specify_creates_and_confirms_requirements_record():
    content = read_command("specify")

    assert "requirements.md" in content
    assert "create-new-feature" in content
    assert "stage summary" in content.lower()
    assert "confirmed" in content
    assert "Do not generate `spec.md`" in content


@pytest.mark.parametrize(
    ("command", "required_inputs", "trace_marker"),
    [
        ("generate-spec", ["requirements.md"], "Sources:"),
        ("spec-to-plan", ["requirements.md", "spec.md"], "Covers:"),
        ("plan-to-tasks", ["requirements.md", "spec.md", "plan.md"], "Covers:"),
    ],
)
def test_generation_commands_enforce_upstream_traceability(command, required_inputs, trace_marker):
    content = read_command(command)

    for required_input in required_inputs:
        assert required_input in content
    assert trace_marker in content
    assert "confirmed" in content
    assert "stop" in content.lower()
    assert "maximum of two" in content.lower()


@pytest.mark.parametrize("command", ["review-spec", "review-plan", "review-tasks"])
def test_review_commands_require_evidence_and_separate_advisories(command):
    content = read_command(command)

    for field in ["Evidence", "Location", "Mismatch", "Impact", "Remediation"]:
        assert field in content
    assert "Risk Advisories" in content
    assert "Design Opportunities" in content
    assert "Advisories do not affect" in content
    assert "same root cause" in content
    assert "Compatibility Score" in content
    assert "Quality Score" not in content


@pytest.mark.parametrize("command", ["review-spec", "review-plan", "review-tasks"])
def test_review_commands_remove_fixed_template_deductions(command):
    content = read_command(command)

    forbidden = [
        "Missing architecture diagram: -15",
        "Missing dependency graph: -10",
        "Technology without version constraint: -5",
        "Component without test task: -12",
        "Independent task missing [P] marker: -3",
    ]
    for rule in forbidden:
        assert rule not in content


def test_compatibility_score_is_derived_from_verified_defects():
    for command in ["review-spec", "review-plan", "review-tasks"]:
        content = read_command(command)
        for status in ["PASS", "PASS_WITH_WARNINGS", "NEEDS_REVISION", "BLOCKED"]:
            assert status in content
        assert "100 - 3" in content
        assert "79 - 8" in content
        assert "49 - 15" in content
        assert "Advisory" in content
        assert "does not affect the score" in content


def test_adjacent_commands_preserve_requirements_authority():
    clarify = read_command("clarify")
    quick = read_command("quick")
    analyze = read_command("analyze")
    implement = read_command("implement-tasks")

    assert "Update `requirements.md` first" in clarify
    assert "confirmed requirement summary" in quick
    assert "requirements.md" in analyze
    assert "end-to-end traceability" in analyze.lower()
    assert "requirements.md" in implement
    assert "explicit path" in implement.lower()
    assert "current branch" in implement.lower()
    assert "legacy spec-only" in implement.lower()
    assert "latest/only" not in implement.lower()
    assert "latest feature" not in implement.lower()


def test_implement_tasks_invokes_complete_feature_defect_gate():
    """The completion gate reviews the complete feature, including non-code files."""
    content = read_command("implement-tasks")
    compact = " ".join(content.split())

    assert "Final Code Review Loop" in content
    assert "/codexspec:review-code --feature <feature-dir>" in content
    assert "complete feature target" in compact
    assert "committed, staged, unstaged, and untracked" in compact
    assert "documentation and configuration" in compact
    assert "Do not pass `--audit`" in content
    assert "Do not pass a narrowed selector" in compact

    for legacy in [
        "no code to review",
        "analyzable source extensions",
        "CRITICAL, HIGH, and MEDIUM",
        "report-only",
        "maintainability, readability, or testability",
        "two-round limit",
        "fix-and-review rounds",
        "Quality Score",
    ]:
        assert legacy not in content


def test_implement_tasks_validates_result_envelope_and_review_topology():
    """Prose, scorecards, malformed output, and shared reviews cannot complete work."""
    content = read_command("implement-tasks")
    compact = " ".join(content.split())

    for field in [
        "schema_version",
        "mode",
        "verdict",
        "target",
        "requirements_coverage",
        "verification",
        "finding_counts",
        "coverage_gap_count",
        "review_context",
        "reviewers",
    ]:
        assert f"`{field}`" in content

    assert "exactly one `<review-code-result>`" in content
    assert "schema version `1`" in content
    assert "`mode: defect`" in content
    assert "target and feature context match" in compact
    assert "`requirements_coverage.status: complete`" in content
    assert "`verification.status: complete`" in content
    assert "`review_context: isolated`" in content
    assert "primary reviewer is `complete`" in compact
    assert "required specialist" in content
    assert "all P0-P3 counts are zero" in compact
    assert "prose cannot override" in compact.lower()
    assert "INCONCLUSIVE" in content


def test_implement_tasks_verifies_findings_before_test_safe_repairs():
    """Only reproduced findings are fixed, with verification appropriate to the artifact."""
    content = read_command("implement-tasks")
    compact = " ".join(content.split())

    assert "independently verify" in content
    assert "trigger, selected-change attribution, impact, and binding obligation" in compact
    assert "Do not edit for an unverified finding" in content
    assert "reproducing regression test" in content
    assert "red-green-refactor" in content
    assert "documentation and non-code configuration" in compact
    assert "applicable deterministic checks" in content
    assert "targeted checks and all project-mandated checks" in compact
    assert "green full-suite baseline" in content
    assert "fresh isolated reviewer" in content
    assert "complete feature target" in content


def test_implement_tasks_uses_progress_guards_and_only_pass_succeeds():
    """The loop is progress-based and every non-PASS terminal state remains blocking."""
    content = read_command("implement-tasks")
    compact = " ".join(content.split())

    for stop_guard in [
        "same defect survives two verified fixes",
        "two consecutive rounds make no substantive progress",
        "new product or architecture decision",
        "same independently refuted false positive recurs",
    ]:
        assert stop_guard in compact
    assert "transient `INCONCLUSIVE` cause" in content
    assert "retry it up to two times" in compact.lower()
    assert "reset the transient retry count" in compact.lower()
    assert "continue while substantive progress" in compact.lower()
    assert "final valid `PASS` envelope" in content
    assert "No finding may be deferred" in content
    assert "FAIL" in content
    assert "INCONCLUSIVE" in content
    assert "must not be converted to success" in content


def test_implement_tasks_preserves_per_task_tdd_and_issue_recording():
    content = read_command("implement-tasks")
    compact = " ".join(content.split())

    assert "TDD Workflow (Per Task)" in content
    assert "Review & Refactor" in content
    assert "Issue Recording" in content
    assert "green full-suite baseline" in compact
    assert "commits remain outside verdict logic" in compact.lower()


@pytest.mark.parametrize("language", ["de", "es", "fr", "ja", "ko", "pt-BR"])
def test_localized_guides_describe_requirements_first_workflow(language):
    guide = (ROOT / "docs" / language / "user-guide" / "commands.md").read_text(encoding="utf-8")
    workflow = (ROOT / "docs" / language / "user-guide" / "workflow.md").read_text(encoding="utf-8")

    assert "requirements.md" in guide
    assert "requirements.md" in workflow
    assert "specify" in guide.lower()
    assert "generate-spec" in guide.lower()
    assert "requirements.md" in guide[guide.lower().index("specify") :]


def test_document_templates_use_consistent_requirement_and_task_policies():
    spec = read_doc("spec-template-detailed")
    tasks = read_doc("tasks-template-detailed")

    assert "REQ-001" in spec
    assert "FR-001" not in spec
    assert "Sources:" in spec
    assert "Tests are required when" in tasks
    assert "only one primary file" not in tasks
    assert "single verifiable outcome" in tasks


def test_platform_scripts_share_feature_resolution_contract():
    bash_common = (ROOT / "scripts" / "bash" / "common.sh").read_text(encoding="utf-8")
    bash_create = (ROOT / "scripts" / "bash" / "create-new-feature.sh").read_text(encoding="utf-8")
    ps_common = (ROOT / "scripts" / "powershell" / "common.ps1").read_text(encoding="utf-8")
    ps_check = (ROOT / "scripts" / "powershell" / "check-prerequisites.ps1").read_text(encoding="utf-8")
    ps_create = (ROOT / "scripts" / "powershell" / "create-new-feature.ps1").read_text(encoding="utf-8")
    architecture = (ROOT / "docs" / "en" / "development" / "scripts-architecture.md").read_text(encoding="utf-8")

    assert "CODEXSPEC_FEATURE" in bash_common
    assert "[0-9]{4}-[0-9]{4}-[0-9]{4}" in bash_common
    assert "ASCII letters or numbers" in bash_create
    assert "Test-FeatureName" in ps_common
    assert "REQUIREMENTS" in ps_common
    assert "[string]$Feature" in ps_check
    assert "PathType Leaf" in ps_common
    assert '$featureId = "$timestamp$suffix"' in ps_create
    assert "ASCII letters or numbers" in ps_create
    assert "requirements.md" in ps_create
    assert "^[0-9]{4}-[0-9]{4}-[0-9]{4}[a-z0-9]{2}-" in ps_common
    assert "Sequential `NNN-name` identifiers are not supported" in architecture
    assert "Legacy compatibility applies to artifacts" in architecture
    assert "The full feature name identifies a workspace" in architecture


# --- Translation-catalog drift guards ---------------------------------------
# Regression for the bug where a redesign updated template frontmatter but the
# translation JSONs (the cache `codexspec init` copies from for non-English
# installs) were not synced, so re-running init kept regenerating stale
# descriptions forever. en.json is the canonical English catalog; localized
# JSONs must mirror its command coverage field-for-field.


def test_en_translation_catalog_matches_template_frontmatter():
    """en.json must exactly track every distributed command's template frontmatter.

    If a template's description/argument-hint changes, en.json must change with
    it or this test fails — forcing the author to also update the localized
    JSONs rather than silently leaving installs on stale strings.
    """
    en = json.loads((TRANSLATIONS / "en.json").read_text(encoding="utf-8"))

    for command_file in COMMANDS.glob("*.md"):
        command = command_file.stem
        if command not in en:
            continue  # command has no catalog entry (e.g. maintainer-only commands)
        description, argument_hint = _template_frontmatter(command)
        assert en[command]["description"] == description, (
            f"en.json/{command} description drifted from template:\n"
            f"  template: {description}\n  en.json : {en[command]['description']}"
        )
        if argument_hint is not None:
            assert en[command].get("argument-hint") == argument_hint, (
                f"en.json/{command} argument-hint drifted from template:\n"
                f"  template: {argument_hint}\n  en.json : {en[command].get('argument-hint')}"
            )


@pytest.mark.parametrize("language", ["zh-CN", "ja", "ko", "de", "es", "fr", "pt-BR"])
def test_localized_translation_catalogs_cover_every_command(language):
    """Every command cataloged in en.json must appear in each localized JSON with a
    non-empty description, and a non-empty argument-hint whenever en.json has one.

    This keeps `codexspec init` from regenerating a stale or missing description for
    any supported language.
    """
    en = json.loads((TRANSLATIONS / "en.json").read_text(encoding="utf-8"))
    localized = json.loads((TRANSLATIONS / f"{language}.json").read_text(encoding="utf-8"))

    cataloged = [
        command
        for command, value in en.items()
        if isinstance(value, dict) and "description" in value and (COMMANDS / f"{command}.md").exists()
    ]

    assert cataloged, "sanity: en.json should catalog at least one command"

    for command in cataloged:
        assert command in localized, f"{language}.json is missing command '{command}' (present in en.json)"
        assert localized[command].get("description"), f"{language}.json/{command} has an empty description"
        if en[command].get("argument-hint"):
            assert localized[command].get("argument-hint"), (
                f"{language}.json/{command} has an empty argument-hint (en.json declares one)"
            )


def test_command_templates_split_interaction_and_document_language():
    """Non-commit templates use the unified Language Preference block distinguishing
    interaction vs document language; commit-affected templates keep the commit-priority
    block unchanged."""
    commit_templates = {"commit-staged", "pr"}

    for command_file in COMMANDS.glob("*.md"):
        command = command_file.stem
        content = command_file.read_text(encoding="utf-8")

        if command in commit_templates:
            # Commit path is unchanged (REQ-008): still references language.commit priority.
            assert "language.commit" in content, f"{command} lost its commit-language priority block"
        else:
            assert "language.interaction" in content, (
                f"{command} must reference language.interaction in its Language Preference block"
            )
            assert "language.document" in content, (
                f"{command} must reference language.document in its Language Preference block"
            )


# --- auto-next chain advance -----------------------------------------------
# `workflow.auto_next`: when enabled and a stage passes, a command auto-invokes
# the next command in the SDD chain (specify -> generate-spec -> spec-to-plan
# -> plan-to-tasks -> implement-tasks). Mirrors the analyze auto-invoke pattern
# added in #17. The source templates live in templates/commands/; installed
# forms live under .claude/commands/codexspec/ (slash) and .agents/skills/
# codexspec-*/ ($mention).

_AUTO_NEXT_SUCCESSOR = {
    "specify": "generate-spec",
    "generate-spec": "spec-to-plan",
    "spec-to-plan": "plan-to-tasks",
    "plan-to-tasks": "implement-tasks",
}


@pytest.mark.parametrize("command", list(_AUTO_NEXT_SUCCESSOR))
def test_chain_commands_have_auto_next_advance(command):
    content = read_command(command)
    successor = _AUTO_NEXT_SUCCESSOR[command]

    assert "Auto-Next Chain Advance" in content
    assert "workflow.auto_next" in content
    # Opt-in: only literal `true` enables (default false / backwards compatible).
    assert "only the literal value `true`" in content
    # Advances to the correct next command.
    assert successor in content
    # One-line transparency notice is emitted (DEC-004).
    assert "auto_next:" in content

    if command == "specify":
        # specify has no review loop; the gate is Completion / final confirmation.
        assert "Completion" in content
        assert "final stage summary" in content
        assert "not each intermediate" in content
    else:
        # Generation commands gate on the review verdict and stop on non-pass.
        assert "PASS" in content
        assert "PASS_WITH_WARNINGS" in content
        assert "NEEDS_REVISION" in content
        assert "BLOCKED" in content


def test_plan_to_tasks_auto_next_runs_after_analyze_and_is_nonblocking():
    content = read_command("plan-to-tasks")

    # analyze runs first (informational) and must not gate implement-tasks (CON-005).
    assert "do NOT block this advance" in content
    # No confirmation prompt before implement-tasks (DEC-001).
    assert "no confirmation prompt" in content
    # The auto-next section is placed after the analyze section.
    assert content.index("Automatic Cross-Artifact Analysis") < content.index("Auto-Next Chain Advance")


def test_implement_tasks_is_terminal_no_auto_next():
    """implement-tasks is the terminal stage; nothing auto-fires after it (REQ-007)."""
    assert "Auto-Next Chain Advance" not in read_command("implement-tasks")


@pytest.mark.parametrize("command", list(_AUTO_NEXT_SUCCESSOR))
def test_auto_next_section_synced_across_distribution_forms(command):
    """The auto-next section is present in all three distribution forms: the source
    template (slash form), the installed Claude command under .claude/ (slash form),
    and the Codex skill under .agents/skills/ ($mention form). Guards self-bootstrap
    drift where a template is edited but a derived copy is not regenerated."""
    successor = _AUTO_NEXT_SUCCESSOR[command]
    template = read_command(command)
    claude_copy = (ROOT / ".claude" / "commands" / "codexspec" / f"{command}.md").read_text(encoding="utf-8")
    skill_copy = (ROOT / ".agents" / "skills" / f"codexspec-{command}" / "SKILL.md").read_text(encoding="utf-8")

    for label, form in [("template", template), ("claude", claude_copy), ("skill", skill_copy)]:
        assert "Auto-Next Chain Advance" in form, f"{command} {label} missing auto-next section"
        assert "workflow.auto_next" in form, f"{command} {label} missing workflow.auto_next"
        assert successor in form, f"{command} {label} missing successor {successor}"

    # Form-specific invocation syntax.
    assert "/codexspec:" in template
    assert "/codexspec:" in claude_copy
    assert "$codexspec:" in skill_copy
