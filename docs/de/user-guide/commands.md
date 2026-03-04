# Befehle

Dies ist die Referenz fuer CodexSpecs Slash-Befehle. Diese Befehle werden in Claude Codes Chat-Interface aufgerufen.

Fuer Workflow-Muster und wann jeder Befehl zu verwenden ist, siehe [Workflow](workflow.md). Fuer CLI-Befehle siehe [CLI](../reference/cli.md).

## Schnellreferenz

| Befehl | Zweck |
|---------|---------|
| `/codexspec.constitution` | Projekt-Verfassung erstellen oder aktualisieren mit artefaktuebergreifender Validierung |
| `/codexspec.specify` | Anforderungen durch interaktives Q&A klaeren |
| `/codexspec.generate-spec` | spec.md-Dokument aus geklaerten Anforderungen generieren |
| `/codexspec.clarify` | Bestehende Spec auf Unklarheiten scannen (iterative Verfeinerung) |
| `/codexspec.spec-to-plan` | Spezifikation in technischen Implementierungsplan konvertieren |
| `/codexspec.plan-to-tasks` | Plan in atomare, TDD-erzwungene Aufgaben aufteilen |
| `/codexspec.implement-tasks` | Aufgaben mit bedingtem TDD-Workflow ausfuehren |
| `/codexspec.review-spec` | Spezifikation auf Vollstaendigkeit und Qualitaet validieren |
| `/codexspec.review-plan` | Technischen Plan auf Machbarkeit und Ausrichtung ueberpruefen |
| `/codexspec.review-tasks` | Aufgabenaufteilung auf TDD-Konformitaet validieren |
| `/codexspec.analyze` | Artefaktuebergreifende Konsistenzanalyse (nur Lesen) |
| `/codexspec.checklist` | Qualitaetschecklisten fuer Anforderungen generieren |
| `/codexspec.tasks-to-issues` | Aufgaben in GitHub-Issues konvertieren |
| `/codexspec.commit` | Conventional-Commits-Nachrichten mit Sitzungskontext generieren |
| `/codexspec.commit-staged` | Commit-Nachricht aus gestageten Aenderungen generieren |

---

## Befehlskategorien

### Kern-Workflow-Befehle

Befehle fuer den primaeren SDD-Workflow: Verfassung → Spezifikation → Plan → Aufgaben → Implementierung.

### Ueberpruefungsbefehle (Qualitaetsgate)

Befehle, die Artefakte in jeder Workflow-Phase validieren. **Empfohlen vor dem Fortfahren zur naechsten Phase.**

### Erweiterte Befehle

Befehle fuer iterative Verfeinerung, artefaktuebergreifende Validierung und Projektmanagement-Integration.

---

## Befehlsreferenz

### `/codexspec.constitution`

Die Projektverfassung erstellen oder aktualisieren. Die Verfassung definiert Architekturprinzipien, Technologie-Stack, Code-Standards und Governance-Regeln, die alle nachfolgenden Entwicklungsentscheidungen leiten.

**Syntax:**
```
/codexspec.constitution [Prinzipien-Beschreibung]
```

**Argumente:**
| Argument | Erforderlich | Beschreibung |
|----------|----------|-------------|
| `Prinzipien-Beschreibung` | Nein | Beschreibung der einzubeziehenden Prinzipien (wird abgefragt, falls nicht angegeben) |

**Was es tut:**
- Erstellt `.codexspec/memory/constitution.md`, falls nicht vorhanden
- Aktualisiert bestehende Verfassung mit neuen Prinzipien
- Validiert artefaktuebergreifende Konsistenz mit Vorlagen
- Generiert Sync-Impact-Report mit Aenderungen und betroffenen Dateien
- Enthaelt Verfassungskonformitaetspruefung fuer abhaengige Vorlagen

**Was es erstellt:**
```
.codexspec/
└── memory/
    └── constitution.md    # Projekt-Governance-Dokument
```

**Beispiel:**
```text
Sie: /codexspec.constitution Fokus auf Codequalitaet, Test-Standards und Clean Architecture

KI:  Erstelle Verfassung...

     ✓ Erstellt .codexspec/memory/constitution.md
     Version: 1.0.0

     Sync-Impact-Report:
     - plan-template-*.md: ✅ ausgerichtet
     - spec-template-*.md: ✅ ausgerichtet
     - tasks-template-*.md: ✅ ausgerichtet

     Kernprinzipien:
     1. Codequalitaet zuerst
     2. Test-Driven Development
     3. Clean Architecture

     Vorgeschlagener Commit: docs: create constitution v1.0.0
```

**Tipps:**
- Definieren Sie Prinzipien frueh im Projekt fuer konsistente Entscheidungsfindung
- Schliessen Sie sowohl technische als auch Prozess-Prinzipien ein
- Ueberpruefen Sie die Verfassung vor wichtigen Feature-Entwicklungen
- Verfassungaenderungen loesen artefaktuebergreifende Validierung aus

---

### `/codexspec.specify`

Anforderungen durch interaktives Q&A klaeren. Dieser Befehl erkundet Ihre urspruengliche Idee, ohne Dateien zu erstellen – Sie behalten die volle Kontrolle.

**Syntax:**
```
/codexspec.specify [Ihre Idee oder Anforderung]
```

**Argumente:**
| Argument | Erforderlich | Beschreibung |
|----------|----------|-------------|
| `Ihre Idee oder Anforderung` | Nein | Urspruengliche Beschreibung dessen, was Sie bauen moechten (wird abgefragt, falls nicht angegeben) |

**Was es tut:**
- Stellt klaerende Fragen, um Ihre Idee zu verstehen
- Erkundet Randfaelle, die Sie moeglicherweise nicht beruecksichtigt haben
- Erarbeitet gemeinsam qualitativ hochwertige Anforderungen durch Dialog
- Fokussiert auf "Was" und "Warum", nicht auf technische Implementierung
- **Erstellt KEINE Dateien** – Sie entscheiden, wann Dokumentation erstellt wird

**Was es NICHT erstellt:**
- Keine Dateien werden waehrend dieses Befehls erstellt
- Anforderungen bleiben im Gespraech, bis Sie zustimmen

