#!/bin/bash
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
#  Concert platform - Check Installation
#
#
#  ©2026 nikh@ch.ibm.com
# ---------------------------------------------------------------------------------------------------------------------------------------------------"
# ---------------------------------------------------------------------------------------------------------------------------------------------------"
# ---------------------------------------------------------------------------------------------------------------------------------------------------"
# ---------------------------------------------------------------------------------------------------------------------------------------------------"



export ERROR_STRING=""
export WARNING_STRING=""

export ERROR=false
export WARNING_STATE=false

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
    text: "🔎 FINALIZING: Checking IBM Concert platform Installation"
EOF




# ---------------------------------------------------------------------------------------------------------------------------------------------------"
# ---------------------------------------------------------------------------------------------------------------------------------------------------"
# Do Not Edit Below
# ---------------------------------------------------------------------------------------------------------------------------------------------------"
# ---------------------------------------------------------------------------------------------------------------------------------------------------"
function handleError(){
    if  ([[ $CURRENT_ERROR == true ]]); 
    then
        ERROR=true
        ERROR_STRING=$ERROR_STRING"\n⭕ $CURRENT_ERROR_STRING"
        echo "      "
        echo "      "
        echo "      ❗***************************************************************************************************************************************************"
        echo "      ❗***************************************************************************************************************************************************"
        echo "      ❗  ❌ The following error was found: "
        echo "      ❗"
        echo "      ❗      ⭕ $CURRENT_ERROR_STRING"; 
        echo "      ❗"
        echo "      ❗***************************************************************************************************************************************************"
        echo "      ❗***************************************************************************************************************************************************"
        echo "      "
        echo "      "

    fi
}


function handleWarning(){
    if  ([[ $CURRENT_WARNING_STATE == true ]]); 
    then
        WARNING_STATE=true
        WARNING_STRING=$WARNING_STRING"\n ⚠️  $CURRENT_WARNING_STRING"
        echo "        ⚠️ ***************************************************************************************************************************************************"
        echo "        ⚠️ ***************************************************************************************************************************************************"
        echo "        ⚠️   The following warning was found: "
        echo "        ⚠️ "
        echo "        ⚠️       ⚠️  $CURRENT_WARNING_STRING"; 
        echo "        ⚠️ "
        echo "        ⚠️ ***************************************************************************************************************************************************"
        echo "        ⚠️ ***************************************************************************************************************************************************"
    fi
}




#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# EXAMINE INSTALLATION
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
      echo ""
      echo "  ------------------------------------------------------------------------------------------------------------------------------------------------------"
      echo "  🚀 Initializing"
      echo "  ------------------------------------------------------------------------------------------------------------------------------------------------------"
      echo ""
      echo "   🛠️  Get Namespaces"
      export CONCERT_NAMESPACE=$(oc get po -A|grep roja-portal |awk '{print$1}')
      export CONCERT_HUB_NAMESPACE=$(oc get po -A|grep ibm-solis-core |awk '{print$1}')
      export CONCERT_WORKFLOWS_NAMESPACE=$(oc get po -A|grep rna-core-mysql |awk '{print$1}')
      export CONCERT_DATAAPPS_NAMESPACE=$(oc get po -A|grep dataapps-solis |awk '{print$1}')
      export CONCERT_OPTIMISE_NAMESPACE=$(oc get po -A|grep t8c-operator |awk '{print$1}')
      echo "CONCERT_NAMESPACE:            $CONCERT_NAMESPACE"
      echo "CONCERT_HUB_NAMESPACE:        $CONCERT_HUB_NAMESPACE"
      echo "CONCERT_WORKFLOWS_NAMESPACE:  $CONCERT_WORKFLOWS_NAMESPACE"
      echo "CONCERT_DATAAPPS_NAMESPACE:   $CONCERT_DATAAPPS_NAMESPACE"
      echo "CONCERT_OPTIMISE_NAMESPACE:   $CONCERT_OPTIMISE_NAMESPACE"



      echo ""
      echo ""
      echo "  ----------------------------------------------------------------------------------------------------------------------------------------------------------"
      echo "   🚀  CHECK IBMDemo Namespaces" 
      echo "  ----------------------------------------------------------------------------------------------------------------------------------------------------------"
      echo ""

    checkNamespace () {
      echo "    🔎 Pods not ready in Namespace $CURRENT_NAMESPACE"

      export ERROR_PODS=$(oc get pods -n $CURRENT_NAMESPACE | grep -v "Completed" | grep "0/"|awk '{print$1}')
      export ERROR_PODS_COUNT=$(oc get pods -n $CURRENT_NAMESPACE | grep -v "Completed" |grep -v nginx-ingress-controller| grep "0/"| grep -c "")
      if  ([[ $ERROR_PODS_COUNT -gt 0 ]]); 
      then 
            export CURRENT_WARNING_STATE=true
            export CURRENT_WARNING_STRING="$ERROR_PODS_COUNT Pods not running in Namespace "$CURRENT_NAMESPACE"  \n"$ERROR_PODS
            handleWarning
      else  
            echo "          ✅ OK: All Pods running and ready in Namespace $CURRENT_NAMESPACE"; 
      fi
      echo ""
      echo ""
    }



      export CURRENT_NAMESPACE=$CONCERT_NAMESPACE
      checkNamespace

      export CURRENT_NAMESPACE=$CONCERT_HUB_NAMESPACE
      checkNamespace

      export CURRENT_NAMESPACE=$CONCERT_WORKFLOWS_NAMESPACE
      checkNamespace

      export CURRENT_NAMESPACE=$CONCERT_DATAAPPS_NAMESPACE
      checkNamespace

      export CURRENT_NAMESPACE=openldap
      checkNamespace

      # export CURRENT_NAMESPACE=sock-shop
      # checkNamespace

      # export CURRENT_NAMESPACE=robot-shop
      # checkNamespace

      # export CURRENT_NAMESPACE=acme-air
      # checkNamespace

      # export CURRENT_NAMESPACE=galaxium-travels
      # checkNamespace



