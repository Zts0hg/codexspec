# Configuration

## Config File Location

`.codexspec/config.yml`

## Configuration Schema

```yaml
version: "1.0"

language:
  output: "en"      # Output language for documents
  templates: "en"   # Template language (keep as "en")

project:
  ai: "claude"      # AI assistant
  created: "2025-02-15"
```

## Language Settings

### `language.output`

The language for Claude interactions and generated documents.

**Supported values:** See [Internationalization](../user-guide/i18n.md#supported-languages)

### `language.templates`

Template language. Should remain as `"en"` for compatibility.

## Project Settings

### `project.ai`

The AI assistant being used. Currently supports:

- `claude` (default)

### `project.created`

Date when the project was initialized.
