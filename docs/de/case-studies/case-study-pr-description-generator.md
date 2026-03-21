# CodexSpec-Anwendungsfall: Hinzufuegen einer PR-Beschreibungsgenerator-Funktion

> Dieses Dokument protokolliert den vollstaendigen Prozess der Verwendung der CodexSpec-Toolkette zum Hinzufuegen einer neuen Funktion zum CodexSpec-Projekt selbst und zeigt die praktische Anwendung von Spec-Driven Development (SDD).

## Ueberblick

**Zielfunktion**: Hinzufuegen des Befehls `/codexspec:pr` zum Generieren strukturierter GitHub PR / GitLab MR-Beschreibungen.

**Entwicklungsprozess**: `specify → generate-spec → review-spec → clarify → spec-to-plan`

**Schluesselmerkmal**: Waehrend der Entwicklung wurden Anforderungsprobleme entdeckt und durch den `clarify`-Befehl angepasst, was die Flexibilitaet von SDD zeigt.

---

## Phase 1: Urspruengliche Anforderungsklaerung (`/codexspec:specify`)

### Urspruengliche Benutzereingabe

```
Ich moechte dem Projekt eine Funktion hinzufuegen: Bereitstellung eines neuen Git-bezogenen Befehls zum Generieren genauer, detaillierter und konformer GitHub PR-Informationen (oder MR-Informationen, fuer GitLab). Hier sind zwei PR-Befehlsinhalte, die ich in anderen Projekten verwendet habe, als Referenz fuer Sie.

[Referenzbeispiel 1 - Strukturierte Beschreibung]
Jetzt spielen Sie bitte die Rolle des Projektbetreuers und schreiben basierend auf unserer bisherigen Arbeit eine klare Pull-Request-Beschreibung fuer diesen Commit.
Die PR-Beschreibung sollte sich an andere Teammitglieder richten und folgende Teile enthalten:
1. Kontext (Context)
2. Implementierung (Implementation)
3. Tests (Testing)
4. Manuelle Verifizierung (How to Verify)

[Referenzbeispiel 2 - Einfache Beschreibung]
Bitte erstellen Sie basierend auf dem Code-Unterschied zwischen dem aktuellen Branch und dem origin/main-Branch eine den Git-Konventionen entsprechende Merge-Request-Titel und -Beschreibung im Markdown-Format. (Verwendung deutscher Beschreibung)
```

### Klaerungsprozess

**F1: Ausgabesprache**

- Optionen: Projekteinstellung folgen / Deutsch / Automatische Erkennung
- **Benutzerauswahl**: Projekteinstellung folgen (aktuell: en)

**F2: Plattformunterstuetzung**

- Optionen: GitHub und GitLab unterstuetzen / Nur GitHub / Plattform automatisch erkennen
- **Benutzerauswahl**: Plattform automatisch erkennen

**F3: PR-Beschreibungsinhalt**

- Optionen: Detaillierte strukturierte Beschreibung / Kurze Beschreibung / Anpassbare Vorlage
- **Benutzerauswahl**: Detaillierte strukturierte Beschreibung (empfohlen)

**F4: Ausloeser**

- Optionen: Aktueller Branch vs origin/main / Nicht gepushte Commits / Zielbranch angebbar
- **Benutzerauswahl**: Zielbranch angebbar

**F5: Spec-Quelle**

- Optionen: Bevorzugt spec.md verwenden / Nur Git-Informationen / Alle Quellen kombinieren
- **Benutzerauswahl**: Alle Quellen kombinieren (empfohlen)

**F6: Benennung**

- Optionen: codexspec.pr / codexspec.create-pr / codexspec.create-mr
- **Benutzerauswahl**: codexspec.pr (empfohlen)

**F7: Behandlung ohne Spec**

- Optionen: Weiter generieren, Kontext ueberspringen / Benutzer auffordern, zuerst Spec zu erstellen / Warnen und fortfahren
- **Benutzerauswahl**: Weiter generieren, Kontext ueberspringen

