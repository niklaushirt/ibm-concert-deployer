#!/bin/sh


echo "*****************************************************************************************************************************"
echo " ✅ STARTING: METRICS STREAMING POD"
echo "*****************************************************************************************************************************"
echo ""
echo "  ⏳ INSTALLATION START TIMESTAMP: $(date)"
echo ""
echo "------------------------------------------------------------------------------------------------------------------------------"


declare -a MY_RES_IDS=(
                    "cfd95b7e-3bc7-4006-a4a8-a73a79c71255","0acf99e5-758b-3d3f-8d8d-6c159322009d","mysql-predictive","MemoryUsagePercent","MemoryUsage","40","9"
                    "cfd95b7e-3bc7-4006-a4a8-a73a79c71255","6e0a7aed-013f-34a7-afa2-dbb66cbf1304","mysql-predictive","MemoryUsageMean","MemoryUsage","50300","500"
                    "cfd95b7e-3bc7-4006-a4a8-a73a79c71255","48fddfac-009b-3cfe-a8d5-9ea76c0e3c4f","mysql-predictive","MemoryUsageMax","MemoryUsage","53980","2000"
                    "cfd95b7e-3bc7-4006-a4a8-a73a79c71255","9ee771c4-6124-3316-ac09-a91e39b64397","mysql-predictive","PodRestarts","PodRestarts","1","1"
                    "cfd95b7e-3bc7-4006-a4a8-a73a79c71255","6f837c30-6dbe-34ca-87b6-1f2abf7eb402","mysql-predictive","TransactionsPerSecond","TransactionsPerSecond","140","20"
                    "cfd95b7e-3bc7-4006-a4a8-a73a79c71255","de4ef4bf-946c-3b27-9863-73c7a7af32d5","mysql-predictive","Latency","Latency","10","4"
                    "cfd95b7e-3bc7-4006-a4a8-a73a79c71255","bdd13495-ed91-316f-8ad2-6575ab59aae5","ratings-predictive","MemoryUsagePercent","MemoryUsage","45","9"
                    "cfd95b7e-3bc7-4006-a4a8-a73a79c71255","caa67515-da0d-33ae-8e56-c03fb35da99b","ratings-predictive","MemoryUsageMean","MemoryUsage","49300","500"
                    "cfd95b7e-3bc7-4006-a4a8-a73a79c71255","a921a433-2878-32b5-a141-769c9717c4bc","ratings-predictive","MemoryUsageMax","MemoryUsage","51980","20000"
                    "cfd95b7e-3bc7-4006-a4a8-a73a79c71255","56afbf4d-4164-3e08-966c-427387e72789","ratings-predictive","PodRestarts","PodRestarts","1","1"
                    "cfd95b7e-3bc7-4006-a4a8-a73a79c71255","820087ad-0a67-3ba5-abce-c2429e7ebece","ratings-predictive","TransactionsPerSecond","TransactionsPerSecond","100","20"
                    "cfd95b7e-3bc7-4006-a4a8-a73a79c71255","e4c36a3d-7ca3-3003-b4b9-4abe4a63ed9e","ratings-predictive","Latency","Latency","2","3"
                    "cfd95b7e-3bc7-4006-a4a8-a73a79c71255","7edec544-92e7-3a88-9e69-8fda5b1c49bb","DCWest1-Rack045-DELL3762","CPU1Temperature","System","80","10"
                    "cfd95b7e-3bc7-4006-a4a8-a73a79c71255","d2643b1c-bd64-3e60-88df-d9c2d969decf","DCWest1-Rack046-DELL3765","CPU1Temperature","System","80","10"
                    "cfd95b7e-3bc7-4006-a4a8-a73a79c71255","46b764cb-9ad6-326d-971b-c15b7423e49a","acme-booking-db","Latency","Latency","20","10"
                    "cfd95b7e-3bc7-4006-a4a8-a73a79c71255","32c45c28-d274-345a-9bb0-7a162565bc43","acme-booking-service","Latency","Latency","15","10"
                    "cfd95b7e-3bc7-4006-a4a8-a73a79c71255","7a82b275-5108-3665-b4bc-c89df485ef50","catalogue-db-predictive","Latency","Latency","18","10"
                    "cfd95b7e-3bc7-4006-a4a8-a73a79c71255","ca73ee22-e57b-38d4-9a40-dad86082bbab","catalogue-predictive","Latency","Latency","12","10"
                    "cfd95b7e-3bc7-4006-a4a8-a73a79c71255","97abafe7-94d3-3aea-b5b7-89c88d069166","acme-booking-service","PodRestarts","PodRestarts","1","1"
                    "cfd95b7e-3bc7-4006-a4a8-a73a79c71255","554d3eb2-c830-3112-a14e-0a54912365d6","acme-booking-db","TransactionsPerSecond","TransactionsPerSecond","110","20"
                    "cfd95b7e-3bc7-4006-a4a8-a73a79c71255","c5b0f2a7-0005-3f53-9eaa-5495d843b454","acme-booking-service","TransactionsPerSecond","TransactionsPerSecond","120","30"
                    "cfd95b7e-3bc7-4006-a4a8-a73a79c71255","3e03e1ba-dbad-3278-a3e6-39797cf0c843","catalogue-db-predictive","TransactionsPerSecond","TransactionsPerSecond","120","20"
                    "cfd95b7e-3bc7-4006-a4a8-a73a79c71255","3fc73093-c20d-3115-8b7c-962f82906e20","catalogue-predictive","TransactionsPerSecond","TransactionsPerSecond","110","20"
                    "cfd95b7e-3bc7-4006-a4a8-a73a79c71255","0fc7bc0d-7c8c-3e70-8091-43d3b2c5d64a","dSwitch-1-vm-network-port-1","TransactionsPerSecond","TransactionsPerSecond","140","10"
                    "cfd95b7e-3bc7-4006-a4a8-a73a79c71255","2b109fd5-8184-3866-918d-970007b57835","dSwitch-5-vm-network-port-1","TransactionsPerSecond","TransactionsPerSecond","110","50"
                    "cfd95b7e-3bc7-4006-a4a8-a73a79c71255","c73fb9e0-bdf4-3e65-b4bb-45926325c269","dcwest1-switch023","TransactionsPerSecond","TransactionsPerSecond","120","30"
                    "cfd95b7e-3bc7-4006-a4a8-a73a79c71255","8755be37-a078-3f8d-9d18-5b9a07c34748","dcwest1-switch025","TransactionsPerSecond","TransactionsPerSecond","140","30"
)


