# Scripts アーキテクチャ分析

このドキュメントは、CodexSpec プロジェクトにおける scripts のコードロジックフローと、それらが Claude Code でどのように使われるかを詳細に説明します。

## 1. 全体アーキテクチャの概要

CodexSpec は **Spec-Driven Development (SDD)** ツールキットであり、CLI + テンプレート + 補助スクリプトの 3 層アーキテクチャを採用しています。

```
┌─────────────────────────────────────────────────────────────────┐
│                        ユーザー層 (CLI)                          │
│  codexspec init | check | version | config                      │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    Claude Code 対話層                            │
│  /codexspec:specify | /codexspec:analyze | ...                  │
│  (.claude/commands/*.md)                                        │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                      補助スクリプト層                            │
│  .codexspec/scripts/*.sh (Bash) または *.ps1 (PowerShell)       │
└─────────────────────────────────────────────────────────────────┘
```

## 2. Scripts のデプロイフロー

### フェーズ 1: `codexspec init` による初期化

`src/codexspec/__init__.py` の `init()` 関数 (343-368 行目) で、OS に応じて対応するスクリプトを自動コピーします。

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

**結果**: OS に応じて、`scripts/bash/` または `scripts/powershell/` のスクリプトがプロジェクトの `.codexspec/scripts/` ディレクトリにコピーされます。

### パス解決の仕組み

`get_scripts_dir()` 関数 (71-90 行目) は複数のインストール形態を扱います。

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

## 3. Claude Code におけるスクリプトの呼び出し仕組み

### 中核の仕組み: YAML frontmatter による宣言

テンプレートファイルは YAML frontmatter でスクリプトの依存関係を宣言します。

```yaml
---
description: コマンドの説明
scripts:
  sh: .codexspec/scripts/check-prerequisites.sh --json --require-tasks --include-tasks
  ps: .codexspec/scripts/check-prerequisites.ps1 -Json -RequireTasks -IncludeTasks
---
```

### プレースホルダの置き換え

テンプレート内では `{SCRIPT}` プレースホルダを使います。

```markdown
### 1. Initialize Context

Run `{SCRIPT}` from repo root and parse JSON for:
- `FEATURE_DIR` - 機能ディレクトリのパス
- `AVAILABLE_DOCS` - 利用可能なドキュメントの一覧
```

### 呼び出しフロー

1. ユーザーが Claude Code で `/codexspec:analyze` を入力
2. Claude が `.claude/commands/codexspec:analyze.md` テンプレートを読み込む
3. OS に応じて、Claude は `{SCRIPT}` を次のように置き換える:
   - **macOS/Linux**: `.codexspec/scripts/check-prerequisites.sh --json --require-tasks --include-tasks`
   - **Windows**: `.codexspec/scripts/check-prerequisites.ps1 -Json -RequireTasks -IncludeTasks`
4. Claude がスクリプトを実行し、JSON 出力をパースして後続の操作に進む

## 4. Scripts の機能詳細

### 4.1 `check-prerequisites.sh/ps1` - 前提条件チェックスクリプト

最も重要なスクリプトで、環境状態を検証して構造化された情報を返します。

#### コア機能

- 現在 feature ブランチにいるかを検証 (フォーマット: `2026-0613-1200ab-feature-name`)
- 必須ファイル (`plan.md`, `tasks.md`) の存在を検出
- JSON 形式でパス情報を返す

#### パラメータオプション

| パラメータ | Bash | PowerShell | 役割 |
|------|------|------------|------|
| JSON 出力 | `--json` | `-Json` | JSON 形式で出力 |
| tasks.md を要求 | `--require-tasks` | `-RequireTasks` | tasks.md の存在を検証 |
| tasks.md を含める | `--include-tasks` | `-IncludeTasks` | AVAILABLE_DOCS に tasks.md を含める |
| パスのみ | `--paths-only` | `-PathsOnly` | 検証をスキップしパスのみ出力 |