**F8: Ausgabemodus**

- Optionen: Terminalausgabe / In Datei speichern / Terminal + optionale Datei
- **Benutzerauswahl**: Terminal + optionale Datei (empfohlen)

**F9: Standardabschnitte**

- Optionen: Kontext, Implementierung, Tests, Verifizierung (alle auswaehlen)
- **Benutzerauswahl**: Alle vier Abschnitte

**F10: Befehlsparameter**

- **Benutzerauswahl**: Alle Parameter sind optionale Parameter
  - `--target-branch`: Standard origin/main
  - `--output`: Standardmaessig nur Terminalausgabe
  - `--sections`: Standardmaessig nach Standard
  - `--no-spec`: spec.md-Dateisuche ueberspringen

### Sprachkonfigurationskorrektur

**Benutzerfeedback**: Die Sprache sollte wie beim `/commit-staged`-Befehl primaer nach dem `language.commit`-Parameter in `config.yml` bestimmt werden. Wenn kein `language.commit`-Parameter gesetzt ist, dann nach `language.output`.

**Aktualisierte Anforderungszusammenfassung**:

```
Sprachprioritaet: language.commit > language.output > Englisch (Standard)
```

---

## Phase 2: Generierung des Spezifikationsdokuments (`/codexspec:generate-spec`)

### Generierte Dokumentstruktur

Das generierte `spec.md` enthaelt folgende Teile:

- **Ueberblick**: Funktionsueberblick
- **Ziele**: 4 Ziele
- **User Stories**: 4 User Stories mit Akzeptanzkriterien
- **Funktionale Anforderungen**: 8 Anforderungen (REQ-001 bis REQ-008)
- **Befehlsparameter**: 4 Parameterdefinitionen
- **Nicht-funktionale Anforderungen**: 3 Anforderungen (Performance, Kompatibilitaet, Fehlerbehandlung)
- **Akzeptanzkriterien (Testfaelle)**: 10 Testfaelle
- **Randfaelle**: 6 Randfaelle
- **Ausgabeformatbeispiel**: GitHub PR und GitLab MR Beispiele
- **Nicht im Scope**: Explizit ausgeschlossene Funktionen
- **Abhaengigkeiten**: Abhaengigkeiten
- **Verwandte Befehle**: Zugehoerige Befehle

### Wichtige Anforderungsauszuege

```markdown
### REQ-003: Sprachkonfiguration
Der Befehl soll die Ausgabesprache in folgender Prioritaetsreihenfolge bestimmen:
1. `language.commit` in `.codexspec/config.yml` (hoechste Prioritaet)
2. `language.output` in `.codexspec/config.yml` (Fallback)
3. Englisch (Standard bei fehlender Konfiguration)
```

---

## Phase 3: Spezifikationsueberpruefung (`/codexspec:review-spec`)

### Ueberpruefungsergebnisse

- **Gesamtstatus**: ✅ Bestanden
- **Qualitaetsbewertung**: 92/100
- **Bereitschaftsstatus**: Bereit fuer Planung

### Gefundene Probleme

**Warnungen (Should Fix)**:

1. **SPEC-001**: Testdatei-Erkennungslogik nicht explizit angegeben
2. **SPEC-002**: Bei mehreren spec.md-Dateien kann "zuletzt geaendert" ungenau sein

**Vorschlaege (Nice to Have)**:

1. Erwaegen Sie das Hinzufuegen eines `--title`-Parameters
2. Hinzufuegen einer Ausgabeformat-Validierungsanforderung
3. Erwaegen Sie die Unterstuetzung von GitHub Enterprise URL-Mustern

### Speicherort des Ueberpruefungsberichts

`.codexspec/specs/001-pr-description-generator/review-spec.md`

---

## Phase 4: Anforderungsklaerung und Anpassung (`/codexspec:clarify`) ⚠️ Kritischer Wendepunkt

### Erkannte Probleme

