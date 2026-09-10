"""Einheitliche Schnittstelle für verschiedene LLM-Anbieter (OpenAI, Claude)."""

from __future__ import annotations

import os
from abc import ABC, abstractmethod


class LLMProvider(ABC):
    """Basisklasse für einen generativen KI-Anbieter."""

    @abstractmethod
    def generate(self, prompt: str) -> str:
        """Erzeugt eine Textantwort für den gegebenen Prompt."""
        raise NotImplementedError


class OpenAIProvider(LLMProvider):
    """Anbindung an die OpenAI-API (Chat Completions)."""

    def __init__(self, api_key: str | None = None, model: str = "gpt-4o-mini") -> None:
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        self.model = model

    def generate(self, prompt: str) -> str:
        if not self.api_key:
            raise RuntimeError("Kein OPENAI_API_KEY gesetzt. Bitte in der .env-Datei hinterlegen.")

        from openai import OpenAI

        client = OpenAI(api_key=self.api_key)
        response = client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content or ""


class ClaudeProvider(LLMProvider):
    """Anbindung an die Anthropic-API (Claude)."""

    def __init__(self, api_key: str | None = None, model: str = "claude-sonnet-4-6") -> None:
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        self.model = model

    def generate(self, prompt: str) -> str:
        if not self.api_key:
            raise RuntimeError("Kein ANTHROPIC_API_KEY gesetzt. Bitte in der .env-Datei hinterlegen.")

        from anthropic import Anthropic

        client = Anthropic(api_key=self.api_key)
        response = client.messages.create(
            model=self.model,
            max_tokens=500,
            messages=[{"role": "user", "content": prompt}],
        )
        return "".join(block.text for block in response.content if hasattr(block, "text"))


def get_provider(name: str) -> LLMProvider:
    """Factory-Funktion: liefert die passende Provider-Instanz für ``name``."""
    normalized = name.strip().lower()
    if normalized == "openai":
        return OpenAIProvider()
    if normalized in {"claude", "anthropic"}:
        return ClaudeProvider()
    raise ValueError(f"Unbekannter Provider: {name!r} (erwartet 'openai' oder 'claude')")
