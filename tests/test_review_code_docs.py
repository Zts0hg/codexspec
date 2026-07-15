"""Cross-locale documentation contract for the review-code breaking change."""

from __future__ import annotations

import re
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
LOCALES = {
    "en": ("README.md", "defect gate"),
    "zh": ("README.zh-CN.md", "缺陷门禁"),
    "ja": ("README.ja.md", "欠陥ゲート"),
    "ko": ("README.ko.md", "결함 게이트"),
    "de": ("README.de.md", "Defekt-Gate"),
    "es": ("README.es.md", "puerta de defectos"),
    "fr": ("README.fr.md", "contrôle de défauts"),
    "pt-BR": ("README.pt-BR.md", "gate de defeitos"),
}


def review_section(locale: str) -> str:
    guide = (ROOT / "docs" / locale / "user-guide" / "commands.md").read_text(encoding="utf-8")
    return guide.split("### `/codexspec:review-code`", 1)[1].split("\n---", 1)[0]


@pytest.mark.parametrize(("locale", "readme_and_term"), LOCALES.items())
def test_localized_guide_documents_defect_gate_and_audit_migration(
    locale: str,
    readme_and_term: tuple[str, str],
) -> None:
    _, defect_term = readme_and_term
    content = review_section(locale)

    assert defect_term.casefold() in content.casefold()
    assert "<!-- REVIEW-CODE-BREAKING: DEFAULT-GATE -->" in content
    assert "<!-- REVIEW-CODE-BREAKING: PATH-AUDIT -->" in content
    assert "<!-- REVIEW-CODE-AUDIT -->" in content

    default_gate, audit = content.split("<!-- REVIEW-CODE-AUDIT -->", 1)
    for syntax in [
        "/codexspec:review-code",
        "/codexspec:review-code --committed",
        "/codexspec:review-code --uncommitted",
        "/codexspec:review-code --commit <sha>",
        "--base <branch>",
        "--parent <n>",
        "--feature <feature-dir>",
        "--focus <instructions>",
    ]:
        assert syntax in default_gate

    for verdict in ["PASS", "FAIL", "INCONCLUSIVE"]:
        assert verdict in default_gate
    assert "<review-code-result>" in default_gate
    assert "Quality Score" not in default_gate

    assert "/codexspec:review-code --audit [paths...]" in audit
    assert "/codexspec:review-code --audit src/" in audit
    assert "PASS" not in audit or "defect gate" in audit.lower()

    successful_bare_path = re.compile(
        r"^(?:You:|你:)?\s*/codexspec:review-code\s+(?!-{1,2})(?:src/|\[[^\]]*(?:path|ruta|chemin)[^\]]*\])",
        re.MULTILINE | re.IGNORECASE,
    )
    assert successful_bare_path.search(content) is None


@pytest.mark.parametrize(("locale", "readme_and_term"), LOCALES.items())
def test_readme_summary_describes_gate_not_default_scorecard(
    locale: str,
    readme_and_term: tuple[str, str],
) -> None:
    readme_name, defect_term = readme_and_term
    content = (ROOT / readme_name).read_text(encoding="utf-8")
    row = next(line for line in content.splitlines() if "`/codexspec:review-code`" in line)

    assert defect_term.casefold() in row.casefold(), locale
    assert "--audit" in row
    assert "Quality Score" not in row
