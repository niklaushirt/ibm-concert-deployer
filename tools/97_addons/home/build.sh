#!/bin/bash
podman machine start

podman login quay.io -u niklaushirt@gmail.com

export CONT_VERSION=1.1


podman buildx build --platform linux/amd64 -t quay.io/niklaushirt/home-ui:$CONT_VERSION --load -f=Containerfile_small
podman push quay.io/niklaushirt/home-ui:$CONT_VERSION



podman run -p 8080:8000 -e TOKEN=test niklaushirt/home-ui:$CONT_VERSION
