#!/bin/bash
set -ex

IMAGE=$(basename $(dirname $(realpath "$0")))

docker run -it --rm --name cscg_${IMAGE} -p 1194:1194/udp --privileged cscg/${IMAGE}
