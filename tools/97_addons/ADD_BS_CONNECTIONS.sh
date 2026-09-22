# ADD NON FUNCTIONING CONNECTIONS FOR DEMO SYSTEMS

export AIOPS_NAMESPACE=$(oc get po -A|grep aiops-orchestrator-controller |awk '{print$1}')
export CPD_ROUTE=$(oc get route -n $AIOPS_NAMESPACE cpd -o jsonpath={.spec.host})
export AIO_PLATFORM_ROUTE=$(oc get route -n $AIOPS_NAMESPACE aimanager-aio-controller -o jsonpath={.spec.host})

echo "        Namespace:          $AIOPS_NAMESPACE"
echo "        CPD_ROUTE:          $CPD_ROUTE"
echo "        AIO_PLATFORM_ROUTE: $AIO_PLATFORM_ROUTE"


echo "       🛠️   Getting ZEN Token"

export CONSOLE_ROUTE=$(oc get route -n $AIOPS_NAMESPACE cp-console  -o jsonpath={.spec.host})          
echo ""
export CPD_ROUTE=$(oc get route -n $AIOPS_NAMESPACE cpd  -o jsonpath={.spec.host})          
export CPADMIN_PWD=$(oc -n $AIOPS_NAMESPACE get secret platform-auth-idp-credentials -o jsonpath='{.data.admin_password}' | base64 -d && echo)
export CPADMIN_USER=$(oc -n $AIOPS_NAMESPACE get secret platform-auth-idp-credentials -o jsonpath='{.data.admin_username}' | base64 -d && echo)
export ACCESS_TOKEN=$(curl -s -k -H "Content-Type: application/x-www-form-urlencoded;charset=UTF-8" -d "grant_type=password&username=$CPADMIN_USER&password=$CPADMIN_PWD&scope=openid" https://$CONSOLE_ROUTE/idprovider/v1/auth/identitytoken|jq -r '.access_token')
export ZEN_API_HOST=$(oc get route -n $AIOPS_NAMESPACE cpd -o jsonpath='{.spec.host}')
export ZEN_TOKEN=$(curl -k -XGET https://$ZEN_API_HOST/v1/preauth/validateAuth \
-H "username: $CPADMIN_USER" \
-H "iam-token: $ACCESS_TOKEN"|jq -r '.accessToken')
echo "        ACCESS_TOKEN: $ZEN_TOKEN"

echo "${ZEN_TOKEN}"
echo "        AI_PLATFORM_ROUTE:  $ZEN_TOKEN"

echo "Sucessfully logged in" 
echo ""


# IRC_NAMESPACE=ibm-aiops
# IRC_INSTANCE=$(oc get issueresolutioncore -n $IRC_NAMESPACE -o custom-columns=name:metadata.name --no-headers)
#  IRC_PRIMARY_OBJECTSERVER_SVC=$IRC_INSTANCE-ir-core-ncoprimary
#  IRC_BACKUP_OBJECTSERVER_SVC=$IRC_INSTANCE-ir-core-ncobackup
#  IRC_PRIMARY_OBJECTSERVER_PORT=$(oc get svc -n $IRC_NAMESPACE $IRC_PRIMARY_OBJECTSERVER_SVC -o jsonpath='{.spec.ports[?(@.name=="primary-tds-port")].port}')
#  IRC_BACKUP_OBJECTSERVER_PORT=$(oc get svc -n $IRC_NAMESPACE $IRC_BACKUP_OBJECTSERVER_SVC -o jsonpath='{.spec.ports[?(@.name=="backup-tds-port")].port}')
#  IRC_OMNI_USERNAME=aiopsprobe
#  IRC_OMNI_PASSWORD=$(oc get secret -n $IRC_NAMESPACE $IRC_INSTANCE-ir-core-omni-secret -o jsonpath='{.data.OMNIBUS_PROBE_PASSWORD}' | base64 --decode && echo)
 
# echo "IRC_NAMESPACE                 "$IRC_NAMESPACE
# echo "IRC_INSTANCE                  "$IRC_INSTANCE
# echo "IRC_PRIMARY_OBJECTSERVER_SVC  "$IRC_PRIMARY_OBJECTSERVER_SVC
# echo "IRC_BACKUP_OBJECTSERVER_SVC   "$IRC_BACKUP_OBJECTSERVER_SVC
# echo "IRC_PRIMARY_OBJECTSERVER_PORT "$IRC_PRIMARY_OBJECTSERVER_PORT
# echo "IRC_BACKUP_OBJECTSERVER_PORT  "$IRC_BACKUP_OBJECTSERVER_PORT
# echo "IRC_OMNI_USERNAME             "$IRC_OMNI_USERNAME
# echo "IRC_OMNI_PASSWORD             "$IRC_OMNI_PASSWORD

# oc extract secret/$IRC_INSTANCE-ir-core-ncoprimary-tls -n $IRC_NAMESPACE --to=. --keys=tls.crt





# --------------------------------------------------------------------------------------------------------
# ADD vSphere-Demo
# --------------------------------------------------------------------------------------------------------
curl "https://$CPD_ROUTE/aiops/integrations/api/controller/grpc/connections/" \
-X 'POST' \
-H 'Content-Type: application/json' \
-H 'Accept: application/json' \
-H 'x-tenantid: cfd95b7e-3bc7-4006-a4a8-a73a79c71255' \
-H "authorization: Bearer $ZEN_TOKEN"   \
--data-binary '{
    "connection_config": {
        "webhook": {
            "authentication": {
                "type": "none"
            },
            "enabled": true,
            "path": "/webhook-connector/vsphere",
            "mappings": "(\n    {\n        \"resource\": {\n          \"name\": $exists(VMWARE_ALARM_TARGET_NAME) ? $length(VMWARE_ALARM_TARGET_NAME) > 0 ? VMWARE_ALARM_TARGET_NAME : \"Unknown\",\n          \"type\": $exists(VMWARE_ALARM_TARGET_ID) ? $length(VMWARE_ALARM_TARGET_ID) > 0 ?\n                  $contains(VMWARE_ALARM_TARGET_ID, /datacenter/i) ? \"Service\" :\n                  $contains(VMWARE_ALARM_TARGET_ID, /datastore-/i) ? \"Service\" :\n                  $contains(VMWARE_ALARM_TARGET_ID, /domain-c/i) ? \"Cluster\" :\n                  $contains(VMWARE_ALARM_TARGET_ID, /host-/i) ? \"Server\" :\n                  $contains(VMWARE_ALARM_TARGET_ID, /resgroup-/i) ? \"Service\" :\n                  $contains(VMWARE_ALARM_TARGET_ID, /network-/i) ? \"Service\" :\n                  $contains(VMWARE_ALARM_TARGET_ID, /dvs-/i) ? \"Service\" :\n                  $contains(VMWARE_ALARM_TARGET_ID, /group-/i) ? \"Service\" :\n                  $contains(VMWARE_ALARM_TARGET_ID, /vm-/i) ? \"Server\" : \"Unknown\",\n          \"ipaddress\": $exists(VMWARE_ALARM_TARGET_ID) ? $length(VMWARE_ALARM_TARGET_ID) > 0 ?\n                       $contains(VMWARE_ALARM_TARGET_ID, /host-/i) ? \n                       $contains(VMWARE_ALARM_TARGET_NAME, /^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/) ?\n                       VMWARE_ALARM_TARGET_NAME :\n                       $contains(VMWARE_ALARM_TARGET_NAME, /^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$|^\\s*((([0-9A-Fa-f]{1,4}:){7}([0-9A-Fa-f]{1,4}|:))|(([0-9A-Fa-f]{1,4}:){6}(:[0-9A-Fa-f]{1,4}|((25[0-5]|2[0-4]\\d|1\\d\\d|[1-9]?\\d)(\\.(25[0-5]|2[0-4]\\d|1\\d\\d|[1-9]?\\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){5}(((:[0-9A-Fa-f]{1,4}){1,2})|:((25[0-5]|2[0-4]\\d|1\\d\\d|[1-9]?\\d)(\\.(25[0-5]|2[0-4]\\d|1\\d\\d|[1-9]?\\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){4}(((:[0-9A-Fa-f]{1,4}){1,3})|((:[0-9A-Fa-f]{1,4})?:((25[0-5]|2[0-4]\\d|1\\d\\d|[1-9]?\\d)(\\.(25[0-5]|2[0-4]\\d|1\\d\\d|[1-9]?\\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){3}(((:[0-9A-Fa-f]{1,4}){1,4})|((:[0-9A-Fa-f]{1,4}){0,2}:((25[0-5]|2[0-4]\\d|1\\d\\d|[1-9]?\\d)(\\.(25[0-5]|2[0-4]\\d|1\\d\\d|[1-9]?\\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){2}(((:[0-9A-Fa-f]{1,4}){1,5})|((:[0-9A-Fa-f]{1,4}){0,3}:((25[0-5]|2[0-4]\\d|1\\d\\d|[1-9]?\\d)(\\.(25[0-5]|2[0-4]\\d|1\\d\\d|[1-9]?\\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){1}(((:[0-9A-Fa-f]{1,4}){1,6})|((:[0-9A-Fa-f]{1,4}){0,4}:((25[0-5]|2[0-4]\\d|1\\d\\d|[1-9]?\\d)(\\.(25[0-5]|2[0-4]\\d|1\\d\\d|[1-9]?\\d)){3}))|:))|(:(((:[0-9A-Fa-f]{1,4}){1,7})|((:[0-9A-Fa-f]{1,4}){0,5}:((25[0-5]|2[0-4]\\d|1\\d\\d|[1-9]?\\d)(\\.(25[0-5]|2[0-4]\\d|1\\d\\d|[1-9]?\\d)){3}))|:)))(%.+)?\\s*$/) ?\n                       VMWARE_ALARM_TARGET_NAME,\n          \"hostname\": $exists(VMWARE_ALARM_TARGET_ID) ? $length(VMWARE_ALARM_TARGET_ID) > 0 ?\n                      $contains(VMWARE_ALARM_TARGET_ID, /host-/i) ? \n                      $contains(VMWARE_ALARM_TARGET_NAME, /^(([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\\-]*[a-zA-Z0-9])\\.)*([A-Za-z0-9]|[A-Za-z0-9][A-Za-z0-9\\-]*[A-Za-z0-9])$/) ?\n                      VMWARE_ALARM_TARGET_NAME\n        },\n        \"type\": {\n          \"eventType\": $exists(VMWARE_ALARM_NEWSTATUS) ? $length(VMWARE_ALARM_NEWSTATUS) > 0 ?\n                      $contains(VMWARE_ALARM_NEWSTATUS, /GREEN/i) ?  \"resolution\" : \"problem\",\n          \"classification\": $exists(VMWARE_ALARM_NAME) ? $length(VMWARE_ALARM_NAME) > 0 ? VMWARE_ALARM_NAME\n        },\n        \"summary\":  $exists(VMWARE_ALARM_ALARMVALUE) ? $length(VMWARE_ALARM_ALARMVALUE) > 0 ? $contains(VMWARE_ALARM_ALARMVALUE, /Current values for metric\\/state/) ?\n                    \"Entity: \" & VMWARE_ALARM_TARGET_NAME & \", \" & VMWARE_ALARM_TRIGGERINGSUMMARY : VMWARE_ALARM_TRIGGERINGSUMMARY,\n        \"severity\": $exists(VMWARE_ALARM_NEWSTATUS) ? $length(VMWARE_ALARM_NEWSTATUS) > 0 ? \n                    $contains(VMWARE_ALARM_NEWSTATUS, /RED/i) ?  6 :\n                    $contains(VMWARE_ALARM_NEWSTATUS, /YELLOW/i) ?  3 :\n                    $contains(VMWARE_ALARM_NEWSTATUS, /GREEN/i) ?  2 :\n                    1,\n        \"expiryTime\": $exists(EXPIRYTIME) ? EXPIRYTIME,\n        \"sender\": {\n          \"name\": $exists(VMWARE_ALARM_EVENT_USERNAME) ? $length(VMWARE_ALARM_EVENT_USERNAME) > 0 ? VMWARE_ALARM_EVENT_USERNAME : \"VMware vSphere\",\n          \"type\": \"Webhook Connector\"\n        }\n      }\n)"
        },
        "deploymentType": "local",
        "display_name": "vSphere-Demo",
        "description": "Automatically created by Nicks scripts",
        "connectionName": "vSphere-Demo"
    },
    "connectorConfig": {
        "AIModelTypeList": ["{{sidePanel.AIModelTypes.logAnomaly}}"],
        "apiAdaptor": "grpc",
        "categories": ["{{connector.common.category.events}}"],
        "datasourceType": "events",
        "deploymentType": ["local"],
        "displayName": "{{connector.webhook.name}}",
        "hasAIModelType": false,
        "hasOptionalConfig": true,
        "hasOptionalText": false,
        "iconFileType": "svg",
        "isObserver": false,
        "requiresTestConnection": false,
        "sidePanelDescription": "{{connector.webhook.sidepanel.sidePanelDescription}}",
        "sidePanelInfo": ["{{sidePanel.information.webhook.1}}", "{{sidePanel.information.webhook.2}}", "{{sidePanel.information.webhook.3}}"],
        "sidePanelInfoHeader": "{{sidePanel.information.header}}",
        "sidePanelOptionalConfigHeader": "{{sidePanel.webhook.optional.config.header}}",
        "sidePanelOptionalConfigList": ["{{sidePanel.webhook.optional.config.1}}"],
        "sidePanelTitle": "{{connector.webhook.sidepanel.sidePanelTitle}}",
        "type": "webhook",
        "url": "https://ibm.biz/aiops-genwebhook"
    }
}'





