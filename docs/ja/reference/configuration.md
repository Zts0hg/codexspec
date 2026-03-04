# 設定

## 設定ファイルの場所

`.codexspec/config.yml`

## 設定スキーマ

```yaml
version: "1.0"

language:
  output: "en"      # ドキュメントの出力言語
  templates: "en"   # テンプレート言語 ("en" のままにしてください)

project:
  ai: "claude"      # AI アシスタント
  created: "2025-02-15"
```

## 言語設定

### `language.output`

Claude とのやり取りや生成されるドキュメントの言語です。

**サポートされている値:** [国際化](../user-guide/i18n.md#supported-languages)を参照

### `language.templates`

テンプレートの言語です。互換性のため `"en"` のままにしてください。

## プロジェクト設定

### `project.ai`

使用する AI アシスタントです。現在以下をサポートしています:

- `claude` (デフォルト)

### `project.created`

プロジェクトが初期化された日付です。
