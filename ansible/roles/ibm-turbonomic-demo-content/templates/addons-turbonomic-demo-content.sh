export TURBO_PASSWORD=CHANGEME




# 🚀 TURBONOMIC - Get ROUTE

    export TURBO_URL=$(oc get route -n turbonomic nginx -o jsonpath={.spec.host})
    echo $TURBO_URL


# 🚀 TURBONOMIC - Init Admin

    echo "------------------------------------------------------------------------------------------------------------------------------"
    echo " 📥 Initialization"

    result=$(curl -XPOST -s -k -c /tmp/cookies -H 'accept: application/json' "https://$TURBO_URL/api/v3/initAdmin" -d "username=administrator&password=$TURBO_PASSWORD")
    echo $result
    result=$(curl -XPOST -s -k -c /tmp/cookies -H 'accept: application/json' "https://$TURBO_URL/api/v3/login?disable_hateoas=true" -d "username=administrator&password=$TURBO_PASSWORD")
    echo $result

        




# 🚀 TURBONOMIC - Login

    echo "------------------------------------------------------------------------------------------------------------------------------"
    echo " 📥 Initialization"
    export TURBO_URL=$TURBO_URL

    while [[ `curl -XPOST -s -k -c /tmp/cookies -H 'accept: application/json' "https://$TURBO_URL/api/v3/login?hateoas=true" -d "username=administrator&password=$TURBO_PASSWORD"` =~ "InvalidCredentialsException" ]]
    do
      echo "Waiting for Turbo Init"
      sleep 15
    done
        







# --------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------
# CREATE DEMO USER
# --------------------------------------------------------------------------------------------------------


# 🚀 TURBONOMIC - Create demo User

    echo "------------------------------------------------------------------------------------------------------------------------------"
    echo " 📥 Create demo User"
    result=$(curl -XPOST -s -k "https://$TURBO_URL/api/v3/users" -b /tmp/cookies  -H 'Content-Type: application/json;' -H 'accept: application/json' -d '  {
      "displayName": "Demo User",
        "username": "{{current_feature.demo_user}}",
        "password": "{{current_demo_pass}}",
        "roles": [
          {
            "name": "ADMINISTRATOR"
          }
        ],
        "loginProvider": "Local",
        "type": "DedicatedCustomer",
        "showSharedUserSC": false
      }
      ')
    echo $result
    echo ""
    echo ""


