export AIOPS_NAMESPACE=$(oc get po -A|grep aiops-orchestrator-controller |awk '{print$1}')
oc delete pod -n $AIOPS_NAMESPACE --ignore-not-found $(oc get po -n $AIOPS_NAMESPACE|grep -v Completed|grep 0/|awk '{print$1}')


