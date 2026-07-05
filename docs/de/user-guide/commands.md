# Commands

Dies ist die Referenz für die Slash-Befehle von CodexSpec. Diese Befehle werden in der Chat-Oberfläche von Claude Code aufgerufen.

Workflow-Muster und der richtige Einsatzort der einzelnen Befehle finden sich unter [Workflow](workflow.md). Zu den CLI-Befehlen siehe [CLI](../reference/cli.md).

## Quick Reference

Nach Kategorie gruppiert – analog zum Katalog im README. Innerhalb jeder Gruppe sind die Befehle in Workflow-Reihenfolge angeordnet.

### Core Workflow Commands

| Befehl | Zweck |
|---------|---------|
| `/codexspec:constitution` | Projektverfassung erstellen oder aktualisieren, inklusive bereichsübergreifender Validierung |
| `/codexspec:specify` | Anforderungen klären, bestätigen und in `requirements.md` festhalten |
| `/codexspec:generate-spec` | `spec.md` aus den geklärten Anforderungen erzeugen (★ Auto-Review) |
| `/codexspec:spec-to-plan` | Spezifikation in einen technischen Umsetzungsplan überführen (★ Auto-Review) |
| `/codexspec:plan-to-tasks` | Plan in nachverfolgbare, prüfbare Aufgaben herunterbrechen (★ Auto-Review) |
| `/codexspec:implement-tasks` | Aufgaben mit bedingtem TDD-Workflow ausführen |

### Review Commands (Quality Gates)

| Befehl | Zweck |
|---------|---------|
| `/codexspec:review-spec` | Spezifikation auf Vollständigkeit und Qualität prüfen |
| `/codexspec:review-plan` | Technischen Plan auf Machbarkeit und Abgestimmtheit prüfen |
| `/codexspec:review-tasks` | Abdeckung, Reihenfolge und Machbarkeit der Aufgaben validieren |

### Enhancement Commands

| Befehl | Zweck |
|---------|---------|
| `/codexspec:config` | Projektkonfiguration interaktiv verwalten (anlegen/ansehen/ändern/zurücksetzen) |
| `/codexspec:clarify` | Bestehende Spezifikation auf Mehrdeutigkeiten prüfen (4 Kategorien, max. 5 Fragen) |
| `/codexspec:analyze` | Bereichsübergreifende Konsistenzanalyse (nur lesend, schweregradbasiert) |
| `/codexspec:checklist` | Checklisten für die Qualität der Anforderungen erzeugen |
| `/codexspec:tasks-to-issues` | Aufgaben in GitHub-Issues überführen |

### Git Workflow Commands

| Befehl | Zweck |
|---------|---------|
| `/codexspec:commit-staged` | Commit-Nachricht aus den gestagten Änderungen erzeugen (session-kontextbewusst) |
| `/codexspec:pr` | PR/MR-Beschreibung aus dem git diff erzeugen (Plattform wird automatisch erkannt) |

### Code Review Commands

| Befehl | Zweck |
|---------|---------|
| `/codexspec:review-code` | Code in jeder beliebigen Sprache prüfen (idiomatische Klarheit, Korrektheit, Robustheit, Architektur) |
| `/codexspec:review-python-code` | Python-Code prüfen (PEP 8, Typsicherheit, Robustheit, Verfassungskonsistenz) |
| `/codexspec:review-react-code` | React-/TypeScript-Code prüfen (Komponentenarchitektur, Hooks-Regeln, State, Performance) |

### Fast Track

| Befehl | Zweck |
|---------|---------|
| `/codexspec:quick` | Einen gestrafften Requirements-First-SDD-Ablauf für kleine Änderungen fahren |

---

## Command Categories

### Core Workflow Commands

Befehle für den primären Requirements-First-SDD-Workflow: Verfassung → Bestätigte Anforderungen → Spezifikation → Plan → Aufgaben → Umsetzung. Bestätigte Anforderungen sind hier die oberste Autorität – nichts in dieser Kette ist verbindlich, bis Sie es am Confirmation Gate explizit bestätigen.

### Review Commands (Quality Gates)

Befehle, die Artefakte an jeder Workflow-Station unter einem **evidence-based review**-Vertrag validieren: Jeder Defekt muss konkrete Angaben zu `Evidence`, `Location`, `Mismatch`, `Impact` und `Remediation` enthalten. Advisory-Hinweise zu Designfragen werden separat ausgewiesen und ändern weder den Status noch lösen sie automatische Änderungen aus. Bestätigte Defekte dürfen repariert und erneut geprüft werden – über maximal zwei Runden; Advisories bleiben durchgehend optional.

### Enhancement Commands

Befehle für die iterative Verfeinerung, die bereichsübergreifende Validierung, die Konfiguration und die Anbindung an das Projektmanagement.

### Git Workflow Commands

Befehle, die fertige Arbeit in teilbare Artefakte verwandeln: Commit-Nachrichten aus dem gestagten Diff und strukturierte PR/MR-Beschreibungen aus dem Branch-Diff.

