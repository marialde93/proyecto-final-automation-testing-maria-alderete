"""
Logger centralizado del framework.
Escribe en logs/suite.log con rotación automática (1MB, 5 backups).
"""
import logging
import pathlib
from logging.handlers import RotatingFileHandler

audit_dir = pathlib.Path("logs")
audit_dir.mkdir(exist_ok=True)

_handler = RotatingFileHandler(
    audit_dir / "suite.log",
    maxBytes=1024 * 1024,
    backupCount=5,
    encoding="utf-8",
)
_formatter = logging.Formatter(
    fmt="%(asctime)s %(levelname)s %(name)s - %(message)s",
    datefmt="%H:%M:%S",
)
_handler.setFormatter(_formatter)

logger = logging.getLogger("proyecto_final_alderete")
logger.setLevel(logging.INFO)
if not logger.handlers:
    logger.addHandler(_handler)
