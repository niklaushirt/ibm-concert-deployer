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
#  IBMAIOPS - Inject Log Files for Inception
#
#
#  ©2026 nikh@ch.ibm.com
# ---------------------------------------------------------------------------------------------------------------------------------------------------"
# ---------------------------------------------------------------------------------------------------------------------------------------------------"
# ---------------------------------------------------------------------------------------------------------------------------------------------------"
# ---------------------------------------------------------------------------------------------------------------------------------------------------"

export num_log_lines=100
export time_increment_sec=60
export WORKING_DIR_LOGS=/tmp/inceptionlogs

export component1=dSwitch-5-vm-network-port-1
export component2=catalogue-db
export component3=catalogue-network

clear

echo "***************************************************************************************************************************************************"
echo "***************************************************************************************************************************************************"
echo "***************************************************************************************************************************************************"
echo "***************************************************************************************************************************************************"
echo "  "
echo "  🚀 IBM AIOps - Inject Log Files for Inception"
echo "  "
echo "***************************************************************************************************************************************************"
echo "***************************************************************************************************************************************************"
echo "***************************************************************************************************************************************************"
echo "  "
echo "  "

#------------------------------------------------------------------------------------------------------------------------------------
#  Get Credentials
#------------------------------------------------------------------------------------------------------------------------------------
echo " "
echo "   ------------------------------------------------------------------------------------------------------------------------------"
echo "   🚀  Initializing..."
echo "   ------------------------------------------------------------------------------------------------------------------------------"
echo " "
echo "     🔎 Lines:      $num_log_lines"
echo "     🔎 Increments: $time_increment_sec"


