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
| `PROJECT_NAME` | 新しいプロジェクトディレクトリの名前 |

**オプション:**

| オプション | 短縮形 | 説明 |
|--------|-------|-------------|
| `--here` | `-h` | 現在のディレクトリで初期化 |
| `--ai` | `-a` | 使用する AI アシスタント (デフォルト: claude) |
| `--lang` | `-l` | 出力言語 (例: en, zh-CN, ja) |
| `--force` | `-f` | 既存のファイルを強制的に上書き |
| `--no-git` | | git 初期化をスキップ |
| `--debug` | `-d` | デバッグ出力を有効化 |

**例:**

```bash
# 新しいプロジェクトを作成
codexspec init my-project

# 現在のディレクトリで初期化
codexspec init . --ai claude

# 中国語で出力
codexspec init my-project --lang zh-CN
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
| `--set-lang` | `-l` | 出力言語を設定 |
| `--list-langs` | | サポートされているすべての言語を一覧表示 |
