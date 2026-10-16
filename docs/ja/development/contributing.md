# コントリビューション

## 前提条件

- Python 3.11+
- uv パッケージマネージャ
- Git

## ローカル開発

```bash
# Clone the repository
git clone https://github.com/Zts0hg/codexspec.git
cd codexspec

# Install development dependencies
uv sync --extra dev

# Run locally
uv run codexspec --help

# Run tests
uv run pytest

# Lint code
uv run ruff check src/
```

## ドキュメント

```bash
# Install docs dependencies
uv sync --extra dev --extra docs

# Preview documentation locally
uv run mkdocs serve

# Build documentation
uv run mkdocs build --strict
```

## ビルド

```bash
uv build
```

## プルリクエストのプロセス

1. リポジトリをフォーク
2. 機能ブランチを作成
3. 変更を加える
4. テストとリントを実行
5. プルリクエストを提出

## コードスタイル

- 行の長さ: 最大 120 文字
- PEP 8 に従う
- 公開関数には型ヒントを使用

テンプレート、パッケージング、初期化を変更する前に、[CLAUDE.md](https://github.com/Zts0hg/codexspec/blob/main/CLAUDE.md)、[AGENTS.md](https://github.com/Zts0hg/codexspec/blob/main/AGENTS.md)、
[リポジトリ構成](https://github.com/Zts0hg/codexspec/blob/main/docs/internal/repository-layout.md)を読んでください。
配布コマンドとスキルのコピーは、自動生成されたインストール成果物です。正規のソースを編集し、再生成してください。
