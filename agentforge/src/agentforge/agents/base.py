"""Gemeinsame Basis für alle Agents sowie der geteilte Pipeline-Kontext."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass
class AgentContext:
    """Zustand, der zwischen Agents innerhalb einer Pipeline weitergereicht wird."""

    data: dict[str, Any] = field(default_factory=dict)


class BaseAgent(ABC):
    """Basisklasse: jeder Agent transformiert einen ``AgentContext``."""

    name: str = "base-agent"

    @abstractmethod
    def run(self, context: AgentContext) -> AgentContext:
        """Führt die Agent-Logik aus und gibt den (ggf. veränderten) Context zurück."""
        raise NotImplementedError
