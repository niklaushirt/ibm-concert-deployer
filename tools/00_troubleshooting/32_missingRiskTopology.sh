# --------------------------------------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------------------------------
# LOAD RISK TOPOLOGY
# --------------------------------------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------------------------------


# --------------------------------------------------------------------------------------------------------------------------------------------------
# LOAD RISK TOPOLOGY - US BIG

echo "----------------------------------------------------------------------------------------------------------"
echo "----------------------------------------------------------------------------------------------------------"
echo "🚀 TOPOLOGY - COPY RISK TOPOLOGY TO POD"
echo "----------------------------------------------------------------------------------------------------------"
echo "Create Custom Topology - Copy Topology to File Observer"

export AIOPS_NAMESPACE=$(oc get po -A|grep aiops-orchestrator-controller |awk '{print$1}')

export TOPOLOGY_NAME=risk-proximity
cd ibm-aiops-deployer/ansible

# Get FILE_OBSERVER_POD
FILE_OBSERVER_POD=$(oc get po -n $AIOPS_NAMESPACE -l app.kubernetes.io/instance=aiops-topology,app.kubernetes.io/name=file-observer -o jsonpath='{.items[0].metadata.name}')
echo $FILE_OBSERVER_POD
LOAD_FILE_NAME=$TOPOLOGY_NAME"-file.txt"

FILE_OBSERVER_CAP=$(pwd)"/roles/ibm-aiops-demo-content/templates/topology/$LOAD_FILE_NAME"


echo $FILE_OBSERVER_POD
echo $FILE_OBSERVER_CAP
echo $TARGET_FILE_PATH
TARGET_FILE_PATH="/opt/ibm/netcool/asm/data/file-observer/${LOAD_FILE_NAME}"
echo "  Copying capture file [${FILE_OBSERVER_CAP}] to file observer pod"
echo "oc cp -n $AIOPS_NAMESPACE ${FILE_OBSERVER_CAP} ${FILE_OBSERVER_POD}:${TARGET_FILE_PATH}"
oc cp -n $AIOPS_NAMESPACE ${FILE_OBSERVER_CAP} ${FILE_OBSERVER_POD}:${TARGET_FILE_PATH}






echo "----------------------------------------------------------------------------------------------------------"
echo "----------------------------------------------------------------------------------------------------------"
echo "🚀 TOPOLOGY - CREATE OVERLAY TOPOLOGY - $TOPOLOGY_NAME"
echo "----------------------------------------------------------------------------------------------------------"
echo "Create Custom Topology - Create File Observer Job"


export AIOPS_NAMESPACE=$(oc get po -A|grep aiops-orchestrator-controller |awk '{print$1}')
LOAD_FILE_NAME=$TOPOLOGY_NAME"-file.txt"
TARGET_FILE_PATH="/opt/ibm/netcool/asm/data/file-observer/${LOAD_FILE_NAME}"


# Get Credentials
export TOPO_REST_USR=$(oc get secret aiops-topology-asm-credentials -n $AIOPS_NAMESPACE -o jsonpath='{.data.username}' | base64 --decode)
export TOPO_REST_PWD=$(oc get secret aiops-topology-asm-credentials -n $AIOPS_NAMESPACE -o jsonpath='{.data.password}' | base64 --decode)
export LOGIN="$TOPO_REST_USR:$TOPO_REST_PWD"

export TOPO_ROUTE="https://"$(oc get route -n $AIOPS_NAMESPACE aiops-topology-file-observer -o jsonpath={.spec.host})
export JOB_ID=$TOPOLOGY_NAME"-topology"

echo "  URL: $TOPO_ROUTE"
echo "  LOGIN: $LOGIN"
echo "  JOB_ID: $JOB_ID"


# Get FILE_OBSERVER JOB
curl -X "POST" "$TOPO_ROUTE/1.0/file-observer/jobs" --insecure \
  -H 'X-TenantID: cfd95b7e-3bc7-4006-a4a8-a73a79c71255' \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -u $LOGIN \
  -d "{
  \"unique_id\": \"${JOB_ID}\",
  \"description\": \"Automatically created by Nicks scripts\",
  \"parameters\": {
      \"file\": \"${TARGET_FILE_PATH}\"
      }
  }"


sleep 10




# --------------------------------------------------------------------------------------------------------------------------------------------------
# LOAD RISK TOPOLOGY - US NETWORK

echo "----------------------------------------------------------------------------------------------------------"
echo "----------------------------------------------------------------------------------------------------------"
echo "🚀 TOPOLOGY - COPY US NETWORK RISK TOPOLOGY TO POD"
echo "----------------------------------------------------------------------------------------------------------"
echo "Create Custom Topology - Copy Topology to File Observer"

export AIOPS_NAMESPACE=$(oc get po -A|grep aiops-orchestrator-controller |awk '{print$1}')


export TOPOLOGY_NAME=us-network-risk
cd ibm-aiops-deployer/ansible

# Get FILE_OBSERVER_POD
FILE_OBSERVER_POD=$(oc get po -n $AIOPS_NAMESPACE -l app.kubernetes.io/instance=aiops-topology,app.kubernetes.io/name=file-observer -o jsonpath='{.items[0].metadata.name}')
echo $FILE_OBSERVER_POD
LOAD_FILE_NAME=$TOPOLOGY_NAME"-file.txt"