# --------------------------------------------------------------------------------------------------------
# ADD Turbonomic-Demo
# --------------------------------------------------------------------------------------------------------
curl "https://$CPD_ROUTE/aiops/integrations/api/controller/grpc/connections/" \
-X 'POST' \
-H 'Content-Type: application/json' \
-H 'Accept: application/json' \
-H 'x-tenantid: cfd95b7e-3bc7-4006-a4a8-a73a79c71255' \
-H "authorization: Bearer $ZEN_TOKEN"   \
--data-binary '{
    "connection_config": {
        "webhook": {
            "authentication": {
                "type": "none"
            },
            "enabled": true,
            "path": "/webhook-connector/turbonomic",
            "mappings": "(\n    {\n        \"severity\": risk.severity = \"MINOR\" ? 3 : risk.severity = \"MAJOR\" ? 4 : risk.severity = \"CRITICAL\" ? 6 : risk.severity= \"UNKNOWN\" ? 1 : 2,\n        \"summary\": details,\n        \"resource\": {\n            \"name\": target.displayName,\n            \"sourceId\": target.uuid\n        },\n        \"type\": {\n            \"classification\": target.className,\n            \"eventType\": actionState = \"CLEARED\" ? \"resolution\":actionState = \"SUCCEEDED\" ? \"resolution\" : \"problem\",\n            \"condition\": risk.subCategory\n        },\n        \"sender\": {\n            \"name\": \"IBM Turbonomic\",\n            \"type\": \"Webhook Connector\"\n        }\n    }\n)\n\n"
        },
        "deploymentType": "local",
        "display_name": "Turbonomic-Demo",
        "description": "Automatically created by Nicks scripts",
        "connectionName": "Turbonomic-Demo"
    },
    "connectorConfig": {
        "AIModelTypeList": ["{{sidePanel.AIModelTypes.logAnomaly}}"],
        "apiAdaptor": "grpc",
        "categories": ["{{connector.common.category.events}}"],
        "datasourceType": "events",
        "deploymentType": ["local"],
        "displayName": "{{connector.webhook.name}}",
        "hasAIModelType": false,
        "hasOptionalConfig": true,
        "hasOptionalText": false,
        "iconFileType": "svg",
        "isObserver": false,
        "requiresTestConnection": false,
        "sidePanelDescription": "{{connector.webhook.sidepanel.sidePanelDescription}}",
        "sidePanelInfo": ["{{sidePanel.information.webhook.1}}", "{{sidePanel.information.webhook.2}}", "{{sidePanel.information.webhook.3}}"],
        "sidePanelInfoHeader": "{{sidePanel.information.header}}",
        "sidePanelOptionalConfigHeader": "{{sidePanel.webhook.optional.config.header}}",
        "sidePanelOptionalConfigList": ["{{sidePanel.webhook.optional.config.1}}"],
        "sidePanelTitle": "{{connector.webhook.sidepanel.sidePanelTitle}}",
        "type": "webhook",
        "url": "https://ibm.biz/aiops-genwebhook"
    }
}'


