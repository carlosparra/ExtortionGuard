# app/core/logging.py
import logging
import sys
from app.core.config import settings

class EnsureRequestId(logging.Filter):
    """Inyecta request_id='' si no está presente en el LogRecord, evitando KeyError en el formatter."""
    def filter(self, record: logging.LogRecord) -> bool:
        if not hasattr(record, "request_id"):
            record.request_id = ""
        return True

def configure_logging() -> None:
    level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)

    handler = logging.StreamHandler(sys.stdout)
    handler.addFilter(EnsureRequestId())
    handler.setFormatter(logging.Formatter(
        "%(asctime)s %(levelname)s %(name)s [%(request_id)s] %(message)s"
    ))

    root = logging.getLogger()
    # limpiar handlers previos (útil con --reload)
    for h in list(root.handlers):
        root.removeHandler(h)
    root.addHandler(handler)
    root.setLevel(level)

    # asegúrate que uvicorn/fastapi propaguen al root
    for name in ("uvicorn", "uvicorn.error", "uvicorn.access", "fastapi"):
        lg = logging.getLogger(name)
        lg.setLevel(level)
        lg.propagate = True
