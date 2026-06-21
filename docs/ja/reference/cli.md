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
| `PROJECT_NAME` | 新しいプロジェクトディレクトリの名前 (現在のディレクトリには `.` または `--here` を使用) |

**オプション:**

| オプション | 短縮形 | 説明 |
|--------|-------|-------------|
| `--here` | `-h` | 現在のディレクトリで初期化 |
| `--ai` | `-a` | 使用する AI アシスタント (デフォルト: claude) |
| `--lang` | `-l` | 出力 (ベース) 言語。interaction/document/commit はこれにフォールバック (例: en, zh-CN, ja) |
| `--interaction-lang` | | インタラクション言語 (LLM との対話 + `codexspec` CLI 出力)。`--lang` を上書き |
| `--document-lang` | | ドキュメント言語 (生成される requirements/spec/plan/tasks)。`--lang` を上書き |
| `--commit-lang` | | コミットメッセージ言語。`--lang` を上書き |
| `--force` | `-f` | 既存のファイルを上書きしプロンプトを自動承認。`config.yml` は再生成しない |
| `--no-git` | | git リポジトリの初期化をスキップ |
| `--debug` | `-d` | デバッグ出力を有効化 |

`--lang` は `output` ベース言語を設定します。`--interaction-lang`、`--document-lang`、`--commit-lang` はそれぞれの次元についてこれを上書きします (各々は `output`、次いで `en` にフォールバック)。完全なモデルについては [国際化](../user-guide/i18n.md) を参照してください。

TTY 環境で `--lang` を付けずに (かつ 3 つの次元フラグすべてを付けずに) 初回 init を実行するとベース言語の入力を求められます。非 TTY (CI/スクリプト) では `en` がデフォルトとなり **完全に非対話型** です。`init` を再実行しても、指定しなかった言語キーは保持されます。`--force` は `config.yml` を再生成しません。

**例:**

```bash
# 新しいプロジェクトを作成
codexspec init my-project

# 現在のディレクトリで初期化
codexspec init . --ai claude

# 完全に非対話型: zh-CN ベース、英語のコミットメッセージ
codexspec init my-project --lang zh-CN --commit-lang en

# 各次域を明示的に設定 (スクリプト可能、プロンプトなし)
codexspec init my-project \
  --interaction-lang zh-CN --document-lang en --commit-lang en
```

---

### `codexspec check`

インストールされているツールを確認します。

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

プロジェクト設定を表示または変更します。

```bash
codexspec config [OPTIONS]
```

**オプション:**

| オプション | 短縮形 | 説明 |
|--------|-------|-------------|
| `--set-lang` | `-l` | 出力 (ベース) 言語を設定 |
| `--set-interaction-lang` | | インタラクション言語 (LLM との対話 + CLI 出力) を設定 |
| `--set-document-lang` | | ドキュメント言語 (生成される spec/plan/tasks) を設定 |
| `--set-commit-lang` | `-c` | コミットメッセージ言語を設定 |
| `--list-langs` | | サポートされているすべての言語を一覧表示 |

各 `--set-*-lang` は 1 つの [言語次元](../user-guide/i18n.md) を更新します。設定しなかった次元は `output`、次いで `en` にフォールバックします。
