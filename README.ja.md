<div align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="codexspec-logo-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="codexspec-logo-light.svg">
    <img alt="CodexSpec Logo" src="codexspec-logo-light.svg" width="420">
  </picture>
</div>

<h1 align="center">CodexSpec</h1>

<p align="center">
  <a href="README.md">English</a> | <a href="README.zh-CN.md">中文</a> | <b>日本語</b> | <a href="README.es.md">Español</a> | <a href="README.pt-BR.md">Português</a> | <a href="README.ko.md">한국어</a> | <a href="README.de.md">Deutsch</a> | <a href="README.fr.md">Français</a>
</p>

<p align="center">
  <a href="https://pypi.org/project/codexspec/"><img src="https://img.shields.io/pypi/v/codexspec.svg?style=for-the-badge" alt="PyPI version"></a>
  <a href="https://pypi.org/project/codexspec/"><img src="https://img.shields.io/pypi/pyversions/codexspec.svg?style=for-the-badge" alt="Python versions"></a>
  <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge" alt="License: MIT"></a>
</p>

<p align="center">
  <strong>Claude Code と OpenAI Codex 向けの要件優先 SDD ツールキット</strong>
</p>

CodexSpec は、確認済みの要件をもとに、仕様書、設計、計画、タスク、実装を作成し、それぞれのつながりを追跡できるようにします。
**何を**作るか、**なぜ**作るかはユーザーが決めます。エージェントはその要件の範囲内で、
レビューの節目とプロジェクトに保存した知識を活用しながら、**どのように**実現するかを具体化します。

Claude Code のスラッシュコマンド、Codex のスキル、または両方から利用できます。
通常の機能開発には、デフォルトで機能ごとに独立した Git worktree を使います。
共有ブループリントを利用すると、確認済み要件のキューをエージェントに自律的に開発させることもできます。