**Benutzerfeedback**:
> Ich habe realisiert, dass es ein Problem bei der Verwendung von spec.md gibt. Wenn ein Benutzer beispielsweise eine sehr kleine Aenderung vornimmt und nicht den standardisierten CodexSpec-Workflow specify->plan->tasks->implement verwendet, sondern direkte Gespraeche oder den in Claude Code integrierten Plan-Modus, und nach Abschluss der Aenderungen den CodexSpec-Befehl separat aufrufen moechte, um konforme PR-Informationen zu generieren. In diesem Fall koennte die standardmaessige Verwendung der zuletzt geaenderten spec.md eine fruehere, mit der aktuellen Aenderung unzusammenhaengende spec.md-Inhalte verwenden.

### Klaerungs-QA-Prozess

**F1: Spec-Auswahlstrategie**

**Kontext**: EC-004 besagt "mehrere spec.md → zuletzt geaenderte verwenden". Aber wenn Benutzer kleine Aenderungen vornehmen, haben sie moeglicherweise nicht den SDD-Workflow verwendet, und die letzte spec.md koennte unzusammenhaengend mit der aktuellen Aenderung sein.

| Option | Beschreibung |
|--------|-------------|
| A | Standardmaessig keine spec.md verwenden, es sei denn, Benutzer gibt `--spec`-Parameter explizit an |
| B | Basierend auf Branch-Namen abgleichen |
| C | Benutzer zur Auswahl auffordern |
| D | Basierend auf Dateiaenderungen abgleichen |

**Benutzerauswahl**: Option A
**Begruendung**: Falsche Referenzierung vermeiden, `--spec`-Parameter ermoeglicht Benutzern, die SDD-Integration benoetigen, explizit anzugeben.

---

**F2: Spec-Inhaltsextraktionsstrategie**

**Kontext**: Was passiert, wenn Benutzer `--spec` verwenden und die spec.md-Struktur unvollstaendig ist?

| Option | Beschreibung |
|--------|-------------|
| A | Bestmoegliche Extraktion, fehlende Teile ueberspringen |
| B | Warnen und Kontext ueberspringen |
| C | Vollstaendige Struktur erfordern, sonst Fehler |

**Benutzerauswahl**: Option A
**Begruendung**: Vermeidung, dass der Workflow aufgrund von Spec-Formatproblemen blockiert wird.

---

**F3: Testdatei-Erkennung**

**Kontext**: Wie werden Testdateien im Testing-Abschnitt erkannt?

| Option | Beschreibung |
|--------|-------------|
| A | Haeufige Verzeichnismuster (tests/, test/) |
| B | Sprachunabhaengige Heuristik (Verzeichnis + Dateinamenmuster) |
| C | Keine aktive Erkennung, nur aus Commit-Nachrichten ableiten |

**Benutzerauswahl**: Option B
**Begruendung**: Abdeckung verschiedener Projektstrukturen in mehreren Sprachen.

---

**F4: PR-Titelgenerierung**

**Kontext**: Wie sollte der PR-Titel generiert werden?

| Option | Beschreibung |
|--------|-------------|
| A | Branch-Namen-Parsing bevorzugen |
| B | Erste Commit-Nachricht bevorzugen |
| C | Kombinierte Generierung (git diff + Branch-Name + Commit-Nachricht) |

**Benutzerauswahl**: Option C
**Benutzerbegruendung**: Der erste Commit koennte nur ein kleiner Teil der Aenderungen sein; Branch-Namen erfordern hohe Namenskonventionen. Da viele Git-Informationen und Code-Aenderungen als Referenz zur Verfuegung stehen, ist eine kombinierte Analyse genauer.

---

**F5: Verifizierungsbefehlsgenerierung**

**Kontext**: Wie werden Verifizierungsbefehle im "How to Verify"-Abschnitt generiert?

| Option | Beschreibung |
|--------|-------------|
| A | Allgemeine Vorlagen |
| B | Projekterkennung (pyproject.toml → pytest, package.json → npm test) |
| C | Aus Commit-Nachrichten ableiten |

