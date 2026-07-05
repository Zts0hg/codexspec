# Konfiguration

## Speicherort der Konfigurationsdatei

`.codexspec/config.yml`

## Konfigurationsschema

```yaml
version: "1.0"

language:
  output: "zh-CN"        # Basissprache; die drei unten fallen darauf zurück, dann "en"
  interaction: "zh-CN"   # LLM-Dialog + codexspec CLI-Ausgabe (optional → Standardwert ist output)
  document: "en"         # Generierte Anforderungen/Spec/Plan/Tasks (optional → Standardwert ist output)
  commit: "en"           # Git-Commit-Nachrichten (optional → Standardwert ist output)
  templates: "en"        # Als "en" belassen

project:
  ai: "claude"
  created: "2025-02-15"

workflow:
  auto_next: false       # Automatisches Weiterschalten zwischen Workflow-Stufen (opt-in)
```

## Spracheinstellungen

CodexSpec unterteilt die Sprache in vier unabhängig konfigurierbare Dimensionen. `output` ist die Basis; `interaction`, `document` und `commit` überschreiben sie und fallen darauf (und dann auf `en`) zurück, wenn sie nicht gesetzt sind. So können Sie beispielsweise mit Claude in einer Sprache kommunizieren, während generierte Artefakte oder Commit-Nachrichten in einer anderen verbleiben.

| Dimension | Schlüssel | Bei init setzen | Später setzen | Steuert | Fällt zurück auf |
|-----------|-----------|-----------------|----------------|---------|-------------------|
| Output (Basis) | `output` | `--lang` | `config --set-lang` | Basis für die anderen drei | `en` |
| Interaction | `interaction` | `--interaction-lang` | `config --set-interaction-lang` | LLM-Dialog + CLI-Ausgabe | output → `en` |
| Document | `document` | `--document-lang` | `config --set-document-lang` | generierte Spec/Plan/Tasks | output → `en` |
| Commit | `commit` | `--commit-lang` | `config --set-commit-lang` | Git-Commit-Nachrichten | output → `en` |
| Templates | `templates` | — | — | Quelle der Befehlsvorlagen (immer `en`) | — |

**Unterstützte Werte:** Siehe [Internationalisierung](../user-guide/i18n.md#unterstuetzte-sprachen)

### `language.output`

Die Basis-Ausgabesprache. Die anderen Dimensionen fallen darauf zurück, wenn sie nicht explizit gesetzt sind.

### `language.interaction`

Sprache für die Konversation zwischen Ihnen und dem LLM sowie für die Terminal-Ausgabe der `codexspec` CLI. Optional – Standardwert ist `output`.

### `language.document`

Sprache für generierte Artefaktdateien (Anforderungen/Spec/Plan/Tasks). Optional – Standardwert ist `output`.

### `language.commit`

Sprache für Git-Commit-Nachrichten. Optional – Standardwert ist `output`.

### `language.templates`

Vorlagensprache. Sollte aus Kompatibilitätsgründen als `"en"` belassen werden.

## Projekteinstellungen

### `project.ai`

Der verwendete AI-Assistent. Steuert, welche Agent-Kontextdateien `codexspec init` ablegt:

- `claude` (Standard) – schreibt `CLAUDE.md` (und `.claude/commands/`).
- `codex` – schreibt stattdessen `AGENTS.md` und `.agents/skills/`.
- `both` – schreibt alles Obige, sodass das Projekt für Claude Code und Codex CLI bereit ist.

`CLAUDE.md` wird immer erstellt (damit das Projekt aus Claude Code nutzbar bleibt); `AGENTS.md` und `.agents/skills/` werden nur erstellt, wenn `project.ai` auf `codex` oder `both` steht.

### `project.created`

Datum, an dem das Projekt initialisiert wurde.

## Workflow-Einstellungen

### `workflow.auto_next`

Steuert, ob die Requirements-First-SDD-Pipeline nach Bestehen der aktuellen Stufe **automatisch zur nächsten Workflow-Stufe weiterschaltet**, anstatt dass Sie den nächsten Befehl manuell anstoßen müssen.

- **Standard:** `false` (opt-in). Nur der literale Wert `true` aktiviert das Weiterschalten.
- **Umschalten / setzen mit:** `codexspec config --auto-next` (bare Flag schaltet den aktuellen Wert um; `on`/`off` übergeben, um ihn explizit zu setzen).

**Kette:**

```
specify → generate-spec → spec-to-plan → plan-to-tasks → implement-tasks
```

**Pass-Gate:**

- `generate-spec`, `spec-to-plan`, `plan-to-tasks`: die eingebaute Review-Schleife des Befehls muss einen Overall-Status von `PASS` oder `PASS_WITH_WARNINGS` melden.
- `specify`: es gibt keine Review-Schleife, deshalb ist das Gate Ihre ausdrückliche Bestätigung, dass die Anforderungs-Erkundung abgeschlossen ist (die **finale** Stufenzusammenfassung, nicht jede intermediate).
- `implement-tasks`: terminale Stufe – danach wird nichts automatisch ausgelöst.

Wenn die Review-Schleife `NEEDS_REVISION` oder `BLOCKED` meldet, hält die Kette an und die Kontrolle geht an Sie zurück. Vor jedem Weiterschalten gibt der Agent eine Notice-Zeile aus (zum Beispiel: `auto_next: review passed → invoking /codexspec:spec-to-plan`).