[📖 ドキュメント](https://zts0hg.github.io/codexspec/) | [中文文档](https://zts0hg.github.io/codexspec/zh/) | [日本語ドキュメント](https://zts0hg.github.io/codexspec/ja/) | [한국어 문서](https://zts0hg.github.io/codexspec/ko/) | [Documentación](https://zts0hg.github.io/codexspec/es/) | [Documentation](https://zts0hg.github.io/codexspec/fr/) | [Dokumentation](https://zts0hg.github.io/codexspec/de/) | [Documentação](https://zts0hg.github.io/codexspec/pt-BR/)

## 目次

- [CodexSpec を選ぶ理由](#codexspec-を選ぶ理由)
- [30 秒クイックスタート](#30-秒クイックスタート)
- [インストール](#インストール)
- [基本ワークフロー](#基本ワークフロー)
- [共有ブループリントと自律開発](#共有ブループリントと自律開発)
- [worktree での開発](#worktree-での開発)
- [既存コードでの作業](#既存コードでの作業)
- [レビューとデバッグ](#レビューとデバッグ)
- [プロジェクト知識](#プロジェクト知識)
- [Git ワークフロー](#git-ワークフロー)
- [利用可能なコマンド](#利用可能なコマンド)
- [設定と国際化](#設定と国際化)
- [プロジェクト構成](#プロジェクト構成)
- [拡張機能の作成資料](#拡張機能の作成資料)
- [開発](#開発)
- [貢献](#貢献)
- [ライセンス](#ライセンス)

## CodexSpec を選ぶ理由

| 必要なこと | CodexSpec でできること |
|------|-------------------------|
| 製品として何を実現するかを明確にする | 仕様書を作成する前に要件を明示的に確認し、`requirements.md` に保存 |
| 開発の経緯を追跡する | 要件 → 仕様 → 設計 → 計画 → タスクを、出典へのリンクで結び付ける |
| 判断の妥当性をレビューする | 4 つの成果物レビューコマンド、成果物間の分析、独立したコード欠陥ゲート |
| セッションや担当者が変わっても作業を引き継ぐ | 機能ごとの記録、プロジェクト原則、再利用できる知識、関連する過去の判断 |
| 複数の機能を並行して開発する | 通常の機能ごとに Git worktree を用意し、同じワークスペースを継続して再利用 |
| 作業をさらに自動化する | 設定に応じたステージの自動進行と、確認済みブループリント要件の自律開発 |
| チームに合った言語で作業する | 対話、ドキュメント、コミットの言語を個別に設定 |

### 要件優先 SDD とは

要件優先の仕様駆動開発では、**確認済み要件を、その機能について最優先の判断基準**とします。
エージェントは実装に向けた成果物を作成する前に、目標、制約、判断、除外事項、未解決の質問、確認の根拠を記録します。

```text
Idea → Confirmed Requirements → Spec → Design → Plan → Tasks → Code
```

製品として何を実現するかは、人との協働を通じて定め、変更します。
自動レビューでは、作成した成果物がその意図に沿っているかを確認します。
自動化を有効にすると、合格したステージから次へ進みます。エージェントが確認済み要件を無断で置き換えることはありません。

## 30 秒クイックスタート

CodexSpec をインストールし、使うアシスタントに合わせてプロジェクトを初期化します。

```bash
uv tool install codexspec

# Create a new project for Claude Code
codexspec init my-project --ai claude

# Or initialize an existing project for Codex
cd your-existing-project
codexspec init . --ai codex

# Use --ai both when you want both integrations
```

初期化したプロジェクトで、インストール済みのアシスタントを起動してください。
ワークフローは共通ですが、呼び出し方は次のように異なります。

| アシスタント | 要件の検討を始めるコマンド |
|-----------|------------------------------|
| Claude Code (`claude`) | `/codexspec:specify I want to build a todo application` |
| Codex (`codex`) | `$codexspec:specify I want to build a todo application` |

必要に応じて `constitution` でプロジェクト原則を調整してください。
最終的な要件サマリーを確認したら、返された機能ディレクトリとワークスペースで作業を続けます。
以降のコマンドについては、[基本ワークフロー](#基本ワークフロー)を参照してください。

Codex デスクトップアプリをお使いの場合は、[Codex にインストールとプロジェクトの初期化を依頼できます](#codex-デスクトップアプリでのインストール)。

## インストール

### Codex デスクトップアプリでのインストール

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

### 前提条件

- Python 3.11+
- [uv](https://docs.astral.sh/uv/)（推奨）、または pip
- 使用するアシスタント：Claude Code または Codex
- worktree での開発や Git ワークフローを利用する場合は Git

### CLI のインストール

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

#### 一度だけ実行する初期化

```bash
uvx codexspec init my-project --ai claude
uvx codexspec init . --ai codex
```

この方法では、プロジェクトコマンドと単独で動作するコミット実行環境がインストールされます。
worktree の作業先選択、blueprint/auto-dev、手動のプロファイルレビューは引き続き CodexSpec CLI を呼び出すため、
これらのワークフローを使う場合は CLI も利用できるようにしておいてください。

#### 開発版

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

PATH やインストールに関する問題への対処は、[Windows トラブルシューティングガイド](docs/en/WINDOWS-TROUBLESHOOTING.md)を参照してください。

</details>

### アップグレードとプロジェクトの更新

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

### プラグインマーケットプレイスからのインストール

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

詳しいセットアップ方法は、[インストール](docs/en/getting-started/installation.md)を参照してください。

## 基本ワークフロー

標準的な機能開発では、各成果物を出典と結び付け、次の流れで進めます。

```text
/specify          → requirements.md
/generate-spec    → spec.md       → review-spec
/spec-to-design   → design.md     → review-design
/design-to-plan   → plan.md       → review-plan
/plan-to-tasks    → tasks.md      → review-tasks → analyze
/implement-tasks  → implementation and complete-feature code review
```

以下の例は、Claude の `/codexspec:` プレフィックスを使っています。
Codex では、コマンド名と引数はそのままに、`$codexspec:` を使ってください。

| ステップ | コマンド | 目的と出力 |
|------|---------|--------------------|
| プロジェクト原則 | `/codexspec:constitution` | `constitution.md` を作成・更新し、影響を受ける成果物を検証 |
| 要件 | `/codexspec:specify <idea>` | 意図を話し合い、最終サマリーを確認して `requirements.md` に保存 |
| 仕様書 | `/codexspec:generate-spec <feature-dir>` | 確認済み要件をもとに、出典参照付きの `spec.md` を作成 |
| システム設計 | `/codexspec:spec-to-design <feature-dir>` | コンポーネント、インターフェース、主要な設計判断を記した `design.md` を作成 |
| 実装計画 | `/codexspec:design-to-plan <feature-dir>` | フェーズ、実行順序、検証方法を記した `plan.md` を作成 |
| タスク | `/codexspec:plan-to-tasks <feature-dir>` | 追跡・検証可能な `tasks.md` を作成し、成果物間の分析を実行 |
| 実装 | `/codexspec:implement-tasks <feature-dir>` | タスクを実行し、結果を検証して、独立した検証を経たレビュー指摘を修正 |

`<feature-dir>` は、要件の検討時に返された機能ディレクトリに置き換えてください。
その worktree で作業を続けるか、明示的なパスを渡すことで、コマンドやセッションが変わっても同じ機能として扱われます。

### specify、clarify、analyze

- **specify** は要件の検討を開始、または再開します。要件サマリーが正式な判断基準になるのは、明示的な確認を得た場合だけです。
- **clarify** は既存の要件や仕様の曖昧さを解消します。1 回の実行で 4 つのカテゴリにわたり、最大 5 つの質問をします。
  まず `requirements.md` を更新し、その後 `spec.md` を同期します。
- **analyze** は要件 → 仕様 → 設計 → 計画 → タスクの流れ全体を確認します。
  上位の判断基準から修正内容が一意に決まる場合は、下位成果物を自動で修正します。`requirements.md` は一切編集しません。
  未解決の指摘は報告します。タスクレビューの合格後に自動実行されますが、情報提供を目的としており、実装の合否は判定しません。

```text
/codexspec:clarify <feature-dir>
/codexspec:analyze <feature-dir>
```

### Quick による小さな変更

局所的な修正など、範囲が明確で小さな変更には `quick` を使います。

```text
/codexspec:quick Fix the empty-state message on the task list
```

Quick は簡潔な要件サマリーを確認して保存した後、仕様作成、計画、タスク化、実装を順に進めます。
各生成コマンドによるレビューも行います。広範な変更や、製品・設計上の選択が未解決の場合は、標準ワークフローを使ってください。
Quick は新しい判断が必要になると一時停止します。

### ワークフローの自動化

`workflow.auto_next` のデフォルトは **false** です。
作業中のワークスペースの設定で `true` にすると、最終的な要件確認後に仕様作成へ進みます。
各生成ステージは `PASS` または `PASS_WITH_WARNINGS` で次へ進み、`NEEDS_REVISION` または `BLOCKED` で停止します。
`implement-tasks` が最終ステージです。

成果物の自動修正は、検証済みの欠陥のうち、上位の根拠から修正内容を導けるものに限られます。
修正とレビューは最大 2 ラウンドまで行います。助言は別に扱います。
実装のレビュー・修正ループには、後述する独自の完了条件があります。

詳しい動作と条件は、[ワークフローガイド](docs/en/user-guide/workflow.md)を参照してください。

## 共有ブループリントと自律開発

開発前に複数の確認済み要件を準備するには `blueprint`、そのキューを開発するには `auto-dev` を使います。

```text
/codexspec:blueprint Add a confirmed requirement for task reminders
/codexspec:auto-dev
```

ブループリントの要件検討では、ユーザーが決めるべき方向性、選択、制約を解決してから要件をキューに入れます。
共有の `.codexspec/blueprint.md` では、`pending`、`in_progress`、`completed` の状態を使います。
保留中の要件は追加、置換、削除、並べ替えができます。進行中と完了済みの項目は、ブループリントの管理操作では読み取り専用です。

Auto-dev はドキュメントに記載された順に開発し、進行中の機能があれば、別の機能を始める前に再開します。
機能が完了するたびにキューを読み直すため、新たに追加された保留中の作業もその実行で処理できます。
確認済み要件の範囲内で SDD の各ステージ、実装、検証、レビュー、修正を行います。
`auto-dev` を呼び出すと、`workflow.auto_next` の値にかかわらず自動化が有効になります。この設定自体は変更しません。

両コマンドは、ブランチ `codexspec/auto-dev` の `worktree-for-codexspec-auto-dev` を共有します。
共通の所有権管理と書き込み保護のもとで同時に操作できますが、要件の開発はそのワークスペースで順次行います。
確認済み要件から決められない製品上の判断が必要になると、通常の自律実行中には質問せず、根拠を示して停止します。

現在の共有ブループリントを変更せずに確認するには、次を実行します。

```bash
codexspec show-blueprint
```

## worktree での開発

Git worktree は、同じリポジトリの別の作業ディレクトリで、それぞれにブランチをチェックアウトできます。
CodexSpec はデフォルトで通常の機能ごとに 1 つ作成します。作成は最初の要件を書き込む前に行い、
その機能のドキュメント、実装、テスト、修正を同じ場所にまとめます。

```text
projects/
├── my-project/
└── my-project-codexspec-worktrees/
    ├── <feature-id>-task-reminders/
    ├── <feature-id>-search/
    ├── worktree-for-codexspec-maintenance/
    └── worktree-for-codexspec-auto-dev/
```

機能の作業を再開するときは、同じワークスペースを再利用します。
独立した設定、プロジェクト憲法、プロファイルの変更には保守用 worktree を使い、開発中の機能における変更はそのワークスペース内で行います。
設定は**チェックアウトごと**に適用されます。作業先となる worktree で変更した設定は、まずその場所で有効になり、
Git での統合を通じて他のチェックアウトに反映されます。CLI コマンドとチェックは、返されたワークスペースで実行してください。

新機能の開発開始時には、コミット済みのローカル main ブランチの履歴と、fetch したリモート main ブランチの履歴を Git の祖先関係で比較し、基準を決めます。
履歴が分岐している場合は、新しい worktree 内でマージして検証する必要があります。
fetch に失敗した場合は警告を出し、ローカルにある参照での続行を認めます。
worktree の作成に失敗しても、main チェックアウトへの書き込みには切り替えません。

`workflow.worktrees` のデフォルトは **true** です。通常の機能と保守作業の分離を無効にするのは、YAML のリテラル `false` だけです。
この設定にかかわらず、blueprint/auto-dev は固定の共有 worktree を使います。
初期化とインストールの更新は、明示的に選択したチェックアウトで行います。
完了した worktree は保持され、完了時に自動でマージや削除は行われません。

[worktree での開発](docs/en/user-guide/workflow.md#worktree-development)と[設定](docs/en/reference/configuration.md#workflowworktrees)を参照してください。

## 既存コードでの作業

既存コードに対しては、目的に応じて 2 つのコマンドを使い分けます。

| コマンド | 用途 | 出力と操作範囲 |
|---------|-----------|-----------------|
| `onboard [path]` | 既存のコードベースから再利用可能なプロジェクト知識を初期登録 | 慣行の候補と、根拠に基づいて範囲を絞った制約をプロファイルに記録。コードは読み取り専用 |
| `reverse-spec [path]` | 既存アーキテクチャの理解、または確認済みの意図とコードの比較 | 成果物の草案または差異レポート。コードは読み取り専用 |

```text
/codexspec:onboard src/
/codexspec:reverse-spec
/codexspec:reverse-spec src/auth
```

Onboard は観察できるコードから慣行を推論し、明示的な禁止事項がある場合にだけ制約を提案します。
慣行の候補はローカルで直ちに有効になります。制約の候補は、セッション内で保存・編集・破棄を決める必要があります。
既存の知識は保持します。初回のコードスキャンをもとに、過去の判断理由や、実際に経験したかどうか分からない落とし穴を作り出すことはありません。

Reverse-spec には 3 つのモードがあります。

- **概要**：パス未指定、またはリポジトリルートを指定した場合。調査するモジュールを選ぶために、アーキテクチャの要点を記した `design.md` と `slices.md` を作成します。
- **生成**：確認済みの基準がないモジュールパスを指定した場合。`spec.md`、`design.md`、未確定・推論段階の要件を草案として作成します。
- **照合**：確認済みの基準があるモジュールを指定した場合。`reconcile.md` を作成し、
  確認済みの仕様・設計に照らして、文書化されていない動作、未実装の仕様、意味の不一致を報告します。意図については要件を判断基準にします。

推論から作成された草案は、人による確認を経て初めて基準として使えます。
照合では、コードの修正、ドキュメントの更新、意図の判断のいずれを進めるべきかを提案しますが、自動では適用しません。

## レビューとデバッグ

4 つの成果物レビュアー `review-spec`、`review-design`、`review-plan`、`review-tasks` は、忠実度、網羅性、実現可能性、内部品質を確認します。
生成後に自動実行され、手動でも呼び出せます。レポートでは、検証済みの欠陥と、合否に影響しないリスクの助言や設計上の改善案を分けて報告し、適合度スコアも示します。

`review-code` は、選択した変更を対象とする独立した欠陥ゲートと、コード全体の明示的な品質評価を提供します。

```text
/codexspec:review-code --feature <feature-dir>
/codexspec:review-code --uncommitted
/codexspec:review-code --audit src/
```

デフォルトでは機能ブランチの差分全体をレビューします。コミット済み、ステージ済み、未ステージ、Git の無視対象でない未追跡の変更がすべて含まれます。
コミット済み、未コミット、単一コミットのいずれかを明示的に選ぶこともできます。
`--feature` は要件の文脈を追加しますが、Git の対象範囲は狭めません。
`--audit` は指定されたパスを評価し、完了判定ではなく、助言としての評価表を作成します。

レビューでは `.codexspec/review-code/` から共通基準を読み込み、関連する動作の観点や、言語・フレームワークごとのチェックを選びます。
指摘には、具体的な根拠、実際に発生し得る条件、選択した変更に起因すること、影響の説明が必要です。
レビュアーはファイルを編集せず、欠陥と根拠のある保守提案を報告します。修正を行う呼び出し元は、それらを独立して検証します。

実装では、コードのタスクはテストを先に書いて進め、ドキュメントや設定は直接変更して適切なチェックを行います。
修正後の差分レビューでは、影響を受けていない範囲の確認結果を再利用できます。
最終的な受け入れには、新たに行う機能全体のレビューで `PASS` を得ること、対象範囲の確認と検証が完了すること、
認定された P0–P3 の欠陥が 1 件も残っていないことが必要です。根拠のある保守提案は別に報告します。

`workflow.auto_maintenance` のデフォルトは **true** です。
修正を行う呼び出し元が、検証済みで互換性を保つ保守改善も適用するかを、この設定で制御します。
無効にしても提案は報告され、欠陥の修正や必須チェックは免除されません。
ステージの自動進行とは独立した設定で、`implement-tasks` の引数ではありません。

根本原因を先に調べるデバッグには、次のコマンドを使います。

```text
/codexspec:debug Investigate intermittent failures when saving a task
```

Debug は、調査 → パターン分析 → 単一仮説の検証 → 失敗するテストを先に書いて修正、の順に進みます。
実装中の修正が行き詰まった場合、単純ではない動作上の欠陥について原因を追う必要がある場合、
同じ種類の根本原因がレビューの複数ラウンドで再発した場合に、この手順へ移ります。
修正が 3 回失敗したら、アーキテクチャを再検討します。

要件の明確さ、完全性、一貫性を評価するには、`checklist` を使います。

```text
/codexspec:checklist Check the authentication requirements for completeness
```

レビュー対象の選び方、引数、詳しい手順は、[コマンドリファレンス](docs/en/user-guide/commands.md)を参照してください。

## プロジェクト知識

プロジェクトプロファイルには、再利用できる知識を `.codexspec/profile/` に保存します。

| カテゴリ | 内容 |
|----------|----------|
| `constraints/` | 明示的な禁止事項と厳守すべき境界。最初に読む |
| `conventions/` | パターン、命名、機能をまたぐ指針 |
| `pitfalls/` | 実際に経験した落とし穴、その原因、回避策、教訓 |
| `decisions/` | 再利用可能なアーキテクチャ上の判断や、機能をまたぐ判断 |
| `strategies/` | 作業方法を変えるべき兆候 |
| `runbooks/` | 順序に沿った作業手順と、失敗時の復旧方法 |

`distill` は作業から再利用可能な知識を抽出します。機能固有の意図は、その機能の要件・設計・計画に残します。
初期化時に CLAUDE.md または AGENTS.md、あるいは両方へガイダンスを追加し、本格的な作業の前にすべての制約と関連知識を読むよう指示します。
後から追加した知識も、再初期化せずに有効になります。候補の記録は慎重に扱い、承認済みの記録には、結果の検証と人による承認が必要です。

```text
/codexspec:distill Capture the reusable lessons from this work
/codexspec:distill review
/codexspec:evolve
```

手動の `distill review`、または新たに抽出する内容がない状態で直接呼び出した `distill` は、ローカルで動作するオフラインのブラウザーワークスペースを開きます。
記録を修正、承認、破棄、保留、統合し、最終的な Markdown をプレビューしてから **すべて適用**を選択できます。
適用するまでは、判断が復旧可能な草案として保存されます。競合チェックにより、一部だけの適用や、通知なしの上書きを防ぎます。
ブラウザーを使えない環境では、明示的にテキスト方式へ切り替えることもできます。

`workflow.auto_distill` のデフォルトは **true** で、3 つの完了時フックを制御します。
`implement-tasks` の成功時、`commit-staged` でコミットを実行したとき、`pr` の生成時です。
コミットのプレビューでは知識を抽出しません。

インストールされたプロジェクトガイダンスは、通常の会話、SDD 外の修正、長時間の `implement-tasks` 実行中にも、
再利用できる知識が得られた時点で記録するようエージェントに求めます。
この指示は完了時の設定とは独立して適用されます。タスク終了時の抽出は、取りこぼしを防ぐ最後の機会です。

同じセッションで繰り返し呼び出された場合は、新しい内容だけを処理します。
セッションが変わった場合は、`distill` がプロファイルを読み、すでに記録されている知識を省きます。
再利用できる内容が残っていなければ、書き込まずに終了します。
自動抽出では、手動レビューを開いたり、人の応答を待ったり、呼び出し元のワークフローを止めたりすることはありません。

`evolve` は、承認済み知識のうちプロジェクト外でも役立つものだけを選び、コマンド・スキルの草案を作成します。
push や、人によるレビューを受けるための貢献 PR の作成前に、明示的な承認を得ます。

詳しい手順は、[プロジェクト知識](docs/en/user-guide/commands.md#codexspecdistill)を参照してください。

### 過去の判断の再利用

要件、設計、実装、デバッグ、レビューについて本格的に判断する前には、`.codexspec/specs/` の関連履歴も参照します。
これは通常の会話と SDD ワークフローの両方に適用されます。
エージェントはユーザーに質問する前に、変更されていない判断、後から追加された内容、明示的に置き換えられた内容をたどります。

古い要件も、変更されていなければ引き続き適用されます。ユーザーの最新の明示的な判断が常に優先され、未確定の提案を確認済みの意図として扱うことはありません。
調べる履歴はタスクに関連する範囲に絞り、十分な背景情報がそろっていれば再利用します。
このガイダンスを受け取るには、既存プロジェクトのインストールを更新してください。

## Git ワークフロー

```text
/codexspec:commit-staged -p
/codexspec:pr --spec <feature-dir>/spec.md
/codexspec:release-notes --from <ref> --to HEAD
/codexspec:tasks-to-issues <feature-dir>
```

- **commit-staged** はステージング領域の内容そのものを分析し、Conventional Commits のメッセージを生成します。
  `-p` では、コミットせずにプレビューできます。ファイルの選択とステージングは、呼び出し元のワークフローが行います。
  許可を得て実行する場合は、保護された実行環境で、コミットする内容が分析対象と一致することを再確認します。
  エージェントのコミットガイダンスは通常の会話、SDD、blueprint、auto-dev にも適用されます。
  コマンドが利用可能であるだけでは、その呼び出しにも、コミットの許可にもなりません。
- **pr** は差分をもとに、構造化された GitHub PR または GitLab MR の説明を生成します。
  `--spec` を指定すると、`spec.md` のファイルパス、またはそのファイルを指す機能ディレクトリ名やプレフィックスから、機能の文脈を追加できます。
  デフォルトでは、ホスティングプラットフォームで使うためのテキストを出力します。
- **release-notes** は Git 履歴から、Keep a Changelog のエントリとリリース本文を作成します。
  デフォルトのセクションは `[Unreleased]` で、`--version` を指定すると、そのラベルを使います。
  ステージング、コミット、バージョン更新、タグ付け、公開、リリース作成は行いません。
- **tasks-to-issues** は既存のタスクから、依存関係と受け入れ基準を含む GitHub Issue を作成します。
  認証済みの GitHub CLI が必要です。Issue のリポジトリが、設定済みのリモートと一致することも検証します。

コミットのプレビューと、許可を得て現在のチェックアウトで行うコミットには、Python 3.11+ と Git が必要です。
実行環境は CLI で初期化したプロジェクトにインストールされ、Claude プラグインにも同梱されます。
エージェントが作成する、内容の変更を伴うマージでも、ステージ済み内容の分析を行います。
履歴だけをつなぐマージでは、ツリーと親を検証しながら Git のデフォルトメッセージを維持します。
fast-forward はコミットを作成しません。

## 利用可能なコマンド

CLI には 6 つの公開コマンドがあります。エージェント連携では 28 コマンドを配布します。
Claude では `/codexspec:<name>`、Codex では `$codexspec:<name>` で呼び出します。
以下の表は、読みやすさのため Claude の表記で統一しています。

### CLI コマンド

| コマンド | 目的 |
|---------|---------|
| `codexspec init` | Claude、Codex、または両方に合わせてプロジェクトを初期化・更新 |
| `codexspec check` | インストール済みのツールと依存関係を確認 |
| `codexspec version` | バージョンとシステム情報を表示 |
| `codexspec config` | プロジェクト設定を表示・変更 |
| `codexspec list-commands` | 利用可能なエージェントコマンドをカテゴリ別に表示 |
| `codexspec show-blueprint` | 共有 worktree のブループリントを変更せずに出力 |

### 基本ワークフローコマンド

| コマンド | 目的 |
|---------|---------|
| `/codexspec:constitution` | プロジェクト原則を作成・更新し、成果物間の整合性を検証 |
| `/codexspec:specify` | 機能要件を話し合い、確認して保存 |
| `/codexspec:blueprint` | ブループリントの確認済み・保留中の要件を準備・管理 |
| `/codexspec:generate-spec` | 確認済み要件から追跡可能な仕様書を作成し、自動レビュー |
| `/codexspec:spec-to-design` | アーキテクチャ、コンポーネント、インターフェース、判断を定義し、自動レビュー |
| `/codexspec:design-to-plan` | 実装のフェーズ、順序、検証を計画し、自動レビュー |
| `/codexspec:plan-to-tasks` | 上位成果物の内容を網羅する検証可能なタスクを作成し、自動レビューと分析 |
| `/codexspec:implement-tasks` | タスクを実行し、結果を検証してレビュー・修正 |
| `/codexspec:auto-dev` | 確認済みブループリント要件をドキュメントの順に自律開発 |

### 成果物レビューコマンド

| コマンド | 目的 |
|---------|---------|
| `/codexspec:review-spec` | 仕様書の忠実度と内部品質を確認 |
| `/codexspec:review-design` | 設計の忠実度、実現可能性、計画に進める状態かを確認 |
| `/codexspec:review-plan` | 計画の忠実度、実現可能性、実装に進める状態かを確認 |
| `/codexspec:review-tasks` | タスクの忠実度、依存関係、実行可能性、検証を確認 |

### 要件、既存コード、デバッグ

| コマンド | 目的 |
|---------|---------|
| `/codexspec:clarify` | 要件の曖昧さを解消し、仕様書より先に要件を更新 |
| `/codexspec:analyze` | 一連の成果物の追跡可能性を確認し、下位成果物を上位の判断基準に合わせて修正 |
| `/codexspec:checklist` | 要件品質のチェックリストを生成 |
| `/codexspec:tasks-to-issues` | 既存のタスクを、実行に移せる GitHub Issue に変換 |
| `/codexspec:debug` | 修正前に根本原因を調査 |
| `/codexspec:reverse-spec` | 既存アーキテクチャの調査、モジュール成果物の草案作成、または基準との差異の報告 |

### プロジェクト知識コマンド

| コマンド | 目的 |
|---------|---------|
| `/codexspec:distill` | 再利用可能な知識を記録、またはローカルワークスペースで候補をレビュー |
| `/codexspec:evolve` | 承認済み知識をもとに、上流への貢献に向けた草案を作成 |
| `/codexspec:onboard` | 既存コードから慣行の候補と、根拠のある制約を初期登録 |

### Git とコードレビューのコマンド

| コマンド | 目的 |
|---------|---------|
| `/codexspec:commit-staged` | ステージ済み変更からメッセージを生成し、プレビューまたは許可を得たコミットを実行 |
| `/codexspec:pr` | 構造化された PR/MR の説明を生成 |
| `/codexspec:release-notes` | 変更履歴のエントリを更新し、Git 履歴からリリース本文を生成 |
| `/codexspec:review-code` | 選択した変更を欠陥ゲートとしてレビュー。パスの品質評価には `--audit` を使用 |

### ユーティリティコマンド

| コマンド | 目的 |
|---------|---------|
| `/codexspec:config` | 対話形式でプロジェクト設定を作成・表示・変更・リセット |
| `/codexspec:quick` | 小さな変更に対し、簡潔な要件優先 SDD ワークフローを実行 |

## 設定と国際化

設定は `.codexspec/config.yml` に保存します。テンプレートは英語のままですが、
エージェントは設定された言語で対話文と成果物を作成します。
標準の言語コードは 13 個です：`en`、`zh-CN`、`zh-TW`、`ja`、`ko`、`es`、`fr`、`de`、`pt`、`ru`、`it`、`ar`、`hi`。
ポルトガル語の CLI コードは `pt` で、ローカライズされたドキュメントと翻訳カタログでは `pt-BR` を使います。

### 言語の個別設定

| 区分 | 設定キー | 初期化時 | 後から設定 | 対象 |
|-----------|------------|-------------------|-----------|----------|
| 出力・基本言語 | `language.output` | `--lang` | `config --set-lang` | 他の言語設定で指定がない場合の基本言語 |
| 対話 | `language.interaction` | `--interaction-lang` | `config --set-interaction-lang` | 会話と CLI 出力 |
| ドキュメント | `language.document` | `--document-lang` | `config --set-document-lang` | 要件、仕様書、設計、計画、タスク |
| コミット | `language.commit` | `--commit-lang` | `config --set-commit-lang` | コミットメッセージと Git ワークフローで生成する文章 |

各言語設定は、それぞれ独立して `language.output`、次に `en` の順でフォールバックします。
`language.templates` は `en` のままです。

```bash
codexspec init my-project --ai both \
  --interaction-lang zh-CN --document-lang en --commit-lang en

codexspec config
codexspec config --set-document-lang en
codexspec config --list-langs
```

初回の TTY 初期化では、`--lang` または 3 つすべての個別言語オプションを指定していなければ、基本言語の選択を求めます。
`--force` は他の初期化時の確認を自動で承認しますが、この言語選択は省略しません。
非 TTY での初期化では、デフォルトで英語を使います。再初期化時も、明示的に設定していない言語キーは保持されます。

### ワークフローとレビューの設定

| 設定 | デフォルト | 動作 | CLI 操作 |
|---------|---------|--------|-------------|
| `workflow.auto_next` | `false` | 合格した通常の SDD ステージから次へ進む | `config --auto-next on\|off` |
| `workflow.auto_distill` | `true` | 完了処理の成功後、人との対話なしに知識を抽出 | `config --auto-distill on\|off` |
| `workflow.auto_maintenance` | `true` | 自動修正時に、検証済みの保守改善を段階的に適用 | `config --auto-maintenance on\|off` |
| `workflow.worktrees` | `true` | 通常の機能と独立した保守作業を別の worktree に分離 | `config --worktrees on\|off` |
| `review.decided_by` | `reviewer` | プロジェクトの運用範囲外で発生する指摘について、判断する人を指定 | `config --decided-by reviewer\|ask` |

真偽値を取る CLI スイッチは、大文字・小文字を区別せず、`on/true/1/yes` と `off/false/0/no` を受け付けます。前後の空白も許容されます。
値を指定せずに使うと、書き込み先チェックアウトの現在値を切り替えます。YAML には真偽値として保存します。

`review.decided_by: reviewer` では、レビュアーが欠陥として認定するかを判断します。
`ask` では、運用範囲外の発生条件を、ユーザーの判断待ちのシナリオとして扱います。
ユーザーは修正するか、そのシナリオを除外するかを一度決め、確認済みの判断は後続のラウンドでも使えるよう保存されます。
判断待ちの項目がある間は完了できません。1 回の `review-code` 実行に限り、`--decided-by` で設定済みのモードを上書きできます。

設定の書き込みも worktree の作業先選択に従います。
main チェックアウトから独立した変更を行う場合は、保守用 worktree に書き込み、main で有効な設定は直ちには変わりません。
機能 worktree 内での変更は、その場所で有効になります。

<details>
<summary>CLI 初期化オプション</summary>

| オプション | 意味 |
|--------|---------|
| `PROJECT_NAME` | 新しいディレクトリの名前。現在のディレクトリには `.` を使用 |
| `--here`, `-h` | 現在のディレクトリを初期化 |
| `--ai`, `-a` | `claude`、`codex`、`both` から選択。デフォルトは `claude` |
| `--lang`, `-l` | 基本となる出力言語を設定 |
| `--interaction-lang` | 対話言語を設定 |
| `--document-lang` | ドキュメント言語を設定 |
| `--commit-lang` | コミットメッセージの言語を設定 |
| `--force`, `-f` | インストール済み成果物を再生成し、移行・更新・準拠に関する確認を自動承認。プロジェクトで作成したコンテキストと、指定に関係のない設定は保持 |
| `--no-git` | Git リポジトリの初期化を省略 |
| `--debug`, `-d` | 詳細なデバッグ情報を表示 |

</details>

<details>
<summary>CLI 設定オプション</summary>

| オプション | 意味 |
|--------|---------|
| `--set-lang`, `-l` | 基本となる出力言語を設定 |
| `--set-interaction-lang` | 対話言語を設定 |
| `--set-document-lang` | ドキュメント言語を設定 |
| `--set-commit-lang`, `-c` | コミットメッセージの言語を設定 |
| `--list-langs` | サポートする言語コードを一覧表示 |
| `--auto-next` | ステージの自動進行を切り替え・設定 |
| `--auto-distill` | 知識の自動抽出を切り替え・設定 |
| `--auto-maintenance` | 段階的な保守改善の自動適用を切り替え・設定 |
| `--worktrees` | チェックアウトごとの worktree 分離を切り替え・設定 |
| `--decided-by` | レビューの判断モードを `reviewer` または `ask` に設定 |

</details>

<details>
<summary>設定例</summary>

```yaml
version: "1.0"

language:
  output: "en"
  interaction: "zh-CN"
  document: "en"
  commit: "en"
  templates: "en"

project:
  ai: "both"

workflow:
  auto_next: false
  auto_distill: true
  auto_maintenance: true
  worktrees: true

review:
  decided_by: reviewer
```

</details>

言語と設定の詳しい動作は、[設定](docs/en/reference/configuration.md)と[国際化](docs/en/user-guide/i18n.md)を参照してください。

## プロジェクト構成

初期化では、共通リソースと、選択したアシスタントとの連携に必要なファイルをインストールします。

```text
my-project/
├── .codexspec/
│   ├── config.yml
│   ├── memory/
│   │   └── constitution.md
│   ├── profile/
│   │   ├── constraints/
│   │   ├── conventions/
│   │   ├── pitfalls/
│   │   ├── decisions/
│   │   ├── strategies/
│   │   └── runbooks/
│   ├── review-code/              # Shared review standards
│   ├── specs/
│   │   └── <feature-id>-<name>/   # Added by feature workflows
│   │       ├── requirements.md
│   │       ├── spec.md
│   │       ├── design.md
│   │       ├── plan.md
│   │       ├── tasks.md
│   │       ├── review-*.md
│   │       └── checklists/       # When requested
│   ├── templates/docs/
│   └── scripts/                 # Platform helpers and commit runtime
├── .claude/commands/codexspec/   # --ai claude or both
├── .agents/skills/              # --ai codex or both
├── CLAUDE.md                    # Claude project context
└── AGENTS.md                    # Codex project context
```

共有ブループリントは専用の auto-dev worktree に置きます。通常のチェックアウトごとに編集可能な別コピーを用意することはありません。
手動の知識レビューで使う草案は Git の管理対象から除外されます。

## 拡張機能の作成資料

リポジトリには、拡張機能のマニフェストテンプレート、コマンド例、[拡張機能開発ガイド](extensions/EXTENSION-DEVELOPMENT-GUIDE.md)が含まれます。
これらは拡張機能を作成するための資料です。現在の CLI に拡張機能のインストール・一覧・削除コマンドはなく、
`extension.yml` のコマンドやフックを自動で読み込むこともありません。
共通レビューリソースには、`.codexspec/review-code/` 配下にプロジェクト独自の内容を追加できます。
初期化時には、置換を求めない限り、既存リソースへの編集内容や追加ファイルを保持します。

## 開発

```bash
git clone https://github.com/Zts0hg/codexspec.git
cd codexspec

# Development tools are an optional dependency extra
uv sync --extra dev
# For documentation builds too: uv sync --extra dev --extra docs

uv run codexspec --help
uv run pytest
uv run ruff check src/
uv build
```

テンプレート、パッケージング、初期化を変更する前に、[CLAUDE.md](CLAUDE.md)、[AGENTS.md](AGENTS.md)、
[リポジトリ構成](docs/internal/repository-layout.md)を読んでください。
配布コマンドとスキルのコピーは、自動生成されたインストール成果物です。正規のソースを編集し、再生成してください。

## 貢献

ローカル環境の準備や貢献の進め方は、[貢献ガイド](docs/en/development/contributing.md)を参照してください。
貢献にあたっては、確認済み要件、出典への追跡可能性、ユーザー向けと保守者向けを分けるパッケージ境界を維持してください。

## ライセンス

MIT — [LICENSE](LICENSE) を参照してください。

## 謝辞

[GitHub spec-kit](https://github.com/github/spec-kit) から着想を得ています。
Claude Code と OpenAI Codex と連携します。
