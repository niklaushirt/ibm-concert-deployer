"""
Base scenario class for IBM AIOps DemoUI.

Defines the interface that all demo scenarios must implement.
"""

from abc import ABC, abstractmethod
from typing import Optional

from ..utils import get_logger

logger = get_logger("scenarios.base")


class Scenario(ABC):
    """
    Abstract base class for demo scenarios.

    Each scenario represents a specific demo use case (e.g., RobotShop, SockShop).
    Subclasses implement the inject(), clear(), and mitigate() methods to control
    the demo flow.
    """

    def __init__(
        self,
        name: str,
        events_data: str = "",
        metrics_data: str = "",
        logs_data: str = "",
    ) -> None:
        """
        Initialize a scenario.

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

    def inject(self) -> str:
        """
        Execute the full scenario injection (events, metrics, logs).

        Subclasses may override to add custom logic or to inject
        data in a specific order.

        Returns:
            'OK' on success.
        """
        logger.info("Injecting scenario: %s", self.name)
        result = "OK"
        return result

    def clear(self) -> str:
        """
        Clear scenario data (alerts, stories, incidents).

        Returns:
            'OK' on success.
        """
        logger.info("Clearing scenario: %s", self.name)
        return "OK"

    def mitigate(self) -> str:
        """
        Mitigate scenario issues (reset to healthy state).

        Returns:
            'OK' on success.
        """
        logger.info("Mitigating scenario: %s", self.name)
        return "OK"

    @property
    def has_events(self) -> bool:
        """Check if this scenario has event data configured."""
        return bool(self.events_data and self.events_data.strip())

    @property
    def has_metrics(self) -> bool:
        """Check if this scenario has metric data configured."""
        return bool(self.metrics_data and self.metrics_data.strip())

    @property
    def has_logs(self) -> bool:
        """Check if this scenario has log data configured."""
        return bool(self.logs_data and self.logs_data.strip())
