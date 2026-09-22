from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse
from django.template import loader
import json
import datetime
import random
import os
import time
from pathlib import Path


DEMO_USER=""
DEMO_PWD=""
TURBO_URL=''
AIOPS_URL=''
CONCERT_URL=''
INSTANA_URL=''


DEMO_PWD=os.environ.get('GLOBAL_PWD')
if DEMO_PWD == None:
    DEMO_PWD="UNDEFINED"


INSTANCE_NAME=os.environ.get('INSTANCE_NAME')
if INSTANCE_NAME == None:
    INSTANCE_NAME="IBMAIOPS"



image_name=INSTANCE_NAME.lower().replace(" ", "_")+".png"
path = Path('./homeapp/static/images/characters/'+image_name)

if path.is_file():
    #print('Custom Image:'+str(path))
    INSTANCE_IMAGE=Path('./static/images/characters/'+image_name)
else:
    INSTANCE_IMAGE="None"



print('     ❓ Getting Details Turbonomic Route')
stream = os.popen('oc get route -n turbonomic nginx -o jsonpath={.spec.host}')
TURBO_URL = stream.read().strip()

print('     ❓ Getting Details Instana Route')
stream = os.popen('oc get route -n instana-core dev-aiops -o jsonpath={.spec.host}')
INSTANA_URL = stream.read().strip()

print('     ❓ Getting Details Concert Route')
stream = os.popen('oc get route -n ibm-concert concert -o jsonpath={.spec.host}')
CONCERT_URL = stream.read().strip()


print('     ❓ Getting Details AIOps Route')
stream = os.popen('oc get route -n ibm-aiops cpd -o jsonpath={.spec.host}')
AIOPS_URL = stream.read().strip()



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
print ('🟣           📥 Instance Image:                 '+str(INSTANCE_IMAGE))



def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")



def home(request):
    template = loader.get_template('home.html')

    context = {
    'INSTANCE_NAME': INSTANCE_NAME,
    'INSTANCE_IMAGE': INSTANCE_IMAGE,
    'DEMO_PWD': DEMO_PWD,
    'TURBO_URL': TURBO_URL,
    'AIOPS_URL': AIOPS_URL,
    'CONCERT_URL': CONCERT_URL,
    'INSTANA_URL': INSTANA_URL,

    'PAGE_TITLE': 'Demo Environments Home',
    'PAGE_NAME': 'home',

    }
    return HttpResponse(template.render(context, request))




