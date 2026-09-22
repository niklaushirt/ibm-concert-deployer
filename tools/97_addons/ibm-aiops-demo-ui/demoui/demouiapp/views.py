from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.template import loader
import os
import sys 
import time 
import hashlib
from threading import Thread
sys.path.append(os.path.abspath("demouiapp"))
from functions import *
from utils.commands import capture_shell, run_shell
INCIDENT_ACTIVE=False
ROBOT_SHOP_OUTAGE_ACTIVE=False
SOCK_SHOP_OUTAGE_ACTIVE=False
CONTACT_INFO=str(os.environ.get('CONTACT_INFO'))

mod_time=os.path.getmtime('./demouiapp/views.py')
mod_time_readable = datetime.datetime.fromtimestamp(mod_time)
print(' 🛠️ Build Date: '+str(mod_time_readable) + ' UTC')
print ('')
print ('')


print ('-------------------------------------------------------------------------------------------------')
print (' 🚀 Warming up')
print ('-------------------------------------------------------------------------------------------------')
print ('')



loggedin='false'
loginip='0.0.0.0'



hasCustomScenario= str(len(CUSTOM_EVENTS)+len(CUSTOM_METRICS)+len(CUSTOM_LOGS)+len(CUSTOM_TOPOLOGY)-1)
hasCustomTopology= str(len(CUSTOM_TOPOLOGY_TAG)+len(CUSTOM_TOPOLOGY_APP_NAME)+len(CUSTOM_TOPOLOGY))






if int(hasCustomTopology) > 0:
    print ('     ✅ Custom Scenario detected  ('+str(hasCustomTopology)+')')
    if (len(checkTopology()) > 0) and (CUSTOM_TOPOLOGY_FORCE_RELOAD == 'False'):
        print ('        ✅ Topology already exists - skipping creation')
        print ('')
        print ('')
        print ('')
    else:
        print ('        ✅ No Topology found - creating')
        loadTopology()
else:
    print ('        ✅ No Custom Topology found - skipping')


# ----------------------------------------------------------------------------------------------------------------------------------------------------
# GET NAMESPACES
# ----------------------------------------------------------------------------------------------------------------------------------------------------
print('     ❓ Getting IBMAIOps Namespace')
stream = capture_shell("oc get po -A|grep aiops-orchestrator-controller |awk '{print$1}'")
aimanagerns = stream.read().strip()
print('        ✅ IBMAIOps Namespace:       '+aimanagerns)



print ('')
print ('     🌏 PUBLIC ROUTES')

stream = capture_shell("oc get route  -n "+aimanagerns+" datalayer-api  -o jsonpath='{.status.ingress[0].host}'")
print('          DATALAYER PUBLIC ROUTE: '+str(stream.read().strip()))
stream = capture_shell("oc get routes iaf-system-kafka-0 -n "+aimanagerns+" -o=jsonpath={.status.ingress[0].host}")
print('          KAFKA PUBLIC ROUTE: '+str(stream.read().strip())+':443')
stream = capture_shell("oc get route -n "+aimanagerns+"| grep ibm-nginx-svc | awk '{print $2}'")
print('          METRIC PUBLIC ROUTE: '+str(stream.read().strip()))
print ('')


print('     ❓ Getting Details Datalayer')
stream = capture_shell("oc get route  -n "+aimanagerns+" datalayer-api  -o jsonpath='{.status.ingress[0].host}'")
DATALAYER_ROUTE = stream.read().strip()
DATALAYER_ROUTE=os.environ.get('DATALAYER_ROUTE_OVERRIDE', default=DATALAYER_ROUTE)
#DATALAYER_ROUTE=os.environ.get('DATALAYER_ROUTE_OVERRIDE', default='aiops-ir-core-ncodl-api.ibm-aiops:10011')
#print('          - DATALAYER_ROUTE: '+str(DATALAYER_ROUTE))

stream = capture_shell("oc get secret -n "+aimanagerns+" aiops-ir-core-ncodl-api-secret -o jsonpath='{.data.username}' | base64 --decode")
DATALAYER_USER = stream.read().strip()
stream = capture_shell("oc get secret -n "+aimanagerns+" aiops-ir-core-ncodl-api-secret -o jsonpath='{.data.password}' | base64 --decode")
DATALAYER_PWD = stream.read().strip()
#print('          - DATALAYER_USER: '+str(DATALAYER_USER))
#print('          - DATALAYER_PWD:  '+str(DATALAYER_PWD))


url = 'https://'+DATALAYER_ROUTE+'/irdatalayer.aiops.io/active/v1/stories'
#print('          - url: '+str(url))

auth=HTTPBasicAuth(DATALAYER_USER, DATALAYER_PWD)
headers = {'Content-Type': 'application/json', 'Accept-Charset': 'UTF-8', 'x-username' : 'admin', 'x-subscription-id' : 'cfd95b7e-3bc7-4006-a4a8-a73a79c71255'}
#print('          - headers: '+str(headers))

print('          Trying connection')

try:
    response = requests.get(url, headers=headers, auth=auth, verify=False)
    #print('          - response:  '+str(response))

except requests.exceptions.RequestException as e:  # This is the correct syntax
    stream = capture_shell("oc get route  -n "+aimanagerns+" datalayer-api  -o jsonpath='{.status.ingress[0].host}'")
    print('     ❗ YOU MIGHT WANT TO USE THE DATALAYER PUBLIC ROUTE: '+str(stream.read().strip()))
    raise SystemExit(e)


responseJSON=response.json()
responseStr=str(json.dumps(responseJSON))

#print('          - responseStr:  '+str(responseStr))


#print('          Print Status')



print('     ❓ Getting Flink Secrets')
stream = capture_shell("oc get secret -n "+aimanagerns+" aiops-ir-lifecycle-flink-admin-user -o jsonpath='{.data.username}' | base64 --decode")
FLINK_IR_USER = stream.read().strip()
stream = capture_shell("oc get secret -n "+aimanagerns+" aiops-ir-lifecycle-flink-admin-user -o jsonpath='{.data.password}' | base64 --decode")
FLINK_IR_PWD = stream.read().strip()
#print('          - FLINK_IR_USER: '+str(FLINK_IR_USER))
#print('          - FLINK_IR_PWD:  '+str(FLINK_IR_PWD))
stream = capture_shell("oc get secret -n "+aimanagerns+" aiops-lad-flink-admin-user -o jsonpath='{.data.username}' | base64 --decode")
FLINK_LAD_USER = stream.read().strip()
stream = capture_shell("oc get secret -n "+aimanagerns+" aiops-lad-flink-admin-user -o jsonpath='{.data.password}' | base64 --decode")
FLINK_LAD_PWD = stream.read().strip()
#print('          - FLINK_LAD_USER: '+str(FLINK_LAD_USER))
#print('          - FLINK_LAD_PWD:  '+str(FLINK_LAD_PWD))


#if 'pirsoscom.github.io/SNOW_INC' in responseStr and '"closed"' not in responseStr and '"resolved"' not in responseStr:
if '"state": "assignedToIndividual"' in responseStr or '"state": "inProgress"' in responseStr or '"state": "unassigned"' in responseStr:
    print('     🔴 INCIDENT FOUND')
    INCIDENT_ACTIVE=True
else:
    print('     🟢 NO INCIDENT')
    INCIDENT_ACTIVE=False

stream = capture_shell("oc get deployment  -n robot-shop ratings  -o yaml")
RATINGS_YAML = stream.read().strip()
if 'ratings-dev' in RATINGS_YAML:
    print('     🔴 ROBOT SHOP OUTAGE ACTIVE')
    ROBOT_SHOP_OUTAGE_ACTIVE=True
else:
    print('     🟢 ROBOT SHOP OUTAGE INACTIVE')
    ROBOT_SHOP_OUTAGE_ACTIVE=False

stream = capture_shell("oc get service  -n sock-shop catalogue  -o yaml")
CATALOG_YAML = stream.read().strip()
if '-outage' in CATALOG_YAML:
    print('     🔴 SOCK SHOP OUTAGE ACTIVE')
    SOCK_SHOP_OUTAGE_ACTIVE=True
else:
    print('     🟢 SOCK SHOP OUTAGE INACTIVE')
    SOCK_SHOP_OUTAGE_ACTIVE=False



print('     🟣 OUTAGE - Incident:'+str(INCIDENT_ACTIVE)+' - RS-OUTAGE:'+str(ROBOT_SHOP_OUTAGE_ACTIVE))

#assignedToIndividual
#inProgress