### Code Review Commands

Befehle, die Quellcode (beliebige Sprache, Python-spezifisch, React/TypeScript-spezifisch) auf idiomatische Klarheit, Korrektheit, Robustheit, Architektur und Verfassungskonformität prüfen. Die Befunde folgen derselben Severity-Disziplin wie die Artefakt-Reviews: CRITICAL/HIGH-Befunde müssen konkrete Evidenz vorweisen; LOW-Hinweise sind rein beratend.

### Fast Track

Ein gestraffter Befehl, der den Requirements-First-SDD-Ablauf für kleine, sauber abgegrenzte Änderungen end-to-end durchläuft.

---

## Command Reference

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

**Was er passiert:**

- Legt `.codexspec/memory/constitution.md` an, falls nicht vorhanden
- Aktualisiert eine bestehende Verfassung um neue Prinzipien
- Prüft die bereichsübergreifende Konsistenz mit den Vorlagen
- Erstellt einen Sync-Impact-Bericht über Änderungen und betroffene Dateien
- Prüft abhängige Vorlagen auf Verfassungskonformität

**Was erstellt wird:**

```
.codexspec/
└── memory/
    └── constitution.md    # Projekt-Governance-Dokument
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

Klärt Anforderungen durch interaktives Frage-Antwort-Spiel, bestätigt die resultierende Zusammenfassung und hält sie für spätere Sitzungen fest.

**Syntax:**

```
/codexspec:specify [your idea or requirement]
```

**Argumente:**

| Argument | Erforderlich | Beschreibung |
|----------|----------|-------------|
| `your idea or requirement` | Nein | Erste Beschreibung dessen, was Sie bauen möchten (wird bei Bedarf abgefragt) |

**Was er passiert:**

- Stellt Klärungsfragen, um Ihre Idee zu erfassen
- Erkennt Randfälle, an die Sie vielleicht nicht gedacht haben
- Erarbeitet in einem Dialog hochwertige Anforderungen
- Konzentriert sich auf das „Was" und „Warum", nicht auf die technische Umsetzung
- Vergibt stabile IDs an bestätigte Needs, Constraints, Decisions, Exclusions und Open Questions
- Dokumentiert Nutzerevidenz und ein Bestätigungs-Log
- Legt den Feature-Workspace und `requirements.md` an

**Was erstellt wird:**

```text
.codexspec/specs/{feature-id}-{feature-name}/requirements.md
```

Nur bestätigte Einträge werden zu verbindlichen Anforderungen. Offene Fragen bleiben ausdrücklich offen. Dies ist die Confirmation Gate für Anforderungen: Nichts ist verbindlich, bis Sie die finale Zusammenfassung explizit bestätigen.

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

### `/codexspec:generate-spec`

Erzeugt das Dokument `spec.md` aus den geklärten Anforderungen. Dieser Befehl fungiert als „Anforderungs-Compiler", der Ihre geklärten Anforderungen in eine strukturierte Spezifikation überführt.

**Syntax:**

```
/codexspec:generate-spec
```

**Argumente:**

| Argument | Erforderlich | Beschreibung |
|----------|----------|-------------|
| Feature-Pfad | Nein | Explizites Feature-Verzeichnis, `requirements.md` oder Ziel-`spec.md`; erforderlich, wenn die Auflösung mehrdeutig ist |

**Was er passiert:**

- Liest bestätigte Anforderungen aus dem gewählten Feature-Workspace
- Unterstützt ältere Workspaces, die nur `spec.md` enthalten, mit einer expliziten Traceability-Warnung
- Erzeugt eine umfassende `spec.md` mit:
  - Feature-Überblick und Zielen
  - User Stories mit Akzeptanzkriterien
  - Funktionalen Anforderungen (REQ-XXX-Format)
  - Nicht-funktionalen Anforderungen (NFR-XXX-Format)
  - Randfällen und deren Behandlung
  - Out-of-Scope-Posten
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
     - Or proceed to /codexspec:spec-to-plan
```

**Tipps:**

- Ausführen, nachdem `/codexspec:specify` die Anforderungen geklärt hat
- Die erzeugte Spezifikation vor dem Weiterarbeiten prüfen
- Für die Qualitätsvalidierung `/codexspec:review-spec` verwenden
- Bei kleinen Anpassungen spec.md direkt bearbeiten

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

**Was er passiert:**

- Untersucht Anforderungen und Spec anhand fokussierter Mehrdeutigkeits-Kategorien
- Stellt gezielte Klärungsfragen (max. 5)
- Aktualisiert nach Bestätigung durch den Nutzer zuerst `requirements.md` und synchronisiert danach `spec.md`
- Integriert ggf. Befunde aus review-spec

**Mehrdeutigkeits-Kategorien:**