# --------------------------------------------------------------------------------------------------------
# ADD PrometheusAlertManager-Demo
# --------------------------------------------------------------------------------------------------------
curl "https://$CPD_ROUTE/aiops/integrations/api/controller/grpc/connections/" \
-X 'POST' \
-H 'Content-Type: application/json' \
-H 'Accept: application/json' \
-H 'x-tenantid: cfd95b7e-3bc7-4006-a4a8-a73a79c71255' \
-H "authorization: Bearer $ZEN_TOKEN"   \
--data-binary '{
    "connection_config": {
        "webhook": {
            "authentication": {
                "type": "none"
            },
            "enabled": true,
            "path": "/webhook-connector/prometheusalert",
            "mappings": "(\n  /* Set resource based on labels available */\n  $resource := function($labels){(\n    $name := $labels.name  ? $labels.name  \n      : $labels.statefulset  ? $labels.statefulset \n      : $labels.deployment  ? $labels.deployment \n      : $labels.daemonset  ? $labels.daemonset \n      : $labels.pod  ? $labels.pod \n      : $labels.container  ? $labels.container \n      : $labels.instance  ? $labels.instance \n      : $labels.app  ? $labels.app \n      : $labels.job_name  ? $labels.job_name \n      : $labels.job  ? $labels.job \n      : $labels.type ? $labels.type: $labels.prometheus;\n      $labels.namespace ? ($name & '/' & $labels.namespace): $name;\n    )\n  };\n  /* Map to event schema */\n  alerts.(\n    { \n      \"summary\": annotations.summary ? annotations.summary: annotations.description ? annotations.description : annotations.message ? annotations.message,\n      \"severity\": $lowercase(labels.severity) = \"critical\" ? 6 : $lowercase(labels.severity) = \"major\" ? 5 : $lowercase(labels.severity) = \"minor\" ? 4 : $lowercase(labels.severity) = \"warning\" ? 3 : 1, \n      \"resource\": {\n        \"name\": $resource(labels)\n      },\n      \"type\": {\n        \"eventType\": $lowercase(status) = \"firing\" ? \"problem\": \"resolution\",\n        \"classification\": labels.alertname\n      },\n      \"links\": [\n        {\n            \"url\": generatorURL\n        }\n      ],\n      \"sender\": {\n        \"name\": \"Prometheus\",\n        \"type\": \"Webhook Connector\"\n      },\n     \"details\": labels\n    }\n  )\n)"
        },
        "deploymentType": "local",
        "display_name": "PrometheusAlertManager-Demo",
        "description": "Automatically created by Nicks scripts",
        "connectionName": "PrometheusAlertManager-Demo"
    },
    "connectorConfig": {
        "AIModelTypeList": ["{{sidePanel.AIModelTypes.logAnomaly}}"],
        "apiAdaptor": "grpc",
        "categories": ["{{connector.common.category.events}}"],
        "datasourceType": "events",
        "deploymentType": ["local"],
        "displayName": "{{connector.webhook.name}}",
        "hasAIModelType": false,
        "hasOptionalConfig": true,
        "hasOptionalText": false,
        "iconFileType": "svg",
        "isObserver": false,
        "requiresTestConnection": false,
        "sidePanelDescription": "{{connector.webhook.sidepanel.sidePanelDescription}}",
        "sidePanelInfo": ["{{sidePanel.information.webhook.1}}", "{{sidePanel.information.webhook.2}}", "{{sidePanel.information.webhook.3}}"],
        "sidePanelInfoHeader": "{{sidePanel.information.header}}",
        "sidePanelOptionalConfigHeader": "{{sidePanel.webhook.optional.config.header}}",
        "sidePanelOptionalConfigList": ["{{sidePanel.webhook.optional.config.1}}"],
        "sidePanelTitle": "{{connector.webhook.sidepanel.sidePanelTitle}}",
        "type": "webhook",
        "url": "https://ibm.biz/aiops-genwebhook"
    }
}'


