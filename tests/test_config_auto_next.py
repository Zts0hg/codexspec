"""Unit tests for the ``--auto-next`` config helpers.

These cover the pure functions (parsing + read/write) used by the
``codexspec config --auto-next`` option. CLI-level integration tests live in
``tests/test_cli.py`` (``TestConfig``).
"""

from __future__ import annotations

from pathlib import Path

import pytest

from codexspec import _read_auto_next, _write_auto_next, parse_auto_next_value


class TestParseAutoNextValue:
    """REQ-003 / NFR-001: accepted token set and rejection of bad values."""

    @pytest.mark.parametrize("raw", ["on", "ON", "On", "true", "TRUE", "1", "yes", "YES", "Yes"])
    def test_truthy_tokens(self, raw: str) -> None:
        assert parse_auto_next_value(raw) is True

    @pytest.mark.parametrize("raw", ["off", "OFF", "false", "FALSE", "0", "no", "NO", "No"])
    def test_falsy_tokens(self, raw: str) -> None:
        assert parse_auto_next_value(raw) is False

    @pytest.mark.parametrize("raw", [" true ", "\ntrue\n", "\tON\t"])
    def test_whitespace_is_stripped(self, raw: str) -> None:
        assert parse_auto_next_value(raw) is True

    @pytest.mark.parametrize("raw", ["maybe", "2", "enable", "yep", " ", "", "auto"])
    def test_invalid_raises_value_error(self, raw: str) -> None:
        with pytest.raises(ValueError):
            parse_auto_next_value(raw)


def _make_config(tmp_path: Path, body: str) -> Path:
    cfg = tmp_path / ".codexspec" / "config.yml"
    cfg.parent.mkdir(parents=True)
    cfg.write_text(body, encoding="utf-8")
    return cfg


class TestReadAutoNext:
    """REQ-004: only literal ``true`` under ``workflow:`` counts as enabled."""

    def test_true(self, tmp_path: Path) -> None:
        cfg = _make_config(tmp_path, "workflow:\n  auto_next: true\n")
        assert _read_auto_next(cfg) is True

    def test_false(self, tmp_path: Path) -> None:
        cfg = _make_config(tmp_path, "workflow:\n  auto_next: false\n")
        assert _read_auto_next(cfg) is False

    def test_malformed_is_false(self, tmp_path: Path) -> None:
        cfg = _make_config(tmp_path, "workflow:\n  auto_next: maybe\n")
        assert _read_auto_next(cfg) is False

    def test_absent_key_is_false(self, tmp_path: Path) -> None:
        cfg = _make_config(tmp_path, "workflow:\n  other: 1\n")
        assert _read_auto_next(cfg) is False

    def test_absent_section_is_false(self, tmp_path: Path) -> None:
        cfg = _make_config(tmp_path, "language:\n  output: en\n")
        assert _read_auto_next(cfg) is False

    def test_scoped_to_workflow_section(self, tmp_path: Path) -> None:
        # auto_next under a different section must NOT count.
        body = "project:\n  auto_next: true\nworkflow:\n  other: 1\n"
        cfg = _make_config(tmp_path, body)
        assert _read_auto_next(cfg) is False

    def test_missing_file_is_false(self, tmp_path: Path) -> None:
        assert _read_auto_next(tmp_path / "nope.yml") is False


class TestWriteAutoNext:
    """REQ-005 / REQ-006 / REQ-011: update, insert, append; preserve comments."""

    def test_update_in_place_true_to_false(self, tmp_path: Path) -> None:
        cfg = _make_config(tmp_path, "workflow:\n  auto_next: true\n")
        assert _write_auto_next(cfg, False) is True
        assert _read_auto_next(cfg) is False
        assert "auto_next: false" in cfg.read_text()

    def test_update_in_place_false_to_true(self, tmp_path: Path) -> None:
        cfg = _make_config(tmp_path, "workflow:\n  auto_next: false\n")
        assert _write_auto_next(cfg, True) is True
        assert _read_auto_next(cfg) is True

    def test_insert_key_into_existing_section(self, tmp_path: Path) -> None:
        body = "language:\n  output: en\nworkflow:\n  other: 1\n"
        cfg = _make_config(tmp_path, body)
        assert _write_auto_next(cfg, True) is True
        text = cfg.read_text()
        # exactly one workflow section, with the new key as a child
        assert text.count("workflow:") == 1
        assert _read_auto_next(cfg) is True
        # the pre-existing child is preserved
        assert "other: 1" in text

    def test_append_section_when_absent(self, tmp_path: Path) -> None:
        cfg = _make_config(tmp_path, "language:\n  output: en\n")
        assert _write_auto_next(cfg, True) is True
        text = cfg.read_text()
        assert text.endswith("workflow:\n  auto_next: true\n")
        assert "output: en" in text  # prior content preserved
        assert _read_auto_next(cfg) is True

    def test_preserves_comments_outside_value(self, tmp_path: Path) -> None:
        body = "# top comment\nlanguage:\n  output: en  # inline\nworkflow:\n  auto_next: true  # chain\n"
        cfg = _make_config(tmp_path, body)
        assert _write_auto_next(cfg, False) is True
        text = cfg.read_text()
        assert "# top comment" in text
        assert "# inline" in text
        # The value line is rewritten bare; its inline comment is not retained
        # (SC-002 preserves comments *outside* the auto_next value line).
        assert "  auto_next: false\n" in text
        assert _read_auto_next(cfg) is False

    def test_empty_file(self, tmp_path: Path) -> None:
        cfg = _make_config(tmp_path, "")
        assert _write_auto_next(cfg, True) is True
        assert _read_auto_next(cfg) is True

    def test_no_trailing_newline(self, tmp_path: Path) -> None:
        cfg = _make_config(tmp_path, "language:\n  output: en")  # no trailing \n
        assert _write_auto_next(cfg, True) is True
        assert _read_auto_next(cfg) is True
