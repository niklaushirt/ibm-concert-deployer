"""
Core functions for IBM AIOps DemoUI.

This module provides the main entry points for injecting events, logs, and
metrics into the IBM AIOps platform. It has been refactored to use modular
injectors and scenarios while maintaining backward compatibility with views.py.

Refactoring Notes:
- Thin wrapper functions now delegate to injectors/ module
- Scenario-specific logic moved to scenarios/ module
- Constants centralized in utils/constants.py
- Type hints and docstrings added throughout
- functions_NG.py merged into this file (saved as functions_legacy.py)

Author: Niklaus Hirt (nikh@ch.ibm.com)
"""

import datetime
import json
import os
import random
import socket
import time
from pathlib import Path
from typing import List, Optional

import requests
import urllib3
from confluent_kafka import KafkaException, Producer
from requests.auth import HTTPBasicAuth

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# -----------------------------------------------------------------------------
# Module-level logging (transitional - will be replaced by logging module)
# -----------------------------------------------------------------------------
print("")
print(
    "*************************************************************************************************"
)
print("            ________  __  ___     ___    ________       ")
print("           /  _/ __ )/  |/  /    /   |  /  _/ __ \\____  _____")
print("           / // __  / /|_/ /    / /| |  / // / / / __ \/ ___/")
print("         _/ // /_/ / /  / /    / ___ |_/ // /_/ / /_/ (__  ) ")
print("        /___/_____/_/  /_/    /_/  |_/___/\\____/ .___/____/  ")
print("                                              /_/")
print(
    "*************************************************************************************************"
)
print("    🛰️  DemoUI for IBM Automation AIOps")
print("       Provided by:")
print("        🇨🇭 Niklaus Hirt (nikh@ch.ibm.com)")
print(
    "*************************************************************************************************"
)
print(
    "-------------------------------------------------------------------------------------------------"
)
print(" 🚀 Prefetching Configuration")
print(
    "-------------------------------------------------------------------------------------------------"
)

# -----------------------------------------------------------------------------
# Default Configuration Values
# -----------------------------------------------------------------------------
LOG_ITERATIONS: int = 5
TOKEN: str = "test"
LOG_TIME_FORMAT: str = "%Y-%m-%dT%H:%M:%S.000000"
LOG_TIME_STEPS: int = 1000
LOG_TIME_SKEW: int = 60
LOG_TIME_ZONE: int = -1


# RobotShop Configuration
DEMO_EVENTS_MEM: Optional[str] = os.environ.get("DEMO_EVENTS_MEM")
DEMO_EVENTS_ROBO_NET: Optional[str] = os.environ.get("DEMO_EVENTS_ROBO_NET")
DEMO_LOGS: Optional[str] = os.environ.get("DEMO_LOGS")
METRICS_TO_SIMULATE_MEM: List[str] = str(
    os.environ.get("METRICS_TO_SIMULATE_MEM")
).split(";")
METRICS_TO_SIMULATE_FIBER: List[str] = str(
    os.environ.get("METRICS_TO_SIMULATE_FIBER")
).split(";")
print(
    "🟣          #METRICS_TO_SIMULATE_FIBER:              "
    + str(len(METRICS_TO_SIMULATE_FIBER))
)

ROBOTSHOP_PROPERTY_RESOURCE_NAME: str = os.environ.get(
    "ROBOTSHOP_PROPERTY_RESOURCE_NAME", "mysql"
)
ROBOTSHOP_PROPERTY_RESOURCE_TYPE: str = os.environ.get(
    "ROBOTSHOP_PROPERTY_RESOURCE_TYPE", "deployment"
)
ROBOTSHOP_PROPERTY_VALUES_NOK: str = os.environ.get(
    "ROBOTSHOP_PROPERTY_VALUES_NOK",
    '{"innodb_buffer_pool_size": "8GB","last_change_by": "Niklaus Hirt"}',
)
ROBOTSHOP_PROPERTY_VALUES_OK: str = os.environ.get(
    "ROBOTSHOP_PROPERTY_VALUES_OK",
    '{"innodb_buffer_pool_size": "8GB","last_change_by": "Scott James"}',
)


# ACME Configuration
METRICS_TO_SIMULATE_FAN_TEMP_ACME: List[str] = str(
    os.environ.get("METRICS_TO_SIMULATE_FAN_TEMP_ACME")
).split(";")
METRICS_TO_SIMULATE_FAN_ACME: List[str] = str(
    os.environ.get("METRICS_TO_SIMULATE_FAN_ACME")
).split(";")
DEMO_EVENTS_FAN_ACME: Optional[str] = os.environ.get("DEMO_EVENTS_FAN_ACME")
METRICS_TO_SIMULATE_FAN_TEMP: List[str] = str(
    os.environ.get("METRICS_TO_SIMULATE_FAN_TEMP")
).split(";")
METRICS_TO_SIMULATE_FAN: List[str] = str(
    os.environ.get("METRICS_TO_SIMULATE_FAN")
).split(";")


# SockShop Configuration
DEMO_LOGS_SOCK: Optional[str] = os.environ.get("DEMO_LOGS_SOCK")
METRICS_TO_SIMULATE_NET_SOCK: List[str] = str(
    os.environ.get("METRICS_TO_SIMULATE_NET_SOCK")
).split(";")
DEMO_EVENTS_NET_SOCK: Optional[str] = os.environ.get("DEMO_EVENTS_NET_SOCK")

# Tube Configuration
DEMO_EVENTS_TUBE: str = os.environ.get("DEMO_EVENTS_TUBE", "")


# Telco Configuration
DEMO_EVENTS_TELCO: str = os.environ.get("DEMO_EVENTS_TELCO", "")
METRICS_TO_SIMULATE_FIBER_NY: List[str] = str(
    os.environ.get("METRICS_TO_SIMULATE_FIBER_NY")
).split(";")
print(
    "🟣          #METRICS_TO_SIMULATE_FIBER_NY:              "
    + str(len(METRICS_TO_SIMULATE_FIBER_NY))
)


# Busy Configuration
DEMO_EVENTS_BUSY: str = os.environ.get("DEMO_EVENTS_BUSY", "")


# Custom Configuration
CUSTOM_NAME: str = os.environ.get("CUSTOM_NAME", "Custom Scenario")
CUSTOM_EVENTS: str = os.environ.get("CUSTOM_EVENTS", "")
CUSTOM_METRICS: List[str] = str(os.environ.get("CUSTOM_METRICS")).split(";")
CUSTOM_LOGS: str = os.environ.get("CUSTOM_LOGS", "")
CUSTOM_TOPOLOGY: str = os.environ.get("CUSTOM_TOPOLOGY", "")
CUSTOM_TOPOLOGY_TAG: str = os.environ.get("CUSTOM_TOPOLOGY_TAG", "")
CUSTOM_TOPOLOGY_APP_NAME: str = os.environ.get("CUSTOM_TOPOLOGY_APP_NAME", "")
CUSTOM_TOPOLOGY_FORCE_RELOAD: str = os.environ.get(
    "CUSTOM_TOPOLOGY_FORCE_RELOAD", "False"
)

CUSTOM_PROPERTY_RESOURCE_NAME: str = os.environ.get("CUSTOM_PROPERTY_RESOURCE_NAME", "")
CUSTOM_PROPERTY_RESOURCE_TYPE: str = os.environ.get("CUSTOM_PROPERTY_RESOURCE_TYPE", "")
CUSTOM_PROPERTY_VALUES_NOK: str = os.environ.get("CUSTOM_PROPERTY_VALUES_NOK", "")
CUSTOM_PROPERTY_VALUES_OK: str = os.environ.get("CUSTOM_PROPERTY_VALUES_OK", "")


# Show Config
GET_CONFIG: str = str(os.environ.get("GET_CONFIG", "false"))


# Global Timing Configuration
METRIC_TIME_SKEW: int = int(os.environ.get("METRIC_TIME_SKEW", "240"))
METRIC_TIME_STEP: int = int(os.environ.get("METRIC_TIME_STEP", "100"))
METRIC_ITERATIONS: int = int(os.environ.get("METRIC_ITERATIONS", "80"))

LOG_ITERATIONS = int(os.environ.get("LOG_ITERATIONS", "5"))
LOG_TIME_FORMAT = os.environ.get("LOG_TIME_FORMAT", "%Y-%m-%dT%H:%M:%S.000000")
LOG_TIME_STEPS = int(os.environ.get("LOG_TIME_STEPS", "1000"))
LOG_TIME_SKEW = int(os.environ.get("LOG_TIME_SKEW", "60"))
LOG_TIME_ZONE = int(os.environ.get("LOG_TIME_ZONE", "-1"))

