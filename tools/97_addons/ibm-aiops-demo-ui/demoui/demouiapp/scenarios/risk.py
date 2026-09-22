"""
Risk proximity demo scenario for IBM AIOps DemoUI.

Triggers File Observer jobs to run network risk topology analysis.
This scenario is unique to functions.py and not present in functions_NG.py.
"""

import os

from ..utils import get_logger
from ..utils.commands import capture_shell

logger = get_logger("scenarios.risk")


class RiskScenario:
    """
    Risk proximity demo scenario controller.

    Triggers IBM AIOps File Observer jobs to analyze network risk
    topologies (US network risk and EU risk proximity).
    """

    def run_observers(self) -> str:
        """
        Execute the risk proximity File Observer jobs.

        This triggers two observer jobs:
        - us-network-risk-topology
        - risk-proximity-EU-topology

        Returns:
            'OK' on success.
        """
        logger.info("START - Inject Events - RISK by running File Observers")

        cmd = self._build_observer_command()

        try:
            stream = capture_shell(cmd)
            output = stream.read().strip()
            logger.info("Risk observer output: %s", output)
        except Exception as e:
            logger.error("Risk observer execution failed: %s", e)

        logger.info("END - Inject Events - RISK")
        return "OK"

    def _build_observer_command(self) -> str:
        """
        Build the shell command to trigger File Observer jobs.

        Returns:
            Shell command string.
        """
        return """
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
