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
#  IBMAIOPS  - Debug AIOPS Installation
#
#
#  ©2026 nikh@ch.ibm.com
# ---------------------------------------------------------------------------------------------------------------------------------------------------"
# ---------------------------------------------------------------------------------------------------------------------------------------------------"
# ---------------------------------------------------------------------------------------------------------------------------------------------------"
# ---------------------------------------------------------------------------------------------------------------------------------------------------"



export TEMP_PATH=~/aiops-install
export ERROR_STRING=""
export WARNING_STRING=""

export ERROR=false
export WARNING_STATE=false

#oc delete ConsoleNotification --all>/dev/null 2>/dev/null

cat <<EOF | oc apply -f -
apiVersion: console.openshift.io/v1
kind: ConsoleNotification
metadata:
    name: ibm-aiops-notification-main
spec:
    backgroundColor: '#1122aa'
    color: '#fff'
    location: BannerTop
    text: "🔎 FINALIZING: Checking IBM AIOps Installation"
EOF




# ---------------------------------------------------------------------------------------------------------------------------------------------------"
# ---------------------------------------------------------------------------------------------------------------------------------------------------"
# Do Not Edit Below
# ---------------------------------------------------------------------------------------------------------------------------------------------------"
# ---------------------------------------------------------------------------------------------------------------------------------------------------"
function handleError(){
    if  ([[ $CURRENT_ERROR == true ]]); 
    then
        ERROR=true
        ERROR_STRING=$ERROR_STRING"\n⭕ $CURRENT_ERROR_STRING"
        echo "      "
        echo "      "
        echo "      ❗***************************************************************************************************************************************************"
        echo "      ❗***************************************************************************************************************************************************"
        echo "      ❗  ❌ The following error was found: "
        echo "      ❗"
        echo "      ❗      ⭕ $CURRENT_ERROR_STRING"; 
        echo "      ❗"
        echo "      ❗***************************************************************************************************************************************************"
        echo "      ❗***************************************************************************************************************************************************"
        echo "      "
        echo "      "

    fi
}


function handleWarning(){
    if  ([[ $CURRENT_WARNING_STATE == true ]]); 
    then
        WARNING_STATE=true
        WARNING_STRING=$WARNING_STRING"\n ⚠️  $CURRENT_WARNING_STRING"
        echo "        ⚠️ ***************************************************************************************************************************************************"
        echo "        ⚠️ ***************************************************************************************************************************************************"
        echo "        ⚠️   The following warning was found: "
        echo "        ⚠️ "
        echo "        ⚠️       ⚠️  $CURRENT_WARNING_STRING"; 
        echo "        ⚠️ "
        echo "        ⚠️ ***************************************************************************************************************************************************"
        echo "        ⚠️ ***************************************************************************************************************************************************"
    fi
}



