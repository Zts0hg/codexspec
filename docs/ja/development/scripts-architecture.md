# Scripts アーキテクチャ分析

このドキュメントは、CodexSpec プロジェクトにおける scripts のコードロジックフローと、それらが Claude Code でどのように使用されるかを詳細に説明します。

## 1. 全体アーキテクチャ概要

CodexSpec は **Spec-Driven Development (SDD)** ツールキットであり、CLI + テンプレート + 補助スクリプトの 3 層アーキテクチャを採用しています:

```
┌─────────────────────────────────────────────────────────────────┐
│                        ユーザー層 (CLI)                          │
│  codexspec init | check | version | config                      │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    Claude Code インタラクション層                │
│  /codexspec.specify | /codexspec.analyze | ...                  │
│  (.claude/commands/*.md)                                        │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                      補助スクリプト層                            │
│  .codexspec/scripts/*.sh (Bash) または *.ps1 (PowerShell)       │
└─────────────────────────────────────────────────────────────────┘
```

## 2. Scripts のデプロイフロー

### フェーズ 1: `codexspec init` 初期化

`src/codexspec/__init__.py` の `init()` 関数（第 343-368 行）で、オペレーティングシステムに基づいて対応するスクリプトを自動コピーします:

```python
# Copy helper scripts based on platform
scripts_source_dir = get_scripts_dir()
if scripts_source_dir.exists():
    if sys.platform == "win32":
        # Windows: PowerShell スクリプトをコピー
        ps_scripts = scripts_source_dir / "powershell"
        for script_file in ps_scripts.glob("*.ps1"):
            dest_file = codexspec_dir / "scripts" / script_file.name
            dest_file.write_text(script_file.read_text(encoding="utf-8"), encoding="utf-8")
    else:
        # macOS/Linux: Bash スクリプトをコピー
        bash_scripts = scripts_source_dir / "bash"
        for script_file in bash_scripts.glob("*.sh"):
            dest_file = codexspec_dir / "scripts" / script_file.name
            dest_file.write_text(script_file.read_text(encoding="utf-8"), encoding="utf-8")
```

**結果**: オペレーティングシステムに基づいて、`scripts/bash/` または `scripts/powershell/` のスクリプトをプロジェクトの `.codexspec/scripts/` ディレクトリにコピーします。

### パス解決メカニズム

`get_scripts_dir()` 関数（第 71-90 行）は複数のインストールシナリオを処理します:

```python
def get_scripts_dir() -> Path:
    # Path 1: Wheel install - scripts packaged inside codexspec package
    installed_scripts = Path(__file__).parent / "scripts"
    if installed_scripts.exists():
        return installed_scripts

    # Path 2: Development/editable install - scripts in project root
    dev_scripts = Path(__file__).parent.parent.parent / "scripts"
    if dev_scripts.exists():
        return dev_scripts

    # Path 3: Fallback
    return installed_scripts
```

## 3. Scripts の Claude Code での呼び出しメカニズム

### コアメカニズム: YAML Frontmatter 宣言

テンプレートファイルは YAML frontmatter でスクリプト依存関係を宣言します:

```yaml
---
description: コマンドの説明
scripts:
  sh: .codexspec/scripts/check-prerequisites.sh --json --require-tasks --include-tasks
  ps: .codexspec/scripts/check-prerequisites.ps1 -Json -RequireTasks -IncludeTasks
---
```

### プレースホルダー置換

テンプレート内で `{SCRIPT}` プレースホルダーを使用:

```markdown
### 1. Initialize Context

Run `{SCRIPT}` from repo root and parse JSON for:
- `FEATURE_DIR` - Feature directory path
- `AVAILABLE_DOCS` - Available documents list
```

### 呼び出しフロー

1. ユーザーが Claude Code で `/codexspec.analyze` を入力
2. Claude が `.claude/commands/codexspec.analyze.md` テンプレートを読み込む
3. オペレーティングシステムに基づいて、Claude が `{SCRIPT}` を置換:
   - **macOS/Linux**: `.codexspec/scripts/check-prerequisites.sh --json --require-tasks --include-tasks`
   - **Windows**: `.codexspec/scripts/check-prerequisites.ps1 -Json -RequireTasks -IncludeTasks`
