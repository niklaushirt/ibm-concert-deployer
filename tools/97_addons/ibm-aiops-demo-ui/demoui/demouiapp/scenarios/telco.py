"""
Telco demo scenario for IBM AIOps DemoUI.

Simulates fiber cut and network issues in a telecom topology.
"""

from ..injectors.event_injector import inject_events
from ..injectors.metric_injector import inject_metrics
from ..utils import get_logger

logger = get_logger("scenarios.telco")


class TelcoScenario:
    """
    Telco demo scenario controller.

    Manages injection of fiber/network events and metrics
    for the telecommunications demo.
    """

    def __init__(
        self,
        events_data: str = "",
        metrics_fiber: str = "",
        metrics_fiber_ny: str = "",
    ) -> None:
        """
        Initialize the Telco scenario.

        Args:
            events_data: Newline-separated event JSON templates.
            metrics_fiber: Semicolon-separated fiber metric definitions.
            metrics_fiber_ny: Semicolon-separated NY fiber metric definitions.
        """
        self.events_data = events_data
        self.metrics_fiber = metrics_fiber
        self.metrics_fiber_ny = metrics_fiber_ny

    def inject_events(
        self,
        datalayer_route: str,
        datalayer_user: str,
        datalayer_pwd: str,
    ) -> str:
        """
        Inject Telco fiber events into the datalayer.

        Args:
            datalayer_route: Route to the IBM AIOps datalayer API.
            datalayer_user: Username for datalayer authentication.
            datalayer_pwd: Password for datalayer authentication.

        Returns:
            'OK' on success.
        """
        logger.info("Injecting Telco events")
        return inject_events(
            datalayer_route=datalayer_route,
            datalayer_user=datalayer_user,
            datalayer_pwd=datalayer_pwd,
            events_data=self.events_data,
            scenario_name="TELCO",
        )

    def inject_fiber_metrics(
        self,
        metric_route: str,
        metric_token: str,
        time_skew: int,
        time_step: int,
    ) -> str:
        """
        Inject Telco fiber metrics.

        Args:
            metric_route: Route to the IBM AIOps metrics API.
            metric_token: Bearer token for metrics authentication.
            time_skew: Initial seconds to add to the base timestamp.
            time_step: Milliseconds to advance between metric points.

        Returns:
            'OK' on success.
        """
        logger.info("Injecting Telco fiber metrics")
        metrics_list = [m for m in self.metrics_fiber.split(";") if m.strip()]
        return inject_metrics(
            metric_route=metric_route,
            metric_token=metric_token,
            metrics_to_simulate=metrics_list,
            time_skew=time_skew,
            time_step=time_step,
            scenario_name="Fiber Telco",
        )

    def inject_fiber_ny_metrics(
        self,
        metric_route: str,
        metric_token: str,
        time_skew: int,
        time_step: int,
    ) -> str:
        """
        Inject Telco NY fiber metrics (Transatlantic scenario).

        Args:
            metric_route: Route to the IBM AIOps metrics API.
            metric_token: Bearer token for metrics authentication.
            time_skew: Initial seconds to add to the base timestamp.
            time_step: Milliseconds to advance between metric points.

        Returns:
            'OK' on success.
        """
        logger.info("Injecting Telco NY fiber metrics")
        metrics_list = [m for m in self.metrics_fiber_ny.split(";") if m.strip()]
        return inject_metrics(
            metric_route=metric_route,
            metric_token=metric_token,
            metrics_to_simulate=metrics_list,
            time_skew=time_skew,
            time_step=time_step,
            scenario_name="Fiber-Transatlantic Telco",
        )
