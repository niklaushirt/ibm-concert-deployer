
import requests
from requests.auth import HTTPBasicAuth
import json
import datetime
import random
import os
import time
from functions import *

DEMO_EVENTS_MEM=os.environ.get('DEMO_EVENTS_MEM')
DEMO_EVENTS_FAN=os.environ.get('DEMO_EVENTS_FAN')
DEMO_LOGS=os.environ.get('DEMO_LOGS')
LOG_ITERATIONS=int(os.environ.get('LOG_ITERATIONS'))
LOG_TIME_FORMAT=os.environ.get('LOG_TIME_FORMAT')
LOG_TIME_STEPS=int(os.environ.get('LOG_TIME_STEPS'))
LOG_TIME_SKEW=int(os.environ.get('LOG_TIME_SKEW'))
LOG_TIME_ZONE=int(os.environ.get('LOG_TIME_ZONE'))

EVENTS_TIME_SKEW=int(os.environ.get('EVENTS_TIME_SKEW'))

INSTANCE_NAME=os.environ.get('INSTANCE_NAME')
if INSTANCE_NAME == None:
    INSTANCE_NAME="IBMAIOPS"


METRIC_TIME_SKEW=int(os.environ.get('METRIC_TIME_SKEW'))
METRIC_TIME_STEP=int(os.environ.get('METRIC_TIME_STEP'))
METRICS_TO_SIMULATE_MEM=str(os.environ.get('METRICS_TO_SIMULATE_MEM')).split(';')
METRICS_TO_SIMULATE_FAN_TEMP=str(os.environ.get('METRICS_TO_SIMULATE_FAN_TEMP')).split(';')
METRICS_TO_SIMULATE_FAN=str(os.environ.get('METRICS_TO_SIMULATE_FAN')).split(';')


DEBUG_ME=os.environ.get('DEBUG_ME',"False")


ACTIVE=os.environ.get('ACTIVE',"False")


WAIT_BASE=int(os.environ.get('WAIT_BASE',"60"))
WAIT_INPROGRESS=int(os.environ.get('WAIT_INPROGRESS',"60"))
WAIT_RESOLVE=int(os.environ.get('WAIT_RESOLVE',"60"))
WAIT_RESTART=int(os.environ.get('WAIT_RESTART',"300"))




print ('*************************************************************************************************')
print ('*************************************************************************************************')
print ('            ________  __  ___     ___    ________       ')
print ('           /  _/ __ )/  |/  /    /   |  /  _/ __ \____  _____')
print ('           / // __  / /|_/ /    / /| |  / // / / / __ \/ ___/')
print ('         _/ // /_/ / /  / /    / ___ |_/ // /_/ / /_/ (__  ) ')
print ('        /___/_____/_/  /_/    /_/  |_/___/\____/ .___/____/  ')
print ('                                              /_/')
print ('*************************************************************************************************')
print ('*************************************************************************************************')
print ('')
print ('    🛰️  Generic Incident Simulator for Concert Operate IBMAIOps')
print ('')
print ('       Provided by:')
print ('        🇨🇭 Niklaus Hirt (nikh@ch.ibm.com)')
print ('')

print ('-------------------------------------------------------------------------------------------------')
print (' 🚀 Warming up')
print ('-------------------------------------------------------------------------------------------------')

#os.system('ls -l')
loggedin='false'
loginip='0.0.0.0'

# ----------------------------------------------------------------------------------------------------------------------------------------------------
# GET NAMESPACES
# ----------------------------------------------------------------------------------------------------------------------------------------------------
print('     ❓ Getting Concert Operate Namespace')
stream = os.popen("oc get po -A|grep aiops-orchestrator-controller |awk '{print$1}'")
aimanagerns = stream.read().strip()
print('        ✅ Concert Operate Namespace:       '+aimanagerns)




# ----------------------------------------------------------------------------------------------------------------------------------------------------
# DEFAULT VALUES
# ----------------------------------------------------------------------------------------------------------------------------------------------------
TOKEN='test'


# ----------------------------------------------------------------------------------------------------------------------------------------------------
# GET CONNECTIONS
# ----------------------------------------------------------------------------------------------------------------------------------------------------
global DATALAYER_ROUTE
global DATALAYER_USER
global DATALAYER_PWD
global api_url

