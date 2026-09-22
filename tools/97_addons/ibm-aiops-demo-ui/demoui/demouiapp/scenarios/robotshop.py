"""
RobotShop demo scenario for IBM AIOps DemoUI.

Simulates memory pressure and network issues in the RobotShop application.
"""

import os
from typing import Optional

from ..injectors.event_injector import inject_events
from ..injectors.log_injector import inject_logs_continuous
from ..injectors.metric_injector import inject_metrics
from ..utils import get_logger
from ..utils.commands import run_shell

logger = get_logger("scenarios.robotshop")


class RobotShopScenario:
    """
    RobotShop demo scenario controller.

    Manages injection of events, metrics, and logs for the RobotShop demo.
    Also handles creation and mitigation of RobotShop outages.
    """

    def __init__(
        self,
        events_data: str = "",
        metrics_data: str = "",
        logs_data: str = "",
        property_resource_name: str = "mysql",
        property_resource_type: str = "deployment",
        property_values_nok: str = "",
        property_values_ok: str = "",
    ) -> None:
        """
        Initialize the RobotShop scenario.

        Args:
            events_data: Newline-separated event JSON templates.
            metrics_data: Semicolon-separated CSV metric definitions.
            logs_data: Newline-separated log templates.
            property_resource_name: Topology resource name to modify.
            property_resource_type: Topology resource type.
            property_values_nok: JSON values to set when injecting issues.
            property_values_ok: JSON values to set when mitigating.
        """
        self.events_data = events_data
        self.metrics_data = metrics_data
        self.logs_data = logs_data
        self.property_resource_name = property_resource_name
        self.property_resource_type = property_resource_type
        self.property_values_nok = property_values_nok
        self.property_values_ok = property_values_ok

    def inject_events(
        self,
        datalayer_route: str,
        datalayer_user: str,
        datalayer_pwd: str,
    ) -> str:
        """
        Inject RobotShop memory events into the datalayer.

        Args:
            datalayer_route: Route to the IBM AIOps datalayer API.
            datalayer_user: Username for datalayer authentication.
            datalayer_pwd: Password for datalayer authentication.

        Returns:
            'OK' on success.
        """
        logger.info("Injecting RobotShop events")
        return inject_events(
            datalayer_route=datalayer_route,
            datalayer_user=datalayer_user,
            datalayer_pwd=datalayer_pwd,
            events_data=self.events_data,
            scenario_name="MEM RobotShop",
        )

    def inject_logs(
        self,
        kafka_broker: str,
        kafka_user: str,
        kafka_pwd: str,
        kafka_topic: str,
        kafka_cert: str,
        time_format: str,
    ) -> str:
        """
        Inject RobotShop logs into Kafka.

        Args:
            kafka_broker: Kafka broker address.
            kafka_user: Kafka SASL username.
            kafka_pwd: Kafka SASL password.
            kafka_topic: Target Kafka topic.
            kafka_cert: CA certificate content.
            time_format: Python strftime format for timestamps.

        Returns:
            'OK' on success.
        """
        logger.info("Injecting RobotShop logs")
        return inject_logs_continuous(
            kafka_broker=kafka_broker,
            kafka_user=kafka_user,
            kafka_pwd=kafka_pwd,
            kafka_topic=kafka_topic,
            kafka_cert=kafka_cert,
            time_format=time_format,
            logs_data=self.logs_data,
            scenario_name="RobotShop",
        )

    def inject_metrics(
        self,
        metric_route: str,
        metric_token: str,
        time_skew: int,
        time_step: int,
    ) -> str:
        """
        Inject RobotShop metrics into the metrics API.

        Args:
            metric_route: Route to the IBM AIOps metrics API.
            metric_token: Bearer token for metrics authentication.
            time_skew: Initial seconds to add to the base timestamp.
            time_step: Milliseconds to advance between metric points.

        Returns:
            'OK' on success.
        """
        logger.info("Injecting RobotShop metrics")
        metrics_list = [m for m in self.metrics_data.split(";") if m.strip()]
        return inject_metrics(
            metric_route=metric_route,
            metric_token=metric_token,
            metrics_to_simulate=metrics_list,
            time_skew=time_skew,
            time_step=time_step,
            scenario_name="RobotShop",
        )

    def create_outage(self) -> None:
        """
        Create RobotShop MySQL outage by pointing ratings to dev DB.

        This simulates a production issue by redirecting the ratings
        service to a non-existent development database.
        """
        logger.info("Creating RobotShop MySQL outage")
        run_shell(
            "oc set env deployment ratings -n robot-shop "
            'PDO_URL="mysql:host=mysql;dbname=ratings-dev;charset=utf8mb4"'
        )
        run_shell("oc set env deployment load -n robot-shop ERROR=1")

    def mitigate_outage(self) -> None:
        """
        Mitigate RobotShop MySQL outage by restoring correct config.

        Resets the ratings service to use the correct production database.
        """
        logger.info("Mitigating RobotShop outage")
        run_shell(
            "oc patch service mysql -n robot-shop "
            '--patch "{\\"spec\\": {\\"selector\\": {\\"service\\": \\"mysql\\"}}}"'
        )
        run_shell("oc set env deployment ratings -n robot-shop PDO_URL-")
        run_shell("oc set env deployment load -n robot-shop ERROR=0")
        run_shell(
            "oc delete pod $(oc get po -n robot-shop|grep shipping|awk '{print$1}') "
            "-n robot-shop --ignore-not-found"
        )
