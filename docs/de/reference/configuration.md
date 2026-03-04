# Konfiguration

## Speicherort der Konfigurationsdatei

`.codexspec/config.yml`

## Konfigurationsschema

```yaml
version: "1.0"

language:
  output: "en"      # Ausgabesprache fuer Dokumente
  templates: "en"   # Vorlagensprache (als "en" belassen)

project:
  ai: "claude"      # KI-Assistent
  created: "2025-02-15"
```

## Spracheinstellungen

### `language.output`

Die Sprache fuer Claude-Interaktionen und generierte Dokumente.

**Unterstuetzte Werte:** Siehe [Internationalisierung](../user-guide/i18n.md#supported-languages)

### `language.templates`

Vorlagensprache. Sollte als `"en"` belassen werden, um die Kompatibilitaet zu gewaehrleisten.

## Projekteinstellungen

### `project.ai`

Der verwendete KI-Assistent. Derzeit unterstuetzt:

- `claude` (Standard)

### `project.created`

Datum, an dem das Projekt initialisiert wurde.
