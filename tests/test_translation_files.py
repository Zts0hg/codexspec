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

REVIEW_CODE_HINTS = {
    "en": """[defect-gate selectors | --audit [paths...]] (all arguments optional)

This command reviews code in one of two mutually exclusive modes.

Mode 1 - Defect gate (default): merge-blocking verdict over a Git change.
  1. No arguments → Full feature-branch delta: merge-base → worktree (on the base branch itself: uncommitted delta)
  2. --committed → Merge-base to HEAD only; excludes staged, unstaged, untracked work
  3. --uncommitted → Staged, unstaged, and untracked work only
  4. --commit <sha> → Exactly that commit; add --parent <n> to select one merge parent
  Modifiers never select a target by themselves:
  - --base <branch> → Override base resolution; valid only with No arguments or --committed
  - --feature <feature-dir> → Attach requirements context for coverage; never changes Git scope
  - --focus <instructions> → Add Risk Pass obligations; repeatable, never narrows scope

Mode 2 - Audit: advisory quality scorecard over current file contents (no gate verdict, no envelope).
  1. --audit → Review the main source directory (default: src/)
  2. --audit <path> [<path>...] → Review only the listed paths, space-separated

A bare path such as src/ is not a valid defect target: migrate it with --audit src/.

Examples:
  /codexspec:review-code
  /codexspec:review-code --uncommitted
  /codexspec:review-code --commit <sha> --parent 1
  /codexspec:review-code --committed --base origin/main
  /codexspec:review-code --feature .codexspec/specs/2026-0714-1030ab-payment --focus "verify retry handling"
  /codexspec:review-code --audit src/api""",
    "zh-CN": """[缺陷门禁选择器 | --audit [paths...]]（所有参数均可选）

本命令以两种互斥模式之一审查代码。

模式一 - 缺陷门禁（默认）：对 Git 变更给出阻断合并的裁定。
  1. 无参数 → 完整特性分支增量：merge-base → 工作区（若在基分支上：仅未提交变更）
  2. --committed → 仅 merge-base → HEAD；排除已暂存、未暂存、未跟踪的变更
  3. --uncommitted → 仅已暂存 + 未暂存 + 未跟踪的变更
  4. --commit <sha> → 仅该提交；加 --parent <n> 选择一个合并父节点
  修饰符自身不选择审查对象：
  - --base <branch> → 覆盖基分支解析；仅可与无参数或 --committed 搭配
  - --feature <feature-dir> → 附加需求上下文用于覆盖检查；绝不改变 Git 范围
  - --focus <instructions> → 追加风险审查义务；可重复，绝不收窄范围

模式二 - 审计（advisory）：对现有文件内容出具建议性质量评分卡（无门禁裁定、无 envelope）。
  1. --audit → 审查主源码目录（默认：src/）
  2. --audit <path> [<path>...] → 仅审查列出的路径，空格分隔

裸路径（如 src/）不是合法的缺陷门禁目标：请用 --audit src/ 迁移。

示例：
  /codexspec:review-code
  /codexspec:review-code --uncommitted
  /codexspec:review-code --commit <sha> --parent 1
  /codexspec:review-code --committed --base origin/main
  /codexspec:review-code --feature .codexspec/specs/2026-0714-1030ab-payment --focus "检查重试处理"
  /codexspec:review-code --audit src/api""",
    "ja": """[欠陥ゲート選択子 | --audit [paths...]]（すべての引数は省略可能）

このコマンドは、相互に排他的な 2 つのモードのいずれかでコードをレビューします。

モード 1 - 欠陥ゲート（デフォルト）：Git 変更に対するマージ阻止判定。
  1. 引数なし → フィーチャーブランチ全体の差分：merge-base → ワークツリー（ベースブランチ上では：未コミットの変更のみ）
  2. --committed → merge-base → HEAD のみ。ステージ済み・未ステージ・未追跡の変更は除外
  3. --uncommitted → ステージ済み + 未ステージ + 未追跡の変更のみ
  4. --commit <sha> → そのコミットのみ。--parent <n> を追加するとマージ親を 1 つ選択
  修飾子はそれ自体では対象を選択しません：
  - --base <branch> → ベース解決を上書き。引数なしまたは --committed とのみ組み合わせ可能
  - --feature <feature-dir> → カバレッジ確認のため要件コンテキストを添付。Git スコープは変更しない
  - --focus <instructions> → リスクパスの義務を追加。繰り返し可能、スコープは狭めない

モード 2 - 監査（advisory）：現在のファイル内容に対するアドバイザリ品質スコアカード（ゲート判定なし、envelope なし）。
  1. --audit → メインのソースディレクトリをレビュー（デフォルト：src/）
  2. --audit <path> [<path>...] → 指定したパスのみをレビュー（スペース区切り）

src/ のような裸のパスは欠陥ゲートの対象として無効です：--audit src/ に移行してください。

例：
  /codexspec:review-code
  /codexspec:review-code --uncommitted
  /codexspec:review-code --commit <sha> --parent 1
  /codexspec:review-code --committed --base origin/main
  /codexspec:review-code --feature .codexspec/specs/2026-0714-1030ab-payment --focus "リトライ処理の確認"
  /codexspec:review-code --audit src/api""",
    "ko": """[결함 게이트 선택자 | --audit [paths...]] (모든 인자는 선택 사항)

이 명령은 상호 배타적인 두 가지 모드 중 하나로 코드를 검토합니다.

모드 1 - 결함 게이트 (기본값): Git 변경에 대한 병합 차단 판정.
  1. 인자 없음 → 전체 피처 브랜치 델타: merge-base → 작업 트리 (베이스 브랜치 자체인 경우: 커밋되지 않은 변경만)
  2. --committed → merge-base → HEAD만. 스테이지됨, 스테이지 안 됨, 추적 안 됨 변경은 제외
  3. --uncommitted → 스테이지됨 + 스테이지 안 됨 + 추적 안 됨 변경만
  4. --commit <sha> → 해당 커밋만. --parent <n>을 추가하면 병합 부모 하나를 선택
  수정자는 그 자체로 대상을 선택하지 않습니다:
  - --base <branch> → 베이스 해석을 재정의. 인자 없음 또는 --committed와만 사용 가능
  - --feature <feature-dir> → 커버리지 확인용 요구사항 컨텍스트를 첨부. Git 범위는 변경하지 않음
  - --focus <instructions> → 리스크 패스 의무를 추가. 반복 가능, 범위를 좁히지 않음

모드 2 - 감사 (advisory): 현재 파일 내용에 대한 자문 품질 스코어카드 (게이트 판정 없음, envelope 없음).
  1. --audit → 메인 소스 디렉터리를 검토 (기본값: src/)
  2. --audit <path> [<path>...] → 나열된 경로만 검토 (공백으로 구분)

src/ 같은 베어 경로는 결함 게이트 대상으로 유효하지 않습니다: --audit src/로 전환하세요.

예시:
  /codexspec:review-code
  /codexspec:review-code --uncommitted
  /codexspec:review-code --commit <sha> --parent 1
  /codexspec:review-code --committed --base origin/main
  /codexspec:review-code --feature .codexspec/specs/2026-0714-1030ab-payment --focus "재시도 처리 확인"
  /codexspec:review-code --audit src/api""",
    "de": """[Defect-Gate-Selektoren | --audit [paths...]] (alle Argumente optional)

Dieser Befehl prüft Code in einem von zwei sich gegenseitig ausschließenden Modi.

Modus 1 - Defect Gate (Standard): merge-blockierendes Urteil über eine Git-Änderung.
  1. Keine Argumente → gesamtes Branch-Delta: merge-base → Worktree (Basis-Branch: nur uncommittete Änderungen)
  2. --committed → nur merge-base → HEAD; schließt gestagte, ungestagte und untracked Änderungen aus
  3. --uncommitted → nur gestagte + ungestagte + untracked Änderungen
  4. --commit <sha> → genau dieser Commit; mit --parent <n> einen Merge-Elternteil wählen
  Modifizierer wählen selbst kein Ziel aus:
  - --base <branch> → Basis-Auflösung überschreiben; nur ohne Argumente oder mit --committed gültig
  - --feature <feature-dir> → Anforderungskontext für die Abdeckung anhängen; ändert den Git-Scope nie
  - --focus <instructions> → Risk-Pass-Pflichten ergänzen; wiederholbar, engt nie ein

Modus 2 - Audit (advisory): beratende Qualitätswertung über den aktuellen Dateiinhalt (kein Gate-Urteil, kein Envelope).
  1. --audit → Hauptquellverzeichnis prüfen (Standard: src/)
  2. --audit <path> [<path>...] → nur die aufgeführten Pfade prüfen, durch Leerzeichen getrennt

Ein nackter Pfad wie src/ ist kein gültiges Defect-Gate-Ziel: mit --audit src/ migrieren.

Beispiele:
  /codexspec:review-code
  /codexspec:review-code --uncommitted
  /codexspec:review-code --commit <sha> --parent 1
  /codexspec:review-code --committed --base origin/main
  /codexspec:review-code --feature .codexspec/specs/2026-0714-1030ab-payment --focus "Retry-Handling prüfen"
  /codexspec:review-code --audit src/api""",
    "es": """[selectores de defect-gate | --audit [paths...]] (todos los argumentos son opcionales)

Este comando revisa código en uno de dos modos mutuamente excluyentes.

Modo 1 - Defect gate (predeterminado): veredicto que bloquea la fusión sobre un cambio de Git.
  1. Sin argumentos → delta completo de la rama: merge-base → worktree (en la rama base: solo cambios sin confirmar)
  2. --committed → solo merge-base → HEAD; excluye lo staged, unstaged y untracked
  3. --uncommitted → solo staged + unstaged + untracked
  4. --commit <sha> → exactamente ese commit; añade --parent <n> para elegir un padre de fusión
  Los modificadores nunca seleccionan un objetivo por sí mismos:
  - --base <branch> → anula la resolución de la base; válido solo sin argumentos o con --committed
  - --feature <feature-dir> → adjunta contexto de requisitos para la cobertura; nunca cambia el alcance de Git
  - --focus <instructions> → añade obligaciones al Risk Pass; repetible, nunca reduce el alcance

Modo 2 - Audit (advisory): scorecard consultivo del contenido de los archivos (sin veredicto de gate ni envelope).
  1. --audit → revisa el directorio principal de código (predeterminado: src/)
  2. --audit <path> [<path>...] → revisa solo las rutas listadas, separadas por espacios

Una ruta desnuda como src/ no es un objetivo de defect gate válido: migre con --audit src/.

Ejemplos:
  /codexspec:review-code
  /codexspec:review-code --uncommitted
  /codexspec:review-code --commit <sha> --parent 1
  /codexspec:review-code --committed --base origin/main
  /codexspec:review-code --feature .codexspec/specs/2026-0714-1030ab-payment --focus "verificar el manejo de reintentos"
  /codexspec:review-code --audit src/api""",
    "fr": """[sélecteurs defect-gate | --audit [paths...]] (tous les arguments sont facultatifs)

Cette commande examine le code dans l'un de deux modes mutuellement exclusifs.

Mode 1 - Defect gate (par défaut) : verdict bloquant la fusion sur une modification Git.
  1. Sans argument → delta complet de la branche : merge-base → worktree (branche de base : non validé uniquement)
  2. --committed → merge-base → HEAD uniquement ; exclut le staged, unstaged et untracked
  3. --uncommitted → staged + unstaged + untracked uniquement
  4. --commit <sha> → exactement ce commit ; ajoutez --parent <n> pour choisir un parent de fusion
  Les modificateurs ne sélectionnent jamais de cible par eux-mêmes :
  - --base <branch> → remplace la résolution de la base ; valable uniquement sans argument ou avec --committed
  - --feature <feature-dir> → joint le contexte des exigences pour la couverture ; ne change jamais le périmètre Git
  - --focus <instructions> → ajoute des obligations au Risk Pass ; répétable, ne rétrécit jamais le périmètre

Mode 2 - Audit (advisory) : grille de qualité consultative du contenu des fichiers (sans verdict de gate ni envelope).
  1. --audit → examine le répertoire source principal (par défaut : src/)
  2. --audit <path> [<path>...] → examine uniquement les chemins listés, séparés par des espaces

Un chemin nu comme src/ n'est pas une cible defect gate valide : migrez avec --audit src/.

Exemples :
  /codexspec:review-code
  /codexspec:review-code --uncommitted
  /codexspec:review-code --commit <sha> --parent 1
  /codexspec:review-code --committed --base origin/main
  /codexspec:review-code --feature .codexspec/specs/2026-0714-1030ab-payment --focus "vérifier les tentatives"
  /codexspec:review-code --audit src/api""",
    "pt-BR": """[seletores defect-gate | --audit [paths...]] (todos os argumentos são opcionais)

Este comando revisa código em um de dois modos mutuamente exclusivos.

Modo 1 - Defect gate (padrão): veredito que bloqueia o merge sobre uma alteração do Git.
  1. Sem argumentos → delta completo do branch: merge-base → worktree (branch base: apenas alterações não commitadas)
  2. --committed → apenas merge-base → HEAD; exclui staged, unstaged e untracked
  3. --uncommitted → apenas staged + unstaged + untracked
  4. --commit <sha> → exatamente aquele commit; adicione --parent <n> para escolher um pai do merge
  Modificadores nunca selecionam um alvo por si mesmos:
  - --base <branch> → sobrepõe a resolução da base; válido apenas sem argumentos ou com --committed
  - --feature <feature-dir> → anexa contexto de requisitos para cobertura; nunca muda o escopo do Git
  - --focus <instructions> → adiciona obrigações ao Risk Pass; repetível, nunca restringe o escopo

Modo 2 - Audit (advisory): scorecard de qualidade do conteúdo dos arquivos (sem veredito de gate nem envelope).
  1. --audit → revisa o diretório principal de código (padrão: src/)
  2. --audit <path> [<path>...] → revisa apenas os caminhos listados, separados por espaço

Um caminho simples como src/ não é um alvo válido do defect gate: migre com --audit src/.

Exemplos:
  /codexspec:review-code
  /codexspec:review-code --uncommitted
  /codexspec:review-code --commit <sha> --parent 1
  /codexspec:review-code --committed --base origin/main
  /codexspec:review-code --feature .codexspec/specs/2026-0714-1030ab-payment --focus "verificar as novas tentativas"
  /codexspec:review-code --audit src/api""",
}
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
        assert command["argument-hint"] == REVIEW_CODE_HINTS[language]
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