4. Claude がスクリプトを実行し、JSON 出力を解析して、後続の操作を継続

## 4. Scripts 機能詳細

### 4.1 `check-prerequisites.sh/ps1` - 前提条件チェックスクリプト

これが最も重要なスクリプトで、環境状態を検証し、構造化された情報を返します。

#### コア機能

- 現在 feature ブランチにいるか検証（形式: `001-feature-name`）
- 必要なファイルの存在を検出 (`plan.md`, `tasks.md`)
- JSON 形式のパス情報を返す

#### パラメータオプション

| パラメータ | Bash | PowerShell | 機能 |
|------|------|------------|------|
| JSON 出力 | `--json` | `-Json` | JSON 形式で出力 |
| tasks.md 要件 | `--require-tasks` | `-RequireTasks` | tasks.md の存在を検証 |
| tasks.md 含有 | `--include-tasks` | `-IncludeTasks` | AVAILABLE_DOCS に tasks.md を含める |
| パスのみ | `--paths-only` | `-PathsOnly` | 検証をスキップし、パスのみ出力 |

#### JSON 出力例

```json
{
  "FEATURE_DIR": "/path/to/.codexspec/specs/001-my-feature",
  "AVAILABLE_DOCS": ["research.md", "data-model.md", "tasks.md"]
}
```

### 4.2 `common.sh/ps1` - 共通ユーティリティ関数

クロスプラットフォームの共通機能を提供:

#### Bash バージョン関数

| 関数 | 機能 |
|------|------|
| `get_feature_id()` | Git ブランチまたは環境変数から feature ID を取得 |
| `get_specs_dir()` | specs ディレクトリパスを取得 |
| `is_codexspec_project()` | CodexSpec プロジェクトかどうかをチェック |
| `require_codexspec_project()` | CodexSpec プロジェクトであることを確認、そうでなければ終了 |
| `log_info/success/warning/error()` | カラーログ出力 |
| `command_exists()` | コマンドが存在するかチェック |

#### PowerShell バージョン関数

| 関数 | 機能 |
|------|------|
| `Get-RepoRoot` | Git リポジトリのルートディレクトリを取得 |
| `Get-CurrentBranch` | 現在のブランチ名を取得 |
| `Test-HasGit` | Git リポジトリがあるか検出 |
| `Test-FeatureBranch` | feature ブランチにいるか検証 |
| `Get-FeaturePathsEnv` | すべての feature 関連パスを取得 |
| `Test-FileExists` | ファイルが存在するかチェック |
| `Test-DirHasFiles` | ディレクトリにファイルがあるかチェック |

### 4.3 `create-new-feature.sh/ps1` - 新機能の作成

#### 機能

- 自動的にインクリメントする feature ID を生成（001, 002, ...）
- feature ディレクトリと初期 spec.md を作成
- 対応する Git ブランチを作成

#### 使用例

```bash
./create-new-feature.sh -n "user authentication" -i 001
```

## 5. Scripts を使用するコマンド

以下の 4 つのコマンドが scripts を使用します:

| コマンド | Scripts パラメータ | 機能 |
|------|--------------|------|
| `/codexspec.clarify` | `--json --paths-only` | パスを取得、ファイル検証なし |
| `/codexspec.checklist` | `--json` | plan.md の存在を検証 |
| `/codexspec.analyze` | `--json --require-tasks --include-tasks` | plan.md + tasks.md を検証 |
| `/codexspec.tasks-to-issues` | `--json --require-tasks --include-tasks` | plan.md + tasks.md を検証 |

## 6. 完全なワークフロー図