**Benutzerauswahl**: Option B
**Begruendung**: Projekterkennung kann nuetzlichere Verifizierungsbefehle generieren.

---

### Zusammenfassung der Klaerungssitzung

| Frage | Entscheidung | Auswirkung |
|------|------|------|
| Spec-Auswahlstrategie | Opt-in via `--spec` | REQ-007, EC-004, Parametertabelle |
| Spec-Inhaltsextraktion | Bestmoegliche Extraktion | REQ-005b, EC-004c |
| Testdatei-Erkennung | Sprachunabhaengige Heuristik | REQ-006b |
| PR-Titelgenerierung | Kombinierte Analyse | REQ-008a |
| Verifizierungsbefehlsgenerierung | Projektdatei-Erkennung | REQ-010 |

### Wichtige Aenderung: Parameterlogik-Umkehr

```
Urspruengliches Design: --no-spec (spec ueberspringen)
Neues Design: --spec (spec aktivieren, opt-in)
```

---

## Phase 5: Technischer Implementierungsplan (`/codexspec:spec-to-plan`)

### Planueberblick

**Implementierungsmethode**: Markdown-Vorlagendatei (konsistent mit `/codexspec:commit-staged`)

**Keine neuen Abhaengigkeiten** - Funktion wird durch Slash-Command-Vorlage implementiert, erfordert keinen Python-Code.

### Zusammenfassung der technischen Entscheidungen

| Entscheidung | Auswahl | Begruendung |
|------|------|------|
| Implementierungsmethode | Markdown-Vorlage | Konsistent mit bestehenden Befehlen, wartbar |
| Sprachprioritaet | commit > output > en | Konsistent mit `/commit-staged`-Befehl |
| Plattformerkennung | Remote-URL-Parsing | Einfach und zuverlaessig |
| Spec-Integration | Opt-in (`--spec`) | Falsche Referenzierung vermeiden |
| Inhaltsextraktion | Bestmoegliche | Blockiert Workflow nicht |
| Test-Erkennung | Verzeichnis+Dateinamenmuster | Sprachunabhaengig |
| Titelgenerierung | Kombinierte Analyse | Am genauesten |
| Befehlserkennung | Projektdatei-Erkennung | Praktischer |
| Ausgabemodus | Terminal zuerst, optionale Datei | Flexibel |

### Implementierungsphasen

1. **Phase 1**: Vorlagenerstellung (YAML-Frontmatter, Sprachkonfiguration, Git-Kontext)
2. **Phase 2**: Kernfunktionalitaet (Spec-Integration, Test-Erkennung, Befehlserkennung, Titelgenerierung)
3. **Phase 3**: Randfallbehandlung
4. **Phase 4**: Tests
5. **Phase 5**: Dokumentationsaktualisierung

### Dateiliste

**Erstellen**:

- `templates/commands/pr.md`

**Aendern**:

- `CLAUDE.md` - Befehlsbeschreibung hinzufuegen
- `README.md` - Befehl zur Liste hinzufuegen

**Testen**:

- `tests/test_pr_template.py`

---