EVENTS_TIME_SKEW: int = int(os.environ.get("EVENTS_TIME_SKEW", "10"))

INSTANCE_NAME: Optional[str] = os.environ.get("INSTANCE_NAME")
if INSTANCE_NAME is None:
    INSTANCE_NAME = "IBMAIOPS"

image_name: str = INSTANCE_NAME.lower().replace(" ", "_") + ".png"
path = Path("./static/images/characters/" + image_name)

if path.is_file():
    INSTANCE_IMAGE: str = str(path)
else:
    INSTANCE_IMAGE: str = "None"


# External URLs
SLACK_URL_ROSH: str = str(os.environ.get("SLACK_URL_ROSH", "NONE"))
SLACK_URL_SOSH: str = str(os.environ.get("SLACK_URL_SOSH", "NONE"))
SLACK_URL_ACME: str = str(os.environ.get("SLACK_URL_ACME", "NONE"))

SNOW_URL_ROSH: str = str(os.environ.get("SNOW_URL_ROSH", "NONE"))
SNOW_URL_SOSH: str = str(os.environ.get("SNOW_URL_SOSH", "NONE"))
SNOW_URL_ACME: str = str(os.environ.get("SNOW_URL_ACME", "NONE"))

INCIDENT_URL_TUBE: str = str(os.environ.get("INCIDENT_URL_TUBE", "NONE"))


print(" ✅ Prefetching Configuration - DONE")
print(
    "-------------------------------------------------------------------------------------------------"
)
print("")
print("")

# Import reconciled modules
# Support both 'from functions import *' (views.py) and 'from .functions import ...' (repository.py)
try:
    from .utils.constants import (
        DATALAYER_API_PATH,
        DEFAULT_METRIC_BATCH_SIZE,
        KAFKA_SASL_MECHANISM,
        KAFKA_SECURITY_PROTOCOL,
        METRICS_API_PATH,
        SUBSCRIPTION_ID,
    )
    from .utils.commands import capture_shell, run_shell
    from .utils.logging_config import get_logger
except ImportError:
    from utils.constants import (
        DATALAYER_API_PATH,
        DEFAULT_METRIC_BATCH_SIZE,
        KAFKA_SASL_MECHANISM,
        KAFKA_SECURITY_PROTOCOL,
        METRICS_API_PATH,
        SUBSCRIPTION_ID,
    )
    from utils.commands import capture_shell, run_shell
    from utils.logging_config import get_logger

logger = get_logger("functions")

# -----------------------------------------------------------------------------
# Alert and Story Management
# -----------------------------------------------------------------------------


def mitigateIssues(
    datalayer_route: str,
    datalayer_user: str,
    datalayer_pwd: str,
) -> str:
    """
    Mitigate all active issues by resetting RobotShop and SockShop outages.

    Restores the MySQL service selector, removes the dev database redirect,
    and resets the load error flag.

    Args:
        datalayer_route: Route to the IBM AIOps datalayer API.
        datalayer_user: Username for datalayer authentication.
        datalayer_pwd: Password for datalayer authentication.

    Returns:
        'OK' on success.
    """
    print("📛 START - mitigateIssues")
    print("🌏 Reset RobotShop MySQL outage")
    run_shell(
        'oc patch service mysql -n robot-shop --patch "{\\"spec\\": {\\"selector\\": {\\"service\\": \\"mysql\\"}}}"'
    )
    run_shell("oc set env deployment ratings -n robot-shop PDO_URL-")
    run_shell("oc set env deployment load -n robot-shop ERROR=0")
    run_shell(
        "oc delete pod $(oc get po -n robot-shop|grep shipping|awk '{print$1}') -n robot-shop --ignore-not-found"
    )
    print("🌏 Mitigate Sockshop Catalog outage")
    run_shell(
        'oc patch service catalogue -n sock-shop --patch "{\\"spec\\": {\\"selector\\": {\\"name\\": \\"catalog\\"}}}"'
    )
    print("✅ END - mitigateIssues")
    return "OK"


def closeAlerts(
    datalayer_route: str,
    datalayer_user: str,
    datalayer_pwd: str,
) -> str:
    """
    Close all active alerts in the IBM AIOps datalayer.

    Sends a PATCH request to set all alerts to 'closed' state.

    Args:
        datalayer_route: Route to the IBM AIOps datalayer API.
        datalayer_user: Username for datalayer authentication.
        datalayer_pwd: Password for datalayer authentication.

    Returns:
        'OK' on success.

    Raises:
        SystemExit: If the datalayer API connection fails.
    """
    print("📛 START - Close Alerts")
    data = '{"state": "closed"}'
    url = "https://" + datalayer_route + DATALAYER_API_PATH + "/alerts"
    auth = HTTPBasicAuth(datalayer_user, datalayer_pwd)
    headers = {
        "Content-Type": "application/json",
        "Accept-Charset": "UTF-8",
        "x-username": "admin",
        "x-subscription-id": SUBSCRIPTION_ID,
    }
    try:
        response = requests.patch(
            url, data=data, headers=headers, auth=auth, verify=False
        )
    except requests.exceptions.RequestException as e:
        stream = capture_shell(
            "oc get route  -n "
            + aimanagerns
            + " datalayer-api  -o jsonpath='{.status.ingress[0].host}'"
        )
        print(
            "     ❗ YOU MIGHT WANT TO USE THE DATALAYER PUBLIC ROUTE: "
            + str(stream.read().strip())
        )
        raise SystemExit(e)

    print("    Close Alerts:" + str(response.content))
    print("✅ END - Close Alerts")
    return "OK"


def closeStories(
    datalayer_route: str,
    datalayer_user: str,
    datalayer_pwd: str,
) -> str:
    """
    Close all active stories in the IBM AIOps datalayer.

    First sets all stories to 'inProgress', then to 'resolved' state.

    Args:
        datalayer_route: Route to the IBM AIOps datalayer API.
        datalayer_user: Username for datalayer authentication.
        datalayer_pwd: Password for datalayer authentication.

    Returns:
        'OK' on success.

    Raises:
        SystemExit: If the datalayer API connection fails.
    """
    print("")
    data_in_progress = '{"state": "inProgress"}'
    data_resolved = '{"state": "resolved"}'
    url = "https://" + datalayer_route + DATALAYER_API_PATH + "/stories"
    auth = HTTPBasicAuth(datalayer_user, datalayer_pwd)
    headers = {
        "Content-Type": "application/json",
        "Accept-Charset": "UTF-8",
        "x-username": "admin",
        "x-subscription-id": SUBSCRIPTION_ID,
    }

    print("📛 START - Set Stories to InProgress")
    try:
        response = requests.patch(
            url, data=data_in_progress, headers=headers, auth=auth, verify=False
        )
    except requests.exceptions.RequestException as e:
        stream = capture_shell(
            "oc get route  -n "
            + aimanagerns
            + " datalayer-api  -o jsonpath='{.status.ingress[0].host}'"
        )
        print(
            "     ❗ YOU MIGHT WANT TO USE THE DATALAYER PUBLIC ROUTE: "
            + str(stream.read().strip())
        )
        raise SystemExit(e)

    time.sleep(10)

    print("📛 START - Set Stories to Resolved")
    try:
        response = requests.patch(
            url, data=data_resolved, headers=headers, auth=auth, verify=False
        )
    except requests.exceptions.RequestException as e:
        stream = capture_shell(
            "oc get route  -n "
            + aimanagerns
            + " datalayer-api  -o jsonpath='{.status.ingress[0].host}'"
        )
        print(
            "     ❗ YOU MIGHT WANT TO USE THE DATALAYER PUBLIC ROUTE: "
            + str(stream.read().strip())
        )
        raise SystemExit(e)

    print("    Close Stories-:" + str(response.content))
    print("✅ END - Close Stories")
    return "OK"


# -----------------------------------------------------------------------------
# Log Injection
# -----------------------------------------------------------------------------


def injectLogsRobotShop(
    kafka_broker: str,
    kafka_user: str,
    kafka_pwd: str,
    kafka_topic_logs: str,
    kafka_cert: str,
    log_time_format: str,
    demo_logs: str,
) -> str:
    """Inject continuous logs for RobotShop scenario.

    Args:
        kafka_broker: Kafka broker address.
        kafka_user: Kafka SASL username.
        kafka_pwd: Kafka SASL password.
        kafka_topic_logs: Target Kafka topic.
        kafka_cert: CA certificate content.
        log_time_format: Python strftime format for timestamps.
        demo_logs: Newline-separated log templates.

    Returns:
        'OK' on success.
    """
    print("📛 START - Inject Logs CONT - ROBOTSHOP")
    injectLogsContinuous(
        kafka_broker,
        kafka_user,
        kafka_pwd,
        kafka_topic_logs,
        kafka_cert,
        log_time_format,
        demo_logs,
    )
    return "OK"


