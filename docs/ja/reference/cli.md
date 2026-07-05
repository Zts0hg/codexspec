# CLI リファレンス

## コマンド

### `codexspec init`

新しい CodexSpec プロジェクトを初期化します。

```bash
codexspec init [PROJECT_NAME] [OPTIONS]
```

**引数:**

| 引数 | 説明 |
|----------|-------------|
| `PROJECT_NAME` | 新しいプロジェクトディレクトリの名前 (カレントディレクトリには `.` または `--here` を使用) |

**オプション:**

| オプション | 短縮形 | 説明 |
|--------|-------|-------------|
| `--here` | `-h` | カレントディレクトリに初期化 |
| `--ai` | `-a` | 使用する AI アシスタント: `claude`, `codex`, `both` (デフォルト: claude) |
| `--lang` | `-l` | 出力 (ベース) 言語。interaction/document/commit はこれにフォールバック (例: en, zh-CN, ja) |
| `--interaction-lang` | | 対話言語 (LLM の対話 + `codexspec` CLI 出力)。`--lang` を上書き |
| `--document-lang` | | ドキュメント言語 (生成される requirements/spec/plan/tasks)。`--lang` を上書き |
| `--commit-lang` | | コミットメッセージの言語。`--lang` を上書き |
| `--force` | `-f` | 既存ファイルを上書きしプロンプトを自動承認。`config.yml` は再生成しない |
| `--no-git` | | git リポジトリの初期化をスキップ |
| `--debug` | `-d` | デバッグ出力を有効化 |

`--lang` は `output` のベース言語を設定します。`--interaction-lang`、`--document-lang`、`--commit-lang` は自身の次元についてこれを上書きします (各々は `output` に、さらに `en` にフォールバック)。モデル全体は [国際化](../user-guide/i18n.md) を参照してください。

TTY 環境で `--lang` を付けずに (かつ 3 つの次元フラグもすべて付けずに) 初めて init を実行するとベース言語のプロンプトが出ます。非 TTY (CI/スクリプト) では `en` がデフォルトとなり、**完全に非対話** です。init を再実行しても、指定しなかった言語キーは保持されます。`--force` は `config.yml` を再生成しません。

**例:**

```bash
# 新規プロジェクトを作成
codexspec init my-project

# カレントディレクトリに初期化
codexspec init . --ai claude

# 一度だけの実行 (インストールなし) ― Codex CLI や両方向けに初期化
uvx codexspec init . --ai codex
uvx codexspec init . --ai both

# 完全非対話: 出力ベースを zh-CN、コミットメッセージを英語
codexspec init my-project --lang zh-CN --commit-lang en

# すべての次元を明示的に指定 (スクリプト可能、プロンプトなし)
codexspec init my-project \
  --interaction-lang zh-CN --document-lang en --commit-lang en
```

---

### `codexspec check`

インストール済みのツールを確認します。

```bash
codexspec check
```

---

### `codexspec version`

バージョン情報を表示します。

```bash
codexspec version
```

---

### `codexspec config`

プロジェクト設定を表示・変更します。

```bash
codexspec config [OPTIONS]
```

**オプション:**

| オプション | 短縮形 | 説明 |
|--------|-------|-------------|
| `--set-lang` | `-l` | 出力 (ベース) 言語を設定 |
| `--set-interaction-lang` | | 対話言語 (LLM の対話 + CLI 出力) を設定 |
| `--set-document-lang` | | ドキュメント言語 (生成される spec/plan/tasks) を設定 |
| `--set-commit-lang` | `-c` | コミットメッセージの言語を設定 |
| `--list-langs` | | サポートされているすべての言語を一覧表示 |
| `--auto-next` | | `workflow.auto_next` の切り替え/設定 (フラグ単独でトグル、on/off も可) |

各 `--set-*-lang` は [言語の次元](../user-guide/i18n.md) のいずれかを更新します。設定しなかった次元は `output` に、さらに `en` にフォールバックします。
