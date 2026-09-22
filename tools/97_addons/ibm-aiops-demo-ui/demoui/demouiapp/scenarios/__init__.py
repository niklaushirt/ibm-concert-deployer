"""
Demo scenario modules for IBM AIOps DemoUI.

Each scenario encapsulates a specific demo use case (RobotShop, SockShop, etc.)
and provides methods to inject events, metrics, and logs.
"""

from .acme import AcmeScenario
from .base import Scenario
from .custom import CustomScenario
from .risk import RiskScenario
from .robotshop import RobotShopScenario
from .sockshop import SockShopScenario
from .telco import TelcoScenario

__all__ = [
    "Scenario",
    "RobotShopScenario",
    "SockShopScenario",
    "AcmeScenario",
    "TelcoScenario",
    "CustomScenario",
    "RiskScenario",
]