**Beispiel:**
```text
Sie: /codexspec.specify Ich moechte eine Task-Management-App bauen

KI:  Schoen! Helfen Ihnen, die Anforderungen zu klaeren.

     Zuerst, wer sind die Zielbenutzer fuer diese App?
     - Einzelne Fachkraefte
     - Kleine Teams
     - Unternehmen
     - Alle oben genannten

Sie: Kleine Teams, hauptsaechlich Software-Entwicklungsteams

KI:  Verstanden. Fuer kleine Dev-Teams:
     - Benoetigen Sie Echtzeit-Zusammenarbeitsfunktionen?
     - Sollten Tasks Untertasks unterstuetzen oder nur flache Listen?
     - Integrationsanforderungen (GitHub, Slack, etc.)?

Sie: Echtzeit ist wichtig. Untertasks ja. GitHub-Integration waere schoen.

KI:  [Fortfaehrt, Anforderungen zu erkunden...]

     Zusammenfassung der geklarten Anforderungen:
     - Ziel: Kleine Dev-Teams (5-20 Personen)
     - Kern: Tasks mit Untertasks, Echtzeit-Updates
     - Integration: GitHub (optional)
     - Prioritaet: Echtzeit-Zusammenarbeit > Untertasks > GitHub

     Bereit, das Spec-Dokument zu generieren?
     Verwenden Sie /codexspec.generate-spec, um spec.md zu erstellen
```

**Tipps:**
- Verwenden Sie fuer anfaengliche Anforderungserkundung
- Keine Sorge wegen Vollstaendigkeit – Verfeinerung ist iterativ
- Stellen Sie Fragen, wenn die KI Annahmen trifft
- Ueberpruefen Sie die Zusammenfassung vor der Spec-Generierung

---

### `/codexspec.generate-spec`

Das `spec.md`-Dokument aus geklarten Anforderungen generieren. Dieser Befehl fungiert als "Anforderungscompiler", der Ihre geklarten Anforderungen in eine strukturierte Spezifikation umwandelt.

**Syntax:**
```
/codexspec.generate-spec
```

**Argumente:**
| Argument | Erforderlich | Beschreibung |
|----------|----------|-------------|
| Keine | - | Verwendet Kontext aus vorheriger `/codexspec.specify`-Sitzung |

**Was es tut:**
- Erstellt Verzeichnis `.codexspec/specs/{NNN}-{feature-name}/`
- Generiert umfassendes `spec.md` mit:
  - Feature-Ueberblick und Ziele
  - User Stories mit Akzeptanzkriterien
  - Funktionale Anforderungen (REQ-XXX-Format)
  - Nicht-funktionale Anforderungen (NFR-XXX-Format)
  - Randfaelle und Behandlungsansaetze
  - Nicht im Scope liegende Elemente

**Was es erstellt:**
```
.codexspec/
└── specs/
    └── 001-task-management/
        └── spec.md
```

**Beispiel:**
```text
Sie: /codexspec.generate-spec

KI:  Generiere Spezifikation...

     ✓ Erstellt .codexspec/specs/001-task-management/spec.md

     Enthaltene Abschnitte:
     - Ueberblick: Task-Management fuer kleine Dev-Teams
     - 4 User Stories mit Akzeptanzkriterien
     - 12 Funktionale Anforderungen (REQ-001 bis REQ-012)
     - 3 Nicht-funktionale Anforderungen (NFR-001 bis NFR-003)
     - 5 Randfaelle dokumentiert
     - Nicht im Scope: Mobile-Apps, Enterprise-SSO

     Naechste Schritte:
     - Ueberpruefen Sie die Spec mit /codexspec.review-spec
     - Oder fahren Sie fort mit /codexspec.spec-to-plan
```

**Tipps:**
- Ausfuehren, nachdem `/codexspec.specify` Anforderungen geklaert hat
- Ueberpruefen Sie die generierte Spec vor dem Fortfahren
- Verwenden Sie `/codexspec.review-spec` fuer Qualitaetsvalidierung
- Bearbeiten Sie spec.md direkt, wenn kleinere Anpassungen noetig sind

---

### `/codexspec.clarify`

Eine bestehende Spezifikation auf Unklarheiten und Luecken scannen. Verwenden Sie dies fuer iterative Verfeinerung nach der anfaenglichen Spec-Erstellung.

**Syntax:**
```
/codexspec.clarify [pfad_zu_spec.md]
```

**Argumente:**
| Argument | Erforderlich | Beschreibung |
|----------|----------|-------------|
| `pfad_zu_spec.md` | Nein | Pfad zur Spec-Datei (automatisch erkannt, falls nicht angegeben) |

**Was es tut:**
- Scannt Spec mit 4 fokussierten Unklarheitskategorien
- Stellt gezielte Klaerungsfragen (maximal 5)
- Aktualisiert spec.md mit Klaerungsantworten
- Integriert review-spec-Ergebnisse, falls verfuegbar

**Unklarheitskategorien:**

| Kategorie | Was es erkennt |
|----------|-----------------|
| **Vollstaendigkeitsluecken** | Fehlende Abschnitte, leerer Inhalt, fehlende Akzeptanzkriterien |
| **Spezifitaetsprobleme** | Vage Begriffe ("schnell", "skalierbar"), undefinierte Einschraenkungen |
| **Verhaltensklarheit** | Fehlerbehandlungsluecken, undefinierte Zustandsuebergaenge |
| **Messbarkeitsprobleme** | Nicht-funktionale Anforderungen ohne Metriken |

**Beispiel:**
```text
Sie: /codexspec.clarify

KI:  Scanne spec.md auf Unklarheiten...

     Probleme in 3 Kategorien gefunden.

     ## Frage 1/5: Spezifitaet

     **Kontext**: NFR-001 besagt "System sollte schnell reagieren"

     **Frage**: Was ist die Zielantwortzeit?

     | Option | Beschreibung | Auswirkung |
     |--------|-------------|--------|
     | A | < 100ms fuer alle Operationen | Hohe Leistungsanforderung |
     | B | < 500ms fuer Lesezugriffe, < 1s fuer Schreibzugriffe | Ausgewogener Ansatz |
     | Custom | Geben Sie eine andere Antwort | - |

     **Empfehlung**: Option B – ausgewogen fuer typische Web-App

Sie: B

KI:  ✓ Aktualisiert NFR-001: Antwortzeit < 500ms Lesezugriffe, < 1s Schreibzugriffe
     Zum Clarifications-Abschnitt in spec.md hinzugefuegt
```