def injectLogsSockShop(
    kafka_broker: str,
    kafka_user: str,
    kafka_pwd: str,
    kafka_topic_logs: str,
    kafka_cert: str,
    log_time_format: str,
    demo_logs_sock: str,
) -> str:
    """Inject generic logs for SockShop scenario.

    Args:
        kafka_broker: Kafka broker address.
        kafka_user: Kafka SASL username.
        kafka_pwd: Kafka SASL password.
        kafka_topic_logs: Target Kafka topic.
        kafka_cert: CA certificate content.
        log_time_format: Python strftime format for timestamps.
        demo_logs_sock: Newline-separated log templates.

    Returns:
        'OK' on success.
    """
    print("📛 START - Inject Logs - SOCKSHOP")
    log_time_format = "%Y-%m-%d %H:%M:%S.000"
    injectLogsGeneric(
        kafka_broker,
        kafka_user,
        kafka_pwd,
        kafka_topic_logs,
        kafka_cert,
        log_time_format,
        demo_logs_sock,
    )
    return "OK"


def injectLogsCUSTOM(
    kafka_broker: str,
    kafka_user: str,
    kafka_pwd: str,
    kafka_topic_logs: str,
    kafka_cert: str,
    log_time_format: str,
    custom_logs: str,
) -> str:
    """Inject generic logs for custom scenario.

    Args:
        kafka_broker: Kafka broker address.
        kafka_user: Kafka SASL username.
        kafka_pwd: Kafka SASL password.
        kafka_topic_logs: Target Kafka topic.
        kafka_cert: CA certificate content.
        log_time_format: Python strftime format for timestamps.
        custom_logs: Newline-separated log templates.

    Returns:
        'OK' on success.
    """
    print("📛 START - Inject Logs - CUSTOM_LOGS")
    log_time_format = "%Y-%m-%d %H:%M:%S.000"
    injectLogsGeneric(
        kafka_broker,
        kafka_user,
        kafka_pwd,
        kafka_topic_logs,
        kafka_cert,
        log_time_format,
        custom_logs,
    )
    return "OK"


def injectLogsContinuous(
    kafka_broker: str,
    kafka_user: str,
    kafka_pwd: str,
    kafka_topic_logs: str,
    kafka_cert: str,
    log_time_format: str,
    demo_logs_generic: str,
) -> str:
    """
    Inject logs with continuous (current-time) timestamps.

    Each log line receives the current timestamp + skew, so repeated
    injections produce logs with the same approximate time.

    Args:
        kafka_broker: Kafka broker address.
        kafka_user: Kafka SASL username.
        kafka_pwd: Kafka SASL password.
        kafka_topic_logs: Target Kafka topic.
        kafka_cert: CA certificate content.
        log_time_format: Python strftime format for timestamps.
        demo_logs_generic: Newline-separated log templates.

    Returns:
        'OK' on success.
    """
    stream = capture_shell('echo "' + kafka_cert + '" > ./demouiapp/ca.crt')
    stream.read().strip()

    print("    📛 KAFKA_BROKER  :" + str(kafka_broker) + ":")

    try:
        conf = {
            "bootstrap.servers": kafka_broker,
            "security.protocol": KAFKA_SECURITY_PROTOCOL,
            "sasl.mechanisms": KAFKA_SASL_MECHANISM,
            "sasl.username": kafka_user,
            "sasl.password": kafka_pwd,
            "client.id": socket.gethostname(),
            "enable.ssl.certificate.verification": "false",
            "ssl.ca.location": "./demouiapp/ca.crt",
        }

        producer = Producer(conf)

        for i in range(1, LOG_ITERATIONS):
            for line in demo_logs_generic.split("\n"):
                timestamp = datetime.datetime.now()
                timestamp = timestamp + datetime.timedelta(minutes=LOG_TIME_SKEW)
                timestampstr = timestamp.strftime(log_time_format) + "+00:00"
                line = line.replace("MY_TIMESTAMP", timestampstr).strip()
                producer.produce(kafka_topic_logs, value=line)
            producer.flush()
            print("    📝 Logs-Injection: " + str(i) + "  :  " + str(timestamp))
            time.sleep(5)
    except KafkaException as e:
        print("Kafka: " + str(e))

    print("✅ END - Inject Logs")
    return "OK"


def injectLogsGeneric(
    kafka_broker: str,
    kafka_user: str,
    kafka_pwd: str,
    kafka_topic_logs: str,
    kafka_cert: str,
    log_time_format: str,
    demo_logs_generic: str,
) -> str:
    """
    Inject logs with progressive timestamps.

    Each log line receives an incrementing timestamp, so the output
    spans a time range proportional to iterations * time_steps.

    Args:
        kafka_broker: Kafka broker address.
        kafka_user: Kafka SASL username.
        kafka_pwd: Kafka SASL password.
        kafka_topic_logs: Target Kafka topic.
        kafka_cert: CA certificate content.
        log_time_format: Python strftime format for timestamps.
        demo_logs_generic: Newline-separated log templates.

    Returns:
        'OK' on success.
    """
    stream = capture_shell('echo "' + kafka_cert + '" > ./demouiapp/ca.crt')
    stream.read().strip()

    print("    📛 KAFKA_BROKER  :" + str(kafka_broker) + ":")

    try:
        conf = {
            "bootstrap.servers": kafka_broker,
            "security.protocol": KAFKA_SECURITY_PROTOCOL,
            "sasl.mechanisms": KAFKA_SASL_MECHANISM,
            "sasl.username": kafka_user,
            "sasl.password": kafka_pwd,
            "client.id": socket.gethostname(),
            "enable.ssl.certificate.verification": "false",
            "ssl.ca.location": "./demouiapp/ca.crt",
        }

        producer = Producer(conf)

        timestamp = datetime.datetime.now()
        print("Base timestamp:" + str(timestamp))
        timestamp = timestamp + datetime.timedelta(minutes=LOG_TIME_SKEW)

        for i in range(1, LOG_ITERATIONS):
            for line in demo_logs_generic.split("\n"):
                timestamp = timestamp + datetime.timedelta(milliseconds=LOG_TIME_STEPS)
                epoch = int(timestamp.timestamp())
                timestampstr = timestamp.strftime(log_time_format) + "+00:00"
                epochstr = str(epoch) + "000"
                line = line.replace("MY_TIMESTAMP", timestampstr).strip()
                line = line.replace("MY_EPOCH", epochstr).strip()
                producer.produce(kafka_topic_logs, value=line)
            producer.flush()
            print("    📝 Logs-Injection: " + str(i) + "  :  " + str(timestamp))

    except KafkaException as e:
        print("Kafka: " + str(e))

    print("✅ END - Inject Logs")
    return "OK"


# -----------------------------------------------------------------------------
# Event Injection
# -----------------------------------------------------------------------------


def injectEventsMemRobot(
    datalayer_route: str,
    datalayer_user: str,
    datalayer_pwd: str,
) -> str:
    """Inject memory events for RobotShop scenario.

    Args:
        datalayer_route: Route to the IBM AIOps datalayer API.
        datalayer_user: Username for datalayer authentication.
        datalayer_pwd: Password for datalayer authentication.

    Returns:
        'OK' on success.
    """
    print("📛 START - Inject Events - MEM ROBOTSHOP")
    injectEventsGeneric(datalayer_route, datalayer_user, datalayer_pwd, DEMO_EVENTS_MEM)
    return "OK"


def injectEventsNetRobot(
    datalayer_route: str,
    datalayer_user: str,
    datalayer_pwd: str,
) -> str:
    """Inject network events for RobotShop scenario.

    Args:
        datalayer_route: Route to the IBM AIOps datalayer API.
        datalayer_user: Username for datalayer authentication.
        datalayer_pwd: Password for datalayer authentication.

    Returns:
        'OK' on success.
    """
    print("📛 START - Inject Events - NET ROBOTSHOP")
    injectEventsGeneric(
        datalayer_route, datalayer_user, datalayer_pwd, DEMO_EVENTS_ROBO_NET
    )
    return "OK"


def injectEventsFanACME(
    datalayer_route: str,
    datalayer_user: str,
    datalayer_pwd: str,
) -> str:
    """Inject fan events for ACME scenario.

    Args:
        datalayer_route: Route to the IBM AIOps datalayer API.
        datalayer_user: Username for datalayer authentication.
        datalayer_pwd: Password for datalayer authentication.

    Returns:
        'OK' on success.
    """
    print("📛 START - Inject Events - FAN ACME")
    injectEventsGeneric(
        datalayer_route, datalayer_user, datalayer_pwd, DEMO_EVENTS_FAN_ACME
    )
    return "OK"


