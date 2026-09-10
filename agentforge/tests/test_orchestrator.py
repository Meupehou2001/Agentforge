"""Tests für die Pipeline (orchestrator.py) – verkettet mehrere (Fake-)Agents."""

from agentforge.agents.base import AgentContext, BaseAgent
from agentforge.orchestrator import Pipeline


class AddOneAgent(BaseAgent):
    name = "add-one"

    def run(self, context: AgentContext) -> AgentContext:
        context.data["counter"] = context.data.get("counter", 0) + 1
        return context


class DoubleAgent(BaseAgent):
    name = "double"

    def run(self, context: AgentContext) -> AgentContext:
        context.data["counter"] = context.data.get("counter", 0) * 2
        return context


def test_pipeline_runs_agents_in_order(tmp_path) -> None:
    pipeline = Pipeline(agents=[AddOneAgent(), DoubleAgent()], log_dir=str(tmp_path))

    result = pipeline.run(initial_data={"counter": 3})

    # (3 + 1) * 2 = 8  -> beweist, dass die Reihenfolge eingehalten wird
    assert result.data["counter"] == 8


def test_pipeline_writes_structured_logs(tmp_path) -> None:
    pipeline = Pipeline(agents=[AddOneAgent()], log_dir=str(tmp_path))
    pipeline.run(initial_data={})

    log_file = tmp_path / "agentforge.log"
    assert log_file.exists()
    content = log_file.read_text(encoding="utf-8")
    assert "add-one" in content
