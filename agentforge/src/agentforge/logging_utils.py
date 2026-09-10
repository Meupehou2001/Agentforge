"""Strukturiertes JSON-Logging für Monitoring und Nachvollziehbarkeit."""

from __future__ import annotations

import json
import logging
from pathlib import Path


class JsonFormatter(logging.Formatter):
    """Formatiert Log-Einträge als einzeiliges JSON (JSON Lines)."""

    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "timestamp": self.formatTime(record, "%Y-%m-%dT%H:%M:%S"),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        for extra_field in ("connector", "result", "agent"):
            if hasattr(record, extra_field):
                payload[extra_field] = getattr(record, extra_field)
        return json.dumps(payload, ensure_ascii=False)


def get_logger(name: str, log_dir: str | Path = "logs") -> logging.Logger:
    """Erstellt (oder holt) einen Logger, der strukturiert nach Datei und Konsole schreibt."""
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger
    logger.setLevel(logging.INFO)
    logger.propagate = False

    log_path = Path(log_dir)
    log_path.mkdir(parents=True, exist_ok=True)

    file_handler = logging.FileHandler(log_path / "agentforge.log", encoding="utf-8")
    file_handler.setFormatter(JsonFormatter())
    logger.addHandler(file_handler)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(JsonFormatter())
    logger.addHandler(stream_handler)

    return logger