def injectEventsNetSock(
    datalayer_route: str,
    datalayer_user: str,
    datalayer_pwd: str,
) -> str:
    """Inject network events for SockShop scenario.

    Args:
        datalayer_route: Route to the IBM AIOps datalayer API.
        datalayer_user: Username for datalayer authentication.
        datalayer_pwd: Password for datalayer authentication.

    Returns:
        'OK' on success.
    """
    print("📛 START - Inject Events - NET SOCKSHOP")
    injectEventsGeneric(
        datalayer_route, datalayer_user, datalayer_pwd, DEMO_EVENTS_NET_SOCK
    )
    return "OK"


def injectEventsTube(
    datalayer_route: str,
    datalayer_user: str,
    datalayer_pwd: str,
) -> str:
    """Inject events for Tube scenario.

    Args:
        datalayer_route: Route to the IBM AIOps datalayer API.
        datalayer_user: Username for datalayer authentication.
        datalayer_pwd: Password for datalayer authentication.

    Returns:
        'OK' on success.
    """
    print("📛 START - Inject Events - TUBE")
    injectEventsGeneric(
        datalayer_route, datalayer_user, datalayer_pwd, DEMO_EVENTS_TUBE
    )
    return "OK"


def injectEventsTelco(
    datalayer_route: str,
    datalayer_user: str,
    datalayer_pwd: str,
) -> str:
    """Inject events for Telco scenario.

    Args:
        datalayer_route: Route to the IBM AIOps datalayer API.
        datalayer_user: Username for datalayer authentication.
        datalayer_pwd: Password for datalayer authentication.

    Returns:
        'OK' on success.
    """
    print("📛 START - Inject Events - TELCO")
    injectEventsGeneric(
        datalayer_route, datalayer_user, datalayer_pwd, DEMO_EVENTS_TELCO
    )
    return "OK"


def injectEventsBusy(
    datalayer_route: str,
    datalayer_user: str,
    datalayer_pwd: str,
) -> str:
    """Inject repeated events for Busy scenario.

    Repeats the same event set 10 times to simulate high event volume.

    Args:
        datalayer_route: Route to the IBM AIOps datalayer API.
        datalayer_user: Username for datalayer authentication.
        datalayer_pwd: Password for datalayer authentication.

    Returns:
        'OK' on success.
    """
    for _ in range(10):
        print("📛 START - Inject Events - BUSY")
        injectEventsGeneric(
            datalayer_route, datalayer_user, datalayer_pwd, DEMO_EVENTS_BUSY
        )
    return "OK"


def injectEventsRisk(
    datalayer_route: str,
    datalayer_user: str,
    datalayer_pwd: str,
) -> str:
    """
    Inject risk events by running File Observer jobs.

    This function is unique to functions.py (not in functions_legacy.py).
    It triggers two observer jobs for network risk topology analysis.

    Args:
        datalayer_route: Route to the IBM AIOps datalayer API.
        datalayer_user: Username for datalayer authentication.
        datalayer_pwd: Password for datalayer authentication.

    Returns:
        'OK' on success.
    """
    print("📛 START - Inject Events - RISK by running File Observers")

    cmd_topo = """
    export AIOPS_NAMESPACE=$(oc get po -A|grep aiops-orchestrator-controller |awk '{print$1}')
    export AIO_PLATFORM_ROUTE=$(oc get route -n $AIOPS_NAMESPACE aimanager-aio-controller -o jsonpath={.spec.host})

    echo "        Namespace:          $AIOPS_NAMESPACE"
    echo "        AIO_PLATFORM_ROUTE: $AIO_PLATFORM_ROUTE"
    echo ""

    export CONSOLE_ROUTE=$(oc get route -n $AIOPS_NAMESPACE cp-console  -o jsonpath={.spec.host})
    export CPD_ROUTE=$(oc get route -n $AIOPS_NAMESPACE cpd  -o jsonpath={.spec.host})
    export CPADMIN_PWD=$(oc -n $AIOPS_NAMESPACE get secret platform-auth-idp-credentials -o jsonpath='{.data.admin_password}' | base64 -d && echo)
    export CPADMIN_USER=$(oc -n $AIOPS_NAMESPACE get secret platform-auth-idp-credentials -o jsonpath='{.data.admin_username}' | base64 -d && echo)
    export ACCESS_TOKEN=$(curl -s -k -H "Content-Type: application/x-www-form-urlencoded;charset=UTF-8" -d "grant_type=password&username=$CPADMIN_USER&password=$CPADMIN_PWD&scope=openid" https://$CONSOLE_ROUTE/idprovider/v1/auth/identitytoken|jq -r '.access_token')
    export ZEN_API_HOST=$(oc get route -n $AIOPS_NAMESPACE cpd -o jsonpath='{.spec.host}')
    export ZEN_TOKEN=$(curl -k -XGET https://$ZEN_API_HOST/v1/preauth/validateAuth \\
    -H "username: $CPADMIN_USER" \\
    -H "iam-token: $ACCESS_TOKEN"|jq -r '.accessToken')

    echo "Successfully logged in"
    echo ""
    echo "Running K8S OBSERVER"

    curl -X 'POST' --insecure \\
      "https://$AIO_PLATFORM_ROUTE/v1/observer/runjob/us-network-risk-topology" \\
      -H 'accept: application/json' \\
      -H 'Content-Type: application/json' \\
      -H "authorization: Bearer $ZEN_TOKEN"

    curl -X 'POST' --insecure \\
      "https://$AIO_PLATFORM_ROUTE/v1/observer/runjob/risk-proximity-EU-topology" \\
      -H 'accept: application/json' \\
      -H 'Content-Type: application/json' \\
      -H "authorization: Bearer $ZEN_TOKEN"
    """

    stream = capture_shell(cmd_topo)
    check_app = stream.read().strip()

    return "OK"


def injectEventsCUSTOM(
    datalayer_route: str,
    datalayer_user: str,
    datalayer_pwd: str,
) -> str:
    """Inject events for custom scenario.

    Args:
        datalayer_route: Route to the IBM AIOps datalayer API.
        datalayer_user: Username for datalayer authentication.
        datalayer_pwd: Password for datalayer authentication.

    Returns:
        'OK' on success.
    """
    print("📛 START - Inject Events - CUSTOM")
    injectEventsGeneric(datalayer_route, datalayer_user, datalayer_pwd, CUSTOM_EVENTS)
    return "OK"


def injectEventsGeneric(
    datalayer_route: str,
    datalayer_user: str,
    datalayer_pwd: str,
    demo_events: str,
) -> str:
    """
    Inject events into the IBM AIOps Datalayer.

    Parses the events data (newline-separated JSON), replaces MY_TIMESTAMP
    placeholders, and POSTs each event to the datalayer API.

    Args:
        datalayer_route: Route to the IBM AIOps datalayer API.
        datalayer_user: Username for datalayer authentication.
        datalayer_pwd: Password for datalayer authentication.
        demo_events: Newline-separated JSON event definitions.

    Returns:
        'OK' on success.

    Raises:
        SystemExit: If the datalayer API connection fails.
    """
    timestamp = datetime.datetime.now()

    url = "https://" + datalayer_route + DATALAYER_API_PATH + "/events"
    auth = HTTPBasicAuth(datalayer_user, datalayer_pwd)
    headers = {
        "Content-Type": "application/json",
        "Accept-Charset": "UTF-8",
        "x-username": "admin",
        "x-subscription-id": SUBSCRIPTION_ID,
    }

    for line in demo_events.split("\n"):
        timestamp = timestamp + datetime.timedelta(seconds=EVENTS_TIME_SKEW)
        timestampstr = timestamp.strftime("%Y-%m-%dT%H:%M:%S.000Z")
        line = line.replace("MY_TIMESTAMP", timestampstr)
        try:
            response = requests.post(
                url, data=line, headers=headers, auth=auth, verify=False
            )
        except requests.exceptions.RequestException as e:
            stream = capture_shell(
                "oc get route  -n "
                + aimanagerns
                + " datalayer-api  -o jsonpath='{.status.ingress[0].host}'"
            )
            print(
                "     ❗ YOU MIGHT WANT TO USE THE DATALAYER PUBLIC ROUTE: "
                + str(stream.read().strip())
            )
            raise SystemExit(e)

        print("    🚀 Events-Injection:" + str(response.content))

    print("✅ END - Inject Events")
    return "OK"


# -----------------------------------------------------------------------------
# Metric Injection
# -----------------------------------------------------------------------------