cmd = '''
echo "  <BR>"
echo "  <h1>🚀 IBM AIOps - Logins and URLs </h1><BR>"
echo "  <BR>"
echo "  <BR>"
echo "  <BR>"
export TEMP_PATH=~/aiops-install

# ---------------------------------------------------------------------------------------------------------------------------------------------------<BR>"
# ---------------------------------------------------------------------------------------------------------------------------------------------------<BR>"
# Do Not Edit Below
# ---------------------------------------------------------------------------------------------------------------------------------------------------<BR>"
# ---------------------------------------------------------------------------------------------------------------------------------------------------<BR>"



export AIOPS_NAMESPACE=$(oc get po -A|grep aiops-orchestrator-controller |awk '{print$1}')
export EVTMGR_NAMESPACE=$(oc get po -A|grep noi-operator |awk '{print$1}')

: "${AIOPS_NAMESPACE:=ibm-aiops}<BR>"
: "${EVTMGR_NAMESPACE:=noi}<BR>"

CLUSTER_ROUTE=$(oc get routes console -n openshift-console | tail -n 1 2>&1 ) 
CLUSTER_FQDN=$( echo $CLUSTER_ROUTE | awk '{print $2}')
CLUSTER_NAME=${CLUSTER_FQDN##*console.}

echo "<HR><BR>"
echo "<h2>🚀 1. IBM AIOps</h2><BR>"
echo "<BR>"

    echo "    -----------------------------------------------------------------------------------------------------------------------------------------------<BR>"
    echo "<h3>    🐣 1.1 Demo UI</h3><BR>"
    appURL=$(oc get routes -n $AIOPS_NAMESPACE-demo-ui ibm-aiops-demo-ui  -o jsonpath="{['spec']['host']}")|| true
    appToken=$(oc get cm -n $AIOPS_NAMESPACE-demo-ui ibm-aiops-demo-ui-config -o jsonpath='{.data.TOKEN}')
    echo "<table>"
    echo "<tr><td style=\"min-width:300px\">🌏 URL:</td><td><a target="_blank" href=\"https://$appURL/\">https://$appURL/</a></td></tr>"
    echo "<tr><td style=\"min-width:300px\">🔐 Token:</td><td>$appToken<BR>"
    echo "</table>"

    echo "<BR>"
    echo "<BR>"

echo "    -----------------------------------------------------------------------------------------------------------------------------------------------<BR>"
echo " <h3>   🚀 1.2 IBMAIOps</h3><BR>"

appURL=$(oc get route -n $AIOPS_NAMESPACE cpd -o jsonpath={.spec.host})

echo "<table>"
echo "<tr><td style=\"min-width:300px\"><h4>📥 IBMAIOps</h4></td><td></td></tr>"
echo "<tr><td style=\"min-width:300px\">🌏 URL:</td><td><a target="_blank" href=\"https://$appURL/\">https://$appURL/</a></td></tr>"
echo "<tr><td style=\"min-width:300px\">🧑 User:</td><td>demo</td></tr>"
echo "<tr><td style=\"min-width:300px\">🔐 Password:</td><td>Selected at installation</td></tr>"
echo "<tr><td style=\"min-width:300px\">&nbsp;</td><td></td></tr>"
echo "<tr><td style=\"min-width:300px\">🧑 User:</td><td>$(oc -n ibm-common-services get secret platform-auth-idp-credentials -o jsonpath='{.data.admin_username}' | base64 --decode && echo)</td></tr>"
echo "<tr><td style=\"min-width:300px\">🔐 Password:</td><td>$(oc -n ibm-common-services get secret platform-auth-idp-credentials -o jsonpath='{.data.admin_password}' | base64 --decode)</td></tr>"
echo "<tr><td style=\"min-width:300px\">&nbsp;</td><td></td></tr>"

appURL=$(oc get route -n ibm-common-services cp-console -o jsonpath={.spec.host})

echo "<tr><td colspan="2" style=\"min-width:300px\"><h4>📥 Administration hub / Common Services</h4></td></tr>"
echo "<tr><td style=\"min-width:300px\">🌏 URL:</td><td><a target="_blank" href=\"https://$appURL/\">https://$appURL/</a></td></tr>"
echo "<tr><td style=\"min-width:300px\">🧑 User:</td><td>demo</td></tr>"
echo "<tr><td style=\"min-width:300px\">🔐 Password:</td><td>Selected at installation</td></tr>"
echo "<tr><td style=\"min-width:300px\">&nbsp;</td><td></td></tr>"
echo "<tr><td style=\"min-width:300px\">🧑 User:</td><td>$(oc -n ibm-common-services get secret platform-auth-idp-credentials -o jsonpath='{.data.admin_username}' | base64 --decode && echo)</td></tr>"
echo "<tr><td style=\"min-width:300px\">🔐 Password:</td><td>$(oc -n ibm-common-services get secret platform-auth-idp-credentials -o jsonpath='{.data.admin_password}' | base64 --decode)</td></tr>"
echo "</table>"
echo "    <BR>"
echo "    <BR>"



    echo "    -----------------------------------------------------------------------------------------------------------------------------------------------<BR>"
    echo "    <h3>🚀 1.3 Demo Apps - Details</h3><BR>"
    appURL=$(oc get routes -n robot-shop robotshop  -o jsonpath="{['spec']['host']}")|| true

    echo "<table>"
    echo "<tr><td style=\"min-width:300px\"><h4>📥 RobotShop:</h4></td><td></td></tr>"
    echo "<tr><td style=\"min-width:300px\">🌏 URL:</td><td><a target="_blank" href=\"https://$appURL/\">https://$appURL/</a></td></tr>"
    echo "</table>"

    echo "<BR>"
    echo "<BR>"

  
echo "    <BR>"
echo "    <BR>"

echo "<HR><BR>"
echo "<h2>🚀 2. IBMAIOps Configuration Information</h2><BR>"
echo "    <BR>"
echo "    -----------------------------------------------------------------------------------------------------------------------------------------------<BR>"
echo "    <h3>🚀 2.1 Configure LDAP - Access Control </h3><BR>"

appURL=$(oc get route -n openldap admin -o jsonpath={.spec.host})

echo "<table>"

echo "<tr><td style=\"min-width:300px\"><h4>📥 Identity providers</h4></td><td></td></tr>"
echo "<tr><td style=\"min-width:300px\">🌏 Connection name:</td><td>LDAP</td></tr>"
echo "<tr><td style=\"min-width:300px\">🛠️  Server type:</td><td>Custom</td></tr>"
echo "<tr><td style=\"min-width:300px\">&nbsp;</td><td></td></tr>"
echo "<tr><td style=\"min-width:300px\">🧒 Base DN:</td><td>dc=ibm,dc=com</td></tr>"
echo "<tr><td style=\"min-width:300px\">🧒 Bind DN:</td><td>cn=admin,dc=ibm,dc=com</td></tr>"
echo "<tr><td style=\"min-width:300px\">🔐 Bind DN password:</td><td>Selected at installation </td></tr>"
echo "<tr><td style=\"min-width:300px\">&nbsp;</td><td></td></tr>"
echo "<tr><td style=\"min-width:300px\">🌏 LDAP server URL:</td><td>ldap://openldap.openldap:389</td></tr>"
echo "<tr><td style=\"min-width:300px\">&nbsp;</td><td></td></tr>"
echo "<tr><td style=\"min-width:300px\">🛠️  Group filter:</td><td>(&(cn=%v)(objectclass=groupOfUniqueNames))</td></tr>"
echo "<tr><td style=\"min-width:300px\">🛠️  User filter:</td><td>(&(uid=%v)(objectclass=Person))</td></tr>"
echo "<tr><td style=\"min-width:300px\">🛠️  Group ID map:</td><td>*:cn</td></tr>"
echo "<tr><td style=\"min-width:300px\">🛠️  User ID map:</td><td>*:uid</td></tr>"
echo "<tr><td style=\"min-width:300px\">🛠️  Group member ID map:</td><td>groupOfUniqueNames:uniqueMember</td></tr>"
echo "<tr><td style=\"min-width:300px\">&nbsp;</td><td></td></tr>"
echo "<tr><td style=\"min-width:300px\"><h4>📥 OpenLDAP Admin Login</h4></td><td></td></tr>"
echo "<tr><td style=\"min-width:300px\">&nbsp;</td><td></td></tr>"
echo "<tr><td style=\"min-width:300px\">🌏 URL:</td><td><a target="_blank" href=\"https://$appURL/\">https://$appURL/</a></td></tr>"
echo "<tr><td style=\"min-width:300px\">🧑 User:</td><td>cn=admin,dc=ibm,dc=com</td></tr>"
echo "<tr><td style=\"min-width:300px\">🔐 Password:</td><td>Selected at installation</td></tr>"

echo "</table>"
echo "    <BR>"
echo "    <BR>"




    echo "    -----------------------------------------------------------------------------------------------------------------------------------------------<BR>"
    echo "    <h3>🚀 2.2 Configure ELK </h3><BR>"
    token=$(oc -n openshift-logging get secret $(oc get secret -n openshift-logging|grep cluster-logging-operator-token-|awk '{print$1}') -o jsonpath='{.data.token}' | base64 --decode && echo)
    routeES=`oc get route elasticsearch -o jsonpath={.spec.host} -n openshift-logging`
    routeKIBANA=`oc get route kibana -o jsonpath={.spec.host} -n openshift-logging`

    echo "<table>"
    echo "<tr><td style=\"min-width:300px\"><h4>📥 ELK</h4></td><td></td></tr>"
    echo "<tr><td style=\"min-width:300px\">🌏 ELK service URL:</td><td>https://$routeES/app*</td></tr>"
    echo "<tr><td style=\"min-width:300px\">🌏 Kibana URL:</td><td><a target="_blank" href=\"https://$routeKIBANA/\">https://$routeKIBANA/</a></td></tr>"
    echo "<tr><td style=\"min-width:300px\">🔐 Authentication type:</td><td>Token</td></tr>"
    echo "<tr><td style=\"min-width:300px\">🔐 Token:</td><td>$token</td></tr>"
    echo "<tr><td style=\"min-width:300px\">🕦 TimeZone:</td><td>set to your Timezone</td></tr>"
    echo "<tr><td style=\"min-width:300px\">🚪 Kibana port:</td><td>443</td></tr>"
    echo "<tr><td style=\"min-width:300px\">&nbsp;</td><td></td></tr>"
    echo "<tr><td style=\"min-width:300px\">🗺️  Mapping:</td><td>"
    echo "&nbsp;{ <BR>"
    echo '&nbsp;&nbsp;&nbsp;  \"codec\": \"elk\",<BR>'
    echo '&nbsp;&nbsp;&nbsp;  \"message_field\": \"message\",<BR>'
    echo '&nbsp;&nbsp;&nbsp;  \"log_entity_types\": \"kubernetes.container_image_id, kubernetes.host, kubernetes.pod_name, kubernetes.namespace_name\",<BR>'
    echo '&nbsp;&nbsp;&nbsp;  \"instance_id_field\": \"kubernetes.container_name\",<BR>'
    echo '&nbsp;&nbsp;&nbsp;  \"rolling_time\": 10,<BR>'
    echo '&nbsp;&nbsp;&nbsp;  \"timestamp_field\": \"@timestamp\"<BR>'
    echo '&nbsp;}</td></tr>'
    echo "<tr><td style=\"min-width:300px\">&nbsp;</td><td></td></tr>"
    echo "<tr><td style=\"min-width:300px\">🗺️  Filter: </td><td>"
    echo "&nbsp;      {<BR>"
    echo "&nbsp;&nbsp;&nbsp;          \"query\": {<BR>"
    echo "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;          \"bool\": {<BR>"
    echo "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;   \"must\": {<BR>"
    echo "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;      \"term\" : { \"kubernetes.namespace_name\" : \"robot-shop\" }<BR>"
    echo "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;   }<BR>"
    echo "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;  }<BR>"
    echo "&nbsp;&nbsp;&nbsp;        }<BR>"
    echo "&nbsp;      }</td></tr>"
    echo "</table>"
    echo "<BR>"
    echo "<BR>"     
echo "    -----------------------------------------------------------------------------------------------------------------------------------------------<BR>"
echo "    <h3>🚀 2.3 Configure Runbooks - Ansible Automation Controller </h3><BR>"
appURL=$(oc get route -n awx awx -o jsonpath={.spec.host})

echo "<table>"
echo "<tr><td style=\"min-width:300px\">🌏 URL for REST API:</td><td><a target="_blank" href=\"https://$appURL/\">https://$appURL/</a></td></tr>"
echo "<tr><td style=\"min-width:300px\">🔐 Authentication type:</td><td>User ID/Password</td></tr>"
echo "<tr><td style=\"min-width:300px\">🧑 User:</td><td>admin</td></tr>"
echo "<tr><td style=\"min-width:300px\">🔐 Password:</td><td>$(oc -n awx get secret awx-admin-password -o jsonpath='{.data.password}' | base64 --decode && echo)</td></tr>"
echo "</table>"
echo "<BR>"
echo "<BR>"


echo "    -----------------------------------------------------------------------------------------------------------------------------------------------<BR>"
echo "    <h3>🚀 2.4 Configure Runbooks - Runbook Parameters </h3><BR>"
DEMO_TOKEN=$(oc create token -n default demo-admin --duration=999999999s)
DEMO_URL=$(oc status|grep -m1 "In project"|awk '{print$6}')

echo "<table>"
echo "<tr><td style=\"min-width:300px\">🌏 Action:</td><td>IBMAIOPS Mitigate Robotshop Ratings Outage<BR>"
echo "<tr><td style=\"min-width:300px\">🔐 Mapping:</td><td>Fixed Value<BR>"
echo "<tr><td style=\"min-width:300px\">🗺️ Value:</td><td>"
echo "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{<BR>"
echo "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; \"my_k8s_apiurl\": \"$DEMO_URL\",<BR>"
echo "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;   \"my_k8s_apikey\": \"$DEMO_TOKEN\"<BR>"
echo "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;}<BR></tr>"
echo "</table>"
echo "<BR>"
echo "<BR>"




echo "    -----------------------------------------------------------------------------------------------------------------------------------------------<BR>"
echo "    <h3>🚀 2.5 Configure Applications - RobotShop Kubernetes Observer </h3><BR>"
API_TOKEN=$(oc create token -n default demo-admin --duration=999999999s)
API_URL=$(oc status|grep -m1 "In project"|awk '{print$6}')
API_SERVER=$(echo $API_URL| cut -d ":" -f 2| tr -d '/')
API_PORT=$(echo $API_URL| cut -d ":" -f 3)

echo "<table>"
echo "<tr><td style=\"min-width:300px\">🛠️  Name:</td><td>RobotShop</td></tr>"
echo "<tr><td>🛠️  Data center:</td><td>robot-shop</td></tr>"
echo "<tr><td>🛠️  Kubernetes master IP address:</td><td>$API_SERVER</td></tr>"
echo "<tr><td>🛠️  Kubernetes API port:</td><td>$API_PORT</td></tr>"
echo "<tr><td>🛠️  Token:</td><td>$API_TOKEN</td></tr>"
echo "<tr><td>🛠️  Trust all HTTPS certificates:</td><td>true</td></tr>"
echo "<tr><td>🛠️  Correlate analytics events:</td><td>true</td></tr>"
echo "<tr><td>🛠️  Namespaces to observe:</td><td>robot-shop</td></tr>"
echo "</table>"
echo "<BR>"
echo "<BR>"


'''

if GET_CONFIG=='true':
    print('     ❓ Getting ALL LOGINS - this may take a minute or two')
    stream = capture_shell(cmd)
    ALL_LOGINS = stream.read().strip()
else:
    print('     ❓ Skip getting ALL LOGINS')
    ALL_LOGINS="❗ Has been disabled in the DemoUI configuration"
    #print ('           ALL_LOGINS:              '+ALL_LOGINS)







# ----------------------------------------------------------------------------------------------------------------------------------------------------
# GET CONNECTIONS
# ----------------------------------------------------------------------------------------------------------------------------------------------------
print('     ❓ Getting Details Kafka')
# stream = capture_shell("oc get kafkatopics -n "+aimanagerns+"  | grep -v cp4waiopscp4waiops| grep cp4waiops-cartridge-logs-elk| awk '{print $1;}'")
# KAFKA_TOPIC_LOGS = stream.read().strip()
KAFKA_TOPIC_LOGS=os.environ.get('KAFKA_TOPIC_LOGS', 'cp4waiops-cartridge-logs-elk-iuacrepx')

# stream = capture_shell("oc get kafkatopics -n "+aimanagerns+"  | grep -v cp4waiopscp4waiops| grep cp4waiops-cartridge-logs-none| awk '{print $1;}'")
# KAFKA_TOPIC_LOGS_NONE = stream.read().strip()
KAFKA_TOPIC_LOGS_NONE=os.environ.get('KAFKA_TOPIC_LOGS_NONE', 'cp4waiops-cartridge-logs-none-fanxygx9')

stream = capture_shell("oc get secret -n "+aimanagerns+" |grep '\-kafka-secret'|awk '{print$1}'")
KAFKA_SECRET = stream.read().strip()
stream = capture_shell("oc get secret "+KAFKA_SECRET+" -n "+aimanagerns+" --template={{.data.username}} | base64 --decode")
KAFKA_USER = stream.read().strip()
stream = capture_shell("oc get secret "+KAFKA_SECRET+" -n "+aimanagerns+" --template={{.data.password}} | base64 --decode")
KAFKA_PWD = stream.read().strip()
stream = capture_shell("oc get routes iaf-system-kafka-0 -n "+aimanagerns+" -o=jsonpath={.status.ingress[0].host}")
KAFKA_BROKER = stream.read().strip()+':443'
KAFKA_BROKER=os.environ.get('KAFKA_BROKER_OVERRIDE', default=KAFKA_BROKER)
#KAFKA_BROKER=os.environ.get('KAFKA_BROKER_OVERRIDE', default='iaf-system-kafka-0.ibm-aiops:9094')

stream = capture_shell("oc get secret -n "+aimanagerns+" kafka-secrets  -o jsonpath='{.data.ca\.crt}'| base64 --decode")
KAFKA_CERT = stream.read().strip()
# stream = capture_shell("oc get secret -n "+aimanagerns+" iaf-system-kafka-brokers  -o jsonpath='{.data..iaf-system-kafka-0\.crt}'| base64 --decode")
# KAFKA_CERT = stream.read().strip()






print('     ❓ Getting Details Metric Endpoint')
stream = capture_shell("oc get route -n "+aimanagerns+"| grep ibm-nginx-svc | awk '{print $2}'")
METRIC_ROUTE = stream.read().strip()
METRIC_ROUTE=os.environ.get('METRIC_ROUTE_OVERRIDE', default=METRIC_ROUTE)

stream = capture_shell("oc get route -n "+aimanagerns+" cp-console  -o jsonpath={.spec.host}")
CONSOLE_ROUTE = stream.read().strip()

stream = capture_shell("oc get secret -n "+aimanagerns+" platform-auth-idp-credentials -o jsonpath='{.data.admin_username}' | base64 --decode")
tmpusr = stream.read().strip()
print('     🟠 USR :'+str(tmpusr))

stream = capture_shell("oc get secret -n "+aimanagerns+" platform-auth-idp-credentials -o jsonpath='{.data.admin_password}' | base64 --decode")
tmppass = stream.read().strip()
print('     🟠 PWD :'+str(tmppass))

stream = capture_shell('curl -s -k -H "Content-Type: application/x-www-form-urlencoded;charset=UTF-8" -d "grant_type=password&username='+tmpusr+'&password='+tmppass+'&scope=openid" https://'+CONSOLE_ROUTE+'/idprovider/v1/auth/identitytoken|jq -r \'.access_token\'')
ACCESS_TOKEN = stream.read().strip()
print('     🟠 ACCESS_TOKEN :'+ACCESS_TOKEN[:25]+'...')



stream = capture_shell('curl -s -k -XGET https://'+METRIC_ROUTE+'/v1/preauth/validateAuth -H "username: '+tmpusr+'" -H "iam-token: '+ACCESS_TOKEN+'"|jq -r ".accessToken"')
METRIC_TOKEN = stream.read().strip()
print('     🟠 METRIC_TOKEN :'+METRIC_TOKEN[:25]+'...')




# ----------------------------------------------------------------------------------------------------------------------------------------------------
# GET CONNECTION DETAILS
# ----------------------------------------------------------------------------------------------------------------------------------------------------
print('     ❓ Getting Details IBMAIOps')
stream = capture_shell('oc get route -n '+aimanagerns+' cpd -o jsonpath={.spec.host}')
aimanager_url = stream.read().strip()
aimanager_url=os.environ.get('AIOPS_URL_OVERRIDE', default=aimanager_url)

stream = capture_shell('oc -n '+aimanagerns+' get secret platform-auth-idp-credentials -o jsonpath={.data.admin_username} | base64 --decode && echo')
aimanager_user = stream.read().strip()
stream = capture_shell('oc -n '+aimanagerns+' get secret platform-auth-idp-credentials -o jsonpath={.data.admin_password} | base64 --decode')
aimanager_pwd = stream.read().strip()



print('     ❓ Getting AWX Connection Details')
stream = capture_shell('oc get route -n awx awx -o jsonpath={.spec.host}')
awx_url = stream.read().strip()
awx_url=os.environ.get('AWX_URL_OVERRIDE', default=awx_url)

awx_user = 'admin'
stream = capture_shell('oc -n awx get secret awx-admin-password -o jsonpath={.data.password} | base64 --decode && echo')
awx_pwd = stream.read().strip()
 
print('     ❓ Getting Details ELK ')
stream = capture_shell('oc get route -n openshift-logging kibana -o jsonpath={.spec.host}')
elk_url = stream.read().strip()

print('     ❓ Getting Details Turbonomic Dashboard')
stream = capture_shell('oc get route -n turbonomic nginx -o jsonpath={.spec.host}')
turbonomic_url = stream.read().strip()

