import instana
import os
import sys 
import time 
import requests
from requests.auth import HTTPBasicAuth
import time
from functions import *
import os
import sqlite3
import hashlib

requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
os.environ['PYTHONWARNINGS']="ignore:Unverified HTTPS request"

ACTIVE=os.environ.get('ACTIVE',"False")
DEBUG_ME=os.environ.get('DEBUG_ME',"False")

POLL_DELAY=int(os.environ.get('POLL_DELAY',5))
INSTANCE_NAME=os.environ.get('INSTANCE_NAME','Demo')
MIN_RANK=int(os.environ.get('MIN_RANK',1))

PROVIDER_NAME=os.environ.get('PROVIDER_NAME','NONE')
PROVIDER_URL=os.environ.get('PROVIDER_URL','NONE')
PROVIDER_USER=os.environ.get('PROVIDER_USER','NONE')
PROVIDER_TOKEN=os.environ.get('PROVIDER_TOKEN','NONE')



if PROVIDER_NAME=="NONE": 
    print ('-------------------------------------------------------------------------------------------------')
    print (' ❗ PROVIDER_NAME not provided')
    print (' ❗ Aborting....')
    print ('-------------------------------------------------------------------------------------------------')
if PROVIDER_URL=="NONE": 
    print ('-------------------------------------------------------------------------------------------------')
    print (' ❗ PROVIDER_URL not provided')
    print (' ❗ Aborting....')
    print ('-------------------------------------------------------------------------------------------------')
if PROVIDER_USER=="NONE": 
    print ('-------------------------------------------------------------------------------------------------')
    print (' ❗ PROVIDER_USER not provided')
    print (' ❗ Aborting....')
    print ('-------------------------------------------------------------------------------------------------')
if PROVIDER_TOKEN=="NONE": 
    print ('-------------------------------------------------------------------------------------------------')
    print (' ❗ PROVIDER_TOKEN not provided')
    print (' ❗ Aborting....')
    print ('-------------------------------------------------------------------------------------------------')



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
print ('    🛰️  '+str(PROVIDER_NAME)+' Incident Pusher for Concert Operate IBMAIOps')
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

print('     🛠️ Initializing DB')
conn = sqlite3.connect('./db/incidents.db')

print('        ✅ Opened database successfully')

try:
    conn.execute('''CREATE TABLE INCIDENTS
            (ID TEXT PRIMARY KEY     NOT NULL, MESSAGE_HASH TEXT NOT NULL, PROVIDER_ID TEXT NOT NULL);''')
except sqlite3.OperationalError as e:
   # handle ConnectionError the exception
   print('        ℹ️  DB: '+str(e))


print ('')

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
print ('')
print('     ❓ Getting Details Datalayer')
stream = os.popen("oc get route  -n "+aimanagerns+" datalayer-api  -o jsonpath='{.status.ingress[0].host}'")
DATALAYER_ROUTE = stream.read().strip()
stream = os.popen("oc get secret -n "+aimanagerns+" aiops-ir-core-ncodl-api-secret -o jsonpath='{.data.username}' | base64 --decode")
DATALAYER_USER = stream.read().strip()
stream = os.popen("oc get secret -n "+aimanagerns+" aiops-ir-core-ncodl-api-secret -o jsonpath='{.data.password}' | base64 --decode")
DATALAYER_PWD = stream.read().strip()


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
print ('           🚀 ACTIVE:             '+ACTIVE)
print ('           🔐 DEBUG:              '+DEBUG_ME)
print ('           🕦 POLL_DELAY:         '+str(POLL_DELAY))
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
print ('     🔎 Target Connection Parameters')
print ('    ---------------------------------------------------------------------------------------------')
print ('           🌏 Provider Name:      '+PROVIDER_NAME)
print ('           🌏 Provider URL:       '+PROVIDER_URL)
print ('')
print ('           👩‍💻 Provider User:      '+PROVIDER_USER)
print ('           🔐 Provider Token:     '+PROVIDER_TOKEN)
print ('')
print ('           📥 Minimum Alert Rank: '+str(MIN_RANK))
print ('')
print ('    ---------------------------------------------------------------------------------------------')
print('')
print('')

print ('    ---------------------------------------------------------------------------------------------')
print ('    ---------------------------------------------------------------------------------------------')
print ('    ---------------------------------------------------------------------------------------------')
print ('    ---------------------------------------------------------------------------------------------')
print ('    ---------------------------------------------------------------------------------------------')
print('TEST')
print('')

url = 'https://'+DATALAYER_ROUTE+'/irdatalayer.aiops.io/active/v1/stories'
auth=HTTPBasicAuth(DATALAYER_USER, DATALAYER_PWD)
headers = {'Content-Type': 'application/json', 'Accept-Charset': 'UTF-8', 'x-username' : 'admin', 'x-subscription-id' : 'cfd95b7e-3bc7-4006-a4a8-a73a79c71255'}
print ('📛 Test Connection')
try:
    response = requests.get(url,  headers=headers, auth=auth, verify=False)
except requests.exceptions.RequestException as e:  # This is the correct syntax
    stream = os.popen("oc get route  -n "+aimanagerns+" datalayer-api  -o jsonpath='{.status.ingress[0].host}'")
    print('     ❗ YOU MIGHT WANT TO USE THE DATALAYER PUBLIC ROUTE: '+str(stream.read().strip()))
    raise SystemExit(e)
print ('    ---------------------------------------------------------------------------------------------')
print ('    ---------------------------------------------------------------------------------------------')
print ('    ---------------------------------------------------------------------------------------------')
print ('    ---------------------------------------------------------------------------------------------')




