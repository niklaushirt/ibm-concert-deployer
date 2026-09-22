
#import instana
import requests
from requests.auth import HTTPBasicAuth
import json
import datetime
import time
import random
import os
from functions import *
import discord
from discord.ext import commands
from urllib.parse import quote_plus
from threading import Thread
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
os.environ['PYTHONWARNINGS']="ignore:Unverified HTTPS request"

# ('--------------------------------------------------')('--------------------------------------------------')--------------
# GET VARIABLES
# ('--------------------------------------------------')('--------------------------------------------------')--------------

INSTANCE_NAME=os.environ.get('INSTANCE_NAME')
if INSTANCE_NAME == None:
    INSTANCE_NAME="IBMAIOPS"




# READ ENVIRONMENT VARIABLES
DEBUG_ME=os.environ.get('DEBUG_ME',"False")
ACTIVE=os.environ.get('ACTIVE',"False")
DISCORD_BOT_TOKEN=os.environ.get('DISCORD_BOT_TOKEN',"None")
DISCORD_BOT_NAME=INSTANCE_NAME.lower()
DISCORD_BOT_PREFIX=os.environ.get('DISCORD_BOT_PREFIX',"/")
ITERATE_ELEMENT=os.environ.get('ITERATE_ELEMENT')
WEBHOOK_DEBUG=os.environ.get('WEBHOOK_DEBUG')

TOKEN=os.environ.get('TOKEN',"None")


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
print ('    🛰️  Discord Bot')
print ('')
print ('       Provided by:')
print ('        🇨🇭 Niklaus Hirt (nikh@ch.ibm.com)')
print ('')

print ('--------------------------------------------------------------------------------')
print (' 🚀 Warming up')
print ('--------------------------------------------------------------------------------')


# ('--------------------------------------------------')('--------------------------------------------------')--------------
# GET NAMESPACES
# ('--------------------------------------------------')('--------------------------------------------------')--------------
print('     ❓ Getting IBMAIOps Namespace')
stream = os.popen("oc get po -A|grep aiops-orchestrator-controller |awk '{print$1}'")
aimanagerns = stream.read().strip()
print('        ✅ IBMAIOps Namespace:       '+aimanagerns)




# ('--------------------------------------------------')('--------------------------------------------------')--------------
# DEFAULT VALUES
# ('--------------------------------------------------')('--------------------------------------------------')--------------



# ('--------------------------------------------------')('--------------------------------------------------')--------------
# GET CONNECTIONS
# ('--------------------------------------------------')('--------------------------------------------------')--------------
global DATALAYER_ROUTE
global DATALAYER_USER
global DATALAYER_PWD
global api_url

# ('--------------------------------------------------')('--------------------------------------------------')--------------
# GET CONNECTIONS
# ('--------------------------------------------------')('--------------------------------------------------')--------------

print('     ❓ Getting Details Datalayer')
stream = os.popen("oc get route  -n "+aimanagerns+" datalayer-api  -o jsonpath='{.status.ingress[0].host}'")
DATALAYER_ROUTE = stream.read().strip()
stream = os.popen("oc get secret -n "+aimanagerns+" aiops-ir-core-ncodl-api-secret -o jsonpath='{.data.username}' | base64 --decode")
DATALAYER_USER = stream.read().strip()
stream = os.popen("oc get secret -n "+aimanagerns+" aiops-ir-core-ncodl-api-secret -o jsonpath='{.data.password}' | base64 --decode")
DATALAYER_PWD = stream.read().strip()


print('     ❓ Getting Details AIOPS UIs')
stream = os.popen("oc get route  -n "+aimanagerns+" cpd  -o jsonpath='{.status.ingress[0].host}'")
CPD_ROUTE = stream.read().strip()
stream = os.popen("oc get route  -n ibm-aiops-demo-ui ibm-aiops-demo-ui  -o jsonpath='{.status.ingress[0].host}'")
DENO_UI_ROUTE = stream.read().strip()
stream = os.popen("oc get route  -n instana-core dev-aiops -o jsonpath='{.status.ingress[0].host}'")
INSTANA_ROUTE = stream.read().strip()
stream = os.popen("oc get route  -n turbonomic nginx -o jsonpath='{.status.ingress[0].host}'")
TURBO_ROUTE = stream.read().strip()





