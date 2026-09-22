
export AIOPS_NAMESPACE=$(oc get po -A|grep aiops-orchestrator-controller |awk '{print$1}')
export ROUTE=$(oc get route -n $AIOPS_NAMESPACE cpd  -o jsonpath={.spec.host})          

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
echo "Login failed: ${ZEN_LOGIN_MESSAGE}" 1>&2

exit 2
fi

ZEN_TOKEN=$(echo "${ZEN_LOGIN_RESPONSE}" | jq -r .token)
echo "${ZEN_TOKEN}"




export demoURL=$(oc get route -n $AIOPS_NAMESPACE-demo-ui ibm-concert-demo-ui  -o jsonpath={.spec.host})          
export ROWS=""

ROWS=$ROWS'{"drilldown_url":  "", "label": "❗ Caution ❗", "sub_text": "Just clicking below will create the incident"},'
ROWS=$ROWS'{"drilldown_url":  "https://'$demoURL'/injectRESTHeadless?app=robotshop", "label": "🧨 RobotShop - Memory Problem", "sub_text": ""},'
ROWS=$ROWS'{"drilldown_url":  "https://'$demoURL'/injectRESTHeadless?app=acme", "label": "✈️ ACME - Server Fan Outage", "sub_text": ""},'
ROWS=$ROWS'{"drilldown_url":  "https://'$demoURL'/injectRESTHeadless?app=tube", "label": "🔥 London Tube - Fire Alert", "sub_text": ""},'
ROWS=$ROWS'{"drilldown_url":  "https://'$demoURL'/injectRESTHeadless?app=busy", "label": "🎡 Simulate Busy Environment", "sub_text": ""}'

PAYLOAD='{ "permissions": ["administrator"],  "window_open_target": "_blank",  "order": 2, "title": "🔴 Create Application Incidents", "template_type": "text_list", "data": { "text_list_data": { "rows": [  '$ROWS'  ] } } } '
echo "PAYLOAD:"$PAYLOAD


export result=$(curl -X "PUT" -k "https://$ROUTE/zen-data/v1/custom_cards/aiopsincident" -H "Authorization: Bearer $ZEN_TOKEN" -H "Content-Type: application/json" -d "$PAYLOAD")
echo "      🔎 Result: "
echo "       "$result



export ROWS=""

ROWS=$ROWS'{"drilldown_url":  "", "label": "❗ Caution ❗", "sub_text": "Just clicking below will create the incident"},'
ROWS=$ROWS'{"drilldown_url":  "https://'$demoURL'/injectRESTHeadless?app=robotshopnet", "label": "🧨 RobotShop - Network Problem", "sub_text": ""},'
ROWS=$ROWS'{"drilldown_url":  "https://'$demoURL'/injectRESTHeadless?app=sockshop", "label": "🧦 SockShop - Network Problem", "sub_text": ""},'
ROWS=$ROWS'{"drilldown_url":  "https://'$demoURL'/injectRESTHeadless?app=telco", "label": "📵 Optical Network - Fiber Cut", "sub_text": ""}'

PAYLOAD='{ "permissions": ["administrator"],  "window_open_target": "_blank",  "order": 5, "title": "🔴 Create Network Incidents", "template_type": "text_list", "data": { "text_list_data": { "rows": [  '$ROWS'  ] } } } '
echo "PAYLOAD:"$PAYLOAD


export result=$(curl -X "PUT" -k "https://$ROUTE/zen-data/v1/custom_cards/aiopsnetincident" -H "Authorization: Bearer $ZEN_TOKEN" -H "Content-Type: application/json" -d "$PAYLOAD")
echo "      🔎 Result: "
echo "       "$result




export ROWS=""

ROWS=$ROWS'{"drilldown_url":  "", "label": "❗ Caution ❗", "sub_text": "Just clicking below will clear all incidents"},'
ROWS=$ROWS'{"drilldown_url":  "https://'$demoURL'/injectRESTHeadless?app=clean", "label": "✅ Clear all Incidents and Alerts", "sub_text": ""}'

PAYLOAD='{ "permissions": ["administrator"],  "window_open_target": "_blank",  "order": 4, "title": "✅ Clear all Incidents", "template_type": "text_list", "data": { "text_list_data": { "rows": [  '$ROWS'  ] } } } '
echo "PAYLOAD:"$PAYLOAD



export result=$(curl -X "PUT" -k "https://$ROUTE/zen-data/v1/custom_cards/aiopsincidentclear" -H "Authorization: Bearer $ZEN_TOKEN" -H "Content-Type: application/json" -d "$PAYLOAD")
echo "      🔎 Result: "
echo "       "$result




appURL=$(oc get routes -n robot-shop robotshop  -o jsonpath="{['spec']['host']}")
sockURL=$(oc get routes -n sock-shop front-end  -o jsonpath="{['spec']['host']}")
ldapURL=$(oc get route -n openldap admin -o jsonpath={.spec.host})
awxUrl=$(oc get route -n awx awx -o jsonpath={.spec.host})
awxPwd=$(oc -n awx get secret awx-admin-password -o jsonpath='{.data.password}' | base64 --decode && echo)



export ROWS=""

if [[ $appURL =~ "robot-shop" ]]; then
echo "RobotShop Present"
ROWS=$ROWS'{"drilldown_url":  "https://'$appURL'", "label": "→  RobotShop", "sub_text": " "},'
fi        
if [[ $sockURL =~ "sock-shop" ]]; then
echo "SockShop Present"
ROWS=$ROWS'{"drilldown_url":  "https://'$sockURL'", "label": "→  SockShop", "sub_text": " "},'
fi
if [[ $ldapURL =~ "openldap" ]]; then
echo "LDAP Present"
ROWS=$ROWS'{"drilldown_url":  "https://'$ldapURL'", "label": "→  LDAP", "sub_text": " "},'
ROWS=$ROWS'{"drilldown_url":  "", "label": " ", "sub_text": "User: cn=admin,dc=ibm,dc=com - Password: aaaaaa "},'
fi
if [[ $awxUrl =~ "awx" ]]; then
echo "AWX Present"
ROWS=$ROWS'{"drilldown_url":  "https://'$awxUrl'", "label": "→  Ansible Tower", "sub_text": " "},'
ROWS=$ROWS'{"drilldown_url":  "", "label": " ", "sub_text": "User: admin - Password: '$awxPwd' "},'
fi



ROWS=$ROWS'{"drilldown_url":  "", "label": "Select your app above.", "sub_text": ""}'


PAYLOAD='{ "permissions": ["administrator"], "window_open_target": "_blank", "order": 3, "title": "🔵   Demo Apps", "template_type": "text_list", "data": { "text_list_data": { "rows": [ '$ROWS' ] } }}'
echo "PAYLOAD:"$PAYLOAD

curl -X "PUT" -k "https://$ROUTE/zen-data/v1/custom_cards/appscard" -H "Authorization: Bearer $ZEN_TOKEN" -H "Content-Type: application/json" -d "$PAYLOAD"

export result=$(curl -X "PUT" -k "https://$ROUTE/zen-data/v1/custom_cards/appscard" -H "Authorization: Bearer $ZEN_TOKEN" -H "Content-Type: application/json" -d "$PAYLOAD")
echo "      🔎 Result: "
echo "       "$result




