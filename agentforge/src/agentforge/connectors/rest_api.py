"""Generischer REST-Konnektor, kompatibel mit Graph-artigen JSON-APIs."""

from __future__ import annotations

from typing import Any

import requests

from .base import Connector


class RestApiConnector(Connector):
    """Generischer REST-Konnektor mit Bearer-Token-Authentifizierung.

    Die Session ist injizierbar (Dependency Injection), damit sie in Tests
    durch ein Fake-Objekt ersetzt werden kann – ohne echten Netzwerkzugriff.
    """

    def __init__(
        self,
        base_url: str,
        token: str | None = None,
        session: "requests.Session | None" = None,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.token = token
        self.session = session or requests.Session()

    def _headers(self) -> dict[str, str]:
        headers = {"Accept": "application/json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

    def fetch(self, resource: str) -> Any:
        response = self.session.get(
            f"{self.base_url}/{resource.lstrip('/')}", headers=self._headers(), timeout=10
        )
        response.raise_for_status()
        return response.json()

    def push(self, resource: str, data: Any) -> None:
        response = self.session.post(
            f"{self.base_url}/{resource.lstrip('/')}", json=data, headers=self._headers(), timeout=10
        )
        response.raise_for_status()