print ('')
print ('')
print ('')
print ('--------------------------------------------------------------------------------')
print (' 🔎 Parameters')
print ('--------------------------------------------------------------------------------')
print ('')
print ('    --------------------------------------------------------------------------------')
print ('     🔎 Global Parameters')
print ('    --------------------------------------------------------------------------------')
print ('           🔐 DEBUG:                        '+DEBUG_ME)
print ('           🚀 ACTIVE:                       '+ACTIVE)
print ('           🔐 Token:                        '+TOKEN)
print ('           🔐 DISCORD_BOT_TOKEN:            '+DISCORD_BOT_TOKEN)
print ('')
print ('           👩‍💻 BOT NAME:                     '+DISCORD_BOT_NAME)
print ('           👩‍💻 BOT PREFIX:                   '+DISCORD_BOT_PREFIX)
print ('')
print ('')
print ('    --------------------------------------------------------------------------------')
print ('     🔎 IBMAIOps Connection Parameters')
print ('    --------------------------------------------------------------------------------')
print ('           🌏 IBMAIOPS:                     '+CPD_ROUTE)
print ('           🌏 Demo UI:                      '+DENO_UI_ROUTE)
print ('           🌏 Instana:                      '+INSTANA_ROUTE)
print ('           🌏 Turbonomic:                   '+TURBO_ROUTE)
print ('')
print ('')
print ('    --------------------------------------------------------------------------------')
print ('     🔎 IBMAIOps Datalayer Parameters')
print ('    --------------------------------------------------------------------------------')
print ('           🌏 Datalayer Route:              '+DATALAYER_ROUTE)
print ('           👩‍💻 Datalayer User:               '+DATALAYER_USER)
print ('           🔐 Datalayer Pwd:                '+DATALAYER_PWD)
print ('')
print ('')
print ('    --------------------------------------------------------------------------------')
print ('     🔎 Simulation Parameters')
print ('    --------------------------------------------------------------------------------')
print ('           INSTANCE_NAME:                    '+str(INSTANCE_NAME))
print ('')
print ('')
print ('    --------------------------------------------------------------------------------')
print('')
print('')
print ('--------------------------------------------------------------------------------')
print (' 🚀 Initializing Simulator')
print ('--------------------------------------------------------------------------------')



# --------------------------------------------------------------------------------
# --------------------------------------------------------------------------------
# ACTIONS
# --------------------------------------------------------------------------------
# --------------------------------------------------------------------------------

# --------------------------------------------------------------------------------
# INSTANA
# --------------------------------------------------------------------------------
def createIncidentInstana():
    print ('    --------------------------------------------------------------------------------')
    print ('     🚀 Creating - Incident Instana')
    print ('    --------------------------------------------------------------------------------')
    instanaCreateIncident()
    print ('     ✅ DONE"')


def resolveIncidentInstana():
    print ('    --------------------------------------------------------------------------------')
    print ('     🚀 Mitigating - Incident Instana')
    print ('    --------------------------------------------------------------------------------')
    instanaMitigateIncident()
    print ('     ✅ DONE"')


# --------------------------------------------------------------------------------
# AIOPS
# --------------------------------------------------------------------------------
def createIncidentRSMem():
    print ('    --------------------------------------------------------------------------------')
    print ('     🚀 Running Simulator - RobotShop Memory')
    print ('    --------------------------------------------------------------------------------')
    stream = os.popen('oc set env deployment ratings -n robot-shop PDO_URL="mysql:host=mysql;dbname=ratings-dev;charset=utf8mb4"')
    RESULT = stream.read().strip()
    print(str(RESULT))
    stream = os.popen('oc set env deployment load -n robot-shop ERROR=1')
    RESULT = stream.read().strip()
    print(str(RESULT))


    url = 'https://'+DENO_UI_ROUTE+'/injectRESTHeadless?app=robotshop'
    headers = {'Content-Type': 'application/json', 'Accept-Charset': 'UTF-8'}
    try:
        response = requests.get(url, headers=headers, verify=False)
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        print('     ❗ There was a hiccup')
        raise SystemExit(e)

    print('         RESULT:'+str(response.content))
    print ('     ✅ DONE"')



def createIncidentRSFiber():
    print ('    --------------------------------------------------------------------------------')
    print ('     🚀 Running Simulator - RobotShop Fiber cut')
    print ('    --------------------------------------------------------------------------------')
    stream = os.popen('oc set env deployment ratings -n robot-shop PDO_URL="mysql:host=mysql;dbname=ratings-dev;charset=utf8mb4"')
    RESULT = stream.read().strip()
    print(str(RESULT))
    stream = os.popen('oc set env deployment load -n robot-shop ERROR=1')
    RESULT = stream.read().strip()
    print(str(RESULT))


    url = 'https://'+DENO_UI_ROUTE+'/injectRESTHeadless?app=robotshopnet'
    headers = {'Content-Type': 'application/json', 'Accept-Charset': 'UTF-8'}
    try:
        response = requests.get(url, headers=headers, verify=False)
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        print('     ❗ There was a hiccup')
        raise SystemExit(e)

    print('         RESULT:'+str(response.content))
    print ('     ✅ DONE"')