# --------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------
# CREATE GROUPS
# --------------------------------------------------------------------------------------------------------
# 🚀 TURBONOMIC - Create Group vSphere VMs

    echo "------------------------------------------------------------------------------------------------------------------------------"
    echo " 📥 Create demo User"
    result=$(curl -XPOST -s -k "https://$TURBO_URL/api/v3/groups" -b /tmp/cookies  -H 'Content-Type: application/json;' -H 'accept: application/json' -d '  
      {
        "displayName": "vSphere VMs",
        "className": "Group",
        "groupType": "VirtualMachine",
        "environmentType": "ONPREM",
        "isStatic": false,
        "logicalOperator": "AND",
        "criteriaList": [
          {
            "expVal": "vCenter",
            "expType": "EQ",
            "filterType": "vmByTargetType",
            "caseSensitive": false,
            "entityType": null,
            "singleLine": false
          }
        ],
        "temporary": false,
        "memberTypes": [
          "VirtualMachine"
        ],
        "entityTypes": [
          "VirtualMachine"
        ],
        "groupOrigin": "USER",
        "groupClassName": "GroupApiDTO"
      }
    
      ')
    echo $result
    echo ""
    echo ""



# 🚀 TURBONOMIC - Create Group Azure VMs

    echo "------------------------------------------------------------------------------------------------------------------------------"
    echo " 📥 Create demo User"
    result=$(curl -XPOST -s -k "https://$TURBO_URL/api/v3/groups" -b /tmp/cookies  -H 'Content-Type: application/json;' -H 'accept: application/json' -d '  
      {
        "displayName": "Azure VMs",
        "className": "Group",
        "groupType": "VirtualMachine",
        "environmentType": "ONPREM",
        "isStatic": false,
        "logicalOperator": "AND",
        "criteriaList": [{
            "expVal": "AZURE",
            "expType": "EQ",
            "filterType": "vmsByCloudProvider",
            "caseSensitive": false,
            "entityType": null,
            "singleLine": false
        }],
        "temporary": false,
        "memberTypes": [
          "VirtualMachine"
        ],
        "entityTypes": [
          "VirtualMachine"
        ],
        "groupOrigin": "USER",
        "groupClassName": "GroupApiDTO"
      }
    
      ')
    echo $result
    echo ""
    echo ""


# 🚀 TURBONOMIC - Create Group AWS VMs

    echo "------------------------------------------------------------------------------------------------------------------------------"
    echo " 📥 Create demo User"
    result=$(curl -XPOST -s -k "https://$TURBO_URL/api/v3/groups" -b /tmp/cookies  -H 'Content-Type: application/json;' -H 'accept: application/json' -d '  
      {
        "displayName": "AWS VMs",
        "className": "Group",
        "groupType": "VirtualMachine",
        "environmentType": "ONPREM",
        "isStatic": false,
        "logicalOperator": "AND",
        "criteriaList": [{
            "expVal": "AWS",
            "expType": "EQ",
            "filterType": "vmsByCloudProvider",
            "caseSensitive": false,
            "entityType": null,
            "singleLine": false
        }],
        "temporary": false,
        "memberTypes": [
          "VirtualMachine"
        ],
        "entityTypes": [
          "VirtualMachine"
        ],
        "groupOrigin": "USER",
        "groupClassName": "GroupApiDTO"
      }
    
      ')
    echo $result
    echo ""
    echo ""




# 🚀 TURBONOMIC - Create Group Google VMs

    echo "------------------------------------------------------------------------------------------------------------------------------"
    echo " 📥 Create demo User"
    result=$(curl -XPOST -s -k "https://$TURBO_URL/api/v3/groups" -b /tmp/cookies  -H 'Content-Type: application/json;' -H 'accept: application/json' -d '  
      {
        "displayName": "Google VMs",
        "className": "Group",
        "groupType": "VirtualMachine",
        "environmentType": "ONPREM",
        "isStatic": false,
        "logicalOperator": "AND",
        "criteriaList": [{
            "expVal": "GCP",
            "expType": "EQ",
            "filterType": "vmsByCloudProvider",
            "caseSensitive": false,
            "entityType": null,
            "singleLine": false
        }],
        "temporary": false,
        "memberTypes": [
          "VirtualMachine"
        ],
        "entityTypes": [
          "VirtualMachine"
        ],
        "groupOrigin": "USER",
        "groupClassName": "GroupApiDTO"
      }
    
      ')
    echo $result
    echo ""
    echo ""


# 🚀 TURBONOMIC - Create Group Kubernetes VMs

    echo "------------------------------------------------------------------------------------------------------------------------------"
    echo " 📥 Create demo User"
    result=$(curl -XPOST -s -k "https://$TURBO_URL/api/v3/groups" -b /tmp/cookies  -H 'Content-Type: application/json;' -H 'accept: application/json' -d '  
      {
        "displayName": "Kubernetes VMs",
        "className": "Group",
        "groupType": "VirtualMachine",
        "environmentType": "ONPREM",
        "isStatic": false,
        "logicalOperator": "AND",
        "criteriaList": [
          {
            "expVal": "Kubernetes",
            "expType": "EQ",
            "filterType": "vmByTargetType",
            "caseSensitive": false,
            "entityType": null,
            "singleLine": false
          }
        ],
        "temporary": false,
        "memberTypes": [
          "VirtualMachine"
        ],
        "entityTypes": [
          "VirtualMachine"
        ],
        "groupOrigin": "USER",
        "groupClassName": "GroupApiDTO"
      }
    
      ')
    echo $result
    echo ""
    echo ""


# 🚀 TURBONOMIC - Create Group RobotShop AppComponents

    result=$(curl -s -k -X 'POST' \
      "https://$TURBO_URL/api/v3/groups" -b /tmp/cookies\
      -H 'accept: application/json' \
      -H 'Content-Type: application/json' \
      -d '  
      {
        "displayName": "RobotShopSynthetic AppComponents",
        "className": "Group",
        "groupType": "ApplicationComponent",
        "severity": "NORMAL",
        "environmentType": "HYBRID",
        "isStatic": false,
        "logicalOperator": "AND",
        "criteriaList": [
          {
            "expVal": ".*robot.*",
            "expType": "RXEQ",
            "filterType": "appCompsByName",
            "caseSensitive": false,
            "entityType": null,
            "singleLine": false
          }
        ],
        "temporary": false,
        "cloudType": "UNKNOWN",
        "memberTypes": [
          "ApplicationComponent"
        ],
        "entityTypes": [
          "ApplicationComponent"
        ],
        "groupOrigin": "USER",
        "groupClassName": "GroupApiDTO"
      }
      ')

    echo $result
    echo ""
    echo ""





# 🚀 TURBONOMIC - Create Licensing Groups

    result=$(curl -s -k -X 'POST' \
      "https://$TURBO_URL/api/v3/groups" -b /tmp/cookies\
      -H 'accept: application/json' \
      -H 'Content-Type: application/json' \
      -d ' {
        "displayName": "_DB_LICENSED_HOST",
        "className": "Group",
        "groupType": "PhysicalMachine",
        "severity": "CRITICAL",
        "environmentType": "ONPREM",
        "isStatic": false,
        "logicalOperator": "AND",
        "criteriaList": [
          {
            "expVal": "192.168.10.87",
            "expType": "RXEQ",
            "filterType": "pmsByName",
            "caseSensitive": false,
            "entityType": null,
            "singleLine": false
          }
        ],
        "temporary": false,
        "cloudType": "UNKNOWN",
        "memberTypes": [
          "PhysicalMachine"
        ],
        "entityTypes": [
          "PhysicalMachine"
        ],
        "groupOrigin": "USER",
        "groupClassName": "GroupApiDTO"
      }
      
      ')

    echo $result|jq -r ".displayName"| sed 's/^/     /'
    export sellerUuid=$(echo $result|jq -r ".uuid")
    echo "sellerUuid: $sellerUuid"
    echo ""



    result=$(curl -s -k -X 'POST' \
      "https://$TURBO_URL/api/v3/groups" -b /tmp/cookies\
      -H 'accept: application/json' \
      -H 'Content-Type: application/json' \
      -d '   {
        "displayName": "_DB_VMs",
        "className": "Group",
        "groupType": "VirtualMachine",
        "severity": "NORMAL",
        "environmentType": "HYBRID",
        "isStatic": false,
        "logicalOperator": "AND",
        "criteriaList": [
          {
            "expVal": ".*mysql.*|.*demo.*|.*backend.*",
            "expType": "RXEQ",
            "filterType": "vmsByName",
            "caseSensitive": false,
            "entityType": null,
            "singleLine": false
          }
        ],
        "temporary": false,
        "cloudType": "HYBRID",
        "memberTypes": [
          "VirtualMachine"
        ],
        "entityTypes": [
          "VirtualMachine"
        ],
        "groupOrigin": "USER",
        "groupClassName": "GroupApiDTO"
      }
      ')

    echo $result|jq -r ".displayName"| sed 's/^/     /'
    export buyerUuid=$(echo $result|jq -r ".uuid")
    echo "buyerUuid: $buyerUuid"
    echo ""


    echo "------------------------------------------------------------------------------------------------------------------------------"
    echo " 🚀 Creating License Policy"
    echo "      sellerUuid: $sellerUuid"
    echo "      buyerUuid: $buyerUuid"



    result=$(curl -XPOST -s -k "https://$TURBO_URL/api/v3/markets/777777/policies" -b /tmp/cookies  -H 'Content-Type: application/json;' -H 'accept: application/json' -d '
    {
      "policyName": "_DB_LICENSE",
      "type": "BIND_TO_GROUP_AND_LICENSE",
      "sellerUuid": "'$sellerUuid'",
      "buyerUuid": "'$buyerUuid'",
      "mergeUuids": [
      
      ],
      "mergeType": "Cluster",
      "capacity": 4,
      "enabled": true,
      "providerEntityType": "Application"
    }')

    echo $result|jq -r ".displayName"| sed 's/^/     /'
    echo ""




    result=$(curl -XPOST -s -k "https://$TURBO_URL/api/v3/markets/777777/policies" -b /tmp/cookies  -H 'Content-Type: application/json;' -H 'accept: application/json' -d '
    {
      "policyName": "_DB_PLACE",
      "type": "AT_MOST_N_BOUND",
      "capacity": 4,
      "sellerUuid": "'$sellerUuid'",
      "buyerUuid": "'$buyerUuid'",
      "mergeUuids": [
      
      ],
      "mergeType": "Cluster",
      "capacity": 4,
      "enabled": true,
      "providerEntityType": "Application"
    }')

    echo $result|jq -r ".displayName"| sed 's/^/     /'
    echo ""







# 🚀 TURBONOMIC - Create Schedule and Maintenance Policy

    result=$(curl -s -k -X 'POST' \
      "https://$TURBO_URL/api/v3/schedules" -b /tmp/cookies \
      -H 'accept: application/json' \
      -H 'Content-Type: application/json' \
      -d '  
        {
          "displayName": "MaintenanceFirstSaturdayOfMonth",
          "startTime": "2023-03-29T01:30",
          "endTime": "2023-03-29T02:30",
          "recurrence": {
            "type": "MONTHLY",
            "daysOfWeek": [
              "Sat"
            ],
            "weekOfTheMonth": [
              1
            ],
            "interval": 1
          },
          "timeZone": "Europe/Paris"
        }
      ')

    echo $result
    echo ""
    echo ""





# --------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------
# DEPLOY DIF METRICS ROBOTSHOP
# --------------------------------------------------------------------------------------------------------


# 🚀 TURBONOMIC - Create RobotShop BusinessApp

    echo "------------------------------------------------------------------------------------------------------------------------------"
    echo " 📥 Create demo User"
    result=$(curl -XPOST -s -k "https://$TURBO_URL/api/v3/topologydefinitions" -b /tmp/cookies  -H 'Content-Type: application/json;' -H 'accept: application/json' -d '  
    {
      "uuid": "285815442727328",
      "displayName": "RobotShopSynthetic",
      "contextBased": true,
      "entityType": "BusinessApplication",
      "entityDefinitionData": {
        "manualConnectionData": {
          "Service": {
            "dynamicConnectionCriteria": [{
              "expVal": ".*robot.*",
              "expType": "RXEQ",
              "filterType": "servicesByName",
              "caseSensitive": false,
              "entityType": null,
              "singleLine": false
            }]
          },
          "Namespace": {
            "dynamicConnectionCriteria": [{
              "expVal": ".*robot.*",
              "expType": "RXEQ",
              "filterType": "namespacesByName",
              "caseSensitive": false,
              "entityType": null,
              "singleLine": false
            }]
          },
          "VirtualMachine": {
            "dynamicConnectionCriteria": [{
              "expVal": ".*demo.*|.*robot.*",
              "expType": "RXEQ",
              "filterType": "vmsByName",
              "caseSensitive": false,
              "entityType": null,
              "singleLine": false
            }]
          },
          "ApplicationComponent": {
            "dynamicConnectionCriteria": [{
              "expVal": "*.robot.*",
              "expType": "RXEQ",
              "filterType": "appCompsByName",
              "caseSensitive": false,
              "entityType": null,
              "singleLine": false
            }]
          }
        }
      }
    }

      ')
    echo $result
    echo ""
    echo ""



# 🚀 TURBONOMIC - Deploy Synthetic Metrics Server for DIF

    echo "------------------------------------------------------------------------------------------------------------------------------"
    echo " 🚀 Deploy Synthetic Metrics Server for DIF"
    oc apply -f ./roles/ibm-turbonomic-demo-content/templates/create-data-ingestion.yaml
    echo ""
    echo ""
    export robotshopUUID=$(curl -XGET -s -k "https://$TURBO_URL/api/v3/topologydefinitions" -b /tmp/cookies  -H 'Content-Type: application/json;' -H 'accept: application/json'|jq -r '.[]|select(.displayName=="RobotShopSynthetic").uuid')
    echo "  🌏 Synthetic Metric URL: http://turbo-dif-service.default:3000/businessApplication/RobotShopSynthetic/$robotshopUUID"
    echo ""
    echo ""




# 🚀 TURBONOMIC - Create SyntheticMetricsHelloWorld

    echo "------------------------------------------------------------------------------------------------------------------------------"
    echo " 📥 Create Hello Metrics"
    result=$(curl -XPOST -s -k "https://$TURBO_URL/api/v3/targets" -b /tmp/cookies  -H 'Content-Type: application/json;' -H 'accept: application/json' -d '{
        "uuid": "74709421524256",
        "displayName": "SyntheticMetricsHelloWorld",
        "category": "Custom",
        "inputFields": [
          {
            "name": "Name",
            "value": "Hello"
          },
          {
            "name": "targetIdentifier",
            "value": "http://turbo-metrics-dif-service.turbonomic:3000/helloworld"
          }
        ],
        "type": "DataIngestionFramework-Turbonomic",
        "readonly": false
      }')

    echo $result
    echo ""
    echo ""



# 🚀 TURBONOMIC - Create SyntheticMetricsRobotShop

    echo "------------------------------------------------------------------------------------------------------------------------------"
    echo " 📥 Create RobotShop Metrics"
    export robotshopUUID=$(curl -XGET -s -k "https://$TURBO_URL/api/v3/topologydefinitions" -b /tmp/cookies  -H 'Content-Type: application/json;' -H 'accept: application/json'|jq -r '.[]|select(.displayName=="RobotShopSynthetic").uuid')

    result=$(curl -XPOST -s -k "https://$TURBO_URL/api/v3/targets" -b /tmp/cookies  -H 'Content-Type: application/json;' -H 'accept: application/json' -d '{
        "uuid": "74709422922224",
        "displayName": "SyntheticMetricsRobotShop",
        "category": "Custom",
        "inputFields": [
          {
            "name": "Name",
            "value": "RobotShopSynthetic"
          },
          {
            "name": "targetIdentifier",
            "value": "http://turbo-metrics-dif-service.turbonomic:3000/businessApplication/RobotShopSynthetic/'$robotshopUUID'"
          }
        ],
        "type": "DataIngestionFramework-Turbonomic",
        "readonly": false
        }
      }')

    echo $result
    echo ""
    echo ""







# --------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------
# DEPLOY MEMORY AND CPU HOGS
# --------------------------------------------------------------------------------------------------------

# 🚀 TURBONOMIC - Deploy Memory and CPU Hogs

    echo "------------------------------------------------------------------------------------------------------------------------------"
    echo " 🚀 Deploy Memory and CPU Hogs"
    oc apply  -f ./roles/ibm-turbonomic-demo-content/templates/prime_numbers-deploy.yaml
    oc apply  -f ./roles/ibm-turbonomic-demo-content/templates/memory_grabber.yaml
    echo ""
    echo ""




# --------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------
# WEBHOOKS
# --------------------------------------------------------------------------------------------------------

# 🚀 TURBONOMIC - Sample Webhook

    echo "------------------------------------------------------------------------------------------------------------------------------"
    echo " 🚀 Deploy Sample Webhook"

    result=$(curl -XPOST -s -k "https://$TURBO_URL/api/v3/workflows" -b /tmp/cookies  -H 'Content-Type: application/json;' -H 'accept: application/json' -d ' {
        "displayName": "My_WebHook",
        "className": "Workflow",
        "description": "My First Webhook",
        "discoveredBy":
        {
            "readonly": false
        },
       "type": "WEBHOOK",
       "typeSpecificDetails": {
       "url": "http://ibm.com",
          "method": "POST",
          "template": "My Webhook Template -- DATA: Action Details: $action.details",
          "type": "WebhookApiDTO"
       }
    }')

    echo $result
    echo ""
    echo ""



# 💊 CERTIFICATES - Patch Certificates for TechZone IPI/UPI

    CLUSTER_ROUTE=$(oc get routes console -n openshift-console | tail -n 1 2>&1 )
    CLUSTER_FQDN=$( echo $CLUSTER_ROUTE | awk '{print $2}')
    CLUSTER_NAME=${CLUSTER_FQDN##*console.}


    if [[ $CLUSTER_NAME =~ "cloud.techzone.ibm.com" ]];
    then
        echo "✅ Seems that you're on Techzone IPI/UPI"  
        echo "✅ Let's patch the certificates"  

        echo "Extracting signed cert"
        oc get secret -n openshift-ingress letsencrypt-certs -o jsonpath='{.data.tls\.crt}'| base64 -d > cert.crt
        oc get secret -n openshift-ingress letsencrypt-certs -o jsonpath='{.data.tls\.key}'| base64 -d > cert.key

        oc create secret tls -n turbonomic nginx-ingressgateway-certs --cert=cert.crt --key=cert.key --dry-run=client -o yaml | oc apply -f -


        REPLICAS=$(oc get pods -n turbonomic |grep nginx|wc -l |xargs)
        oc scale Deployment/nginx --replicas=0 -n turbonomic
        sleep 10
        oc scale Deployment/nginx --replicas=${REPLICAS} -n turbonomic
    else
        echo "✅ Seems that you're NOT on Techzone IPI/UPI"  
        echo "✅ No need to patch the certificates any further"  
    fi













# 🚀 TURBONOMIC - Create RobotShop Optimisation Automation

    curl -XPOST -s -k "https://$TURBO_URL/api/v3/settingspolicies" -b /tmp/cookies  -H 'Content-Type: application/json;' -H 'accept: application/json' \
            -d '{
      "disabled": false,
      "entityType": "WorkloadController",
      "displayName": "RobotShop Automatic Optimization",
      "scopes": [{
          "uuid": "286812328290544"
      }],
      "settingsManagers": [{
          "uuid": "automationmanager",
          "displayName": "Action Mode Settings",
          "category": "Automation",
          "settings": [{
              "uuid": "resizeCPULimitUp",
              "value": "AUTOMATIC",
              "valueType": "STRING",
              "valueObjectType": "String",
              "defaultValue": "MANUAL",
              "entityType": "WorkloadController",
              "displayName": "VCPU Limit Resize up",
              "options": [{
                  "label": "Recommend",
                  "value": "RECOMMEND"
              }, {
                  "label": "External Approval",
                  "value": "EXTERNAL_APPROVAL"
              }, {
                  "label": "Manual",
                  "value": "MANUAL"
              }, {
                  "label": "Automatic",
                  "value": "AUTOMATIC"
              }]
          }, {
              "uuid": "resizeMemRequestDown",
              "value": "AUTOMATIC",
              "valueType": "STRING",
              "valueObjectType": "String",
              "defaultValue": "MANUAL",
              "entityType": "WorkloadController",
              "displayName": "VMEM Request Resize down",
              "options": [{
                  "label": "Recommend",
                  "value": "RECOMMEND"
              }, {
                  "label": "External Approval",
                  "value": "EXTERNAL_APPROVAL"
              }, {
                  "label": "Manual",
                  "value": "MANUAL"
              }, {
                  "label": "Automatic",
                  "value": "AUTOMATIC"
              }]
          }, {
              "uuid": "resizeMemLimitDown",
              "value": "AUTOMATIC",
              "valueType": "STRING",
              "valueObjectType": "String",
              "defaultValue": "MANUAL",
              "entityType": "WorkloadController",
              "displayName": "VMEM Limit Resize down",
              "options": [{
                  "label": "Recommend",
                  "value": "RECOMMEND"
              }, {
                  "label": "External Approval",
                  "value": "EXTERNAL_APPROVAL"
              }, {
                  "label": "Manual",
                  "value": "MANUAL"
              }, {
                  "label": "Automatic",
                  "value": "AUTOMATIC"
              }]
          }, {
              "uuid": "resizeMemLimitUp",
              "value": "AUTOMATIC",
              "valueType": "STRING",
              "valueObjectType": "String",
              "defaultValue": "MANUAL",
              "entityType": "WorkloadController",
              "displayName": "VMEM Limit Resize up",
              "options": [{
                  "label": "Recommend",
                  "value": "RECOMMEND"
              }, {
                  "label": "External Approval",
                  "value": "EXTERNAL_APPROVAL"
              }, {
                  "label": "Manual",
                  "value": "MANUAL"
              }, {
                  "label": "Automatic",
                  "value": "AUTOMATIC"
              }]
          }, {
              "uuid": "resizeCPURequestDown",
              "value": "AUTOMATIC",
              "valueType": "STRING",
              "valueObjectType": "String",
              "defaultValue": "MANUAL",
              "entityType": "WorkloadController",
              "displayName": "VCPU Request Resize down",
              "options": [{
                  "label": "Recommend",
                  "value": "RECOMMEND"
              }, {
                  "label": "External Approval",
                  "value": "EXTERNAL_APPROVAL"
              }, {
                  "label": "Manual",
                  "value": "MANUAL"
              }, {
                  "label": "Automatic",
                  "value": "AUTOMATIC"
              }]
          }, {
              "uuid": "resizeCPULimitDown",
              "value": "AUTOMATIC",
              "valueType": "STRING",
              "valueObjectType": "String",
              "defaultValue": "MANUAL",
              "entityType": "WorkloadController",
              "displayName": "VCPU Limit Resize down",
              "options": [{
                  "label": "Recommend",
                  "value": "RECOMMEND"
              }, {
                  "label": "External Approval",
                  "value": "EXTERNAL_APPROVAL"
              }, {
                  "label": "Manual",
                  "value": "MANUAL"
              }, {
                  "label": "Automatic",
                  "value": "AUTOMATIC"
              }]
          }]
      }]
    }'


    result=$(curl -s -k -X 'POST' \
      "https://$TURBO_URL/api/v3/groups" -b /tmp/cookies\
      -H 'accept: application/json' \
      -H 'Content-Type: application/json' \
      -d '  
      {
        "displayName": "RobotShop Workload Controllers",
        "className": "Group",
        "groupType": "WorkloadController",
        "severity": "CRITICAL",
        "environmentType": "HYBRID",
        "isStatic": false,
        "logicalOperator": "AND",
        "criteriaList": [
      {
        "expVal": "robot-shop",
        "expType": "EQ",
        "filterType": "workloadControllersByNamespace",
        "caseSensitive": false,
        "entityType": null,
        "singleLine": false
      }
        ],
        "temporary": false,
        "cloudType": "UNKNOWN",
        "memberTypes": [
          "WorkloadController"
        ],
        "entityTypes": [
          "WorkloadController"
        ],
        "groupOrigin": "USER",
        "groupClassName": "GroupApiDTO"
      }
      ')

    echo $result


