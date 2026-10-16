<a id="available-commands"></a>

# Verfügbare Befehle

Die CLI bietet sechs öffentliche Befehle. Die Agentenintegrationen liefern
28 Befehle: Claude verwendet `/codexspec:<name>`, Codex `$codexspec:<name>`.
Der besseren Lesbarkeit halber verwenden die folgenden Tabellen Claudes Schreibweise.

<a id="cli-commands"></a>

## CLI-Befehle

| Befehl | Zweck |
|---------|---------|
| `codexspec init` | Ein Projekt für Claude, Codex oder beide initialisieren oder die Installation erneuern |
| `codexspec check` | Installierte Werkzeuge und Abhängigkeiten prüfen |
| `codexspec version` | Versions- und Systeminformationen anzeigen |
| `codexspec config` | Projektkonfiguration anzeigen oder ändern |
| `codexspec list-commands` | Verfügbare Agentenbefehle nach Kategorie auflisten |
| `codexspec show-blueprint` | Den Blueprint des gemeinsamen Worktrees ausgeben, ohne ihn zu ändern |

<a id="core-workflow-commands"></a>

## Befehle des Kern-Workflows

| Befehl | Zweck |
|---------|---------|
| `/codexspec:constitution` | Projektprinzipien erstellen oder aktualisieren und artefaktübergreifend validieren |
| `/codexspec:specify` | Feature-Anforderungen besprechen, bestätigen und dauerhaft speichern |
| `/codexspec:blueprint` | Bestätigte, ausstehende Blueprint-Anforderungen vorbereiten oder pflegen |
| `/codexspec:generate-spec` | Bestätigte Anforderungen in eine nachvollziehbare Spezifikation überführen; automatisches Review |
| `/codexspec:spec-to-design` | Architektur, Komponenten, Schnittstellen und Entscheidungen festlegen; automatisches Review |
| `/codexspec:design-to-plan` | Implementierungsphasen, Reihenfolge und Verifikation planen; automatisches Review |
| `/codexspec:plan-to-tasks` | Überprüfbare Aufgaben erstellen, die vorgelagerte Vorgaben abdecken; automatisches Review und analyze |
| `/codexspec:implement-tasks` | Aufgaben ausführen, Ergebnisse verifizieren, prüfen und korrigieren |
| `/codexspec:auto-dev` | Bestätigte Blueprint-Anforderungen autonom in der Reihenfolge des Dokuments entwickeln |

<a id="artifact-review-commands"></a>

## Befehle für Artefakt-Reviews

| Befehl | Zweck |
|---------|---------|
| `/codexspec:review-spec` | Übereinstimmung der Spezifikation mit den Vorgaben und ihre interne Qualität prüfen |
| `/codexspec:review-design` | Übereinstimmung des Entwurfs mit den Vorgaben, Machbarkeit und Eignung für die Planung prüfen |
| `/codexspec:review-plan` | Übereinstimmung des Plans mit den Vorgaben, Machbarkeit und Eignung für die Implementierung prüfen |
| `/codexspec:review-tasks` | Übereinstimmung der Aufgaben mit den Vorgaben, Abhängigkeiten, Ausführbarkeit und Verifikation prüfen |

<a id="requirements-existing-code-and-debugging"></a>

## Anforderungen, bestehender Code und Debugging

| Befehl | Zweck |
|---------|---------|
| `/codexspec:clarify` | Mehrdeutige Anforderungen klären; zuerst die Anforderungen und dann die Spezifikation aktualisieren |
| `/codexspec:analyze` | Durchgängige Nachvollziehbarkeit prüfen und nachgelagerte Artefakte an die maßgeblichen Vorgaben anpassen |
| `/codexspec:checklist` | Eine Checkliste zur Anforderungsqualität erstellen |
| `/codexspec:tasks-to-issues` | Bestehende Aufgaben in umsetzbare GitHub-Issues überführen |
| `/codexspec:debug` | Die Ursachen untersuchen, bevor eine Korrektur vorgenommen wird |
| `/codexspec:reverse-spec` | Bestehende Architektur untersuchen, Modul-Artefakte entwerfen oder Abweichungen von der Ausgangsbasis melden |

<a id="project-knowledge-commands"></a>

## Befehle für Projektwissen

| Befehl | Zweck |
|---------|---------|
| `/codexspec:distill` | Wiederverwendbares Wissen erfassen oder Einträge mit Kandidatenstatus im lokalen Arbeitsbereich prüfen |
| `/codexspec:evolve` | Geprüftes Wissen in einen Entwurf für einen Upstream-Beitrag überführen |
| `/codexspec:onboard` | Aus bestehendem Code Konventionseinträge mit Kandidatenstatus und belegte Einschränkungen gewinnen |

<a id="git-and-code-review-commands"></a>

## Git- und Code-Review-Befehle

| Befehl | Zweck |
|---------|---------|
| `/codexspec:commit-staged` | Nachrichten aus Änderungen im Staging-Bereich erstellen; Vorschau oder Ausführung eines autorisierten Commits |
| `/codexspec:pr` | Eine strukturierte PR/MR-Beschreibung erstellen |
| `/codexspec:release-notes` | Einen Changelog-Eintrag pflegen und einen Veröffentlichungstext aus dem Git-Verlauf erstellen |
| `/codexspec:review-code` | Ausgewählte Änderungen als Defekt-Gate prüfen; mit `--audit` die Codequalität in angegebenen Pfaden bewerten |

<a id="utility-commands"></a>

## Hilfsbefehle

| Befehl | Zweck |
|---------|---------|
| `/codexspec:config` | Projektkonfiguration interaktiv erstellen, anzeigen, ändern oder zurücksetzen |
| `/codexspec:quick` | Einen kompakten Requirements-First-SDD-Workflow für kleine Änderungen ausführen |

Die alten Python-/React-Prüfeinstiege bleiben aus Gründen der Plugin-Kompatibilität erhalten und gehören nicht zum installierten Katalog mit 28 Befehlen. Verwenden Sie `review-code` mit den jeweils passenden Sprach- und Framework-Regeln sowie `--audit` für eine pfadbezogene Bewertung.

## Befehlsreferenz

### `/codexspec:constitution`

Erstellt oder aktualisiert die Projektverfassung. Die Verfassung legt Architekturprinzipien, Technologie-Stack, Code-Standards und Governance-Regeln fest, die alle späteren Entwicklungsentscheidungen leiten.

**Syntax:**

```
/codexspec:constitution [principles description]
```

**Argumente:**

| Argument | Erforderlich | Beschreibung |
|----------|----------|-------------|
| `principles description` | Nein | Beschreibung der aufzunehmenden Prinzipien (wird bei Bedarf abgefragt) |

**Was der Befehl tut:**

- Legt `.codexspec/memory/constitution.md` an, falls nicht vorhanden
- Aktualisiert eine bestehende Verfassung um neue Prinzipien
- Prüft die bereichsübergreifende Konsistenz mit den Vorlagen
- Erstellt einen Sync-Impact-Bericht über Änderungen und betroffene Dateien
- Prüft abhängige Vorlagen auf Verfassungskonformität

**Was erstellt wird:**

```
.codexspec/
└── memory/
    └── constitution.md    # Project governance document
```

**Beispiel:**

```text
You: /codexspec:constitution Focus on code quality, testing standards, and clean architecture

AI:  Creating constitution...

     ✓ Created .codexspec/memory/constitution.md
     Version: 1.0.0

     Sync Impact Report:
     - plan-template-*.md: ✅ aligned
     - spec-template-*.md: ✅ aligned
     - tasks-template-*.md: ✅ aligned

     Core Principles:
     1. Code Quality First
     2. Test-Driven Development
     3. Clean Architecture

     Suggested commit: docs: create constitution v1.0.0
```

**Tipps:**

- Definieren Sie Prinzipien früh im Projekt, um konsistente Entscheidungen zu gewährleisten
- Berücksichtigen Sie sowohl technische als auch prozessuale Prinzipien
- Verfassung vor größeren Feature-Entwicklungen durchsehen
- Änderungen an der Verfassung lösen eine bereichsübergreifende Validierung aus

---

### `/codexspec:specify`

Klärt Anforderungen durch einen interaktiven Dialog, bestätigt die resultierende Zusammenfassung und hält sie für spätere Sitzungen fest.

**Syntax:**

```
/codexspec:specify [your idea or requirement]
```

**Argumente:**

| Argument | Erforderlich | Beschreibung |
|----------|----------|-------------|
| `your idea or requirement` | Nein | Erste Beschreibung dessen, was Sie bauen möchten (wird bei Bedarf abgefragt) |

**Was der Befehl tut:**

- Stellt Klärungsfragen, um Ihre Idee zu erfassen
- Erkennt Randfälle, an die Sie vielleicht nicht gedacht haben
- Erarbeitet in einem Dialog hochwertige Anforderungen
- Konzentriert sich auf das „Was" und „Warum", nicht auf die technische Umsetzung
- Vergibt stabile IDs an bestätigte Anforderungen, Constraints, Decisions, Exclusions und Open Questions
- Dokumentiert Belege aus den Aussagen des Nutzers und ein Bestätigungs-Log
- Legt den Feature-Workspace und `requirements.md` an

**Was erstellt wird:**

