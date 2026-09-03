# Produktionsplan Berliner Wirtschaft

Web-Seite, die aus **Planungsjahr + Erscheinungsterminen** den kompletten
Produktionsplan des Magazins *Berliner Wirtschaft* rückwärts terminiert –
alle 24 Produktionsschritte je Heft, unter Berücksichtigung von Wochenenden,
Berliner Feiertagen und festen Ziel-Wochentagen.

Die Seite ersetzt die Excel-Vorlage `BW_2027_Produktionsplan_automatisierungsplan.xlsx`
(Blätter *Plan*, *Feiertage*, *Eingabe*, *Stammdaten*). Der Rechenkern ist eine
1:1-Portierung der dortigen LAMBDA-Funktion `fnPlantermin` und liefert für 2027
**exakt dieselben 240 Termine** wie die Excel.

## Benutzung

```
python3 build.py     # erzeugt index.html aus src/app.html
```

Danach `index.html` im Browser öffnen – kein Server, kein Build-Werkzeug,
keine Abhängigkeiten. Die Datei läuft auch von einem Netzlaufwerk oder als
GitHub Page. Alle Eingaben werden im Browser (localStorage) gespeichert.

## Aufbau

| Datei | Inhalt |
|---|---|
| `src/app.html` | Die komplette Anwendung: Styles, Markup, Rechenkern (einzige Quelle) |
| `build.py` | Verpackt `src/app.html` in ein vollständiges HTML-Dokument |
| `index.html` | Erzeugt – die auslieferbare Seite |

`src/app.html` ist bewusst ohne `<!doctype>`/`<html>`/`<head>`/`<body>` geschrieben,
damit dieselbe Quelle als eigenständige Seite **und** als eingebettetes Artifact läuft.

## Rechenregel

Jeder Schritt ist definiert durch **Anker**, **Versatz**, **Ziel-Wochentag** und
**Suchrichtung**:

1. `Basis = Termin des Ankerschritts + Versatz` (Kalendertage).
   Schritt 24 (E-Tag) ist die Wurzel und rechnet vom Erscheinungstermin.
2. Ist die Basis ein Wochenende, ein Feiertag oder – bei festem Ziel-Wochentag –
   der falsche Wochentag, wird der nächste zulässige Tag gesucht:
   * `Richtung = rückwärts` (Standard): letzter zulässiger Tag ≤ Basis
   * `Richtung = vorwärts`: erster zulässiger Tag ≥ Basis (nur Schritt 7)
3. Bei festem Ziel-Wochentag zählen nur Tage dieses Wochentags, die kein
   Feiertag sind; bei „flexibel“ jeder Arbeitstag (Mo–Fr, kein Feiertag).

Der Erscheinungstermin selbst wird vorab auf den letzten Arbeitstag gezogen,
falls er auf ein Wochenende oder einen Feiertag fällt.

Anker, Versatz, Ziel-Wochentag, Richtung und Phase sind im Reiter **Regelwerk**
frei änderbar; Zirkelbezüge werden erkannt und gemeldet.

## Manuelle Termine

Einzelne Termine lassen sich pro Ausgabe von Hand setzen – für Urlaubszeiten,
Feiertagsbrücken oder Sonderfälle. Ein Klick auf eine Zelle im Terminplan oder
auf eine Zeile in der Ausgaben-Ansicht öffnet die Eingabe; sie zeigt den
automatischen Termin zum Vergleich und warnt, wenn das gewählte Datum auf ein
Wochenende, einen Feiertag oder den falschen Wochentag fällt – ohne es zu
verhindern, denn die Entscheidung trifft die Redaktion.

Ein fester Termin wird unverändert übernommen. **Alle Schritte, die ihn als
Anker haben, rechnen von dort aus weiter** – in der Rückwärtskette sind das die
vorgelagerten Schritte. Zieht man etwa den Start der Seitenfreigabe im Mai-Heft
eine Woche vor, wandern Redaktionsschluss, Anzeigenschluss, beide
Redaktionskonferenzen und der Druckunterlagenschluss mit; alles nach dem
Seitenfreigabe-Start bleibt am E-Tag verankert.

Gesetzte Termine sind blau markiert, stehen gesammelt in der Karte *Manuelle
Termine* und lassen sich einzeln oder gesamt auf Automatik zurückstellen. Der
Export weist sie in der Spalte *Herkunft* aus. Ein Jahreswechsel oder ein neuer
Terminvorschlag verwirft sie (mit „Rückgängig“ wiederherstellbar), weil die
Daten sonst nicht mehr zum Plan passen.

## Unterschiede zur Excel-Vorlage

| Punkt | Excel | Diese Seite |
|---|---|---|
| Feiertagsjahre | nur das Planungsjahr | Vor-, Planungs- und Folgejahr – das Januar/Februar-Heft wird im Dezember des Vorjahres produziert, dessen Weihnachtsfeiertage die Excel nicht kennt |
| Internationaler Frauentag (8.3.) | fehlt | enthalten (seit 2019 gesetzlicher Feiertag in Berlin) |
| Reformationstag (31.10.) | enthalten | abgeschaltet (in Berlin kein gesetzlicher Feiertag) |
| Heiligabend / Silvester | – | abschaltbare Vorschläge für Betriebsruhe |

Die Schaltfläche **„Feiertage wie in der Excel“** stellt den Excel-Stand her.
Für 2027 sind beide Varianten bis auf die Frauentags-Kette identisch.

## Prüfungen

Der Reiter *Prüfung* meldet unter anderem verschobene Erscheinungstermine,
Schritte, die durch Feiertagsketten um drei Tage oder mehr wandern, Termine
zwischen den Jahren, Schritte hinter ihrem Anker, Ausgaben in falscher
Reihenfolge und ungewöhnliche Vorlaufzeiten.

## Export

CSV-Matrix und CSV-Terminliste (Semikolon + BOM, öffnen direkt in Excel),
`.ics` mit jedem Termin als ganztägiger Kalendereintrag, JSON-Konfiguration
zum Sichern und Weitergeben sowie eine Druckansicht (A4 quer).
