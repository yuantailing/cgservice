#!/bin/bash
set -ex

IMAGE=$(basename $(dirname $(realpath "$0")))

docker run -it --rm --name cscg_${IMAGE} \
    -v /srv/ftp:/srv/ftp \
    --net=host \
    cscg/${IMAGE}
