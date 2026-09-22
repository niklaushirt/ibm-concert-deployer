"""
Metric injector for IBM AIOps DemoUI.

Handles injection of simulated metrics into the IBM AIOps Metrics API.
Supports CSV-formatted metric definitions with configurable variation.
"""

import datetime
import json
import os
import random
from dataclasses import dataclass
from typing import List, Optional

import requests

from ..utils import METRICS_API_PATH, SUBSCRIPTION_ID, get_logger
from ..utils.commands import capture_shell
from ..utils.constants import (
    DEFAULT_METRIC_BATCH_SIZE,
    DEFAULT_METRIC_ITERATIONS,
)

logger = get_logger("injectors.metric")


@dataclass
class MetricDefinition:
    """Parsed metric definition from CSV line."""

    resource_name: str
    metric_name: str
    group_id: str
    fix_value: str
    variation: str


def parse_metric_line(line: str) -> MetricDefinition:
    """
    Parse a CSV metric definition line.

    Expected format: resource_name,metric_name,group_id,fix_value,variation

    Args:
        line: CSV-formatted metric definition.

    Returns:
        Parsed MetricDefinition.
    """
    elements = line.strip().split(",")
    return MetricDefinition(
        resource_name=elements[0],
        metric_name=elements[1],
        group_id=elements[2],
        fix_value=elements[3],
        variation=elements[4],
    )


def inject_metrics(
    metric_route: str,
    metric_token: str,
    metrics_to_simulate: List[str],
    time_skew: int,
    time_step: int,
    scenario_name: str = "generic",
    iterations: Optional[int] = None,
) -> str:
    """
    Inject simulated metrics into the IBM AIOps Metrics API.

    Generates metric batches by iterating through the definitions,
    adding random variation to values, and POSTing to the metrics endpoint.

    Args:
        metric_route: Route to the IBM AIOps metrics API.
        metric_token: Bearer token for metrics authentication.
        metrics_to_simulate: List of CSV metric definitions.
        time_skew: Initial seconds to add to the base timestamp.
        time_step: Milliseconds to advance between metric points.
        scenario_name: Human-readable scenario identifier.
        iterations: Number of injection iterations (default from constants).

    Returns:
        'OK' on success.

    Raises:
        SystemExit: If the metrics API connection fails.
    """
    if iterations is None:
        iterations = DEFAULT_METRIC_ITERATIONS

    logger.info("START - Inject Metrics - %s", scenario_name)
    logger.info("METRICS_TO_SIMULATE: %s", metrics_to_simulate)
    logger.info("#METRICS_TO_SIMULATE: %d", len(metrics_to_simulate))

    # Resolve route and token from cluster if needed
    metric_route = _resolve_metric_route(metric_route)
    metric_token = _resolve_metric_token(metric_route)

    timestamp = datetime.datetime.now() + datetime.timedelta(seconds=time_skew)
    url = f"https://{metric_route}{METRICS_API_PATH}"
    headers = {
        "Content-Type": "application/json",
        "Accept-Charset": "UTF-8",
        "Authorization": f"Bearer {metric_token}",
        "X-TenantID": SUBSCRIPTION_ID,
    }

    curr_iterations = 0

    for i in range(1, iterations + 1):
        output_json = '{"groups":['
        curr_iterations += 1

        for _batch in range(1, DEFAULT_METRIC_BATCH_SIZE + 1):
            for line in metrics_to_simulate:
                line = line.strip()
                if not line:
                    continue

                timestamp = timestamp + datetime.timedelta(milliseconds=time_step)
                my_timestamp = timestamp.strftime("%s") + "000"
                my_timestamp_readable = timestamp.strftime("%Y-%m-%dT%H:%M:%S.000Z")

                md = parse_metric_line(line)
                current_value = _compute_value(
                    md.fix_value, md.variation, curr_iterations
                )

                current_line = json.dumps(
                    {
                        "timestamp": my_timestamp,
                        "resourceID": md.resource_name,
                        "metrics": {md.metric_name: current_value},
                        "attributes": {
                            "group": md.group_id,
                            "node": md.resource_name,
                        },
                    }
                )
                output_json = output_json + current_line + ","

        # Remove trailing comma and close JSON
        output_json = output_json.rstrip(",") + "]}"

        try:
            response = requests.post(
                url, data=output_json, headers=headers, verify=False
            )
        except requests.exceptions.RequestException as e:
            _log_metric_route_hint()
            raise SystemExit(e)

        logger.info(
            "Metrics-Injection: %s - %s - %s",
            scenario_name,
            my_timestamp_readable,
            response.content,
        )

    logger.info("END - Inject Metrics - %s", scenario_name)
    return "OK"


