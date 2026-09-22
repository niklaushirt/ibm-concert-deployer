"""
Event injector for IBM AIOps DemoUI.

Handles injection of events into the IBM AIOps Datalayer API.
Replaces the thin wrapper functions (injectEventsMemRobot, injectEventsNetRobot, etc.)
with a data-driven approach.
"""

import datetime
import os
from dataclasses import dataclass
from typing import Optional

import requests
from requests.auth import HTTPBasicAuth

from ..utils import DATALAYER_API_PATH, SUBSCRIPTION_ID, get_logger
from ..utils.commands import capture_shell
from ..utils.constants import DEFAULT_EVENTS_TIME_SKEW

logger = get_logger("injectors.event")


@dataclass
class EventConfig:
    """Configuration for a specific event injection scenario."""

    name: str
    events_data: str
    time_skew: int = DEFAULT_EVENTS_TIME_SKEW


def inject_events(
    datalayer_route: str,
    datalayer_user: str,
    datalayer_pwd: str,
    events_data: str,
    scenario_name: str = "generic",
    time_skew: int = DEFAULT_EVENTS_TIME_SKEW,
) -> str:
    """
    Inject events into the IBM AIOps Datalayer.

    Parses the events data (newline-separated JSON), replaces MY_TIMESTAMP
    placeholders, and POSTs each event to the datalayer API.

    Args:
        datalayer_route: Route to the IBM AIOps datalayer API.
        datalayer_user: Username for datalayer authentication.
        datalayer_pwd: Password for datalayer authentication.
        events_data: Newline-separated JSON event definitions.
        scenario_name: Human-readable scenario identifier for logging.
        time_skew: Seconds to add between each event's timestamp.

    Returns:
        'OK' on success.

    Raises:
        SystemExit: If the datalayer API connection fails.
    """
    logger.info("START - Inject Events - %s", scenario_name)

    url = f"https://{datalayer_route}{DATALAYER_API_PATH}/events"
    auth = HTTPBasicAuth(datalayer_user, datalayer_pwd)
    headers = {
        "Content-Type": "application/json",
        "Accept-Charset": "UTF-8",
        "x-username": "admin",
        "x-subscription-id": SUBSCRIPTION_ID,
    }

    timestamp = datetime.datetime.now()

    for line in events_data.split("\n"):
        line = line.strip()
        if not line:
            continue

        timestamp = timestamp + datetime.timedelta(seconds=time_skew)
        timestampstr = timestamp.strftime("%Y-%m-%dT%H:%M:%S.000Z")
        line = line.replace("MY_TIMESTAMP", timestampstr)

        try:
            response = requests.post(
                url, data=line, headers=headers, auth=auth, verify=False
            )
            logger.info("Events-Injection response: %s", response.content)
        except requests.exceptions.RequestException as e:
            _log_datalayer_route_hint()
            raise SystemExit(e)

    logger.info("END - Inject Events - %s", scenario_name)
    return "OK"


def inject_events_repeated(
    datalayer_route: str,
    datalayer_user: str,
    datalayer_pwd: str,
    events_data: str,
    scenario_name: str = "repeated",
    repetitions: int = 10,
    time_skew: int = DEFAULT_EVENTS_TIME_SKEW,
) -> str:
    """
    Inject the same set of events multiple times.

    Used by the 'BUSY' scenario to simulate high event volume.

    Args:
        datalayer_route: Route to the IBM AIOps datalayer API.
        datalayer_user: Username for datalayer authentication.
        datalayer_pwd: Password for datalayer authentication.
        events_data: Newline-separated JSON event definitions.
        scenario_name: Human-readable scenario identifier for logging.
        repetitions: Number of times to repeat the injection.
        time_skew: Seconds to add between each event's timestamp.

    Returns:
        'OK' on success.
    """
    for i in range(repetitions):
        logger.info("Repetition %d/%d - %s", i + 1, repetitions, scenario_name)
        inject_events(
            datalayer_route=datalayer_route,
            datalayer_user=datalayer_user,
            datalayer_pwd=datalayer_pwd,
            events_data=events_data,
            scenario_name=scenario_name,
            time_skew=time_skew,
        )
    return "OK"


def _log_datalayer_route_hint() -> None:
    """Log a hint about using the public datalayer route."""
    try:
        stream = capture_shell(
            "oc get route -n "
            + _get_aiops_namespace()
            + " datalayer-api -o jsonpath='{.status.ingress[0].host}'"
        )
        route = stream.read().strip()
        logger.warning("YOU MIGHT WANT TO USE THE DATALAYER PUBLIC ROUTE: %s", route)
    except Exception:
        pass


def _get_aiops_namespace() -> str:
    """Retrieve the IBM AIOps namespace from the cluster."""
    stream = capture_shell(
        "oc get po -A | grep aiops-orchestrator-controller | awk '{print $1}'"
    )
    return stream.read().strip()