#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# WRAP UP
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------



      echo ""
      echo ""
    if  ([[ $ERROR == true ]]); 
    then
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ERROR
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        shopt -s xpg_echo
        echo ""
        echo ""
        echo "***************************************************************************************************************************************************"
        echo "***************************************************************************************************************************************************"
        echo "  ❗ Your installation has the following problems ❗"
        echo ""
        echo "      $ERROR_STRING" | sed 's/^/       /'
        echo ""
        echo "***************************************************************************************************************************************************"
        echo "***************************************************************************************************************************************************"
        echo ""
        echo "  🚀 Try to re-run the installer to see if this solves the problem"
        echo "  🛠️  To do this just delete the ibm-install-concert pod in the ibm-installer Namespace"
        echo "  🛠️  Explained in detail here: https://github.com/niklaushirt/ibm-concert-deployer/tree/main#re-run-the-installer"
        echo ""
        echo "***************************************************************************************************************************************************"
        echo "***************************************************************************************************************************************************"
        echo ""

        echo ""
        echo ""
        OPENSHIFT_ROUTE=$(oc get route -n openshift-console console -o jsonpath={.spec.host})
        INSTALL_POD=$(oc get po -n ibm-installer -l app=ibm-installer --no-headers|grep "Running"|grep "1/1"|awk '{print$1}')

#oc delete ConsoleNotification --all>/dev/null 2>/dev/null
cat <<EOF | oc apply -f -
apiVersion: console.openshift.io/v1
kind: ConsoleNotification
metadata:
    name: ibm-concert-operate-notification-warning
spec:
    backgroundColor: '#dd4500'
    color: '#fff'
    location: "BannerTop"
    text: "⚠️ WARNING: Your Installation has some problems. Please check the Installation Logs and re-run the installer by deleting the Pod"
EOF

    elif  ([[ $WARNING_STATE == true ]]); 
    then
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# OK
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        shopt -s xpg_echo
        echo ""
        echo ""
        echo "***************************************************************************************************************************************************"
        echo "***************************************************************************************************************************************************"
        echo ""
        echo "  🟢🟢🟢 Your installation looks fine"
        echo ""
        echo ""
        echo "  ⚠️  But we encountered the following non blocking warnings"
        echo ""
        echo "      $WARNING_STRING" | sed 's/^/       /'
        echo ""
        echo "***************************************************************************************************************************************************"
        echo "***************************************************************************************************************************************************"
        echo ""


    else
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# NO ERROR
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        echo "***************************************************************************************************************************************************"
        echo "***************************************************************************************************************************************************"
        echo ""
        echo "  🟢🟢🟢 Your installation looks fine"
        echo ""
        echo "***************************************************************************************************************************************************"
        echo "***************************************************************************************************************************************************"

    fi



