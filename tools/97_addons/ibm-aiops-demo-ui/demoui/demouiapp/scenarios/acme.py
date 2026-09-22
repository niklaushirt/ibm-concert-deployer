"""
ACME demo scenario for IBM AIOps DemoUI.

Simulates fan temperature and speed issues in ACME manufacturing equipment.
"""

from ..injectors.event_injector import inject_events
from ..injectors.metric_injector import inject_metrics
from ..utils import get_logger

logger = get_logger("scenarios.acme")


class AcmeScenario:
    """
    ACME demo scenario controller.

    Manages injection of fan temperature/speed events and metrics
    for the ACME manufacturing demo.
    """

    def __init__(
        self,
        events_data: str = "",
        metrics_fan_temp: str = "",
        metrics_fan: str = "",
    ) -> None:
        """
        Initialize the ACME scenario.

        Args:
            events_data: Newline-separated event JSON templates.
            metrics_fan_temp: Semicolon-separated fan temp metric definitions.
            metrics_fan: Semicolon-separated fan speed metric definitions.
        """
        self.events_data = events_data
        self.metrics_fan_temp = metrics_fan_temp
        self.metrics_fan = metrics_fan

    def inject_events(
        self,
        datalayer_route: str,
        datalayer_user: str,
        datalayer_pwd: str,
    ) -> str:
        """
        Inject ACME fan events into the datalayer.

        Args:
            datalayer_route: Route to the IBM AIOps datalayer API.
            datalayer_user: Username for datalayer authentication.
            datalayer_pwd: Password for datalayer authentication.

        Returns:
            'OK' on success.
        """
        logger.info("Injecting ACME events")
        return inject_events(
            datalayer_route=datalayer_route,
            datalayer_user=datalayer_user,
            datalayer_pwd=datalayer_pwd,
            events_data=self.events_data,
            scenario_name="FAN ACME",
        )

    def inject_fan_temp_metrics(
        self,
        metric_route: str,
        metric_token: str,
    ) -> str:
        """
        Inject ACME fan temperature metrics.

        Args:
            metric_route: Route to the IBM AIOps metrics API.
            metric_token: Bearer token for metrics authentication.

        Returns:
            'OK' on success.
        """
        logger.info("Injecting ACME fan temp metrics")
        metrics_list = [m for m in self.metrics_fan_temp.split(";") if m.strip()]
        return inject_metrics(
            metric_route=metric_route,
            metric_token=metric_token,
            metrics_to_simulate=metrics_list,
            time_skew=0,
            time_step=120,
            scenario_name="FAN-TEMP ACME",
        )

    def inject_fan_metrics(
        self,
        metric_route: str,
        metric_token: str,
        time_skew: int,
        time_step: int,
    ) -> str:
        """
        Inject ACME fan speed metrics.

        Args:
            metric_route: Route to the IBM AIOps metrics API.
            metric_token: Bearer token for metrics authentication.
            time_skew: Initial seconds to add to the base timestamp.
            time_step: Milliseconds to advance between metric points.

        Returns:
            'OK' on success.
        """
        logger.info("Injecting ACME fan metrics")
        metrics_list = [m for m in self.metrics_fan.split(";") if m.strip()]
        return inject_metrics(
            metric_route=metric_route,
            metric_token=metric_token,
            metrics_to_simulate=metrics_list,
            time_skew=time_skew,
            time_step=time_step,
            scenario_name="FAN ACME",
        )
