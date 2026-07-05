# 設定

## 設定ファイルの場所

`.codexspec/config.yml`

## 設定スキーマ

```yaml
version: "1.0"

language:
  output: "zh-CN"        # ベース言語。以下の 3 つはここにフォールバックし、さらに "en" にフォールバック
  interaction: "zh-CN"   # LLM の対話 + codexspec CLI の出力 (任意 → デフォルトは output)
  document: "en"         # 生成される requirements/spec/plan/tasks (任意 → デフォルトは output)
  commit: "en"           # git コミットメッセージ (任意 → デフォルトは output)
  templates: "en"        # "en" のまま保持

project:
  ai: "claude"
  created: "2025-02-15"

workflow:
  auto_next: false       # ワークフローステージ間の自動進行 (オプトイン)
```

## 言語設定

CodexSpec は言語を、個別に設定可能な 4 つの次元に分割します。`output` がベースであり、`interaction`・`document`・`commit` は output を上書きしつつ、未設定時は output (さらに `en`) にフォールバックします。これにより、たとえば Claude との対話はある言語で行いながら、生成される成果物やコミットメッセージを別の言語に保つ、といったことができます。

| 次元 | キー | init で設定 | 後から設定 | 制御する対象 | フォールバック先 |
|-----------|-----|-------------|-----------|----------|---------------|
| 出力 (ベース) | `output` | `--lang` | `config --set-lang` | 他の 3 つのベース | `en` |
| 対話 | `interaction` | `--interaction-lang` | `config --set-interaction-lang` | LLM の対話 + CLI 出力 | output → `en` |
| ドキュメント | `document` | `--document-lang` | `config --set-document-lang` | 生成される spec/plan/tasks | output → `en` |
| コミット | `commit` | `--commit-lang` | `config --set-commit-lang` | git コミットメッセージ | output → `en` |
| テンプレート | `templates` | — | — | コマンドテンプレートのソース (常に `en`) | — |

**サポートされる値:** [国際化](../user-guide/i18n.md#supported-languages) を参照

### `language.output`

ベースとなる出力言語です。他の次元が明示的に設定されていない場合は、ここにフォールバックします。

### `language.interaction`

あなたと LLM との対話、および `codexspec` CLI のターミナル出力の言語です。任意で、デフォルトは `output` です。

### `language.document`

生成される成果物ファイル (requirements/spec/plan/tasks) の言語です。任意で、デフォルトは `output` です。

### `language.commit`

git コミットメッセージの言語です。任意で、デフォルトは `output` です。

### `language.templates`

テンプレートの言語です。互換性のため `"en"` のままにしてください。

## プロジェクト設定

### `project.ai`

使用する AI アシスタントです。`codexspec init` がどのエージェントコンテキストファイルを書き出すかを制御します。

- `claude` (デフォルト) ― `CLAUDE.md` (および `.claude/commands/`) を書き出し。
- `codex` ― 代わりに `AGENTS.md` と `.agents/skills/` を書き出し。
- `both` ― 上記すべてを書き出し、プロジェクトを Claude Code と Codex CLI の両方で使えるようにします。

`CLAUDE.md` は常に作成されます (プロジェクトが Claude Code からも使えるようにするため)。`AGENTS.md` と `.agents/skills/` は `project.ai` が `codex` または `both` の場合にのみ作成されます。

### `project.created`

プロジェクトを初期化した日付です。

## ワークフロー設定

### `workflow.auto_next`

現在のステージがパスした後に、Requirements-First SDD パイプラインが次のステージへ **自動的に進む** か、手動で次のコマンドをトリガーする必要があるかを制御します。

- **デフォルト:** `false` (オプトイン)。リテラル値 `true` のみが自動進行を有効にします。
- **切り替え / 設定:** `codexspec config --auto-next` (フラグ単独で現在値をトグル。`on`/`off` を渡して明示的に設定も可)。

**チェーン:**

```
specify → generate-spec → spec-to-plan → plan-to-tasks → implement-tasks
```

**パスの条件:**

- `generate-spec`, `spec-to-plan`, `plan-to-tasks`: コマンド組み込みのレビューループが Overall Status `PASS` または `PASS_WITH_WARNINGS` を報告すること。
- `specify`: レビューループはないため、要件の発見が完了したことの明示的な確認 (各中間サマリではなく**最終**ステージサマリでの確認) がゲートになります。
- `implement-tasks`: 終端ステージであり、後に自動で発火するものはありません。

レビューループが `NEEDS_REVISION` または `BLOCKED` を報告した場合、チェーンは止まり、あなたに制御が戻ります。各進行の前に、エージェントは 1 行の通知を出します (例: `auto_next: review passed → invoking /codexspec:spec-to-plan`)。
