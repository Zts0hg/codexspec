<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/images/codexspec-logo-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/images/codexspec-logo-light.svg">
  <img alt="CodexSpec Logo" src="assets/images/codexspec-logo-light.svg" width="420">
</picture>

# CodexSpecへようこそ

[![PyPI version](https://img.shields.io/pypi/v/codexspec:svg)](https://pypi.org/project/codexspec/)
[![Python](https://img.shields.io/pypi/pyversions/codexspec:svg)](https://pypi.org/project/codexspec/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Claude Code向けSpec-Driven Development (SDD) ツールキット**

CodexSpecは、構造化された仕様駆動アプローチを使用して高品質なソフトウェアを構築するのに役立つツールキットです。仕様を直接実装をガイドする実行可能なアーティファクトにすることで、従来の開発アプローチを転換します。

## なぜCodexSpecなのか？

### 人間とAIの協調

CodexSpecは、**効果的なAI支援開発にはすべての段階で人間の積極的な参加が必要**という信念に基づいて構築されています。

| 問題 | 解決策 |
|---------|----------|
| 不明確な要件 | 構築前に対話形式で明確化 |
| 不完全な仕様 | スコアリング付きの専用レビューコマンド |
| 整合性のない技術計画 | 憲法ベースの検証 |
| 曖昧なタスク分割 | TDD強制タスク生成 |

### 主な機能

- **憲法ベース** - すべての決定を導くプロジェクト原則を確立
- **対話型明確化** - Q&Aベースの要件精緻化
- **レビューコマンド** - 各段階でアーティファクトを検証
- **TDD対応** - タスクに組み込まれたテストファースト手法
- **i18nサポート** - LLM翻訳による13以上の言語対応

## クイックスタート

```bash
# インストール
uv tool install codexspec

# 新しいプロジェクトを作成
codexspec init my-project

# または既存のプロジェクトで初期化
codexspec init . --ai claude
```

[インストールガイド](getting-started/installation.md)

## ワークフロー概要

```
アイデア -> 明確化 -> レビュー -> 計画 -> レビュー -> タスク -> レビュー -> 実装
              ^                ^                ^
           人間の確認        人間の確認        人間の確認
```

すべてのアーティファクトには、進行前にAI出力を検証するための対応するレビューコマンドがあります。

[ワークフローを学ぶ](user-guide/workflow.md)

## ライセンス

MITライセンス - 詳細は[LICENSE](https://github.com/Zts0hg/codexspec/blob/main/LICENSE)を参照してください。
