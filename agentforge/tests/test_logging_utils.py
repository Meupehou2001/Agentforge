"""Tests für das strukturierte Logging (logging_utils.py)."""

import json
from pathlib import Path

from agentforge.logging_utils import get_logger


def test_get_logger_writes_valid_json_lines(tmp_path: Path) -> None:
    logger = get_logger("test-logger-unique", log_dir=str(tmp_path))
    logger.info("Testnachricht")

    log_file = tmp_path / "agentforge.log"
    lines = log_file.read_text(encoding="utf-8").strip().splitlines()

    assert len(lines) >= 1
    payload = json.loads(lines[-1])
    assert payload["message"] == "Testnachricht"
    assert payload["level"] == "INFO"


def test_get_logger_reuses_existing_handlers(tmp_path: Path) -> None:
    logger1 = get_logger("reuse-logger", log_dir=str(tmp_path))
    logger2 = get_logger("reuse-logger", log_dir=str(tmp_path))

    assert logger1 is logger2
    assert len(logger1.handlers) == len(logger2.handlers)
