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
#  Train on Log Templates
#
#  CloudPak for AIOps
#
#  ©2026 nikh@ch.ibm.com
# ---------------------------------------------------------------------------------------------------------------------------------------------------"
# ---------------------------------------------------------------------------------------------------------------------------------------------------"
# ---------------------------------------------------------------------------------------------------------------------------------------------------"
# ---------------------------------------------------------------------------------------------------------------------------------------------------"



# Paths to find info in JSON
export entityIDString="kubernetes.container_name"
export messagePayloadString="message"

DAYS_TO_INJECT=7

OS=$(uname -s | tr '[:upper:]' '[:lower:]')
SED="sed"
if [ "${OS}" == "darwin" ]; then
    SED="gsed"
    if [ ! -x "$(command -v ${SED})"  ]; then
    __output "This script requires $SED, but it was not found.  Perform \"brew install gnu-sed\" and try again."
    exit
    fi
fi


#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# DO NOT MODIFY BELOW
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
clear

echo ""
echo ""
echo ""
echo ""
echo ""
echo "         ________  __  ___     ___    ________       "     
echo "        /  _/ __ )/  |/  /    /   |  /  _/ __ \____  _____"
echo "        / // __  / /|_/ /    / /| |  / // / / / __ \/ ___/"
echo "      _/ // /_/ / /  / /    / ___ |_/ // /_/ / /_/ (__  ) "
echo "     /___/_____/_/  /_/    /_/  |_/___/\____/ .___/____/  "
echo "                                           /_/            "
echo ""
echo ""
echo ""
echo "***************************************************************************************************************************************************"
echo "***************************************************************************************************************************************************"
echo ""
echo " 🚀  Train on Log Templates"
echo ""
echo "***************************************************************************************************************************************************"
echo "***************************************************************************************************************************************************"
echo ""
echo ""
echo "--------------------------------------------------------------------------------------------------"
echo "--------------------------------------------------------------------------------------------------"
echo "--------------------------------------------------------------------------------------------------"

echo "  📦 Parameters"
echo ""

echo "       entityIDString:         $entityIDString"
echo "       messagePayloadString:   $messagePayloadString"

export TEMPLATE_DIR_LOGS=./templates/logs
export WORKING_DIR_LOGS=/tmp/lags

echo ""
echo ""

# Read Template File template.tpl
echo "  📦 Template File"
templateFile=$(<$TEMPLATE_DIR_LOGS/template.tpl)
echo $templateFile|jq | ${SED} 's/^/          /'

mkdir -p $WORKING_DIR_LOGS
mkdir -p /tmp/training-files-logs



echo ""
echo ""
echo ""
echo ""
echo "🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣"
echo ""
echo "  🚀 STEP 1: Creating Template File"
echo ""

currentLine=0

if [[ -f $WORKING_DIR_LOGS/logs.json ]] ;
then
  echo "     ✅ Already exists: Skipping"
