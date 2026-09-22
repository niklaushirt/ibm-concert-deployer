
INSTALL_POD=$(oc get po -n ibm-installer|grep ibm-aiops-install-training-step2|awk '{print$1}')
oc logs -n ibm-installer -f $INSTALL_POD