```text
.codexspec/specs/{feature-id}-{feature-name}/requirements.md
```

Nur bestätigte Einträge werden zu verbindlichen Anforderungen. Offene Fragen bleiben ausdrücklich offen. Dies ist die Bestätigungsstufe für Anforderungen: Nichts ist verbindlich, bis Sie die finale Zusammenfassung explizit bestätigen.

**Beispiel:**

```text
You: /codexspec:specify I want to build a task management app

AI:  Great! Let me help you clarify the requirements.

     First, who are the target users for this app?
     - Individual professionals
     - Small teams
     - Enterprise organizations
     - All of the above

You: Small teams, mainly software development teams

AI:  Got it. For small dev teams:
     - Do you need real-time collaboration features?
     - Should tasks support sub-tasks or just flat lists?
     - Any integration requirements (GitHub, Slack, etc.)?

You: Real-time is important. Sub-tasks yes. GitHub integration would be nice.

AI:  [Continues exploring requirements...]

     Summary of clarified requirements:
     - Target: Small dev teams (5-20 people)
     - Core: Tasks with sub-tasks, real-time updates
     - Integration: GitHub (optional)
     - Priority: Real-time collaboration > Sub-tasks > GitHub

     Ready to generate the spec document?
     Use /codexspec:generate-spec to create spec.md
```

**Tipps:**

- Für die anfängliche Anforderungserkundung einsetzen
- Vollständigkeit ist nicht nötig – Verfeinerung erfolgt iterativ
- Bei Annahmen der AI nachfragen
- Zusammenfassung vor der Spec-Erzeugung prüfen

---

### `/codexspec:blueprint`

Mit `blueprint` bereiten Sie mehrere bestätigte Anforderungen vor der Entwicklung
vor. Mit `auto-dev` lassen Sie diese Liste abarbeiten:

```text
/codexspec:blueprint Add a confirmed requirement for task reminders
/codexspec:auto-dev
```

Bei der Anforderungsermittlung für den Blueprint werden Richtung, Entscheidungen
und Einschränkungen, die der Benutzer festlegen muss, geklärt, bevor eine
Anforderung in die Liste aufgenommen wird. Die gemeinsame Datei
`.codexspec/blueprint.md` verwendet die Zustände `pending`, `in_progress` und
`completed`. Sie können ausstehende Anforderungen anhängen, ersetzen, löschen
oder neu anordnen. Aktive und abgeschlossene Einträge sind bei der
Blueprint-Pflege schreibgeschützt.

Auto-dev folgt der Reihenfolge im Dokument. Es setzt ein bereits begonnenes
Feature fort, bevor es ein weiteres beginnt, und liest die Liste nach jedem
Abschluss erneut. So können auch neu angehängte ausstehende Anforderungen in den
laufenden Durchgang aufgenommen werden. Es führt SDD-Phasen, Implementierung,
Verifikation, Reviews und Korrekturen innerhalb der bestätigten Anforderungen
aus. Ein Aufruf von `auto-dev` aktiviert diese Automatisierung unabhängig von
`workflow.auto_next`, ohne diese Einstellung zu ändern.

Beide Befehle nutzen `worktree-for-codexspec-auto-dev` auf dem Branch
`codexspec/auto-dev`. Unter den gemeinsamen Regeln zur Zuständigkeit und zum
Schreibschutz können sie gleichzeitig arbeiten. Die Anforderungen werden in
diesem Arbeitsbereich nacheinander entwickelt. Lässt sich eine Produktentscheidung
nicht aus den bestätigten Anforderungen ableiten, wird der Durchgang mit
entsprechenden Belegen angehalten. Während der normalen autonomen Ausführung
werden dazu keine Rückfragen gestellt.

Zeigen Sie den aktuellen gemeinsamen Blueprint an, ohne ihn zu ändern:

```bash
codexspec show-blueprint
```

---

### `/codexspec:generate-spec`

Bestätigte Anforderungen in eine nachvollziehbare Spezifikation überführen; automatisches Review.

**Syntax:**

```
/codexspec:generate-spec
```

**Argumente:**

| Argument | Erforderlich | Beschreibung |
|----------|----------|-------------|
| Feature-Pfad | Nein | Explizites Feature-Verzeichnis, `requirements.md` oder Ziel-`spec.md`; erforderlich, wenn die Auflösung mehrdeutig ist |

**Was der Befehl tut:**

- Liest bestätigte Anforderungen aus dem gewählten Feature-Workspace
- Unterstützt ältere Workspaces, die nur `spec.md` enthalten, mit einer expliziten Traceability-Warnung
- Erzeugt eine umfassende `spec.md` mit:
  - Feature-Überblick und Zielen
  - User Stories mit Akzeptanzkriterien
  - Funktionalen Anforderungen (REQ-XXX-Format)
  - Nicht-funktionalen Anforderungen (NFR-XXX-Format)
  - Randfällen und deren Behandlung
  - ausgeschlossenen Themen
- Fügt `Sources`-Verweise auf die Anforderungs-IDs hinzu
- Hält zur Bestätigung an, statt Autoritätskonflikte per Annahme aufzulösen
- Prüft automatisch und kann evidenzbasierte Defekte über maximal zwei Runden reparieren

**Was erstellt wird:**

```
.codexspec/
└── specs/
    └── 2026-0613-1200ab-task-management/
        └── spec.md
```

**Beispiel:**

```text
You: /codexspec:generate-spec

AI:  Generating specification...

     ✓ Created .codexspec/specs/2026-0613-1200ab-task-management/spec.md

     Sections included:
     - Overview: Task management for small dev teams
     - 4 User Stories with acceptance criteria
     - 12 Functional Requirements (REQ-001 to REQ-012)
     - 3 Non-Functional Requirements (NFR-001 to NFR-003)
     - 5 Edge Cases documented
     - Out of Scope: Mobile apps, Enterprise SSO

     Next steps:
     - Review the spec with /codexspec:review-spec
     - Or proceed to /codexspec:spec-to-design
```

---

### `/codexspec:spec-to-design`

Liest die bestätigten Dateien `requirements.md` und `spec.md`, die Projektgrundsätze und relevante Fakten aus dem Repository. Erstellt `design.md` mit Komponenten, Schnittstellen, Datenfluss, Alternativen und Entscheidungen samt Verweisen auf die zugrunde liegenden Anforderungen. Führt `review-design` automatisch aus. Ändert eine Entwurfsentscheidung die bestätigte Absicht oder erfordert sie eine neue Nutzerentscheidung, wird der Ablauf angehalten.

```text
/codexspec:spec-to-design <feature-dir>
```

---

### `/codexspec:design-to-plan`

Wandelt den bestätigten Entwurf in einen Implementierungsplan um. Führen Sie zuerst `spec-to-design` aus, um Architektur, Komponenten, Schnittstellen und Technologieentscheidungen festzulegen.

```text
/codexspec:design-to-plan [design.md | spec.md | feature-directory]
```

Liest `requirements.md`, `spec.md`, `design.md` und die Projektverfassung. Plant Implementierungsphasen, Reihenfolge und Verifikation und verweist auf den Entwurf, statt das System neu zu entwerfen. Jede Plankomponente enthält `Covers: REQ-xxx; Design: <design component>`.

Erstellt `plan.md` und startet `review-plan`. Bei aktiviertem `auto_next` folgt nach erfolgreicher Prüfung `plan-to-tasks`. Änderungen an bestätigten Absichten benötigen eine Bestätigung. Ein expliziter Pfad hat Vorrang vor dem aktuellen Feature-Branch; bei Mehrdeutigkeit ist eine Auswahl erforderlich. Für ältere Features ohne `design.md` bleibt die Planung anhand von `spec.md` möglich.

---

### `/codexspec:plan-to-tasks`

Bricht den technischen Plan in ausführbare Aufgaben mit expliziter Abdeckung und prüfbaren Ergebnissen herunter.

**Syntax:**

```
/codexspec:plan-to-tasks [path_to_spec.md path_to_plan.md]
```

**Argumente:**

| Argument | Erforderlich | Beschreibung |
|----------|----------|-------------|
| `paths` | Nein | Pfade zu Spec und Plan (werden bei Bedarf automatisch erkannt) |

**Was der Befehl tut:**

- Legt Aufgaben mit jeweils einem prüfbaren Ergebnis an; eine Aufgabe darf mehrere eng verwandte Dateien berühren
- Verwendet test-first-Reihenfolge nur, wenn sie durch Plan, Verfassung, bestätigte Anforderungen oder Risiko erforderlich ist
- Markiert Aufgaben nur dann mit `[P]`, wenn sie tatsächlich unabhängig sind
- Gibt exakte Dateipfade für jede Aufgabe an
- Fügt `Covers`-Links zu Plan- und Anforderungs-IDs hinzu

**Was erstellt wird:**

```
.codexspec/
└── specs/
    └── 2026-0613-1200ab-task-management/
        └── tasks.md    # Task breakdown
```

**Aufgaben-Struktur:**

```markdown
### Task 2.1: Write Tests for Entity A [P]
- **Type**: Testing
- **Files**: `tests/test_entity_a.py`
- **Description**: Write unit tests for Entity A
- **Dependencies**: Task 1.3
- **Est. Complexity**: Low
```

