"""
Repository module for IBM AIOps DemoUI.

Single import point for all refactored modules. This module re-exports
all public symbols from injectors, scenarios, and utilities so that
existing code (views.py) can import from a single location.

Usage:
    from .repository import inject_events, RobotShopScenario, SUBSCRIPTION_ID
"""

# -----------------------------------------------------------------------------
# Constants
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# Legacy compatibility - re-export from functions.py for backward compatibility
# -----------------------------------------------------------------------------
from .functions import (
    CUSTOM_EVENTS,
    CUSTOM_LOGS,
    CUSTOM_METRICS,
    CUSTOM_NAME,
    CUSTOM_PROPERTY_RESOURCE_NAME,
    CUSTOM_PROPERTY_RESOURCE_TYPE,
    CUSTOM_PROPERTY_VALUES_NOK,
    CUSTOM_PROPERTY_VALUES_OK,
    CUSTOM_TOPOLOGY,
    CUSTOM_TOPOLOGY_APP_NAME,
    CUSTOM_TOPOLOGY_FORCE_RELOAD,
    CUSTOM_TOPOLOGY_TAG,
    DEMO_EVENTS_BUSY,
    DEMO_EVENTS_FAN_ACME,
    DEMO_EVENTS_MEM,
    DEMO_EVENTS_NET_SOCK,
    DEMO_EVENTS_ROBO_NET,
    DEMO_EVENTS_TELCO,
    DEMO_EVENTS_TUBE,
    DEMO_LOGS,
    DEMO_LOGS_SOCK,
    EVENTS_TIME_SKEW,
    GET_CONFIG,
    INCIDENT_URL_TUBE,
    INSTANCE_IMAGE,
    INSTANCE_NAME,
    # Configuration
    LOG_ITERATIONS,
    LOG_TIME_FORMAT,
    LOG_TIME_SKEW,
    LOG_TIME_STEPS,
    LOG_TIME_ZONE,
    METRIC_ITERATIONS,
    METRIC_TIME_SKEW,
    METRIC_TIME_STEP,
    METRICS_TO_SIMULATE_FAN,
    METRICS_TO_SIMULATE_FAN_ACME,
    METRICS_TO_SIMULATE_FAN_TEMP,
    METRICS_TO_SIMULATE_FAN_TEMP_ACME,
    METRICS_TO_SIMULATE_FIBER,
    METRICS_TO_SIMULATE_FIBER_NY,
    METRICS_TO_SIMULATE_MEM,
    METRICS_TO_SIMULATE_NET_SOCK,
    ROBOTSHOP_PROPERTY_RESOURCE_NAME,
    ROBOTSHOP_PROPERTY_RESOURCE_TYPE,
    ROBOTSHOP_PROPERTY_VALUES_NOK,
    ROBOTSHOP_PROPERTY_VALUES_OK,
    SLACK_URL_ACME,
    SLACK_URL_ROSH,
    SLACK_URL_SOSH,
    SNOW_URL_ACME,
    SNOW_URL_ROSH,
    SNOW_URL_SOSH,
    TOKEN,
    # Topology management
    checkTopology,
    closeAlerts,
    closeStories,
    injectEventsBusy,
    injectEventsCUSTOM,
    injectEventsFanACME,
    injectEventsGeneric,
    # Event injection
    injectEventsMemRobot,
    injectEventsNetRobot,
    injectEventsNetSock,
    injectEventsRisk,
    injectEventsTelco,
    injectEventsTube,
    injectLogsContinuous,
    injectLogsCUSTOM,
    injectLogsGeneric,
    # Log injection
    injectLogsRobotShop,
    injectLogsSockShop,
    injectMetrics,
    injectMetricsCUSTOM,
    injectMetricsFan,
    injectMetricsFanACME,
    injectMetricsFanTemp,
    injectMetricsFanTempACME,
    injectMetricsFiber,
    injectMetricsFiberTransatlantic,
    # Metric injection
    injectMetricsMem,
    injectMetricsSockNet,
    loadTopology,
    # Alert/Story management
    mitigateIssues,
    modifyMYSQL,
    modifyProperty,
    resetMYSQL,
)

# -----------------------------------------------------------------------------
# Event Injection
# -----------------------------------------------------------------------------
from .injectors.event_injector import (
    EventConfig,
    inject_events,
    inject_events_repeated,
)