FILE_OBSERVER_CAP=$(pwd)"/roles/ibm-aiops-demo-content/templates/topology/$LOAD_FILE_NAME"

echo $FILE_OBSERVER_POD
echo $FILE_OBSERVER_CAP
echo $TARGET_FILE_PATH
TARGET_FILE_PATH="/opt/ibm/netcool/asm/data/file-observer/${LOAD_FILE_NAME}"
echo "  Copying capture file [${FILE_OBSERVER_CAP}] to file observer pod"
echo "oc cp -n $AIOPS_NAMESPACE ${FILE_OBSERVER_CAP} ${FILE_OBSERVER_POD}:${TARGET_FILE_PATH}"
oc cp -n $AIOPS_NAMESPACE ${FILE_OBSERVER_CAP} ${FILE_OBSERVER_POD}:${TARGET_FILE_PATH}






echo "----------------------------------------------------------------------------------------------------------"
echo "----------------------------------------------------------------------------------------------------------"
echo "🚀 TOPOLOGY - CREATE OVERLAY TOPOLOGY - $TOPOLOGY_NAME"
echo "----------------------------------------------------------------------------------------------------------"
echo "Create Custom Topology - Create File Observer Job"


export AIOPS_NAMESPACE=$(oc get po -A|grep aiops-orchestrator-controller |awk '{print$1}')
LOAD_FILE_NAME=$TOPOLOGY_NAME"-file.txt"
TARGET_FILE_PATH="/opt/ibm/netcool/asm/data/file-observer/${LOAD_FILE_NAME}"


# Get Credentials
export TOPO_REST_USR=$(oc get secret aiops-topology-asm-credentials -n $AIOPS_NAMESPACE -o jsonpath='{.data.username}' | base64 --decode)
export TOPO_REST_PWD=$(oc get secret aiops-topology-asm-credentials -n $AIOPS_NAMESPACE -o jsonpath='{.data.password}' | base64 --decode)
export LOGIN="$TOPO_REST_USR:$TOPO_REST_PWD"

export TOPO_ROUTE="https://"$(oc get route -n $AIOPS_NAMESPACE aiops-topology-file-observer -o jsonpath={.spec.host})
export JOB_ID=$TOPOLOGY_NAME"-topology"

echo "  URL: $TOPO_ROUTE"
echo "  LOGIN: $LOGIN"
echo "  JOB_ID: $JOB_ID"


# Get FILE_OBSERVER JOB
curl -X "POST" "$TOPO_ROUTE/1.0/file-observer/jobs" --insecure \
  -H 'X-TenantID: cfd95b7e-3bc7-4006-a4a8-a73a79c71255' \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -u $LOGIN \
  -d "{
  \"unique_id\": \"${JOB_ID}\",
  \"description\": \"Automatically created by Nicks scripts\",
  \"parameters\": {
      \"file\": \"${TARGET_FILE_PATH}\"
      }
  }"


sleep 10




# --------------------------------------------------------------------------------------------------------------------------------------------------
# LOAD RISK TOPOLOGY - EU

echo "----------------------------------------------------------------------------------------------------------"
echo "----------------------------------------------------------------------------------------------------------"
echo "🚀 TOPOLOGY - COPY EU RISK TOPOLOGY TO POD"
echo "----------------------------------------------------------------------------------------------------------"

export AIOPS_NAMESPACE=$(oc get po -A|grep aiops-orchestrator-controller |awk '{print$1}')

echo "Create Custom Topology - Copy Topology to File Observer"

export TOPOLOGY_NAME=risk-proximity-EU
cd ibm-aiops-deployer/ansible

# Get FILE_OBSERVER_POD
FILE_OBSERVER_POD=$(oc get po -n $AIOPS_NAMESPACE -l app.kubernetes.io/instance=aiops-topology,app.kubernetes.io/name=file-observer -o jsonpath='{.items[0].metadata.name}')
echo $FILE_OBSERVER_POD
LOAD_FILE_NAME=$TOPOLOGY_NAME"-file.txt"

FILE_OBSERVER_CAP=$(pwd)"/roles/ibm-aiops-demo-content/templates/topology/$LOAD_FILE_NAME"

echo $FILE_OBSERVER_POD
echo $FILE_OBSERVER_CAP
echo $TARGET_FILE_PATH
TARGET_FILE_PATH="/opt/ibm/netcool/asm/data/file-observer/${LOAD_FILE_NAME}"
echo "  Copying capture file [${FILE_OBSERVER_CAP}] to file observer pod"
echo "oc cp -n $AIOPS_NAMESPACE ${FILE_OBSERVER_CAP} ${FILE_OBSERVER_POD}:${TARGET_FILE_PATH}"
oc cp -n $AIOPS_NAMESPACE ${FILE_OBSERVER_CAP} ${FILE_OBSERVER_POD}:${TARGET_FILE_PATH}






echo "----------------------------------------------------------------------------------------------------------"
echo "----------------------------------------------------------------------------------------------------------"
echo "🚀 TOPOLOGY - CREATE EU OVERLAY TOPOLOGY - $TOPOLOGY_NAME"
echo "----------------------------------------------------------------------------------------------------------"
echo "Create Custom Topology - Create File Observer Job"