**Beispiel:**

```text
You: /codexspec:plan-to-tasks

AI:  Breaking down plan into tasks...

     ✓ Created tasks.md
     Total: 24 tasks
     Parallelizable: 8 tasks (33%)

     Phase 1: Foundation (4 tasks)
     Phase 2: Core Implementation - TDD (10 tasks)
     Phase 3: Integration (4 tasks)
     Phase 4: Interface Layer (3 tasks)
     Phase 5: Testing & Documentation (3 tasks)

     Execution Order:
     Phase 1 → [Phase 2 tasks in parallel groups] → Phase 3 → Phase 4 → Phase 5

     Checkpoints defined at each phase boundary.
```

**Tipps:**

- Jede Aufgabe sollte genau ein prüfbares Ergebnis liefern und darf eng verwandte Dateien mit umfassen
- Test-Aufgaben gehen der Umsetzung nur voraus, wenn test-first erforderlich ist
- `[P]` kennzeichnet tatsächlich unabhängige, parallelisierbare Aufgaben
- Abhängigkeiten vor der Umsetzung prüfen

Nach dem Erstellen der Aufgaben wird `review-tasks` ausgeführt. Bei `PASS` oder `PASS_WITH_WARNINGS` folgt einmalig `analyze`; die Analyse führt keine zusätzliche Abschlussbedingung ein. Die Aufgaben decken bestätigte Anforderungen, Spezifikation, Entwurf und Plan ab.

---

### `/codexspec:implement-tasks`

Aufgaben ausführen, Ergebnisse verifizieren, prüfen und korrigieren.

```text
/codexspec:implement-tasks <feature-dir>
```

Vier Artefakt-Reviewer prüfen Übereinstimmung mit den Vorgaben, Abdeckung,
Machbarkeit und interne Qualität: `review-spec`, `review-design`, `review-plan`
und `review-tasks`. Sie laufen nach der Generierung automatisch und lassen sich
auch manuell aufrufen. Ihre Berichte unterscheiden verifizierte Fehler von
nicht blockierenden Risikohinweisen und möglichen Verbesserungen des Entwurfs.
Sie enthalten außerdem eine Kompatibilitätsbewertung.

`review-code` bietet eine separate Fehlerprüfung für ausgewählte Änderungen als
Freigabekriterium (Defekt-Gate) sowie eine explizite Qualitätsbewertung des gesamten Codes:

```text
/codexspec:review-code --feature <feature-dir>
/codexspec:review-code --uncommitted
/codexspec:review-code --audit src/
```

Standardmäßig wird die vollständige Differenz des Feature-Branches geprüft:
Änderungen mit Commit, Änderungen im Staging-Bereich, Änderungen außerhalb des
Staging-Bereichs und nicht ignorierte unversionierte Änderungen. Sie können
explizit nur Änderungen mit Commit, Änderungen ohne Commit oder einen einzelnen
Commit als Prüfgrundlage auswählen. `--feature` ergänzt den Anforderungskontext,
ohne den Git-Prüfumfang einzuschränken. `--audit` bewertet die angegebenen Pfade
und erstellt eine beratende Bewertung statt eines Abschlussurteils.

Reviews laden gemeinsame Standards aus `.codexspec/review-code/` und wählen die
relevanten Verhaltensdimensionen sowie Prüfungen für Sprache und Framework aus.
Jeder Befund benötigt konkrete Belege, einen tatsächlich erreichbaren Auslöser,
eine Zuordnung zur ausgewählten Änderung und eine Beschreibung der Auswirkungen.
Der Reviewer meldet Fehler und belegte Wartungsempfehlungen, ohne Dateien zu
bearbeiten. Die Stelle, die die Korrektur ausführt, prüft diese Befunde unabhängig.

Bei Code-Aufgaben werden zuerst Tests geschrieben. Dokumentations- und
Konfigurationsaufgaben werden direkt umgesetzt und mit geeigneten Prüfungen
verifiziert. Nach Korrekturen kann ein inkrementelles Review die Prüfabdeckung
unveränderter Bereiche wiederverwenden. Für die endgültige Abnahme sind ein
frisches `PASS` für das vollständige Feature, vollständige Prüfabdeckung und
Verifikation sowie null anerkannte P0–P3-Fehler erforderlich. Belegte
Wartungsempfehlungen werden separat gemeldet.

`workflow.auto_maintenance` ist standardmäßig **true** und bestimmt, ob bei
Korrekturen auch verifizierte, kompatible Wartungsverbesserungen umgesetzt werden.
Wird es deaktiviert, werden diese Empfehlungen weiterhin gemeldet; Fehler müssen
weiterhin behoben und erforderliche Prüfungen weiterhin ausgeführt werden. Die
Einstellung ist unabhängig vom automatischen Phasenübergang und kein Argument
von `implement-tasks`.

Für Debugging, bei dem zuerst die Ursache untersucht wird:

```text
/codexspec:debug Investigate intermittent failures when saving a task
```

Debug folgt der Reihenfolge Untersuchung → Musteranalyse → Prüfung einer
Einzelhypothese → Korrektur mit einem zuerst fehlschlagenden Test. Bei der
Implementierung wird diese Untersuchung hinzugezogen, wenn Korrekturen nicht
vorankommen, ein nicht trivialer Korrektheitsfehler nachvollzogen werden muss
oder Fehler derselben Ursachenklasse in mehreren Review-Runden wiederkehren.
Nach drei fehlgeschlagenen Korrekturen wird die Architektur neu bewertet.

Mit `checklist` prüfen Sie die Klarheit, Vollständigkeit und Konsistenz der Anforderungen:

```text
/codexspec:checklist Check the authentication requirements for completeness
```

Die [Befehlsreferenz](commands.md) erläutert die Auswahl des
Review-Umfangs, die Argumente und die Verfahren im Detail.

---

### `/codexspec:auto-dev`

Bestätigte Blueprint-Anforderungen autonom in der Reihenfolge des Dokuments entwickeln.

