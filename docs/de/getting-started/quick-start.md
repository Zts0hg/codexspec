# Schnellstart

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
Befehle finden Sie unter [Kern-Workflow](../user-guide/workflow.md#core-workflow).

Wenn Sie die Codex-Desktop-App verwenden, können Sie [Codex mit der Installation und Initialisierung Ihres Projekts beauftragen](installation.md#install-with-the-codex-desktop-app).

<a id="core-workflow"></a>

## Kern-Workflow

Der Standard-Workflow für Features bewahrt eine durch Quellenverweise verknüpfte Kette:

```text
/specify          → requirements.md
/generate-spec    → spec.md       → review-spec
/spec-to-design   → design.md     → review-design
/design-to-plan   → plan.md       → review-plan
/plan-to-tasks    → tasks.md      → review-tasks → analyze
/implement-tasks  → implementation and complete-feature code review
```

Die folgenden Beispiele verwenden Claudes Präfix `/codexspec:`. Verwenden Sie in
Codex `$codexspec:` mit demselben Befehlsnamen und denselben Argumenten.

| Schritt | Befehl | Zweck und Ergebnis |
|------|---------|--------------------|
| Projektprinzipien | `/codexspec:constitution` | `constitution.md` erstellen oder aktualisieren und betroffene Artefakte validieren |
| Anforderungen | `/codexspec:specify <idea>` | Zielsetzung besprechen, die abschließende Zusammenfassung bestätigen und `requirements.md` dauerhaft speichern |
| Spezifikation | `/codexspec:generate-spec <feature-dir>` | Bestätigte Anforderungen mit Quellenverweisen in `spec.md` überführen |
| Systementwurf | `/codexspec:spec-to-design <feature-dir>` | `design.md` mit Komponenten, Schnittstellen und wesentlichen Entwurfsentscheidungen erstellen |
| Implementierungsplan | `/codexspec:design-to-plan <feature-dir>` | `plan.md` mit Phasen, Reihenfolge und Verifikation erstellen |
| Aufgaben | `/codexspec:plan-to-tasks <feature-dir>` | Nachvollziehbare, überprüfbare Aufgaben in `tasks.md` erstellen und die artefaktübergreifende Analyse ausführen |
| Implementierung | `/codexspec:implement-tasks <feature-dir>` | Aufgaben ausführen, Ergebnisse verifizieren und unabhängig bestätigte Review-Befunde beheben |

Ersetzen Sie `<feature-dir>` durch das Feature-Verzeichnis, das bei der
Anforderungsermittlung zurückgegeben wurde. Arbeiten Sie in dessen Worktree
weiter oder geben Sie seinen expliziten Pfad an. So beziehen sich alle Befehle
und Sitzungen weiterhin auf dasselbe Feature.

<a id="specify-clarify-and-analyze"></a>

### specify, clarify und analyze

- **specify** beginnt die Anforderungsermittlung oder nimmt sie wieder auf. Erst
  die explizite Bestätigung macht die Zusammenfassung der Anforderungen verbindlich.
- **clarify** klärt Mehrdeutigkeiten in vorhandenen Anforderungen und der
  Spezifikation. Pro Aufruf werden bis zu fünf Fragen aus vier Kategorien gestellt.
  Zuerst wird `requirements.md` aktualisiert, anschließend `spec.md` synchronisiert.
- **analyze** prüft die gesamte Kette Anforderungen → Spezifikation → Entwurf →
  Plan → Aufgaben. Es korrigiert nachgelagerte Artefakte automatisch, wenn sich
  die Korrektur eindeutig aus den maßgeblichen vorgelagerten Quellen ergibt.
  `requirements.md` wird niemals bearbeitet. Ungelöste Befunde werden gemeldet.
  Die Analyse läuft automatisch nach einem bestandenen Aufgaben-Review und dient
  der Information; sie ist kein Freigabekriterium für die Implementierung.

```text
/codexspec:clarify <feature-dir>
/codexspec:analyze <feature-dir>
```

<a id="small-changes-with-quick"></a>

### Kleine Änderungen mit Quick

Nutzen Sie `quick` für kleine, klar abgegrenzte Änderungen, etwa eine punktuelle Korrektur:

```text
/codexspec:quick Fix the empty-state message on the task list
```

Quick bestätigt und speichert eine kompakte Zusammenfassung der Anforderungen.
Danach koordiniert es Spezifikation, Planung, Aufgaben und Implementierung
mitsamt den Reviews der Generierungsbefehle. Umfangreiche Änderungen oder noch
offene Produkt- und Entwurfsentscheidungen erfordern den Standard-Workflow.
Quick pausiert, sobald eine neue Entscheidung benötigt wird.

<a id="workflow-automation"></a>

### Workflow-Automatisierung

`workflow.auto_next` ist standardmäßig **false**. Steht es in der Konfiguration
des aktiven Arbeitsbereichs auf `true`, folgt auf die abschließende Bestätigung
der Anforderungen automatisch die Spezifikation. Jede Generierungsphase führt
nach `PASS` oder `PASS_WITH_WARNINGS` zur nächsten Phase. `NEEDS_REVISION` oder
`BLOCKED` hält die Kette an. Mit `implement-tasks` endet sie.

Artefakte werden automatisch nur bei verifizierten Fehlern korrigiert, deren
Behebung sich aus vorgelagerten Belegen ergibt. Dafür sind höchstens zwei
Korrektur- und Review-Runden vorgesehen. Empfehlungen werden separat behandelt.
Für die Review- und Korrekturschleife der Implementierung gelten eigene
Abschlussregeln, die weiter unten beschrieben sind.

Die genauen Regeln finden Sie in der [Workflow-Anleitung](../user-guide/workflow.md).

<a id="project-structure"></a>

## Projektstruktur

Die Initialisierung installiert gemeinsame Ressourcen und die ausgewählte
Assistentenintegration:

```text
my-project/
├── .codexspec/
│   ├── config.yml
│   ├── memory/
│   │   └── constitution.md
│   ├── profile/
│   │   ├── constraints/
│   │   ├── conventions/
│   │   ├── pitfalls/
│   │   ├── decisions/
│   │   ├── strategies/
│   │   └── runbooks/
│   ├── review-code/              # Shared review standards
│   ├── specs/
│   │   └── <feature-id>-<name>/   # Added by feature workflows
│   │       ├── requirements.md
│   │       ├── spec.md
│   │       ├── design.md
│   │       ├── plan.md
│   │       ├── tasks.md
│   │       ├── review-*.md
│   │       └── checklists/       # When requested
│   ├── templates/docs/
│   └── scripts/                 # Platform helpers and commit runtime
├── .claude/commands/codexspec/   # --ai claude or both
├── .agents/skills/              # --ai codex or both
├── CLAUDE.md                    # Claude project context
└── AGENTS.md                    # Codex project context
```

Der gemeinsame Blueprint liegt im dedizierten auto-dev-Worktree. In den regulären
Checkouts gibt es keine separat bearbeitbare Kopie. Entwürfe für die manuelle
Wissensprüfung sind von Git ausgeschlossen.
