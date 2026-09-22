echo "" 
echo "" 
echo "" 
echo "*****************************************************************************************************************************"
echo "*****************************************************************************************************************************"
echo "         ________  __  ___     ___    ________       "     
echo "        /  _/ __ )/  |/  /    /   |  /  _/ __ \____  _____"
echo "        / // __  / /|_/ /    / /| |  / // / / / __ \/ ___/"
echo "      _/ // /_/ / /  / /    / ___ |_/ // /_/ / /_/ (__  ) "
echo "     /___/_____/_/  /_/    /_/  |_/___/\____/ .___/____/  "
echo "                                           /_/            "
echo ""
echo "   🐥 IBM AIOPs - Event Driven Ansible / Turbonomic Integration - PoC"
echo ""
echo "*****************************************************************************************************************************"
echo "*****************************************************************************************************************************"
echo ""
echo "------------------------------------------------------------------------------------------------------------------------------"
echo " 📥 Installing EDA Instance"
echo "----------------------------------------------------------------------------------------------------------------"
echo "" 
echo "    🌏  https://github.com/ansible/event-driven-ansible" 
echo "    🌏  https://github.com/ansible/ansible-rulebook" 
echo "" 
echo "" 






oc apply -f ./tools/97_addons/ibm-aiops-eda/create-eda.yaml

sleep 15

echo "------------------------------------------------------------------------------------------------------------------------------"
echo " 📥 Initialization"

export TURBO_PASSWORD=CHANGEME
export WORKFLOW_NAME="EDA_WEBHOOK"

export EDA_URL=$(oc get route -n eda eda-instance -o jsonpath={.spec.host})
echo "    🌏 EDA_URL:   $EDA_URL"

export TURBO_URL=$(oc get route -n ibm-concert-optimise nginx -o jsonpath={.spec.host})
echo "    🌏 TURBO_URL: $TURBO_URL"
echo ""

echo "------------------------------------------------------------------------------------------------------------------------------"
echo " 📥 Login to Turbo"
export result=$(curl -XPOST -s -k -c /tmp/cookies -H 'accept: application/json' "https://$TURBO_URL/api/v3/login?disable_hateoas=true" -d "username=administrator&password=$TURBO_PASSWORD")
echo $result

echo "------------------------------------------------------------------------------------------------------------------------------"
echo " 📥 Get Existing Workflows"
export workflows=$(curl -XGET -s -k "https://$TURBO_URL/api/v3/workflows" -b /tmp/cookies  -H 'Content-Type: application/json;' -H 'accept: application/json')
echo $workflows|jq
echo ""
echo ""
echo ""

echo "------------------------------------------------------------------------------------------------------------------------------"
echo " 📥 Delete Existing EDA Workflow"
export existingWorkflow=$(echo $workflows|jq  '.[]|select(.displayName | contains("'$WORKFLOW_NAME'"))'| jq -r ".uuid")

if [[ $existingWorkflow != "" ]] ;
then
    echo "   ✅ Webhook already exists."
    #curl -XDELETE -s -k "https://$TURBO_URL/api/v3/workflows/$existingWorkflow" -b /tmp/cookies  -H 'Content-Type: application/json;' -H 'accept: application/json'
    WF_ID=$existingWorkflow
else
    echo "------------------------------------------------------------------------------------------------------------------------------"
    echo " 📥 Create EDA Workflow"
    result=$(curl -XPOST -s -k "https://$TURBO_URL/api/v3/workflows" -b /tmp/cookies  -H 'Content-Type: application/json;' -H 'accept: application/json' -d ' {
            "displayName": "'$WORKFLOW_NAME'",
            "className": "Workflow",
            "description": "'$WORKFLOW_NAME'",
            "discoveredBy":
            {
                "readonly": false
            },
        "type": "WEBHOOK",
        "typeSpecificDetails": {
        "url": "http://'$EDA_URL'/endpoint",
            "method": "POST",
            "template": "{  \"uuid\":\"$action.uuid\",   \"createTime\":\"$action.createTime\",  \"actionType\":\"$action.actionType\",  \"actionState\":\"$action.actionState\",  \"actionMode\":\"$action.actionMode\",  \"details\":\"$action.details\",  \"importance\": \"$action.importance\",  \"target\":{    \"uuid\":\"$action.target.uuid\",    \"displayName\":\"$action.target.displayName\",    \"className\":\"$action.target.className\",    \"environmentType\":\"$action.target.environmentType\"  },  \"risk\":{      \"subCategory\":\"$action.risk.subCategory\",     \"severity\":\"$action.risk.severity\",    \"importance\": \"$action.risk.importance\"  }}",
            "type": "WebhookApiDTO"
        }
        }')

    #echo $result| jq -r ".uuid"

    export WF_ID=$(echo $result| jq -r ".uuid")
    echo "    🛠️ Webhook ID: $WF_ID"
    echo ""
fi









echo ""
echo ""
read -p " Do you want to install EDA Server as well (not needed for EDA PoC)❓ [Y,n] " DO_COMM
if [[ $DO_COMM == "n" ||  $DO_COMM == "N" ]]; then


    echo "    ⚠️  Skipping"
    echo "--------------------------------------------------------------------------------------------"
    echo  ""    
    echo  ""
    echo ""

else

    echo ""
    echo "----------------------------------------------------------------------------------------------------------------"
    echo " 🚀  Install EDA Server" 
    echo "----------------------------------------------------------------------------------------------------------------"
    echo "" 
    echo "    🌏  https://github.com/ansible/eda-server" 

    oc create ns eda-server
    oc apply -n eda-server -f ./tools/97_addons/ibm-aiops-eda/eda-server
fi




