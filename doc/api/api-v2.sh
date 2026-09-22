# DEMO

export AIOPS_NAMESPACE=$(oc get po -A|grep aiops-orchestrator-controller |awk '{print$1}')
export CONSOLE_ROUTE=$(oc get route -n $AIOPS_NAMESPACE cp-console  -o jsonpath={.spec.host})          
export CPD_ROUTE=$(oc get route -n $AIOPS_NAMESPACE cpd  -o jsonpath={.spec.host})          
export CPADMIN_PWD=$(oc get secret -n $AIOPS_NAMESPACE platform-auth-idp-credentials -o jsonpath='{.data.admin_password}' | base64 --decode)
export CPADMIN_USER=$(oc get secret -n $AIOPS_NAMESPACE platform-auth-idp-credentials -o jsonpath='{.data.admin_username}' | base64 --decode)
echo "CONSOLE_ROUTE: "$CONSOLE_ROUTE
echo "CPD_ROUTE: "$CPD_ROUTE
echo "CPADMIN_USER: "$CPADMIN_USER
echo "CPADMIN_PWD: "$CPADMIN_PWD    

export ACCESS_TOKEN=$(curl -s -k -H "Content-Type: application/x-www-form-urlencoded;charset=UTF-8" -d "grant_type=password&username=$CPADMIN_USER&password=$CPADMIN_PWD&scope=openid" https://$CONSOLE_ROUTE/idprovider/v1/auth/identitytoken|jq -r '.access_token')
export ZEN_API_HOST=$(oc get route -n $AIOPS_NAMESPACE cpd -o jsonpath='{.spec.host}')
export ZEN_TOKEN=$(curl -k -XGET https://$ZEN_API_HOST/v1/preauth/validateAuth \
-H "username: $CPADMIN_USER" \
-H "iam-token: $ACCESS_TOKEN"|jq -r '.accessToken')
echo $ZEN_TOKEN






# CPADMIN

export AIOPS_NAMESPACE=$(oc get po -A|grep aiops-orchestrator-controller |awk '{print$1}')
export CONSOLE_ROUTE=$(oc get route -n $AIOPS_NAMESPACE cp-console  -o jsonpath={.spec.host})          
export CPD_ROUTE=$(oc get route -n $AIOPS_NAMESPACE cpd  -o jsonpath={.spec.host})          
export CPADMIN_PWD=$(oc get secret -n $AIOPS_NAMESPACE platform-auth-idp-credentials -o jsonpath='{.data.admin_password}' | base64 --decode)
export CPADMIN_USER=$(oc get secret -n $AIOPS_NAMESPACE platform-auth-idp-credentials -o jsonpath='{.data.admin_username}' | base64 --decode)
echo "CONSOLE_ROUTE: "$CONSOLE_ROUTE
echo "CPD_ROUTE: "$CPD_ROUTE
echo "CPADMIN_USER: "$CPADMIN_USER
echo "CPADMIN_PWD: "$CPADMIN_PWD    

export ACCESS_TOKEN=$(curl -s -k -H "Content-Type: application/x-www-form-urlencoded;charset=UTF-8" -d "grant_type=password&username=$CPADMIN_USER&password=$CPADMIN_PWD&scope=openid" https://$CONSOLE_ROUTE/idprovider/v1/auth/identitytoken|jq -r '.access_token')
export ZEN_API_HOST=$(oc get route -n $AIOPS_NAMESPACE cpd -o jsonpath='{.spec.host}')
export ZEN_TOKEN=$(curl -k -XGET https://$ZEN_API_HOST/v1/preauth/validateAuth \
-H "username: $CPADMIN_USER" \
-H "iam-token: $ACCESS_TOKEN"|jq -r '.accessToken')
echo $ZEN_TOKEN



export values=$(curl -k -X GET  --header 'Accept: application/json' -H "Authorization: Bearer ${ZEN_TOKEN}" https://$CPD_ROUTE/aiops/api/v2/alerts -H "accept: application/json" -H "Content-Type: application/json" -H "X-TenantID: cfd95b7e-3bc7-4006-a4a8-a73a79c71255" )
echo $values| jq


export values=$(curl -k -X GET  --header 'Accept: application/json' -H "Authorization: Bearer ${ZEN_TOKEN}" https://$CPD_ROUTE/aiops/api/v2/incidents/ -H "accept: application/json" -H "Content-Type: application/json" -H "X-TenantID: cfd95b7e-3bc7-4006-a4a8-a73a79c71255" )
echo $values| jq

export values=$(curl -k -X GET  --header 'Accept: application/json' -H "Authorization: Bearer ${ZEN_TOKEN}" https://$CPD_ROUTE/aiops/api/v2/configuration/policies -H "accept: application/json" -H "Content-Type: application/json" -H "X-TenantID: cfd95b7e-3bc7-4006-a4a8-a73a79c71255" | jq)
echo $values| jq

export values=$(curl -k -X GET  --header 'Accept: application/json' -H "Authorization: Bearer ${ZEN_TOKEN}" https://$CPD_ROUTE/aiops/api/v2/configuration/filters -H "accept: application/json" -H "Content-Type: application/json" -H "X-TenantID: cfd95b7e-3bc7-4006-a4a8-a73a79c71255" )
echo $values| jq

export values=$(curl -k -X GET  --header 'Accept: application/json' -H "Authorization: Bearer ${ZEN_TOKEN}" https://$CPD_ROUTE/aiops/api/v2/configuration/views -H "accept: application/json" -H "Content-Type: application/json" -H "X-TenantID: cfd95b7e-3bc7-4006-a4a8-a73a79c71255" )
echo $values| jq

export values=$(curl -k -X GET  --header 'Accept: application/json' -H "Authorization: Bearer ${ZEN_TOKEN}" https://$CPD_ROUTE/aiops/api/v2/configuration/menus -H "accept: application/json" -H "Content-Type: application/json" -H "X-TenantID: cfd95b7e-3bc7-4006-a4a8-a73a79c71255" )
echo $values| jq

export values=$(curl -k -X GET  --header 'Accept: application/json' -H "Authorization: Bearer ${ZEN_TOKEN}" https://$CPD_ROUTE/aiops/api/v2/configuration/tools -H "accept: application/json" -H "Content-Type: application/json" -H "X-TenantID: cfd95b7e-3bc7-4006-a4a8-a73a79c71255" )
echo $values| jq

export values=$(curl -k -X GET  --header 'Accept: application/json' -H "Authorization: Bearer ${ZEN_TOKEN}" https://$CPD_ROUTE/aiops/api/v2/configuration/runbooks -H "accept: application/json" -H "Content-Type: application/json" -H "X-TenantID: cfd95b7e-3bc7-4006-a4a8-a73a79c71255" )
echo $values| jq

export values=$(curl -k -X GET  --header 'Accept: application/json' -H "Authorization: Bearer ${ZEN_TOKEN}" https://$CPD_ROUTE/aiops/api/v2/configuration/user-preferences -H "accept: application/json" -H "Content-Type: application/json" -H "X-TenantID: cfd95b7e-3bc7-4006-a4a8-a73a79c71255" )
echo $values| jq

export values=$(curl -k -X GET  --header 'Accept: application/json' -H "Authorization: Bearer ${ZEN_TOKEN}" https://$CPD_ROUTE/aiops/api/v2/configuration/user-preferences/_self -H "accept: application/json" -H "Content-Type: application/json" -H "X-TenantID: cfd95b7e-3bc7-4006-a4a8-a73a79c71255" )
echo $values| jq 


export values=$(curl -k -X GET  --header 'Accept: application/json' -H "Authorization: Bearer ${ZEN_TOKEN}" https://$CPD_ROUTE/aiops/api/v2/configuration/policies -H "accept: application/json" -H "Content-Type: application/json" -H "X-TenantID: cfd95b7e-3bc7-4006-a4a8-a73a79c71255" | jq)
echo $values| jq



export values=$(curl -k -X GET  --header 'Accept: application/json' -H "Authorization: Bearer ${ZEN_TOKEN}" https://$CPD_ROUTE/aiops/api/v2/configuration/views -H "accept: application/json" -H "Content-Type: application/json" -H "X-TenantID: cfd95b7e-3bc7-4006-a4a8-a73a79c71255" )
echo $values|jq -r -c '.views[]| select( .name == "DEMO Incidents View")|.id'

export values=$(curl -k -X GET  --header 'Accept: application/json' -H "Authorization: Bearer ${ZEN_TOKEN}" https://$CPD_ROUTE/aiops/api/v2/configuration/user-preferences -H "accept: application/json" -H "Content-Type: application/json" -H "X-TenantID: cfd95b7e-3bc7-4006-a4a8-a73a79c71255" )
echo $values| jq


  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   198  100   198    0     0    405      0 --:--:-- --:--:-- --:--:--   405
{
  "preferences": [
    {
      "defaultView": "bf812cff-4961-4dfd-b832-4b947241366a",
      "rowColorToggle": true,
      "defaultIncidentAlertView": "bf812cff-4961-4dfd-b832-4b947241366a",
      "ael_user_properties_refresh_time": 60
    }
  ]
}



echo $values|jq -c '.results[]| select( .name == "IBM AIOPS Execution Environment")|.id'



export values=$(curl -k -X GET  --header 'Accept: application/json' -H "Authorization: Bearer ${ZEN_TOKEN}" https://$CPD_ROUTE/aiops/api/v2/metering/stats/resources -H "accept: application/json" -H "Content-Type: application/json" -H "X-TenantID: cfd95b7e-3bc7-4006-a4a8-a73a79c71255" | jq)
echo $values| jq

export values=$(curl -k -X GET  --header 'Accept: application/json' -H "Authorization: Bearer ${ZEN_TOKEN}" https://$CPD_ROUTE/aiops/api/v2/metering/resources&start_date=aaaa&end_date=bbbb -H "accept: application/json" -H "Content-Type: application/json" -H "X-TenantID: cfd95b7e-3bc7-4006-a4a8-a73a79c71255" | jq)
echo $values| jq



export values=$(curl -k -X GET  --header 'Accept: application/json' -H "Authorization: Bearer ${ZEN_TOKEN}" https://$CPD_ROUTE/aiops/api/v2/configuration/algorithms -H "accept: application/json" -H "Content-Type: application/json" -H "X-TenantID: cfd95b7e-3bc7-4006-a4a8-a73a79c71255" )
echo $values| jq

export values=$(curl -k -X GET  --header 'Accept: application/json' -H "Authorization: Bearer ${ZEN_TOKEN}" https://$CPD_ROUTE/aiops/api/v2/configuration/training-definitions -H "accept: application/json" -H "Content-Type: application/json" -H "X-TenantID: cfd95b7e-3bc7-4006-a4a8-a73a79c71255" )
echo $values| jq







export result=$(curl -k -X GET  https://$CPD_ROUTE/aiops/api/v2/configuration/policies \
    -H 'Accept: application/json' \
    -H "Authorization: Bearer ${ZEN_TOKEN}" \
    -H "accept: application/json" \
    -H "Content-Type: application/json" \
    -H "X-TenantID: cfd95b7e-3bc7-4006-a4a8-a73a79c71255"|grep "DEMO Incident - robot-shop"|wc -l|tr -d ' ')
echo $result


  export result=$(curl -XGET -k -s "https://$POLICY_ROUTE/policyregistry.ibm-netcool-prod.aiops.io/v1alpha/system/cfd95b7e-3bc7-4006-a4a8-a73a79c71255/"  \
      -H 'X-TenantID: cfd95b7e-3bc7-4006-a4a8-a73a79c71255' \
      -H 'content-type: application/json' \
      -u $POLICY_LOGIN|grep "DEMO Incident - robot-shop"|wc -l|tr -d ' ')







export values=$(curl -k -X GET  --header 'Accept: application/json' -H "Authorization: Bearer ${ZEN_TOKEN}" https://$CPD_ROUTE/aiops/api/v2/configuration/topology/config/backup -H "accept: application/json" -H "Content-Type: application/json" -H "X-TenantID: cfd95b7e-3bc7-4006-a4a8-a73a79c71255" | jq)
echo $values| jq






export AIOPS_NAMESPACE=$(oc get po -A|grep aiops-orchestrator-controller |awk '{print$1}')
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

ZEN_TOKEN=$(echo "${ZEN_LOGIN_RESPONSE}" | jq -r .token)
echo $ZEN_TOKEN

export ROUTE=$(oc get route -n $AIOPS_NAMESPACE cpd -o jsonpath={.spec.host})
echo "ROUTE: "$ROUTE



curl -k -X GET  --header 'Accept: application/json' -H "Authorization: Bearer ${ZEN_TOKEN}" https://$ROUTE/aiops/api/v2/alerts -H "accept: application/json" -H "Content-Type: application/json" -H "X-TenantID: cfd95b7e-3bc7-4006-a4a8-a73a79c71255" | jq)
    echo $values




    export values=$(curl -k -X GET  --header 'Accept: application/json' -H "Authorization: Bearer ${ZEN_TOKEN}" https://$ROUTE/aiops/api/v2/configuration/user-preferences/_self -H "accept: application/json" -H "Content-Type: application/json" -H "X-TenantID: cfd95b7e-3bc7-4006-a4a8-a73a79c71255" | jq '.preferences[] | select(.key == "alertList") | .value')
    echo $values
    export newvalues=$(echo $values | sed -e "s/false/true/g")
    echo $newvalues
    if [[ $existing == "" ]]; then
        export payload='{"value": { "rowColorToggle": true, "ael_user_properties_refresh_time": 60 }}'
    else
        export payload='{"value": '"$newvalues"'}'
    fi  
    echo $payload   


    curl -X 'PUT' \
      "https://$ROUTE/aiops/api/v2/configuration/user-preferences/_self/alertList" \
      -H 'accept: application/json' \
      -H 'x-tenant-id: cfd95b7e-3bc7-4006-a4a8-a73a79c71255' \
      -H "Authorization: Bearer ${ZEN_TOKEN}" \
      -H 'Content-Type: application/json' \
      -d "$payload "











    export AIOPS_NAMESPACE=$(oc get po -A|grep aiops-orchestrator-controller |awk '{print$1}')
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

    ZEN_TOKEN=$(echo "${ZEN_LOGIN_RESPONSE}" | jq -r .token)
    echo $ZEN_TOKEN

    export ROUTE=$(oc get route -n $AIOPS_NAMESPACE cpd -o jsonpath={.spec.host})
    echo "ROUTE: "$ROUTE



    curl "https://$ROUTE/aiops/api/v2/events" \
    -X 'GET' \
    -H "Authorization: bearer $ZEN_TOKEN" \
    -H 'Content-Type: application/json' \
    -H 'X-TenantID: cfd95b7e-3bc7-4006-a4a8-a73a79c71255' 







/aiops/api/issue-resolution/mime/v1/customisation/words


    curl "https://$ROUTE/aiops/api/issue-resolution/v1/alerts/" \
    -X 'GET' \
    -H "Authorization: Bearer $ZEN_TOKEN" \
    -H 'Content-Type: application/json' \
    -H 'X-TenantID: cfd95b7e-3bc7-4006-a4a8-a73a79c71255' 
    
    
    $ROUTE/aiops/api/issue-resolution/v1/alerts/
    
    \
    --data-raw '{"operationName":"createTrainingDefinition","variables":{"definitionName":"aiops_chat_assistant_configuration","description":"","algorithmName":"AIOps_Chat_Assistant","createdBy":" ","trainingSchedule":{"frequency":"manual","repeat":"daily","atTimeHour":0,"atTimeMinute":0,"timeRangeValidStart":null,"timeRangeValidEnd":null,"noEndDate":false},"promoteOption":"whenTrainingComplete","enableSelectiveTraining":false,"enableLADGoldenSignal":false,"integrationGenAI":"","enableGenAI":false,"dataSetIds":[]},"query":"mutation createTrainingDefinition($definitionName: String!, $description: String!, $algorithmName: String!, $createdBy: String, $trainingSchedule: TrainingScheduleInput!, $promoteOption: PromoteOption!, $enableSelectiveTraining: Boolean, $dataSetIds: [ID], $enableLADGoldenSignal: Boolean, $integrationGenAI: String, $enableGenAI: Boolean) {\n  createTrainingDefinition(\n    definitionName: $definitionName\n    description: $description\n    algorithmName: $algorithmName\n    createdBy: $createdBy\n    trainingSchedule: $trainingSchedule\n    promoteOption: $promoteOption\n    enableSelectiveTraining: $enableSelectiveTraining\n    dataSetIds: $dataSetIds\n    enableLADGoldenSignal: $enableLADGoldenSignal\n    integrationGenAI: $integrationGenAI\n    enableGenAI: $enableGenAI\n  ) {\n    status\n    message\n    __typename\n  }\n}"}'


curl "https://<Endpoint URL>" --header 'Content-Type: application/json' --header "Authorization: ZenApiKey <ZenApiKey>" --header 'X-TenantID: cfd95b7e-3bc7-4006-a4a8-a73a79c71255' --insecure

    curl "https://$ROUTE/aiops/aimodels/api/p/ai_platform_api" \
    -X 'POST' \
    -H "Authorization: bearer $ZEN_TOKEN" \
    -H 'Content-Type: application/json' \
    --data-raw '{"operationName":"createTrainingDefinition","variables":{"definitionName":"aiops_chat_assistant_configuration","description":"","algorithmName":"AIOps_Chat_Assistant","createdBy":" ","trainingSchedule":{"frequency":"manual","repeat":"daily","atTimeHour":0,"atTimeMinute":0,"timeRangeValidStart":null,"timeRangeValidEnd":null,"noEndDate":false},"promoteOption":"whenTrainingComplete","enableSelectiveTraining":false,"enableLADGoldenSignal":false,"integrationGenAI":"","enableGenAI":false,"dataSetIds":[]},"query":"mutation createTrainingDefinition($definitionName: String!, $description: String!, $algorithmName: String!, $createdBy: String, $trainingSchedule: TrainingScheduleInput!, $promoteOption: PromoteOption!, $enableSelectiveTraining: Boolean, $dataSetIds: [ID], $enableLADGoldenSignal: Boolean, $integrationGenAI: String, $enableGenAI: Boolean) {\n  createTrainingDefinition(\n    definitionName: $definitionName\n    description: $description\n    algorithmName: $algorithmName\n    createdBy: $createdBy\n    trainingSchedule: $trainingSchedule\n    promoteOption: $promoteOption\n    enableSelectiveTraining: $enableSelectiveTraining\n    dataSetIds: $dataSetIds\n    enableLADGoldenSignal: $enableLADGoldenSignal\n    integrationGenAI: $integrationGenAI\n    enableGenAI: $enableGenAI\n  ) {\n    status\n    message\n    __typename\n  }\n}"}'







# Put connection name from UI here
CONNECTION_NAME="impacty"

CONNECTION_ID=$(oc get connectorconfiguration "${CONNECTION_NAME}" -o jsonpath='{.spec.connectionID}')

# These are the client id and secret already mounted in the connector,
# which it uses today to authenticate with the bridge
# These are generated in connector-manager, so this could be enhanced to also create 
# a matching scoped zen user as below
CLIENT_ID=$(oc get secret -n $AIOPS_NAMESPACE connector-"${CONNECTION_ID}" -o jsonpath='{.data.client-id}' | base64 --decode)
CLIENT_SECRET=$(oc get secret -n $AIOPS_NAMESPACE connector-"${CONNECTION_ID}" -o jsonpath='{.data.client-secret}' | base64 --decode)

CLIENT_ID=$(oc get secret -n $AIOPS_NAMESPACE connector-"${CONNECTION_ID}" -o jsonpath='{.data.client-id}' | base64 --decode)
CLIENT_SECRET=$(oc get secret -n $AIOPS_NAMESPACE connector-"${CONNECTION_ID}" -o jsonpath='{.data.client-secret}' | base64 --decode)









CLIENT_ID=admin
CLIENT_SECRET="$(oc get secret admin-user-details -n $AIOPS_NAMESPACE -o jsonpath='{ .data.initial_admin_password }' | base64 --decode)"


IDP_URL="https://$(oc get route -n $AIOPS_NAMESPACE platform-id-provider -o jsonpath='{.spec.host}')/idprovider"
ZEN_URL="https://$(oc get route -n $AIOPS_NAMESPACE cpd -o jsonpath='{.spec.host}')"

ZEN_SERVICE_BROKER_SECRET="$(oc get secret -n $AIOPS_NAMESPACE zen-service-broker-secret -o jsonpath='{.data.token}' | base64 --decode)"

echo "CONNECTION_ID: ${CONNECTION_ID}"
echo "CLIENT_ID: ${CLIENT_ID}"
echo "CLIENT_SECRET: ${CLIENT_SECRET}"
echo "IDP_URL: ${IDP_URL}"
echo "ZEN_URL: ${ZEN_URL}"
echo "ZEN_SERVICE_BROKER_SECRET: ${ZEN_SERVICE_BROKER_SECRET}"


# Gets a CPFS IAM token using the connector's existing credentials
IAM_TOKEN=$(
  curl -k -X POST \
    -H 'Content-Type: application/x-www-form-urlencoded;charset=UTF-8' \
    -d "grant_type=cpclient_credentials&client_id=${CLIENT_ID}&client_secret=${CLIENT_SECRET}&scope=openid" \
    "${IDP_URL}/v1/auth/token" | \
      jq -r .access_token
)

echo "IAM_TOKEN: ${IAM_TOKEN}"

# Exchange the IAM token for a Zen token - this will have the permissions of
# the service user created above
ZEN_TOKEN=$(
  curl -k "${ZEN_URL}/v1/preauth/validateAuth" \
    -H "username: ${CLIENT_ID}" \
    -H "iam-token: ${IAM_TOKEN}" | \
      jq -r '.accessToken'
)

echo "ZEN_TOKEN: ${ZEN_TOKEN}"


# Can now just use that to access AIOps APIs until its expiry:
curl -k "${ZEN_URL}/aiops/api/v2/alerts" \
 -H "Accept: application/json" \
  -H "Authorization: Bearer ${ZEN_TOKEN}"

# Or exchange the token for a longer/shorter lived one (can also
# set lifetime to 0 to make it last indefinitely)
ZEN_TOKEN_FOR_24_HOURS=$(
  curl -k \
    -XPOST \
    -H 'Content-Type: application/json' \
    -H "Authorization: Bearer ${ZEN_TOKEN}" \
    -H 'lifetime: 24' \
    -H 'cache-control: no-cache' \
    "${ZEN_URL}/usermgmt/v1/usermgmt/getTimedToken" | \
      jq -r .accessToken
)

# Which can be used the same way:
curl -k "${ZEN_URL}/aiops/api/v2/alerts" \
 -H "Accept: application/json" \
  -H "Authorization: Bearer ${ZEN_TOKEN_FOR_24_HOURS}"

