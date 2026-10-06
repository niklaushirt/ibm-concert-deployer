from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.http import JsonResponse
from django.template import loader
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_http_methods, require_POST
import os
import sys 
import time 
from threading import Thread
sys.path.append(os.path.abspath("demouiapp"))
from functions import *
from utils.commands import capture_shell, run_shell
from .authentication import (
    clear_authenticated_session,
    credentials_match,
    establish_authenticated_session,
    is_authenticated,
    is_login_rate_limited,
    register_login_failure,
    reset_login_failures,
)
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



# Authentication is enforced per request by TokenAuthenticationMiddleware.
# This value is now only a legacy template display flag for protected pages.
loggedin='true'



hasCustomScenario= str(len(CUSTOM_EVENTS)+len(CUSTOM_METRICS)+len(CUSTOM_LOGS)+len(CUSTOM_TOPOLOGY)-1)
hasCustomTopology= str(len(CUSTOM_TOPOLOGY_TAG)+len(CUSTOM_TOPOLOGY_APP_NAME)+len(CUSTOM_TOPOLOGY))





# ----------------------------------------------------------------------------------------------------------------------------------------------------
# GET NAMESPACES
# ----------------------------------------------------------------------------------------------------------------------------------------------------
print('     ❓ Getting Concert platform Namespace')
stream = capture_shell("oc get po -A|grep roja-ui |awk '{print$1}'")
platformns = stream.read().strip()
print('        ✅ Concert platform Namespace:       '+platformns)


print('     ❓ Getting Concert platform Hub Namespace')
stream = capture_shell("oc get po -A|grep ibm-solis-core |awk '{print$1}'")
platformhubns = stream.read().strip()
print('        ✅ Concert platform Hub Namespace:       '+platformhubns)



print ('')
print ('     🌏 PUBLIC ROUTES')



ENV_CMD=str(os.environ.get('ENV_CMD', default=''))



WATSON_CMD = '''
CONCERT_NAMESPACE=$(oc get po -A|grep roja-portal |awk '{print$1}')
API_KEY="$(oc get secret app-cfg-secret -n $CONCERT_NAMESPACE -o jsonpath='{ .data.WATSONX_API_KEY }' | base64 --decode)"
RESPONSE=$(curl -s -X POST https://iam.cloud.ibm.com/identity/token -H "Content-Type: application/x-www-form-urlencoded" -d "grant_type=urn:ibm:params:oauth:grant-type:apikey&apikey=$API_KEY")

#echo "$RESPONSE" | jq

if echo "$RESPONSE" | jq -e '.errorMessage' > /dev/null 2>&1; then
echo "0"
else
echo "1"
fi
'''


print('     ❓ Getting WATSON Configured')
stream = capture_shell(WATSON_CMD)
WATSON_OK = bool(int(stream.read().strip()))

print ('        ✅ WATSON_OK:       '+str(WATSON_OK))




print('     ❓ Getting System Info - this may take a minute or two')
stream = capture_shell(ENV_CMD)
ALL_LOGINS = stream.read().strip()

#print ('        ✅ ALL LOGINS:       '+ALL_LOGINS)


# ----------------------------------------------------------------------------------------------------------------------------------------------------
# GET CONNECTION DETAILS
# ----------------------------------------------------------------------------------------------------------------------------------------------------
print('     ❓ Getting Details IBM Concert Platform')
stream = capture_shell('oc get route -n '+platformns+' concert -o jsonpath={.spec.host}')
concertplatform_url = stream.read().strip()


# KEYCLOAK
print('     ❓ Getting Details Keycloak ')
stream = capture_shell("oc exec -it $(kubectl get pods -n "+platformhubns+"  | grep ibm-solis-embedded-keycloak | awk '{print $1}') -n "+platformhubns+"  -- env | grep 'KC_BOOTSTRAP_ADMIN_USERNAME='| cut -d= -f2")
keycloak_user = stream.read().strip()

stream = capture_shell("oc exec -it $(kubectl get pods -n "+platformhubns+"  | grep ibm-solis-embedded-keycloak | awk '{print $1}') -n "+platformhubns+"  -- env | grep 'KC_BOOTSTRAP_ADMIN_PASSWORD='| cut -d= -f2")
keycloak_pwd = stream.read().strip()

stream = capture_shell("oc get route solis-hub -o jsonpath={.spec.host} -n "+platformhubns)
keycloak_url = stream.read().strip()+"/sys/internal/kc"


