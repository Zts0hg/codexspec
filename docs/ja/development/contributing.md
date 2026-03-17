# コントリビューション

## 前提条件

- Python 3.11+
- uv パッケージマネージャー
- Git

## ローカル開発

```bash
# リポジトリをクローン
git clone https://github.com/Zts0hg/codexspec:git
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

## ドキュメント

```bash
# ドキュメント依存関係をインストール
uv sync --extra docs

# ドキュメントをローカルでプレビュー
uv run mkdocs serve

# ドキュメントをビルド
uv run mkdocs build
```

## ビルド

```bash
uv build
```

## プルリクエストのプロセス

1. リポジトリをフォークする
2. フィーチャーブランチを作成する
3. 変更を加える
4. テストとリントを実行する
5. プルリクエストを送信する

## コードスタイル

- 行の長さ: 最大 120 文字
- PEP 8 に従う
- パブリック関数には型ヒントを使用する
