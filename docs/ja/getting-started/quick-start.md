# クイックスタート

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
以降のコマンドについては、[基本ワークフロー](../user-guide/workflow.md#core-workflow)を参照してください。

Codex デスクトップアプリをお使いの場合は、[Codex にインストールとプロジェクトの初期化を依頼できます](installation.md#install-with-the-codex-desktop-app)。

<a id="core-workflow"></a>

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

<a id="specify-clarify-and-analyze"></a>

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

<a id="small-changes-with-quick"></a>

### Quick による小さな変更

局所的な修正など、範囲が明確で小さな変更には `quick` を使います。

```text
/codexspec:quick Fix the empty-state message on the task list
```

Quick は簡潔な要件サマリーを確認して保存した後、仕様作成、計画、タスク化、実装を順に進めます。
各生成コマンドによるレビューも行います。広範な変更や、製品・設計上の選択が未解決の場合は、標準ワークフローを使ってください。
Quick は新しい判断が必要になると一時停止します。

<a id="workflow-automation"></a>

### ワークフローの自動化

`workflow.auto_next` のデフォルトは **false** です。
作業中のワークスペースの設定で `true` にすると、最終的な要件確認後に仕様作成へ進みます。
各生成ステージは `PASS` または `PASS_WITH_WARNINGS` で次へ進み、`NEEDS_REVISION` または `BLOCKED` で停止します。
`implement-tasks` が最終ステージです。

成果物の自動修正は、検証済みの欠陥のうち、上位の根拠から修正内容を導けるものに限られます。
修正とレビューは最大 2 ラウンドまで行います。助言は別に扱います。
実装のレビュー・修正ループには、後述する独自の完了条件があります。

詳しい動作と条件は、[ワークフローガイド](../user-guide/workflow.md)を参照してください。

<a id="project-structure"></a>

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