def createIncidentFan():
    print ('    --------------------------------------------------------------------------------')
    print ('     🚀 Running Simulator - ACME Fan')
    print ('    --------------------------------------------------------------------------------')


    url = 'https://'+DENO_UI_ROUTE+'/injectRESTHeadless?app=acme'
    headers = {'Content-Type': 'application/json', 'Accept-Charset': 'UTF-8'}
    try:
        response = requests.get(url, headers=headers, verify=False)
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        print('     ❗ There was a hiccup')
        raise SystemExit(e)
    print('         RESULT:'+str(response.content))
    print ('     ✅ DONE"')


def createIncidentSock():
    print ('    --------------------------------------------------------------------------------')
    print ('     🚀 Running Simulator - SockShop Network')
    print ('    --------------------------------------------------------------------------------')
    stream = os.popen('oc patch service catalogue -n sock-shop --patch "{\\"spec\\": {\\"selector\\": {\\"name\\": \\"catalog-outage\\"}}}"')
    RESULT = stream.read().strip()
    print(str(RESULT))


    url = 'https://'+DENO_UI_ROUTE+'/injectRESTHeadless?app=sockshop'
    headers = {'Content-Type': 'application/json', 'Accept-Charset': 'UTF-8'}
    try:
        response = requests.get(url, headers=headers, verify=False)
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        print('     ❗ There was a hiccup')
        raise SystemExit(e)    
        print('         RESULT:'+str(response.content))
    print ('     ✅ DONE"')


def setInProgressID(incident_id):
    print ('    --------------------------------------------------------------------------------')
    print ('     🚀 Updating Incident')
    print ('    --------------------------------------------------------------------------------')

    print ('         🚀 Updating Incident to "inProgress" - '+incident_id)
    updateIncidentsID(DATALAYER_ROUTE,DATALAYER_USER,DATALAYER_PWD,"inProgress",incident_id)
    print ('     ✅ DONE"')


def setResolvedID(incident_id):
    print ('    --------------------------------------------------------------------------------')
    print ('     🚀 Updating Incident')
    print ('    --------------------------------------------------------------------------------')
    stream = os.popen('oc set env deployment ratings -n robot-shop PDO_URL-')
    RESULT = stream.read().strip()
    print(str(RESULT))
    stream = os.popen('oc set env deployment load -n robot-shop ERROR=0')
    RESULT = stream.read().strip()
    print(str(RESULT))
    stream = os.popen('oc patch service catalogue -n sock-shop --patch "{\\"spec\\": {\\"selector\\": {\\"name\\": \\"catalog\\"}}}"')
    RESULT = stream.read().strip()
    print(str(RESULT))

    print ('         🚀 Updating Incident to "resolved" - '+incident_id)
    updateIncidentsID(DATALAYER_ROUTE,DATALAYER_USER,DATALAYER_PWD,"resolved",incident_id)
    print ('     ✅ DONE"')



def setInProgress():
    print ('    --------------------------------------------------------------------------------')
    print ('     🚀 Updating Incidents')
    print ('    --------------------------------------------------------------------------------')

    print ('         🚀 Updating Incidents to "inProgress"')
    updateIncidents(DATALAYER_ROUTE,DATALAYER_USER,DATALAYER_PWD,"inProgress")
    print ('     ✅ DONE"')



def setResolved():
    print ('    --------------------------------------------------------------------------------')
    print ('     🚀 Updating Incidents')
    print ('    --------------------------------------------------------------------------------')
    stream = os.popen('oc set env deployment ratings -n robot-shop PDO_URL-')
    RESULT = stream.read().strip()
    print(str(RESULT))
    stream = os.popen('oc set env deployment load -n robot-shop ERROR=0')
    RESULT = stream.read().strip()
    print(str(RESULT))

    stream = os.popen('oc patch service catalogue -n sock-shop --patch "{\\"spec\\": {\\"selector\\": {\\"name\\": \\"catalog-outage\\"}}}"')
    RESULT = stream.read().strip()
    print(str(RESULT))


    print ('         🚀 Updating Incidents to "resolved"')
    updateIncidents(DATALAYER_ROUTE,DATALAYER_USER,DATALAYER_PWD,"resolved")
    print ('     ✅ DONE"')
 

    
def setClosed():
    print ('    --------------------------------------------------------------------------------')
    print ('     🚀 Updating Incidents')
    print ('    --------------------------------------------------------------------------------')
    stream = os.popen('oc set env deployment ratings -n robot-shop PDO_URL-')
    RESULT = stream.read().strip()
    print(str(RESULT))
    stream = os.popen('oc set env deployment load -n robot-shop ERROR=0')
    RESULT = stream.read().strip()
    print(str(RESULT))

    print ('     🚀 Updating Incidents and Alerts to "closed"')
    updateAlerts(DATALAYER_ROUTE,DATALAYER_USER,DATALAYER_PWD,"closed")
    updateIncidents(DATALAYER_ROUTE,DATALAYER_USER,DATALAYER_PWD,"closed")
    print ('     ✅ DONE"')





