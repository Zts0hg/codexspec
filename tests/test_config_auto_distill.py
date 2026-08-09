"""Unit tests for the ``--auto-distill`` config helpers.

Unlike ``auto_next``, ``auto_distill`` defaults to ON (opt-out): only the literal
``false`` disables it. CLI-level integration tests live in ``tests/test_cli.py``
(``TestConfig``).
"""

from __future__ import annotations

from pathlib import Path

import pytest

from codexspec import _read_auto_distill, _write_auto_distill, parse_auto_distill_value


class TestParseAutoDistillValue:
    """Accepted token set (shared with ``--auto-next``) and rejection of bad values."""

    @pytest.mark.parametrize("raw", ["on", "ON", "On", "true", "TRUE", "1", "yes", "YES", "Yes"])
    def test_truthy_tokens(self, raw: str) -> None:
        assert parse_auto_distill_value(raw) is True

    @pytest.mark.parametrize("raw", ["off", "OFF", "false", "FALSE", "0", "no", "NO", "No"])
    def test_falsy_tokens(self, raw: str) -> None:
        assert parse_auto_distill_value(raw) is False

    @pytest.mark.parametrize("raw", [" true ", "\ntrue\n", "\tON\t"])
    def test_whitespace_is_stripped(self, raw: str) -> None:
        assert parse_auto_distill_value(raw) is True

    @pytest.mark.parametrize("raw", ["maybe", "2", "enable", "yep", " ", "", "auto"])
    def test_invalid_raises_value_error(self, raw: str) -> None:
        with pytest.raises(ValueError):
            parse_auto_distill_value(raw)


def _make_config(tmp_path: Path, body: str) -> Path:
    cfg = tmp_path / ".codexspec" / "config.yml"
    cfg.parent.mkdir(parents=True)
    cfg.write_text(body, encoding="utf-8")
    return cfg


class TestReadAutoDistill:
    """Default ON: only a literal ``false`` under ``workflow:`` disables."""

    def test_true(self, tmp_path: Path) -> None:
        cfg = _make_config(tmp_path, "workflow:\n  auto_distill: true\n")
        assert _read_auto_distill(cfg) is True

    def test_false(self, tmp_path: Path) -> None:
        cfg = _make_config(tmp_path, "workflow:\n  auto_distill: false\n")
        assert _read_auto_distill(cfg) is False

    def test_malformed_is_true(self, tmp_path: Path) -> None:
        # opt-out default: anything that is not the literal ``false`` is enabled.
        cfg = _make_config(tmp_path, "workflow:\n  auto_distill: maybe\n")
        assert _read_auto_distill(cfg) is True

    def test_absent_key_is_true(self, tmp_path: Path) -> None:
        cfg = _make_config(tmp_path, "workflow:\n  other: 1\n")
        assert _read_auto_distill(cfg) is True

    def test_absent_section_is_true(self, tmp_path: Path) -> None:
        cfg = _make_config(tmp_path, "language:\n  output: en\n")
        assert _read_auto_distill(cfg) is True

    def test_scoped_to_workflow_section(self, tmp_path: Path) -> None:
        # auto_distill:false under a different section must NOT disable;
        # workflow has no auto_distill -> default enabled.
        body = "project:\n  auto_distill: false\nworkflow:\n  other: 1\n"
        cfg = _make_config(tmp_path, body)
        assert _read_auto_distill(cfg) is True

    def test_missing_file_is_true(self, tmp_path: Path) -> None:
        assert _read_auto_distill(tmp_path / "nope.yml") is True


class TestWriteAutoDistill:
    """update, insert, append; preserve comments (mirrors ``_write_auto_next``)."""

    def test_update_in_place_true_to_false(self, tmp_path: Path) -> None:
        cfg = _make_config(tmp_path, "workflow:\n  auto_distill: true\n")
        assert _write_auto_distill(cfg, False) is True
        assert _read_auto_distill(cfg) is False
        assert "auto_distill: false" in cfg.read_text()

    def test_update_in_place_false_to_true(self, tmp_path: Path) -> None:
        cfg = _make_config(tmp_path, "workflow:\n  auto_distill: false\n")
        assert _write_auto_distill(cfg, True) is True
        assert _read_auto_distill(cfg) is True

    def test_insert_key_into_existing_section(self, tmp_path: Path) -> None:
        body = "language:\n  output: en\nworkflow:\n  other: 1\n"
        cfg = _make_config(tmp_path, body)
        assert _write_auto_distill(cfg, False) is True
        text = cfg.read_text()
        assert text.count("workflow:") == 1
        assert _read_auto_distill(cfg) is False
        assert "other: 1" in text  # pre-existing child preserved

    def test_append_section_when_absent(self, tmp_path: Path) -> None:
        cfg = _make_config(tmp_path, "language:\n  output: en\n")
        assert _write_auto_distill(cfg, False) is True
        text = cfg.read_text()
        assert text.endswith("workflow:\n  auto_distill: false\n")
        assert "output: en" in text  # prior content preserved
        assert _read_auto_distill(cfg) is False

    def test_preserves_comments_outside_value(self, tmp_path: Path) -> None:
        body = "# top comment\nlanguage:\n  output: en  # inline\nworkflow:\n  auto_distill: false  # distill\n"
        cfg = _make_config(tmp_path, body)
        assert _write_auto_distill(cfg, True) is True
        text = cfg.read_text()
        assert "# top comment" in text
        assert "# inline" in text
        # The value line is rewritten bare; its inline comment is not retained.
        assert "  auto_distill: true\n" in text
        assert _read_auto_distill(cfg) is True

    def test_empty_file(self, tmp_path: Path) -> None:
        cfg = _make_config(tmp_path, "")
        assert _write_auto_distill(cfg, False) is True
        assert _read_auto_distill(cfg) is False

    def test_no_trailing_newline(self, tmp_path: Path) -> None:
        cfg = _make_config(tmp_path, "language:\n  output: en")  # no trailing \n
        assert _write_auto_distill(cfg, False) is True
        assert _read_auto_distill(cfg) is False