| Kategorie | Was sie erkennt |
|----------|-----------------|
| **Completeness Gaps** | Fehlende Abschnitte, leerer Inhalt, nicht vorhandene Akzeptanzkriterien |
| **Specificity Issues** | Vage Begriffe („schnell", „skalierbar"), undefinierte Constraints |
| **Behavioral Clarity** | Lücken in der Fehlerbehandlung, undefinierte Zustandsübergänge |
| **Measurability Problems** | Nicht-funktionale Anforderungen ohne Metriken |

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

### `/codexspec:spec-to-plan`

Überführt die Feature-Spezifikation in einen technischen Umsetzungsplan. Hier definieren Sie, **wie** das Feature gebaut wird.

**Syntax:**

```
/codexspec:spec-to-plan [path_to_spec.md]
```

**Argumente:**

| Argument | Erforderlich | Beschreibung |
|----------|----------|-------------|
| `path_to_spec.md` | Nein | Pfad zur Spec-Datei (wird aus `.codexspec/specs/` automatisch erkannt, falls nicht angegeben) |

**Was er passiert:**

- Liest Spezifikation und Verfassung
- Nimmt nur die technischen Details auf, die durch bestätigte Anforderungen und Repository-Randbedingungen benötigt werden
- Prüft anwendbare Verfassungsregeln, ohne optionale Konventionen zu Feature-Anforderungen zu erklären
- Fügt `Covers`-Links zu Spezifikations-Anforderungen hinzu
- Dokumentiert technische Entscheidungen mitsamt Begründung
- Hält an, wenn eine Entscheidung die bestätigte Intention verändern würde

**Was erstellt wird:**

```
.codexspec/
└── specs/
    └── 2026-0613-1200ab-task-management/
        └── plan.md    # Technischer Umsetzungsplan
```

**Beispiel:**

```text
You: /codexspec:spec-to-plan Use Python FastAPI for backend, React for frontend, PostgreSQL for database

AI:  Generating technical plan...

     Constitutionality Review:
     ✓ Clean Architecture: Modular design with clear boundaries
     ✓ TDD: Test-first approach enforced in phases
     ✓ Code Quality: Linting and type hints required

     Architecture:
     - Backend: FastAPI with layered architecture
     - Frontend: React with component structure
     - Database: PostgreSQL with migration strategy

     Module Dependency Graph:
     ┌─────────────┐
     │    API      │
     └──────┬──────┘
            │
     ┌──────▼──────┐
     │  Services   │
     └──────┬──────┘
            │
     ┌──────▼──────┐
     │    Data     │
     └─────────────┘

     ✓ Created plan.md
     5 Implementation Phases defined
```

**Tipps:**

- Ausführen, wenn die Spezifikation geprüft und stabil ist
- Anwendbare Verfassungsregeln sind verpflichtend; irrelevante Vorlagenkonventionen nicht
- Relevante Abschnitte je nach Projekttyp aufnehmen
- Plan prüfen, bevor es weiter zu den Aufgaben geht

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

**Was er passiert:**

- Legt Aufgaben mit jeweils einem prüfbaren Ergebnis an; eine Aufgabe darf mehrere eng verwandte Dateien berühren
- Verwendet test-first-Reihenfolge nur, wenn sie durch Plan, Verfassung, bestätigte Needs oder Risiko erforderlich ist
- Markiert Aufgaben nur dann mit `[P]`, wenn sie tatsächlich unabhängig sind
- Gibt exakte Dateipfade für jede Aufgabe an
- Fügt `Covers`-Links zu Plan- und Anforderungs-IDs hinzu

**Was erstellt wird:**

```
.codexspec/
└── specs/
    └── 2026-0613-1200ab-task-management/
        └── tasks.md    # Aufgaben-Aufschlüsselung
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

---

### `/codexspec:implement-tasks`

Führt die Umsetzungsaufgaben mit bedingtem TDD-Workflow aus. Arbeitet die Aufgabenliste systematisch ab.

**Syntax:**

```
/codexspec:implement-tasks [tasks_path]
/codexspec:implement-tasks [spec_path plan_path tasks_path]
```

**Argumente:**

| Argument | Erforderlich | Beschreibung |
|----------|----------|-------------|
| `tasks_path` | Nein | Pfad zu tasks.md (wird bei Bedarf automatisch erkannt) |
| `spec_path plan_path tasks_path` | Nein | Explizite Pfade zu allen drei Dokumenten |

**Dateiauflösung:**

- **Keine Argumente**: Automatische Erkennung aus `.codexspec/specs/`
- **Ein Argument**: Wird als Pfad zu `tasks.md` behandelt, die anderen werden aus demselben Verzeichnis abgeleitet
- **Drei Argumente**: Explizite Pfade zu spec.md, plan.md und tasks.md

**Was er passiert:**

- Liest tasks.md und identifiziert offene Aufgaben
- Wendet den TDD-Workflow auf Code-Aufgaben an:
  - **Red**: Zunächst fehlschlagende Tests schreiben
  - **Green**: So implementieren, dass die Tests durchlaufen
  - **Verify**: Alle Tests ausführen
  - **Refactor**: Verbessern, während die Tests grün bleiben
- Direkte Umsetzung bei nicht testbaren Aufgaben (Doku, Konfiguration)
- Aktualisiert die Checkboxen der Aufgaben mit dem Fortschritt
- Hält Blocker in issues.md fest, falls welche auftreten

**TDD-Workflow für Code-Aufgaben:**

```
Red → Green → Verify → Refactor → Mark Complete
```

**Direkte Umsetzung bei Nicht-Testbarem:**

- Dokumentationsdateien
- Konfigurationsdateien
- Statische Assets
- Infrastrukturdateien

**Beispiel:**

```text
You: /codexspec:implement-tasks