#  "dSwitch-1-vm-network-port-1,TransactionsPerSecond,TransactionsPerSecond,0,1"
#   "dcwest1-switch023,TransactionsPerSecond,TransactionsPerSecond,60,30"


export INTERVAL_SECONDS=5

export AIOPS_NAMESPACE=$(oc get po -A|grep aimanager-operator |awk '{print$1}')
echo "       ✅ OK - AI Manager:               $AIOPS_NAMESPACE"


#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# DO NOT MODIFY BELOW
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

export DATE_FORMAT="+%s"
export DATE_FORMAT_READABLE="+%Y-%m-%d %H:%M:%S"



echo "   "
echo "   "
echo "   "
echo "   "
echo "   ----------------------------------------------------------------------------------------------------------------------------------------"
echo "     🚀  Inject Synthetic Metrics"
echo "   ----------------------------------------------------------------------------------------------------------------------------------------"



echo "   ----------------------------------------------------------------------------------------------------------------------------------------"
echo "     🔐  Getting Namespace"
echo "   ----------------------------------------------------------------------------------------------------------------------------------------"
export AIOPS_NAMESPACE=$(oc get po -A|grep aiops-orchestrator-controller |awk '{print$1}')

oc project $AIOPS_NAMESPACE >/dev/null 2>/dev/null




#--------------------------------------------------------------------------------------------------------------------------------------------
#  Launch Log Injection as a parallel thread
#--------------------------------------------------------------------------------------------------------------------------------------------
echo "      -------------------------------------------------------------------------------------------------------------------------------------"
echo "       🌏  Injecting Metrics Anomaly Data" 
echo "           Quit with Ctrl-Z"
echo "      -------------------------------------------------------------------------------------------------------------------------------------"
echo ""

# Loop until CTRL-C
while true
do

      export HR_BASE_TIMESTAMP=$(date "$DATE_FORMAT_READABLE")
      export BASE_TIMESTAMP=$HR_BASE_TIMESTAMP"+00"

      echo "        Iteration at "$BASE_TIMESTAMP
      VALUES=""

      for value in "${MY_RES_IDS[@]}"
      do

            #echo $value


            t_uid=$(echo $value | cut -d',' -f1)
            mr_id=$(echo $value | cut -d',' -f2)
            MY_RESOURCE_ID=$(echo $value | cut -d',' -f3)
            MY_METRIC_NAME=$(echo $value | cut -d',' -f4)
            MY_GROUP_ID=$(echo $value | cut -d',' -f5)
            MY_FIX_VALUE=$(echo $value | cut -d',' -f6)
            MY_VARIATION=$(echo $value | cut -d',' -f7)
            
            my_random_value=$(($RANDOM%(100*$MY_VARIATION)))
            #echo $my_random_value
            export CURRENT_VALUE=$(echo $(($my_random_value+(100*$MY_FIX_VALUE)))| sed -e 's/..$/.&/;t' -e 's/.$/.0&/')
            #echo "Current Value: "$CURRENT_VALUE


            my_random_value=$(($RANDOM%(100*$MY_VARIATION)))
            export CURRENT_VALUE=$(echo $(($my_random_value+(100*$MY_FIX_VALUE)))| sed -e 's/..$/.&/;t' -e 's/.$/.0&/')
            export AVG_VALUE=$(($MY_VARIATION/2+$MY_FIX_VALUE))
            export MAX_VALUE=$(($MY_VARIATION+$MY_FIX_VALUE))
            export MIN_VALUE=$(($MY_FIX_VALUE))

            echo "           - Resource: "$MY_RESOURCE_ID", Metric: "$MY_METRIC_NAME", Value: "$CURRENT_VALUE", Min: "$MIN_VALUE", Max: "$MAX_VALUE", Avg: "$AVG_VALUE


            VALUES=$VALUES"('"$t_uid"','"$mr_id"','"$BASE_TIMESTAMP"','"$CURRENT_VALUE"','"$MIN_VALUE"','"$MAX_VALUE"','"$AVG_VALUE"','f'),"

      done
      export VALUES=$(echo $VALUES | sed 's/.$//')
      export SQL_COMMAND="INSERT INTO aiops_ir_ai.metric_values (t_uid, mr_id, tstamp, value, min, max, expected, anomalous) VALUES $VALUES;"
      
      #echo $SQL_COMMAND

      oc exec -ti -n $AIOPS_NAMESPACE aiops-ir-analytics-postgres-1 -c postgres -- bash -c "psql -U postgres -d aiops_ir_ai -c \"${SQL_COMMAND}\""

      sleep $INTERVAL_SECONDS
done


