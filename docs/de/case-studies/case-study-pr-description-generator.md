# CodexSpec-Fallstudie: Hinzufügen eines PR-Beschreibungs-Generators zum Projekt

> Historische Fallstudie: Gespräch, Zwischenentscheidungen, Befehlsfolge und Prüfergebnisse dokumentieren den damaligen Workflow, nicht die heute geltenden Befehlsregeln. Der aktuelle Standardablauf enthält eine eigene Entwurfsphase und `review-design`; `clarify` aktualisiert zuerst die bestätigten Anforderungen und danach die Spezifikation. Siehe [aktueller Workflow](../user-guide/workflow.md) und [PR-Befehlsreferenz](../user-guide/commands.md#codexspecpr).

> Dieses Dokument hält den vollständigen Prozess fest, wie die CodexSpec-Toolchain genutzt wurde, um dem CodexSpec-Projekt selbst ein neues Feature hinzuzufügen – und zeigt Spec-Driven Development (SDD) in der Praxis.

## Überblick

**Ziel-Feature**: Den Befehl `/codexspec:pr` hinzufügen, der strukturierte GitHub-PR- / GitLab-MR-Beschreibungen erzeugt. (Den nutzerseitigen Überblick über den ausgelieferten Befehl finden Sie im [README-Eintrag zu `/codexspec:pr`](https://github.com/Zts0hg/codexspec/blob/main/README.md).)

**Entwicklungsfluss**: `specify → generate-spec → review-spec → clarify → design-to-plan`

**Schlüsselmerkmal**: Ein Anforderungsproblem tauchte mitten im Fluss auf und wurde über den Befehl `clarify` korrigiert – ein Beleg für die Flexibilität von SDD. Das ist ein konkretes Beispiel für das CodexSpec-**Confirmation Gate**: nichts ist verbindlich, bis Sie es ausdrücklich bestätigen, und eine zuvor akzeptierte Entscheidung kann am Clarify-Checkpoint wiedereröffnet und umgekehrt werden.

---

## Phase 1: Ursprüngliche Anforderungs-Klärung (`/codexspec:specify`)

### Ursprüngliche Nutzereingabe

```
I want to add a feature to the project: a new Git-related command that generates accurate, detailed, and standards-compliant GitHub PR descriptions (or MR descriptions, for GitLab). Below are two PR commands I have used in other projects, provided for reference.

[Reference Example 1 - Structured Description]
Now, acting as a project maintainer, based on all the work we have done so far, write a clear Pull Request description for this submission.
The PR description should be aimed at the other reviewers on the team and include the following sections:
1. Context
2. Implementation
3. Testing
4. How to Verify

[Reference Example 2 - Simple Description]
Based on the code diff between the current branch and origin/main, use Markdown to produce a Merge Request title and description that comply with Git conventions. (Describe in Chinese.)
```

### Klärungs-Prozess

**F1: Ausgabesprache**

- Optionen: Projektkonfiguration folgen / Chinesisch / Automatisch erkennen
- **Nutzerwahl**: Projektkonfiguration folgen (aktuell: en)

**F2: Plattform-Unterstützung**

- Optionen: GitHub und GitLab unterstützen / Nur GitHub / Plattform automatisch erkennen
- **Nutzerwahl**: Plattform automatisch erkennen

**F3: Inhalt der PR-Beschreibung**

- Optionen: Detaillierte strukturierte Beschreibung / Knappe Beschreibung / Anpassbare Vorlage
- **Nutzerwahl**: Detaillierte strukturierte Beschreibung (empfohlen)

**F4: Trigger-Bedingung**

- Optionen: Aktueller Branch vs origin/main / Nicht gepushte Commits / Konfigurierbarer Ziel-Branch
- **Nutzerwahl**: Konfigurierbarer Ziel-Branch

**F5: Spec-Quelle**

- Optionen: spec.md bevorzugen / Nur Git-Infos / Alle Quellen kombinieren
- **Nutzerwahl**: Alle Quellen kombinieren (empfohlen)

**F6: Namensgebung**

- Optionen: codexspec.pr / codexspec.create-pr / codexspec.create-mr
- **Nutzerwahl**: codexspec.pr (empfohlen)

**F7: Umgang mit fehlender Spec**

- Optionen: Weiter erzeugen, Context überspringen / Nutzer auffordern, zuerst Spec anzulegen / Warnen und fortfahren
- **Nutzerwahl**: Weiter erzeugen, Context überspringen

**F8: Ausgabe-Methode**

- Optionen: Terminal-Ausgabe / In Datei speichern / Terminal + optionale Datei
- **Nutzerwahl**: Terminal + optionale Datei (empfohlen)

**F9: Standard-Abschnitte**

- Optionen: Context, Implementation, Testing, How to Verify (alle ausgewählt)
- **Nutzerwahl**: Alle vier Abschnitte

**F10: Befehlsparameter**

- **Nutzerwahl**: Alle Parameter sind optional
  - `--target-branch`: Standard origin/main
  - `--output`: Wenn nicht angegeben, Standard nur Terminal-Ausgabe
  - `--sections`: Wenn nicht angegeben, den Defaults folgen
  - `--no-spec`: spec.md-Lookup überspringen

### Korrektur der Sprachkonfiguration

**Nutzer-Feedback**: Das Sprachverhalten sollte dem Befehl `/commit-staged` entsprechen – zuerst `language.commit` aus `config.yml` beachten und nur auf `language.output` zurückfallen, wenn `language.commit` nicht gesetzt ist.

**Aktualisierte Anforderungszusammenfassung**:

```
Language priority: language.commit > language.output > English (default)
```

---

## Phase 2: Spezifikationsdokument erzeugen (`/codexspec:generate-spec`)

### Struktur des erzeugten Dokuments

Das erzeugte `spec.md` enthält folgende Abschnitte:

- **Overview**: Feature-Überblick
- **Goals**: 4 Ziele
- **User Stories**: 4 User Stories mit Akzeptanzkriterien
- **Functional Requirements**: 8 Anforderungen (REQ-001 bis REQ-008)
- **Command Parameters**: 4 Parameterdefinitionen
- **Non-Functional Requirements**: 3 Anforderungen (Performance, Kompatibilität, Fehlerbehandlung)
- **Acceptance Criteria (Test Cases)**: 10 Testfälle
- **Edge Cases**: 6 Randfälle
- **Output Format Example**: GitHub-PR- und GitLab-MR-Beispiele
- **Out of Scope**: Explizit ausgeschlossene Features
- **Dependencies**: Abhängigkeiten
- **Related Commands**: Verwandte Befehle

### Auszug einer Schlüsselanforderung

```markdown
### REQ-003: Language Configuration
The command shall determine output language in the following priority order:
1. `language.commit` in `.codexspec/config.yml` (highest priority)
2. `language.output` in `.codexspec/config.yml` (fallback)
3. English (default if no configuration)
```

---

## Phase 3: Spezifikations-Review (`/codexspec:review-spec`)

### Review-Ergebnis

- **Gesamtstatus**: ✅ Pass
- **Qualitäts-Score**: 92/100
- **Readiness**: Ready for Planning

### Gefundene Punkte

**Warnungen (Should Fix)**:

1. **SPEC-001**: Die Logik zur Testdatei-Erkennung ist nicht explizit spezifiziert
2. **SPEC-002**: Wenn mehrere spec.md-Dateien existieren, kann „zuletzt geändert" ungenau sein

**Vorschläge (Nice to Have)**:

1. Einen `--title`-Parameter in Betracht ziehen
2. Eine Anforderung zur Ausgabeformat-Validierung hinzufügen
3. Unterstützung für GitHub-Enterprise-URL-Muster in Betracht ziehen

### Ort des Review-Berichts

`.codexspec/specs/2026-0613-1200ab-pr-description-generator/review-spec.md`

Dies ist ein **evidenzbasiertes Review**: Jede Warnung und jeder Vorschlag oben ist an eine konkrete, identifizierbare Lücke in der Spec gebunden, und empfehlende Posten (Nice to Have) beeinflussen die Akzeptanz nicht und lösen keine automatischen Änderungen aus.

---

## Phase 4: Anforderungs-Klärung und -Anpassung (`/codexspec:clarify`) – kritischer Wendepunkt

### Entdecktes Problem

**Nutzer-Feedback**:
> Mir ist klar geworden, dass es ein Problem beim Einsatz von spec.md gibt. Ein Nutzer beispielsweise macht vielleicht eine sehr kleine Änderung und durchläuft nicht CodexSpecs Standardfluss specify → plan → tasks → implement. Stattdessen ändert er direkt über Konversation oder Claude Codes eingebauten Plan-Modus und möchte nach Abschluss der Änderungen einen CodexSpec-Befehl separat aufrufen, um eine standardkonforme PR-Beschreibung zu erzeugen. In diesem Fall würde der Default auf die zuletzt geänderte spec.md Inhalte aus einer früheren spec.md ziehen, die mit dieser Änderung nichts zu tun hat.

Das ist das **Confirmation Gate** in Aktion: Die frühere Entscheidung („Default auf die zuletzt geänderte spec.md") war zwar erfasst, aber nicht in dem Sinne verbindlich, dass sie unumkehrbar wäre – der Nutzer hat sie am Clarify-Checkpoint mit neuen Informationen über ein reales Nutzungsmuster wiedereröffnet, und der zuvor akzeptierte Default wurde umgestoßen.

### Klärungs-Q&A-Prozess

**F1: Strategie zur Spec-Auswahl**

**Kontext**: Die aktuelle EC-004 besagt „mehrere spec.md-Dateien → die zuletzt geänderte verwenden". Wenn ein Nutzer aber eine kleine Änderung ohne den SDD-Fluss macht, ist die zuletzt geänderte spec.md möglicherweise unabhängig von der aktuellen Änderung.

| Option | Beschreibung |
|--------|-------------|
| A | spec.md standardmäßig nicht verwenden, außer der Nutzer gibt explizit `--spec` an |
| B | Nach Branch-Namen matchen |
| C | Den Nutzer zur Auswahl auffordern |
| D | Nach Dateiänderungen matchen |

**Nutzerwahl**: Option A
**Begründung**: Vermeidet fehlerhafte Referenzen; der Parameter `--spec` erlaubt Nutzern, die SDD-Integration wünschen, explizit einzuschalten.

---

**F2: Strategie zur Spec-Inhaltsextraktion**

**Kontext**: Wenn der Nutzer `--spec` angibt, was passiert, wenn die spec.md-Struktur unvollständig ist?

| Option | Beschreibung |
|--------|-------------|
| A | Best-Effort-Extraktion, fehlende Abschnitte überspringen |
| B | Warnen und Context überspringen |
| C | Vollständige Struktur verlangen, sonst Fehler |

**Nutzerwahl**: Option A
**Begründung**: Vermeidet, dass ein Spec-Formatproblem den Workflow blockiert.

---

**F3: Testdatei-Erkennung**

**Kontext**: Wie sollte der Testing-Abschnitt Testdateien entdecken?

| Option | Beschreibung |
|--------|-------------|
| A | Gängige Verzeichnismuster (tests/, test/) |
| B | Sprachagnostische Heuristiken (Verzeichnis + Dateinamenmuster) |
| C | Keine aktive Erkennung; nur aus Commit-Nachrichten ableiten |

**Nutzerwahl**: Option B
**Begründung**: Deckt unterschiedliche Projektstrukturen über verschiedene Sprachen hinweg ab.

---

**F4: PR-Titelgenerierung**

**Kontext**: Wie sollte der PR-Titel erzeugt werden?

| Option | Beschreibung |
|--------|-------------|
| A | Branch-Namen-Parsing zuerst |
| B | Erste Commit-Nachricht zuerst |
| C | Synthetisieren (git diff + Branch-Name + Commit-Nachrichten) |

**Nutzerwahl**: Option C
**Nutzerbegründung**: Der erste Commit mag nur einen kleinen Teil der Änderung abbilden, und Branch-Namen setzen starke Naming-Disziplin voraus. Mit umfangreichen Git-Informationen und Code-Änderungen als Referenz ist eine synthetisierte Analyse genauer.

---

**F5: Generierung des Verifizierungs-Befehls**

**Kontext**: Wie sollte der Abschnitt „How to Verify" Verifizierungs-Befehle erzeugen?

| Option | Beschreibung |
|--------|-------------|
| A | Generische Vorlagen |
| B | Projekt-Erkennung (pyproject.toml → pytest, package.json → npm test) |
| C | Aus Commit-Nachrichten ableiten |

**Nutzerwahl**: Option B
**Begründung**: Projekt-Erkennung liefert praktischere Verifizierungs-Befehle.

---

### Zusammenfassung der Klärungs-Session

| Frage | Entscheidung | Auswirkung |
|----------|----------|--------|
| Spec-Auswahlstrategie | Opt-in via `--spec` | REQ-007, EC-004, Parametertabelle |
| Spec-Inhaltsextraktion | Best-Effort-Extraktion | REQ-005b, EC-004c |
| Testdatei-Erkennung | Sprachagnostische Heuristiken | REQ-006b |
| PR-Titelgenerierung | Synthetisierte Analyse | REQ-008a |
| Verifizierungs-Befehlsgenerierung | Projektdatei-Erkennung | REQ-010 |

### Schlüsseländerung: Umkehr der Parameter-Logik

```
Original design: --no-spec (skip spec)
New design:      --spec (enable spec, opt-in)
```

Diese Umkehr ist die anschaulichste Illustration des Confirmation Gate in dieser Fallstudie: Ein Default, der ursprünglich „verbindlich" war (`--no-spec`, d. h. spec standardmäßig an), wurde wiedereröffnet, umgekehrt und als opt-in neu bestätigt, nachdem der Nutzer einen realen Workflow aufgezeigt hatte, den dieser Standardwert beeinträchtigt hätte.

---

## Phase 5: Technischer Implementierungsplan (`/codexspec:design-to-plan`)

### Plan-Überblick

**Implementierungsansatz**: Markdown-Vorlagendatei (konsistent mit `/codexspec:commit-staged`)

**Keine neuen Abhängigkeiten** – das Feature wird über eine Slash-Befehls-Vorlage geliefert und benötigt keinen Python-Code.

### Zusammenfassung der technischen Entscheidungen

| Entscheidung | Wahl | Grund |
|----------|--------|--------|
| Implementierungsansatz | Markdown-Vorlage | Konsistent mit bestehenden Befehlen, pflegeleicht |
| Sprachpriorität | commit > output > en | Konsistent mit `/commit-staged` |
| Plattform-Erkennung | Remote-URL-Parsing | Einfach und zuverlässig |
| Spec-Integration | Opt-in (`--spec`) | Vermeidet fehlerhafte Referenzen |
| Inhaltsextraktion | Best-Effort | Blockiert den Workflow nicht |
| Test-Erkennung | Verzeichnis + Dateinamenmuster | Sprachagnostisch |
| Titelgenerierung | Synthetisierte Analyse | Am genauesten |
| Befehls-Erkennung | Projektdatei-Erkennung | Praktischer |
| Ausgabe-Modus | Terminal zuerst, optionale Datei | Flexibel |

### Implementierungs-Phasen

1. **Phase 1**: Vorlagenerstellung (YAML-Frontmatter, Sprachkonfiguration, Git-Kontext)
2. **Phase 2**: Kernfunktionalität (Spec-Integration, Test-Erkennung, Befehls-Erkennung, Titelgenerierung)
3. **Phase 3**: Behandlung von Randfällen
4. **Phase 4**: Tests
5. **Phase 5**: Dokumentations-Updates

### Datei-Manifest

**Erstellt**:

- `templates/commands/pr.md`

**Geändert**:

- `CLAUDE.md` – Befehlsbeschreibung hinzufügen
- `README.md` – Befehl zur Liste hinzufügen

**Tests**:

- `tests/test_pr_template.py`

---

## Vollständiges Flussdiagramm

```
┌─────────────────────────────────────────────────────────────────────────┐
│                   CodexSpec SDD Development Flow                        │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  /codexspec:specify                                                     │
│  ├─ Clarify requirements through Q&A                                    │
│  ├─ User provides reference examples                                    │
│  └─ 10 questions covering language, platform, content, parameters, etc. │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  /codexspec:generate-spec                                               │
│  ├─ Generate a complete spec.md                                         │
│  ├─ 4 user stories, 8 functional requirements, 10 test cases            │
│  └─ Saved to .codexspec/specs/2026-0613-1200ab-pr-description-generator/spec.md │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  /codexspec:review-spec                                                 │
│  ├─ Quality score: 92/100                                               │
│  ├─ Found 2 warnings (test-file discovery, multi-spec handling)         │
│  └─ Status: Pass, can proceed to planning                               │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  /codexspec:clarify  (Critical adjustment)                              │
│  ├─ User surfaces a real-world usage issue                              │
│  ├─ 5 clarification questions, all answered                             │
│  ├─ Key change: --no-spec → --spec (opt-in)                             │
│  └─ Added 5 requirements (REQ-005b, 006b, 008a, 010, updated 007)       │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  /codexspec:design-to-plan                                                │
│  ├─ Update the technical implementation plan                            │
│  ├─ 9 technical decisions, including 5 new ones                         │
│  ├─ 5 implementation phases                                             │
│  └─ Saved to .codexspec/specs/2026-0613-1200ab-pr-description-generator/plan.md │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  Subsequent steps (not completed in this session)                       │
│  ├─ /codexspec:review-plan - Validate plan quality                      │
│  ├─ /codexspec:plan-to-tasks - Break down into executable tasks         │
│  └─ /codexspec:implement-tasks - Execute the implementation             │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Wesentliche Erkenntnisse

### 1. Der Wert der Clarify-Phase

Dieser Fall zeigt die alles entscheidende Rolle des Befehls `clarify`:

- **Der Nutzer entdeckt ein reales Problem bei der Nutzung** – das Risiko, spec.md in Small-Change-Szenarien fehlerhaft zu verwenden
- **Ein Designfehler wird durch klärendes Q&A gelöst** – Wechsel von Auto-Erkennung zu Opt-in
- **Anforderungsänderungen werden systematisch erfasst** – alle Änderungen werden im Clarifications-Abschnitt von spec.md gespeichert

### 2. Flexibilität des SDD-Flusses

- Es ist kein linearer Fluss; Sie können in jeder Phase zurückkehren und anpassen
- `clarify` lässt sich nach `review-spec` und vor `design-to-plan` einfügen
- Sowohl das Spezifikationsdokument als auch der technische Plan werden aktualisiert, um die Änderung widerzuspiegeln

### 3. Evolution des Parameter-Designs

```
Initial design:
  --no-spec: skip spec.md (used by default)

Final design:
  --spec: enable spec.md (not used by default)
```

Diese Änderung spiegelt einen Design-Wechsel von „Standard-SDD-Workflow" zu „ebenfalls Nicht-SDD-Workflows unterstützen" und macht das Werkzeug universeller.

### 4. Dokumentations-Outputs

| Phase | Ausgabedatei | Inhalt |
|-------|-------------|---------|
| generate-spec | spec.md | Vollständiges Spezifikationsdokument |
| review-spec | review-spec.md | Qualitäts-Review-Bericht |
| clarify | (aktualisiert spec.md) | Klärungs-Einträge + Anforderungs-Updates |
| design-to-plan | plan.md | Technischer Implementierungsplan |

---

## Anhang: Befehls-Kurzreferenz

```bash
# 1. Initial requirement clarification
/codexspec:specify

# 2. Generate the specification document
/codexspec:generate-spec

# 3. Review the specification quality
/codexspec:review-spec

# 4. Clarify/adjust requirements (optional; use when an issue is found)
/codexspec:clarify [issue description]

# 5. Generate the technical plan
/codexspec:design-to-plan

# 6. Review the plan quality (optional)
/codexspec:review-plan

# 7. Break down into tasks
/codexspec:plan-to-tasks

# 8. Execute the implementation
/codexspec:implement-tasks
```

---

*Dieses Dokument wurde vom CodexSpec-SDD-Workflow erzeugt und hält eine reale Entwicklungs-Konversation fest.*