print('     ❓ Getting Details Instana Dashboard')
stream = capture_shell('oc get route -n instana-core dev-aiops -o jsonpath={.spec.host}')
instana_url = stream.read().strip()


print('     ❓ Getting Details Openshift Console')
stream = capture_shell('oc get route -n openshift-console console -o jsonpath={.spec.host}')
openshift_server = stream.read().strip()
openshift_url = 'https://'+openshift_server.replace("console-openshift-console.apps", "api")+':6443'
stream = capture_shell("oc -n openshift-authentication get secret $(oc get secret -n openshift-authentication |grep -m1 oauth-openshift-token|awk '{print$1}') -o jsonpath='{.data.token}'|base64 --decode")
openshift_token = stream.read().strip()

# stream = capture_shell("oc config view --minify|grep 'server:'| sed 's/.*server: .*\///'| head -1")
# #stream = capture_shell("oc status|head -1|awk '{print$6}'")
# openshift_server = stream.read().strip()
stream = capture_shell("oc get deployment -n ibm-aiops-demo-ui ibm-aiops-demo-ui -ojson|jq -r '.spec.template.spec.containers[0].image'")
demo_image = stream.read().strip()



print('     ❓ Getting Details Vault')
stream = capture_shell('oc get route -n '+aimanagerns+' ibm-vault-deploy-vault-route -o jsonpath={.spec.host}')
vault_url = stream.read().strip()
stream = capture_shell('oc get secret -n '+aimanagerns+' ibm-vault-deploy-vault-credential -o jsonpath={.data.token} | base64 --decode')
vault_token = stream.read().strip()

print('     ❓ Getting Details LDAP ')
stream = capture_shell('oc get route -n openldap admin -o jsonpath={.spec.host}')
ladp_url = stream.read().strip()
ladp_user = 'cn=admin,dc=ibm,dc=com'
ladp_pwd = 'Selected at installation'

print('     ❓ Getting Details Flink Task Manager')
stream = capture_shell('oc get routes -n '+aimanagerns+' job-manager  -o jsonpath={.spec.host}')
flink_url = stream.read().strip()
stream = capture_shell('oc get routes -n '+aimanagerns+' job-manager-policy  -o jsonpath={.spec.host}')
flink_url_policy = stream.read().strip()

print('     ❓ Getting Details Spark Master')
stream = capture_shell('oc get routes -n '+aimanagerns+' spark  -o jsonpath={.spec.host}')
spark_url = stream.read().strip()

print('     ❓ Getting Details RobotShop')
stream = capture_shell('oc get routes -n robot-shop robotshop  -o jsonpath={.spec.host}')
robotshop_url = stream.read().strip()
robotshop_url=os.environ.get('ROBOTSHOP_URL_OVERRIDE', default=robotshop_url)
#print ('🟣🟣🟣🟣🟣🟣🟣🟣'+str(os.environ.get('ROBOTSHOP_URL_OVERRIDE')))


print('     ❓ Getting Details SockShop')
stream = capture_shell('oc get routes -n sock-shop front-end  -o jsonpath={.spec.host}')
sockshop_url = stream.read().strip()
sockshop_url=os.environ.get('SOCKSHOP_URL_OVERRIDE', default=sockshop_url)

# ----------------------------------------------------------------------------------------------------------------------------------------------------
# GET ENVIRONMENT VALUES
# ----------------------------------------------------------------------------------------------------------------------------------------------------
TOKEN=os.environ.get('TOKEN')
ADMIN_MODE=os.environ.get('ADMIN_MODE')
SIMULATION_MODE=os.environ.get('SIMULATION_MODE')
DEMO_USER=os.environ.get('DEMO_USER')
DEMO_PWD=os.environ.get('DEMO_PWD')

print ('')
print (' ✅ Warming up - DONE')
print ('-------------------------------------------------------------------------------------------------')
print ('')
print ('')
print ('')
print ('')


print ('🟣')
print ('🟣-------------------------------------------------------------------------------------------------')
print ('🟣  🟢 Global Configuration')
print ('🟣-------------------------------------------------------------------------------------------------')
print ('🟣')
print ('🟣    ---------------------------------------------------------------------------------------------')
print ('🟣     🔎 Simulation Parameters')
print ('🟣    ---------------------------------------------------------------------------------------------')
print ('🟣           📥 Instance Name:                  '+str(INSTANCE_NAME))
print ('🟣           🔐 Login Token:                    '+TOKEN)
print ('🟣')   
print ('🟣           🟠 Admin Mode:                     '+ADMIN_MODE)
print ('🟣           ⚠️  Can create incident:            '+SIMULATION_MODE)
print ('🟣')   
print ('🟣           🔏 Login for all sytems:                      ')
print ('🟣             👩‍💻 Demo User:                    '+DEMO_USER)
print ('🟣             🔐 Demo Password:                '+DEMO_PWD)
print ('🟣')
print ('🟣           🖼️  Image for UI:                   '+str(INSTANCE_IMAGE))
print ('🟣')
print ('🟣           🔎 Read Configuration:             '+str(GET_CONFIG))
print ('🟣')  
print ('🟣')  
print ('🟣    ---------------------------------------------------------------------------------------------')
print ('🟣     🔎 Simulation Parameters')
print ('🟣    ---------------------------------------------------------------------------------------------')
print ('🟣           🔄 LOG_ITERATIONS:                 '+str(LOG_ITERATIONS))
print ('🟣           🕦 LOG_TIME_FORMAT:                '+LOG_TIME_FORMAT)
print ('🟣           🔄 LOG_TIME_STEPS:                 '+str(LOG_TIME_STEPS))
print ('🟣           🔄 LOG_TIME_SKEW Logs:             '+str(LOG_TIME_SKEW))
print ('🟣           🔐 LOG_TIME_ZONE Cert:             '+str(LOG_TIME_ZONE))
print ('🟣')
print ('🟣           🕦 EVENTS_TIME_SKEW:               '+str(EVENTS_TIME_SKEW))
print ('🟣           📝 DEMO_EVENTS_ROBO_MEM:           '+str(len(DEMO_EVENTS_MEM)))
print ('🟣           📝 DEMO_EVENTS_ROBO_NET:           '+str(len(DEMO_EVENTS_ROBO_NET)))
print ('🟣           📝 DEMO_EVENTS_SOCK:               '+str(len(DEMO_EVENTS_NET_SOCK)))
print ('🟣           📝 DEMO_EVENTS_ACME:               '+str(len(DEMO_EVENTS_FAN_ACME)))
print ('🟣           📝 DEMO_EVENTS_TUBE:               '+str(len(DEMO_EVENTS_TUBE)))
print ('🟣           📝 DEMO_EVENTS_TELCO:              '+str(len(DEMO_EVENTS_TELCO)))
print ('🟣           📝 DEMO_EVENTS_BUSY:               '+str(len(DEMO_EVENTS_BUSY)))
print ('🟣')
print ('🟣           🕦 METRIC_TIME_SKEW:               '+str(METRIC_TIME_SKEW))
print ('🟣           🔄 METRIC_TIME_STEP:               '+str(METRIC_TIME_STEP))
print ('🟣           🔄 METRIC_ITERATIONS:              '+str(METRIC_ITERATIONS))
print ('🟣           📈 METRICS_TO_SIMULATE_MEM:        '+str(len(METRICS_TO_SIMULATE_MEM)))
print ('🟣           📈 METRICS_TO_SIMULATE_FAN_TEMP:   '+str(len(METRICS_TO_SIMULATE_FAN_TEMP)))
print ('🟣           📈 METRICS_TO_SIMULATE_FAN:        '+str(len(METRICS_TO_SIMULATE_FAN)))
print ('🟣')
print ('🟣           📈 ROBOTSHOP_PROPERTY_RESOURCE_NAME:  '+str(ROBOTSHOP_PROPERTY_RESOURCE_NAME))
print ('🟣           📈 ROBOTSHOP_PROPERTY_RESOURCE_TYPE:  '+str(ROBOTSHOP_PROPERTY_RESOURCE_TYPE))
print ('🟣           📈 ROBOTSHOP_PROPERTY_VALUES_NOK:     '+str(ROBOTSHOP_PROPERTY_VALUES_NOK))
print ('🟣           📈 ROBOTSHOP_PROPERTY_VALUES_OK:      '+str(ROBOTSHOP_PROPERTY_VALUES_OK))

print ('🟣')
print ('🟣           📥 URLs for static Slack and SNOW Integration (set to NONE if not needed): ')
print ('🟣')
print ('🟣               🌏 SLACK_URL_ROSH:                 '+str(SLACK_URL_ROSH))
print ('🟣               🌏 SLACK_URL_SOSH:                 '+str(SLACK_URL_SOSH))
print ('🟣               🌏 SLACK_URL_ACME:                 '+str(SLACK_URL_ACME))
print ('🟣')    
print ('🟣               🌏 SNOW_URL_ROSH:                  '+str(SNOW_URL_ROSH))
print ('🟣               🌏 SNOW_URL_SOSH:                  '+str(SNOW_URL_SOSH))
print ('🟣               🌏 SNOW_URL_ACME:                  '+str(SNOW_URL_ACME))
print ('🟣')
print ('🟣               🌏 INCIDENT_URL_TUBE:              '+str(INCIDENT_URL_TUBE))
print ('🟣')
print ('🟣')
print ('🟣    ---------------------------------------------------------------------------------------------')
print ('🟣     🔎 CUSTOM Simulation Parameters')
print ('🟣    ---------------------------------------------------------------------------------------------')
print ('🟣           📈 CUSTOM_NAME:                    '+str(CUSTOM_NAME))
print ('🟣           📈 CUSTOM_EVENTS:                  '+str(len(CUSTOM_EVENTS)))
print ('🟣           📈 CUSTOM_METRICS:                 '+str(len(CUSTOM_METRICS)-1))
print ('🟣           📈 CUSTOM_LOGS:                    '+str(len(CUSTOM_LOGS)))
print ('🟣           📈 CUSTOM_TOPOLOGY_APP_NAME:       '+str(CUSTOM_TOPOLOGY_APP_NAME))
print ('🟣           📈 CUSTOM_TOPOLOGY_TAG:            '+str(CUSTOM_TOPOLOGY_TAG))
print ('🟣           📈 CUSTOM_TOPOLOGY:                '+str(len(CUSTOM_TOPOLOGY)))
print ('🟣           📈 CUSTOM_PROPERTY_RESOURCE_NAME:  '+str(CUSTOM_PROPERTY_RESOURCE_NAME))
print ('🟣           📈 CUSTOM_PROPERTY_RESOURCE_TYPE:  '+str(CUSTOM_PROPERTY_RESOURCE_TYPE))
print ('🟣           📈 CUSTOM_PROPERTY_VALUES_NOK:     '+str(CUSTOM_PROPERTY_VALUES_NOK))
print ('🟣           📈 CUSTOM_PROPERTY_VALUES_OK:      '+str(CUSTOM_PROPERTY_VALUES_OK))
print ('🟣')
print ('🟣')
print ('🟣    ---------------------------------------------------------------------------------------------')
print ('🟣     🔎 System Parameters')
print ('🟣    ---------------------------------------------------------------------------------------------')
print ('🟣           🌏 KafkaBroker:                    '+KAFKA_BROKER)
print ('🟣           👩‍💻 KafkaUser:                      '+KAFKA_USER)
print ('🟣           🔐 KafkaPWD:                       '+KAFKA_PWD)
print ('🟣           📥 KafkaTopic Logs:                '+KAFKA_TOPIC_LOGS)
print ('🟣           📥 KafkaTopic Logs None:           '+KAFKA_TOPIC_LOGS_NONE)
print ('🟣           🔐 Kafka Cert:                     '+KAFKA_CERT[:25]+'...')
print ('🟣')   
print ('🟣           🌏 Datalayer Route:                '+DATALAYER_ROUTE)
print ('🟣           👩‍💻 Datalayer User:                 '+DATALAYER_USER)
print ('🟣           🔐 Datalayer Pwd:                  '+DATALAYER_PWD)
print ('🟣')   
print ('🟣           🌏 Metric Route:                   '+METRIC_ROUTE)
print ('🟣           🔐 Metric Token:                   '+METRIC_TOKEN[:25]+'...')

print ('🟣')   
print ('🟣           🌏 OCP Route:                      '+openshift_url)
print ('🟣           🌏 OCP Server:                     '+openshift_server)
print ('🟣           🔐 OCP Token:                      '+openshift_token[:25]+'...')
print ('🟣')   
print ('🟣')
print ('🟣    ---------------------------------------------------------------------------------------------')
print ('🟣     🌏 URLs')
print ('🟣    ---------------------------------------------------------------------------------------------')
print ('🟣           🌏 RobotShop URL:                  '+robotshop_url)
print ('🟣           🌏 SockShop URL:                   '+sockshop_url)
print ('🟣           🌏 AWX URL:                        '+awx_url)
print ('🟣           🌏 AIOPS URL:                      '+aimanager_url)
print ('🟣')   
print ('🟣')
print ('🟣    --------------------------------------------------------------------------------------------------')
print ('🟣')

print ('')




print ('')
print ('')
print ('')
print ('')


print ('*************************************************************************************************')
print (' ✅ DEMOUI is READY')
print ('*************************************************************************************************')


# ----------------------------------------------------------------------------------------------------------------------------------------------------
# REST ENDPOINTS
# ----------------------------------------------------------------------------------------------------------------------------------------------------

def get_base_context(page_title='Welcome to your Demo UI', page_name='index'):
    return {
        'loggedin': loggedin,
        'aimanager_url': aimanager_url,
        'aimanager_user': aimanager_user,
        'aimanager_pwd': aimanager_pwd,
        'DEMO_USER': DEMO_USER,
        'DEMO_PWD': DEMO_PWD,
        'awx_url': awx_url,
        'awx_user': awx_user,
        'awx_pwd': awx_pwd,
        'elk_url': elk_url,
        'turbonomic_url': turbonomic_url,
        'instana_url': instana_url,
        'openshift_url': openshift_url,
        'openshift_token': openshift_token,
        'openshift_server': openshift_server,
        'vault_url': vault_url,
        'vault_token': vault_token,
        'ladp_url': ladp_url,
        'ladp_user': ladp_user,
        'ladp_pwd': ladp_pwd,
        'flink_url': flink_url,
        'flink_url_policy': flink_url_policy,
        'robotshop_url': robotshop_url,
        'sockshop_url': sockshop_url,
        'spark_url': spark_url,
        'INSTANCE_NAME': INSTANCE_NAME,
        'INSTANCE_IMAGE': INSTANCE_IMAGE,
        'ADMIN_MODE': ADMIN_MODE,
        'hasCustomScenario': int(hasCustomScenario),
        'CUSTOM_NAME': CUSTOM_NAME,
        'INCIDENT_ACTIVE': INCIDENT_ACTIVE,
        'ROBOT_SHOP_OUTAGE_ACTIVE': ROBOT_SHOP_OUTAGE_ACTIVE,
        'SOCK_SHOP_OUTAGE_ACTIVE': SOCK_SHOP_OUTAGE_ACTIVE,
        'SIMULATION_MODE': SIMULATION_MODE,
        'PAGE_TITLE': page_title,
        'PAGE_NAME': page_name,
    }


