#!/bin/bash

set -ex

service vsftpd start || true
#vsftpd /etc/vsftpd.conf

while [ 1 ]; do sleep 1h; done
