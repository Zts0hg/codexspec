# インストール

## 前提条件

- Python 3.11+
- [uv](https://docs.astral.sh/uv/)（推奨）またはpip

## オプション1: uvでインストール（推奨）

CodexSpecをインストールする最も簡単な方法はuvを使用することです：

```bash
uv tool install codexspec
```

## オプション2: pipでインストール

または、pipを使用することもできます：

```bash
pip install codexspec
```

## オプション3: 一時的な使用

インストールせずに直接実行：

```bash
# 新しいプロジェクトを作成
uvx codexspec init my-project

# 既存のプロジェクトで初期化
cd your-existing-project
uvx codexspec init . --ai claude
```

## オプション4: GitHubからインストール

最新の開発版の場合：

```bash
# uvを使用
uv tool install git+https://github.com/Zts0hg/codexspec:git

# pipを使用
pip install git+https://github.com/Zts0hg/codexspec:git

# 特定のブランチまたはタグ
uv tool install git+https://github.com/Zts0hg/codexspec:git@main
uv tool install git+https://github.com/Zts0hg/codexspec:git@v0.2.0
```

## インストールの確認

```bash
codexspec --help
codexspec version
```

## アップグレード

```bash
# uvを使用
uv tool install codexspec --upgrade

# pipを使用
pip install --upgrade codexspec
```

## 次のステップ

[クイックスタート](quick-start.md)
