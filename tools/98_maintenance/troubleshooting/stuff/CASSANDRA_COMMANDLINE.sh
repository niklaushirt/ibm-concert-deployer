echo "   ------------------------------------------------------------------------------------------------------------------------------"
echo "   🔎  Get Cassandra Authentication"	
echo "   ------------------------------------------------------------------------------------------------------------------------------"
export AIOPS_NAMESPACE=$(oc get po -A|grep aiops-orchestrator-controller |awk '{print$1}')
export CASSANDRA_PASS=$(oc get secret aiops-topology-cassandra-auth-secret -n $AIOPS_NAMESPACE -o jsonpath='{.data.password}' | base64 -d)
export CASSANDRA_USER=$(oc get secret aiops-topology-cassandra-auth-secret -n $AIOPS_NAMESPACE -o jsonpath='{.data.username}' | base64 -d)

echo "CASSANDRA_USER:$CASSANDRA_USER"
echo "CASSANDRA_PASS:$CASSANDRA_PASS"




oc exec -ti -n $AIOPS_NAMESPACE aiops-topology-cassandra-0 -- bash -c "/opt/ibm/cassandra/bin/cqlsh --ssl -u $CASSANDRA_USER -p $CASSANDRA_PASS -e  \"SELECT COUNT(*) FROM tararam.dt_metric_value;\""
oc exec -ti -n $AIOPS_NAMESPACE aiops-topology-cassandra-0 -- bash -c "/opt/ibm/cassandra/bin/cqlsh --ssl -u $CASSANDRA_USER -p $CASSANDRA_PASS -e  \"SELECT * FROM tararam.md_metric_resource;\""
oc exec -ti -n $AIOPS_NAMESPACE aiops-topology-cassandra-0 -- bash -c "/opt/ibm/cassandra/bin/cqlsh --ssl -u $CASSANDRA_USER -p $CASSANDRA_PASS -e  \"SELECT * FROM tararam.md_block_resource;\""
oc exec -ti -n $AIOPS_NAMESPACE aiops-topology-cassandra-0 -- bash -c "/opt/ibm/cassandra/bin/cqlsh --ssl -u $CASSANDRA_USER -p $CASSANDRA_PASS -e  \"SELECT * FROM tararam.md_group;\""
oc exec -ti -n $AIOPS_NAMESPACE aiops-topology-cassandra-0 -- bash -c "/opt/ibm/cassandra/bin/cqlsh --ssl -u $CASSANDRA_USER -p $CASSANDRA_PASS -e  \"SELECT * FROM tararam.md_resource;\""



oc exec -ti -n $AIOPS_NAMESPACE aiops-topology-cassandra-0 -- bash -c "/opt/ibm/cassandra/bin/cqlsh --ssl -u $CASSANDRA_USER -p $CASSANDRA_PASS -e  \"SELECT * FROM system_schema.keyspaces;\""
oc exec -ti -n $AIOPS_NAMESPACE aiops-topology-cassandra-0 -- bash -c "/opt/ibm/cassandra/bin/cqlsh --ssl -u $CASSANDRA_USER -p $CASSANDRA_PASS -e  \"SELECT table_name FROM system_schema.tables WHERE keyspace_name = 'tararam';\""


oc exec -ti -n $AIOPS_NAMESPACE aiops-topology-cassandra-0 -- bash -c "/opt/ibm/cassandra/bin/cqlsh --ssl -u $CASSANDRA_USER -p $CASSANDRA_PASS -e  \"describe keyspaces;\""
oc exec -ti -n $AIOPS_NAMESPACE aiops-topology-cassandra-0 -- bash -c "/opt/ibm/cassandra/bin/cqlsh --ssl -u $CASSANDRA_USER -p $CASSANDRA_PASS -e  \"describe keyspace tararam;\""
oc exec -ti -n $AIOPS_NAMESPACE aiops-topology-cassandra-0 -- bash -c "/opt/ibm/cassandra/bin/cqlsh --ssl -u $CASSANDRA_USER -p $CASSANDRA_PASS -e  \"describe tables;\""


oc exec -ti -n $AIOPS_NAMESPACE aiops-topology-cassandra-0 -- bash -c "/opt/ibm/cassandra/bin/cqlsh --ssl -u $CASSANDRA_USER -p $CASSANDRA_PASS"





oc exec -ti -n $AIOPS_NAMESPACE aiops-topology-cassandra-0 -- bash -c "/opt/ibm/cassandra/bin/cqlsh --ssl -u $CASSANDRA_USER -p $CASSANDRA_PASS -e  \"TRUNCATE  tararam.dt_metric_value;\"
oc exec -ti -n $AIOPS_NAMESPACE aiops-topology-cassandra-0 -- bash -c "/opt/ibm/cassandra/bin/cqlsh --ssl -u $CASSANDRA_USER -p $CASSANDRA_PASS -e  \"TRUNCATE  tararam.md_metric_resource;\"




