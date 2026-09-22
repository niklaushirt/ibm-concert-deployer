"""
Tests for IBM AIOps DemoUI refactored modules.

Covers:
- Phase 4: Injector refactoring (event, log, metric injectors)
- Phase 5: Scenario definitions (RobotShop, SockShop, ACME, Telco, Custom, Risk)
- Phase 6: Reconciliation (functions.py merged with functions_NG.py)
- Phase 7: Type hints, docstrings, and repository module

Run with:
    python -m pytest demouiapp/tests_injectors.py -v
    # or from demoui/:
    python -m pytest demouiapp/tests_injectors.py -v
"""

import datetime
import os

# Ensure the project root is on the path
import sys
import unittest
from unittest.mock import MagicMock, mock_open, patch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestConstants(unittest.TestCase):
    """Test that constants are properly defined and accessible."""

    def test_subscription_id_is_string(self):
        from demouiapp.utils.constants import SUBSCRIPTION_ID

        self.assertIsInstance(SUBSCRIPTION_ID, str)
        self.assertEqual(SUBSCRIPTION_ID, "cfd95b7e-3bc7-4006-a4a8-a73a79c71255")

    def test_api_paths_are_defined(self):
        from demouiapp.utils.constants import (
            DATALAYER_API_PATH,
            METRICS_API_PATH,
            TOPOLOGY_API_PATH,
        )

        self.assertIn("/v1", DATALAYER_API_PATH)
        self.assertIn("/topology", TOPOLOGY_API_PATH)
        self.assertIn("/metrics", METRICS_API_PATH)

    def test_kafka_defaults(self):
        from demouiapp.utils.constants import (
            KAFKA_SASL_MECHANISM,
            KAFKA_SECURITY_PROTOCOL,
        )

        self.assertEqual(KAFKA_SECURITY_PROTOCOL, "SASL_SSL")
        self.assertEqual(KAFKA_SASL_MECHANISM, "SCRAM-SHA-512")

    def test_default_values(self):
        from demouiapp.utils.constants import (
            DEFAULT_EVENTS_TIME_SKEW,
            DEFAULT_LOG_ITERATIONS,
            DEFAULT_METRIC_BATCH_SIZE,
            DEFAULT_METRIC_ITERATIONS,
        )

        self.assertEqual(DEFAULT_METRIC_ITERATIONS, 80)
        self.assertEqual(DEFAULT_METRIC_BATCH_SIZE, 40)
        self.assertEqual(DEFAULT_LOG_ITERATIONS, 5)
        self.assertEqual(DEFAULT_EVENTS_TIME_SKEW, 10)


class TestLogging(unittest.TestCase):
    """Test logging configuration."""

    def test_setup_logging_returns_logger(self):
        from demouiapp.utils.logging_config import setup_logging

        logger = setup_logging()
        self.assertIsNotNone(logger)
        self.assertEqual(logger.name, "demoui")

    def test_get_logger_returns_logger(self):
        from demouiapp.utils.logging_config import get_logger

        logger = get_logger()
        self.assertIsNotNone(logger)

    def test_get_logger_with_name(self):
        from demouiapp.utils.logging_config import get_logger

        logger = get_logger("test_module")
        self.assertEqual(logger.name, "demoui.test_module")


class TestMetricDefinition(unittest.TestCase):
    """Test metric parsing from CSV lines."""

    def test_parse_metric_line(self):
        from demouiapp.injectors.metric_injector import parse_metric_line

        line = "mysql-predictive,MemoryUsagePercent,MemoryUsage,97,3"
        md = parse_metric_line(line)

        self.assertEqual(md.resource_name, "mysql-predictive")
        self.assertEqual(md.metric_name, "MemoryUsagePercent")
        self.assertEqual(md.group_id, "MemoryUsage")
        self.assertEqual(md.fix_value, "97")
        self.assertEqual(md.variation, "3")

    def test_parse_metric_line_with_iterations(self):
        from demouiapp.injectors.metric_injector import parse_metric_line

        line = "mysql-predictive,PodRestarts,PodRestarts,ITERATIONS,1"
        md = parse_metric_line(line)

        self.assertEqual(md.fix_value, "ITERATIONS")
        self.assertEqual(md.variation, "1")


class TestEventConfig(unittest.TestCase):
    """Test event configuration dataclass."""

    def test_event_config_defaults(self):
        from demouiapp.injectors.event_injector import EventConfig

        config = EventConfig(name="test", events_data="some_data")
        self.assertEqual(config.name, "test")
        self.assertEqual(config.events_data, "some_data")
        self.assertEqual(config.time_skew, 10)  # DEFAULT_EVENTS_TIME_SKEW