# ----------------------------------------------------------------------------------------------------------------------------------------------------
# GET CONNECTIONS
# ----------------------------------------------------------------------------------------------------------------------------------------------------
print('     ❓ Getting Details Kafka')
stream = os.popen("oc get kafkatopics -n "+aimanagerns+"  | grep -v cp4waiopscp4waiops| grep cp4waiops-cartridge-logs-elk| awk '{print $1;}'")
KAFKA_TOPIC_LOGS = stream.read().strip()
stream = os.popen("oc get secret -n "+aimanagerns+" |grep 'aiops-kafka-secret'|awk '{print$1}'")
KAFKA_SECRET = stream.read().strip()
stream = os.popen("oc get secret "+KAFKA_SECRET+" -n "+aimanagerns+" --template={{.data.username}} | base64 --decode")
KAFKA_USER = stream.read().strip()
stream = os.popen("oc get secret "+KAFKA_SECRET+" -n "+aimanagerns+" --template={{.data.password}} | base64 --decode")
KAFKA_PWD = stream.read().strip()
stream = os.popen("oc get routes iaf-system-kafka-0 -n "+aimanagerns+" -o=jsonpath={.status.ingress[0].host}")
KAFKA_BROKER = stream.read().strip()
stream = os.popen("oc get secret -n "+aimanagerns+" kafka-secrets  -o jsonpath='{.data.ca\.crt}'| base64 --decode")
KAFKA_CERT = stream.read().strip()

print('     ❓ Getting Details Datalayer')
stream = os.popen("oc get route  -n "+aimanagerns+" datalayer-api  -o jsonpath='{.status.ingress[0].host}'")
DATALAYER_ROUTE = stream.read().strip()
stream = os.popen("oc get secret -n "+aimanagerns+" aiops-ir-core-ncodl-api-secret -o jsonpath='{.data.username}' | base64 --decode")
DATALAYER_USER = stream.read().strip()
stream = os.popen("oc get secret -n "+aimanagerns+" aiops-ir-core-ncodl-api-secret -o jsonpath='{.data.password}' | base64 --decode")
DATALAYER_PWD = stream.read().strip()

print('     ❓ Getting Details Metric Endpoint')
stream = os.popen("oc get route -n "+aimanagerns+"| grep ibm-nginx-svc | awk '{print $2}'")
METRIC_ROUTE = stream.read().strip()
stream = os.popen("oc get secret -n "+aimanagerns+" admin-user-details -o jsonpath='{.data.initial_admin_password}' | base64 --decode")
tmppass = stream.read().strip()
stream = os.popen('curl -k -s -X POST https://'+METRIC_ROUTE+'/icp4d-api/v1/authorize -H "Content-Type: application/json" -d "{\\\"username\\\": \\\"admin\\\",\\\"password\\\": \\\"'+tmppass+'\\\"}" | jq .token | sed "s/\\\"//g"')
METRIC_TOKEN = stream.read().strip()





ITERATE_ELEMENT=os.environ.get('ITERATE_ELEMENT')
WEBHOOK_DEBUG=os.environ.get('WEBHOOK_DEBUG')



print ('')
print ('')
print ('')
print ('-------------------------------------------------------------------------------------------------')
print (' 🔎 Parameters')
print ('-------------------------------------------------------------------------------------------------')
print ('')
print ('    ---------------------------------------------------------------------------------------------')
print ('     🔎 Global Parameters')
print ('    ---------------------------------------------------------------------------------------------')
print ('           🔐 DEBUG:              '+DEBUG_ME)
print ('           🔐 Token:              '+TOKEN)
print ('')
print ('')

