# AgentForge – Framework für KI-Agenten & Automatisierung

AgentForge ist ein modulares Python-Framework, das zeigt, wie sich
einfache KI-Agenten, Datenanbindungen und Automatisierungsbausteine zu
einer wiederverwendbaren Pipeline kombinieren lassen. Es entstand, um
praktische Erfahrung in den Bereichen zu vertiefen, die für moderne
Softwareentwicklung mit generativer KI relevant sind: LLM-Integration,
API-Konnektoren, Datenaufbereitung, Testautomatisierung und Monitoring.

## Architektur

```
                       ┌────────────────────┐
                       │      Pipeline       │
                       │   (orchestrator.py) │
                       └─────────┬──────────┘
                                 │ AgentContext
        ┌────────────────────────┼────────────────────────┐
        │                        │                         │
┌───────▼────────┐     ┌─────────▼─────────┐     ┌─────────▼─────────┐
│ DocumentationAgent│  │ DataCleaningAgent  │     │  MonitoringAgent   │
│  (LLM-gestützt)  │   │  (pandas-basiert)  │     │ (Connector-Health) │
└───────┬────────┘     └─────────┬─────────┘     └─────────┬─────────┘
        │                        │                         │
┌───────▼────────┐     ┌─────────▼─────────┐     ┌─────────▼─────────┐
│ providers.py    │     │ data/cleaning.py   │     │ connectors/*.py    │
│ (OpenAI, Claude) │    │  (pandas)          │     │ (Filesystem, REST) │
└─────────────────┘     └────────────────────┘     └────────────────────┘
```

Jeder Agent erbt von `BaseAgent` und implementiert `run(context)`. Die
`Pipeline`-Klasse verkettet beliebig viele Agents und reicht einen
gemeinsamen `AgentContext` (ein einfaches Dict-Wrapper-Objekt) durch
alle Stufen weiter – inklusive strukturiertem JSON-Logging pro Schritt.

## Module im Überblick

| Modul | Zweck |
|---|---|
| `providers.py` | Einheitliche Schnittstelle zu OpenAI- und Claude-API |
| `codeanalysis.py` | Statische Analyse von Python-Code (`ast`) – findet Funktionen ohne Docstring |
| `connectors/filesystem.py` | Lesen/Schreiben lokaler Dateien über eine einheitliche Connector-Schnittstelle |
| `connectors/rest_api.py` | Generischer REST-Konnektor (Bearer-Token), kompatibel mit Graph-artigen APIs |
| `data/cleaning.py` | Datenaufbereitung mit pandas: Duplikate, fehlende Werte, Ausreißer |
| `agents/doc_agent.py` | Agent: generiert Docstring-/Test-Vorschläge per LLM |
| `agents/data_agent.py` | Agent: bereinigt einen DataFrame über eine Standardpipeline |
| `agents/monitor_agent.py` | Agent: prüft den Health-Status konfigurierter Konnektoren |
| `orchestrator.py` | `Pipeline`-Klasse zum Verketten mehrerer Agents |
| `logging_utils.py` | Strukturiertes JSON-Logging (Datei + Konsole) |
| `cli.py` | Kommandozeilen-Interface mit den Subkommandos `doc-scan`, `clean-data`, `monitor` |

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
cp .env.example .env   # API-Key(s) eintragen
```

## Nutzung (CLI)

**Undokumentierten Code finden und Vorschläge generieren:**
```bash
agentforge doc-scan ./mein_projekt --provider openai --output report.md
agentforge doc-scan ./mein_projekt --provider claude --limit 5
```

**CSV-Datei bereinigen (Duplikate entfernen, fehlende Werte auffüllen):**
```bash
agentforge clean-data rohdaten.csv bereinigt.csv --dedupe id,email --fill-strategy median
```

**Konnektoren überwachen:**
```bash
agentforge monitor --connector local=./data --connector backup=./backup
```

## Nutzung (als Bibliothek – eigene Pipeline bauen)

```python
from agentforge.orchestrator import Pipeline
from agentforge.agents.data_agent import DataCleaningAgent
from agentforge.agents.monitor_agent import MonitoringAgent
from agentforge.connectors.filesystem import FileSystemConnector
import pandas as pd

pipeline = Pipeline(agents=[
    DataCleaningAgent(dedupe_subset=["id"], fill_strategy="median"),
    MonitoringAgent(connectors={"data": FileSystemConnector("./data")}),
])

result = pipeline.run(initial_data={"raw_dataframe": pd.read_csv("input.csv")})
print(result.data["cleaned_dataframe"].head())
print(result.data["monitoring"])
```

## Tests

Alle Module sind mit `pytest` getestet – LLM-Aufrufe und REST-Requests
werden konsequent gemockt, sodass die komplette Suite **ohne** echte
API-Keys und **ohne** Netzwerkzugriff läuft:

```bash
pytest -v
```

Abgedeckt sind: Codeanalyse, Provider-Fehlerbehandlung, beide
Konnektoren, Datenbereinigung, alle drei Agents, die Pipeline-Reihenfolge
sowie das strukturierte Logging.

## Motivation & Ausblick

Das Projekt ist bewusst als kleines, aber vollständiges Framework
aufgebaut statt als einzelnes Skript: Es zeigt Trennung von
Verantwortlichkeiten (Provider / Connector / Agent / Pipeline),
Testautomatisierung und strukturiertes Logging – Bausteine, die in
größeren KI-Automatisierungsprojekten in ähnlicher Form vorkommen.

Mögliche Erweiterungen: Azure-Konnektor (analog zu `rest_api.py`),
MCP-Konnektor für Agent-Tool-Aufrufe, YAML-basierte Pipeline-Konfiguration,
Retry-/Backoff-Logik für die API-Provider.

## Lizenz

MIT – siehe [LICENSE](./LICENSE).
