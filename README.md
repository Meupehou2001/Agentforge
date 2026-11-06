# AgentForge

**Ein kleines Python-Framework, mit dem sich KI-Agenten und Automatisierungsschritte zu einer eigenen Pipeline zusammenstecken lassen.**

![Python](https://img.shields.io/badge/Python-3.x-blue) ![Tests](https://img.shields.io/badge/Tests-pytest-green) ![Lizenz](https://img.shields.io/badge/Lizenz-MIT-lightgrey)

---

## Worum geht es?

Viele Aufgaben in der Softwareentwicklung wiederholen sich: Code dokumentieren, Daten aufräumen, prüfen, ob Schnittstellen noch erreichbar sind. AgentForge zerlegt solche Aufgaben in kleine **Agents**. Jeder Agent erledigt genau eine Aufgabe. Eine **Pipeline** verbindet mehrere Agents zu einem Ablauf und gibt die Ergebnisse von Schritt zu Schritt weiter.

Das Projekt ist als kleines, aber vollständiges Framework gebaut und nicht als einzelnes Skript. Es zeigt, wie man KI-Modelle (OpenAI und Claude), Daten und Automatisierung sauber voneinander trennt und testbar macht.

## Was kann AgentForge?

Zurzeit gibt es drei fertige Agents:

- **Dokumentations-Agent:** Durchsucht ein Python-Projekt nach Funktionen ohne Docstring und lässt ein Sprachmodell (OpenAI oder Claude) Vorschläge für Dokumentation und Tests schreiben.
- **Daten-Agent:** Bereinigt eine CSV-Datei. Er entfernt Duplikate, füllt fehlende Werte auf (zum Beispiel mit dem Median) und erkennt Ausreißer.
- **Monitoring-Agent:** Prüft, ob angebundene Datenquellen (lokale Ordner oder REST-APIs) erreichbar sind.

Du kannst sie einzeln über die Kommandozeile nutzen oder in Python zu einer eigenen Pipeline verketten.

## So funktioniert es

1. Jeder Agent erbt von `BaseAgent` und hat eine Methode `run(context)`.
2. Die `Pipeline` führt die Agents nacheinander aus.
3. Alle Agents teilen sich einen gemeinsamen `AgentContext`, in dem Zwischenergebnisse liegen.
4. Jeder Schritt wird als JSON-Log in einer Datei und in der Konsole festgehalten.

Die KI-Modelle (OpenAI, Claude) und die Datenquellen (Dateisystem, REST-API) sind über einheitliche Schnittstellen angebunden. Dadurch lassen sie sich austauschen, ohne die Agents zu ändern.

## Schnellstart

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
cp .env.example .env    # hier deine API-Schlüssel eintragen
```

### Beispiele für die Kommandozeile

Nicht dokumentierten Code finden und Vorschläge erzeugen:

```bash
agentforge doc-scan ./mein_projekt --provider openai --output report.md
agentforge doc-scan ./mein_projekt --provider claude --limit 5
```

CSV-Datei bereinigen:

```bash
agentforge clean-data rohdaten.csv bereinigt.csv --dedupe id,email --fill-strategy median
```

Datenquellen überwachen:

```bash
agentforge monitor --connector local=./data --connector backup=./backup
```

### Eigene Pipeline in Python

```python
import pandas as pd
from agentforge.orchestrator import Pipeline
from agentforge.agents.data_agent import DataCleaningAgent
from agentforge.agents.monitor_agent import MonitoringAgent
from agentforge.connectors.filesystem import FileSystemConnector

pipeline = Pipeline(agents=[
    DataCleaningAgent(dedupe_subset=["id"], fill_strategy="median"),
    MonitoringAgent(connectors={"data": FileSystemConnector("./data")}),
])

result = pipeline.run(initial_data={"raw_dataframe": pd.read_csv("input.csv")})
print(result.data["cleaned_dataframe"].head())
print(result.data["monitoring"])
```

## Projektaufbau

```
agentforge/
├── agents/            # die drei Agents (Doku, Daten, Monitoring)
├── connectors/        # Anbindung an Dateisystem und REST-APIs
├── data/              # Datenbereinigung mit pandas
├── providers.py       # gemeinsame Schnittstelle zu OpenAI und Claude
├── codeanalysis.py    # findet Funktionen ohne Docstring
├── orchestrator.py    # die Pipeline
├── logging_utils.py   # strukturiertes JSON-Logging
└── cli.py             # Kommandozeile
```

## Tests

Alle Module sind mit `pytest` getestet. Aufrufe an KI-Modelle und REST-APIs werden dabei ersetzt (gemockt). Die Tests laufen deshalb ohne API-Schlüssel und ohne Internet:

```bash
pytest -v
```

## Warum dieses Projekt?

Ich wollte praktische Erfahrung mit dem sammeln, was moderne Softwareentwicklung mit generativer KI ausmacht: Anbindung von Sprachmodellen, Datenaufbereitung, Automatisierung, Tests und Logging. AgentForge zeigt dabei eine klare Trennung der Verantwortlichkeiten (Provider, Connector, Agent, Pipeline) und die Bausteine, die in größeren KI-Projekten ähnlich vorkommen.

## Mögliche Erweiterungen

- Azure-Konnektor, analog zum REST-Konnektor
- MCP-Konnektor, damit Agents externe Werkzeuge aufrufen können
- Pipelines per YAML-Datei konfigurieren
- Wiederholungsversuche (Retry und Backoff) bei Fehlern der KI-Anbieter

## Lizenz

MIT. Details stehen in der Datei [LICENSE](LICENSE).

## Autor

**Ulrich Varnel Meupehou Moutcheu**, Student der Medieninformatik an der Hochschule Osnabrück. Weitere Projekte findest du auf meinem GitHub-Profil: [github.com/Meupehou2001](https://github.com/Meupehou2001)