class TestLogConfig(unittest.TestCase):
    """Test log configuration dataclass."""

    def test_log_config_defaults(self):
        from demouiapp.injectors.log_injector import LogConfig

        config = LogConfig(name="test", logs_data="some_logs")
        self.assertEqual(config.name, "test")
        self.assertEqual(config.mode, "generic")
        self.assertEqual(config.iterations, 5)


class TestScenarios(unittest.TestCase):
    """Test scenario classes."""

    def test_robotshop_scenario_init(self):
        from demouiapp.scenarios.robotshop import RobotShopScenario

        scenario = RobotShopScenario(
            events_data="event1\nevent2",
            metrics_data="metric1;metric2",
            logs_data="log1\nlog2",
        )
        self.assertEqual(scenario.events_data, "event1\nevent2")
        self.assertEqual(scenario.metrics_data, "metric1;metric2")
        self.assertEqual(scenario.logs_data, "log1\nlog2")
        self.assertEqual(scenario.property_resource_name, "mysql")

    def test_sockshop_scenario_init(self):
        from demouiapp.scenarios.sockshop import SockShopScenario

        scenario = SockShopScenario(
            events_data="sock_event",
            metrics_data="sock_metric",
            logs_data="sock_log",
        )
        self.assertEqual(scenario.events_data, "sock_event")

    def test_acme_scenario_init(self):
        from demouiapp.scenarios.acme import AcmeScenario

        scenario = AcmeScenario(
            events_data="acme_event",
            metrics_fan_temp="fan_temp_metric",
            metrics_fan="fan_metric",
        )
        self.assertEqual(scenario.events_data, "acme_event")
        self.assertEqual(scenario.metrics_fan_temp, "fan_temp_metric")
        self.assertEqual(scenario.metrics_fan, "fan_metric")

    def test_telco_scenario_init(self):
        from demouiapp.scenarios.telco import TelcoScenario

        scenario = TelcoScenario(
            events_data="telco_event",
            metrics_fiber="fiber_metric",
            metrics_fiber_ny="fiber_ny_metric",
        )
        self.assertEqual(scenario.events_data, "telco_event")
        self.assertEqual(scenario.metrics_fiber, "fiber_metric")
        self.assertEqual(scenario.metrics_fiber_ny, "fiber_ny_metric")

    def test_custom_scenario_has_data(self):
        from demouiapp.scenarios.custom import CustomScenario

        # With data
        scenario = CustomScenario(
            name="Test",
            events_data="some_event",
            metrics_data="",
            logs_data="",
        )
        self.assertTrue(scenario.has_data)

        # Without data
        scenario_empty = CustomScenario(
            name="Empty",
            events_data="",
            metrics_data="",
            logs_data="",
        )
        self.assertFalse(scenario_empty.has_data)

        # With metrics only
        scenario_metrics = CustomScenario(
            name="MetricsOnly",
            events_data="",
            metrics_data="metric1;metric2",
            logs_data="",
        )
        self.assertTrue(scenario_metrics.has_data)

    def test_custom_scenario_name_default(self):
        from demouiapp.scenarios.custom import CustomScenario

        scenario = CustomScenario()
        self.assertEqual(scenario.name, "Custom Scenario")

    def test_risk_scenario_exists(self):
        from demouiapp.scenarios.risk import RiskScenario

        scenario = RiskScenario()
        self.assertIsNotNone(scenario)

    def test_base_scenario(self):
        from demouiapp.scenarios.base import Scenario

        # Scenario is abstract, but we can check its properties
        # by creating a concrete subclass
        class TestScenario(Scenario):
            pass

        ts = TestScenario(name="test", events_data="e", metrics_data="m", logs_data="l")
        self.assertTrue(ts.has_events)
        self.assertTrue(ts.has_metrics)
        self.assertTrue(ts.has_logs)

        ts_empty = TestScenario(name="empty")
        self.assertFalse(ts_empty.has_events)
        self.assertFalse(ts_empty.has_metrics)
        self.assertFalse(ts_empty.has_logs)