print('     ❓ Getting Details LDAP ')
stream = capture_shell('oc get route -n openldap admin -o jsonpath={.spec.host}')
ladp_url = stream.read().strip()
ladp_user = 'cn=admin,dc=ibm,dc=com'
ladp_pwd = os.environ.get('DEMO_PWD')






print('     ❓ Getting Details ELK ')
stream = capture_shell('oc get route -n openshift-logging kibana -o jsonpath={.spec.host}')
elk_url = stream.read().strip()

print('     ❓ Getting Details Turbonomic Dashboard')
stream = capture_shell('oc get route -n ibm-concert-optimise nginx -o jsonpath={.spec.host}')
turbonomic_url = stream.read().strip()

print('     ❓ Getting Details Instana Dashboard')
stream = capture_shell('oc get route -n instana-core dev-aiops -o jsonpath={.spec.host}')
instana_url = stream.read().strip()


print('     ❓ Getting Details Openshift Console')
stream = capture_shell('oc get route -n openshift-console console -o jsonpath={.spec.host}')
openshift_server = stream.read().strip()
openshift_url = 'https://'+openshift_server.replace("console-openshift-console.apps", "api")+':6443'
stream = capture_shell("oc create token -n default demo-admin-concert --duration=999999999s")
openshift_token = stream.read().strip()

# stream = capture_shell("oc config view --minify|grep 'server:'| sed 's/.*server: .*\///'| head -1")
# #stream = capture_shell("oc status|head -1|awk '{print$6}'")
# openshift_server = stream.read().strip()
stream = capture_shell("oc get deployment -n ibm-demo-ui ibm-demo-ui -ojson|jq -r '.spec.template.spec.containers[0].image'")
demo_image = stream.read().strip()



print('     ❓ Getting Details RobotShop')
stream = capture_shell('oc get routes -n robot-shop robotshop  -o jsonpath={.spec.host}')
robotshop_url = stream.read().strip()
robotshop_url=os.environ.get('ROBOTSHOP_URL_OVERRIDE', default=robotshop_url)
#print ('🟣🟣🟣🟣🟣🟣🟣🟣'+str(os.environ.get('ROBOTSHOP_URL_OVERRIDE')))


print('     ❓ Getting Details SockShop')
stream = capture_shell('oc get routes -n sock-shop front-end  -o jsonpath={.spec.host}')
sockshop_url = stream.read().strip()
sockshop_url=os.environ.get('SOCKSHOP_URL_OVERRIDE', default=sockshop_url)


print('     ❓ Getting Details Galaxium Travels')
stream = capture_shell('oc get routes -n galaxium-travels galaxium  -o jsonpath={.spec.host}')
galaxium_travels_url = stream.read().strip()
galaxium_travels_url=os.environ.get('GALAXIUM_TRAVELS_URL_OVERRIDE', default=galaxium_travels_url)
#print ('🟣🟣🟣🟣🟣🟣🟣🟣'+str(os.environ.get('GALAXIUM_TRAVELS_URL_OVERRIDE')))