# ----------------------------------------------------------------------------------------------------------------------------------------------------
#    ADD SLACK AND SNOW Links to Incidents
# ----------------------------------------------------------------------------------------------------------------------------------------------------

def addExternalLinksToIncident(request):
    print('🌏 addExternalLinksToIncident')


    if ('https:' in SLACK_URL_ROSH or 'https:' in SNOW_URL_ROSH  or 'https:' in SLACK_URL_SOSH   or 'https:' in SNOW_URL_SOSH   or 'https:' in SLACK_URL_ACME   or 'https:' in SNOW_URL_ACME):
        print ('    ---------------------------------------------------------------------------------------------')
        print ('    🔗 addExternalLinksToIncident - Wait 20 Seconds for Incident to be created then retry every 20 seconds for 2 minutes')
        print ('    ---------------------------------------------------------------------------------------------')

        foundStory=False
        for retry in range(6):

            time.sleep(20)

            url = 'https://'+DATALAYER_ROUTE+'/irdatalayer.aiops.io/active/v1/stories'
            auth=HTTPBasicAuth(DATALAYER_USER, DATALAYER_PWD)
            headers = {'Content-Type': 'application/json', 'Accept-Charset': 'UTF-8', 'x-username' : 'admin', 'x-subscription-id' : 'cfd95b7e-3bc7-4006-a4a8-a73a79c71255'}
            try:    
                response = requests.get(url, headers=headers, auth=auth, verify=False)
            except requests.exceptions.RequestException as e:  # This is the correct syntax
                stream = capture_shell("oc get route  -n "+aimanagerns+" datalayer-api  -o jsonpath='{.status.ingress[0].host}'")
                print('     ❗ YOU MIGHT WANT TO USE THE DATALAYER PUBLIC ROUTE: '+str(stream.read().strip()))
                raise SystemExit(e)

            responseJSON=response.json()
            responseStr=str(json.dumps(responseJSON))
            #print ('aaaa'+responseStr)
            print ('    ---------------------------------------------------------------------------------------------')
            print ('    🔗 addExternalLinksToIncident - Checking Incidents')
            print ('    ---------------------------------------------------------------------------------------------'  )
            for i in responseJSON.get('stories'):
                if 'resolved' not in i['state'] and 'closed' not in i['state'] :
                    print("    🔗 addExternalLinksToIncident - Found Incident: "+i['title']+" : "+i['state'])

                    foundStory=True

                    if 'Sudden increase ' in i['title'] or 'Optimise Buffer Pool ' in i['title'] or 'Commit in repository' in i['title'] or 'Resize up vMEM' in i['title'] or 'MySQL' in i['title'] or 'Robot' in i['title'] or 'Erroneous call rate' in i['title'] or 'ArgoCD' in i['title'] or 'Database' in i['title'] or 'Erroneous' in i['title'] or 'Jenkins' in i['title']:
                        current_id=str(i['id'])
                        # print(i['title'])
                        # print(current_id)
                        if 'https:' in SLACK_URL_ROSH:
                            print ('    ---------------------------------------------------------------------------------------------')
                            print ('     🛠️ Adding Slack RobotShop')
                            print ('    ---------------------------------------------------------------------------------------------')
                            patch_data={ "insights": [{"id": "b7248e70-ec13-4d1f-a005-0cf517d82391", "type": "aiops.ibm.com/insight-type/chatops/metadata", "source": "chatops", "details": { "id": "c27b7a0c-246a-47e8-85f0-041566f57d00", "name": "Slack","app_state": "{'channel':'C05RPF0QZ47','alertVisibility':{},'addedIncidents':[],'storyId':'5eee46e6-8086-4b8c-85a8-10e250e82bf8','ts':'1696922654.186279','isExpanded':false}","permalink": ""+SLACK_URL_ROSH+"","channel_name": "cp4aiops-demo"}}]}
                            url = 'https://'+DATALAYER_ROUTE+'/irdatalayer.aiops.io/active/v1/stories/'+current_id
                            auth=HTTPBasicAuth(DATALAYER_USER, DATALAYER_PWD)
                            headers = {'Content-Type': 'application/json', 'Accept-Charset': 'UTF-8', 'x-username' : 'admin', 'x-subscription-id' : 'cfd95b7e-3bc7-4006-a4a8-a73a79c71255'}
                            response = requests.patch(url, headers=headers, auth=auth, verify=False, data =json.dumps(patch_data))
                            print(str(response.content))
                        else:
                            print ('        ❌ addExternalLinksToIncident - Skipping SLACK_URL_ROSH')
                        if 'https:' in SNOW_URL_ROSH:
                            print ('    ---------------------------------------------------------------------------------------------')
                            print ('     🛠️ Adding SNOW RobotShop')
                            print ('    ---------------------------------------------------------------------------------------------')
                            patch_data={ "insights": [{"id": "c5242c61-9dee-4bcb-82de-9f64e9ac667e","type": "aiops.ibm.com/insight-type/itsm/metadata","source": "chatops","details": {"id": "9c587715-4eee-4dd1-a129-041566f57d00","name": "Service now","type": "aiops.ibm.com/insight-type/itsm/metadata","app_state": "{'sysId': '9eec516193f5b510a2e7bba97bba1002', 'success': 'True', 'incidentNumber': 'INC0010003'}","permalink": ""+SNOW_URL_ROSH+"","ticket_num": "INC0010003"}}]}
                            url = 'https://'+DATALAYER_ROUTE+'/irdatalayer.aiops.io/active/v1/stories/'+current_id
                            auth=HTTPBasicAuth(DATALAYER_USER, DATALAYER_PWD)
                            headers = {'Content-Type': 'application/json', 'Accept-Charset': 'UTF-8', 'x-username' : 'admin', 'x-subscription-id' : 'cfd95b7e-3bc7-4006-a4a8-a73a79c71255'}
                            response = requests.patch(url, headers=headers, auth=auth, verify=False, data =json.dumps(patch_data))
                            print(str(response.content))
                        else:
                            print ('        ❌ addExternalLinksToIncident - Skipping SNOW_URL_ROSH')




                    if 'Switch Outage' in i['title']:
                        current_id=str(i['id'])
                        # print(i['title'])
                        # print(current_id)
                        if 'https:' in SLACK_URL_SOSH:
                            print ('    ---------------------------------------------------------------------------------------------')
                            print ('     🛠️ Adding Slack SockShop')
                            print ('    ---------------------------------------------------------------------------------------------')
                            patch_data={ "insights": [{"id": "b7248e70-ec13-4d1f-a005-0cf517d82390", "type": "aiops.ibm.com/insight-type/chatops/metadata", "source": "chatops", "details": { "id": "c27b7a0c-246a-47e8-85f0-041566f57d01", "name": "Slack","app_state": "{'channel':'C05RPF0QZ47','alertVisibility':{},'addedIncidents':[],'storyId':'5eee46e6-8086-4b8c-85a8-10e250e82bf8','ts':'1696922654.186279','isExpanded':false}","permalink": ""+SLACK_URL_SOSH+"","channel_name": "cp4aiops-demo"}}]}
                            url = 'https://'+DATALAYER_ROUTE+'/irdatalayer.aiops.io/active/v1/stories/'+current_id
                            auth=HTTPBasicAuth(DATALAYER_USER, DATALAYER_PWD)
                            headers = {'Content-Type': 'application/json', 'Accept-Charset': 'UTF-8', 'x-username' : 'admin', 'x-subscription-id' : 'cfd95b7e-3bc7-4006-a4a8-a73a79c71255'}
                            response = requests.patch(url, headers=headers, auth=auth, verify=False, data =json.dumps(patch_data))
                            print(str(response.content))
                        else:
                            print ('        ❌ addExternalLinksToIncident - Skipping SLACK_URL_SOSH')
                        if 'https:' in SNOW_URL_SOSH:
                            print ('    ---------------------------------------------------------------------------------------------')
                            print ('     🛠️ Adding SNOW SockShop')
                            print ('    ---------------------------------------------------------------------------------------------')
                            patch_data={ "insights": [{"id": "c5242c61-9dee-4bcb-82de-9f64e9ac667f","type": "aiops.ibm.com/insight-type/itsm/metadata","source": "chatops","details": {"id": "9c587715-4eee-4dd1-a129-041566f57d01","name": "Service now","type": "aiops.ibm.com/insight-type/itsm/metadata","app_state": "{'sysId': '9eec516193f5b510a2e7bba97bba1002', 'success': 'True', 'incidentNumber': 'INC0010002'}","permalink": ""+SNOW_URL_SOSH+"","ticket_num": "INC0010002"}}]}
                            url = 'https://'+DATALAYER_ROUTE+'/irdatalayer.aiops.io/active/v1/stories/'+current_id
                            auth=HTTPBasicAuth(DATALAYER_USER, DATALAYER_PWD)
                            headers = {'Content-Type': 'application/json', 'Accept-Charset': 'UTF-8', 'x-username' : 'admin', 'x-subscription-id' : 'cfd95b7e-3bc7-4006-a4a8-a73a79c71255'}
                            response = requests.patch(url, headers=headers, auth=auth, verify=False, data =json.dumps(patch_data))
                            print(str(response.content))
                        else:
                            print ('        ❌ addExternalLinksToIncident - Skipping SNOW_URL_SOSH')

                    if 'Fan malfunction' in i['title']:
                        current_id=str(i['id'])
                        # print(i['title'])
                        # print(current_id)
                        if 'https:' in SLACK_URL_ACME:
                            print ('    ---------------------------------------------------------------------------------------------')
                            print ('     🛠️ Adding Slack ACME')
                            print ('    ---------------------------------------------------------------------------------------------')
                            patch_data={ "insights": [{"id": "b7248e70-ec13-4d1f-a005-0cf517d82392", "type": "aiops.ibm.com/insight-type/chatops/metadata", "source": "chatops", "details": { "id": "c27b7a0c-246a-47e8-85f0-041566f57d02", "name": "Slack","app_state": "{'channel':'C05RPF0QZ47','alertVisibility':{},'addedIncidents':[],'storyId':'5eee46e6-8086-4b8c-85a8-10e250e82bf8','ts':'1696922654.186279','isExpanded':false}","permalink": ""+SLACK_URL_ACME+"","channel_name": "cp4aiops-demo"}}]}
                            url = 'https://'+DATALAYER_ROUTE+'/irdatalayer.aiops.io/active/v1/stories/'+current_id
                            auth=HTTPBasicAuth(DATALAYER_USER, DATALAYER_PWD)
                            headers = {'Content-Type': 'application/json', 'Accept-Charset': 'UTF-8', 'x-username' : 'admin', 'x-subscription-id' : 'cfd95b7e-3bc7-4006-a4a8-a73a79c71255'}
                            response = requests.patch(url, headers=headers, auth=auth, verify=False, data =json.dumps(patch_data))
                            print(str(response.content))
                        else:
                            print ('        ❌ addExternalLinksToIncident - Skipping SLACK_URL_ACME')
                        if 'https:' in SNOW_URL_ACME:
                            print ('    ---------------------------------------------------------------------------------------------')
                            print ('     🛠️ Adding SNOW ACME')
                            print ('    ---------------------------------------------------------------------------------------------')
                            patch_data={ "insights": [{"id": "c5242c61-9dee-4bcb-82de-9f64e9ac667d","type": "aiops.ibm.com/insight-type/itsm/metadata","source": "chatops","details": {"id": "9c587715-4eee-4dd1-a129-041566f57d02","name": "Service now","type": "aiops.ibm.com/insight-type/itsm/metadata","app_state": "{'sysId': '9eec516193f5b510a2e7bba97bba1002', 'success': 'True', 'incidentNumber': 'INC0010001'}","permalink": ""+SNOW_URL_ACME+"","ticket_num": "INC0010001"}}]}
                            url = 'https://'+DATALAYER_ROUTE+'/irdatalayer.aiops.io/active/v1/stories/'+current_id
                            auth=HTTPBasicAuth(DATALAYER_USER, DATALAYER_PWD)
                            headers = {'Content-Type': 'application/json', 'Accept-Charset': 'UTF-8', 'x-username' : 'admin', 'x-subscription-id' : 'cfd95b7e-3bc7-4006-a4a8-a73a79c71255'}
                            response = requests.patch(url, headers=headers, auth=auth, verify=False, data =json.dumps(patch_data))
                            print(str(response.content))
                        else:
                            print ('        ❌ addExternalLinksToIncident - Skipping SNOW_URL_ACME')


                    if 'fire' in i['title'] or 'delays' in i['title']:
                        current_id=str(i['id'])
                        # print(i['title'])
                        # print(current_id)
                        if 'https:' in INCIDENT_URL_TUBE:
                            print ('    ---------------------------------------------------------------------------------------------')
                            print ('     🛠️ Adding Incident Tube')
                            print ('    ---------------------------------------------------------------------------------------------')
                            patch_data={ "insights": [{"id": "c5242c61-9dee-4bcb-82de-9f64e9ac667d","type": "aiops.ibm.com/insight-type/itsm/metadata","source": "chatops","details": {"id": "9c587715-4eee-4dd1-a129-041566f57d02","name": "Dashboard","type": "aiops.ibm.com/insight-type/itsm/metadata","app_state": "{'sysId': '9eec516193f5b510a2e7bba97bba1002', 'success': 'True', 'incidentNumber': 'MILE_END'}","permalink": ""+INCIDENT_URL_TUBE+"","ticket_num": "MILE_END"}}]} 
                            url = 'https://'+DATALAYER_ROUTE+'/irdatalayer.aiops.io/active/v1/stories/'+current_id
                            auth=HTTPBasicAuth(DATALAYER_USER, DATALAYER_PWD)
                            headers = {'Content-Type': 'application/json', 'Accept-Charset': 'UTF-8', 'x-username' : 'admin', 'x-subscription-id' : 'cfd95b7e-3bc7-4006-a4a8-a73a79c71255'}
                            response = requests.patch(url, headers=headers, auth=auth, verify=False, data =json.dumps(patch_data))
                            print(str(response.content))
                        else:
                            print ('        ❌ addExternalLinksToIncident - Skipping INCIDENT_URL_TUBE')
                print('    🔗 addExternalLinksToIncident - Added some links')
                

            if foundStory:
                print ('    🔗 addExternalLinksToIncident - Links have been added to Incidents ')
                break
            print ('    🔗 addExternalLinksToIncident - Retrying: Wait 20 Seconds for Incident to be created then retry every 20 seconds for 2 minutes')

        print ('    ---------------------------------------------------------------------------------------------')
        print ('    ---------------------------------------------------------------------------------------------')
        print('✅ addExternalLinksToIncident - DONE')
        print ('    ---------------------------------------------------------------------------------------------')
    else:
        print ('    ---------------------------------------------------------------------------------------------')
        print ('    ❌ Skipping SNOW and Slack Links')
        print ('    ---------------------------------------------------------------------------------------------')
 


# ----------------------------------------------------------------------------------------------------------------------------------------------------
#    INSTANA
# ----------------------------------------------------------------------------------------------------------------------------------------------------

