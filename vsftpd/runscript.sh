#!/bin/bash

set -ex

# see https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/5/html/5.6_technical_notes/vsftpd
trap "SIGUSR1 received" SIGUSR1

vsftpd /etc/vsftpd.conf