**Tipps:**
- Verwenden, wenn spec.md existiert, aber Verfeinerung benoetigt
- Integriert mit `/codexspec.review-spec`-Ergebnissen
- Maximal 5 Fragen pro Sitzung
- Mehrmals ausfuehren fuer komplexe Spezifikationen

---

### `/codexspec.spec-to-plan`

Die Feature-Spezifikation in einen technischen Implementierungsplan konvertieren. Hier definieren Sie, **wie** das Feature gebaut wird.

**Syntax:**
```
/codexspec.spec-to-plan [pfad_zu_spec.md]
```

**Argumente:**
| Argument | Erforderlich | Beschreibung |
|----------|----------|-------------|
| `pfad_zu_spec.md` | Nein | Pfad zur Spec-Datei (automatisch aus `.codexspec/specs/` erkannt, falls nicht angegeben) |

**Was es tut:**
- Liest Spezifikation und Verfassung
- Definiert Tech-Stack mit Versionseinschraenkungen
- Fuehrt Verfassungskonformitaetspruefung durch (obligatorisch, falls Verfassung existiert)
- Erstellt Architektur mit Modulabhaengigkeitsgraph
- Dokumentiert technische Entscheidungen mit Begruendung
- Plant Implementierungsphasen

**Was es erstellt:**
```
.codexspec/
└── specs/
    └── 001-task-management/
        └── plan.md    # Technischer Implementierungsplan
```

**Beispiel:**
```text
Sie: /codexspec.spec-to-plan Python FastAPI fuer Backend, React fuer Frontend, PostgreSQL fuer Datenbank verwenden

KI:  Generiere technischen Plan...

     Verfassungskonformitaetspruefung:
     ✓ Clean Architecture: Modulares Design mit klaren Grenzen
     ✓ TDD: Test-First-Ansatz in Phasen erzwungen
     ✓ Codequalitaet: Linting und Type-Hints erforderlich

     Architektur:
     - Backend: FastAPI mit geschichteter Architektur
     - Frontend: React mit Komponentenstruktur
     - Datenbank: PostgreSQL mit Migrationsstrategie

     Modulabhaengigkeitsgraph:
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

     ✓ Erstellt plan.md
     5 Implementierungsphasen definiert
```

**Tipps:**
- Ausfuehren, nachdem Spec ueberprueft und stabil ist
- Verfassungskonformitaetspruefung ist obligatorisch, falls Verfassung existiert
- Relevante Abschnitte basierend auf Projekttyp einbeziehen
- Plan ueberpruefen, bevor zu Aufgaben fortgefahren wird

---

### `/codexspec.plan-to-tasks`

Den technischen Plan in atomare, umsetzbare Aufgaben mit TDD-Erzwingung aufteilen.

**Syntax:**
```
/codexspec.plan-to-tasks [pfad_zu_spec.md pfad_zu_plan.md]
```

**Argumente:**
| Argument | Erforderlich | Beschreibung |
|----------|----------|-------------|
| `Pfade` | Nein | Pfade zu Spec und Plan (automatisch erkannt, falls nicht angegeben) |

**Was es tut:**
- Erstellt atomare Aufgaben (eine Primaerdatei pro Aufgabe)
- Erzwingt TDD: Testaufgaben gehen Implementierungsaufgaben voraus
- Markiert parallelisierbare Aufgaben mit `[P]`
- Spezifiziert exakte Dateipfade fuer jede Aufgabe
- Definiert Phasen-Checkpoints

**Was es erstellt:**
```
.codexspec/
└── specs/
    └── 001-task-management/
        └── tasks.md    # Aufgabenaufteilung
```

**Aufgabenstruktur:**
```markdown
### Aufgabe 2.1: Tests fuer Entity A schreiben [P]
- **Typ**: Testing
- **Dateien**: `tests/test_entity_a.py`
- **Beschreibung**: Unit-Tests fuer Entity A schreiben
- **Abhaengigkeiten**: Aufgabe 1.3
- **Geschaetzte Komplexitaet**: Niedrig
```

**Beispiel:**
```text
Sie: /codexspec.plan-to-tasks

KI:  Teile Plan in Aufgaben auf...

     ✓ Erstellt tasks.md
     Gesamt: 24 Aufgaben
     Parallelisierbar: 8 Aufgaben (33%)

     Phase 1: Fundament (4 Aufgaben)
     Phase 2: Kern-Implementierung - TDD (10 Aufgaben)
     Phase 3: Integration (4 Aufgaben)
     Phase 4: Schnittstellenebene (3 Aufgaben)
     Phase 5: Test & Dokumentation (3 Aufgaben)

     Ausfuehrungsreihenfolge:
     Phase 1 → [Phase 2 Aufgaben in parallelen Gruppen] → Phase 3 → Phase 4 → Phase 5

     Checkpoints an jeder Phasengrenze definiert.
```

**Tipps:**
- Jede Aufgabe sollte nur EINE Primaerdatei umfassen
- Testaufgaben gehen immer Implementierungsaufgaben voraus
- `[P]` markiert wirklich unabhaengige parallelisierbare Aufgaben
- Abhaengigkeiten vor Implementierung ueberpruefen

---

### `/codexspec.implement-tasks`

Implementierungsaufgaben mit bedingtem TDD-Workflow ausfuehren. Arbeitet systematisch die Aufgabenliste durch.

**Syntax:**
```
/codexspec.implement-tasks [tasks_pfad]
/codexspec.implement-tasks [spec_pfad plan_pfad tasks_pfad]
```