AI:  Starting implementation...

     Loading context:
     - spec.md ✓
     - plan.md ✓
     - tasks.md ✓
     - constitution.md ✓

     Tech Stack: Python 3.11+ / FastAPI / PostgreSQL / pytest

     Working on Task 1.1: Setup Project Structure
     ✓ Created src/taskman/__init__.py
     ✓ Created pyproject.toml
     [x] Task 1.1 Complete

     Working on Task 2.1: Write Tests for Task Entity [P]
     ✓ Created tests/test_task.py
     Running tests... 5 passed (all expected failures)
     [x] Task 2.1 Complete

     Working on Task 2.2: Implement Task Entity
     ✓ Created src/taskman/models/task.py
     Running tests... 5 passed
     [x] Task 2.2 Complete

     ...
```

**Tipps:**

- Kann nach einer Unterbrechung dort weitermachen, wo aufgehört wurde
- Blocker werden in issues.md festgehalten
- Commits erfolgen nach bedeutenden Aufgaben/Phasen
- Vorab `/codexspec:review-tasks` zur Validierung ausführen

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

**Was er passiert:**

- Prüft die Treue gegenüber den Einträgen der bestätigten `requirements.md`
- Prüft interne Konsistenz, Klarheit und Überprüfbarkeit
- Behandelt einen fehlenden Vorlagenabschnitt nur dann als Defekt, wenn verbindlicher Inhalt ihn verlangt
- Verlangt für jeden Defekt die Felder `Evidence`, `Location`, `Mismatch`, `Impact` und `Remediation`
- Trennt `Risk Advisories / Design Opportunities` von Defekten
- Erzeugt einen Status sowie einen Kompatibilitäts-Score, der aus den klassifizierten Befunden abgeleitet wird

**Geteilter Review-Vertrag:**

| Kategorie | Bedeutung |
|----------|---------|
| Fidelity-Defekt | Konfligiert mit einer autoritativen Quelle oder lässt sie weg |
| Intrinsic-Defekt | Intern widersprüchlich, nicht durchführbar oder nicht überprüfbar |
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

- Vor `/codexspec:spec-to-plan` ausführen
- `BLOCKED` und `NEEDS_REVISION` bedeuten: nicht weiterfahren
- Advisories nicht zu Anforderungen hochstufen
- Nach Korrekturen erneut ausführen

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

**Was er passiert:**

- Verifiziert `Covers`-Links und die erforderliche Spec-Abdeckung
- Prüft anwendbare Verfassungsregeln und Repository-Fakten
- Markiert unbegründete Komplexität nur, wenn sie konkrete Kosten oder Konflikte erzeugt
- Verlangt für jeden Defekt die Evidenz-Felder und fasst Befunde mit derselben Ursache zusammen
- Weist optionale Architektur-Verbesserungen als Advisories aus
- Nutzt den geteilten Status- und Kompatibilitäts-Score-Vertrag

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

**Was er passiert:**

- Prüft, ob alle erforderlichen Plan-Posten und Anforderungen durch Aufgaben abgedeckt sind
- Validiert test-first-Reihenfolge nur dort, wo eine autoritative Quelle sie verlangt
- Verifiziert, dass jede Aufgabe genau ein überprüfbares Ergebnis hat
- Validiert Abhängigkeiten (keine Zyklen, korrekte Reihenfolge)
- Prüft die Parallelisierungs-Marker
- Validiert Dateipfade
- Verlangt für jeden Defekt die Evidenz-Felder
- Weist optionale Prozess-Verbesserungen als Advisories aus
- Nutzt den geteilten Status- und Kompatibilitäts-Score-Vertrag

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

### `/codexspec:analyze`

Führt eine zerstörungsfreie Konsistenzanalyse über requirements.md, spec.md, plan.md und tasks.md durch. Erkennt Autoritätskonflikte, Traceability-Lücken, Duplikate und fehlende Abdeckung.

**Syntax:**

```
/codexspec:analyze
```

**Argumente:**

| Argument | Erforderlich | Beschreibung |
|----------|----------|-------------|
| Keine | – | Analysiert die Artefakte des aktuellen Features |

**Was er passiert:**

- Erkennt Duplikate über Artefakte hinweg
- Identifiziert Mehrdeutigkeiten ohne messbare Kriterien
- Findet zu schwach spezifizierte Posten
- Prüft die Verfassungs-Konformität
- Bildet die Abdeckung von Anforderungen auf Aufgaben ab
- Meldet Inkonsistenzen in Terminologie und Reihenfolge

**Severity-Stufen:**

| Stufe | Definition |
|-------|------------|
| **CRITICAL** | Verfassungsverstoß, fehlendes Kern-Artefakt, null Abdeckung |
| **HIGH** | Doppelte/konfligierende Anforderung, mehrdeutiges Sicherheitsattribut |
| **MEDIUM** | Terminologie-Drift, fehlende nicht-funktionale Abdeckung |
| **LOW** | Stil-/Worting-Verbesserungen |

**Beispiel:**

```text
You: /codexspec:analyze

