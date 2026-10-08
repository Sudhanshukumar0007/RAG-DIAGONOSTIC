"""
shared_logger.py — centralized rotating logger for the RAG diagnostic experiment.
Every script imports get_logger() from here so all steps go to the same log file.
"""

import logging
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path

LOG_DIR = Path(__file__).parent / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / "experiment.log"

_logger: logging.Logger | None = None


def get_logger(name: str = "rag_diagnostic") -> logging.Logger:
    """Return (and lazily create) the shared experiment logger."""
    global _logger
    if _logger is not None:
        return _logger

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # ---------- Console handler (INFO and above) ----------
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_fmt = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(message)s", datefmt="%H:%M:%S"
    )
    console_handler.setFormatter(console_fmt)

    # ---------- File handler (DEBUG and above, rotating 10 MB × 3) ----------
    file_handler = RotatingFileHandler(
        LOG_FILE, maxBytes=10 * 1024 * 1024, backupCount=3, encoding="utf-8"
    )
    file_handler.setLevel(logging.DEBUG)
    file_fmt = logging.Formatter(
        "%(asctime)s [%(levelname)-8s] [%(module)s:%(lineno)d] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    file_handler.setFormatter(file_fmt)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    # Silence noisy third-party loggers
    for noisy in ("httpx", "httpcore", "urllib3", "chromadb", "sentence_transformers"):
        logging.getLogger(noisy).setLevel(logging.WARNING)

    _logger = logger
    return logger