**Argumente:**
| Argument | Erforderlich | Beschreibung |
|----------|----------|-------------|
| `tasks_pfad` | Nein | Pfad zu tasks.md (automatisch erkannt, falls nicht angegeben) |
| `spec_pfad plan_pfad tasks_pfad` | Nein | Explizite Pfade zu allen drei Dokumenten |

**Dateiaufloesung:**
- **Keine Argumente**: Automatische Erkennung aus `.codexspec/specs/`
- **Ein Argument**: Als `tasks.md`-Pfad behandeln, andere aus demselben Verzeichnis ableiten
- **Drei Argumente**: Explizite Pfade zu spec.md, plan.md und tasks.md

**Was es tut:**
- Liest tasks.md und identifiziert unvollstaendige Aufgaben
- Wendet TDD-Workflow fuer Code-Aufgaben an:
  - **Red**: Zuerst fehlschlagende Tests schreiben
  - **Green**: Implementieren, um Tests zu bestehen
  - **Verify**: Alle Tests ausfuehren
  - **Refactor**: Verbessern, waehrend Tests gruen bleiben
- Direkte Implementierung fuer nicht-testbare Aufgaben (Docs, Config)
- Aktualisiert Aufgaben-Checkboxes waehrend der Arbeit
- Protokolliert Blocker in issues.md, falls aufgetreten

**TDD-Workflow fuer Code-Aufgaben:**
```
Red → Green → Verify → Refactor → Als komplett markieren
```

**Direkte Implementierung fuer Nicht-Testbare:**
- Dokumentationsdateien
- Konfigurationsdateien
- Statische Assets
- Infrastrukturdateien

**Beispiel:**
```text
Sie: /codexspec.implement-tasks

KI:  Starte Implementierung...

     Lade Kontext:
     - spec.md ✓
     - plan.md ✓
     - tasks.md ✓
     - constitution.md ✓

     Tech-Stack: Python 3.11+ / FastAPI / PostgreSQL / pytest

     Arbeite an Aufgabe 1.1: Projektstruktur einrichten
     ✓ Erstellt src/taskman/__init__.py
     ✓ Erstellt pyproject.toml
     [x] Aufgabe 1.1 komplett

     Arbeite an Aufgabe 2.1: Tests fuer Task-Entity schreiben [P]
     ✓ Erstellt tests/test_task.py
     Fuehre Tests aus... 5 bestanden (alle erwarteten Fehler)
     [x] Aufgabe 2.1 komplett

     Arbeite an Aufgabe 2.2: Task-Entity implementieren
     ✓ Erstellt src/taskman/models/task.py
     Fuehre Tests aus... 5 bestanden
     [x] Aufgabe 2.2 komplett

     ...
```

**Tipps:**
- Kann fortgesetzt werden, falls unterbrochen
- Blocker werden in issues.md protokolliert
- Commits werden nach bedeutenden Aufgaben/Phasen gemacht
- Zuerst `/codexspec.review-tasks` fuer Validierung ausfuehren

---

### `/codexspec.review-spec`

Die Spezifikation auf Vollstaendigkeit, Klarheit, Konsistenz und Bereitschaft fuer technische Planung validieren.

**Syntax:**
```
/codexspec.review-spec [pfad_zu_spec.md]
```

**Argumente:**
| Argument | Erforderlich | Beschreibung |
|----------|----------|-------------|
| `pfad_zu_spec.md` | Nein | Pfad zur Spec-Datei (automatisch erkannt, falls nicht angegeben) |

**Was es tut:**
- Prueft Vollstaendigkeit aller erforderlichen Abschnitte
- Bewertet Klarheit und Spezifitaet
- Verifiziert interne Konsistenz
- Beurteilt Testbarkeit der Anforderungen
- Prueft Verfassungsausrichtung
- Generiert bewerteten Ueberpruefungsbericht

**Ueberpruefungsdimensionen:**

| Dimension | Gewichtung | Was es validiert |
|-----------|--------|-------------------|
| Vollstaendigkeit | 25% | Alle Abschnitte vorhanden und substantiell |
| Klarheit | 25% | Keine vage Sprache, eindeutige Interpretationen |
| Konsistenz | 20% | Keine internen Widersprueche |
| Testbarkeit | 20% | Anforderungen koennen verifiziert werden |
| Verfassungsausrichtung | 10% | Richtet sich nach Projektprinzipien |

**Beispiel:**
```text
Sie: /codexspec.review-spec

KI:  Ueberpruefe Spezifikation...

     # Spezifikations-Ueberpruefungsbericht

     ## Zusammenfassung
     - **Gesamtstatus**: ⚠️ Ueberarbeitungsbedarf
     - **Qualitaetsbewertung**: 72/100
     - **Bereitschaft**: Ueberarbeitung erforderlich

     ## Abschnittsanalyse
     | Abschnitt | Status | Vollstaendigkeit | Qualitaet |
     |---------|--------|--------------|---------|
     | Ueberblick | ✅ | 100% | Hoch |
     | Ziele | ✅ | 100% | Hoch |
     | User Stories | ⚠️ | 80% | Mittel |
     | Funktionale Anforderungen | ✅ | 100% | Hoch |
     | Nicht-funktionale Anforderungen | ⚠️ | 50% | Mittel |
     | Randfaelle | ❌ | 0% | N/A |

     ## Kritische Probleme (Muss behoben werden)
     - [SPEC-001]: Randfaelle-Abschnitt ist leer
       - Auswirkung: Wichtige Fehlerszenarien koennten verpasst werden
       - Vorschlag: Mindestens 3-5 Randfaelle dokumentieren

     ## Warnungen (Sollte behoben werden)
     - [SPEC-002]: NFR-001 verwendet vagen Begriff "schnell"
       - Auswirkung: Kann ohne Metriken nicht verifiziert werden
       - Vorschlag: Konkrete Antwortzeit angeben

     ## Empfehlungen
     1. Randfaelle-Abschnitt mit Behandlungsansaetzen hinzufuegen
     2. Nicht-funktionale Anforderungen quantifizieren
     3. Akzeptanzkriterien zu User Story 3 hinzufuegen

     Verfuegbare Nachbereitung:
     - /codexspec.clarify - um Unklarheiten zu beheben
     - /codexspec.spec-to-plan - wenn Probleme geloest
```

