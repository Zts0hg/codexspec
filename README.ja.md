# CodexSpec

[English](README.md) | [中文](README.zh-CN.md) | **日本語** | [Español](README.es.md) | [Português](README.pt-BR.md) | [한국어](README.ko.md) | [Deutsch](README.de.md) | [Français](README.fr.md)

[![PyPI version](https://img.shields.io/pypi/v/codexspec.svg)](https://pypi.org/project/codexspec/)
[![Python](https://img.shields.io/pypi/pyversions/codexspec.svg)](https://pypi.org/project/codexspec/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Claude Code 向けスペック駆動開発 (SDD) ツールキット**

CodexSpec は、構造化されたスペック駆動アプローチを使用して高品質なソフトウェアを構築するのに役立つツールキットです。仕様を実行可能なアーティファクトに変換し、実装を直接ガイドすることで、従来の開発手法を一新します。

## 特徴

- **構造化ワークフロー**: 開発の各フェーズに明確なコマンド
- **Claude Code 統合**: Claude Code のスラッシュコマンドをネイティブサポート
- **憲法ベース**: プロジェクトの原則がすべての決定をガイド
- **スペックファースト**: 「どう」の前に「何」と「なぜ」を定義
- **プラン駆動**: 技術選択は要件の後に行う
- **タスク指向**: 実装を実行可能なタスクに分解
- **品質保証**: レビュー、分析、チェックリストコマンドを内蔵
- **国際化 (i18n)**: LLM ダイナミック翻訳による多言語サポート
- **クロスプラットフォーム**: Bash と PowerShell スクリプトの両方をサポート
- **拡張可能**: カスタムコマンド用のプラグインアーキテクチャ

## インストール

### 前提条件

- Python 3.11+
- [uv](https://docs.astral.sh/uv/)（推奨）または pip

### 方法 1: uv でインストール（推奨）

uv を使用するのが最も簡単なインストール方法です：

```bash
uv tool install codexspec
```

### 方法 2: pip でインストール

または pip を使用：

```bash
pip install codexspec
```

### 方法 3: 一時使用

インストールせずに直接実行：

```bash
# 新しいプロジェクトを作成
uvx codexspec init my-project

# 既存のプロジェクトで初期化
cd your-existing-project
uvx codexspec init . --ai claude
```

### 方法 4: GitHub からインストール（開発版）

最新の開発版または特定のブランチからインストール：

```bash
# uv を使用
uv tool install git+https://github.com/Zts0hg/codexspec.git

# pip を使用
pip install git+https://github.com/Zts0hg/codexspec.git

# 特定のブランチまたはタグ
uv tool install git+https://github.com/Zts0hg/codexspec.git@main
uv tool install git+https://github.com/Zts0hg/codexspec.git@v0.2.0
```

## クイックスタート

インストール後、CLI を使用できます：

```bash
# 新しいプロジェクトを作成（日本語出力）
codexspec init my-project --lang ja

# 既存のプロジェクトで初期化
codexspec init . --ai claude

# インストールされたツールを確認
codexspec check

# バージョンを表示
codexspec version
```

最新版にアップグレード：

```bash
# uv を使用
uv tool install codexspec --upgrade

# pip を使用
pip install --upgrade codexspec
```

## 使用方法

### 1. プロジェクトの初期化

[インストール](#インストール)後、プロジェクトを作成または初期化します：

```bash
codexspec init my-awesome-project --lang ja
```

### 2. プロジェクト原則の確立

プロジェクトディレクトリで Claude Code を起動します：

```bash
cd my-awesome-project
claude
```

`/codexspec.constitution` コマンドを使用してプロジェクトのガバナンス原則を作成します：

```
/codexspec.constitution コード品質、テスト標準、クリーンアーキテクチャに焦点を当てた原則を作成
```

### 3. 要件の明確化

`/codexspec.specify` を使用して、インタラクティブなQ&Aで要件を**探索・明確化**します：

```
/codexspec.specify タスク管理アプリケーションを構築したい
```

このコマンドは：
- アイデアを理解するための明確化質問を行う
- 考虑されていないエッジケースを探索
- ダイアログを通じて高品質な要件を共創
- ファイルを自動生成**しない** - ユーザーがコントロール

### 4. スペックドキュメントの生成

要件が明確になったら、`/codexspec.generate-spec` を使用して `spec.md` ドキュメントを作成します：

```
/codexspec.generate-spec
```

このコマンドは「要件コンパイラ」として機能し、明確化された要件を構造化されたスペックドキュメントに変換します。

### 5. 技術計画の作成

`/codexspec.spec-to-plan` を使用して実装方法を定義します：

```
/codexspec.spec-to-plan バックエンドに Python と FastAPI、データベースに PostgreSQL、フロントエンドに React を使用
```

### 6. タスクの生成

`/codexspec.plan-to-tasks` を使用して計画を分解します：

```
/codexspec.plan-to-tasks
```

### 7. 分析（オプションだが推奨）

`/codexspec.analyze` を使用してクロスアーティファクト整合性チェックを行います：

```
/codexspec.analyze
```

### 8. 実装

`/codexspec.implement-tasks` を使用して実装を実行します：

```
/codexspec.implement-tasks
```

## 利用可能なコマンド

### CLI コマンド

| コマンド | 説明 |
|----------|------|
| `codexspec init` | 新しい CodexSpec プロジェクトを初期化 |
| `codexspec check` | インストールされたツールを確認 |
| `codexspec version` | バージョン情報を表示 |
| `codexspec config` | プロジェクト設定を表示または変更 |

### `codexspec init` オプション

| オプション | 説明 |
|------------|------|
| `PROJECT_NAME` | 新しいプロジェクトディレクトリの名前 |
| `--here`, `-h` | 現在のディレクトリで初期化 |
| `--ai`, `-a` | 使用する AI アシスタント（デフォルト：claude） |
| `--lang`, `-l` | 出力言語（例：en, zh-CN, ja） |
| `--force`, `-f` | 既存のファイルを強制上書き |
| `--no-git` | git 初期化をスキップ |
| `--debug`, `-d` | デバッグ出力を有効化 |

### `codexspec config` オプション

| オプション | 説明 |
|------------|------|
| `--set-lang`, `-l` | 出力言語を設定 |
| `--list-langs` | サポートされている言語を一覧表示 |

### スラッシュコマンド

初期化後、Claude Code で以下のスラッシュコマンドが利用可能です：

#### コアコマンド

| コマンド | 説明 |
|----------|------|
| `/codexspec.constitution` | プロジェクトのガバナンス原則を作成または更新 |
| `/codexspec.specify` | インタラクティブなQ&Aで要件を**明確化**（ファイル生成なし） |
| `/codexspec.generate-spec` | 要件明確化後に `spec.md` ドキュメントを**生成** |
| `/codexspec.spec-to-plan` | スペックを技術計画に変換 |
| `/codexspec.plan-to-tasks` | 計画を実行可能なタスクに分解 |
| `/codexspec.implement-tasks` | 分解に従ってタスクを実行 |

#### レビューコマンド

| コマンド | 説明 |
|----------|------|
| `/codexspec.review-spec` | スペックの完全性をレビュー |
| `/codexspec.review-plan` | 技術計画の実現可能性をレビュー |
| `/codexspec.review-tasks` | タスク分解の完全性をレビュー |

#### 拡張コマンド

| コマンド | 説明 |
|----------|------|
| `/codexspec.clarify` | 既存のspec.mdをスキャンして曖昧な領域を特定し、明確化内容で更新 |
| `/codexspec.analyze` | クロスアーティファクト整合性分析 |
| `/codexspec.checklist` | 要件の品質チェックリストを生成 |
| `/codexspec.tasks-to-issues` | タスクを GitHub issues に変換 |

## ワークフロー概要

```
┌──────────────────────────────────────────────────────────────┐
│                    CodexSpec ワークフロー                     │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  1. Constitution  ──►  プロジェクト原則を定義                 │
│         │                                                    │
│         ▼                                                    │
│  2. Specify  ───────►  インタラクティブQ&Aで要件              │
│         │             を明確化（ファイル作成なし）            │
│         │                                                    │
│         ▼                                                    │
│  3. Generate Spec  ─►  spec.md ドキュメントを作成            │
│         │             （ユーザーが明示的に呼び出し）          │
│         │                                                    │
│         ▼                                                    │
│  4. Review Spec  ───►  スペックを検証                         │
│         │                                                    │
│         ▼                                                    │
│  5. Clarify  ───────►  曖昧さを解決（オプション）             │
│         │                                                    │
│         ▼                                                    │
│  6. Spec to Plan  ──►  技術計画を作成                         │
│         │                                                    │
│         ▼                                                    │
│  7. Review Plan  ───►  技術計画を検証                         │
│         │                                                    │
│         ▼                                                    │
│  8. Plan to Tasks  ─►  タスク分解を生成                       │
│         │                                                    │
│         ▼                                                    │
│  9. Analyze  ───────►  クロスアーティファクト整合性（オプション）│
│         │                                                    │
│         ▼                                                    │
│  10. Review Tasks  ─►  タスク分解を検証                       │
│         │                                                    │
│         ▼                                                    │
│  11. Implement  ─────►  実装を実行                            │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

### 重要概念：要件明確化ワークフロー

CodexSpecはワークフローの異なる段階に対して**2つの異なる明確化コマンド**を提供します：

#### specify vs clarify：どちらを使うべきか？

| 側面 | `/codexspec.specify` | `/codexspec.clarify` |
|------|----------------------|----------------------|
| **目的** | 初期要件の探索 | 既存スペックの反復的な精緻化 |
| **使用タイミング** | 新しいアイデアから開始、spec.mdなし | spec.mdが存在、ギャップを埋める必要あり |
| **入力** | あなたの初期アイデアまたは要件 | 既存のspec.mdファイル |
| **出力** | なし（ダイアログのみ） | 明確化内容でspec.mdを更新 |
| **方法** | オープンエンドのQ&A | 構造化された曖昧さスキャン（6カテゴリ） |
| **質問制限** | 無制限 | 最大5問 |
| **典型的な用途** | "ToDoアプリを構築したい" | "スペックにエラー処理の詳細がない" |

#### 2段階スペック作成

ドキュメント生成の前に：

| 段階 | コマンド | 目的 | 出力 |
|------|----------|------|------|
| **探索** | `/codexspec.specify` | インタラクティブQ&Aで要件を探索・精緻化 | なし（ダイアログのみ） |
| **生成** | `/codexspec.generate-spec` | 明確化された要件を構造化ドキュメントにコンパイル | `spec.md` |

#### 反復的明確化

spec.md作成後：

```
spec.md ──► /codexspec.clarify ──► 更新されたspec.md（Clarificationsセクション付き）
                │
                └── 6カテゴリの曖昧さをスキャン：
                    • 機能スコープと動作
                    • ドメインとデータモデル
                    • インタラクションとUXフロー
                    • 非機能品質属性
                    • エッジケースと失敗処理
                    • 競合解決
```

#### この設計の利点

- **人間-AI協調**：要件発見に積極的に参加
- **明示的制御**：あなたが決定したときのみファイルを作成
- **品質重視**：ドキュメント化の前に要件を十分に探索
- **反復的精緻化**：理解が深まるにつれてスペックを段階的に改善

## プロジェクト構造

初期化後、プロジェクトは以下の構造になります：

```
my-project/
├── .codexspec/
│   ├── memory/
│   │   └── constitution.md    # プロジェクトのガバナンス原則
│   ├── specs/
│   │   └── {feature-id}/
│   │       ├── spec.md        # 機能スペック
│   │       ├── plan.md        # 技術計画
│   │       ├── tasks.md       # タスク分解
│   │       └── checklists/    # 品質チェックリスト
│   ├── templates/             # カスタムテンプレート
│   ├── scripts/               # ヘルパースクリプト
│   │   ├── bash/              # Bash スクリプト
│   │   └── powershell/        # PowerShell スクリプト
│   └── extensions/            # カスタム拡張
├── .claude/
│   └── commands/              # Claude Code 用スラッシュコマンド
└── CLAUDE.md                  # Claude Code 用コンテキスト
```

## 国際化 (i18n)

CodexSpec は **LLM ダイナミック翻訳**を通じて複数の言語をサポートしています。翻訳されたテンプレートを維持するのではなく、Claude が実行時に言語設定に基づいてコンテンツを翻訳します。

### 言語設定

**初期化時：**
```bash
# 日本語出力でプロジェクトを作成
codexspec init my-project --lang ja

# 中国語出力でプロジェクトを作成
codexspec init my-project --lang zh-CN
```

**初期化後：**
```bash
# 現在の設定を表示
codexspec config

# 言語設定を変更
codexspec config --set-lang ja

# サポートされている言語を一覧表示
codexspec config --list-langs
```

### 設定ファイル

`.codexspec/config.yml` ファイルに言語設定が保存されます：

```yaml
version: "1.0"

language:
  # Claude のやり取りと生成ドキュメントの出力言語
  output: "ja"

  # テンプレート言語 - 互換性のため "en" を維持
  templates: "en"

project:
  ai: "claude"
  created: "2026-02-15"
```

### サポートされている言語

| コード | 言語 |
|--------|------|
| `en` | English（デフォルト） |
| `zh-CN` | 中文（简体） |
| `zh-TW` | 中文（繁體） |
| `ja` | 日本語 |
| `ko` | 한국어 |
| `es` | Español |
| `fr` | Français |
| `de` | Deutsch |
| `pt` | Português |
| `ru` | Русский |
| `it` | Italiano |
| `ar` | العربية |
| `hi` | हिन्दी |

### 仕組み

1. **単一の英語テンプレート**: すべてのコマンドテンプレートは英語のまま
2. **言語設定**: プロジェクトが出力言語の設定を指定
3. **動的翻訳**: Claude が英語の指示を読み、ターゲット言語で出力
4. **コンテキスト認識**: 技術用語（JWT、OAuth など）は必要に応じて英語のまま

### メリット

- **翻訳メンテナンス不要**: 複数のテンプレートバージョンを維持する必要がない
- **常に最新**: テンプレートの更新は自動的にすべての言語に反映
- **コンテキスト認識翻訳**: Claude が自然で状況に適した翻訳を提供
- **無制限の言語**: Claude がサポートする任意の言語が即座に利用可能

## 拡張システム

CodexSpec はカスタムコマンドを追加するためのプラグインアーキテクチャをサポートしています：

### 拡張の構造

```
my-extension/
├── extension.yml          # 拡張マニフェスト
├── commands/              # カスタムスラッシュコマンド
│   └── command.md
└── README.md
```

### 拡張の作成

1. `extensions/template/` からテンプレートをコピー
2. `extension.yml` を拡張の詳細で変更
3. `commands/` にカスタムコマンドを追加
4. ローカルでテストして公開

詳細は `extensions/EXTENSION-DEVELOPMENT-GUIDE.md` を参照してください。

## 開発

### 前提条件

- Python 3.11+
- uv パッケージマネージャー
- Git

### ローカル開発

```bash
# リポジトリをクローン
git clone https://github.com/Zts0hg/codexspec.git
cd codexspec

# 開発依存関係をインストール
uv sync --dev

# ローカルで実行
uv run codexspec --help

# テストを実行
uv run pytest

# コードをリント
uv run ruff check src/
```

### ビルド

```bash
# パッケージをビルド
uv build
```

## spec-kit との比較

CodexSpec は GitHub の spec-kit に触発されていますが、いくつかの重要な違いがあります：

| 機能 | spec-kit | CodexSpec |
|------|----------|-----------|
| コア思想 | スペック駆動開発 | スペック駆動開発 |
| CLI 名 | `specify` | `codexspec` |
| 主要 AI | マルチエージェントサポート | Claude Code に注力 |
| コマンドプレフィックス | `/speckit.*` | `/codexspec.*` |
| ワークフロー | specify → plan → tasks → implement | constitution → specify → generate-spec → plan → tasks → analyze → implement |
| 2段階スペック | なし | あり（明確化 + 生成） |
| レビューステップ | オプション | 組み込みレビューコマンド |
| Clarify コマンド | あり | あり |
| Analyze コマンド | あり | あり |
| Checklist コマンド | あり | あり |
| 拡張システム | あり | あり |
| PowerShell スクリプト | あり | あり |
| i18n サポート | なし | あり（LLM 翻訳で 13 以上の言語） |

## フィロソフィー

CodexSpec は以下の核心原則に従います：

1. **意図駆動開発**: スペックは「どう」の前に「何」を定義する
2. **リッチなスペック作成**: ガードレールと組織原則を使用
3. **マルチステップ洗練**: ワンショットのコード生成ではなく
4. **AI への高い依存**: スペック解釈に AI を活用
5. **レビュー指向**: 各アーティファクトを進める前に検証
6. **品質ファースト**: 要件品質のためのチェックリストと分析を内蔵

## 貢献

貢献を歓迎します！プルリクエストを提出する前に貢献ガイドラインをお読みください。

## ライセンス

MIT ライセンス - 詳細は [LICENSE](LICENSE) を参照。

## 謝辞

- [GitHub spec-kit](https://github.com/github/spec-kit) に触発
- [Claude Code](https://claude.ai/code) のために構築