# --------------------------------------------------------------------------------
# --------------------------------------------------------------------------------
# IN BOT
# --------------------------------------------------------------------------------
# --------------------------------------------------------------------------------

class IncidentBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix=commands.when_mentioned_or('/'), intents=intents)



    # --------------------------------------------------------------------------------
    # HANDLE MESSAGES
    # --------------------------------------------------------------------------------
    async def on_message(self, message):
        if message.author.id == self.user.id:
            return

        print ('--------------------------------------------------------------------------------')
        print("🟡🟡 Command received for Bot: "+str(message.content)) 
        

        if message.content.startswith(DISCORD_BOT_PREFIX+'guess'):
            await message.channel.send('Guess a number between 1 and 10.')

        if message.content.startswith(DISCORD_BOT_PREFIX+DISCORD_BOT_NAME):

            print("  ✅ Command is for me, as my name is "+DISCORD_BOT_PREFIX+DISCORD_BOT_NAME) 
            print ('--------------------------------------------------------------------------------')
            print("") 

            myMessage=message.content
            myArguments=myMessage.split()

            # --------------------------------------------------------------------------------
            # EMPTY COMMAND
            if len(myArguments) < 2:
                print("  🚀 Command Detail: ROOT")
                await message.channel.send('--------------------------------------------------')
                await message.channel.send('**🤖 Welcome to the IBM AIOps Discord Bot for the "'+INSTANCE_NAME+'" Environment**')
                await message.channel.send('--------------------------------------------------')
                await message.channel.send('**🚀 Demo Assets**')
                view = AIOPSLink(DENO_UI_ROUTE,'Demo Dashboard')
                await message.channel.send(view=view)
                view = AIOPSLink(CPD_ROUTE,'IBM AIOps')
                await message.channel.send(view=view)
                if INSTANA_ROUTE != '':
                    view = AIOPSLink(INSTANA_ROUTE,'Instana')
                    await message.channel.send(view=view)
                if TURBO_ROUTE != '':
                    view = AIOPSLink(TURBO_ROUTE,'Turbonomic')
                    await message.channel.send(view=view)

                await message.channel.send('--------------------------------------------------')
                await message.channel.send('**🚀 AIOps Incidents**')
                view = IncidentsActions()
                await message.channel.send(view=view)
                view = IncidentCreateActions()
                await message.channel.send(view=view)

                
                await message.channel.send('--------------------------------------------------')
                await message.channel.send('**🚀 Instana Incidents**')
                view = IncidentInstana()
                await message.channel.send(view=view)


                await message.channel.send('--------------------------------------------------')
                await message.channel.send('**🚀 Open Incidents**')
                await message.channel.send('--------------------------------------------------')
                print ('           🌏 Datalayer Route:              '+DATALAYER_ROUTE)
                print ('           👩‍💻 Datalayer User:               '+DATALAYER_USER)
                print ('           🔐 Datalayer Pwd:                '+DATALAYER_PWD)

                actIncidents=getIncidents(DATALAYER_ROUTE,DATALAYER_USER,DATALAYER_PWD, CPD_ROUTE)
                for currentIncident in actIncidents['stories']:
                    outputString=""
                    incident_id=currentIncident["id"]
                    incidentState=currentIncident["state"]
                    if incidentState=="assignedToIndividual":
                        stateString="🔵 Assigned To Individual"
                    elif incidentState=="inProgress":
                        stateString="🟢 In Progress"
                    elif incidentState=="onHold":
                        stateString="🟠 On Hold"
                    elif incidentState=="resolved":
                        stateString="🔴 Resolved"
                    elif incidentState=="closed":
                        stateString="❌ Closed"
                    else:
                        stateString="inProgress"
                    title=currentIncident["title"]
                    priority=currentIncident["priority"]
                    owner=currentIncident["owner"]
                    url='https://'+CPD_ROUTE+'/aiops/cfd95b7e-3bc7-4006-a4a8-a73a79c71255/resolution-hub/incidents/all/'+incident_id+'/overview'
                    #debug(currentIncident)
                    # print('     ✅ Name: '+title)
                    # print('     ✅ priority: '+str(priority))
                    # print('     ✅ owner: '+owner)

                    outputString=outputString+'\n\n📥 **'+title.strip()+'**\n   > Priority: '+str(priority)+'\n   > Owner: '+owner+'\n   > State: '+stateString+'\n\n' 
                    # print('     ✅ Incident: '+outputString)
                    # print('      ')
                    await message.channel.send(outputString)

                    # We create the view and assign it to a variable so we can wait for it later.
                    view = Incident(incident_id,url)
                    await message.channel.send(view=view)

                    view = IncidentActions(incident_id,url)
                    await message.channel.send(view=view)
                    await message.channel.send('--------------------------------------------------')
                await message.channel.send(' \ntype "'+DISCORD_BOT_PREFIX+DISCORD_BOT_NAME+' help" to get a list of all possible commands.')

            else:
                myArgument=myArguments[1]


                # --------------------------------------------------------------------------------
                # BOT COMMANDS
                # --------------------------------------------------------------------------------
                 # COMMAND BUTTONS

                if myArgument == "demo":
                    print("  🚀 Command Detail: demo")
                    await message.channel.send('--------------------------------------------------')
                    await message.channel.send('**🚀 Demo Assets**')
                    view = AIOPSLink(DENO_UI_ROUTE,'Demo Dashboard')
                    await message.channel.send(view=view)
                    await message.channel.send('> Password: '+TOKEN)

                    view = AIOPSLink(CPD_ROUTE,'IBMAIOps')
                    await message.channel.send(view=view)
                    await message.channel.send('> User    : demo')
                    await message.channel.send('> Password: '+TOKEN)

                    view = AIOPSLink(INSTANA_ROUTE,'Instana')
                    await message.channel.send(view=view)
                    await message.channel.send('> User    : admin@instana.local')
                    await message.channel.send('> Password: '+TOKEN)

                    view = AIOPSLink(TURBO_ROUTE,'Turbonomic')
                    await message.channel.send(view=view)
                    await message.channel.send('> User    : administrator')
                    await message.channel.send('> Password: '+TOKEN)

                elif myArgument == "aiops":
                    print("  🚀 Command Detail: aiops")
                    await message.channel.send('--------------------------------------------------')
                    await message.channel.send('**🚀 AIOps Incidents**')
                    view = IncidentsActions()
                    await message.channel.send(view=view)
                    view = IncidentActions()
                    await message.channel.send(view=view)


                elif myArgument == "instana":
                    print("  🚀 Command Detail: instana")
                    await message.channel.send('--------------------------------------------------')
                    await message.channel.send('**🚀 Instana Incidents**')
                    view = IncidentInstana()
                    await message.channel.send(view=view)
    
                
                # CREATE INCIDENT MEMORY LEAK
                elif myArgument == "incident":
                    print("  🚀 Command Detail: incident")
                    await message.channel.send('🚀 '+INSTANCE_NAME+' Simulating RobotShop - Memory Incident')
                    print('    🟠 Create THREADS')
                    threadRun = Thread(target=createIncidentRSMem)
                    print('    🟠 Start THREADS')
                    threadRun.start()
                    await message.channel.send('✅ Simulation is running in the background')


                # --------------------------------------------------------------------------------
                # CREATE INCIDENT MEMORY LEAK
                elif myArgument == "incidentMem":
                    print("  🚀 Command Detail: incidentMem")
                    await message.channel.send('🚀 '+INSTANCE_NAME+' Simulating RobotShop - Memory Incident')
                    print('    🟠 Create THREADS')
                    threadRun = Thread(target=createIncidentRSMem)
                    print('    🟠 Start THREADS')
                    threadRun.start()
                    await message.channel.send('✅ Simulation is running in the background')

                # --------------------------------------------------------------------------------
                # CREATE INCIDENT MEMORY LEAK
                elif myArgument == "incidentNet":
                    print("  🚀 Command Detail: incidentNet")
                    await message.channel.send('🚀 '+INSTANCE_NAME+' Simulating RobotShop - Fiber Cut Incident')
                    print('    🟠 Create THREADS')
                    threadRun = Thread(target=createIncidentRSFiber)
                    print('    🟠 Start THREADS')
                    threadRun.start()
                    await message.channel.send('✅ Simulation is running in the background')


                # --------------------------------------------------------------------------------
                # CREATE INCIDENT FAN FAILURE
                elif myArgument == "incidentSock":
                    print("  🚀 Command Detail: incidentSock")
                    await message.channel.send('🚀 '+INSTANCE_NAME+' Simulating SockShop - Net Incident')
                    print('    🟠 Create THREADS')
                    threadRun = Thread(target=createIncidentSock)
                    print('    🟠 Start THREADS')
                    threadRun.start()
                    await message.channel.send('✅ Simulation is running in the background')


                # --------------------------------------------------------------------------------
                # CREATE INCIDENT FAN FAILURE
                elif myArgument == "incidentFan":
                    print("  🚀 Command Detail: incidentFan")
                    await message.channel.send('🚀 '+INSTANCE_NAME+' Simulating ACME - Fan Incident')
                    print('    🟠 Create THREADS')
                    threadRun = Thread(target=createIncidentFan)
                    print('    🟠 Start THREADS')
                    threadRun.start()
                    await message.channel.send('✅ Simulation is running in the background')


                # --------------------------------------------------------------------------------
                 # SET Incidents TO InProgress
                elif myArgument == "progress":
                    print("  🚀 Command Detail: progress")
                    await message.channel.send('🚀 '+INSTANCE_NAME+' Set Incidents to InProgress')
                    print('    🟠 Create THREADS')
                    threadRun = Thread(target=setInProgress)
                    print('    🟠 Start THREADS')
                    threadRun.start()


                # --------------------------------------------------------------------------------
                 # SET Incidents TO Resolved
                elif myArgument == "resolve":
                    print("  🚀 Command Detail: resolve")
                    await message.channel.send('🚀 '+INSTANCE_NAME+' Set Incidents to Resolved')
                    print('    🟠 Create THREADS')
                    threadRun = Thread(target=setResolved)
                    print('    🟠 Start THREADS')
                    threadRun.start()

                # --------------------------------------------------------------------------------
                 # SET Incidents TO Resolved
                elif myArgument == "close":
                    print("  🚀 Command Detail: close")
                    await message.channel.send('🚀 '+INSTANCE_NAME+' Set Incidents to Resolved')
                    print('    🟠 Create THREADS')
                    threadRun = Thread(target=setResolved)
                    print('    🟠 Start THREADS')
                    threadRun.start()


                # --------------------------------------------------------------------------------
                 # SET Incidents TO Resolved
                elif myArgument == "reset":
                    print("  🚀 Command Detail: reset")
                    await message.channel.send('🚀 '+INSTANCE_NAME+' Reset Demo Environment')
                    print('    🟠 Create THREADS')
                    threadRun = Thread(target=setResolved)
                    print('    🟠 Start THREADS')
                    threadRun.start()
                    await message.channel.send('ℹ️ Give the environment 5 Minutes to clean up')


                # --------------------------------------------------------------------------------
                # WELCOME MESSAGE
                elif (myArgument == "welcome") or (myArgument == "help"):
                    print("  🚀 Command Detail: "+myArgument)
                    await message.channel.send('**🚀 Available Commands**')
                    await message.channel.send('   🛠️ Demo Assets:')
                    await message.channel.send('      '+DISCORD_BOT_PREFIX+DISCORD_BOT_NAME+' **demo**        :  Prints links and logins to demo assets')
                    await message.channel.send('   🛠️ Command Buttons:')
                    await message.channel.send('      '+DISCORD_BOT_PREFIX+DISCORD_BOT_NAME+' **aiops**      :  Prints buttons to create or mitigate AIOPS incidents')
                    await message.channel.send('      '+DISCORD_BOT_PREFIX+DISCORD_BOT_NAME+' **instana**     :  Prints buttons to create or mitigate Instana incidents')
                    await message.channel.send('   🛠️ Incidents:')
                    await message.channel.send('      '+DISCORD_BOT_PREFIX+DISCORD_BOT_NAME+' **Incidents**     :  List all Incidents')
                    await message.channel.send('   🛠️ Simulation:')
                    await message.channel.send('      '+DISCORD_BOT_PREFIX+DISCORD_BOT_NAME+' **incident**     :  Simulates a Memory Problem in RobotShop')
                    await message.channel.send('      '+DISCORD_BOT_PREFIX+DISCORD_BOT_NAME+' **incidentMem**  :  Simulates a Memory Problem in RobotShop')
                    await message.channel.send('      '+DISCORD_BOT_PREFIX+DISCORD_BOT_NAME+' **incidentNet**  :  Simulates a Fiber Cut in RobotShop')
                    await message.channel.send('      '+DISCORD_BOT_PREFIX+DISCORD_BOT_NAME+' **incidentSock** :  Simulates a Netowrk Problem in SockShop')
                    await message.channel.send('      '+DISCORD_BOT_PREFIX+DISCORD_BOT_NAME+' **incidentFan**  :  Simulates a Fan problem in ACME')
                    await message.channel.send('   🛠️ Modify Incidents:')
                    await message.channel.send('      '+DISCORD_BOT_PREFIX+DISCORD_BOT_NAME+' **progress**    :  Set all Incidents to InProgress')
                    await message.channel.send('      '+DISCORD_BOT_PREFIX+DISCORD_BOT_NAME+' **resolve **    :  Set all Incidents to Resolved')
                    await message.channel.send('      '+DISCORD_BOT_PREFIX+DISCORD_BOT_NAME+' **close**       :  Set all Incidents to Resolved')
                    await message.channel.send('      '+DISCORD_BOT_PREFIX+DISCORD_BOT_NAME+' **reset**       :  Set all Incidents to Resolved')




                # --------------------------------------------------------------------------------
                # GET Incidents
                elif myArgument == "incidents":
                    print("  🚀 Command Detail: Incidents")
                    await message.channel.send('**🚀 '+INSTANCE_NAME+' Open Incidents**')
                    await message.channel.send('--------------------------------------------------')
                    print ('           🌏 Datalayer Route:              '+DATALAYER_ROUTE)
                    print ('           👩‍💻 Datalayer User:               '+DATALAYER_USER)
                    print ('           🔐 Datalayer Pwd:                '+DATALAYER_PWD)

                    actIncidents=getIncidents(DATALAYER_ROUTE,DATALAYER_USER,DATALAYER_PWD, CPD_ROUTE)
                    for currentIncident in actIncidents['stories']:
                        outputString=""
                        incident_id=currentIncident["id"]
                        incidentState=currentIncident["state"]
                        if incidentState=="assignedToIndividual":
                            stateString="🔵 Assigned To Individual"
                        elif incidentState=="inProgress":
                            stateString="🟢 In Progress"
                        elif incidentState=="onHold":
                            stateString="🟠 On Hold"
                        elif incidentState=="resolved":
                            stateString="🔴 Resolved"
                        elif incidentState=="closed":
                            stateString="❌ Closed"
                        else:
                            stateString="inProgress"
                        title=currentIncident["title"]
                        priority=currentIncident["priority"]
                        owner=currentIncident["owner"]
                        url='https://'+CPD_ROUTE+'/aiops/cfd95b7e-3bc7-4006-a4a8-a73a79c71255/resolution-hub/incidents/all/'+incident_id+'/overview'
                        #debug(currentIncident)
                        # print('     ✅ Name: '+title)
                        # print('     ✅ priority: '+str(priority))
                        # print('     ✅ owner: '+owner)

                        outputString=outputString+'\n\n📥 **'+title.strip()+'**\n   > Priority: '+str(priority)+'\n   > Owner: '+owner+'\n   > State: '+stateString+'\n\n' 
                        # print('     ✅ Incident: '+outputString)
                        # print('      ')
                        await message.channel.send(outputString)

                        # We create the view and assign it to a variable so we can wait for it later.
                        view = Incident(incident_id,url)
                        await message.channel.send(view=view)

                        view = IncidentActions(incident_id,url)
                        await message.channel.send(view=view)
                        await message.channel.send('--------------------------------------------------')


                    #await message.channel.send('✅ DONE')





                # --------------------------------------------------------------------------------
                # UNKNOWN COMMAND
                else:
                    print(" ❗Unknown Command")
                    await message.channel.send('🟠 Unknown Command '+myArgument+'. Type "'+DISCORD_BOT_PREFIX+DISCORD_BOT_NAME+' welcome" to get a list of available commands.')
        else:
            print("  📵 Command is not for me. My name is "+DISCORD_BOT_PREFIX+DISCORD_BOT_NAME) 
            print ('--------------------------------------------------------------------------------')
            print("") 
            print("") 



    # --------------------------------------------------------------------------------
    # HANDLE REACTIONS
    # --------------------------------------------------------------------------------
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        """Gives a role based on a reaction emoji."""
        # Make sure that the message the user is reacting to is the one we care about.
        print('A:'+str(payload))
        print('B:'+str(self.fetch_user))