AI:  Analyzing artifacts...

     # Specification Analysis Report

     ## Coverage Summary
     | Requirement Key | Has Task? | Task IDs |
     |-----------------|-----------|----------|
     | REQ-001 | ✅ | 2.1, 2.2 |
     | REQ-002 | ✅ | 2.3, 2.4 |
     | REQ-003 | ❌ | None |

     ## Issues Found

     | ID | Category | Severity | Summary |
     |----|----------|----------|---------|
     | A1 | Coverage | CRITICAL | REQ-003 has no task coverage |
     | A2 | Duplication | HIGH | REQ-005 and REQ-008 overlap |
     | A3 | Ambiguity | MEDIUM | NFR-002 "secure" not defined |

     ## Metrics
     - Total Requirements: 12
     - Total Tasks: 24
     - Coverage: 92% (11/12 requirements)
     - Critical Issues: 1

     ## Next Actions
     1. Add tasks for REQ-003 (CRITICAL)
     2. Consider merging REQ-005 and REQ-008
     3. Define "secure" in NFR-002

     Resolve CRITICAL issues before /codexspec:implement-tasks
```

**Tipps:**

- Nach `/codexspec:plan-to-tasks`, vor der Umsetzung ausführen
- CRITICAL-Befunde sollten die Umsetzung blockieren
- Nur-lesend – es werden keine Dateien verändert
- Befunde nutzen, um die Artefaktqualität zu verbessern

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

**Was er passiert:**

- Erzeugt nach Qualitätsdimensionen gegliederte Checklisten
- Legt die Checklisten im Verzeichnis `FEATURE_DIR/checklists/` ab
- Die Posten konzentrieren sich auf die Qualität der Anforderungen, nicht auf Umsetzungstests

**Qualitätsdimensionen:**

- **Requirement Completeness**: Sind alle notwendigen Anforderungen vorhanden?
- **Requirement Clarity**: Sind die Anforderungen spezifisch und eindeutig?
- **Requirement Consistency**: Sind die Anforderungen ohne Widersprüche aufeinander abgestimmt?
- **Acceptance Criteria Quality**: Sind die Erfolgskriterien messbar?
- **Scenario Coverage**: Sind alle Abläufe/Fälle abgedeckt?
- **Edge Case Coverage**: Sind die Randbedingungen definiert?
- **Non-Functional Requirements**: Sind Performance, Security, Accessibility spezifiziert?
- **Dependencies & Assumptions**: Sind sie dokumentiert?

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

**Was er passiert:**

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

---

### `/codexspec:commit-staged`

Erzeugt eine Conventional-Commits-konforme Commit-Nachricht auf Basis gestagter Git-Änderungen mit Berücksichtigung des Session-Kontexts. Dieser Befehl versteht Ihre Entwicklungssession und liefert dadurch aussagekräftige Commit-Nachrichten.

**Syntax:**

```
/codexspec:commit-staged [-p]
```

**Argumente:**

| Argument | Erforderlich | Beschreibung |
|----------|----------|-------------|
| `-p` | Nein | Vorschau-Modus – Nachricht anzeigen, ohne zu committen |

**Was er passiert:**

- Führt `git diff --staged` aus, um die gestagten Änderungen zu holen
- Analysiert Änderungen und Session-Kontext, um die Intention zu erfassen
- Folgt der Conventional-Commits-Spezifikation
- Im Ausführungs-Modus (Standard): committet sofort nach der Erzeugung der Nachricht
- Im Vorschau-Modus (`-p`): zeigt die Nachricht, ohne zu committen
- Meldet einen Fehler, wenn keine gestagten Änderungen vorliegen

**Beispiel:**

```text
You: /codexspec:commit-staged

AI:  Analyzing staged changes...

     Files staged:
     - src/auth/service.py
     - tests/test_auth.py

     Generated commit message:
     feat(auth): implement token refresh logic

     - Add refresh token generation
     - Include token expiration handling
     - Add tests for refresh flow

     Executing commit...

     ✓ Committed: def5678
```

**Beispiel Vorschau-Modus:**

```text
You: /codexspec:commit-staged -p