echo ""
echo ""
echo ""
echo ""
echo ""
echo ""
echo ""
echo ""
echo ""
echo ""
echo ""
echo ""
echo ""
echo ""
echo ""
echo ""
echo ""
echo ""
echo ""
echo ""
echo ""
echo ""

echo "***************************************************************************************************************************************************"
echo "***************************************************************************************************************************************************"
echo "***************************************************************************************************************************************************"
echo "***************************************************************************************************************************************************"
echo "***************************************************************************************************************************************************"
echo "***************************************************************************************************************************************************"
echo "***************************************************************************************************************************************************"
echo "***************************************************************************************************************************************************"
echo ""
echo "  🟢🟢🟢 Your Concert platform Credentials"
echo ""
echo "***************************************************************************************************************************************************"
echo "***************************************************************************************************************************************************"

cd  /tmp/ibm-concert
echo ""
echo ""
echo "------------------------------------------------------------------------------------------------------------------------------"
echo " ✅ LOGINS"
echo "------------------------------------------------------------------------------------------------------------------------------"

export OCP_URL=$(oc get Infrastructure cluster -o jsonpath={.status.apiServerURL})
export OCP_TOKEN=$(oc create token -n ibm-installer ibm-installer-admin --duration=999999999s)
#export OCP_TOKEN=$(oc -n openshift-authentication get secret $(oc get secret -n openshift-authentication |grep -m1 oauth-openshift-token|awk '{print$1}') -o jsonpath='{.data.token}'|base64 --decode)
echo "  🌏 URL:         $OCP_URL"
echo "  🫅 User:        kubeadmin"
echo "  🔐 Token:       $OCP_TOKEN"
echo ""
echo ""
echo ""
echo ""
echo ""
echo ""


echo "------------------------------------------------------------------------------------------------------------------------------"
echo " ✅ LOGINS FOR RESILIENCE"
echo "------------------------------------------------------------------------------------------------------------------------------"
oc create serviceaccount -n default demo-admin-concert>/dev/null 2>/dev/null
oc create clusterrolebinding demo-admin-concert --clusterrole=cluster-admin --serviceaccount=default:demo-admin-concert>/dev/null 2>/dev/null
API_TOKEN=$(oc create token -n default demo-admin-concert --duration=999999999s)

CONSOLE_PATH=$(oc get route -n openshift-console console -o jsonpath={.spec.host})
CONSOLE_URL="https://"$CONSOLE_PATH
API_URL=${CONSOLE_URL/console-openshift-console.apps/api}:6443

echo ""
echo "  🌏 API URL  :   $API_URL"
echo "  🔐 API TOKEN:   $API_TOKEN"

echo ""
echo ""
echo ""
echo ""
echo ""
echo ""






echo "------------------------------------------------------------------------------------------------------------------------------"
echo " ✅ CHECK WATSONX CREDENTIALS"
echo "------------------------------------------------------------------------------------------------------------------------------"
CONCERT_NAMESPACE=$(oc get po -A|grep roja-portal |awk '{print$1}')

API_KEY="$(oc get secret app-cfg-secret -n $CONCERT_NAMESPACE -o jsonpath='{ .data.WATSONX_API_KEY }' | base64 --decode)"


RESPONSE=$(curl -s -X POST \
https://iam.cloud.ibm.com/identity/token \
-H "Content-Type: application/x-www-form-urlencoded" \
-d "grant_type=urn:ibm:params:oauth:grant-type:apikey&apikey=$API_KEY")

#echo "$RESPONSE" | jq

if echo "$RESPONSE" | jq -e '.errorMessage' > /dev/null 2>&1; then
echo ""
echo "    🔴🔴🔴🔴🔴🔴 WATSONX TOKEN INVALID - Error returned from IAM. You won't be able to access the WatsonX services in Concert platform."
echo ""
exit 1
else
echo ""
echo "    ✅ Successfully retrieved IAM token. You can access the WatsonX services in Concert platform."
echo ""
fi

echo "  ------------------------------------------------------------------------------------------------------------------------------"
echo "  🛠️ Available Projects:"

IAM_TOKEN=$(echo "$RESPONSE" | jq -r .access_token)


curl -s \
-H "Authorization: Bearer $IAM_TOKEN" \
"https://api.dataplatform.cloud.ibm.com/v2/projects?limit=100" | jq -r '.resources[] | "     - " + .entity.name + " - " + .metadata.guid'