mkdir $WORKING_DIR_LOGS  >/tmp/demo.log 2>&1  || true
rm $WORKING_DIR_LOGS/*   >/tmp/demo.log 2>&1  || true
echo " "
echo " "
echo " "

export utc_timestamp=$(date +'%Y-%m-%d %H:%M:%S.000')
echo "   ------------------------------------------------------------------------------------------------------------------------------"
echo "    🚀 Logs Starting at $utc_timestamp"
echo "   ------------------------------------------------------------------------------------------------------------------------------"
echo " "


for i in $(seq 1 $time_increment_sec $(($num_log_lines*$time_increment_sec)))
do

export my_timestamp=$(date -v+${i}S +'%s')
export utc_timestamp=$(date -v+${i}S +'%Y-%m-%d %H:%M:%S.000')



printf "       $(($i/$time_increment_sec))/$num_log_lines"\\r



message1="[$utc_timestamp] dSwitch 5 - vm-network - port-1 is up."
message2="[$utc_timestamp] All is good in catalogue-db."
message3="[$utc_timestamp] All is good in catalogue-network."

echo "{\"_index\":\"app-000003\",\"_type\":\"_doc\",\"_source\":{\"kubernetes\":{\"container_name\":\""$component1"\",\"host\":\"KUBE1\",\"namespace_labels\":{\"kubernetes_io/metadata_name\":\"sock-shop\"},\"container_image\":\"docker.io/"$component1":latest\",\"namespace_name\":\"sock-shop\",\"pod_name\":\""$component1"\"},\"message\":\""$message1"\",\"hostname\":\""$component1"\",\"log_type\":\"application\",\"@timestamp\":\""$my_timestamp"000\"}}">>$WORKING_DIR_LOGS/sock_logs.json
echo "{\"_index\":\"app-000003\",\"_type\":\"_doc\",\"_source\":{\"kubernetes\":{\"container_name\":\""$component2"\",\"host\":\"KUBE1\",\"namespace_labels\":{\"kubernetes_io/metadata_name\":\"sock-shop\"},\"container_image\":\"docker.io/"$component2":latest\",\"namespace_name\":\"sock-shop\",\"pod_name\":\""$component2"\"},\"message\":\""$message2"\",\"hostname\":\""$component2"\",\"log_type\":\"application\",\"@timestamp\":\""$my_timestamp"000\"}}">>$WORKING_DIR_LOGS/sock_logs.json
echo "{\"_index\":\"app-000003\",\"_type\":\"_doc\",\"_source\":{\"kubernetes\":{\"container_name\":\""$component3"\",\"host\":\"KUBE1\",\"namespace_labels\":{\"kubernetes_io/metadata_name\":\"sock-shop\"},\"container_image\":\"docker.io/"$component3":latest\",\"namespace_name\":\"sock-shop\",\"pod_name\":\""$component3"\"},\"message\":\""$message3"\",\"hostname\":\""$component3"\",\"log_type\":\"application\",\"@timestamp\":\""$my_timestamp"000\"}}">>$WORKING_DIR_LOGS/sock_logs.json



message1="[$utc_timestamp] ERROR: dSwitch 5 - vm-network - port-1 is down."
message2="[$utc_timestamp] ERROR: network is offline"
message3="[$utc_timestamp] ERROR: catalogue-db is offline."
echo "{\"_index\":\"app-000003\",\"_type\":\"_doc\",\"_source\":{\"kubernetes\":{\"container_name\":\""$component1"\",\"host\":\"KUBE1\",\"namespace_labels\":{\"kubernetes_io/metadata_name\":\"sock-shop\"},\"container_image\":\"docker.io/"$component1":latest\",\"namespace_name\":\"sock-shop\",\"pod_name\":\""$component1"\"},\"message\":\""$message1"\",\"hostname\":\""$component1"\",\"log_type\":\"application\",\"@timestamp\":\""$my_timestamp"000\"}}">>$WORKING_DIR_LOGS/sock_logs.json
echo "{\"_index\":\"app-000003\",\"_type\":\"_doc\",\"_source\":{\"kubernetes\":{\"container_name\":\""$component2"\",\"host\":\"KUBE1\",\"namespace_labels\":{\"kubernetes_io/metadata_name\":\"sock-shop\"},\"container_image\":\"docker.io/"$component2":latest\",\"namespace_name\":\"sock-shop\",\"pod_name\":\""$component2"\"},\"message\":\""$message2"\",\"hostname\":\""$component2"\",\"log_type\":\"application\",\"@timestamp\":\""$my_timestamp"000\"}}">>$WORKING_DIR_LOGS/sock_logs.json
echo "{\"_index\":\"app-000003\",\"_type\":\"_doc\",\"_source\":{\"kubernetes\":{\"container_name\":\""$component3"\",\"host\":\"KUBE1\",\"namespace_labels\":{\"kubernetes_io/metadata_name\":\"sock-shop\"},\"container_image\":\"docker.io/"$component3":latest\",\"namespace_name\":\"sock-shop\",\"pod_name\":\""$component3"\"},\"message\":\""$message3"\",\"hostname\":\""$component3"\",\"log_type\":\"application\",\"@timestamp\":\""$my_timestamp"000\"}}">>$WORKING_DIR_LOGS/sock_logs.json


message1="[$utc_timestamp] Port is down."
message2="[$utc_timestamp] Port unreachable."
message3="[$utc_timestamp] SQL: Database connection error."
echo "{\"_index\":\"app-000003\",\"_type\":\"_doc\",\"_source\":{\"kubernetes\":{\"container_name\":\""$component1"\",\"host\":\"KUBE1\",\"namespace_labels\":{\"kubernetes_io/metadata_name\":\"sock-shop\"},\"container_image\":\"docker.io/"$component1":latest\",\"namespace_name\":\"sock-shop\",\"pod_name\":\""$component1"\"},\"message\":\""$message1"\",\"hostname\":\""$component1"\",\"log_type\":\"application\",\"@timestamp\":\""$my_timestamp"000\"}}">>$WORKING_DIR_LOGS/sock_logs.json
echo "{\"_index\":\"app-000003\",\"_type\":\"_doc\",\"_source\":{\"kubernetes\":{\"container_name\":\""$component2"\",\"host\":\"KUBE1\",\"namespace_labels\":{\"kubernetes_io/metadata_name\":\"sock-shop\"},\"container_image\":\"docker.io/"$component2":latest\",\"namespace_name\":\"sock-shop\",\"pod_name\":\""$component2"\"},\"message\":\""$message2"\",\"hostname\":\""$component2"\",\"log_type\":\"application\",\"@timestamp\":\""$my_timestamp"000\"}}">>$WORKING_DIR_LOGS/sock_logs.json
echo "{\"_index\":\"app-000003\",\"_type\":\"_doc\",\"_source\":{\"kubernetes\":{\"container_name\":\""$component3"\",\"host\":\"KUBE1\",\"namespace_labels\":{\"kubernetes_io/metadata_name\":\"sock-shop\"},\"container_image\":\"docker.io/"$component3":latest\",\"namespace_name\":\"sock-shop\",\"pod_name\":\""$component3"\"},\"message\":\""$message3"\",\"hostname\":\""$component3"\",\"log_type\":\"application\",\"@timestamp\":\""$my_timestamp"000\"}}">>$WORKING_DIR_LOGS/sock_logs.json


message1="[$utc_timestamp] ERROR: No connection."
message2="[$utc_timestamp] ERROR: No connection."
message3="[$utc_timestamp] ERROR: No connection."
echo "{\"_index\":\"app-000003\",\"_type\":\"_doc\",\"_source\":{\"kubernetes\":{\"container_name\":\""$component1"\",\"host\":\"KUBE1\",\"namespace_labels\":{\"kubernetes_io/metadata_name\":\"sock-shop\"},\"container_image\":\"docker.io/"$component1":latest\",\"namespace_name\":\"sock-shop\",\"pod_name\":\""$component1"\"},\"message\":\""$message1"\",\"hostname\":\""$component1"\",\"log_type\":\"application\",\"@timestamp\":\""$my_timestamp"000\"}}">>$WORKING_DIR_LOGS/sock_logs.json
echo "{\"_index\":\"app-000003\",\"_type\":\"_doc\",\"_source\":{\"kubernetes\":{\"container_name\":\""$component2"\",\"host\":\"KUBE1\",\"namespace_labels\":{\"kubernetes_io/metadata_name\":\"sock-shop\"},\"container_image\":\"docker.io/"$component2":latest\",\"namespace_name\":\"sock-shop\",\"pod_name\":\""$component2"\"},\"message\":\""$message2"\",\"hostname\":\""$component2"\",\"log_type\":\"application\",\"@timestamp\":\""$my_timestamp"000\"}}">>$WORKING_DIR_LOGS/sock_logs.json
echo "{\"_index\":\"app-000003\",\"_type\":\"_doc\",\"_source\":{\"kubernetes\":{\"container_name\":\""$component3"\",\"host\":\"KUBE1\",\"namespace_labels\":{\"kubernetes_io/metadata_name\":\"sock-shop\"},\"container_image\":\"docker.io/"$component3":latest\",\"namespace_name\":\"sock-shop\",\"pod_name\":\""$component3"\"},\"message\":\""$message3"\",\"hostname\":\""$component3"\",\"log_type\":\"application\",\"@timestamp\":\""$my_timestamp"000\"}}">>$WORKING_DIR_LOGS/sock_logs.json


message1="[$utc_timestamp] ERROR: No throughput"
message2="[$utc_timestamp] SQL: catalogue-db unavailable."
message3="[$utc_timestamp] SQL: catalogue-db unavailable."
echo "{\"_index\":\"app-000003\",\"_type\":\"_doc\",\"_source\":{\"kubernetes\":{\"container_name\":\""$component1"\",\"host\":\"KUBE1\",\"namespace_labels\":{\"kubernetes_io/metadata_name\":\"sock-shop\"},\"container_image\":\"docker.io/"$component1":latest\",\"namespace_name\":\"sock-shop\",\"pod_name\":\""$component1"\"},\"message\":\""$message1"\",\"hostname\":\""$component1"\",\"log_type\":\"application\",\"@timestamp\":\""$my_timestamp"000\"}}">>$WORKING_DIR_LOGS/sock_logs.json
echo "{\"_index\":\"app-000003\",\"_type\":\"_doc\",\"_source\":{\"kubernetes\":{\"container_name\":\""$component2"\",\"host\":\"KUBE1\",\"namespace_labels\":{\"kubernetes_io/metadata_name\":\"sock-shop\"},\"container_image\":\"docker.io/"$component2":latest\",\"namespace_name\":\"sock-shop\",\"pod_name\":\""$component2"\"},\"message\":\""$message2"\",\"hostname\":\""$component2"\",\"log_type\":\"application\",\"@timestamp\":\""$my_timestamp"000\"}}">>$WORKING_DIR_LOGS/sock_logs.json
echo "{\"_index\":\"app-000003\",\"_type\":\"_doc\",\"_source\":{\"kubernetes\":{\"container_name\":\""$component3"\",\"host\":\"KUBE1\",\"namespace_labels\":{\"kubernetes_io/metadata_name\":\"sock-shop\"},\"container_image\":\"docker.io/"$component3":latest\",\"namespace_name\":\"sock-shop\",\"pod_name\":\""$component3"\"},\"message\":\""$message3"\",\"hostname\":\""$component3"\",\"log_type\":\"application\",\"@timestamp\":\""$my_timestamp"000\"}}">>$WORKING_DIR_LOGS/sock_logs.json





done

printf "       Done    "

export utc_timestamp=$(date -v+${i}S +'%Y-%m-%d %H:%M:%S.000')
echo " "
echo " "
echo "   ------------------------------------------------------------------------------------------------------------------------------"
echo "    ✅ Logs Ending at $utc_timestamp"
echo "   ------------------------------------------------------------------------------------------------------------------------------"


exit 1

echo " "
echo "   ------------------------------------------------------------------------------------------------------------------------------"
echo "   🚀  Initializing..."
echo "   ------------------------------------------------------------------------------------------------------------------------------"
echo " "
echo " "
echo "   ------------------------------------------------------------------------------------------------------------------------------"
echo "     🔬 Getting Installation Namespace"

export AIOPS_NAMESPACE=$(oc get po -A|grep aiops-orchestrator-controller |awk '{print$1}')
echo "       ✅ OK - IBMAIOps:    $AIOPS_NAMESPACE"


echo " "
echo "   ------------------------------------------------------------------------------------------------------------------------------"
echo "     📥 Get Kafka Topics"
export KAFKA_TOPIC_LOGS=$(oc get kafkatopics -n $AIOPS_NAMESPACE | grep cp4waiops-cartridge-logs-none| awk '{print $1;}')


echo " "
echo "   ------------------------------------------------------------------------------------------------------------------------------"
echo "     🔐 Get Kafka Password"
export KAFKA_SECRET=$(oc get secret -n $AIOPS_NAMESPACE |grep 'aiops-kafka-secret'|awk '{print$1}')
export SASL_USER=$(oc get secret $KAFKA_SECRET -n $AIOPS_NAMESPACE --template={{.data.username}} | base64 --decode)
export SASL_PASSWORD=$(oc get secret $KAFKA_SECRET -n $AIOPS_NAMESPACE --template={{.data.password}} | base64 --decode)
export KAFKA_BROKER=$(oc get routes iaf-system-kafka-0 -n $AIOPS_NAMESPACE -o=jsonpath='{.status.ingress[0].host}{"\n"}'):443



#------------------------------------------------------------------------------------------------------------------------------------
#  Get Kafkacat executable
#------------------------------------------------------------------------------------------------------------------------------------
echo " "
echo "   ------------------------------------------------------------------------------------------------------------------------------"
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

#------------------------------------------------------------------------------------------------------------------------------------
#  Get the cert for kafkacat
#------------------------------------------------------------------------------------------------------------------------------------
echo " "
echo "   ------------------------------------------------------------------------------------------------------------------------------"
echo "     🥇 Getting Kafka Cert"
oc extract secret/kafka-secrets -n $AIOPS_NAMESPACE --keys=ca.crt --confirm  >/tmp/demo.log 2>&1  || true
echo "      ✅ OK"


#------------------------------------------------------------------------------------------------------------------------------------
#  Check Credentials
#------------------------------------------------------------------------------------------------------------------------------------
echo " "
echo " "
echo "   ------------------------------------------------------------------------------------------------------------------------------"
echo "   🔗  Checking credentials"
echo "   ------------------------------------------------------------------------------------------------------------------------------"

if [[ $KAFKA_TOPIC_LOGS == "" ]] ;
then
      echo " ❌ Please create the $LOG_TYPE Kafka Log Integration. Aborting..."
      exit 1
else
      echo "       ✅ OK - Logs Topic"
fi


if [[ $KAFKA_BROKER == "" ]] ;
then
      echo " ❌ Make sure that your Kafka instance is accesssible. Aborting..."
      exit 1
else
      echo "       ✅ OK - Kafka Broker"
fi

echo " "
echo " "
echo " "
echo " "

echo "   ----------------------------------------------------------------------------------------------------------------------------------------"
echo "     🔎  Parameters for Incident Simulation for $APP_NAME"
echo "   ----------------------------------------------------------------------------------------------------------------------------------------"
echo "     "
echo "       🗂  Log Topic                   : $KAFKA_TOPIC_LOGS"
echo "       🌏 Kafka Broker URL            : $KAFKA_BROKER"
echo "       🔐 Kafka User                  : $SASL_USER"
echo "       🔐 Kafka Password              : $SASL_PASSWORD"
echo "       🖥️  Kafka Executable            : $KAFKACAT_EXE"
echo "     "
echo "     "
echo "       📂 Directory for Logs          : $WORKING_DIR_LOGS"
echo "   ----------------------------------------------------------------------------------------------------------------------------------------"
echo "   "
echo "   "
echo "   ----------------------------------------------------------------------------------------------------------------------------------------"
echo "     🗄️  Log Files to be loaded"
echo "   ----------------------------------------------------------------------------------------------------------------------------------------"
ls -1 $WORKING_DIR_LOGS | grep "json" | sed 's/^/       /'
echo "     "


echo "   "
echo "   "
echo "   ----------------------------------------------------------------------------------------------------------------------------------------"
echo "     🚀  Preparing Log Data"
echo "   ----------------------------------------------------------------------------------------------------------------------------------------"

#ls -al $WORKING_DIR_LOGS

      mkdir /tmp/inception-files-logs/    >/tmp/demo.log 2>&1  || true
      rm /tmp/inception-files-logs/*    >/tmp/demo.log 2>&1  || true


for actFile in $(ls -1 $WORKING_DIR_LOGS | grep "json"); 
do 

#------------------------------------------------------------------------------------------------------------------------------------
#  Prepare the Data
#------------------------------------------------------------------------------------------------------------------------------------

      echo "      -------------------------------------------------------------------------------------------------------------------------------------"
      echo "        🛠️   Preparing Data for file $actFile"
      echo "      -------------------------------------------------------------------------------------------------------------------------------------"


      #------------------------------------------------------------------------------------------------------------------------------------
      #  Create file and structure in /tmp
      #------------------------------------------------------------------------------------------------------------------------------------
      mkdir /tmp/inception-files-logs/   >/tmp/demo.log 2>&1  || true
      rm /tmp/inception-files-logs/x*   >/tmp/demo.log 2>&1  || true
      rm /tmp/inception-files-logs/timestampedErrorFile.json   >/tmp/demo.log 2>&1  || true
      rm /tmp/inception-files-logs/timestampedErrorFile.json-e   >/tmp/demo.log 2>&1  || true
      rm /tmp/inception-files-logs/logs-robotshop-kafka.json  >/tmp/demo.log 2>&1  || true
      cp $WORKING_DIR_LOGS/$actFile /tmp/inception-files-logs/timestampedErrorFile.json    >/tmp/demo.log 2>&1  || true
      cd /tmp/inception-files-logs/    >/tmp/demo.log 2>&1  || true


      #------------------------------------------------------------------------------------------------------------------------------------
      #  Split the files in 1500 line chunks for kafkacat
      #------------------------------------------------------------------------------------------------------------------------------------
      echo "          🔨 Splitting"
      split -l 1500 ./timestampedErrorFile.json $actFile
      rm timestampedErrorFile.json-e   >/tmp/demo.log 2>&1  || true
      rm timestampedErrorFile.json   >/tmp/demo.log 2>&1  || true
      #cat xaa
      cd -      >/tmp/demo.log 2>&1  || true

      echo "          ✅ OK"
      echo " "
done



echo "   ----------------------------------------------------------------------------------------------------------------------------------------"
echo "     🚀  Generated Log Data Files"
echo "   ----------------------------------------------------------------------------------------------------------------------------------------"
ls -al /tmp/inception-files-logs | sed 's/^/          /'


echo "   "
echo "   "
echo "   "
echo "   "
echo "   ----------------------------------------------------------------------------------------------------------------------------------------"
echo "     🚀  Inject Log Files"
echo "   ----------------------------------------------------------------------------------------------------------------------------------------"


cd /tmp/inception-files-logs/
#ls -1
export NUM_FILES=$(ls | wc -l)
cd -  >/tmp/demo.log 2>&1  || true



#------------------------------------------------------------------------------------------------------------------------------------
#  Inject the Data
#------------------------------------------------------------------------------------------------------------------------------------
echo "      -------------------------------------------------------------------------------------------------------------------------------------"
echo "       🌏  Injecting Log Anomaly Data" 
echo "           Quit with Ctrl-Z"
echo "      -------------------------------------------------------------------------------------------------------------------------------------"
ACT_COUNT=0
for FILE in /tmp/inception-files-logs/*; do 
      if [[ $FILE =~ "json"  ]]; then
            ACT_COUNT=`expr $ACT_COUNT + 1`
            echo "          Injecting file ($ACT_COUNT/$(($NUM_FILES-1))) - $FILE"
            #echo "                 ${KAFKACAT_EXE} -v -X security.protocol=SASL_SSL -X ssl.ca.location=./ca.crt -X sasl.mechanisms=SCRAM-SHA-512  -X sasl.username=token -X sasl.password=$KAFKA_PASSWORD -b $KAFKA_BROKER -P -t $KAFKA_TOPIC_LOGS -l $FILE   "
            ${KAFKACAT_EXE} -v -X security.protocol=SASL_SSL -X ssl.ca.location=./ca.crt -X sasl.mechanisms=SCRAM-SHA-512  -X sasl.username=$SASL_USER -X sasl.password=$SASL_PASSWORD -b $KAFKA_BROKER -P -t $KAFKA_TOPIC_LOGS -l $FILE || true  >/tmp/demo.log 2>&1  || true
            echo " "
            echo "          ✅ OK"
            echo " "
      fi
done

echo "***************************************************************************************************************************************************"
echo "***************************************************************************************************************************************************"
echo "  "
echo "  ✅ Done"
echo "  "
echo "***************************************************************************************************************************************************"
echo "***************************************************************************************************************************************************"




