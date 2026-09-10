"""Statische Analyse von Python-Dateien: findet Funktionen ohne Docstring."""

from __future__ import annotations

import ast
from dataclasses import dataclass
from pathlib import Path


@dataclass
class FunctionInfo:
    """Beschreibt eine gefundene Funktion ohne Docstring."""

    name: str
    file_path: Path
    lineno: int
    source: str


def find_python_files(root: Path) -> list[Path]:
    """Liefert alle .py-Dateien unterhalb von ``root`` (rekursiv)."""
    return sorted(p for p in root.rglob("*.py") if p.is_file())


def find_undocumented_functions(file_path: Path) -> list[FunctionInfo]:
    """Findet alle Funktionen (inkl. Methoden) ohne Docstring in einer Datei."""
    source_text = file_path.read_text(encoding="utf-8")
    tree = ast.parse(source_text, filename=str(file_path))

    results: list[FunctionInfo] = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if ast.get_docstring(node) is None:
                snippet = ast.get_source_segment(source_text, node) or ""
                results.append(
                    FunctionInfo(name=node.name, file_path=file_path, lineno=node.lineno, source=snippet)
                )
    return results


def analyze_project(root: Path) -> list[FunctionInfo]:
    """Analysiert alle Python-Dateien in ``root`` und sammelt Funktionen ohne Docstring."""
    findings: list[FunctionInfo] = []
    for file_path in find_python_files(root):
        findings.extend(find_undocumented_functions(file_path))
    return findings
