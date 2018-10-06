#!/bin/bash
set -ex

IMAGE=$(basename $(dirname $(realpath $0)))

docker run -it --rm --name cscg_${IMAGE} -p 1723:1723 --privileged cscg/${IMAGE}