# --------------------------------------------------------------------------------
# --------------------------------------------------------------------------------
# CUSTOM VIEWS
# --------------------------------------------------------------------------------
# --------------------------------------------------------------------------------
class AIOPSLink(discord.ui.View):
    def __init__(self, URL: str, label: str):
        super().__init__()
        # print ("label "+label)
        # print ("URL "+URL)
        self.add_item(discord.ui.Button(label=label, style=discord.ButtonStyle.green, url='https://'+URL))


class Incident(discord.ui.View):
    def __init__(self, incidentID: str, incidentURL: str):
        super().__init__()
        # print ("incidentID"+incidentID)
        # print ("incidentURL"+incidentURL)

        self.add_item(discord.ui.Button(label='Open Incident: ', style=discord.ButtonStyle.green, url=incidentURL))


class IncidentActions(discord.ui.View):
    def __init__(self, incidentID: str, incidentURL: str):
        super().__init__(timeout=None)
        self.currentIncidentID=incidentID
        self.add_buttons(self.currentIncidentID)

    def add_buttons(self,currentIncidentID):
            button_green = discord.ui.Button(label='Acknowledge Incident', style=discord.ButtonStyle.green)
            button_red = discord.ui.Button(label='Resolve Incident', style=discord.ButtonStyle.red)

            async def fbutton_green(interaction: discord.Interaction):
                await interaction.response.send_message('🟠 Acknowledge Incident', ephemeral=True)
                print('AWAIT'+currentIncidentID)
                setInProgressID(currentIncidentID)

            async def fbutton_red(interaction: discord.Interaction):
                print(self.currentIncidentID)
                await interaction.response.send_message('🔴 Resolve Incident', ephemeral=True)
                print('AWAIT'+currentIncidentID)
                setResolvedID(currentIncidentID)

            button_green.callback = fbutton_green
            self.add_item(button_green)
            button_red.callback = fbutton_red
            self.add_item(button_red)


