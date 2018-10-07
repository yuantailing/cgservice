#!/bin/bash
set -ex

# see https://hub.docker.com/_/httpd/

IMAGE=$(basename $(dirname $(realpath "$0")))

docker run -it --rm --name cscg_${IMAGE} \
    -v /srv/ftp:/srv/ftp \
    -v /etc/letsencrypt:/etc/letsencrypt:ro \
    -p 80:80 \
    -p 443:443 \
    cscg/${IMAGE}
