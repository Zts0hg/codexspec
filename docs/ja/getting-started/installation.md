# インストール

## 前提条件

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) (推奨) または pip

## オプション 1: uv でインストール (推奨)

CodexSpec をインストールする最も簡単な方法は uv を使うことです。

```bash
uv tool install codexspec
```

## オプション 2: pip でインストール

代わりに pip を使うこともできます。

```bash
pip install codexspec
```

## オプション 3: インストールせずに一度だけ実行

インストールを行わずに、直接実行することもできます。

```bash
# 新規プロジェクトを作成
uvx codexspec init my-project

# 既存プロジェクトで Claude Code 向けに初期化
cd your-existing-project
uvx codexspec init . --ai claude

# Codex CLI 向けに初期化
uvx codexspec init . --ai codex

# Claude Code と Codex CLI の両方向けに初期化 (.claude/ と .agents/ の両方を書き出し)
uvx codexspec init . --ai both
```

## オプション 4: GitHub からインストール

最新の開発版を使いたい場合はこちら。

```bash
# uv を使う場合
uv tool install git+https://github.com/Zts0hg/codexspec.git

# pip を使う場合
pip install git+https://github.com/Zts0hg/codexspec.git

# 特定のブランチやタグ
uv tool install git+https://github.com/Zts0hg/codexspec.git@main
uv tool install git+https://github.com/Zts0hg/codexspec.git@v0.5.6
```

## オプション 5: プラグインマーケットプレースからのインストール (代替手段)

CodexSpec は Claude Code のプラグインとしても利用できます。CLI ツールをインストールせずに CodexSpec のスラッシュコマンドを Claude Code 上で直接使いたい場合に適しています。CLI は完全な Requirements-First SDD の体験を提供する一方、プラグインは Claude Code 上でスラッシュコマンド群を利用できるようにします。

### インストール手順

Claude Code 内で次を実行します。

```bash
# マーケットプレースを追加
> /plugin marketplace add Zts0hg/codexspec

# プラグインをインストール
> /plugin install codexspec@codexspec-market
```

### プラグイン利用者の言語設定

プラグインマーケットプレースからインストールした後は、`/codexspec:config` スラッシュコマンドを使って希望の言語を設定します (CLI の `codexspec config` コマンドは CLI のインストールがないと使えません)。

```bash
# 対話型設定を起動
> /codexspec:config

# または現在の設定を表示
> /codexspec:config --view
```

config コマンドは出力言語 (生成されるドキュメントの言語) とコミットメッセージの言語の選択を対話的に案内し、`.codexspec/config.yml` に書き出します。多言語サポートは CLI と同じ LLM による動的翻訳を利用します。

### インストール方法の比較

| 方法 | 向いている用途 | 提供される機能 |
|--------|----------|----------|
| **CLI インストール** (`uv tool install` または `pip install`) | 完全な開発ワークフロー | CLI コマンド (`init`, `check`, `config`, `version`) + スラッシュコマンド |
| **プラグインマーケットプレース** | クイックスタート、既存プロジェクト | スラッシュコマンドのみ (言語設定には `/codexspec:config` を使用) |

**注**: プラグインは `strict: false` モードを使用し、LLM による動的翻訳を通じた既存の多言語サポートを再利用します。

## インストールの確認

```bash
codexspec --help
codexspec version
```

(プラグインマーケットプレースからのインストールの場合は、Claude Code 内で `/codexspec:config --view` などのスラッシュコマンドを実行して確認してください。)

## アップグレード

```bash
# uv を使う場合
uv tool install codexspec --upgrade

# pip を使う場合
pip install --upgrade codexspec
```

(プラグインマーケットプレースからのインストールは Claude Code のプラグインマネージャによって更新されます。)

## 次のステップ

[クイックスタート](quick-start.md)