else
    echo "">$WORKING_DIR_LOGS/logs.json

    # Loop over all *.log files in the TEMPLATE_DIR_LOGS directory
    for actFile in $(ls -1 $TEMPLATE_DIR_LOGS | grep "log");
    do
        totalLines=$(cat $TEMPLATE_DIR_LOGS/$actFile|wc -l| tr -d ' ')
        export componentName=${actFile%.*}
        echo ""
        echo "   --------------------------------------------------------------------------------------------------"
        echo "     🛠️ Treating File: $componentName"

          if [[ $actFile =~ ".log" ]] ;
          then
            # Read Line by Line
            while IFS= read -r line
            do

            ((currentLine++))

              # Get Entity ID
              entityID=$(jq -r ".$entityIDString" <<< "$line")
              printf "\r         🌶️ Component ($currentLine/$totalLines): $entityID                    "\\r
              if [[ ! -z $entityID ]] ;
              then
                # Get Message Payload (some trickery involved to handle escaped embedded JSON)
                messagePayload=$(echo $line | ${SED} 's/\\"/@@@@/g'| ${SED} 's/\\/!!!!!!/g'| jq ".$messagePayloadString")
                echo $templateFile | ${SED} "s^{{entityID}}^$entityID^g"| ${SED} "s^{{messagePayload}}^$messagePayload^g" | ${SED} 's/\"\"/\"/g'  >>$WORKING_DIR_LOGS/logs.json
                
                
                #messagePayload=$(jq ".$messagePayloadString" <<< "$line")
                #echo $messagePayload
                #echo $templateFile | sed "s^{{entityID}}^$entityID^"| sed "s^{{messagePayload}}^$messagePayload^"   >>$WORKING_DIR_LOGS/logs.json
                #echo "${templateFile//@@entityID@@/$entityID}"
                #echo $templateFile | sed "s/{{entityID}}/$entityID/"| sed "s&{{messagePayload}}&${messagePayload}&"  #>>$WORKING_DIR_LOGS/logs.json
                #echo $line |jq ".$entityID"
                #echo "${line//\\\\/\\\\\\}" |jq ".$entityID"
                #echo $line|jq ".$entityID"
                #echo $line|jq ".$messagePayload"
              fi
            done < "$TEMPLATE_DIR_LOGS/$actFile"
          fi
    done


    # Restore escaped embedded JSON
    ${SED} -i 's/@@@@/\\\"/g' $WORKING_DIR_LOGS/logs.json

    echo ""
    echo ""
    echo "    --------------------------------------------------------------------------------------------------"
    echo "      ✅ DONE"
    echo "    --------------------------------------------------------------------------------------------------"


fi


echo ""
echo ""
echo "     --------------------------------------------------------------------------------------------------"
echo "      ❤️‍🩹 Entity Count"
echo ""
cat $WORKING_DIR_LOGS/logs.json|jq '.["kubernetes"].container_name' | sort | uniq -c| ${SED} 's/^/          /'
echo ""
echo ""
echo ""
echo "     --------------------------------------------------------------------------------------------------"
echo "       👨‍🎤 Entity Example"
echo ""
head -n 2 $WORKING_DIR_LOGS/logs.json|jq | ${SED} 's/^/          /'









