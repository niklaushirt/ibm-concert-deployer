export AIOPS_NAMESPACE=$(oc get po -A|grep aiops-orchestrator-controller |awk '{print$1}')
PGUSER=$(oc get secret -n $AIOPS_NAMESPACE aiops-topology-postgres-user -o jsonpath="{.data.username}"| base64 --decode)
PGASSWORD=$(oc get secret -n $AIOPS_NAMESPACE aiops-topology-postgres-user -o jsonpath="{.data.password}"| base64 --decode)
echo "Connect to:    jdbc:postgresql://localhost/aiops_topology"
echo "User:          $PGUSER"
echo "Password:      $PGASSWORD"
oc -n $AIOPS_NAMESPACE port-forward ibm-aiops-edb-postgres-1 5432:5432



