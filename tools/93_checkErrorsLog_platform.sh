
#oc delete ConsoleNotification --all>/dev/null 2>/dev/null

cat <<EOF | oc apply -f -
apiVersion: console.openshift.io/v1
kind: ConsoleNotification
metadata:
    name: ibm-concert-operate-notification-main
spec:
    backgroundColor: '#1122aa'
    color: '#fff'
    location: BannerTop
    text: "🔎 FINALIZING: Checking Installation Logs"
EOF


num_failed=$(cat /tmp/ansible.log|grep "failed=[1-9]"|wc -l)
if [ $num_failed -gt 0 ];
then
echo "ERROR in Logs"
echo ""
echo "*****************************************************************************************************************************"
echo " ❌ FATAL ERROR: Please check the Installation Logs"
echo "*****************************************************************************************************************************"
OPENSHIFT_ROUTE=$(oc get route -n openshift-console console -o jsonpath={.spec.host})
INSTALL_POD=$(oc get po -n ibm-installer -l app=ibm-installer --no-headers|grep "Running"|grep "1/1"|awk '{print$1}')

oc delete ConsoleNotification ibm-concert-operate-notification
cat <<EOF | oc apply -f -
apiVersion: console.openshift.io/v1
kind: ConsoleNotification
metadata:
    name: ibm-concert-operate-notification-main
spec:
    backgroundColor: '#9a0000'
    color: '#fff'
    location: "BannerTop"
    text: "❌ FATAL ERROR: Please check the Installation Logs and re-run the installer by deleting the Pod"
    link:
        href: "https://$OPENSHIFT_ROUTE/k8s/ns/ibm-installer/pods/$INSTALL_POD/logs"
        text: Open Logs

EOF
else

oc delete ConsoleNotification ibm-concert-operate-notification-concert>/dev/null 2>/dev/null
oc delete ConsoleNotification ibm-concert-operate-notification-password>/dev/null 2>/dev/null
oc delete ConsoleNotification ibm-concert-operate-notification-status>/dev/null 2>/dev/null   
export CONCERT_NAMESPACE=$(oc get po -A|grep roja-portal |awk '{print$1}')
export appURL=$(oc get routes -n $CONCERT_NAMESPACE concert  -o jsonpath="{['spec']['host']}")|| true
cat <<EOF | oc apply -f -
apiVersion: console.openshift.io/v1
kind: ConsoleNotification
metadata:
    name: ibm-concert-operate-notification-concert
spec:
    backgroundColor: '#009a00'
    color: '#fff'
    link:
        href: "https://$appURL"
        text: IBM Concert Platform
    location: BannerTop
    text: "✅ IBM Concert Platform is installed in this cluster. 🚀 Access it here:"
EOF

echo ""
echo " 🟢🟢🟢 Logs are looking good."
fi









