#!/bin/bash
set -ex

IMAGE=$(basename $(dirname $(realpath $0)))

docker run -it --rm --name cscg_${IMAGE} \
    -p 8000:8000 \
    cscg/${IMAGE}
