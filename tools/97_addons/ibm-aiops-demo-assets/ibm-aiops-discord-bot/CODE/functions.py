import requests
from requests.auth import HTTPBasicAuth
import json
import datetime
import random
import os
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
os.environ['PYTHONWARNINGS']="ignore:Unverified HTTPS request"

INSTANCE_NAME=os.environ.get('INSTANCE_NAME')
if INSTANCE_NAME == None:
    INSTANCE_NAME="IBMAIOPS"




# ----------------------------------------------------------------------------------------------------------------------------------------------------
# GET Incidents
# ----------------------------------------------------------------------------------------------------------------------------------------------------
 
def getIncidents(DATALAYER_ROUTE,DATALAYER_USER,DATALAYER_PWD, CPD_ROUTE):


    url = 'https://'+DATALAYER_ROUTE+'/irdatalayer.aiops.io/active/v1/stories'
    auth=HTTPBasicAuth(DATALAYER_USER, DATALAYER_PWD)
    headers = {'Content-Type': 'application/json', 'Accept-Charset': 'UTF-8', 'x-username' : 'admin', 'x-subscription-id' : 'cfd95b7e-3bc7-4006-a4a8-a73a79c71255'}
    #response = requests.get(url, headers=headers, verify=False)
    try:
        response = requests.get(url, headers=headers, auth=auth, verify=False)
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        print('     ❗ There was a hiccup')
        #raise SystemExit(e)
    actIncidents=response.json()
    #print ('    🟣🟣🟣🟣🟣 Incidents:'+str(response.content))
    return actIncidents





# ----------------------------------------------------------------------------------------------------------------------------------------------------
# CLOSE ALERTS AND Incidents
# ----------------------------------------------------------------------------------------------------------------------------------------------------
#open
#clear
#closed
def updateAlerts(DATALAYER_ROUTE,DATALAYER_USER,DATALAYER_PWD, STATE):
    #print('              ')
    #print('               ------------------------------------------------------------------------------------------------')
    #print('               📛 Close Alerts')
    data = '{"state": "'+STATE+'"}'
    # print(data)
    # print(type(data))
    url = 'https://'+DATALAYER_ROUTE+'/irdatalayer.aiops.io/active/v1/alerts'
    auth=HTTPBasicAuth(DATALAYER_USER, DATALAYER_PWD)
    headers = {'Content-Type': 'application/json', 'Accept-Charset': 'UTF-8', 'x-username' : 'admin', 'x-subscription-id' : 'cfd95b7e-3bc7-4006-a4a8-a73a79c71255'}
    try:
        response = requests.patch(url, data=data, headers=headers, auth=auth, verify=False)
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        print('     ❗ There was a hiccup')
        raise SystemExit(e)
    #print('                   RESULT:'+str(response.content))
    #print('               ✅ Close Alerts')
    #print('               ------------------------------------------------------------------------------------------------')

    return 'OK'

#resolved
#assignedToIndividual
#inProgress
#resolved
#closed
def updateIncidentsID(DATALAYER_ROUTE,DATALAYER_USER,DATALAYER_PWD, STATE, incident_id):
    #print('              ')
    #print('               ------------------------------------------------------------------------------------------------')
    #print('               📛 Close Incidents')
    data = '{"state": "'+STATE+'"}'
    # print(data)
    # print(type(data))

    url = 'https://'+DATALAYER_ROUTE+'/irdatalayer.aiops.io/active/v1/incidents/'+incident_id
    auth=HTTPBasicAuth(DATALAYER_USER, DATALAYER_PWD)
    headers = {'Content-Type': 'application/json', 'Accept-Charset': 'UTF-8', 'x-username' : 'admin', 'x-subscription-id' : 'cfd95b7e-3bc7-4006-a4a8-a73a79c71255'}
    try:
        response = requests.patch(url, data=data, headers=headers, auth=auth, verify=False)
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        print('     ❗ There was a hiccup')
        raise SystemExit(e)
    print('                   RESULT:'+str(response.content))
    print('               ✅ updateIncidentsID')
    print('               ------------------------------------------------------------------------------------------------')

    return 'OK'


#resolved
#assignedToIndividual
#inProgress
#resolved
#closed
def updateIncidents(DATALAYER_ROUTE,DATALAYER_USER,DATALAYER_PWD, STATE):
    #print('              ')
    #print('               ------------------------------------------------------------------------------------------------')
    #print('               📛 Close Incidents')
    data = '{"state": "'+STATE+'"}'
    # print(data)
    # print(type(data))

    url = 'https://'+DATALAYER_ROUTE+'/irdatalayer.aiops.io/active/v1/stories'
    auth=HTTPBasicAuth(DATALAYER_USER, DATALAYER_PWD)
    headers = {'Content-Type': 'application/json', 'Accept-Charset': 'UTF-8', 'x-username' : 'admin', 'x-subscription-id' : 'cfd95b7e-3bc7-4006-a4a8-a73a79c71255'}
    try:
        response = requests.patch(url, data=data, headers=headers, auth=auth, verify=False)
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        print('     ❗ There was a hiccup')
        raise SystemExit(e)
    print('                   RESULT:'+str(response.content))
    print('               ✅ updateIncidents')
    print('               ------------------------------------------------------------------------------------------------')

    return 'OK'

# ----------------------------------------------------------------------------------------------------------------------------------------------------
# INSTANA INCIDENT
# ----------------------------------------------------------------------------------------------------------------------------------------------------
def instanaCreateIncident():
    stream = os.popen('oc set env deployment ratings -n robot-shop PDO_URL="mysql:host=mysql;dbname=ratings-dev;charset=utf8mb4"')
    RESULT = stream.read().strip()
    print(str(RESULT))
    stream = os.popen('oc set env deployment load -n robot-shop ERROR=1')
    RESULT = stream.read().strip()
    print(str(RESULT))


def instanaMitigateIncident():
    stream = os.popen('oc set env deployment ratings -n robot-shop PDO_URL-')
    RESULT = stream.read().strip()
    print(str(RESULT))
    stream = os.popen('oc set env deployment load -n robot-shop ERROR=0')
    RESULT = stream.read().strip()
    print(str(RESULT))









