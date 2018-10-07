#!/bin/bash

set -ex

# enable IP forwarding
sysctl -w net.ipv4.ip_forward=1

# configure firewall
iptables -t nat -A POSTROUTING -s 10.62.0.0/24 ! -d 10.62.0.0/24 -j MASQUERADE
iptables -A FORWARD -s 10.62.0.0/24 -p tcp -m tcp --tcp-flags FIN,SYN,RST,ACK SYN -j TCPMSS --set-mss 1356

# redirect net.tsinghua.edu.cn
netredirect=$(nslookup netredirect | awk -F': ' 'NR==6 {print $2}')
iptables -t nat -A PREROUTING -d net.tsinghua.edu.cn -j DNAT --to ${netredirect}

exec "$@"
