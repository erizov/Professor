import logging
from typing import Optional

_INITIALIZED: Optional[bool] = None


def _ensure_basic_config() -> None:
    global _INITIALIZED
    if _INITIALIZED:
        return
    root = logging.getLogger()
    # Configure only if no handlers exist (prevents duplicates under pytest or multiple imports)
    if not root.handlers:
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        )
    _INITIALIZED = True


def get_logger(name: str) -> logging.Logger:
    """Return a module-level logger with sane defaults.

    Ensures basic configuration is present once. Algorithms can call:
        from framework.logging_utils import get_logger
        logger = get_logger(__name__)
        logger.info("message")
    """
    _ensure_basic_config()
    return logging.getLogger(name)