def instanaCreateIncident(request):
    print('🌏 instanaCreateIncident')
    global loggedin, INCIDENT_ACTIVE, ROBOT_SHOP_OUTAGE_ACTIVE, SOCK_SHOP_OUTAGE_ACTIVE
    print('     🟣 OUTAGE - Incident:'+str(INCIDENT_ACTIVE)+' - RS-OUTAGE:'+str(ROBOT_SHOP_OUTAGE_ACTIVE)+' - SOCK-OUTAGE:'+str(SOCK_SHOP_OUTAGE_ACTIVE))

    verifyLogin(request)
    if loggedin=='true':
        template = loader.get_template('demouiapp/home.html')

        print('🌏 Create Instana outage')
        run_shell('oc set env deployment ratings -n robot-shop PDO_URL="mysql:host=mysql;dbname=ratings-dev;charset=utf8mb4"')
        run_shell('oc set env deployment load -n robot-shop ERROR=1')

        url = 'https://'+DATALAYER_ROUTE+'/irdatalayer.aiops.io/active/v1/stories'
        auth=HTTPBasicAuth(DATALAYER_USER, DATALAYER_PWD)
        headers = {'Content-Type': 'application/json', 'Accept-Charset': 'UTF-8', 'x-username' : 'admin', 'x-subscription-id' : 'cfd95b7e-3bc7-4006-a4a8-a73a79c71255'}
        try:
            response = requests.get(url, headers=headers, auth=auth, verify=False)
        except requests.exceptions.RequestException as e:
            stream = capture_shell("oc get route  -n "+aimanagerns+" datalayer-api  -o jsonpath='{.status.ingress[0].host}'")
            print('     ❗ YOU MIGHT WANT TO USE THE DATALAYER PUBLIC ROUTE: '+str(stream.read().strip()))
            raise SystemExit(e)

        responseJSON=response.json()
        responseStr=str(json.dumps(responseJSON))
        if '"state": "assignedToIndividual"' in responseStr or '"state": "inProgress"' in responseStr or '"state": "unassigned"' in responseStr:
            print('     🔴 INCIDENT FOUND')
            INCIDENT_ACTIVE=True
        else:
            print('     🟢 NO INCIDENT')
            INCIDENT_ACTIVE=False
        ROBOT_SHOP_OUTAGE_ACTIVE=True

    else:
        template = loader.get_template('demouiapp/loginui.html')
    return HttpResponse(template.render(get_base_context(), request))


def instanaMitigateIncident(request):
    print('🌏 instanaMitigateIncident')
    global loggedin, INCIDENT_ACTIVE, ROBOT_SHOP_OUTAGE_ACTIVE, SOCK_SHOP_OUTAGE_ACTIVE

    print('     🟣 OUTAGE - Incident:'+str(INCIDENT_ACTIVE)+' - RS-OUTAGE:'+str(ROBOT_SHOP_OUTAGE_ACTIVE)+' - SOCK-OUTAGE:'+str(SOCK_SHOP_OUTAGE_ACTIVE))
    verifyLogin(request)
    if loggedin=='true':
        template = loader.get_template('demouiapp/home.html')

        print('🌏 Mitigate Instana outage')
        run_shell('oc patch service mysql -n robot-shop --patch "{\\"spec\\": {\\"selector\\": {\\"service\\": \\"mysql\\"}}}"')
        run_shell('oc set env deployment ratings -n robot-shop PDO_URL-')
        run_shell('oc set env deployment load -n robot-shop ERROR=0')
        run_shell("oc delete pod $(oc get po -n robot-shop|grep shipping|awk '{print$1}') -n robot-shop --ignore-not-found")
        print('🌏 Mitigate Sockshop Catalog outage')
        run_shell('oc patch service catalogue -n sock-shop --patch "{\\"spec\\": {\\"selector\\": {\\"name\\": \\"catalog\\"}}}"')

        url = 'https://'+DATALAYER_ROUTE+'/irdatalayer.aiops.io/active/v1/stories'
        auth=HTTPBasicAuth(DATALAYER_USER, DATALAYER_PWD)
        headers = {'Content-Type': 'application/json', 'Accept-Charset': 'UTF-8', 'x-username' : 'admin', 'x-subscription-id' : 'cfd95b7e-3bc7-4006-a4a8-a73a79c71255'}
        try:
            response = requests.get(url, headers=headers, auth=auth, verify=False)
        except requests.exceptions.RequestException as e:
            stream = capture_shell("oc get route  -n "+aimanagerns+" datalayer-api  -o jsonpath='{.status.ingress[0].host}'")
            print('     ❗ YOU MIGHT WANT TO USE THE DATALAYER PUBLIC ROUTE: '+str(stream.read().strip()))
            raise SystemExit(e)

        responseJSON=response.json()
        responseStr=str(json.dumps(responseJSON))
        if '"state": "assignedToIndividual"' in responseStr or '"state": "inProgress"' in responseStr:
            print('     🔴 INCIDENT FOUND')
            INCIDENT_ACTIVE=True
        else:
            print('     🟢 NO INCIDENT')
            INCIDENT_ACTIVE=False

        ROBOT_SHOP_OUTAGE_ACTIVE=False
        SOCK_SHOP_OUTAGE_ACTIVE=False

    else:
        template = loader.get_template('demouiapp/loginui.html')
    return HttpResponse(template.render(get_base_context(), request))



# ----------------------------------------------------------------------------------------------------------------------------------------------------
#    AIOPS
# ----------------------------------------------------------------------------------------------------------------------------------------------------

def injectAllREST(request):
    print('🌏 injectAllREST')
    global loggedin, INCIDENT_ACTIVE, ROBOT_SHOP_OUTAGE_ACTIVE, SOCK_SHOP_OUTAGE_ACTIVE
    print('     🟣 OUTAGE - Incident:'+str(INCIDENT_ACTIVE)+' - RS-OUTAGE:'+str(ROBOT_SHOP_OUTAGE_ACTIVE)+' - SOCK-OUTAGE:'+str(SOCK_SHOP_OUTAGE_ACTIVE))
    verifyLogin(request)

    if loggedin=='true':
        template = loader.get_template('demouiapp/home.html')

        print('  🟠 Create THREADS')
        threadEvents = Thread(target=injectEventsMemRobot, args=(DATALAYER_ROUTE,DATALAYER_USER,DATALAYER_PWD))
        threadMetrics = Thread(target=injectMetricsMem, args=(METRIC_ROUTE,METRIC_TOKEN,))
        threadLogs = Thread(target=injectLogsRobotShop, args=(KAFKA_BROKER,KAFKA_USER,KAFKA_PWD,KAFKA_TOPIC_LOGS,KAFKA_CERT,LOG_TIME_FORMAT,DEMO_LOGS,))
        threadLinks = Thread(target=addExternalLinksToIncident, args=(request,))

        print('  🟠 Start THREADS')
        threadEvents.start()
        threadMetrics.start()
        threadLogs.start()
        threadLinks.start()

        print('🌏 Create RobotShop MySQL outage')
        run_shell('oc set env deployment ratings -n robot-shop PDO_URL="mysql:host=mysql;dbname=ratings-dev;charset=utf8mb4"')
        run_shell('oc set env deployment load -n robot-shop ERROR=1')

        INCIDENT_ACTIVE=True
        ROBOT_SHOP_OUTAGE_ACTIVE=True

        print('  🟠 Create THREADS CUSTOM_PROPS')
        threadProps = Thread(target=modifyProperty, args=(ROBOTSHOP_PROPERTY_RESOURCE_NAME,ROBOTSHOP_PROPERTY_RESOURCE_TYPE,ROBOTSHOP_PROPERTY_VALUES_NOK,))
        print('  🟠 Start THREADS CUSTOM_PROPS')
        threadProps.start()

    else:
        template = loader.get_template('demouiapp/loginui.html')

    return HttpResponse(template.render(get_base_context(), request))





def injectAllRobotNetREST(request):
    print('🌏 injectAllRobotNetREST')
    global loggedin, INCIDENT_ACTIVE, ROBOT_SHOP_OUTAGE_ACTIVE, SOCK_SHOP_OUTAGE_ACTIVE
    print('     🟣 OUTAGE - Incident:'+str(INCIDENT_ACTIVE)+' - RS-OUTAGE:'+str(ROBOT_SHOP_OUTAGE_ACTIVE)+' - SOCK-OUTAGE:'+str(SOCK_SHOP_OUTAGE_ACTIVE))
    verifyLogin(request)

    if loggedin=='true':
        template = loader.get_template('demouiapp/home.html')

        print('  🟠 Create THREADS')
        threadEvents = Thread(target=injectEventsNetRobot, args=(DATALAYER_ROUTE,DATALAYER_USER,DATALAYER_PWD))
        threadMetrics = Thread(target=injectMetricsMem, args=(METRIC_ROUTE,METRIC_TOKEN,))
        threadMetricsFib = Thread(target=injectMetricsFiber, args=(METRIC_ROUTE,METRIC_TOKEN,))
        threadLogs = Thread(target=injectLogsRobotShop, args=(KAFKA_BROKER,KAFKA_USER,KAFKA_PWD,KAFKA_TOPIC_LOGS,KAFKA_CERT,LOG_TIME_FORMAT,DEMO_LOGS,))
        threadLinks = Thread(target=addExternalLinksToIncident, args=(request,))

        print('  🟠 Start THREADS')
        threadEvents.start()
        threadMetrics.start()
        threadMetricsFib.start()
        threadLogs.start()
        threadLinks.start()

        print('🌏 Create RobotShop MySQL outage')
        run_shell('oc set env deployment ratings -n robot-shop PDO_URL="mysql:host=mysql;dbname=ratings-dev;charset=utf8mb4"')
        run_shell('oc set env deployment load -n robot-shop ERROR=1')

        INCIDENT_ACTIVE=True
        ROBOT_SHOP_OUTAGE_ACTIVE=True

        print('  🟠 Start THREADS CUSTOM_PROPS')
        Thread(target=modifyProperty, args=('frapod01','fiberConnection','{"availability": "ERROR"}')).start()
        Thread(target=modifyProperty, args=('bepod01','fiberConnection','{"availability": "ERROR"}')).start()

    else:
        template = loader.get_template('demouiapp/loginui.html')

    return HttpResponse(template.render(get_base_context(), request))





def httpCommand(request):
    print('🌏 httpCommand')
    global loggedin
    global INCIDENT_ACTIVE
    global ROBOT_SHOP_OUTAGE_ACTIVE
    global SOCK_SHOP_OUTAGE_ACTIVE
    print('     🟣 OUTAGE - Incident:'+str(INCIDENT_ACTIVE)+' - RS-OUTAGE:'+str(ROBOT_SHOP_OUTAGE_ACTIVE)+' - SOCK-OUTAGE:'+str(SOCK_SHOP_OUTAGE_ACTIVE))

    currentcommand=request.GET.get("command", '{"command":"resetUplink", "status":"ok"}')
    print('  🟠 '+currentcommand)

    payload = currentcommand
    return HttpResponse(payload, content_type="application/json", status=201)






