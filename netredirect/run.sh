#!/bin/bash
set -ex

IMAGE=$(basename $(dirname $(realpath "$0")))

docker run -it --rm --name cscg_${IMAGE} \
    -v cgservice_letsencrypt:/etc/letsencrypt \
    -p 80:80 \
    -p 443:443 \
    cscg/${IMAGE}