**Tipps:**
- Vor `/codexspec.spec-to-plan` ausfuehren
- Kritische Probleme vor dem Fortfahren beheben
- Warnungen blockieren nicht, zeigen aber Risiko an
- Nach Korrekturen erneut ausfuehren

---

### `/codexspec.review-plan`

Den technischen Implementierungsplan auf Machbarkeit, Architekturqualitaet und Ausrichtung an der Spezifikation ueberpruefen.

**Syntax:**
```
/codexspec.review-plan [pfad_zu_plan.md]
```

**Argumente:**
| Argument | Erforderlich | Beschreibung |
|----------|----------|-------------|
| `pfad_zu_plan.md` | Nein | Pfad zur Plan-Datei (automatisch erkannt, falls nicht angegeben) |

**Was es tut:**
- Verifiziert, dass Spec-Anforderungen Plan-Abdeckung haben
- Bewertet Tech-Stack-Auswahlen
- Beurteilt Architekturentscheidungen
- Validiert Implementierungsphasen
- Prueft Verfassungsausrichtung
- Generiert bewerteten Ueberpruefungsbericht

**Ueberpruefungsdimensionen:**

| Dimension | Gewichtung | Was es validiert |
|-----------|--------|-------------------|
| Spec-Ausrichtung | 30% | Alle Anforderungen haben Implementierung |
| Tech-Stack | 15% | Angemessene Technologieauswahlen |
| Architekturqualitaet | 25% | Solides Design und Muster |
| Phasenplanung | 15% | Logische und realistische Phasen |
| Verfassungsausrichtung | 15% | Folgt Projektprinzipien |

**Beispiel:**
```text
Sie: /codexspec.review-plan

KI:  Ueberpruefe technischen Plan...

     # Plan-Ueberpruefungsbericht

     ## Zusammenfassung
     - **Gesamtstatus**: ✅ Bestanden
     - **Qualitaetsbewertung**: 85/100
     - **Bereitschaft**: Bereit fuer Aufgabenaufteilung

     ## Spec-Ausrichtung
     | Anforderung | Abdeckung | Status |
     |-------------|----------|--------|
     | REQ-001 bis REQ-012 | ✅ Voll | Alle abgedeckt |
     | US-001 bis US-004 | ✅ Voll | Alle abgedeckt |
     | NFR-001 bis NFR-003 | ⚠️ Teilweise | Caching nicht detailliert |

     ## Architektur-Ueberpruefung
     Staerken:
     - Saubere Trennung der Zuständigkeiten
     - Gut definierte Modulgrenzen
     - Angemessene Designmuster

     Bedenken:
     - Fehlende Fehlerbehandlungsstrategie-Dokumentation

     ## Verfassungsausrichtung
     | Prinzip | Compliance |
     |-----------|------------|
     | Clean Architecture | ✅ |
     | TDD | ✅ |
     | Codequalitaet | ✅ |

     Bereit fuer /codexspec.plan-to-tasks
```

**Tipps:**
- Vor `/codexspec.plan-to-tasks` ausfuehren
- Kritische Probleme sollten geloest werden
- Verwenden, um Architekturprobleme frueh zu erkennen
- Verifizieren, dass Tech-Stack mit Team-Faehigkeiten uebereinstimmt

---

### `/codexspec.review-tasks`

Die Aufgabenaufteilung auf Vollstaendigkeit, TDD-Konformitaet, korrekte Reihenfolge und korrekte Abhaengigkeiten validieren.

**Syntax:**
```
/codexspec.review-tasks [pfad_zu_tasks.md]
```

**Argumente:**
| Argument | Erforderlich | Beschreibung |
|----------|----------|-------------|
| `pfad_zu_tasks.md` | Nein | Pfad zur Aufgaben-Datei (automatisch erkannt, falls nicht angegeben) |

**Was es tut:**
- Prueft, ob alle Plan-Elemente Aufgaben-Abdeckung haben
- Validiert TDD-Konformitaet (Tests vor Implementierung)
- Verifiziert Aufgabengranularitaet (atomar, Fokus auf einzelne Datei)
- Validiert Abhaengigkeiten (keine Zyklen, korrekte Reihenfolge)
- Ueberprueft Parallelisierungsmarkierungen
- Validiert Dateipfade

**Ueberpruefungsdimensionen:**

| Dimension | Gewichtung | Was es validiert |
|-----------|--------|-------------------|
| Plan-Abdeckung | 30% | Alle Plan-Elemente haben Aufgaben |
| TDD-Konformitaet | 25% | Test-First-Workflow erzwungen |
| Abhaengigkeit & Reihenfolge | 20% | Korrekte Abhaengigkeiten, keine Zyklen |
| Aufgabengranularitaet | 15% | Atomar, angemessener Umfang |
| Parallelisierung & Dateien | 10% | Korrekte Markierungen und Pfade |

**Beispiel:**
```text
Sie: /codexspec.review-tasks

KI:  Ueberpruefe Aufgabenaufteilung...

     # Aufgaben-Ueberpruefungsbericht

     ## Zusammenfassung
     - **Gesamtstatus**: ⚠️ Ueberarbeitungsbedarf
     - **Qualitaetsbewertung**: 78/100
     - **Gesamtaufgaben**: 24
     - **Parallelisierbar**: 8 (33%)

     ## TDD-Konformitaet
     | Komponente | Testaufgabe | Test vor Impl | Status |
     |-----------|-----------|------------------|--------|
     | Task-Entity | ✅ | ✅ | ✅ |
     | User-Entity | ✅ | ✅ | ✅ |
     | TaskService | ❌ Fehlt | N/A | ❌ |

     ## TDD-Verstoesse
     - [TDD-001]: TaskService fehlt Testaufgabe

     ## Abhaengigkeitsprobleme
     - [DEP-001]: Aufgabe 2.5 als [P] markiert, haengt aber von 2.4 ab

     ## Empfehlungen
     1. Testaufgabe fuer TaskService vor Implementierung hinzufuegen
     2. Parallelisierungsmarkierung auf Aufgabe 2.5 korrigieren

     Probleme vor /codexspec.implement-tasks beheben
```