def injectRESTHeadless(request):
    print('🌏 injectRESTHEadless')
    global loggedin
    global INCIDENT_ACTIVE
    global ROBOT_SHOP_OUTAGE_ACTIVE
    global SOCK_SHOP_OUTAGE_ACTIVE
    print('     🟣 OUTAGE - Incident:'+str(INCIDENT_ACTIVE)+' - RS-OUTAGE:'+str(ROBOT_SHOP_OUTAGE_ACTIVE)+' - SOCK-OUTAGE:'+str(SOCK_SHOP_OUTAGE_ACTIVE))

    currentapp=request.GET.get("app", "robotshop")
    print('  🟠 '+currentapp)

    if currentapp=='robotshop':
        print('  🟠 Create THREADS')
        threadEvents = Thread(target=injectEventsMemRobot, args=(DATALAYER_ROUTE,DATALAYER_USER,DATALAYER_PWD))
        threadMetrics = Thread(target=injectMetricsMem, args=(METRIC_ROUTE,METRIC_TOKEN,))
        threadLogs = Thread(target=injectLogsRobotShop, args=(KAFKA_BROKER,KAFKA_USER,KAFKA_PWD,KAFKA_TOPIC_LOGS,KAFKA_CERT,LOG_TIME_FORMAT,DEMO_LOGS,))
        threadLinks = Thread(target=addExternalLinksToIncident, args=(request,))

        print('  🟠 Start THREADS')
        threadEvents.start()
        threadMetrics.start()
        threadLogs.start()
        threadLinks.start()
        # print('  🟠 Join THREADS')
        print('🌏 Create RobotShop MySQL outage')
        run_shell('oc set env deployment ratings -n robot-shop PDO_URL="mysql:host=mysql;dbname=ratings-dev;charset=utf8mb4"')
        run_shell('oc set env deployment load -n robot-shop ERROR=1')

        addExternalLinksToIncident(request)
        INCIDENT_ACTIVE=True
        ROBOT_SHOP_OUTAGE_ACTIVE=True
        
        print('  🟠 Create THREADS CUSTOM_PROPS')
        threadLogs = Thread(target=modifyProperty, args=(ROBOTSHOP_PROPERTY_RESOURCE_NAME,ROBOTSHOP_PROPERTY_RESOURCE_TYPE,ROBOTSHOP_PROPERTY_VALUES_NOK,))
        print('  🟠 Start THREADS CUSTOM_PROPS')
        threadLogs.start()

    if currentapp=='robotshopnet':
        print('  🟠 Create THREADS')
        
        threadEvents = Thread(target=injectEventsNetRobot, args=(DATALAYER_ROUTE,DATALAYER_USER,DATALAYER_PWD))
        threadMetrics = Thread(target=injectMetricsMem, args=(METRIC_ROUTE,METRIC_TOKEN,))
        threadLogs = Thread(target=injectLogsRobotShop, args=(KAFKA_BROKER,KAFKA_USER,KAFKA_PWD,KAFKA_TOPIC_LOGS,KAFKA_CERT,LOG_TIME_FORMAT,DEMO_LOGS,))
        threadLinks = Thread(target=addExternalLinksToIncident, args=(request,))

        print('  🟠 Start THREADS')
        # start the threads
        threadEvents.start()
        threadMetrics.start()
        threadLogs.start()
        threadLinks.start()

        print('🌏 Create RobotShop MySQL outage')
        run_shell('oc set env deployment ratings -n robot-shop PDO_URL="mysql:host=mysql;dbname=ratings-dev;charset=utf8mb4"')
        run_shell('oc set env deployment load -n robot-shop ERROR=1')

        #addExternalLinksToIncident(request)
        INCIDENT_ACTIVE=True
        ROBOT_SHOP_OUTAGE_ACTIVE=True

        print('  🟠 Create THREADS CUSTOM_PROPS')
        #threadLogs = Thread(target=modifyProperty, args=(ROBOTSHOP_PROPERTY_RESOURCE_NAME,ROBOTSHOP_PROPERTY_RESOURCE_TYPE,ROBOTSHOP_PROPERTY_VALUES_NOK,))
        threadLogs1 = Thread(target=modifyProperty, args=('frapod01','fiberConnection','{"availability": "ERROR"}',))
        print('  🟠 Start THREADS CUSTOM_PROPS')
        threadLogs1.start()
        print('  🟠 Create THREADS CUSTOM_PROPS')
        #threadLogs = Thread(target=modifyProperty, args=(ROBOTSHOP_PROPERTY_RESOURCE_NAME,ROBOTSHOP_PROPERTY_RESOURCE_TYPE,ROBOTSHOP_PROPERTY_VALUES_NOK,))
        threadLogs2 = Thread(target=modifyProperty, args=('bepod01','fiberConnection','{"availability": "ERROR"}',))
        print('  🟠 Start THREADS CUSTOM_PROPS')
        threadLogs2.start()


    elif currentapp=='sockshop':

        INCIDENT_ACTIVE=True
        SOCK_SHOP_OUTAGE_ACTIVE=True

        print('🌏 Create Sockshop Catalog outage')
        print('🌏 Create Optical Network outage')

        run_shell('oc patch service catalogue -n sock-shop --patch "{\\"spec\\": {\\"selector\\": {\\"name\\": \\"catalog-outage\\"}}}"')


        print('  🟠 Create THREADS')
        threadEvents = Thread(target=injectEventsNetSock, args=(DATALAYER_ROUTE,DATALAYER_USER,DATALAYER_PWD))
        threadMetrics = Thread(target=injectMetricsSockNet, args=(METRIC_ROUTE,METRIC_TOKEN,))
        threadLogs = Thread(target=injectLogsSockShop, args=(KAFKA_BROKER,KAFKA_USER,KAFKA_PWD,KAFKA_TOPIC_LOGS_NONE,KAFKA_CERT,LOG_TIME_FORMAT,DEMO_LOGS_SOCK,))
        #threadEvents1 = Thread(target=injectEventsTelco, args=(DATALAYER_ROUTE,DATALAYER_USER,DATALAYER_PWD))

        print('  🟠 Start THREADS')
        # start the threads
        threadMetrics.start()
        threadEvents.start()
        threadLogs.start()
        #threadEvents1.start()

        #time.sleep(3)

        threadLinks = Thread(target=addExternalLinksToIncident, args=(request,))
        threadLinks.start()



    elif currentapp=='acme':

        INCIDENT_ACTIVE=True

        print('  🟠 Create THREADS')
        threadMetrics1 = Thread(target=injectMetricsFanTempACME, args=(METRIC_ROUTE,METRIC_TOKEN,))
        threadEvents = Thread(target=injectEventsFanACME, args=(DATALAYER_ROUTE,DATALAYER_USER,DATALAYER_PWD))
        threadMetrics2 = Thread(target=injectMetricsFanACME, args=(METRIC_ROUTE,METRIC_TOKEN,))

        print('  🟠 Start THREADS')
        # start the threads
        threadMetrics1.start()
        threadEvents.start()
        threadMetrics2.start()
        #time.sleep(3)

        threadLinks = Thread(target=addExternalLinksToIncident, args=(request,))
        threadLinks.start()


    elif currentapp=='tube':

        INCIDENT_ACTIVE=True

        print('🌏 Create London Underground outage')

        print('  🟠 Create THREADS')
        threadEvents = Thread(target=injectEventsTube, args=(DATALAYER_ROUTE,DATALAYER_USER,DATALAYER_PWD))

        print('  🟠 Start THREADS')
        # start the threads
        threadEvents.start()
        #time.sleep(3)

        threadLinks = Thread(target=addExternalLinksToIncident, args=(request,))
        threadLinks.start()



    elif currentapp=='telco':

        INCIDENT_ACTIVE=True

        print('🌏 Create Optical Network outage')

        print('  🟠 Create THREADS')
        threadEvents = Thread(target=injectEventsTelco, args=(DATALAYER_ROUTE,DATALAYER_USER,DATALAYER_PWD))

        print('  🟠 Start THREADS')
        # start the threads
        threadEvents.start()
        #time.sleep(3)

    elif currentapp=='busy':

        INCIDENT_ACTIVE=True

        print('🌏 Simulate Busy Environment')

        print('  🟠 Create THREADS')
        threadEvents = Thread(target=injectEventsBusy, args=(DATALAYER_ROUTE,DATALAYER_USER,DATALAYER_PWD))

        print('  🟠 Start THREADS')
        # start the threads
        threadEvents.start()
        #time.sleep(3)



    elif currentapp=='all':
        print('  🟠 Create THREADS')
        threadEvents = Thread(target=injectEventsMemRobot, args=(DATALAYER_ROUTE,DATALAYER_USER,DATALAYER_PWD))
        threadMetrics = Thread(target=injectMetricsMem, args=(METRIC_ROUTE,METRIC_TOKEN,))
        threadLogs = Thread(target=injectLogsRobotShop, args=(KAFKA_BROKER,KAFKA_USER,KAFKA_PWD,KAFKA_TOPIC_LOGS,KAFKA_CERT,LOG_TIME_FORMAT,DEMO_LOGS,))
        threadLinks = Thread(target=addExternalLinksToIncident, args=(request,))

        print('  🟠 Start THREADS')
        threadEvents.start()
        threadMetrics.start()
        threadLogs.start()
        threadLinks.start()
        # print('  🟠 Join THREADS')
        print('🌏 Create RobotShop MySQL outage')
        run_shell('oc set env deployment ratings -n robot-shop PDO_URL="mysql:host=mysql;dbname=ratings-dev;charset=utf8mb4"')
        run_shell('oc set env deployment load -n robot-shop ERROR=1')

        addExternalLinksToIncident(request)
        INCIDENT_ACTIVE=True
        ROBOT_SHOP_OUTAGE_ACTIVE=True
        SOCK_SHOP_OUTAGE_ACTIVE=True

        print('🌏 Create Sockshop Catalog outage')
        run_shell('oc patch service catalogue -n sock-shop --patch "{\\"spec\\": {\\"selector\\": {\\"name\\": \\"catalog-outage\\"}}}"')


        print('  🟠 Create THREADS')
        threadEvents = Thread(target=injectEventsNetSock, args=(DATALAYER_ROUTE,DATALAYER_USER,DATALAYER_PWD))
        threadMetrics = Thread(target=injectMetricsSockNet, args=(METRIC_ROUTE,METRIC_TOKEN,))
        threadLogs = Thread(target=injectLogsSockShop, args=(KAFKA_BROKER,KAFKA_USER,KAFKA_PWD,KAFKA_TOPIC_LOGS_NONE,KAFKA_CERT,LOG_TIME_FORMAT,DEMO_LOGS_SOCK,))

        print('  🟠 Start THREADS')
        # start the threads
        threadMetrics.start()
        threadEvents.start()
        threadLogs.start()
        #time.sleep(3)

        threadLinks = Thread(target=addExternalLinksToIncident, args=(request,))
        threadLinks.start()


        print('  🟠 Create THREADS')
        threadMetrics1 = Thread(target=injectMetricsFanTempACME, args=(METRIC_ROUTE,METRIC_TOKEN,))
        threadEvents = Thread(target=injectEventsFanACME, args=(DATALAYER_ROUTE,DATALAYER_USER,DATALAYER_PWD))
        threadMetrics2 = Thread(target=injectMetricsFanACME, args=(METRIC_ROUTE,METRIC_TOKEN,))

        print('  🟠 Start THREADS')
        # start the threads
        threadMetrics1.start()
        threadEvents.start()
        threadMetrics2.start()
        #time.sleep(3)

        threadLinks = Thread(target=addExternalLinksToIncident, args=(request,))
        threadLinks.start()


        print('🌏 Create London Underground outage')

        print('  🟠 Create THREADS')
        threadEvents = Thread(target=injectEventsTube, args=(DATALAYER_ROUTE,DATALAYER_USER,DATALAYER_PWD))

        print('  🟠 Start THREADS')
        # start the threads
        threadEvents.start()
        #time.sleep(3)

        threadLinks = Thread(target=addExternalLinksToIncident, args=(request,))
        threadLinks.start()

        print('  🟠 Create THREADS CUSTOM_PROPS')
        threadLogs = Thread(target=modifyProperty, args=(ROBOTSHOP_PROPERTY_RESOURCE_NAME,ROBOTSHOP_PROPERTY_RESOURCE_TYPE,ROBOTSHOP_PROPERTY_VALUES_NOK,))
        print('  🟠 Start THREADS CUSTOM_PROPS')
        threadLogs.start()



    elif currentapp=='clean':

        print('  🟠 Create THREADS')
        threadMitigateIssues = Thread(target=mitigateIssues, args=(DATALAYER_ROUTE,DATALAYER_USER,DATALAYER_PWD))
        threadCloseAlerts = Thread(target=closeAlerts, args=(DATALAYER_ROUTE,DATALAYER_USER,DATALAYER_PWD))
        threadCloseStories = Thread(target=closeStories, args=(DATALAYER_ROUTE,DATALAYER_USER,DATALAYER_PWD))
        print('  🟠 Create THREADS CUSTOM_PROPS')
        threadLogs = Thread(target=modifyProperty, args=(ROBOTSHOP_PROPERTY_RESOURCE_NAME,ROBOTSHOP_PROPERTY_RESOURCE_TYPE,ROBOTSHOP_PROPERTY_VALUES_OK,))
        print('  🟠 Start THREADS CUSTOM_PROPS')
        threadLogs.start()
        print('  🟠 Create THREADS CUSTOM_PROPS')
        #threadLogs = Thread(target=modifyProperty, args=(ROBOTSHOP_PROPERTY_RESOURCE_NAME,ROBOTSHOP_PROPERTY_RESOURCE_TYPE,ROBOTSHOP_PROPERTY_VALUES_NOK,))
        threadLogs1 = Thread(target=modifyProperty, args=('frapod01','fiberConnection','{"availability": "OK"}',))
        print('  🟠 Start THREADS CUSTOM_PROPS')
        threadLogs1.start()
        print('  🟠 Create THREADS CUSTOM_PROPS')
        #threadLogs = Thread(target=modifyProperty, args=(ROBOTSHOP_PROPERTY_RESOURCE_NAME,ROBOTSHOP_PROPERTY_RESOURCE_TYPE,ROBOTSHOP_PROPERTY_VALUES_NOK,))
        threadLogs2 = Thread(target=modifyProperty, args=('bepod01','fiberConnection','{"availability": "OK"}',))
        print('  🟠 Start THREADS CUSTOM_PROPS')
        threadLogs2.start()

        if len(CUSTOM_PROPERTY_RESOURCE_NAME)>0:
            print('  🟠 Create THREADS CUSTOM_PROPS')
            threadLogs = Thread(target=modifyProperty, args=(CUSTOM_PROPERTY_RESOURCE_NAME,CUSTOM_PROPERTY_RESOURCE_TYPE,CUSTOM_PROPERTY_VALUES_OK,))
            print('  🟠 Start THREADS CUSTOM_PROPS')
            threadLogs.start()


        print('  🟠 Start THREADS')
        # start the threads
        threadMitigateIssues.start()
        threadCloseAlerts.start()
        threadCloseStories.start()
        time.sleep(1)

        INCIDENT_ACTIVE=False
        ROBOT_SHOP_OUTAGE_ACTIVE=False
        SOCK_SHOP_OUTAGE_ACTIVE=False


    return HttpResponse("Status OK :"+currentapp, content_type="application/json", status=201)




def injectAllFanACMEREST(request):
    print('🌏 injectAllFanACMEREST')
    global loggedin, INCIDENT_ACTIVE, ROBOT_SHOP_OUTAGE_ACTIVE, SOCK_SHOP_OUTAGE_ACTIVE
    print('     🟣 OUTAGE - Incident:'+str(INCIDENT_ACTIVE)+' - ACME-OUTAGE:'+str(ROBOT_SHOP_OUTAGE_ACTIVE))
    verifyLogin(request)
    if loggedin=='true':
        template = loader.get_template('demouiapp/home.html')

        INCIDENT_ACTIVE=True

        print('  🟠 Create THREADS')
        threadMetrics1 = Thread(target=injectMetricsFanTempACME, args=(METRIC_ROUTE,METRIC_TOKEN,))
        threadEvents = Thread(target=injectEventsFanACME, args=(DATALAYER_ROUTE,DATALAYER_USER,DATALAYER_PWD))
        threadMetrics2 = Thread(target=injectMetricsFanACME, args=(METRIC_ROUTE,METRIC_TOKEN,))

        print('  🟠 Start THREADS')
        threadMetrics1.start()
        threadEvents.start()
        threadMetrics2.start()

        Thread(target=addExternalLinksToIncident, args=(request,)).start()

    else:
        template = loader.get_template('demouiapp/loginui.html')

    return HttpResponse(template.render(get_base_context(), request))


def injectAllNetSOCKREST(request):
    print('🌏 injectAllNetSOCKREST')
    global loggedin, INCIDENT_ACTIVE, ROBOT_SHOP_OUTAGE_ACTIVE, SOCK_SHOP_OUTAGE_ACTIVE
    print('     🟣 OUTAGE - Incident:'+str(INCIDENT_ACTIVE)+' - SOCK-OUTAGE:'+str(ROBOT_SHOP_OUTAGE_ACTIVE))
    verifyLogin(request)
    if loggedin=='true':
        template = loader.get_template('demouiapp/home.html')

        INCIDENT_ACTIVE=True
        SOCK_SHOP_OUTAGE_ACTIVE=True

        print('🌏 Create Sockshop Catalog outage')
        run_shell('oc patch service catalogue -n sock-shop --patch "{\\"spec\\": {\\"selector\\": {\\"name\\": \\"catalog-outage\\"}}}"')

        print('  🟠 Create THREADS')
        threadEvents = Thread(target=injectEventsNetSock, args=(DATALAYER_ROUTE,DATALAYER_USER,DATALAYER_PWD))
        threadMetrics = Thread(target=injectMetricsSockNet, args=(METRIC_ROUTE,METRIC_TOKEN,))
        threadLogs = Thread(target=injectLogsSockShop, args=(KAFKA_BROKER,KAFKA_USER,KAFKA_PWD,KAFKA_TOPIC_LOGS_NONE,KAFKA_CERT,LOG_TIME_FORMAT,DEMO_LOGS_SOCK,))

        print('  🟠 Start THREADS')
        threadMetrics.start()
        threadEvents.start()
        threadLogs.start()

        Thread(target=addExternalLinksToIncident, args=(request,)).start()

    else:
        template = loader.get_template('demouiapp/loginui.html')

    return HttpResponse(template.render(get_base_context(), request))



def injectAllTELCOREST(request):
    print('🌏 injectAllTELCOREST')
    global loggedin, INCIDENT_ACTIVE, ROBOT_SHOP_OUTAGE_ACTIVE, SOCK_SHOP_OUTAGE_ACTIVE
    print('     🟣 OUTAGE - Incident:'+str(INCIDENT_ACTIVE)+' - SOCK-OUTAGE:'+str(ROBOT_SHOP_OUTAGE_ACTIVE))
    verifyLogin(request)
    if loggedin=='true':
        template = loader.get_template('demouiapp/home.html')

        INCIDENT_ACTIVE=True

        print('🌏 Create Optical Network outage')

        print('  🟠 Create THREADS')
        threadEvents = Thread(target=injectEventsTelco, args=(DATALAYER_ROUTE,DATALAYER_USER,DATALAYER_PWD))
        threadMetricsFibTransatlantic = Thread(target=injectMetricsFiberTransatlantic, args=(METRIC_ROUTE,METRIC_TOKEN,))

        print('  🟠 Start THREADS')
        threadEvents.start()
        threadMetricsFibTransatlantic.start()

    else:
        template = loader.get_template('demouiapp/loginui.html')

    return HttpResponse(template.render(get_base_context(), request))