print ('    ---------------------------------------------------------------------------------------------')
print ('     🔎 Concert Operate Connection Parameters')
print ('    ---------------------------------------------------------------------------------------------')
print ('           🌏 Datalayer Route:    '+DATALAYER_ROUTE)
print ('           👩‍💻 Datalayer User:     '+DATALAYER_USER)
print ('           🔐 Datalayer Pwd:      '+DATALAYER_PWD)
print ('')
print ('')
print ('    ---------------------------------------------------------------------------------------------')
print ('     🔎 Simulation Parameters')
print ('    ---------------------------------------------------------------------------------------------')
print ('           INSTANCE_NAME:                  '+str(INSTANCE_NAME))
print ('           LOG_ITERATIONS:                 '+str(LOG_ITERATIONS))
print ('           LOG_TIME_FORMAT:                '+LOG_TIME_FORMAT)
print ('           LOG_TIME_STEPS:                 '+str(LOG_TIME_STEPS))
print ('           LOG_TIME_SKEW Logs:             '+str(LOG_TIME_SKEW))
print ('           LOG_TIME_ZONE Cert:             '+str(LOG_TIME_ZONE))
print ('')
print ('           EVENTS_TIME_SKEW:               '+str(EVENTS_TIME_SKEW))
print ('           DEMO_EVENTS_MEM:                '+str(len(DEMO_EVENTS_MEM)))
print ('           DEMO_EVENTS_FAN:                '+str(len(DEMO_EVENTS_FAN)))
print ('')
print ('           METRIC_TIME_SKEW:               '+str(METRIC_TIME_SKEW))
print ('           METRIC_TIME_STEP:               '+str(METRIC_TIME_STEP))
print ('           METRICS_TO_SIMULATE_MEM:        '+str(len(METRICS_TO_SIMULATE_MEM)))
print ('           METRICS_TO_SIMULATE_FAN_TEMP:   '+str(len(METRICS_TO_SIMULATE_FAN_TEMP)))
print ('           METRICS_TO_SIMULATE_FAN:        '+str(len(METRICS_TO_SIMULATE_FAN)))
print ('')
print ('           WAIT_BASE:                      '+str(WAIT_BASE))
print ('           WAIT_INPROGRESS:                '+str(WAIT_INPROGRESS))
print ('           WAIT_RESOLVE:                   '+str(WAIT_RESOLVE))
print ('           WAIT_RESTART:                   '+str(WAIT_RESTART))
print ('')
print ('    ---------------------------------------------------------------------------------------------')
print('')
print('')

print ('    ---------------------------------------------------------------------------------------------')
print ('     🔎 Simulation Endpoints')
print ('    ---------------------------------------------------------------------------------------------')
print ('           KafkaBroker:           '+KAFKA_BROKER)
print ('           KafkaUser:             '+KAFKA_USER)
print ('           KafkaPWD:              '+KAFKA_PWD)
print ('           KafkaTopic Logs:       '+KAFKA_TOPIC_LOGS)
print ('           Kafka Cert:            '+KAFKA_CERT[:25]+'...')
print ('')   
print ('')   
print ('           Datalayer Route:       '+DATALAYER_ROUTE)
print ('           Datalayer User:        '+DATALAYER_USER)
print ('           Datalayer Pwd:         '+DATALAYER_PWD)
print ('')   
print ('           Metric Route:          '+METRIC_ROUTE)
print ('           Metric Token:          '+METRIC_TOKEN[:25]+'...')
print ('')   
print ('           Token:                 '+TOKEN)
print ('')   

print ('-------------------------------------------------------------------------------------------------')
print (' 🚀 Initializing Simulator')
print ('-------------------------------------------------------------------------------------------------')


#resolved
#assignedToIndividual
#inProgress
#resolved
#closed

print ('-------------------------------------------------------------------------------------------------')
print (' 🚀 Running Simulator')
print ('-------------------------------------------------------------------------------------------------')