class TestRepository(unittest.TestCase):
    """Test that repository.py re-exports all expected symbols."""

    def test_repository_exports_constants(self):
        from demouiapp.repository import (
            DATALAYER_API_PATH,
            KAFKA_SECURITY_PROTOCOL,
            METRICS_API_PATH,
            SUBSCRIPTION_ID,
        )

        self.assertIsNotNone(SUBSCRIPTION_ID)
        self.assertIsNotNone(DATALAYER_API_PATH)

    def test_repository_exports_injectors(self):
        from demouiapp.repository import (
            EventConfig,
            LogConfig,
            MetricDefinition,
            inject_events,
            inject_events_repeated,
            inject_logs_continuous,
            inject_logs_generic,
            inject_metrics,
            parse_metric_line,
        )

        # All should be callable or classes
        self.assertTrue(callable(inject_events))
        self.assertTrue(callable(inject_events_repeated))
        self.assertTrue(callable(inject_logs_continuous))
        self.assertTrue(callable(inject_logs_generic))
        self.assertTrue(callable(inject_metrics))
        self.assertTrue(callable(parse_metric_line))

    def test_repository_exports_scenarios(self):
        from demouiapp.repository import (
            AcmeScenario,
            CustomScenario,
            RiskScenario,
            RobotShopScenario,
            Scenario,
            SockShopScenario,
            TelcoScenario,
        )

        # All should be classes
        self.assertTrue(isinstance(RobotShopScenario, type))
        self.assertTrue(isinstance(SockShopScenario, type))
        self.assertTrue(isinstance(AcmeScenario, type))
        self.assertTrue(isinstance(TelcoScenario, type))
        self.assertTrue(isinstance(CustomScenario, type))
        self.assertTrue(isinstance(RiskScenario, type))

    def test_repository_exports_legacy_functions(self):
        """Test backward compatibility - legacy function names should still be importable."""
        from demouiapp.repository import (
            checkTopology,
            closeAlerts,
            closeStories,
            injectEventsBusy,
            injectEventsCUSTOM,
            injectEventsFanACME,
            injectEventsGeneric,
            injectEventsMemRobot,
            injectEventsNetRobot,
            injectEventsNetSock,
            injectEventsRisk,
            injectEventsTelco,
            injectEventsTube,
            injectLogsContinuous,
            injectLogsCUSTOM,
            injectLogsGeneric,
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
            injectMetricsMem,
            injectMetricsSockNet,
            loadTopology,
            mitigateIssues,
            modifyMYSQL,
            modifyProperty,
            resetMYSQL,
        )

        # All should be callable
        self.assertTrue(callable(injectEventsMemRobot))
        self.assertTrue(callable(injectEventsGeneric))
        self.assertTrue(callable(injectLogsRobotShop))
        self.assertTrue(callable(injectLogsGeneric))
        self.assertTrue(callable(injectMetricsMem))
        self.assertTrue(callable(injectMetrics))
        self.assertTrue(callable(mitigateIssues))
        self.assertTrue(callable(closeAlerts))
        self.assertTrue(callable(closeStories))


class TestReconciliation(unittest.TestCase):
    """
    Test that functions.py contains all unique features from both
    functions.py and functions_NG.py (now functions_legacy.py).
    """

    def test_injectEventsRisk_exists(self):
        """injectEventsRisk was unique to functions.py."""
        from demouiapp.functions import injectEventsRisk

        self.assertTrue(callable(injectEventsRisk))

    def test_injectMetricsFiber_exists(self):
        """injectMetricsFiber was unique to functions.py."""
        from demouiapp.functions import injectMetricsFiber

        self.assertTrue(callable(injectMetricsFiber))

    def test_injectMetricsFiberTransatlantic_exists(self):
        """injectMetricsFiberTransatlantic was unique to functions.py."""
        from demouiapp.functions import injectMetricsFiberTransatlantic

        self.assertTrue(callable(injectMetricsFiberTransatlantic))

    def test_all_common_functions_exist(self):
        """All functions present in both files should exist in reconciled version."""
        from demouiapp import functions

        expected_functions = [
            "mitigateIssues",
            "closeAlerts",
            "closeStories",
            "injectLogsRobotShop",
            "injectLogsSockShop",
            "injectLogsCUSTOM",
            "injectLogsContinuous",
            "injectLogsGeneric",
            "injectEventsMemRobot",
            "injectEventsNetRobot",
            "injectEventsFanACME",
            "injectEventsNetSock",
            "injectEventsTube",
            "injectEventsTelco",
            "injectEventsBusy",
            "injectEventsCUSTOM",
            "injectEventsGeneric",
            "injectMetricsMem",
            "injectMetricsFanTemp",
            "injectMetricsFan",
            "injectMetricsFanTempACME",
            "injectMetricsFanACME",
            "injectMetricsSockNet",
            "injectMetricsCUSTOM",
            "injectMetrics",
            "checkTopology",
            "modifyProperty",
            "modifyMYSQL",
            "resetMYSQL",
            "loadTopology",
        ]
        for func_name in expected_functions:
            self.assertTrue(
                hasattr(functions, func_name),
                f"Missing function: {func_name}",
            )
            self.assertTrue(
                callable(getattr(functions, func_name)),
                f"Not callable: {func_name}",
            )

    def test_functions_legacy_exists(self):
        """functions_NG.py should be renamed to functions_legacy.py."""
        from demouiapp import functions_legacy

        self.assertIsNotNone(functions_legacy)