Siehe [`blueprint`](#codexspecblueprint).

```text
/codexspec:auto-dev
```

---

### `/codexspec:review-spec`

Validiert die Spezifikation gegen die bestätigten Anforderungen und gegen ihre eigene interne Qualität.

**Syntax:**

```
/codexspec:review-spec [path_to_spec.md]
```

**Argumente:**

| Argument | Erforderlich | Beschreibung |
|----------|----------|-------------|
| `path_to_spec.md` | Nein | Pfad zur Spec-Datei (wird bei Bedarf automatisch erkannt) |

**Was der Befehl tut:**

- Prüft die Treue gegenüber den Einträgen der bestätigten `requirements.md`
- Prüft interne Konsistenz, Klarheit und Überprüfbarkeit
- Behandelt einen fehlenden Vorlagenabschnitt nur dann als Defekt, wenn verbindlicher Inhalt ihn verlangt
- Verlangt für jeden Defekt die Felder `Evidence`, `Location`, `Mismatch`, `Impact` und `Remediation`
- Trennt `Risk Advisories / Design Opportunities` von Defekten
- Erzeugt einen Status sowie einen Kompatibilitäts-Score, der aus den klassifizierten Befunden abgeleitet wird

**Gemeinsame Prüfregeln:**

| Kategorie | Bedeutung |
|----------|---------|
| Abweichung von der Vorgabe | Widerspricht einer maßgeblichen Quelle oder lässt erforderliche Inhalte daraus aus |
| Interner Mangel | Intern widersprüchlich, nicht durchführbar oder nicht überprüfbar |
| Advisory | Optionale Verbesserung ohne Evidenz für einen aktuellen Defekt |

Der Status lautet `PASS`, `PASS_WITH_WARNINGS`, `NEEDS_REVISION` oder `BLOCKED`. Advisories ändern weder Status noch Score.

**Beispiel:**

```text
You: /codexspec:review-spec

AI:  Overall Status: NEEDS_REVISION
     Compatibility Score: 79/100

     Warning SPEC-001
     Evidence: CON-002 requires a measurable response-time limit.
     Location: spec.md, REQ-006
     Mismatch: "Respond quickly" has no measurable threshold.
     Impact: Acceptance cannot be verified.
     Remediation: Ask the user to confirm a threshold, update requirements.md,
                  then synchronize REQ-006.

     Risk Advisories / Design Opportunities:
     - None
```

**Tipps:**

- Vor `/codexspec:spec-to-design` ausführen
- `BLOCKED` und `NEEDS_REVISION` bedeuten: noch nicht bereit für den nächsten Schritt
- Advisories nicht zu Anforderungen hochstufen
- Nach Korrekturen erneut ausführen

---

### `/codexspec:review-design`

Prüft `design.md` anhand der bestätigten Anforderungen und der Spezifikation auf Übereinstimmung, Machbarkeit und Eignung als Grundlage für die Planung. Belegte Fehler werden getrennt von optionalen Entwurfsverbesserungen gemeldet. Es gelten dieselben Statuswerte und Reparaturgrenzen wie bei den anderen Artefaktprüfungen.

```text
/codexspec:review-design <feature-dir>
```

---

### `/codexspec:review-plan`

Prüft den technischen Umsetzungsplan auf Treue, Machbarkeit und begründete technische Entscheidungen.

**Syntax:**

```
/codexspec:review-plan [path_to_plan.md]
```

**Argumente:**

| Argument | Erforderlich | Beschreibung |
|----------|----------|-------------|
| `path_to_plan.md` | Nein | Pfad zur Plan-Datei (wird bei Bedarf automatisch erkannt) |

**Was der Befehl tut:**

- Verifiziert `Covers`-Links und die erforderliche Spec-Abdeckung
- Prüft anwendbare Verfassungsregeln und Repository-Fakten
- Markiert unbegründete Komplexität nur, wenn sie konkrete Kosten oder Konflikte erzeugt
- Verlangt für jeden Defekt die Evidenz-Felder und fasst Befunde mit derselben Ursache zusammen
- Weist optionale Architektur-Verbesserungen als Advisories aus
- Nutzt den gemeinsamen Regeln für Status und Kompatibilitätsbewertung

**Beispiel:**

```text
You: /codexspec:review-plan

AI:  Overall Status: PASS
     Compatibility Score: 100/100
     Verified defects: none

     Risk Advisories / Design Opportunities:
     - A caching layer may become useful if production measurements exceed
       the confirmed latency target. It is not required by the current plan.
```

**Tipps:**

- Vor `/codexspec:plan-to-tasks` ausführen
- Evidenzbasierte Defekte vor der Aufgabengenerierung auflösen
- Spekulative Architektur-Ideen im Advisory-Abschnitt halten
- Prüfen, dass der Tech-Stack zu den Fähigkeiten des Teams passt

Die Planung setzt die bestätigte `design.md` um, ohne Architekturentscheidungen erneut zu öffnen. Die Prüfung bewertet sowohl die Entwurfsverweise des Plans als auch seine Anforderungsabdeckung.

---

### `/codexspec:review-tasks`

Validiert die Aufgaben-Aufschlüsselung auf Abdeckung, prüfbare Ergebnisse, korrekte Reihenfolge und tragfähige Abhängigkeiten.

**Syntax:**

```
/codexspec:review-tasks [path_to_tasks.md]
```

**Argumente:**

| Argument | Erforderlich | Beschreibung |
|----------|----------|-------------|
| `path_to_tasks.md` | Nein | Pfad zur tasks-Datei (wird bei Bedarf automatisch erkannt) |

**Was der Befehl tut:**

- Prüft, ob alle erforderlichen Plan-Posten und Anforderungen durch Aufgaben abgedeckt sind
- Validiert test-first-Reihenfolge nur dort, wo eine autoritative Quelle sie verlangt
- Verifiziert, dass jede Aufgabe genau ein überprüfbares Ergebnis hat
- Validiert Abhängigkeiten (keine Zyklen, korrekte Reihenfolge)
- Prüft die Parallelisierungs-Marker
- Validiert Dateipfade
- Verlangt für jeden Defekt die Evidenz-Felder
- Weist optionale Prozess-Verbesserungen als Advisories aus
- Nutzt den gemeinsamen Regeln für Status und Kompatibilitätsbewertung

**Beispiel:**

```text
You: /codexspec:review-tasks

AI:  Overall Status: NEEDS_REVISION
     Compatibility Score: 79/100

     Warning TASK-001
     Evidence: Task 2.5 declares a dependency on Task 2.4.
     Location: tasks.md, Task 2.5
     Mismatch: Task 2.5 is also marked [P].
     Impact: Parallel execution can start before its prerequisite completes.
     Remediation: Remove [P] or remove the dependency if the plan proves independence.
```

**Tipps:**

- Vor `/codexspec:implement-tasks` ausführen
- Befunde zur Test-Reihenfolge sind nur dann Defekte, wenn eine autoritative Quelle Tests verlangt
- Prüfen, dass die Parallelisierungs-Marker stimmen
- Verifizieren, dass Dateipfade zur Projektstruktur passen

---

### `/codexspec:clarify`

Untersucht eine bestehende Spezifikation auf Mehrdeutigkeiten und Lücken. Einsatzgebiet ist die iterative Verfeinerung nach der ersten Spec-Erstellung.

**Syntax:**

```
/codexspec:clarify [path_to_spec.md]
```

**Argumente:**

| Argument | Erforderlich | Beschreibung |
|----------|----------|-------------|
| `path_to_spec.md` | Nein | Pfad zur Spec-Datei (wird bei Bedarf automatisch erkannt) |

**Was der Befehl tut:**

- Untersucht Anforderungen und Spec anhand fokussierter Mehrdeutigkeits-Kategorien
- Stellt gezielte Klärungsfragen (max. 5)
- Aktualisiert nach Bestätigung durch den Nutzer zuerst `requirements.md` und synchronisiert danach `spec.md`
- Integriert ggf. Befunde aus review-spec

**Mehrdeutigkeits-Kategorien:**

| Kategorie | Was sie erkennt |
|----------|-----------------|
| **Fehlende Angaben** | Fehlende Abschnitte, leerer Inhalt, nicht vorhandene Akzeptanzkriterien |
| **Mangelnde Konkretisierung** | Vage Begriffe („schnell", „skalierbar"), undefinierte Constraints |
| **Klarheit des Verhaltens** | Lücken in der Fehlerbehandlung, undefinierte Zustandsübergänge |
| **Fehlende Messbarkeit** | Nicht-funktionale Anforderungen ohne Metriken |

**Beispiel:**

```text
You: /codexspec:clarify

AI:  Scanning spec.md for ambiguities...

     Found issues in 3 categories.

     ## Question 1/5: Specificity

     **Context**: NFR-001 states "System should respond quickly"

     **Question**: What is the target response time?

     | Option | Description | Impact |
     |--------|-------------|--------|
     | A | < 100ms for all operations | High performance requirement |
     | B | < 500ms for reads, < 1s for writes | Balanced approach |
     | Custom | Provide a different answer | - |

     **Recommendation**: Option B - balanced for typical web app

You: B

AI:  ✓ Updated NFR-001: Response time < 500ms reads, < 1s writes
     Added to Clarifications section in spec.md
```

**Tipps:**

- Verwenden, wenn spec.md existiert, aber verfeinert werden muss
- Integriert Befunde aus `/codexspec:review-spec`
- Maximal 5 Fragen pro Durchlauf
- Bei komplexen Spezifikationen mehrfach ausführen

---

### `/codexspec:analyze`

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

Fehlt bei einem älteren Feature `requirements.md`, beginnt die Analyse mit `spec.md`, weist auf die fehlenden Belege aus der ursprünglichen Diskussion hin und meldet Befunde, ohne Artefakte zu ändern. Auch eine fehlende ältere `design.md` verhindert die Analyse nicht.

---

### `/codexspec:checklist`

Erzeugt Qualitäts-Checklisten zur Validierung von Vollständigkeit, Klarheit und Konsistenz der Anforderungen. Diese sind gewissermaßen „Unit-Tests für das Anforderungsschreiben".

**Syntax:**

```
/codexspec:checklist [focus_area]
```

**Argumente:**

| Argument | Erforderlich | Beschreibung |
|----------|----------|-------------|
| `focus_area` | Nein | Domänen-Fokus (z. B. „ux", „api", „security", „performance") |

**Was der Befehl tut:**

- Erzeugt nach Qualitätsdimensionen gegliederte Checklisten
- Legt die Checklisten im Verzeichnis `FEATURE_DIR/checklists/` ab
- Die Posten konzentrieren sich auf die Qualität der Anforderungen, nicht auf Umsetzungstests

**Qualitätsdimensionen:**

- **Vollständigkeit der Anforderungen**: Sind alle notwendigen Anforderungen vorhanden?
- **Klarheit der Anforderungen**: Sind die Anforderungen spezifisch und eindeutig?
- **Konsistenz der Anforderungen**: Sind die Anforderungen ohne Widersprüche aufeinander abgestimmt?
- **Qualität der Akzeptanzkriterien**: Sind die Erfolgskriterien messbar?
- **Szenarioabdeckung**: Sind alle Abläufe/Fälle abgedeckt?
- **Randfallabdeckung**: Sind die Randbedingungen definiert?
- **Nichtfunktionale Anforderungen**: Sind Performance, Security, Accessibility spezifiziert?
- **Abhängigkeiten und Annahmen**: Sind sie dokumentiert?

**Beispiele für Checklisten-Typen:**

- `ux.md` – visuelle Hierarchie, Interaktionszustände, Accessibility
- `api.md` – Fehlerformate, Rate Limiting, Authentifizierung
- `security.md` – Datenschutz, Bedrohungsmodell, Reaktion auf Einbrüche
- `performance.md` – Metriken, Lastbedingungen, Degradation

**Beispiel:**

```text
You: /codexspec:checklist security

AI:  Generating security checklist...

     ✓ Created .codexspec/specs/2026-0613-1200ab-task-management/checklists/security.md

     ## Security Requirements Quality Checklist

     ### Authentication Requirements
     - [ ] CHK001 - Are authentication requirements defined for all protected endpoints? [Completeness]
     - [ ] CHK002 - Is password complexity explicitly specified? [Clarity]
     - [ ] CHK003 - Are session timeout requirements quantified? [Measurability]

     ### Data Protection
     - [ ] CHK004 - Are data encryption requirements specified at rest? [Completeness]
     - [ ] CHK005 - Are data encryption requirements specified in transit? [Completeness]
     - [ ] CHK006 - Is PII handling explicitly documented? [Clarity]

     Total: 15 items across 4 categories
```

**Tipps:**

- Checklisten validieren die Anforderungsqualität, nicht die Korrektheit der Umsetzung
- Für Anforderungs-Review und -Verbesserung einsetzen
- Domänenspezifische Checklisten für fokussierte Validierung anlegen
- Vor dem Übergang zur technischen Planung ausführen

---

### `/codexspec:tasks-to-issues`

Wandelt Aufgaben aus `tasks.md` in GitHub-Issues für Projekt-Tracking und Zusammenarbeit um.

**Syntax:**

```
/codexspec:tasks-to-issues
```

**Argumente:**

| Argument | Erforderlich | Beschreibung |
|----------|----------|-------------|
| Keine | – | Wandelt alle Aufgaben des aktuellen Features um |

**Was der Befehl tut:**

- Liest Task-IDs, Beschreibungen, Abhängigkeiten und Dateipfade aus
- Erzeugt GitHub-Issues mit strukturiertem Body
- Vergibt Labels anhand des Aufgaben-Typs (setup, implementation, testing, documentation)
- Verknüpft Abhängigkeiten zwischen Issues
- Meldet erzeugte Issues mitsamt URLs

**Voraussetzungen:**

- Git-Repository mit GitHub-Remote
- GitHub CLI (`gh`) installiert und authentifiziert
- `tasks.md` ist vorhanden

**Beispiel:**

```text
You: /codexspec:tasks-to-issues

AI:  Converting tasks to GitHub issues...

     Repository: github.com/example/taskman

     Creating issues:
     ✓ #42: Task 1.1 - Setup Project Structure (setup)
     ✓ #43: Task 2.1 - Write Tests for Task Entity (testing)
     ✓ #44: Task 2.2 - Implement Task Entity (implementation)
     ...

     Summary:
     - Issues created: 24
     - Labels applied: setup(4), implementation(12), testing(5), documentation(3)
     - Dependencies linked: 18

     View issues: https://github.com/example/taskman/issues
```

**Tipps:**

- Setzt GitHub-CLI-Authentifizierung voraus (`gh auth login`)
- Funktioniert nur mit GitHub-Repositories
- Erzeugt Issues in der Standard-Konfiguration des Repositories
- Vor dem Lauf auf Duplikate prüfen

Prüfen Sie vor dem Erstellen von Issues das Ziel-Repository anhand seines Remotes und holen Sie eine ausdrückliche Freigabe ein. Eine erzeugte Aufgabenliste ist allein noch keine Erlaubnis zur Veröffentlichung.

---

### `/codexspec:debug`

Die Ursachen untersuchen, bevor eine Korrektur vorgenommen wird.

Siehe [Workflow](workflow.md#review-and-debugging).

```text
/codexspec:debug Investigate intermittent failures when saving a task
```

---

### `/codexspec:reverse-spec`

Für unterschiedliche Ziele gibt es zwei Einstiegspunkte:

| Befehl | Zweck | Ergebnis und Grenzen |
|---------|-----------|-----------------|
| `onboard [path]` | Wiederverwendbares Projektwissen aus einer bestehenden Codebasis aufbauen | Konventionseinträge mit Kandidatenstatus und nur eng gefasste und durch konkrete Belege gestützte Einschränkungen im Profil; der Code bleibt schreibgeschützt |
| `reverse-spec [path]` | Die vorhandene Architektur verstehen oder Code mit der bestätigten Zielsetzung vergleichen | Artefakte als Entwurf oder ein Abweichungsbericht; der Code bleibt schreibgeschützt |

```text
/codexspec:onboard src/
/codexspec:reverse-spec
/codexspec:reverse-spec src/auth
```

Onboard leitet Konventionen aus dem beobachtbaren Code ab und schlägt
Einschränkungen ausschließlich auf Grundlage expliziter Verbote vor.
Konventionseinträge mit Kandidatenstatus werden lokal sofort wirksam. Bei
Einschränkungen mit Kandidatenstatus ist in der Sitzung eine Entscheidung nötig:
speichern, bearbeiten oder verwerfen. Onboard bewahrt vorhandenes Wissen und
erfindet bei einer erstmaligen Untersuchung weder Begründungen früherer
Entscheidungen noch Erfahrungswissen über Fallstricke.

Reverse-spec bietet drei Modi:

- **Überblick**: Ohne Pfad oder bei Angabe des Repository-Stammverzeichnisses
  erstellt es einen knappen Architekturentwurf in `design.md` sowie `slices.md`
  zur Auswahl der zu untersuchenden Module.
- **Generieren**: Bei einem Modulpfad ohne bestätigte Ausgangsbasis entstehen
  Entwürfe von `spec.md`, `design.md` und offene oder abgeleitete Anforderungen.
- **Abgleichen**: Bei einem Modul mit bestätigter Ausgangsbasis entsteht
  `reconcile.md`. Es meldet undokumentiertes Verhalten, nicht implementierte
  Spezifikationen und semantische Abweichungen von der bestätigten Spezifikation
  und dem bestätigten Entwurf. Die Anforderungen bestimmen dabei die Zielsetzung.

Abgeleitete Entwürfe müssen von einem Menschen bestätigt werden, bevor sie als
Ausgangsbasis dienen können. Der Abgleich nennt die vorgeschlagene Vorgehensweise:
Code korrigieren, Dokumente aktualisieren oder die Zielsetzung klären. Er setzt
sie nicht automatisch um.

---

### `/codexspec:distill`

Erfasst wiederverwendbares, funktionsübergreifendes Wissen in `.codexspec/profile/` und prüft offene Kandidaten, ohne deren Markdown-Dateien von Hand zu bearbeiten.

**Syntax:**

```text
/codexspec:distill [interaction segment]
/codexspec:distill review
```

**Manuelle Prüfung:**

- `/codexspec:distill review` – oder ein direkter Aufruf ohne neuen Abschnitt zum Extrahieren – öffnet eine Offline-HTML-Seite, die ausschließlich von `127.0.0.1` ausgeliefert wird. Ihre Kopfzeile nennt das Projektverzeichnis, in das die Sitzung schreibt, damit zwei gleichzeitig geöffnete Prüfungen nicht verwechselt werden können.
- Die Seite unterstützt strukturierte Überarbeitung, Freigabe, Verwerfen, Zurückstellen, Zusammenführung, eine vollständige Übersicht der vorgemerkten Entscheidungen und ein ausdrückliches **Alle anwenden**. Eine Überarbeitung oder Zusammenführung muss ihre exakte endgültige Markdown-Vorschau zeigen, bevor dieselbe Aktion vorgemerkt werden kann; die Seite nennt vor jeder Entscheidung, in welchem der drei Vorschauzustände ein Eintrag ist – keine Vorschau, mit den aktuellen Änderungen übereinstimmend, oder seit der Vorschau geändert.
- Jede Aktion, die Eintragsdateien entfernt, verlangt eine zweite Bestätigung mit ihrer Folge: Verwerfen nennt die Datei, die beim Anwenden gelöscht wird, eine Zusammenführung nennt die Anzahl der Mitgliedseinträge, die sie löscht, und das Verwerfen des Entwurfs nennt die Anzahl der vorgemerkten Entscheidungen, die verloren gehen.
- Ein Eintrag wird nur mit menschlicher Freigabe **und** ergebnisbasiertem Verifikationsbeleg `vetted`. Die Seite zeigt vor der Freigabe, ob die gespeicherten Belege diese Anforderung bereits erfüllen.
- Die Warteschlange gruppiert Einträge nach dem, was entschieden ist, und zeigt, wie viele der offenen Einträge bereits erledigt sind. Nach einer vorgemerkten Entscheidung springt die Seite zum nächsten unentschiedenen Eintrag; ein Schalter in der Kopfzeile schaltet das ab.
- Die Seite ist über die Tastatur bedienbar – `?` zeigt die Tasten. Keine einzelne Taste wendet den Stapel an, bricht die Sitzung ab oder verwirft den Entwurf.
- Vorgemerkte Entscheidungen liegen in einem wiederherstellbaren, von Git ausgeschlossenen Projektentwurf. Pro Projekt ist nur eine schreibende Prüfung aktiv.
- Ein strukturell beschädigter Entwurf bleibt mit einer verwertbaren Diagnose erhalten und wird nur durch ein ausdrückliches Verwerfen entfernt.
- Beim Anwenden werden die Quell-Hashes erneut geprüft; hat sich ein Eintrag geändert, wird der gesamte Stapel abgelehnt. Eine gleichzeitige Änderung wird nie überschrieben und kein Teilerfolg gemeldet.
- Alle Seitenressourcen werden mit CodexSpec ausgeliefert. Die Seite nutzt kein CDN, keinen Remote-Modellaufruf und keine Telemetrie.
- Lässt sich kein Browser öffnen, gibt der Befehl die tokengeschützte lokale URL aus. Fordern Sie den ausdrücklichen Textmodus an, wenn ein Browser unpassend ist; er nutzt dieselbe Prüfung und denselben Schreibpfad.

Auto-Distill bleibt nicht-interaktiv und nicht-blockierend: Es öffnet die Seite nie, startet keine Textprüfung und wartet nicht auf einen gespeicherten Entwurf.

---

### `/codexspec:evolve`

`evolve` wählt nur geprüftes Wissen aus, das auch außerhalb des Projekts nützlich
ist, und erstellt daraus einen Befehls- oder Skill-Entwurf. Vor einem Push oder
dem Öffnen eines Beitrags-PRs zur menschlichen Prüfung holt es explizite Zustimmung ein.

```text
/codexspec:evolve
```

---

### `/codexspec:onboard`

Aus bestehendem Code Konventionseinträge mit Kandidatenstatus und belegte Einschränkungen gewinnen.

Siehe [`reverse-spec`](#codexspecreverse-spec).

```text
/codexspec:onboard src/
```

---

### `/codexspec:commit-staged`

```text
/codexspec:commit-staged -p
/codexspec:pr --spec <feature-dir>/spec.md
/codexspec:release-notes --from <ref> --to HEAD
/codexspec:tasks-to-issues <feature-dir>
```

- **commit-staged** analysiert den exakten Staging-Bereich und erstellt eine
  Nachricht gemäß Conventional Commits. Mit `-p` sehen Sie eine Vorschau, ohne
  einen Commit zu erstellen. Der aufrufende Workflow wählt die Dateien aus und
  übernimmt sie in den Staging-Bereich. Die autorisierte Ausführung nutzt die
  abgesicherte Laufzeitumgebung und prüft erneut, ob der tatsächlich im Commit
  gespeicherte Inhalt mit der Analyse übereinstimmt. Die Commit-Hinweise für
  Agenten gelten in gewöhnlichen Gesprächen sowie in SDD-, Blueprint- und
  auto-dev-Workflows. Die bloße Verfügbarkeit des Befehls ruft ihn weder auf noch
  autorisiert sie einen Commit.
- **pr** erstellt aus der Differenz eine strukturierte Beschreibung für einen
  GitHub-PR oder GitLab-MR. `--spec` ergänzt optional den Feature-Kontext. Dazu
  dient ein Dateipfad zu `spec.md` oder ein Name beziehungsweise Präfix eines
  Feature-Verzeichnisses, der zu dieser Datei aufgelöst wird. Standardmäßig wird
  Text zur Verwendung auf der Hosting-Plattform ausgegeben.
- **release-notes** erstellt aus dem Git-Verlauf einen Eintrag nach Keep a
  Changelog und einen Veröffentlichungstext. Der Standardabschnitt ist
  `[Unreleased]`; `--version` verwendet die angegebene Bezeichnung. Es übernimmt
  keine Dateien in den Staging-Bereich, erstellt keine Commits, erhöht keine
  Versionen, setzt keine Tags, veröffentlicht nichts und erstellt kein Release.
- **tasks-to-issues** erstellt GitHub-Issues aus bestehenden Aufgaben, einschließlich
  Abhängigkeiten und Abnahmekriterien. Es benötigt eine authentifizierte GitHub-CLI
  und prüft, ob das Issue-Repository dem konfigurierten Remote entspricht.

Für die direkte Commit-Vorschau und autorisierte Commits im aktuellen
Arbeitsverzeichnis sind Python 3.11+ und Git erforderlich. Die Laufzeitumgebung wird mit
CLI-Projekten installiert und mit dem Claude-Plugin ausgeliefert. Auch vom
Agenten erstellte Merges mit Inhaltsänderungen nutzen die Staging-Analyse.
Merges, die nur Historien verbinden, behalten die Standardnachricht von Git
bei; Baum und Eltern-Commits werden dennoch validiert. Fast-Forwards erstellen keinen Commit.

Der gemeinsame Helfer `.codexspec/scripts/commit-staged-helper.py` (oder die mitgelieferte Plugin-Kopie) benötigt Python 3.11+ und Git, ruft kein LLM auf, erhält Git hooks und weist indexierte Inhalte zurück, die sich nach der Analyse geändert haben. Eine einmalige Initialisierung stellt diese Laufzeit bereit; Workspace-Routing, blueprint und auto-dev benötigen weiterhin die CLI.

---

### `/codexspec:pr`

Erzeugt eine strukturierte GitHub-Pull-Request-/GitLab-Merge-Request-Beschreibung aus dem git diff. Integriert optional `spec.md` für SDD-nachverfolgbaren Kontext.

**Syntax:**

```
/codexspec:pr [--target-branch <branch>] [--sections <list>] [--spec <id-or-path>] [--output <file>]
```

**Argumente:**

| Argument | Erforderlich | Beschreibung |
|----------|----------|-------------|
| `--target-branch <branch>` | Nein | Branch, gegen den verglichen wird (Default: `origin/main`) |
| `--sections <list>` | Nein | Kommaseparierte Teilmenge aus `summary, changes, testing, verify, checklist, notes` (Default: `all`) |
| `--spec <id-or-path>` | Nein | Optionale Spec-Integration: eine Feature-ID (z. B. `2025-0321-1430k7-auth`), aufgelöst unter `.codexspec/specs/`, oder ein expliziter `path/to/spec.md`. Weglassen, um nur aus git zu erzeugen |
| `--output <file>` | Nein | Beschreibung in eine Datei schreiben statt auf das Terminal |

**Was der Befehl tut:**

- Sammelt den Git-Kontext (aktueller Branch, Remote-URL, vorausliegende Commits, Dateiänderungen, vollständiger Diff, Commit-Nachrichten) gegenüber dem Ziel-Branch
- Erkennt die Plattform automatisch anhand der Remote-URL: GitHub → „Pull Request", GitLab → „Merge Request", andere/keine → fällt auf GitHub-Terminologie zurück und warnt
- Lädt `.codexspec/memory/constitution.md`, falls vorhanden, und richtet die Beschreibung an den Dokumentations-/Code-Review-Standards aus
- Berücksichtigt `language.commit` (dann `language.output`, dann Englisch) für die Sprache der Beschreibung; technische Begriffe (API, JWT, PR, MR) bleiben angemessen auf Englisch
- Fügt bei Angabe von `--spec` einen Context-Abschnitt mit User Stories und Anforderungen aus spec.md hinzu; andernfalls wird rein aus dem Diff erzeugt
- Gibt Abschnitte gemäß `--sections` aus (Summary, Changes, Testing, Verification Steps, Pre-merge Checklist, Notes / Breaking Changes)

**Beispiel:**

```text
You: /codexspec:pr --spec 2026-0613-1200ab-task-management

AI:  Generating Pull Request description...

     Platform: GitHub (github.com/example/taskman)
     Branch:   feature/task-management  →  origin/main
     Commits:  8 ahead

     ## Pull Request: Task management for small dev teams

     ### Context
     - User stories and REQ-* pulled from spec.md

     ### Summary
     - Adds task CRUD, sub-tasks, and real-time updates

     ### Changes
     - src/taskman/models/task.py (new)
     - src/taskman/api/tasks.py (new)
     - ...

     ### Verification Steps
     1. `uv run pytest`
     2. `uv run codexspec check`
```

**Tipps:**

- `--spec` für kleine Bugfixes oder Änderungen ohne formale Spezifikation weglassen
- Mit `/codexspec:commit-staged` kombinieren, um aus derselben Arbeit sowohl eine Commit-Nachricht als auch eine PR-Beschreibung zu erzeugen
- Siehe die [Fallstudie zum PR-Beschreibungs-Generator](../case-studies/case-study-pr-description-generator.md) für ein durchgespieltes, durchgängiges Beispiel dieses Befehls (inklusive Einbindung des spec.md-Kontexts)

---

### `/codexspec:release-notes`

```text
/codexspec:commit-staged -p
/codexspec:pr --spec <feature-dir>/spec.md
/codexspec:release-notes --from <ref> --to HEAD
/codexspec:tasks-to-issues <feature-dir>
```

- **commit-staged** analysiert den exakten Staging-Bereich und erstellt eine
  Nachricht gemäß Conventional Commits. Mit `-p` sehen Sie eine Vorschau, ohne
  einen Commit zu erstellen. Der aufrufende Workflow wählt die Dateien aus und
  übernimmt sie in den Staging-Bereich. Die autorisierte Ausführung nutzt die
  abgesicherte Laufzeitumgebung und prüft erneut, ob der tatsächlich im Commit
  gespeicherte Inhalt mit der Analyse übereinstimmt. Die Commit-Hinweise für
  Agenten gelten in gewöhnlichen Gesprächen sowie in SDD-, Blueprint- und
  auto-dev-Workflows. Die bloße Verfügbarkeit des Befehls ruft ihn weder auf noch
  autorisiert sie einen Commit.
- **pr** erstellt aus der Differenz eine strukturierte Beschreibung für einen
  GitHub-PR oder GitLab-MR. `--spec` ergänzt optional den Feature-Kontext. Dazu
  dient ein Dateipfad zu `spec.md` oder ein Name beziehungsweise Präfix eines
  Feature-Verzeichnisses, der zu dieser Datei aufgelöst wird. Standardmäßig wird
  Text zur Verwendung auf der Hosting-Plattform ausgegeben.
- **release-notes** erstellt aus dem Git-Verlauf einen Eintrag nach Keep a
  Changelog und einen Veröffentlichungstext. Der Standardabschnitt ist
  `[Unreleased]`; `--version` verwendet die angegebene Bezeichnung. Es übernimmt
  keine Dateien in den Staging-Bereich, erstellt keine Commits, erhöht keine
  Versionen, setzt keine Tags, veröffentlicht nichts und erstellt kein Release.
- **tasks-to-issues** erstellt GitHub-Issues aus bestehenden Aufgaben, einschließlich
  Abhängigkeiten und Abnahmekriterien. Es benötigt eine authentifizierte GitHub-CLI
  und prüft, ob das Issue-Repository dem konfigurierten Remote entspricht.

Für die direkte Commit-Vorschau und autorisierte Commits im aktuellen
Arbeitsverzeichnis sind Python 3.11+ und Git erforderlich. Die Laufzeitumgebung wird mit
CLI-Projekten installiert und mit dem Claude-Plugin ausgeliefert. Auch vom
Agenten erstellte Merges mit Inhaltsänderungen nutzen die Staging-Analyse.
Merges, die nur Historien verbinden, behalten die Standardnachricht von Git
bei; Baum und Eltern-Commits werden dennoch validiert. Fast-Forwards erstellen keinen Commit.

#### Optionen für Release Notes

| Befehle | Referenz |
|---|---|
| `--version <X.Y.Z>` | Angegebenes Versionslabel; sonst `[Unreleased]` |
| `--from <ref>` | Startreferenz; sonst letzter erreichbarer Tag, danach eine zuordenbare Changelog-Version, danach die vollständige Historie |
| `--to <ref>` | Endreferenz; standardmäßig `HEAD` |
| `--output <file>` | Datei für den Release-Text; sonst Terminalausgabe |
| `--spec <feature>` | Optionaler Feature-Kontext; ist das Feature nicht auflösbar, wird dies gemeldet und die Erzeugung mit Git fortgesetzt |

---

### `/codexspec:review-code`

Prüft die ausgewählte Git-Änderung vor dem Merge als striktes Defekt-Gate. Das Standardziel umfasst den vollständigen Feature-Unterschied; explizite Selektoren wählen committed, uncommitted oder einen einzelnen Commit, aber keine Pfadfilter.

<!-- REVIEW-CODE-BREAKING: DEFAULT-GATE -->
<!-- REVIEW-CODE-BREAKING: PATH-AUDIT -->

**Standardmodus der Prüfung:**

- Der Standardbefehl ist jetzt ein änderungsbezogenes Defekt-Gate und kein allgemeiner Qualitätsscore.
- Positionspfade sind nicht mehr gültig. Verwenden Sie `--audit` ausdrücklich für den beratenden Pfad-Qualitätsscore.

**Syntax des Defekt-Gates:**

```text
/codexspec:review-code
/codexspec:review-code --committed [--base <branch>] [--feature <feature-dir>] [--focus <instructions>]
/codexspec:review-code --uncommitted [--feature <feature-dir>] [--focus <instructions>]
/codexspec:review-code --commit <sha> [--parent <n>] [--feature <feature-dir>] [--focus <instructions>]
/codexspec:review-code [--committed] --incremental-from <fingerprint> [--feature <feature-dir>]
```

Jede Defekt-Gate-Form akzeptiert zusätzlich `--decided-by reviewer|ask`, das `review.decided_by` für diesen Lauf überschreibt.

<!-- REVIEW-CODE-SYSTEM-CONTRACT -->
<!-- REVIEW-CODE-VARIANT-SEARCH -->
<!-- REVIEW-CODE-NEUTRAL-HANDOFF -->

Das Gate inventarisiert alle ausgewählten Artefakte, bewertet zutreffende Anforderungen und führt fünf Pässe in dieser Reihenfolge aus: Scope, System Contract, Behavior, Risk und Verification. Es erfasst belegte modulübergreifende Verträge und semantische Review-Partitionen; jede bestätigte wiederholbare Ursache löst vor Abschluss der Runde eine begrenzte Suche nach verwandten Vorkommen aus. Auf sechs Berichtsabschnitte folgt ein maschinenlesbarer Ergebnisblock `<review-code-result>` mit `schema_version: "3"`. Der Ergebnisblock enthält Zielidentität, Abdeckung und objektive Prüfpflichten nach der Reparatur. Der Aufrufer bewahrt diese neutralen Pflichten für eine neue vollständige Prüfung auf, ohne Reparaturbegründungen oder frühere Korrektheitsschlüsse weiterzugeben. Das Ergebnis ist genau `PASS`, `FAIL` oder `INCONCLUSIVE`: Jeder P0-P3-Befund führt zu `FAIL`; fehlende Pflichtnachweise oder unvollständige Abdeckung führen zu `INCONCLUSIVE`.

**Inkrementelle Runden.** Nach einer Reparatur prüft `--incremental-from <fingerprint>` nur, was sich seit diesem früheren Ergebnis geändert hat: die geänderten Dateien, die Review-Partitionen und Verträge, die sie berühren, und die übernommenen Verpflichtungen. Die Abdeckung unveränderter, nicht betroffener Dateien wird wiederverwendet; der Reviewer meldet dennoch jeden Defekt, den er an anderer Stelle findet. Ein inkrementelles `PASS` schließt ein Feature nie ab: `implement-tasks` führt zuerst ein vollständiges Review aus, nach jeder Reparatur inkrementelle Reviews und zum Schluss ein frisches vollständiges Review als Abnahme. Review-Aufzeichnungen liegen außerhalb des Repositorys in Ihrem Benutzer-Cache-Verzeichnis (`~/.cache/codexspec/review/` bzw. `%LOCALAPPDATA%\codexspec\review\`); im Gespräch erscheinen nur der Bericht und der Ergebnisblock.

**Entscheidungsmodus.** `review.decided_by` in `.codexspec/config.yml` legt fest, wer über einen Befund entscheidet, dessen Auslöser außerhalb des realen Einsatzkontexts des Projekts liegt, etwa eine Eingabe, die das Projekt nie erhält. Mit dem Standardwert `reviewer` verhält sich das Review genau wie bisher. Mit `ask` meldet das Review einen solchen Punkt als offene Szenario-Entscheidung, statt daran zu scheitern, und `implement-tasks` fragt Sie einmal: beheben oder das Szenario als außerhalb des Umfangs akzeptieren. Ihre Antwort wird als bestätigter `CON`- oder `OUT`-Eintrag in `requirements.md` festgehalten, sodass spätere Runden den Punkt nicht erneut melden.

```text
You: /codexspec:review-code --feature .codexspec/specs/2026-0714-example

AI:  ## Verdict
     **PASS** — all required review and verification completed with no findings.
```

**Anwendbare Standards und Wartung.** Jede Prüfung liest die gemeinsamen Regeln und den gewählten Modus, bewertet alle sieben Dimensionen und lädt Details nur bei Relevanz für Verhalten, Vertrag oder Abhängigkeiten. Auch unveränderte Abhängigkeiten können beim Nachverfolgen Sprach- oder Framework-Prüfungen aktivieren. Wartungsvorschläge brauchen Belege für ein gegenwärtiges Problem und eine lokale, verhaltenskompatible Verbesserung. Vermutete künftige Komplexität oder reine Stilgrenzwerte rechtfertigen keine Reparatur. Das Defektergebnis bleibt bei Version 3; ein separates `<review-code-maintenance>` in Version 1 meldet Vorschläge mit demselben Zielfingerabdruck. Die eigenständige Prüfung meldet sie nur. `implement-tasks` prüft und bearbeitet sie gemäß `workflow.auto_maintenance` (Standard `true`). Korrekturen werden fortgesetzt, solange sie substanzielle Fortschritte erzielen; die bestehenden Abbruchbedingungen gelten weiterhin. Es gibt keine feste Obergrenze für die Anzahl der Runden. Die abschließende Abnahme erfordert eine neue vollständige Prüfung.

Boolesche CLI-Schalter akzeptieren `on/true/1/yes` und `off/false/0/no` unabhängig
von Groß- und Kleinschreibung und auch mit umgebenden Leerzeichen. Ein boolescher
Schalter ohne Wert kehrt den aktuellen Wert im Ziel-Checkout um. Gespeicherte
YAML-Werte sind boolesch.

`codexspec init` installiert die gemeinsamen Prüfdaten für Claude Code und Codex unter `.codexspec/review-code/`. `--force` aktualisiert ausgelieferte Daten und behält Erweiterungsdateien mit anderen Pfaden. Die reine CLI-Installation erstellt keine Projektdateien. Bei ausschließlicher Plugin-Nutzung ohne installierten Projektbaum werden dieselben Daten aus dem vom Host aufgelösten Plugin-Stamm geladen.

<!-- REVIEW-CODE-AUDIT -->

#### Pfad-Qualitätsaudit

Der explizite audit-Zweig prüft vollständige aktuelle Dateiinhalte auf idiomatische Klarheit, Korrektheit, Robustheit, Architektur und Verfassungskonformität. Der Score ist beratend und kann `implement-tasks` nicht abschließen.

**Syntax:**

```
/codexspec:review-code --audit [paths...]
```

**Argumente:**

| Argument | Erforderlich | Beschreibung |
|----------|----------|-------------|
| `path...` | Nein | Eine oder mehrere zu prüfende Quelldateien oder Verzeichnisse (leerzeichengetrennt). Default ist `src/`, falls weggelassen |

**Was der Befehl tut:**

- Erkennt die Primärsprache(n) anhand der Dateierweiterungen und fährt bei gemischtsprachigen Zielen mit einem separaten Durchlauf pro Sprache fort
- Startet statische Analyse-Werkzeuge, wenn deren Konfiguration vorhanden ist (`ruff`/`mypy`, `eslint`/`tsc`, `go vet`/`gofmt`, `cargo check`/`cargo clippy`, `shellcheck`); überspringt die betreffenden Prüfungen andernfalls und meldet reduzierte Abdeckung
- Bewertet vier Dimensionen: Idiomatic Clarity & Simplicity, Correctness & Explicit Contracts, Runtime Robustness & Resource Discipline sowie Architecture & Design Integrity
- Blendet für erkannte Frameworks verpflichtende Unterabschnitte ein (z. B. Hooks Compliance bei React, Ownership & Borrowing bei Rust, Goroutine & Context Discipline bei Go, Memory & Lifetime Safety bei C/C++, Execution Safety bei Shell)
- Gleicht Befunde gegen `.codexspec/memory/constitution.md` ab, falls vorhanden; fehlt sie, entfällt die Bewertung der Verfassungskonformität und ihr Gewicht wird umverteilt
- Klassifiziert Befunde nach Schweregrad: CRITICAL, HIGH, MEDIUM, LOW (LOW-Hinweise sind auf maximal 5 Punkte Gesamt-Abzug begrenzt)

**Beispiel:**

```text
You: /codexspec:review-code --audit src/

AI:  # Code Review Report

     ## Summary
     - Overall Status: Needs Work
     - Quality Score: 78/100
     - Detected Language: Python

     ## Static Analysis Results
     | Tool   | Status | Issues | Details                |
     |--------|--------|--------|------------------------|
     | ruff   | Warn   | 3      | Unused imports, line length |
     | mypy   | Pass   | 0      | No type errors         |

     ## Detailed Findings
     ### Critical Issues (CRITICAL)
     - [ ] [CODE-001] src/auth/service.py:42 - bare `except Exception:` swallows the original cause
       Impact: Original error context is lost during debugging.
       Suggestion: narrow the exception and re-raise with `raise ... from err`.

     ### Suggestions (LOW)
     - [ ] [CODE-004] src/auth/service.py:120 - manual loop where a comprehension suffices

     ## Recommendations
     1. Priority 1: Fix CODE-001 before merge.
     2. Priority 2: Apply LOW suggestions opportunistically.
```

**Tipps:**

- Mehrere Pfade übergeben, um einen fokussierten Ausschnitt zu prüfen, z. B. `src/ tests/`
- Der Score ist beratend; die CRITICAL/HIGH-Befunde sind das handlungsrelevante Signal

---

### `/codexspec:config`

Verwaltet die Projektkonfiguration interaktiv (anlegen/ansehen/ändern/zurücksetzen). Dies ist das Slash-Befehl-Gegenstück zur CLI `codexspec config` – ideal für Installationen über den Plugin Marketplace.

**Syntax:**

```
/codexspec:config [--view]
```

**Argumente:**

| Argument | Erforderlich | Beschreibung |
|----------|----------|-------------|
| `--view` | Nein | Zeigt die aktuelle Konfiguration an, ohne sie zu ändern. Ohne Argumente wird das interaktive Verwaltungs-Menü geöffnet |

**Was der Befehl tut:**

- Ausschließlich auf `.codexspec/config.yml` gerichtet
- `--view` (oder die Menüoption „View current config") gibt die Datei in lesbarer Form aus; meldet „Configuration Not Found", falls sie fehlt
- Der interaktive Modus bietet bei bestehender Konfiguration: View, Modify, Reset to defaults, Cancel
- Ohne bestehende Konfiguration läuft der Anlege-Flow, der eine minimale, nur `output` enthaltende Konfiguration schreibt (interaction/document/commit fallen auf `output`, danach `en` zurück, sodass eine reine `output`-Datei voll funktionsfähig ist)
- Lässt Sie jede Sprach-Dimension einzeln setzen (output, interaction, document, commit) und Workflow-Optionen wie `auto_next` umschalten

**Was erstellt/bearbeitet wird:**

```
.codexspec/config.yml
```

**Beispiel:**

```text
You: /codexspec:config

AI:  ## Configuration Manager

     Configuration file found at .codexspec/config.yml.
     What would you like to do?
     - View current config
     - Modify config
     - Reset to defaults
     - Cancel

You: Modify config

AI:  Select a dimension to change:
     - Output language (base)
     - Interaction language
     - Document language
     - Commit-message language
     - workflow.auto_next
     - workflow.auto_distill
     - workflow.auto_maintenance
     - workflow.worktrees (default on; checkout-local)
     - review.decided_by

You: Output language (base) → zh-CN

AI:  ✓ Updated language.output: "zh-CN"
     (interaction and document fall back to output, then en.)
```

**Tipps:**

- `/codexspec:config --view` verwenden, um den aktuellen Zustand zu inspizieren, bevor etwas geändert wird
- Eine frische oder zurückgesetzte Konfiguration schreibt nur `output`; `interaction`/`document` nur setzen, wenn sie von `output` abweichen sollen
- Für skriptgesteuerte Änderungen im Terminal ist die CLI `codexspec config` vorzuziehen (`--set-lang`, `--set-interaction-lang`, `--set-document-lang`, `--set-commit-lang`, `--auto-next`)

Das interaktive Menü verwaltet außerdem `workflow.auto_distill`, `workflow.auto_maintenance`, `workflow.worktrees` und `review.decided_by`. Konfigurationsänderungen folgen dem Worktree-Routing und gelten jeweils für den einzelnen Checkout.

---

### `/codexspec:quick`

Führt einen vereinfachten Requirements-First-SDD-Ablauf für kleine Änderungen aus.

**Syntax:**

```
/codexspec:quick [describe a small requirement]
```

**Argumente:**

| Argument | Erforderlich | Beschreibung |
|----------|----------|-------------|
| `describe a small requirement` | Nein | Kurze Beschreibung der kleinen, sauber abgegrenzten Änderung (wird bei Bedarf abgefragt) |

**Was der Befehl tut:**

- Bewertet den Umfang (berührte Dateien, Modul-Spanne, neue Abhängigkeiten, ungelöste Produktentscheidungen) und empfiehlt bei breiten Änderungen oder mehreren unabhängigen Ergebnissen den Standard-Ablauf
- Legt einen Feature-Workspace und `requirements.md` mit derselben Zeitstempel-Konvention wie `/codexspec:specify` an
- Löst nur die Mehrdeutigkeiten auf, die die Umsetzung wesentlich beeinflussen; präsentiert eine kompakte bestätigte Zusammenfassung (`NEED-*`, relevante `CON-*`/`DEC-*`, `OUT-*`, ungelöste `OPEN-*`)
- Hält am Confirmation Gate: Es wird nichts erzeugt, bevor Sie die Zusammenfassung bestätigen
- Führt die Generierungsbefehle nacheinander für das neue Feature-Verzeichnis aus: `/codexspec:generate-spec`, `/codexspec:design-to-plan`, `/codexspec:plan-to-tasks`, `/codexspec:implement-tasks`
- Überlässt die Auto-Review-Schleife dem jeweiligen Generierungs-Befehl; hält an und fragt den Nutzer, wenn ein Review eine neue Produkt- oder Architekturentscheidung erfordert
- Meldet Feature-Verzeichnis, Artefakt-Pfade, Review-Ergebnisse, die Verifizierung der Umsetzung sowie ungelöste Advisories separat

**Was erstellt wird:**

```text
.codexspec/specs/{timestamp}-{feature-name}/
├── requirements.md
├── spec.md
├── plan.md
└── tasks.md
```

**Beispiel:**

```text
You: /codexspec:quick Add a "remember me" checkbox to the login form

AI:  Scope check: 1 component, 1 form field, no new dependencies. Quick is appropriate.

     Confirmed requirements:
     - NEED-1: "Remember me" checkbox on the login form (default unchecked)
     - DEC-1: Persist a long-lived refresh token only when checked
     OUT-1: SSO / social login (unchanged)

     Confirm this summary to start the automated flow. [y/N]

You: y

AI:  Running generate-spec → design-to-plan → plan-to-tasks → implement-tasks ...

     ✓ Feature dir: .codexspec/specs/2026-0713-0915ab-remember-me/
     ✓ All reviews PASS_WITH_WARNINGS or higher
     ✓ Implementation verified
     Open advisories: none
```

**Tipps:**

- Quick für kleine Änderungen mit genau einem Ergebnis verwenden; andernfalls `/codexspec:specify` und den Standard-Ablauf verwenden
- Eine Bestätigung ist weiterhin nötig – Quick leitet nie eine Produktentscheidung ab, nur um die Automatisierung am Laufen zu halten
- Wenn ein Generierungs-Review `NEEDS_REVISION`/`BLOCKED` liefert, hält Quick an und gibt die Kontrolle an Sie zurück

---