while True:
    if ACTIVE=="True": 

        print ('-------------------------------------------------------------------------------------------------')
        print (' 🚀 SIMULATOR ROBOT SHOP')
        print ('-------------------------------------------------------------------------------------------------')

        print ('     🚀 Simulating Events ROBOTSHOP')
        injectEventsMem(DATALAYER_ROUTE,DATALAYER_USER,DATALAYER_PWD)

        print ('     🚀 Simulating Metrics ROBOTSHOP')
        injectMetricsMem(METRIC_ROUTE,METRIC_TOKEN)

        print ('     🚀 Simulating Logs ROBOTSHOP')
        injectLogs(KAFKA_BROKER,KAFKA_USER,KAFKA_PWD,KAFKA_TOPIC_LOGS,KAFKA_CERT,LOG_TIME_FORMAT,DEMO_LOGS)

        print ('     🚀 Simulating Metrics ROBOTSHOP')
        injectMetricsMem(METRIC_ROUTE,METRIC_TOKEN)

        print ('     🚀 Simulating Logs ROBOTSHOP')
        injectLogs(KAFKA_BROKER,KAFKA_USER,KAFKA_PWD,KAFKA_TOPIC_LOGS,KAFKA_CERT,LOG_TIME_FORMAT,DEMO_LOGS)

        print ('     🚀 Simulating Events ROBOTSHOP')
        injectEventsMem(DATALAYER_ROUTE,DATALAYER_USER,DATALAYER_PWD)
        print ('     🚀 Simulating Events ROBOTSHOP')
        injectEventsMem(DATALAYER_ROUTE,DATALAYER_USER,DATALAYER_PWD)
        print ('     🚀 Simulating Events ROBOTSHOP')
        injectEventsMem(DATALAYER_ROUTE,DATALAYER_USER,DATALAYER_PWD)
        print ('     🚀 Simulating Events ROBOTSHOP')
        injectEventsMem(DATALAYER_ROUTE,DATALAYER_USER,DATALAYER_PWD)
        print ('     🚀 Simulating Events ROBOTSHOP')
        injectEventsMem(DATALAYER_ROUTE,DATALAYER_USER,DATALAYER_PWD)
        print ('     🚀 Simulating Events ROBOTSHOP')
        injectEventsMem(DATALAYER_ROUTE,DATALAYER_USER,DATALAYER_PWD)
        print ('     🚀 Simulating Events ROBOTSHOP')
        injectEventsMem(DATALAYER_ROUTE,DATALAYER_USER,DATALAYER_PWD)
        print ('     🚀 Simulating Events ROBOTSHOP')
        injectEventsMem(DATALAYER_ROUTE,DATALAYER_USER,DATALAYER_PWD)
        print ('     🚀 Simulating Event ROBOTSHOPs')
        injectEventsMem(DATALAYER_ROUTE,DATALAYER_USER,DATALAYER_PWD)


        print ('-------------------------------------------------------------------------------------------------')
        print (' 🕦 Waiting '+str(WAIT_INPROGRESS)+' Seconds before Acknowledge')
        print ('-------------------------------------------------------------------------------------------------')
        time.sleep(WAIT_INPROGRESS)


        print ('-------------------------------------------------------------------------------------------------')
        print (' 🚀 Update Stories to InProgress')
        print ('-------------------------------------------------------------------------------------------------')
        updateStories(DATALAYER_ROUTE,DATALAYER_USER,DATALAYER_PWD,"inProgress")



        print ('-------------------------------------------------------------------------------------------------')
        print (' 🕦 Waiting '+str(WAIT_RESOLVE)+' Seconds before Resolve')
        print ('-------------------------------------------------------------------------------------------------')
        time.sleep(WAIT_RESOLVE)

        print ('-------------------------------------------------------------------------------------------------')
        print (' 🚀 Update Stories to Resolved')
        print ('-------------------------------------------------------------------------------------------------')
        updateStories(DATALAYER_ROUTE,DATALAYER_USER,DATALAYER_PWD,"resolved")


        print ('-------------------------------------------------------------------------------------------------')
        print (' 🕦 Waiting 30 Seconds before Close')
        print ('-------------------------------------------------------------------------------------------------')
        time.sleep(30)

        print ('-------------------------------------------------------------------------------------------------')
        print (' 🚀 Update Stories to Closed')
        print ('-------------------------------------------------------------------------------------------------')
        updateAlerts(DATALAYER_ROUTE,DATALAYER_USER,DATALAYER_PWD,"closed")
        updateStories(DATALAYER_ROUTE,DATALAYER_USER,DATALAYER_PWD,"closed")
        
        print ('-------------------------------------------------------------------------------------------------')
        print (' 🕦 Waiting '+str(WAIT_RESTART)+' Seconds before recreating scenario')
        print ('-------------------------------------------------------------------------------------------------')
        time.sleep(WAIT_RESTART)


        print ('-------------------------------------------------------------------------------------------------')
        print (' 🚀 SIMULATOR SOCK SHOP')
        print ('-------------------------------------------------------------------------------------------------')

        print ('     🚀 Simulating Events SOCKSHOP')
        injectEventsNet(DATALAYER_ROUTE,DATALAYER_USER,DATALAYER_PWD)

        print ('     🚀 Simulating Metrics SOCKSHOP')
        injectMetricsNet(METRIC_ROUTE,METRIC_TOKEN)

        print ('     🚀 Simulating Metrics SOCKSHOP')
        injectMetricsNet(METRIC_ROUTE,METRIC_TOKEN)

        print ('     🚀 Simulating Events SOCKSHOP')
        injectEventsNet(DATALAYER_ROUTE,DATALAYER_USER,DATALAYER_PWD)
        print ('     🚀 Simulating Events SOCKSHOP')
        injectEventsNet(DATALAYER_ROUTE,DATALAYER_USER,DATALAYER_PWD)
        print ('     🚀 Simulating Events SOCKSHOP')
        injectEventsNet(DATALAYER_ROUTE,DATALAYER_USER,DATALAYER_PWD)
        print ('     🚀 Simulating Events SOCKSHOP')
        injectEventsNet(DATALAYER_ROUTE,DATALAYER_USER,DATALAYER_PWD)
        print ('     🚀 Simulating Events SOCKSHOP')
        injectEventsNet(DATALAYER_ROUTE,DATALAYER_USER,DATALAYER_PWD)
        print ('     🚀 Simulating Events SOCKSHOP')
        injectEventsNet(DATALAYER_ROUTE,DATALAYER_USER,DATALAYER_PWD)
        print ('     🚀 Simulating Events SOCKSHOP')
        injectEventsNet(DATALAYER_ROUTE,DATALAYER_USER,DATALAYER_PWD)
        print ('     🚀 Simulating Events SOCKSHOP')
        injectEventsNet(DATALAYER_ROUTE,DATALAYER_USER,DATALAYER_PWD)
        print ('     🚀 Simulating Event SOCKSHOP')
        injectEventsNet(DATALAYER_ROUTE,DATALAYER_USER,DATALAYER_PWD)

        print ('     🚀 Simulating Metrics SOCKSHOP')
        injectMetricsNet(METRIC_ROUTE,METRIC_TOKEN)

        print ('-------------------------------------------------------------------------------------------------')
        print (' 🕦 Waiting '+str(WAIT_INPROGRESS)+' Seconds before Acknowledge')
        print ('-------------------------------------------------------------------------------------------------')
        time.sleep(WAIT_INPROGRESS)


        print ('-------------------------------------------------------------------------------------------------')
        print (' 🚀 Update Stories to InProgress')
        print ('-------------------------------------------------------------------------------------------------')
        updateStories(DATALAYER_ROUTE,DATALAYER_USER,DATALAYER_PWD,"inProgress")



        print ('-------------------------------------------------------------------------------------------------')
        print (' 🕦 Waiting '+str(WAIT_RESOLVE)+' Seconds before Resolve')
        print ('-------------------------------------------------------------------------------------------------')
        time.sleep(WAIT_RESOLVE)

        print ('-------------------------------------------------------------------------------------------------')
        print (' 🚀 Update Stories to Resolved')
        print ('-------------------------------------------------------------------------------------------------')
        updateStories(DATALAYER_ROUTE,DATALAYER_USER,DATALAYER_PWD,"resolved")


        print ('-------------------------------------------------------------------------------------------------')
        print (' 🕦 Waiting 30 Seconds before Close')
        print ('-------------------------------------------------------------------------------------------------')
        time.sleep(30)

        print ('-------------------------------------------------------------------------------------------------')
        print (' 🚀 Update Stories to Closed')
        print ('-------------------------------------------------------------------------------------------------')
        updateAlerts(DATALAYER_ROUTE,DATALAYER_USER,DATALAYER_PWD,"closed")
        updateStories(DATALAYER_ROUTE,DATALAYER_USER,DATALAYER_PWD,"closed")
        
        print ('-------------------------------------------------------------------------------------------------')
        print (' 🕦 Waiting '+str(WAIT_RESTART)+' Seconds before recreating scenario')
        print ('-------------------------------------------------------------------------------------------------')
        time.sleep(WAIT_RESTART)


        print ('-------------------------------------------------------------------------------------------------')
        print (' 🚀 SIMULATOR ACME AIR')
        print ('-------------------------------------------------------------------------------------------------')

        print ('     🚀 Simulating Events ACME AIR')
        injectEventsFan(DATALAYER_ROUTE,DATALAYER_USER,DATALAYER_PWD)

        print ('     🚀 Simulating Metrics ACME AIR')
        injectMetricsFan(METRIC_ROUTE,METRIC_TOKEN)

        print ('     🚀 Simulating Metrics ACME AIR')
        injectMetricsFan(METRIC_ROUTE,METRIC_TOKEN)

        print ('     🚀 Simulating Events ACME AIR')
        injectEventsFan(DATALAYER_ROUTE,DATALAYER_USER,DATALAYER_PWD)
        print ('     🚀 Simulating Events ACME AIR')
        injectEventsFan(DATALAYER_ROUTE,DATALAYER_USER,DATALAYER_PWD)
        print ('     🚀 Simulating Events ACME AIR')
        injectEventsFan(DATALAYER_ROUTE,DATALAYER_USER,DATALAYER_PWD)
        print ('     🚀 Simulating Events ACME AIR')
        injectEventsFan(DATALAYER_ROUTE,DATALAYER_USER,DATALAYER_PWD)
        print ('     🚀 Simulating Events ACME AIR')
        injectEventsFan(DATALAYER_ROUTE,DATALAYER_USER,DATALAYER_PWD)
        print ('     🚀 Simulating Events ACME AIR')
        injectEventsFan(DATALAYER_ROUTE,DATALAYER_USER,DATALAYER_PWD)
        print ('     🚀 Simulating Events ACME AIR')
        injectEventsFan(DATALAYER_ROUTE,DATALAYER_USER,DATALAYER_PWD)
        print ('     🚀 Simulating Events ACME AIR')
        injectEventsFan(DATALAYER_ROUTE,DATALAYER_USER,DATALAYER_PWD)
        print ('     🚀 Simulating Event ACME AIR')
        injectEventsFan(DATALAYER_ROUTE,DATALAYER_USER,DATALAYER_PWD)
        
        print ('     🚀 Simulating Metrics ACME AIR')
        injectMetricsFan(METRIC_ROUTE,METRIC_TOKEN)



        print ('-------------------------------------------------------------------------------------------------')
        print (' 🕦 Waiting '+str(WAIT_INPROGRESS)+' Seconds before Acknowledge')
        print ('-------------------------------------------------------------------------------------------------')
        time.sleep(WAIT_INPROGRESS)


        print ('-------------------------------------------------------------------------------------------------')
        print (' 🚀 Update Stories to InProgress')
        print ('-------------------------------------------------------------------------------------------------')
        updateStories(DATALAYER_ROUTE,DATALAYER_USER,DATALAYER_PWD,"inProgress")



        print ('-------------------------------------------------------------------------------------------------')
        print (' 🕦 Waiting '+str(WAIT_RESOLVE)+' Seconds before Resolve')
        print ('-------------------------------------------------------------------------------------------------')
        time.sleep(WAIT_RESOLVE)

        print ('-------------------------------------------------------------------------------------------------')
        print (' 🚀 Update Stories to Resolved')
        print ('-------------------------------------------------------------------------------------------------')
        updateStories(DATALAYER_ROUTE,DATALAYER_USER,DATALAYER_PWD,"resolved")


        print ('-------------------------------------------------------------------------------------------------')
        print (' 🕦 Waiting 30 Seconds before Close')
        print ('-------------------------------------------------------------------------------------------------')
        time.sleep(30)

        print ('-------------------------------------------------------------------------------------------------')
        print (' 🚀 Update Stories to Closed')
        print ('-------------------------------------------------------------------------------------------------')
        updateAlerts(DATALAYER_ROUTE,DATALAYER_USER,DATALAYER_PWD,"closed")
        updateStories(DATALAYER_ROUTE,DATALAYER_USER,DATALAYER_PWD,"closed")
        
        print ('-------------------------------------------------------------------------------------------------')
        print (' 🕦 Waiting '+str(WAIT_RESTART)+' Seconds before recreating scenario')
        print ('-------------------------------------------------------------------------------------------------')
        time.sleep(WAIT_RESTART)
    else:
        print ('     ❌ Inactive - Waiting 15 Seconds')
        time.sleep(15)



print ('')
print ('')
print ('')
print ('-------------------------------------------------------------------------------------------------')
print (' ✅ Pusher is DONE')
print ('-------------------------------------------------------------------------------------------------')
print ('')
print ('')




