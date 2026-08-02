"""
SuperNinja shared logging helpers (Sprint 75 task 12, 19).

Provides:
- get_logger(name)            : ready-to-use logger with rotating file handler
- json_logger(name)           : structured JSON logger (one record per line)
- new_correlation_id()        : per-command trace id
- with_correlation_id(logger) : LoggerAdapter that injects {cid: ...} into every record

Log files rotate at 10 MB by default and keep 5 backups.
"""

from __future__ import annotations

import json
import logging
import logging.handlers
import os
import time
import uuid
from typing import Optional

DEFAULT_LOG_DIR = os.environ.get("SN_LOG_DIR", "/workspace/logs")
DEFAULT_MAX_BYTES = int(os.environ.get("SN_LOG_MAX_BYTES", str(10 * 1024 * 1024)))
DEFAULT_BACKUP_COUNT = int(os.environ.get("SN_LOG_BACKUP_COUNT", "5"))


def _ensure_dir(path: str) -> None:
    try:
        os.makedirs(path, exist_ok=True)
    except OSError:
        pass


def get_logger(
    name: str,
    *,
    log_dir: str = DEFAULT_LOG_DIR,
    max_bytes: int = DEFAULT_MAX_BYTES,
    backup_count: int = DEFAULT_BACKUP_COUNT,
    level: Optional[int] = None,
) -> logging.Logger:
    """Return a logger that writes to console + a rotating file in log_dir."""
    logger = logging.getLogger(name)
    if getattr(logger, "_sn_configured", False):
        return logger

    logger.setLevel(level or os.environ.get("SN_LOG_LEVEL", "INFO"))
    fmt = logging.Formatter(
        "%(asctime)s %(levelname)s [%(name)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Console
    sh = logging.StreamHandler()
    sh.setFormatter(fmt)
    logger.addHandler(sh)

    # Rotating file
    _ensure_dir(log_dir)
    try:
        fh = logging.handlers.RotatingFileHandler(
            os.path.join(log_dir, f"{name}.log"),
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding="utf-8",
        )
        fh.setFormatter(fmt)
        logger.addHandler(fh)
    except OSError:
        # Read-only filesystem etc. — keep going with console only.
        pass

    logger._sn_configured = True  # type: ignore[attr-defined]
    return logger


class _JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "ts": time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime(record.created)),
            "lvl": record.levelname,
            "logger": record.name,
            "msg": record.getMessage(),
        }
        cid = getattr(record, "cid", None)
        if cid:
            payload["cid"] = cid
        if record.exc_info:
            payload["exc"] = self.formatException(record.exc_info)
        return json.dumps(payload, ensure_ascii=False)


def json_logger(
    name: str,
    *,
    log_dir: str = DEFAULT_LOG_DIR,
    max_bytes: int = DEFAULT_MAX_BYTES,
    backup_count: int = DEFAULT_BACKUP_COUNT,
) -> logging.Logger:
    """JSON-structured logger (one JSON record per line)."""
    logger = logging.getLogger(f"{name}.json")
    if getattr(logger, "_sn_configured", False):
        return logger
    logger.setLevel(os.environ.get("SN_LOG_LEVEL", "INFO"))

    _ensure_dir(log_dir)
    try:
        fh = logging.handlers.RotatingFileHandler(
            os.path.join(log_dir, f"{name}.jsonl"),
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding="utf-8",
        )
        fh.setFormatter(_JsonFormatter())
        logger.addHandler(fh)
    except OSError:
        pass

    logger._sn_configured = True  # type: ignore[attr-defined]
    return logger


def new_correlation_id() -> str:
    """Short id for tracing one command end-to-end."""
    return uuid.uuid4().hex[:12]


class _CidAdapter(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        cid = self.extra.get("cid")
        if cid:
            kwargs.setdefault("extra", {})["cid"] = cid
            return f"[cid={cid}] {msg}", kwargs
        return msg, kwargs


def with_correlation_id(logger: logging.Logger, cid: Optional[str] = None) -> logging.LoggerAdapter:
    return _CidAdapter(logger, {"cid": cid or new_correlation_id()})