# --------------------------------------------------------------------------------------------------------
# ADD Zabbix-Demo
# --------------------------------------------------------------------------------------------------------
curl "https://$CPD_ROUTE/aiops/integrations/api/controller/grpc/connections/" \
-X 'POST' \
-H 'Content-Type: application/json' \
-H 'Accept: application/json' \
-H 'x-tenantid: cfd95b7e-3bc7-4006-a4a8-a73a79c71255' \
-H "authorization: Bearer $ZEN_TOKEN"   \
--data-binary '{
    "connection_config": {
        "webhook": {
            "authentication": {
                "type": "none"
            },
            "enabled": true,
            "path": "/webhook-connector/zabbix",
            "mappings": "(\n  {\n      \"severity\": severity=\"5\"?6:severity=\"4\"?5:severity=\"3\"?4:severity=\"2\"?3:severity=\"1\"?2:1,\n      \"summary\": message,\n      \"resource\": {\n          \"name\": deviceName,\n          \"hostname\": hostname,\n          \"ipAddress\": ipaddress,\n          \"sourceId\": hostid,\n          \"port\": hostport\n      },\n      \"type\": {\n          \"classification\": triggerdesc,\n          \"eventType\":  recoveryValue = \"0\" ? \"resolution\" : \"problem\"\n      },\n      \"sender\": {\n          \"name\": \"Zabbix\",\n          \"sourceId\": $exists(actionName) ? $length(actionName) > 0 ? \"Trigger action: \" & actionName,\n          \"type\": \"Webhook Connector\"\n      }\n  }\n)"
        },
        "deploymentType": "local",
        "display_name": "Zabbix-Demo",
        "description": "Automatically created by Nicks scripts",
        "connectionName": "Zabbix-Demo"
    },
    "connectorConfig": {
        "AIModelTypeList": ["{{sidePanel.AIModelTypes.logAnomaly}}"],
        "apiAdaptor": "grpc",
        "categories": ["{{connector.common.category.events}}"],
        "datasourceType": "events",
        "deploymentType": ["local"],
        "displayName": "{{connector.webhook.name}}",
        "hasAIModelType": false,
        "hasOptionalConfig": true,
        "hasOptionalText": false,
        "iconFileType": "svg",
        "isObserver": false,
        "requiresTestConnection": false,
        "sidePanelDescription": "{{connector.webhook.sidepanel.sidePanelDescription}}",
        "sidePanelInfo": ["{{sidePanel.information.webhook.1}}", "{{sidePanel.information.webhook.2}}", "{{sidePanel.information.webhook.3}}"],
        "sidePanelInfoHeader": "{{sidePanel.information.header}}",
        "sidePanelOptionalConfigHeader": "{{sidePanel.webhook.optional.config.header}}",
        "sidePanelOptionalConfigList": ["{{sidePanel.webhook.optional.config.1}}"],
        "sidePanelTitle": "{{connector.webhook.sidepanel.sidePanelTitle}}",
        "type": "webhook",
        "url": "https://ibm.biz/aiops-genwebhook"
    }
}'



# --------------------------------------------------------------------------------------------------------
# ADD KubeCostWebhook-Demo
# --------------------------------------------------------------------------------------------------------
curl "https://$CPD_ROUTE/aiops/integrations/api/controller/grpc/connections/" \
-X 'POST' \
-H 'Content-Type: application/json' \
-H 'Accept: application/json' \
-H 'x-tenantid: cfd95b7e-3bc7-4006-a4a8-a73a79c71255' \
-H "authorization: Bearer $ZEN_TOKEN"   \
--data-binary '{
    "connection_config": {
        "webhook": {
            "authentication": {
                "type": "none"
            },
            "enabled": true,
            "path": "/webhook-connector/kubecost",
            "mappings": "(\n  {\n      \"severity\": 6,\n      \"summary\": text,\n      \"resource\": {\n          \"name\": \"Your Cluster\"\n      },\n      \"type\": {\n          \"classification\": \"kubecost\",\n          \"eventType\":  \"problem\"\n      },\n      \"sender\": {\n          \"name\": \"KubeCost\",\n          \"sourceId\": \"KubeCost\",\n          \"type\": \"Webhook Connector\"\n      }\n  }\n)"
        },
        "deploymentType": "local",
        "display_name": "KubeCostWebhookDemo",
        "description": "Automatically created by Nicks scripts",
        "connectionName": "KubeCostWebhookDemo"
    },
    "connectorConfig": {
        "AIModelTypeList": ["{{sidePanel.AIModelTypes.logAnomaly}}"],
        "apiAdaptor": "grpc",
        "categories": ["{{connector.common.category.events}}"],
        "datasourceType": "events",
        "deploymentType": ["local"],
        "displayName": "{{connector.webhook.name}}",
        "hasAIModelType": false,
        "hasOptionalConfig": true,
        "hasOptionalText": false,
        "iconFileType": "svg",
        "isObserver": false,
        "requiresTestConnection": false,
        "sidePanelDescription": "{{connector.webhook.sidepanel.sidePanelDescription}}",
        "sidePanelInfo": ["{{sidePanel.information.webhook.1}}", "{{sidePanel.information.webhook.2}}", "{{sidePanel.information.webhook.3}}"],
        "sidePanelInfoHeader": "{{sidePanel.information.header}}",
        "sidePanelOptionalConfigHeader": "{{sidePanel.webhook.optional.config.header}}",
        "sidePanelOptionalConfigList": ["{{sidePanel.webhook.optional.config.1}}"],
        "sidePanelTitle": "{{connector.webhook.sidepanel.sidePanelTitle}}",
        "type": "webhook",
        "url": "https://ibm.biz/aiops-genwebhook"
    }
}'




