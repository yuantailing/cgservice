#!/bin/bash
set -ex

mkdir -p /var/run/vsftpd/empty

exec "$@"