def injectMetricsMem(
    metric_route: str,
    metric_token: str,
) -> str:
    """Inject memory metrics for RobotShop scenario.

    Args:
        metric_route: Route to the IBM AIOps metrics API.
        metric_token: Bearer token for metrics authentication.

    Returns:
        'OK' on success.
    """
    print("📛 START - Inject Metrics - MEM ROBOTSHOP")
    METRIC_TIME_SKEW = int(os.environ.get("METRIC_TIME_SKEW"))
    METRIC_TIME_STEP = int(os.environ.get("METRIC_TIME_STEP"))
    injectMetrics(
        metric_route,
        metric_token,
        METRICS_TO_SIMULATE_MEM,
        METRIC_TIME_SKEW,
        METRIC_TIME_STEP,
        "injectMetricsMem",
    )
    return "OK"


def injectMetricsFiber(
    metric_route: str,
    metric_token: str,
) -> str:
    """
    Inject fiber metrics for Telco scenario.

    This function is unique to functions.py (not in functions_legacy.py).

    Args:
        metric_route: Route to the IBM AIOps metrics API.
        metric_token: Bearer token for metrics authentication.

    Returns:
        'OK' on success.
    """
    print("📛 START - Inject Metrics - FIBER ROBOTSHOP")
    METRIC_TIME_SKEW = int(os.environ.get("METRIC_TIME_SKEW"))
    METRIC_TIME_STEP = int(os.environ.get("METRIC_TIME_STEP"))
    injectMetrics(
        metric_route,
        metric_token,
        METRICS_TO_SIMULATE_FIBER,
        METRIC_TIME_SKEW,
        METRIC_TIME_STEP,
        "injectMetricsFiber",
    )
    return "OK"


def injectMetricsFiberTransatlantic(
    metric_route: str,
    metric_token: str,
) -> str:
    """
    Inject NY fiber metrics for Transatlantic Telco scenario.

    This function is unique to functions.py (not in functions_legacy.py).

    Args:
        metric_route: Route to the IBM AIOps metrics API.
        metric_token: Bearer token for metrics authentication.

    Returns:
        'OK' on success.
    """
    print("📛 START - Inject Metrics - FIBER TRANSATLANTIC")
    METRIC_TIME_SKEW = int(os.environ.get("METRIC_TIME_SKEW"))
    METRIC_TIME_STEP = int(os.environ.get("METRIC_TIME_STEP"))
    injectMetrics(
        metric_route,
        metric_token,
        METRICS_TO_SIMULATE_FIBER_NY,
        METRIC_TIME_SKEW,
        METRIC_TIME_STEP,
        "injectMetricsFiberTransatlantic",
    )
    return "OK"


def injectMetricsFanTemp(
    metric_route: str,
    metric_token: str,
) -> str:
    """Inject fan temperature metrics for RobotShop scenario.

    Args:
        metric_route: Route to the IBM AIOps metrics API.
        metric_token: Bearer token for metrics authentication.

    Returns:
        'OK' on success.
    """
    print("📛 START - Inject Metrics - FAN-TEMP ROBOTSHOP")
    METRIC_TIME_SKEW = 0
    METRIC_TIME_STEP = 120
    injectMetrics(
        metric_route,
        metric_token,
        METRICS_TO_SIMULATE_FAN_TEMP,
        METRIC_TIME_SKEW,
        METRIC_TIME_STEP,
        "injectMetricsFanTemp",
    )
    return "OK"


def injectMetricsFan(
    metric_route: str,
    metric_token: str,
) -> str:
    """Inject fan speed metrics for RobotShop scenario.

    Args:
        metric_route: Route to the IBM AIOps metrics API.
        metric_token: Bearer token for metrics authentication.

    Returns:
        'OK' on success.
    """
    print("📛 START - Inject Metrics - FAN ROBOTSHOP")
    METRIC_TIME_SKEW = int(os.environ.get("METRIC_TIME_SKEW"))
    METRIC_TIME_STEP = int(os.environ.get("METRIC_TIME_STEP"))
    injectMetrics(
        metric_route,
        metric_token,
        METRICS_TO_SIMULATE_FAN,
        METRIC_TIME_SKEW,
        METRIC_TIME_STEP,
        "injectMetricsFan",
    )
    return "OK"


def injectMetricsFanTempACME(
    metric_route: str,
    metric_token: str,
) -> str:
    """Inject fan temperature metrics for ACME scenario.

    Args:
        metric_route: Route to the IBM AIOps metrics API.
        metric_token: Bearer token for metrics authentication.

    Returns:
        'OK' on success.
    """
    print("📛 START - Inject Metrics - FAN-TEMP ACME")
    METRIC_TIME_SKEW = 0
    METRIC_TIME_STEP = 120
    injectMetrics(
        metric_route,
        metric_token,
        METRICS_TO_SIMULATE_FAN_TEMP_ACME,
        METRIC_TIME_SKEW,
        METRIC_TIME_STEP,
        "injectMetricsFanTempACME",
    )
    return "OK"


def injectMetricsFanACME(
    metric_route: str,
    metric_token: str,
) -> str:
    """Inject fan speed metrics for ACME scenario.

    Args:
        metric_route: Route to the IBM AIOps metrics API.
        metric_token: Bearer token for metrics authentication.

    Returns:
        'OK' on success.
    """
    print("📛 START - Inject Metrics - FAN ACME")
    METRIC_TIME_SKEW = int(os.environ.get("METRIC_TIME_SKEW"))
    METRIC_TIME_STEP = int(os.environ.get("METRIC_TIME_STEP"))
    injectMetrics(
        metric_route,
        metric_token,
        METRICS_TO_SIMULATE_FAN_ACME,
        METRIC_TIME_SKEW,
        METRIC_TIME_STEP,
        "injectMetricsFanACME",
    )
    return "OK"


def injectMetricsSockNet(
    metric_route: str,
    metric_token: str,
) -> str:
    """Inject network metrics for SockShop scenario.

    Args:
        metric_route: Route to the IBM AIOps metrics API.
        metric_token: Bearer token for metrics authentication.

    Returns:
        'OK' on success.
    """
    print("📛 START - Inject Metrics - NET SOCKSHOP")
    METRIC_TIME_SKEW = int(os.environ.get("METRIC_TIME_SKEW"))
    METRIC_TIME_STEP = int(os.environ.get("METRIC_TIME_STEP"))
    injectMetrics(
        metric_route,
        metric_token,
        METRICS_TO_SIMULATE_NET_SOCK,
        METRIC_TIME_SKEW,
        METRIC_TIME_STEP,
        "injectMetricsSockNet",
    )
    return "OK"


def injectMetricsCUSTOM(
    metric_route: str,
    metric_token: str,
) -> str:
    """Inject metrics for custom scenario.

    Args:
        metric_route: Route to the IBM AIOps metrics API.
        metric_token: Bearer token for metrics authentication.

    Returns:
        'OK' on success.
    """
    print("📛 START - Inject Metrics - CUSTOM METRICS")
    METRIC_TIME_SKEW = 0
    METRIC_TIME_STEP = 0
    injectMetrics(
        metric_route,
        metric_token,
        CUSTOM_METRICS,
        METRIC_TIME_SKEW,
        METRIC_TIME_STEP,
        "injectMetricsCUSTOM",
    )
    return "OK"


