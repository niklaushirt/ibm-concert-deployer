#!/bin/bash
podman machine start

podman login quay.io -u niklaushirt@gmail.com

cd tools/97_addons/ibm-demo-ui/demoui


export CONT_VERSION=5.2.0
podman buildx build --platform linux/amd64 -t quay.io/niklaushirt/ibm-demo-ui:$CONT_VERSION --load -f=Containerfile_small
podman push quay.io/niklaushirt/ibm-demo-ui:$CONT_VERSION
