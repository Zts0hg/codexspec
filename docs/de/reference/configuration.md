# Konfiguration

## Speicherort der Konfigurationsdatei

`.codexspec/config.yml`

## Konfigurationsschema

```yaml
version: "1.0"

language:
  output: "zh-CN"        # Basissprache; die drei unten fall darauf zurueck, dann "en"
  interaction: "zh-CN"   # LLM-Dialog + codexspec CLI-Ausgabe (optional → Standardwert ist output)
  document: "en"         # Generierte Anforderungen/Spec/Plan/Tasks (optional → Standardwert ist output)
  commit: "en"           # Git-Commit-Nachrichten (optional → Standardwert ist output)
  templates: "en"        # Vorlagensprache (als "en" belassen)

project:
  ai: "claude"      # KI-Assistent
  created: "2025-02-15"
```

## Spracheinstellungen

CodexSpec unterteilt die Sprache in vier unabhaengig konfigurierbare Dimensionen. `output` ist die Basis; `interaction`, `document` und `commit` ueberschreiben sie und fallen darauf (und dann auf `en`) zurueck, wenn sie nicht gesetzt sind. So koennen Sie beispielsweise mit Claude in einer Sprache kommunizieren, waehrend generierte Artefakte oder Commit-Nachrichten in einer anderen verbleiben.

| Dimension | Schluessel | Bei init setzen | Spaeter setzen | Steuert | Faellt zurueck auf |
|-----------|------------|-----------------|----------------|---------|-------------------|
| Output (Basis) | `output` | `--lang` | `config --set-lang` | Basis fuer die anderen drei | `en` |
| Interaction | `interaction` | `--interaction-lang` | `config --set-interaction-lang` | LLM-Dialog + CLI-Ausgabe | output → `en` |
| Document | `document` | `--document-lang` | `config --set-document-lang` | generierte Spec/Plan/Tasks | output → `en` |
| Commit | `commit` | `--commit-lang` | `config --set-commit-lang` | Git-Commit-Nachrichten | output → `en` |
| Templates | `templates` | — | — | Quelle der Befehlsvorlagen (immer `en`) | — |

**Unterstuetzte Werte:** Siehe [Internationalisierung](../user-guide/i18n.md#supported-languages)

### `language.output`

Die Basis-Ausgabesprache. Die anderen Dimensionen fallen darauf zurueck, wenn sie nicht explizit gesetzt sind.

### `language.interaction`

Sprache fuer die Konversation zwischen Ihnen und dem LLM sowie fuer die Terminal-Ausgabe der `codexspec` CLI. Optional — Standardwert ist `output`.

### `language.document`

Sprache fuer generierte Artefaktdateien (Anforderungen/Spec/Plan/Tasks). Optional — Standardwert ist `output`.

### `language.commit`

Sprache fuer Git-Commit-Nachrichten. Optional — Standardwert ist `output`.

### `language.templates`

Vorlagensprache. Sollte aus Kompatibilitaetsgruenden als `"en"` belassen werden.

## Projekteinstellungen

### `project.ai`

Der verwendete KI-Assistent. Derzeit unterstuetzt:

- `claude` (Standard)

### `project.created`

Datum, an dem das Projekt initialisiert wurde.