echo ""
echo ""
echo ""
echo ""
echo ""
echo ""



echo "------------------------------------------------------------------------------------------------------------------------------"
echo " ✅ LDAP CREDENTIALS"
echo "------------------------------------------------------------------------------------------------------------------------------"

echo "id": "LDAP",
echo "realm": "REALM",
echo "url": "ldap://openldap.openldap:389",
echo "host": "openldap.openldap",
echo "port": "389",
echo "protocol": "ldap",
echo "basedn": "dc=ibm,dc=com",
echo "binddn": "cn=admin,dc=ibm,dc=com",
echo "bindpassword: The one you selected at installation time",
echo "type": "Custom",
echo "ignorecase": "false",
echo "userfilter": "(&(uid=%v)(objectclass=Person))",
echo "useridmap": "*:uid",
echo "groupfilter": "(&(cn=%v)(objectclass=groupOfUniqueNames))",
echo "groupidmap": "*:cn",
echo "groupmemberidmap": "groupOfUniqueNames:uniqueMember",
echo "nestedsearch": "false",
echo "pagingsearch": "false"
export openldap_app_route=$(oc get route -n openldap admin -o jsonpath={.spec.host})          
echo "openldap_app_route:     https://$openldap_app_route"


oc delete ConsoleNotification ibm-concert-operate-notification-openldap>/dev/null 2>/dev/null
cat <<EOF | oc apply -f -
apiVersion: console.openshift.io/v1
kind: ConsoleNotification
metadata:
      name: ibm-concert-operate-notification-openldap
spec:
      backgroundColor: '#003148'
      color: '#fff'
      link:
            href: "https://$openldap_app_route"
            text: OpenLDAP
      location: BannerTop
      text: "✅ IBM Concert OpenLDAP. User: cn=admin,dc=ibm,dc=com - Password: From Configuration   🚀 Access it here:"
EOF


oc delete ConsoleLink ibm-concert-openldap>/dev/null 2>/dev/null
cat <<EOF | oc apply -f -
apiVersion: console.openshift.io/v1
kind: ConsoleLink
metadata:
      name: ibm-concert-openldap
spec:
      applicationMenu:
            imageURL: 'http://raw.githubusercontent.com/niklaushirt/ibm-concert-deployer/main/doc/pics/icons/launch.svg'
            section: Admin Tools
      href: https://$openldap_app_route
      location: ApplicationMenu
      text: IBM Concert OpenLDAP
EOF

echo ""
echo ""
echo ""
echo ""
echo ""
echo ""



echo "------------------------------------------------------------------------------------------------------------------------------"
echo " ✅ KEYCLOAK CREDENTIALS"
echo "------------------------------------------------------------------------------------------------------------------------------"

export CONCERT_HUB_NAMESPACE=$(oc get po -A|grep ibm-solis-core |awk '{print$1}')
export CONCERT_NAMESPACE=$(oc get po -A|grep roja-portal |awk '{print$1}')

oc delete ConsoleNotification ibm-concert-operate-notification-kc>/dev/null 2>/dev/null
export KC_USER=$(kubectl exec -it $(kubectl get pods -n $CONCERT_HUB_NAMESPACE  | grep "ibm-solis-embedded-keycloak" | awk '{print $1}') -n $CONCERT_HUB_NAMESPACE  -- env | grep 'KC_BOOTSTRAP_ADMIN_USERNAME='| cut -d= -f2)
export KC_PWD=$(kubectl exec -it $(kubectl get pods -n $CONCERT_HUB_NAMESPACE  | grep "ibm-solis-embedded-keycloak" | awk '{print $1}') -n $CONCERT_HUB_NAMESPACE  -- env | grep 'KC_BOOTSTRAP_ADMIN_PASSWORD='| cut -d= -f2)
export KC_ROUTE=$(oc get route solis-hub -o jsonpath={.spec.host} -n $CONCERT_HUB_NAMESPACE)


echo "KC_USER:        $KC_USER"
echo "KC_PWD:         $KC_PWD"
echo "KC_ROUTE:       https://$KC_ROUTE/sys/internal/kc"

export appURL=$(oc get routes -n $CONCERT_NAMESPACE concert  -o jsonpath="{['spec']['host']}")|| true
cat <<EOF | oc apply -f -
apiVersion: console.openshift.io/v1
kind: ConsoleNotification
metadata:
      name: ibm-concert-operate-notification-kc
