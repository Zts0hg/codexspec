<a id="installation"></a>

# インストール

<a id="install-with-the-codex-desktop-app"></a>

## Codex デスクトップアプリでのインストール

デスクトップアプリから Codex に依頼すれば、CodexSpec のインストールとプロジェクトのセットアップを直接実行できます。

1. Codex デスクトップアプリにローカルプロジェクトを追加し、作業するフォルダーを選びます。
2. そのプロジェクトでチャットを開始し、次のプロンプトを貼り付けます。
3. 依存関係のダウンロードやインストールについてアプリが許可を求めたら、該当する操作を承認して続行します。

```text
Please install and initialize CodexSpec in the current project.
Project: https://github.com/Zts0hg/codexspec

Complete the setup directly instead of asking me to run terminal commands.

Check the environment. If uv or Python 3.11+ is missing, install the required
tools in my user directory using their official installation instructions.
Install the latest stable release of CodexSpec.

For a new setup, initialize the current project for Codex in English:
codexspec init . --ai codex --lang en

If CodexSpec is already configured, check its version and configuration before
updating. Preserve existing requirements, project principles, user files,
and configuration settings.

Verify that the CLI works and that AGENTS.md and the CodexSpec skill files
under .agents/skills/ are installed. Explain the result and how to start
describing my requirements in plain English. If the skills are not yet
available in this chat, tell me whether to start a new chat or restart the app.
```

中国語での応答とドキュメントが必要な場合は、`--lang en` を `--lang zh-CN` に置き換え、結果も中国語で説明するよう Codex に依頼してください。

この方法でインストールされる CLI とプロジェクトスキルは、以下の手動セットアップと同じです。
`$codexspec:specify I want to build a todo application` のようなプロンプトで利用を始められます。
ローカルスキルの検出と更新については、[OpenAI のスキルガイド](https://learn.chatgpt.com/docs/build-skills)を参照してください。

<a id="prerequisites"></a>

## 前提条件

- Python 3.11+
- [uv](https://docs.astral.sh/uv/)（推奨）、または pip
- 使用するアシスタント：Claude Code または Codex
- worktree での開発や Git ワークフローを利用する場合は Git

<a id="cli-installation"></a>

## CLI のインストール

```bash
uv tool install codexspec

# Or use pip
pip install codexspec

# Verify the CLI and inspect available commands
codexspec version
codexspec --help
codexspec list-commands
```

新しいプロジェクトは `codexspec init my-project --ai claude`、現在のディレクトリは
`codexspec init . --ai codex` で初期化します。両方の連携を使う場合は `--ai both` を指定してください。
アシスタントのデフォルトは `claude` です。Codex または両方を使う場合は、値を明示的に指定します。

<details>
<summary>その他のインストール方法</summary>

<a id="one-time-initialization"></a>

### 一度だけ実行する初期化

```bash
uvx codexspec init my-project --ai claude
uvx codexspec init . --ai codex
```

この方法では、プロジェクトコマンドと単独で動作するコミット実行環境がインストールされます。
worktree の作業先選択、blueprint/auto-dev、手動のプロファイルレビューは引き続き CodexSpec CLI を呼び出すため、
これらのワークフローを使う場合は CLI も利用できるようにしておいてください。

<a id="development-versions"></a>

### 開発版

```bash
uv tool install git+https://github.com/Zts0hg/codexspec.git
uv tool install git+https://github.com/Zts0hg/codexspec.git@main

# Replace <tag> with the version you want
uv tool install git+https://github.com/Zts0hg/codexspec.git@<tag>
```

</details>

<details>
<summary>Windows でのインストール</summary>

PowerShell で実行します。

```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
# Restart PowerShell, then:
uv tool install codexspec
codexspec version
```

PATH やインストールに関する問題への対処は、[Windows トラブルシューティングガイド](../WINDOWS-TROUBLESHOOTING.md)を参照してください。

</details>

<a id="upgrade-and-refresh-a-project"></a>

## アップグレードとプロジェクトの更新

CLI の更新と、プロジェクトにインストール済みのコマンドの更新は、それぞれ別に行います。

```bash
uv tool install codexspec --upgrade
# Or: pip install --upgrade codexspec

# In the project you want to refresh; select its desired integration(s)
codexspec init . --force --ai both
```

片方の連携だけが必要な場合は、`--ai claude` または `--ai codex` を指定してください。
`--force` は配布コマンドとスクリプトを再生成し、レビューリソースを更新します。
移行、コマンド更新、プロジェクト憲法への準拠に関する確認も自動で承認します。
既存の要件とプロジェクト原則は維持されます。コンテキストファイルも既存の本文を残したまま、管理対象のガイダンスだけを更新します。
明示的に設定していない設定キーは、そのまま保持されます。

計画作成には `design-to-plan` を使います。インストールの更新時に旧 `spec-to-plan` エントリは廃止され、エイリアスも残りません。

<a id="plugin-marketplace-installation"></a>

## プラグインマーケットプレイスからのインストール

Claude Code では、マーケットプレイスからプラグインをインストールできます。

```text
/plugin marketplace add Zts0hg/codexspec
/plugin install codexspec@codexspec-market
/codexspec:config
```

プラグインにはコマンドに加え、ステージ済み内容のコミット分析と過去の要件の参照を促す、セッション開始時のガイダンスが含まれます。
再開したセッションにも適用されます。プラグインのインストールだけではプロジェクトは初期化されません。
言語、ワークフロー、レビューの設定を作成・変更するには `/codexspec:config` を使ってください。
プロジェクトの基本構成をすべて用意する場合は、CLI で初期化します。

コミットのプレビューや、許可を得て現在のチェックアウトで行うコミットは、Python 3.11+ と Git があれば、
常設の CodexSpec CLI がなくても同梱の実行環境で実行できます。
worktree の作業先選択、blueprint/auto-dev、手動のプロファイルレビューには引き続き CLI が必要です。
プラグインの起動フックを使うには、PATH 上の Git と、コマンドフックの `args`（exec 形式）に対応した Claude Code バージョンが必要です。
このガイダンスはエージェントへの指示であり、手動で実行する Git コマンドには介入しません。

詳しいセットアップ方法は、[インストール](installation.md)を参照してください。
