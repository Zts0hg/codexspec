<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/images/codexspec-logo-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/images/codexspec-logo-light.svg">
  <img alt="CodexSpec Logo" src="assets/images/codexspec-logo-light.svg" width="420">
</picture>

# CodexSpec へようこそ

[![PyPI version](https://img.shields.io/pypi/v/codexspec.svg)](https://pypi.org/project/codexspec/)
[![Python](https://img.shields.io/pypi/pyversions/codexspec.svg)](https://pypi.org/project/codexspec/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Claude Code 向けの Requirements-First SDD ツールキット**

CodexSpec は、**Requirements-First Spec-Driven Development (SDD)** を通じて高品質なソフトウェアの構築を支援します。確認された要件が最優先の権威であり、あなたが明示的に確認するまでは何も確定しません。すぐにコードに取り掛かるのではなく、**何を**・**なぜ**作るかを先に確定し、それから**どうやって**作るかを決めます。

## なぜ CodexSpec を使うのか？

Claude Code に CodexSpec を上乗せする理由とは何か？ 比較をご覧ください。

| 観点 | Claude Code 単体 | CodexSpec + Claude Code |
|--------|------------------|-------------------------|
| **多言語サポート** | デフォルトは英語での対話 | チームの言語を設定でき、協業とレビューがより円滑に |
| **トレーサビリティ** | セッション終了後の意思決定の追跡が困難 | すべての spec・plan・task が `.codexspec/specs/` に保存される |
| **セッションの再開** | plan モードの中断から復帰しにくい | 複数コマンドへの分割と永続化されたドキュメントにより容易に復帰 |
| **チームガバナンス** | 統一原則がなくスタイルが一貫しない | `constitution.md` がチームの基準と品質を強制 |

### Requirements-First SDD とは？

**Requirements-First SDD** は、Spec-Driven Development (SDD) の手法に一点のアップグレードを加えたものです。**確認された要件が最優先の権威**になります。*何を*作り*なぜ*作るかを、*どうやって*作るかの前に定義して確認し、あなたが明示的に確認するまでは何も確定しません。

```
Traditional:  Idea → Code → Debug → Rewrite
SDD:          Idea → Confirmed Requirements → Spec → Plan → Tasks → Code
```

### 主な特徴

- **憲法に基づく開発** - すべての意思決定を導くプロジェクト原則を確立
- **要件の永続的な記録** - `/specify` はドキュメント生成前に、確認された議論の内容を `requirements.md` に記録
- **自動レビュー** - 生成された spec・plan・task の各成果物すべてに組み込みの品質チェックを同梱
- **対話型の明確化** - Q&A による要件の洗練
- **成果物間の分析** - 実装前に不整合を検出
- **トレーサブルなタスク** - タスク分割は要件と計画のカバレッジを保持し、**Conditional TDD** を適用（plan・憲法・リスクで要求される場合のみテストファーストの順序を採用。ドキュメントや設定など検証不可能なタスクは直接実装）
- **Claude Code とのネイティブ連携** - スラッシュコマンドがシームレスに動作
- **多言語サポート** - LLM による動的翻訳で 13 以上の言語に対応
- **クロスプラットフォーム** - Bash と PowerShell のスクリプトを同梱
- **拡張可能** - カスタムコマンド向けのプラグインアーキテクチャ

## クイックスタート

```bash
# インストール
uv tool install codexspec

# 新規プロジェクトを作成
codexspec init my-project

# または既存プロジェクトで初期化
codexspec init . --ai claude
```

[完全なインストールガイド](getting-started/installation.md)

## ワークフローの概要

CodexSpec は開発を **レビュー可能なチェックポイント** として構造化します。確認された要件は、各段階でのレビューを経て spec・plan・task を通じてコードへと流れていきます。

```
Idea → Confirmed Requirements → Spec → Plan → Tasks → Code
```

各成果物は専用のコマンドで生成され、次の段階に進む前に検証されます。

```
Idea → /specify → requirements.md → /generate-spec → spec.md → /spec-to-plan → plan.md → /plan-to-tasks → tasks.md → /implement
                                                   │                         │                            │
                                              Review spec               Review plan                  Review tasks
```

### 確認ゲート (Confirmation Gate)

決定的な差別化要因となるのが **Confirmation Gate** です。要件・spec・plan・task は、あなたが人間として明示的に確認した後にのみ確定されます。確認された要件は最優先の機能権威であるため、AI が暗黙に意思決定を固定することはありません。派生した成果物には明示的なソースリンクが付き、矛盾は伝播されずに逆追跡されます。

### 反復型の品質ループ

すべての生成コマンドには **自動的かつ証拠に基づくレビュー** が備わっています。欠陥には具体的な証拠が必要で、助言的な提案は自動変更をトリガーせず、検証された欠陥は最大 2 ラウンドまで修正と再レビューを行えます。このループにより、あなたが細部までいちいち世話を焼かなくても品質が上がり続けます。

[ワークフローを学ぶ](user-guide/workflow.md)

## ライセンス

MIT License - 詳細は [LICENSE](https://github.com/Zts0hg/codexspec/blob/main/LICENSE) を参照してください。
