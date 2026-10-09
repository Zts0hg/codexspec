"""Tests for the ``review.decided_by`` configuration key.

``review.decided_by`` selects who decides about a review-code finding whose
trigger lies outside the project's real operating context: ``reviewer`` (the
default, today's behavior) or ``ask`` (the user decides once). These tests cover
the read/write helpers and the ``codexspec config --decided-by`` option.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Generator

import pytest
from typer.testing import CliRunner

from codexspec import (
    _read_review_decided_by,
    _write_review_decided_by,
    _yaml_has_duplicate_keys,
    app,
    parse_decided_by_value,
)


def _make_config(tmp_path: Path, body: str) -> Path:
    cfg = tmp_path / ".codexspec" / "config.yml"
    cfg.parent.mkdir(parents=True, exist_ok=True)
    cfg.write_text(body, encoding="utf-8")
    return cfg


class TestParseDecidedByValue:
    @pytest.mark.parametrize("raw", ["reviewer", "ask", " ask ", "ASK", "Reviewer"])
    def test_accepted_tokens(self, raw: str) -> None:
        assert parse_decided_by_value(raw) == raw.strip().lower()

    @pytest.mark.parametrize("raw", ["", " ", "maybe", "user", "true", "asked"])
    def test_invalid_raises_value_error(self, raw: str) -> None:
        with pytest.raises(ValueError):
            parse_decided_by_value(raw)


class TestReadReviewDecidedBy:
    def test_absent_section_is_reviewer(self, tmp_path: Path) -> None:
        """TS-2.1"""
        cfg = _make_config(tmp_path, "language:\n  output: en\n")
        assert _read_review_decided_by(cfg) == "reviewer"

    def test_missing_file_is_reviewer(self, tmp_path: Path) -> None:
        """TS-2.1"""
        assert _read_review_decided_by(tmp_path / "missing.yml") == "reviewer"

    def test_absent_key_is_reviewer(self, tmp_path: Path) -> None:
        """TS-2.1"""
        cfg = _make_config(tmp_path, "review:\n  other: 1\n")
        assert _read_review_decided_by(cfg) == "reviewer"

    @pytest.mark.parametrize("value", ["ask", "reviewer"])
    def test_valid_values(self, tmp_path: Path, value: str) -> None:
        """TS-2.2"""
        cfg = _make_config(tmp_path, f"review:\n  decided_by: {value}  # who decides\n")
        assert _read_review_decided_by(cfg) == value

    def test_invalid_value_is_reported_not_masked(self, tmp_path: Path) -> None:
        """TS-2.3: an invalid stored value is returned as-is, never as ``reviewer``."""
        cfg = _make_config(tmp_path, "review:\n  decided_by: maybe\n")
        assert _read_review_decided_by(cfg) == "maybe"

    def test_scoped_to_review_section(self, tmp_path: Path) -> None:
        cfg = _make_config(tmp_path, "workflow:\n  decided_by: ask\nreview:\n  other: 1\n")
        assert _read_review_decided_by(cfg) == "reviewer"


class TestWriteReviewDecidedBy:
    def test_creates_review_section_and_preserves_content(self, tmp_path: Path) -> None:
        """TS-2.4"""
        body = "# top comment\nlanguage:\n  output: en  # inline\nworkflow:\n  auto_next: true\n"
        cfg = _make_config(tmp_path, body)
        assert _write_review_decided_by(cfg, "ask") is True
        text = cfg.read_text(encoding="utf-8")
        assert text.startswith(body)
        assert text.endswith("review:\n  decided_by: ask\n")
        assert _read_review_decided_by(cfg) == "ask"

    def test_inserts_key_into_existing_section(self, tmp_path: Path) -> None:
        """TS-2.4"""
        cfg = _make_config(tmp_path, "review:\n  other: 1\n")
        assert _write_review_decided_by(cfg, "ask") is True
        text = cfg.read_text(encoding="utf-8")
        assert text.count("review:") == 1
        assert "other: 1" in text
        assert _read_review_decided_by(cfg) == "ask"

    def test_updates_in_place_without_duplicate(self, tmp_path: Path) -> None:
        """TS-2.5"""
        cfg = _make_config(tmp_path, "review:\n  decided_by: ask\nworkflow:\n  auto_next: true\n")
        assert _write_review_decided_by(cfg, "reviewer") is True
        text = cfg.read_text(encoding="utf-8")
        assert text.count("decided_by:") == 1
        assert "  decided_by: reviewer\n" in text
        assert "auto_next: true" in text

    def test_rejects_invalid_value(self, tmp_path: Path) -> None:
        cfg = _make_config(tmp_path, "review:\n  decided_by: ask\n")
        with pytest.raises(ValueError):
            _write_review_decided_by(cfg, "maybe")
        assert "decided_by: ask" in cfg.read_text(encoding="utf-8")


@pytest.fixture
def project(tmp_path: Path) -> Generator[Path, None, None]:
    original = os.getcwd()
    os.chdir(tmp_path)
    try:
        yield tmp_path
    finally:
        os.chdir(original)


def _write_project_config(project_dir: Path, body: str) -> Path:
    cfg = _make_config(project_dir, body)
    # Exercise in-place configuration behavior, as the other config CLI tests do.
    from codexspec.worktrees import write_worktrees

    write_worktrees(cfg, False)
    return cfg


class TestConfigDecidedByCli:
    def test_set_ask(self, project: Path) -> None:
        """TS-2.6"""
        cfg = _write_project_config(project, "language:\n  output: en\n")
        result = CliRunner().invoke(app, ["config", "--decided-by", "ask"])
        assert result.exit_code == 0, result.stdout
        assert "review.decided_by = ask" in result.stdout
        assert _read_review_decided_by(cfg) == "ask"

    def test_invalid_value_exits_and_leaves_file_unchanged(self, project: Path) -> None:
        """TS-2.7"""
        cfg = _write_project_config(project, "review:\n  decided_by: reviewer\n")
        before = cfg.read_text(encoding="utf-8")
        result = CliRunner().invoke(app, ["config", "--decided-by", "foo"])
        assert result.exit_code == 1
        assert "Invalid --decided-by value" in result.stdout
        assert "reviewer, ask" in result.stdout
        assert cfg.read_text(encoding="utf-8") == before

    def test_bare_config_shows_default(self, project: Path) -> None:
        """TS-2.8: absent key displays the effective default."""
        _write_project_config(project, "language:\n  output: en\n")
        result = CliRunner().invoke(app, ["config"])
        assert result.exit_code == 0, result.stdout
        assert "Effective review.decided_by: reviewer" in result.stdout

    def test_bare_config_flags_invalid_value(self, project: Path) -> None:
        """TS-2.8: an invalid stored value is shown as invalid, not as the default."""
        _write_project_config(project, "review:\n  decided_by: maybe\n")
        result = CliRunner().invoke(app, ["config"])
        assert result.exit_code == 0, result.stdout
        assert "Effective review.decided_by: reviewer" not in result.stdout
        assert "review.decided_by: invalid value 'maybe'" in result.stdout
        assert "reviewer, ask" in result.stdout


# --- /codexspec:config template (templates/commands/config.md) ---

CONFIG_TEMPLATE = Path(__file__).parent.parent / "templates" / "commands" / "config.md"


def _decided_by_flow() -> str:
    """Return the decision-mode flow with whitespace collapsed (prose wraps freely)."""
    content = CONFIG_TEMPLATE.read_text(encoding="utf-8")
    start = content.index('3c. For "Review decision mode"')
    end = content.index("4. Update the configuration file", start)
    return " ".join(content[start:end].split())


class TestConfigTemplateDecidedBy:
    def test_menu_offers_review_decision_mode(self) -> None:
        """TS-4.1: the Modify menu lists the key with both values and the default."""
        content = CONFIG_TEMPLATE.read_text(encoding="utf-8")
        modify_menu = content.split("Which setting would you like to modify?", 1)[1].split("```", 1)[0]
        assert "Review decision mode" in modify_menu
        assert "review.decided_by" in modify_menu
        flow = _decided_by_flow()
        assert "`reviewer`" in flow and "`ask`" in flow
        assert "default" in flow and "absent key/section means `reviewer`" in flow

    def test_flow_writes_under_review_mapping_in_place(self) -> None:
        """TS-4.2"""
        flow = _decided_by_flow()
        assert "update the value in place when the key exists" in flow
        assert "under the `review:` section, creating that section if absent" in flow
        assert "preserving every other line and comment" in flow

    def test_flow_accepts_only_reviewer_or_ask(self) -> None:
        """TS-4.3"""
        flow = _decided_by_flow()
        assert "Never write any other value" in flow
        assert "report it as invalid" in flow


@pytest.mark.parametrize("stored", ['"ask"', "'ask'"])
def test_read_accepts_yaml_quoted_values(tmp_path: Path, stored: str) -> None:
    """Review round 1 F-002: a YAML-quoted valid value is the same value."""
    cfg = _make_config(tmp_path, f"review:\n  decided_by: {stored}\n")
    assert _read_review_decided_by(cfg) == "ask"


def test_write_updates_a_quoted_value_in_place(tmp_path: Path) -> None:
    cfg = _make_config(tmp_path, 'review:\n  decided_by: "ask"\n')
    assert _write_review_decided_by(cfg, "reviewer") is True
    assert cfg.read_text(encoding="utf-8").count("decided_by:") == 1
    assert _read_review_decided_by(cfg) == "reviewer"


# --- Review round 4: YAML semantics, never a false success ---


@pytest.mark.parametrize(
    ("body", "expected"),
    [
        ("review:\n  decided_by:\n", "null"),
        ("review:\n  decided_by: ~\n", "null"),
        ("review:\n# note\n  decided_by: ask\n", "ask"),
        ("review: {decided_by: ask}\n", "ask"),
        ("review:\n  decided_by: ask # why\n", "ask"),
    ],
)
def test_read_follows_yaml_semantics(tmp_path: Path, body: str, expected: str) -> None:
    cfg = _make_config(tmp_path, body)
    assert _read_review_decided_by(cfg) == expected


@pytest.mark.parametrize(
    "body",
    [
        "review:\n  decided_by:\n",
        "review:\n# note\n  decided_by: ask\n",
        "review: {decided_by: ask}\n",
        "# top\nlanguage:\n  output: en\n",
    ],
)
def test_write_takes_effect_under_yaml_or_reports_failure(tmp_path: Path, body: str) -> None:
    import yaml

    cfg = _make_config(tmp_path, body)
    ok = _write_review_decided_by(cfg, "reviewer")
    data = yaml.safe_load(cfg.read_text(encoding="utf-8")) or {}
    if ok:
        assert data["review"]["decided_by"] == "reviewer"
    else:
        assert cfg.read_text(encoding="utf-8") == body


# --- Review round 5: whole-document verification (class-level fix) ---


@pytest.mark.parametrize(
    "body",
    [
        "review: {decided_by: ask, extra: keep}\n",
        "review: &r\n  extra: keep\n",
        '"review":\n  decided_by: ask\n  extra: keep\n',
        "review:\n  sub:\n    decided_by: keep\n",
        "review:\n  note: |\n    decided_by: keep-this-text\n",
    ],
)
def test_write_never_changes_anything_but_the_target_key(tmp_path: Path, body: str) -> None:
    import yaml

    cfg = _make_config(tmp_path, body)
    before = yaml.safe_load(body)
    ok = _write_review_decided_by(cfg, "reviewer")
    text = cfg.read_text(encoding="utf-8")
    if not ok:
        assert text == body
        return
    after = yaml.safe_load(text)
    expected = {**before, "review": {**(before.get("review") or {}), "decided_by": "reviewer"}}
    assert after == expected
    assert not _yaml_has_duplicate_keys(text)


def test_read_reports_duplicate_review_keys_as_invalid(tmp_path: Path) -> None:
    cfg = _make_config(tmp_path, "review:\n  decided_by: ask\nreview:\n  decided_by: reviewer\n")
    assert _read_review_decided_by(cfg) not in ("ask", "reviewer")