def injectMetrics(
    metric_route: str,
    metric_token: str,
    metrics_to_simulate: List[str],
    metric_time_skew: int,
    metric_time_step: int,
    metric_name: str,
) -> str:
    """
    Inject simulated metrics into the IBM AIOps Metrics API.

    Generates metric batches by iterating through the definitions,
    adding random variation to values, and POSTing to the metrics endpoint.

    Args:
        metric_route: Route to the IBM AIOps metrics API.
        metric_token: Bearer token for metrics authentication.
        metrics_to_simulate: List of CSV metric definitions.
        metric_time_skew: Initial seconds to add to the base timestamp.
        metric_time_step: Milliseconds to advance between metric points.
        metric_name: Human-readable metric scenario identifier.

    Returns:
        'OK' on success.

    Raises:
        SystemExit: If the metrics API connection fails.
    """
    print("🟣          METRICS_TO_SIMULATE:               " + str(metrics_to_simulate))
    print(
        "🟣          #METRICS_TO_SIMULATE:              "
        + str(len(metrics_to_simulate))
    )

    stream = capture_shell(
        "oc get po -A|grep aiops-orchestrator-controller |awk '{print$1}'"
    )
    aimanagerns = stream.read().strip()

    print("     ❓ Getting Details Metric Endpoint")
    stream = capture_shell(
        "oc get route -n " + aimanagerns + "| grep ibm-nginx-svc | awk '{print $2}'"
    )
    metric_route = stream.read().strip()
    metric_route = os.environ.get("METRIC_ROUTE_OVERRIDE", default=metric_route)

    stream = capture_shell(
        "oc get route -n " + aimanagerns + " cp-console  -o jsonpath={.spec.host}"
    )
    console_route = stream.read().strip()

    stream = capture_shell(
        "oc get secret -n "
        + aimanagerns
        + " platform-auth-idp-credentials -o jsonpath='{.data.admin_username}' | base64 --decode"
    )
    tmpusr = stream.read().strip()
    print("     🟠 USR :" + str(tmpusr))

    stream = capture_shell(
        "oc get secret -n "
        + aimanagerns
        + " platform-auth-idp-credentials -o jsonpath='{.data.admin_password}' | base64 --decode"
    )
    tmppass = stream.read().strip()
    print("     🟠 PWD :" + str(tmppass))

    stream = capture_shell(
        'curl -s -k -H "Content-Type: application/x-www-form-urlencoded;charset=UTF-8" '
        '-d "grant_type=password&username='
        + tmpusr
        + "&password="
        + tmppass
        + '&scope=openid" '
        "https://"
        + console_route
        + "/idprovider/v1/auth/identitytoken|jq -r '.access_token'"
    )
    access_token = stream.read().strip()
    print("     🟠 ACCESS_TOKEN :" + access_token[:25] + "...")

    stream = capture_shell(
        "curl -s -k -XGET https://" + metric_route + "/v1/preauth/validateAuth "
        '-H "username: '
        + tmpusr
        + '" -H "iam-token: '
        + access_token
        + '"|jq -r ".accessToken"'
    )
    metric_token = stream.read().strip()
    print("     🟠 METRIC_TOKEN :" + metric_route[:25] + "...")

    requests.packages.urllib3.disable_warnings()

    timestamp = datetime.datetime.now()
    timestamp = timestamp + datetime.timedelta(seconds=metric_time_skew)

    curr_iterations = 0
    url = "https://" + metric_route + METRICS_API_PATH

    headers = {
        "Content-Type": "application/json",
        "Accept-Charset": "UTF-8",
        "Authorization": "Bearer " + metric_token,
        "X-TenantID": SUBSCRIPTION_ID,
    }

    for i in range(1, METRIC_ITERATIONS):
        output_json = '{"groups":['
        curr_iterations = curr_iterations + 1

        for _ in range(1, 40):
            for line in metrics_to_simulate:
                line = line.strip()
                timestamp = timestamp + datetime.timedelta(
                    milliseconds=metric_time_step
                )
                my_timestamp = timestamp.strftime("%s")
                my_timestamp = my_timestamp + "000"
                my_timestamp_readable = timestamp.strftime("%Y-%m-%dT%H:%M:%S.000Z")

                elements = line.split(",")
                my_resource_name = elements[0]
                my_metric_name = elements[1]
                my_group_id = elements[2]
                my_fix_value = elements[3]
                my_variation = elements[4]

                if my_fix_value == "ITERATIONS":
                    current_value = str(int(my_variation) + 2 * int(curr_iterations))
                else:
                    current_value = str(
                        random.randint(
                            int(my_fix_value), int(my_fix_value) + int(my_variation)
                        )
                    )

                current_line = (
                    '{"timestamp":"'
                    + my_timestamp
                    + '","resourceID":"'
                    + my_resource_name
                    + '","metrics":{'
                    + '"'
                    + my_metric_name
                    + '":'
                    + current_value
                    + "},"
                    + '"attributes":{"group":"'
                    + my_group_id
                    + '","node":"'
                    + my_resource_name
                    + '"} },'
                )
                output_json = output_json + current_line

        last_line = (
            '{"timestamp":"'
            + my_timestamp
            + '","resourceID":"'
            + my_resource_name
            + '","metrics":{'
            + '"'
            + my_metric_name
            + '":'
            + current_value
            + "},"
            + '"attributes":{"group":"'
            + my_group_id
            + '","node":"'
            + my_resource_name
            + '"} }'
        )
        output_json = output_json + last_line
        output_json = output_json + "]}"

        try:
            response = requests.post(
                url, data=output_json, headers=headers, verify=False
            )
        except requests.exceptions.RequestException as e:
            stream = capture_shell(
                "oc get route -n "
                + aimanagerns
                + "| grep ibm-nginx-svc | awk '{print $2}'"
            )
            print(
                "     ❗ YOU MIGHT WANT TO USE THE METRIC PUBLIC ROUTE: "
                + str(stream.read().strip())
            )
            raise SystemExit(e)

        print(
            "    🚇 Metrics-Injection:"
            + str(metric_name)
            + " - "
            + str(my_timestamp_readable)
            + " - "
            + str(response.content)
        )

    print("✅ END - Inject Metrics")
    return "OK"


# -----------------------------------------------------------------------------
# Topology Management
# -----------------------------------------------------------------------------


def checkTopology() -> str:
    """
    Check if custom topology already exists in the cluster.

    Returns:
        Combined APP_ID and TEMPLATE_ID strings if topology exists, empty string otherwise.
    """
    print("🛠️ checkTopology")
    print("     ❓ Check if topology already exists")

    cmd_topo = (
        '''
    export APP_NAME="'''
        + CUSTOM_TOPOLOGY_APP_NAME
        + """"
    export APP_NAME_ID=$(echo $APP_NAME| tr '[:upper:]' '[:lower:]'| tr ' ' '-')

    export AIOPS_NAMESPACE=$(oc get po -A|grep aiops-orchestrator-controller |awk '{print$1}')
    export TOPOLOGY_REST_USR=$(oc get secret aiops-topology-asm-credentials -n $AIOPS_NAMESPACE -o jsonpath='{.data.username}' | base64 --decode)
    export TOPOLOGY_REST_PWD=$(oc get secret aiops-topology-asm-credentials -n $AIOPS_NAMESPACE -o jsonpath='{.data.password}' | base64 --decode)

    export TOPO_MGT_ROUTE="https://"$(oc get route -n $AIOPS_NAMESPACE aiops-topology-topology -o jsonpath={.spec.host})

    export LOGIN="$TOPOLOGY_REST_USR:$TOPOLOGY_REST_PWD"

    export APP_ID=$(curl -s -X "GET" "$TOPO_MGT_ROUTE/1.0/topology/groups?_field=*&_filter=keyIndexName%3D$APP_NAME_ID" --insecure -u $LOGIN -H 'Content-Type: application/json' -H 'X-TenantID: cfd95b7e-3bc7-4006-a4a8-a73a79c71255'|jq -r -c '._items[]|._id'| tail -1)
    export TEMPLATE_ID=$(curl -s -X "GET" "$TOPO_MGT_ROUTE/1.0/topology/groups?_field=*&_filter=keyIndexName%3Dcustom-template" --insecure -u $LOGIN -H 'Content-Type: application/json' -H 'X-TenantID: cfd95b7e-3bc7-4006-a4a8-a73a79c71255'|jq -r -c '._items[]|._id'| tail -1)
    echo $APP_ID$TEMPLATE_ID
    """
    )

    stream = capture_shell(cmd_topo)
    check_app = stream.read().strip()

    return check_app


def modifyProperty(
    resource_name: str,
    resource_type: str,
    values: str,
) -> None:
    """
    Modify a topology resource's properties.

    Args:
        resource_name: Name of the topology resource to modify.
        resource_type: Type of the topology resource.
        values: JSON string of property values to set.
    """
    print("🛠️ modifyProperty")
    print("🟣           📈 DCUSTOM_PROPERTY_RESOURCE_NAME:    " + str(resource_name))
    print("🟣           📈 DCUSTOM_PROPERTY_RESOURCE_TYPE:    " + str(resource_type))
    print("🟣           📈 DCUSTOM_PROPERTY_VALUES_NOK:       " + str(values))

    cmd_topo = (
        """
    echo "🚀 Modify """
        + resource_name
        + """ for Demo"
    export AIOPS_NAMESPACE=$(oc get po -A|grep aiops-orchestrator-controller |awk '{print$1}')
    export TOPO_REST_USR=$(oc get secret aiops-topology-asm-credentials -n $AIOPS_NAMESPACE -o jsonpath='{.data.username}' | base64 --decode)
    export TOPO_REST_PWD=$(oc get secret aiops-topology-asm-credentials -n $AIOPS_NAMESPACE -o jsonpath='{.data.password}' | base64 --decode)
    export TOPO_MGT_ROUTE="https://"$(oc get route -n $AIOPS_NAMESPACE aiops-topology-topology -o jsonpath={.spec.host})
    export LOGIN="$TOPO_REST_USR:$TOPO_REST_PWD"

    export OBJ_ID=$(curl -k -s -X "GET" "$TOPO_MGT_ROUTE/1.0/topology/resources?_filter=name%3D"""
        + resource_name
        + """&_filter=entityTypes%3D"""
        + resource_type
        + """&_field=uniqueId&_include_global_resources=false&_include_count=false&_include_status=false&_include_status_severity=false&_include_metadata=false&_return_composites=false" --insecure -u $LOGIN -H 'Content-Type: application/json' -H 'X-TenantID: cfd95b7e-3bc7-4006-a4a8-a73a79c71255'|jq -r -c '._items[]|._id'| tail -1)
    echo $OBJ_ID

    export result=$(curl -k -s -X "POST" "$TOPO_MGT_ROUTE/1.0/topology/resources/$OBJ_ID" --insecure -u $LOGIN -H 'Content-Type: application/json' -H 'X-TenantID: cfd95b7e-3bc7-4006-a4a8-a73a79c71255' -d ' """
        + values
        + """ ')
    echo "    result: $result"
    """
    )

    print("           cmdTopo:              " + cmd_topo)

    try:
        stream = capture_shell(cmd_topo)
        res = stream.read().strip()
        print("           modifyProperty DONE:              " + res)
    except Exception as error:
        print("           🟥 modifyProperty ERROR:              " + str(error))


