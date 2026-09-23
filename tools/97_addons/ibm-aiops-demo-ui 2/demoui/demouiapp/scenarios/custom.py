"""
Custom demo scenario for IBM AIOps DemoUI.

Loads user-defined events, metrics, and logs from environment variables.
"""

from ..injectors.event_injector import inject_events
from ..injectors.log_injector import inject_logs_generic
from ..injectors.metric_injector import inject_metrics
from ..utils import get_logger

logger = get_logger("scenarios.custom")


class CustomScenario:
    """
    Custom demo scenario controller.

    Loads scenario data from environment variables (CUSTOM_EVENTS,
    CUSTOM_METRICS, CUSTOM_LOGS, CUSTOM_NAME) to allow arbitrary
    demo scenarios without code changes.
    """

    def __init__(
        self,
        name: str = "Custom Scenario",
        events_data: str = "",
        metrics_data: str = "",
        logs_data: str = "",
    ) -> None:
        """
        Initialize the custom scenario.

        Args:
            name: Human-readable scenario name.
            events_data: Newline-separated event JSON templates.
            metrics_data: Semicolon-separated CSV metric definitions.
            logs_data: Newline-separated log templates.
        """
        self.name = name
        self.events_data = events_data
        self.metrics_data = metrics_data
        self.logs_data = logs_data

    @property
    def has_data(self) -> bool:
        """Check if this scenario has any data configured."""
        return (
            bool(self.events_data.strip())
            or bool(self.metrics_data.strip())
            or bool(self.logs_data.strip())
        )

    def inject_events(
        self,
        datalayer_route: str,
        datalayer_user: str,
        datalayer_pwd: str,
    ) -> str:
        """
        Inject custom events into the datalayer.

        Args:
            datalayer_route: Route to the IBM AIOps datalayer API.
            datalayer_user: Username for datalayer authentication.
            datalayer_pwd: Password for datalayer authentication.

        Returns:
            'OK' on success.
        """
        if not self.events_data.strip():
            logger.info("No custom events configured")
            return "OK"

        logger.info("Injecting custom events: %s", self.name)
        return inject_events(
            datalayer_route=datalayer_route,
            datalayer_user=datalayer_user,
            datalayer_pwd=datalayer_pwd,
            events_data=self.events_data,
            scenario_name=self.name,
        )

    def inject_logs(
        self,
        kafka_broker: str,
        kafka_user: str,
        kafka_pwd: str,
        kafka_topic: str,
        kafka_cert: str,
    ) -> str:
        """
        Inject custom logs into Kafka.

        Args:
            kafka_broker: Kafka broker address.
            kafka_user: Kafka SASL username.
            kafka_pwd: Kafka SASL password.
            kafka_topic: Target Kafka topic.
            kafka_cert: CA certificate content.

        Returns:
            'OK' on success.
        """
        if not self.logs_data.strip():
            logger.info("No custom logs configured")
            return "OK"

        logger.info("Injecting custom logs: %s", self.name)
        time_format = "%Y-%m-%d %H:%M:%S.000"
        return inject_logs_generic(
            kafka_broker=kafka_broker,
            kafka_user=kafka_user,
            kafka_pwd=kafka_pwd,
            kafka_topic=kafka_topic,
            kafka_cert=kafka_cert,
            time_format=time_format,
            logs_data=self.logs_data,
            scenario_name=self.name,
        )

    def inject_metrics(
        self,
        metric_route: str,
        metric_token: str,
    ) -> str:
        """
        Inject custom metrics into the metrics API.

        Args:
            metric_route: Route to the IBM AIOps metrics API.
            metric_token: Bearer token for metrics authentication.

        Returns:
            'OK' on success.
        """
        if not self.metrics_data.strip():
            logger.info("No custom metrics configured")
            return "OK"

        logger.info("Injecting custom metrics: %s", self.name)
        metrics_list = [m for m in self.metrics_data.split(";") if m.strip()]
        return inject_metrics(
            metric_route=metric_route,
            metric_token=metric_token,
            metrics_to_simulate=metrics_list,
            time_skew=0,
            time_step=0,
            scenario_name=self.name,
        )