AI:  Preview mode - no commit will be executed

     Suggested commit message:
     feat(auth): implement token refresh logic

     - Add refresh token generation
     - Include token expiration handling
     - Add tests for refresh flow
```

**Tipps:**

- Änderungen vorher mit `git add` stagen
- Analysiert nur die gestagten Inhalte – respektiert den zweistufigen Commit-Workflow von Git
- Berücksichtigt den Session-Kontext für aussagekräftige Commit-Nachrichten
- Flag `-p` nutzen, um vor dem Committen eine Vorschau zu sehen
- Folgt standardmäßig der Conventional-Commits-Spezifikation

---

### `/codexspec:review-code`

Prüft Code in jeder beliebigen Sprache auf idiomatische Klarheit, Korrektheit, Robustheit, Architektur und Verfassungskonformität.

**Syntax:**

```
/codexspec:review-code [path...]
```

**Argumente:**

| Argument | Erforderlich | Beschreibung |
|----------|----------|-------------|
| `path...` | Nein | Eine oder mehrere zu prüfende Quelldateien oder Verzeichnisse (leerzeichengetrennt). Default ist `src/`, falls weggelassen |

**Was er passiert:**

- Erkennt die Primärsprache(n) anhand der Dateierweiterungen und fährt bei gemischtsprachigen Zielen mit einem separaten Durchlauf pro Sprache fort
- Startet statische Analyse-Werkzeuge, wenn deren Konfiguration vorhanden ist (`ruff`/`mypy`, `eslint`/`tsc`, `go vet`/`gofmt`, `cargo check`/`cargo clippy`, `shellcheck`); bricht sonst graceful ab und meldet reduzierte Abdeckung
- Bewertet vier Dimensionen: Idiomatic Clarity & Simplicity, Correctness & Explicit Contracts, Runtime Robustness & Resource Discipline sowie Architecture & Design Integrity
- Blendet für erkannte Frameworks verpflichtende Unterabschnitte ein (z. B. Hooks Compliance bei React, Ownership & Borrowing bei Rust, Goroutine & Context Discipline bei Go, Memory & Lifetime Safety bei C/C++, Execution Safety bei Shell)
- Gleicht Befunde gegen `.codexspec/memory/constitution.md` ab, falls vorhanden; fehlt sie, entfällt die Verfassungs-Achse und ihr Gewicht wird umverteilt
- Klassifiziert Befunde nach Schweregrad: CRITICAL, HIGH, MEDIUM, LOW (LOW-Hinweise sind auf maximal 5 Punkte Gesamt-Abzug begrenzt)

**Beispiel:**

```text
You: /codexspec:review-code src/

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
- Bei reinen Python- oder React-Projekten bevorzugt `/codexspec:review-python-code` bzw. `/codexspec:review-react-code` für tiefergehende, sprachspezifische Prüfungen verwenden
- Nach Korrekturen erneut laufen lassen, um zu bestätigen, dass der Score sich erholt (≥ 95 erwartet, sobald die CRITICAL/HIGH-Befunde behoben sind)

---

### `/codexspec:review-python-code`

Prüft Python-Code auf PEP-8-Konformität, Typsicherheit, technische Robustheit und Verfassungs Konsistenz.

**Syntax:**

```
/codexspec:review-python-code [path...]
```

**Argumente:**

| Argument | Erforderlich | Beschreibung |
|----------|----------|-------------|
| `path...` | Nein | Eine oder mehrere zu prüfende Python-Dateien oder -Verzeichnisse (leerzeichengetrennt). Default ist `src/`, falls weggelassen |

**Was er passiert:**

- Führt `ruff check` für PEP-8-/Linting-Ergebnisse und `mypy` für die Typprüfung aus
- Begutachtet vier Python-spezifische Dimensionen: Pythonic & KISS Principle, Type Safety & Explicitness, Engineering Robustness und Constitution Alignment
- Prüft die Vollständigkeit von Typ-Annotationen, den Umgang mit breiten Exceptions und den Erhalt des Kontexts via `raise ... from err`
- Validiert Ressourcen-Management (`with`-Context-Manager), die Korrektheit von async/await und eine disziplinierte, strukturierte `logging`-Nutzung
- Gleicht Befunde gegen die MUST/SHOULD-Prinzipien in `.codexspec/memory/constitution.md` ab, falls vorhanden
- Klassifiziert Befunde nach Schweregrad: CRITICAL (Verstöße gegen MUST der Verfassung, Logik-Bugs, Sicherheitslücken), HIGH (Typsicherheits-Lücken, ruff/mypy-Fehler, Ressourcen-Lecks), MEDIUM (Design-/Refactor-Potenzial, fehlende Annotationen), LOW (Lesbarkeit, Pythonic Sugar)

**Beispiel:**