function check_array_crd(){

      echo "    --------------------------------------------------------------------------------------------"
      echo "    🔎 Check $CHECK_NAME"
      echo "    --------------------------------------------------------------------------------------------"

      for ELEMENT in ${CHECK_ARRAY[@]}; do
            ELEMENT_NAME=${ELEMENT##*/}
            ELEMENT_TYPE=${ELEMENT%%/*}
       echo "   Check $ELEMENT_NAME ($ELEMENT_TYPE) ..."

            ELEMENT_OK=$(oc get $ELEMENT -n $AIOPS_NAMESPACE | grep "AGE" || true) 

            if  ([[ ! $ELEMENT_OK =~ "AGE" ]]); 
            then 
                  echo "      ⭕ $ELEMENT not present"; 
                  echo ""
            else
                  echo "          ✅ OK: $ELEMENT"; 

            fi
      done
      export CHECK_NAME=""
}

function check_array(){

      echo "    --------------------------------------------------------------------------------------------"
      echo "    🔎 Check $CHECK_NAME"
      echo "    --------------------------------------------------------------------------------------------"

      for ELEMENT in ${CHECK_ARRAY[@]}; do
            ELEMENT_NAME=${ELEMENT##*/}
            ELEMENT_TYPE=${ELEMENT%%/*}
       echo "   Check $ELEMENT_NAME ($ELEMENT_TYPE) ..."

            ELEMENT_OK=$(oc get $ELEMENT -n $AIOPS_NAMESPACE | grep $ELEMENT_NAME || true) 

            if  ([[ ! $ELEMENT_OK =~ "$ELEMENT_NAME" ]]); 
            then 
                  echo "      ⭕ $ELEMENT not present"; 
                  echo ""
            else
                  echo "          ✅ OK: $ELEMENT"; 

            fi
      done
      export CHECK_NAME=""
}













#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# EXAMINE INSTALLATION
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
      echo ""
      echo "  ------------------------------------------------------------------------------------------------------------------------------------------------------"
      echo "  🚀 Initializing"
      echo "  ------------------------------------------------------------------------------------------------------------------------------------------------------"
      echo ""
      echo "   🛠️  Get Namespaces"
      export AIOPS_NAMESPACE=$(oc get po -A|grep aiops-orchestrator-controller |awk '{print$1}')
      echo "          IBM AIOps Namespace: $AIOPS_NAMESPACE"


      echo "   🌐  Get Cluster Route"
      oc create route passthrough --insecure-policy="Redirect" aiops-opensearch -n $AIOPS_NAMESPACE --service="aiops-opensearch" --port="http"


        CLUSTER_ROUTE=$(oc get routes console -n openshift-console | tail -n 1 2>&1 ) 
        CLUSTER_FQDN=$( echo $CLUSTER_ROUTE | awk '{print $2}')
        CLUSTER_NAME=${CLUSTER_FQDN##*console.}



      echo "   🌐  Get API Route"
      oc create route passthrough ai-platform-api -n $AIOPS_NAMESPACE  --service=aimanager-aio-ai-platform-api-server --port=4000 --insecure-policy=Redirect --wildcard-policy=None>/dev/null 2>/dev/null
      export ROUTE=$(oc get route -n $AIOPS_NAMESPACE ai-platform-api  -o jsonpath={.spec.host})
      echo "          Route: $ROUTE"
      
      
      echo "   🔐  Getting ZEN Token"
      export AIOPS_NAMESPACE=$(oc get po -A|grep aiops-orchestrator-controller |awk '{print$1}')
      export CONSOLE_ROUTE=$(oc get route -n $AIOPS_NAMESPACE cp-console  -o jsonpath={.spec.host})          
      export CPD_ROUTE=$(oc get route -n $AIOPS_NAMESPACE cpd  -o jsonpath={.spec.host})          
      export CPADMIN_PWD=$(oc -n $AIOPS_NAMESPACE get secret platform-auth-idp-credentials -o jsonpath='{.data.admin_password}' | base64 -d && echo)
      export CPADMIN_USER=$(oc -n $AIOPS_NAMESPACE get secret platform-auth-idp-credentials -o jsonpath='{.data.admin_username}' | base64 -d && echo)

      export ACCESS_TOKEN=$(curl -s -k -H "Content-Type: application/x-www-form-urlencoded;charset=UTF-8" -d "grant_type=password&username=$CPADMIN_USER&password=$CPADMIN_PWD&scope=openid" https://$CONSOLE_ROUTE/idprovider/v1/auth/identitytoken|jq -r '.access_token')
      export ZEN_API_HOST=$(oc get route -n $AIOPS_NAMESPACE cpd -o jsonpath='{.spec.host}')
      export ZEN_TOKEN=$(curl -s -k -XGET https://$ZEN_API_HOST/v1/preauth/validateAuth \
      -H "username: $CPADMIN_USER" \
      -H "iam-token: $ACCESS_TOKEN"|jq -r '.accessToken')
      
      echo "             🙎‍♂️ CPADMIN_USER:   $CPADMIN_USER"
      echo "             🔐 CPADMIN_PWD:     $CPADMIN_PWD"
      echo "             🔐 ZEN_TOKEN:       ${ZEN_TOKEN:0:25}....."
      echo ""
      echo ""
      
      echo "          ✅ OK:Sucessfully logged in" 

      echo ""
      echo ""
      echo "  ----------------------------------------------------------------------------------------------------------------------------------------------------------"
      echo "   🚀  CHECK IBMAIOPS Operators" 
      echo "  ----------------------------------------------------------------------------------------------------------------------------------------------------------"
      echo ""
      echo "    🔎 Installed Openshift Operator Versions"
      oc get -n $AIOPS_NAMESPACE ClusterServiceVersion | sed 's/^/       /'
      echo ""


      export PODS_COUNT=$(oc get pods -n $AIOPS_NAMESPACE | grep -v "Completed"| grep "Running" | grep -c "")
      if  ([[ $PODS_COUNT -lt 125 ]]); 
      then 
            echo "       ❗ FATAL: CP4AIOPS could not be installed - only $PODS_COUNT Pods running (should be around 130)"; 

#oc delete ConsoleNotification --all>/dev/null 2>/dev/null
cat <<EOF | oc apply -f -
apiVersion: console.openshift.io/v1
kind: ConsoleNotification
metadata:
    name: ibm-aiops-notification-fatal
spec:
    backgroundColor: '#ff0000'
    color: '#fff'
    location: BannerTop
    text: " 💣 FATAL: CP4AIOPS could not be installed - only $PODS_COUNT Pods running (should be around 130)"
EOF
cat <<EOF | oc apply -f -
apiVersion: console.openshift.io/v1
kind: ConsoleNotification
metadata:
    name: ibm-aiops-notification-help
spec:
    backgroundColor: '#dd4500'
    color: '#fff'
    location: BannerTop
    link:
        href: "https://github.com/niklaushirt/ibm-aiops-deployer?tab=readme-ov-file#7-troubleshooting"
        text: Troubleshooting

    text: " Nothing the script can do here. Check the Link or Slack to see if this is a known problem."
EOF

            exit 1
      fi


      echo ""
      echo ""
      echo "  ----------------------------------------------------------------------------------------------------------------------------------------------------------"
      echo "   🚀  CHECK IBMAIOPS Demo Namespaces" 
      echo "  ----------------------------------------------------------------------------------------------------------------------------------------------------------"
      echo ""

    checkNamespace () {
      echo "    🔎 Pods not ready in Namespace $CURRENT_NAMESPACE"

      export ERROR_PODS=$(oc get pods -n $CURRENT_NAMESPACE | grep -v "Completed" | grep "0/"|awk '{print$1}')
      export ERROR_PODS_COUNT=$(oc get pods -n $CURRENT_NAMESPACE | grep -v "Completed" |grep -v nginx-ingress-controller| grep "0/"| grep -c "")
      if  ([[ $ERROR_PODS_COUNT -gt 0 ]]); 
      then 
            export CURRENT_WARNING_STATE=true
            export CURRENT_WARNING_STRING="$ERROR_PODS_COUNT Pods not running in Namespace "$CURRENT_NAMESPACE"  \n"$ERROR_PODS
            handleWarning
      else  
            echo "          ✅ OK: All Pods running and ready in Namespace $CURRENT_NAMESPACE"; 
      fi
      echo ""
      echo ""
    }



      export CURRENT_NAMESPACE=ibm-cert-manager
      checkNamespace

      export CURRENT_NAMESPACE=$AIOPS_NAMESPACE
      checkNamespace

      export CURRENT_NAMESPACE=awx
      checkNamespace

      export CURRENT_NAMESPACE=openldap
      checkNamespace

      export CURRENT_NAMESPACE=awx
      checkNamespace

      export CURRENT_NAMESPACE=ibm-aiops-demo-ui
      checkNamespace

      export CURRENT_NAMESPACE=sock-shop
      checkNamespace

      export CURRENT_NAMESPACE=robot-shop
      checkNamespace

      
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# EXAMINE CONNECTIONS
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

      echo ""
      echo ""
      echo "  ----------------------------------------------------------------------------------------------------------------------------------------------------------"
      echo "  🚀 CHECK CONNECTIONS"
      echo "  ----------------------------------------------------------------------------------------------------------------------------------------------------------"
      echo ""


      export AI_PLATFORM_ROUTE=$(oc get route -n $AIOPS_NAMESPACE ai-platform-api  -o jsonpath={.spec.host})
      export AIO_PLATFORM_ROUTE=$(oc get route -n $AIOPS_NAMESPACE aimanager-aio-controller -o jsonpath={.spec.host})

      echo "             🌐 AI_PLATFORM_ROUTE:  $AI_PLATFORM_ROUTE"
      echo "             🌐 AIO_PLATFORM_ROUTE: $AIO_PLATFORM_ROUTE"
      echo ""


      export result=$(curl -s -X 'GET' --insecure \
      "https://$AIO_PLATFORM_ROUTE/v3/connections" \
      -H 'accept: application/json' \
      -H 'Content-Type: application/json' \
            -H "authorization: Bearer $ZEN_TOKEN" |jq|grep ELKGoldenSignal|wc -l|tr -d ' ')

      #echo $result

      if  ([[ $result -lt 1 ]]); 
            then 
                  export CURRENT_ERROR=true
                  export CURRENT_ERROR_STRING="ELKGoldenSignal connection missing"
                  handleError
            else  
                  echo "          ✅ OK - ELKGoldenSignal Connection exists"; 
            fi





#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# EXAMINE TRAINING
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


      echo ""
      echo ""
      echo "  ----------------------------------------------------------------------------------------------------------------------------------------------------------"
      echo "  🚀 CHECK Trained Models"
      echo "  ----------------------------------------------------------------------------------------------------------------------------------------------------------"
      echo ""

      export result=$(curl "https://$ROUTE/graphql" -k -s -H "authorization: Bearer $ZEN_TOKEN" -H 'Accept-Encoding: gzip, deflate, br' -H 'Content-Type: application/json' -H 'Accept: application/json' -H 'Connection: keep-alive' -H 'DNT: 1' -H 'Origin: https://ai-platform-api-ibm-aiops.itzroks-270003bu3k-qd899z-6ccd7f378ae819553d37d5f2ee142bd6-0000.eu-de.containers.appdomain.cloud' --data-binary '{"query":"query {\n    getTrainingDefinitions {\n      definitionName\n      algorithmName\n      version\n      deployedVersion\n      description\n      createdBy\n      modelDeploymentDate\n   }\n   }"}' --compressed --compressed)
      export trainedAlgorithms=$(echo $result |jq -r ".data.getTrainingDefinitions[].algorithmName")
      

      if  ([[ $trainedAlgorithms =~ "Log_Anomaly_" ]]); 
      then
            echo "          ✅ OK: Defined - Log_Anomaly_Detection (NLP or Golden Signal)"; 
      else
            echo "       ⚠️ WARINING: Log_Anomaly_Detection (NLP or Golden Signal) not ready yet."; 
            echo "       ⚠️ WARINING: This can be totally normal - please check in the UI"; 

            # export CURRENT_ERROR=true
            # export CURRENT_ERROR_STRING="Log_Anomaly_Detection not trained (NLP or Golden Signal)"
            # handleError
      fi

      if  ([[ $trainedAlgorithms =~ "Similar_Incidents" ]]); 
      then
            echo "          ✅ OK: Defined - Similar_Incidents"; 
      else
            export CURRENT_ERROR=true
            export CURRENT_ERROR_STRING="Similar_Incidents not trained"
            handleError
      fi

      if  ([[ $trainedAlgorithms =~ "Metric_Anomaly_Detection" ]]); 
      then
            echo "          ✅ OK: Defined - Metric_Anomaly_Detection"; 
      else
            export CURRENT_ERROR=true
            export CURRENT_ERROR_STRING="Metric_Anomaly_Detection not trained"
            handleError
      fi

      if  ([[ $trainedAlgorithms =~ "Change_Risk" ]]); 
      then
            echo "          ✅ OK: Defined - Change_Risk"; 
      else
            export CURRENT_ERROR=true
            export CURRENT_ERROR_STRING="Change_Risk not trained"
            handleError
      fi


      if  ([[ $trainedAlgorithms =~ "Temporal_Grouping" ]]); 
      then
            echo "          ✅ OK: Defined - Temporal_Grouping"; 
      else
            export CURRENT_ERROR=true
            export CURRENT_ERROR_STRING="Temporal_Grouping not trained"
            handleError
      fi

      # if  ([[ $trainedAlgorithms =~ "Alert_Seasonality_Detection" ]]); 
      # then
      #       echo "          ✅ OK: Defined - Alert_Seasonality_Detection"; 
      # else
      #       export CURRENT_ERROR=true
      #       export CURRENT_ERROR_STRING="Alert_Seasonality_Detection not trained"
      #       handleError
      # fi


      # if  ([[ $trainedAlgorithms =~ "Alert_X_In_Y_Supression" ]]); 
      # then
      #       echo "          ✅ OK: Defined - Alert_X_In_Y_Supression"; 
      # else
      #       export CURRENT_ERROR=true
      #       export CURRENT_ERROR_STRING="Alert_X_In_Y_Supression not trained"
      #       handleError
      # fi




#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# CHECK LAGS TRAINING
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


      echo ""
      echo ""
      echo "  ----------------------------------------------------------------------------------------------------------------------------------------------------------"
      echo "  🚀 CHECK LAGS TRAINING"
      echo "  ----------------------------------------------------------------------------------------------------------------------------------------------------------"
      echo ""
      export username=elastic
      export password=$(oc get secret $(oc get secrets | grep aiops-opensearch-admin-secret | awk '!/-min/' | awk '{print $1;}') -o jsonpath="{.data.password}"| base64 --decode)	
      export ES_ROUTE=$(oc get route -n $AIOPS_NAMESPACE aiops-opensearch  -o jsonpath={.spec.host})
      echo "             🌐 Elastic URL:                  $ES_ROUTE"	
      echo "             🙎‍♂️ User:                         $username"	
      echo "             🔐 Password:                     $password"	
      echo ""	



      echo "      🔎  Get logMetrics"	
      export result=$(oc exec -ti -n $AIOPS_NAMESPACE aiops-ir-analytics-postgres-1 -c postgres -- bash -c "psql -U postgres -d aiops_ir_ai -c \"SELECT count(*) FROM aiops_ir_ai.metric_metadata WHERE group_name LIKE '%logMetrics%';\""|grep ' 0'|wc -l|tr -d ' ')
      #echo $result

      if  ([[ $result == "1" ]]); 
            then 
                  export CURRENT_WARNING_STATE=true
                  export CURRENT_WARNING_STRING="LAGS training incomplete - Log into CP4AIOPS and re-run the Metrics Training"
                  handleWarning

                  export AIOPS_NAMESPACE=$(oc get po -A|grep aiops-orchestrator-controller |awk '{print$1}')

                  echo "      ***************************************************************************************************************************************************"
                  echo "      ⚠️  RE-START - LOAD LOG TRAINING DATA to mitigate Problem - This will take about 5-10 minutes"
                  oc apply -f ./tools/98_maintenance/jobs/loads/reload-job-lags.yaml
                  sleep 15

                  echo "      ***************************************************************************************************************************************************"
                  echo "      🛠️   Waiting for LAGS data load to complete"
                  oc wait --for=condition=complete -n ibm-installer --timeout=5000s job/reload-lags-indexes


                  echo "      ***************************************************************************************************************************************************"
                  echo "      🛠️   CONFIG - LAGS POD"
                  oc set env deploy -n $AIOPS_NAMESPACE aimanager-aio-log-anomaly-golden-signals --overwrite BUCKET_SIZE_IN_MILLIS="3600000" 
                  oc set env deploy -n $AIOPS_NAMESPACE aimanager-aio-log-anomaly-golden-signals --overwrite HISTORIC_START_TIMESTAMP-
                  oc set env deploy -n $AIOPS_NAMESPACE aimanager-aio-log-anomaly-golden-signals --overwrite HISTORIC_TIME_RANGE-

                  echo "      ***************************************************************************************************************************************************"
                  echo "      🛠️   RESTART - LAGS POD"
                  oc delete pod -n $AIOPS_NAMESPACE --ignore-not-found $(oc get po -n $AIOPS_NAMESPACE|grep golden-signals|awk '{print$1}')



                  echo "      ***************************************************************************************************************************************************"
                  echo "      🛠️   RESTART - LOG INJECTION POD"
                  oc delete pod -n $AIOPS_NAMESPACE-demo-ui --ignore-not-found $(oc get po -n $AIOPS_NAMESPACE-demo-ui|grep ibm-aiops-stream-lags-normal|awk '{print$1}')



                  echo "      ***************************************************************************************************************************************************"
                  echo "      🛠️   RERUN - MetricAnomaly"
                  export FILE_NAME=run-analysis-METRIC.graphql
                  export FILE_PATH="/ibm-aiops-deployer/ansible/roles/ibm-aiops-demo-content/templates/training/training-definitions/"
                  /ibm-aiops-deployer/ansible/roles/ibm-aiops-demo-content/templates/training/scripts/execute-graphql.sh



            else  
                  echo "          ✅ OK - ELKGoldenSignal exists"; 
            fi






      echo "      🔎  Get ElasticSearch LAGS Index"	
      oc project $AIOPS_NAMESPACE > /dev/null 2>&1	

      export existingIndexes=$(curl -s -k -u $username:$password -XGET https://$ES_ROUTE/_cat/indices|grep 1000-1000-la_golden_signals-models|wc -l|tr -d ' ')

      #echo "existingIndexes: $existingIndexes"

      if  ([[ $existingIndexes == "0" ]]); 
            then 
                  export CURRENT_WARNING_STATE=true
                  export CURRENT_WARNING_STRING="LAGS training incomplete - Log into CP4AIOPS and re-run the Metrics Training"
                  handleWarning
            else  
                  echo "          ✅ OK: LAGS Golden Signals Index exists in ElasticSearch"; 
            fi



#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# EXAMINE AWX
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

      echo ""
      echo ""
      echo "  ----------------------------------------------------------------------------------------------------------------------------------------------------------"
      echo "  🚀 CHECK AWX"
      echo "  ----------------------------------------------------------------------------------------------------------------------------------------------------------"
      echo ""

    export AWX_ROUTE=$(oc get route -n awx awx -o jsonpath={.spec.host})
    export AWX_URL=$(echo "https://$AWX_ROUTE")
    export AWX_PWD=$(oc -n awx get secret awx-admin-password -o jsonpath='{.data.password}' | base64 --decode && echo)


    echo "      🔎 Check AWX Project"
    export AWX_PROJECT_STATUS=$(curl -X "GET" -s "$AWX_URL/api/v2/projects/" -u "admin:$AWX_PWD" --insecure -H 'content-type: application/json'|jq|grep successful|grep -c "")
    if  ([[ $AWX_PROJECT_STATUS -lt 4 ]]); 
      then 
            export CURRENT_ERROR=true
            export CURRENT_ERROR_STRING="AWX Project not ready"
            handleError
      else  
            echo "          ✅ OK"; 
      fi

    echo "      🔎 Check AWX Inventory"
    export AWX_INVENTORY_COUNT=$(curl -X "GET" -s "$AWX_URL/api/v2/inventories/" -u "admin:$AWX_PWD" --insecure -H 'content-type: application/json'|grep "IBM AIOPS Runbooks"|wc -l|tr -d ' ')
    if  ([[ $AWX_INVENTORY_COUNT -lt 1 ]]); 
      then 
            export CURRENT_ERROR=true
            export CURRENT_ERROR_STRING="AWX Inventory not ready"
            handleError
      else  
            echo "          ✅ OK"; 
      fi

    echo "      🔎 Check AWX Templates"
    export AWX_TEMPLATE_COUNT=$(curl -X "GET" -s "$AWX_URL/api/v2/job_templates/" -u "admin:$AWX_PWD" --insecure -H 'content-type: application/json'| jq ".count")
    if  ([[ $AWX_TEMPLATE_COUNT -lt 5 ]]); 
      then 
            export CURRENT_ERROR=true
            export CURRENT_ERROR_STRING="AWX Templates not ready"
            handleError
      else  
            echo "          ✅ OK ($AWX_TEMPLATE_COUNT Templates)"; 
            curl -X "GET" -s "$AWX_URL/api/v2/job_templates/" -u "admin:$AWX_PWD" --insecure -H 'content-type: application/json'|jq -r '.results[].name'| sed 's/^/          - /'



            
      fi



#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# EXAMINE POLICIES
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

      echo ""
      echo ""
      echo "  ----------------------------------------------------------------------------------------------------------------------------------------------------------"
      echo "  🚀 CHECK IBM AIOps Runbooks"
      echo "  ----------------------------------------------------------------------------------------------------------------------------------------------------------"
      echo ""


    CPD_ROUTE=$(oc get route cpd -n $AIOPS_NAMESPACE  -o jsonpath={.spec.host} || true) 

    echo "      🔎 Check IBMAIOPS Runbooks"

    export result=$(curl -X "GET" -s -k "https://$CPD_ROUTE/aiops/api/story-manager/rba/v1/runbooks" \
        -H "Authorization: bearer $ZEN_TOKEN" \
        -H 'Content-Type: application/json; charset=utf-8')
    export RB_COUNT=$(echo $result|jq ".[].name"|grep -c "")
    if  ([[ $RB_COUNT -lt 7 ]]); 
      then 
            export CURRENT_ERROR=true
            export CURRENT_ERROR_STRING="IBMAIOps Runbooks not ready"
            echo $result|jq -r '.[].name'| sed 's/^/          - /'
            handleError
      else  
            echo "          ✅ OK ($RB_COUNT Runbooks)"; 
            echo $result|jq -r '.[].name'| sed 's/^/          - /'
      fi



#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# EXAMINE POLICIES
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

      echo ""
      echo ""
      echo "  ----------------------------------------------------------------------------------------------------------------------------------------------------------"
      echo "  🚀 CHECK IBM AIOps Policies"
      echo "  ----------------------------------------------------------------------------------------------------------------------------------------------------------"
      echo ""


    export POLICY_USERNAME=$(oc get secret -n $AIOPS_NAMESPACE aiops-ir-lifecycle-policy-registry-svc -o jsonpath='{.data.username}' | base64 --decode)
    export POLICY_PASSWORD=$(oc get secret -n $AIOPS_NAMESPACE aiops-ir-lifecycle-policy-registry-svc -o jsonpath='{.data.password}' | base64 --decode)
    export POLICY_LOGIN="$POLICY_USERNAME:$POLICY_PASSWORD"
    export POLICY_ROUTE=$(oc get routes -n $AIOPS_NAMESPACE policy-api -o jsonpath="{['spec']['host']}")

    echo "      🔎 Check Policies"
    export POLICY_COUNT=$(curl -XGET -k -s "https://$POLICY_ROUTE/policyregistry.ibm-netcool-prod.aiops.io/v1alpha/system/cfd95b7e-3bc7-4006-a4a8-a73a79c71255/"  \
      -H 'X-TenantID: cfd95b7e-3bc7-4006-a4a8-a73a79c71255' \
      -H 'content-type: application/json' \
      -u $POLICY_LOGIN|grep "DEMO"|wc -l|tr -d ' ')

    if  ([[ $POLICY_COUNT -lt 5 ]]); 
      then 
            export CURRENT_ERROR=true
            export CURRENT_ERROR_STRING="Policies Missing"
            handleError
      else  
            echo "          ✅ OK ($POLICY_COUNT Policies)"; 
            curl -XGET -k -s "https://$POLICY_ROUTE/policyregistry.ibm-netcool-prod.aiops.io/v1alpha/system/cfd95b7e-3bc7-4006-a4a8-a73a79c71255/"  \
            -H 'X-TenantID: cfd95b7e-3bc7-4006-a4a8-a73a79c71255' \
            -H 'content-type: application/json' \
            -u $POLICY_LOGIN|jq -r ".[].metadata"|jq -r '.name'|grep "DEMO"| sed 's/^/          - /'
      fi



#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# WRAP UP
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------



      echo ""
      echo ""
    if  ([[ $ERROR == true ]]); 
    then
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ERROR
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        shopt -s xpg_echo
        echo ""
        echo ""
        echo "***************************************************************************************************************************************************"
        echo "***************************************************************************************************************************************************"
        echo "  ❗ Your installation has the following problems ❗"
        echo ""
        echo "      $ERROR_STRING" | sed 's/^/       /'
        echo ""
        echo "***************************************************************************************************************************************************"
        echo "***************************************************************************************************************************************************"
        echo ""
        echo "  🚀 Try to re-run the installer to see if this solves the problem"
        echo "  🛠️  To do this just delete the ibm-aiops-install-aiops pod in the ibm-aiop Namespace"
        echo "  🛠️  Explained in detail here: https://github.com/niklaushirt/ibm-aiops-deployer/tree/main#re-run-the-installer"
        echo ""
        echo "***************************************************************************************************************************************************"
        echo "***************************************************************************************************************************************************"
        echo ""

        echo ""
        echo ""
        OPENSHIFT_ROUTE=$(oc get route -n openshift-console console -o jsonpath={.spec.host})
        INSTALL_POD=$(oc get po -n ibm-installer -l app=ibm-installer --no-headers|grep "Running"|grep "1/1"|awk '{print$1}')

#oc delete ConsoleNotification --all>/dev/null 2>/dev/null
cat <<EOF | oc apply -f -
apiVersion: console.openshift.io/v1
kind: ConsoleNotification
metadata:
    name: ibm-aiops-notification-warning
spec:
    backgroundColor: '#dd4500'
    color: '#fff'
    location: "BannerTop"
    text: "⚠️ WARNING: Your Installation has some problems. Please check the Installation Logs and re-run the installer by deleting the Pod"
    link:
        href: "https://$OPENSHIFT_ROUTE/k8s/ns/ibm-installer/pods/$INSTALL_POD/logs"
        text: Open Logs
EOF
export AIOPS_NAMESPACE=$(oc get po -A|grep aiops-orchestrator-controller |awk '{print$1}')
export appURL=$(oc get routes -n $AIOPS_NAMESPACE-demo-ui ibm-aiops-demo-ui  -o jsonpath="{['spec']['host']}")|| true
export DEMO_PWD=$(oc get cm -n $AIOPS_NAMESPACE-demo-ui ibm-aiops-demo-ui-config -o jsonpath='{.data.TOKEN}')
cat <<EOF | oc apply -f -
apiVersion: console.openshift.io/v1
kind: ConsoleNotification
metadata:
    name: ibm-aiops-notification-main
spec:
    backgroundColor: '#009a00'
    color: '#fff'
    link:
        href: "https://$appURL"
        text: DemoUI
    location: BannerTop
    text: "⚠️ IBMAIOPS is installed in this cluster. 🚀 Access the DemoUI with Password '$DEMO_PWD' here:"
EOF

    elif  ([[ $WARNING_STATE == true ]]); 
    then
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ERROR
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        shopt -s xpg_echo
        echo ""
        echo ""
        echo "***************************************************************************************************************************************************"
        echo "***************************************************************************************************************************************************"
        echo ""
        echo "  🟢🟢🟢 Your installation looks fine"
        echo ""
        echo ""
        echo "  ⚠️  But we encountered the following non blocking warnings"
        echo ""
        echo "      $WARNING_STRING" | sed 's/^/       /'
        echo ""
        echo "***************************************************************************************************************************************************"
        echo "***************************************************************************************************************************************************"
        echo ""

export AIOPS_NAMESPACE=$(oc get po -A|grep aiops-orchestrator-controller |awk '{print$1}')
export appURL=$(oc get routes -n $AIOPS_NAMESPACE-demo-ui ibm-aiops-demo-ui  -o jsonpath="{['spec']['host']}")|| true
export DEMO_PWD=$(oc get cm -n $AIOPS_NAMESPACE-demo-ui ibm-aiops-demo-ui-config -o jsonpath='{.data.TOKEN}')
#oc delete ConsoleNotification --all>/dev/null 2>/dev/null
cat <<EOF | oc apply -f -
apiVersion: console.openshift.io/v1
kind: ConsoleNotification
metadata:
    name: ibm-aiops-notification-main
spec:
    backgroundColor: '#009a00'
    color: '#fff'
    link:
        href: "https://$appURL"
        text: DemoUI
    location: BannerTop
    text: "✅ IBMAIOPS is installed in this cluster. 🚀 Access the DemoUI with Password '$DEMO_PWD' here:"
EOF


    else
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# NO ERROR
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        echo "***************************************************************************************************************************************************"
        echo "***************************************************************************************************************************************************"
        echo ""
        echo "  🟢🟢🟢 Your installation looks fine"
        echo ""
        echo "***************************************************************************************************************************************************"
        echo "***************************************************************************************************************************************************"

export AIOPS_NAMESPACE=$(oc get po -A|grep aiops-orchestrator-controller |awk '{print$1}')
export appURL=$(oc get routes -n $AIOPS_NAMESPACE-demo-ui ibm-aiops-demo-ui  -o jsonpath="{['spec']['host']}")|| true
export DEMO_PWD=$(oc get cm -n $AIOPS_NAMESPACE-demo-ui ibm-aiops-demo-ui-config -o jsonpath='{.data.TOKEN}')
#oc delete ConsoleNotification --all>/dev/null 2>/dev/null
cat <<EOF | oc apply -f -
apiVersion: console.openshift.io/v1
kind: ConsoleNotification
metadata:
    name: ibm-aiops-notification-main
spec:
    backgroundColor: '#009a00'
    color: '#fff'
    link:
        href: "https://$appURL"
        text: DemoUI
    location: BannerTop
    text: "✅ IBMAIOPS is installed in this cluster. 🚀 Access the DemoUI with Password '$DEMO_PWD' here:"
EOF

    fi



