"""Zentrale Konfiguration von AgentForge, geladen aus Umgebungsvariablen."""

from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass
class Settings:
    """Laufzeitkonfiguration für AgentForge."""

    openai_api_key: str | None = None
    anthropic_api_key: str | None = None
    log_dir: str = "logs"

    @classmethod
    def from_env(cls) -> "Settings":
        """Lädt die Konfiguration aus den Umgebungsvariablen (bzw. einer .env-Datei)."""
        return cls(
            openai_api_key=os.environ.get("OPENAI_API_KEY"),
            anthropic_api_key=os.environ.get("ANTHROPIC_API_KEY"),
            log_dir=os.environ.get("AGENTFORGE_LOG_DIR", "logs"),
        )