export AIOPS_NAMESPACE=$(oc get po -A|grep aiops-orchestrator-controller |awk '{print$1}')
LOAD_FILE_NAME=$TOPOLOGY_NAME"-file.txt"
TARGET_FILE_PATH="/opt/ibm/netcool/asm/data/file-observer/${LOAD_FILE_NAME}"


# Get Credentials
export TOPO_REST_USR=$(oc get secret aiops-topology-asm-credentials -n $AIOPS_NAMESPACE -o jsonpath='{.data.username}' | base64 --decode)
export TOPO_REST_PWD=$(oc get secret aiops-topology-asm-credentials -n $AIOPS_NAMESPACE -o jsonpath='{.data.password}' | base64 --decode)
export LOGIN="$TOPO_REST_USR:$TOPO_REST_PWD"

export TOPO_ROUTE="https://"$(oc get route -n $AIOPS_NAMESPACE aiops-topology-file-observer -o jsonpath={.spec.host})
export JOB_ID=$TOPOLOGY_NAME"-topology"

echo "  URL: $TOPO_ROUTE"
echo "  LOGIN: $LOGIN"
echo "  JOB_ID: $JOB_ID"


# Get FILE_OBSERVER JOB
curl -X "POST" "$TOPO_ROUTE/1.0/file-observer/jobs" --insecure \
  -H 'X-TenantID: cfd95b7e-3bc7-4006-a4a8-a73a79c71255' \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -u $LOGIN \
  -d "{
  \"unique_id\": \"${JOB_ID}\",
  \"description\": \"Automatically created by Nicks scripts\",
  \"parameters\": {
      \"file\": \"${TARGET_FILE_PATH}\"
      }
  }"


sleep 10









# --------------------------------------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------------------------------
# CRATE FILTERS
# --------------------------------------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------------------------------





export AIOPS_NAMESPACE=$(oc get po -A|grep aiops-orchestrator-controller |awk '{print$1}')
export CONSOLE_ROUTE=$(oc get route -n $AIOPS_NAMESPACE cp-console  -o jsonpath={.spec.host})          
export CPD_ROUTE=$(oc get route -n $AIOPS_NAMESPACE cpd  -o jsonpath={.spec.host})          
export CPADMIN_PWD=$(oc -n $AIOPS_NAMESPACE get secret platform-auth-idp-credentials -o jsonpath='{.data.admin_password}' | base64 -d && echo)
export CPADMIN_USER=$(oc -n $AIOPS_NAMESPACE get secret platform-auth-idp-credentials -o jsonpath='{.data.admin_username}' | base64 -d && echo)
export ACCESS_TOKEN=$(curl -s -k -H "Content-Type: application/x-www-form-urlencoded;charset=UTF-8" -d "grant_type=password&username=$CPADMIN_USER&password=$CPADMIN_PWD&scope=openid" https://$CONSOLE_ROUTE/idprovider/v1/auth/identitytoken|jq -r '.access_token')
export ZEN_API_HOST=$(oc get route -n $AIOPS_NAMESPACE cpd -o jsonpath='{.spec.host}')
export ZEN_TOKEN=$(curl -k -XGET https://$ZEN_API_HOST/v1/preauth/validateAuth \
-H "username: $CPADMIN_USER" \
-H "iam-token: $ACCESS_TOKEN"|jq -r '.accessToken')
echo $ZEN_TOKEN

export ROUTE=$(oc get route -n $AIOPS_NAMESPACE cpd -o jsonpath={.spec.host})


# curl "https://$ROUTE/api/p/hdm_asm_ui_api/1.0/ui-api/userconfig/filters" \
# -X 'GET' \
# -H 'content-type: application/json' \
# -H 'accept: */*' \
# -H 'content-type: application/json' \
# -H "Cookie: ___tk67142224=1655282500640; ibm-private-cloud-session=$ZEN_TOKEN" 



curl "https://$ROUTE/api/p/hdm_asm_ui_api/1.0/ui-api/userconfig/filters" \
-X 'POST' \
-H 'content-type: application/json' \
-H 'accept: */*' \
-H 'content-type: application/json' \
-H "Cookie: ___tk67142224=1655282500640; ibm-private-cloud-session=$ZEN_TOKEN" \
-d '{ 
        "name": "Country: USA",
        "description": "Automatically created by Nicks scripts",
        "type": "inventory",
        "mode": "basic",
        "accessControlList": {
            "read": {
                "teams": [],
                "users": [
                    "*"
                ]
            },
            "admin": {
                "teams": [],
                "users": [
                    "demo"
                ]
            },
            "write": {
                "teams": [],
                "users": []
            }
        },
    "conditionSet": {
    "conditions": [
        {
        "id": "geoLocationCondition",
        "type": "condition",
        "field": "geolocation",
        "value": "POLYGON ((-124.980469 48.516604, -123.222656 48.370848, -123.046875 49.066668, -94.526367 49.037868, -89.516602 47.960502, -82.617188 45.367584, -82.529297 41.738528, -71.367188 45.305803, -69.169922 47.428087, -67.104492 44.527843, -80.683594 30.600094, -79.365234 25.045792, -82.397461 25.363882, -84.506836 29.496988, -89.516602 28.806174, -94.394531 29.075375, -97.646484 26.037042, -102.392578 29.840644, -117.597656 32.398516, -124.453125 40.111689, -124.980469 48.516604))",
        "operator": "contains"
        }
    ]
    }
}'