**Tipps:**
- Vor `/codexspec.implement-tasks` ausfuehren
- TDD-Verstoesse sind kritisch fuer Codequalitaet
- Pruefen, dass Parallelisierungsmarkierungen korrekt sind
- Verifizieren, dass Dateipfade mit Projektstruktur uebereinstimmen

---

### `/codexspec.analyze`

Eine zerstoerungsfreie artefaktuebergreifende Konsistenzanalyse ueber spec.md, plan.md und tasks.md durchfuehren. Identifiziert Inkonsistenzen, Duplikate und Abdeckungsluecken.

**Syntax:**
```
/codexspec.analyze
```

**Argumente:**
| Argument | Erforderlich | Beschreibung |
|----------|----------|-------------|
| Keine | - | Analysiert die Artefakte des aktuellen Features |

**Was es tut:**
- Erkennt Duplikate ueber Artefakte hinweg
- Identifiziert Unklarheiten ohne messbare Kriterien
- Findet unzureichend spezifizierte Elemente
- Prueft Verfassungsausrichtung
- Ordnet Anforderungsabdeckung zu Aufgaben
- Meldet Inkonsistenzen in Terminologie und Reihenfolge

**Schweregrade:**

| Stufe | Definition |
|-------|------------|
| **CRITICAL** | Verfassungsverletzung, fehlendes Kern-Artefakt, Null Abdeckung |
| **HIGH** | Doppelte/konfliktierende Anforderung, mehrdeutiges Sicherheitsattribut |
| **MEDIUM** | Terminologie-Drift, fehlende nicht-funktionale Abdeckung |
| **LOW** | Stil/Wortlaut-Verbesserungen |

**Beispiel:**
```text
Sie: /codexspec.analyze

KI:  Analysiere Artefakte...

     # Spezifikations-Analysebericht

     ## Abdeckungszusammenfassung
     | Anforderungsschluessel | Hat Aufgabe? | Aufgaben-IDs |
     |-----------------|-----------|----------|
     | REQ-001 | ✅ | 2.1, 2.2 |
     | REQ-002 | ✅ | 2.3, 2.4 |
     | REQ-003 | ❌ | Keine |

     ## Gefundene Probleme

     | ID | Kategorie | Schweregrad | Zusammenfassung |
     |----|----------|----------|---------|
     | A1 | Abdeckung | CRITICAL | REQ-003 hat keine Aufgabenabdeckung |
     | A2 | Duplikat | HIGH | REQ-005 und REQ-008 ueberlappen |
     | A3 | Unklarheit | MEDIUM | NFR-002 "sicher" nicht definiert |

     ## Metriken
     - Gesamtanforderungen: 12
     - Gesamtaufgaben: 24
     - Abdeckung: 92% (11/12 Anforderungen)
     - Kritische Probleme: 1

     ## Naechste Aktionen
     1. Aufgaben fuer REQ-003 hinzufuegen (CRITICAL)
     2. Erwaegen, REQ-005 und REQ-008 zusammenzufassen
     3. "sicher" in NFR-002 definieren

     CRITICAL-Probleme vor /codexspec.implement-tasks loesen
```

**Tipps:**
- Nach `/codexspec.plan-to-tasks` ausfuehren, vor Implementierung
- CRITICAL-Probleme sollten Implementierung blockieren
- Nur-Lese-Analyse – keine Dateien werden geaendert
- Erkenntnisse zur Verbesserung der Artefaktqualitaet verwenden

---

### `/codexspec.checklist`

Qualitaetschecklisten zur Validierung von Anforderungsvollstaendigkeit, -klarheit und -konsistenz generieren. Dies sind "Unit-Tests fuer das Schreiben von Anforderungen".

**Syntax:**
```
/codexspec.checklist [fokusbereich]
```

**Argumente:**
| Argument | Erforderlich | Beschreibung |
|----------|----------|-------------|
| `fokusbereich` | Nein | Domänenfokus (z.B. "ux", "api", "security", "performance") |

**Was es tut:**
- Generiert Checklisten, organisiert nach Qualitaetsdimensionen
- Erstellt Checklisten im `FEATURE_DIR/checklists/`-Verzeichnis
- Elemente fokussieren auf Anforderungsqualitaet, nicht Implementierungstests

**Qualitaetsdimensionen:**
- **Anforderungsvollstaendigkeit**: Sind alle notwendigen Anforderungen vorhanden?
- **Anforderungsklarheit**: Sind Anforderungen spezifisch und eindeutig?
- **Anforderungskonsistenz**: Richtet sich Anforderungen ohne Konflikte aus?
- **Akzeptanzkriterienqualitaet**: Sind Erfolgskriterien messbar?
- **Szenarioabdeckung**: Sind alle Ablaeufe/Faelle adressiert?
- **Randfallabdeckung**: Sind Randbedingungen definiert?
- **Nicht-funktionale Anforderungen**: Performance, Sicherheit, Barrierefreiheit spezifiziert?
- **Abhaengigkeiten & Annahmen**: Sind sie dokumentiert?

**Beispiel-Checklisten-Typen:**
- `ux.md` - Visuelle Hierarchie, Interaktionszustaende, Barrierefreiheit
- `api.md` - Fehlerformate, Rate-Limiting, Authentifizierung
- `security.md` - Datenschutz, Bedrohungsmodell, Verletzungsreaktion
- `performance.md` - Metriken, Lastbedingungen, Verschlechterung

**Beispiel:**
```text
Sie: /codexspec.checklist security

KI:  Generiere Security-Checkliste...

     ✓ Erstellt .codexspec/specs/001-task-management/checklists/security.md

     ## Security-Anforderungen Qualitaetscheckliste

     ### Authentifizierungsanforderungen
     - [ ] CHK001 - Sind Authentifizierungsanforderungen fuer alle geschuetzten Endpunkte definiert? [Vollstaendigkeit]
     - [ ] CHK002 - Ist Passwortkomplexitaet explizit spezifiziert? [Klarheit]
     - [ ] CHK003 - Sind Session-Timeout-Anforderungen quantifiziert? [Messbarkeit]

     ### Datenschutz
     - [ ] CHK004 - Sind Datenverschluesselungsanforderungen fuer Ruhedaten spezifiziert? [Vollstaendigkeit]
     - [ ] CHK005 - Sind Datenverschluesselungsanforderungen fuer Uebertragung spezifiziert? [Vollstaendigkeit]
     - [ ] CHK006 - Ist PII-Behandlung explizit dokumentiert? [Klarheit]

     Gesamt: 15 Elemente in 4 Kategorien
```

