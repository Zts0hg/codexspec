# CodexSpec

![CodexSpec](assets/images/codexspec-logo-light.svg#only-light){ width="420" }

![CodexSpec](assets/images/codexspec-logo-dark.svg#only-dark){ width="420" }

**Claude Code と OpenAI Codex 向けの要件優先 SDD ツールキット**

CodexSpec は、確認済みの要件をもとに、仕様書、設計、計画、タスク、実装を作成し、それぞれのつながりを追跡できるようにします。
**何を**作るか、**なぜ**作るかはユーザーが決めます。エージェントはその要件の範囲内で、
レビューの節目とプロジェクトに保存した知識を活用しながら、**どのように**実現するかを具体化します。

Claude Code のスラッシュコマンド、Codex のスキル、または両方から利用できます。
通常の機能開発には、デフォルトで機能ごとに独立した Git worktree を使います。
共有ブループリントを利用すると、確認済み要件のキューをエージェントに自律的に開発させることもできます。

<a id="why-choose-codexspec"></a>

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

<a id="what-is-requirements-first-sdd"></a>

### 要件優先 SDD とは

要件優先の仕様駆動開発では、**確認済み要件を、その機能について最優先の判断基準**とします。
エージェントは実装に向けた成果物を作成する前に、目標、制約、判断、除外事項、未解決の質問、確認の根拠を記録します。

```text
Idea → Confirmed Requirements →     Spec    →     Design    →     Plan    →    Tasks     →     Code
                 ↓                   ↓              ↓              ↓             ↓              ↓
         User confirmation      review-spec   review-design   review-plan   review-tasks   review-code
```

要件を確認するのはユーザーです。仕様からコードまで、そこから作成される各成果物には、それぞれ対応するレビューがあります。

製品として何を実現するかは、人との協働を通じて定め、変更します。
自動レビューでは、作成した成果物がその意図に沿っているかを確認します。
自動化を有効にすると、合格したステージから次へ進みます。エージェントが確認済み要件を無断で置き換えることはありません。

[![CodexSpec：要件優先の開発フロー、各段階のレビューと経験を次に生かす循環](../../assets/workflow/workflow-ja-light.png#only-light)](../../assets/workflow/workflow-ja-light.png#only-light)

[![CodexSpec：要件優先の開発フロー、各段階のレビューと経験を次に生かす循環](../../assets/workflow/workflow-ja-dark.png#only-dark)](../../assets/workflow/workflow-ja-dark.png#only-dark)

図を原寸で開く： [☀️](../../assets/workflow/workflow-ja-light.png) · [🌙](../../assets/workflow/workflow-ja-dark.png)

<a id="30-second-quick-start"></a>

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
以降のコマンドについては、[基本ワークフロー](user-guide/workflow.md#core-workflow)を参照してください。

Codex デスクトップアプリをお使いの場合は、[Codex にインストールとプロジェクトの初期化を依頼できます](getting-started/installation.md#install-with-the-codex-desktop-app)。