class IncidentsActions(discord.ui.View):
    def __init__(self):
        super().__init__()

    @discord.ui.button(label='Acknowledge all Incidents', style=discord.ButtonStyle.green, custom_id='persistent_view:ackall')
    async def green(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('🟠 Acknowledged all Incidents', ephemeral=True)
        setInProgress()

    @discord.ui.button(label='Resolve all Incidents', style=discord.ButtonStyle.green, custom_id='persistent_view:closeall')
    async def red(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('🔴 Resolved all Incidents', ephemeral=True)
        setResolved()


class IncidentCreateActions(discord.ui.View):
    def __init__(self):
        super().__init__()

    @discord.ui.button(label='RobotShop - Memory Problem', style=discord.ButtonStyle.red, custom_id='persistent_view:rsmem')
    async def green(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('🚀 Simulating RobotShop - Memory Incident', ephemeral=True)
        print('    🟠 Create THREADS')
        threadRun = Thread(target=createIncidentRSMem)
        print('    🟠 Start THREADS')
        threadRun.start()

    @discord.ui.button(label='RobotShop - Fiber Cut', style=discord.ButtonStyle.red, custom_id='persistent_view:rsnet')
    async def blue(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('🚀 Simulating RobotShop - Fiber Cut Incident', ephemeral=True)
        print('    🟠 Create THREADS')
        threadRun = Thread(target=createIncidentRSFiber)
        print('    🟠 Start THREADS')
        threadRun.start()


    @discord.ui.button(label='SockShop - Network Failure', style=discord.ButtonStyle.red, custom_id='persistent_view:sonet')
    async def orange(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('🚀 Simulating SockShop - Network Incident', ephemeral=True)
        print('    🟠 Create THREADS')
        threadRun = Thread(target=createIncidentSock)
        print('    🟠 Start THREADS')
        threadRun.start()


    @discord.ui.button(label='ACME - Fan Failure', style=discord.ButtonStyle.red, custom_id='persistent_view:acfan')
    async def red(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('🚀 Simulating ACME - Fan Incident', ephemeral=True)
        print('    🟠 Create THREADS')
        threadRun = Thread(target=createIncidentFan)
        print('    🟠 Start THREADS')
        threadRun.start()


class IncidentInstana(discord.ui.View):
    def __init__(self):
        super().__init__()

    @discord.ui.button(label='Resolve Incident - Instana', style=discord.ButtonStyle.green, custom_id='persistent_view:instr')
    async def green(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('🚀 Mitigating Incident - Instana', ephemeral=True)
        print('    🟠 Create THREADS')
        threadRun = Thread(target=resolveIncidentInstana)
        print('    🟠 Start THREADS')
        threadRun.start()


    @discord.ui.button(label='Create Incident - Instana', style=discord.ButtonStyle.red, custom_id='persistent_view:instc')
    async def red(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('🚀 Simulating Incident - Instana', ephemeral=True)
        print('    🟠 Create THREADS')
        threadRun = Thread(target=createIncidentInstana)
        print('    🟠 Start THREADS')
        threadRun.start()



# --------------------------------------------------------------------------------
# --------------------------------------------------------------------------------
# RUN THIS PUPPY
# --------------------------------------------------------------------------------
# --------------------------------------------------------------------------------
bot = IncidentBot()


if ACTIVE=="True": 
    if DISCORD_BOT_TOKEN=="CHANGEME": 
        print ('--------------------------------------------------------------------------------')
        print (' ❗ Bot Token not defined!!!')
        print ('--------------------------------------------------------------------------------')
    else:
        bot.run(DISCORD_BOT_TOKEN)
else:
    while True:
        print ('--------------------------------------------------------------------------------')
        print (' ❗ Bot is DISABLED')
        print ('--------------------------------------------------------------------------------')
        time.sleep(15)


print ('')
print ('')
print ('')
print ('--------------------------------------------------------------------------------')
print (' ✅ Bot is DONE')
print ('--------------------------------------------------------------------------------')
print ('')
print ('')




