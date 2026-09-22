"""
Data injection modules for IBM AIOps DemoUI.

Replaces the thin wrapper functions in functions.py with a data-driven approach.
"""

from .event_injector import EventConfig, inject_events, inject_events_repeated
from .log_injector import (
    LogConfig,
    inject_logs_continuous,
    inject_logs_generic,
)
from .metric_injector import (
    MetricDefinition,
    inject_metrics,
    parse_metric_line,
)

__all__ = [
    # Event injection
    "EventConfig",
    "inject_events",
    "inject_events_repeated",
    # Log injection
    "LogConfig",
    "inject_logs_continuous",
    "inject_logs_generic",
    # Metric injection
    "MetricDefinition",
    "inject_metrics",
    "parse_metric_line",
]
