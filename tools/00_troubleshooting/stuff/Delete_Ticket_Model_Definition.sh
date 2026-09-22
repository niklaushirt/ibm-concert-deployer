
export AIOPS_NAMESPACE=$(oc get po -A|grep aiops-orchestrator-controller |awk '{print$1}')
echo "       ✅ IBMAIOps:         OK - $AIOPS_NAMESPACE"

export ROUTE=$(oc get route -n $AIOPS_NAMESPACE cpd  -o jsonpath={.spec.host})
echo "       ✅ Route:            OK - $ROUTE"


echo "       🛠️   Getting ZEN Token"

ZEN_API_HOST=$(oc get route -n $AIOPS_NAMESPACE cpd -o jsonpath='{.spec.host}')
ZEN_LOGIN_URL="https://${ZEN_API_HOST}/v1/preauth/signin"
LOGIN_USER=admin
LOGIN_PASSWORD="$(oc get secret admin-user-details -n $AIOPS_NAMESPACE -o jsonpath='{ .data.initial_admin_password }' | base64 --decode)"

ZEN_LOGIN_RESPONSE=$(
curl -k \
-H 'Content-Type: application/json' \
-XPOST \
"${ZEN_LOGIN_URL}" \
-d '{
    "username": "'"${LOGIN_USER}"'",
    "password": "'"${LOGIN_PASSWORD}"'"
}' 2> /dev/null
)

ZEN_LOGIN_MESSAGE=$(echo "${ZEN_LOGIN_RESPONSE}" | jq -r .message)

if [ "${ZEN_LOGIN_MESSAGE}" != "success" ]; then
    echo "Login failed: ${ZEN_LOGIN_MESSAGE}"
    exit 2
fi

ZEN_TOKEN=$(echo "${ZEN_LOGIN_RESPONSE}" | jq -r .token)
#echo "${ZEN_TOKEN}"
echo "Sucessfully logged in" 
echo ""



curl "https://$ROUTE/aiops/aimodels/api/p/ai_platform_api" \
-X 'POST' \
-H 'Content-Type: application/json' \
-H 'Accept: */*' \
-H 'Sec-Fetch-Site: same-origin' \
-H 'Accept-Language: en-GB,en;q=0.9' \
-H "authorization: Bearer $ZEN_TOKEN"  \
--data-raw '{    "operationName": "deleteTrainingDefinition",    "variables": {        "definitionName": "ChangeRisk"    },   "query": "mutation deleteTrainingDefinition($definitionName: String!) {\n  deleteTrainingDefinition(\n    definitionName: $definitionName\n    ) {\n    status\n    message\n    __typename\n  }\n}"}'


curl "https://$ROUTE/aiops/aimodels/api/p/ai_platform_api" \
-X 'POST' \
-H 'Content-Type: application/json' \
-H 'Accept: */*' \
-H 'Sec-Fetch-Site: same-origin' \
-H 'Accept-Language: en-GB,en;q=0.9' \
-H "authorization: Bearer $ZEN_TOKEN"  \
--data-raw '{    "operationName": "deleteTrainingDefinition",    "variables": {        "definitionName": "SimilarIncidents"    },   "query": "mutation deleteTrainingDefinition($definitionName: String!) {\n  deleteTrainingDefinition(\n    definitionName: $definitionName\n    ) {\n    status\n    message\n    __typename\n  }\n}"}'