def injectAllTUBEREST(request):
    print('🌏 injectAllTUBEREST')
    global loggedin, INCIDENT_ACTIVE, ROBOT_SHOP_OUTAGE_ACTIVE, SOCK_SHOP_OUTAGE_ACTIVE
    print('     🟣 OUTAGE - Incident:'+str(INCIDENT_ACTIVE)+' - SOCK-OUTAGE:'+str(ROBOT_SHOP_OUTAGE_ACTIVE))
    verifyLogin(request)
    if loggedin=='true':
        template = loader.get_template('demouiapp/home.html')

        INCIDENT_ACTIVE=True

        print('🌏 Create London Underground outage')

        print('  🟠 Create THREADS')
        threadEvents = Thread(target=injectEventsTube, args=(DATALAYER_ROUTE,DATALAYER_USER,DATALAYER_PWD))

        print('  🟠 Start THREADS')
        threadEvents.start()

        Thread(target=addExternalLinksToIncident, args=(request,)).start()

    else:
        template = loader.get_template('demouiapp/loginui.html')

    return HttpResponse(template.render(get_base_context(), request))




def injectLogsREST(request):
    print('🌏 injectLogsREST')
    global loggedin, INCIDENT_ACTIVE, ROBOT_SHOP_OUTAGE_ACTIVE, SOCK_SHOP_OUTAGE_ACTIVE
    print('     🟣 OUTAGE - Incident:'+str(INCIDENT_ACTIVE)+' - RS-OUTAGE:'+str(ROBOT_SHOP_OUTAGE_ACTIVE)+' - SOCK-OUTAGE:'+str(SOCK_SHOP_OUTAGE_ACTIVE))
    verifyLogin(request)
    if loggedin=='true':
        template = loader.get_template('demouiapp/home.html')
        injectLogsRobotShop(KAFKA_BROKER,KAFKA_USER,KAFKA_PWD,KAFKA_TOPIC_LOGS,KAFKA_CERT,LOG_TIME_FORMAT,DEMO_LOGS)
    else:
        template = loader.get_template('demouiapp/loginui.html')
    return HttpResponse(template.render(get_base_context(), request))


def injectEventsREST(request):
    print('🌏 injectEventsREST')
    global loggedin, INCIDENT_ACTIVE, ROBOT_SHOP_OUTAGE_ACTIVE, SOCK_SHOP_OUTAGE_ACTIVE
    print('     🟣 OUTAGE - Incident:'+str(INCIDENT_ACTIVE)+' - RS-OUTAGE:'+str(ROBOT_SHOP_OUTAGE_ACTIVE)+' - SOCK-OUTAGE:'+str(SOCK_SHOP_OUTAGE_ACTIVE))
    verifyLogin(request)

    if loggedin=='true':
        injectEventsMemRobot(DATALAYER_ROUTE,DATALAYER_USER,DATALAYER_PWD)
        template = loader.get_template('demouiapp/home.html')
    else:
        template = loader.get_template('demouiapp/loginui.html')
    return HttpResponse(template.render(get_base_context(), request))


def injectMetricsREST(request):
    print('🌏 injectMetricsREST')
    global loggedin, INCIDENT_ACTIVE, ROBOT_SHOP_OUTAGE_ACTIVE, SOCK_SHOP_OUTAGE_ACTIVE
    print('     🟣 OUTAGE - Incident:'+str(INCIDENT_ACTIVE)+' - RS-OUTAGE:'+str(ROBOT_SHOP_OUTAGE_ACTIVE)+' - SOCK-OUTAGE:'+str(SOCK_SHOP_OUTAGE_ACTIVE))
    verifyLogin(request)

    if loggedin=='true':
        injectMetricsMem(METRIC_ROUTE,METRIC_TOKEN)
        template = loader.get_template('demouiapp/home.html')
    else:
        template = loader.get_template('demouiapp/loginui.html')
    return HttpResponse(template.render(get_base_context(), request))


def injectCUSTOM(request):
    print('🌏 injectCUSTOM')
    global loggedin, INCIDENT_ACTIVE, ROBOT_SHOP_OUTAGE_ACTIVE, SOCK_SHOP_OUTAGE_ACTIVE
    print('     🟣 OUTAGE - Incident:'+str(INCIDENT_ACTIVE)+' - RS-OUTAGE:'+str(ROBOT_SHOP_OUTAGE_ACTIVE)+' - SOCK-OUTAGE:'+str(SOCK_SHOP_OUTAGE_ACTIVE))
    verifyLogin(request)
    if loggedin=='true':
        template = loader.get_template('demouiapp/home.html')

        print ('🟣           📈 CUSTOM_NAME:                    '+str(CUSTOM_NAME))
        print ('🟣           📈 CUSTOM_EVENTS:                  '+str(len(CUSTOM_EVENTS)))
        print ('🟣           📈 CUSTOM_METRICS:                 '+str(len(CUSTOM_METRICS)-1))
        print ('🟣           📈 CUSTOM_LOGS:                    '+str(len(CUSTOM_LOGS)))
        print ('🟣           📈 CUSTOM_TOPOLOGY:                '+str(len(CUSTOM_TOPOLOGY)))
        print ('🟣           📈 CUSTOM_PROPERTY_RESOURCE_NAME:    '+str(CUSTOM_PROPERTY_RESOURCE_NAME))
        print ('🟣           📈 CUSTOM_PROPERTY_RESOURCE_TYPE:    '+str(CUSTOM_PROPERTY_RESOURCE_TYPE))
        print ('🟣           📈 CUSTOM_PROPERTY_VALUES_NOK:     '+str(CUSTOM_PROPERTY_VALUES_NOK))
        print ('🟣           📈 CUSTOM_PROPERTY_VALUES_OK:      '+str(CUSTOM_PROPERTY_VALUES_OK))

        if len(CUSTOM_EVENTS)>0:
            print('  🟠 Start THREADS CUSTOM_EVENTS')
            Thread(target=injectEventsCUSTOM, args=(DATALAYER_ROUTE,DATALAYER_USER,DATALAYER_PWD)).start()

        if len(CUSTOM_METRICS)>1:
            print('  🟠 Start THREADS CUSTOM_METRICS')
            Thread(target=injectMetricsCUSTOM, args=(METRIC_ROUTE,METRIC_TOKEN,)).start()

        if len(CUSTOM_LOGS)>0:
            print('  🟠 Start THREADS CUSTOM_LOGS')
            Thread(target=injectLogsCUSTOM, args=(KAFKA_BROKER,KAFKA_USER,KAFKA_PWD,KAFKA_TOPIC_LOGS,KAFKA_CERT,LOG_TIME_FORMAT,DEMO_LOGS,)).start()

        if len(CUSTOM_PROPERTY_RESOURCE_NAME)>0:
            print('  🟠 Start THREADS CUSTOM_PROPS')
            Thread(target=modifyProperty, args=(CUSTOM_PROPERTY_RESOURCE_NAME,CUSTOM_PROPERTY_RESOURCE_TYPE,CUSTOM_PROPERTY_VALUES_NOK,)).start()

    else:
        template = loader.get_template('demouiapp/loginui.html')

    return HttpResponse(template.render(get_base_context(), request))





def clearAllREST(request):
    print('🌏 clearAllREST')
    global loggedin, INCIDENT_ACTIVE, ROBOT_SHOP_OUTAGE_ACTIVE, SOCK_SHOP_OUTAGE_ACTIVE
    print('     🟣 OUTAGE - Incident:'+str(INCIDENT_ACTIVE)+' - RS-OUTAGE:'+str(ROBOT_SHOP_OUTAGE_ACTIVE)+' - SOCK-OUTAGE:'+str(SOCK_SHOP_OUTAGE_ACTIVE))
    verifyLogin(request)
    if loggedin=='true':
        template = loader.get_template('demouiapp/home.html')

        print('  🟠 Create THREADS')
        threadMitigateIssues = Thread(target=mitigateIssues, args=(DATALAYER_ROUTE,DATALAYER_USER,DATALAYER_PWD))
        threadCloseAlerts = Thread(target=closeAlerts, args=(DATALAYER_ROUTE,DATALAYER_USER,DATALAYER_PWD))
        threadCloseStories = Thread(target=closeStories, args=(DATALAYER_ROUTE,DATALAYER_USER,DATALAYER_PWD))

        print('  🟠 Start THREADS')
        threadMitigateIssues.start()
        threadCloseAlerts.start()
        threadCloseStories.start()
        time.sleep(1)

        INCIDENT_ACTIVE=False
        ROBOT_SHOP_OUTAGE_ACTIVE=False
        SOCK_SHOP_OUTAGE_ACTIVE=False

        print('  🟠 Start THREADS PROPS')
        Thread(target=modifyProperty, args=(ROBOTSHOP_PROPERTY_RESOURCE_NAME,ROBOTSHOP_PROPERTY_RESOURCE_TYPE,ROBOTSHOP_PROPERTY_VALUES_OK,)).start()
        Thread(target=modifyProperty, args=('frapod01','fiberConnection','{"availability": "OK"}')).start()
        Thread(target=modifyProperty, args=('bepod01','fiberConnection','{"availability": "OK"}')).start()

        time.sleep(5)
        if len(CUSTOM_PROPERTY_RESOURCE_NAME)>0:
            Thread(target=modifyProperty, args=(CUSTOM_PROPERTY_RESOURCE_NAME,CUSTOM_PROPERTY_RESOURCE_TYPE,CUSTOM_PROPERTY_VALUES_OK,)).start()

    else:
        template = loader.get_template('demouiapp/loginui.html')

    return HttpResponse(template.render(get_base_context(), request))


def clearEventsREST(request):
    print('🌏 clearEventsREST')
    global loggedin, INCIDENT_ACTIVE, ROBOT_SHOP_OUTAGE_ACTIVE, SOCK_SHOP_OUTAGE_ACTIVE
    print('     🟣 OUTAGE - Incident:'+str(INCIDENT_ACTIVE)+' - RS-OUTAGE:'+str(ROBOT_SHOP_OUTAGE_ACTIVE)+' - SOCK-OUTAGE:'+str(SOCK_SHOP_OUTAGE_ACTIVE))
    verifyLogin(request)
    if loggedin=='true':
        template = loader.get_template('demouiapp/home.html')
        closeAlerts(DATALAYER_ROUTE,DATALAYER_USER,DATALAYER_PWD)
        print('  🟠 Start THREADS PROPS')
        Thread(target=modifyProperty, args=(ROBOTSHOP_PROPERTY_RESOURCE_NAME,ROBOTSHOP_PROPERTY_RESOURCE_TYPE,ROBOTSHOP_PROPERTY_VALUES_OK,)).start()
        Thread(target=modifyProperty, args=('frapod01','fiberConnection','{"availability": "OK"}')).start()
        Thread(target=modifyProperty, args=('bepod01','fiberConnection','{"availability": "OK"}')).start()

        if len(CUSTOM_PROPERTY_RESOURCE_NAME)>0:
            Thread(target=modifyProperty, args=(CUSTOM_PROPERTY_RESOURCE_NAME,CUSTOM_PROPERTY_RESOURCE_TYPE,CUSTOM_PROPERTY_VALUES_OK,)).start()

    else:
        template = loader.get_template('demouiapp/loginui.html')

    return HttpResponse(template.render(get_base_context(), request))


def clearStoriesREST(request):
    print('🌏 clearStoriesREST')
    global loggedin, INCIDENT_ACTIVE, ROBOT_SHOP_OUTAGE_ACTIVE, SOCK_SHOP_OUTAGE_ACTIVE
    print('     🟣 OUTAGE - Incident:'+str(INCIDENT_ACTIVE)+' - RS-OUTAGE:'+str(ROBOT_SHOP_OUTAGE_ACTIVE)+' - SOCK-OUTAGE:'+str(SOCK_SHOP_OUTAGE_ACTIVE))
    verifyLogin(request)
    if loggedin=='true':
        template = loader.get_template('demouiapp/home.html')
        closeStories(DATALAYER_ROUTE,DATALAYER_USER,DATALAYER_PWD)
        print('  🟠 Start THREADS PROPS')
        Thread(target=modifyProperty, args=(ROBOTSHOP_PROPERTY_RESOURCE_NAME,ROBOTSHOP_PROPERTY_RESOURCE_TYPE,ROBOTSHOP_PROPERTY_VALUES_OK,)).start()
        Thread(target=modifyProperty, args=('frapod01','fiberConnection','{"availability": "OK"}')).start()
        Thread(target=modifyProperty, args=('bepod01','fiberConnection','{"availability": "OK"}')).start()

        if len(CUSTOM_PROPERTY_RESOURCE_NAME)>0:
            Thread(target=modifyProperty, args=(CUSTOM_PROPERTY_RESOURCE_NAME,CUSTOM_PROPERTY_RESOURCE_TYPE,CUSTOM_PROPERTY_VALUES_OK,)).start()

    else:
        template = loader.get_template('demouiapp/loginui.html')
        INCIDENT_ACTIVE=False
        ROBOT_SHOP_OUTAGE_ACTIVE=False
        SOCK_SHOP_OUTAGE_ACTIVE=False

    return HttpResponse(template.render(get_base_context(), request))




def reloadTopology(request):
    print('🌏 reloadTopology')
    global loggedin, INCIDENT_ACTIVE, ROBOT_SHOP_OUTAGE_ACTIVE, SOCK_SHOP_OUTAGE_ACTIVE
    print('     🟣 OUTAGE - Incident:'+str(INCIDENT_ACTIVE)+' - RS-OUTAGE:'+str(ROBOT_SHOP_OUTAGE_ACTIVE)+' - SOCK-OUTAGE:'+str(SOCK_SHOP_OUTAGE_ACTIVE))
    verifyLogin(request)
    if loggedin=='true':
        template = loader.get_template('demouiapp/home.html')
        loadTopology()
    else:
        template = loader.get_template('demouiapp/loginui.html')
        INCIDENT_ACTIVE=False
        ROBOT_SHOP_OUTAGE_ACTIVE=False
        SOCK_SHOP_OUTAGE_ACTIVE=False

    return HttpResponse(template.render(get_base_context(), request))




def injectBusy(request):
    print('🌏 injectBusy')
    global loggedin, INCIDENT_ACTIVE, ROBOT_SHOP_OUTAGE_ACTIVE, SOCK_SHOP_OUTAGE_ACTIVE
    print('     🟣 OUTAGE - Incident:'+str(INCIDENT_ACTIVE)+' - RS-OUTAGE:'+str(ROBOT_SHOP_OUTAGE_ACTIVE)+' - SOCK-OUTAGE:'+str(SOCK_SHOP_OUTAGE_ACTIVE))
    verifyLogin(request)
    if loggedin=='true':
        template = loader.get_template('demouiapp/home.html')

        INCIDENT_ACTIVE=True

        print('🌏 Simulate Busy Environment')
        Thread(target=injectEventsBusy, args=(DATALAYER_ROUTE,DATALAYER_USER,DATALAYER_PWD)).start()

    else:
        template = loader.get_template('demouiapp/loginui.html')
        INCIDENT_ACTIVE=False
        ROBOT_SHOP_OUTAGE_ACTIVE=False
        SOCK_SHOP_OUTAGE_ACTIVE=False

    return HttpResponse(template.render(get_base_context(), request))




