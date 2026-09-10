"""Tests für die Provider-Abstraktion (providers.py) – API-Aufrufe werden gemockt."""

import pytest

from agentforge.providers import ClaudeProvider, OpenAIProvider, get_provider


def test_openai_provider_raises_without_api_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    provider = OpenAIProvider(api_key=None)
    with pytest.raises(RuntimeError):
        provider.generate("Hallo")


def test_claude_provider_raises_without_api_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    provider = ClaudeProvider(api_key=None)
    with pytest.raises(RuntimeError):
        provider.generate("Hallo")


def test_get_provider_returns_correct_type() -> None:
    assert isinstance(get_provider("openai"), OpenAIProvider)
    assert isinstance(get_provider("claude"), ClaudeProvider)
    assert isinstance(get_provider("anthropic"), ClaudeProvider)


def test_get_provider_rejects_unknown_name() -> None:
    with pytest.raises(ValueError):
        get_provider("does-not-exist")
