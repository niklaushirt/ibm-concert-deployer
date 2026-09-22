export DOCKER_USER=your_docker_username
export DOCKER_PWD=your_docker_password

oc get secret/pull-secret -n openshift-config -oyaml > pull-secret-backup.yaml
oc get secret/pull-secret -n openshift-config --template='{{index .data ".dockerconfigjson" | base64decode}}' > temp-pull-secret.yaml
oc registry login --registry="docker.io" --auth-basic="$DOCKER_USER:$DOCKER_PWD" --to=temp-pull-secret.yaml
oc set data secret/pull-secret -n openshift-config --from-file=.dockerconfigjson=temp-pull-secret.yaml