#### JSON 出力の例

```json
{
  "FEATURE_DIR": "/path/to/.codexspec/specs/2026-0613-1200ab-my-feature",
  "AVAILABLE_DOCS": ["research.md", "data-model.md", "tasks.md"]
}
```

### 4.2 `common.sh/ps1` - 共通ユーティリティ関数

クロスプラットフォームな共通機能を提供します。

#### Bash 版の関数

| 関数 | 役割 |
|------|------|
| `get_feature_id()` | Git ブランチや環境変数から feature ID を取得 |
| `get_specs_dir()` | specs ディレクトリのパスを取得 |
| `is_codexspec_project()` | CodexSpec プロジェクトかどうかを確認 |
| `require_codexspec_project()` | CodexSpec プロジェクト内であることを保証、そうでなければ終了 |
| `log_info/success/warning/error()` | カラー付きログ出力 |
| `command_exists()` | コマンドが存在するかを確認 |

#### PowerShell 版の関数

| 関数 | 役割 |
|------|------|
| `Get-RepoRoot` | Git リポジトリのルートディレクトリを取得 |
| `Get-CurrentBranch` | 現在のブランチ名を取得 |
| `Test-HasGit` | Git リポジトリがあるかを検出 |
| `Test-FeatureBranch` | feature ブランチにいるかを検証 |
| `Get-FeaturePathsEnv` | feature 関連のすべてのパスを取得 |
| `Test-FileExists` | ファイルが存在するかを確認 |
| `Test-DirHasFiles` | ディレクトリにファイルがあるかを確認 |

### 4.3 `create-new-feature.sh/ps1` - 新機能の作成

#### 機能

- `YYYY-MMDD-HHMMxx` 形式の feature ID を自動生成
- feature ディレクトリと初期 requirements.md を作成
- 対応する Git ブランチを作成
- 短縮名を正規化したあと、ASCII 文字または数字を少なくとも 1 つ含むことを要求

#### 使用例

```bash
./create-new-feature.sh -n "user authentication"
```

#### 機能の命名規約

- 連番 `NNN-name` 形式の識別子はサポートされません。タイムスタンプ名のみが
  サポートされる機能命名形式です。
- レガシー互換性は成果物に適用されます。`requirements.md` が存在しない場合は、
  既存の `spec.md` が使われることがあります。これは代替のディレクトリや
  ブランチ命名形式を有効にするものではありません。
- 機能のフルネームはワークスペースを一意に特定します:
  `YYYY-MMDD-HHMMxx-short-name`。独立して作成されたワークスペースは、
  短縮名が異なる場合に同じタイムスタンプ ID を共有することがあります。
- 短縮 ID のルックアップはローカルの利便性のためだけのものです。複数ディレクトリが
  一致する場合、解決はワークスペースを選択・上書きせずに曖昧さを報告します。

## 5. Scripts を使用するコマンド

次の 4 つのコマンドが scripts を使用します。

| コマンド | Scripts パラメータ | 役割 |
|------|--------------|------|
| `/codexspec:clarify` | `--json --paths-only` | パスを取得し、ファイルを検証しない |
| `/codexspec:checklist` | `--json` | plan.md の存在を検証 |
| `/codexspec:analyze` | `--json --require-tasks --include-tasks` | plan.md と tasks.md を検証 |
| `/codexspec:tasks-to-issues` | `--json --require-tasks --include-tasks` | plan.md と tasks.md を検証 |

## 6. 完全なワークフロー図