# ----------------------------------------------------------------------------------------------------------------------------------------------------
# GET ENVIRONMENT VALUES
# ----------------------------------------------------------------------------------------------------------------------------------------------------
TOKEN=os.environ.get('TOKEN')
ADMIN_MODE=os.environ.get('ADMIN_MODE')
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
print ('🟣           🔐 Login Token:                    configured')
print ('🟣')   
print ('🟣           🟠 Admin Mode:                     '+ADMIN_MODE)
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
print ('🟣')
print ('🟣')
print ('🟣    ---------------------------------------------------------------------------------------------')
print ('🟣     🔎 System Parameters')
print ('🟣    ---------------------------------------------------------------------------------------------')
print ('🟣')   
print ('🟣           🌏 OCP Route:                      '+openshift_url)
print ('🟣           🌏 OCP Server:                     '+openshift_server)
print ('🟣           🔐 OCP Token:                      '+openshift_token[:25]+'...')
print ('🟣')   
print ('🟣')
print ('🟣    ---------------------------------------------------------------------------------------------')
print ('🟣     🌏 Keycloak')
print ('🟣    ---------------------------------------------------------------------------------------------')
print ('🟣           🌏 Keycloak User:                  '+keycloak_user)
print ('🟣           🌏 Keycloak Password:              '+keycloak_pwd)
print ('🟣           🌏 Keycloak URL:                   '+keycloak_url)
print ('🟣')   
print ('🟣    ---------------------------------------------------------------------------------------------')
print ('🟣     🌏 URLs')
print ('🟣    ---------------------------------------------------------------------------------------------')
print ('🟣           🌏 RobotShop URL:                  '+robotshop_url)
print ('🟣           🌏 SockShop URL:                   '+sockshop_url)
print ('🟣           🌏 Galaxium Travels URL:           '+galaxium_travels_url)
print ('🟣           🌏 Concert Platform URL:           '+concertplatform_url)
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
        'loggedin': 'true',
        'DEMO_USER': DEMO_USER,
        'DEMO_PWD': DEMO_PWD,
        'elk_url': elk_url,
        'turbonomic_url': turbonomic_url,
        'instana_url': instana_url,
        'openshift_url': openshift_url,
        'openshift_token': openshift_token,
        'openshift_server': openshift_server,
        'ladp_url': ladp_url,
        'ladp_user': ladp_user,
        'ladp_pwd': ladp_pwd,
        'robotshop_url': robotshop_url,
        'sockshop_url': sockshop_url,
        'galaxium_travels_url': galaxium_travels_url,
        'INSTANCE_NAME': INSTANCE_NAME,
        'INSTANCE_IMAGE': INSTANCE_IMAGE,
        'ADMIN_MODE': ADMIN_MODE,
        'hasCustomScenario': int(hasCustomScenario),
        'CUSTOM_NAME': CUSTOM_NAME,
        'INCIDENT_ACTIVE': INCIDENT_ACTIVE,
        'ROBOT_SHOP_OUTAGE_ACTIVE': ROBOT_SHOP_OUTAGE_ACTIVE,
        'SOCK_SHOP_OUTAGE_ACTIVE': SOCK_SHOP_OUTAGE_ACTIVE,
        'PAGE_TITLE': page_title,
        'PAGE_NAME': page_name,
        'platformns': platformns,
        'concertplatform_url': concertplatform_url,
        'keycloak_user': keycloak_user,
        'keycloak_pwd': keycloak_pwd,
        'keycloak_url': keycloak_url,
        'WATSON_OK': WATSON_OK,
        'ALL_LOGINS': ALL_LOGINS,




    }




@never_cache
@require_http_methods(["GET", "POST"])
def login(request):
    if request.method == "GET":
        if is_authenticated(request):
            return redirect("index")
        return render(request, "demouiapp/loginui.html", {
            "loggedin": "false",
            "INSTANCE_NAME": INSTANCE_NAME,
            "INSTANCE_IMAGE": INSTANCE_IMAGE,
        })

    context = {
        "loggedin": "false",
        "INSTANCE_NAME": INSTANCE_NAME,
        "INSTANCE_IMAGE": INSTANCE_IMAGE,
    }

    if is_login_rate_limited(request):
        context["login_error"] = "Too many failed attempts. Please wait a few minutes and try again."
        return render(request, "demouiapp/loginui.html", context, status=429)

    if credentials_match(request.POST.get("token", "")):
        reset_login_failures(request)
        establish_authenticated_session(request)
        return redirect("index")

    register_login_failure(request)
    context["login_error"] = "The access password is not valid."
    return render(request, "demouiapp/loginui.html", context, status=401)


@never_cache
@require_POST
def logout(request):
    clear_authenticated_session(request)
    return redirect("login")


def verifyLogin(request):
    return is_authenticated(request)





# ----------------------------------------------------------------------------------------------------------------------------------------------------
# PAGE ENDPOINTS
# ----------------------------------------------------------------------------------------------------------------------------------------------------

def loginui(request):
    return redirect("login")


def index(request):
    print('🌏 index')
    global loggedin, INCIDENT_ACTIVE, ROBOT_SHOP_OUTAGE_ACTIVE, SOCK_SHOP_OUTAGE_ACTIVE
    print('     🟣 OUTAGE - Incident:'+str(INCIDENT_ACTIVE)+' - RS-OUTAGE:'+str(ROBOT_SHOP_OUTAGE_ACTIVE)+' - SOCK-OUTAGE:'+str(SOCK_SHOP_OUTAGE_ACTIVE))

    verifyLogin(request)

    if loggedin=='true':
        template = loader.get_template('demouiapp/home.html')

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
    return HttpResponse(template.render(get_base_context(page_title='IBM Concert platform Demo UI', page_name='doc'), request))


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
    context = get_base_context(page_title='Configuration for the IBM Concert platform Training', page_name='config')
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