**Tipps:**
- Checklisten validieren Anforderungsqualitaet, nicht Implementierungskorrektheit
- Fuer Anforderungsueberpruefung und -verbesserung verwenden
- Domänenspezifische Checklisten fuer fokussierte Validierung erstellen
- Vor dem Fortfahren zur technischen Planung ausfuehren

---

### `/codexspec.tasks-to-issues`

Aufgaben aus `tasks.md` in GitHub-Issues fuer Projektverfolgung und Zusammenarbeit konvertieren.

**Syntax:**
```
/codexspec.tasks-to-issues
```

**Argumente:**
| Argument | Erforderlich | Beschreibung |
|----------|----------|-------------|
| Keine | - | Konvertiert alle Aufgaben des aktuellen Features |

**Was es tut:**
- Parst Aufgaben-IDs, Beschreibungen, Abhaengigkeiten und Dateipfade
- Erstellt GitHub-Issues mit strukturiertem Body
- Fuegt Labels basierend auf Aufgabentyp hinzu (setup, implementation, testing, documentation)
- Verknuepft Abhaengigkeiten zwischen Issues
- Meldet erstellte Issues mit URLs

**Voraussetzungen:**
- Git-Repository mit GitHub-Remote
- GitHub CLI (`gh`) installiert und authentifiziert
- `tasks.md`-Datei existiert

**Beispiel:**
```text
Sie: /codexspec.tasks-to-issues

KI:  Konvertiere Aufgaben zu GitHub-Issues...

     Repository: github.com/example/taskman

     Erstelle Issues:
     ✓ #42: Aufgabe 1.1 - Projektstruktur einrichten (setup)
     ✓ #43: Aufgabe 2.1 - Tests fuer Task-Entity schreiben (testing)
     ✓ #44: Aufgabe 2.2 - Task-Entity implementieren (implementation)
     ...

     Zusammenfassung:
     - Issues erstellt: 24
     - Labels angewendet: setup(4), implementation(12), testing(5), documentation(3)
     - Abhaengigkeiten verknuepft: 18

     Issues ansehen: https://github.com/example/taskman/issues
```

**Tipps:**
- Erfordert GitHub-CLI-Authentifizierung (`gh auth login`)
- Funktioniert nur mit GitHub-Repositories
- Erstellt Issues in der Standardkonfiguration des Repositories
- Vor dem Ausfuehren auf Duplikate pruefen

---

### `/codexspec.commit`

Eine Conventional-Commits-konforme Commit-Nachricht basierend auf Git-Status und Sitzungskontext generieren. Dieser Befehl ist kontextbewusst und behandelt verschiedene Git-Zustaende.

**Syntax:**
```
/codexspec.commit
```

**Argumente:**
| Argument | Erforderlich | Beschreibung |
|----------|----------|-------------|
| Keine | - | Analysiert aktuellen Git-Zustand und Sitzungskontext |

**Was es tut:**
- Sammelt Git-Kontext (Branch, Status, gestagete/ungestagete Aenderungen)
- Analysiert Sitzungsgespraechsverlauf fuer Intent-Verstaendnis
- Folgt Prioritaetslogik basierend auf Git-Zustand:
  - **Gestagete Aenderungen existieren**: Commit-Nachricht nur aus gestageten Aenderungen generieren
  - **Keine gestageten, aber ungestagete Aenderungen**: Commit-Nachricht mit Staging-Erinnerung vorschlagen
  - **Keine Aenderungen**: Sauberes Arbeitsverzeichnis melden
- Generiert Conventional-Commits-konforme Nachrichten
- Bestaetigt mit Benutzer vor der Ausfuehrung des Commits

**Git-Zustandsbehandlung:**

| Zustand | Verhalten |
|-------|----------|
| Gestagete Aenderungen | Nachricht generieren, bestaetigen, committen |
| Nur ungestagete | Nachricht vorschlagen, an Staging erinnern, fragen ob alle stagen |
| Sauber | "Keine Aenderungen erkannt" melden |

**Beispiel:**
```text
Sie: /codexspec.commit

KI:  Analysiere Git-Kontext...

     Branch: feature/add-auth
     Gestagete: 2 Dateien
     Ungestagete: 3 Dateien

     Vorgeschlagene Commit-Nachricht:
     feat(auth): add JWT authentication module

     - Implement token generation and validation
     - Add middleware for protected routes
     - Include unit tests for auth service

     Commit bestaetigen? (y/n)

Sie: y

KI:  ✓ Committed: abc1234
```

**Tipps:**
- Flexibler als `/codexspec.commit-staged` – behandelt verschiedene Git-Zustaende
- Beruecksichtigt Sitzungskontext fuer sinnvolle Commit-Nachrichten
- Bestaetigt immer vor dem Committen
- Fuer ungestagete Aenderungen, klare Erinnerung zum Staging zuerst

---

### `/codexspec.commit-staged`

Eine Conventional-Commits-konforme Commit-Nachricht basierend ausschliesslich auf gestageten Git-Aenderungen generieren. Dies ist ein einfacherer, fokussierter Befehl, wenn Sie Ihre Aenderungen bereits gestaget haben.

**Syntax:**
```
/codexspec.commit-staged
```

**Argumente:**
| Argument | Erforderlich | Beschreibung |
|----------|----------|-------------|
| Keine | - | Analysiert nur gestagete Aenderungen |

**Was es tut:**
- Fuehrt `git diff --staged` aus, um gestagete Aenderungen abzurufen
- Analysiert Aenderungen und generiert Commit-Nachricht
- Folgt Conventional-Commits-Spezifikation
- Bestaetigt mit Benutzer vor dem Committen
- Meldet Fehler, wenn keine gestageten Aenderungen existieren

