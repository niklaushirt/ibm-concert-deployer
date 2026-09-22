#!/bin/bash
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#     ________  __  ___   __________    ___         __                        __  _
#    /  _/ __ )/  |/  /  /  _/_  __/   /   | __  __/ /_____  ____ ___  ____ _/ /_(_)___  ____
#    / // __  / /|_/ /   / /  / /     / /| |/ / / / __/ __ \/ __ `__ \/ __ `/ __/ / __ \/ __ \
#  _/ // /_/ / /  / /  _/ /  / /     / ___ / /_/ / /_/ /_/ / / / / / / /_/ / /_/ / /_/ / / / /
# /___/_____/_/  /_/  /___/ /_/     /_/  |_\__,_/\__/\____/_/ /_/ /_/\__,_/\__/_/\____/_/ /_/
#
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------"
#  IBMAIOPS - Get Logins and URLs
#
#
#  ©2026 nikh@ch.ibm.com
# ---------------------------------------------------------------------------------------------------------------------------------------------------"
# ---------------------------------------------------------------------------------------------------------------------------------------------------"
# ---------------------------------------------------------------------------------------------------------------------------------------------------"
# ---------------------------------------------------------------------------------------------------------------------------------------------------"


echo "***************************************************************************************************************************************************"
echo "***************************************************************************************************************************************************"
echo "***************************************************************************************************************************************************"
echo "***************************************************************************************************************************************************"
echo ""
echo "       ________  __  ___     ___    ________       "
echo "      /  _/ __ )/  |/  /    /   |  /  _/ __ \____  _____"
echo "      / // __  / /|_/ /    / /| |  / // / / / __ \/ ___/"
echo "    _/ // /_/ / /  / /    / ___ |_/ // /_/ / /_/ (__  ) "
echo "   /___/_____/_/  /_/    /_/  |_/___/\____/ .___/____/  "
echo "                                         /_/"
echo ""

echo "  "
echo "  🚀 IBM AIOps - Logins and URLs"
echo "  "
echo "***************************************************************************************************************************************************"
echo "***************************************************************************************************************************************************"
echo "***************************************************************************************************************************************************"
echo "  "
echo "  "
export TEMP_PATH=~/aiops-install

# ---------------------------------------------------------------------------------------------------------------------------------------------------"
# ---------------------------------------------------------------------------------------------------------------------------------------------------"
# Do Not Edit Below
# ---------------------------------------------------------------------------------------------------------------------------------------------------"
# ---------------------------------------------------------------------------------------------------------------------------------------------------"



export AIOPS_NAMESPACE=$(oc get po -A|grep aiops-orchestrator-controller |awk '{print$1}')

: "${AIOPS_NAMESPACE:=ibm-aiops}"

