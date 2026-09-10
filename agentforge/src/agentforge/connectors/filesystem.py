"""Konnektor für lokale Dateien – nützlich für Tests und lokale Automatisierung."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .base import Connector


class FileSystemConnector(Connector):
    """Liest und schreibt Ressourcen relativ zu einem Wurzelverzeichnis."""

    def __init__(self, root: Path | str) -> None:
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

    def fetch(self, resource: str) -> str:
        path = self.root / resource
        if not path.exists():
            raise FileNotFoundError(f"Resource nicht gefunden: {resource}")
        return path.read_text(encoding="utf-8")

    def push(self, resource: str, data: Any) -> None:
        path = self.root / resource
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(str(data), encoding="utf-8")

    def list_resources(self, pattern: str = "*") -> list[str]:
        """Listet alle Dateien im Wurzelverzeichnis, die auf ``pattern`` passen."""
        return sorted(str(p.relative_to(self.root)) for p in self.root.glob(pattern) if p.is_file())
