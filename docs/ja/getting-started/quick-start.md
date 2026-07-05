# クイックスタート

このページでは、完全な **Requirements-First SDD** の流れを 8 ステップで説明します。
確認された要件が最優先の権威であり、あなたが明示的に確認するまでは何も確定しません ― 各段階はあなたが制御する **Confirmation Gate** で終わります。

小さく範囲が明確な変更であれば、完全なウォークスルーを省いて [`/codexspec:quick`](#小さな変更-codexspecquick) を実行することもできます。

## 1. プロジェクトを初期化する

インストールが終わったら、プロジェクトを作成または初期化します。

```bash
# 新規プロジェクトを作成
codexspec init my-awesome-project

# またはカレントディレクトリで初期化
codexspec init . --ai claude

# 中国語で出力 (出力のベースを設定)
codexspec init my-project --lang zh-CN

# 完全非対話 (CI/スクリプト向け): 出力ベースを zh-CN、コミットメッセージを英語
codexspec init my-project --lang zh-CN --commit-lang en

# すべての言語次元を明示的に指定 (スクリプト可能、プロンプトなし)
codexspec init my-project \
  --interaction-lang zh-CN --document-lang en --commit-lang en
```

その後、プロジェクトに移動して Claude Code を起動します。

```bash
cd my-awesome-project
claude
```

## 2. プロジェクト原則を定める

constitution コマンドを使って、後続のすべての成果物が照らし合わせる基準を設定します。

```
/codexspec:constitution Create principles focused on code quality and testing
```

## 3. 要件を明確化する

`/codexspec:specify` を使って要件を探索します。

```
/codexspec:specify I want to build a task management application
```

このコマンドは明確化の質問を投げかけ、エッジケースを浮かび上がらせ、最終的な要件サマリを確認に渡します。確認されたサマリは `requirements.md` に永続化されます。

> **Confirmation Gate**: `/codexspec:specify` は、あなたが明示的に確認した項目だけを書き込みます。提示される要件サマリは、あなたが受け入れるまでは確定**しません**。yes と言う前であれば、どの項目でも却下・修正・再検討できます。ここであなたが確認した内容は、下流のどのコマンドでも覆せません。

## 4. 仕様書を生成する

要件サマリが確認されたら、spec ドキュメントを生成します。

```
/codexspec:generate-spec
```

`generate-spec` は、確認された項目を構造化された `spec.md` にまとめ直します。トレーサビリティのためのソース参照を付与した上で、自動レビューを実行します (欠陥には具体的証拠が必要、助言的提案は自動変更をトリガーしない、検証された欠陥は最大 2 ラウンドまで修正と再レビューが可能)。

## 5. レビュー・検証する

**推奨:** 次に進む前に spec を検証します。

```
/codexspec:review-spec
```

これは **証拠に基づくレビュー** です。報告される欠陥はすべて具体的な証拠を引用し、設計の助言は受け入れ判断から切り離して扱われます。

## 6. 技術計画を作成する

```
/codexspec:spec-to-plan Use Python FastAPI for backend
```

計画は仕様の要件への `Covers` リンクを記録し、該当する憲法原則を検証します。

## 7. タスクを生成する

```
/codexspec:plan-to-tasks
```

タスクは検証可能な結果を中心に構成され、計画と要件へのトレーサビリティリンクを持ちます。テストファーストの順序は**条件付き**で適用されます ― plan・憲法・タスクのリスクで要求される場合のみです。ドキュメントや設定など検証不可能なタスクは直接実装されます。

## 8. 実装する

```
/codexspec:implement-tasks
```

実装は **conditional TDD** に従います。コードのタスクは要求された場合に Red → Green → Verify → Refactor のサイクルを使い、ドキュメントや設定のタスクは直接実装されます。

## 小さな変更: `/codexspec:quick`

小さく範囲が明確な変更であれば、8 ステップの完全なウォークスルーは不要です。`/codexspec:quick` は単一のコマンドでコンパクトな Requirements-First SDD フローを実行します。

```
/codexspec:quick Add a "remember me" checkbox to the login form
```

Quick は完全なフローと同じガードレールを守ります。

- `/codexspec:specify` と同じタイムスタンプ規約で、機能ワークスペースと `requirements.md` を作成します。
- 簡潔な確認済み要件サマリ (`NEED-*`、関連する `CON-*`/`DEC-*`、`OUT-*`、未解決の `OPEN-*`) を提示し、あなたの明示的な確認を待ちます ― **Confirmation Gate** は引き続き適用されます。
- その後、`/codexspec:generate-spec` → `/codexspec:spec-to-plan` → `/codexspec:plan-to-tasks` → `/codexspec:implement-tasks` をその機能ディレクトリに対して連鎖実行します。各生成コマンドは自身の自動レビューループを持ちます。

変更が広範になったり複数の独立した結果を持つことが分かった場合、Quick は一旦止まり、標準フローへの切り替えを勧めます。

## プロジェクト構造

初期化後の構造は次のとおりです。

```
my-project/
├── .codexspec/
│   ├── memory/
│   │   └── constitution.md    # プロジェクト憲法
│   ├── specs/
│   │   └── {feature-id}/
│   │       ├── spec.md        # 機能仕様書
│   │       ├── plan.md        # 技術計画
│   │       ├── tasks.md       # タスク分割
│   │       └── checklists/    # 品質チェックリスト
│   ├── templates/             # カスタムテンプレート
│   ├── scripts/               # ヘルパースクリプト
│   └── extensions/            # カスタム拡張
├── .claude/
│   └── commands/              # Claude Code スラッシュコマンド
├── .agents/
│   └── skills/                # Codex スキル (--ai codex または both で初期化した場合)
├── CLAUDE.md                  # Claude Code コンテキスト
└── AGENTS.md                  # Codex コンテキスト
```

## 次のステップ

[完全なワークフローガイド](../user-guide/workflow.md)
