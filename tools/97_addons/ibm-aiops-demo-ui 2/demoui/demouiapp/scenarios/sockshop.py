"""
SockShop demo scenario for IBM AIOps DemoUI.

Simulates network issues in the SockShop catalog service.
"""

from ..injectors.event_injector import inject_events
from ..injectors.log_injector import inject_logs_generic
from ..injectors.metric_injector import inject_metrics
from ..utils import get_logger

logger = get_logger("scenarios.sockshop")


class SockShopScenario:
    """
    SockShop demo scenario controller.

    Manages injection of events, metrics, and logs for the SockShop demo.
    Also handles creation and mitigation of SockShop catalog outages.
    """

    def __init__(
        self,
        events_data: str = "",
        metrics_data: str = "",
        logs_data: str = "",
    ) -> None:
        """
        Initialize the SockShop scenario.

        Args:
            events_data: Newline-separated event JSON templates.
            metrics_data: Semicolon-separated CSV metric definitions.
            logs_data: Newline-separated log templates.
        """
        self.events_data = events_data
        self.metrics_data = metrics_data
        self.logs_data = logs_data

    def inject_events(
        self,
        datalayer_route: str,
        datalayer_user: str,
        datalayer_pwd: str,
    ) -> str:
        """
        Inject SockShop network events into the datalayer.

        Args:
            datalayer_route: Route to the IBM AIOps datalayer API.
            datalayer_user: Username for datalayer authentication.
            datalayer_pwd: Password for datalayer authentication.

        Returns:
            'OK' on success.
        """
        logger.info("Injecting SockShop events")
        return inject_events(
            datalayer_route=datalayer_route,
            datalayer_user=datalayer_user,
            datalayer_pwd=datalayer_pwd,
            events_data=self.events_data,
            scenario_name="NET SockShop",
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
        Inject SockShop logs into Kafka.

        Args:
            kafka_broker: Kafka broker address.
            kafka_user: Kafka SASL username.
            kafka_pwd: Kafka SASL password.
            kafka_topic: Target Kafka topic.
            kafka_cert: CA certificate content.

        Returns:
            'OK' on success.
        """
        logger.info("Injecting SockShop logs")
        time_format = "%Y-%m-%d %H:%M:%S.000"
        return inject_logs_generic(
            kafka_broker=kafka_broker,
            kafka_user=kafka_user,
            kafka_pwd=kafka_pwd,
            kafka_topic=kafka_topic,
            kafka_cert=kafka_cert,
            time_format=time_format,
            logs_data=self.logs_data,
            scenario_name="SockShop",
        )

    def inject_metrics(
        self,
        metric_route: str,
        metric_token: str,
        time_skew: int,
        time_step: int,
    ) -> str:
        """
        Inject SockShop network metrics into the metrics API.

        Args:
            metric_route: Route to the IBM AIOps metrics API.
            metric_token: Bearer token for metrics authentication.
            time_skew: Initial seconds to add to the base timestamp.
            time_step: Milliseconds to advance between metric points.

        Returns:
            'OK' on success.
        """
        logger.info("Injecting SockShop metrics")
        metrics_list = [m for m in self.metrics_data.split(";") if m.strip()]
        return inject_metrics(
            metric_route=metric_route,
            metric_token=metric_token,
            metrics_to_simulate=metrics_list,
            time_skew=time_skew,
            time_step=time_step,
            scenario_name="SockShop",
        )
