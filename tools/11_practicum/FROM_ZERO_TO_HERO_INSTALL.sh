cat << EOF | oc apply -f -
apiVersion: v1                     
kind: Namespace
metadata:
  name: ibm-installer
---
kind: ServiceAccount
apiVersion: v1
metadata:
  name: ibm-installer-admin
  namespace: ibm-installer
---
kind: ClusterRoleBinding
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: ibm-installer-admin
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: cluster-admin
subjects:
  - kind: ServiceAccount
    name: ibm-installer-admin
    namespace: ibm-installer
---
kind: ClusterRoleBinding
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: ibm-installer-default-admin
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: cluster-admin
subjects:
  - kind: ServiceAccount
    name: default
    namespace: ibm-installer
---
apiVersion: batch/v1
kind: Job
metadata:
  name: aiops-easy-install-aimanager-practicum
  namespace: ibm-installer
  labels:
   aiops-type: data-load-job
spec:
  serviceAccount: ibm-installer-admin
  template:
    spec:
      containers:
        - name: install
          image: quay.io/niklaushirt/ibm-aiops-tools:5.1.0
          imagePullPolicy: IfNotPresent
          resources:
            requests:
              memory: "64Mi"
              cpu: "150m"
            limits:
              memory: "2024Mi"
              cpu: "1200m"
          command:
            - /bin/sh
            - -c
            - |
              #!/bin/bash
              #set -x

              echo "*****************************************************************************************************************************"
              echo " ✅ STARTING: INSTALL IBMAIOps with Demo Content"
              echo "*****************************************************************************************************************************"
              echo ""
              echo ""
              echo "------------------------------------------------------------------------------------------------------------------------------"
              echo " 📥 Clone Repo https://github.com/niklaushirt/ibm-aiops-deployer.git"
              git clone https://github.com/niklaushirt/ibm-aiops-deployer.git -b main

              
              cd ibm-aiops-deployer
              echo ""
              echo ""

              echo "------------------------------------------------------------------------------------------------------------------------------"
              echo " 🚀 Prepare Ansible"
              ansible-galaxy collection install community.kubernetes:1.2.1
              ansible-galaxy collection install kubernetes.core:2.2.3
              ansible-galaxy collection install cloud.common
              pip install openshift pyyaml kubernetes 
              echo ""
              echo ""

              echo "------------------------------------------------------------------------------------------------------------------------------"
              echo " 🚀 Starting Installation"
              ansible-playbook ./ansible/ibm-itautomation-products-install.yaml -e "config_file_path=./configs/ibm-aiops-practicum.yaml"
              echo ""
              echo ""
              echo "*****************************************************************************************************************************"
              echo " ✅ DONE"
              echo "*****************************************************************************************************************************"

              while true
              do
                sleep 1000
              done

      restartPolicy: Never
  backoffLimit: 500
EOF