curl "https://$ROUTE/api/p/hdm_asm_ui_api/1.0/ui-api/userconfig/filters" \
-X 'POST' \
-H 'content-type: application/json' \
-H 'accept: */*' \
-H 'content-type: application/json' \
-H "Cookie: ___tk67142224=1655282500640; ibm-private-cloud-session=$ZEN_TOKEN" \
-d '{ 
        "name": "Region: Western Europe",
        "description": "Automatically created by Nicks scripts",
        "type": "inventory",
        "mode": "basic",
        "accessControlList": {
            "read": {
                "teams": [],
                "users": [
                    "*"
                ]
            },
            "admin": {
                "teams": [],
                "users": [
                    "demo"
                ]
            },
            "write": {
                "teams": [],
                "users": []
            }
        },
    "conditionSet": {
    "conditions": [
        {
        "id": "geoLocationCondition",
        "type": "condition",
        "field": "geolocation",
        "value": "POLYGON ((-12.480469 43.261206, -6.855469 35.137879, 10.898438 37.857507, 18.632813 35.603719, 25.664063 35.56798, 28.476563 39.232253, 30.629883 44.308127, 30.498047 47.487513, 20.874023 55.9492, 15.380859 55.776573, 3.603516 55.128649, -2.724609 61.648162, -12.744141 59.623325, -12.480469 43.261206))",
        "operator": "contains"
        }
    ]
    }
}'




curl "https://$ROUTE/api/p/hdm_asm_ui_api/1.0/ui-api/userconfig/filters" \
-X 'POST' \
-H 'content-type: application/json' \
-H 'accept: */*' \
-H 'content-type: application/json' \
-H "Cookie: ___tk67142224=1655282500640; ibm-private-cloud-session=$ZEN_TOKEN" \
-d '{ 
        "name": "Country: Switzerland",
        "description": "Automatically created by Nicks scripts",
        "type": "inventory",
        "mode": "basic",
        "accessControlList": {
            "read": {
                "teams": [],
                "users": [
                    "*"
                ]
            },
            "admin": {
                "teams": [],
                "users": [
                    "demo"
                ]
            },
            "write": {
                "teams": [],
                "users": []
            }
        },
    "conditionSet": {
    "conditions": [
        {
        "id": "geoLocationCondition",
        "type": "condition",
        "field": "geolocation",
        "value": "POLYGON ((9.008789 45.847934, 8.432007 46.452997, 8.00354 46.035109, 7.108154 45.867063, 6.729126 46.418926, 5.987549 46.103709, 6.053467 46.592844, 6.899414 47.282956, 6.866455 47.390912, 6.987305 47.513491, 7.190552 47.513491, 7.432251 47.483801, 7.613525 47.591346, 8.223267 47.609867, 8.448486 47.576526, 8.410034 47.713458, 8.55835 47.809465, 8.909912 47.646887, 9.18457 47.669087, 9.569092 47.528329, 9.651489 47.379754, 9.442749 47.058896, 9.865723 47.021461, 10.217285 46.863947, 10.387573 46.995241, 10.48645 46.871458, 10.409546 46.641894, 10.508423 46.607941, 10.447998 46.490829, 10.228271 46.607941, 10.063477 46.430285, 10.184326 46.29002, 10.079956 46.214051, 9.931641 46.362093, 9.536133 46.301406, 9.420776 46.475699, 9.30542 46.418926, 9.272461 46.221652, 9.102173 46.118942, 9.008789 45.847934))",
        "operator": "contains"
        }
    ]
    }
}'





curl "https://$ROUTE/api/p/hdm_asm_ui_api/1.0/ui-api/userconfig/filters" \
-X 'POST' \
-H 'content-type: application/json' \
-H 'accept: */*' \
-H 'content-type: application/json' \
-H "Cookie: ___tk67142224=1655282500640; ibm-private-cloud-session=$ZEN_TOKEN" \
-d '{ 
        "name": "Area: Berne",
        "description": "Automatically created by Nicks scripts",
        "type": "inventory",
        "mode": "basic",
        "accessControlList": {
            "read": {
                "teams": [],
                "users": [
                    "*"
                ]
            },
            "admin": {
                "teams": [],
                "users": [
                    "demo"
                ]
            },
            "write": {
                "teams": [],
                "users": []
            }
        },
    "conditionSet": {
    "conditions": [
        {
        "id": "geoLocationCondition",
        "type": "condition",
        "field": "geolocation",
        "value": "POLYGON ((7.385216 46.957996, 7.400322 46.901258, 7.534904 46.889997, 7.57576 46.906653, 7.584 46.974396, 7.551727 47.018653, 7.436714 47.030823, 7.385216 46.957996))",
        "operator": "contains"
        }
    ]
    }
}'




curl "https://$ROUTE/api/p/hdm_asm_ui_api/1.0/ui-api/userconfig/filters" \
-X 'POST' \
-H 'content-type: application/json' \
-H 'accept: */*' \
-H 'content-type: application/json' \
-H "Cookie: ___tk67142224=1655282500640; ibm-private-cloud-session=$ZEN_TOKEN" \
-d '{ 
        "name": "Area: London",
        "description": "Automatically created by Nicks scripts",
        "type": "inventory",
        "mode": "basic",
        "accessControlList": {
            "read": {
                "teams": [],
                "users": [
                    "*"
                ]
            },
            "admin": {
                "teams": [],
                "users": [
                    "demo"
                ]
            },
            "write": {
                "teams": [],
                "users": []
            }
        },
    "conditionSet": {
    "conditions": [
        {
        "id": "geoLocationCondition",
        "type": "condition",
        "field": "geolocation",
        "value": "POLYGON ((-0.181274 51.261915, -0.532837 51.409486, -0.494385 51.679368, 0.087891 51.68618, 0.291138 51.556582, 0.175781 51.28597, -0.181274 51.261915))",
        "operator": "contains"
        }
    ]
    }
}'