```
┌──────────────────────────────────────────────────────────────────────────┐
│                        初期化フェーズ                                      │
│                                                                          │
│  $ codexspec init my-project                                             │
│       │                                                                  │
│       ├── .codexspec/ ディレクトリ構造を作成                              │
│       ├── scripts/*.sh → .codexspec/scripts/ にコピー                    │
│       ├── templates/commands/*.md → .claude/commands/ にコピー           │
│       └── constitution.md, config.yml, CLAUDE.md を作成                  │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌──────────────────────────────────────────────────────────────────────────┐
│                        使用フェーズ (Claude Code)                          │
│                                                                          │
│  ユーザー: /codexspec.analyze                                            │
│       │                                                                  │
│       ├── Claude が .claude/commands/codexspec.analyze.md を読み込み     │
│       │                                                                  │
│       ├── YAML frontmatter の scripts 宣言を解析                         │
│       │   scripts:                                                       │
│       │     sh: .codexspec/scripts/check-prerequisites.sh --json ...    │
│       │                                                                  │
│       ├── {SCRIPT} プレースホルダーを置換                                 │
│       │                                                                  │
│       ├── スクリプトを実行:                                              │
│       │   $ .codexspec/scripts/check-prerequisites.sh --json ...        │
│       │                                                                  │
│       ├── JSON 出力を解析:                                               │
│       │   {"FEATURE_DIR": "...", "AVAILABLE_DOCS": [...]}               │
│       │                                                                  │
│       ├── spec.md, plan.md, tasks.md を読み込み                          │
│       │                                                                  │
│       └── 分析レポートを生成                                             │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
```

## 7. 設計のハイライト

### 7.1 クロスプラットフォーム互換性

Bash と PowerShell バージョンの両方をメンテナンスし、`sys.platform` で自動選択:

```python
if sys.platform == "win32":
    # PowerShell スクリプトをコピー
else:
    # Bash スクリプトをコピー
```

### 7.2 宣言的設定

YAML frontmatter でスクリプト依存関係を宣言し、明確で直感的:

```yaml
scripts:
  sh: .codexspec/scripts/check-prerequisites.sh --json
  ps: .codexspec/scripts/check-prerequisites.ps1 -Json
```

### 7.3 JSON 出力

スクリプトは構造化データを出力し、Claude が解析しやすい:

```json
{
  "FEATURE_DIR": "/path/to/.codexspec/specs/001-feature",
  "AVAILABLE_DOCS": ["research.md", "data-model.md"]
}
```

### 7.4 段階的検証

異なるコマンドは異なるパラメータを使用し、必要に応じて検証:

| フェーズ | コマンド | 検証レベル |
|------|------|----------|
| 計画前 | `/codexspec.clarify` | パスのみ |
| 計画後 | `/codexspec.checklist` | plan.md |
| タスク後 | `/codexspec.analyze` | plan.md + tasks.md |

### 7.5 Git 統合

- ブランチ名から自動的に feature ID を抽出
- ブランチ命名検証をサポート（`^\d{3}-` 形式）
- 環境変数オーバーライドをサポート（`SPECIFY_FEATURE` / `CODEXSPEC_FEATURE`）

## 8. 重要なコードパス

| ファイル | 行番号/場所 | 機能 |
|------|-----------|------|
| `src/codexspec/__init__.py` | 343-368 | スクリプトコピーロジック |
| `src/codexspec/__init__.py` | 71-90 | `get_scripts_dir()` パス解決 |
| `scripts/bash/check-prerequisites.sh` | 全文 | Bash 前提条件チェックメインスクリプト |
| `scripts/powershell/check-prerequisites.ps1` | 56-146 | PowerShell 前提条件チェックスクリプト |
| `scripts/bash/common.sh` | 全文 | Bash 共通ユーティリティ関数 |
| `scripts/powershell/common.ps1` | 全文 | PowerShell 共通ユーティリティ関数 |
| `templates/commands/*.md` | YAML frontmatter | スクリプト宣言 |

## 9. スクリプトファイルリスト

### Bash スクリプト (`scripts/bash/`)

```
scripts/bash/
├── check-prerequisites.sh   # 前提条件チェックメインスクリプト
├── common.sh                # 共通ユーティリティ関数
└── create-new-feature.sh    # 新機能の作成
```

### PowerShell スクリプト (`scripts/powershell/`)

```
scripts/powershell/
├── check-prerequisites.ps1  # 前提条件チェックメインスクリプト
├── common.ps1               # 共通ユーティリティ関数
└── create-new-feature.ps1   # 新機能の作成
```

---

*このドキュメントは CodexSpec プロジェクトにおける scripts の完全なアーキテクチャと使用フローを記録しています。更新がある場合は、同期して修正してください。*
