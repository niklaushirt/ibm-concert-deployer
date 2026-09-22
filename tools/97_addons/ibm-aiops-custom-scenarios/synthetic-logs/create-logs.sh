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
echo ""
echo ""
echo "🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣"
echo ""
echo "  🚀 STEP 2: Creating Hourly Template File"
echo ""

if [[ -f $WORKING_DIR_LOGS/logs_TS.json ]] ;
then
  echo "     ✅ Already exists: Skipping"
else

    # Read Line by Line
    ITERATIONS=11
    OS=$(uname -s | tr '[:upper:]' '[:lower:]')
    SECONDS=0

    echo "" > $WORKING_DIR_LOGS/logs_TS.json

    #while [[ ! $my_date =~ "2023-12-31T22" ]]; do
    while [ $SECONDS -lt 3600 ]; do
    while IFS= read -r line
    do
        if [ $ITERATIONS -gt 3 ]; then
            ITERATIONS=0

            if [ "${OS}" == "darwin" ]; then
              # Suppose we're on Mac
              export my_date=$(date -v-${SECONDS}S -j -f %Y%m%d-%H%M%S 20240101-000000 "+:%M:%S.000000+00:00.00") 
              #export my_date=$(date -v-${SECONDS}S -j -f %Y%m%d-%H%M%S 20240101-000000 "+%Y-%m-%dT%H:%M:%S.000000+00:00.00") 
            else
              export my_date=$(date -d ${SECONDS}' seconds ago' "+:%M:%S.000000+00:00.00")
              #export my_date=$(date -d ${SECONDS}' seconds ago' "+%Y-%m-%dT%H:%M:%S.000000+00:00.00" -d 2024-01-01)
            fi
            ((SECONDS++))
            printf "\r         🌶️ Seconds ($SECONDS/3600)                    "\\r

            
        fi
        ((ITERATIONS++))

      #echo $my_date

      #echo "         🌶️ Component ($currentLine/$totalLines): $line"
      echo $line|${SED} "s/@MY_TIMESTAMP/@MY_TIMESTAMP$my_date/g" >> $WORKING_DIR_LOGS/logs_TS.json
    done < "$WORKING_DIR_LOGS/logs.json"
    done

    echo ""
    echo ""
    echo "    --------------------------------------------------------------------------------------------------"
    echo "      ✅ DONE"
    echo "    --------------------------------------------------------------------------------------------------"

fi 



echo ""
echo ""
echo ""
echo ""
echo "🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣"
echo ""
echo "  🚀 STEP 3: Creating Injection Files"
echo ""

OS=$(uname -s | tr '[:upper:]' '[:lower:]')

MAX_HOURS=$(($DAYS_TO_INJECT*24))
#echo "MAX_HOURS:   $MAX_HOURS"
HOURS=0
mkdir -p $WORKING_DIR_LOGS/to_inject

while [ $HOURS -lt $MAX_HOURS ];
do
  ((HOURS++))
  if [ "${OS}" == "darwin" ]; then
    # Suppose we're on Mac
    export my_date=$(date -v-${HOURS}H "+%Y-%m-%dT%H")
  else
    export my_date=$(date -d ${HOURS}' hours ago' "+%Y-%m-%dT%H")
  fi

  printf "\r         🌶️ File ($HOURS/$MAX_HOURS)                    "\\r

  #echo $WORKING_DIR_LOGS/to_inject/$my_date.log
  cp $WORKING_DIR_LOGS/logs_TS.json $WORKING_DIR_LOGS/to_inject/$my_date.log
  ${SED} -i -e "s/@MY_TIMESTAMP/$my_date/g" $WORKING_DIR_LOGS/to_inject/$my_date.log
  
done

rm -f $WORKING_DIR_LOGS/to_inject/*.log-e
#ls -1 $WORKING_DIR_LOGS/to_inject| ${SED} 's/^/          /'

echo ""
echo ""
echo "    --------------------------------------------------------------------------------------------------"
echo "      ✅ DONE"
echo "    --------------------------------------------------------------------------------------------------"




echo ""
echo ""
echo "🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣"
echo ""
echo " 🚀   STEP 4: Log injection"
echo ""

echo "   ------------------------------------------------------------------------------------------------------------------------------"
read  -t 5 -p "    ❓ Do you want to inject the Logs❓ [y,N] " DO_COMM
echo "   ------------------------------------------------------------------------------------------------------------------------------"
if [[ $DO_COMM == "y" ||  $DO_COMM == "Y" ]]; then
    echo " "
    echo "   ------------------------------------------------------------------------------------------------------------------------------"
    echo "   🚀  Initializing..."
    echo "   ------------------------------------------------------------------------------------------------------------------------------"

    cd $WORKING_DIR_LOGS/to_inject

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
  


    FILES_COUNT=0
    MAX_FILES_COUNT=$(($DAYS_TO_INJECT*24))

    for actFile in $(ls -1 $WORKING_DIR_LOGS/to_inject | grep "log"); 
    do 
            if [[ $actFile =~ ".log"  ]]; then
                    ((FILES_COUNT++))

                    #echo "   🚀  Injecting $actFile"
                    printf "\r         🚀 Injecting $actFile ($FILES_COUNT/$MAX_FILES_COUNT)                    "\\r

                    split -l 1500 -a 6 $actFile
                    for actFileSplit in $(ls -1 $WORKING_DIR_LOGS/to_inject | grep "xa"); 
                    do 
                      #echo "              $actFileSplit"
                      ${KAFKACAT_EXE} -v -X security.protocol=SASL_SSL -X ssl.ca.location=./ca.crt -X sasl.mechanisms=SCRAM-SHA-512  -X sasl.username=$SASL_USER -X sasl.password=$SASL_PASSWORD -b $KAFKA_BROKER -P -t $KAFKA_TOPIC_LOGS -l $actFileSplit
                    done
                    rm -f xa*
            fi
    done


    echo ""
    echo ""
    echo "    --------------------------------------------------------------------------------------------------"
    echo "      ✅ DONE"
    echo "    --------------------------------------------------------------------------------------------------"

fi


echo "***************************************************************************************************************************************************"
echo "***************************************************************************************************************************************************"
echo ""
echo " ✅ DONE"
echo ""
echo "***************************************************************************************************************************************************"
echo "***************************************************************************************************************************************************"


exit 1