CLUSTER_ROUTE=$(oc get routes console -n openshift-console | tail -n 1 2>&1 ) 
CLUSTER_FQDN=$( echo $CLUSTER_ROUTE | awk '{print $2}')
CLUSTER_NAME=${CLUSTER_FQDN##*console.}








echo "***************************************************************************************************************************************************"
echo "***************************************************************************************************************************************************"
echo "🚀 1. IBM AIOps"
echo "***************************************************************************************************************************************************"
echo "***************************************************************************************************************************************************"
echo "    "
DEMOUI_READY=$(oc get pod -n $AIOPS_NAMESPACE-demo-ui | grep 'demo-ui' || true) 
if [[ $DEMOUI_READY =~ "1/1" ]]; 
then

    echo "    -----------------------------------------------------------------------------------------------------------------------------------------------"
    echo "    -----------------------------------------------------------------------------------------------------------------------------------------------"
    echo "    🐣 1.1 Demo UI"
    echo "    -----------------------------------------------------------------------------------------------------------------------------------------------"
    echo "    -----------------------------------------------------------------------------------------------------------------------------------------------"
    echo "    "
    appURL=$(oc get routes -n $AIOPS_NAMESPACE-demo-ui ibm-aiops-demo-ui  -o jsonpath="{['spec']['host']}")|| true
    appToken=$(oc get cm -n $AIOPS_NAMESPACE-demo-ui ibm-aiops-demo-ui-config -o jsonpath='{.data.TOKEN}')
    echo "            🐣 Demo UI:"   
    echo "    " 
    echo "                🌏 URL:           https://$appURL/"
    echo "                🔐 Token:         $appToken"
    echo ""
    echo ""
fi

echo "    "
echo "    "
echo "    "
echo "    "
echo "    -----------------------------------------------------------------------------------------------------------------------------------------------"
echo "    -----------------------------------------------------------------------------------------------------------------------------------------------"
echo "    🚀 1.2 IBMAIOps"
echo "    -----------------------------------------------------------------------------------------------------------------------------------------------"
echo "    -----------------------------------------------------------------------------------------------------------------------------------------------"
echo "    "
echo "      📥 IBMAIOps"
echo ""
echo "                🌏 URL:           https://$(oc get route -n $AIOPS_NAMESPACE cpd -o jsonpath={.spec.host})"
echo ""    
echo "                🧑 User:          $(oc -n $AIOPS_NAMESPACE get secret platform-auth-idp-credentials -o jsonpath='{.data.admin_username}' | base64 --decode && echo)"
echo "                🔐 Password:      $(oc -n $AIOPS_NAMESPACE get secret platform-auth-idp-credentials -o jsonpath='{.data.admin_password}' | base64 --decode)"
echo "     "    
echo "     "    
echo "     "           

    




DEMO_READY=$(oc get ns robot-shop  --ignore-not-found|| true) 
if [[ $DEMO_READY =~ "Active" ]]; 
then

    echo "    -----------------------------------------------------------------------------------------------------------------------------------------------"
    echo "    -----------------------------------------------------------------------------------------------------------------------------------------------"
    echo "    🚀 1.3 Demo Apps - Details"
    echo "    -----------------------------------------------------------------------------------------------------------------------------------------------"
    echo "    -----------------------------------------------------------------------------------------------------------------------------------------------"
    echo "    "
    appURL=$(oc get routes -n robot-shop robotshop  -o jsonpath="{['spec']['host']}")|| true
    echo "            📥 RobotShop:"   
    echo "    " 
    echo "                🌏 APP URL:       https://$appURL/"
    echo "  "
    echo "    "
    echo "    "
    echo "    "
    echo "    "
  
fi






echo "    "
echo "    "
echo "    "
echo "    "
echo "***************************************************************************************************************************************************"
echo "***************************************************************************************************************************************************"
echo "🚀 2. IBMAIOps Configuration Information"
echo "***************************************************************************************************************************************************"
echo "***************************************************************************************************************************************************"
echo "    "
echo "    "
echo "    "
echo "    -----------------------------------------------------------------------------------------------------------------------------------------------"
echo "    -----------------------------------------------------------------------------------------------------------------------------------------------"
echo "    🚀 2.1 Configure LDAP - Access Control "
echo "    -----------------------------------------------------------------------------------------------------------------------------------------------"
echo "    -----------------------------------------------------------------------------------------------------------------------------------------------"
echo "    " 
echo "            📥 Identity providers:"
echo ""
echo "                🌏 Connection name:      LDAP"
echo "                🛠️  Server type:          Custom"
echo "                "
echo "                🧒 Base DN:              dc=ibm,dc=com"
echo "                🧒 Bind DN:              cn=admin,dc=ibm,dc=com"
echo "                🔐 Bind DN password:     Selected at installation "
echo "                 "
echo "                🌏 LDAP server URL:      ldap://openldap.openldap:389"
echo "                 "
echo "                🛠️  Group filter:         (&(cn=%v)(objectclass=groupOfUniqueNames))"
echo "                🛠️  User filter:          (&(uid=%v)(objectclass=Person))"
echo "                🛠️  Group ID map:         *:cn"
echo "                🛠️  User ID map:          *:uid"
echo "                🛠️  Group member ID map:  groupOfUniqueNames:uniqueMember"
echo "    "
echo "    "
echo "            📥 OPENLDAP ADMIN LOGIN:"
echo "    " 
echo "                🌏 URL:           https://$(oc get route -n openldap admin -o jsonpath={.spec.host})"
echo "                🧑 User:          cn=admin,dc=ibm,dc=com"
echo "                🔐 Password:      Selected at installation"
echo ""
echo ""
echo ""
echo ""
ELK_READY=$(oc get ns openshift-logging  --ignore-not-found|| true) 
if [[ $ELK_READY =~ "Active" ]]; 
then
    echo "    -----------------------------------------------------------------------------------------------------------------------------------------------"
    echo "    -----------------------------------------------------------------------------------------------------------------------------------------------"
    echo "    🚀 2.2 Configure ELK "
    echo "    -----------------------------------------------------------------------------------------------------------------------------------------------"
    echo "    -----------------------------------------------------------------------------------------------------------------------------------------------"
    token=$(oc -n openshift-logging get secret $(oc get secret -n openshift-logging|grep cluster-logging-operator-token-|awk '{print$1}') -o jsonpath='{.data.token}' | base64 --decode && echo)
    routeES=`oc get route elasticsearch -o jsonpath={.spec.host} -n openshift-logging`
    routeKIBANA=`oc get route kibana -o jsonpath={.spec.host} -n openshift-logging`
    echo "      "
    echo "            📥 ELK:"
    echo "      "
    echo "               🌏 ELK service URL             : https://$routeES/app*"
    echo "               🌏 Kibana URL                  : https://$routeKIBANA"
    echo "               🔐 Authentication type         : Token"
    echo "               🔐 Token                       : $token"
    echo "      "
    echo "               🗺️  Filter                     : "
    echo ""
    echo "                      {"
    echo "                        \"query\": {"
    echo "                          \"bool\": {"
    echo "                               \"must\": {"
    echo "                                  \"term\" : { \"kubernetes.namespace_name\" : \"robot-shop\" }"
    echo "                               }"
    echo "                              }"
    echo "                          }"
    echo "                      }"
    echo "                  "
    echo "  "
    echo ""
    echo ""
    echo "               🕦 TimeZone	                : set to your Timezone"
    echo "               🚪 Kibana port                 : 443"
    echo "  "
    echo ""
    echo ""
    echo "               🗺️  Mapping                     : "
    echo "  "    
    echo "{ "
    echo "  \"codec\": \"elk\","
    echo "  \"message_field\": \"message\","
    echo "  \"log_entity_types\": \"kubernetes.container_image_id, kubernetes.host, kubernetes.pod_name, kubernetes.namespace_name\","
    echo "  \"instance_id_field\": \"kubernetes.container_name\","
    echo "  \"rolling_time\": 10,"
    echo "  \"timestamp_field\": \"@timestamp\""
    echo "}"
    echo "  " 
fi
echo "    -----------------------------------------------------------------------------------------------------------------------------------------------"
echo "    -----------------------------------------------------------------------------------------------------------------------------------------------"
echo "    🚀 2.3 Configure Runbooks - Ansible Automation Controller "
echo "    -----------------------------------------------------------------------------------------------------------------------------------------------"
echo "    -----------------------------------------------------------------------------------------------------------------------------------------------"
echo "    "
echo "            📥 Add connection :"
echo ""
echo "                🌏 URL for REST API:      https://$(oc get route -n awx awx -o jsonpath={.spec.host})"
echo "                🔐 Authentication type:   User ID/Password"
echo "                🧑 User:                  admin"
echo "                🔐 Password:              $(oc -n awx get secret awx-admin-password -o jsonpath='{.data.password}' | base64 --decode && echo)"
echo ""
echo ""
echo ""
echo ""
echo ""
echo ""
echo ""
echo ""
echo "    -----------------------------------------------------------------------------------------------------------------------------------------------"
echo "    -----------------------------------------------------------------------------------------------------------------------------------------------"
echo "    🚀 2.4 Configure Runbooks - Runbook Parameters "
echo "    -----------------------------------------------------------------------------------------------------------------------------------------------"
echo "    -----------------------------------------------------------------------------------------------------------------------------------------------"
echo "    "
echo "            📥 Add connection :"
echo ""
echo "                🌏 Action:      IBMAIOPS Mitigate Robotshop Ratings Outage"
echo "                🗺️ Value:                  "
DEMO_TOKEN=$(oc create token -n default demo-admin --duration=999999999s)
DEMO_URL=$(oc status|grep -m1 "In project"|awk '{print$6}')

echo "                        {"
echo "                         \"my_k8s_apiurl\": \"$DEMO_URL\","
echo "                           \"my_k8s_apikey\": \"$DEMO_TOKEN\""
echo "                        }"
echo ""
echo ""
echo ""
echo ""
echo "    -----------------------------------------------------------------------------------------------------------------------------------------------"
echo "    -----------------------------------------------------------------------------------------------------------------------------------------------"
echo "    🚀 2.5 Configure Applications - RobotShop Kubernetes Observer "
echo "    -----------------------------------------------------------------------------------------------------------------------------------------------"
echo "    -----------------------------------------------------------------------------------------------------------------------------------------------"
echo "    " 

API_TOKEN=$(oc create token -n default demo-admin --duration=999999999s)
API_URL=$(oc status|grep -m1 "In project"|awk '{print$6}')
API_SERVER=$(echo $API_URL| cut -d ":" -f 2| tr -d '/')
API_PORT=$(echo $API_URL| cut -d ":" -f 3)

echo ""
echo "                🛠️  Name:                          RobotShop"
echo "                🛠️  Data center:                   robot-shop"
echo "                🛠️  Kubernetes master IP address:  $API_SERVER"
echo "                🛠️  Kubernetes API port:           $API_PORT"
echo "                🛠️  Token:                         $API_TOKEN"
echo "                🛠️  Trust all HTTPS certificates:  true"
echo "                🛠️  Correlate analytics events:    true"
echo "                🛠️  Namespaces to observe:         robot-shop"
echo ""
echo ""
echo ""
echo ""







echo "    "
echo "    "
echo "    "
echo "    "


echo "***************************************************************************************************************************************************"
echo "***************************************************************************************************************************************************"
echo "🚀 Openshift Connection Details"
echo "***************************************************************************************************************************************************"
echo "***************************************************************************************************************************************************"
echo ""
echo "  📥 Openshift Console"
echo ""
echo "            🌏 URL:               https://$(oc get route -n openshift-console console -o jsonpath={.spec.host})"
echo " "
echo " "
echo " "
echo "  📥 Openshift Command Line - ADMIN"
echo ""
API_TOKEN=$(oc create token -n default demo-admin --duration=999999999s)
CONSOLE_URL="https://"$(oc get route -n openshift-console console -o jsonpath={.spec.host})
API_URL=${CONSOLE_URL/console-openshift-console.apps/api}:6443
echo "            🌏 URL:               $API_URL"
echo "            🔐 Token:             $API_TOKEN"
echo ""
echo ""
echo "            🧑 Login:   oc login --server=$API_URL:6443 --token=$API_TOKEN"
echo " "
echo " "
echo " "
echo " "
echo " "
echo " "
echo " "
echo " "
echo "  📥 Openshift Command Line - DEMO"
echo ""
DEMO_TOKEN=$(oc create token -n default demo-admin --duration=999999999s)
DEMO_URL=$(oc status|grep -m1 "In project"|awk '{print$6}')
echo "            🌏 URL:               $DEMO_URL"
echo "            🔐 Token:             $DEMO_TOKEN"
echo ""
echo ""
echo "            🧑 Login:   oc login --token=$DEMO_TOKEN --server=$DEMO_URL"
echo ""
echo ""
echo ""
echo ""
echo ""
echo ""
echo ""


echo "***************************************************************************************************************************************************"
echo "***************************************************************************************************************************************************"
echo "🚀 Additional Components"
echo "***************************************************************************************************************************************************"
echo "***************************************************************************************************************************************************"
echo "    "
echo "    "
echo "    "

TURBO_READY=$(oc get ns turbonomic --ignore-not-found|| true) 
if [[ $TURBO_READY =~ "Active" ]]; 
then
    echo "    -----------------------------------------------------------------------------------------------------------------------------------------------"
    echo "    -----------------------------------------------------------------------------------------------------------------------------------------------"
    echo "    🚀 Turbonomic Dashboard "
    echo "    -----------------------------------------------------------------------------------------------------------------------------------------------"
    echo "    -----------------------------------------------------------------------------------------------------------------------------------------------"
    echo "    "
    echo "            📥 Turbonomic Dashboard :"
    echo ""
    echo "                🌏 URL:           https://$(oc get route -n turbonomic nginx -o jsonpath={.spec.host})"
    echo "                🧑 User:          administrator"
    echo "                🔐 Password:      As set at init step"
    echo "    "
    echo "    "
    echo "    "
    echo "    "
fi




AWX_READY=$(oc get ns awx  --ignore-not-found|| true) 
if [[ $AWX_READY =~ "Active" ]]; 
then
    echo "    -----------------------------------------------------------------------------------------------------------------------------------------------"
    echo "    -----------------------------------------------------------------------------------------------------------------------------------------------"
    echo "    🚀 AWX "
    echo "    -----------------------------------------------------------------------------------------------------------------------------------------------"
    echo "    -----------------------------------------------------------------------------------------------------------------------------------------------"
    echo "    "
    echo "            📥 AWX :"
    echo ""
    echo "                🌏 URL:           https://$(oc get route -n awx awx -o jsonpath={.spec.host})"
    echo "                🧑 User:          admin"
    echo "                🔐 Password:      $(oc -n awx get secret awx-admin-password -o jsonpath='{.data.password}' | base64 --decode && echo)"
    echo "    "
    echo "    "
    echo "    "
    echo "    "
fi









ELK_READY=$(oc get ns openshift-logging  --ignore-not-found|| true) 
if [[ $ELK_READY =~ "Active" ]]; 
then
    echo "    -----------------------------------------------------------------------------------------------------------------------------------------------"
    echo "    -----------------------------------------------------------------------------------------------------------------------------------------------"
    echo "    🚀 ELK "
    echo "    -----------------------------------------------------------------------------------------------------------------------------------------------"
    echo "    -----------------------------------------------------------------------------------------------------------------------------------------------"
    token=$(oc -n openshift-logging get secret $(oc get secret -n openshift-logging|grep cluster-logging-operator-token-|awk '{print$1}') -o jsonpath='{.data.token}' | base64 --decode && echo)
    routeES=`oc get route elasticsearch -o jsonpath={.spec.host} -n openshift-logging`
    routeKIBANA=`oc get route kibana -o jsonpath={.spec.host} -n openshift-logging`
    echo "      "
    echo "            📥 ELK:"
    echo "      "
    echo "               🌏 ELK service URL             : https://$routeES/app*"
    echo "               🌏 Kibana URL                  : https://$routeKIBANA"
    echo "               🔐 Authentication type         : Token"
    echo "               🔐 Token                       : $token"
    echo "      "
    echo "               🗺️  Filter                     : "
    echo ""
    echo "      {"
    echo "        \"query\": {"
    echo "          \"bool\": {"
    echo "               \"must\": {"
    echo "                  \"term\" : { \"kubernetes.namespace_name\" : \"robot-shop\" }"
    echo "               }"
    echo "              }"
    echo "          }"
    echo "      }"
    echo ""
    echo "               🚪 Kibana port                 : 443"
    echo ""
    echo "               🗺️  Mapping                     : "
    echo "{ "
    echo "  \"codec\": \"elk\","
    echo "  \"message_field\": \"message\","
    echo "  \"log_entity_types\": \"kubernetes.container_image_id, kubernetes.host, kubernetes.pod_name, kubernetes.namespace_name\","
    echo "  \"resource_id\": \"kubernetes.container_name\","
    echo "  \"instance_id_field\": \"kubernetes.namespace_name\","
    echo "  \"rolling_time\": 10,"
    echo "  \"timestamp_field\": \"@timestamp\""
    echo "}"
    echo "  "
    echo ""
    echo ""
    echo ""

    echo "  "
    echo ""
    echo ""
    echo ""
    echo ""
    echo ""
    echo ""

 fi



echo "    "
echo "    "
echo "    "
echo "    "
echo "    "
echo "    "
echo "    "
echo "    "
echo "    "
echo "    "
echo "    "
echo "    "







echo "***************************************************************************************************************************************************"
echo "***************************************************************************************************************************************************"
echo "🚀 IBM AIOps - Technical Links"
echo "***************************************************************************************************************************************************"
echo "***************************************************************************************************************************************************"
echo "    "






ROUTE_READY=$(oc get routes -n $AIOPS_NAMESPACE job-manager  --ignore-not-found|| true) 
if [[ $ROUTE_READY =~ "job-manager" ]]; 
then
    echo "    -----------------------------------------------------------------------------------------------------------------------------------------------"
    echo "    -----------------------------------------------------------------------------------------------------------------------------------------------"
    echo "    🚀 Flink Task Manager - Ingestion"
    echo "    -----------------------------------------------------------------------------------------------------------------------------------------------"
    echo "    -----------------------------------------------------------------------------------------------------------------------------------------------"
    appURL=$(oc get routes -n $AIOPS_NAMESPACE job-manager  -o jsonpath="{['spec']['host']}")
    echo "    " 
    echo "                🌏 APP URL:       https://$appURL/"
    echo "    "
    echo "                In Chrome: if you get blocked just type "thisisunsafe" and it will continue (you don't get any visual feedback when typing!)"
    echo "    "
    echo "    "
    echo "    "
    echo "    "
fi

ROUTE_READY=$(oc get routes -n $AIOPS_NAMESPACE job-manager-policy  --ignore-not-found|| true) 
if [[ $ROUTE_READY =~ "job-manager" ]]; 
then
    echo "    -----------------------------------------------------------------------------------------------------------------------------------------------"
    echo "    -----------------------------------------------------------------------------------------------------------------------------------------------"
    echo "    🚀 Flink Task Manager - Policy Framework"
    echo "    -----------------------------------------------------------------------------------------------------------------------------------------------"
    echo "    -----------------------------------------------------------------------------------------------------------------------------------------------"
    appURL=$(oc get routes -n $AIOPS_NAMESPACE job-manager-policy  -o jsonpath="{['spec']['host']}")
    echo "    " 
    echo "                🌏 APP URL:       https://$appURL/"
    echo "    "
    echo "                In Chrome: if you get blocked just type "thisisunsafe" and it will continue (you don't get any visual feedback when typing!)"
    echo "    "
    echo "    "
    echo "    "
    echo "    "
fi 


ROUTE_READY=$(oc get routes -n $AIOPS_NAMESPACE spark  --ignore-not-found|| true) 
if [[ $ROUTE_READY =~ "job-manager" ]]; 
then
    echo "    -----------------------------------------------------------------------------------------------------------------------------------------------"
    echo "    -----------------------------------------------------------------------------------------------------------------------------------------------"
    echo "    🚀 Spark Master"
    echo "    -----------------------------------------------------------------------------------------------------------------------------------------------"
    echo "    -----------------------------------------------------------------------------------------------------------------------------------------------"
    appURL=$(oc get routes -n $AIOPS_NAMESPACE sparkadmin  -o jsonpath="{['spec']['host']}")
    echo "    " 
    echo "            📥 Spark Master:"
    echo "    " 
    echo "                🌏 APP URL:       https://$appURL/"
    echo "    "
    echo "    "
    echo "    "
    echo "    "
    echo "    "
fi






ROOK_READY=$(oc get ns rook-ceph  --ignore-not-found|| true) 
if [[ $ROOK_READY =~ "Active" ]]; 
then
    echo "    -----------------------------------------------------------------------------------------------------------------------------------------------"
    echo "    -----------------------------------------------------------------------------------------------------------------------------------------------"
    echo "    🚀 Rook/Ceph Dashboard "
    echo "    -----------------------------------------------------------------------------------------------------------------------------------------------"
    echo "    -----------------------------------------------------------------------------------------------------------------------------------------------"
    echo "    " 
    echo "            📥 Rook/Ceph Dashboard :"
    echo "    " 
    echo "                🌏 URL:           https://dash-rook-ceph.$CLUSTER_NAME/"
    echo "                🧑 User:          admin"
    echo "                🔐 Password:      $(oc -n rook-ceph get secret rook-ceph-dashboard-password -o jsonpath="{['data']['password']}" | base64 --decode)"
    echo "    "
    echo "    "
    echo "    "
    echo "    "    
fi


echo ""
echo ""

echo "***************************************************************************************************************************************************"
echo "***************************************************************************************************************************************************"
echo "🚀 IBM AIOps - DEMO Connections"
echo "***************************************************************************************************************************************************"
echo "***************************************************************************************************************************************************"
echo "    "




echo "    -----------------------------------------------------------------------------------------------------------------------------------------------"
echo "    -----------------------------------------------------------------------------------------------------------------------------------------------"
echo "    🚀 Service Now "
echo "    -----------------------------------------------------------------------------------------------------------------------------------------------"
echo "    -----------------------------------------------------------------------------------------------------------------------------------------------"
echo "    " 
echo "            📥 Login SNOW Dev Portal (if you have to wake the dev instance):"
echo "    " 
echo "                🌏 URL:                   https://developer.servicenow.com/dev.do"
echo "                🧑 User:                  demo@mydemo.center"
echo "                🔐 Password:              Selected at installationIBM"
echo ""
echo ""
echo "            📥  Login SNOW Instance::"
echo ""
echo "                🌏 URL:                   https://dev56805.service-now.com"
echo "                🧑 User ID:               abraham.lincoln             (if you followed the demo install instructions)"
echo "                🔐 Password:              Selected at installation                   (if you followed the demo install instructions)"
echo "                🔐 Encrypted Password:    g4W3L7/eFsUjV0eMncBkbg==    (if you followed the demo install instructions)"
echo ""
echo ""
echo "            📥 INTEGRATION SNOW-->IBMAIOPS:"
echo "    " 
echo "                🌏 URL:                   https://$(oc get route -n $AIOPS_NAMESPACE cpd -o jsonpath={.spec.host})    (URL for IBM IBM AIOps connection)"
echo "                📛 Instance Name:         aimanager"
echo "                🧑 User:                  admin"
echo "                🔐 Password:              $(oc -n $AIOPS_NAMESPACE get secret platform-auth-idp-credentials -o jsonpath='{.data.admin_password}' | base64 --decode)"
echo ""
echo ""
echo ""
echo ""
echo ""
echo ""
echo ""
echo ""



echo "***************************************************************************************************************************************************"
echo "***************************************************************************************************************************************************"
echo "🚀 IBM AIOps - APIs"
echo "***************************************************************************************************************************************************"
echo "***************************************************************************************************************************************************"
echo ""



echo "        -----------------------------------------------------------------------------------------------------------------------------------------------"
echo "        -----------------------------------------------------------------------------------------------------------------------------------------------"
echo "        🚀 IBMAIOPS APIs "
echo "        -----------------------------------------------------------------------------------------------------------------------------------------------"
echo "        -----------------------------------------------------------------------------------------------------------------------------------------------"


apiURL=$(oc get routes -n $AIOPS_NAMESPACE aiops-topology-merge  -o jsonpath="{['spec']['host']}")
echo "                🌏 Topology Merge:           https://$apiURL/"
echo "    "
apiURL=$(oc get routes -n $AIOPS_NAMESPACE aiops-topology-rest-observer  -o jsonpath="{['spec']['host']}")
echo "                🌏 Topology REST:            https://$apiURL/"
echo "    "
apiURL=$(oc get routes -n $AIOPS_NAMESPACE aiops-topology-file-observer  -o jsonpath="{['spec']['host']}")
echo "                🌏 Topology File:            https://$apiURL/"
echo "    "
apiURL=$(oc get routes -n $AIOPS_NAMESPACE  aiops-topology-topology  -o jsonpath="{['spec']['host']}")
echo "                🌏 Topology Manage:          https://$apiURL/"
echo "                🌏 Topology SWAGGER:         https://$apiURL/1.0/topology/swagger"
echo "    "
apiURL=$(oc get routes -n $AIOPS_NAMESPACE datalayer-api  -o jsonpath="{['spec']['host']}")
echo "                🌏 Datalayer API:            https://$apiURL/"
echo "                🌏 Datalayer SWAGGER:        https://$apiURL/irdatalayer.aiops.io/docs/active/v1"
echo "    "
apiURL=$(oc get routes -n $AIOPS_NAMESPACE aimanager-aio-controller  -o jsonpath="{['spec']['host']}")
echo "                🌏 AIO Controller API:       https://$apiURL/"
#echo "                🌏 AIO Controller SWAGGER:   https://$apiURL/irdatalayer.aiops.io/openapi/ui/#/"
echo "                🌏 AIO Controller SWAGGER:   https://$apiURL/openapi/ui/#/"

echo ""
echo ""
echo ""
echo "                🌏 METRICS:                  https://$(oc get route -n $AIOPS_NAMESPACE cpd -o jsonpath={.spec.host})/aiops/cfd95b7e-3bc7-4006-a4a8-a73a79c71255/resolution-hub/alerts/anomaly/details?metric=MemoryUsagePercent&group=MemoryUsage&resource=mysql-predictive&policyId=1ffe8c50-e103-11ec-984f-17ba5df49c3f&isAiopsPolicy=true&viewname=Example_IBM_RelatedEvents&viewtype=3"


echo ""
echo ""
echo ""
echo ""
echo ""