```
┌──────────────────────────────────────────────────────────────────────────┐
│                        初期化フェーズ                                     │
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
│                        使用フェーズ (Claude Code)                         │
│                                                                          │
│  ユーザー: /codexspec:analyze                                            │
│       │                                                                  │
│       ├── Claude が .claude/commands/codexspec:analyze.md を読み込み     │
│       │                                                                  │
│       ├── YAML frontmatter の scripts 宣言をパース                       │
│       │   scripts:                                                       │
│       │     sh: .codexspec/scripts/check-prerequisites.sh --json ...     │
│       │                                                                  │
│       ├── {SCRIPT} プレースホルダを置き換え                               │
│       │                                                                  │
│       ├── スクリプトを実行:                                              │
│       │   $ .codexspec/scripts/check-prerequisites.sh --json ...         │
│       │                                                                  │
│       ├── JSON 出力をパース:                                             │
│       │   {"FEATURE_DIR": "...", "AVAILABLE_DOCS": [...]}               │
│       │                                                                  │
│       ├── spec.md, plan.md, tasks.md を読み込み                          │
│       │                                                                  │
│       └── 分析レポートを生成                                             │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
```

## 7. 設計の亮点

### 7.1 クロスプラットフォーム互換

Bash 版と PowerShell 版を両方保守し、`sys.platform` で自動選択します。

```python
if sys.platform == "win32":
    # PowerShell スクリプトをコピー
else:
    # Bash スクリプトをコピー
```

### 7.2 宣言的設定

YAML frontmatter でスクリプトの依存関係を宣言し、明快さを実現します。

```yaml
scripts:
  sh: .codexspec/scripts/check-prerequisites.sh --json
  ps: .codexspec/scripts/check-prerequisites.ps1 -Json
```

### 7.3 JSON 出力

スクリプトが構造化データを出力するため、Claude がパースしやすくなります。

```json
{
  "FEATURE_DIR": "/path/to/.codexspec/specs/2026-0613-1200ab-feature",
  "AVAILABLE_DOCS": ["research.md", "data-model.md"]
}
```

### 7.4 段階的検証

コマンドごとに異なるパラメータを使い、必要に応じて検証します。

| フェーズ | コマンド | 検証レベル |
|------|------|----------|
| 計画前 | `/codexspec:clarify` | パスのみ |
| 計画後 | `/codexspec:checklist` | plan.md |
| タスク後 | `/codexspec:analyze` | plan.md + tasks.md |

### 7.5 Git 連携

- ブランチ名から feature ID を自動抽出
- ブランチ命名の検証をサポート (`^\d{3}-` 形式)
- 環境変数による上書きをサポート (`CODEXSPEC_FEATURE`)

## 8. 主要コードパス

| ファイル | 行番号/位置 | 機能 |
|------|-----------|------|
| `src/codexspec/__init__.py` | 343-368 | スクリプトコピーのロジック |
| `src/codexspec/__init__.py` | 71-90 | `get_scripts_dir()` のパス解決 |
| `scripts/bash/check-prerequisites.sh` | 全文 | Bash 前提条件チェックのメインスクリプト |
| `scripts/powershell/check-prerequisites.ps1` | 56-146 | PowerShell 前提条件チェックスクリプト |
| `scripts/bash/common.sh` | 全文 | Bash 共通ユーティリティ関数 |
| `scripts/powershell/common.ps1` | 全文 | PowerShell 共通ユーティリティ関数 |
| `templates/commands/*.md` | YAML frontmatter | スクリプト宣言 |

## 9. スクリプトファイル一覧

### Bash スクリプト (`scripts/bash/`)

```
scripts/bash/
├── check-prerequisites.sh   # 前提条件チェックのメインスクリプト
├── common.sh                # 共通ユーティリティ関数
└── create-new-feature.sh    # 新機能の作成
```

### PowerShell スクリプト (`scripts/powershell/`)

```
scripts/powershell/
├── check-prerequisites.ps1  # 前提条件チェックのメインスクリプト
├── common.ps1               # 共通ユーティリティ関数
└── create-new-feature.ps1   # 新機能の作成
```

---

*このドキュメントは CodexSpec プロジェクトにおける scripts の完全なアーキテクチャと利用フローを記録したものです。更新があれば、合わせて修正してください。*
