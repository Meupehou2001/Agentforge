"""Gemeinsame Schnittstelle für alle Konnektoren."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class Connector(ABC):
    """Basisklasse für alle Datenquellen-Konnektoren (Dateisystem, REST-APIs, ...)."""

    @abstractmethod
    def fetch(self, resource: str) -> Any:
        """Liest eine Ressource und gibt sie zurück."""
        raise NotImplementedError

    @abstractmethod
    def push(self, resource: str, data: Any) -> None:
        """Schreibt Daten in eine Ressource."""
        raise NotImplementedError