```text
You: /codexspec:review-python-code src/codexspec/

AI:  # Python Code Review Report

     ## Static Analysis
     | Tool  | Status | Issues |
     |-------|--------|--------|
     | ruff  | Pass   | 0      |
     | mypy  | Pass   | 0      |

     ## Findings
     ### Warnings (HIGH)
     - [ ] [CODE-002] src/codexspec/__init__.py:218 - public function missing return type annotation
       Suggestion: add the return type and verify with mypy.

     ### Suggestions (LOW)
     - [ ] [CODE-004] src/codexspec/cli.py:140 - use `pathlib.Path` instead of `os.path` string concatenation
```

**Tipps:**

- Stattdessen verwenden, wenn das Ziel nur Python ist und Sie PEP-8-/Typsicherheits-Tiefe wollen (statt `/codexspec:review-code`)
- `ruff` und `mypy` müssen im Zielprojekt installiert und konfiguriert sein, um die volle Abdeckung zu erreichen; bei Fehlen meldet der Befehl reduzierte Abdeckung
- MUST-Prinzipien der Verfassung werden gewertet; sprachagnostische Meta-Prinzipien (Testbarkeit, Einfachheit) greifen, wenn keine Verfassung existiert

---

### `/codexspec:review-react-code`

Prüft React-/TypeScript-Code auf Komponentenarchitektur, Hooks-Regeln, State-Management, Performance und Verfassungs Konsistenz.

**Syntax:**

```
/codexspec:review-react-code [path...]
```

**Argumente:**

| Argument | Erforderlich | Beschreibung |
|----------|----------|-------------|
| `path...` | Nein | Eine oder mehrere zu prüfende React-/TypeScript-Dateien oder -Verzeichnisse (leerzeichengetrennt; erwartet `.tsx`, `.ts`, `.jsx`, `.js`). Default ist `src/`, falls weggelassen |

**Was er passiert:**

- Führt `npx eslint` aus (wenn eine ESLint-Konfiguration existiert) und `npx tsc --noEmit` (wenn ein `tsconfig.json` existiert)
- Begutachtet vier React-spezifische Dimensionen: Component Atomicity & Single Responsibility, Hooks Compliance & Side-Effects Management, State Management & Data Flow sowie Performance & Robustness
- Verifiziert, dass `useEffect`-Dependency-Arrays erschöpfend sind, erkennt den Missbrauch von abgeleitetem State als State und markiert unnötige Effects
- Prüft auf Stale-Closure-Risiken, fehlendes Effect-Cleanup, Prop-Drilling, unmemorisierte teure Renders sowie fehlende Loading-/Error-Zustände
- Gleicht Befunde gegen `.codexspec/memory/constitution.md` ab, falls vorhanden
- Klassifiziert Befunde nach Schweregrad: CRITICAL (Verstöße gegen Hooks-Regeln, Race Conditions), HIGH (fehlendes Cleanup, unbehandelte Promise-Rejections), MEDIUM (Refactor-Kandidaten), LOW (Lesbarkeit)

**Beispiel:**

```text
You: /codexspec:review-react-code src/components/

AI:  # React Code Review Report

     ## Static Analysis
     | Tool  | Status | Issues |
     |-------|--------|--------|
     | eslint| Warn   | 2      |
     | tsc   | Pass   | 0      |

     ## Findings
     ### Critical Issues (CRITICAL)
     - [ ] [CODE-001] src/components/UserProfile.tsx:38 - `useEffect` missing `userId` in dependency array
       Impact: stale closure fetches the wrong user after navigation.
       Suggestion: add `userId` to the dependency array or extract to a custom hook.

     ### Suggestions (LOW)
     - [ ] [CODE-004] src/components/Button.tsx:12 - extract derived value instead of `useState`
```

**Tipps:**

- Stattdessen verwenden, wenn das Ziel nur React/TypeScript ist und Sie Hooks-/Komponentenarchitektur-Tiefe wollen (statt `/codexspec:review-code`)
- Für die volle Abdeckung sollten sowohl ESLint als auch ein `tsconfig.json` vorhanden sein; bei Fehlen meldet der Befehl reduzierte Abdeckung
- React-Befunde lagern sich auf die generischen TypeScript-Prüfungen auf, sodass Typsicherheits-Probleme weiterhin sichtbar werden

---

### `/codexspec:quick`

Fährt einen gestrafften Requirements-First-SDD-Ablauf für kleine Änderungen.

**Syntax:**

```
/codexspec:quick [describe a small requirement]
```

**Argumente:**

| Argument | Erforderlich | Beschreibung |
|----------|----------|-------------|
| `describe a small requirement` | Nein | Kurze Beschreibung der kleinen, sauber abgegrenzten Änderung (wird bei Bedarf abgefragt) |

**Was er passiert:**

