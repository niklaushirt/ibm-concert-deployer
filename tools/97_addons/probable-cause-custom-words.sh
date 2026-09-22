
    echo "----------------------------------------------------------------------------------------------------------"
    echo "----------------------------------------------------------------------------------------------------------"
    echo "🚀 PROBABLE CAUSE - CUSTOM WORD LIST"
    echo "----------------------------------------------------------------------------------------------------------"


export AIOPS_NAMESPACE=$(oc get po -A|grep aimanager-operator |awk '{print$1}')
export ROUTE=$(oc get -n $AIOPS_NAMESPACE route | grep ibm-nginx-svc | awk '{print $2}')
echo $ROUTE
PASS=$(oc get secret -n $AIOPS_NAMESPACE admin-user-details -o jsonpath='{.data.initial_admin_password}' | base64 --decode)
echo $PASS
export TOKEN=$(curl -k -s -X POST https://$ROUTE/icp4d-api/v1/authorize -H 'Content-Type: application/json' -d "{\"username\": \"admin\",\"password\": \"$PASS\"}" | jq .token | sed 's/\"//g')
echo $TOKEN



echo ""
echo ""
echo "----------------------------------------------------------------------------------------------------------"
echo "   🚀 PROBABLE CAUSE - BACKUP WORD LIST"


curl -k -X GET  --header 'Accept: application/json' -H "Authorization: Bearer ${TOKEN}" https://$ROUTE/aiops/api/issue-resolution/mime/v1/customisation/words -H "accept: application/json" -H "Content-Type: application/json" -H "X-TenantID: cfd95b7e-3bc7-4006-a4a8-a73a79c71255" > backup_words.json




echo ""
echo ""
echo "----------------------------------------------------------------------------------------------------------"
echo "   🚀 PROBABLE CAUSE - EMPTY WORD LIST"


curl -k -X POST --header 'Accept: application/json' -H "Authorization: Bearer ${TOKEN}" -H "Content-Type: application/json" https://$ROUTE/aiops/api/issue-resolution/mime/v1/customisation/words -H "accept: application/json" -H "X-TenantID: cfd95b7e-3bc7-4006-a4a8-a73a79c71255" -d '
{"words": [
    {
            "word": "empty",
            "caseSenstive": false,
            "weight": 99.0
        }]
    }'

curl -k -X GET  --header 'Accept: application/json' -H "Authorization: Bearer ${TOKEN}" https://$ROUTE/aiops/api/issue-resolution/mime/v1/customisation/words -H "accept: application/json" -H "Content-Type: application/json" -H "X-TenantID: cfd95b7e-3bc7-4006-a4a8-a73a79c71255" 






    echo ""
    echo ""
    echo "----------------------------------------------------------------------------------------------------------"
    echo "   🚀 PROBABLE CAUSE - LOAD WORD LIST"

curl -k -X POST --header 'Accept: application/json' -H "Authorization: Bearer ${TOKEN}" -H "Content-Type: application/json" https://$ROUTE/aiops/api/issue-resolution/mime/v1/customisation/words -H "accept: application/json" -H "X-TenantID: cfd95b7e-3bc7-4006-a4a8-a73a79c71255" -d '{"words": [
{
        "word": "Commit",
        "caseSenstive": true,
        "weight": 200.0
    }, {
        "word": "Erroneus",
        "caseSenstive": true,
        "weight": 50.0
    },  {
            "word": "change detected",
            "caseSenstive": true,
            "weight": 80.0
    },{
        "word": "not responding",
        "caseSenstive": false,
        "weight": 70.0
    }, {
        "word": "LOF",
        "caseSenstive": true,
        "weight": 50.0
    }, {
        "word": "unreachable",
        "caseSenstive": false,
        "weight": 20.0
    }, {
        "word": "cpu",
        "caseSenstive": false,
        "weight": 40.0
    }, {
        "word": "utilization",
        "caseSenstive": false,
        "weight": 20.0
    }, {
        "word": "LOS",
        "caseSenstive": true,
        "weight": 60.0
    }, {
        "word": "100",
        "caseSenstive": false,
        "weight": 60.0
    }, {
        "word": "fail",
        "caseSenstive": false,
        "weight": 70.0
    }, {
        "word": "disk",
        "caseSenstive": false,
        "weight": 40.0
    }, {
        "word": "80",
        "caseSenstive": false,
        "weight": 30.0
    }, {
        "word": "change",
        "caseSenstive": false,
        "weight": 40.0
    }, {
        "word": "60",
        "caseSenstive": false,
        "weight": 15.0
    }, {
        "word": "85",
        "caseSenstive": false,
        "weight": 35.0
    }, {
        "word": "shutdown",
        "caseSenstive": false,
        "weight": 50.0
    }, {
        "word": "closed",
        "caseSenstive": false,
        "weight": 40.0
    }, {
        "word": "full",
        "caseSenstive": false,
        "weight": 40.0
    }, {
        "word": "critical",
        "caseSenstive": false,
        "weight": 50.0
    }, {
        "word": "configuration",
        "caseSenstive": false,
        "weight": 20.0
    }, {
        "word": "update",
        "caseSenstive": false,
        "weight": 40.0
    }, {
        "word": "battery",
        "caseSenstive": false,
        "weight": 40.0
    }, {
        "word": "malfunction",
        "caseSenstive": false,
        "weight": 40.0
    }, {
        "word": "down",
        "caseSenstive": false,
        "weight": 40.0
    }, {
        "word": "loss",
        "caseSenstive": false,
        "weight": 30.0
    }, {
        "word": "high",
        "caseSenstive": false,
        "weight": 40.0
    }, {
        "word": "lost",
        "caseSenstive": false,
        "weight": 40.0
    }, {
        "word": "fan",
        "caseSenstive": false,
        "weight": 40.0
    }, {
        "word": "90",
        "caseSenstive": false,
        "weight": 40.0
    }, {
        "word": "70",
        "caseSenstive": false,
        "weight": 20.0
    }, {
        "word": "shut down",
        "caseSenstive": false,
        "weight": 50.0
    }, {
        "word": "50",
        "caseSenstive": false,
        "weight": 5.0
    }, {
        "word": "95",
        "caseSenstive": false,
        "weight": 50.0
    }, {
        "word": "75",
        "caseSenstive": false,
        "weight": 25.0
    }, {
        "word": "utilisation",
        "caseSenstive": false,
        "weight": 20.0
    }, {
        "word": "55",
        "caseSenstive": false,
        "weight": 10.0
    }, {
        "word": "temperature",
        "caseSenstive": false,
        "weight": 40.0
    }]
}'
curl -k -X GET  --header 'Accept: application/json' -H "Authorization: Bearer ${TOKEN}" https://$ROUTE/aiops/api/issue-resolution/mime/v1/customisation/words -H "accept: application/json" -H "Content-Type: application/json" -H "X-TenantID: cfd95b7e-3bc7-4006-a4a8-a73a79c71255" 