def injectRisk(request):
    print('🌏 injectRisk')
    global loggedin, INCIDENT_ACTIVE, ROBOT_SHOP_OUTAGE_ACTIVE, SOCK_SHOP_OUTAGE_ACTIVE
    print('     🟣 OUTAGE - Incident:'+str(INCIDENT_ACTIVE)+' - RS-OUTAGE:'+str(ROBOT_SHOP_OUTAGE_ACTIVE)+' - SOCK-OUTAGE:'+str(SOCK_SHOP_OUTAGE_ACTIVE))
    verifyLogin(request)
    if loggedin=='true':
        template = loader.get_template('demouiapp/home.html')

        INCIDENT_ACTIVE=True

        print('🌏 Simulate Environmental Risks')
        Thread(target=injectEventsRisk, args=(DATALAYER_ROUTE,DATALAYER_USER,DATALAYER_PWD)).start()

    else:
        template = loader.get_template('demouiapp/loginui.html')
        INCIDENT_ACTIVE=False
        ROBOT_SHOP_OUTAGE_ACTIVE=False
        SOCK_SHOP_OUTAGE_ACTIVE=False

    return HttpResponse(template.render(get_base_context(), request))




def login(request):
    print('🌏 login')

    global loggedin, loginip, INCIDENT_ACTIVE, ROBOT_SHOP_OUTAGE_ACTIVE, SOCK_SHOP_OUTAGE_ACTIVE
    print('     🟣 OUTAGE - Incident:'+str(INCIDENT_ACTIVE)+' - RS-OUTAGE:'+str(ROBOT_SHOP_OUTAGE_ACTIVE)+' - SOCK-OUTAGE:'+str(SOCK_SHOP_OUTAGE_ACTIVE))

    response = HttpResponse()

    currentip=request.META.get('REMOTE_ADDR')
    verifyLogin(request)
    currenttoken=request.GET.get("token", "none")
    token=os.environ.get('TOKEN')
    print ('  🔐 Login attempt with Password/Token: '+currenttoken + ' from ' +str(currentip))
    if token==currenttoken:
        loggedin='true'
        template = loader.get_template('demouiapp/home.html')
        print ('  ✅ Login SUCCESSFUL')

        response.set_cookie('last_visit', time.localtime())
        response.set_cookie('IP', request.META.get('REMOTE_ADDR'))
        response.set_cookie('token', hashlib.md5((token).encode()).hexdigest())
    else:
        loggedin='false'
        template = loader.get_template('demouiapp/loginui.html')
        print ('  ❗ Login NOT SUCCESSFUL')

        response.set_cookie('last_visit', 'none')
        response.set_cookie('IP', 'none')
        response.set_cookie('token', 'none')

    response.write(template.render(get_base_context(), request))
    return response


def verifyLogin(request):
    actToken=request.COOKIES.get('token', 'none')
    print('   🔎 PROVIDED TOKEN:'+str(actToken))

    global loggedin
    
    actloginip=request.META.get('REMOTE_ADDR')
    token=os.environ.get('TOKEN')

    if str(actToken)!=hashlib.md5((token).encode()).hexdigest():
        loggedin='false'

        #print('        ❌ LOGIN NOK: NEW IP')
        print('   🔎 Check IP : ❌ LOGIN NOK: ACT SESSION TOKEN:'+str(actToken)+' - LOGGED IN: '+str(loggedin))
        print('   🔎 SESSION TOKEN:'+str(actToken))
    else:
        #print('   🔎 Check IP : ✅ LOGIN OK: '+str(loggedin))
        #print('        ✅ LOGIN OK')
        #loggedin='true'
        loginip=request.META.get('REMOTE_ADDR')





# ----------------------------------------------------------------------------------------------------------------------------------------------------
# PAGE ENDPOINTS
# ----------------------------------------------------------------------------------------------------------------------------------------------------

def loginui(request):
    print('🌏 loginui')
    global loggedin

    verifyLogin(request)
    template = loader.get_template('demouiapp/login.html')
    context = {
        'loggedin': loggedin,
    }
    return HttpResponse(template.render(context, request))


def index(request):
    print('🌏 index')
    global loggedin, INCIDENT_ACTIVE, ROBOT_SHOP_OUTAGE_ACTIVE, SOCK_SHOP_OUTAGE_ACTIVE
    print('     🟣 OUTAGE - Incident:'+str(INCIDENT_ACTIVE)+' - RS-OUTAGE:'+str(ROBOT_SHOP_OUTAGE_ACTIVE)+' - SOCK-OUTAGE:'+str(SOCK_SHOP_OUTAGE_ACTIVE))

    verifyLogin(request)

    if loggedin=='true':
        template = loader.get_template('demouiapp/home.html')
        url = 'https://'+DATALAYER_ROUTE+'/irdatalayer.aiops.io/active/v1/stories'
        auth=HTTPBasicAuth(DATALAYER_USER, DATALAYER_PWD)
        headers = {'Content-Type': 'application/json', 'Accept-Charset': 'UTF-8', 'x-username' : 'admin', 'x-subscription-id' : 'cfd95b7e-3bc7-4006-a4a8-a73a79c71255'}
        try:
            response = requests.get(url, headers=headers, auth=auth, verify=False)
        except requests.exceptions.RequestException as e:  # This is the correct syntax
            stream = capture_shell("oc get route  -n "+aimanagerns+" datalayer-api  -o jsonpath='{.status.ingress[0].host}'")
            print('     ❗ YOU MIGHT WANT TO USE THE DATALAYER PUBLIC ROUTE: '+str(stream.read().strip()))
            raise SystemExit(e)

        responseJSON=response.json()
        responseStr=str(json.dumps(responseJSON))
        if '"state": "assignedToIndividual"' in responseStr or '"state": "inProgress"' in responseStr or '"state": "unassigned"' in responseStr:
            print('     🔴 INCIDENT FOUND')
            INCIDENT_ACTIVE=True
        else:
            print('     🟢 NO INCIDENT')
            INCIDENT_ACTIVE=False

        stream = capture_shell("oc get deployment  -n robot-shop ratings  -o yaml")
        RATINGS_YAML = stream.read().strip()
        if 'ratings-dev' in RATINGS_YAML:
            print('     🔴 ROBOT SHOP OUTAGE ACTIVE')
            ROBOT_SHOP_OUTAGE_ACTIVE=True
        else:
            print('     🟢 ROBOT SHOP OUTAGE INACTIVE')
            ROBOT_SHOP_OUTAGE_ACTIVE=False

        stream = capture_shell("oc get service  -n sock-shop catalogue  -o yaml")
        CATALOG_YAML = stream.read().strip()
        if '-outage' in CATALOG_YAML:
            print('     🔴 SOCK SHOP OUTAGE ACTIVE')
            SOCK_SHOP_OUTAGE_ACTIVE=True
        else:
            print('     🟢 SOCK SHOP OUTAGE INACTIVE')
            SOCK_SHOP_OUTAGE_ACTIVE=False


    else:
        template = loader.get_template('demouiapp/loginui.html')

    return HttpResponse(template.render(get_base_context(), request))


def doc(request):
    print('🌏 doc')
    global loggedin, INCIDENT_ACTIVE, ROBOT_SHOP_OUTAGE_ACTIVE, SOCK_SHOP_OUTAGE_ACTIVE
    print('     🟣 OUTAGE - Incident:'+str(INCIDENT_ACTIVE)+' - RS-OUTAGE:'+str(ROBOT_SHOP_OUTAGE_ACTIVE)+' - SOCK-OUTAGE:'+str(SOCK_SHOP_OUTAGE_ACTIVE))

    verifyLogin(request)

    if loggedin=='true':
        template = loader.get_template('demouiapp/doc.html')
    else:
        template = loader.get_template('demouiapp/loginui.html')
    return HttpResponse(template.render(get_base_context(page_title='IBM AIOps Demo UI', page_name='doc'), request))


def apps(request):
    print('🌏 apps')
    global loggedin, INCIDENT_ACTIVE, ROBOT_SHOP_OUTAGE_ACTIVE, SOCK_SHOP_OUTAGE_ACTIVE
    print('     🟣 OUTAGE - Incident:'+str(INCIDENT_ACTIVE)+' - RS-OUTAGE:'+str(ROBOT_SHOP_OUTAGE_ACTIVE)+' - SOCK-OUTAGE:'+str(SOCK_SHOP_OUTAGE_ACTIVE))

    verifyLogin(request)

    if loggedin=='true':
        template = loader.get_template('demouiapp/apps.html')
    else:
        template = loader.get_template('demouiapp/loginui.html')
    return HttpResponse(template.render(get_base_context(page_title='IBM IT-Automation Solutions', page_name='apps'), request))


def apps_system(request):
    print('🌏 apps_system')
    global loggedin, INCIDENT_ACTIVE, ROBOT_SHOP_OUTAGE_ACTIVE, SOCK_SHOP_OUTAGE_ACTIVE
    print('     🟣 OUTAGE - Incident:'+str(INCIDENT_ACTIVE)+' - RS-OUTAGE:'+str(ROBOT_SHOP_OUTAGE_ACTIVE)+' - SOCK-OUTAGE:'+str(SOCK_SHOP_OUTAGE_ACTIVE))

    verifyLogin(request)

    if loggedin=='true':
        template = loader.get_template('demouiapp/apps_system.html')
    else:
        template = loader.get_template('demouiapp/loginui.html')
    context = get_base_context(page_title='System Tools', page_name='system')
    context.update({
        'FLINK_IR_USER': FLINK_IR_USER,
        'FLINK_IR_PWD': FLINK_IR_PWD,
        'FLINK_LAD_USER': FLINK_LAD_USER,
        'FLINK_LAD_PWD': FLINK_LAD_PWD,
    })
    return HttpResponse(template.render(context, request))


def apps_demo(request):
    print('🌏 apps_demo')
    global loggedin, INCIDENT_ACTIVE, ROBOT_SHOP_OUTAGE_ACTIVE, SOCK_SHOP_OUTAGE_ACTIVE
    print('     🟣 OUTAGE - Incident:'+str(INCIDENT_ACTIVE)+' - RS-OUTAGE:'+str(ROBOT_SHOP_OUTAGE_ACTIVE)+' - SOCK-OUTAGE:'+str(SOCK_SHOP_OUTAGE_ACTIVE))

    verifyLogin(request)

    if loggedin=='true':
        template = loader.get_template('demouiapp/apps_demo.html')
    else:
        template = loader.get_template('demouiapp/loginui.html')
    return HttpResponse(template.render(get_base_context(page_title='Demo Scenarios', page_name='demo'), request))


def apps_additional(request):
    print('🌏 apps_additional')
    global loggedin, INCIDENT_ACTIVE, ROBOT_SHOP_OUTAGE_ACTIVE, SOCK_SHOP_OUTAGE_ACTIVE
    print('     🟣 OUTAGE - Incident:'+str(INCIDENT_ACTIVE)+' - RS-OUTAGE:'+str(ROBOT_SHOP_OUTAGE_ACTIVE)+' - SOCK-OUTAGE:'+str(SOCK_SHOP_OUTAGE_ACTIVE))

    verifyLogin(request)

    if loggedin=='true':
        template = loader.get_template('demouiapp/apps_additional.html')
    else:
        template = loader.get_template('demouiapp/loginui.html')
    context = get_base_context(page_title='Third-party Tools', page_name='TEST')
    context.update({
        'SLACK_URL_ROSH': SLACK_URL_ROSH,
        'SLACK_URL_SOSH': SLACK_URL_SOSH,
        'SLACK_URL_ACME': SLACK_URL_ACME,
        'SNOW_URL_ROSH': SNOW_URL_ROSH,
        'SNOW_URL_SOSH': SNOW_URL_SOSH,
        'SNOW_URL_ACME': SNOW_URL_ACME,
        'INCIDENT_URL_TUBE': INCIDENT_URL_TUBE,
    })
    return HttpResponse(template.render(context, request))


def about(request):
    print('🌏 about')

    global loggedin, INCIDENT_ACTIVE, ROBOT_SHOP_OUTAGE_ACTIVE, SOCK_SHOP_OUTAGE_ACTIVE
    print('     🟣 OUTAGE - Incident:'+str(INCIDENT_ACTIVE)+' - RS-OUTAGE:'+str(ROBOT_SHOP_OUTAGE_ACTIVE)+' - SOCK-OUTAGE:'+str(SOCK_SHOP_OUTAGE_ACTIVE))

    verifyLogin(request)

    if loggedin=='true':
        template = loader.get_template('demouiapp/about.html')
    else:
        template = loader.get_template('demouiapp/loginui.html')
    context = get_base_context(page_title='About', page_name='about')
    context.update({
        'DEMO_IMAGE': demo_image,
        'ALL_LOGINS': ALL_LOGINS,
        'mod_time_readable': mod_time_readable,
        'CUSTOM_EVENTS': CUSTOM_EVENTS,
        'CUSTOM_METRICS': CUSTOM_METRICS,
        'CUSTOM_LOGS': CUSTOM_LOGS,
        'CUSTOM_TOPOLOGY': CUSTOM_TOPOLOGY,
        'CUSTOM_TOPOLOGY_APP_NAME': CUSTOM_TOPOLOGY_APP_NAME,
        'CUSTOM_TOPOLOGY_TAG': CUSTOM_TOPOLOGY_TAG,
    })
    return HttpResponse(template.render(context, request))


def config(request):
    print('🌏 config')
    global loggedin, INCIDENT_ACTIVE, ROBOT_SHOP_OUTAGE_ACTIVE, SOCK_SHOP_OUTAGE_ACTIVE
    print('     🟣 OUTAGE - Incident:'+str(INCIDENT_ACTIVE)+' - RS-OUTAGE:'+str(ROBOT_SHOP_OUTAGE_ACTIVE)+' - SOCK-OUTAGE:'+str(SOCK_SHOP_OUTAGE_ACTIVE))

    verifyLogin(request)

    if loggedin=='true':
        template = loader.get_template('demouiapp/config.html')
    else:
        template = loader.get_template('demouiapp/loginui.html')
    context = get_base_context(page_title='Configuration for the IBM AIOps Training', page_name='config')
    context['ALL_LOGINS'] = ALL_LOGINS
    return HttpResponse(template.render(context, request))

def watsonx(request):
    template = loader.get_template('demouiapp/watsonx.html')
    context = {
        'loggedin': loggedin,
        'INSTANCE_NAME': INSTANCE_NAME
    }
    return HttpResponse(template.render(context, request))




def index1(request):
    template = loader.get_template('demouiapp/index.html')
    context = {
        'loggedin': loggedin,
        'INSTANCE_NAME': INSTANCE_NAME
    }
    return HttpResponse(template.render(context, request))


def health(request):
    return HttpResponse('healthy')
