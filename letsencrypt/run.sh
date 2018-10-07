#!/bin/bash
set -ex

IMAGE=$(basename $(dirname $(realpath $0)))

docker run -it --rm --name cscg_${IMAGE} \
    --env-file sites.env \
    -v /srv/ftp:/srv/ftp \
    -v cgservice_letsencrypt:/etc/letsencrypt \
    cscg/${IMAGE}
