#!/bin/bash
set -ex

IMAGE=$(basename $(dirname $(realpath "$0")))

docker build . -t cscg/${IMAGE}
