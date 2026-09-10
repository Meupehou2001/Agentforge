"""Tests für die statische Codeanalyse (codeanalysis.py)."""

from pathlib import Path

from agentforge.codeanalysis import analyze_project, find_undocumented_functions

SAMPLE_CODE = '''
def documented_function():
    """Diese Funktion hat bereits einen Docstring."""
    return 42


def undocumented_function(x, y):
    return x + y


class Foo:
    def method_without_docstring(self):
        return self
'''


def test_find_undocumented_functions_detects_missing_docstrings(tmp_path: Path) -> None:
    file_path = tmp_path / "sample.py"
    file_path.write_text(SAMPLE_CODE, encoding="utf-8")

    findings = find_undocumented_functions(file_path)
    names = {f.name for f in findings}

    assert "undocumented_function" in names
    assert "method_without_docstring" in names
    assert "documented_function" not in names


def test_analyze_project_scans_all_python_files(tmp_path: Path) -> None:
    (tmp_path / "a.py").write_text("def a():\n    return 1\n", encoding="utf-8")
    (tmp_path / "b.py").write_text("def b():\n    \"\"\"Docstring.\"\"\"\n    return 2\n", encoding="utf-8")

    findings = analyze_project(tmp_path)
    names = {f.name for f in findings}

    assert names == {"a"}