curl "https://$ROUTE/api/p/hdm_asm_ui_api/1.0/ui-api/userconfig/filters" \
-X 'POST' \
-H 'content-type: application/json' \
-H 'accept: */*' \
-H 'content-type: application/json' \
-H "Cookie: ___tk67142224=1655282500640; ibm-private-cloud-session=$ZEN_TOKEN" \
-d '{ 
        "name": "Infra: Network Equipment",
        "description": "Automatically created by Nicks scripts",
        "type": "inventory",
        "mode": "basic",
        "accessControlList": {
            "read": {
                "teams": [],
                "users": [
                    "*"
                ]
            },
            "admin": {
                "teams": [],
                "users": [
                    "demo"
                ]
            },
            "write": {
                "teams": [],
                "users": []
            }
        },
        "conditionSet": {
            "conditions": [{
                "id": "filterBuilderCondition-myrouter",
                "type": "condition",
                "field": "entityTypes",
                "operator": "includesAny",
                "value": ["router","switch","location","networkinterface","fiberPort","fiberConnection"]
            }]
        }
}'


curl "https://$ROUTE/api/p/hdm_asm_ui_api/1.0/ui-api/userconfig/filters" \
-X 'POST' \
-H 'content-type: application/json' \
-H 'accept: */*' \
-H 'content-type: application/json' \
-H "Cookie: ___tk67142224=1655282500640; ibm-private-cloud-session=$ZEN_TOKEN" \
-d '{ 
        "name": "_Global Risks",
        "description": "Automatically created by Nicks scripts",
        "type": "inventory",
        "mode": "basic",
        "accessControlList": {
            "read": {
                "teams": [],
                "users": [
                    "*"
                ]
            },
            "admin": {
                "teams": [],
                "users": [
                    "demo"
                ]
            },
            "write": {
                "teams": [],
                "users": []
            }
        },
        "conditionSet": {
            "conditions": [{
                "id": "filterBuilderCondition-myrisks",
                "type": "condition",
                "field": "entityTypes",
                "operator": "includesAny",
                "value": ["fire","alertHeadline","weatherAlert","wildfire","earthquake","storm","tsunami","volcano","avalanche","landslide","drought","heatwave","coldwave","wildfire","hazardousMaterialRelease","nuclearIncident"]
            }]
        }
}'





curl "https://$ROUTE/api/p/hdm_asm_ui_api/1.0/ui-api/userconfig/filters" \
-X 'POST' \
-H 'content-type: application/json' \
-H 'accept: */*' \
-H 'content-type: application/json' \
-H "Cookie: ___tk67142224=1655282500640; ibm-private-cloud-session=$ZEN_TOKEN" \
-d '{ 
        "name": "App: RobotShop",
        "description": "Automatically created by Nicks scripts",
        "type": "inventory",
        "mode": "basic",
        "accessControlList": {
            "read": {
                "teams": [],
                "users": [
                    "*"
                ]
            },
            "admin": {
                "teams": [],
                "users": [
                    "demo"
                ]
            },
            "write": {
                "teams": [],
                "users": []
            }
        },
        "conditionSet": {
        "conditions": [{
            "id": "filterBuilderCondition-1754913872305",
            "field": "tags",
            "operator": "matches",
            "value": ["namespace:robot-shop"],
            "type": "condition"
        }]
        }
}'





curl "https://$ROUTE/api/p/hdm_asm_ui_api/1.0/ui-api/userconfig/filters" \
-X 'POST' \
-H 'content-type: application/json' \
-H 'accept: */*' \
-H 'content-type: application/json' \
-H "Cookie: ___tk67142224=1655282500640; ibm-private-cloud-session=$ZEN_TOKEN" \
-d '{ 
        "name": "App: SockShop",
        "description": "Automatically created by Nicks scripts",
        "type": "inventory",
        "mode": "basic",
        "accessControlList": {
            "read": {
                "teams": [],
                "users": [
                    "*"
                ]
            },
            "admin": {
                "teams": [],
                "users": [
                    "demo"
                ]
            },
            "write": {
                "teams": [],
                "users": []
            }
        },
        "conditionSet": {
        "conditions": [{
            "id": "filterBuilderCondition-1754913872305",
            "field": "tags",
            "operator": "matches",
            "value": ["namespace:sock-shop"],
            "type": "condition"
        }]
        }
}'




