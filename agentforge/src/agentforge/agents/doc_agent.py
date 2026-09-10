"""Agent: generiert Docstring- und Test-Vorschläge für undokumentierten Code."""

from __future__ import annotations

from pathlib import Path

from ..codeanalysis import analyze_project
from ..providers import LLMProvider
from .base import AgentContext, BaseAgent

DOCSTRING_PROMPT_TEMPLATE = """\
Du bist ein erfahrener Python-Entwickler. Schlage für die folgende Funktion
einen kurzen, prägnanten Docstring (Google-Style) sowie einen einfachen
pytest-Unit-Test vor. Antworte ausschließlich mit Code, ohne Erklärtext.

Funktion:
```python
{source}
```
"""


class DocumentationAgent(BaseAgent):
    """Findet Funktionen ohne Docstring und lässt Vorschläge per LLM generieren."""

    name = "documentation-agent"

    def __init__(self, provider: LLMProvider, project_path: Path | str, limit: int | None = None) -> None:
        self.provider = provider
        self.project_path = Path(project_path)
        self.limit = limit

    def run(self, context: AgentContext) -> AgentContext:
        findings = analyze_project(self.project_path)
        if self.limit is not None:
            findings = findings[: self.limit]

        suggestions = []
        for function in findings:
            prompt = DOCSTRING_PROMPT_TEMPLATE.format(source=function.source)
            suggestion = self.provider.generate(prompt)
            suggestions.append(
                {
                    "function": function.name,
                    "file": str(function.file_path),
                    "line": function.lineno,
                    "suggestion": suggestion,
                }
            )

        context.data["doc_suggestions"] = suggestions
        return context
