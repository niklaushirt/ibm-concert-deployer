export AIOPS_NAMESPACE=$(oc get po -A|grep aiops-orchestrator-controller |awk '{print$1}')

export USER_PASS="$(oc get secret aiops-ir-core-ncodl-api-secret -o jsonpath='{.data.username}' | base64 --decode):$(oc get secret -n $AIOPS_NAMESPACE aiops-ir-core-ncodl-api-secret -o jsonpath='{.data.password}' | base64 --decode)"
sleep 2
export DATALAYER_ROUTE=$(oc get route  -n $AIOPS_NAMESPACE datalayer-api  -o jsonpath='{.status.ingress[0].host}')

echo "       ✅ OK - AIOPS_NAMESPACE:    $AIOPS_NAMESPACE"
echo "       ✅ OK - USER_PASS:          $USER_PASS"
echo "       ✅ OK - DATALAYER_ROUTE:    $DATALAYER_ROUTE"




curl "https://$DATALAYER_ROUTE/irdatalayer.aiops.io/active/v1/alerts" --insecure -s  -X GET -u "${USER_PASS}" -H 'Content-Type: application/json' -H 'x-username:admin' -H 'x-subscription-id:cfd95b7e-3bc7-4006-a4a8-a73a79c71255' | jq '.alerts[] |= del(.sender.sourceId, .resource.sourceId, .insights, .firstOccurrenceTime, .lastOccurrenceTime, .lastStateChangeTime, .relatedStoryIds, .relatedContextualStoryIds)' | jq > eu.json






},{
}
{

