#!/bin/bash

set -ex

# configure firewall
iptables -t nat -A POSTROUTING -s 10.62.0.0/24 ! -d 10.62.0.0/24 -j MASQUERADE

# redirect net.tsinghua.edu.cn
netredirect=$(nslookup netredirect | awk -F': ' 'NR==6 {print $2}')
iptables -t nat -A PREROUTING -d 166.111.204.120 -j DNAT --to ${netredirect}
iptables -t nat -A PREROUTING -d 101.6.4.100 -j DNAT --to ${netredirect}

openvpn server.conf
