<a id="configuration-and-internationalization"></a>

# 設定と国際化

設定は `.codexspec/config.yml` に保存します。テンプレートは英語のままですが、
エージェントは設定された言語で対話文と成果物を作成します。
標準の言語コードは 13 個です：`en`、`zh-CN`、`zh-TW`、`ja`、`ko`、`es`、`fr`、`de`、`pt`、`ru`、`it`、`ar`、`hi`。
ポルトガル語の CLI コードは `pt` で、ローカライズされたドキュメントと翻訳カタログでは `pt-BR` を使います。

<a id="language-dimensions"></a>

## 言語の個別設定

| 区分 | 設定キー | 初期化時 | 後から設定 | 対象 |
|-----------|------------|-------------------|-----------|----------|
| 出力・基本言語 | `language.output` | `--lang` | `config --set-lang` | 他の言語設定で指定がない場合の基本言語 |
| 対話 | `language.interaction` | `--interaction-lang` | `config --set-interaction-lang` | 会話と CLI 出力 |
| ドキュメント | `language.document` | `--document-lang` | `config --set-document-lang` | 要件、仕様書、設計、計画、タスク |
| コミット | `language.commit` | `--commit-lang` | `config --set-commit-lang` | コミットメッセージと Git ワークフローで生成する文章 |

各言語設定は、それぞれ独立して `language.output`、次に `en` の順でフォールバックします。
`language.templates` は `en` のままです。

```bash
codexspec init my-project --ai both \
  --interaction-lang zh-CN --document-lang en --commit-lang en

codexspec config
codexspec config --set-document-lang en
codexspec config --list-langs
```

初回の TTY 初期化では、`--lang` または 3 つすべての個別言語オプションを指定していなければ、基本言語の選択を求めます。
`--force` は他の初期化時の確認を自動で承認しますが、この言語選択は省略しません。
非 TTY での初期化では、デフォルトで英語を使います。再初期化時も、明示的に設定していない言語キーは保持されます。

<a id="workflow-and-review-settings"></a>

## ワークフローとレビューの設定

| 設定 | デフォルト | 動作 | CLI 操作 |
|---------|---------|--------|-------------|
| `workflow.auto_next` | `false` | 合格した通常の SDD ステージから次へ進む | `config --auto-next on\|off` |
| `workflow.auto_distill` | `true` | 完了処理の成功後、人との対話なしに知識を抽出 | `config --auto-distill on\|off` |
| `workflow.auto_maintenance` | `true` | 自動修正時に、検証済みの保守改善を段階的に適用 | `config --auto-maintenance on\|off` |
| `workflow.worktrees` | `true` | 通常の機能と独立した保守作業を別の worktree に分離 | `config --worktrees on\|off` |
| `review.decided_by` | `reviewer` | プロジェクトの運用範囲外で発生する指摘について、判断する人を指定 | `config --decided-by reviewer\|ask` |

真偽値を取る CLI スイッチは、大文字・小文字を区別せず、`on/true/1/yes` と `off/false/0/no` を受け付けます。前後の空白も許容されます。
値を指定せずに使うと、書き込み先チェックアウトの現在値を切り替えます。YAML には真偽値として保存します。

`review.decided_by: reviewer` では、レビュアーが欠陥として認定するかを判断します。
`ask` では、運用範囲外の発生条件を、ユーザーの判断待ちのシナリオとして扱います。
ユーザーは修正するか、そのシナリオを除外するかを一度決め、確認済みの判断は後続のラウンドでも使えるよう保存されます。
判断待ちの項目がある間は完了できません。1 回の `review-code` 実行に限り、`--decided-by` で設定済みのモードを上書きできます。

設定の書き込みも worktree の作業先選択に従います。
main チェックアウトから独立した変更を行う場合は、保守用 worktree に書き込み、main で有効な設定は直ちには変わりません。
機能 worktree 内での変更は、その場所で有効になります。

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

<details>
<summary>設定例</summary>

```yaml
version: "1.0"

language:
  output: "en"
  interaction: "zh-CN"
  document: "en"
  commit: "en"
  templates: "en"

project:
  ai: "both"

workflow:
  auto_next: false
  auto_distill: true
  auto_maintenance: true
  worktrees: true

review:
  decided_by: reviewer
```

</details>

言語と設定の詳しい動作は、[設定](configuration.md)と[国際化](../user-guide/i18n.md)を参照してください。