def modifyMYSQL() -> None:
    """Modify MySQL buffer pool size for demo (sets to 1GB)."""
    print("🛠️ modifyMYSQL")

    cmd_topo = """
    export AIOPS_NAMESPACE=$(oc get po -A|grep aiops-orchestrator-controller |awk '{print$1}')
    export TOPO_REST_USR=$(oc get secret aiops-topology-asm-credentials -n $AIOPS_NAMESPACE -o jsonpath='{.data.username}' | base64 --decode)
    export TOPO_REST_PWD=$(oc get secret aiops-topology-asm-credentials -n $AIOPS_NAMESPACE -o jsonpath='{.data.password}' | base64 --decode)
    export TOPO_MGT_ROUTE="https://"$(oc get route -n $AIOPS_NAMESPACE aiops-topology-topology -o jsonpath={.spec.host})
    export LOGIN="$TOPO_REST_USR:$TOPO_REST_PWD"

    export MYSQL_ID=$(curl -X "GET" "$TOPO_MGT_ROUTE/1.0/topology/resources?_filter=name%3Dmysql&_filter=entityTypes%3Ddeployment&_field=uniqueId&_include_global_resources=false&_include_count=false&_include_status=false&_include_status_severity=false&_include_metadata=false&_return_composites=false" --insecure -u $LOGIN -H 'Content-Type: application/json' -H 'X-TenantID: cfd95b7e-3bc7-4006-a4a8-a73a79c71255'|jq -r -c '._items[]|._id'| tail -1)

    export result=$(curl -X "POST" "$TOPO_MGT_ROUTE/1.0/topology/resources/$MYSQL_ID" --insecure -u $LOGIN -H 'Content-Type: application/json' -H 'X-TenantID: cfd95b7e-3bc7-4006-a4a8-a73a79c71255' -d '{"innodb_buffer_pool_size": "1GB"}')
    echo $result
    """

    print("   🚀 Modify innodb_buffer_pool_size for Demo")
    stream = capture_shell(cmd_topo)
    res = stream.read().strip()
    print("           DONE:              " + res)


def resetMYSQL() -> None:
    """Reset MySQL buffer pool size to normal (sets to 8GB)."""
    print("🛠️ resetMYSQL")

    cmd_topo = """
    export AIOPS_NAMESPACE=$(oc get po -A|grep aiops-orchestrator-controller |awk '{print$1}')
    export TOPO_REST_USR=$(oc get secret aiops-topology-asm-credentials -n $AIOPS_NAMESPACE -o jsonpath='{.data.username}' | base64 --decode)
    export TOPO_REST_PWD=$(oc get secret aiops-topology-asm-credentials -n $AIOPS_NAMESPACE -o jsonpath='{.data.password}' | base64 --decode)
    export TOPO_MGT_ROUTE="https://"$(oc get route -n $AIOPS_NAMESPACE aiops-topology-topology -o jsonpath={.spec.host})
    export LOGIN="$TOPO_REST_USR:$TOPO_REST_PWD"

    export MYSQL_ID=$(curl -X "GET" "$TOPO_MGT_ROUTE/1.0/topology/resources?_filter=name%3Dmysql&_filter=entityTypes%3Ddeployment&_field=uniqueId&_include_global_resources=false&_include_count=false&_include_status=false&_include_status_severity=false&_include_metadata=false&_return_composites=false" --insecure -u $LOGIN -H 'Content-Type: application/json' -H 'X-TenantID: cfd95b7e-3bc7-4006-a4a8-a73a79c71255'|jq -r -c '._items[]|._id'| tail -1)

    export result=$(curl -X "POST" "$TOPO_MGT_ROUTE/1.0/topology/resources/$MYSQL_ID" --insecure -u $LOGIN -H 'Content-Type: application/json' -H 'X-TenantID: cfd95b7e-3bc7-4006-a4a8-a73a79c71255' -d '{"innodb_buffer_pool_size": "8GB"}')
    echo $result
    """

    print("   🚀 Reset innodb_buffer_pool_size for Demo")
    stream = capture_shell(cmd_topo)
    res = stream.read().strip()
    print("           DONE:              " + res)