# --------------------------------------------------------------------------------------------------------
# ADD Impact-Demo
# --------------------------------------------------------------------------------------------------------
curl "https://$CPD_ROUTE/aiops/integrations/api/controller/grpc/connections/" \
-X 'POST' \
-H 'Content-Type: application/json' \
-H 'Accept: application/json' \
-H 'x-tenantid: cfd95b7e-3bc7-4006-a4a8-a73a79c71255' \
-H "authorization: Bearer $ZEN_TOKEN"   \
--data-binary '{
    "connection_config": {
        "deploymentType": "local",
        "display_name": "Impact-Demo",
        "url": "https://impact.demo.com:16311",
        "backendUrl": "https://impact.demo.com:9081",
        "username": "admin",
        "password": "admin"
    },
    "connectorConfig": {
        "AIModelTypeList": ["{{connector.impact.sidePanel.AIModelTypes}}"],
        "AIModelTypeListHeader": "{{connector.impact.AIModelTypeListHeader}}",
        "apiAdaptor": "grpc",
        "categories": ["{{connector.common.category.events}}"],
        "datasourceType": "tickets",
        "deploymentType": ["local", "remote"],
        "displayName": "{{connector.impact.name}}",
        "hasAIModelType": true,
        "hasOptionalConfig": false,
        "hasOptionalText": false,
        "iconFileType": "svg",
        "isIBM": true,
        "sidePanelDescription": "{{connector.impact.sidePanelDescription}}",
        "sidePanelInfo": ["{{connector.impact.sidePanelInfo.1}}", "{{connector.impact.sidePanelInfo.2}}", "{{connector.impact.sidePanelInfo.3}}"],
        "sidePanelInfoHeader": "{{sidePanel.information.header}}",
        "sidePanelTitle": "{{connector.impact.sidePanelTitle}}",
        "type": "ibm-grpc-impact-connector",
        "url": "https://ibm.biz/int-impact"
    }
}'



# --------------------------------------------------------------------------------------------------------
# ADD PagerDuty-Demo
# --------------------------------------------------------------------------------------------------------
curl "https://$CPD_ROUTE/aiops/integrations/api/controller/connections/" \
-X 'POST' \
-H 'Content-Type: application/json' \
-H 'Accept: application/json' \
-H 'x-tenantid: cfd95b7e-3bc7-4006-a4a8-a73a79c71255' \
-H "authorization: Bearer $ZEN_TOKEN"   \
--data-binary '{
    "connection_config": {
        "collection_mode": "inference",
        "base_parallelism": 1,
        "sampling_rate": 60,
        "data_flow": true,
        "display_name": "PagerDuty-Demo",
        "token": "aaaaaaaaaa"
    },
    "mapping": {
        "codec": "pagerduty"
    },
    "connectorConfig": {
        "AIModelTypeList": ["{{sidePanel.AIModelTypes.probableCause}}", "{{sidePanel.AIModelTypes.scope_based}}", "{{sidePanel.AIModelTypes.temporal}}", "{{sidePanel.AIModelTypes.topological}}"],
        "categories": ["{{connector.common.category.events}}"],
        "datasourceType": "alerts",
        "deploymentType": ["local"],
        "disabledModule": "logs",
        "displayName": "{{connector.pagerduty.name}}",
        "hasAIModelType": true,
        "hasOptionalConfig": false,
        "hasOptionalText": false,
        "iconFileType": "svg",
        "isObserver": false,
        "sidePanelDescription": "{{connector.pagerduty.sidepanel.description}}",
        "sidePanelInfo": ["{{common.egress_warning}}", "{{sidePanel.information.pagerduty.1}}", "{{sidePanel.information.pagerduty.2}}", "{{sidePanel.information.pagerduty.3}}", "{{sidePanel.information.pagerduty.4}}", "{{sidePanel.information.pagerduty.5}}", "{{sidePanel.information.pagerduty.6}}"],
        "sidePanelInfoHeader": "{{sidePanel.information.header}}",
        "sidePanelTitle": "{{sidePanel.title.pagerduty}}",
        "type": "pagerduty",
        "url": "https://ibm.biz/int-pagerduty"
    }
}'




# --------------------------------------------------------------------------------------------------------
# ADD GitHub-Demo
# --------------------------------------------------------------------------------------------------------
curl "https://$CPD_ROUTE/aiops/integrations/api/controller/grpc/connections/" \
-X 'POST' \
-H 'Content-Type: application/json' \
-H 'Accept: application/json' \
-H 'x-tenantid: cfd95b7e-3bc7-4006-a4a8-a73a79c71255' \
-H "authorization: Bearer $ZEN_TOKEN"   \
--data-binary '{
  "displayName": "GitHub-Demo",
  "connection_type": "github",
  "connection_config": {
    "collectionMode": "live",
    "data_flow": false,
    "issueSamplingRate": 1,
    "mappingsGithub": "({\n    \"title\": $string(incident.title),\n    \"body\": $join([\"Incident Id:\", $string(incident.id),\n                   \"\\nAIOPS Incident Overview URL: https://\", $string(URL_PREFIX), \"/aiops/default/resolution-hub/incidents/all/\", $string(incident.id), \"/overview\",\n                   \"\\nStatus: \", $string(incident.state),\n                   \"\\nDescription: \", $string(incident.description)]),\n    \"labels\": [$join([\"priority:\", $string(incident.priority)])]\n})\n",
    "owner": "niklaushirt",
    "repo": "niklaushirt",
    "token": "",
    "url": "https://github.com/",
    "username": "niklaushirt",
    "display_name": "GitHub-Demo",
    "description": "Automatically created by Nicks scripts",
    "deploymentType": "local"
  },
  "connection_id": "github-demo"
}'


