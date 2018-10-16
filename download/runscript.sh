#!/bin/bash

set -ex

mkdir -p /mnt/download/mysite
mkdir -p /mnt/download/log

# reject net.tsinghua.edu.cn
iptables -A OUTPUT -d 166.111.204.120 -j REJECT
iptables -A OUTPUT -d 101.6.4.100 -j REJECT

service apache2 start
python3 update.py &
aria2c --conf-path /srv/aria/aria2.conf &
python3 manage.py runserver
