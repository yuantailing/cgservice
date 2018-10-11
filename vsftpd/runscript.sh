#!/bin/bash

set -ex

if [ -n "${SSL_ENABLE}" ]; then
    sed -i 's/#ssl_enable=YES/ssl_enable=YES/g' /etc/vsftpd.conf
fi

# see https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/5/html/5.6_technical_notes/vsftpd
trap "SIGUSR1 received" SIGUSR1

vsftpd /etc/vsftpd.conf
