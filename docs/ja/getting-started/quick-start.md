# クイックスタート

## 1. プロジェクトの初期化

インストール後、プロジェクトを作成または初期化します：

```bash
# 新しいプロジェクトを作成
codexspec init my-awesome-project

# または現在のディレクトリで初期化
codexspec init . --ai claude

# 中国語出力で作成
codexspec init my-project --lang zh-CN
```

## 2. プロジェクト原則の確立

プロジェクトディレクトリでClaude Codeを起動します：

```bash
cd my-awesome-project
claude
```

constitutionコマンドを使用します：

```
/codexspec.constitution コード品質とテストに焦点を当てた原則を作成
```

## 3. 要件の明確化

`/codexspec.specify`を使用して要件を探索します：

```
/codexspec.specify タスク管理アプリケーションを構築したい
```

## 4. 仕様書の生成

明確化が完了したら、仕様書ドキュメントを生成します：

```
/codexspec.generate-spec
```

## 5. レビューと検証

**推奨:** 進行前に検証します：

```
/codexspec.review-spec
```

## 6. 技術計画の作成

```
/codexspec.spec-to-plan バックエンドにPython FastAPIを使用
```

## 7. タスクの生成

```
/codexspec.plan-to-tasks
```

## 8. 実装

```
/codexspec.implement-tasks
```

## プロジェクト構造

初期化後：

```
my-project/
+-- .codexspec/
|   +-- memory/
|   |   +-- constitution.md
|   +-- specs/
|   |   +-- {feature-id}/
|   |       +-- spec.md
|   |       +-- plan.md
|   |       +-- tasks.md
|   +-- scripts/
+-- .claude/
|   +-- commands/
+-- CLAUDE.md
```

## 次のステップ

[フルワークフローガイド](../user-guide/workflow.md)
