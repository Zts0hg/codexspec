"""Tests for translation file structure and completeness."""

import json
from pathlib import Path

import pytest

# Expected structure
REQUIRED_CLI_KEYS = ["init", "list_commands", "set_language"]
REQUIRED_INIT_KEYS = [
    "migration_found",
    "migration_complete",
    "update_confirm",
    "commands_updated",
    "success_message",
    "error_no_project_name",
]
REQUIRED_ROOT_KEYS = [
    "constitution",
    "specify",
    "clarify",
    "analyze",
    "checklist",
    "generate-spec",
    "spec-to-plan",
    "plan-to-tasks",
    "review-spec",
    "review-plan",
    "review-tasks",
    "implement-tasks",
    "tasks-to-issues",
    "commit",
    "commit-staged",
    "pr",
]

TRANSLATIONS_DIR = Path(__file__).parent.parent / "templates" / "translations"

REVIEW_CODE_HINT = (
    "[--committed | --uncommitted | --commit <sha>] [--base <branch>] "
    "[--parent <n>] [--feature <feature-dir>] [--focus <instructions>]... | --audit [paths...]"
)
REVIEW_CODE_DESCRIPTIONS = {
    "en": "Review a selected change as a strict defect gate, or audit paths with --audit",
    "zh-CN": "将所选变更作为严格缺陷门禁进行审查，或使用 --audit 审计路径",
    "ja": "選択した変更を厳格な欠陥ゲートとしてレビューするか、--audit でパスを監査",
    "ko": "선택한 변경을 엄격한 결함 게이트로 검토하거나 --audit로 경로 감사",
    "de": "Ausgewählte Änderungen als striktes Defekt-Gate prüfen oder Pfade mit --audit auditieren",
    "es": "Revisar el cambio seleccionado como puerta de defectos estricta o auditar rutas con --audit",
    "fr": "Examiner la modification sélectionnée comme contrôle strict des défauts ou auditer des chemins avec --audit",
    "pt-BR": "Revisar a alteração selecionada como gate de defeitos estrito ou auditar caminhos com --audit",
}


class TestTranslationFilesValidJson:
    """Ensure all translation files are valid JSON."""

    @pytest.mark.parametrize("lang_file", TRANSLATIONS_DIR.glob("*.json"))
    def test_json_valid(self, lang_file):
        """Each translation file should be valid JSON."""
        content = lang_file.read_text(encoding="utf-8")
        try:
            json.loads(content)
        except json.JSONDecodeError as e:
            pytest.fail(f"{lang_file.name} has invalid JSON: {e}")


class TestTranslationFilesStructure:
    """Ensure all translation files have correct structure."""

    @pytest.mark.parametrize("lang_file", TRANSLATIONS_DIR.glob("*.json"))
    def test_has_cli_section(self, lang_file):
        """Each translation file should have 'cli' section."""
        data = json.loads(lang_file.read_text(encoding="utf-8"))
        assert "cli" in data, f"{lang_file.name} missing 'cli' section"

    @pytest.mark.parametrize("lang_file", TRANSLATIONS_DIR.glob("*.json"))
    def test_cli_has_required_keys(self, lang_file):
        """CLI section should have init, list_commands, set_language."""
        data = json.loads(lang_file.read_text(encoding="utf-8"))
        cli = data.get("cli", {})
        for key in REQUIRED_CLI_KEYS:
            assert key in cli, f"{lang_file.name} cli section missing '{key}'"

    @pytest.mark.parametrize("lang_file", TRANSLATIONS_DIR.glob("*.json"))
    def test_cli_init_has_required_keys(self, lang_file):
        """CLI init section should have all required message keys."""
        data = json.loads(lang_file.read_text(encoding="utf-8"))
        init = data.get("cli", {}).get("init", {})
        for key in REQUIRED_INIT_KEYS:
            assert key in init, f"{lang_file.name} cli.init missing '{key}'"

    @pytest.mark.parametrize("lang_file", TRANSLATIONS_DIR.glob("*.json"))
    def test_has_root_command_translations(self, lang_file):
        """Each file should have root-level command translations."""
        data = json.loads(lang_file.read_text(encoding="utf-8"))
        for key in REQUIRED_ROOT_KEYS:
            assert key in data, f"{lang_file.name} missing root key '{key}'"


class TestTranslationFilesCompleteness:
    """Ensure translations are complete (no missing keys vs baseline)."""

    def test_all_languages_have_same_cli_keys_as_baseline(self):
        """All languages should have the same CLI keys as English baseline."""
        en_file = TRANSLATIONS_DIR / "en.json"
        if not en_file.exists():
            pytest.skip("English baseline file not found")

        en_data = json.loads(en_file.read_text(encoding="utf-8"))
        en_cli = en_data.get("cli", {})

        for lang_file in TRANSLATIONS_DIR.glob("*.json"):
            if lang_file.name == "en.json":
                continue  # Skip baseline comparison for en.json

            data = json.loads(lang_file.read_text(encoding="utf-8"))
            cli = data.get("cli", {})

            # Check each key in baseline exists in translation
            for section in en_cli:
                assert section in cli, f"{lang_file.name} missing cli.{section}"
                if isinstance(en_cli[section], dict):
                    for key in en_cli[section]:
                        assert key in cli[section], f"{lang_file.name} missing cli.{section}.{key}"


class TestReviewCodeTranslationContract:
    """The breaking review syntax must update every cached command catalog."""

    @pytest.mark.parametrize(("language", "description"), REVIEW_CODE_DESCRIPTIONS.items())
    def test_review_code_uses_change_gate_metadata(self, language, description):
        data = json.loads((TRANSLATIONS_DIR / f"{language}.json").read_text(encoding="utf-8"))
        command = data["review-code"]

        assert command["description"] == description
        assert command["argument-hint"] == REVIEW_CODE_HINT
        assert "--audit" in command["description"]
        for token in [
            "--committed",
            "--uncommitted",
            "--commit <sha>",
            "--base <branch>",
            "--parent <n>",
            "--feature <feature-dir>",
            "--focus <instructions>",
            "--audit [paths...]",
        ]:
            assert token in command["argument-hint"]
