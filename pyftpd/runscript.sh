#!/bin/bash

set -ex

if [ -n "${SSL_ENABLE}" ]; then
    mkdir -p ~ftp/certs
    cp $(realpath /etc/letsencrypt/live/cgservice/fullchain.pem) ~ftp/certs/fullchain.pem
    cp $(realpath /etc/letsencrypt/live/cgservice/privkey.pem) ~ftp/certs/privkey.pem
    chown ftp:ftp ~ftp/certs/{fullchain,privkey}.pem
fi

chown ftp:ftp /opt/ftp/settings.py

su ftp -c "python3 /opt/ftp/main.py"
