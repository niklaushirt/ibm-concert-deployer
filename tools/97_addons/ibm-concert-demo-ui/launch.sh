#!/usr/bin/env bash

# export AIOPS_URL_OVERRIDE='testaiops'
# export ROBOTSHOP_URL_OVERRIDE='testrobot'
# export SOCKSHOP_URL_OVERRIDE='testsock'
# export AWX_URL_OVERRIDE='testawx'
export CONTACT_INFO='<p style="font-size:40px;">Contacts</p><BR><p>Niklaus Hirt - nikh@ch.ibm.com</p><p></p>'

# export KAFKA_BROKER_OVERRIDE='iaf-system-kafka-0.ibm-aiops:9094'
# export DATALAYER_ROUTE_OVERRIDE="aiops-ir-core-ncodl-api.ibm-aiops:10011"
# export METRIC_ROUTE_OVERRIDE="ibm-nginx-svc.ibm-aiops:443"


export DEMO_PWD=changeme
export DEMO_USER=demo
export ADMIN_MODE='true'
export INSTANCE_NAME=Nick
export TOKEN=test
export DJANGO_DEBUG=true
export DJANGO_SECRET_KEY="${DJANGO_SECRET_KEY:-$(python3 -c 'import secrets; print(secrets.token_urlsafe(64))')}"

export ENV_CMD="
    export OCP_URL=\$(oc get Infrastructure cluster -o jsonpath={.status.apiServerURL})
    export OCP_TOKEN=\$(oc create token -n ibm-installer ibm-installer-admin --duration=999999999s)

    echo \"------------------------------------------------------------------------------------------------------------------------------<BR>\"
    echo \" ✅ LOGINS FOR RESILIENCE<BR>\"
    echo \"------------------------------------------------------------------------------------------------------------------------------<BR>\"
    export API_TOKEN=\$(oc create token -n default demo-admin-concert --duration=999999999s)

    export CONSOLE_PATH=\$(oc get route -n openshift-console console -o jsonpath={.spec.host})
    export CONSOLE_URL=\"https://\"\$CONSOLE_PATH
    export API_URL=\${CONSOLE_URL/console-openshift-console.apps/api}:6443

    echo \"<BR>\"
    echo \"  🌏 API URL  :   \$OCP_URL<BR>\"
    echo \"  🔐 API TOKEN:   \$OCP_TOKEN\"

    echo \"<BR>\"
    echo \"<BR>\"


 

    echo \"------------------------------------------------------------------------------------------------------------------------------<BR>\"
    echo \" ✅ CHECK WATSONX CREDENTIALS<BR>\"
    echo \"------------------------------------------------------------------------------------------------------------------------------<BR>\"
    CONCERT_NAMESPACE=\$(oc get po -A|grep roja-portal |awk '{print\$1}')

    API_KEY=\"\$(oc get secret app-cfg-secret -n \$CONCERT_NAMESPACE -o jsonpath='{ .data.WATSONX_API_KEY }' | base64 --decode)\"


    RESPONSE=\$(curl -s -X POST \
    https://iam.cloud.ibm.com/identity/token \
    -H \"Content-Type: application/x-www-form-urlencoded\" \
    -d \"grant_type=urn:ibm:params:oauth:grant-type:apikey&apikey=\$API_KEY\")

    #echo \"\$RESPONSE\" | jq

    if echo \"\$RESPONSE\" | jq -e '.errorMessage' > /dev/null 2>&1; then
    echo \"<BR>\"
    echo \"    🔴🔴🔴🔴🔴🔴 WATSONX TOKEN INVALID - Error returned from IAM. You won't be able to access the WatsonX services in Concert platform.<BR>\"
    echo \"\"
    exit 1
    else
    echo \"<BR>\"
    echo \"    ✅ Successfully retrieved IAM token. You can access the WatsonX services in Concert platform.<BR>\"
    echo \"<BR>\"
    fi


    echo \"------------------------------------------------------------------------------------------------------------------------------<BR>\"
    echo \" ✅ LDAP CREDENTIALS<BR>\"
    echo \"------------------------------------------------------------------------------------------------------------------------------<BR>\"

    echo \"id\": \"LDAP<BR>\"
    echo \"realm\": \"REALM<BR>\"
    echo \"url\": \"ldap://openldap.openldap:389<BR>\"
    echo \"host\": \"openldap.openldap<BR>\"
    echo \"port\": \"389<BR>\"
    echo \"protocol\": \"ldap<BR>\"
    echo \"basedn\": \"dc=ibm,dc=com<BR>\"
    echo \"binddn\": \"cn=admin,dc=ibm,dc=com<BR>\"
    echo \"bindpassword: The one you selected at installation time<BR>\"
    echo \"type\": \"Custom<BR>\"
    echo \"ignorecase\": \"false<BR>\"
    echo \"userfilter\": \"(&(uid=%v)(objectclass=Person))<BR>\"
    echo \"useridmap\": \"*:uid<BR>\"
    echo \"groupfilter\": \"(&(cn=%v)(objectclass=groupOfUniqueNames))<BR>\"
    echo \"groupidmap\": \"*:cn<BR>\"
    echo \"groupmemberidmap\": \"groupOfUniqueNames:uniqueMember<BR>\"
    echo \"nestedsearch\": \"false<BR>\"
    echo \"pagingsearch\": \"false<BR>\"
    export openldap_app_route=\$(oc get route -n openldap admin -o jsonpath={.spec.host})          
    echo \"openldap_app_route:     https://\$openldap_app_route<BR>\"


"

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/demoui"

export PYTHONUNBUFFERED=1

python3 -m venv venv

if ! venv/bin/python -m pip --version >/dev/null 2>&1; then
  venv/bin/python -m ensurepip --upgrade
fi

venv/bin/python -m pip install -r requirements.txt

exec venv/bin/python -m gunicorn demoui.wsgi:application \
  --bind 0.0.0.0:8000 \
  --workers 1 \
  --timeout 300 \
  --capture-output \
  --enable-stdio-inheritance \
  --log-level info \
  --access-logfile - \
  --error-logfile -