curl "https://$ROUTE/api/p/hdm_asm_ui_api/1.0/ui-api/userconfig/filters" \
-X 'POST' \
-H 'content-type: application/json' \
-H 'accept: */*' \
-H 'content-type: application/json' \
-H "Cookie: ___tk67142224=1655282500640; ibm-private-cloud-session=$ZEN_TOKEN" \
-d '{ 
        "name": "App: ACME",
        "description": "Automatically created by Nicks scripts",
        "type": "inventory",
        "mode": "basic",
        "accessControlList": {
            "read": {
                "teams": [],
                "users": [
                    "*"
                ]
            },
            "admin": {
                "teams": [],
                "users": [
                    "demo"
                ]
            },
            "write": {
                "teams": [],
                "users": []
            }
        },
        "conditionSet": {
        "conditions": [{
            "id": "filterBuilderCondition-1754913872305",
            "field": "tags",
            "operator": "matches",
            "value": ["namespace:acme"],
            "type": "condition"
        }]
        }
}'


curl "https://$ROUTE/api/p/hdm_asm_ui_api/1.0/ui-api/userconfig/filters" \
-X 'POST' \
-H 'content-type: application/json' \
-H 'accept: */*' \
-H 'content-type: application/json' \
-H "Cookie: ___tk67142224=1655282500640; ibm-private-cloud-session=$ZEN_TOKEN" \
-d '{ 
        "name": "Infra: Fiber Network",
        "description": "Automatically created by Nicks scripts",
        "type": "inventory",
        "mode": "basic",
        "accessControlList": {
            "read": {
                "teams": [],
                "users": [
                    "*"
                ]
            },
            "admin": {
                "teams": [],
                "users": [
                    "demo"
                ]
            },
            "write": {
                "teams": [],
                "users": []
            }
        },
        "conditionSet": {
        "conditions": [{
            "id": "filterBuilderCondition-1754913872305",
            "field": "tags",
            "operator": "matches",
            "value": ["app:telco"],
            "type": "condition"
        }]
        }
}'






# --------------------------------------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------------------------------
# CREATE TEMPLATES AND RULES
# --------------------------------------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------------------------------

