
INSTALL_POD=$(oc get po -n ibm-installer|grep install|awk '{print$1}')
oc logs -n ibm-installer -f $INSTALL_POD