## Vollstaendiges Flussdiagramm

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         CodexSpec SDD-Entwicklungsprozess                │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  /codexspec:specify                                                      │
│  ├─ Anforderungen durch Q&A klaeren                                     │
│  ├─ Benutzer hat Referenzbeispiele bereitgestellt                       │
│  └─ 10 Fragen, die Sprache, Plattform, Inhalt, Parameter abdecken       │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  /codexspec:generate-spec                                                │
│  ├─ Vollstaendige spec.md generieren                                    │
│  ├─ 4 User Stories, 8 funktionale Anforderungen, 10 Testfaelle          │
│  └─ Speichern unter .codexspec/specs/001-pr-description-generator/spec.md│
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  /codexspec:review-spec                                                  │
│  ├─ Qualitaetsbewertung: 92/100                                         │
│  ├─ 2 Warnungen gefunden (Testdatei-Erkennung, Multi-Spec-Behandlung)   │
│  └─ Status: Bestanden, kann in Planungsphase eintreten                  │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  /codexspec:clarify  ⚠️ Kritische Anpassung                              │
│  ├─ Benutzer hat tatsaechliches Nutzungsproblem entdeckt                │
│  ├─ 5 Klaerungsfragen, alle beantwortet                                 │
│  ├─ Wichtige Aenderung: --no-spec → --spec (opt-in)                     │
│  └─ 5 neue Anforderungen (REQ-005b, 006b, 008a, 010, Update 007)        │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  /codexspec:spec-to-plan                                                 │
│  ├─ Technischen Implementierungsplan aktualisieren                      │
│  ├─ 9 technische Entscheidungen, einschliesslich 5 neuer                │
│  ├─ 5 Implementierungsphasen                                             │
│  └─ Speichern unter .codexspec/specs/001-pr-description-generator/plan.md│
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  Nachste Schritte (in dieser Session nicht abgeschlossen)                │
│  ├─ /codexspec:review-plan - Planqualitaet validieren                   │
│  ├─ /codexspec:plan-to-tasks - In ausfuehrbare Aufgaben aufteilen       │
│  └─ /codexspec:implement-tasks - Implementierung ausfuehren             │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Wichtige Lektionen

### 1. Wert der Klaerungsphase

Dieser Fall zeigt die kritische Rolle des `clarify`-Befehls:

- **Benutzer entdeckt tatsaechliche Probleme bei der Verwendung** - Risiko der spec.md-Fehlverwendung bei kleinen Aenderungen
- **Designfehler durch Klaerungs-Q&A loesen** - Von automatischer Erkennung zu Opt-in-Modus geaendert
- **Anforderungsaenderungen werden systematisch protokolliert** - Alle Aenderungen im Clarifications-Abschnitt von spec.md gespeichert

### 2. Flexibilitaet des SDD-Prozesses

- Kein linearer Prozess, kann in jeder Phase zur Anpassung zurueckkehren
- `clarify` kann nach `review-spec` und vor `spec-to-plan` eingefuegt werden
- Spezifikationsdokumente und technische Plaene werden aktualisiert, um Aenderungen widerzuspiegeln

### 3. Evolution des Parameterdesigns

```
Urspruengliches Design:
  --no-spec: spec.md ueberspringen (standardmaessig verwenden)

Endgueltiges Design:
  --spec: spec.md aktivieren (standardmaessig nicht verwenden)
```

Diese Aenderung spiegelt den Designwandel vom "Standard-SDD-Workflow" zur "Unterstuetzung nicht-SDD-Workflows" wider und macht das Werkzeug universeller.

### 4. Dokumentenausgabe

| Phase | Ausgabedatei | Inhalt |
|------|----------|------|
| generate-spec | spec.md | Vollstaendiges Spezifikationsdokument |
| review-spec | review-spec.md | Qualitaetspruefungsbericht |
| clarify | (aktualisiert spec.md) | Klaerungsprotokoll + Anforderungs-Updates |
| spec-to-plan | plan.md | Technischer Implementierungsplan |

---

## Anhang: Befehlsreferenz

```bash
# 1. Urspruengliche Anforderungsklaerung
/codexspec:specify

# 2. Spezifikationsdokument generieren
/codexspec:generate-spec

# 3. Spezifikationsqualitaet ueberpruefen
/codexspec:review-spec

# 4. Anforderungen klaeren/anpassen (optional, nach Problemendeckung verwenden)
/codexspec:clarify [Problembeschreibung]

# 5. Technischen Plan generieren
/codexspec:spec-to-plan

# 6. Planqualitaet ueberpruefen (optional)
/codexspec:review-plan

# 7. In Aufgaben aufteilen
/codexspec:plan-to-tasks

# 8. Implementierung ausfuehren
/codexspec:implement-tasks
```

---

*Dieses Dokument wurde automatisch vom CodexSpec SDD-Workflow generiert und protokolliert den tatsaechlichen Entwicklungsgespraechsprozess.*