# --------------------------------------------------------------------------------------------------------
# ADD NOI-Objectserver-Test-Demo
# --------------------------------------------------------------------------------------------------------
curl "https://$CPD_ROUTE/aiops/integrations/api/controller/grpc/connections/" \
-X 'POST' \
-H 'Content-Type: application/json' \
-H 'Accept: application/json' \
-H 'x-tenantid: cfd95b7e-3bc7-4006-a4a8-a73a79c71255' \
-H "authorization: Bearer $ZEN_TOKEN"   \
--data-binary '{
    "displayName": "NOI-Objectserver-Test-Demo",
    "description": "Automatically created by Nicks scripts",
    "status": "Disabled",
    "connection_type": "netcool-connector",
    "connection_config": {
        "backup_objectserver": {
            "api_port": 4200
        },
        "collectAlerts": true,
        "filter": "",
        "mapping": "{}",
        "password": "",
        "primary_objectserver": {
            "api_port": 4100,
            "url": "https://primary-objectserver-test.demo.ibm.com"
        },
        "tls": false,
        "username": "nhirt",
        "display_name": "NOI-Objectserver-Test-Demo",
        "description": "Automatically created by Nicks scripts",
        "deploymentType": "local"
    },
    "connection_id": "noiobjectserver-demo-test"
}'


# --------------------------------------------------------------------------------------------------------
# ADD NOI-Objectserver-Prod-Demo
# --------------------------------------------------------------------------------------------------------
curl "https://$CPD_ROUTE/aiops/integrations/api/controller/grpc/connections/" \
-X 'POST' \
-H 'Content-Type: application/json' \
-H 'Accept: application/json' \
-H 'x-tenantid: cfd95b7e-3bc7-4006-a4a8-a73a79c71255' \
-H "authorization: Bearer $ZEN_TOKEN"   \
--data-binary '{
    "displayName": "NOI-Objectserver-Prod-Demo",
    "description": "Automatically created by Nicks scripts",
    "status": "Disabled",
    "connection_type": "netcool-connector",
    "connection_config": {
        "backup_objectserver": {
            "api_port": 4200
        },
        "collectAlerts": true,
        "filter": "",
        "mapping": "{}",
        "password": "",
        "primary_objectserver": {
            "api_port": 4100,
            "url": "https://primary-objectserver-prod.demo.ibm.com"
        },
        "tls": false,
        "username": "nhirt",
        "display_name": "NOI-Objectserver-Prod-Demo",
        "description": "Automatically created by Nicks scripts",
        "deploymentType": "local"
    },
    "connection_id": "noiobjectserver-demo-prod"
}'

# --------------------------------------------------------------------------------------------------------
# ADD NOI-Impact-Demo
# --------------------------------------------------------------------------------------------------------
curl "https://$CPD_ROUTE/aiops/integrations/api/controller/grpc/connections/" \
-X 'POST' \
-H 'Content-Type: application/json' \
-H 'Accept: application/json' \
-H 'x-tenantid: cfd95b7e-3bc7-4006-a4a8-a73a79c71255' \
-H "authorization: Bearer $ZEN_TOKEN"   \
--data-binary '{
    "displayName": "NOI-Impact-Demo",
    "connection_type": "ibm-grpc-impact-connector",
    "connection_config": {
        "backendUrl": "https://primary-objectserver.demo.ibm.com",
        "password": "",
        "url": "https://impact.demo.ibm.com",
        "username": "admin",
        "display_name": "NOIImpactDemo",
        "description": "Automatically created by Nicks scripts",
        "deploymentType": "local"
    },
    "connection_id": "noi-impact-demo"
}'


# --------------------------------------------------------------------------------------------------------
# ADD Instana-Demo
# --------------------------------------------------------------------------------------------------------
curl "https://$CPD_ROUTE/aiops/integrations/api/controller/grpc/connections/" \
-X 'POST' \
-H 'Content-Type: application/json' \
-H 'Accept: application/json' \
-H 'x-tenantid: cfd95b7e-3bc7-4006-a4a8-a73a79c71255' \
-H "authorization: Bearer $ZEN_TOKEN"   \
--data-binary '{
    "connection_config": {
        "deploymentType": "local",
        "topology": {
            "enable_topology_flow": true,
            "time_window": 86400,
            "connection_interval": 600,
            "white_list_pattern": ".*",
            "import_app_perspectives_as_aiops_apps": true
        },
        "event": {
            "enable_event_flow": true,
            "types": ["incident"]
        },
        "metric": {
            "enable_metric_flow": true,
            "plugin_selection_option": "[]",
            "collect_live_data_flow": true,
            "aggregation_interval": 5
        },
        "using_proxy": false,
        "display_name": "Instana-Demo",
        "description": "Automatically created by Nicks scripts",
        "endpoint": "https://instana.demo.ibm.com",
        "api_token": "apitoken"
    },
    "connectorConfig": {
        "AIModelTypeList": ["{{sidePanel.AIModelTypes.probableCause}}", "{{sidePanel.AIModelTypes.temporalCorrelation}}"],
        "apiAdaptor": "grpc",
        "categories": ["{{connector.common.category.events}}", "{{connector.common.category.metrics}}", "{{connector.common.category.topology}}"],
        "datasourceType": "events",
        "deploymentType": ["local", "remote"],
        "displayName": "{{connector.instana.name}}",
        "hasAIModelType": true,
        "hasOptionalConfig": true,
        "hasOptionalText": false,
        "iconFileType": "png",
        "isIBM": true,
        "requiresTestConnection": false,
        "sidePanelDescription": "{{connector.instana.sidepanel.description}}",
        "sidePanelInfo": ["{{sidePanel.information.instana.2}}", "{{sidePanel.information.instana.4}}", "{{sidePanel.information.instana.6}}", "{{sidePanel.information.instana.5}}"],
        "sidePanelInfoHeader": "{{sidePanel.information.header}}",
        "sidePanelOptionalConfigHeader": "{{sidePanel.optional.instana.header}}",
        "sidePanelOptionalConfigList": ["{{sidePanel.optional.instana.topology}}", "{{sidePanel.optional.instana.event}}", "{{sidePanel.optional.instana.metric}}"],
        "sidePanelTitle": "{{sidePanel.title.instana}}",
        "type": "instana",
        "url": "https://ibm.biz/int-instana"
    }
}'








