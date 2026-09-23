#!/bin/bash

# 20 ITERATIONS gives you about 2.5 months of synthetic data
export MAX_ITERATIONS=20

# The default work sub-directory
export DIR_PREFIX=my-data







#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# DO NOT MODIFY BELOW
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

declare -a MY_RES_IDS=()
export DEFAULT_FILTER="."


echo "***************************************************************************************************************************************"
echo "***************************************************************************************************************************************"
echo ""
echo " 🚀  Concert Operate Load Synthetic Metrics Dump"
echo ""
echo "***************************************************************************************************************************************"
echo ""
echo ""


if [[ $INPUT_DIR_PREFIX == "" ]];
then

      echo "     --------------------------------------------------------------------------------------------"
      echo "     📂 Specify the output sub-directory (default is $DIR_PREFIX): "
      read INPUT_DIR_PREFIX
else
      export DIR_PREFIX=$INPUT_DIR_PREFIX
fi
if [[ $INPUT_DIR_PREFIX == "" ]];
then 
      export DIR_PREFIX=$DIR_PREFIX
else
      export DIR_PREFIX=$INPUT_DIR_PREFIX
fi
echo ""
echo ""

export WORKING_DIR_OUTPUT="./$DIR_PREFIX/output"

DUMPS_EXIST=$(ls -1 $WORKING_DIR_OUTPUT| wc -l)

if [[ ! $DUMPS_EXIST -gt "0" ]]; then
      echo "    ❗ No Dumps Present - you have to create dumps first or copy them manually to $WORKING_DIR_OUTPUT"
      echo "    ❗ Aborting...."
      exit 0

else
      echo "    ✅ Dumps Exist"
fi


echo "***************************************************************************************************************************************"
echo "***************************************************************************************************************************************"
echo ""
echo ""
echo ""
echo ""



echo "***************************************************************************************************************************************"
echo "***************************************************************************************************************************************"
echo " 📂  Directories" 
echo "***************************************************************************************************************************************"
echo "***************************************************************************************************************************************"
echo ""
echo "Synthetic Data:       $WORKING_DIR_OUTPUT"
echo ""
echo ""
echo ""







echo "***************************************************************************************************************************************"
echo "***************************************************************************************************************************************"
echo " 🚀   LOAD files into Cassandra tables from $WORKING_DIR_OUTPUT" 
echo "***************************************************************************************************************************************"
echo "***************************************************************************************************************************************"
echo ""

read -p "  Do you want to load the new synthetic data into Cassandra❓ [y,N] " DO_COMM
if [[ $DO_COMM == "y" ||  $DO_COMM == "Y" ]]; then

      echo  ""    
      echo  ""
      echo "     --------------------------------------------------------------------------------------------"
      echo "     💾 Copy files to Pod filesystem (you can ignore rsync not available in container)"
      oc exec -ti aiops-topology-cassandra-0 -- bash -c "rm /tmp/tara*"| sed 's/^/           /'
      #ls -1 $WORKING_DIR_OUTPUT| sed 's/^/           /'
      oc rsync $WORKING_DIR_OUTPUT/ aiops-topology-cassandra-0:/tmp/| sed 's/^/           /'


      echo  ""    
      echo  ""
      echo "     --------------------------------------------------------------------------------------------"
      echo "     🧻 Empty the tables"
      oc exec -ti aiops-topology-cassandra-0 -- bash -c "/opt/ibm/cassandra/bin/cqlsh --ssl -u \$CASSANDRA_USER -p \$CASSANDRA_PASS -e \"TRUNCATE  tararam.dt_metric_value;\""| sed 's/^/           /'
      oc exec -ti aiops-topology-cassandra-0 -- bash -c "/opt/ibm/cassandra/bin/cqlsh --ssl -u \$CASSANDRA_USER -p \$CASSANDRA_PASS -e \"TRUNCATE  tararam.md_metric_resource;\""| sed 's/^/           /'


      echo  ""    
      echo  ""
      echo "     --------------------------------------------------------------------------------------------"
      echo "     📥 Load the dumps"
      oc exec -ti aiops-topology-cassandra-0 -- bash -c "/opt/ibm/cassandra/bin/cqlsh --ssl -u \$CASSANDRA_USER -p \$CASSANDRA_PASS -e \"copy tararam.dt_metric_value from '/tmp/tararam.dt_metric_value.csv' with header=true;\""| sed 's/^/           /'
      oc exec -ti aiops-topology-cassandra-0 -- bash -c "/opt/ibm/cassandra/bin/cqlsh --ssl -u \$CASSANDRA_USER -p \$CASSANDRA_PASS -e \"copy tararam.md_metric_resource from '/tmp/tararam.md_metric_resource.csv' with header=true;\""| sed 's/^/           /'



      echo  ""    
      echo  ""
      echo "     --------------------------------------------------------------------------------------------"
      echo "     🔎 Check the data"
      oc exec -ti aiops-topology-cassandra-0 -- bash -c "/opt/ibm/cassandra/bin/cqlsh --ssl -u \$CASSANDRA_USER -p \$CASSANDRA_PASS -e \"SELECT COUNT(*) FROM tararam.dt_metric_value;\""| sed 's/^/           /'
      oc exec -ti aiops-topology-cassandra-0 -- bash -c "/opt/ibm/cassandra/bin/cqlsh --ssl -u \$CASSANDRA_USER -p \$CASSANDRA_PASS -e \"SELECT * FROM tararam.md_metric_resource;\""| sed 's/^/           /'


else
      echo "    ⚠️  Skipping"
      echo "--------------------------------------------------------------------------------------------"
      echo  ""    
      echo  ""
fi
      echo  ""    
      echo  ""
      echo  ""    
      echo  ""




echo "***************************************************************************************************************************************"
echo "***************************************************************************************************************************************"
echo ""
echo " 🚀  Concert Operate Create Synthetic Metrics"
echo " ✅  Done..... "
echo ""
echo "***************************************************************************************************************************************"
echo "***************************************************************************************************************************************"


