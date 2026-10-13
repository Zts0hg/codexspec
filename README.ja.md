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
  <strong>Claude Code と OpenAI Codex のための要件優先 SDD ツールキット</strong>
</p>

CodexSpec は、確認済みの要件を、追跡可能な仕様書、設計、計画、タスク、実装へとつなげます。
**何を**作るか、**なぜ**作るかを決めるのはあなたです。エージェントはその確認済み要件の範囲内で、
レビューの確認点と永続的なプロジェクト知識を使い、**どのように**実現するかを具体化します。

Claude Code のスラッシュコマンド、Codex のスキル、または両方で利用できます。通常の機能開発では、
デフォルトで独立した Git worktree を使用します。任意の共有ブループリントを使えば、
確認済み要件のキューをエージェントが自律的に開発できます。

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

| ニーズ | CodexSpec が提供するもの |
|------|-------------------------|
| 明確な製品意図 | 仕様書の作成前に明示的な確認を行い、`requirements.md` に永続的に記録 |
| 追跡可能な開発 | 要件 → 仕様 → 設計 → 計画 → タスクを通じた出典へのリンク |
| レビューできる判断 | 4 つの成果物レビューコマンド、成果物間の分析、独立したコード欠陥ゲート |
| セッションとチームでの継続性 | 機能の記録、プロジェクト原則、再利用可能な知識、関連する過去の判断 |
| 複数機能の並行開発 | 通常の機能ごとに 1 つの Git worktree を作成し、同じワークスペースを安定して再利用 |
| より多くの自動化 | 任意のステージ自動進行と、確認済みブループリント要件の自律開発 |
| チームの言語設定 | 対話、ドキュメント、コミットの言語を個別に設定 |

### 要件優先 SDD とは

要件優先の仕様駆動開発では、**確認済み要件を、その機能について最優先の判断基準**とします。
エージェントは実装成果物を導出する前に、目標、制約、判断、除外事項、未解決の質問、確認の証拠を記録します。

```text
Idea → Confirmed Requirements → Spec → Design → Plan → Tasks → Code
```

製品意図の確立と変更は、人との協働で行います。自動レビューは、導出された成果物がその意図に沿うかを確認します。
自動化を有効にすると、合格したステージから次へ進みますが、エージェントが確認済み要件を黙って置き換えることはありません。

## 30 秒クイックスタート

CodexSpec をインストールし、利用するアシスタント向けに初期化します。

```bash
uv tool install codexspec

# Create a new project for Claude Code
codexspec init my-project --ai claude

# Or initialize an existing project for Codex
cd your-existing-project
codexspec init . --ai codex

# Use --ai both when you want both integrations
```

初期化したプロジェクトで、インストール済みのアシスタントを起動します。同じワークフローを、次の 2 つの呼び出し形式で使用できます。

| アシスタント | 要件の検討を開始 |
|-----------|------------------------------|
| Claude Code (`claude`) | `/codexspec:specify I want to build a todo application` |
| Codex (`codex`) | `$codexspec:specify I want to build a todo application` |