# -----------------------------------------------------------------------------
# Log Injection
# -----------------------------------------------------------------------------
from .injectors.log_injector import (
    LogConfig,
    inject_logs_continuous,
    inject_logs_generic,
)

# -----------------------------------------------------------------------------
# Metric Injection
# -----------------------------------------------------------------------------
from .injectors.metric_injector import (
    MetricDefinition,
    inject_metrics,
    parse_metric_line,
)
from .scenarios.acme import AcmeScenario

# -----------------------------------------------------------------------------
# Scenarios
# -----------------------------------------------------------------------------
from .scenarios.base import Scenario
from .scenarios.custom import CustomScenario
from .scenarios.risk import RiskScenario
from .scenarios.robotshop import RobotShopScenario
from .scenarios.sockshop import SockShopScenario
from .scenarios.telco import TelcoScenario
from .utils.constants import (
    DATALAYER_API_PATH,
    DEFAULT_EVENTS_TIME_SKEW,
    DEFAULT_LOG_ITERATIONS,
    DEFAULT_LOG_TIME_FORMAT,
    DEFAULT_LOG_TIME_SKEW,
    DEFAULT_LOG_TIME_STEPS,
    DEFAULT_LOG_TIME_ZONE,
    DEFAULT_METRIC_BATCH_SIZE,
    DEFAULT_METRIC_ITERATIONS,
    DEFAULT_METRIC_TIME_SKEW,
    DEFAULT_METRIC_TIME_STEP,
    KAFKA_SASL_MECHANISM,
    KAFKA_SECURITY_PROTOCOL,
    METRICS_API_PATH,
    SUBSCRIPTION_ID,
    TOPOLOGY_API_PATH,
)

# -----------------------------------------------------------------------------
# Logging
# -----------------------------------------------------------------------------
from .utils.logging_config import get_logger, setup_logging

__all__ = [
    # Constants
    "SUBSCRIPTION_ID",
    "DATALAYER_API_PATH",
    "TOPOLOGY_API_PATH",
    "METRICS_API_PATH",
    "KAFKA_SECURITY_PROTOCOL",
    "KAFKA_SASL_MECHANISM",
    "DEFAULT_METRIC_BATCH_SIZE",
    "DEFAULT_METRIC_ITERATIONS",
    "DEFAULT_LOG_ITERATIONS",
    "DEFAULT_LOG_TIME_FORMAT",
    "DEFAULT_LOG_TIME_STEPS",
    "DEFAULT_LOG_TIME_SKEW",
    "DEFAULT_LOG_TIME_ZONE",
    "DEFAULT_EVENTS_TIME_SKEW",
    "DEFAULT_METRIC_TIME_SKEW",
    "DEFAULT_METRIC_TIME_STEP",
    # Logging
    "setup_logging",
    "get_logger",
    # Event injection
    "EventConfig",
    "inject_events",
    "inject_events_repeated",
    "injectEventsMemRobot",
    "injectEventsNetRobot",
    "injectEventsFanACME",
    "injectEventsNetSock",
    "injectEventsTube",
    "injectEventsTelco",
    "injectEventsBusy",
    "injectEventsRisk",
    "injectEventsCUSTOM",
    "injectEventsGeneric",
    # Log injection
    "LogConfig",
    "inject_logs_continuous",
    "inject_logs_generic",
    "injectLogsRobotShop",
    "injectLogsSockShop",
    "injectLogsCUSTOM",
    "injectLogsContinuous",
    "injectLogsGeneric",
    # Metric injection
    "MetricDefinition",
    "parse_metric_line",
    "inject_metrics",
    "injectMetricsMem",
    "injectMetricsFiber",
    "injectMetricsFiberTransatlantic",
    "injectMetricsFanTemp",
    "injectMetricsFan",
    "injectMetricsFanTempACME",
    "injectMetricsFanACME",
    "injectMetricsSockNet",
    "injectMetricsCUSTOM",
    "injectMetrics",
    # Scenarios
    "Scenario",
    "RobotShopScenario",
    "SockShopScenario",
    "AcmeScenario",
    "TelcoScenario",
    "CustomScenario",
    "RiskScenario",
    # Alert/Story management
    "mitigateIssues",
    "closeAlerts",
    "closeStories",
    # Topology management
    "checkTopology",
    "modifyProperty",
    "modifyMYSQL",
    "resetMYSQL",
    "loadTopology",
]
