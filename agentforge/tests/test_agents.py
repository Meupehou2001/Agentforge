"""Tests für die einzelnen Agents – LLM-Provider und Konnektoren werden gemockt."""

from pathlib import Path

import pandas as pd
import pytest

from agentforge.agents.base import AgentContext
from agentforge.agents.data_agent import DataCleaningAgent
from agentforge.agents.doc_agent import DocumentationAgent
from agentforge.agents.monitor_agent import MonitoringAgent
from agentforge.connectors.filesystem import FileSystemConnector
from agentforge.providers import LLMProvider


class FakeProvider(LLMProvider):
    def __init__(self) -> None:
        self.calls: list[str] = []

    def generate(self, prompt: str) -> str:
        self.calls.append(prompt)
        return "def test_generated():\n    assert True"


def test_documentation_agent_generates_suggestions(tmp_path: Path) -> None:
    (tmp_path / "module.py").write_text("def foo():\n    return 1\n", encoding="utf-8")
    provider = FakeProvider()
    agent = DocumentationAgent(provider=provider, project_path=tmp_path)

    context = agent.run(AgentContext())

    assert len(context.data["doc_suggestions"]) == 1
    assert context.data["doc_suggestions"][0]["function"] == "foo"
    assert len(provider.calls) == 1


def test_data_cleaning_agent_cleans_dataframe() -> None:
    df = pd.DataFrame({"a": [1.0, 1.0, None], "b": ["x", "x", "y"]})
    agent = DataCleaningAgent(dedupe_subset=["a", "b"], fill_strategy="zero")

    context = agent.run(AgentContext(data={"raw_dataframe": df}))

    cleaned = context.data["cleaned_dataframe"]
    assert len(cleaned) == 2
    assert context.data["rows_before"] == 3
    assert context.data["rows_after"] == 2


def test_data_cleaning_agent_raises_without_input() -> None:
    agent = DataCleaningAgent()
    with pytest.raises(ValueError):
        agent.run(AgentContext())


def test_monitoring_agent_reports_ok_for_healthy_connector(tmp_path: Path) -> None:
    connector = FileSystemConnector(root=tmp_path)
    connector.push("health", "ok")
    agent = MonitoringAgent(connectors={"local": connector})

    context = agent.run(AgentContext())

    assert context.data["monitoring"]["local"]["status"] == "ok"


def test_monitoring_agent_reports_error_for_missing_resource(tmp_path: Path) -> None:
    connector = FileSystemConnector(root=tmp_path)  # keine "health"-Datei angelegt
    agent = MonitoringAgent(connectors={"local": connector})

    context = agent.run(AgentContext())

    assert context.data["monitoring"]["local"]["status"] == "error"
