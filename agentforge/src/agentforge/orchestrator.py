"""Pipeline: verkettet mehrere Agents und reicht den Context durch."""

from __future__ import annotations

from .agents.base import AgentContext, BaseAgent
from .logging_utils import get_logger


class Pipeline:
    """Führt eine geordnete Liste von Agents nacheinander aus."""

    def __init__(self, agents: list[BaseAgent], log_dir: str = "logs") -> None:
        self.agents = agents
        # Logger-Name enthält log_dir, damit zwei Pipelines mit unterschiedlichen
        # Log-Verzeichnissen (z. B. in Tests) nicht denselben gecachten Logger teilen.
        self.logger = get_logger(f"pipeline[{log_dir}]", log_dir=log_dir)

    def run(self, initial_data: dict | None = None) -> AgentContext:
        """Führt alle Agents nacheinander aus und gibt den finalen Context zurück."""
        context = AgentContext(data=dict(initial_data or {}))
        for agent in self.agents:
            self.logger.info(f"Starte Agent: {agent.name}", extra={"agent": agent.name})
            context = agent.run(context)
            self.logger.info(f"Agent abgeschlossen: {agent.name}", extra={"agent": agent.name})
        return context