def _compute_value(fix_value: str, variation: str, iteration: int) -> int:
    """
    Compute the metric value based on fix_value and variation.

    If fix_value is 'ITERATIONS', the value increases linearly.
    Otherwise, a random value within [fix_value, fix_value + variation] is used.

    Args:
        fix_value: Base value or 'ITERATIONS'.
        variation: Range for randomization or increment for iterations.
        iteration: Current iteration number.

    Returns:
        Computed metric value.
    """
    if fix_value == "ITERATIONS":
        return int(variation) + 2 * int(iteration)
    return random.randint(int(fix_value), int(fix_value) + int(variation))


def _resolve_metric_route(route: str) -> str:
    """Resolve the metrics route from the cluster, with env override."""
    stream = capture_shell(
        "oc get po -A | grep aiops-orchestrator-controller | awk '{print $1}'"
    )
    ns = stream.read().strip()

    stream = capture_shell(f"oc get route -n {ns} | grep ibm-nginx-svc | awk '{{print $2}}'")
    resolved = stream.read().strip()
    return os.environ.get("METRIC_ROUTE_OVERRIDE", resolved)


def _resolve_metric_token(route: str) -> str:
    """
    Resolve the metrics API token via the cluster auth flow.

    This performs the full OAuth + preauth validation sequence.

    Args:
        route: Metrics API route.

    Returns:
        Valid bearer token.
    """
    stream = capture_shell(
        "oc get po -A | grep aiops-orchestrator-controller | awk '{print $1}'"
    )
    ns = stream.read().strip()

    stream = capture_shell(f"oc get route -n {ns} cp-console -o jsonpath={{.spec.host}}")
    console_route = stream.read().strip()

    stream = capture_shell(
        f"oc get secret -n {ns} platform-auth-idp-credentials "
        f"-o jsonpath='{{.data.admin_username}}' | base64 --decode"
    )
    user = stream.read().strip()

    stream = capture_shell(
        f"oc get secret -n {ns} platform-auth-idp-credentials "
        f"-o jsonpath='{{.data.admin_password}}' | base64 --decode"
    )
    pwd = stream.read().strip()

    stream = capture_shell(
        f'curl -s -k -H "Content-Type: application/x-www-form-urlencoded;charset=UTF-8" '
        f'-d "grant_type=password&username={user}&password={pwd}&scope=openid" '
        f"https://{console_route}/idprovider/v1/auth/identitytoken|jq -r '.access_token' "
    )
    access_token = stream.read().strip()

    stream = capture_shell(
        f"curl -s -k -XGET https://{route}/v1/preauth/validateAuth "
        f'-H "username: {user}" -H "iam-token: {access_token}"|jq -r ".accessToken"'
    )
    return stream.read().strip()


def _log_metric_route_hint() -> None:
    """Log a hint about using the public metrics route."""
    try:
        stream = capture_shell(
            "oc get po -A | grep aiops-orchestrator-controller | awk '{print $1}'"
        )
        ns = stream.read().strip()
        stream = capture_shell(
            f"oc get route -n {ns} | grep ibm-nginx-svc | awk '{{print $2}}'"
        )
        logger.warning(
            "YOU MIGHT WANT TO USE THE METRIC PUBLIC ROUTE: %s", stream.read().strip()
        )
    except Exception:
        pass
