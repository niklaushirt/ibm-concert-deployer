"""
Log injector for IBM AIOps DemoUI.

Handles injection of log entries into Kafka. Supports both continuous
(repeating current timestamp) and generic (progressive timestamp) modes.
"""

import datetime
import os
import socket
from dataclasses import dataclass
from typing import Optional

from confluent_kafka import KafkaException, Producer

from ..utils import KAFKA_SASL_MECHANISM, KAFKA_SECURITY_PROTOCOL, get_logger
from ..utils.commands import capture_shell
from ..utils.constants import (
    DEFAULT_LOG_ITERATIONS,
    DEFAULT_LOG_TIME_FORMAT,
    DEFAULT_LOG_TIME_SKEW,
    DEFAULT_LOG_TIME_STEPS,
)

logger = get_logger("injectors.log")


@dataclass
class LogConfig:
    """Configuration for a specific log injection scenario."""

    name: str
    logs_data: str
    time_format: str = DEFAULT_LOG_TIME_FORMAT
    iterations: int = DEFAULT_LOG_ITERATIONS
    time_steps: int = DEFAULT_LOG_TIME_STEPS
    time_skew: int = DEFAULT_LOG_TIME_SKEW
    mode: str = "generic"  # 'continuous' or 'generic'


def inject_logs_continuous(
    kafka_broker: str,
    kafka_user: str,
    kafka_pwd: str,
    kafka_topic: str,
    kafka_cert: str,
    time_format: str,
    logs_data: str,
    iterations: int = DEFAULT_LOG_ITERATIONS,
    time_skew: int = DEFAULT_LOG_TIME_SKEW,
    scenario_name: str = "continuous",
) -> str:
    """
    Inject logs with a continuous (current-time) timestamp.

    Each log line receives the current timestamp + skew, so repeated
    injections produce logs with the same approximate time.

    Args:
        kafka_broker: Kafka broker address.
        kafka_user: Kafka SASL username.
        kafka_pwd: Kafka SASL password.
        kafka_topic: Target Kafka topic.
        kafka_cert: CA certificate content.
        time_format: Python strftime format for timestamps.
        logs_data: Newline-separated log templates.
        iterations: Number of injection iterations.
        time_skew: Minutes to add to each timestamp.
        scenario_name: Human-readable scenario identifier.

    Returns:
        'OK' on success.
    """
    logger.info("START - Inject Logs CONT - %s", scenario_name)

    _write_cert(kafka_cert)
    conf = _build_kafka_conf(kafka_broker, kafka_user, kafka_pwd)
    producer = Producer(conf)

    for i in range(1, iterations + 1):
        for line in logs_data.split("\n"):
            line = line.strip()
            if not line:
                continue

            timestamp = datetime.datetime.now() + datetime.timedelta(minutes=time_skew)
            timestampstr = timestamp.strftime(time_format) + "+00:00"
            line = line.replace("MY_TIMESTAMP", timestampstr)
            producer.produce(kafka_topic, value=line)

        producer.flush()
        logger.info("Logs-Injection iteration %d: %s", i, timestamp)

    logger.info("END - Inject Logs - %s", scenario_name)
    return "OK"


def inject_logs_generic(
    kafka_broker: str,
    kafka_user: str,
    kafka_pwd: str,
    kafka_topic: str,
    kafka_cert: str,
    time_format: str,
    logs_data: str,
    iterations: int = DEFAULT_LOG_ITERATIONS,
    time_steps: int = DEFAULT_LOG_TIME_STEPS,
    time_skew: int = DEFAULT_LOG_TIME_SKEW,
    scenario_name: str = "generic",
) -> str:
    """
    Inject logs with progressive timestamps.

    Each log line receives an incrementing timestamp, so the output
    spans a time range proportional to iterations * time_steps.

    Args:
        kafka_broker: Kafka broker address.
        kafka_user: Kafka SASL username.
        kafka_pwd: Kafka SASL password.
        kafka_topic: Target Kafka topic.
        kafka_cert: CA certificate content.
        time_format: Python strftime format for timestamps.
        logs_data: Newline-separated log templates.
        iterations: Number of injection iterations.
        time_steps: Milliseconds to advance between log lines.
        time_skew: Initial minutes to add to the base timestamp.
        scenario_name: Human-readable scenario identifier.

    Returns:
        'OK' on success.
    """
    logger.info("START - Inject Logs - %s", scenario_name)

    _write_cert(kafka_cert)
    conf = _build_kafka_conf(kafka_broker, kafka_user, kafka_pwd)
    producer = Producer(conf)

    timestamp = datetime.datetime.now()
    logger.info("Base timestamp: %s", timestamp)
    timestamp = timestamp + datetime.timedelta(minutes=time_skew)

    for i in range(1, iterations + 1):
        for line in logs_data.split("\n"):
            line = line.strip()
            if not line:
                continue

            timestamp = timestamp + datetime.timedelta(milliseconds=time_steps)
            epoch = int(timestamp.timestamp())
            timestampstr = timestamp.strftime(time_format) + "+00:00"
            epochstr = str(epoch) + "000"
            line = line.replace("MY_TIMESTAMP", timestampstr)
            line = line.replace("MY_EPOCH", epochstr)
            producer.produce(kafka_topic, value=line)

        producer.flush()
        logger.info("Logs-Injection iteration %d: %s", i, timestamp)

    logger.info("END - Inject Logs - %s", scenario_name)
    return "OK"


def _write_cert(kafka_cert: str) -> None:
    """Write the Kafka CA certificate to a temporary file."""
    stream = capture_shell(f'echo "{kafka_cert}" > ./demouiapp/ca.crt')
    stream.read().strip()


def _build_kafka_conf(
    broker: str,
    user: str,
    pwd: str,
) -> dict:
    """
    Build the Kafka producer configuration dictionary.

    Args:
        broker: Kafka broker address.
        user: SASL username.
        pwd: SASL password.

    Returns:
        Configuration dict for confluent_kafka.Producer.
    """
    return {
        "bootstrap.servers": broker,
        "security.protocol": KAFKA_SECURITY_PROTOCOL,
        "sasl.mechanisms": KAFKA_SASL_MECHANISM,
        "sasl.username": user,
        "sasl.password": pwd,
        "client.id": socket.gethostname(),
        "enable.ssl.certificate.verification": "false",
        "ssl.ca.location": "./demouiapp/ca.crt",
    }