export AIOPS_NAMESPACE=$(oc get po -A|grep aiops-orchestrator-controller |awk '{print$1}')
export CONSOLE_ROUTE=$(oc get route -n $AIOPS_NAMESPACE cp-console  -o jsonpath={.spec.host})          
export CPD_ROUTE=$(oc get route -n $AIOPS_NAMESPACE cpd  -o jsonpath={.spec.host})          
export CPADMIN_PWD=$(oc -n $AIOPS_NAMESPACE get secret platform-auth-idp-credentials -o jsonpath='{.data.admin_password}' | base64 -d && echo)
export CPADMIN_USER=$(oc -n $AIOPS_NAMESPACE get secret platform-auth-idp-credentials -o jsonpath='{.data.admin_username}' | base64 -d && echo)
export ACCESS_TOKEN=$(curl -s -k -H "Content-Type: application/x-www-form-urlencoded;charset=UTF-8" -d "grant_type=password&username=$CPADMIN_USER&password=$CPADMIN_PWD&scope=openid" https://$CONSOLE_ROUTE/idprovider/v1/auth/identitytoken|jq -r '.access_token')
export ZEN_API_HOST=$(oc get route -n $AIOPS_NAMESPACE cpd -o jsonpath='{.spec.host}')
export ZEN_TOKEN=$(curl -k -XGET https://$ZEN_API_HOST/v1/preauth/validateAuth \
-H "username: $CPADMIN_USER" \
-H "iam-token: $ACCESS_TOKEN"|jq -r '.accessToken')
echo $ZEN_TOKEN

export ROUTE=$(oc get route -n $AIOPS_NAMESPACE cpd -o jsonpath={.spec.host})


# ---------------------------------
# inGroup
# ---------------------------------

export result=$(curl "https://$ROUTE/api/p/hdm_asm_ui_api/1.0/ui-api/templates?templateType=token" \
-X 'POST' \
-H 'content-type: application/json' \
-H 'accept: */*' \
-H 'content-type: application/json' \
-H "Cookie: ___tk67142224=1655282500640; ibm-private-cloud-session=$ZEN_TOKEN" \
-d ' {
"keyIndexName": "topologyTemplate:inGroupTemplate",
"templateType": "token",
"description": "Automatically created by Nicks scripts",
"extraProperties": {
  "correlatable": "true",
  "iconId": "network",
  "window": {
    "type": "rolling",
    "durationMS": 900000
  },
  "defaultHopType": "e2e"
},
"userId": "demo",
"_groupCount": 0,
"name": "inGroupTemplate",
"entityTypes": ["network"]
}')





export result=$(curl "https://$ROUTE/api/p/hdm_asm_ui_api/1.0/ui-api/templates?templateType=token" \
-X 'POST' \
-H 'content-type: application/json' \
-H 'accept: */*' \
-H 'content-type: application/json' \
-H "Cookie: ___tk67142224=1655282500640; ibm-private-cloud-session=$ZEN_TOKEN" \
-d ' {
"keyIndexName": "topologyTemplate:inGroupTemplate",
"templateType": "token",
"description": "Automatically created by Nicks scripts",
"extraProperties": {
  "correlatable": "true",
  "iconId": "network",
  "window": {
    "type": "rolling",
    "durationMS": 900000
  },
  "defaultHopType": "e2e"
},
"userId": "demo",
"_groupCount": 0,
"name": "inGroupTemplate",
"entityTypes": ["network"]
}')

export templateID=$(echo $result | jq -r '._id')
echo $templateID



export resultRule=$(curl "https://$ROUTE/api/p/hdm_asm_ui_api/1.0/ui-api/rules" \
-X 'POST' \
-H 'content-type: application/json' \
-H 'accept: */*' \
-H 'content-type: application/json' \
-H "Cookie: ___tk67142224=1655282500640; ibm-private-cloud-session=$ZEN_TOKEN" \
-d '{
  "name": "inGroupTemplate--inGroupRule",
  "ruleType": "groupPerTokenRule",
  "ruleStatus": "enabled",
  "tokens": ["Group ${inGroup}"],
  "observers": [],
  "providers": [],
  "entityTypes": [],
  "templateName": "inGroupTemplate",
  "_references": [{
      "_fromId": "'${templateID}'",
      "_edgeType": "managesRule"
  }]
}')


echo $resultRule


# ---------------------------------
# city
# ---------------------------------

export result=$(curl "https://$ROUTE/api/p/hdm_asm_ui_api/1.0/ui-api/templates?templateType=token" \
-X 'POST' \
-H 'content-type: application/json' \
-H 'accept: */*' \
-H 'content-type: application/json' \
-H "Cookie: ___tk67142224=1655282500640; ibm-private-cloud-session=$ZEN_TOKEN" \
-d '{
    "name": "cityTemplate",
    "description": "Automatically created by Nicks scripts",
    "keyIndexName": "topologyTemplate:cityTemplate",
    "templateType": "token",
    "entityTypes": ["infrastructure"],
    "extraProperties": {
        "correlatable": true,
        "iconId": "site",
        "window": {
            "type": "rolling",
            "durationMS": 900000
        },
        "defaultHopType": "e2e"
    },
    "tags": []
}')





export result=$(curl "https://$ROUTE/api/p/hdm_asm_ui_api/1.0/ui-api/templates?templateType=token" \
-X 'POST' \
-H 'content-type: application/json' \
-H 'accept: */*' \
-H 'content-type: application/json' \
-H "Cookie: ___tk67142224=1655282500640; ibm-private-cloud-session=$ZEN_TOKEN" \
-d '{
    "name": "cityTemplate",
    "description": "Automatically created by Nicks scripts",
    "keyIndexName": "topologyTemplate:cityTemplate",
    "templateType": "token",
    "entityTypes": ["infrastructure"],
    "extraProperties": {
        "correlatable": true,
        "iconId": "site",
        "window": {
            "type": "rolling",
            "durationMS": 900000
        },
        "defaultHopType": "e2e"
    },
    "tags": []
}')




export templateID=$(echo $result | jq -r '._id')
echo $templateID

export resultRule=$(curl "https://$ROUTE/api/p/hdm_asm_ui_api/1.0/ui-api/rules" \
-X 'POST' \
-H 'content-type: application/json' \
-H 'accept: */*' \
-H 'content-type: application/json' \
-H "Cookie: ___tk67142224=1655282500640; ibm-private-cloud-session=$ZEN_TOKEN" \
-d '{
    "name": "cityTemplate--cityRule",
    "ruleType": "groupPerTokenRule",
    "ruleStatus": "enabled",
    "tokens": ["Site ${city}"],
    "observers": [],
    "providers": [],
    "entityTypes": [],
    "templateName": "cityTemplate",
    "_references": [{
        "_fromId": "'${templateID}'",
        "_edgeType": "managesRule"
    }]
}')

echo $resultRule






# ---------------------------------
# app
# ---------------------------------

export result=$(curl "https://$ROUTE/api/p/hdm_asm_ui_api/1.0/ui-api/templates?templateType=token" \
-X 'POST' \
-H 'content-type: application/json' \
-H 'accept: */*' \
-H 'content-type: application/json' \
-H "Cookie: ___tk67142224=1655282500640; ibm-private-cloud-session=$ZEN_TOKEN" \
-d '{
    "name": "appTemplate",
    "description": "Automatically created by Nicks scripts",
    "keyIndexName": "topologyTemplate:appTemplate",
    "templateType": "token",
    "entityTypes": ["namespace"],
    "extraProperties": {
        "correlatable": true,
        "iconId": "application",
        "window": {
            "type": "rolling",
            "durationMS": 900000
        },
        "defaultHopType": "e2e"
    },
    "tags": []
}')



export result=$(curl "https://$ROUTE/api/p/hdm_asm_ui_api/1.0/ui-api/templates?templateType=token" \
-X 'POST' \
-H 'content-type: application/json' \
-H 'accept: */*' \
-H 'content-type: application/json' \
-H "Cookie: ___tk67142224=1655282500640; ibm-private-cloud-session=$ZEN_TOKEN" \
-d '{
    "name": "appTemplate",
    "description": "Automatically created by Nicks scripts",
    "keyIndexName": "topologyTemplate:appTemplate",
    "templateType": "token",
    "entityTypes": ["namespace"],
    "extraProperties": {
        "correlatable": true,
        "iconId": "application",
        "window": {
            "type": "rolling",
            "durationMS": 900000
        },
        "defaultHopType": "e2e"
    },
    "tags": []
}')




export templateID=$(echo $result | jq -r '._id')
echo $templateID

export resultRule=$(curl "https://$ROUTE/api/p/hdm_asm_ui_api/1.0/ui-api/rules" \
-X 'POST' \
-H 'content-type: application/json' \
-H 'accept: */*' \
-H 'content-type: application/json' \
-H "Cookie: ___tk67142224=1655282500640; ibm-private-cloud-session=$ZEN_TOKEN" \
-d '{
    "name": "appTemplate--appRule",
    "ruleType": "groupPerTokenRule",
    "ruleStatus": "enabled",
    "tokens": ["Application ${app}"],
    "observers": [],
    "providers": [],
    "entityTypes": [],
    "templateName": "appTemplate",
    "_references": [{
        "_fromId": "'${templateID}'",
        "_edgeType": "managesRule"
    }]
}')

echo $resultRule




# ---------------------------------
# location
# ---------------------------------

export result=$(curl "https://$ROUTE/api/p/hdm_asm_ui_api/1.0/ui-api/templates?templateType=token" \
-X 'POST' \
-H 'content-type: application/json' \
-H 'accept: */*' \
-H 'content-type: application/json' \
-H "Cookie: ___tk67142224=1655282500640; ibm-private-cloud-session=$ZEN_TOKEN" \
-d '{
    "name": "locationTemplate",
    "description": "Automatically created by Nicks scripts",
    "keyIndexName": "topologyTemplate:locationTemplate",
    "templateType": "token",
    "entityTypes": ["infrastructure"],
    "extraProperties": {
        "correlatable": true,
        "iconId": "site",
        "window": {
            "type": "rolling",
            "durationMS": 900000
        },
        "defaultHopType": "e2e"
    },
    "tags": []
}')



export result=$(curl "https://$ROUTE/api/p/hdm_asm_ui_api/1.0/ui-api/templates?templateType=token" \
-X 'POST' \
-H 'content-type: application/json' \
-H 'accept: */*' \
-H 'content-type: application/json' \
-H "Cookie: ___tk67142224=1655282500640; ibm-private-cloud-session=$ZEN_TOKEN" \
-d '{
    "name": "locationTemplate",
    "description": "Automatically created by Nicks scripts",
    "keyIndexName": "topologyTemplate:locationTemplate",
    "templateType": "token",
    "entityTypes": ["infrastructure"],
    "extraProperties": {
        "correlatable": true,
        "iconId": "site",
        "window": {
            "type": "rolling",
            "durationMS": 900000
        },
        "defaultHopType": "e2e"
    },
    "tags": []
}')




export templateID=$(echo $result | jq -r '._id')
echo $templateID

export resultRule=$(curl "https://$ROUTE/api/p/hdm_asm_ui_api/1.0/ui-api/rules" \
-X 'POST' \
-H 'content-type: application/json' \
-H 'accept: */*' \
-H 'content-type: application/json' \
-H "Cookie: ___tk67142224=1655282500640; ibm-private-cloud-session=$ZEN_TOKEN" \
-d '{
    "name": "locationTemplate--locationRule",
    "ruleType": "groupPerTokenRule",
    "ruleStatus": "enabled",
    "tokens": ["Site ${location}"],
    "observers": [],
    "providers": [],
    "entityTypes": [],
    "templateName": "locationTemplate",
    "_references": [{
        "_fromId": "'${templateID}'",
        "_edgeType": "managesRule"
    }]
}')

echo $resultRule







# --------------------------------------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------------------------------
# RERUN OBSERVER JOBS
# --------------------------------------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------------------------------

export AIOPS_NAMESPACE=$(oc get po -A|grep aiops-orchestrator-controller |awk '{print$1}')
export AIO_PLATFORM_ROUTE=$(oc get route -n $AIOPS_NAMESPACE aimanager-aio-controller -o jsonpath={.spec.host})

echo "        Namespace:          $AIOPS_NAMESPACE"
echo "        AIO_PLATFORM_ROUTE: $AIO_PLATFORM_ROUTE"
echo ""

echo "Sucessfully logged in" 
echo ""
echo "Running K8S OBSERVER"



curl -X 'POST' --insecure \
"https://$AIO_PLATFORM_ROUTE/v1/observer/runjob/robot-shop-topology" \
-H 'accept: application/json' \
-H 'Content-Type: application/json' \
-H "authorization: Bearer $ZEN_TOKEN"  


curl -X 'POST' --insecure \
"https://$AIO_PLATFORM_ROUTE/v1/observer/runjob/sock-shop-topology" \
-H 'accept: application/json' \
-H 'Content-Type: application/json' \
-H "authorization: Bearer $ZEN_TOKEN"  

curl -X 'POST' --insecure \
"https://$AIO_PLATFORM_ROUTE/v1/observer/runjob/us-network-risk-topology" \
-H 'accept: application/json' \
-H 'Content-Type: application/json' \
-H "authorization: Bearer $ZEN_TOKEN"  


curl -X 'POST' --insecure \
"https://$AIO_PLATFORM_ROUTE/v1/observer/runjob/risk-proximity-EU-topology" \
-H 'accept: application/json' \
-H 'Content-Type: application/json' \
-H "authorization: Bearer $ZEN_TOKEN"  

curl -X 'POST' --insecure \
"https://$AIO_PLATFORM_ROUTE/v1/observer/runjob/acme-topology" \
-H 'accept: application/json' \
-H 'Content-Type: application/json' \
-H "authorization: Bearer $ZEN_TOKEN"  


curl -X 'POST' --insecure \
"https://$AIO_PLATFORM_ROUTE/v1/observer/runjob/risk-proximity-topology" \
-H 'accept: application/json' \
-H 'Content-Type: application/json' \
-H "authorization: Bearer $ZEN_TOKEN"  

