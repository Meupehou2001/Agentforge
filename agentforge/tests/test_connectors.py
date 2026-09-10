"""Tests für die Konnektoren (filesystem.py, rest_api.py) – kein echter Netzwerkzugriff."""

from pathlib import Path

import pytest

from agentforge.connectors.filesystem import FileSystemConnector
from agentforge.connectors.rest_api import RestApiConnector


def test_filesystem_connector_push_and_fetch(tmp_path: Path) -> None:
    connector = FileSystemConnector(root=tmp_path)
    connector.push("notes/example.txt", "Hallo Welt")

    result = connector.fetch("notes/example.txt")

    assert result == "Hallo Welt"


def test_filesystem_connector_fetch_missing_raises(tmp_path: Path) -> None:
    connector = FileSystemConnector(root=tmp_path)
    with pytest.raises(FileNotFoundError):
        connector.fetch("does-not-exist.txt")


def test_filesystem_connector_list_resources(tmp_path: Path) -> None:
    connector = FileSystemConnector(root=tmp_path)
    connector.push("a.txt", "1")
    connector.push("b.txt", "2")

    resources = connector.list_resources("*.txt")

    assert resources == ["a.txt", "b.txt"]


class FakeResponse:
    def __init__(self, json_data, status_code=200):
        self._json_data = json_data
        self.status_code = status_code

    def raise_for_status(self):
        if self.status_code >= 400:
            raise RuntimeError(f"HTTP {self.status_code}")

    def json(self):
        return self._json_data


class FakeSession:
    def __init__(self):
        self.get_calls = []
        self.post_calls = []

    def get(self, url, headers=None, timeout=None):
        self.get_calls.append((url, headers))
        return FakeResponse({"status": "ok"})

    def post(self, url, json=None, headers=None, timeout=None):
        self.post_calls.append((url, json, headers))
        return FakeResponse({"received": json})


def test_rest_api_connector_fetch_uses_bearer_token() -> None:
    session = FakeSession()
    connector = RestApiConnector(base_url="https://api.example.com", token="secret-token", session=session)

    result = connector.fetch("health")

    assert result == {"status": "ok"}
    url, headers = session.get_calls[0]
    assert url == "https://api.example.com/health"
    assert headers["Authorization"] == "Bearer secret-token"


def test_rest_api_connector_push_sends_json() -> None:
    session = FakeSession()
    connector = RestApiConnector(base_url="https://api.example.com", session=session)

    connector.push("items", {"name": "Test"})

    url, payload, _ = session.post_calls[0]
    assert url == "https://api.example.com/items"
    assert payload == {"name": "Test"}
