# 設定

## 設定ファイルの場所

`.codexspec/config.yml`

## 設定スキーマ

```yaml
version: "1.0"

language:
  output: "zh-CN"        # ベース言語。以下 3 つはこれに (次いで "en") フォールバック
  interaction: "zh-CN"   # LLM との対話 + codexspec CLI 出力 (省略可 → デフォルトは output)
  document: "en"         # 生成される requirements/spec/plan/tasks (省略可 → デフォルトは output)
  commit: "en"           # git コミットメッセージ (省略可 → デフォルトは output)
  templates: "en"        # テンプレート言語 ("en" のまま)

project:
  ai: "claude"      # AI アシスタント
  created: "2025-02-15"
```

## 言語設定

CodexSpec は言語を独立に設定可能な 4 つの次元に分割しています。`output` がベースであり、`interaction`、`document`、`commit` はこれを上書きし、未設定時はこれに (次いで `en`) フォールバックします。これにより例えば、ある言語で Claude と対話しながら、生成されるアーティファクトやコミットメッセージは別の言語に保つ、といった運用が可能です。

| 次元 | `config.yml` キー | init で設定 | 後から設定 | 制御対象 | フォールバック先 |
|-----------|------------------|-------------|-----------|----------|---------------|
| Output (ベース) | `output` | `--lang` | `config --set-lang` | 他 3 つのベース | `en` |
| Interaction | `interaction` | `--interaction-lang` | `config --set-interaction-lang` | LLM との対話 + CLI 出力 | output → `en` |
| Document | `document` | `--document-lang` | `config --set-document-lang` | 生成される spec/plan/tasks | output → `en` |
| Commit | `commit` | `--commit-lang` | `config --set-commit-lang` | git コミットメッセージ | output → `en` |
| Templates | `templates` | — | — | コマンドテンプレートのソース (常に `en`) | — |

**サポートされている値:** [国際化](../user-guide/i18n.md#supported-languages)を参照

### `language.output`

ベースとなる出力言語です。他の次元が明示的に設定されていない場合、これにフォールバックします。

### `language.interaction`

あなたと LLM との対話、および `codexspec` CLI の端末出力の言語です。省略可能で、デフォルトは `output` です。

### `language.document`

生成されるアーティファクトファイル (requirements/spec/plan/tasks) の言語です。省略可能で、デフォルトは `output` です。

### `language.commit`

git コミットメッセージの言語です。省略可能で、デフォルトは `output` です。

### `language.templates`

テンプレートの言語です。互換性のため `"en"` のままにしてください。

## プロジェクト設定

### `project.ai`

使用する AI アシスタントです。現在以下をサポートしています:

- `claude` (デフォルト)

### `project.created`

プロジェクトが初期化された日付です。
