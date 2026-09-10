"""Agent: prüft den Gesundheitsstatus konfigurierter Konnektoren (Monitoring)."""

from __future__ import annotations

import time

from ..connectors.base import Connector
from ..logging_utils import get_logger
from .base import AgentContext, BaseAgent


class MonitoringAgent(BaseAgent):
    """Führt für jeden übergebenen Konnektor einen einfachen Health-Check durch."""

    name = "monitoring-agent"

    def __init__(self, connectors: dict[str, Connector], health_resource: str = "health") -> None:
        self.connectors = connectors
        self.health_resource = health_resource
        self.logger = get_logger(self.name)

    def run(self, context: AgentContext) -> AgentContext:
        statuses: dict[str, dict] = {}
        for conn_name, connector in self.connectors.items():
            start = time.perf_counter()
            try:
                connector.fetch(self.health_resource)
                latency_ms = round((time.perf_counter() - start) * 1000, 2)
                statuses[conn_name] = {"status": "ok", "latency_ms": latency_ms}
            except Exception as exc:  # noqa: BLE001 - Monitoring soll nie hart abbrechen
                statuses[conn_name] = {"status": "error", "error": str(exc)}

            self.logger.info(
                "connector_check",
                extra={"connector": conn_name, "result": statuses[conn_name]},
            )

        context.data["monitoring"] = statuses
        return context