spec:
      backgroundColor: '#003148'
      color: '#fff'
      link:
            href: "https://$KC_ROUTE/sys/internal/kc"
            text: IBM KeyCloak
      location: BannerTop
      text: "✅ IBM Concert KeyCloak. User: $KC_USER - Password: $KC_PWD  🚀 Access it here:"
EOF


oc delete ConsoleLink ibm-concert-kc>/dev/null 2>/dev/null
cat <<EOF | oc apply -f -
apiVersion: console.openshift.io/v1
kind: ConsoleLink
metadata:
      name: ibm-concert-kc
spec:
      applicationMenu:
            imageURL: 'https://raw.githubusercontent.com/niklaushirt/ibm-concert-deployer/main/doc/pics/icons/launch.svg'
            section: Admin Tools
      href: https://$KC_ROUTE/sys/internal/kc
      location: ApplicationMenu
      text: IBM Concert KeyCloak
EOF

echo ""
echo ""
echo ""
echo ""
echo ""
echo ""



oc delete ConsoleNotification ibm-concert-operate-notification-turbo>/dev/null 2>/dev/null
export appURL=$(oc get routes -n ibm-concert-optimise nginx -o jsonpath="{['spec']['host']}")|| true
cat <<EOF | oc apply -f -
apiVersion: console.openshift.io/v1
kind: ConsoleNotification
metadata:
      name: ibm-concert-operate-notification-turbo
spec:
      backgroundColor: '#003148'
      color: '#fff'
      location: BannerTop
      text: "✅ IBM Concert Optimise Lite is installed in this cluster."
EOF




oc delete ConsoleNotification ibm-concert-operate-notification-concert>/dev/null 2>/dev/null
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




oc delete ConsoleLink ibm-concert-platform>/dev/null 2>/dev/null
cat <<EOF | oc apply -f -
apiVersion: console.openshift.io/v1
kind: ConsoleLink
metadata:
      name: ibm-concert-platform
spec:
      applicationMenu:
            imageURL: https://raw.githubusercontent.com/niklaushirt/ibm-concert-deployer/main/doc/pics/icons/ibm-cloud-pak--multicloud-mgmt.svg
            section: IBM IT Automation
      href: https://$appURL
      location: ApplicationMenu
      text: IBM Concert platform
EOF




oc delete ConsoleNotification ibm-concert-operate-notification-demoui>/dev/null 2>/dev/null
export CONCERT_DEMO_UI_NAMESPACE=$(oc get po -A|grep ibm-demo-ui |grep -v ibm-demo-ui-create |awk '{print$1}')
export appURL=$(oc get routes -n $CONCERT_DEMO_UI_NAMESPACE ibm-demo-ui -o jsonpath="{['spec']['host']}")|| true
cat <<EOF | oc apply -f -
apiVersion: console.openshift.io/v1
kind: ConsoleNotification
metadata:
    name: ibm-concert-operate-notification-demoui
spec:
    backgroundColor: '#009a00'
    color: '#fff'
    link:
        href: "https://$appURL"
        text: IBM Concert Demo UI
    location: BannerTop
    text: "✅ IBM Concert Demo UI is installed in this cluster. 🚀 Access it here:"
EOF



oc delete ConsoleLink ibm-concert-operate-link-demoui>/dev/null 2>/dev/null
cat <<EOF | oc apply -f -
apiVersion: console.openshift.io/v1
kind: ConsoleLink
metadata:
      name: ibm-concert-operate-link-demoui
spec:
      applicationMenu:
            imageURL: 'https://raw.githubusercontent.com/niklaushirt/ibm-concert-deployer/main/doc/pics/icons/demo-icon-white.svg'
            section: IBM Demo
      href: https://$appURL
      location: ApplicationMenu
      text: IBM Concert platform Demo UI
EOF






echo "***************************************************************************************************************************************************"
echo "***************************************************************************************************************************************************"
echo ""
echo "  🟢🟢🟢 Done"
echo ""
echo "***************************************************************************************************************************************************"
echo "***************************************************************************************************************************************************"
echo "***************************************************************************************************************************************************"
echo "***************************************************************************************************************************************************"
echo "***************************************************************************************************************************************************"
echo "***************************************************************************************************************************************************"
echo "***************************************************************************************************************************************************"
echo "***************************************************************************************************************************************************"



oc delete ConsoleNotification ibm-concert-operate-notification-main>/dev/null 2>/dev/null



