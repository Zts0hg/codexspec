# CLI リファレンス

<a id="cli-commands"></a>

## CLI コマンド

| コマンド | 目的 |
|---------|---------|
| `codexspec init` | Claude、Codex、または両方に合わせてプロジェクトを初期化・更新 |
| `codexspec check` | インストール済みのツールと依存関係を確認 |
| `codexspec version` | バージョンとシステム情報を表示 |
| `codexspec config` | プロジェクト設定を表示・変更 |
| `codexspec list-commands` | 利用可能なエージェントコマンドをカテゴリ別に表示 |
| `codexspec show-blueprint` | 共有 worktree のブループリントを変更せずに出力 |

<a id="cli-installation"></a>

## CLI のインストール

```bash
uv tool install codexspec

# Or use pip
pip install codexspec

# Verify the CLI and inspect available commands
codexspec version
codexspec --help
codexspec list-commands
```

新しいプロジェクトは `codexspec init my-project --ai claude`、現在のディレクトリは
`codexspec init . --ai codex` で初期化します。両方の連携を使う場合は `--ai both` を指定してください。
アシスタントのデフォルトは `claude` です。Codex または両方を使う場合は、値を明示的に指定します。

<details>
<summary>その他のインストール方法</summary>

<a id="one-time-initialization"></a>

### 一度だけ実行する初期化

```bash
uvx codexspec init my-project --ai claude
uvx codexspec init . --ai codex
```

この方法では、プロジェクトコマンドと単独で動作するコミット実行環境がインストールされます。
worktree の作業先選択、blueprint/auto-dev、手動のプロファイルレビューは引き続き CodexSpec CLI を呼び出すため、
これらのワークフローを使う場合は CLI も利用できるようにしておいてください。

<a id="development-versions"></a>

### 開発版

```bash
uv tool install git+https://github.com/Zts0hg/codexspec.git
uv tool install git+https://github.com/Zts0hg/codexspec.git@main

# Replace <tag> with the version you want
uv tool install git+https://github.com/Zts0hg/codexspec.git@<tag>
```

</details>

<details>
<summary>Windows でのインストール</summary>

PowerShell で実行します。

```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
# Restart PowerShell, then:
uv tool install codexspec
codexspec version
```

PATH やインストールに関する問題への対処は、[Windows トラブルシューティングガイド](../WINDOWS-TROUBLESHOOTING.md)を参照してください。

</details>

<a id="upgrade-and-refresh-a-project"></a>

## アップグレードとプロジェクトの更新

CLI の更新と、プロジェクトにインストール済みのコマンドの更新は、それぞれ別に行います。

```bash
uv tool install codexspec --upgrade
# Or: pip install --upgrade codexspec

# In the project you want to refresh; select its desired integration(s)
codexspec init . --force --ai both
```

片方の連携だけが必要な場合は、`--ai claude` または `--ai codex` を指定してください。
`--force` は配布コマンドとスクリプトを再生成し、レビューリソースを更新します。
移行、コマンド更新、プロジェクト憲法への準拠に関する確認も自動で承認します。
既存の要件とプロジェクト原則は維持されます。コンテキストファイルも既存の本文を残したまま、管理対象のガイダンスだけを更新します。
明示的に設定していない設定キーは、そのまま保持されます。

計画作成には `design-to-plan` を使います。インストールの更新時に旧 `spec-to-plan` エントリは廃止され、エイリアスも残りません。

<details>
<summary>CLI 初期化オプション</summary>

| オプション | 意味 |
|--------|---------|
| `PROJECT_NAME` | 新しいディレクトリの名前。現在のディレクトリには `.` を使用 |
| `--here`, `-h` | 現在のディレクトリを初期化 |
| `--ai`, `-a` | `claude`、`codex`、`both` から選択。デフォルトは `claude` |
| `--lang`, `-l` | 基本となる出力言語を設定 |
| `--interaction-lang` | 対話言語を設定 |
| `--document-lang` | ドキュメント言語を設定 |
| `--commit-lang` | コミットメッセージの言語を設定 |
| `--force`, `-f` | インストール済み成果物を再生成し、移行・更新・準拠に関する確認を自動承認。プロジェクトで作成したコンテキストと、指定に関係のない設定は保持 |
| `--no-git` | Git リポジトリの初期化を省略 |
| `--debug`, `-d` | 詳細なデバッグ情報を表示 |

</details>

<details>
<summary>CLI 設定オプション</summary>

| オプション | 意味 |
|--------|---------|
| `--set-lang`, `-l` | 基本となる出力言語を設定 |
| `--set-interaction-lang` | 対話言語を設定 |
| `--set-document-lang` | ドキュメント言語を設定 |
| `--set-commit-lang`, `-c` | コミットメッセージの言語を設定 |
| `--list-langs` | サポートする言語コードを一覧表示 |
| `--auto-next` | ステージの自動進行を切り替え・設定 |
| `--auto-distill` | 知識の自動抽出を切り替え・設定 |
| `--auto-maintenance` | 段階的な保守改善の自動適用を切り替え・設定 |
| `--worktrees` | チェックアウトごとの worktree 分離を切り替え・設定 |
| `--decided-by` | レビューの判断モードを `reviewer` または `ask` に設定 |

</details>

## `codexspec show-blueprint`

固定ブランチ `codexspec/auto-dev` と `worktree-for-codexspec-auto-dev` にある完全な
`.codexspec/blueprint.md` を標準出力へそのまま表示します。リポジトリ、ブランチ、worktree、
またはファイルがない場合は標準エラーへ診断を出力し、ゼロ以外で終了します。読み取り専用で、
fetch、merge、書き込み、ロックは実行しません。

```bash
codexspec show-blueprint
```