- Bewertet den Umfang (berührte Dateien, Modul-Spanne, neue Abhängigkeiten, ungelöste Produktentscheidungen) und empfiehlt bei breiten Änderungen oder mehreren unabhängigen Ergebnissen den Standard-Ablauf
- Legt einen Feature-Workspace und `requirements.md` mit derselben Zeitstempel-Konvention wie `/codexspec:specify` an
- Löst nur die Mehrdeutigkeiten auf, die die Umsetzung materiell verändern; präsentiert eine kompakte bestätigte Zusammenfassung (`NEED-*`, relevante `CON-*`/`DEC-*`, `OUT-*`, ungelöste `OPEN-*`)
- Hält am Confirmation Gate: Es wird nichts erzeugt, bevor Sie die Zusammenfassung bestätigen
- Kettenet die Generierungs-Befehle gegen das neue Feature-Verzeichnis: `/codexspec:generate-spec`, `/codexspec:spec-to-plan`, `/codexspec:plan-to-tasks`, `/codexspec:implement-tasks`
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

AI:  Running generate-spec → spec-to-plan → plan-to-tasks → implement-tasks ...

     ✓ Feature dir: .codexspec/specs/2026-0713-0915ab-remember-me/
     ✓ All reviews PASS_WITH_WARNINGS or higher
     ✓ Implementation verified
     Open advisories: none
```

**Tipps:**

- Quick genuinely kleinen, eindeutigen Änderungen vorbehalten; andernfalls `/codexspec:specify` und den Standard-Ablauf verwenden
- Eine Bestätigung ist weiterhin nötig – Quick leitet nie eine Produktentscheidung ab, nur um die Automatisierung am Laufen zu halten
- Wenn ein Generierungs-Review `NEEDS_REVISION`/`BLOCKED` liefert, hält Quick an und gibt die Kontrolle an Sie zurück

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

**Was er passiert:**

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
- Siehe die [Fallstudie zum PR-Beschreibungs-Generator](../case-studies/case-study-pr-description-generator.md) für ein durchgespieltes, end-to-end-Beispiel dieses Befehls (inklusive Einbindung des spec.md-Kontexts)

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

**Was er passiert:**

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

You: Output language (base) → zh-CN

AI:  ✓ Updated language.output: "zh-CN"
     (interaction and document fall back to output, then en.)
```

**Tipps:**

- `/codexspec:config --view` verwenden, um den aktuellen Zustand zu inspizieren, bevor etwas geändert wird
- Eine frische oder zurückgesetzte Konfiguration schreibt nur `output`; `interaction`/`document` nur setzen, wenn sie von `output` abweichen sollen
- Für skriptgesteuerte Änderungen im Terminal ist die CLI `codexspec config` vorzuziehen (`--set-lang`, `--set-interaction-lang`, `--set-document-lang`, `--set-commit-lang`, `--auto-next`)

---

## Workflow Overview

```text
Idea → /specify → requirements.md → /generate-spec → spec.md → /spec-to-plan → plan.md → /plan-to-tasks → tasks.md → /implement
                                                   │                         │                            │
                                              Review spec               Review plan                  Review tasks
```

Jedes Review ist ein menschliches Checkpoint. Es validiert Treue und inhärente Qualität anhand evidenzbasierter Befunde. Advisory-Hinweise zu Designfragen bleiben separat und blockieren niemals das Weiterkommen. Bestätigte Defekte dürfen repariert und erneut geprüft werden – über maximal zwei Runden.

---

## Troubleshooting

### „Feature directory not found"

Der Befehl konnte das Feature-Verzeichnis nicht finden.

**Lösungen:**

- Zuerst `codexspec init` ausführen, um das Projekt zu initialisieren
- Prüfen, ob das Verzeichnis `.codexspec/specs/` existiert
- Sicherstellen, dass Sie im korrekten Projektverzeichnis sind
- Bei mehreren Kandidaten ein explizites Feature-Verzeichnis oder einen Artefakt-Pfad übergeben

### „No spec.md found"

Die Spezifikationsdatei existiert noch nicht.

**Lösungen:**

- Zuerst `/codexspec:specify` ausführen, um die Anforderungen zu klären
- Dann `/codexspec:generate-spec` ausführen, um spec.md anzulegen

### „Constitution not found"

Es existiert keine Projektverfassung.

**Lösungen:**

- `/codexspec:constitution` ausführen, um eine anzulegen
- Die Verfassung ist optional, wird aber für konsistente Entscheidungen empfohlen

### „Tasks file not found"

Die Aufgaben-Aufschlüsselung existiert nicht.

**Lösungen:**

- Sicherstellen, dass zuerst `/codexspec:spec-to-plan` ausgeführt wurde
- Danach `/codexspec:plan-to-tasks` ausführen, um tasks.md anzulegen

### „GitHub CLI not authenticated"

Der Befehl `/codexspec:tasks-to-issues` erfordert eine GitHub-Authentifizierung.

**Lösungen:**

- GitHub CLI installieren: `brew install gh` (macOS) oder Äquivalent
- Authentifizieren: `gh auth login`
- Verifizieren: `gh auth status`

---

## Next Steps

- [Workflow](workflow.md) – Häufige Muster und der Einsatzort der einzelnen Befehle
- [CLI](../reference/cli.md) – Terminal-Befehle zur Projektinitialisierung