def loadTopology() -> str:
    """
    Load custom topology into IBM AIOps.

    Creates the topology file, uploads it to the file observer pod,
    creates the file observer job, template, and application group.

    Returns:
        'OK' on success.
    """
    print("🛠️ loadTopology")

    # Create topology file and upload
    cmd_topo = (
        """
    echo \'"""
        + str(CUSTOM_TOPOLOGY)
        + """\'  > ./custom-topology.txt

    export AIOPS_NAMESPACE=$(oc get po -A|grep aiops-orchestrator-controller |awk '{print$1}')

    FILE_OBSERVER_POD=$(oc get po -n $AIOPS_NAMESPACE -l app.kubernetes.io/instance=aiops-topology,app.kubernetes.io/name=file-observer -o jsonpath='{.items[0].metadata.name}')
    LOAD_FILE_NAME="custom-topology.txt"
    FILE_OBSERVER_CAP=$(pwd)"/custom-topology.txt"
    TARGET_FILE_PATH="/opt/ibm/netcool/asm/data/file-observer/${LOAD_FILE_NAME}"

    echo "  Copying capture file to file observer pod"
    oc cp -n $AIOPS_NAMESPACE -c aiops-topology-file-observer ${FILE_OBSERVER_CAP} ${FILE_OBSERVER_POD}:${TARGET_FILE_PATH}
    """
    )

    if len(CUSTOM_TOPOLOGY) > 0:
        print("   🚀 Custom Topology - FileObserver demoui-custom-topology")
        print("     ❓ Upload Custom Topology - this may take a minute or two")
        stream = capture_shell(cmd_topo)
        create_topo = stream.read().strip()
        print("           Upload Custom Topology:              " + create_topo)
    else:
        print("     ❓ Skip Creating Custom Topology")
        print("     ❗ Has been disabled in the DemoUI configuration")

    # Create File Observer job
    cmd_topo = """
    export AIOPS_NAMESPACE=$(oc get po -A|grep aiops-orchestrator-controller |awk '{print$1}')
    LOAD_FILE_NAME="custom-topology.txt"
    TARGET_FILE_PATH="/opt/ibm/netcool/asm/data/file-observer/${LOAD_FILE_NAME}"

    export TOPO_REST_USR=$(oc get secret aiops-topology-asm-credentials -n $AIOPS_NAMESPACE -o jsonpath='{.data.username}' | base64 --decode)
    export TOPO_REST_PWD=$(oc get secret aiops-topology-asm-credentials -n $AIOPS_NAMESPACE -o jsonpath='{.data.password}' | base64 --decode)
    export LOGIN="$TOPO_REST_USR:$TOPO_REST_PWD"

    export TOPO_ROUTE="https://"$(oc get route -n $AIOPS_NAMESPACE aiops-topology-file-observer -o jsonpath={.spec.host})
    export JOB_ID=demoui-custom-topology

    echo '{\"unique_id\": \"demoui-custom-topology\",\"description\": \"Automatically created by Nicks scripts\",\"parameters\": {\"file\": \"/opt/ibm/netcool/asm/data/file-observer/custom-topology.txt\"}}' > /tmp/custom-topology-observer.txt

    curl -X "POST" -s "$TOPO_ROUTE/1.0/file-observer/jobs" --insecure \\
        -H 'X-TenantID: cfd95b7e-3bc7-4006-a4a8-a73a79c71255' \\
        -H "accept: application/json" \\
        -H "Content-Type: application/json"\\
        -u $LOGIN \\
        -d @/tmp/custom-topology-observer.txt
    """

    if len(CUSTOM_TOPOLOGY) > 0:
        print(
            "     ❓ Creating Custom Topology File Observer - this may take a minute or two"
        )
        stream = capture_shell(cmd_topo)
        create_topo = stream.read().strip()

    # Create Template
    cmd_topo = (
        '''
    export AIOPS_NAMESPACE=$(oc get po -A|grep aiops-orchestrator-controller |awk '{print$1}')

    export TOPO_REST_USR=$(oc get secret aiops-topology-asm-credentials -n $AIOPS_NAMESPACE -o jsonpath='{.data.username}' | base64 --decode)
    export TOPO_REST_PWD=$(oc get secret aiops-topology-asm-credentials -n $AIOPS_NAMESPACE -o jsonpath='{.data.password}' | base64 --decode)
    export LOGIN="$TOPO_REST_USR:$TOPO_REST_PWD"

    export TOPO_ROUTE="https://"$(oc get route -n $AIOPS_NAMESPACE aiops-topology-file-observer -o jsonpath={.spec.host})
    export TOPO_MGT_ROUTE="https://"$(oc get route -n $AIOPS_NAMESPACE aiops-topology-topology -o jsonpath={.spec.host})

    export TEMPLATE_ID=$(curl -s -X "GET" "$TOPO_MGT_ROUTE/1.0/topology/groups?_field=*&_filter=keyIndexName%3Dcustom-template" --insecure -u $LOGIN -H 'Content-Type: application/json' -H 'X-TenantID: cfd95b7e-3bc7-4006-a4a8-a73a79c71255'|jq -r -c '._items[]|._id'| tail -1)

    echo "    TEMPLATE_ID: $TEMPLATE_ID"

    if [ -z "$TEMPLATE_ID" ]
    then
        echo "  Create Template"
        curl -s -X "POST" "$TOPO_MGT_ROUTE/1.0/topology/groups" --insecure \\
        -u $LOGIN \\
        -H 'Content-Type: application/json' \\
        -H 'X-TenantID: cfd95b7e-3bc7-4006-a4a8-a73a79c71255' \\
        -d '  {
            "keyIndexName": "custom-template",
            "_correlationEnabled": "true",
            "iconId": "application",
            "businessCriticality": "Gold",
            "vertexType": "group",
            "groupTokens": [
                "'''
        + CUSTOM_TOPOLOGY_TAG
        + '''"
            ],
            "correlatable": "true",
            "name": "custom-template",
            "entityTypes": [
                "completeGroup",
                "compute"
            ],
            "tags": [
                "demo"
            ]
        }'
    else
        echo "  Recreate Template"
        curl -s -X "DELETE" "$TOPO_MGT_ROUTE/1.0/topology/groups/$TEMPLATE_ID" --insecure \\
        -u $LOGIN \\
        -H 'Content-Type: application/json' \\
        -H 'X-TenantID: cfd95b7e-3bc7-4006-a4a8-a73a79c71255'

        curl -s -X "POST" "$TOPO_MGT_ROUTE/1.0/topology/groups" --insecure \\
        -u $LOGIN \\
        -H 'Content-Type: application/json' \\
        -H 'X-TenantID: cfd95b7e-3bc7-4006-a4a8-a73a79c71255' \\
        -d '  {
            "keyIndexName": "custom-template",
            "_correlationEnabled": "true",
            "iconId": "application",
            "businessCriticality": "Gold",
            "vertexType": "group",
            "groupTokens": [
                "'''
        + CUSTOM_TOPOLOGY_TAG
        + """"
            ],
            "correlatable": "true",
            "name": "custom-template",
            "entityTypes": [
                "completeGroup",
                "compute"
            ],
            "tags": [
                "demo"
            ]
        }'
    fi
    """
    )

    if len(CUSTOM_TOPOLOGY_TAG) > 0:
        print(
            "     ❓ Creating Custom Topology Template - this may take a minute or two"
        )
        stream = capture_shell(cmd_topo)
        create_topo = stream.read().strip()

    # Create Application
    cmd_topo = (
        '''
    echo "Create Custom Topology - Add Members to App"

    export APP_NAME="'''
        + CUSTOM_TOPOLOGY_APP_NAME
        + """"
    export APP_NAME_ID=$(echo $APP_NAME| tr '[:upper:]' '[:lower:]'| tr ' ' '-')

    export AIOPS_NAMESPACE=$(oc get po -A|grep aiops-orchestrator-controller |awk '{print$1}')
    export TOPOLOGY_REST_USR=$(oc get secret aiops-topology-asm-credentials -n $AIOPS_NAMESPACE -o jsonpath='{.data.username}' | base64 --decode)
    export TOPOLOGY_REST_PWD=$(oc get secret aiops-topology-asm-credentials -n $AIOPS_NAMESPACE -o jsonpath='{.data.password}' | base64 --decode)

    export TOPO_MGT_ROUTE="https://"$(oc get route -n $AIOPS_NAMESPACE aiops-topology-topology -o jsonpath={.spec.host})

    export LOGIN="$TOPOLOGY_REST_USR:$TOPOLOGY_REST_PWD"

    export APP_ID=$(curl -s -X "GET" "$TOPO_MGT_ROUTE/1.0/topology/groups?_field=*&_filter=keyIndexName%3D$APP_NAME_ID" --insecure -u $LOGIN -H 'Content-Type: application/json' -H 'X-TenantID: cfd95b7e-3bc7-4006-a4a8-a73a79c71255'|jq -r -c '._items[]|._id'| tail -1)
    export TEMPLATE_ID=$(curl -s -X "GET" "$TOPO_MGT_ROUTE/1.0/topology/groups?_field=*&_filter=keyIndexName%3Dcustom-template" --insecure -u $LOGIN -H 'Content-Type: application/json' -H 'X-TenantID: cfd95b7e-3bc7-4006-a4a8-a73a79c71255'|jq -r -c '._items[]|._id'| tail -1)

    echo '{\"keyIndexName\": \"'$APP_NAME_ID'\",\"_correlationEnabled\": \"true\",\"iconId\": \"cluster\",\"businessCriticality\": \"Platinum\",\"vertexType\": \"group\",\"correlatable\": \"true\",\"disruptionCostPerMin\": \"1000\",\"name\": \"'$APP_NAME'\",\"entityTypes\": [\"waiopsApplication\"],\"tags\": [\"app:'$APP_NAME_ID'\"]}' > /tmp/custom-topology-app.txt

    if [ -z "$APP_ID" ]
    then
        echo "  Creating Application"
        curl -s -X "POST" "$TOPO_MGT_ROUTE/1.0/topology/groups" --insecure \\
        -u $LOGIN \\
        -H 'Content-Type: application/json' \\
        -H 'X-TenantID: cfd95b7e-3bc7-4006-a4a8-a73a79c71255' \\
        -d @/tmp/custom-topology-app.txt
    else
        echo "  Application already exists"
        echo "  Re-Creating Application"
        curl -s -X "DELETE" "$TOPO_MGT_ROUTE/1.0/topology/groups/$APP_ID" --insecure \\
        -u $LOGIN \\
        -H 'Content-Type: application/json' \\
        -H 'X-TenantID: cfd95b7e-3bc7-4006-a4a8-a73a79c71255'

        curl -s -X "POST" "$TOPO_MGT_ROUTE/1.0/topology/groups" --insecure \\
        -u $LOGIN \\
        -H 'Content-Type: application/json' \\
        -H 'X-TenantID: cfd95b7e-3bc7-4006-a4a8-a73a79c71255' \\
        -d @/tmp/custom-topology-app.txt
    fi

    export APP_ID=$(curl -s -X "GET" "$TOPO_MGT_ROUTE/1.0/topology/groups?_field=*&_filter=keyIndexName%3D$APP_NAME_ID" --insecure -u $LOGIN -H 'Content-Type: application/json' -H 'X-TenantID: cfd95b7e-3bc7-4006-a4a8-a73a79c71255'|jq -r -c '._items[]|._id'| tail -1)

    echo "  Add Template (File Observer) Resources"
    curl -s -X "POST" "$TOPO_MGT_ROUTE/1.0/topology/groups/$APP_ID/members" --insecure \\
    -u $LOGIN \\
    -H 'Content-Type: application/json' \\
    -H 'X-TenantID: cfd95b7e-3bc7-4006-a4a8-a73a79c71255' \\
    -d '{
        \"_id\": \"'$TEMPLATE_ID'\"
    }'
    """
    )

    if len(CUSTOM_TOPOLOGY_APP_NAME) > 0:
        print(
            "     ❓ Creating Custom Topology Application - this may take a minute or two"
        )
        stream = capture_shell(cmd_topo)
        create_topo = stream.read().strip()
        print("   🚀 Get Parameters")

    return "OK"
