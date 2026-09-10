"""Kommandozeilen-Interface für AgentForge mit mehreren Subkommandos."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd

from .agents.data_agent import DataCleaningAgent
from .agents.doc_agent import DocumentationAgent
from .agents.monitor_agent import MonitoringAgent
from .agents.base import AgentContext
from .connectors.filesystem import FileSystemConnector
from .providers import get_provider


def _cmd_doc_scan(args: argparse.Namespace) -> int:
    provider = get_provider(args.provider)
    agent = DocumentationAgent(provider=provider, project_path=args.path, limit=args.limit)
    context = agent.run(AgentContext())

    suggestions = context.data["doc_suggestions"]
    if not suggestions:
        print("Keine Funktionen ohne Docstring gefunden. ✅")
        return 0

    lines = ["# AgentForge – Dokumentations-Vorschläge", ""]
    for item in suggestions:
        lines.append(f"## `{item['function']}` – {item['file']}:{item['line']}")
        lines.append("")
        lines.append(item["suggestion"].strip())
        lines.append("")
    report = "\n".join(lines)

    if args.output:
        Path(args.output).write_text(report, encoding="utf-8")
        print(f"Report geschrieben nach: {args.output}")
    else:
        print(report)
    return 0


def _cmd_clean_data(args: argparse.Namespace) -> int:
    df = pd.read_csv(args.input)
    dedupe_subset = args.dedupe.split(",") if args.dedupe else None

    agent = DataCleaningAgent(dedupe_subset=dedupe_subset, fill_strategy=args.fill_strategy)
    context = agent.run(AgentContext(data={"raw_dataframe": df}))

    cleaned = context.data["cleaned_dataframe"]
    cleaned.to_csv(args.output, index=False)
    print(
        f"Bereinigt: {context.data['rows_before']} → {context.data['rows_after']} Zeilen. "
        f"Ausgabe: {args.output}"
    )
    return 0


def _cmd_monitor(args: argparse.Namespace) -> int:
    connectors = {}
    for entry in args.connector:
        name, path = entry.split("=", 1)
        connectors[name] = FileSystemConnector(root=path)

    agent = MonitoringAgent(connectors=connectors)
    context = agent.run(AgentContext())

    for name, status in context.data["monitoring"].items():
        print(f"{name}: {status}")
    return 0


def build_arg_parser() -> argparse.ArgumentParser:
    """Erstellt den Argument-Parser mit allen Subkommandos."""
    parser = argparse.ArgumentParser(
        prog="agentforge",
        description="Modulares Framework für KI-Agenten und Automatisierung.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    doc_scan = subparsers.add_parser("doc-scan", help="Findet undokumentierte Funktionen und schlägt Docstrings/Tests vor")
    doc_scan.add_argument("path", type=Path)
    doc_scan.add_argument("--provider", choices=["openai", "claude"], default="openai")
    doc_scan.add_argument("--limit", type=int, default=None)
    doc_scan.add_argument("--output", type=Path, default=None)
    doc_scan.set_defaults(func=_cmd_doc_scan)

    clean_data = subparsers.add_parser("clean-data", help="Bereinigt eine CSV-Datei (Duplikate, fehlende Werte)")
    clean_data.add_argument("input", type=Path)
    clean_data.add_argument("output", type=Path)
    clean_data.add_argument("--dedupe", type=str, default=None, help="Kommagetrennte Spalten für Duplikat-Erkennung")
    clean_data.add_argument("--fill-strategy", choices=["mean", "median", "zero"], default="mean")
    clean_data.set_defaults(func=_cmd_clean_data)

    monitor = subparsers.add_parser("monitor", help="Prüft den Status konfigurierter Konnektoren")
    monitor.add_argument(
        "--connector", action="append", default=[], help="name=pfad, mehrfach angebbar"
    )
    monitor.set_defaults(func=_cmd_monitor)

    return parser


def main(argv: list[str] | None = None) -> int:
    """Einstiegspunkt des CLI-Tools."""
    parser = build_arg_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