# --------------------------------------------------------------------------------------------------------
# ADD GenericWebhook-Demo
# --------------------------------------------------------------------------------------------------------
curl "https://$CPD_ROUTE/aiops/integrations/api/controller/grpc/connections/" \
-X 'POST' \
-H 'Content-Type: application/json' \
-H 'Accept: application/json' \
-H 'x-tenantid: cfd95b7e-3bc7-4006-a4a8-a73a79c71255' \
-H "authorization: Bearer $ZEN_TOKEN"   \
--data-binary '{
    "connection_config": {
        "webhook": {
            "authentication": {
                "type": "basic_authentication",
                "credentials": {
                    "username": "demo",
                    "password": "demo"
                }
            },
            "enabled": true,
            "path": "/webhook-connector/5596czc2bu8",
            "mappings": "(\n    {\n        \"severity\": risk.severity = \"MINOR\" ? 3 : risk.severity = \"MAJOR\" ? 4 : risk.severity = \"CRITICAL\" ? 6 : risk.severity= \"UNKNOWN\" ? 1 : 2,\n        \"summary\": details,\n        \"resource\": {\n            \"name\": target.displayName,\n            \"sourceId\": target.uuid\n        },\n        \"type\": {\n            \"classification\": target.className,\n            \"eventType\": actionState = \"CLEARED\" ? \"resolution\":actionState = \"SUCCEEDED\" ? \"resolution\" : \"problem\",\n            \"condition\": risk.subCategory\n        },\n        \"sender\": {\n            \"name\": \"IBM Turbonomic\",\n            \"type\": \"Webhook Connector\"\n        }\n    }\n)"
        },
        "deploymentType": "local",
        "display_name": "GenericWebhook-Demo",
        "description": "Automatically created by Nicks scripts",
        "connectionName": "GenericWebhook-Demo"
    },
    "connectorConfig": {
        "AIModelTypeList": ["{{sidePanel.AIModelTypes.logAnomaly}}"],
        "apiAdaptor": "grpc",
        "categories": ["{{connector.common.category.events}}"],
        "datasourceType": "events",
        "deploymentType": ["local"],
        "displayName": "{{connector.webhook.name}}",
        "hasAIModelType": false,
        "hasOptionalConfig": true,
        "hasOptionalText": false,
        "iconFileType": "svg",
        "isObserver": false,
        "requiresTestConnection": false,
        "sidePanelDescription": "{{connector.webhook.sidepanel.sidePanelDescription}}",
        "sidePanelInfo": ["{{sidePanel.information.webhook.1}}", "{{sidePanel.information.webhook.2}}", "{{sidePanel.information.webhook.3}}"],
        "sidePanelInfoHeader": "{{sidePanel.information.header}}",
        "sidePanelOptionalConfigHeader": "{{sidePanel.webhook.optional.config.header}}",
        "sidePanelOptionalConfigList": ["{{sidePanel.webhook.optional.config.1}}"],
        "sidePanelTitle": "{{connector.webhook.sidepanel.sidePanelTitle}}",
        "type": "webhook",
        "url": "https://ibm.biz/aiops-genwebhook"
    }
}'



# --------------------------------------------------------------------------------------------------------
# ADD Email-Demo
# --------------------------------------------------------------------------------------------------------
curl "https://$CPD_ROUTE/aiops/integrations/api/controller/grpc/connections/" \
-X 'POST' \
-H 'Content-Type: application/json' \
-H 'Accept: application/json' \
-H 'x-tenantid: cfd95b7e-3bc7-4006-a4a8-a73a79c71255' \
-H "authorization: Bearer $ZEN_TOKEN"   \
--data-binary '{
    "connection_config": {
        "emailPort": 25,
        "deploymentType": "local",
        "createMappings": "({\n    \"subject\": $join([\"Incident Created: \", $string(incident.title)]),\n    \"message\": $join([\"AIOPS Incident Overview URL: https://\", $string(URL_PREFIX), \"/aiops/default/resolution-hub/incidents/all/\", $string(incident.id), \"/overview\",\n                      \"\\nPriority: \", $string(incident.priority),\n                      \"\\nStatus: \", $string(incident.state),\n                      \"\\nTime opened: \", $string(incident.createdTime),\n                      \"\\nGroup: \", $string(incident.team),\n                      \"\\nOwner: \", $string(incident.owner),\n                      \"\\nDescription: \", $string(incident.description)])\n})\n",
        "closeMappings": "({\n    \"subject\": $join([\"Incident Closed: \", $string(incident.title)]),\n    \"message\": $join([\"Incident ID: \", $string(incident.id),\n                      \"\\nPriority: \", $string(incident.priority),\n                      \"\\nStatus: \", $string(incident.state),\n                      \"\\nTime opened: \", $string(incident.createdTime),\n                      \"\\nGroup: \", $string(incident.team),\n                      \"\\nOwner: \", $string(incident.owner),\n                      \"\\nDescription: \", $string(incident.description)])\n})\n",
        "display_name": "Email-Demo",
        "description": "Automatically created by Nicks scripts",
        "emailHost": "mysmtp.ibm.com",
        "emailSource": "demo@ibm.com",
        "emailSecret": "emailsecret",
        "recipients": "demo@ibm.com"
    },
    "connectorConfig": {
        "apiAdaptor": "grpc",
        "categories": ["{{connector.common.category.notifications}}"],
        "datasourceType": "events",
        "deploymentType": ["local", "remote"],
        "displayName": "{{connector.email.name}}",
        "hasAIModelType": false,
        "hasOptionalConfig": false,
        "hasOptionalText": false,
        "hasOtherConsiderations": true,
        "iconFileType": "svg",
        "isIBM": true,
        "otherConsideration": "{{connector.email.sidePanel.otherConsideration}}",
        "sidePanelDescription": "{{connector.email.sidePanelDescription}}",
        "sidePanelInfo": ["{{connector.email.sidePanelInfo.1}}", "{{connector.email.sidePanelInfo.2}}", "{{connector.email.sidePanelInfo.3}}", "{{connector.email.sidePanelInfo.4}}", "{{connector.email.sidePanelInfo.5}}", "{{connector.email.sidePanelInfo.6}}"],
        "sidePanelInfoHeader": "{{sidePanel.information.header}}",
        "sidePanelTitle": "{{connector.email.sidePanelTitle}}",
        "type": "email-notifications",
        "url": "https://ibm.biz/int-email-notification"
    }
}'