必要に応じて `constitution` でプロジェクト原則を調整します。最終的な要件サマリーを確認し、
返された機能ディレクトリとワークスペースで作業を続けます。以降のコマンドは[基本ワークフロー](#基本ワークフロー)を参照してください。

Codex デスクトップアプリを使っていますか。[Codex にプロジェクトのインストールと初期化を依頼できます](#codex-デスクトップアプリでインストール)。

## インストール

### Codex デスクトップアプリでインストール

デスクトップアプリから、Codex に CodexSpec のインストールとプロジェクトのセットアップを直接依頼できます。

1. Codex デスクトップアプリにローカルプロジェクトを追加し、作業するフォルダーを選択します。
2. そのプロジェクトでチャットを開始し、次のプロンプトを貼り付けます。
3. アプリが依存関係のダウンロードやインストールの許可を求めた場合は、要求された操作を承認して続行します。

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

中国語の応答とドキュメントが必要な場合は、`--lang en` を `--lang zh-CN` に置き換え、結果を中国語で説明するよう Codex に依頼してください。

Codex は、下記の手動セットアップと同じ CLI とプロジェクトスキルをインストールします。
`$codexspec:specify I want to build a todo application` のようなプロンプトで利用を開始できます。
ローカルスキルの検出と更新の動作は、[OpenAI のスキルガイド](https://learn.chatgpt.com/docs/build-skills)を参照してください。

### 前提条件

- Python 3.11+
- [uv](https://docs.astral.sh/uv/)（推奨）、または pip
- 使用するアシスタント：Claude Code または Codex
- worktree での開発と Git ワークフローに必要な Git

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
アシスタントのデフォルトは `claude` です。Codex または両方を使う場合は、値を明示的に選択してください。

<details>
<summary>その他のインストール方法</summary>

#### 一度だけ実行する初期化

```bash
uvx codexspec init my-project --ai claude
uvx codexspec init . --ai codex
```

一度だけの初期化で、プロジェクトコマンドと独立したコミット実行環境がインストールされます。
worktree の作業先選択、blueprint/auto-dev、手動のプロファイルレビューでは引き続き CodexSpec CLI を呼び出すため、
これらのワークフローで利用できるようにしてください。

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

PowerShell を使用します。

```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
# Restart PowerShell, then:
uv tool install codexspec
codexspec version
```

PATH とインストールの問題への対処は、[Windows トラブルシューティングガイド](docs/en/WINDOWS-TROUBLESHOOTING.md)を参照してください。

</details>

### アップグレードとプロジェクトの更新

CLI の更新と、プロジェクトにインストールされたコマンドの更新は別の手順です。

```bash
uv tool install codexspec --upgrade
# Or: pip install --upgrade codexspec

# In the project you want to refresh; select its desired integration(s)
codexspec init . --force --ai both
```

片方の連携だけを使う場合は、`--ai claude` または `--ai codex` を指定してください。
`--force` は配布コマンドとスクリプトを再生成し、レビューリソースを更新します。
また、移行、コマンド更新、プロジェクト憲法への準拠に関する確認を自動承認します。
既存の要件とプロジェクト原則は維持され、既存のコンテキストファイルの本文を残したまま管理対象のガイダンスが更新されます。
明示的に設定していない設定キーも維持されます。

計画作成コマンドは `design-to-plan` です。インストールの更新時に旧 `spec-to-plan` エントリは廃止され、エイリアスは残りません。

### プラグインマーケットプレイスからのインストール

Claude Code では、マーケットプレイスからプラグインをインストールします。

```text
/plugin marketplace add Zts0hg/codexspec
/plugin install codexspec@codexspec-market
/codexspec:config
```

プラグインはコマンドと、ステージ済みコミットの分析および過去の要件の参照に関するセッション開始時のガイダンスを提供します。
再開したセッションにも適用されます。プラグインのインストールではプロジェクトは初期化されません。
`/codexspec:config` で言語、ワークフロー、レビュー設定を作成・変更してください。
完全なプロジェクト構成が必要な場合は CLI で初期化します。

直接のコミットプレビューと、許可されたその場でのコミットは、Python 3.11+ と Git があれば、
常設の CodexSpec CLI なしでも同梱の実行環境を利用できます。worktree の作業先選択、blueprint/auto-dev、
手動のプロファイルレビューには引き続き CLI が必要です。プラグインの起動フックには PATH 上の Git と、
コマンドフックの `args`（exec 形式）をサポートする Claude Code バージョンが必要です。
ガイダンスはエージェント向けであり、手動の Git コマンドを横取りするものではありません。

詳細なセットアップは、[インストール](docs/en/getting-started/installation.md)を参照してください。

## 基本ワークフロー

標準的な機能開発ワークフローでは、出典と結び付いた流れを維持します。

```text
/specify          → requirements.md
/generate-spec    → spec.md       → review-spec
/spec-to-design   → design.md     → review-design
/design-to-plan   → plan.md       → review-plan
/plan-to-tasks    → tasks.md      → review-tasks → analyze
/implement-tasks  → implementation and complete-feature code review
```

以下の例では Claude の `/codexspec:` プレフィックスを使っています。
Codex では、同じコマンド名と引数に `$codexspec:` を付けてください。

| ステップ | コマンド | 目的と出力 |
|------|---------|--------------------|
| プロジェクト原則 | `/codexspec:constitution` | `constitution.md` を作成・更新し、影響を受ける成果物を検証 |
| 要件 | `/codexspec:specify <idea>` | 意図を検討し、最終サマリーを確認して `requirements.md` に永続化 |
| 仕様書 | `/codexspec:generate-spec <feature-dir>` | 確認済み要件を、出典参照を持つ `spec.md` にまとめる |
| システム設計 | `/codexspec:spec-to-design <feature-dir>` | コンポーネント、インターフェース、主要な設計判断を含む `design.md` を作成 |
| 実装計画 | `/codexspec:design-to-plan <feature-dir>` | フェーズ、順序、検証を含む `plan.md` を作成 |
| タスク | `/codexspec:plan-to-tasks <feature-dir>` | 追跡・検証可能な `tasks.md` を作成し、成果物間の分析を実行 |
| 実装 | `/codexspec:implement-tasks <feature-dir>` | タスクを実行し、結果を検証して、独立した検証を経たレビュー指摘を修正 |

`<feature-dir>` は要件の検討時に返された機能ディレクトリに置き換えてください。
その worktree で続行するか、明示的なパスを渡すことで、コマンドやセッションをまたいでも同じ機能の識別情報が維持されます。

### specify、clarify、analyze

- **specify** は要件の検討を開始または再開します。要件サマリーが拘束力を持つのは、明示的に確認された場合だけです。
- **clarify** は既存の要件・仕様の曖昧さを解消します。1 回の実行で 4 カテゴリにわたり最大 5 つの質問を行います。
  最初に `requirements.md` を更新し、次に `spec.md` を同期します。
- **analyze** は要件 → 仕様 → 設計 → 計画 → タスクの全体を確認します。
  上位成果物の判断基準から修正内容が一意に決まる場合、下位成果物に確定的な修正を自動適用しますが、
  `requirements.md` は一切編集しません。未解決の指摘は報告されます。
  タスクレビューの合格後に自動実行され、情報提供を目的とし、実装の合否ゲートにはなりません。

```text
/codexspec:clarify <feature-dir>
/codexspec:analyze <feature-dir>
```

### Quick による小さな変更

局所的な修正など、範囲が明確な小さな変更には `quick` を使います。

```text
/codexspec:quick Fix the empty-state message on the task list
```

Quick は簡潔な要件サマリーを確認して永続化し、生成コマンドのレビューを伴う仕様作成、計画、タスク化、実装を統括します。
広範な変更や未解決の製品・設計上の選択がある場合は、標準ワークフローを使用してください。
Quick は新しい判断が必要になると一時停止します。

### ワークフローの自動化

`workflow.auto_next` のデフォルトは **false** です。作業中のワークスペースの設定で `true` にすると、
最終的な要件確認後に仕様作成へ進みます。各生成ステージは `PASS` または `PASS_WITH_WARNINGS` の後に進み、
`NEEDS_REVISION` または `BLOCKED` で流れが停止します。`implement-tasks` が最終ステージです。

成果物の自動修正は、上位の証拠から修正内容が導かれる検証済みの欠陥に限定され、修正とレビューは最大 2 ラウンドです。
助言は別扱いのままです。実装のレビュー・修正ループには、後述する独自の完了条件があります。

詳細な契約は、[ワークフローガイド](docs/en/user-guide/workflow.md)を参照してください。

## 共有ブループリントと自律開発

開発前に複数の確認済み要件を準備するには `blueprint`、そのキューを開発するには `auto-dev` を使います。

```text
/codexspec:blueprint Add a confirmed requirement for task reminders
/codexspec:auto-dev
```

ブループリントの要件検討では、要件をキューに入れる前に、ユーザーが決めるべき方向性、選択、制約を解決します。
共有の `.codexspec/blueprint.md` は `pending`、`in_progress`、`completed` の状態を使用します。
保留中の要件は追加、置換、削除、並べ替えが可能です。実行中および完了済みの項目は、ブループリントの保守では読み取り専用です。

Auto-dev はドキュメントの順序に従い、別の機能を開始する前に実行中の機能を再開します。
完了のたびにキューを読み直すため、新たに追加された保留中の作業もその実行に加われます。
確認済み要件の範囲内で SDD ステージ、実装、検証、レビュー、修正を実行します。
`auto-dev` の呼び出しは `workflow.auto_next` とは独立して自動化を有効にし、その設定を変更しません。

両コマンドは `worktree-for-codexspec-auto-dev` を共有し、そのブランチは `codexspec/auto-dev` です。
共有の所有権と書き込み保護の下で同時に操作できますが、要件の開発はそのワークスペースで順番に行われます。
確認済み要件から解決できない製品判断がある場合、通常の自律実行中に質問するのではなく、証拠を示して実行を停止します。

現在の共有ブループリントを変更せずに確認します。

```bash
codexspec show-blueprint
```

## worktree での開発

Git worktree は、同じリポジトリに対する別の作業ディレクトリで、独自のブランチをチェックアウトします。
CodexSpec は通常の機能ごとにデフォルトで 1 つ使用し、最初の要件を書き込む前に作成します。
その機能のドキュメント、実装、テスト、修正をまとめて保持します。

```text
projects/
├── my-project/
└── my-project-codexspec-worktrees/
    ├── <feature-id>-task-reminders/
    ├── <feature-id>-search/
    ├── worktree-for-codexspec-maintenance/
    └── worktree-for-codexspec-auto-dev/
```

機能の作業を続けるときは、そのワークスペースを再利用します。単独の設定、プロジェクト憲法、プロファイルの変更は
保守用 worktree を使用し、作業中の機能で行った変更はその場所に残ります。
設定は**チェックアウトごと**です。作業先として選ばれた worktree で変更した設定は、まずその場所で有効になり、
Git 統合を通じて他のチェックアウトに反映されます。CLI コマンドとチェックは、返されたワークスペースで実行してください。

新機能の基準となる履歴は、コミット済みのローカル main ブランチと fetch したリモート main ブランチの履歴を、
Git の祖先関係で比較して決めます。分岐した履歴は新しい worktree 内でマージされ、検証が必要です。
fetch の失敗時は警告を出し、ローカルで利用できる参照の使用を許可します。
作成に失敗しても、main チェックアウトへの書き込みには切り替えません。

`workflow.worktrees` のデフォルトは **true** です。通常の機能と保守作業の分離を無効にするのは、YAML のリテラル `false` だけです。
Blueprint/auto-dev は、どちらの場合も固定の共有 worktree を使います。初期化とインストールの更新は、明示的に選択したチェックアウトで動作します。
完了した worktree は保持され、完了時に自動でマージや削除は行われません。

[worktree での開発](docs/en/user-guide/workflow.md#worktree-development)と[設定](docs/en/reference/configuration.md#workflowworktrees)を参照してください。

## 既存コードでの作業

目的に応じて 2 つの入口を使い分けます。

| コマンド | 用途 | 出力と境界 |
|---------|-----------|-----------------|
| `onboard [path]` | 既存のコードベースから再利用可能なプロジェクト知識を蓄積 | 候補の慣行と限定された証拠に基づく制約をプロファイルに記録。コードは読み取り専用 |
| `reverse-spec [path]` | 既存のアーキテクチャを理解、またはコードを確認済みの意図と比較 | 成果物の草案または差異レポート。コードは読み取り専用 |

```text
/codexspec:onboard src/
/codexspec:reverse-spec
/codexspec:reverse-spec src/auth
```

Onboard は観測できるコードから慣行を推論し、明示的な禁止事項からのみ制約を提案します。
慣行の候補はローカルで直ちに有効になります。制約の候補には、セッション内で保存・編集・破棄を決める必要があります。
既存の知識を維持し、初回のスキャンから過去の判断理由や経験上の落とし穴を作り出すことはありません。

Reverse-spec には 3 つのモードがあります。

- **概要**：パス未指定またはリポジトリルートの場合、調査するモジュールを選ぶための簡潔なアーキテクチャの `design.md` と `slices.md` を作成します。
- **生成**：確認済みの基準がないモジュールパスの場合、`spec.md`、`design.md`、未確定・推論段階の要件の草案を作成します。
- **照合**：確認済みの基準があるモジュールの場合、`reconcile.md` を作成します。
  確認済みの仕様・設計に対して、文書化されていない動作、未実装の仕様、意味の不一致を報告し、意図の判断基準には要件を用います。

推論による草案は、人による確認を経て初めて基準になります。
照合では、コードを修正する、ドキュメントを更新する、意図を決めるといった推奨方向を報告しますが、自動適用はしません。

## レビューとデバッグ

4 つの成果物レビュアー `review-spec`、`review-design`、`review-plan`、`review-tasks` が、忠実度、網羅性、実現可能性、内部品質を確認します。
生成後に自動実行され、手動でも呼び出せます。レポートは、検証済みの欠陥を、合否を左右しないリスクの助言や設計改善の機会と区別し、適合度スコアも示します。

`review-code` は、変更範囲に対する独立した欠陥ゲートと、明示的なコード全体の品質評価を提供します。

```text
/codexspec:review-code --feature <feature-dir>
/codexspec:review-code --uncommitted
/codexspec:review-code --audit src/
```

デフォルトのレビューは、コミット済み、ステージ済み、未ステージ、未追跡かつ無視対象でない変更を含む、機能ブランチの差分全体を対象にします。
コミット済み、未コミット、単一コミットの証拠を明示的に選択することもできます。
`--feature` は Git の対象範囲を狭めずに要件の文脈を追加します。
`--audit` は指定パスを評価し、完了判定ではなく助言用の評価表を作成します。

レビューは `.codexspec/review-code/` から共通基準を読み込み、関連する動作の観点と言語・フレームワークのチェックを選びます。
指摘には、具体的な証拠、実際に到達可能な発生条件、選択した変更への帰属、影響が必要です。
レビュアーはファイルを編集せずに欠陥と根拠のある保守提案を報告し、修正を行う呼び出し元が独立して検証します。

実装では、コードタスクにはテスト先行を使い、ドキュメント・設定には適切なチェックを伴う直接実装を使います。
修正後の差分レビューでは、影響を受けていない範囲の確認結果を再利用できます。
最終受け入れには、新たに行う機能全体のレビューでの `PASS`、対象範囲の確認と検証の完了、採用された P0–P3 欠陥がゼロであることが必要です。
根拠のある保守提案は別に報告されます。

`workflow.auto_maintenance` のデフォルトは **true** で、修正を行う呼び出し元が、検証済みで互換性のある保守改善も適用するかを制御します。
無効にしても提案は報告され、欠陥や必須チェックが免除されるわけではありません。
ステージの自動進行とは独立しており、`implement-tasks` の引数ではありません。

根本原因の調査を先に行うデバッグには、次を使います。

```text
/codexspec:debug Investigate intermittent failures when saving a task
```

Debug は、調査 → パターン分析 → 単一仮説の検証 → 失敗するテストを先に書いて修正、の順に進みます。
実装時には、修正が行き詰まった場合、単純ではない正しさの欠陥を追跡する必要がある場合、
または同じ根本原因の種類がレビューの複数ラウンドで再発した場合に、この手順へ移ります。
修正が 3 回失敗すると、アーキテクチャを再評価します。

要件の明確さ、完全性、一貫性を評価するには、`checklist` を使います。

```text
/codexspec:checklist Check the authentication requirements for completeness
```

レビューの選択方法、引数、詳細な手順は、[コマンドリファレンス](docs/en/user-guide/commands.md)を参照してください。

## プロジェクト知識

プロジェクトプロファイルは、再利用可能な知識を `.codexspec/profile/` に保存します。

| カテゴリ | 内容 |
|----------|----------|
| `constraints/` | 明示的な禁止事項と厳格な境界。最初に読む |
| `conventions/` | パターン、命名、機能をまたぐガイダンス |
| `pitfalls/` | 経験した落とし穴、原因、回避策、教訓 |
| `decisions/` | 再利用可能なアーキテクチャおよび機能をまたぐ判断 |
| `strategies/` | 作業方法の変更を促す兆候 |
| `runbooks/` | 順序のある手順と失敗時の復旧 |

`distill` は作業から再利用可能な知識を抽出し、機能固有の意図はその機能の要件・設計・計画に残します。
Init は、実質的な作業の前にすべての制約と関連知識を読むよう、CLAUDE.md または AGENTS.md、あるいは両方にガイダンスを設置します。
後から追加した知識も、再初期化せずに有効になります。候補の記録は慎重に用い、承認済みの記録には結果の検証と人による支持が必要です。

```text
/codexspec:distill Capture the reusable lessons from this work
/codexspec:distill review
/codexspec:evolve
```

手動の `distill review`、または新たに抽出する内容がない直接の `distill` は、ローカルのオフラインブラウザーワークスペースを開きます。
記録の修正、承認、破棄、保留、統合を行い、最終的な Markdown をプレビューしてから **すべて適用**を選択できます。
適用までは判断が復旧可能な草案に残ります。競合チェックにより、一部だけの適用や無通知の上書きを防ぎます。
ブラウザーのない環境向けに、明示的なテキスト方式への切り替えも利用できます。

`workflow.auto_distill` のデフォルトは **true** で、3 つの完了時フックを制御します。
`implement-tasks` の成功、`commit-staged` によるコミット実行、`pr` の生成です。コミットプレビューでは知識の抽出は行われません。

インストールされたプロジェクトガイダンスでは、通常の会話、SDD 外の修正、長い `implement-tasks` の実行中にも、
再利用可能な知識が得られた時点で記録するようエージェントに求めます。
このガイダンスは完了時の設定とは独立して適用され、タスク終了時の抽出が最後の取りこぼし防止となります。

セッション内で繰り返し発動する場合は、新しい内容だけを処理します。セッションをまたぐ場合、`distill` はプロファイルを読み、
すでに扱われた知識を飛ばします。再利用可能な内容が残っていなければ、書き込まずに終了します。
自動抽出は手動レビューを開かず、人を待たず、呼び出し元のワークフローを妨げません。

`evolve` はプロジェクト外でも役立つ承認済みの知識だけを選び、コマンド・スキルの草案にまとめます。
push または人によるレビューのための貢献 PR を開く前に、明示的な承認を得ます。

詳細は、[プロジェクト知識](docs/en/user-guide/commands.md#codexspecdistill)を参照してください。

### 過去の判断の再利用

実質的な要件、設計、実装、デバッグ、レビューの判断前には、`.codexspec/specs/` 内の関連する履歴も参照します。
これは通常の会話にも SDD ワークフローにも適用されます。
エージェントはユーザーに尋ねる前に、変更されていない判断、後からの追加、明示的な置き換えを再構成します。

古い要件も変更されていなければ引き続き適用されます。ユーザーの最新の明示的な判断が常に優先され、
未確定の提案を確認済みの意図として扱いません。検索範囲はタスクに絞り、十分な背景情報は再利用します。
このガイダンスを受け取るには、既存プロジェクトのインストールを更新してください。

## Git ワークフロー

```text
/codexspec:commit-staged -p
/codexspec:pr --spec <feature-dir>/spec.md
/codexspec:release-notes --from <ref> --to HEAD
/codexspec:tasks-to-issues <feature-dir>
```

- **commit-staged** はステージング領域を厳密に分析し、Conventional Commits のメッセージを生成します。
  `-p` はコミットせずにプレビューします。ファイルの選択とステージングは呼び出し元のワークフローが行います。
  許可された実行では保護された実行環境を使い、コミット対象の内容が分析と一致することを再確認します。
  エージェントのコミットガイダンスは通常の会話、SDD、blueprint、auto-dev のワークフローに適用されますが、
  コマンドが利用可能であるだけでは呼び出しにもコミット許可にもなりません。
- **pr** は差分から構造化された GitHub PR または GitLab MR の説明を生成します。
  `--spec` は任意で、`spec.md` のファイルパス、またはそのファイルに解決される機能ディレクトリ名やプレフィックスから、機能の文脈を追加します。
  デフォルトの出力は、ホスティングプラットフォームで使用するテキストです。
- **release-notes** は Git 履歴から Keep a Changelog のエントリとリリース本文を導出します。
  デフォルトのセクションは `[Unreleased]` で、`--version` は指定されたラベルを使います。
  ステージング、コミット、バージョン更新、タグ付け、公開、リリース作成は行いません。
- **tasks-to-issues** は既存のタスクから、依存関係と受け入れ基準を含む GitHub Issue を作成します。
  認証済みの GitHub CLI が必要で、Issue のリポジトリが設定済みのリモートと一致することを検証します。

直接のコミットプレビューと、許可されたその場でのコミットには Python 3.11+ と Git が必要です。
実行環境は CLI プロジェクトにインストールされ、Claude プラグインにも同梱されます。
内容の変更を伴うエージェント作成のマージも、ステージ済み内容の分析を使います。
履歴だけをつなぐマージでは、ツリーと親を検証しながら Git のデフォルトメッセージを維持し、fast-forward ではコミットを作成しません。

## 利用可能なコマンド

CLI には 6 つの公開コマンドがあります。エージェント連携では 28 コマンドを配布します。
Claude は `/codexspec:<name>`、Codex は `$codexspec:<name>` を使います。
以下の表では読みやすさのため Claude の表記を使っています。

### CLI コマンド

| コマンド | 目的 |
|---------|---------|
| `codexspec init` | Claude、Codex、または両方に向けてプロジェクトを初期化・更新 |
| `codexspec check` | インストール済みツールと依存関係を確認 |
| `codexspec version` | バージョンとシステム情報を表示 |
| `codexspec config` | プロジェクト設定を表示・変更 |
| `codexspec list-commands` | 利用可能なエージェントコマンドをカテゴリ別に一覧表示 |
| `codexspec show-blueprint` | 共有 worktree のブループリントを変更せずに出力 |

### 基本ワークフローコマンド

| コマンド | 目的 |
|---------|---------|
| `/codexspec:constitution` | 成果物間の検証を伴うプロジェクト原則の作成・更新 |
| `/codexspec:specify` | 機能要件を検討、確認、永続化 |
| `/codexspec:blueprint` | 確認済みで保留中のブループリント要件を準備・保守 |
| `/codexspec:generate-spec` | 確認済み要件を追跡可能な仕様書にまとめ、自動レビュー |
| `/codexspec:spec-to-design` | アーキテクチャ、コンポーネント、インターフェース、判断を定義し、自動レビュー |
| `/codexspec:design-to-plan` | 実装フェーズ、順序、検証を計画し、自動レビュー |
| `/codexspec:plan-to-tasks` | 上位成果物の内容を網羅する検証可能なタスクを作成し、自動レビューと分析 |
| `/codexspec:implement-tasks` | タスクを実行し、結果を検証してレビュー・修正 |
| `/codexspec:auto-dev` | 確認済みブループリント要件をドキュメントの順序で自律開発 |

### 成果物レビューコマンド

| コマンド | 目的 |
|---------|---------|
| `/codexspec:review-spec` | 仕様書の忠実度と内部品質を確認 |
| `/codexspec:review-design` | 設計の忠実度、実現可能性、計画準備状況を確認 |
| `/codexspec:review-plan` | 計画の忠実度、実現可能性、実装準備状況を確認 |
| `/codexspec:review-tasks` | タスクの忠実度、依存関係、実行可能性、検証を確認 |

### 要件、既存コード、デバッグ

| コマンド | 目的 |
|---------|---------|
| `/codexspec:clarify` | 要件の曖昧さを解消し、仕様書より先に要件を更新 |
| `/codexspec:analyze` | 端から端までの追跡可能性を確認し、下位成果物を判断基準に適合 |
| `/codexspec:checklist` | 要件品質チェックリストを生成 |
| `/codexspec:tasks-to-issues` | 既存のタスクを実行可能な GitHub Issue に変換 |
| `/codexspec:debug` | 修正を適用する前に根本原因を調査 |
| `/codexspec:reverse-spec` | 既存のアーキテクチャを調査、モジュール成果物の草案を作成、または基準との差異を報告 |

### プロジェクト知識コマンド

| コマンド | 目的 |
|---------|---------|
| `/codexspec:distill` | 再利用可能な知識を記録、またはローカルワークスペースで候補をレビュー |
| `/codexspec:evolve` | 承認済み知識を上流への貢献の草案にまとめる |
| `/codexspec:onboard` | 既存コードから候補の慣行と証拠に基づく制約を蓄積 |

### Git とコードレビューのコマンド

| コマンド | 目的 |
|---------|---------|
| `/codexspec:commit-staged` | ステージ済み変更からメッセージを生成し、プレビューまたは許可されたコミットを実行 |
| `/codexspec:pr` | 構造化された PR/MR の説明を生成 |
| `/codexspec:release-notes` | 変更履歴のエントリを保守し、Git 履歴からリリース本文を生成 |
| `/codexspec:review-code` | 選択した変更を欠陥ゲートとしてレビュー。パスの品質評価には `--audit` を使用 |

### ユーティリティコマンド

| コマンド | 目的 |
|---------|---------|
| `/codexspec:config` | 対話的にプロジェクト設定を作成・表示・変更・リセット |
| `/codexspec:quick` | 小さな変更に対して簡潔な要件優先 SDD ワークフローを実行 |

## 設定と国際化

設定は `.codexspec/config.yml` に保存されます。テンプレートは英語のままで、エージェントは設定された言語で対話文と成果物を作成します。
標準の言語コードは 13 個で、`en`、`zh-CN`、`zh-TW`、`ja`、`ko`、`es`、`fr`、`de`、`pt`、`ru`、`it`、`ar`、`hi` です。
ポルトガル語の CLI コードは `pt` ですが、ローカライズされたドキュメントと翻訳カタログでは `pt-BR` を使います。

### 言語の区分

| 区分 | 設定キー | 初期化時 | 後から設定 | 制御対象 |
|-----------|------------|-------------------|-----------|----------|
| 出力・基準 | `language.output` | `--lang` | `config --set-lang` | 他の言語区分のフォールバック |
| 対話 | `language.interaction` | `--interaction-lang` | `config --set-interaction-lang` | 会話と CLI 出力 |
| ドキュメント | `language.document` | `--document-lang` | `config --set-document-lang` | 要件、仕様書、設計、計画、タスク |
| コミット | `language.commit` | `--commit-lang` | `config --set-commit-lang` | コミットメッセージと Git による成果物提供の内容 |

各言語区分は独立して `language.output`、次に `en` へフォールバックします。`language.templates` は `en` のままです。

```bash
codexspec init my-project --ai both \
  --interaction-lang zh-CN --document-lang en --commit-lang en

codexspec config
codexspec config --set-document-lang en
codexspec config --list-langs
```

初回の TTY 初期化では、`--lang` または 3 つすべての個別言語オプションを指定しない限り、基準言語を尋ねます。
`--force` は他の初期化時の確認を自動承認しますが、この言語選択は省略しません。
非 TTY での初期化はデフォルトで英語になります。再初期化では、明示的に設定していない言語キーを維持します。

### ワークフローとレビューの設定

| 設定 | デフォルト | 効果 | CLI 操作 |
|---------|---------|--------|-------------|
| `workflow.auto_next` | `false` | 合格した通常の SDD ステージを進める | `config --auto-next on\|off` |
| `workflow.auto_distill` | `true` | 完了処理の成功後に非対話的に知識を抽出 | `config --auto-distill on\|off` |
| `workflow.auto_maintenance` | `true` | 自動修正中に検証済みの段階的な保守を適用 | `config --auto-maintenance on\|off` |
| `workflow.worktrees` | `true` | 通常の機能と単独の保守作業を分離 | `config --worktrees on\|off` |
| `review.decided_by` | `reviewer` | プロジェクトの運用範囲外で発生する指摘の判断者 | `config --decided-by reviewer\|ask` |

真偽値の CLI スイッチは、大文字・小文字を区別せず、前後の空白も含めて `on/true/1/yes` と `off/false/0/no` を受け付けます。
値を付けずに真偽値スイッチを使うと、書き込み先チェックアウトの現在値を切り替えます。YAML に保存される値は真偽値です。

`review.decided_by: reviewer` では、レビュアーが欠陥として採用するかを判断します。
`ask` では、運用範囲外の発生条件は保留中のシナリオ判断となり、修正するか、そのシナリオを除外するかをユーザーが一度決めます。
確認済みの判断は後続ラウンドのために保存されます。保留中の判断があると完了できません。
単一の `review-code` 実行では、`--decided-by` で設定済みモードを上書きできます。

設定の書き込みは worktree の作業先選択に従います。main チェックアウトからの単独の変更は保守用 worktree で行われ、
main の実効設定は直ちには変わりません。機能 worktree 内の変更は、その場所で有効になります。

<details>
<summary>CLI 初期化オプション</summary>

| オプション | 意味 |
|--------|---------|
| `PROJECT_NAME` | 新しいディレクトリ名。現在のディレクトリには `.` を使用 |
| `--here`, `-h` | 現在のディレクトリを初期化 |
| `--ai`, `-a` | `claude`、`codex`、`both` のいずれか。デフォルトは `claude` |
| `--lang`, `-l` | 基準となる出力言語を設定 |
| `--interaction-lang` | 対話言語を設定 |
| `--document-lang` | ドキュメント言語を設定 |
| `--commit-lang` | コミットメッセージの言語を設定 |
| `--force`, `-f` | インストール済み成果物を再生成し、移行・更新・準拠の確認を自動承認。プロジェクト作成のコンテキストと無関係な設定は維持 |
| `--no-git` | Git リポジトリの初期化を省略 |
| `--debug`, `-d` | 詳細なデバッグ出力を表示 |

</details>

<details>
<summary>CLI 設定オプション</summary>

| オプション | 意味 |
|--------|---------|
| `--set-lang`, `-l` | 基準となる出力言語を設定 |
| `--set-interaction-lang` | 対話言語を設定 |
| `--set-document-lang` | ドキュメント言語を設定 |
| `--set-commit-lang`, `-c` | コミットメッセージの言語を設定 |
| `--list-langs` | サポートする言語コードを一覧表示 |
| `--auto-next` | ステージの自動進行を切り替え・設定 |
| `--auto-distill` | 自動知識抽出を切り替え・設定 |
| `--auto-maintenance` | 自動での段階的な保守を切り替え・設定 |
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

言語と設定の詳細な動作は、[設定](docs/en/reference/configuration.md)と[国際化](docs/en/user-guide/i18n.md)を参照してください。

## プロジェクト構成

初期化では、共通リソースと選択したアシスタント連携をインストールします。

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

共有ブループリントは専用の auto-dev worktree に置かれ、通常のチェックアウトごとに編集可能な別コピーを持つことはありません。
手動の知識レビューの草案は Git から除外されます。

## 拡張機能の作成資料

リポジトリには、拡張機能のマニフェストテンプレート、コマンド例、[拡張機能開発ガイド](extensions/EXTENSION-DEVELOPMENT-GUIDE.md)が含まれます。
これらは作成用の資料です。現在の CLI には拡張機能のインストール・一覧・削除コマンドはなく、
`extension.yml` のコマンドやフックを自動的に読み込むこともありません。
共通レビューリソースは `.codexspec/review-code/` 内のプロジェクト固有の追加をサポートします。
初期化では、置換を要求しない限り、既存のリソース編集と追加ファイルを維持します。

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
配布コマンドとスキルのコピーは生成されたインストール成果物です。正規の出典を編集して再生成してください。

## 貢献

ローカル環境の準備と貢献の進め方は、[貢献ガイド](docs/en/development/contributing.md)を参照してください。
貢献では、確認済み要件、出典への追跡可能性、ユーザー向けと保守者向けのパッケージ境界を維持してください。

## ライセンス

MIT — [LICENSE](LICENSE) を参照してください。

## 謝辞

[GitHub spec-kit](https://github.com/github/spec-kit) から着想を得ています。
Claude Code と OpenAI Codex に連携します。