class TestTypeHints(unittest.TestCase):
    """Test that key functions have proper type hints."""

    def test_inject_events_has_type_hints(self):
        from demouiapp.injectors.event_injector import inject_events

        hints = inject_events.__annotations__
        self.assertIn("datalayer_route", hints)
        self.assertIn("return", hints)

    def test_inject_logs_generic_has_type_hints(self):
        from demouiapp.injectors.log_injector import inject_logs_generic

        hints = inject_logs_generic.__annotations__
        self.assertIn("kafka_broker", hints)
        self.assertIn("return", hints)

    def test_inject_metrics_has_type_hints(self):
        from demouiapp.injectors.metric_injector import inject_metrics

        hints = inject_metrics.__annotations__
        self.assertIn("metric_route", hints)
        self.assertIn("metrics_to_simulate", hints)
        self.assertIn("return", hints)

    def test_parse_metric_line_has_type_hints(self):
        from demouiapp.injectors.metric_injector import parse_metric_line

        hints = parse_metric_line.__annotations__
        self.assertIn("line", hints)
        self.assertIn("return", hints)

    def test_scenario_classes_have_type_hints(self):
        from demouiapp.scenarios.robotshop import RobotShopScenario

        hints = RobotShopScenario.__init__.__annotations__
        self.assertIn("events_data", hints)
        self.assertIn("return", hints)


class TestDocstrings(unittest.TestCase):
    """Test that key functions have docstrings."""

    def test_inject_events_has_docstring(self):
        from demouiapp.injectors.event_injector import inject_events

        self.assertIsNotNone(inject_events.__doc__)
        self.assertIn("Inject events", inject_events.__doc__)

    def test_inject_logs_generic_has_docstring(self):
        from demouiapp.injectors.log_injector import inject_logs_generic

        self.assertIsNotNone(inject_logs_generic.__doc__)
        self.assertIn("Inject logs", inject_logs_generic.__doc__)

    def test_inject_metrics_has_docstring(self):
        from demouiapp.injectors.metric_injector import inject_metrics

        self.assertIsNotNone(inject_metrics.__doc__)
        self.assertIn("Inject simulated metrics", inject_metrics.__doc__)

    def test_scenario_classes_have_docstrings(self):
        from demouiapp.scenarios.acme import AcmeScenario
        from demouiapp.scenarios.custom import CustomScenario
        from demouiapp.scenarios.robotshop import RobotShopScenario
        from demouiapp.scenarios.sockshop import SockShopScenario
        from demouiapp.scenarios.telco import TelcoScenario

        self.assertIsNotNone(RobotShopScenario.__doc__)
        self.assertIsNotNone(SockShopScenario.__doc__)
        self.assertIsNotNone(AcmeScenario.__doc__)
        self.assertIsNotNone(TelcoScenario.__doc__)
        self.assertIsNotNone(CustomScenario.__doc__)


class TestFunctionsModuleDocstrings(unittest.TestCase):
    """Test that reconciled functions.py has docstrings."""

    def test_functions_module_has_docstring(self):
        from demouiapp import functions

        self.assertIsNotNone(functions.__doc__)

    def test_mitigate_issues_has_docstring(self):
        from demouiapp.functions import mitigateIssues

        self.assertIsNotNone(mitigateIssues.__doc__)

    def test_close_alerts_has_docstring(self):
        from demouiapp.functions import closeAlerts

        self.assertIsNotNone(closeAlerts.__doc__)

    def test_inject_events_generic_has_docstring(self):
        from demouiapp.functions import injectEventsGeneric

        self.assertIsNotNone(injectEventsGeneric.__doc__)

    def test_inject_metrics_has_docstring(self):
        from demouiapp.functions import injectMetrics

        self.assertIsNotNone(injectMetrics.__doc__)


if __name__ == "__main__":
    unittest.main()
