# CodexSpec

![CodexSpec](assets/images/codexspec-logo-light.svg#only-light){ width="420" }

![CodexSpec](assets/images/codexspec-logo-dark.svg#only-dark){ width="420" }

**Ein Toolkit für Requirements-First SDD mit Claude Code und OpenAI Codex**

CodexSpec erstellt aus bestätigten Anforderungen Spezifikationen, Entwürfe, Pläne,
Aufgaben und Implementierungen, die sich auf ihre Quellen zurückführen lassen.
Sie entscheiden, **was** entwickelt werden soll und **warum**. Der Agent erarbeitet
innerhalb dieser bestätigten Anforderungen das **Wie** und nutzt dabei
Review-Prüfpunkte und dauerhaft gespeichertes Projektwissen.

Nutzen Sie CodexSpec mit den Slash-Befehlen von Claude Code, mit Codex-Skills oder
mit beiden. Für reguläre Features werden standardmäßig separate Git-Worktrees
verwendet. Mit einem optionalen gemeinsamen Blueprint kann der Agent eine Liste
bestätigter Anforderungen autonom abarbeiten.

<a id="why-choose-codexspec"></a>

## Warum CodexSpec?

| Bedarf | Was CodexSpec bietet |
|------|-------------------------|
| Klarer Zweck des Produkts | Explizite Bestätigung und dauerhaft gespeicherte Anforderungen in `requirements.md` vor der Spezifikation |
| Nachvollziehbare Entwicklung | Quellenverweise entlang der Kette Anforderungen → Spezifikation → Entwurf → Plan → Aufgaben |
| Überprüfbare Entscheidungen | Vier Befehle zur Prüfung von Artefakten, eine artefaktübergreifende Analyse und eine separate Codeprüfung, bei der Fehler die Freigabe verhindern |
| Kontinuität zwischen Sitzungen und im Team | Feature-Aufzeichnungen, Projektprinzipien, wiederverwendbares Wissen und relevante frühere Entscheidungen |
| Mehrere Features gleichzeitig | Ein Git-Worktree pro regulärem Feature; der zugehörige Arbeitsbereich wird zuverlässig wiederverwendet |
| Mehr Automatisierung | Optionaler automatischer Übergang zwischen Phasen und autonome Entwicklung bestätigter Blueprint-Anforderungen |
| Sprachpräferenzen im Team | Unabhängig wählbare Sprachen für Interaktion, Dokumente und Commits |

<a id="what-is-requirements-first-sdd"></a>

### Was ist Requirements-First SDD?

Bei Requirements-First Spec-Driven Development sind **bestätigte Anforderungen
für ein Feature die maßgebliche Grundlage mit der höchsten Priorität**. Bevor der
Agent daraus Implementierungsartefakte ableitet, hält er Ziele, Einschränkungen,
Entscheidungen, Ausschlüsse, offene Fragen und die Belege für die Bestätigung fest.

```text
Idea → Confirmed Requirements →     Spec    →     Design    →     Plan    →    Tasks     →     Code
                 ↓                   ↓              ↓              ↓             ↓              ↓
         User confirmation      review-spec   review-design   review-plan   review-tasks   review-code
```

Sie bestätigen die Anforderungen. Jedes daraus abgeleitete Artefakt wird eigens
geprüft – von der Spezifikation bis zum Code.

In der Zusammenarbeit mit Menschen wird festgelegt und geändert, was das Produkt
leisten soll. Automatische Reviews prüfen die abgeleiteten Artefakte anhand dieser
Vorgaben. Wird die Automatisierung aktiviert, setzt sie die Arbeit nach erfolgreich
geprüften Phasen fort. Sie berechtigt den Agenten nicht, bestätigte Anforderungen
stillschweigend zu ersetzen.

[![CodexSpec: anforderungsorientierte Entwicklung, Reviews je Phase und Wiederverwendung von Erfahrungen](../../assets/workflow/workflow-de-light.png#only-light)](../../assets/workflow/workflow-de-light.png#only-light)

[![CodexSpec: anforderungsorientierte Entwicklung, Reviews je Phase und Wiederverwendung von Erfahrungen](../../assets/workflow/workflow-de-dark.png#only-dark)](../../assets/workflow/workflow-de-dark.png#only-dark)

Diagramm in voller Größe öffnen: [☀️](../../assets/workflow/workflow-de-light.png) · [🌙](../../assets/workflow/workflow-de-dark.png)

<a id="30-second-quick-start"></a>

## Schnellstart in 30 Sekunden

Installieren Sie CodexSpec und initialisieren Sie das Projekt für den Assistenten,
den Sie verwenden:

```bash
uv tool install codexspec

# Create a new project for Claude Code
codexspec init my-project --ai claude

# Or initialize an existing project for Codex
cd your-existing-project
codexspec init . --ai codex

# Use --ai both when you want both integrations
```

Starten Sie den installierten Assistenten im initialisierten Projekt. Je nach
Assistent wird derselbe Workflow auf eine der folgenden Arten aufgerufen:

| Assistent | Anforderungsermittlung starten |
|-----------|------------------------------|
| Claude Code (`claude`) | `/codexspec:specify I want to build a todo application` |
| Codex (`codex`) | `$codexspec:specify I want to build a todo application` |

Passen Sie die Projektprinzipien bei Bedarf mit `constitution` an. Bestätigen Sie
die abschließende Zusammenfassung der Anforderungen. Arbeiten Sie anschließend
im zurückgegebenen Feature-Verzeichnis und Arbeitsbereich weiter. Die weiteren
Befehle finden Sie unter [Kern-Workflow](user-guide/workflow.md#core-workflow).

Wenn Sie die Codex-Desktop-App verwenden, können Sie [Codex mit der Installation und Initialisierung Ihres Projekts beauftragen](getting-started/installation.md#install-with-the-codex-desktop-app).
