# https://github.com/ibm/aiops-ui-extension-template
# https://github.com/IBM/aiops-ui-extension-template/blob/30bf967282a2520089112eb9181ebefefa06b249/doc/getting-started.md


#--------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------
# Create for your user in the UI
export API_KEY=xxxxxx
#--------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------




#cd /tmp
cd 
git clone https://github.com/ibm/aiops-ui-extension-template
cd aiops-ui-extension-template

rm target.json

npm i
npm run enable -- -n ibm-aiops


export AIOPS_NAMESPACE=$(oc get po -A|grep aiops-orchestrator-controller |awk '{print$1}')
export CPD_ROUTE=$(oc get route -n $AIOPS_NAMESPACE cpd  -o jsonpath={.spec.host})          
export CPADMIN_PWD=$(oc -n $AIOPS_NAMESPACE get secret platform-auth-idp-credentials -o jsonpath='{.data.admin_password}' | base64 -d && echo)
export CPADMIN_USER=$(oc -n $AIOPS_NAMESPACE get secret platform-auth-idp-credentials -o jsonpath='{.data.admin_username}' | base64 -d && echo)


cat <<EOF >target.json
{
  "url": "https://$CPD_ROUTE/",
  "username": "$CPADMIN_USER",
  "apiKey": "$API_KEY",
  "tenantId": "cfd95b7e-3bc7-4006-a4a8-a73a79c71255",
  "bundleName": "alerts-examples"
}
EOF
cat target.json
npm run deploy -- -n  ibm-aiops


cat target.json


npm start

npm run deploy -- -n  ibm-aiops