#while True:
# print ('test')
# api_url = "https://jsonplaceholder.typicode.com/todos/1"
# response = requests.get(api_url)
# print(response.json())
# print(response.status_code)

# curl "https://$DATALAYER_ROUTE/irdatalayer.aiops.io/active/v1/stories" --insecure --silent -X GET -u "$USER_PASS" -H "Content-Type: application/json" -H "x-username:admin" -H "x-subscription-id:cfd95b7e-3bc7-4006-a4a8-a73a79c71255"

print ('-------------------------------------------------------------------------------------------------')
print (' 🚀 Initializing Pusher')
print ('-------------------------------------------------------------------------------------------------')






api_url = "https://"+DATALAYER_ROUTE+"/irdatalayer.aiops.io/active/v1/stories"

s = requests.Session()
s.auth=HTTPBasicAuth(DATALAYER_USER, DATALAYER_PWD)
s.headers = {'Content-Type': 'application/json', 'Accept-Charset': 'UTF-8', 'x-username' : 'cpadmin', 'x-subscription-id' : 'cfd95b7e-3bc7-4006-a4a8-a73a79c71255'}

print('     🌏 Running Initial Query')
try:
    response = s.get(api_url, verify=False)
except requests.ConnectionError as e:
   # handle ConnectionError the exception
   print('     ❗ Connection Error')
   print(str(e))

#print(response.json())
print('     ✅ Query Status: '+str(response.status_code))

# headers =  "{'Content-Type':'application/json'; 'x-username':'admin'; 'x-subscription-id':'cfd95b7e-3bc7-4006-a4a8-a73a79c71255' }"
# response = requests.get(api_url, headers=headers, auth=(DATALAYER_USER, DATALAYER_PWD))

#print(response.json())
actStories=response.json()
#print(actStories['stories'])
#print(actStories['stories'][0]['description'])

savedIncidentCount= len(actStories['stories'])

# if DEBUG_ME:
savedIncidentCount=savedIncidentCount-1

print('     🔄 Initial Incident Count:'+str(savedIncidentCount))
print('')
print('')


# ------------------------------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------------------------------
# RUN THIS PUPPY
# ------------------------------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------------------------------

if ACTIVE=="True": 
    print ('-------------------------------------------------------------------------------------------------')
    print (' 🚀 Running Pusher')
    print ('-------------------------------------------------------------------------------------------------')

    treatedStories=[]

    while True:
        debug ('    🔎 treatedStories:'+str(treatedStories))
        debug('     🌏 Running Query')
        s = requests.Session()
        s.auth=HTTPBasicAuth(DATALAYER_USER, DATALAYER_PWD)
        s.headers = {'Content-Type': 'application/json', 'Accept-Charset': 'UTF-8', 'x-username' : 'cpadmin', 'x-subscription-id' : 'cfd95b7e-3bc7-4006-a4a8-a73a79c71255'}

        try:
            response = s.get(api_url, verify=False)
        except requests.ConnectionError as e:
            # handle ConnectionError the exception
            print('     ❗ Connection Error')
            print(str(e))


        #print(response.json())
        debug('     ✅ Query Status: '+str(response.status_code))
        actStories=response.json()


        for currentIncident in actStories['stories']:
            incident_id=currentIncident["id"]
            incidentState=currentIncident["state"]
            lastChangedTime=currentIncident["lastChangedTime"]
            messageHash=hashlib.md5(str(currentIncident).encode()).hexdigest()
            #debug(currentIncident)
            debug('     ✅ Check for: '+incident_id)
            debug('     ✅ Incident State: '+incidentState)
            debug('     ✅ Last Changed: '+lastChangedTime)
            debug('     ✅ Hash: '+messageHash)
            debug('      ')

            if incidentState != 'closed':
                if checkIDExistsDB(conn, incident_id) == 0:
                #if id not in treatedStories:
                        debug('     🛠️ Treating Incident with ID: '+incident_id)
                        treatedStories.append(incident_id)
                        processIncident(currentIncident, DATALAYER_USER, DATALAYER_PWD, DATALAYER_ROUTE, conn, incident_id, messageHash)
                        #closeIncident(conn, incident_id)

                        #debug(currentIncident)
                else:
                    if needsUpdate(conn, incident_id, messageHash) == 1:
                        print('       🟠 NEEDS UPDATE: '+incident_id)
                        provider_id=getMessageIdDB(conn, incident_id)
                        updateIncident(currentIncident, DATALAYER_USER, DATALAYER_PWD, DATALAYER_ROUTE, provider_id)
                    else:
                        debug('       🟢 Already Treated: '+incident_id)
                    
            else:
                if checkIDExistsDB(conn, incident_id) > 0:
                    print('       🔴 Closing Incident: '+incident_id)
                    closeIncident(conn, incident_id, DATALAYER_USER, DATALAYER_PWD, DATALAYER_ROUTE)

        debug ('     🕦 Wait '+str(POLL_DELAY)+' seconds')

        time.sleep(POLL_DELAY)
        debug ('    ---------------------------------------------------------------------------------------------')
else:
    while True:
        print ('-------------------------------------------------------------------------------------------------')
        print (' ❗ Incident Pusher is DISABLED')
        print ('-------------------------------------------------------------------------------------------------')
        time.sleep(15)

print ('')
print ('')
print ('')
print ('-------------------------------------------------------------------------------------------------')
print (' ✅ Pusher is DONE')
print ('-------------------------------------------------------------------------------------------------')
print ('')
print ('')




