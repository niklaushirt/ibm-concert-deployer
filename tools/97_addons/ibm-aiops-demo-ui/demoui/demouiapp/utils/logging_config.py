"""
Logging configuration for IBM AIOps DemoUI.

Centralized logging setup that replaces scattered print() statements.
"""

import logging
import sys
from typing import Optional

_LOGGING_CONFIGURED = False


def setup_logging(
    level: int = logging.INFO,
    name: str = "demoui",
) -> logging.Logger:
    """
    Configure and return the root logger for the DemoUI application.

    Args:
        level: Logging level (default: logging.INFO).
        name: Logger name (default: 'demoui').

    Returns:
        Configured logger instance.
    """
    global _LOGGING_CONFIGURED
    if _LOGGING_CONFIGURED:
        return logging.getLogger(name)

    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Avoid duplicate handlers on repeated calls
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(level)
        formatter = logging.Formatter(
            fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    _LOGGING_CONFIGURED = True
    return logger


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """
    Get a logger instance, creating the root 'demoui' logger if none exists.

    Args:
        name: Optional sub-logger name. Prepended to 'demoui.' if provided.

    Returns:
        Logger instance.
    """
    if name:
        return logging.getLogger(f"demoui.{name}")
    return logging.getLogger("demoui")
