#!/bin/bash


podman machine start

podman login quay.io -u niklaushirt@gmail.com


export CONT_VERSION=1.0.0

podman buildx build --platform linux/amd64 -t quay.io/niklaushirt/ibm-concert-tools:$CONT_VERSION --load .
podman push quay.io/niklaushirt/ibm-concert-tools:$CONT_VERSION




podman tag quay.io/niklaushirt/ibm-concert-tools:1.0.0 quay.io/niklaushirt/ibm-concert-tools:1.0.0
podman push quay.io/niklaushirt/ibm-concert-tools:1.0.0