# --------------------------------------------------------------------------------------------------------
# ADD Dynatrace-Demo
# --------------------------------------------------------------------------------------------------------
curl "https://$CPD_ROUTE/aiops/integrations/api/controller/grpc/connections/" \
-X 'POST' \
-H 'Content-Type: application/json' \
-H 'Accept: application/json' \
-H 'x-tenantid: cfd95b7e-3bc7-4006-a4a8-a73a79c71255' \
-H "authorization: Bearer $ZEN_TOKEN"   \
--data-binary '{
    "connection_config": {
        "installationType": "local",
        "authType": "apitoken",
        "vault": {},
        "metrics": {
            "enabled": false,
            "poll_rate": 300
        },
        "events": {
            "enabled": true,
            "poll_rate": 60
        },
        "display_name": "Dynatrace-Demo",
        "description": "Automatically created by Nicks scripts",        
        "dataSourceBaseUrl": "https://dynatrace.demo.ibm.com",
        "zone": "demo",
        "accessToken": "accesstoken",
        "sensorName": "com.instana.plugin.dynatrace"
    },
    "connectorConfig": {
        "AIModelTypeList": ["{{sidePanel.AIModelTypes.metricAnomaly}}"],
        "apiAdaptor": "grpc",
        "categories": ["{{connector.common.category.metrics}}", "{{connector.common.category.events}}"],
        "datasourceType": "metrics,events",
        "deploymentType": ["local", "remote"],
        "displayName": "{{connector.dynatrace.name}}",
        "hasAIModelType": true,
        "hasOptionalConfig": true,
        "hasOptionalText": false,
        "iconFileName": "dynatrace",
        "iconFileType": "svg",
        "interviewExperience": "dynatrace",
        "isCommonCollector": true,
        "isTechnicalPreview": true,
        "sensorMapping": {
            "connection_config.accessToken": "key",
            "connection_config.dataSourceBaseUrl": "endpoint",
            "connection_config.enabled": "enabled",
            "connection_config.events": "events",
            "connection_config.metrics": "metrics",
            "connection_config.tags": "tags",
            "connection_config.vault.secretKey": "key.configuration_from.secret_key.key",
            "connection_config.vault.secretPath": "key.configuration_from.secret_key.path",
            "connection_config.vaultToken": "key.configuration_from.type",
            "connection_config.zone": "zone"
        },
        "sensorName": "com.instana.plugin.dynatrace",
        "sensorVaultPath": "key",
        "sidePanelDescription": "{{sidePanel.dynatrace.cdc.description}}",
        "sidePanelInfo": ["{{sidePanel.information.instana.2}}", "{{connector.common.form.access_token.label}}"],
        "sidePanelInfoHeader": "{{sidePanel.information.header}}",
        "sidePanelOptionalConfigHeader": "{{sidePanel.dynatrace.config.header}}",
        "sidePanelOptionalConfigList": ["{{sidePanel.dynatrace_agent.configList1}}", "{{sidePanel.dynatrace_agent.configList2}}"],
        "sidePanelTitle": "{{connector.dynatrace.sidePanelTitle}}",
        "type": "dynatrace-agent",
        "url": "https://ibm.biz/int-dynatrace-agent"
    }
}'


# --------------------------------------------------------------------------------------------------------
# ADD Slack-Demo
# --------------------------------------------------------------------------------------------------------
curl -X 'POST' --insecure \
"https://$AIO_PLATFORM_ROUTE/v3/connections" \
-H 'accept: application/json' \
-H 'Content-Type: application/json' \
  -H "authorization: Bearer $ZEN_TOKEN"  \
-d '{
    "aiopsedge_id": "null",
    "application_group_id": "1000",
    "application_id": "1000",
    "connection_config": {
      "connection_type": "slack",
      "creator_user_name": "",
      "reactive_channel": "reactivechannel",
      "using_proxy": false,
      "proactive_channel": "proactivechannel",
      "lang_id": "en",
      "bot_token": "bottoken",
      "secret": "signingsecret",
      "display_name": "Slack-Demo",
      "description": "Automatically created by Nicks scripts"
    },
    "connection_id": "443ad7c9-4b99-4172-85a5-9411c0073196",
    "connection_type": "slack",
    "connection_updated_at": "2024-05-24T07:39:08.249386Z",
    "created_at": "null",
    "created_by": "null",
    "data_flow": false,
    "datasource_type": "slack",
    "global_id": "4",
    "mapping": {},
    "name": "null",
    "request_action": "get",
    "state": "null",
    "updated_by": "null"
  }'




# --------------------------------------------------------------------------------------------------------
# ADD Teams-Demo
# --------------------------------------------------------------------------------------------------------
curl -X 'POST' --insecure \
"https://$AIO_PLATFORM_ROUTE/v3/connections" \
-H 'accept: application/json' \
-H 'Content-Type: application/json' \
  -H "authorization: Bearer $ZEN_TOKEN"  \
-d '{
      "aiopsedge_id": "null",
      "application_group_id": "1000",
      "application_id": "1000",
      "connection_config": {
        "connection_type": "teams",
        "creator_user_name": "",
        "reactive_channel": "reactivechannel",
        "using_proxy": false,
        "app_password": "apppassword",
        "proactive_channel": "proactivechannel",
        "lang_id": "en",
        "display_name": "Teams-Demo",
        "description": "Automatically created by Nicks scripts",
        "app_id": "dsafads"
      },
      "connection_id": "3be692db-0fac-4649-baed-9643b0495efd",
      "connection_type": "teams",
      "connection_updated_at": "2024-05-23T10:09:38.339959Z",
      "created_at": "null",
      "created_by": "null",
      "data_flow": false,
      "datasource_type": "teams",
      "global_id": "2",
      "mapping": {},
      "name": "null",
      "request_action": "get",
      "state": "null",
      "updated_by": "null"
    }'