echo ""
echo ""
echo "🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣"
echo ""
echo " 🚀   STEP 4: Log injection"
echo ""

    echo " "
    echo "   ------------------------------------------------------------------------------------------------------------------------------"
    echo "   🚀  Initializing..."
    echo "   ------------------------------------------------------------------------------------------------------------------------------"


    export AIOPS_NAMESPACE=$(oc get po -A|grep aiops-orchestrator-controller |awk '{print$1}')
    echo "       ✅ OK - IBMAIOps:    $AIOPS_NAMESPACE"


    echo "     🔐 Get Kafka Password"
    export KAFKA_SECRET=$(oc get secret -n $AIOPS_NAMESPACE |grep 'aiops-kafka-secret'|awk '{print$1}')
    export SASL_USER=$(oc get secret $KAFKA_SECRET -n $AIOPS_NAMESPACE --template={{.data.username}} | base64 --decode)
    export SASL_PASSWORD=$(oc get secret $KAFKA_SECRET -n $AIOPS_NAMESPACE --template={{.data.password}} | base64 --decode)
    export KAFKA_BROKER=$(oc get routes iaf-system-kafka-0 -n $AIOPS_NAMESPACE -o=jsonpath='{.status.ingress[0].host}{"\n"}'):443

    #------------------------------------------------------------------------------------------------------------------------------------
    #  Get the cert for kafkacat
    #------------------------------------------------------------------------------------------------------------------------------------
    echo "     🥇 Getting Kafka Cert"
    oc extract secret/kafka-secrets -n $AIOPS_NAMESPACE --keys=ca.crt --confirm| ${SED} 's/^/            /'
    echo ""
    echo ""

    #------------------------------------------------------------------------------------------------------------------------------------
    #  Get Kafkacat executable
    #------------------------------------------------------------------------------------------------------------------------------------
    echo "     📥  Getting Kafkacat executable"
    if [ -x "$(command -v kafkacat)" ]; then
          export KAFKACAT_EXE=kafkacat
    else
          if [ -x "$(command -v kcat)" ]; then
                export KAFKACAT_EXE=kcat
          else
                echo "     ❗ ERROR: kafkacat is not installed."
                echo "     ❌ Aborting..."
                exit 1
          fi
    fi
    echo " "




    echo "     📥 Get Kafka Topics"
    #export KAFKA_TOPIC_LOGS=$(oc get kafkatopics -n $AIOPS_NAMESPACE | grep cp4waiops-cartridge-logs-elk| awk '{print $1;}')
    export KAFKA_TOPIC_LOGS=$(${KAFKACAT_EXE} -v -X security.protocol=SASL_SSL -X ssl.ca.location=./ca.crt -X sasl.mechanisms=SCRAM-SHA-512 -X sasl.username=$SASL_USER -X sasl.password=$SASL_PASSWORD -b $KAFKA_BROKER -L -J| jq -r '.topics[].topic' | grep cp4waiops-cartridge-logs-elk| head -n 1)


    if [[ "${KAFKA_TOPIC_LOGS}" == "" ]]; then
        echo "          ❗ Please define a Kafka connection in IBMAIOps of type $LOG_TYPE."
        echo "          ❗ Existing Log Topics are:"
        oc get kafkatopics -n $AIOPS_NAMESPACE | grep cp4waiops-cartridge-logs-| awk '{print $1;}'| ${SED} 's/^/                /'
        echo ""
        echo "          ❌ Exiting....."
        #exit 1 

    else
        echo "        🟢 OK"
    fi





    echo "   ----------------------------------------------------------------------------------------------------------------------------------------"
    echo "     🔎  Parameters for Incident Simulation for $APP_NAME"
    echo "   ----------------------------------------------------------------------------------------------------------------------------------------"
    echo "     "
    echo "       🗂  Log Topic                   : $KAFKA_TOPIC_LOGS"
    echo "       🌏 Kafka Broker URL            : $KAFKA_BROKER"
    echo "       🔐 Kafka User                  : $SASL_USER"
    echo "       🔐 Kafka Password              : $SASL_PASSWORD"
    echo "       🖥️  Kafka Executable           : $KAFKACAT_EXE"
    echo "     "
    echo "       📂 Directory for Logs          : $WORKING_DIR_LOGS"
    echo "   ----------------------------------------------------------------------------------------------------------------------------------------"
    echo "   "

    echo "   "
  

      while true 
      do
        while IFS= read -r line
        do
          entityID=$(jq -r ".$entityIDString" <<< "$line")
          messagePayload=$(jq -r ".$messagePayloadString" <<< "$line")

          export my_date=$(date  "+%Y-%m-%dT%H:%M:%S.000000+00:00.00") 
          echo "         🌶️ Injecting    $my_date  -       ${entityID:0:15} : ${messagePayload:0:30}"
          #printf "\r         🌶️ Injecting    $my_date  -       ${entityID:0:15} : ${messagePayload:0:20}                                        "\\r

          export lineTS=$(echo $line|${SED} "s/@MY_TIMESTAMP/$my_date/g")
          #echo $lineTS
          ${KAFKACAT_EXE} -v -X security.protocol=SASL_SSL -X ssl.ca.location=./ca.crt -X sasl.mechanisms=SCRAM-SHA-512  -X sasl.username=$SASL_USER -X sasl.password=$SASL_PASSWORD -b $KAFKA_BROKER -P -t $KAFKA_TOPIC_LOGS <<< $lineTS

      done < "$WORKING_DIR_LOGS/logs.json"
    done





    echo ""
    echo ""
    echo "    --------------------------------------------------------------------------------------------------"
    echo "      ✅ DONE"
    echo "    --------------------------------------------------------------------------------------------------"



echo "***************************************************************************************************************************************************"
echo "***************************************************************************************************************************************************"
echo ""
echo " ✅ DONE"
echo ""
echo "***************************************************************************************************************************************************"
echo "***************************************************************************************************************************************************"


exit 1