**Beispiel:**
```text
Sie: /codexspec.commit-staged

KI:  Analysiere gestagete Aenderungen...

     Gestagete Dateien:
     - src/auth/service.py
     - tests/test_auth.py

     Vorgeschlagene Commit-Nachricht:
     feat(auth): implement token refresh logic

     - Add refresh token generation
     - Include token expiration handling
     - Add tests for refresh flow

     Commit bestaetigen? (y/n)

Sie: y

KI:  ✓ Committed: def5678
```

**Tipps:**
- Aenderungen zuerst mit `git add` stagen
- Analysiert nur gestageten Inhalt – ignoriert ungestagete
- Einfacher als `/codexspec.commit`, wenn Sie wissen, was Sie committen moechten
- `/codexspec.commit` fuer kontextbewusstere Nachrichten verwenden

---

## Workflow-Ueberblick

```
┌──────────────────────────────────────────────────────────────────────────┐
│                    CodexSpec Mensch-KI-Zusammenarbeits-Workflow           │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  1. Verfassung  ──►  Projektprinzipien definieren                        │
│         │                         mit artefaktuebergreifender Validierung │
│         ▼                                                                │
│  2. Specify  ───────►  Interaktives Q&A, um Anforderungen zu klaeren     │
│         │               (keine Datei erstellt - menschliche Kontrolle)    │
│         ▼                                                                │
│  3. Generate Spec  ─►  spec.md-Dokument erstellen                        │
│         │                                                                │
│         ▼                                                                │
│  ╔═══════════════════════════════════════════════════════════════════╗   │
│  ║  ★ REVIEW-GATE 1: /codexspec.review-spec ★                        ║   │
│  ║  Validieren: Vollstaendigkeit, Klarheit, Testbarkeit, Verfassung   ║   │
│  ╚═══════════════════════════════════════════════════════════════════╝   │
│         │                                                                │
│         ▼                                                                │
│  4. Clarify  ───────►  Unklarheiten loesen (iterativ)                    │
│         │               4 zielgerichtete Kategorien, max 5 Fragen         │
│         ▼                                                                │
│  5. Spec to Plan  ──►  Technischen Plan erstellen mit:                   │
│         │               • Verfassungskonformitaetspruefung (OBLIGATORISCH)│
│         │               • Modulabhaengigkeitsgraph                        │
│         ▼                                                                │
│  ╔═══════════════════════════════════════════════════════════════════╗   │
│  ║  ★ REVIEW-GATE 2: /codexspec.review-plan ★                        ║   │
│  ║  Validieren: Spec-Ausrichtung, Architektur, Tech-Stack, Phasen     ║   │
│  ╚═══════════════════════════════════════════════════════════════════╝   │
│         │                                                                │
│         ▼                                                                │
│  6. Plan to Tasks  ─►  Atomare Aufgaben generieren mit:                  │
│         │               • TDD-Erzwingung (Tests vor Impl)                │
│         │               • Parallel-Markierungen [P]                      │
│         │               • Dateipfad-Spezifikationen                       │
│         ▼                                                                │
│  ╔═══════════════════════════════════════════════════════════════════╗   │
│  ║  ★ REVIEW-GATE 3: /codexspec.review-tasks ★                       ║   │
│  ║  Validieren: Abdeckung, TDD-Konformitaet, Abhaengigkeiten, Granular.║   │
│  ╚═══════════════════════════════════════════════════════════════════╝   │
│         │                                                                │
│         ▼                                                                │
│  7. Analyze  ───────►  Artefaktuebergreifende Konsistenzpruefung         │
│         │               Luecken, Duplikate, Verfassungsprobleme erkennen │
│         ▼                                                                │
│  8. Implement  ─────►  Mit bedingtem TDD-Workflow ausfuehren             │
│                          Code: Test-First | Docs/Config: Direkt          │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
```

**Schluesselpunkt**: Jedes Review-Gate (★) ist ein **Mensch-Checkpoint**, wo Sie KI-Ausgabe validieren, bevor Sie mehr Zeit investieren. Das Ueberspringen dieser Gates fuehrt oft zu kostspieligen Nachbesserungen.

---

## Problembehebung

### "Feature-Verzeichnis nicht gefunden"

Der Befehl konnte das Feature-Verzeichnis nicht lokalisieren.

**Loesungen:**
- Zuerst `codexspec init` ausfuehren, um das Projekt zu initialisieren
- Pruefen, dass `.codexspec/specs/`-Verzeichnis existiert
- Verifizieren, dass Sie im korrekten Projektverzeichnis sind

### "Keine spec.md gefunden"

Die Spezifikationsdatei existiert noch nicht.

**Loesungen:**
- Zuerst `/codexspec.specify` ausfuehren, um Anforderungen zu klaeren
- Dann `/codexspec.generate-spec` ausfuehren, um spec.md zu erstellen

### "Verfassung nicht gefunden"

Keine Projektverfassung existiert.

**Loesungen:**
- `/codexspec.constitution` ausfuehren, um eine zu erstellen
- Verfassung ist optional, aber empfohlen fuer konsistente Entscheidungen

### "Aufgabendatei nicht gefunden"

Die Aufgabenaufteilung existiert nicht.

**Loesungen:**
- Sicherstellen, dass Sie zuerst `/codexspec.spec-to-plan` ausgefuehrt haben
- Dann `/codexspec.plan-to-tasks` ausfuehren, um tasks.md zu erstellen

### "GitHub-CLI nicht authentifiziert"

Der `/codexspec.tasks-to-issues`-Befehl erfordert GitHub-Authentifizierung.

**Loesungen:**
- GitHub-CLI installieren: `brew install gh` (macOS) oder aequivalent
- Authentifizieren: `gh auth login`
- Verifizieren: `gh auth status`

---

## Naechste Schritte

- [Workflow](workflow.md) - Haeufige Muster und wann jeder Befehl zu verwenden ist
- [CLI](../reference/cli.md) - Terminal-Befehle fuer Projekt-Initialisierung
